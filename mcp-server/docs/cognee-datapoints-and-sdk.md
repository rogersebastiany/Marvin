# Cognee — DataPoint custom graph_model, SDK, quickstart


---

## 1. 

## Get Started with Cognee

Quickstart your journey with Cognee. Install, configure, and run your first example to build AI memory applications.

## Core Concepts: Understanding Cognee

Learn about Cognee’s architecture, building blocks, and main operations that power the system.

## Setup Configuration

Set up LLM providers, embedding engines, vector stores, and graph databases to customize Cognee for your needs.

## Essential Guides and Customizing Cognee

Step-by-step guides for customizing Cognee, including custom tasks, pipelines, and advanced configuration.

## Examples and Use Cases

Explore real-world examples and use cases for building AI memory applications with Cognee.

---

## 2. Install cognee

## Latest commit

## History

[History](/topoteretes/cognee/commits/main/README.md)

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

✴️ *Available as a plugin for your Claude Code — [claude-code-plugin](https://github.com/topoteretes/cognee-integrations/tree/main/integrations/claude-code)*

Cognee memory plugin

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

Cognee's API gives you four operations — `remember`, `recall`, `forget`, and `improve`:

```
import cognee
import asyncio

async def main():
    # Store permanently in the knowledge graph (runs add + cognify + improve)
    await cognee.remember("Cognee turns documents into AI memory.")

    # Store in session memory (fast cache, syncs to graph in background)
    await cognee.remember("User prefers detailed explanations.", session_id="chat_1")

    # Query with auto-routing (picks best search strategy automatically)
    results = await cognee.recall("What does Cognee do?")
    for result in results:
        print(result)

    # Query session memory first, fall through to graph if needed
    results = await cognee.recall("What does the user prefer?", session_id="chat_1")
    for result in results:
        print(result)

    # Delete when done
    await cognee.forget(dataset="main_dataset")

if     asyncio.run(main())
```

### Use the Cognee CLI

```
cognee-cli remember "Cognee turns documents into AI memory."

cognee-cli recall "What does Cognee do?"

cognee-cli forget --all
```

To open the local UI, run:

```
cognee-cli -ui
```

## Use with AI Agents

### Claude Code

Install the [Cognee memory plugin](https://github.com/topoteretes/cognee-integrations/tree/main/integrations/claude-code) to give Claude Code persistent memory across sessions. The plugin automatically captures tool calls into session memory via hooks and syncs to the permanent knowledge graph at session end.

**Setup:**

```
# Install cognee
pip install cognee

# Configure
export LLM_API_KEY="your-openai-key"

# Clone the plugin
git clone https://github.com/topoteretes/cognee-integrations.git

# Enable it (add to ~/.zshrc for permanent use)
claude --plugin-dir ./cognee-integrations/integrations/claude-code
```

Or connect to Cognee Cloud instead of running locally:

```
export COGNEE_SERVICE_URL="https://your-instance.cognee.ai"
export COGNEE_API_KEY="ck_..."
```

The plugin hooks into Claude Code's lifecycle — `SessionStart` initializes memory, `PostToolUse` captures actions, `UserPromptSubmit` injects relevant context, `PreCompact` preserves memory across context resets, and `SessionEnd` bridges session data into the permanent graph.

### Hermes Agent

Enable Cognee as the memory provider in [Hermes Agent](https://github.com/NousResearch/hermes-agent) for session-aware knowledge graph memory with auto-routing recall.

**Setup:**

```
# ~/.hermes/config.yaml
memory:
  provider: cognee
```

```
export LLM_API_KEY="your-openai-key"
hermes  # start chatting — session memory and graph persistence are automatic
```

Or run `hermes memory setup` and select Cognee. For Cognee Cloud, set `COGNEE_SERVICE_URL` and `COGNEE_API_KEY` in `~/.hermes/.env`.

### Connect to Cognee Cloud

Point any Python agent at a managed Cognee instance — all SDK calls route to the cloud:

```
import cognee

await cognee.serve(url="https://your-instance.cognee.ai", api_key="ck_...")

await cognee.remember("important context")
results = await cognee.recall("what happened?")

await cognee.disconnect()
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
| **Cognee Cloud** | Managed service, no infrastructure to maintain | [Sign up](https://www.cognee.ai) or `await cognee.serve()` |
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

---

## 3. quickstart

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

## Bibliography

1. [](https://docs.cognee.ai/)
2. [Install cognee](https://github.com/topoteretes/cognee/blob/main/README.md)
3. [quickstart](https://docs.cognee.ai/quickstart)