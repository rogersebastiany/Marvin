"""
Pydantic DataPoint models for Cognee — Tautologia Ontológica schema.

These models define the shape of the knowledge graph Cognee writes to
Neo4j. By passing ``Concept`` as the ``graph_model`` argument to
``cognee.cognify()`` we get ``:Concept`` nodes (not ``:Entity``) with our
16 typed relation edges, directly into the same Neo4j instance Marvin's
``mcp-server/ontology.py`` already queries.

Key facts grounded in cognee 0.5.8 source:

1. **Class name → Neo4j label.** ``DataPoint.__init__`` sets
   ``self.type = self.__class__.__name__`` (DataPoint.py:59), and that
   ``type`` field is what becomes the node label in the graph store. So
   ``class Concept(DataPoint)`` produces ``:Concept`` nodes — exactly
   what ``ontology.py`` queries with ``MATCH (c:Concept ...)``.

2. **Custom graph_model takes the entity-centric branch.** In
   ``extract_graph_from_data.py:99-103``, when ``graph_model is not
   KnowledgeGraph``, Cognee skips ``expand_with_nodes_and_edges`` and
   attaches the LLM-extracted object as ``chunk.contains``. This means
   our model must be a SINGLE root DataPoint per chunk, with related
   entities as fields — not a ``{nodes: [...], edges: [...]}`` shape.

3. **Field name → edge type.** Per the architecture docs, a field like
   ``author: Author`` produces an edge with type ``"author"``. We use
   snake_case fields matching ``relation_types.json`` (lowercased); the
   post-processor in ``cognify_vaults.py`` normalizes to SCREAMING_CASE.

4. **Deterministic IDs via uuid5.** ``DataPoint.id`` defaults to
   ``uuid4()``, so the same concept extracted from two chunks would
   create two distinct nodes. We override ``id`` in a model_validator
   using the same formula Cognee uses internally
   (``generate_node_id.py``): ``uuid5(NAMESPACE_OID, slug(name))``.
   Same name → same UUID → graph store MERGEs → automatic dedup.

5. **Index fields.** ``metadata.index_fields`` controls which fields are
   embedded into the vector store. We index ``name`` and ``description``
   so Marvin's ``retrieve()`` (and Cognee's own search) can find
   concepts by both label and meaning.

The 16 relation fields below MUST mirror ``mcp-server/relation_types.json``.
A drift check at module load fails fast if they get out of sync.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional
from uuid import NAMESPACE_OID, uuid5

from pydantic import model_validator
from cognee.infrastructure.engine import DataPoint

# ── Load schema for the runtime drift check ──────────────────────────
_RELATION_TYPES_PATH = (
    Path(__file__).parent.parent / "mcp-server" / "relation_types.json"
)
with open(_RELATION_TYPES_PATH) as f:
    _RELATION_TYPES = json.load(f)


def _slug(name: str) -> str:
    """Canonical slug for ID generation — mirrors cognee's generate_node_id."""
    return name.lower().strip().replace(" ", "_").replace("'", "")


class Concept(DataPoint):
    """
    A node in the Tautologia Ontológica knowledge graph.

    Each ``Concept`` becomes a ``:Concept`` node in Neo4j and is indexed
    by ``name`` and ``description`` in the vector store. Relationship
    fields produce typed edges to other Concepts — Cognee's LLM
    extraction populates these per-chunk; ``cognify_vaults.py``'s
    post-processor normalizes edge types to SCREAMING_CASE.
    """

    name: str
    description: str

    # ── Symmetric relations (3) ──────────────────────────────────────
    relates_to: List["Concept"] = []
    contradicts: List["Concept"] = []
    analogous_to: List["Concept"] = []

    # ── Directional relations (13) ───────────────────────────────────
    implements: List["Concept"] = []
    proves: List["Concept"] = []
    requires: List["Concept"] = []
    extends: List["Concept"] = []
    enables: List["Concept"] = []
    exemplifies: List["Concept"] = []
    composes: List["Concept"] = []
    evolves_from: List["Concept"] = []
    infers: List["Concept"] = []
    formalizes: List["Concept"] = []
    defines: List["Concept"] = []
    reduces: List["Concept"] = []
    mitigates: List["Concept"] = []

    metadata: dict = {"index_fields": ["name", "description"]}

    @model_validator(mode="after")
    def _set_deterministic_id(self):
        """Override the default ``uuid4`` with ``uuid5(slug(name))`` so
        the same concept extracted from different chunks resolves to a
        single node when MERGEd into Neo4j."""
        stable = uuid5(NAMESPACE_OID, _slug(self.name))
        object.__setattr__(self, "id", stable)
        return self


Concept.model_rebuild()  # finalize the self-reference


# ── Drift check ──────────────────────────────────────────────────────
# Catches "someone added a relation type to relation_types.json without
# updating the model" — fails fast at import, not at extraction time.
_OWN_FIELDS = {
    name
    for name in Concept.model_fields
    if name not in {"name", "description", "metadata"}
} - set(DataPoint.model_fields)

_EXPECTED = {name.lower() for name in _RELATION_TYPES}

if _OWN_FIELDS != _EXPECTED:
    missing = sorted(_EXPECTED - _OWN_FIELDS)
    extra = sorted(_OWN_FIELDS - _EXPECTED)
    raise RuntimeError(
        f"Concept model drift vs relation_types.json — "
        f"missing fields: {missing}, extra fields: {extra}"
    )
