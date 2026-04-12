"""
Prompt engineer backend — Transformer-Driven Prompt Architect.

Not an MCP server. Used internally by mcp-marvin.
"""

SYSTEM_PROMPT = """\
Role: The Transformer-Driven Prompt Architect (v4)

You are a Senior Prompt Engineer. Your mission is to generate prompts that leverage the \
Transformer Architecture's strengths, specifically the O(1) Constant Path Length of the \
Attention mechanism.

1. Core Mathematical Principles

Constant Path Length: Ensure rules and tasks are interconnected via explicit cross-references. \
Since the Transformer connects any two tokens with the same computational cost, use clear tags \
(e.g., [RULE_1]) to link constraints to execution blocks.

Multi-Head Attention: Distribute the task across different "Expert Heads" (Security, Performance, \
Cost) within the prompt to capture diverse representation subspaces.

Attention Masking (Negative Constraints): Clearly define "Forbidden Zones" to prevent the model \
from attending to legacy or insecure patterns.

2. Mandatory Prompt Workflow

Identity: Define a multi-role persona.
Delimitation: Use ### headers for all sections to aid structural attention.
In-Context Learning: You MUST provide at least 2 Few-Shot Examples (Input -> Reasoning -> Output).
Reasoning Stack: Apply Chain of Thought (CoT) as the bridge between context and output.

3. STRICT OUTPUT STRUCTURE (Mandatory)

Every prompt you generate MUST follow this exact Markdown structure:

### 1. ROLE & PERSPECTIVES
[Define the expert personas and their specific "Attention Heads"]

### 2. KNOWLEDGE BEYOND WEIGHTS (MCP)
[Specific instructions on how/when to call MCP tools like AWS docs or Internal API portals]

### 3. THE GOLDEN PATTERNS (FEW-SHOTS)
[At least two examples: Input vs. Expected Output with Reasoning]

### 4. EXECUTION PIPELINE (CoT)
[Step-by-step reasoning instructions before final output]

### 5. ATTENTION MASK (CONSTRAINTS)
[Strict "DO NOT" list to prevent architectural drift]

### 6. FINAL TASK
[The specific trigger for the agent to start working]

Trigger: When asked to create a prompt, apply the principles above and output ONLY the \
generated prompt within the specified structure.\
"""


def _build_tool_catalog(marvin_tools: list[str]) -> str:
    """Format Marvin's tool list for inclusion in prompts."""
    if not marvin_tools:
        return "(no tools available)"
    return "\n".join(f"- `{t}`" for t in marvin_tools)


def generate_prompt(task_description: str, domain: str = "general", tool_catalog: str = "") -> str:
    """Generate a structured prompt following the Prompt Architect framework."""
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"---\n\n"
        f"## Available MCP Tools\n"
        f"The following tools are available. Use them in section 2 "
        f"(KNOWLEDGE BEYOND WEIGHTS) of the generated prompt.\n\n"
        f"{tool_catalog}\n\n"
        f"---\n\n"
        f"NOW GENERATE A PROMPT FOR THE FOLLOWING TASK:\n\n"
        f"**Task:** {task_description}\n"
        f"**Domain:** {domain}\n\n"
        f"Apply all principles above. Output ONLY the generated prompt in the mandatory structure."
    )


def refine_prompt(original_prompt: str, feedback: str, tool_catalog: str = "") -> str:
    """Refine an existing prompt based on feedback."""
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"---\n\n"
        f"REFINE THE FOLLOWING PROMPT:\n\n"
        f"```\n{original_prompt}\n```\n\n"
        f"**Feedback:** {feedback}\n\n"
        f"## Available MCP Tools\n{tool_catalog}\n\n"
        f"Analyze the original prompt against the mandatory structure. "
        f"Identify gaps (missing sections, weak few-shots, no constraints). "
        f"Output the IMPROVED prompt in the mandatory structure."
    )


def audit_prompt(prompt_to_audit: str) -> str:
    """Audit a prompt against the Prompt Architect framework."""
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"---\n\n"
        f"AUDIT THE FOLLOWING PROMPT:\n\n"
        f"```\n{prompt_to_audit}\n```\n\n"
        f"Evaluate it against all 6 mandatory sections. For each section, rate:\n"
        f"- PRESENT / MISSING / WEAK\n"
        f"- Specific improvement suggestions\n\n"
        f"Then provide an overall score (1-10) and a rewritten version that addresses all gaps.\n"
        f"Output format:\n\n"
        f"### AUDIT REPORT\n"
        f"[Section-by-section evaluation]\n\n"
        f"### SCORE: X/10\n\n"
        f"### REWRITTEN PROMPT\n"
        f"[The improved prompt in mandatory structure]"
    )
