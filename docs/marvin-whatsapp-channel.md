# Marvin WhatsApp Channel

## Overview

WhatsApp integration for Marvin, located at `/home/rgr/lab/marvin-whatsapp/`. Enables Marvin to communicate via WhatsApp text and voice messages. Three files: `main.go`, `brain.py`, `memory.py`.

## Architecture: Go gateway + file IPC + Python brain

```
WhatsApp Web ←WebSocket→ main.go (Go/whatsmeow) ←JSONL files→ brain.py (Python)
                                                                   ↕
                                                              memory.py (SQLite)
                                                                   ↕
                                                              Milvus + OpenAI
```

## main.go — Go Gateway (354 lines)

**Module:** `github.com/rogersebastiany/marvin-whatsapp` (Go 1.24)

**Dependencies:** whatsmeow (WhatsApp Web multi-device), go-sqlite3 (session store), qrterminal (QR login), protobuf.

**Session management:**
- SQLite-backed session in `session.db` via whatsmeow's `sqlstore`
- First run: generates QR code in terminal for WhatsApp pairing
- Subsequent runs: auto-reconnects with stored session

**Message flow (inbound):**
1. Event handler receives `*events.Message`
2. `atomic.Bool` listening flag gates all processing
3. LID (Linked ID) resolution: converts `lid` server JIDs to phone numbers via `Store.LIDs.GetPNForLID`
4. Audio messages → `saveAudio()` downloads via `client.Download()`, saves as `audio/{from}_{messageID}.ogg`, appends to inbox with `audioPath`
5. Text messages → extracted from `ExtendedTextMessage` or `Conversation`, ALL sent to brain (no filtering in Go — brain.py handles trigger/session logic)

**IPC protocol — inbox.jsonl:**
```json
{"from":"5511999999999","chat":"5511999999999@s.whatsapp.net","text":"hey marvin","timestamp":"2026-04-10T12:00:00-03:00"}
{"from":"5511999999999","chat":"5511999999999@s.whatsapp.net","audioPath":"audio/5511999999999_ABCD1234.ogg","timestamp":"..."}
```

**Message flow (outbound) — `watchOutbox()`:**
- Polls `outbox.jsonl` every 500ms with file offset tracking
- Text: `client.SendMessage()` with `waE2E.Message{Conversation: ...}`
- Audio: `client.Upload()` (MediaAudio) then `SendMessage` with `AudioMessage` struct:
  - `PTT: true` (push-to-talk = voice note bubble, not audio file)
  - Duration detected via `ffprobe -v quiet -show_entries format=duration` (fallback: 5s)
  - Mimetype: `audio/ogg; codecs=opus`
  - Includes FileEncSHA256, FileSHA256, FileLength for WhatsApp verification

**IPC protocol — outbox.jsonl:**
```json
{"to":"5511999999999@s.whatsapp.net","message":"*Marvin:* Hello!"}
{"to":"5511999999999@s.whatsapp.net","audioPath":"audio/reply_abc12345.ogg"}
```

**Recipient parsing:** `parseRecipient()` appends `@s.whatsapp.net` if no `@` present, then `types.ParseJID()`.

**Marvin name variants (Go side):**
`marvin`, `maureen`, `marven`, `marvyn`, `marwin`, `marvel`, `margin`, `martin`, `marcin`, `marvim`

## brain.py — Python Brain (343 lines)

**Startup:** Connects to Milvus, opens SQLite via `get_db()`, seeks to end of `inbox.jsonl` (only processes new messages), polls every 500ms.

**Config (env vars):**
- `OPENAI_API_KEY` — required
- `MILVUS_HOST` / `MILVUS_PORT` — defaults localhost:19530
- Models: `gpt-4o-mini` (LLM), `text-embedding-3-small` (embeddings), `tts-1` (TTS), `onyx` (voice)

**Milvus search — `search_milvus(query, limit=5)`:**
- Embeds query with text-embedding-3-small
- Searches two collections:
  - `concepts`: output_fields = name, vault, summary, content (truncated to 500 chars)
  - `doc_chunks`: output_fields = doc_name, heading, content (truncated to 500 chars)
- Both use COSINE metric, nprobe=16
- Returns formatted context string with `---` separators

**Processing pipeline per message:**
1. Parse JSONL line from inbox
2. If audio: transcribe with Whisper (`whisper-1`)
3. **Session/trigger check:**
   - Marvin name variant found → activate session for this chat
   - No name but active session → `is_still_talking_to_marvin()` GPT classifier checks with last 10 messages as context. If yes → continue. If no → deactivate session, skip.
   - No name and no session → skip
4. `store_message()` — persist incoming message to SQLite
5. `rate_politeness(text)` — GPT rates 0.0–1.0 (temperature=0, max_tokens=5)
6. `update_politeness()` — EMA blend with alpha=0.3
7. `get_chat_history(chat, limit=10)` — last 10 messages for conversation context
8. `politeness_tone()` — map coefficient to tone instruction
9. `search_milvus(text)` — RAG retrieval from shared Milvus
10. Generate reply (with history + tone + knowledge context):
    - **Text in → text out:** `generate_reply()` — max_tokens=1000, temperature=0.7
    - **Audio in → voice out:** `generate_voice_reply()` — max_tokens=300 (shorter for speech), then TTS to `audio/reply_{uuid8}.ogg` (opus format). Sends a `*Marvin:* 🎙️` text first, then the voice note. Falls back to text on TTS error.
11. `store_message()` — persist outgoing message
12. Append to outbox.jsonl

**Text replies** are prefixed with `*Marvin:*` (bold in WhatsApp) to identify the bot since it sends from the user's own account.

