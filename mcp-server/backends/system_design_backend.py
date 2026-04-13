"""
System design backend — Mermaid.js diagram generation and review.

Not an MCP server. Used internally by mcp-marvin.
Domain-specific tooling for system architecture diagrams using Mermaid.js
syntax. Supports C4, flowchart, sequence, and architecture-beta diagrams
with structured scoring criteria.
"""

import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
DIAGRAMS_DIR = Path(__file__).parent.parent.parent / "diagrams"
DIAGRAMS_DIR.mkdir(exist_ok=True)


def _safe_diagram_path(filename: str) -> Path | None:
    """Resolve a diagram filename within DIAGRAMS_DIR, blocking path traversal."""
    path = (DIAGRAMS_DIR / filename).resolve()
    if not str(path).startswith(str(DIAGRAMS_DIR.resolve())):
        return None
    return path


def _load_syntax_refs() -> str:
    """Load all mermaid-*.md docs as syntax reference for diagram generation."""
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
    """Review a Mermaid.js diagram for correctness and quality.

    Includes domain-specific scoring criteria for system design diagrams
    and validates the diagram type keyword.
    """
    validation = _validate_mermaid_syntax(mermaid_code)
    validation_note = f"\n\n**⚠ Syntax Warning:** {validation}\n" if validation else ""

    return (
        f"# Task: Review a System Design Diagram\n\n"
        f"## Diagram to Review\n```mermaid\n{mermaid_code}\n```\n"
        f"{validation_note}\n"
        f"{DIAGRAM_GUIDELINES}\n\n"
        f"## Mermaid.js Syntax Reference\n{MERMAID_SYNTAX}\n\n"
        f"## Review Criteria\n"
        f"Score each 1-10:\n"
        f"1. **Syntax Correctness** — valid mermaid code? Starts with recognized diagram type?\n"
        f"2. **Completeness** — all components and relationships? External actors shown?\n"
        f"3. **Clarity** — labels on every edge? Layout direction consistent? Subgraphs for grouping?\n"
        f"4. **Best Practices** — one concern per diagram? Short IDs with descriptive labels? "
        f"Protocols/tech on relationship labels? Trust zones or network boundaries shown?\n"
        f"5. **Domain Accuracy** — does the diagram accurately represent the system described?\n\n"
        f"Output: scores table, specific issues with line references, "
        f"concrete suggestions, improved version in ```mermaid block."
    )


# Valid Mermaid diagram type keywords for domain validation
_VALID_DIAGRAM_TYPES = frozenset({
    "flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram",
    "erDiagram", "gantt", "pie", "gitgraph", "mindmap", "timeline",
    "C4Context", "C4Container", "C4Component", "C4Dynamic", "C4Deployment",
    "architecture-beta", "block-beta", "sankey-beta", "xychart-beta",
    "journey", "quadrantChart", "requirementDiagram", "zenuml", "packet-beta",
})


def _validate_mermaid_syntax(code: str) -> str | None:
    """Check if code starts with a valid Mermaid diagram type keyword.

    Returns None if valid, error message if invalid.
    """
    first_line = code.strip().split("\n")[0].strip()
    # Extract the keyword (first word, ignoring direction like LR/TB)
    keyword = re.split(r"[\s\-]", first_line)[0]
    if keyword in _VALID_DIAGRAM_TYPES:
        return None
    return f"Unrecognized Mermaid diagram type '{keyword}'. Expected one of: {', '.join(sorted(_VALID_DIAGRAM_TYPES))}"


def save_diagram(mermaid_code: str, filename: str) -> str:
    """Save a mermaid diagram to diagrams/. Validates syntax keyword first."""
    if not filename.endswith(".mmd"):
        filename += ".mmd"
    path = _safe_diagram_path(filename)
    if not path:
        return f"Invalid filename '{filename}'."
    warning = _validate_mermaid_syntax(mermaid_code)
    if warning:
        log.warning("save_diagram: %s", warning)
    path.write_text(mermaid_code)
    log.info("Saved diagram: diagrams/%s (%d chars)", filename, len(mermaid_code))
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
