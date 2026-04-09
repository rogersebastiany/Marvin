uv

:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}

\_\_md\_scope=new URL(".",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}

"undefined"!=typeof \_\_md\_analytics&&\_\_md\_analytics()

{
"datePublished": "2026-03-13 14:17:06Z",
"dateModified": "2026-03-13 14:17:06Z",
"@context": "https://schema.org",
"@type": "WebSite",
"name": "Astral Docs",
"url": "https://docs.astral.sh"
}

[Skip to content](#uv)

uv

Introduction

var palette=\_\_md\_get("\_\_palette");if(palette&&palette.color){if("(prefers-color-scheme)"===palette.color.media){var media=matchMedia("(prefers-color-scheme: light)"),input=document.querySelector(media.matches?"[data-md-color-media='(prefers-color-scheme: light)']":"[data-md-color-media='(prefers-color-scheme: dark)']");palette.color.media=input.getAttribute("data-md-color-media"),palette.color.scheme=input.getAttribute("data-md-color-scheme"),palette.color.primary=input.getAttribute("data-md-color-primary"),palette.color.accent=input.getAttribute("data-md-color-accent")}for(var[key,value]of Object.entries(palette.color))document.body.setAttribute("data-md-color-"+key,value)}

Initializing search

[uv](https://github.com/astral-sh/uv "Go to repository")

uv

[uv](https://github.com/astral-sh/uv "Go to repository")

* Introduction

  [Introduction](.)

  Table of contents
  + [Highlights](#highlights)
  + [Installation](#installation)
  + [Projects](#projects)
  + [Scripts](#scripts)
  + [Tools](#tools)
  + [Python versions](#python-versions)
  + [The pip interface](#the-pip-interface)
  + [Learn more](#learn-more)
* [Getting started](getting-started/)

  Getting started
  + [Installation](getting-started/installation/)
  + [First steps](getting-started/first-steps/)
  + [Features](getting-started/features/)
  + [Getting help](getting-started/help/)
* [Guides](guides/)

  Guides
  + [Installing Python](guides/install-python/)
  + [Running scripts](guides/scripts/)
  + [Using tools](guides/tools/)
  + [Working on projects](guides/projects/)
  + [Publishing packages](guides/package/)
  + [Migration](guides/migration/)

    Migration
    - [From pip to a uv project](guides/migration/pip-to-project/)
  + [Integrations](guides/integration/)

    Integrations
    - [Docker](guides/integration/docker/)
    - [Jupyter](guides/integration/jupyter/)
    - [marimo](guides/integration/marimo/)
    - [GitHub Actions](guides/integration/github/)
    - [GitLab CI/CD](guides/integration/gitlab/)
    - [Pre-commit](guides/integration/pre-commit/)
    - [PyTorch](guides/integration/pytorch/)
    - [FastAPI](guides/integration/fastapi/)
    - [Azure Artifacts](guides/integration/azure/)
    - [Google Artifact Registry](guides/integration/google/)
    - [AWS CodeArtifact](guides/integration/aws/)
    - [JFrog Artifactory](guides/integration/jfrog/)
    - [Renovate](guides/integration/renovate/)
    - [Dependabot](guides/integration/dependabot/)
    - [AWS Lambda](guides/integration/aws-lambda/)
    - [Coiled](guides/integration/coiled/)
* [Concepts](concepts/)

  Concepts
  + [Projects](concepts/projects/)

    Projects
    - [Structure and files](concepts/projects/layout/)
    - [Creating projects](concepts/projects/init/)
    - [Managing dependencies](concepts/projects/dependencies/)
    - [Running commands](concepts/projects/run/)
    - [Locking and syncing](concepts/projects/sync/)
    - [Configuring projects](concepts/projects/config/)
    - [Building distributions](concepts/projects/build/)
    - [Exporting lockfiles](concepts/projects/export/)
    - [Using workspaces](concepts/projects/workspaces/)
  + [Tools](concepts/tools/)
  + [Python versions](concepts/python-versions/)
  + [Configuration files](concepts/configuration-files/)
  + [Package indexes](concepts/indexes/)
  + [Resolution](concepts/resolution/)
  + [Build backend](concepts/build-backend/)
  + [Authentication](concepts/authentication/)

    Authentication
    - [The auth CLI](concepts/authentication/cli/)
    - [HTTP credentials](concepts/authentication/http/)
    - [Git credentials](concepts/authentication/git/)
    - [TLS certificates](concepts/authentication/certificates/)
    - [Third-party services](concepts/authentication/third-party/)
  + [Caching](concepts/cache/)
  + [Preview features](concepts/preview/)
  + [The pip interface](pip/)

    The pip interface
    - [Using environments](pip/environments/)
    - [Managing packages](pip/packages/)
    - [Inspecting environments](pip/inspection/)
    - [Declaring dependencies](pip/dependencies/)
    - [Locking environments](pip/compile/)
    - [Compatibility with pip](pip/compatibility/)
* [Reference](reference/)

  Reference
  + [Commands](reference/cli/)
  + [Settings](reference/settings/)
  + [Environment variables](reference/environment/)
  + [Storage](reference/storage/)
  + [Installer options](reference/installer/)
  + [Troubleshooting](reference/troubleshooting/)

    Troubleshooting
    - [Build failures](reference/troubleshooting/build-failures/)
    - [Reproducible examples](reference/troubleshooting/reproducible-examples/)
  + [Internals](reference/internals/)

    Internals
    - [Resolver](reference/internals/resolver/)
    - [Workspace Metadata](reference/internals/metadata/)
  + [Benchmarks](reference/benchmarks/)
  + [Policies](reference/policies/)

    Policies
    - [Versioning](reference/policies/versioning/)
    - [Platform support](reference/policies/platforms/)
    - [Python support](reference/policies/python/)
    - [Rust support](reference/policies/rust/)
    - [License](reference/policies/license/)

Table of contents

* [Highlights](#highlights)
* [Installation](#installation)
* [Projects](#projects)
* [Scripts](#scripts)
* [Tools](#tools)
* [Python versions](#python-versions)
* [The pip interface](#the-pip-interface)
* [Learn more](#learn-more)

# [uv](#uv)

An extremely fast Python package and project manager, written in Rust.

*Installing [Trio](https://trio.readthedocs.io/)'s dependencies with a warm cache.*

## [Highlights](#highlights)

* A single tool to replace `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and
  more.
* [10-100x faster](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md) than `pip`.
* Provides [comprehensive project management](#projects), with a
  [universal lockfile](concepts/projects/layout/#the-lockfile).
* [Runs scripts](#scripts), with support for
  [inline dependency metadata](guides/scripts/#declaring-script-dependencies).
* [Installs and manages](#python-versions) Python versions.
* [Runs and installs](#tools) tools published as Python packages.
* Includes a [pip-compatible interface](#the-pip-interface) for a performance boost with a familiar
  CLI.
* Supports Cargo-style [workspaces](concepts/projects/workspaces/) for scalable projects.
* Disk-space efficient, with a [global cache](concepts/cache/) for dependency deduplication.
* Installable without Rust or Python via `curl` or `pip`.
* Supports macOS, Linux, and Windows.

uv is backed by [Astral](https://astral.sh), the creators of
[Ruff](https://github.com/astral-sh/ruff).

## [Installation](#installation)

Install uv with our official standalone installer:

macOS and LinuxWindows

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

```
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, check out the [first steps](getting-started/first-steps/) or read on for a brief overview.

Tip

uv may also be installed with pip, Homebrew, and more. See all of the methods on the
[installation page](getting-started/installation/).

## [Projects](#projects)

uv manages project dependencies and environments, with support for lockfiles, workspaces, and more,
similar to `rye` or `poetry`:

```
$ uv init example
Initialized project `example` at `/home/user/example`

$ cd example

$ uv add ruff
Creating virtual environment at: .venv
Resolved 2 packages in 170ms
   Built example @ file:///home/user/example
Prepared 2 packages in 627ms
Installed 2 packages in 1ms
 + example==0.1.0 (from file:///home/user/example)
 + ruff==0.5.4

$ uv run ruff check
All checks passed!

$ uv lock
Resolved 2 packages in 0.33ms

$ uv sync
Resolved 2 packages in 0.70ms
Checked 1 package in 0.02ms
```

See the [project guide](guides/projects/) to get started.

uv also supports building and publishing projects, even if they're not managed with uv. See the
[packaging guide](guides/package/) to learn more.

## [Scripts](#scripts)

uv manages dependencies and environments for single-file scripts.

Create a new script and add inline metadata declaring its dependencies:

```
$ echo 'import requests; print(requests.get("https://astral.sh"))' > example.py

$ uv add --script example.py requests
Updated `example.py`
```

Then, run the script in an isolated virtual environment:

```
$ uv run example.py
Reading inline script metadata from: example.py
Installed 5 packages in 12ms
<Response [200]>
```

See the [scripts guide](guides/scripts/) to get started.

## [Tools](#tools)

uv executes and installs command-line tools provided by Python packages, similar to `pipx`.

Run a tool in an ephemeral environment using `uvx` (an alias for `uv tool run`):

```
$ uvx pycowsay 'hello world!'
Resolved 1 package in 167ms
Installed 1 package in 9ms
 + pycowsay==0.0.0.2
  """

  ------------
< hello world! >
  ------------
   \   ^__^
    \  (oo)\_______
       (__)\       )\/\
           ||----w |
           ||     ||
```

Install a tool with `uv tool install`:

```
$ uv tool install ruff
Resolved 1 package in 6ms
Installed 1 package in 2ms
 + ruff==0.5.4
Installed 1 executable: ruff

$ ruff --version
ruff 0.5.4
```

See the [tools guide](guides/tools/) to get started.

## [Python versions](#python-versions)

uv installs Python and allows quickly switching between versions.

Install multiple Python versions:

```
$ uv python install 3.10 3.11 3.12
Searching for Python versions matching: Python 3.10
Searching for Python versions matching: Python 3.11
Searching for Python versions matching: Python 3.12
Installed 3 versions in 3.42s
 + cpython-3.10.14-macos-aarch64-none
 + cpython-3.11.9-macos-aarch64-none
 + cpython-3.12.4-macos-aarch64-none
```

Download Python versions as needed:

```
$ uv venv --python 3.12.0
Using CPython 3.12.0
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

$ uv run --python [email protected] -- python
Python 3.8.16 (a9dbdca6fc3286b0addd2240f11d97d8e8de187a, Dec 29 2022, 11:45:30)
[PyPy 7.3.11 with GCC Apple LLVM 13.1.6 (clang-1316.0.21.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>>
```

Use a specific Python version in the current directory:

```
$ uv python pin 3.11
Pinned `.python-version` to `3.11`
```

See the [installing Python guide](guides/install-python/) to get started.

## [The pip interface](#the-pip-interface)

uv provides a drop-in replacement for common `pip`, `pip-tools`, and `virtualenv` commands.

uv extends their interfaces with advanced features, such as dependency version overrides,
platform-independent resolutions, reproducible resolutions, alternative resolution strategies, and
more.

Migrate to uv without changing your existing workflows — and experience a 10-100x speedup — with the
`uv pip` interface.

Compile requirements into a platform-independent requirements file:

```
$ uv pip compile requirements.in \
   --universal \
   --output-file requirements.txt
Resolved 43 packages in 12ms
```

Create a virtual environment:

```
$ uv venv
Using CPython 3.12.3
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

Install the locked requirements:

```
$ uv pip sync requirements.txt
Resolved 43 packages in 11ms
Installed 43 packages in 208ms
 + babel==2.15.0
 + black==24.4.2
 + certifi==2024.7.4
 ...
```

See the [pip interface documentation](pip/) to get started.

## [Learn more](#learn-more)

See the [first steps](getting-started/first-steps/) or jump straight to the
[guides](guides/) to start using uv.

March 13, 2026

var tabs=\_\_md\_get("\_\_tabs");if(Array.isArray(tabs))e:for(var set of document.querySelectorAll(".tabbed-set")){var labels=set.querySelector(".tabbed-labels");for(var tab of tabs)for(var label of labels.getElementsByTagName("label"))if(label.innerText.trim()===tab){var input=document.getElementById(label.htmlFor);input.checked=!0;continue e}}
var target=document.getElementById(location.hash.slice(1));target&&target.name&&(target.checked=target.name.startsWith("\_\_tabbed\_"))

Back to top

[Next

Getting started](getting-started/)

Made with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

{"annotate": null, "base": ".", "features": ["navigation.path", "navigation.instant", "navigation.instant.prefetch", "navigation.instant.progress", "navigation.sections", "navigation.indexes", "navigation.tracking", "content.code.annotate", "toc.follow", "navigation.footer", "navigation.top", "content.code.copy", "content.tabs.link"], "search": "assets/javascripts/workers/search.2c215733.min.js", "tags": null, "translations": {"clipboard.copied": "Copied to clipboard", "clipboard.copy": "Copy to clipboard", "search.result.more.one": "1 more on this page", "search.result.more.other": "# more on this page", "search.result.none": "No matching documents", "search.result.one": "1 matching document", "search.result.other": "# matching documents", "search.result.placeholder": "Type to start searching", "search.result.term.missing": "Missing", "select.version": "Select version"}, "version": null}