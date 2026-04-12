"""
Neo4j Observability PDF Report Generator.

Generates matplotlib visualizations from the knowledge graph and compiles
everything into a single PDF with the full determinism report.

Aligned with Cognee Era 2 schema:
  - 16 typed edge types (not just RELATES_TO)
  - Concept.description (not .content), TextSummary nodes (not .summary)
  - No vault property — uses edge type distribution and cross-document bridging

Usage:
    uv run python generate_pdf_report.py
"""

import os
import textwrap
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from neo4j import GraphDatabase

from determinism_report import report as run_determinism_report, _status

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "tautologia")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Style ---
COLORS = {
    "primary": "#4C72B0",
    "secondary": "#DD8452",
    "tertiary": "#55A868",
    "quaternary": "#C44E52",
    "tautological": "#55A868",
    "high": "#4C72B0",
    "moderate": "#DDC852",
    "low": "#DD8452",
    "critical": "#C44E52",
}

# Color palette for edge types
EDGE_COLORS = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860",
]

plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#e0e0e0",
    "axes.labelcolor": "#e0e0e0",
    "text.color": "#e0e0e0",
    "xtick.color": "#e0e0e0",
    "ytick.color": "#e0e0e0",
    "grid.color": "#2a2a4a",
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})


def get_driver():
    return GraphDatabase.driver(URI, auth=AUTH)


def fetch_all_data(driver):
    """Fetch all graph data in a single session."""
    data = {}
    with driver.session() as s:
        # Basic stats
        data["total"] = s.run("MATCH (c:Concept) RETURN count(c) AS n").single()["n"]
        data["all_edges"] = s.run("MATCH ()-[r]->() RETURN count(r) AS n").single()["n"]

        # Semantic edges (Concept→Concept, non-COMPOSES)
        data["semantic_edges"] = s.run(
            "MATCH (a:Concept)-[r]->(b:Concept) "
            "WHERE type(r) <> 'COMPOSES' "
            "RETURN count(r) AS n"
        ).single()["n"]

        data["isolated"] = s.run(
            "MATCH (c:Concept) WHERE NOT (c)-[]-() "
            "RETURN count(c) AS n"
        ).single()["n"]

        # Edge type breakdown
        edge_types = s.run(
            "MATCH ()-[r]->() RETURN type(r) AS t, count(r) AS c ORDER BY c DESC"
        )
        data["edge_breakdown"] = {r["t"]: r["c"] for r in edge_types}

        # Semantic edge type breakdown (Concept→Concept only)
        sem_types = s.run(
            "MATCH (a:Concept)-[r]->(b:Concept) "
            "RETURN type(r) AS t, count(r) AS c ORDER BY c DESC"
        )
        data["semantic_breakdown"] = {r["t"]: r["c"] for r in sem_types}

        # Node label distribution
        label_dist = s.run(
            "MATCH (n) "
            "WITH CASE "
            "  WHEN 'Concept' IN labels(n) THEN 'Concept' "
            "  WHEN 'TextSummary' IN labels(n) THEN 'TextSummary' "
            "  WHEN 'DocumentChunk' IN labels(n) THEN 'DocumentChunk' "
            "  WHEN 'TextDocument' IN labels(n) THEN 'TextDocument' "
            "  ELSE 'Other' "
            "END AS label "
            "RETURN label, count(*) AS n ORDER BY n DESC"
        )
        data["label_dist"] = {r["label"]: r["n"] for r in label_dist}

        # Degree distribution (all edges, Concept nodes only)
        degrees = s.run(
            "MATCH (c:Concept)-[r]-() WITH c, count(r) AS deg RETURN deg ORDER BY deg"
        )
        data["degrees"] = [r["deg"] for r in degrees]

        # Semantic degree distribution (Concept↔Concept, non-COMPOSES)
        sem_degrees = s.run(
            "MATCH (c:Concept)-[r]-(other:Concept) "
            "WHERE type(r) <> 'COMPOSES' "
            "WITH c, count(r) AS deg RETURN deg ORDER BY deg"
        )
        data["semantic_degrees"] = [r["deg"] for r in sem_degrees]

        # Top concepts by semantic connections
        top = s.run(
            "MATCH (c:Concept)-[r]-(other:Concept) "
            "WHERE type(r) <> 'COMPOSES' "
            "WITH c, count(r) AS connections, "
            "  count(DISTINCT type(r)) AS edge_types "
            "ORDER BY connections DESC LIMIT 20 "
            "RETURN c.name AS name, connections, edge_types"
        )
        data["top"] = [dict(r) for r in top]

        # Orphans — least connected by semantic edges
        orphans = s.run(
            "MATCH (c:Concept)-[r]-(other:Concept) "
            "WHERE type(r) <> 'COMPOSES' "
            "WITH c, count(r) AS connections "
            "ORDER BY connections ASC LIMIT 20 "
            "RETURN c.name AS name, connections"
        )
        data["orphans"] = [dict(r) for r in orphans]

        # Cross-document concepts (appear in 2+ TextDocuments)
        cross_doc = s.run(
            "MATCH (c:Concept)-[:COMPOSES]-(:DocumentChunk)-[:COMPOSES]-(td:TextDocument) "
            "WITH c, count(DISTINCT td) AS doc_count "
            "WHERE doc_count >= 2 "
            "ORDER BY doc_count DESC LIMIT 15 "
            "RETURN c.name AS name, doc_count"
        )
        data["cross_doc"] = [dict(r) for r in cross_doc]

        # Degree stats
        degree_stats = s.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS deg "
            "RETURN min(deg) AS min_deg, max(deg) AS max_deg, "
            "  avg(deg) AS avg_deg, count(c) AS connected_nodes"
        ).single()
        data["degree_stats"] = {
            "min": degree_stats["min_deg"] or 0,
            "avg": degree_stats["avg_deg"] or 0,
            "max": degree_stats["max_deg"] or 0,
        }

        total = data["total"]
        data["density"] = data["all_edges"] / (total * (total - 1)) * 100 if total > 1 else 0

        # Run determinism metrics
        metrics, weights, composite = run_determinism_report(s)
        data["metrics"] = metrics
        data["weights"] = weights
        data["composite"] = composite

    return data


