"""
Neo4j Observability PDF Report Generator.

Generates matplotlib visualizations from the knowledge graph and compiles
everything into a single PDF with the full determinism report.

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

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "tautologia")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Style ---
COLORS = {
    "thesis": "#4C72B0",
    "implementation": "#DD8452",
    "both": "#55A868",
    "tautological": "#55A868",
    "high": "#4C72B0",
    "moderate": "#DDC852",
    "low": "#DD8452",
    "critical": "#C44E52",
}

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
        data["edges"] = s.run("MATCH ()-[r:RELATES_TO]->() RETURN count(r) AS n").single()["n"]
        data["ghosts"] = s.run("MATCH (c:Concept {ghost: true}) RETURN count(c) AS n").single()["n"]
        data["isolated"] = s.run(
            "MATCH (c:Concept) WHERE NOT (c)-[:RELATES_TO]-() RETURN count(c) AS n"
        ).single()["n"]

        # Vault distribution
        vaults = s.run(
            "MATCH (c:Concept) RETURN c.vault AS vault, count(*) AS n ORDER BY n DESC"
        )
        data["vaults"] = {r["vault"]: r["n"] for r in vaults}

        # Degree distribution
        degrees = s.run(
            "MATCH (c:Concept)-[r]-() WITH c, count(r) AS deg RETURN deg ORDER BY deg"
        )
        data["degrees"] = [r["deg"] for r in degrees]

        # Top concepts by connections
        top = s.run(
            "MATCH (c:Concept)-[r]-() "
            "RETURN c.name AS name, c.vault AS vault, count(r) AS connections "
            "ORDER BY connections DESC LIMIT 20"
        )
        data["top"] = [dict(r) for r in top]

        # Orphans (least connected)
        orphans = s.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS connections ORDER BY connections ASC LIMIT 15 "
            "RETURN c.name AS name, c.vault AS vault, connections"
        )
        data["orphans"] = [dict(r) for r in orphans]

        # Bridges
        bridges = s.run(
            "MATCH (c:Concept)-[:RELATES_TO]-(t:Concept {vault: 'thesis'}) "
            "WITH c, count(DISTINCT t) AS thesis_links "
            "MATCH (c)-[:RELATES_TO]-(i:Concept {vault: 'implementation'}) "
            "WITH c, thesis_links, count(DISTINCT i) AS impl_links "
            "RETURN c.name AS name, c.vault AS vault, "
            "  thesis_links, impl_links, thesis_links + impl_links AS total "
            "ORDER BY total DESC LIMIT 15"
        )
        data["bridges"] = [dict(r) for r in bridges]

        # Determinism metrics
        with_content = s.run(
            "MATCH (c:Concept) WHERE c.content IS NOT NULL AND size(c.content) > 10 "
            "RETURN count(c) AS n"
        ).single()["n"]
        with_summary = s.run(
            "MATCH (c:Concept) WHERE c.summary IS NOT NULL AND size(c.summary) > 5 "
            "RETURN count(c) AS n"
        ).single()["n"]

        total = data["total"]
        ghosts = data["ghosts"]
        ghost_coverage = (total - ghosts) / total * 100 if total else 0
        content_coverage = with_content / total * 100 if total else 0
        summary_coverage = with_summary / total * 100 if total else 0

        # Connectivity score
        degree_stats = s.run(
            "MATCH (c:Concept)-[r]-() "
            "WITH c, count(r) AS deg "
            "RETURN min(deg) AS min_deg, max(deg) AS max_deg, "
            "  avg(deg) AS avg_deg, count(c) AS connected_nodes"
        ).single()
        min_deg = degree_stats["min_deg"] or 0
        avg_deg = degree_stats["avg_deg"] or 0
        max_deg = degree_stats["max_deg"] or 0
        connected = degree_stats["connected_nodes"] or 0
        connectivity_score = 0
        if total > 0:
            connected_pct = connected / total * 100
            min_deg_score = min(min_deg / 3, 1.0) * 100
            connectivity_score = (connected_pct + min_deg_score) / 2

        # Bidirectionality
        reciprocal = s.run(
            "MATCH (a:Concept)-[r1:RELATES_TO]->(b:Concept) "
            "WHERE (b)-[:RELATES_TO]->(a) "
            "RETURN count(r1) AS n"
        ).single()["n"]
        edges_count = data["edges"]
        bidirectional_pct = reciprocal / edges_count * 100 if edges_count else 0

        # Vault bridging
        bridge_concepts = s.run(
            "MATCH (c:Concept)-[:RELATES_TO]-(t:Concept) "
            "WHERE t.vault IN ['thesis', 'both'] "
            "WITH c, count(DISTINCT t) AS thesis_neighbors WHERE thesis_neighbors > 0 "
            "MATCH (c)-[:RELATES_TO]-(i:Concept) "
            "WHERE i.vault IN ['implementation', 'both'] "
            "WITH c, count(DISTINCT i) AS impl_neighbors WHERE impl_neighbors > 0 "
            "RETURN count(c) AS n"
        ).single()["n"]
        vault_bridging = bridge_concepts / total * 100 if total else 0

        # Tool tautology
        tool_concepts = s.run(
            "MATCH (c:Concept) WHERE c.name IN "
            "['docs-server','web-to-docs','prompt-engineer','system-design',"
            "'mcp-ontology-server','mcp-memory-server'] RETURN count(c) AS total"
        ).single()["total"]
        tautological_tools = s.run(
            "MATCH (c:Concept) WHERE c.name IN "
            "['docs-server','web-to-docs','mcp-ontology-server','mcp-memory-server'] "
            "RETURN count(c) AS n"
        ).single()["n"]
        partial_tools = s.run(
            "MATCH (c:Concept) WHERE c.name IN ['prompt-engineer','system-design'] "
            "RETURN count(c) AS n"
        ).single()["n"]
        tool_tautology = 0
        if tool_concepts > 0:
            tool_tautology = (tautological_tools + partial_tools * 0.5) / tool_concepts * 100

        data["metrics"] = {
            "ghost_coverage": ghost_coverage,
            "content_coverage": content_coverage,
            "summary_coverage": summary_coverage,
            "connectivity": connectivity_score,
            "bidirectionality": bidirectional_pct,
            "vault_bridging": vault_bridging,
            "tool_tautology": tool_tautology,
        }
        weights = {
            "ghost_coverage": 0.20,
            "content_coverage": 0.15,
            "summary_coverage": 0.05,
            "connectivity": 0.20,
            "bidirectionality": 0.10,
            "vault_bridging": 0.15,
            "tool_tautology": 0.15,
        }
        data["weights"] = weights
        data["composite"] = sum(data["metrics"][k] * weights[k] for k in weights)
        data["degree_stats"] = {
            "min": min_deg, "avg": avg_deg, "max": max_deg,
        }
        data["density"] = edges_count / (total * (total - 1)) * 100 if total > 1 else 0

        # Per-concept degree for vault coloring
        per_concept = s.run(
            "MATCH (c:Concept)-[r]-() "
            "RETURN c.name AS name, c.vault AS vault, count(r) AS deg "
            "ORDER BY deg DESC"
        )
        data["per_concept_degree"] = [dict(r) for r in per_concept]

        # Ghost list
        ghost_list = s.run(
            "MATCH (c:Concept {ghost: true}) RETURN c.name AS name"
        )
        data["ghost_list"] = [r["name"] for r in ghost_list]

        # Weakly connected
        weak = s.run(
            "MATCH (c:Concept)-[r]-() WITH c, count(r) AS deg WHERE deg < 3 "
            "RETURN c.name AS name, deg ORDER BY deg"
        )
        data["weak"] = [dict(r) for r in weak]

        # Content-less
        no_content = s.run(
            "MATCH (c:Concept) WHERE c.content IS NULL OR size(c.content) <= 10 "
            "RETURN c.name AS name ORDER BY name"
        )
        data["no_content"] = [r["name"] for r in no_content]

        # Unbridged
        unbridged = s.run(
            "MATCH (c:Concept) "
            "WHERE NOT EXISTS { "
            "  MATCH (c)-[:RELATES_TO]-(t:Concept) WHERE t.vault IN ['thesis','both'] "
            "} OR NOT EXISTS { "
            "  MATCH (c)-[:RELATES_TO]-(i:Concept) WHERE i.vault IN ['implementation','both'] "
            "} "
            "RETURN c.name AS name, c.vault AS vault ORDER BY vault, name"
        )
        data["unbridged"] = [dict(r) for r in unbridged]

    return data


def status_label(score):
    if score >= 95:
        return "TAUTOLOGICAL"
    elif score >= 80:
        return "HIGH"
    elif score >= 60:
        return "MODERATE"
    elif score >= 40:
        return "LOW"
    else:
        return "CRITICAL"


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
        "Ghost\nCoverage", "Content\nCoverage", "Summary\nCoverage",
        "Connectivity", "Bidirection-\nality", "Vault\nBridging", "Tool\nTautology",
    ]
    values = [metrics[k] for k in [
        "ghost_coverage", "content_coverage", "summary_coverage",
        "connectivity", "bidirectionality", "vault_bridging", "tool_tautology",
    ]]

    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_closed = values + values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    # Draw reference circles
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


def chart_vault_distribution(data):
    """Pie chart of vault distribution."""
    fig, ax = plt.subplots(figsize=(6, 5))
    vaults = data["vaults"]
    labels = list(vaults.keys())
    sizes = list(vaults.values())
    colors = [COLORS.get(v, "#888888") for v in labels]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, textprops={"color": "#e0e0e0"},
    )
    for t in autotexts:
        t.set_weight("bold")
    ax.set_title("Vault Distribution", size=14, weight="bold")
    plt.tight_layout()
    return fig


def chart_degree_distribution(data):
    """Histogram of degree distribution."""
    fig, ax = plt.subplots(figsize=(8, 5))
    degrees = data["degrees"]
    bins = range(0, max(degrees) + 5, 5)
    ax.hist(degrees, bins=bins, color="#4C72B0", edgecolor="#2a2a4a", alpha=0.85)
    ax.axvline(np.mean(degrees), color="#DD8452", linestyle="--", linewidth=2, label=f"Mean: {np.mean(degrees):.1f}")
    ax.axvline(np.median(degrees), color="#55A868", linestyle="--", linewidth=2, label=f"Median: {np.median(degrees):.0f}")
    ax.set_xlabel("Degree (connections)")
    ax.set_ylabel("Number of concepts")
    ax.set_title("Degree Distribution", size=14, weight="bold")
    ax.legend(facecolor="#16213e", edgecolor="#3a3a5a")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def chart_top_concepts(data):
    """Horizontal bar chart of top 20 concepts by connections."""
    fig, ax = plt.subplots(figsize=(10, 7))
    top = data["top"]
    names = [t["name"] for t in reversed(top)]
    connections = [t["connections"] for t in reversed(top)]
    vault_colors = [COLORS.get(t["vault"], "#888") for t in reversed(top)]

    bars = ax.barh(names, connections, color=vault_colors, edgecolor="#2a2a4a")
    ax.set_xlabel("Connections")
    ax.set_title("Top 20 Most Connected Concepts", size=14, weight="bold")
    ax.grid(True, axis="x", alpha=0.3)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS["thesis"], label="thesis"),
        Patch(facecolor=COLORS["implementation"], label="implementation"),
        Patch(facecolor=COLORS["both"], label="both"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", facecolor="#16213e", edgecolor="#3a3a5a")
    plt.tight_layout()
    return fig


def chart_orphans(data):
    """Bar chart of least connected concepts."""
    fig, ax = plt.subplots(figsize=(9, 5))
    orphans = data["orphans"]
    names = [o["name"] for o in orphans]
    conns = [o["connections"] for o in orphans]
    vault_colors = [COLORS.get(o["vault"], "#888") for o in orphans]

    ax.bar(range(len(names)), conns, color=vault_colors, edgecolor="#2a2a4a")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", size=8)
    ax.set_ylabel("Connections")
    ax.set_title("Least Connected Concepts (Orphans)", size=14, weight="bold")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def chart_bridges(data):
    """Stacked bar chart showing thesis vs implementation links for bridge concepts."""
    fig, ax = plt.subplots(figsize=(10, 6))
    bridges = data["bridges"]
    names = [b["name"] for b in bridges]
    thesis = [b["thesis_links"] for b in bridges]
    impl = [b["impl_links"] for b in bridges]
    x = range(len(names))

    ax.bar(x, thesis, color=COLORS["thesis"], label="Thesis links", edgecolor="#2a2a4a")
    ax.bar(x, impl, bottom=thesis, color=COLORS["implementation"], label="Implementation links", edgecolor="#2a2a4a")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha="right", size=8)
    ax.set_ylabel("Cross-vault links")
    ax.set_title("Top Bridge Concepts (Theory ↔ Implementation)", size=14, weight="bold")
    ax.legend(facecolor="#16213e", edgecolor="#3a3a5a")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def chart_metrics_bar(data):
    """Horizontal bar chart of all determinism metrics with weights."""
    fig, ax = plt.subplots(figsize=(9, 5))
    metrics = data["metrics"]
    weights = data["weights"]
    labels_map = {
        "ghost_coverage": "Ghost Coverage",
        "content_coverage": "Content Coverage",
        "summary_coverage": "Summary Coverage",
        "connectivity": "Connectivity",
        "bidirectionality": "Bidirectionality",
        "vault_bridging": "Vault Bridging",
        "tool_tautology": "Tool Tautology",
    }
    keys = list(labels_map.keys())
    labels = [f"{labels_map[k]} (w={weights[k]})" for k in keys]
    values = [metrics[k] for k in keys]
    colors = [status_color(v) for v in values]

    y = range(len(labels))
    bars = ax.barh(list(reversed(labels)), list(reversed(values)), color=list(reversed(colors)), edgecolor="#2a2a4a")

    # Value labels
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

    # Background bar
    ax.barh(0, 100, height=0.6, color="#2a2a4a", edgecolor="#3a3a5a")
    # Score bar
    ax.barh(0, score, height=0.6, color=status_color(score), edgecolor="#2a2a4a")

    # Threshold markers
    for threshold, label in [(40, "LOW"), (60, "MOD"), (80, "HIGH"), (95, "TAUT")]:
        ax.axvline(threshold, color="#e0e0e0", linewidth=1, linestyle=":", alpha=0.4)
        ax.text(threshold, 0.45, label, ha="center", va="bottom", size=7, alpha=0.6)

    ax.text(score / 2, 0, f"{score:.1f}%", ha="center", va="center", size=20, weight="bold", color="#e0e0e0")
    ax.text(50, -0.55, f"Status: {status_label(score)}", ha="center", va="center", size=12, weight="bold",
            color=status_color(score))

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])
    ax.set_xlabel("Composite Determinism Score (%)")
    ax.set_title("Ontological Determinism Gauge", size=14, weight="bold")
    plt.tight_layout()
    return fig


# ============================================================
# TEXT REPORT PAGE
# ============================================================

def text_report_page(data):
    """Full text determinism report as a figure."""
    fig = plt.figure(figsize=(11, 14))
    fig.patch.set_facecolor("#1a1a2e")

    metrics = data["metrics"]
    weights = data["weights"]
    total = data["total"]
    edges = data["edges"]
    ghosts = data["ghosts"]
    ds = data["degree_stats"]
    density = data["density"]
    composite = data["composite"]

    lines = []
    lines.append("=" * 70)
    lines.append("  ONTOLOGICAL DETERMINISM REPORT")
    lines.append("  Tautologia Ontológica — Knowledge Graph Assessment")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"  Graph: {total} concepts, {edges} edges, {ghosts} ghosts")
    lines.append(f"  Density: {density:.2f}% of max possible edges")
    lines.append(f"  Degree: min={ds['min']}, avg={ds['avg']:.1f}, max={ds['max']}")
    lines.append(f"  Isolated: {data['isolated']}")
    lines.append("")
    lines.append("-" * 70)
    lines.append(f"  {'Metric':<38} {'Score':>8}  {'Status':<15} {'Weight'}")
    lines.append("-" * 70)

    labels = {
        "ghost_coverage": "Ghost Coverage (defined/referenced)",
        "content_coverage": "Content Coverage (has substance)",
        "summary_coverage": "Summary Coverage (has summary)",
        "connectivity": "Connectivity (no orphans, min 3)",
        "bidirectionality": "Bidirectionality (A→B and B→A)",
        "vault_bridging": "Vault Bridging (theory↔impl)",
        "tool_tautology": "Tool Tautology (tautological tools)",
    }

    for key in weights:
        score = metrics[key]
        status = status_label(score)
        w = weights[key]
        lines.append(f"  {labels[key]:<38} {score:>7.1f}%  {status:<15} w={w}")

    lines.append("-" * 70)
    lines.append(f"  {'COMPOSITE DETERMINISM SCORE':<38} {composite:>7.1f}%  {status_label(composite)}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("GAPS TO 100%:")
    lines.append("")

    if ghosts > 0:
        lines.append(f"  ⚠ {ghosts} ghost nodes (referenced but undefined)")
        for name in data["ghost_list"]:
            lines.append(f"      - {name}")

    if data["no_content"]:
        lines.append(f"  ⚠ {len(data['no_content'])} concepts without content: {', '.join(data['no_content'][:10])}")

    if data["weak"]:
        lines.append(f"  ⚠ {len(data['weak'])} weakly connected concepts (< 3 edges):")
        for w in data["weak"]:
            lines.append(f"      - {w['name']} ({w['deg']} edges)")

    bidir = metrics["bidirectionality"]
    if bidir < 80:
        lines.append(f"  ⚠ Only {bidir:.0f}% of edges are bidirectional")
        lines.append("      One-directional links = unvalidated from one side")

    if data["unbridged"]:
        lines.append(f"  ⚠ {len(data['unbridged'])} concepts not bridging both vaults:")
        for u in data["unbridged"][:15]:
            lines.append(f"      - [{u['vault']}] {u['name']}")
        if len(data["unbridged"]) > 15:
            lines.append(f"      ... and {len(data['unbridged']) - 15} more")

    tt = metrics["tool_tautology"]
    if tt < 100:
        lines.append(f"  ⚠ Tool tautology at {tt:.0f}%")
        lines.append("      prompt-engineer and system-design are partially tautological")
        lines.append("      (generation tools — output is constrained but not closed)")

    lines.append("")
    if composite >= 95:
        lines.append("  ✓ Graph is approaching ontological completeness.")
    elif composite >= 80:
        lines.append("  → Graph is well-structured. Address gaps above to approach 100%.")
    else:
        lines.append("  → Significant gaps remain. Focus on content and connectivity.")

    text = "\n".join(lines)
    fig.text(0.05, 0.97, text, transform=fig.transFigure, fontsize=8.5,
             verticalalignment="top", fontfamily="monospace", color="#e0e0e0")
    return fig


# ============================================================
# MAIN
# ============================================================

def main():
    print("Connecting to Neo4j...")
    driver = get_driver()

    print("Fetching graph data...")
    data = fetch_all_data(driver)
    driver.close()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(OUTPUT_DIR, f"neo4j_observability_{timestamp}.pdf")

    print("Generating charts...")
    charts = [
        ("Composite Gauge", chart_composite_gauge),
        ("Determinism Radar", chart_determinism_radar),
        ("Metrics Breakdown", chart_metrics_bar),
        ("Vault Distribution", chart_vault_distribution),
        ("Degree Distribution", chart_degree_distribution),
        ("Top Concepts", chart_top_concepts),
        ("Orphans", chart_orphans),
        ("Bridges", chart_bridges),
    ]

    with PdfPages(pdf_path) as pdf:
        # Title page
        fig = plt.figure(figsize=(11, 8.5))
        fig.patch.set_facecolor("#1a1a2e")
        fig.text(0.5, 0.6, "Neo4j Observability Report", ha="center", va="center",
                 size=28, weight="bold", color="#e0e0e0")
        fig.text(0.5, 0.5, "Tautologia Ontológica — Knowledge Graph", ha="center", va="center",
                 size=16, color="#8888aa")
        fig.text(0.5, 0.40, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ha="center",
                 va="center", size=12, color="#6666aa")
        fig.text(0.5, 0.32, f"{data['total']} concepts  |  {data['edges']} edges  |  "
                 f"Composite Score: {data['composite']:.1f}%  ({status_label(data['composite'])})",
                 ha="center", va="center", size=13, weight="bold",
                 color=status_color(data["composite"]))
        pdf.savefig(fig)
        plt.close(fig)
        print("  [1/10] Title page")

        # Chart pages
        for i, (name, chart_fn) in enumerate(charts, 2):
            fig = chart_fn(data)
            pdf.savefig(fig)
            plt.close(fig)
            print(f"  [{i}/{len(charts)+2}] {name}")

        # Full text report
        fig = text_report_page(data)
        pdf.savefig(fig)
        plt.close(fig)
        print(f"  [{len(charts)+2}/{len(charts)+2}] Full Determinism Report")

    print(f"\nPDF saved to: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    main()