**System prompts:**
- Text: "You are Marvin, an AI assistant with deep knowledge in software engineering, system design, and computer science. You reply in the same language the user writes. Keep replies concise and practical — this is WhatsApp, not an essay."
- Voice: Same but adds "This reply will be converted to a voice message, so keep it SHORT and conversational. Max 2-3 sentences. No bullet points, no markdown, no lists."
- Both include: "Never mention that you searched a database or retrieved context."
- Both include: "You have conversation memory — you can see recent messages from this chat and you remember what was discussed. Reference past messages naturally when relevant. Never say you can't access or remember previous messages."
- Tone instruction appended based on politeness coefficient
- Context injected as system message (truncated to 4000 chars)
- History injected as system message formatted as "User: ... / Marvin: ..."
- Strips `@Marvin` / `@marvin` from user text before sending to LLM

**Marvin name variants (Python side, duplicated):**
Same 10 variants as Go side.

## memory.py — SQLite Persistence (90 lines)

**Database:** `marvin_memory.db` with WAL journal mode.

**Schema:**
```sql
CREATE TABLE users (
    phone       TEXT PRIMARY KEY,
    name        TEXT DEFAULT '',
    politeness  REAL DEFAULT 0.5,      -- EMA politeness coefficient
    msg_count   INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT datetime('now'),
    updated_at  TEXT DEFAULT datetime('now')
);

CREATE TABLE messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    phone       TEXT NOT NULL,          -- FK to users
    chat        TEXT NOT NULL,          -- WhatsApp JID (group or 1:1)
    direction   TEXT NOT NULL,          -- 'in' or 'out'
    text        TEXT DEFAULT '',
    audio_path  TEXT DEFAULT '',
    timestamp   TEXT DEFAULT datetime('now')
);
-- Indexes on (chat, timestamp) and (phone, timestamp)
```

**Key functions:**
- `ensure_user(phone)` — upsert, default politeness=0.5
- `store_message(phone, chat, direction, text, audio_path, timestamp)` — insert message + increment msg_count
- `get_chat_history(chat, limit=10)` — last N messages ordered chronologically (SELECT DESC + reverse in Python)
- `update_politeness(phone, score, alpha=0.3)` — `new = 0.3 * score + 0.7 * old`, clamped [0.0, 1.0], rounded to 3 decimals

## Politeness Coefficient

Each incoming text is rated by GPT-4o-mini:
- System prompt: "Rate the politeness of this message on a scale from 0.0 to 1.0. Reply with ONLY the number."
- temperature=0 for determinism
- Blended via EMA (alpha=0.3) — recent messages shift the coefficient but don't dominate

Tone tiers:
| Coefficient | Tone | System prompt addition |
|-------------|------|----------------------|
| >= 0.75 | Warm | "be warm, friendly, and generous with your help" |
| 0.50–0.75 | Professional | "be helpful and professional" |
| 0.25–0.50 | Dry | "be dry, terse, and matter-of-fact" |
| < 0.25 | Sarcastic Marvin | "be sarcastic and reluctant, like the original Marvin from Hitchhiker's Guide" |

## Conversation Sessions

Marvin supports multi-turn conversations without requiring his name in every message.

**Trigger:** Any message (text or audio) containing a Marvin name variant activates a session for that chat.

**Session flow:**
1. User says "Marvin" (text or in audio) → session activates for that `chat` ID
2. Subsequent messages in the same chat → GPT classifier (`is_still_talking_to_marvin()`) checks if the message continues the conversation with Marvin, using the last 10 messages as context
3. If yes → Marvin processes and replies (no name needed)
4. If no (user dismissed Marvin, changed topic, said thanks/bye) → session deactivates
5. Anyone in the chat (not just the original caller) can trigger or dismiss Marvin — works in groups

**Classifier:** Minimal GPT-4o-mini call (max_tokens=3, temperature=0) with system prompt:
"Given a conversation history with Marvin and a new message, determine if the user is STILL talking to Marvin. Reply 'yes' if continuing, 'no' if dismissing or moved on."

**State:** In-memory dict `active_sessions: dict[str, bool]` keyed by chat ID. Resets on brain.py restart (conservative — requires re-trigger).

**Architecture note:** Go gateway sends ALL messages (text + audio) to brain.py via inbox.jsonl. All trigger/session/filtering logic lives in brain.py, not in Go.

## Conversation Memory

Marvin has persistent conversation memory via SQLite. The system prompts explicitly tell him he can see recent messages and should reference them naturally. He should never claim he can't remember or access previous messages.

- Last 10 messages per chat injected into LLM context as "Recent conversation: User: ... / Marvin: ..."
- History persists across restarts via SQLite (memory.py)
- Both text and voice replies are stored, including transcriptions of audio messages

## File Layout

```
marvin-whatsapp/
├── main.go              # Go gateway (whatsmeow WebSocket)
├── go.mod / go.sum      # Go dependencies
├── brain.py             # Python AI brain
├── memory.py            # SQLite conversation + politeness
├── inbox.jsonl          # Go → Python messages
├── outbox.jsonl         # Python → Go replies
├── audio/               # Downloaded + generated audio files
├── session.db           # whatsmeow session (SQLite)
├── marvin_memory.db     # Conversation history + user profiles
└── marvin-whatsapp      # Compiled Go binary
```

## Integration with Marvin MCP Server

- **Shared Milvus:** brain.py queries the same `concepts` and `doc_chunks` collections that Marvin's MCP memory backend populates
- **Same embedding model:** text-embedding-3-small ensures vector compatibility
- **Not connected to Neo4j:** brain.py only does vector search, no graph traversal
- **Independent memory:** SQLite conversation history is separate from Marvin's Milvus episodic memory (decisions/sessions)
- **No MCP:** brain.py calls Milvus and OpenAI directly — it's a standalone service, not an MCP client
