# Cognee - Knowledge Graph Memory Engine for AI Agents


---

## 1. Add text to cognee

Cognee - Build AI memory with a Knowledge Engine that learns

[Demo](https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s)
.
[Docs](https://docs.cognee.ai/)
.
[Learn More](https://cognee.ai)
·
[Join Discord](https://discord.gg/NQPKmU5CCg)
·
[Join r/AIMemory](https://www.reddit.com/r/AIMemory/)
.
[Community Plugins & Add-ons](https://github.com/topoteretes/cognee-community)

[![GitHub forks](https://img.shields.io/github/forks/topoteretes/cognee.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/topoteretes/cognee/network/)
[![GitHub stars](https://img.shields.io/github/stars/topoteretes/cognee.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/topoteretes/cognee/stargazers/)
[![GitHub commits](https://badgen.net/github/commits/topoteretes/cognee)](https://GitHub.com/topoteretes/cognee/commit/)
[![GitHub tag](https://badgen.net/github/tag/topoteretes/cognee)](https://github.com/topoteretes/cognee/tags/)
[![Downloads](https://static.pepy.tech/badge/cognee)](https://pepy.tech/project/cognee)
[![License](https://img.shields.io/github/license/topoteretes/cognee?colorA=00C586&colorB=000000)](https://github.com/topoteretes/cognee/blob/main/LICENSE)
[![Contributors](https://img.shields.io/github/contributors/topoteretes/cognee?colorA=00C586&colorB=000000)](https://github.com/topoteretes/cognee/graphs/contributors)
Use our knowledge engine to build personalized and dynamic memory for AI Agents.

🌐 Available Languages
:
[Deutsch](https://www.readme-i18n.com/topoteretes/cognee?lang=de) |
[Español](https://www.readme-i18n.com/topoteretes/cognee?lang=es) |
[Français](https://www.readme-i18n.com/topoteretes/cognee?lang=fr) |
[日本語](https://www.readme-i18n.com/topoteretes/cognee?lang=ja) |
[한국어](README_ko.md) |
[Português](https://www.readme-i18n.com/topoteretes/cognee?lang=pt) |
[Русский](https://www.readme-i18n.com/topoteretes/cognee?lang=ru) |
[中文](https://www.readme-i18n.com/topoteretes/cognee?lang=zh)

## About Cognee
Cognee is an open-source knowledge engine that lets you ingest data in any format or structure and continuously learns to provide the right context for AI agents. It combines vector search, graph databases and cognitive science approaches to make your documents both searchable by meaning and connected by relationships as they change and evolve.
:star: \_Help us reach more developers and grow the cognee community. Star this repo!\_
:books: \_Check our detailed [documentation](https://docs.cognee.ai/getting-started/installation#environment-configuration) for setup and configuration.\_
:crab: \_Available as a plugin for your OpenClaw — [cognee-openclaw](https://www.npmjs.com/package/@cognee/cognee-openclaw)\_
### Why use Cognee:
- Knowledge infrastructure — unified ingestion, graph/vector search, runs locally, ontology grounding, multimodal
- Persistent and Learning Agents - learn from feedback, context management, cross-agent knowledge sharing
- Reliable and Trustworthy Agents - agentic user/tenant isolation, traceability, OTEL collector, audit traits
### Product Features## Basic Usage & Feature Guide
To learn more, [check out this short, end-to-end Colab walkthrough](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing) of Cognee's core features.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing)
## Quickstart
Let’s try Cognee in just a few lines of code.
### Prerequisites
- Python 3.10 to 3.13
### Step 1: Install Cognee
You can install Cognee with \*\*pip\*\*, \*\*poetry\*\*, \*\*uv\*\*, or your preferred Python package manager.
```bash
uv pip install cognee
```
### Step 2: Configure the LLM
```python
import os
os.environ["LLM\_API\_KEY"] = "YOUR OPENAI\_API\_KEY"
```
Alternatively, create a `.env` file using our [template](https://github.com/topoteretes/cognee/blob/main/.env.template).
To integrate other LLM providers, see our [LLM Provider Documentation](https://docs.cognee.ai/setup-configuration/llm-providers).
### Step 3: Run the Pipeline
Cognee will take your documents, load them into the knowledge angine and search combined vector/graph relationships.
Now, run a minimal pipeline:
```python
import cognee
import asyncio
from pprint import pprint
async def main():
# Add text to cognee
await cognee.add("Cognee turns documents into AI memory.")
# Add to knowledge engine
await cognee.cognify()
# Query the knowledge graph
results = await cognee.search("What does Cognee do?")
# Display the results
for result in results:
pprint(result)
if \_\_name\_\_ == '\_\_main\_\_':
asyncio.run(main())
```
As you can see, the output is generated from the document we previously stored in Cognee:
```bash
Cognee turns documents into AI memory.
```
### Use the Cognee CLI
As an alternative, you can get started with these essential commands:
```bash
cognee-cli add "Cognee turns documents into AI memory."
cognee-cli cognify
cognee-cli search "What does Cognee do?"
cognee-cli delete --all
```
To open the local UI, run:
```bash
cognee-cli -ui
```
## Examples
Browse more examples in the [`examples/`](examples/) folder — demos, guides, custom pipelines, and database configurations.
\*\*Use Case 1 — Customer Support Agent\*\*
```python
Goal: Resolve customer issues using their personal data across finance, support, and product history.
User: "My invoice looks wrong and the issue is still not resolved."
Cognee tracks: past interactions, failed actions, resolved cases, product history
# Agent response:
Agent: "I found 2 similar billing cases resolved last month.
The issue was caused by a sync delay between payment
and invoice systems — a fix was applied on your account."
# What happens under the hood:
- Unifies data sources from various company channels
- Reconstructs the interaction timeline and tracks outcomes
- Retrieves similar resolved cases
- Maps to the best resolution strategy
- Updates memory after execution so the agent never repeats the same mistake
```
\*\*Use Case 2 — Expert Knowledge Distillation (SQL Copilot)\*\*
```python
Goal: Help junior analysts solve tasks by reusing expert-level queries, patterns, and reasoning.
User: "How do I calculate customer retention for this dataset?"
Cognee tracks: expert SQL queries, workflow patterns, schema structures, successful implementations
# Agent response:
Agent: "Here's how senior analysts solved a similar retention query.
Cognee matched your schema to a known structure and adapted
the expert's logic to fit your dataset."
# What happens under the hood:
- Extracts and stores patterns from expert SQL queries and workflows
- Maps the current schema to previously seen structures
- Retrieves similar tasks and their successful implementations
- Adapts expert reasoning to the current context
- Updates memory with new successful patterns so junior analysts perform at near-expert level
```
## Deploy Cognee
Use [Cognee Cloud](https://www.cognee.ai) for a fully managed experience, or self-host with one of the 1-click deployment configurations below.
| Platform | Best For | Command |
|----------|----------|---------|
| \*\*Cognee Cloud\*\* | Managed service, no infrastructure to maintain | [Sign up](https://www.cognee.ai) |
| \*\*Modal\*\* | Serverless, auto-scaling, GPU workloads | `bash distributed/deploy/modal-deploy.sh` |
| \*\*Railway\*\* | Simplest PaaS, native Postgres | `railway init && railway up` |
| \*\*Fly.io\*\* | Edge deployment, persistent volumes | `bash distributed/deploy/fly-deploy.sh` |
| \*\*Render\*\* | Simple PaaS with managed Postgres | Deploy to Render button |
| \*\*Daytona\*\* | Cloud sandboxes (SDK or CLI) | See `distributed/deploy/daytona\_sandbox.py` |
See the [`distributed/`](distributed/) folder for deploy scripts, worker configurations, and additional details.
## Latest News
[![Watch Demo](https://img.youtube.com/vi/8hmqS2Y5RVQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s)
## Community & Support
### Contributing
We welcome contributions from the community! Your input helps make Cognee better for everyone. See [`CONTRIBUTING.md`](CONTRIBUTING.md) to get started.
### Code of Conduct
We're committed to fostering an inclusive and respectful community. Read our [Code of Conduct](https://github.com/topoteretes/cognee/blob/main/CODE\_OF\_CONDUCT.md) for guidelines.
## Research & Citation
We recently published a research paper on optimizing knowledge graphs for LLM reasoning:
```bibtex
@misc{markovic2025optimizinginterfaceknowledgegraphs,
title={Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning},
author={Vasilije Markovic and Lazar Obradovic and Laszlo Hajdu and Jovan Pavlovic},
year={2025},
eprint={2505.24478},
archivePrefix={arXiv},
primaryClass={cs.AI},
url={https://arxiv.org/abs/2505.24478},
}
```

---

## 2. quickstart

After completing the [installation steps](https://docs.cognee.ai/getting-started/installation) successfully, run your first Cognee example to see AI memory in action.

## [​](#basic-usage) Basic Usage

This minimal example shows how to add content, process it, and perform a search:

```
import cognee
import asyncio

async def main():

    # Create a clean slate for cognee -- reset data and system state
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # Add sample content
    text = "Cognee turns documents into AI memory."
    await cognee.add(text)

    # Process with LLMs to build the knowledge graph
    await cognee.cognify()

    # Search the knowledge graph
    results = await cognee.search(
        query_text="What does Cognee do?"
    )

    # Print
    for result in results:
        print(result)

if     asyncio.run(main())
```

Visualisation

Interactive knowledge graph visualization — drag nodes, zoom, and hover for details. Create your own visualization with 2 additional lines of code [here](/guides/graph-visualization).

## [​](#what-just-happened) What just happened

The code demonstrates Cognee’s three core operations:

* **`.add`** — Adds data to Cognee so they can be cognified. In this case, we added a single string (“Cognee turns documents into AI memory”); from Cognee’s perspective, this string is a document.
* **`.cognify`** — This is where the cognification happens. All documents are chunked, entities are extracted, relationships are made, and summaries are generated. In this case, we can expect entities like Frodo, One Ring, and Mordor.
* **`.search`** — Queries the knowledge graph using vector similarity and graph traversal to find relevant information and return contextual results.

## [​](#about-async-/-await-in-cognee) About `async` / `await` in Cognee

**Cognee uses asynchronous code extensively.** That means many of its functions are defined with `async` and must be called with `await`. This lets Python handle waiting (e.g. for I/O or network calls) without blocking the rest of your program.

Async basics

This example uses `async` / `await`, Python’s way of doing asynchronous programming.
Asynchronous programming is used when functions may block because they are waiting for something (for example, a reply from an API call). By writing `async def`, you define a function that can pause at certain points.
The `await` keyword marks those calls that may need to pause.
To run such functions, Python provides the `asyncio` library. It uses a loop, called the event loop, which executes your code in order but, whenever a function is waiting, can temporarily run another one. From inside your function, though, everything still runs top-to-bottom: each line after an `await` only executes once the awaited call has finished.

Async resources

* A good starting point is this [guide](https://realpython.com/async-io-python/).
* Official documentation is available [here](https://docs.python.org/3/library/asyncio.html).

## [​](#next-steps) Next Steps

## Cognee core concepts

Learn about Cognee’s core concepts, architecture, building blocks, and main operations.

## Enrich your graph with memify

Add derived facts like coding rules to your knowledge graph.

---

## 3. LLM

Set up your environment and install Cognee to start building AI memory.

Python **3.9 – 3.12** is required to run Cognee.

## [​](#prerequisites) Prerequisites

Environment Configuration

* We recommend creating a `.env` file in your project root
* Cognee supports many configuration options, and a `.env` file keeps them organized

API Keys & Models

You have two main options for configuring LLM and embedding providers:**Option 1: OpenAI (Simplest)**

* Single API key handles both LLM and embeddings
* Uses gpt-4o-mini for LLM and text-embedding-3-small for embeddings by default
* Works out of the box with minimal configuration

**Option 2: Other Providers**

* Configure both LLM and embedding providers separately
* Supports Gemini, Anthropic, Ollama, and more
* Requires setting both `LLM_*` and `EMBEDDING_*` variables

By default, Cognee uses OpenAI for both LLMs and embeddings. If you change the LLM provider but don’t configure embeddings, it will still default to OpenAI.

Virtual Environment

* We recommend using [uv](https://github.com/astral-sh/uv) for virtual environment management
* Run the following commands to create and activate a virtual environment:

```
uv venv && source .venv/bin/activate
```

Optional

Database

* PostgreSQL database is required if you plan to use PostgreSQL as your relational database (requires `postgres` extra)

## [​](#setup) Setup

* OpenAI (Recommended)
* Other Providers (Gemini, Anthropic, etc.)

## 

**Environment:** Add your OpenAI API key to your `.env` file:

```
LLM_API_KEY="your_openai_api_key"
```

**Installation:** Install Cognee with all extras:

```
uv pip install cognee
```

**What this gives you**: Cognee installed with default local databases (SQLite, LanceDB, Kuzu) — no external servers required.

This single API key handles both LLM and embeddings. We use gpt-4o-mini for the LLM model and text-embedding-3-small for embeddings by default.

## 

**Environment:** Configure both LLM and embedding providers in your `.env` file. Here is an example for Gemini:

```
# LLM
LLM_PROVIDER="gemini"
LLM_MODEL="gemini/gemini-flash-latest"
LLM_API_KEY="your_gemini_api_key"

# Embeddings
EMBEDDING_PROVIDER="gemini"
EMBEDDING_MODEL="gemini/gemini-embedding-001"
EMBEDDING_API_KEY="your_gemini_api_key"
```

Make sure to configure both LLM and embedding settings. If you only set one, the other will default to OpenAI.

**Installation:** Install Cognee with provider-specific extras (`gemini`, `anthropic`, `ollama`, `mistral`, `huggingface`, or `groq`) for example:

```
uv pip install cognee[gemini]
```

**What this gives you**: Cognee installed with your chosen providers and default local databases.For detailed configuration options, see our [LLM](/setup-configuration/llm-providers) and [Embeddings](/setup-configuration/embedding-providers) guides.

## [​](#next-steps) Next Steps

## Run Your First Example

**Quickstart Tutorial**Get started with Cognee by running your first knowledge graph example.

## Explore Advanced Features

**Core Concepts**Dive deeper into Cognee’s powerful features and capabilities.

---

## 4. All data stored locally

Cognee is designed for flexible deployment across development and production environments, with configurable data storage backends that scale with your needs.

## [​](#data-storage-architecture) Data Storage Architecture

Cognee operates on a three-tier data storage model, each optimized for specific data types and query patterns:

## Graph Database

**Relationships & Entities**Stores knowledge graph structure, entity relationships, and semantic connections.

## Vector Database

**Embeddings & Search**Handles semantic embeddings for similarity search and content retrieval.

## Relational Database

**Metadata & State**Manages datasets, user permissions, pipeline state, and operational data.

Each storage layer can be deployed as managed services, self-hosted servers, or file-based systems (like S3 buckets), giving you complete flexibility over your infrastructure.

## [​](#deployment-options) Deployment Options

Choose the deployment strategy that matches your requirements:

* Development
* Production
* Hybrid

**Local & Testing**

* **Docker**: Containerized local deployment with embedded databases
* **MCP**: Direct integration with code editors and IDEs
* **File-based**: SQLite, local files, and embedded vector stores

**Scalable & Managed**

* **Modal**: Serverless deployment with auto-scaling
* **Kubernetes**: Container orchestration with Helm charts
* **EC2**: Traditional cloud server deployment
* **Cloud Services**: Managed databases (RDS, Neo4j Aura, Qdrant)

**Flexible Storage**

* **S3 + Servers**: File storage in S3 with managed database services
* **Multi-cloud**: Different storage tiers across cloud providers
* **Edge**: Local processing with cloud storage backends

## [​](#storage-configuration-examples) Storage Configuration Examples

Local Development

**Embedded & File-based**

```
# All data stored locally
GRAPH_DATABASE=networkx
VECTOR_DATABASE=lancedb
RELATIONAL_DATABASE=sqlite://./cognee.db
```

**Multi-Agent Limitation**: Default Kuzu graph store uses file-based locking and is not suitable for concurrent access from multiple agents. Use Neo4j or FalkorDB for multi-agent deployments.

Cloud Production

**Managed Services**

```
# Fully managed cloud services
GRAPH_DATABASE=neo4j://your-aura-instance
VECTOR_DATABASE=pinecone://your-index
RELATIONAL_DATABASE=postgresql://your-rds-instance
```

Hybrid S3

**S3 + Managed Databases**

```
# Vector data in S3, databases managed
VECTOR_DATABASE=s3://your-bucket/vectors/
GRAPH_DATABASE=neo4j://managed-instance
RELATIONAL_DATABASE=postgresql://rds-instance
```

## [​](#quick-start-guide) Quick Start Guide

1

Choose Deployment

Select your deployment method based on scale and requirements

2

Configure Storage

Set up your preferred combination of graph, vector, and relational databases

3

Deploy & Test

Launch Cognee and verify connectivity to all storage backends

4

Scale

Adjust storage and compute resources based on usage patterns

## [​](#deployment-methods) Deployment Methods

## Modal Deployment

**Serverless & Auto-scaling**Perfect for variable workloads with automatic resource management.

## Kubernetes (Helm)

**Enterprise & Production**Container orchestration with full control and high availability.

## EC2 Deployment

**Traditional Cloud**Standard server deployment with custom configurations.

## [​](#architecture-benefits) Architecture Benefits

**Flexible Data Tiers**: Each storage layer can be independently scaled, managed, or migrated without affecting others.

**Cost Optimization**: Use file-based storage (S3) for archival data and managed services for active workloads.

**Security**: Ensure proper network security and access controls across all storage tiers in production deployments.

## [​](#need-help) Need Help?

## Join Our Community

Get deployment support, share configurations, and connect with other Cognee users.

---

## 5. getting-started

Give Cognee your documents, and it creates a graph of raw information, extracted concepts, and meaningful relationships you can query.

## [​](#why-ai-memory-matters) Why AI memory matters

When you call an LLM, each request is stateless: it doesn’t remember what happened in the last call, and it doesn’t know about the rest of your documents.
That makes it hard to build applications that actually use your documents and carry context forward. You need a memory layer that can link your documents together and create the right context for every LLM call.

## [​](#how-cognee-works) How Cognee works

When it comes to your data, Cognee knows what matters. There are four key operations in Cognee:

* **`.add` — Prepare for cognification:**
  Send in your data asynchronously. Cognee cleans and prepares your data so that the memory layer can be created.
* **`.cognify` — Build a knowledge graph with embeddings:**
  Cognee splits your documents into chunks, extract entities, relations, and links it all into a queryable graph, that serves as the basis for the memory layer.
* **`.search` — Query with context:**
  Queries combine vector similarity with graph traversal. Depending on the mode, cognee can fetch raw nodes, explore relationships, or generate natural-language answers through RAG. It always creates the right context for the LLM.
* **[`.memify`](/core-concepts/main-operations/memify) — Enrich the graph with derived knowledge:**
  Run configurable enrichment pipelines on an existing knowledge graph to add coding-rule associations, triplet embeddings, session persistence, or custom derived nodes and edges.

## [​](#ready-to-get-started) Ready to get started?

## Set up your environment

**Installation Guide**Set up your environment and install Cognee to start building AI memory.

## Run your first example

**Quickstart Tutorial**Get started with Cognee by running your first knowledge graph example.

## Keep exploring

**Core Concepts**Dive deeper into Cognee’s powerful features and capabilities.

---

## 6. Agent response:

[Branches](/topoteretes/cognee/branches)[Tags](/topoteretes/cognee/tags)

## Folders and files

| Name | | Name | Last commit message | Last commit date |
| --- | --- | --- | --- | --- |
| Latest commit History[6,394 Commits](/topoteretes/cognee/commits/main/) | | |
| [.devcontainer](/topoteretes/cognee/tree/main/.devcontainer ".devcontainer") | | [.devcontainer](/topoteretes/cognee/tree/main/.devcontainer ".devcontainer") |  |  |
| [.github](/topoteretes/cognee/tree/main/.github ".github") | | [.github](/topoteretes/cognee/tree/main/.github ".github") |  |  |
| [assets](/topoteretes/cognee/tree/main/assets "assets") | | [assets](/topoteretes/cognee/tree/main/assets "assets") |  |  |
| [bin](/topoteretes/cognee/tree/main/bin "bin") | | [bin](/topoteretes/cognee/tree/main/bin "bin") |  |  |
| [cognee-frontend](/topoteretes/cognee/tree/main/cognee-frontend "cognee-frontend") | | [cognee-frontend](/topoteretes/cognee/tree/main/cognee-frontend "cognee-frontend") |  |  |
| [cognee-mcp](/topoteretes/cognee/tree/main/cognee-mcp "cognee-mcp") | | [cognee-mcp](/topoteretes/cognee/tree/main/cognee-mcp "cognee-mcp") |  |  |
| [cognee-starter-kit](/topoteretes/cognee/tree/main/cognee-starter-kit "cognee-starter-kit") | | [cognee-starter-kit](/topoteretes/cognee/tree/main/cognee-starter-kit "cognee-starter-kit") |  |  |
| [cognee](/topoteretes/cognee/tree/main/cognee "cognee") | | [cognee](/topoteretes/cognee/tree/main/cognee "cognee") |  |  |
| [deployment](/topoteretes/cognee/tree/main/deployment "deployment") | | [deployment](/topoteretes/cognee/tree/main/deployment "deployment") |  |  |
| [distributed](/topoteretes/cognee/tree/main/distributed "distributed") | | [distributed](/topoteretes/cognee/tree/main/distributed "distributed") |  |  |
| [evals](/topoteretes/cognee/tree/main/evals "evals") | | [evals](/topoteretes/cognee/tree/main/evals "evals") |  |  |
| [examples](/topoteretes/cognee/tree/main/examples "examples") | | [examples](/topoteretes/cognee/tree/main/examples "examples") |  |  |
| [licenses](/topoteretes/cognee/tree/main/licenses "licenses") | | [licenses](/topoteretes/cognee/tree/main/licenses "licenses") |  |  |
| [logs](/topoteretes/cognee/tree/main/logs "logs") | | [logs](/topoteretes/cognee/tree/main/logs "logs") |  |  |
| [notebooks](/topoteretes/cognee/tree/main/notebooks "notebooks") | | [notebooks](/topoteretes/cognee/tree/main/notebooks "notebooks") |  |  |
| [tools](/topoteretes/cognee/tree/main/tools "tools") | | [tools](/topoteretes/cognee/tree/main/tools "tools") |  |  |
| [working\_dir\_error\_replication](/topoteretes/cognee/tree/main/working_dir_error_replication "working_dir_error_replication") | | [working\_dir\_error\_replication](/topoteretes/cognee/tree/main/working_dir_error_replication "working_dir_error_replication") |  |  |
| [.coderabbit.yaml](/topoteretes/cognee/blob/main/.coderabbit.yaml ".coderabbit.yaml") | | [.coderabbit.yaml](/topoteretes/cognee/blob/main/.coderabbit.yaml ".coderabbit.yaml") |  |  |
| [.dockerignore](/topoteretes/cognee/blob/main/.dockerignore ".dockerignore") | | [.dockerignore](/topoteretes/cognee/blob/main/.dockerignore ".dockerignore") |  |  |
| [.dockerignore.ci](/topoteretes/cognee/blob/main/.dockerignore.ci ".dockerignore.ci") | | [.dockerignore.ci](/topoteretes/cognee/blob/main/.dockerignore.ci ".dockerignore.ci") |  |  |
| [.env.example](/topoteretes/cognee/blob/main/.env.example ".env.example") | | [.env.example](/topoteretes/cognee/blob/main/.env.example ".env.example") |  |  |
| [.env.template](/topoteretes/cognee/blob/main/.env.template ".env.template") | | [.env.template](/topoteretes/cognee/blob/main/.env.template ".env.template") |  |  |
| [.gitattributes](/topoteretes/cognee/blob/main/.gitattributes ".gitattributes") | | [.gitattributes](/topoteretes/cognee/blob/main/.gitattributes ".gitattributes") |  |  |
| [.gitguardian.yml](/topoteretes/cognee/blob/main/.gitguardian.yml ".gitguardian.yml") | | [.gitguardian.yml](/topoteretes/cognee/blob/main/.gitguardian.yml ".gitguardian.yml") |  |  |
| [.gitignore](/topoteretes/cognee/blob/main/.gitignore ".gitignore") | | [.gitignore](/topoteretes/cognee/blob/main/.gitignore ".gitignore") |  |  |
| [.mergify.yml](/topoteretes/cognee/blob/main/.mergify.yml ".mergify.yml") | | [.mergify.yml](/topoteretes/cognee/blob/main/.mergify.yml ".mergify.yml") |  |  |
| [.pre-commit-config.yaml](/topoteretes/cognee/blob/main/.pre-commit-config.yaml ".pre-commit-config.yaml") | | [.pre-commit-config.yaml](/topoteretes/cognee/blob/main/.pre-commit-config.yaml ".pre-commit-config.yaml") |  |  |
| [.pylintrc](/topoteretes/cognee/blob/main/.pylintrc ".pylintrc") | | [.pylintrc](/topoteretes/cognee/blob/main/.pylintrc ".pylintrc") |  |  |
| [AGENTS.md](/topoteretes/cognee/blob/main/AGENTS.md "AGENTS.md") | | [AGENTS.md](/topoteretes/cognee/blob/main/AGENTS.md "AGENTS.md") |  |  |
| [CLAUDE.md](/topoteretes/cognee/blob/main/CLAUDE.md "CLAUDE.md") | | [CLAUDE.md](/topoteretes/cognee/blob/main/CLAUDE.md "CLAUDE.md") |  |  |
| [CODE\_OF\_CONDUCT.md](/topoteretes/cognee/blob/main/CODE_OF_CONDUCT.md "CODE_OF_CONDUCT.md") | | [CODE\_OF\_CONDUCT.md](/topoteretes/cognee/blob/main/CODE_OF_CONDUCT.md "CODE_OF_CONDUCT.md") |  |  |
| [CONTRIBUTING.md](/topoteretes/cognee/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") | | [CONTRIBUTING.md](/topoteretes/cognee/blob/main/CONTRIBUTING.md "CONTRIBUTING.md") |  |  |
| [CONTRIBUTORS.md](/topoteretes/cognee/blob/main/CONTRIBUTORS.md "CONTRIBUTORS.md") | | [CONTRIBUTORS.md](/topoteretes/cognee/blob/main/CONTRIBUTORS.md "CONTRIBUTORS.md") |  |  |
| [DCO.md](/topoteretes/cognee/blob/main/DCO.md "DCO.md") | | [DCO.md](/topoteretes/cognee/blob/main/DCO.md "DCO.md") |  |  |
| [Dockerfile](/topoteretes/cognee/blob/main/Dockerfile "Dockerfile") | | [Dockerfile](/topoteretes/cognee/blob/main/Dockerfile "Dockerfile") |  |  |
| [Dockerfile.ci](/topoteretes/cognee/blob/main/Dockerfile.ci "Dockerfile.ci") | | [Dockerfile.ci](/topoteretes/cognee/blob/main/Dockerfile.ci "Dockerfile.ci") |  |  |
| [LICENSE](/topoteretes/cognee/blob/main/LICENSE "LICENSE") | | [LICENSE](/topoteretes/cognee/blob/main/LICENSE "LICENSE") |  |  |
| [NOTICE.md](/topoteretes/cognee/blob/main/NOTICE.md "NOTICE.md") | | [NOTICE.md](/topoteretes/cognee/blob/main/NOTICE.md "NOTICE.md") |  |  |
| [README.md](/topoteretes/cognee/blob/main/README.md "README.md") | | [README.md](/topoteretes/cognee/blob/main/README.md "README.md") |  |  |
| [README\_ko.md](/topoteretes/cognee/blob/main/README_ko.md "README_ko.md") | | [README\_ko.md](/topoteretes/cognee/blob/main/README_ko.md "README_ko.md") |  |  |
| [SECURITY.md](/topoteretes/cognee/blob/main/SECURITY.md "SECURITY.md") | | [SECURITY.md](/topoteretes/cognee/blob/main/SECURITY.md "SECURITY.md") |  |  |
| [docker-compose.yml](/topoteretes/cognee/blob/main/docker-compose.yml "docker-compose.yml") | | [docker-compose.yml](/topoteretes/cognee/blob/main/docker-compose.yml "docker-compose.yml") |  |  |
| [entrypoint.sh](/topoteretes/cognee/blob/main/entrypoint.sh "entrypoint.sh") | | [entrypoint.sh](/topoteretes/cognee/blob/main/entrypoint.sh "entrypoint.sh") |  |  |
| [mise.toml](/topoteretes/cognee/blob/main/mise.toml "mise.toml") | | [mise.toml](/topoteretes/cognee/blob/main/mise.toml "mise.toml") |  |  |
| [mypy.ini](/topoteretes/cognee/blob/main/mypy.ini "mypy.ini") | | [mypy.ini](/topoteretes/cognee/blob/main/mypy.ini "mypy.ini") |  |  |
| [poetry.lock](/topoteretes/cognee/blob/main/poetry.lock "poetry.lock") | | [poetry.lock](/topoteretes/cognee/blob/main/poetry.lock "poetry.lock") |  |  |
| [pyproject.toml](/topoteretes/cognee/blob/main/pyproject.toml "pyproject.toml") | | [pyproject.toml](/topoteretes/cognee/blob/main/pyproject.toml "pyproject.toml") |  |  |
| [uv.lock](/topoteretes/cognee/blob/main/uv.lock "uv.lock") | | [uv.lock](/topoteretes/cognee/blob/main/uv.lock "uv.lock") |  |  |
|  | | |

## Repository files navigation

Cognee - Build AI memory with a Knowledge Engine that learns

[Demo](https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s)
.
[Docs](https://docs.cognee.ai/)
.
[Learn More](https://cognee.ai)
·
[Join Discord](https://discord.gg/NQPKmU5CCg)
·
[Join r/AIMemory](https://www.reddit.com/r/AIMemory/)
.
[Community Plugins & Add-ons](https://github.com/topoteretes/cognee-community)

Use our knowledge engine to build personalized and dynamic memory for AI Agents.

🌐 Available Languages
:
[Deutsch](https://www.readme-i18n.com/topoteretes/cognee?lang=de) |
[Español](https://www.readme-i18n.com/topoteretes/cognee?lang=es) |
[Français](https://www.readme-i18n.com/topoteretes/cognee?lang=fr) |
[日本語](https://www.readme-i18n.com/topoteretes/cognee?lang=ja) |
[한국어](/topoteretes/cognee/blob/main/README_ko.md) |
[Português](https://www.readme-i18n.com/topoteretes/cognee?lang=pt) |
[Русский](https://www.readme-i18n.com/topoteretes/cognee?lang=ru) |
[中文](https://www.readme-i18n.com/topoteretes/cognee?lang=zh)

## About Cognee

Cognee is an open-source knowledge engine that lets you ingest data in any format or structure and continuously learns to provide the right context for AI agents. It combines vector search, graph databases and cognitive science approaches to make your documents both searchable by meaning and connected by relationships as they change and evolve.

⭐ *Help us reach more developers and grow the cognee community. Star this repo!*

📚 *Check our detailed [documentation](https://docs.cognee.ai/getting-started/installation#environment-configuration) for setup and configuration.*

🦀 *Available as a plugin for your OpenClaw — [cognee-openclaw](https://www.npmjs.com/package/@cognee/cognee-openclaw)*

### Why use Cognee:

* Knowledge infrastructure — unified ingestion, graph/vector search, runs locally, ontology grounding, multimodal
* Persistent and Learning Agents - learn from feedback, context management, cross-agent knowledge sharing
* Reliable and Trustworthy Agents - agentic user/tenant isolation, traceability, OTEL collector, audit traits

### Product Features

## Basic Usage & Feature Guide

To learn more, [check out this short, end-to-end Colab walkthrough](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing) of Cognee's core features.

## Quickstart

Let’s try Cognee in just a few lines of code.

### Prerequisites

* Python 3.10 to 3.13

### Step 1: Install Cognee

You can install Cognee with **pip**, **poetry**, **uv**, or your preferred Python package manager.

```
uv pip install cognee
```

### Step 2: Configure the LLM

```
import os
os.environ["LLM_API_KEY"] = "YOUR OPENAI_API_KEY"
```

Alternatively, create a `.env` file using our [template](https://github.com/topoteretes/cognee/blob/main/.env.template).

To integrate other LLM providers, see our [LLM Provider Documentation](https://docs.cognee.ai/setup-configuration/llm-providers).

### Step 3: Run the Pipeline

Cognee will take your documents, load them into the knowledge angine and search combined vector/graph relationships.

Now, run a minimal pipeline:

```
import cognee
import asyncio
from pprint import pprint

async def main():
    # Add text to cognee
    await cognee.add("Cognee turns documents into AI memory.")

    # Add to knowledge engine
    await cognee.cognify()

    # Query the knowledge graph
    results = await cognee.search("What does Cognee do?")

    # Display the results
    for result in results:
        pprint(result)

if     asyncio.run(main())
```

As you can see, the output is generated from the document we previously stored in Cognee:

```
  Cognee turns documents into AI memory.
```

### Use the Cognee CLI

As an alternative, you can get started with these essential commands:

```
cognee-cli add "Cognee turns documents into AI memory."

cognee-cli cognify

cognee-cli search "What does Cognee do?"
cognee-cli delete --all
```

To open the local UI, run:

```
cognee-cli -ui
```

## Examples

Browse more examples in the [`examples/`](/topoteretes/cognee/blob/main/examples) folder — demos, guides, custom pipelines, and database configurations.

**Use Case 1 — Customer Support Agent**

```
Goal: Resolve customer issues using their personal data across finance, support, and product history.

User: "My invoice looks wrong and the issue is still not resolved."

Cognee tracks: past interactions, failed actions, resolved cases, product history

# Agent response:
Agent: "I found 2 similar billing cases resolved last month.
        The issue was caused by a sync delay between payment
        and invoice systems — a fix was applied on your account."

# What happens under the hood:
- Unifies data sources from various company channels
- Reconstructs the interaction timeline and tracks outcomes
- Retrieves similar resolved cases
- Maps to the best resolution strategy
- Updates memory after execution so the agent never repeats the same mistake
```

**Use Case 2 — Expert Knowledge Distillation (SQL Copilot)**

```
Goal: Help junior analysts solve tasks by reusing expert-level queries, patterns, and reasoning.

User: "How do I calculate customer retention for this dataset?"

Cognee tracks: expert SQL queries, workflow patterns, schema structures, successful implementations

# Agent response:
Agent: "Here's how senior analysts solved a similar retention query.
        Cognee matched your schema to a known structure and adapted
        the expert's logic to fit your dataset."

# What happens under the hood:
- Extracts and stores patterns from expert SQL queries and workflows
- Maps the current schema to previously seen structures
- Retrieves similar tasks and their successful implementations
- Adapts expert reasoning to the current context
- Updates memory with new successful patterns so junior analysts perform at near-expert level
```

## Deploy Cognee

Use [Cognee Cloud](https://www.cognee.ai) for a fully managed experience, or self-host with one of the 1-click deployment configurations below.

| Platform | Best For | Command |
| --- | --- | --- |
| **Cognee Cloud** | Managed service, no infrastructure to maintain | [Sign up](https://www.cognee.ai) |
| **Modal** | Serverless, auto-scaling, GPU workloads | `bash distributed/deploy/modal-deploy.sh` |
| **Railway** | Simplest PaaS, native Postgres | `railway init && railway up` |
| **Fly.io** | Edge deployment, persistent volumes | `bash distributed/deploy/fly-deploy.sh` |
| **Render** | Simple PaaS with managed Postgres | Deploy to Render button |
| **Daytona** | Cloud sandboxes (SDK or CLI) | See `distributed/deploy/daytona_sandbox.py` |

See the [`distributed/`](/topoteretes/cognee/blob/main/distributed) folder for deploy scripts, worker configurations, and additional details.

## Latest News

## Community & Support

### Contributing

We welcome contributions from the community! Your input helps make Cognee better for everyone. See [`CONTRIBUTING.md`](/topoteretes/cognee/blob/main/CONTRIBUTING.md) to get started.

### Code of Conduct

We're committed to fostering an inclusive and respectful community. Read our [Code of Conduct](https://github.com/topoteretes/cognee/blob/main/CODE_OF_CONDUCT.md) for guidelines.

## Research & Citation

We recently published a research paper on optimizing knowledge graphs for LLM reasoning:

```
@misc{markovic2025optimizinginterfaceknowledgegraphs,
      title={Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning},
      author={Vasilije Markovic and Lazar Obradovic and Laszlo Hajdu and Jovan Pavlovic},
      year={2025},
      eprint={2505.24478},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.24478},
}
```

## About

Knowledge Engine for AI Agent Memory in 6 lines of code

[www.cognee.ai](https://www.cognee.ai "https://www.cognee.ai")

### Topics

[open-source](/topics/open-source "Topic: open-source")
[ai](/topics/ai "Topic: ai")
[knowledge](/topics/knowledge "Topic: knowledge")
[neo4j](/topics/neo4j "Topic: neo4j")
[knowledge-graph](/topics/knowledge-graph "Topic: knowledge-graph")
[openai](/topics/openai "Topic: openai")
[help-wanted](/topics/help-wanted "Topic: help-wanted")
[graph-database](/topics/graph-database "Topic: graph-database")
[ai-agents](/topics/ai-agents "Topic: ai-agents")
[contributions-welcome](/topics/contributions-welcome "Topic: contributions-welcome")
[cognitive-architecture](/topics/cognitive-architecture "Topic: cognitive-architecture")
[good-first-issue](/topics/good-first-issue "Topic: good-first-issue")
[rag](/topics/rag "Topic: rag")
[good-first-pr](/topics/good-first-pr "Topic: good-first-pr")
[vector-database](/topics/vector-database "Topic: vector-database")
[graph-rag](/topics/graph-rag "Topic: graph-rag")
[ai-memory](/topics/ai-memory "Topic: ai-memory")
[cognitive-memory](/topics/cognitive-memory "Topic: cognitive-memory")
[graphrag](/topics/graphrag "Topic: graphrag")
[context-engineering](/topics/context-engineering "Topic: context-engineering")

### Resources

[Readme](#readme-ov-file)

### License

[Apache-2.0 license](#Apache-2.0-1-ov-file)

### Code of conduct

[Code of conduct](#coc-ov-file)

### Contributing

[Contributing](#contributing-ov-file)

### Security policy

[Security policy](#security-ov-file)

[Activity](/topoteretes/cognee/activity)

[Custom properties](/topoteretes/cognee/custom-properties)

### Stars

[**15.1k**
stars](/topoteretes/cognee/stargazers)

### Watchers

[**64**
watching](/topoteretes/cognee/watchers)

### Forks

[**1.5k**
forks](/topoteretes/cognee/forks)

[Report repository](/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Ftopoteretes%2Fcognee&report=topoteretes+%28user%29)

## [Releases 92](/topoteretes/cognee/releases)

[v0.5.5.dev1

Latest

Apr 10, 2026](/topoteretes/cognee/releases/tag/v0.5.5.dev1)

[+ 91 releases](/topoteretes/cognee/releases)

## [Packages](/orgs/topoteretes/packages?repo_name=cognee)

## [Contributors](/topoteretes/cognee/graphs/contributors)

## Languages

* [Python
  93.5%](/topoteretes/cognee/search?l=python)
* [TypeScript
  5.9%](/topoteretes/cognee/search?l=typescript)
* [Shell
  0.3%](/topoteretes/cognee/search?l=shell)
* [Dockerfile
  0.2%](/topoteretes/cognee/search?l=dockerfile)
* [CSS
  0.1%](/topoteretes/cognee/search?l=css)
* [Mako
  0.0%](/topoteretes/cognee/search?l=mako)

---

## 7. [​](#cognee-api-reference) Cognee API Reference

Welcome to the Cognee API documentation. This comprehensive reference covers all endpoints for building, managing, and querying your memory using Cognee’s powerful platform.

## [​](#getting-started) Getting Started

Before using the API, you need to choose how to run Cognee. You have two main options:

## Cognee Cloud

**Managed Cloud Platform**Production-ready, fully managed service with automatic scaling and enterprise features.

## Local Docker Setup

**Self-Hosted Development**Run Cognee locally using Docker for development, testing, and custom deployments.

## [​](#setup-options) Setup Options

* Cognee Cloud
* Local Docker

**Managed Service - Recommended for Production**

1. **Sign up** at [platform.cognee.ai](https://platform.cognee.ai/)
2. **Create API Key** in your dashboard
3. **Start using** the API immediately

```
# Base URL for Cognee Cloud
BASE_URL="https://api.cognee.ai"

# Authentication
curl -H "X-Api-Key: YOUR-API-KEY" \
     -H "Content-Type: application/json" \
     $BASE_URL/api/health
```

Cognee Cloud provides enterprise-grade infrastructure with automatic scaling, managed databases, and 24/7 monitoring.

**Self-Hosted - Perfect for Development**Quick start with Docker (single command):

```
# Create environment file
echo 'LLM_API_KEY="your_openai_api_key"' > .env

# Run Cognee container
docker run --env-file ./.env -p 8000:8000 --rm -it cognee/cognee:main
```

Or use Docker Compose from the [Cognee repository](https://github.com/topoteretes/cognee):

```
# Clone repository
git clone https://github.com/topoteretes/cognee.git
cd cognee

# Set up environment
cp .env.template .env
# Edit .env with your API keys

# Start with Docker Compose
docker-compose up -d
```

Local setup uses embedded databases by default (SQLite, LanceDB, NetworkX) for easy development.

## [​](#api-base-urls) API Base URLs

Production (Cognee Cloud)

```
https://api.cognee.ai
```

**Authentication**: X-Api-Key header
**Rate Limits**: Based on your subscription plan
**Availability**: 99.9% uptime SLA

Local Development

```
http://localhost:8000
```

**Authentication**: Optional (can be disabled for local development)
**Rate Limits**: None
**Availability**: Depends on your local setup

## [​](#authentication) Authentication

* Cognee Cloud
* Local Docker

**API Key Authentication**All requests require an API key in the header:

```
X-Api-Key: YOUR-API-KEY
Content-Type: application/json
```

Get your API key from the [Cognee Cloud dashboard](https://platform.cognee.ai/).

**Optional Authentication**Local development typically runs without authentication:

```
Content-Type: application/json
```

To enable authentication locally, set `REQUIRE_AUTH=true` in your `.env` file.

## [​](#core-api-endpoints) Core API Endpoints

The Cognee API provides endpoints for the complete knowledge graph lifecycle:

## Data Ingestion

**`POST /api/add`**Add text, documents, or structured data to your knowledge base.

## Knowledge Processing

**`POST /api/cognify`**Transform raw data into structured knowledge graphs with entities and relationships.

## Semantic Search

**`POST /api/search`**Query your knowledge graph using natural language or structured queries.

## Data Management

**`DELETE /api/v1/datasets`**Remove specific data items or entire datasets from your knowledge base.

## [​](#api-features) API Features

Multiple Search Types

Flexible Data Formats

Support for various input formats locally and strings on Cognee Cloud:

* **Text**: Raw text strings, documents, articles
* **Structured**: JSON, CSV, XML data
* **Code**: Source code files and repositories
* **URLs**: Web pages and online content

## [​](#data-deletion) Data Deletion

Cognee provides granular control over data deletion through the `datasets` endpoints.

```
# List datasets you can access
curl "http://localhost:8000/api/v1/datasets" \
  -H "Authorization: Bearer $TOKEN"
```

Deletion requires the `delete` permission on the target dataset. See [Permissions](/core-concepts/multi-user-mode/permissions-system/overview) for details.  
`DELETE /api/v1/delete` is deprecated. Use the `datasets` endpoints above instead.

## [​](#quick-example) Quick Example

Here’s a complete example using the API:

```
import requests

# Configuration
BASE_URL = "http://localhost:8000"  # or https://api.cognee.ai for Cognee Cloud
API_KEY = "your-api-key"  # only for Cognee Cloud

headers = {
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY  # only for Cognee Cloud
}

# 1. Add data
add_response = requests.post(
    f"{BASE_URL}/api/add",
    json={"data": "AI is transforming how we work and live."},
    headers=headers
)

# 2. Process into knowledge graph
cognify_response = requests.post(
    f"{BASE_URL}/api/cognify",
    json={"datasets": ["main_dataset"]},
    headers=headers
)

# 3. Search the knowledge graph
search_response = requests.post(
    f"{BASE_URL}/api/search",
    json={
        "query": "What is AI?",
        "search_type": "GRAPH_COMPLETION"
    },
    headers=headers
)

print(search_response.json())
```

## [​](#interactive-api-explorer) Interactive API Explorer

## OpenAPI Specification

**Try the API interactively**All endpoints on the left side of the page are automatically generated from our OpenAPI specification, providing interactive examples and real-time testing capabilities.

* Cognee Cloud
* Local Docker

**Interactive Swagger Endpoint Docs**Our endpoints are also documented in Swagger with live testing capabilities. You can access the Swagger docs for Cognee Cloud at:

```
https://api.cognee.ai/docs
```

**Interactive Swagger Endpoint Docs**Our endpoints are also documented in Swagger with live testing capabilities. After you have started your local Cognee instance, you can access the Swagger docs at:

```
http://localhost:8000/docs
```

## [​](#error-handling) Error Handling

All API endpoints return standard HTTP status codes:

* **200**: Success
* **400**: Bad Request - Invalid parameters
* **401**: Unauthorized - Invalid or missing API key
* **404**: Not Found - Resource doesn’t exist
* **429**: Too Many Requests - Rate limit exceeded
* **500**: Internal Server Error - Server-side error

Always implement proper error handling in your applications to gracefully handle API failures and rate limits.

## [​](#next-steps) Next Steps

## Explore Endpoints

**API Documentation**Browse all available endpoints with interactive examples below.

## Community Support

**Get Help**Join our Discord community for support and discussions.

---

## Bibliography

1. [Add text to cognee](https://raw.githubusercontent.com/topoteretes/cognee/main/README.md)
2. [quickstart](https://docs.cognee.ai/getting-started/quickstart)
3. [LLM](https://docs.cognee.ai/getting-started/installation)
4. [All data stored locally](https://docs.cognee.ai/how-to-guides/)
5. [getting-started](https://docs.cognee.ai/getting-started)
6. [Agent response:](https://github.com/topoteretes/cognee)
7. [[​](#cognee-api-reference) Cognee API Reference](https://docs.cognee.ai/reference/)