def status_color(score):
    if score >= 95:
        return COLORS["tautological"]
    elif score >= 80:
        return COLORS["high"]
    elif score >= 60:
        return COLORS["moderate"]
    elif score >= 40:
        return COLORS["low"]
    else:
        return COLORS["critical"]


# ============================================================
# CHART GENERATORS
# ============================================================

def chart_determinism_radar(data):
    """Radar chart of the 7 determinism metrics."""
    metrics = data["metrics"]
    labels = [
        "Grounding", "Content\nCoverage", "Summary\nCoverage",
        "Connectivity", "Bidirection-\nality", "Edge\nDiversity", "Tool\nTautology",
    ]
    values = [metrics[k] for k in [
        "grounding", "content_coverage", "summary_coverage",
        "connectivity", "bidirectionality", "edge_diversity", "tool_tautology",
    ]]

    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_closed = values + values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    for pct in [25, 50, 75, 100]:
        circle = np.full(len(angles), pct)
        ax.plot(angles, circle, color="#3a3a5a", linewidth=0.5, linestyle="--")

    ax.fill(angles, values_closed, alpha=0.25, color="#4C72B0")
    ax.plot(angles, values_closed, color="#6C92D0", linewidth=2, marker="o", markersize=6)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=9)
    ax.set_ylim(0, 105)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"], size=8)
    ax.set_title(
        f"Determinism Radar — Composite: {data['composite']:.1f}%",
        size=14, weight="bold", pad=20,
    )
    plt.tight_layout()
    return fig


def chart_edge_type_distribution(data):
    """Horizontal bar chart of edge type counts."""
    fig, ax = plt.subplots(figsize=(9, 6))
    breakdown = data["edge_breakdown"]
    types = list(reversed(list(breakdown.keys())))
    counts = list(reversed(list(breakdown.values())))
    colors = [EDGE_COLORS[i % len(EDGE_COLORS)] for i in range(len(types))]
    colors.reverse()

    bars = ax.barh(types, counts, color=colors, edgecolor="#2a2a4a")
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + max(counts) * 0.01, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", ha="left", size=8, weight="bold")

    ax.set_xlabel("Count")
    ax.set_title(f"Edge Type Distribution ({sum(breakdown.values())} total edges)", size=14, weight="bold")
    ax.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    return fig


def chart_node_label_distribution(data):
    """Pie chart of node label distribution."""
    fig, ax = plt.subplots(figsize=(6, 5))
    label_dist = data["label_dist"]
    labels = list(label_dist.keys())
    sizes = list(label_dist.values())
    colors = [COLORS["primary"], COLORS["secondary"], COLORS["tertiary"], COLORS["quaternary"], "#888"][:len(labels)]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, textprops={"color": "#e0e0e0"},
    )
    for t in autotexts:
        t.set_weight("bold")
    ax.set_title(f"Node Label Distribution ({sum(sizes)} total)", size=14, weight="bold")
    plt.tight_layout()
    return fig


