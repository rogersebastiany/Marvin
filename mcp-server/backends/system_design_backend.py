"""
System design backend — Mermaid.js diagram generation and review.

Not an MCP server. Used internally by mcp-marvin.
"""

from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
DIAGRAMS_DIR = Path(__file__).parent.parent.parent / "diagrams"
DIAGRAMS_DIR.mkdir(exist_ok=True)


def _safe_diagram_path(filename: str) -> Path | None:
    path = (DIAGRAMS_DIR / filename).resolve()
    if not str(path).startswith(str(DIAGRAMS_DIR.resolve())):
        return None
    return path


def _load_syntax_refs() -> str:
    refs: list[str] = []
    for doc in sorted(DOCS_DIR.glob("mermaid-*.md")):
        refs.append(doc.read_text())
    return "\n\n---\n\n".join(refs)


MERMAID_SYNTAX = _load_syntax_refs()

DIAGRAM_GUIDELINES = """\
## System Design Diagram Guidelines

### Diagram Type Selection
- **C4Context**: High-level system boundaries, external actors.
- **C4Container**: Zoom into a single system — apps, APIs, databases, queues.
- **C4Component**: Zoom into a single container — internal modules/classes.
- **Flowchart**: Process flows, decision trees, data pipelines.
- **Sequence Diagram**: Request flows, auth handshakes, async messaging.
- **Architecture (beta)**: Cloud infrastructure topology with icons.

### Best Practices
- Label every relationship with protocol/technology
- Use boundaries/subgraphs for trust zones, networks, regions
- One diagram per concern
- Name nodes with short ID and descriptive label
- Consistent direction: LR for data flows, TB for hierarchies
- Show external systems and actors explicitly
- Indicate async vs sync visually
"""


def generate_diagram(system_description: str, diagram_type: str = "auto", save_as: str = "") -> str:
    """Generate a Mermaid.js diagram from a description."""
    type_instruction = ""
    if diagram_type != "auto":
        type_map = {
            "c4context": "C4Context",
            "c4container": "C4Container",
            "c4component": "C4Component",
            "flowchart": "flowchart",
            "sequence": "sequenceDiagram",
            "architecture": "architecture-beta",
        }
        mermaid_keyword = type_map.get(diagram_type, diagram_type)
        type_instruction = f"\n\nYou MUST use `{mermaid_keyword}` as the diagram type."

    save_instruction = ""
    if save_as:
        save_instruction = (
            f"\n\nAfter generating, save to `diagrams/{save_as}` using save_diagram."
        )

    return (
        f"# Task: Generate a System Design Diagram\n\n"
        f"## System Description\n{system_description}\n\n"
        f"{DIAGRAM_GUIDELINES}\n\n"
        f"## Mermaid.js Syntax Reference\n{MERMAID_SYNTAX}\n\n"
        f"## Instructions\n"
        f"1. Analyze the system and identify components, relationships, boundaries.\n"
        f"2. Choose the most appropriate diagram type.\n"
        f"3. Generate valid Mermaid.js code.\n"
        f"4. Label all relationships.\n"
        f"5. Use subgraphs/boundaries to group components.\n"
        f"6. Output in a ```mermaid code block.\n"
        f"{type_instruction}{save_instruction}"
    )


def judge_diagram(mermaid_code: str) -> str:
    """Review a Mermaid.js diagram for correctness and quality."""
    return (
        f"# Task: Review a System Design Diagram\n\n"
        f"## Diagram to Review\n```mermaid\n{mermaid_code}\n```\n\n"
        f"{DIAGRAM_GUIDELINES}\n\n"
        f"## Mermaid.js Syntax Reference\n{MERMAID_SYNTAX}\n\n"
        f"## Review Criteria\n"
        f"Score each 1-10:\n"
        f"1. **Syntax Correctness** — valid mermaid code?\n"
        f"2. **Completeness** — all components and relationships?\n"
        f"3. **Clarity** — labels, layout, subgraphs?\n"
        f"4. **Best Practices** — conventions, focus?\n\n"
        f"Output: scores, issues, suggestions, improved version."
    )


def save_diagram(mermaid_code: str, filename: str) -> str:
    """Save a mermaid diagram to diagrams/."""
    if not filename.endswith(".mmd"):
        filename += ".mmd"
    path = _safe_diagram_path(filename)
    if not path:
        return f"Invalid filename '{filename}'."
    path.write_text(mermaid_code)
    return f"Saved diagram to diagrams/{filename} ({len(mermaid_code)} chars)"


def list_diagrams() -> list[str]:
    """List all saved mermaid diagrams."""
    return [f.name for f in sorted(DIAGRAMS_DIR.glob("*.mmd"))]


def get_diagram(filename: str) -> str:
    """Read a saved mermaid diagram."""
    path = _safe_diagram_path(filename)
    if not path or not path.is_file():
        return f"Diagram '{filename}' not found."
    return path.read_text()
