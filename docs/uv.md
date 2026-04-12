# uv Package Manager


---

## 1. An extremely fast Python package and project manager, written in Rust.

*Installing [Trio](https://trio.readthedocs.io/)'s dependencies with a warm cache.*

## 

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

## 

Install uv with our official standalone installer:

```
$ curl-LsSfhttps://astral.sh/uv/install.sh|sh
```

```
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, check out the [first steps](getting-started/first-steps/) or read on for a brief overview.

Tip

uv may also be installed with pip, Homebrew, and more. See all of the methods on the
[installation page](getting-started/installation/).

## 

uv manages project dependencies and environments, with support for lockfiles, workspaces, and more,
similar to `rye` or `poetry`:

```
$ uvinitexample
Initialized project `example` at `/home/user/example`

$ cdexample

$ uvaddruff
Creating virtual environment at: .venv
Resolved 2 packages in 170ms
   Built example @ file:///home/user/example
Prepared 2 packages in 627ms
Installed 2 packages in 1ms
 + example==0.1.0 (from file:///home/user/example)
 + ruff==0.5.4

$ uvrunruffcheck
All checks passed!

$ uvlock
Resolved 2 packages in 0.33ms

$ uvsync
Resolved 2 packages in 0.70ms
Checked 1 package in 0.02ms
```

See the [project guide](guides/projects/) to get started.

uv also supports building and publishing projects, even if they're not managed with uv. See the
[packaging guide](guides/package/) to learn more.

## 

uv manages dependencies and environments for single-file scripts.

Create a new script and add inline metadata declaring its dependencies:

```
$ echo'import requests; print(requests.get("https://astral.sh"))'>example.py

$ uvadd--scriptexample.pyrequests
Updated `example.py`
```

Then, run the script in an isolated virtual environment:

```
$ uvrunexample.py
Reading inline script metadata from: example.py
Installed 5 packages in 12ms
<Response [200]>
```

See the [scripts guide](guides/scripts/) to get started.

## 

uv executes and installs command-line tools provided by Python packages, similar to `pipx`.

Run a tool in an ephemeral environment using `uvx` (an alias for `uv tool run`):

```
$ uvxpycowsay'hello world!'
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
$ uvtoolinstallruff
Resolved 1 package in 6ms
Installed 1 package in 2ms
 + ruff==0.5.4
Installed 1 executable: ruff

$ ruff--version
ruff 0.5.4
```

See the [tools guide](guides/tools/) to get started.

## 

uv installs Python and allows quickly switching between versions.

Install multiple Python versions:

```
$ uvpythoninstall3.103.113.12
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
$ uvvenv--python3.12.0
Using CPython 3.12.0
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

$ uvrun--python[email protected]--python
Python 3.8.16 (a9dbdca6fc3286b0addd2240f11d97d8e8de187a, Dec 29 2022, 11:45:30)
[PyPy 7.3.11 with GCC Apple LLVM 13.1.6 (clang-1316.0.21.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>>
```

Use a specific Python version in the current directory:

```
$ uvpythonpin3.11
Pinned `.python-version` to `3.11`
```

See the [installing Python guide](guides/install-python/) to get started.

## 

uv provides a drop-in replacement for common `pip`, `pip-tools`, and `virtualenv` commands.

uv extends their interfaces with advanced features, such as dependency version overrides,
platform-independent resolutions, reproducible resolutions, alternative resolution strategies, and
more.

Migrate to uv without changing your existing workflows — and experience a 10-100x speedup — with the
`uv pip` interface.

Compile requirements into a platform-independent requirements file:

```
$ uvpipcompilerequirements.in\
--universal\
--output-filerequirements.txt
Resolved 43 packages in 12ms
```

Create a virtual environment:

```
$ uvvenv
Using CPython 3.12.3
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

Install the locked requirements:

```
$ uvpipsyncrequirements.txt
Resolved 43 packages in 11ms
Installed 43 packages in 208ms
 + babel==2.15.0
 + black==24.4.2
 + certifi==2024.7.4
 ...
```

See the [pip interface documentation](pip/) to get started.

## 

See the [first steps](getting-started/first-steps/) or jump straight to the
[guides](guides/) to start using uv.

---

## 2. uv supports managing Python projects, which define their dependencies in a `pyproject.toml` file.

## 

You can create a new Python project using the `uv init` command:

```
$ uvinithello-world
$ cdhello-world
```

Alternatively, you can initialize a project in the working directory:

```
$ mkdirhello-world
$ cdhello-world
$ uvinit
```

uv will create the following files:

```
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

The `main.py` file contains a simple "Hello world" program. Try it out with `uv run`:

```
$ uvrunmain.py
Hello from hello-world!
```

## 

A project consists of a few important parts that work together and allow uv to manage your project.
In addition to the files created by `uv init`, uv will create a virtual environment and `uv.lock`
file in the root of your project the first time you run a project command, i.e., `uv run`,
`uv sync`, or `uv lock`.

A complete listing would look like:

```
.
├── .venv
│   ├── bin
│   ├── lib
│   └── pyvenv.cfg
├── .python-version
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock
```

### 

The `pyproject.toml` contains metadata about your project:

pyproject.toml

```
[project]
name="hello-world"
version="0.1.0"
description="Add your description here"
readme="README.md"
dependencies=[]
```

You'll use this file to specify dependencies, as well as details about the project such as its
description or license. You can edit this file manually, or use commands like `uv add` and
`uv remove` to manage your project from the terminal.

Tip

See the official [`pyproject.toml` guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
for more details on getting started with the `pyproject.toml` format.

You'll also use this file to specify uv [configuration options](../../concepts/configuration-files/)
in a [`[tool.uv]`](../../reference/settings/) section.

### 

The `.python-version` file contains the project's default Python version. This file tells uv which
Python version to use when creating the project's virtual environment.

### 

The `.venv` folder contains your project's virtual environment, a Python environment that is
isolated from the rest of your system. This is where uv will install your project's dependencies.

See the [project environment](../../concepts/projects/layout/#the-project-environment) documentation
for more details.

### 

`uv.lock` is a cross-platform lockfile that contains exact information about your project's
dependencies. Unlike the `pyproject.toml` which is used to specify the broad requirements of your
project, the lockfile contains the exact resolved versions that are installed in the project
environment. This file should be checked into version control, allowing for consistent and
reproducible installations across machines.

`uv.lock` is a human-readable TOML file but is managed by uv and should not be edited manually.

See the [lockfile](../../concepts/projects/layout/#the-lockfile) documentation for more details.

## 

You can add dependencies to your `pyproject.toml` with the `uv add` command. This will also update
the lockfile and project environment:

```
$ uvaddrequests
```

You can also specify version constraints or alternative sources:

```
$ # Specify a version constraint
$ uvadd'requests==2.31.0'

$ # Add a git dependency
$ uvaddgit+https://github.com/psf/requests
```

If you're migrating from a `requirements.txt` file, you can use `uv add` with the `-r` flag to add
all dependencies from the file:

```
$ # Add all dependencies from `requirements.txt`.
$ uvadd-rrequirements.txt-cconstraints.txt
```

To remove a package, you can use `uv remove`:

```
$ uvremoverequests
```

To upgrade a package, run `uv lock` with the `--upgrade-package` flag:

```
$ uvlock--upgrade-packagerequests
```

The `--upgrade-package` flag will attempt to update the specified package to the latest compatible
version, while keeping the rest of the lockfile intact.

See the documentation on [managing dependencies](../../concepts/projects/dependencies/) for more
details.

## 

The `uv version` command can be used to read your package's version.

To get the version of your package, run `uv version`:

```
$ uvversion
hello-world 0.7.0
```

To get the version without the package name, use the `--short` option:

```
$ uvversion--short
0.7.0
```

To get version information in a JSON format, use the `--output-format json` option:

```
$ uvversion--output-formatjson
{
    "package_name": "hello-world",
    "version": "0.7.0",
    "commit_info": null
}
```

See the [publishing guide](../package/#updating-your-version) for details on updating your package
version.

## 

`uv run` can be used to run arbitrary scripts or commands in your project environment.

Prior to every `uv run` invocation, uv will verify that the lockfile is up-to-date with the
`pyproject.toml`, and that the environment is up-to-date with the lockfile, keeping your project
in-sync without the need for manual intervention. `uv run` guarantees that your command is run in an
environment with all required dependencies at their locked versions.

Note

`uv run` does not remove extraneous packages (those not in the lockfile) from the environment
by default. See [handling of extraneous packages](../../concepts/projects/sync/#handling-of-extraneous-packages)
for details.

For example, to use `flask`:

```
$ uvaddflask
$ uvrun--flaskrun-p3000
```

Or, to run a script:

example.py

```
# Require a project dependency
importflask

print("hello world")
```

```
$ uvrunexample.py
```

Alternatively, you can use `uv sync` to manually update the environment then activate it before
executing a command:

```
$ uvsync
$ source.venv/bin/activate
$ flaskrun-p3000
$ pythonexample.py
```

```
PS> uv sync
PS> .venv\Scripts\activate
PS> flask run -p 3000
PS> python example.py
```

Note

The virtual environment must be active to run scripts and commands in the project without `uv run`. Virtual environment activation differs per shell and platform.

See the documentation on [running commands and scripts](../../concepts/projects/run/) in projects for
more details.

## 

`uv build` can be used to build source distributions and binary distributions (wheel) for your
project.

By default, `uv build` will build the project in the current directory, and place the built
artifacts in a `dist/` subdirectory:

```
$ uvbuild
$ lsdist/
hello-world-0.1.0-py3-none-any.whl
hello-world-0.1.0.tar.gz
```

See the documentation on [building projects](../../concepts/projects/build/) for more details.

## 

To learn more about working on projects with uv, see the
[projects concept](../../concepts/projects/) page and the
[command reference](../../reference/cli/#uv).

Or, read on to learn how to
[export a uv lockfile to different formats](../../concepts/projects/export/).

---

## Bibliography

1. [An extremely fast Python package and project manager, written in Rust.](https://docs.astral.sh/uv/)
2. [uv supports managing Python projects, which define their dependencies in a `pyproject.toml` file.](https://docs.astral.sh/uv/guides/projects/)