def chart_degree_distribution(data):
    """Histogram of semantic degree distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: All edges
    degrees = data["degrees"]
    if degrees:
        bins = range(0, max(degrees) + 5, 5)
        ax1.hist(degrees, bins=bins, color="#4C72B0", edgecolor="#2a2a4a", alpha=0.85)
        ax1.axvline(np.mean(degrees), color="#DD8452", linestyle="--", linewidth=2,
                     label=f"Mean: {np.mean(degrees):.1f}")
        ax1.axvline(np.median(degrees), color="#55A868", linestyle="--", linewidth=2,
                     label=f"Median: {np.median(degrees):.0f}")
    ax1.set_xlabel("Degree (all edges)")
    ax1.set_ylabel("Concepts")
    ax1.set_title("All Edges", size=12, weight="bold")
    ax1.legend(facecolor="#16213e", edgecolor="#3a3a5a", fontsize=8)
    ax1.grid(True, alpha=0.3)

    # Right: Semantic edges only
    sem_degrees = data["semantic_degrees"]
    if sem_degrees:
        bins = range(0, max(sem_degrees) + 3, 2)
        ax2.hist(sem_degrees, bins=bins, color="#55A868", edgecolor="#2a2a4a", alpha=0.85)
        ax2.axvline(np.mean(sem_degrees), color="#DD8452", linestyle="--", linewidth=2,
                     label=f"Mean: {np.mean(sem_degrees):.1f}")
        ax2.axvline(np.median(sem_degrees), color="#4C72B0", linestyle="--", linewidth=2,
                     label=f"Median: {np.median(sem_degrees):.0f}")
    ax2.set_xlabel("Degree (semantic only)")
    ax2.set_ylabel("Concepts")
    ax2.set_title("Semantic Edges (Concept↔Concept)", size=12, weight="bold")
    ax2.legend(facecolor="#16213e", edgecolor="#3a3a5a", fontsize=8)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Degree Distribution", size=14, weight="bold")
    plt.tight_layout()
    return fig


def chart_top_concepts(data):
    """Horizontal bar chart of top 20 concepts by semantic connections."""
    fig, ax = plt.subplots(figsize=(10, 7))
    top = data["top"]
    names = [t["name"] for t in reversed(top)]
    connections = [t["connections"] for t in reversed(top)]
    edge_types = [t["edge_types"] for t in reversed(top)]

    # Color by edge type diversity: more types = greener
    max_types = max(edge_types) if edge_types else 1
    colors = [plt.cm.RdYlGn(et / max_types * 0.8 + 0.2) for et in edge_types]

    bars = ax.barh(names, connections, color=colors, edgecolor="#2a2a4a")

    # Annotate with edge type count
    for bar, et in zip(bars, edge_types):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{et} types", va="center", ha="left", size=7, alpha=0.7)

    ax.set_xlabel("Semantic Connections")
    ax.set_title("Top 20 Most Connected Concepts (semantic edges)", size=14, weight="bold")
    ax.grid(True, axis="x", alpha=0.3)

    # Colorbar legend
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, norm=plt.Normalize(1, max_types))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.02, aspect=30)
    cbar.set_label("Edge Type Diversity", size=9)

    plt.tight_layout()
    return fig


def chart_orphans(data):
    """Bar chart of least connected concepts (semantic edges)."""
    fig, ax = plt.subplots(figsize=(9, 5))
    orphans = data["orphans"]
    if not orphans:
        ax.text(0.5, 0.5, "No orphans found", ha="center", va="center", size=14)
        return fig

    names = [o["name"] for o in orphans]
    conns = [o["connections"] for o in orphans]

    ax.bar(range(len(names)), conns, color="#C44E52", edgecolor="#2a2a4a", alpha=0.85)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", size=7)
    ax.set_ylabel("Semantic Connections")
    ax.set_title("Least Connected Concepts (semantic edges only)", size=14, weight="bold")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def chart_cross_document(data):
    """Bar chart of concepts that appear across multiple source documents."""
    fig, ax = plt.subplots(figsize=(10, 6))
    cross = data["cross_doc"]
    if not cross:
        ax.text(0.5, 0.5, "No cross-document concepts found", ha="center", va="center", size=14)
        ax.set_title("Cross-Document Bridging Concepts", size=14, weight="bold")
        plt.tight_layout()
        return fig

    names = [c["name"] for c in cross]
    docs = [c["doc_count"] for c in cross]

    bars = ax.barh(list(reversed(names)), list(reversed(docs)),
                   color="#55A868", edgecolor="#2a2a4a", alpha=0.85)
    for bar, d in zip(bars, reversed(docs)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f"{d} docs", va="center", ha="left", size=8, weight="bold")

    ax.set_xlabel("Source Documents")
    ax.set_title("Cross-Document Bridging Concepts", size=14, weight="bold")
    ax.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    return fig


def chart_metrics_bar(data):
    """Horizontal bar chart of all determinism metrics with weights."""
    fig, ax = plt.subplots(figsize=(9, 5))
    metrics = data["metrics"]
    weights = data["weights"]
    labels_map = {
        "grounding": "Grounding",
        "content_coverage": "Content Coverage",
        "summary_coverage": "Summary Coverage",
        "connectivity": "Connectivity",
        "bidirectionality": "Bidirectionality",
        "edge_diversity": "Edge Diversity",
        "tool_tautology": "Tool Tautology",
    }
    keys = list(labels_map.keys())
    labels = [f"{labels_map[k]} (w={weights[k]})" for k in keys]
    values = [metrics[k] for k in keys]
    colors = [status_color(v) for v in values]

    bars = ax.barh(list(reversed(labels)), list(reversed(values)),
                   color=list(reversed(colors)), edgecolor="#2a2a4a")

    for bar, val in zip(bars, reversed(values)):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", ha="left", size=9, weight="bold")

    ax.set_xlim(0, 115)
    ax.axvline(95, color="#55A868", linestyle=":", linewidth=1.5, alpha=0.6, label="Tautological (95%)")
    ax.axvline(80, color="#4C72B0", linestyle=":", linewidth=1.5, alpha=0.6, label="High (80%)")
    ax.set_xlabel("Score (%)")
    ax.set_title("Determinism Metrics Breakdown", size=14, weight="bold")
    ax.legend(facecolor="#16213e", edgecolor="#3a3a5a", loc="lower right")
    ax.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    return fig


def chart_composite_gauge(data):
    """Gauge-style visualization of composite score."""
    fig, ax = plt.subplots(figsize=(7, 4))
    score = data["composite"]

    ax.barh(0, 100, height=0.6, color="#2a2a4a", edgecolor="#3a3a5a")
    ax.barh(0, score, height=0.6, color=status_color(score), edgecolor="#2a2a4a")

    for threshold, label in [(40, "LOW"), (60, "MOD"), (80, "HIGH"), (95, "TAUT")]:
        ax.axvline(threshold, color="#e0e0e0", linewidth=1, linestyle=":", alpha=0.4)
        ax.text(threshold, 0.45, label, ha="center", va="bottom", size=7, alpha=0.6)

    ax.text(score / 2, 0, f"{score:.1f}%", ha="center", va="center", size=20,
            weight="bold", color="#e0e0e0")
    ax.text(50, -0.55, f"Status: {_status(score)}", ha="center", va="center",
            size=12, weight="bold", color=status_color(score))

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])
    ax.set_xlabel("Composite Determinism Score (%)")
    ax.set_title("Ontological Determinism Gauge", size=14, weight="bold")
    plt.tight_layout()
    return fig


# ============================================================
# MAIN
# ============================================================

def main():
    print("Connecting to Neo4j...")
    driver = get_driver()

    print("Fetching graph data and running determinism report...")
    data = fetch_all_data(driver)
    driver.close()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(OUTPUT_DIR, f"neo4j_observability_{timestamp}.pdf")

    print("\nGenerating charts...")
    charts = [
        ("Composite Gauge", chart_composite_gauge),
        ("Determinism Radar", chart_determinism_radar),
        ("Metrics Breakdown", chart_metrics_bar),
        ("Edge Type Distribution", chart_edge_type_distribution),
        ("Node Label Distribution", chart_node_label_distribution),
        ("Degree Distribution", chart_degree_distribution),
        ("Top Concepts", chart_top_concepts),
        ("Orphans", chart_orphans),
        ("Cross-Document Bridges", chart_cross_document),
    ]

    with PdfPages(pdf_path) as pdf:
        # Title page
        fig = plt.figure(figsize=(11, 8.5))
        fig.patch.set_facecolor("#1a1a2e")
        fig.text(0.5, 0.6, "Neo4j Observability Report", ha="center", va="center",
                 size=28, weight="bold", color="#e0e0e0")
        fig.text(0.5, 0.5, "Tautologia Ontologica — Knowledge Graph", ha="center", va="center",
                 size=16, color="#8888aa")
        fig.text(0.5, 0.40, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ha="center",
                 va="center", size=12, color="#6666aa")

        total = data["total"]
        all_edges = data["all_edges"]
        sem_edges = data["semantic_edges"]
        edge_types = len(data["edge_breakdown"])
        fig.text(0.5, 0.32,
                 f"{total} concepts  |  {all_edges} edges ({sem_edges} semantic, {edge_types} types)  |  "
                 f"Score: {data['composite']:.1f}%  ({_status(data['composite'])})",
                 ha="center", va="center", size=12, weight="bold",
                 color=status_color(data["composite"]))
        pdf.savefig(fig)
        plt.close(fig)
        print("  [1/{0}] Title page".format(len(charts) + 1))

        # Chart pages
        for i, (name, chart_fn) in enumerate(charts, 2):
            fig = chart_fn(data)
            pdf.savefig(fig)
            plt.close(fig)
            print(f"  [{i}/{len(charts)+1}] {name}")

    print(f"\nPDF saved to: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    main()
