# Transformer-Driven Prompt Architect

The [[prompt-engineer]] framework for generating structured prompts. 6 mandatory sections, each attacking a dimension of the [[Espaço Amostral]]. Based on the mathematical principles of the Transformer: Constant Path Length of Attention, Multi-Head Attention, and Attention Masking.

---

## Mathematical Principles

**Constant Path Length O(1):** The Transformer's attention mechanism connects any two tokens with the same computational cost. The framework exploits this with explicit cross-references -- tags like `[RULE_1]` that link constraints to execution blocks. The model does not need to "search" for the connection; it is explicit.

It is the same principle as [[MCP]]: O(1) indirect addressing. In the prompt, cross-references are the internal MCP of the text.

**Multi-Head Attention:** Distributing the task across multiple "Expert Heads" -- Security, Performance, Cost. Each head operates in a different subspace of attention. In section 1 (ROLE & PERSPECTIVES), multiple personas capture different subspaces of the problem.

**Attention Masking (Negative Constraints):** Defining "Forbidden Zones" that prevent the model from attending to legacy or insecure patterns. In section 5 (ATTENTION MASK), the "DO NOT" list is a literal mask -- it blocks regions of the [[Espaço Amostral]].

## The 6 Mandatory Sections

| Section | What it defines | Dimension it reduces |
|---|---|---|
| 1. ROLE & PERSPECTIVES | Expert personas with "Attention Heads" | Who responds |
| 2. KNOWLEDGE BEYOND WEIGHTS (MCP) | Instructions on when/how to use [[Primitivas MCP\|tools]] | What to consult |
| 3. THE GOLDEN PATTERNS (FEW-SHOTS) | Minimum 2 examples Input -> Reasoning -> Output | What correct looks like |
| 4. EXECUTION PIPELINE (CoT) | Step-by-step Chain of Thought | How to reason |
| 5. ATTENTION MASK (CONSTRAINTS) | "DO NOT" list | What not to do |
| 6. FINAL TASK | Specific trigger to begin | What to do now |

Each section is a [[Redução de Espaço na Prática|reduction]] operation on the [[Espaço Amostral]]: section 1 constrains the "who" space, section 2 the "with what", section 3 the "what it looks like", section 4 the "how to think", section 5 the "what to avoid", section 6 the "what to do."

## [[Catálogo de Tools]] Injection

Section 2 (KNOWLEDGE BEYOND WEIGHTS) is where the auto-discovered catalog is injected. The generated prompt tells the model: "these tools exist in the workspace, use them in the MCP section of the prompt you are generating." It is meta-context -- [[Contexto Programático|context]] about how to provide context.

## Role in the Thesis

The framework is a formalization of how to assemble [[Contexto]] that maximizes [[Determinismo Mensurável|determinism]]. Each section attacks a source of [[Drift]]:
- Without role -> persona drift (who is responding?)
- Without few-shots -> format drift (what should the response look like?)
- Without constraints -> scope drift (what is forbidden?)

With all 6 sections filled, the prompt is the task's [[Ontologia]] -- complete enough that the response is nearly [[Tautologia|tautological]].

---

Related to: [[prompt-engineer]], [[Catálogo de Tools]], [[Contexto Programático]], [[Anti-Alucinação]], [[Redução de Espaço na Prática]], [[Determinismo Mensurável]], [[MCP]], [[Primitivas MCP]], [[Espaço Amostral]], [[Drift]]
