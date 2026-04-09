What’s New In Python 3.12 — Python 3.12.13 documentation

@media only screen {
table.full-width-table {
width: 100%;
}
}

Theme
Auto
Light
Dark

### [Table of Contents](../contents.html)

* [What’s New In Python 3.12](#)
  + [Summary – Release highlights](#summary-release-highlights)
  + [New Features](#new-features)
    - [PEP 695: Type Parameter Syntax](#pep-695-type-parameter-syntax)
    - [PEP 701: Syntactic formalization of f-strings](#pep-701-syntactic-formalization-of-f-strings)
    - [PEP 684: A Per-Interpreter GIL](#pep-684-a-per-interpreter-gil)
    - [PEP 669: Low impact monitoring for CPython](#pep-669-low-impact-monitoring-for-cpython)
    - [PEP 688: Making the buffer protocol accessible in Python](#pep-688-making-the-buffer-protocol-accessible-in-python)
    - [PEP 709: Comprehension inlining](#pep-709-comprehension-inlining)
    - [Improved Error Messages](#improved-error-messages)
  + [New Features Related to Type Hints](#new-features-related-to-type-hints)
    - [PEP 692: Using `TypedDict` for more precise `**kwargs` typing](#pep-692-using-typeddict-for-more-precise-kwargs-typing)
    - [PEP 698: Override Decorator for Static Typing](#pep-698-override-decorator-for-static-typing)
  + [Other Language Changes](#other-language-changes)
  + [New Modules](#new-modules)
  + [Improved Modules](#improved-modules)
    - [array](#array)
    - [asyncio](#asyncio)
    - [calendar](#calendar)
    - [csv](#csv)
    - [dis](#dis)
    - [fractions](#fractions)
    - [importlib.resources](#importlib-resources)
    - [inspect](#inspect)
    - [itertools](#itertools)
    - [math](#math)
    - [os](#os)
    - [os.path](#os-path)
    - [pathlib](#pathlib)
    - [platform](#platform)
    - [pdb](#pdb)
    - [random](#random)
    - [shutil](#shutil)
    - [sqlite3](#sqlite3)
    - [statistics](#statistics)
    - [sys](#sys)
    - [tempfile](#tempfile)
    - [threading](#threading)
    - [tkinter](#tkinter)
    - [tokenize](#tokenize)
    - [types](#types)
    - [typing](#typing)
    - [unicodedata](#unicodedata)
    - [unittest](#unittest)
    - [uuid](#uuid)
  + [Optimizations](#optimizations)
  + [CPython bytecode changes](#cpython-bytecode-changes)
  + [Demos and Tools](#demos-and-tools)
  + [Deprecated](#deprecated)
    - [Pending Removal in Python 3.13](#pending-removal-in-python-3-13)
    - [Pending Removal in Python 3.14](#pending-removal-in-python-3-14)
    - [Pending Removal in Python 3.15](#pending-removal-in-python-3-15)
    - [Pending Removal in Python 3.16](#pending-removal-in-python-3-16)
    - [Pending Removal in Future Versions](#pending-removal-in-future-versions)
  + [Removed](#removed)
    - [asynchat and asyncore](#asynchat-and-asyncore)
    - [configparser](#configparser)
    - [distutils](#distutils)
    - [ensurepip](#ensurepip)
    - [enum](#enum)
    - [ftplib](#ftplib)
    - [gzip](#gzip)
    - [hashlib](#hashlib)
    - [importlib](#importlib)
    - [imp](#imp)
    - [io](#io)
    - [locale](#locale)
    - [smtpd](#smtpd)
    - [sqlite3](#id2)
    - [ssl](#ssl)
    - [unittest](#id3)
    - [webbrowser](#webbrowser)
    - [xml.etree.ElementTree](#xml-etree-elementtree)
    - [zipimport](#zipimport)
    - [Others](#others)
  + [Porting to Python 3.12](#porting-to-python-3-12)
    - [Changes in the Python API](#changes-in-the-python-api)
  + [Build Changes](#build-changes)
  + [C API Changes](#c-api-changes)
    - [New Features](#id4)
    - [Porting to Python 3.12](#id5)
    - [Deprecated](#id6)
      * [Pending Removal in Python 3.14](#id7)
      * [Pending Removal in Python 3.15](#id8)
      * [Pending Removal in Future Versions](#id9)
    - [Removed](#id10)
  + [Notable changes in 3.12.4](#notable-changes-in-3-12-4)
    - [ipaddress](#ipaddress)
  + [Notable changes in 3.12.5](#notable-changes-in-3-12-5)
    - [email](#email)
  + [Notable changes in 3.12.6](#notable-changes-in-3-12-6)
    - [email](#id11)
  + [Notable changes in 3.12.8](#notable-changes-in-3-12-8)
    - [sys](#id12)
  + [Notable changes in 3.12.10](#notable-changes-in-3-12-10)
    - [os.path](#id13)
    - [tarfile](#tarfile)

#### Previous topic

[What’s New in Python](index.html "previous chapter")

#### Next topic

[What’s New In Python 3.11](3.11.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/whatsnew/3.12.rst)

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](3.11.html "What’s New In Python 3.11") |
* [previous](index.html "What’s New in Python") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [What’s New in Python](index.html) »
* What’s New In Python 3.12
* |
* Theme
  Auto
  Light
  Dark
   |

# What’s New In Python 3.12[¶](#what-s-new-in-python-3-12 "Link to this heading")

Editor:
:   Adam Turner

This article explains the new features in Python 3.12, compared to 3.11.
Python 3.12 was released on October 2, 2023.
For full details, see the [changelog](changelog.html#changelog).

See also

[**PEP 693**](https://peps.python.org/pep-0693/) – Python 3.12 Release Schedule

## Summary – Release highlights[¶](#summary-release-highlights "Link to this heading")

Python 3.12 is a stable release of the Python programming language,
with a mix of changes to the language and the standard library.
The library changes focus on cleaning up deprecated APIs, usability, and correctness.
Of note, the `distutils` package has been removed from the standard library.
Filesystem support in [`os`](../library/os.html#module-os "os: Miscellaneous operating system interfaces.") and [`pathlib`](../library/pathlib.html#module-pathlib "pathlib: Object-oriented filesystem paths") has seen a number of improvements,
and several modules have better performance.

The language changes focus on usability,
as [f-strings](../glossary.html#term-f-string) have had many limitations removed
and ‘Did you mean …’ suggestions continue to improve.
The new [type parameter syntax](#whatsnew312-pep695)
and [`type`](../reference/simple_stmts.html#type) statement improve ergonomics for using [generic types](../glossary.html#term-generic-type) and [type aliases](../glossary.html#term-type-alias) with static type checkers.

This article doesn’t attempt to provide a complete specification of all new features,
but instead gives a convenient overview.
For full details, you should refer to the documentation,
such as the [Library Reference](../library/index.html#library-index)
and [Language Reference](../reference/index.html#reference-index).
If you want to understand the complete implementation and design rationale for a change,
refer to the PEP for a particular new feature;
but note that PEPs usually are not kept up-to-date
once a feature has been fully implemented.

---

New syntax features:

* [PEP 695](#whatsnew312-pep695), type parameter syntax and the [`type`](../reference/simple_stmts.html#type) statement

New grammar features:

* [PEP 701](#whatsnew312-pep701), [f-strings](../glossary.html#term-f-string) in the grammar

Interpreter improvements:

* [PEP 684](#whatsnew312-pep684), a unique per-interpreter [GIL](../glossary.html#term-global-interpreter-lock)
* [PEP 669](#whatsnew312-pep669), low impact monitoring
* [Improved ‘Did you mean …’ suggestions](#improved-error-messages)
  for [`NameError`](../library/exceptions.html#NameError "NameError"), [`ImportError`](../library/exceptions.html#ImportError "ImportError"), and [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError") exceptions

Python data model improvements:

* [PEP 688](#whatsnew312-pep688), using the [buffer protocol](../c-api/buffer.html#bufferobjects) from Python

Significant improvements in the standard library:

* The [`pathlib.Path`](../library/pathlib.html#pathlib.Path "pathlib.Path") class now supports subclassing
* The [`os`](../library/os.html#module-os "os: Miscellaneous operating system interfaces.") module received several improvements for Windows support
* A [command-line interface](../library/sqlite3.html#sqlite3-cli) has been added to the
  [`sqlite3`](../library/sqlite3.html#module-sqlite3 "sqlite3: A DB-API 2.0 implementation using SQLite 3.x.") module
* [`isinstance()`](../library/functions.html#isinstance "isinstance") checks against [`runtime-checkable protocols`](../library/typing.html#typing.runtime_checkable "typing.runtime_checkable") enjoy a speed up of between two and 20 times
* The [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") package has had a number of performance improvements,
  with some benchmarks showing a 75% speed up.
* A [command-line interface](../library/uuid.html#uuid-cli) has been added to the
  [`uuid`](../library/uuid.html#module-uuid "uuid: UUID objects (universally unique identifiers) according to RFC 4122") module
* Due to the changes in [PEP 701](#whatsnew312-pep701),
  producing tokens via the [`tokenize`](../library/tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module is up to 64% faster.

Security improvements:

* Replace the builtin [`hashlib`](../library/hashlib.html#module-hashlib "hashlib: Secure hash and message digest algorithms.") implementations of
  SHA1, SHA3, SHA2-384, SHA2-512, and MD5 with formally verified code from the
  [HACL\*](https://github.com/hacl-star/hacl-star/) project.
  These builtin implementations remain as fallbacks that are only used when
  OpenSSL does not provide them.

C API improvements:

* [PEP 697](#whatsnew312-pep697), unstable C API tier
* [PEP 683](#whatsnew312-pep683), immortal objects

CPython implementation improvements:

* [PEP 709](#whatsnew312-pep709), comprehension inlining
* [CPython support](../howto/perf_profiling.html#perf-profiling) for the Linux `perf` profiler
* Implement stack overflow protection on supported platforms

New typing features:

* [PEP 692](#whatsnew312-pep692), using [`TypedDict`](../library/typing.html#typing.TypedDict "typing.TypedDict") to
  annotate [\*\*kwargs](../glossary.html#term-argument)
* [PEP 698](#whatsnew312-pep698), [`typing.override()`](../library/typing.html#typing.override "typing.override") decorator

Important deprecations, removals or restrictions:

* [**PEP 623**](https://peps.python.org/pep-0623/): Remove `wstr` from Unicode objects in Python’s C API,
  reducing the size of every [`str`](../library/stdtypes.html#str "str") object by at least 8 bytes.
* [**PEP 632**](https://peps.python.org/pep-0632/): Remove the `distutils` package.
  See [**the migration guide**](https://peps.python.org/pep-0632/#migration-advice)
  for advice replacing the APIs it provided.
  The third-party [Setuptools](https://setuptools.pypa.io/en/latest/deprecated/distutils-legacy.html)
  package continues to provide `distutils`,
  if you still require it in Python 3.12 and beyond.
* [gh-95299](https://github.com/python/cpython/issues/95299): Do not pre-install `setuptools` in virtual environments
  created with [`venv`](../library/venv.html#module-venv "venv: Creation of virtual environments.").
  This means that `distutils`, `setuptools`, `pkg_resources`,
  and `easy_install` will no longer available by default; to access these
  run `pip install setuptools` in the [activated](../library/venv.html#venv-explanation)
  virtual environment.
* The `asynchat`, `asyncore`, and `imp` modules have been
  removed, along with several [`unittest.TestCase`](../library/unittest.html#unittest.TestCase "unittest.TestCase")
  [method aliases](#unittest-testcase-removed-aliases).

## New Features[¶](#new-features "Link to this heading")

### PEP 695: Type Parameter Syntax[¶](#pep-695-type-parameter-syntax "Link to this heading")

Generic classes and functions under [**PEP 484**](https://peps.python.org/pep-0484/) were declared using a verbose syntax
that left the scope of type parameters unclear and required explicit declarations of
variance.

[**PEP 695**](https://peps.python.org/pep-0695/) introduces a new, more compact and explicit way to create
[generic classes](../reference/compound_stmts.html#generic-classes) and [functions](../reference/compound_stmts.html#generic-functions):

```
def max[T](args: Iterable[T]) -> T:
    ...

class list[T]:
    def __getitem__(self, index: int, /) -> T:
        ...

    def append(self, element: T) -> None:
        ...
```

In addition, the PEP introduces a new way to declare [type aliases](../library/typing.html#type-aliases)
using the [`type`](../reference/simple_stmts.html#type) statement, which creates an instance of
[`TypeAliasType`](../library/typing.html#typing.TypeAliasType "typing.TypeAliasType"):

```
type Point = tuple[float, float]
```

Type aliases can also be [generic](../reference/compound_stmts.html#generic-type-aliases):

```
type Point[T] = tuple[T, T]
```

The new syntax allows declaring [`TypeVarTuple`](../library/typing.html#typing.TypeVarTuple "typing.TypeVarTuple")
and [`ParamSpec`](../library/typing.html#typing.ParamSpec "typing.ParamSpec") parameters, as well as [`TypeVar`](../library/typing.html#typing.TypeVar "typing.TypeVar")
parameters with bounds or constraints:

```
type IntFunc[**P] = Callable[P, int]  # ParamSpec
type LabeledTuple[*Ts] = tuple[str, *Ts]  # TypeVarTuple
type HashableSequence[T: Hashable] = Sequence[T]  # TypeVar with bound
type IntOrStrSequence[T: (int, str)] = Sequence[T]  # TypeVar with constraints
```

The value of type aliases and the bound and constraints of type variables
created through this syntax are evaluated only on demand (see
[lazy evaluation](../reference/executionmodel.html#lazy-evaluation)). This means type aliases are able to
refer to other types defined later in the file.

Type parameters declared through a type parameter list are visible within the
scope of the declaration and any nested scopes, but not in the outer scope. For
example, they can be used in the type annotations for the methods of a generic
class or in the class body. However, they cannot be used in the module scope after
the class is defined. See [Type parameter lists](../reference/compound_stmts.html#type-params) for a detailed description of the
runtime semantics of type parameters.

In order to support these scoping semantics, a new kind of scope is introduced,
the [annotation scope](../reference/executionmodel.html#annotation-scopes). Annotation scopes behave for the
most part like function scopes, but interact differently with enclosing class scopes.
In Python 3.13, [annotations](../glossary.html#term-annotation) will also be evaluated in
annotation scopes.

See [**PEP 695**](https://peps.python.org/pep-0695/) for more details.

(PEP written by Eric Traut. Implementation by Jelle Zijlstra, Eric Traut,
and others in [gh-103764](https://github.com/python/cpython/issues/103764).)

### PEP 701: Syntactic formalization of f-strings[¶](#pep-701-syntactic-formalization-of-f-strings "Link to this heading")

[**PEP 701**](https://peps.python.org/pep-0701/) lifts some restrictions on the usage of [f-strings](../glossary.html#term-f-string).
Expression components inside f-strings can now be any valid Python expression,
including strings reusing the same quote as the containing f-string,
multi-line expressions, comments, backslashes, and unicode escape sequences.
Let’s cover these in detail:

* Quote reuse: in Python 3.11, reusing the same quotes as the enclosing f-string
  raises a [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError"), forcing the user to either use other available
  quotes (like using double quotes or triple quotes if the f-string uses single
  quotes). In Python 3.12, you can now do things like this:

  ```
  >>> songs = ['Take me back to Eden', 'Alkaline', 'Ascensionism']
  >>> f"This is the playlist: {", ".join(songs)}"
  'This is the playlist: Take me back to Eden, Alkaline, Ascensionism'
  ```

  Note that before this change there was no explicit limit in how f-strings can
  be nested, but the fact that string quotes cannot be reused inside the
  expression component of f-strings made it impossible to nest f-strings
  arbitrarily. In fact, this is the most nested f-string that could be written:

  ```
  >>> f"""{f'''{f'{f"{1+1}"}'}'''}"""
  '2'
  ```

  As now f-strings can contain any valid Python expression inside expression
  components, it is now possible to nest f-strings arbitrarily:

  ```
  >>> f"{f"{f"{f"{f"{f"{1+1}"}"}"}"}"}"
  '2'
  ```
* Multi-line expressions and comments: In Python 3.11, f-string expressions
  must be defined in a single line, even if the expression within the f-string
  could normally span multiple lines
  (like literal lists being defined over multiple lines),
  making them harder to read. In Python 3.12 you can now define f-strings
  spanning multiple lines, and add inline comments:

  ```
  >>> f"This is the playlist: {", ".join([
  ...     'Take me back to Eden',  # My, my, those eyes like fire
  ...     'Alkaline',              # Not acid nor alkaline
  ...     'Ascensionism'           # Take to the broken skies at last
  ... ])}"
  'This is the playlist: Take me back to Eden, Alkaline, Ascensionism'
  ```
* Backslashes and unicode characters: before Python 3.12 f-string expressions
  couldn’t contain any `\` character. This also affected unicode [escape
  sequences](../reference/lexical_analysis.html#escape-sequences) (such as `\N{snowman}`) as these contain
  the `\N` part that previously could not be part of expression components of
  f-strings. Now, you can define expressions like this:

  ```
  >>> print(f"This is the playlist: {"\n".join(songs)}")
  This is the playlist: Take me back to Eden
  Alkaline
  Ascensionism
  >>> print(f"This is the playlist: {"\N{BLACK HEART SUIT}".join(songs)}")
  This is the playlist: Take me back to Eden♥Alkaline♥Ascensionism
  ```

See [**PEP 701**](https://peps.python.org/pep-0701/) for more details.

As a positive side-effect of how this feature has been implemented (by parsing f-strings
with [**the PEG parser**](https://peps.python.org/pep-0617/)), now error messages for f-strings are more precise
and include the exact location of the error. For example, in Python 3.11, the following
f-string raises a [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError"):

```
>>> my_string = f"{x z y}" + f"{1 + 1}"
  File "<stdin>", line 1
    (x z y)
     ^^^
SyntaxError: f-string: invalid syntax. Perhaps you forgot a comma?
```

but the error message doesn’t include the exact location of the error within the line and
also has the expression artificially surrounded by parentheses. In Python 3.12, as f-strings
are parsed with the PEG parser, error messages can be more precise and show the entire line:

```
>>> my_string = f"{x z y}" + f"{1 + 1}"
  File "<stdin>", line 1
    my_string = f"{x z y}" + f"{1 + 1}"
                   ^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

(Contributed by Pablo Galindo, Batuhan Taskaya, Lysandros Nikolaou, Cristián
Maureira-Fredes and Marta Gómez in [gh-102856](https://github.com/python/cpython/issues/102856). PEP written by Pablo Galindo,
Batuhan Taskaya, Lysandros Nikolaou and Marta Gómez).

### PEP 684: A Per-Interpreter GIL[¶](#pep-684-a-per-interpreter-gil "Link to this heading")

[**PEP 684**](https://peps.python.org/pep-0684/) introduces a per-interpreter [GIL](../glossary.html#term-global-interpreter-lock),
so that sub-interpreters may now be created with a unique GIL per interpreter.
This allows Python programs to take full advantage of multiple CPU
cores. This is currently only available through the C-API,
though a Python API is [**anticipated for 3.13**](https://peps.python.org/pep-0554/).

Use the new [`Py_NewInterpreterFromConfig()`](../c-api/init.html#c.Py_NewInterpreterFromConfig "Py_NewInterpreterFromConfig") function to
create an interpreter with its own GIL:

```
PyInterpreterConfig config = {
    .check_multi_interp_extensions = 1,
    .gil = PyInterpreterConfig_OWN_GIL,
};
PyThreadState *tstate = NULL;
PyStatus status = Py_NewInterpreterFromConfig(&tstate, &config);
if (PyStatus_Exception(status)) {
    return -1;
}
/* The new interpreter is now active in the current thread. */
```

For further examples how to use the C-API for sub-interpreters with a
per-interpreter GIL, see [Modules/\_xxsubinterpretersmodule.c](https://github.com/python/cpython/tree/3.12/Modules/_xxsubinterpretersmodule.c).

(Contributed by Eric Snow in [gh-104210](https://github.com/python/cpython/issues/104210), etc.)

### PEP 669: Low impact monitoring for CPython[¶](#pep-669-low-impact-monitoring-for-cpython "Link to this heading")

[**PEP 669**](https://peps.python.org/pep-0669/) defines a new [`API`](../library/sys.monitoring.html#module-sys.monitoring "sys.monitoring: Access and control event monitoring") for profilers,
debuggers, and other tools to monitor events in CPython.
It covers a wide range of events, including calls,
returns, lines, exceptions, jumps, and more.
This means that you only pay for what you use, providing support
for near-zero overhead debuggers and coverage tools.
See [`sys.monitoring`](../library/sys.monitoring.html#module-sys.monitoring "sys.monitoring: Access and control event monitoring") for details.

(Contributed by Mark Shannon in [gh-103082](https://github.com/python/cpython/issues/103082).)

### PEP 688: Making the buffer protocol accessible in Python[¶](#pep-688-making-the-buffer-protocol-accessible-in-python "Link to this heading")

[**PEP 688**](https://peps.python.org/pep-0688/) introduces a way to use the [buffer protocol](../c-api/buffer.html#bufferobjects)
from Python code. Classes that implement the [`__buffer__()`](../reference/datamodel.html#object.__buffer__ "object.__buffer__") method
are now usable as buffer types.

The new [`collections.abc.Buffer`](../library/collections.abc.html#collections.abc.Buffer "collections.abc.Buffer") ABC provides a standard
way to represent buffer objects, for example in type annotations.
The new [`inspect.BufferFlags`](../library/inspect.html#inspect.BufferFlags "inspect.BufferFlags") enum represents the flags that
can be used to customize buffer creation.
(Contributed by Jelle Zijlstra in [gh-102500](https://github.com/python/cpython/issues/102500).)

### PEP 709: Comprehension inlining[¶](#pep-709-comprehension-inlining "Link to this heading")

Dictionary, list, and set comprehensions are now inlined, rather than creating a
new single-use function object for each execution of the comprehension. This
speeds up execution of a comprehension by up to two times.
See [**PEP 709**](https://peps.python.org/pep-0709/) for further details.

Comprehension iteration variables remain isolated and don’t overwrite a
variable of the same name in the outer scope, nor are they visible after the
comprehension. Inlining does result in a few visible behavior changes:

* There is no longer a separate frame for the comprehension in tracebacks,
  and tracing/profiling no longer shows the comprehension as a function call.
* The [`symtable`](../library/symtable.html#module-symtable "symtable: Interface to the compiler's internal symbol tables.") module will no longer produce child symbol tables for each
  comprehension; instead, the comprehension’s locals will be included in the
  parent function’s symbol table.
* Calling [`locals()`](../library/functions.html#locals "locals") inside a comprehension now includes variables
  from outside the comprehension, and no longer includes the synthetic `.0`
  variable for the comprehension “argument”.
* A comprehension iterating directly over `locals()` (e.g. `[k for k in
  locals()]`) may see “RuntimeError: dictionary changed size during iteration”
  when run under tracing (e.g. code coverage measurement). This is the same
  behavior already seen in e.g. `for k in locals():`. To avoid the error, first
  create a list of keys to iterate over: `keys = list(locals()); [k for k in
  keys]`.

(Contributed by Carl Meyer and Vladimir Matveev in [**PEP 709**](https://peps.python.org/pep-0709/).)

### Improved Error Messages[¶](#improved-error-messages "Link to this heading")

* Modules from the standard library are now potentially suggested as part of
  the error messages displayed by the interpreter when a [`NameError`](../library/exceptions.html#NameError "NameError") is
  raised to the top level. (Contributed by Pablo Galindo in [gh-98254](https://github.com/python/cpython/issues/98254).)

  ```
  >>> sys.version_info
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  NameError: name 'sys' is not defined. Did you forget to import 'sys'?
  ```
* Improve the error suggestion for [`NameError`](../library/exceptions.html#NameError "NameError") exceptions for instances.
  Now if a [`NameError`](../library/exceptions.html#NameError "NameError") is raised in a method and the instance has an
  attribute that’s exactly equal to the name in the exception, the suggestion
  will include `self.<NAME>` instead of the closest match in the method
  scope. (Contributed by Pablo Galindo in [gh-99139](https://github.com/python/cpython/issues/99139).)

  ```
  >>> class A:
  ...    def __init__(self):
  ...        self.blech = 1
  ...
  ...    def foo(self):
  ...        somethin = blech
  ...
  >>> A().foo()
  Traceback (most recent call last):
    File "<stdin>", line 1
      somethin = blech
                 ^^^^^
  NameError: name 'blech' is not defined. Did you mean: 'self.blech'?
  ```
* Improve the [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError") error message when the user types `import x
  from y` instead of `from y import x`. (Contributed by Pablo Galindo in [gh-98931](https://github.com/python/cpython/issues/98931).)

  ```
  >>> import a.y.z from b.y.z
  Traceback (most recent call last):
    File "<stdin>", line 1
      import a.y.z from b.y.z
      ^^^^^^^^^^^^^^^^^^^^^^^
  SyntaxError: Did you mean to use 'from ... import ...' instead?
  ```
* [`ImportError`](../library/exceptions.html#ImportError "ImportError") exceptions raised from failed `from <module> import
  <name>` statements now include suggestions for the value of `<name>` based on the
  available names in `<module>`. (Contributed by Pablo Galindo in [gh-91058](https://github.com/python/cpython/issues/91058).)

  ```
  >>> from collections import chainmap
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ImportError: cannot import name 'chainmap' from 'collections'. Did you mean: 'ChainMap'?
  ```

## New Features Related to Type Hints[¶](#new-features-related-to-type-hints "Link to this heading")

This section covers major changes affecting [**type hints**](https://peps.python.org/pep-0484/) and
the [`typing`](../library/typing.html#module-typing "typing: Support for type hints (see :pep:`484`).") module.

### PEP 692: Using `TypedDict` for more precise `**kwargs` typing[¶](#pep-692-using-typeddict-for-more-precise-kwargs-typing "Link to this heading")

Typing `**kwargs` in a function signature as introduced by [**PEP 484**](https://peps.python.org/pep-0484/) allowed
for valid annotations only in cases where all of the `**kwargs` were of the
same type.

[**PEP 692**](https://peps.python.org/pep-0692/) specifies a more precise way of typing `**kwargs` by relying on
typed dictionaries:

```
from typing import TypedDict, Unpack

class Movie(TypedDict):
  name: str
  year: int

def foo(**kwargs: Unpack[Movie]): ...
```

See [**PEP 692**](https://peps.python.org/pep-0692/) for more details.

(Contributed by Franek Magiera in [gh-103629](https://github.com/python/cpython/issues/103629).)

### PEP 698: Override Decorator for Static Typing[¶](#pep-698-override-decorator-for-static-typing "Link to this heading")

A new decorator [`typing.override()`](../library/typing.html#typing.override "typing.override") has been added to the [`typing`](../library/typing.html#module-typing "typing: Support for type hints (see :pep:`484`).")
module. It indicates to type checkers that the method is intended to override
a method in a superclass. This allows type checkers to catch mistakes where
a method that is intended to override something in a base class
does not in fact do so.

Example:

```
from typing import override

class Base:
  def get_color(self) -> str:
    return "blue"

class GoodChild(Base):
  @override  # ok: overrides Base.get_color
  def get_color(self) -> str:
    return "yellow"

class BadChild(Base):
  @override  # type checker error: does not override Base.get_color
  def get_colour(self) -> str:
    return "red"
```

See [**PEP 698**](https://peps.python.org/pep-0698/) for more details.

(Contributed by Steven Troxler in [gh-101561](https://github.com/python/cpython/issues/101561).)

## Other Language Changes[¶](#other-language-changes "Link to this heading")

* The parser now raises [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError") when parsing source code containing
  null bytes. (Contributed by Pablo Galindo in [gh-96670](https://github.com/python/cpython/issues/96670).)
* A backslash-character pair that is not a valid escape sequence now generates
  a [`SyntaxWarning`](../library/exceptions.html#SyntaxWarning "SyntaxWarning"), instead of [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning").
  For example, `re.compile("\d+\.\d+")` now emits a [`SyntaxWarning`](../library/exceptions.html#SyntaxWarning "SyntaxWarning")
  (`"\d"` is an invalid escape sequence, use raw strings for regular
  expression: `re.compile(r"\d+\.\d+")`).
  In a future Python version, [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError") will eventually be raised,
  instead of [`SyntaxWarning`](../library/exceptions.html#SyntaxWarning "SyntaxWarning").
  (Contributed by Victor Stinner in [gh-98401](https://github.com/python/cpython/issues/98401).)
* Octal escapes with value larger than `0o377` (ex: `"\477"`), deprecated
  in Python 3.11, now produce a [`SyntaxWarning`](../library/exceptions.html#SyntaxWarning "SyntaxWarning"), instead of
  [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning").
  In a future Python version they will be eventually a [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError").
  (Contributed by Victor Stinner in [gh-98401](https://github.com/python/cpython/issues/98401).)
* Variables used in the target part of comprehensions that are not stored to
  can now be used in assignment expressions (`:=`).
  For example, in `[(b := 1) for a, b.prop in some_iter]`, the assignment to
  `b` is now allowed. Note that assigning to variables stored to in the target
  part of comprehensions (like `a`) is still disallowed, as per [**PEP 572**](https://peps.python.org/pep-0572/).
  (Contributed by Nikita Sobolev in [gh-100581](https://github.com/python/cpython/issues/100581).)
* Exceptions raised in a class or type’s `__set_name__` method are no longer
  wrapped by a [`RuntimeError`](../library/exceptions.html#RuntimeError "RuntimeError"). Context information is added to the
  exception as a [**PEP 678**](https://peps.python.org/pep-0678/) note. (Contributed by Irit Katriel in [gh-77757](https://github.com/python/cpython/issues/77757).)
* When a `try-except*` construct handles the entire [`ExceptionGroup`](../library/exceptions.html#ExceptionGroup "ExceptionGroup")
  and raises one other exception, that exception is no longer wrapped in an
  [`ExceptionGroup`](../library/exceptions.html#ExceptionGroup "ExceptionGroup"). Also changed in version 3.11.4. (Contributed by Irit
  Katriel in [gh-103590](https://github.com/python/cpython/issues/103590).)
* The Garbage Collector now runs only on the eval breaker mechanism of the
  Python bytecode evaluation loop instead of object allocations. The GC can
  also run when [`PyErr_CheckSignals()`](../c-api/exceptions.html#c.PyErr_CheckSignals "PyErr_CheckSignals") is called so C extensions that
  need to run for a long time without executing any Python code also have a
  chance to execute the GC periodically. (Contributed by Pablo Galindo in
  [gh-97922](https://github.com/python/cpython/issues/97922).)
* All builtin and extension callables expecting boolean parameters now accept
  arguments of any type instead of just [`bool`](../library/functions.html#bool "bool") and [`int`](../library/functions.html#int "int").
  (Contributed by Serhiy Storchaka in [gh-60203](https://github.com/python/cpython/issues/60203).)
* [`memoryview`](../library/stdtypes.html#memoryview "memoryview") now supports the half-float type (the “e” format code).
  (Contributed by Donghee Na and Antoine Pitrou in [gh-90751](https://github.com/python/cpython/issues/90751).)
* [`slice`](../library/functions.html#slice "slice") objects are now hashable, allowing them to be used as dict keys and
  set items. (Contributed by Will Bradshaw, Furkan Onder, and Raymond Hettinger in [gh-101264](https://github.com/python/cpython/issues/101264).)
* [`sum()`](../library/functions.html#sum "sum") now uses Neumaier summation to improve accuracy and commutativity
  when summing floats or mixed ints and floats.
  (Contributed by Raymond Hettinger in [gh-100425](https://github.com/python/cpython/issues/100425).)
* [`ast.parse()`](../library/ast.html#ast.parse "ast.parse") now raises [`SyntaxError`](../library/exceptions.html#SyntaxError "SyntaxError") instead of [`ValueError`](../library/exceptions.html#ValueError "ValueError")
  when parsing source code containing null bytes. (Contributed by Pablo Galindo
  in [gh-96670](https://github.com/python/cpython/issues/96670).)
* The extraction methods in [`tarfile`](../library/tarfile.html#module-tarfile "tarfile: Read and write tar-format archive files."), and [`shutil.unpack_archive()`](../library/shutil.html#shutil.unpack_archive "shutil.unpack_archive"),
  have a new a *filter* argument that allows limiting tar features than may be
  surprising or dangerous, such as creating files outside the destination
  directory.
  See [tarfile extraction filters](../library/tarfile.html#tarfile-extraction-filter) for details.
  In Python 3.14, the default will switch to `'data'`.
  (Contributed by Petr Viktorin in [**PEP 706**](https://peps.python.org/pep-0706/).)
* [`types.MappingProxyType`](../library/types.html#types.MappingProxyType "types.MappingProxyType") instances are now hashable if the underlying
  mapping is hashable.
  (Contributed by Serhiy Storchaka in [gh-87995](https://github.com/python/cpython/issues/87995).)
* Add [support for the perf profiler](../howto/perf_profiling.html#perf-profiling) through the new
  environment variable [`PYTHONPERFSUPPORT`](../using/cmdline.html#envvar-PYTHONPERFSUPPORT)
  and command-line option [`-X perf`](../using/cmdline.html#cmdoption-X),
  as well as the new [`sys.activate_stack_trampoline()`](../library/sys.html#sys.activate_stack_trampoline "sys.activate_stack_trampoline"),
  [`sys.deactivate_stack_trampoline()`](../library/sys.html#sys.deactivate_stack_trampoline "sys.deactivate_stack_trampoline"),
  and [`sys.is_stack_trampoline_active()`](../library/sys.html#sys.is_stack_trampoline_active "sys.is_stack_trampoline_active") functions.
  (Design by Pablo Galindo. Contributed by Pablo Galindo and Christian Heimes
  with contributions from Gregory P. Smith [Google] and Mark Shannon
  in [gh-96123](https://github.com/python/cpython/issues/96123).)

## New Modules[¶](#new-modules "Link to this heading")

* None.

## Improved Modules[¶](#improved-modules "Link to this heading")

### array[¶](#array "Link to this heading")

* The [`array.array`](../library/array.html#array.array "array.array") class now supports subscripting, making it a
  [generic type](../glossary.html#term-generic-type). (Contributed by Jelle Zijlstra in [gh-98658](https://github.com/python/cpython/issues/98658).)

### asyncio[¶](#asyncio "Link to this heading")

* The performance of writing to sockets in [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") has been
  significantly improved. `asyncio` now avoids unnecessary copying when
  writing to sockets and uses [`sendmsg()`](../library/socket.html#socket.socket.sendmsg "socket.socket.sendmsg") if the platform
  supports it. (Contributed by Kumar Aditya in [gh-91166](https://github.com/python/cpython/issues/91166).)
* Add [`asyncio.eager_task_factory()`](../library/asyncio-task.html#asyncio.eager_task_factory "asyncio.eager_task_factory") and [`asyncio.create_eager_task_factory()`](../library/asyncio-task.html#asyncio.create_eager_task_factory "asyncio.create_eager_task_factory")
  functions to allow opting an event loop in to eager task execution,
  making some use-cases 2x to 5x faster.
  (Contributed by Jacob Bower & Itamar Oren in [gh-102853](https://github.com/python/cpython/issues/102853), [gh-104140](https://github.com/python/cpython/issues/104140), and [gh-104138](https://github.com/python/cpython/issues/104138))
* On Linux, [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") uses [`asyncio.PidfdChildWatcher`](../library/asyncio-policy.html#asyncio.PidfdChildWatcher "asyncio.PidfdChildWatcher") by default
  if [`os.pidfd_open()`](../library/os.html#os.pidfd_open "os.pidfd_open") is available and functional instead of
  [`asyncio.ThreadedChildWatcher`](../library/asyncio-policy.html#asyncio.ThreadedChildWatcher "asyncio.ThreadedChildWatcher").
  (Contributed by Kumar Aditya in [gh-98024](https://github.com/python/cpython/issues/98024).)
* The event loop now uses the best available child watcher for each platform
  ([`asyncio.PidfdChildWatcher`](../library/asyncio-policy.html#asyncio.PidfdChildWatcher "asyncio.PidfdChildWatcher") if supported and
  [`asyncio.ThreadedChildWatcher`](../library/asyncio-policy.html#asyncio.ThreadedChildWatcher "asyncio.ThreadedChildWatcher") otherwise), so manually
  configuring a child watcher is not recommended.
  (Contributed by Kumar Aditya in [gh-94597](https://github.com/python/cpython/issues/94597).)
* Add *loop\_factory* parameter to [`asyncio.run()`](../library/asyncio-runner.html#asyncio.run "asyncio.run") to allow specifying
  a custom event loop factory.
  (Contributed by Kumar Aditya in [gh-99388](https://github.com/python/cpython/issues/99388).)
* Add C implementation of [`asyncio.current_task()`](../library/asyncio-task.html#asyncio.current_task "asyncio.current_task") for 4x-6x speedup.
  (Contributed by Itamar Oren and Pranav Thulasiram Bhat in [gh-100344](https://github.com/python/cpython/issues/100344).)
* [`asyncio.iscoroutine()`](../library/asyncio-task.html#asyncio.iscoroutine "asyncio.iscoroutine") now returns `False` for generators as
  [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") does not support legacy generator-based coroutines.
  (Contributed by Kumar Aditya in [gh-102748](https://github.com/python/cpython/issues/102748).)
* [`asyncio.wait()`](../library/asyncio-task.html#asyncio.wait "asyncio.wait") and [`asyncio.as_completed()`](../library/asyncio-task.html#asyncio.as_completed "asyncio.as_completed") now accepts generators
  yielding tasks.
  (Contributed by Kumar Aditya in [gh-78530](https://github.com/python/cpython/issues/78530).)

### calendar[¶](#calendar "Link to this heading")

* Add enums [`calendar.Month`](../library/calendar.html#calendar.Month "calendar.Month") and [`calendar.Day`](../library/calendar.html#calendar.Day "calendar.Day")
  defining months of the year and days of the week.
  (Contributed by Prince Roshan in [gh-103636](https://github.com/python/cpython/issues/103636).)

### csv[¶](#csv "Link to this heading")

* Add [`csv.QUOTE_NOTNULL`](../library/csv.html#csv.QUOTE_NOTNULL "csv.QUOTE_NOTNULL") and [`csv.QUOTE_STRINGS`](../library/csv.html#csv.QUOTE_STRINGS "csv.QUOTE_STRINGS") flags to
  provide finer grained control of `None` and empty strings by
  [`csv.writer`](../library/csv.html#csv.writer "csv.writer") objects.

### dis[¶](#dis "Link to this heading")

* Pseudo instruction opcodes (which are used by the compiler but
  do not appear in executable bytecode) are now exposed in the
  [`dis`](../library/dis.html#module-dis "dis: Disassembler for Python bytecode.") module.
  [`HAVE_ARGUMENT`](../library/dis.html#opcode-HAVE_ARGUMENT) is still relevant to real opcodes,
  but it is not useful for pseudo instructions. Use the new
  [`dis.hasarg`](../library/dis.html#dis.hasarg "dis.hasarg") collection instead.
  (Contributed by Irit Katriel in [gh-94216](https://github.com/python/cpython/issues/94216).)
* Add the [`dis.hasexc`](../library/dis.html#dis.hasexc "dis.hasexc") collection to signify instructions that set
  an exception handler. (Contributed by Irit Katriel in [gh-94216](https://github.com/python/cpython/issues/94216).)

### fractions[¶](#fractions "Link to this heading")

* Objects of type [`fractions.Fraction`](../library/fractions.html#fractions.Fraction "fractions.Fraction") now support float-style
  formatting. (Contributed by Mark Dickinson in [gh-100161](https://github.com/python/cpython/issues/100161).)

### importlib.resources[¶](#importlib-resources "Link to this heading")

* [`importlib.resources.as_file()`](../library/importlib.resources.html#importlib.resources.as_file "importlib.resources.as_file") now supports resource directories.
  (Contributed by Jason R. Coombs in [gh-97930](https://github.com/python/cpython/issues/97930).)
* Rename first parameter of [`importlib.resources.files()`](../library/importlib.resources.html#importlib.resources.files "importlib.resources.files") to *anchor*.
  (Contributed by Jason R. Coombs in [gh-100598](https://github.com/python/cpython/issues/100598).)

### inspect[¶](#inspect "Link to this heading")

* Add [`inspect.markcoroutinefunction()`](../library/inspect.html#inspect.markcoroutinefunction "inspect.markcoroutinefunction") to mark sync functions that return
  a [coroutine](../glossary.html#term-coroutine) for use with [`inspect.iscoroutinefunction()`](../library/inspect.html#inspect.iscoroutinefunction "inspect.iscoroutinefunction").
  (Contributed by Carlton Gibson in [gh-99247](https://github.com/python/cpython/issues/99247).)
* Add [`inspect.getasyncgenstate()`](../library/inspect.html#inspect.getasyncgenstate "inspect.getasyncgenstate") and [`inspect.getasyncgenlocals()`](../library/inspect.html#inspect.getasyncgenlocals "inspect.getasyncgenlocals")
  for determining the current state of asynchronous generators.
  (Contributed by Thomas Krennwallner in [gh-79940](https://github.com/python/cpython/issues/79940).)
* The performance of [`inspect.getattr_static()`](../library/inspect.html#inspect.getattr_static "inspect.getattr_static") has been considerably
  improved. Most calls to the function should be at least 2x faster than they
  were in Python 3.11. (Contributed by Alex Waygood in [gh-103193](https://github.com/python/cpython/issues/103193).)

### itertools[¶](#itertools "Link to this heading")

* Add [`itertools.batched()`](../library/itertools.html#itertools.batched "itertools.batched") for collecting into even-sized
  tuples where the last batch may be shorter than the rest.
  (Contributed by Raymond Hettinger in [gh-98363](https://github.com/python/cpython/issues/98363).)

### math[¶](#math "Link to this heading")

* Add [`math.sumprod()`](../library/math.html#math.sumprod "math.sumprod") for computing a sum of products.
  (Contributed by Raymond Hettinger in [gh-100485](https://github.com/python/cpython/issues/100485).)
* Extend [`math.nextafter()`](../library/math.html#math.nextafter "math.nextafter") to include a *steps* argument
  for moving up or down multiple steps at a time. (Contributed by
  Matthias Goergens, Mark Dickinson, and Raymond Hettinger in [gh-94906](https://github.com/python/cpython/issues/94906).)

### os[¶](#os "Link to this heading")

* Add [`os.PIDFD_NONBLOCK`](../library/os.html#os.PIDFD_NONBLOCK "os.PIDFD_NONBLOCK") to open a file descriptor
  for a process with [`os.pidfd_open()`](../library/os.html#os.pidfd_open "os.pidfd_open") in non-blocking mode.
  (Contributed by Kumar Aditya in [gh-93312](https://github.com/python/cpython/issues/93312).)
* [`os.DirEntry`](../library/os.html#os.DirEntry "os.DirEntry") now includes an [`os.DirEntry.is_junction()`](../library/os.html#os.DirEntry.is_junction "os.DirEntry.is_junction")
  method to check if the entry is a junction.
  (Contributed by Charles Machalow in [gh-99547](https://github.com/python/cpython/issues/99547).)
* Add [`os.listdrives()`](../library/os.html#os.listdrives "os.listdrives"), [`os.listvolumes()`](../library/os.html#os.listvolumes "os.listvolumes") and [`os.listmounts()`](../library/os.html#os.listmounts "os.listmounts")
  functions on Windows for enumerating drives, volumes and mount points.
  (Contributed by Steve Dower in [gh-102519](https://github.com/python/cpython/issues/102519).)
* [`os.stat()`](../library/os.html#os.stat "os.stat") and [`os.lstat()`](../library/os.html#os.lstat "os.lstat") are now more accurate on Windows.
  The `st_birthtime` field will now be filled with the creation time
  of the file, and `st_ctime` is deprecated but still contains the
  creation time (but in the future will return the last metadata change,
  for consistency with other platforms). `st_dev` may be up to 64 bits
  and `st_ino` up to 128 bits depending on your file system, and
  `st_rdev` is always set to zero rather than incorrect values.
  Both functions may be significantly faster on newer releases of
  Windows. (Contributed by Steve Dower in [gh-99726](https://github.com/python/cpython/issues/99726).)
* As of 3.12.4, [`os.mkdir()`](../library/os.html#os.mkdir "os.mkdir") and [`os.makedirs()`](../library/os.html#os.makedirs "os.makedirs") on Windows
  now support passing a *mode* value of `0o700` to apply access
  control to the new directory. This implicitly affects
  [`tempfile.mkdtemp()`](../library/tempfile.html#tempfile.mkdtemp "tempfile.mkdtemp") and is a mitigation for [**CVE 2024-4030**](https://www.cve.org/CVERecord?id=CVE-2024-4030).
  Other values for *mode* continue to be ignored.
  (Contributed by Steve Dower in [gh-118486](https://github.com/python/cpython/issues/118486).)

### os.path[¶](#os-path "Link to this heading")

* Add [`os.path.isjunction()`](../library/os.path.html#os.path.isjunction "os.path.isjunction") to check if a given path is a junction.
  (Contributed by Charles Machalow in [gh-99547](https://github.com/python/cpython/issues/99547).)
* Add [`os.path.splitroot()`](../library/os.path.html#os.path.splitroot "os.path.splitroot") to split a path into a triad
  `(drive, root, tail)`. (Contributed by Barney Gale in [gh-101000](https://github.com/python/cpython/issues/101000).)

### pathlib[¶](#pathlib "Link to this heading")

* Add support for subclassing [`pathlib.PurePath`](../library/pathlib.html#pathlib.PurePath "pathlib.PurePath") and
  [`pathlib.Path`](../library/pathlib.html#pathlib.Path "pathlib.Path"), plus their Posix- and Windows-specific variants.
  Subclasses may override the [`pathlib.PurePath.with_segments()`](../library/pathlib.html#pathlib.PurePath.with_segments "pathlib.PurePath.with_segments") method
  to pass information between path instances.
* Add [`pathlib.Path.walk()`](../library/pathlib.html#pathlib.Path.walk "pathlib.Path.walk") for walking the directory trees and generating
  all file or directory names within them, similar to [`os.walk()`](../library/os.html#os.walk "os.walk").
  (Contributed by Stanislav Zmiev in [gh-90385](https://github.com/python/cpython/issues/90385).)
* Add *walk\_up* optional parameter to [`pathlib.PurePath.relative_to()`](../library/pathlib.html#pathlib.PurePath.relative_to "pathlib.PurePath.relative_to")
  to allow the insertion of `..` entries in the result; this behavior is
  more consistent with [`os.path.relpath()`](../library/os.path.html#os.path.relpath "os.path.relpath").
  (Contributed by Domenico Ragusa in [gh-84538](https://github.com/python/cpython/issues/84538).)
* Add [`pathlib.Path.is_junction()`](../library/pathlib.html#pathlib.Path.is_junction "pathlib.Path.is_junction") as a proxy to [`os.path.isjunction()`](../library/os.path.html#os.path.isjunction "os.path.isjunction").
  (Contributed by Charles Machalow in [gh-99547](https://github.com/python/cpython/issues/99547).)
* Add *case\_sensitive* optional parameter to [`pathlib.Path.glob()`](../library/pathlib.html#pathlib.Path.glob "pathlib.Path.glob"),
  [`pathlib.Path.rglob()`](../library/pathlib.html#pathlib.Path.rglob "pathlib.Path.rglob") and [`pathlib.PurePath.match()`](../library/pathlib.html#pathlib.PurePath.match "pathlib.PurePath.match") for matching
  the path’s case sensitivity, allowing for more precise control over the matching process.

### platform[¶](#platform "Link to this heading")

* Add support for detecting Windows 11 and Windows Server releases past 2012.
  Previously, lookups on Windows Server platforms newer than Windows Server 2012
  and on Windows 11 would return `Windows-10`.
  (Contributed by Steve Dower in [gh-89545](https://github.com/python/cpython/issues/89545).)

### pdb[¶](#pdb "Link to this heading")

* Add convenience variables to hold values temporarily for debug session
  and provide quick access to values like the current frame or the return
  value.
  (Contributed by Tian Gao in [gh-103693](https://github.com/python/cpython/issues/103693).)

### random[¶](#random "Link to this heading")

* Add [`random.binomialvariate()`](../library/random.html#random.binomialvariate "random.binomialvariate").
  (Contributed by Raymond Hettinger in [gh-81620](https://github.com/python/cpython/issues/81620).)
* Add a default of `lambd=1.0` to [`random.expovariate()`](../library/random.html#random.expovariate "random.expovariate").
  (Contributed by Raymond Hettinger in [gh-100234](https://github.com/python/cpython/issues/100234).)

### shutil[¶](#shutil "Link to this heading")

* [`shutil.make_archive()`](../library/shutil.html#shutil.make_archive "shutil.make_archive") now passes the *root\_dir* argument to custom
  archivers which support it.
  In this case it no longer temporarily changes the current working directory
  of the process to *root\_dir* to perform archiving.
  (Contributed by Serhiy Storchaka in [gh-74696](https://github.com/python/cpython/issues/74696).)
* [`shutil.rmtree()`](../library/shutil.html#shutil.rmtree "shutil.rmtree") now accepts a new argument *onexc* which is an
  error handler like *onerror* but which expects an exception instance
  rather than a *(typ, val, tb)* triplet. *onerror* is deprecated.
  (Contributed by Irit Katriel in [gh-102828](https://github.com/python/cpython/issues/102828).)
* [`shutil.which()`](../library/shutil.html#shutil.which "shutil.which") now consults the *PATHEXT* environment variable to
  find matches within *PATH* on Windows even when the given *cmd* includes
  a directory component.
  (Contributed by Charles Machalow in [gh-103179](https://github.com/python/cpython/issues/103179).)

  [`shutil.which()`](../library/shutil.html#shutil.which "shutil.which") will call `NeedCurrentDirectoryForExePathW` when
  querying for executables on Windows to determine if the current working
  directory should be prepended to the search path.
  (Contributed by Charles Machalow in [gh-103179](https://github.com/python/cpython/issues/103179).)

  [`shutil.which()`](../library/shutil.html#shutil.which "shutil.which") will return a path matching the *cmd* with a component
  from `PATHEXT` prior to a direct match elsewhere in the search path on
  Windows.
  (Contributed by Charles Machalow in [gh-103179](https://github.com/python/cpython/issues/103179).)

### sqlite3[¶](#sqlite3 "Link to this heading")

* Add a [command-line interface](../library/sqlite3.html#sqlite3-cli).
  (Contributed by Erlend E. Aasland in [gh-77617](https://github.com/python/cpython/issues/77617).)
* Add the [`sqlite3.Connection.autocommit`](../library/sqlite3.html#sqlite3.Connection.autocommit "sqlite3.Connection.autocommit") attribute
  to [`sqlite3.Connection`](../library/sqlite3.html#sqlite3.Connection "sqlite3.Connection")
  and the *autocommit* parameter to [`sqlite3.connect()`](../library/sqlite3.html#sqlite3.connect "sqlite3.connect")
  to control [**PEP 249**](https://peps.python.org/pep-0249/)-compliant
  [transaction handling](../library/sqlite3.html#sqlite3-transaction-control-autocommit).
  (Contributed by Erlend E. Aasland in [gh-83638](https://github.com/python/cpython/issues/83638).)
* Add *entrypoint* keyword-only parameter to
  [`sqlite3.Connection.load_extension()`](../library/sqlite3.html#sqlite3.Connection.load_extension "sqlite3.Connection.load_extension"),
  for overriding the SQLite extension entry point.
  (Contributed by Erlend E. Aasland in [gh-103015](https://github.com/python/cpython/issues/103015).)
* Add [`sqlite3.Connection.getconfig()`](../library/sqlite3.html#sqlite3.Connection.getconfig "sqlite3.Connection.getconfig") and
  [`sqlite3.Connection.setconfig()`](../library/sqlite3.html#sqlite3.Connection.setconfig "sqlite3.Connection.setconfig") to [`sqlite3.Connection`](../library/sqlite3.html#sqlite3.Connection "sqlite3.Connection")
  to make configuration changes to a database connection.
  (Contributed by Erlend E. Aasland in [gh-103489](https://github.com/python/cpython/issues/103489).)

### statistics[¶](#statistics "Link to this heading")

* Extend [`statistics.correlation()`](../library/statistics.html#statistics.correlation "statistics.correlation") to include as a `ranked` method
  for computing the Spearman correlation of ranked data.
  (Contributed by Raymond Hettinger in [gh-95861](https://github.com/python/cpython/issues/95861).)

### sys[¶](#sys "Link to this heading")

* Add the [`sys.monitoring`](../library/sys.monitoring.html#module-sys.monitoring "sys.monitoring: Access and control event monitoring") namespace to expose the new [PEP 669](#whatsnew312-pep669) monitoring API.
  (Contributed by Mark Shannon in [gh-103082](https://github.com/python/cpython/issues/103082).)
* Add [`sys.activate_stack_trampoline()`](../library/sys.html#sys.activate_stack_trampoline "sys.activate_stack_trampoline") and
  [`sys.deactivate_stack_trampoline()`](../library/sys.html#sys.deactivate_stack_trampoline "sys.deactivate_stack_trampoline") for activating and deactivating
  stack profiler trampolines,
  and [`sys.is_stack_trampoline_active()`](../library/sys.html#sys.is_stack_trampoline_active "sys.is_stack_trampoline_active") for querying if stack profiler
  trampolines are active.
  (Contributed by Pablo Galindo and Christian Heimes
  with contributions from Gregory P. Smith [Google] and Mark Shannon
  in [gh-96123](https://github.com/python/cpython/issues/96123).)
* Add [`sys.last_exc`](../library/sys.html#sys.last_exc "sys.last_exc") which holds the last unhandled exception that
  was raised (for post-mortem debugging use cases). Deprecate the
  three fields that have the same information in its legacy form:
  [`sys.last_type`](../library/sys.html#sys.last_type "sys.last_type"), [`sys.last_value`](../library/sys.html#sys.last_value "sys.last_value") and [`sys.last_traceback`](../library/sys.html#sys.last_traceback "sys.last_traceback").
  (Contributed by Irit Katriel in [gh-102778](https://github.com/python/cpython/issues/102778).)
* [`sys._current_exceptions()`](../library/sys.html#sys._current_exceptions "sys._current_exceptions") now returns a mapping from thread-id to an
  exception instance, rather than to a `(typ, exc, tb)` tuple.
  (Contributed by Irit Katriel in [gh-103176](https://github.com/python/cpython/issues/103176).)
* [`sys.setrecursionlimit()`](../library/sys.html#sys.setrecursionlimit "sys.setrecursionlimit") and [`sys.getrecursionlimit()`](../library/sys.html#sys.getrecursionlimit "sys.getrecursionlimit").
  The recursion limit now applies only to Python code. Builtin functions do
  not use the recursion limit, but are protected by a different mechanism
  that prevents recursion from causing a virtual machine crash.

### tempfile[¶](#tempfile "Link to this heading")

* The [`tempfile.NamedTemporaryFile`](../library/tempfile.html#tempfile.NamedTemporaryFile "tempfile.NamedTemporaryFile") function has a new optional parameter
  *delete\_on\_close* (Contributed by Evgeny Zorin in [gh-58451](https://github.com/python/cpython/issues/58451).)
* [`tempfile.mkdtemp()`](../library/tempfile.html#tempfile.mkdtemp "tempfile.mkdtemp") now always returns an absolute path, even if the
  argument provided to the *dir* parameter is a relative path.
* As of 3.12.4 on Windows, the default mode `0o700` used by
  [`tempfile.mkdtemp()`](../library/tempfile.html#tempfile.mkdtemp "tempfile.mkdtemp") now limits access to the new directory due to
  changes to [`os.mkdir()`](../library/os.html#os.mkdir "os.mkdir"). This is a mitigation for [**CVE 2024-4030**](https://www.cve.org/CVERecord?id=CVE-2024-4030).
  (Contributed by Steve Dower in [gh-118486](https://github.com/python/cpython/issues/118486).)

### threading[¶](#threading "Link to this heading")

* Add [`threading.settrace_all_threads()`](../library/threading.html#threading.settrace_all_threads "threading.settrace_all_threads") and
  [`threading.setprofile_all_threads()`](../library/threading.html#threading.setprofile_all_threads "threading.setprofile_all_threads") that allow to set tracing and
  profiling functions in all running threads in addition to the calling one.
  (Contributed by Pablo Galindo in [gh-93503](https://github.com/python/cpython/issues/93503).)

### tkinter[¶](#tkinter "Link to this heading")

* `tkinter.Canvas.coords()` now flattens its arguments.
  It now accepts not only coordinates as separate arguments
  (`x1, y1, x2, y2, ...`) and a sequence of coordinates
  (`[x1, y1, x2, y2, ...]`), but also coordinates grouped in pairs
  (`(x1, y1), (x2, y2), ...` and `[(x1, y1), (x2, y2), ...]`),
  like `create_*()` methods.
  (Contributed by Serhiy Storchaka in [gh-94473](https://github.com/python/cpython/issues/94473).)

### tokenize[¶](#tokenize "Link to this heading")

* The [`tokenize`](../library/tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module includes the changes introduced in [**PEP 701**](https://peps.python.org/pep-0701/).
  (Contributed by Marta Gómez Macías and Pablo Galindo in [gh-102856](https://github.com/python/cpython/issues/102856).)
  See [Porting to Python 3.12](#whatsnew312-porting-to-python312) for more information on the
  changes to the [`tokenize`](../library/tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module.

### types[¶](#types "Link to this heading")

* Add [`types.get_original_bases()`](../library/types.html#types.get_original_bases "types.get_original_bases") to allow for further introspection of
  [User-defined generic types](../library/typing.html#user-defined-generics) when subclassed. (Contributed by
  James Hilton-Balfe and Alex Waygood in [gh-101827](https://github.com/python/cpython/issues/101827).)

### typing[¶](#typing "Link to this heading")

* [`isinstance()`](../library/functions.html#isinstance "isinstance") checks against
  [`runtime-checkable protocols`](../library/typing.html#typing.runtime_checkable "typing.runtime_checkable") now use
  [`inspect.getattr_static()`](../library/inspect.html#inspect.getattr_static "inspect.getattr_static") rather than [`hasattr()`](../library/functions.html#hasattr "hasattr") to lookup whether
  attributes exist. This means that descriptors and [`__getattr__()`](../reference/datamodel.html#object.__getattr__ "object.__getattr__")
  methods are no longer unexpectedly evaluated during `isinstance()` checks
  against runtime-checkable protocols. However, it may also mean that some
  objects which used to be considered instances of a runtime-checkable protocol
  may no longer be considered instances of that protocol on Python 3.12+, and
  vice versa. Most users are unlikely to be affected by this change.
  (Contributed by Alex Waygood in [gh-102433](https://github.com/python/cpython/issues/102433).)
* The members of a runtime-checkable protocol are now considered “frozen” at
  runtime as soon as the class has been created. Monkey-patching attributes
  onto a runtime-checkable protocol will still work, but will have no impact on
  [`isinstance()`](../library/functions.html#isinstance "isinstance") checks comparing objects to the protocol. For example:

  ```
  >>> from typing import Protocol, runtime_checkable
  >>> @runtime_checkable
  ... class HasX(Protocol):
  ...     x = 1
  ...
  >>> class Foo: ...
  ...
  >>> f = Foo()
  >>> isinstance(f, HasX)
  False
  >>> f.x = 1
  >>> isinstance(f, HasX)
  True
  >>> HasX.y = 2
  >>> isinstance(f, HasX)  # unchanged, even though HasX now also has a "y" attribute
  True
  ```

  This change was made in order to speed up `isinstance()` checks against
  runtime-checkable protocols.
* The performance profile of [`isinstance()`](../library/functions.html#isinstance "isinstance") checks against
  [`runtime-checkable protocols`](../library/typing.html#typing.runtime_checkable "typing.runtime_checkable") has changed
  significantly. Most `isinstance()` checks against protocols with only a few
  members should be at least 2x faster than in 3.11, and some may be 20x
  faster or more. However, `isinstance()` checks against protocols with many
  members may be slower than in Python 3.11. (Contributed by Alex
  Waygood in [gh-74690](https://github.com/python/cpython/issues/74690) and [gh-103193](https://github.com/python/cpython/issues/103193).)
* All [`typing.TypedDict`](../library/typing.html#typing.TypedDict "typing.TypedDict") and [`typing.NamedTuple`](../library/typing.html#typing.NamedTuple "typing.NamedTuple") classes now have the
  `__orig_bases__` attribute. (Contributed by Adrian Garcia Badaracco in
  [gh-103699](https://github.com/python/cpython/issues/103699).)
* Add `frozen_default` parameter to [`typing.dataclass_transform()`](../library/typing.html#typing.dataclass_transform "typing.dataclass_transform").
  (Contributed by Erik De Bonte in [gh-99957](https://github.com/python/cpython/issues/99957).)

### unicodedata[¶](#unicodedata "Link to this heading")

* The Unicode database has been updated to version 15.0.0. (Contributed by
  Benjamin Peterson in [gh-96734](https://github.com/python/cpython/issues/96734)).

### unittest[¶](#unittest "Link to this heading")

Add a `--durations` command line option, showing the N slowest test cases:

```
python3 -m unittest --durations=3 lib.tests.test_threading
.....
Slowest test durations
----------------------------------------------------------------------
1.210s     test_timeout (Lib.test.test_threading.BarrierTests)
1.003s     test_default_timeout (Lib.test.test_threading.BarrierTests)
0.518s     test_timeout (Lib.test.test_threading.EventTests)

(0.000 durations hidden.  Use -v to show these durations.)
----------------------------------------------------------------------
Ran 158 tests in 9.869s

OK (skipped=3)
```

(Contributed by Giampaolo Rodola in [gh-48330](https://github.com/python/cpython/issues/48330))

### uuid[¶](#uuid "Link to this heading")

* Add a [command-line interface](../library/uuid.html#uuid-cli).
  (Contributed by Adam Chhina in [gh-88597](https://github.com/python/cpython/issues/88597).)

## Optimizations[¶](#optimizations "Link to this heading")

* Remove `wstr` and `wstr_length` members from Unicode objects.
  It reduces object size by 8 or 16 bytes on 64bit platform. ([**PEP 623**](https://peps.python.org/pep-0623/))
  (Contributed by Inada Naoki in [gh-92536](https://github.com/python/cpython/issues/92536).)
* Add experimental support for using the BOLT binary optimizer in the build
  process, which improves performance by 1-5%.
  (Contributed by Kevin Modzelewski in [gh-90536](https://github.com/python/cpython/issues/90536) and tuned by Donghee Na in [gh-101525](https://github.com/python/cpython/issues/101525))
* Speed up the regular expression substitution (functions [`re.sub()`](../library/re.html#re.sub "re.sub") and
  [`re.subn()`](../library/re.html#re.subn "re.subn") and corresponding `re.Pattern` methods) for
  replacement strings containing group references by 2–3 times.
  (Contributed by Serhiy Storchaka in [gh-91524](https://github.com/python/cpython/issues/91524).)
* Speed up [`asyncio.Task`](../library/asyncio-task.html#asyncio.Task "asyncio.Task") creation by deferring expensive string formatting.
  (Contributed by Itamar Oren in [gh-103793](https://github.com/python/cpython/issues/103793).)
* The [`tokenize.tokenize()`](../library/tokenize.html#tokenize.tokenize "tokenize.tokenize") and [`tokenize.generate_tokens()`](../library/tokenize.html#tokenize.generate_tokens "tokenize.generate_tokens") functions are
  up to 64% faster as a side effect of the changes required to cover [**PEP 701**](https://peps.python.org/pep-0701/) in
  the [`tokenize`](../library/tokenize.html#module-tokenize "tokenize: Lexical scanner for Python source code.") module. (Contributed by Marta Gómez Macías and Pablo Galindo
  in [gh-102856](https://github.com/python/cpython/issues/102856).)
* Speed up [`super()`](../library/functions.html#super "super") method calls and attribute loads via the
  new [`LOAD_SUPER_ATTR`](../library/dis.html#opcode-LOAD_SUPER_ATTR) instruction. (Contributed by Carl Meyer and
  Vladimir Matveev in [gh-103497](https://github.com/python/cpython/issues/103497).)

## CPython bytecode changes[¶](#cpython-bytecode-changes "Link to this heading")

* Remove the `LOAD_METHOD` instruction. It has been merged into
  [`LOAD_ATTR`](../library/dis.html#opcode-LOAD_ATTR). [`LOAD_ATTR`](../library/dis.html#opcode-LOAD_ATTR) will now behave like the old
  `LOAD_METHOD` instruction if the low bit of its oparg is set.
  (Contributed by Ken Jin in [gh-93429](https://github.com/python/cpython/issues/93429).)
* Remove the `JUMP_IF_FALSE_OR_POP` and `JUMP_IF_TRUE_OR_POP`
  instructions. (Contributed by Irit Katriel in [gh-102859](https://github.com/python/cpython/issues/102859).)
* Remove the `PRECALL` instruction. (Contributed by Mark Shannon in
  [gh-92925](https://github.com/python/cpython/issues/92925).)
* Add the [`BINARY_SLICE`](../library/dis.html#opcode-BINARY_SLICE) and [`STORE_SLICE`](../library/dis.html#opcode-STORE_SLICE) instructions.
  (Contributed by Mark Shannon in [gh-94163](https://github.com/python/cpython/issues/94163).)
* Add the [`CALL_INTRINSIC_1`](../library/dis.html#opcode-CALL_INTRINSIC_1) instructions.
  (Contributed by Mark Shannon in [gh-99005](https://github.com/python/cpython/issues/99005).)
* Add the [`CALL_INTRINSIC_2`](../library/dis.html#opcode-CALL_INTRINSIC_2) instruction.
  (Contributed by Irit Katriel in [gh-101799](https://github.com/python/cpython/issues/101799).)
* Add the [`CLEANUP_THROW`](../library/dis.html#opcode-CLEANUP_THROW) instruction.
  (Contributed by Brandt Bucher in [gh-90997](https://github.com/python/cpython/issues/90997).)
* Add the `END_SEND` instruction.
  (Contributed by Mark Shannon in [gh-103082](https://github.com/python/cpython/issues/103082).)
* Add the [`LOAD_FAST_AND_CLEAR`](../library/dis.html#opcode-LOAD_FAST_AND_CLEAR) instruction as part of the
  implementation of [**PEP 709**](https://peps.python.org/pep-0709/). (Contributed by Carl Meyer in [gh-101441](https://github.com/python/cpython/issues/101441).)
* Add the [`LOAD_FAST_CHECK`](../library/dis.html#opcode-LOAD_FAST_CHECK) instruction.
  (Contributed by Dennis Sweeney in [gh-93143](https://github.com/python/cpython/issues/93143).)
* Add the [`LOAD_FROM_DICT_OR_DEREF`](../library/dis.html#opcode-LOAD_FROM_DICT_OR_DEREF), [`LOAD_FROM_DICT_OR_GLOBALS`](../library/dis.html#opcode-LOAD_FROM_DICT_OR_GLOBALS),
  and [`LOAD_LOCALS`](../library/dis.html#opcode-LOAD_LOCALS) opcodes as part of the implementation of [**PEP 695**](https://peps.python.org/pep-0695/).
  Remove the `LOAD_CLASSDEREF` opcode, which can be replaced with
  [`LOAD_LOCALS`](../library/dis.html#opcode-LOAD_LOCALS) plus [`LOAD_FROM_DICT_OR_DEREF`](../library/dis.html#opcode-LOAD_FROM_DICT_OR_DEREF). (Contributed
  by Jelle Zijlstra in [gh-103764](https://github.com/python/cpython/issues/103764).)
* Add the [`LOAD_SUPER_ATTR`](../library/dis.html#opcode-LOAD_SUPER_ATTR) instruction. (Contributed by Carl Meyer and
  Vladimir Matveev in [gh-103497](https://github.com/python/cpython/issues/103497).)
* Add the [`RETURN_CONST`](../library/dis.html#opcode-RETURN_CONST) instruction. (Contributed by Wenyang Wang in [gh-101632](https://github.com/python/cpython/issues/101632).)

## Demos and Tools[¶](#demos-and-tools "Link to this heading")

* Remove the `Tools/demo/` directory which contained old demo scripts. A copy
  can be found in the [old-demos project](https://github.com/gvanrossum/old-demos).
  (Contributed by Victor Stinner in [gh-97681](https://github.com/python/cpython/issues/97681).)
* Remove outdated example scripts of the `Tools/scripts/` directory.
  A copy can be found in the [old-demos project](https://github.com/gvanrossum/old-demos).
  (Contributed by Victor Stinner in [gh-97669](https://github.com/python/cpython/issues/97669).)

## Deprecated[¶](#deprecated "Link to this heading")

* [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library."): The *type*, *choices*, and *metavar* parameters
  of `argparse.BooleanOptionalAction` are deprecated
  and will be removed in 3.14.
  (Contributed by Nikita Sobolev in [gh-92248](https://github.com/python/cpython/issues/92248).)
* [`ast`](../library/ast.html#module-ast "ast: Abstract Syntax Tree classes and manipulation."): The following [`ast`](../library/ast.html#module-ast "ast: Abstract Syntax Tree classes and manipulation.") features have been deprecated in documentation since
  Python 3.8, now cause a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") to be emitted at runtime
  when they are accessed or used, and will be removed in Python 3.14:

  + `ast.Num`
  + `ast.Str`
  + `ast.Bytes`
  + `ast.NameConstant`
  + `ast.Ellipsis`

  Use [`ast.Constant`](../library/ast.html#ast.Constant "ast.Constant") instead.
  (Contributed by Serhiy Storchaka in [gh-90953](https://github.com/python/cpython/issues/90953).)
* [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O."):

  + The child watcher classes [`asyncio.MultiLoopChildWatcher`](../library/asyncio-policy.html#asyncio.MultiLoopChildWatcher "asyncio.MultiLoopChildWatcher"),
    [`asyncio.FastChildWatcher`](../library/asyncio-policy.html#asyncio.FastChildWatcher "asyncio.FastChildWatcher"), [`asyncio.AbstractChildWatcher`](../library/asyncio-policy.html#asyncio.AbstractChildWatcher "asyncio.AbstractChildWatcher")
    and [`asyncio.SafeChildWatcher`](../library/asyncio-policy.html#asyncio.SafeChildWatcher "asyncio.SafeChildWatcher") are deprecated and
    will be removed in Python 3.14.
    (Contributed by Kumar Aditya in [gh-94597](https://github.com/python/cpython/issues/94597).)
  + [`asyncio.set_child_watcher()`](../library/asyncio-policy.html#asyncio.set_child_watcher "asyncio.set_child_watcher"), [`asyncio.get_child_watcher()`](../library/asyncio-policy.html#asyncio.get_child_watcher "asyncio.get_child_watcher"),
    [`asyncio.AbstractEventLoopPolicy.set_child_watcher()`](../library/asyncio-policy.html#asyncio.AbstractEventLoopPolicy.set_child_watcher "asyncio.AbstractEventLoopPolicy.set_child_watcher") and
    [`asyncio.AbstractEventLoopPolicy.get_child_watcher()`](../library/asyncio-policy.html#asyncio.AbstractEventLoopPolicy.get_child_watcher "asyncio.AbstractEventLoopPolicy.get_child_watcher") are deprecated
    and will be removed in Python 3.14.
    (Contributed by Kumar Aditya in [gh-94597](https://github.com/python/cpython/issues/94597).)
  + The [`get_event_loop()`](../library/asyncio-eventloop.html#asyncio.get_event_loop "asyncio.get_event_loop") method of the
    default event loop policy now emits a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") if there
    is no current event loop set and it decides to create one.
    (Contributed by Serhiy Storchaka and Guido van Rossum in [gh-100160](https://github.com/python/cpython/issues/100160).)
* [`calendar`](../library/calendar.html#module-calendar "calendar: Functions for working with calendars, including some emulation of the Unix cal program."): `calendar.January` and `calendar.February` constants are deprecated and
  replaced by [`calendar.JANUARY`](../library/calendar.html#calendar.JANUARY "calendar.JANUARY") and [`calendar.FEBRUARY`](../library/calendar.html#calendar.FEBRUARY "calendar.FEBRUARY").
  (Contributed by Prince Roshan in [gh-103636](https://github.com/python/cpython/issues/103636).)
* [`collections.abc`](../library/collections.abc.html#module-collections.abc "collections.abc: Abstract base classes for containers"): Deprecated [`collections.abc.ByteString`](../library/collections.abc.html#collections.abc.ByteString "collections.abc.ByteString").
  Prefer `Sequence` or [`collections.abc.Buffer`](../library/collections.abc.html#collections.abc.Buffer "collections.abc.Buffer").
  For use in typing, prefer a union, like `bytes | bytearray`, or [`collections.abc.Buffer`](../library/collections.abc.html#collections.abc.Buffer "collections.abc.Buffer").
  (Contributed by Shantanu Jain in [gh-91896](https://github.com/python/cpython/issues/91896).)
* [`datetime`](../library/datetime.html#module-datetime "datetime: Basic date and time types."): [`datetime.datetime`](../library/datetime.html#datetime.datetime "datetime.datetime")’s [`utcnow()`](../library/datetime.html#datetime.datetime.utcnow "datetime.datetime.utcnow") and
  [`utcfromtimestamp()`](../library/datetime.html#datetime.datetime.utcfromtimestamp "datetime.datetime.utcfromtimestamp") are deprecated and will be
  removed in a future version. Instead, use timezone-aware objects to represent
  datetimes in UTC: respectively, call [`now()`](../library/datetime.html#datetime.datetime.now "datetime.datetime.now") and
  [`fromtimestamp()`](../library/datetime.html#datetime.datetime.fromtimestamp "datetime.datetime.fromtimestamp") with the *tz* parameter set to
  [`datetime.UTC`](../library/datetime.html#datetime.UTC "datetime.UTC").
  (Contributed by Paul Ganssle in [gh-103857](https://github.com/python/cpython/issues/103857).)
* [`email`](../library/email.html#module-email "email: Package supporting the parsing, manipulating, and generating email messages."): Deprecate the *isdst* parameter in [`email.utils.localtime()`](../library/email.utils.html#email.utils.localtime "email.utils.localtime").
  (Contributed by Alan Williams in [gh-72346](https://github.com/python/cpython/issues/72346).)
* [`importlib.abc`](../library/importlib.html#module-importlib.abc "importlib.abc: Abstract base classes related to import"): Deprecated the following classes, scheduled for removal in
  Python 3.14:

  + `importlib.abc.ResourceReader`
  + `importlib.abc.Traversable`
  + `importlib.abc.TraversableResources`

  Use [`importlib.resources.abc`](../library/importlib.resources.abc.html#module-importlib.resources.abc "importlib.resources.abc: Abstract base classes for resources") classes instead:

  + [`importlib.resources.abc.Traversable`](../library/importlib.resources.abc.html#importlib.resources.abc.Traversable "importlib.resources.abc.Traversable")
  + [`importlib.resources.abc.TraversableResources`](../library/importlib.resources.abc.html#importlib.resources.abc.TraversableResources "importlib.resources.abc.TraversableResources")

  (Contributed by Jason R. Coombs and Hugo van Kemenade in [gh-93963](https://github.com/python/cpython/issues/93963).)
* [`itertools`](../library/itertools.html#module-itertools "itertools: Functions creating iterators for efficient looping."): Deprecate the support for copy, deepcopy, and pickle operations,
  which is undocumented, inefficient, historically buggy, and inconsistent.
  This will be removed in 3.14 for a significant reduction in code
  volume and maintenance burden.
  (Contributed by Raymond Hettinger in [gh-101588](https://github.com/python/cpython/issues/101588).)
* [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism."): In Python 3.14, the default [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.")
  start method will change to a safer one on Linux, BSDs,
  and other non-macOS POSIX platforms where `'fork'` is currently
  the default ([gh-84559](https://github.com/python/cpython/issues/84559)). Adding a runtime warning about this was deemed too
  disruptive as the majority of code is not expected to care. Use the
  [`get_context()`](../library/multiprocessing.html#multiprocessing.get_context "multiprocessing.get_context") or
  [`set_start_method()`](../library/multiprocessing.html#multiprocessing.set_start_method "multiprocessing.set_start_method") APIs to explicitly specify when
  your code *requires* `'fork'`. See [contexts and start methods](../library/multiprocessing.html#multiprocessing-start-methods).
* [`pkgutil`](../library/pkgutil.html#module-pkgutil "pkgutil: Utilities for the import system."): [`pkgutil.find_loader()`](../library/pkgutil.html#pkgutil.find_loader "pkgutil.find_loader") and [`pkgutil.get_loader()`](../library/pkgutil.html#pkgutil.get_loader "pkgutil.get_loader")
  are deprecated and will be removed in Python 3.14;
  use [`importlib.util.find_spec()`](../library/importlib.html#importlib.util.find_spec "importlib.util.find_spec") instead.
  (Contributed by Nikita Sobolev in [gh-97850](https://github.com/python/cpython/issues/97850).)
* [`pty`](../library/pty.html#module-pty "pty: Pseudo-Terminal Handling for Unix. (Unix)"): The module has two undocumented `master_open()` and `slave_open()`
  functions that have been deprecated since Python 2 but only gained a
  proper [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") in 3.12. Remove them in 3.14.
  (Contributed by Soumendra Ganguly and Gregory P. Smith in [gh-85984](https://github.com/python/cpython/issues/85984).)
* [`os`](../library/os.html#module-os "os: Miscellaneous operating system interfaces."):

  + The `st_ctime` fields return by [`os.stat()`](../library/os.html#os.stat "os.stat") and [`os.lstat()`](../library/os.html#os.lstat "os.lstat") on
    Windows are deprecated. In a future release, they will contain the last
    metadata change time, consistent with other platforms. For now, they still
    contain the creation time, which is also available in the new `st_birthtime`
    field. (Contributed by Steve Dower in [gh-99726](https://github.com/python/cpython/issues/99726).)
  + On POSIX platforms, [`os.fork()`](../library/os.html#os.fork "os.fork") can now raise a
    [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") when it can detect being called from a
    multithreaded process. There has always been a fundamental incompatibility
    with the POSIX platform when doing so. Even if such code *appeared* to work.
    We added the warning to raise awareness as issues encountered by code doing
    this are becoming more frequent. See the [`os.fork()`](../library/os.html#os.fork "os.fork") documentation for
    more details along with [this discussion on fork being incompatible with threads](https://discuss.python.org/t/concerns-regarding-deprecation-of-fork-with-alive-threads/33555) for *why* we’re now surfacing this
    longstanding platform compatibility problem to developers.

  When this warning appears due to usage of [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") or
  [`concurrent.futures`](../library/concurrent.futures.html#module-concurrent.futures "concurrent.futures: Execute computations concurrently using threads or processes.") the fix is to use a different
  [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") start method such as `"spawn"` or `"forkserver"`.
* [`shutil`](../library/shutil.html#module-shutil "shutil: High-level file operations, including copying."): The *onerror* argument of [`shutil.rmtree()`](../library/shutil.html#shutil.rmtree "shutil.rmtree") is deprecated;
  use *onexc* instead. (Contributed by Irit Katriel in [gh-102828](https://github.com/python/cpython/issues/102828).)
* [`sqlite3`](../library/sqlite3.html#module-sqlite3 "sqlite3: A DB-API 2.0 implementation using SQLite 3.x."):

  + [default adapters and converters](../library/sqlite3.html#sqlite3-default-converters) are now deprecated.
    Instead, use the [Adapter and converter recipes](../library/sqlite3.html#sqlite3-adapter-converter-recipes)
    and tailor them to your needs.
    (Contributed by Erlend E. Aasland in [gh-90016](https://github.com/python/cpython/issues/90016).)
  + In [`execute()`](../library/sqlite3.html#sqlite3.Cursor.execute "sqlite3.Cursor.execute"), [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") is now emitted
    when [named placeholders](../library/sqlite3.html#sqlite3-placeholders) are used together with
    parameters supplied as a [sequence](../glossary.html#term-sequence) instead of as a [`dict`](../library/stdtypes.html#dict "dict").
    Starting from Python 3.14, using named placeholders with parameters supplied
    as a sequence will raise a [`ProgrammingError`](../library/sqlite3.html#sqlite3.ProgrammingError "sqlite3.ProgrammingError").
    (Contributed by Erlend E. Aasland in [gh-101698](https://github.com/python/cpython/issues/101698).)
* [`sys`](../library/sys.html#module-sys "sys: Access system-specific parameters and functions."): The [`sys.last_type`](../library/sys.html#sys.last_type "sys.last_type"), [`sys.last_value`](../library/sys.html#sys.last_value "sys.last_value") and [`sys.last_traceback`](../library/sys.html#sys.last_traceback "sys.last_traceback")
  fields are deprecated. Use [`sys.last_exc`](../library/sys.html#sys.last_exc "sys.last_exc") instead.
  (Contributed by Irit Katriel in [gh-102778](https://github.com/python/cpython/issues/102778).)
* [`tarfile`](../library/tarfile.html#module-tarfile "tarfile: Read and write tar-format archive files."): Extracting tar archives without specifying *filter* is deprecated until
  Python 3.14, when `'data'` filter will become the default.
  See [Extraction filters](../library/tarfile.html#tarfile-extraction-filter) for details.
* [`typing`](../library/typing.html#module-typing "typing: Support for type hints (see :pep:`484`)."):

  + [`typing.Hashable`](../library/typing.html#typing.Hashable "typing.Hashable") and [`typing.Sized`](../library/typing.html#typing.Sized "typing.Sized"), aliases for
    [`collections.abc.Hashable`](../library/collections.abc.html#collections.abc.Hashable "collections.abc.Hashable") and [`collections.abc.Sized`](../library/collections.abc.html#collections.abc.Sized "collections.abc.Sized") respectively, are
    deprecated. ([gh-94309](https://github.com/python/cpython/issues/94309).)
  + [`typing.ByteString`](../library/typing.html#typing.ByteString "typing.ByteString"), deprecated since Python 3.9, now causes a
    [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") to be emitted when it is used.
    (Contributed by Alex Waygood in [gh-91896](https://github.com/python/cpython/issues/91896).)
* [`xml.etree.ElementTree`](../library/xml.etree.elementtree.html#module-xml.etree.ElementTree "xml.etree.ElementTree: Implementation of the ElementTree API."): The module now emits [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning")
  when testing the truth value of an [`xml.etree.ElementTree.Element`](../library/xml.etree.elementtree.html#xml.etree.ElementTree.Element "xml.etree.ElementTree.Element").
  Before, the Python implementation emitted [`FutureWarning`](../library/exceptions.html#FutureWarning "FutureWarning"), and the C
  implementation emitted nothing.
  (Contributed by Jacob Walls in [gh-83122](https://github.com/python/cpython/issues/83122).)
* The 3-arg signatures (type, value, traceback) of [`coroutine throw()`](../reference/datamodel.html#coroutine.throw "coroutine.throw"), [`generator throw()`](../reference/expressions.html#generator.throw "generator.throw") and
  [`async generator throw()`](../reference/expressions.html#agen.athrow "agen.athrow") are deprecated and
  may be removed in a future version of Python. Use the single-arg versions
  of these functions instead. (Contributed by Ofey Chan in [gh-89874](https://github.com/python/cpython/issues/89874).)
* [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") is now raised when [`__package__`](../reference/datamodel.html#module.__package__ "module.__package__") on a
  module differs from
  [`__spec__.parent`](../library/importlib.html#importlib.machinery.ModuleSpec.parent "importlib.machinery.ModuleSpec.parent") (previously
  it was [`ImportWarning`](../library/exceptions.html#ImportWarning "ImportWarning")).
  (Contributed by Brett Cannon in [gh-65961](https://github.com/python/cpython/issues/65961).)
* Setting [`__package__`](../reference/datamodel.html#module.__package__ "module.__package__") or [`__cached__`](../reference/datamodel.html#module.__cached__ "module.__cached__") on a
  module is deprecated, and will cease to be set or taken into consideration by
  the import system in Python 3.14. (Contributed by Brett Cannon in [gh-65961](https://github.com/python/cpython/issues/65961).)
* The bitwise inversion operator (`~`) on bool is deprecated. It will throw an
  error in Python 3.16. Use `not` for logical negation of bools instead.
  In the rare case that you really need the bitwise inversion of the underlying
  `int`, convert to int explicitly: `~int(x)`. (Contributed by Tim Hoffmann
  in [gh-103487](https://github.com/python/cpython/issues/103487).)
* Accessing [`co_lnotab`](../reference/datamodel.html#codeobject.co_lnotab "codeobject.co_lnotab") on code objects was deprecated in
  Python 3.10 via [**PEP 626**](https://peps.python.org/pep-0626/),
  but it only got a proper [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") in 3.12.
  May be removed in 3.15.
  (Contributed by Nikita Sobolev in [gh-101866](https://github.com/python/cpython/issues/101866).)

### Pending Removal in Python 3.13[¶](#pending-removal-in-python-3-13 "Link to this heading")

Modules (see [**PEP 594**](https://peps.python.org/pep-0594/)):

* [`aifc`](../library/aifc.html#module-aifc "aifc: Read and write audio files in AIFF or AIFC format. (deprecated)")
* [`audioop`](../library/audioop.html#module-audioop "audioop: Manipulate raw audio data. (deprecated)")
* [`cgi`](../library/cgi.html#module-cgi "cgi: Helpers for running Python scripts via the Common Gateway Interface. (deprecated)")
* [`cgitb`](../library/cgitb.html#module-cgitb "cgitb: Configurable traceback handler for CGI scripts. (deprecated)")
* [`chunk`](../library/chunk.html#module-chunk "chunk: Module to read IFF chunks. (deprecated)")
* [`crypt`](../library/crypt.html#module-crypt "crypt: The crypt() function used to check Unix passwords. (deprecated) (Unix)")
* [`imghdr`](../library/imghdr.html#module-imghdr "imghdr: Determine the type of image contained in a file or byte stream. (deprecated)")
* [`mailcap`](../library/mailcap.html#module-mailcap "mailcap: Mailcap file handling. (deprecated)")
* [`msilib`](../library/msilib.html#module-msilib "msilib: Creation of Microsoft Installer files, and CAB files. (deprecated) (Windows)")
* [`nis`](../library/nis.html#module-nis "nis: Interface to Sun's NIS (Yellow Pages) library. (deprecated) (Unix)")
* [`nntplib`](../library/nntplib.html#module-nntplib "nntplib: NNTP protocol client (requires sockets). (deprecated)")
* [`ossaudiodev`](../library/ossaudiodev.html#module-ossaudiodev "ossaudiodev: Access to OSS-compatible audio devices. (deprecated) (Linux, FreeBSD)")
* [`pipes`](../library/pipes.html#module-pipes "pipes: A Python interface to Unix shell pipelines. (deprecated) (Unix)")
* [`sndhdr`](../library/sndhdr.html#module-sndhdr "sndhdr: Determine type of a sound file. (deprecated)")
* [`spwd`](../library/spwd.html#module-spwd "spwd: The shadow password database (getspnam() and friends). (deprecated) (Unix)")
* [`sunau`](../library/sunau.html#module-sunau "sunau: Provide an interface to the Sun AU sound format. (deprecated)")
* [`telnetlib`](../library/telnetlib.html#module-telnetlib "telnetlib: Telnet client class. (deprecated)")
* [`uu`](../library/uu.html#module-uu "uu: Encode and decode files in uuencode format. (deprecated)")
* [`xdrlib`](../library/xdrlib.html#module-xdrlib "xdrlib: Encoders and decoders for the External Data Representation (XDR). (deprecated)")

Other modules:

* `lib2to3`, and the **2to3** program ([gh-84540](https://github.com/python/cpython/issues/84540))

APIs:

* `configparser.LegacyInterpolation` ([gh-90765](https://github.com/python/cpython/issues/90765))
* `locale.resetlocale()` ([gh-90817](https://github.com/python/cpython/issues/90817))
* `turtle.RawTurtle.settiltangle()` ([gh-50096](https://github.com/python/cpython/issues/50096))
* `unittest.findTestCases()` ([gh-50096](https://github.com/python/cpython/issues/50096))
* `unittest.getTestCaseNames()` ([gh-50096](https://github.com/python/cpython/issues/50096))
* `unittest.makeSuite()` ([gh-50096](https://github.com/python/cpython/issues/50096))
* `unittest.TestProgram.usageExit()` ([gh-67048](https://github.com/python/cpython/issues/67048))
* `webbrowser.MacOSX` ([gh-86421](https://github.com/python/cpython/issues/86421))
* [`classmethod`](../library/functions.html#classmethod "classmethod") descriptor chaining ([gh-89519](https://github.com/python/cpython/issues/89519))
* [`importlib.resources`](../library/importlib.resources.html#module-importlib.resources "importlib.resources: Package resource reading, opening, and access") deprecated methods:

  + `contents()`
  + `is_resource()`
  + `open_binary()`
  + `open_text()`
  + `path()`
  + `read_binary()`
  + `read_text()`

  Use [`importlib.resources.files()`](../library/importlib.resources.html#importlib.resources.files "importlib.resources.files") instead. Refer to [importlib-resources: Migrating from Legacy](https://importlib-resources.readthedocs.io/en/latest/using.html#migrating-from-legacy) ([gh-106531](https://github.com/python/cpython/issues/106531))

### Pending Removal in Python 3.14[¶](#pending-removal-in-python-3-14 "Link to this heading")

* [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library."): The *type*, *choices*, and *metavar* parameters
  of `argparse.BooleanOptionalAction` are deprecated
  and will be removed in 3.14.
  (Contributed by Nikita Sobolev in [gh-92248](https://github.com/python/cpython/issues/92248).)
* [`ast`](../library/ast.html#module-ast "ast: Abstract Syntax Tree classes and manipulation."): The following features have been deprecated in documentation
  since Python 3.8, now cause a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") to be emitted at
  runtime when they are accessed or used, and will be removed in Python 3.14:

  + `ast.Num`
  + `ast.Str`
  + `ast.Bytes`
  + `ast.NameConstant`
  + `ast.Ellipsis`

  Use [`ast.Constant`](../library/ast.html#ast.Constant "ast.Constant") instead.
  (Contributed by Serhiy Storchaka in [gh-90953](https://github.com/python/cpython/issues/90953).)
* [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O."):

  + The child watcher classes [`MultiLoopChildWatcher`](../library/asyncio-policy.html#asyncio.MultiLoopChildWatcher "asyncio.MultiLoopChildWatcher"),
    [`FastChildWatcher`](../library/asyncio-policy.html#asyncio.FastChildWatcher "asyncio.FastChildWatcher"), [`AbstractChildWatcher`](../library/asyncio-policy.html#asyncio.AbstractChildWatcher "asyncio.AbstractChildWatcher")
    and [`SafeChildWatcher`](../library/asyncio-policy.html#asyncio.SafeChildWatcher "asyncio.SafeChildWatcher") are deprecated and
    will be removed in Python 3.14.
    (Contributed by Kumar Aditya in [gh-94597](https://github.com/python/cpython/issues/94597).)
  + [`asyncio.set_child_watcher()`](../library/asyncio-policy.html#asyncio.set_child_watcher "asyncio.set_child_watcher"), [`asyncio.get_child_watcher()`](../library/asyncio-policy.html#asyncio.get_child_watcher "asyncio.get_child_watcher"),
    [`asyncio.AbstractEventLoopPolicy.set_child_watcher()`](../library/asyncio-policy.html#asyncio.AbstractEventLoopPolicy.set_child_watcher "asyncio.AbstractEventLoopPolicy.set_child_watcher") and
    [`asyncio.AbstractEventLoopPolicy.get_child_watcher()`](../library/asyncio-policy.html#asyncio.AbstractEventLoopPolicy.get_child_watcher "asyncio.AbstractEventLoopPolicy.get_child_watcher") are deprecated
    and will be removed in Python 3.14.
    (Contributed by Kumar Aditya in [gh-94597](https://github.com/python/cpython/issues/94597).)
  + The [`get_event_loop()`](../library/asyncio-eventloop.html#asyncio.get_event_loop "asyncio.get_event_loop") method of the
    default event loop policy now emits a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") if there
    is no current event loop set and it decides to create one.
    (Contributed by Serhiy Storchaka and Guido van Rossum in [gh-100160](https://github.com/python/cpython/issues/100160).)
* [`collections.abc`](../library/collections.abc.html#module-collections.abc "collections.abc: Abstract base classes for containers"): Deprecated [`ByteString`](../library/collections.abc.html#collections.abc.ByteString "collections.abc.ByteString").
  Prefer `Sequence` or [`Buffer`](../library/collections.abc.html#collections.abc.Buffer "collections.abc.Buffer").
  For use in typing, prefer a union, like `bytes | bytearray`,
  or [`collections.abc.Buffer`](../library/collections.abc.html#collections.abc.Buffer "collections.abc.Buffer").
  (Contributed by Shantanu Jain in [gh-91896](https://github.com/python/cpython/issues/91896).)
* [`email`](../library/email.html#module-email "email: Package supporting the parsing, manipulating, and generating email messages."): Deprecated the *isdst* parameter in [`email.utils.localtime()`](../library/email.utils.html#email.utils.localtime "email.utils.localtime").
  (Contributed by Alan Williams in [gh-72346](https://github.com/python/cpython/issues/72346).)
* [`importlib`](../library/importlib.html#module-importlib "importlib: The implementation of the import machinery."): `__package__` and `__cached__` will cease to be set or
  taken into consideration by the import system ([gh-97879](https://github.com/python/cpython/issues/97879)).
* [`importlib.abc`](../library/importlib.html#module-importlib.abc "importlib.abc: Abstract base classes related to import") deprecated classes:

  + `importlib.abc.ResourceReader`
  + `importlib.abc.Traversable`
  + `importlib.abc.TraversableResources`

  Use [`importlib.resources.abc`](../library/importlib.resources.abc.html#module-importlib.resources.abc "importlib.resources.abc: Abstract base classes for resources") classes instead:

  + [`importlib.resources.abc.Traversable`](../library/importlib.resources.abc.html#importlib.resources.abc.Traversable "importlib.resources.abc.Traversable")
  + [`importlib.resources.abc.TraversableResources`](../library/importlib.resources.abc.html#importlib.resources.abc.TraversableResources "importlib.resources.abc.TraversableResources")

  (Contributed by Jason R. Coombs and Hugo van Kemenade in [gh-93963](https://github.com/python/cpython/issues/93963).)
* [`itertools`](../library/itertools.html#module-itertools "itertools: Functions creating iterators for efficient looping.") had undocumented, inefficient, historically buggy,
  and inconsistent support for copy, deepcopy, and pickle operations.
  This will be removed in 3.14 for a significant reduction in code
  volume and maintenance burden.
  (Contributed by Raymond Hettinger in [gh-101588](https://github.com/python/cpython/issues/101588).)
* [`multiprocessing`](../library/multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism."): The default start method will change to a safer one on
  Linux, BSDs, and other non-macOS POSIX platforms where `'fork'` is currently
  the default ([gh-84559](https://github.com/python/cpython/issues/84559)). Adding a runtime warning about this was deemed too
  disruptive as the majority of code is not expected to care. Use the
  [`get_context()`](../library/multiprocessing.html#multiprocessing.get_context "multiprocessing.get_context") or
  [`set_start_method()`](../library/multiprocessing.html#multiprocessing.set_start_method "multiprocessing.set_start_method") APIs to explicitly specify when
  your code *requires* `'fork'`. See [Contexts and start methods](../library/multiprocessing.html#multiprocessing-start-methods).
* [`pathlib`](../library/pathlib.html#module-pathlib "pathlib: Object-oriented filesystem paths"): [`is_relative_to()`](../library/pathlib.html#pathlib.PurePath.is_relative_to "pathlib.PurePath.is_relative_to") and
  [`relative_to()`](../library/pathlib.html#pathlib.PurePath.relative_to "pathlib.PurePath.relative_to"): passing additional arguments is
  deprecated.
* [`pkgutil`](../library/pkgutil.html#module-pkgutil "pkgutil: Utilities for the import system."): [`find_loader()`](../library/pkgutil.html#pkgutil.find_loader "pkgutil.find_loader") and [`get_loader()`](../library/pkgutil.html#pkgutil.get_loader "pkgutil.get_loader")
  now raise [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning");
  use [`importlib.util.find_spec()`](../library/importlib.html#importlib.util.find_spec "importlib.util.find_spec") instead.
  (Contributed by Nikita Sobolev in [gh-97850](https://github.com/python/cpython/issues/97850).)
* [`pty`](../library/pty.html#module-pty "pty: Pseudo-Terminal Handling for Unix. (Unix)"):

  + `master_open()`: use [`pty.openpty()`](../library/pty.html#pty.openpty "pty.openpty").
  + `slave_open()`: use [`pty.openpty()`](../library/pty.html#pty.openpty "pty.openpty").
* [`sqlite3`](../library/sqlite3.html#module-sqlite3 "sqlite3: A DB-API 2.0 implementation using SQLite 3.x."):

  + [`version`](../library/sqlite3.html#sqlite3.version "sqlite3.version") and [`version_info`](../library/sqlite3.html#sqlite3.version_info "sqlite3.version_info").
  + [`execute()`](../library/sqlite3.html#sqlite3.Cursor.execute "sqlite3.Cursor.execute") and [`executemany()`](../library/sqlite3.html#sqlite3.Cursor.executemany "sqlite3.Cursor.executemany")
    if [named placeholders](../library/sqlite3.html#sqlite3-placeholders) are used and
    *parameters* is a sequence instead of a [`dict`](../library/stdtypes.html#dict "dict").
* [`typing`](../library/typing.html#module-typing "typing: Support for type hints (see :pep:`484`)."): [`ByteString`](../library/typing.html#typing.ByteString "typing.ByteString"), deprecated since Python 3.9,
  now causes a [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") to be emitted when it is used.
* [`urllib`](../library/urllib.html#module-urllib "urllib"):
  `urllib.parse.Quoter` is deprecated: it was not intended to be a
  public API.
  (Contributed by Gregory P. Smith in [gh-88168](https://github.com/python/cpython/issues/88168).)

### Pending Removal in Python 3.15[¶](#pending-removal-in-python-3-15 "Link to this heading")

* [`http.server.CGIHTTPRequestHandler`](../library/http.server.html#http.server.CGIHTTPRequestHandler "http.server.CGIHTTPRequestHandler") will be removed along with its
  related `--cgi` flag to `python -m http.server`. It was obsolete and
  rarely used. No direct replacement exists. *Anything* is better than CGI
  to interface a web server with a request handler.
* [`importlib`](../library/importlib.html#module-importlib "importlib: The implementation of the import machinery."):

  + `load_module()` method: use `exec_module()` instead.
* [`locale`](../library/locale.html#module-locale "locale: Internationalization services."): [`locale.getdefaultlocale()`](../library/locale.html#locale.getdefaultlocale "locale.getdefaultlocale") was deprecated in Python 3.11
  and originally planned for removal in Python 3.13 ([gh-90817](https://github.com/python/cpython/issues/90817)),
  but removal has been postponed to Python 3.15.
  Use [`locale.setlocale()`](../library/locale.html#locale.setlocale "locale.setlocale"), [`locale.getencoding()`](../library/locale.html#locale.getencoding "locale.getencoding") and
  [`locale.getlocale()`](../library/locale.html#locale.getlocale "locale.getlocale") instead.
  (Contributed by Hugo van Kemenade in [gh-111187](https://github.com/python/cpython/issues/111187).)
* [`pathlib`](../library/pathlib.html#module-pathlib "pathlib: Object-oriented filesystem paths"):
  [`pathlib.PurePath.is_reserved()`](../library/pathlib.html#pathlib.PurePath.is_reserved "pathlib.PurePath.is_reserved") is deprecated and scheduled for
  removal in Python 3.15. From Python 3.13 onwards, use `os.path.isreserved`
  to detect reserved paths on Windows.
* [`platform`](../library/platform.html#module-platform "platform: Retrieves as much platform identifying data as possible."):
  [`java_ver()`](../library/platform.html#platform.java_ver "platform.java_ver") is deprecated and will be removed in 3.15.
  It was largely untested, had a confusing API,
  and was only useful for Jython support.
  (Contributed by Nikita Sobolev in [gh-116349](https://github.com/python/cpython/issues/116349).)
* [`sysconfig`](../library/sysconfig.html#module-sysconfig "sysconfig: Python's configuration information"):

  + The *check\_home* argument of [`sysconfig.is_python_build()`](../library/sysconfig.html#sysconfig.is_python_build "sysconfig.is_python_build") has been
    deprecated since Python 3.12.
* [`threading`](../library/threading.html#module-threading "threading: Thread-based parallelism."):
  Passing any arguments to [`threading.RLock()`](../library/threading.html#threading.RLock "threading.RLock") is now deprecated.
  C version allows any numbers of args and kwargs,
  but they are just ignored. Python version does not allow any arguments.
  All arguments will be removed from [`threading.RLock()`](../library/threading.html#threading.RLock "threading.RLock") in Python 3.15.
  (Contributed by Nikita Sobolev in [gh-102029](https://github.com/python/cpython/issues/102029).)
* [`typing.NamedTuple`](../library/typing.html#typing.NamedTuple "typing.NamedTuple"):

  + The undocumented keyword argument syntax for creating `NamedTuple` classes
    (`NT = NamedTuple("NT", x=int)`) is deprecated, and will be disallowed in
    3.15. Use the class-based syntax or the functional syntax instead.
* [`types`](../library/types.html#module-types "types: Names for built-in types."):

  + [`types.CodeType`](../library/types.html#types.CodeType "types.CodeType"): Accessing [`co_lnotab`](../reference/datamodel.html#codeobject.co_lnotab "codeobject.co_lnotab") was
    deprecated in [**PEP 626**](https://peps.python.org/pep-0626/)
    since 3.10 and was planned to be removed in 3.12,
    but it only got a proper [`DeprecationWarning`](../library/exceptions.html#DeprecationWarning "DeprecationWarning") in 3.12.
    May be removed in 3.15.
    (Contributed by Nikita Sobolev in [gh-101866](https://github.com/python/cpython/issues/101866).)
* [`typing`](../library/typing.html#module-typing "typing: Support for type hints (see :pep:`484`)."):

  + When using the functional syntax to create a `NamedTuple` class, failing to
    pass a value to the *fields* parameter (`NT = NamedTuple("NT")`) is
    deprecated. Passing `None` to the *fields* parameter
    (`NT = NamedTuple("NT", None)`) is also deprecated. Both will be
    disallowed in Python 3.15. To create a `NamedTuple` class with 0 fields, use
    `class NT(NamedTuple): pass` or `NT = NamedTuple("NT", [])`.
* [`typing.TypedDict`](../library/typing.html#typing.TypedDict "typing.TypedDict"): When using the functional syntax to create a
  `TypedDict` class, failing to pass a value to the *fields* parameter (`TD =
  TypedDict("TD")`) is deprecated. Passing `None` to the *fields* parameter
  (`TD = TypedDict("TD", None)`) is also deprecated. Both will be disallowed
  in Python 3.15. To create a `TypedDict` class with 0 fields, use `class
  TD(TypedDict): pass` or `TD = TypedDict("TD", {})`.
* [`wave`](../library/wave.html#module-wave "wave: Provide an interface to the WAV sound format."): Deprecate the `getmark()`, `setmark()` and `getmarkers()`
  methods of the [`wave.Wave_read`](../library/wave.html#wave.Wave_read "wave.Wave_read") and [`wave.Wave_write`](../library/wave.html#wave.Wave_write "wave.Wave_write") classes.
  They will be removed in Python 3.15.
  (Contributed by Victor Stinner in [gh-105096](https://github.com/python/cpython/issues/105096).)

### Pending Removal in Python 3.16[¶](#pending-removal-in-python-3-16 "Link to this heading")

* The import system:

  + Setting [`__loader__`](../reference/datamodel.html#module.__loader__ "module.__loader__") on a module while
    failing to set [`__spec__.loader`](../library/importlib.html#importlib.machinery.ModuleSpec.loader "importlib.machinery.ModuleSpec.loader")
    is deprecated. In Python 3.16, `__loader__` will cease to be set or
    taken into consideration by the import system or the standard library.
* [`array`](../library/array.html#module-array "array: Space efficient arrays of uniformly typed numeric values."):
  [`array.array`](../library/array.html#array.array "array.array") `'u'` type (`wchar_t`):
  use the `'w'` type instead (`Py_UCS4`).
* [`builtins`](../library/builtins.html#module-builtins "builtins: The module that provides the built-in namespace."):
  `~bool`, bitwise inversion on bool.
* [`symtable`](../library/symtable.html#module-symtable "symtable: Interface to the compiler's internal symbol tables."):
  Deprecate [`symtable.Class.get_methods()`](../library/symtable.html#symtable.Class.get_methods "symtable.Class.get_methods") due to the lack of interest.
  (Contributed by Bénédikt Tran in [gh-119698](https://github.com/python/cpython/issues/119698).)

### Pending Removal in Future Versions[¶](#pending-removal-in-future-versions "Link to this heading")

The following APIs will be removed in the future,
although there is currently no date scheduled for their removal.

* [`argparse`](../library/argparse.html#module-argparse "argparse: Command-line option and argument parsing library."): Nesting argument groups and nesting mutually exclusive
  groups are deprecated.
* [`array`](../library/array.html#module-array "array: Space efficient arrays of uniformly typed numeric values.")’s `'u'` format code ([gh-57281](https://github.com/python/cpython/issues/57281))
* [`builtins`](../library/builtins.html#module-builtins "builtins: The module that provides the built-in namespace."):

  + `bool(NotImplemented)`.
  + Generators: `throw(type, exc, tb)` and `athrow(type, exc, tb)`
    signature is deprecated: use `throw(exc)` and `athrow(exc)` instead,
    the single argument signature.
  + Currently Python accepts numeric literals immediately followed by keywords,
    for example `0in x`, `1or x`, `0if 1else 2`. It allows confusing and
    ambiguous expressions like `[0x1for x in y]` (which can be interpreted as
    `[0x1 for x in y]` or `[0x1f or x in y]`). A syntax warning is raised
    if the numeric literal is immediately followed by one of keywords
    [`and`](../reference/expressions.html#and), [`else`](../reference/compound_stmts.html#else), [`for`](../reference/compound_stmts.html#for), [`if`](../reference/compound_stmts.html#if),
    [`in`](../reference/expressions.html#in), [`is`](../reference/expressions.html#is) and [`or`](../reference/expressions.html#or). In a future release it
    will be changed to a syntax error. ([gh-87999](https://github.com/python/cpython/issues/87999))
  + Support for `__index__()` and `__int__()` method returning non-int type:
    these methods will be required to return an instance of a strict subclass of
    [`int`](../library/functions.html#int "int").
  + Support for `__float__()` method returning a strict subclass of
    [`float`](../library/functions.html#float "float"): these methods will be required to return an instance of
    [`float`](../library/functions.html#float "float").
  + Support for `__complex__()` method returning a strict subclass of
    [`complex`](../library/functions.html#complex "complex"): these methods will be required to return an instance of
    [`complex`](../library/functions.html#complex "complex").
  + Delegation of `int()` to `__trunc__()` method.
  + Passing a complex number as the *real* or *imag* argument in the
    [`complex()`](../library/functions.html#complex "complex") constructor is now deprecated; it should only be passed
    as a single positional argument.
    (Contributed by Serhiy Storchaka in [gh-109218](https://github.com/python/cpython/issues/109218).)
* [`calendar`](../library/calendar.html#module-calendar "calendar: Functions for working with calendars, including some emulation of the Unix cal program."): `calendar.January` and `calendar.February` constants are
  deprecated and replaced by [`calendar.JANUARY`](../library/calendar.html#calendar.JANUARY "calendar.JANUARY") and
  [`calendar.FEBRUARY`](../library/calendar.html#calendar.FEBRUARY "calendar.FEBRUARY").
  (Contributed by Prince Roshan in [gh-103636](https://github.com/python/cpython/issues/103636).)
* [`codeobject.co_lnotab`](../reference/datamodel.html#codeobject.co_lnotab "codeobject.co_lnotab"): use the [`codeobject.co_lines()`](../reference/datamodel.html#codeobject.co_lines "codeobject.co_lines") method
  instead.
* [`datetime`](../library/datetime.html#module-datetime "datetime: Basic date and time types."):

  + [`utcnow()`](../library/datetime.html#datetime.datetime.utcnow "datetime.datetime.utcnow"):
    use `datetime.datetime.now(tz=datetime.UTC)`.
  + [`utcfromtimestamp()`](../library/datetime.html#datetime.datetime.utcfromtimestamp "datetime.datetime.utcfromtimestamp"):
    use `datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)`.
* [`gettext`](../library/gettext.html#module-gettext "gettext: Multilingual internationalization services."): Plural value must be an integer.
* [`importlib`](../library/importlib.html#module-importlib "importlib: The implementation of the import machinery."):

  + [`cache_from_source()`](../library/importlib.html#importlib.util.cache_from_source "importlib.util.cache_from_source") *debug\_override* parameter is
    deprecated: use the *optimization* parameter instead.
* [`importlib.metadata`](../library/importlib.metadata.html#module-importlib.metadata "importlib.metadata: Accessing package metadata"):

  + `EntryPoints` tuple interface.
  + Implicit `None` on return values.
* [`mailbox`](../library/mailbox.html#module-mailbox "mailbox: Manipulate mailboxes in various formats"): Use of StringIO input and text mode is deprecated, use
  BytesIO and binary mode instead.
* [`os`](../library/os.html#module-os "os: Miscellaneous operating system interfaces."): Calling [`os.register_at_fork()`](../library/os.html#os.register_at_fork "os.register_at_fork") in multi-threaded process.
* `pydoc.ErrorDuringImport`: A tuple value for *exc\_info* parameter is
  deprecated, use an exception instance.
* [`re`](../library/re.html#module-re "re: Regular expression operations."): More strict rules are now applied for numerical group references
  and group names in regular expressions. Only sequence of ASCII digits is now
  accepted as a numerical reference. The group name in bytes patterns and
  replacement strings can now only contain ASCII letters and digits and
  underscore.
  (Contributed by Serhiy Storchaka in [gh-91760](https://github.com/python/cpython/issues/91760).)
* `sre_compile`, `sre_constants` and `sre_parse` modules.
* [`shutil`](../library/shutil.html#module-shutil "shutil: High-level file operations, including copying."): [`rmtree()`](../library/shutil.html#shutil.rmtree "shutil.rmtree")’s *onerror* parameter is deprecated in
  Python 3.12; use the *onexc* parameter instead.
* [`ssl`](../library/ssl.html#module-ssl "ssl: TLS/SSL wrapper for socket objects") options and protocols:

  + [`ssl.SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") without protocol argument is deprecated.
  + [`ssl.SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext"): [`set_npn_protocols()`](../library/ssl.html#ssl.SSLContext.set_npn_protocols "ssl.SSLContext.set_npn_protocols") and
    `selected_npn_protocol()` are deprecated: use ALPN
    instead.
  + `ssl.OP_NO_SSL*` options
  + `ssl.OP_NO_TLS*` options
  + `ssl.PROTOCOL_SSLv3`
  + `ssl.PROTOCOL_TLS`
  + `ssl.PROTOCOL_TLSv1`
  + `ssl.PROTOCOL_TLSv1_1`
  + `ssl.PROTOCOL_TLSv1_2`
  + `ssl.TLSVersion.SSLv3`
  + `ssl.TLSVersion.TLSv1`
  + `ssl.TLSVersion.TLSv1_1`
* [`threading`](../library/threading.html#module-threading "threading: Thread-based parallelism.") methods:

  + `threading.Condition.notifyAll()`: use [`notify_all()`](../library/threading.html#threading.Condition.notify_all "threading.Condition.notify_all").
  + `threading.Event.isSet()`: use [`is_set()`](../library/threading.html#threading.Event.is_set "threading.Event.is_set").
  + `threading.Thread.isDaemon()`, [`threading.Thread.setDaemon()`](../library/threading.html#threading.Thread.setDaemon "threading.Thread.setDaemon"):
    use [`threading.Thread.daemon`](../library/threading.html#threading.Thread.daemon "threading.Thread.daemon") attribute.
  + `threading.Thread.getName()`, [`threading.Thread.setName()`](../library/threading.html#threading.Thread.setName "threading.Thread.setName"):
    use [`threading.Thread.name`](../library/threading.html#threading.Thread.name "threading.Thread.name") attribute.
  + `threading.currentThread()`: use [`threading.current_thread()`](../library/threading.html#threading.current_thread "threading.current_thread").
  + `threading.activeCount()`: use [`threading.active_count()`](../library/threading.html#threading.active_count "threading.active_count").
* [`typing.Text`](../library/typing.html#typing.Text "typing.Text") ([gh-92332](https://github.com/python/cpython/issues/92332)).
* [`unittest.IsolatedAsyncioTestCase`](../library/unittest.html#unittest.IsolatedAsyncioTestCase "unittest.IsolatedAsyncioTestCase"): it is deprecated to return a value
  that is not `None` from a test case.
* [`urllib.parse`](../library/urllib.parse.html#module-urllib.parse "urllib.parse: Parse URLs into or assemble them from components.") deprecated functions: [`urlparse()`](../library/urllib.parse.html#urllib.parse.urlparse "urllib.parse.urlparse") instead

  + `splitattr()`
  + `splithost()`
  + `splitnport()`
  + `splitpasswd()`
  + `splitport()`
  + `splitquery()`
  + `splittag()`
  + `splittype()`
  + `splituser()`
  + `splitvalue()`
  + `to_bytes()`
* [`urllib.request`](../library/urllib.request.html#module-urllib.request "urllib.request: Extensible library for opening URLs."): [`URLopener`](../library/urllib.request.html#urllib.request.URLopener "urllib.request.URLopener") and
  [`FancyURLopener`](../library/urllib.request.html#urllib.request.FancyURLopener "urllib.request.FancyURLopener") style of invoking requests is
  deprecated. Use newer [`urlopen()`](../library/urllib.request.html#urllib.request.urlopen "urllib.request.urlopen") functions and methods.
* [`wsgiref`](../library/wsgiref.html#module-wsgiref "wsgiref: WSGI Utilities and Reference Implementation."): `SimpleHandler.stdout.write()` should not do partial
  writes.
* [`xml.etree.ElementTree`](../library/xml.etree.elementtree.html#module-xml.etree.ElementTree "xml.etree.ElementTree: Implementation of the ElementTree API."): Testing the truth value of an
  [`Element`](../library/xml.etree.elementtree.html#xml.etree.ElementTree.Element "xml.etree.ElementTree.Element") is deprecated. In a future release it
  will always return `True`. Prefer explicit `len(elem)` or
  `elem is not None` tests instead.
* [`zipimport.zipimporter.load_module()`](../library/zipimport.html#zipimport.zipimporter.load_module "zipimport.zipimporter.load_module") is deprecated:
  use [`exec_module()`](../library/zipimport.html#zipimport.zipimporter.exec_module "zipimport.zipimporter.exec_module") instead.

## Removed[¶](#removed "Link to this heading")

### asynchat and asyncore[¶](#asynchat-and-asyncore "Link to this heading")

* These two modules have been removed
  according to the schedule in [**PEP 594**](https://peps.python.org/pep-0594/),
  having been deprecated in Python 3.6.
  Use [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") instead.
  (Contributed by Nikita Sobolev in [gh-96580](https://github.com/python/cpython/issues/96580).)

### configparser[¶](#configparser "Link to this heading")

* Several names deprecated in the [`configparser`](../library/configparser.html#module-configparser "configparser: Configuration file parser.") way back in 3.2 have
  been removed per [gh-89336](https://github.com/python/cpython/issues/89336):

  + [`configparser.ParsingError`](../library/configparser.html#configparser.ParsingError "configparser.ParsingError") no longer has a `filename` attribute
    or argument. Use the `source` attribute and argument instead.
  + [`configparser`](../library/configparser.html#module-configparser "configparser: Configuration file parser.") no longer has a `SafeConfigParser` class. Use the
    shorter [`ConfigParser`](../library/configparser.html#configparser.ConfigParser "configparser.ConfigParser") name instead.
  + [`configparser.ConfigParser`](../library/configparser.html#configparser.ConfigParser "configparser.ConfigParser") no longer has a `readfp` method.
    Use [`read_file()`](../library/configparser.html#configparser.ConfigParser.read_file "configparser.ConfigParser.read_file") instead.

### distutils[¶](#distutils "Link to this heading")

* Remove the `distutils` package. It was deprecated in Python 3.10 by
  [**PEP 632**](https://peps.python.org/pep-0632/) “Deprecate distutils module”. For projects still using
  `distutils` and cannot be updated to something else, the `setuptools`
  project can be installed: it still provides `distutils`.
  (Contributed by Victor Stinner in [gh-92584](https://github.com/python/cpython/issues/92584).)

### ensurepip[¶](#ensurepip "Link to this heading")

* Remove the bundled setuptools wheel from [`ensurepip`](../library/ensurepip.html#module-ensurepip "ensurepip: Bootstrapping the \"pip\" installer into an existing Python installation or virtual environment."),
  and stop installing setuptools in environments created by [`venv`](../library/venv.html#module-venv "venv: Creation of virtual environments.").

  `pip (>= 22.1)` does not require setuptools to be installed in the
  environment. `setuptools`-based (and `distutils`-based) packages
  can still be used with `pip install`, since pip will provide
  `setuptools` in the build environment it uses for building a
  package.

  `easy_install`, `pkg_resources`, `setuptools` and `distutils`
  are no longer provided by default in environments created with
  `venv` or bootstrapped with `ensurepip`, since they are part of
  the `setuptools` package. For projects relying on these at runtime,
  the `setuptools` project should be declared as a dependency and
  installed separately (typically, using pip).

  (Contributed by Pradyun Gedam in [gh-95299](https://github.com/python/cpython/issues/95299).)

### enum[¶](#enum "Link to this heading")

* Remove [`enum`](../library/enum.html#module-enum "enum: Implementation of an enumeration class.")’s `EnumMeta.__getattr__`, which is no longer needed for
  enum attribute access.
  (Contributed by Ethan Furman in [gh-95083](https://github.com/python/cpython/issues/95083).)

### ftplib[¶](#ftplib "Link to this heading")

* Remove [`ftplib`](../library/ftplib.html#module-ftplib "ftplib: FTP protocol client (requires sockets).")’s `FTP_TLS.ssl_version` class attribute: use the
  *context* parameter instead.
  (Contributed by Victor Stinner in [gh-94172](https://github.com/python/cpython/issues/94172).)

### gzip[¶](#gzip "Link to this heading")

* Remove the `filename` attribute of [`gzip`](../library/gzip.html#module-gzip "gzip: Interfaces for gzip compression and decompression using file objects.")’s [`gzip.GzipFile`](../library/gzip.html#gzip.GzipFile "gzip.GzipFile"),
  deprecated since Python 2.6, use the [`name`](../library/gzip.html#gzip.GzipFile.name "gzip.GzipFile.name") attribute
  instead. In write mode, the `filename` attribute added `'.gz'` file
  extension if it was not present.
  (Contributed by Victor Stinner in [gh-94196](https://github.com/python/cpython/issues/94196).)

### hashlib[¶](#hashlib "Link to this heading")

* Remove the pure Python implementation of [`hashlib`](../library/hashlib.html#module-hashlib "hashlib: Secure hash and message digest algorithms.")’s
  [`hashlib.pbkdf2_hmac()`](../library/hashlib.html#hashlib.pbkdf2_hmac "hashlib.pbkdf2_hmac"), deprecated in Python 3.10. Python 3.10 and
  newer requires OpenSSL 1.1.1 ([**PEP 644**](https://peps.python.org/pep-0644/)): this OpenSSL version provides
  a C implementation of [`pbkdf2_hmac()`](../library/hashlib.html#hashlib.pbkdf2_hmac "hashlib.pbkdf2_hmac") which is faster.
  (Contributed by Victor Stinner in [gh-94199](https://github.com/python/cpython/issues/94199).)

### importlib[¶](#importlib "Link to this heading")

* Many previously deprecated cleanups in [`importlib`](../library/importlib.html#module-importlib "importlib: The implementation of the import machinery.") have now been
  completed:

  + References to, and support for `module_repr()` has been removed.
    (Contributed by Barry Warsaw in [gh-97850](https://github.com/python/cpython/issues/97850).)
  + `importlib.util.set_package`, `importlib.util.set_loader` and
    `importlib.util.module_for_loader` have all been removed. (Contributed by
    Brett Cannon and Nikita Sobolev in [gh-65961](https://github.com/python/cpython/issues/65961) and [gh-97850](https://github.com/python/cpython/issues/97850).)
  + Support for `find_loader()` and `find_module()` APIs have been
    removed. (Contributed by Barry Warsaw in [gh-98040](https://github.com/python/cpython/issues/98040).)
  + `importlib.abc.Finder`, `pkgutil.ImpImporter`, and `pkgutil.ImpLoader`
    have been removed. (Contributed by Barry Warsaw in [gh-98040](https://github.com/python/cpython/issues/98040).)

### imp[¶](#imp "Link to this heading")

* The `imp` module has been removed. (Contributed by Barry Warsaw in
  [gh-98040](https://github.com/python/cpython/issues/98040).)

  To migrate, consult the following correspondence table:

  > | imp | importlib |
  > | --- | --- |
  > | `imp.NullImporter` | Insert `None` into `sys.path_importer_cache` |
  > | `imp.cache_from_source()` | [`importlib.util.cache_from_source()`](../library/importlib.html#importlib.util.cache_from_source "importlib.util.cache_from_source") |
  > | `imp.find_module()` | [`importlib.util.find_spec()`](../library/importlib.html#importlib.util.find_spec "importlib.util.find_spec") |
  > | `imp.get_magic()` | [`importlib.util.MAGIC_NUMBER`](../library/importlib.html#importlib.util.MAGIC_NUMBER "importlib.util.MAGIC_NUMBER") |
  > | `imp.get_suffixes()` | [`importlib.machinery.SOURCE_SUFFIXES`](../library/importlib.html#importlib.machinery.SOURCE_SUFFIXES "importlib.machinery.SOURCE_SUFFIXES"), [`importlib.machinery.EXTENSION_SUFFIXES`](../library/importlib.html#importlib.machinery.EXTENSION_SUFFIXES "importlib.machinery.EXTENSION_SUFFIXES"), and [`importlib.machinery.BYTECODE_SUFFIXES`](../library/importlib.html#importlib.machinery.BYTECODE_SUFFIXES "importlib.machinery.BYTECODE_SUFFIXES") |
  > | `imp.get_tag()` | [`sys.implementation.cache_tag`](../library/sys.html#sys.implementation "sys.implementation") |
  > | `imp.load_module()` | [`importlib.import_module()`](../library/importlib.html#importlib.import_module "importlib.import_module") |
  > | `imp.new_module(name)` | `types.ModuleType(name)` |
  > | `imp.reload()` | [`importlib.reload()`](../library/importlib.html#importlib.reload "importlib.reload") |
  > | `imp.source_from_cache()` | [`importlib.util.source_from_cache()`](../library/importlib.html#importlib.util.source_from_cache "importlib.util.source_from_cache") |
  > | `imp.load_source()` | *See below* |

  Replace `imp.load_source()` with:

  ```
  import importlib.util
  import importlib.machinery

  def load_source(modname, filename):
      loader = importlib.machinery.SourceFileLoader(modname, filename)
      spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
      module = importlib.util.module_from_spec(spec)
      # The module is always executed and not cached in sys.modules.
      # Uncomment the following line to cache the module.
      # sys.modules[module.__name__] = module
      loader.exec_module(module)
      return module
  ```
* Remove `imp` functions and attributes with no replacements:

  + Undocumented functions:

    - `imp.init_builtin()`
    - `imp.load_compiled()`
    - `imp.load_dynamic()`
    - `imp.load_package()`
  + `imp.lock_held()`, `imp.acquire_lock()`, `imp.release_lock()`:
    the locking scheme has changed in Python 3.3 to per-module locks.
  + `imp.find_module()` constants: `SEARCH_ERROR`, `PY_SOURCE`,
    `PY_COMPILED`, `C_EXTENSION`, `PY_RESOURCE`, `PKG_DIRECTORY`,
    `C_BUILTIN`, `PY_FROZEN`, `PY_CODERESOURCE`, `IMP_HOOK`.

### io[¶](#io "Link to this heading")

* Remove [`io`](../library/io.html#module-io "io: Core tools for working with streams.")’s `io.OpenWrapper` and `_pyio.OpenWrapper`, deprecated in Python
  3.10: just use [`open()`](../library/functions.html#open "open") instead. The [`open()`](../library/functions.html#open "open") ([`io.open()`](../library/io.html#io.open "io.open"))
  function is a built-in function. Since Python 3.10, `_pyio.open()` is
  also a static method.
  (Contributed by Victor Stinner in [gh-94169](https://github.com/python/cpython/issues/94169).)

### locale[¶](#locale "Link to this heading")

* Remove [`locale`](../library/locale.html#module-locale "locale: Internationalization services.")’s `locale.format()` function, deprecated in Python 3.7:
  use [`locale.format_string()`](../library/locale.html#locale.format_string "locale.format_string") instead.
  (Contributed by Victor Stinner in [gh-94226](https://github.com/python/cpython/issues/94226).)

### smtpd[¶](#smtpd "Link to this heading")

* The `smtpd` module has been removed according to the schedule in [**PEP 594**](https://peps.python.org/pep-0594/),
  having been deprecated in Python 3.4.7 and 3.5.4.
  Use the [aiosmtpd](https://pypi.org/project/aiosmtpd/) PyPI module or any other
  [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.")-based server instead.
  (Contributed by Oleg Iarygin in [gh-93243](https://github.com/python/cpython/issues/93243).)

### sqlite3[¶](#id2 "Link to this heading")

* The following undocumented [`sqlite3`](../library/sqlite3.html#module-sqlite3 "sqlite3: A DB-API 2.0 implementation using SQLite 3.x.") features, deprecated in Python
  3.10, are now removed:

  + `sqlite3.enable_shared_cache()`
  + `sqlite3.OptimizedUnicode`

  If a shared cache must be used, open the database in URI mode using the
  `cache=shared` query parameter.

  The `sqlite3.OptimizedUnicode` text factory has been an alias for
  [`str`](../library/stdtypes.html#str "str") since Python 3.3. Code that previously set the text factory to
  `OptimizedUnicode` can either use `str` explicitly, or rely on the
  default value which is also `str`.

  (Contributed by Erlend E. Aasland in [gh-92548](https://github.com/python/cpython/issues/92548).)

### ssl[¶](#ssl "Link to this heading")

* Remove [`ssl`](../library/ssl.html#module-ssl "ssl: TLS/SSL wrapper for socket objects")’s `ssl.RAND_pseudo_bytes()` function, deprecated in Python 3.6:
  use [`os.urandom()`](../library/os.html#os.urandom "os.urandom") or [`ssl.RAND_bytes()`](../library/ssl.html#ssl.RAND_bytes "ssl.RAND_bytes") instead.
  (Contributed by Victor Stinner in [gh-94199](https://github.com/python/cpython/issues/94199).)
* Remove the `ssl.match_hostname()` function.
  It was deprecated in Python 3.7. OpenSSL performs
  hostname matching since Python 3.7, Python no longer uses the
  `ssl.match_hostname()` function.
  (Contributed by Victor Stinner in [gh-94199](https://github.com/python/cpython/issues/94199).)
* Remove the `ssl.wrap_socket()` function, deprecated in Python 3.7:
  instead, create a [`ssl.SSLContext`](../library/ssl.html#ssl.SSLContext "ssl.SSLContext") object and call its
  [`ssl.SSLContext.wrap_socket`](../library/ssl.html#ssl.SSLContext.wrap_socket "ssl.SSLContext.wrap_socket") method. Any package that still uses
  `ssl.wrap_socket()` is broken and insecure. The function neither sends a
  SNI TLS extension nor validates the server hostname. Code is subject to [**CWE 295**](https://cwe.mitre.org/data/definitions/295.html)
  (Improper Certificate Validation).
  (Contributed by Victor Stinner in [gh-94199](https://github.com/python/cpython/issues/94199).)

### unittest[¶](#id3 "Link to this heading")

* Remove many long-deprecated [`unittest`](../library/unittest.html#module-unittest "unittest: Unit testing framework for Python.") features:

  + A number of [`TestCase`](../library/unittest.html#unittest.TestCase "unittest.TestCase") method aliases:

    | Deprecated alias | Method Name | Deprecated in |
    | --- | --- | --- |
    | `failUnless` | [`assertTrue()`](../library/unittest.html#unittest.TestCase.assertTrue "unittest.TestCase.assertTrue") | 3.1 |
    | `failIf` | [`assertFalse()`](../library/unittest.html#unittest.TestCase.assertFalse "unittest.TestCase.assertFalse") | 3.1 |
    | `failUnlessEqual` | [`assertEqual()`](../library/unittest.html#unittest.TestCase.assertEqual "unittest.TestCase.assertEqual") | 3.1 |
    | `failIfEqual` | [`assertNotEqual()`](../library/unittest.html#unittest.TestCase.assertNotEqual "unittest.TestCase.assertNotEqual") | 3.1 |
    | `failUnlessAlmostEqual` | [`assertAlmostEqual()`](../library/unittest.html#unittest.TestCase.assertAlmostEqual "unittest.TestCase.assertAlmostEqual") | 3.1 |
    | `failIfAlmostEqual` | [`assertNotAlmostEqual()`](../library/unittest.html#unittest.TestCase.assertNotAlmostEqual "unittest.TestCase.assertNotAlmostEqual") | 3.1 |
    | `failUnlessRaises` | [`assertRaises()`](../library/unittest.html#unittest.TestCase.assertRaises "unittest.TestCase.assertRaises") | 3.1 |
    | `assert_` | [`assertTrue()`](../library/unittest.html#unittest.TestCase.assertTrue "unittest.TestCase.assertTrue") | 3.2 |
    | `assertEquals` | [`assertEqual()`](../library/unittest.html#unittest.TestCase.assertEqual "unittest.TestCase.assertEqual") | 3.2 |
    | `assertNotEquals` | [`assertNotEqual()`](../library/unittest.html#unittest.TestCase.assertNotEqual "unittest.TestCase.assertNotEqual") | 3.2 |
    | `assertAlmostEquals` | [`assertAlmostEqual()`](../library/unittest.html#unittest.TestCase.assertAlmostEqual "unittest.TestCase.assertAlmostEqual") | 3.2 |
    | `assertNotAlmostEquals` | [`assertNotAlmostEqual()`](../library/unittest.html#unittest.TestCase.assertNotAlmostEqual "unittest.TestCase.assertNotAlmostEqual") | 3.2 |
    | `assertRegexpMatches` | [`assertRegex()`](../library/unittest.html#unittest.TestCase.assertRegex "unittest.TestCase.assertRegex") | 3.2 |
    | `assertRaisesRegexp` | [`assertRaisesRegex()`](../library/unittest.html#unittest.TestCase.assertRaisesRegex "unittest.TestCase.assertRaisesRegex") | 3.2 |
    | `assertNotRegexpMatches` | [`assertNotRegex()`](../library/unittest.html#unittest.TestCase.assertNotRegex "unittest.TestCase.assertNotRegex") | 3.5 |

    You can use <https://github.com/isidentical/teyit> to automatically modernise
    your unit tests.
  + Undocumented and broken [`TestCase`](../library/unittest.html#unittest.TestCase "unittest.TestCase") method
    `assertDictContainsSubset` (deprecated in Python 3.2).
  + Undocumented [`TestLoader.loadTestsFromModule`](../library/unittest.html#unittest.TestLoader.loadTestsFromModule "unittest.TestLoader.loadTestsFromModule") parameter *use\_load\_tests*
    (deprecated and ignored since Python 3.5).
  + An alias of the [`TextTestResult`](../library/unittest.html#unittest.TextTestResult "unittest.TextTestResult") class:
    `_TextTestResult` (deprecated in Python 3.2).

  (Contributed by Serhiy Storchaka in [gh-89325](https://github.com/python/cpython/issues/89325).)

### webbrowser[¶](#webbrowser "Link to this heading")

* Remove support for obsolete browsers from [`webbrowser`](../library/webbrowser.html#module-webbrowser "webbrowser: Easy-to-use controller for web browsers.").
  The removed browsers include: Grail, Mosaic, Netscape, Galeon, Skipstone,
  Iceape, Firebird, and Firefox versions 35 and below ([gh-102871](https://github.com/python/cpython/issues/102871)).

### xml.etree.ElementTree[¶](#xml-etree-elementtree "Link to this heading")

* Remove the `ElementTree.Element.copy()` method of the
  pure Python implementation, deprecated in Python 3.10, use the
  [`copy.copy()`](../library/copy.html#copy.copy "copy.copy") function instead. The C implementation of [`xml.etree.ElementTree`](../library/xml.etree.elementtree.html#module-xml.etree.ElementTree "xml.etree.ElementTree: Implementation of the ElementTree API.")
  has no `copy()` method, only a `__copy__()` method.
  (Contributed by Victor Stinner in [gh-94383](https://github.com/python/cpython/issues/94383).)

### zipimport[¶](#zipimport "Link to this heading")

* Remove [`zipimport`](../library/zipimport.html#module-zipimport "zipimport: Support for importing Python modules from ZIP archives.")’s `find_loader()` and `find_module()` methods,
  deprecated in Python 3.10: use the `find_spec()` method instead. See
  [**PEP 451**](https://peps.python.org/pep-0451/) for the rationale.
  (Contributed by Victor Stinner in [gh-94379](https://github.com/python/cpython/issues/94379).)

### Others[¶](#others "Link to this heading")

* Remove the `suspicious` rule from the documentation `Makefile` and
  `Doc/tools/rstlint.py`, both in favor of [sphinx-lint](https://github.com/sphinx-contrib/sphinx-lint).
  (Contributed by Julien Palard in [gh-98179](https://github.com/python/cpython/issues/98179).)
* Remove the *keyfile* and *certfile* parameters from the
  [`ftplib`](../library/ftplib.html#module-ftplib "ftplib: FTP protocol client (requires sockets)."), [`imaplib`](../library/imaplib.html#module-imaplib "imaplib: IMAP4 protocol client (requires sockets)."), [`poplib`](../library/poplib.html#module-poplib "poplib: POP3 protocol client (requires sockets).") and [`smtplib`](../library/smtplib.html#module-smtplib "smtplib: SMTP protocol client (requires sockets).") modules,
  and the *key\_file*, *cert\_file* and *check\_hostname* parameters from the
  [`http.client`](../library/http.client.html#module-http.client "http.client: HTTP and HTTPS protocol client (requires sockets).") module,
  all deprecated since Python 3.6. Use the *context* parameter
  (*ssl\_context* in [`imaplib`](../library/imaplib.html#module-imaplib "imaplib: IMAP4 protocol client (requires sockets).")) instead.
  (Contributed by Victor Stinner in [gh-94172](https://github.com/python/cpython/issues/94172).)
* Remove `Jython` compatibility hacks from several stdlib modules and tests.
  (Contributed by Nikita Sobolev in [gh-99482](https://github.com/python/cpython/issues/99482).)
* Remove `_use_broken_old_ctypes_structure_semantics_` flag
  from [`ctypes`](../library/ctypes.html#module-ctypes "ctypes: A foreign function library for Python.") module.
  (Contributed by Nikita Sobolev in [gh-99285](https://github.com/python/cpython/issues/99285).)

## Porting to Python 3.12[¶](#porting-to-python-3-12 "Link to this heading")

This section lists previously described changes and other bugfixes
that may require changes to your code.

### Changes in the Python API[¶](#changes-in-the-python-api "Link to this heading")

* More strict rules are now applied for numerical group references and
  group names in regular expressions.
  Only sequence of ASCII digits is now accepted as a numerical reference.
  The group name in bytes patterns and replacement strings can now only
  contain ASCII letters and digits and underscore.
  (Contributed by Serhiy Storchaka in [gh-91760](https://github.com/python/cpython/issues/91760).)
* Remove `randrange()` functionality deprecated since Python 3.10. Formerly,
  `randrange(10.0)` losslessly converted to `randrange(10)`. Now, it raises a
  [`TypeError`](../library/exceptions.html#TypeError "TypeError"). Also, the exception raised for non-integer values such as
  `randrange(10.5)` or `randrange('10')` has been changed from [`ValueError`](../library/exceptions.html#ValueError "ValueError") to
  [`TypeError`](../library/exceptions.html#TypeError "TypeError"). This also prevents bugs where `randrange(1e25)` would silently
  select from a larger range than `randrange(10**25)`.
  (Originally suggested by Serhiy Storchaka [gh-86388](https://github.com/python/cpython/issues/86388).)
* [`argparse.ArgumentParser`](../library/argparse.html#argparse.ArgumentParser "argparse.ArgumentParser") changed encoding and error handler
  for reading arguments from file (e.g. `fromfile_prefix_chars` option)
  from default text encoding (e.g. [`locale.getpreferredencoding(False)`](../library/locale.html#locale.getpreferredencoding "locale.getpreferredencoding"))
  to [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler).
  Argument files should be encoded in UTF-8 instead of ANSI Codepage on Windows.
* Remove the `asyncore`-based `smtpd` module deprecated in Python 3.4.7
  and 3.5.4. A recommended replacement is the
  [`asyncio`](../library/asyncio.html#module-asyncio "asyncio: Asynchronous I/O.")-based [aiosmtpd](https://pypi.org/project/aiosmtpd/) PyPI module.
* [`shlex.split()`](../library/shlex.html#shlex.split "shlex.split"): Passing `None` for *s* argument now raises an
  exception, rather than reading [`sys.stdin`](../library/sys.html#sys.stdin "sys.stdin"). The feature was deprecated
  in Python 3.9.
  (Contributed by Victor Stinner in [gh-94352](https://github.com/python/cpython/issues/94352).)
* The [`os`](../library/os.html#module-os "os: Miscellaneous operating system interfaces.") module no longer accepts bytes-like paths, like
  [`bytearray`](../library/stdtypes.html#bytearray "bytearray") and [`memoryview`](../library/stdtypes.html#memoryview "memoryview") types: only the exact
  [`bytes`](../library/stdtypes.html#bytes "bytes") type is accepted for bytes strings.
  (Contributed by Victor Stinner in [gh-98393](https://github.com/python/cpython/issues/98393).)
* [`syslog.openlog()`](../library/syslog.html#syslog.openlog "syslog.openlog") and [`syslog.closelog()`](../library/syslog.html#syslog.closelog "syslog.closelog") now fail if used in subinterpreters.
  [`syslog.syslog()`](../library/syslog.html#syslog.syslog "syslog.syslog") may still be used in subinterpreters,
  but now only if [`syslog.openlog()`](../library/syslog.html#syslog.openlog "syslog.openlog") has already been called in the main interpreter.
  These new restrictions do not apply to the main interpreter,
  so only a very small set of users might be affected.
  This change helps with interpreter isolation. Furthermore, [`syslog`](../library/syslog.html#module-syslog "syslog: An interface to the Unix syslog library routines. (Unix)") is a wrapper
  around process-global resources, which are best managed from the main interpreter.
  (Contributed by Donghee Na in [gh-99127](https://github.com/python/cpython/issues/99127).)
* The undocumented locking behavior of [`cached_property()`](../library/functools.html#functools.cached_property "functools.cached_property")
  is removed, because it locked across all instances of the class, leading to high
  lock contention. This means that a cached property getter function could now run
  more than once for a single instance, if two threads race. For most simple
  cached properties (e.g. those that are idempotent and simply calculate a value
  based on other attributes of the instance) this will be fine. If
  synchronization is needed, implement locking within the cached property getter
  function or around multi-threaded access points.
* [`sys._current_exceptions()`](../library/sys.html#sys._current_exceptions "sys._current_exceptions") now returns a mapping from thread-id to an
  exception instance, rather than to a `(typ, exc, tb)` tuple.
  (Contributed by Irit Katriel in [gh-103176](https://github.com/python/cpython/issues/103176).)
* When extracting tar files using [`tarfile`](../library/tarfile.html#module-tarfile "tarfile: Read and write tar-format archive files.") or
  [`shutil.unpack_archive()`](../library/shutil.html#shutil.unpack_archive "shutil.unpack_archive"), pass the *filter* argument to limit features
  that may be surprising or dangerous.
  See [Extraction filters](../library/tarfile.html#tarfile-extraction-filter) for details.
* The output of the [`tokenize.tokenize()`](../library/tokenize.html#tokenize.tokenize "tokenize.tokenize") and [`tokenize.generate_tokens()`](../library/tokenize.html#tokenize.generate_tokens "tokenize.generate_tokens")
  functions is now changed due to the changes introduced in [**PEP 701**](https://peps.python.org/pep-0701/). This
  means that `STRING` tokens are not emitted any more for f-strings and the
  tokens described in [**PEP 701**](https://peps.python.org/pep-0701/) are now produced instead: `FSTRING_START`,
  `FSTRING_MIDDLE` and `FSTRING_END` are now emitted for f-string “string”
  parts in addition to the appropriate tokens for the tokenization in the
  expression components. For example for the f-string `f"start {1+1} end"`
  the old version of the tokenizer emitted:

  ```
  1,0-1,18:           STRING         'f"start {1+1} end"'
  ```

  while the new version emits:

  ```
  1,0-1,2:            FSTRING_START  'f"'
  1,2-1,8:            FSTRING_MIDDLE 'start '
  1,8-1,9:            OP             '{'
  1,9-1,10:           NUMBER         '1'
  1,10-1,11:          OP             '+'
  1,11-1,12:          NUMBER         '1'
  1,12-1,13:          OP             '}'
  1,13-1,17:          FSTRING_MIDDLE ' end'
  1,17-1,18:          FSTRING_END    '"'
  ```

  Additionally, there may be some minor behavioral changes as a consequence of the
  changes required to support [**PEP 701**](https://peps.python.org/pep-0701/). Some of these changes include:

  + The `type` attribute of the tokens emitted when tokenizing some invalid Python
    characters such as `!` has changed from `ERRORTOKEN` to `OP`.
  + Incomplete single-line strings now also raise [`tokenize.TokenError`](../library/tokenize.html#tokenize.TokenError "tokenize.TokenError") as incomplete
    multiline strings do.
  + Some incomplete or invalid Python code now raises [`tokenize.TokenError`](../library/tokenize.html#tokenize.TokenError "tokenize.TokenError") instead of
    returning arbitrary `ERRORTOKEN` tokens when tokenizing it.
  + Mixing tabs and spaces as indentation in the same file is not supported anymore and will
    raise a [`TabError`](../library/exceptions.html#TabError "TabError").
* The [`threading`](../library/threading.html#module-threading "threading: Thread-based parallelism.") module now expects the `_thread` module to have
  an `_is_main_interpreter` attribute. It is a function with no
  arguments that returns `True` if the current interpreter is the
  main interpreter.

  Any library or application that provides a custom `_thread` module
  should provide `_is_main_interpreter()`.
  (See [gh-112826](https://github.com/python/cpython/issues/112826).)

## Build Changes[¶](#build-changes "Link to this heading")

* Python no longer uses `setup.py` to build shared C extension modules.
  Build parameters like headers and libraries are detected in `configure`
  script. Extensions are built by `Makefile`. Most extensions use
  `pkg-config` and fall back to manual detection.
  (Contributed by Christian Heimes in [gh-93939](https://github.com/python/cpython/issues/93939).)
* `va_start()` with two parameters, like `va_start(args, format),`
  is now required to build Python.
  `va_start()` is no longer called with a single parameter.
  (Contributed by Kumar Aditya in [gh-93207](https://github.com/python/cpython/issues/93207).)
* CPython now uses the ThinLTO option as the default link time optimization policy
  if the Clang compiler accepts the flag.
  (Contributed by Donghee Na in [gh-89536](https://github.com/python/cpython/issues/89536).)
* Add `COMPILEALL_OPTS` variable in `Makefile` to override [`compileall`](../library/compileall.html#module-compileall "compileall: Tools for byte-compiling all Python source files in a directory tree.")
  options (default: `-j0`) in `make install`. Also merged the 3
  `compileall` commands into a single command to build .pyc files for all
  optimization levels (0, 1, 2) at once.
  (Contributed by Victor Stinner in [gh-99289](https://github.com/python/cpython/issues/99289).)
* Add platform triplets for 64-bit LoongArch:

  + loongarch64-linux-gnusf
  + loongarch64-linux-gnuf32
  + loongarch64-linux-gnu

  (Contributed by Zhang Na in [gh-90656](https://github.com/python/cpython/issues/90656).)
* `PYTHON_FOR_REGEN` now require Python 3.10 or newer.
* Autoconf 2.71 and aclocal 1.16.4 is now required to regenerate
  `!configure`.
  (Contributed by Christian Heimes in [gh-89886](https://github.com/python/cpython/issues/89886).)
* Windows builds and macOS installers from python.org now use OpenSSL 3.0.

## C API Changes[¶](#c-api-changes "Link to this heading")

### New Features[¶](#id4 "Link to this heading")

* [**PEP 697**](https://peps.python.org/pep-0697/): Introduce the [Unstable C API tier](../c-api/stable.html#unstable-c-api),
  intended for low-level tools like debuggers and JIT compilers.
  This API may change in each minor release of CPython without deprecation
  warnings.
  Its contents are marked by the `PyUnstable_` prefix in names.

  Code object constructors:

  + `PyUnstable_Code_New()` (renamed from `PyCode_New`)
  + `PyUnstable_Code_NewWithPosOnlyArgs()` (renamed from `PyCode_NewWithPosOnlyArgs`)

  Extra storage for code objects ([**PEP 523**](https://peps.python.org/pep-0523/)):

  + `PyUnstable_Eval_RequestCodeExtraIndex()` (renamed from `_PyEval_RequestCodeExtraIndex`)
  + `PyUnstable_Code_GetExtra()` (renamed from `_PyCode_GetExtra`)
  + `PyUnstable_Code_SetExtra()` (renamed from `_PyCode_SetExtra`)

  The original names will continue to be available until the respective
  API changes.

  (Contributed by Petr Viktorin in [gh-101101](https://github.com/python/cpython/issues/101101).)
* [**PEP 697**](https://peps.python.org/pep-0697/): Add an API for extending types whose instance memory layout is
  opaque:

  + [`PyType_Spec.basicsize`](../c-api/type.html#c.PyType_Spec.basicsize "PyType_Spec.basicsize") can be zero or negative to specify
    inheriting or extending the base class size.
  + [`PyObject_GetTypeData()`](../c-api/object.html#c.PyObject_GetTypeData "PyObject_GetTypeData") and [`PyType_GetTypeDataSize()`](../c-api/object.html#c.PyType_GetTypeDataSize "PyType_GetTypeDataSize")
    added to allow access to subclass-specific instance data.
  + [`Py_TPFLAGS_ITEMS_AT_END`](../c-api/typeobj.html#c.Py_TPFLAGS_ITEMS_AT_END "Py_TPFLAGS_ITEMS_AT_END") and [`PyObject_GetItemData()`](../c-api/object.html#c.PyObject_GetItemData "PyObject_GetItemData")
    added to allow safely extending certain variable-sized types, including
    [`PyType_Type`](../c-api/type.html#c.PyType_Type "PyType_Type").
  + [`Py_RELATIVE_OFFSET`](../c-api/structures.html#c.Py_RELATIVE_OFFSET "Py_RELATIVE_OFFSET") added to allow defining
    [`members`](../c-api/structures.html#c.PyMemberDef "PyMemberDef") in terms of a subclass-specific struct.

  (Contributed by Petr Viktorin in [gh-103509](https://github.com/python/cpython/issues/103509).)
* Add the new [limited C API](../c-api/stable.html#limited-c-api) function [`PyType_FromMetaclass()`](../c-api/type.html#c.PyType_FromMetaclass "PyType_FromMetaclass"),
  which generalizes the existing [`PyType_FromModuleAndSpec()`](../c-api/type.html#c.PyType_FromModuleAndSpec "PyType_FromModuleAndSpec") using
  an additional metaclass argument.
  (Contributed by Wenzel Jakob in [gh-93012](https://github.com/python/cpython/issues/93012).)
* API for creating objects that can be called using
  [the vectorcall protocol](../c-api/call.html#vectorcall) was added to the
  [Limited API](../c-api/stable.html#stable):

  + [`Py_TPFLAGS_HAVE_VECTORCALL`](../c-api/typeobj.html#c.Py_TPFLAGS_HAVE_VECTORCALL "Py_TPFLAGS_HAVE_VECTORCALL")
  + [`PyVectorcall_NARGS()`](../c-api/call.html#c.PyVectorcall_NARGS "PyVectorcall_NARGS")
  + [`PyVectorcall_Call()`](../c-api/call.html#c.PyVectorcall_Call "PyVectorcall_Call")
  + [`vectorcallfunc`](../c-api/call.html#c.vectorcallfunc "vectorcallfunc")

  The [`Py_TPFLAGS_HAVE_VECTORCALL`](../c-api/typeobj.html#c.Py_TPFLAGS_HAVE_VECTORCALL "Py_TPFLAGS_HAVE_VECTORCALL") flag is now removed from a class
  when the class’s [`__call__()`](../reference/datamodel.html#object.__call__ "object.__call__") method is reassigned.
  This makes vectorcall safe to use with mutable types (i.e. heap types
  without the immutable flag, [`Py_TPFLAGS_IMMUTABLETYPE`](../c-api/typeobj.html#c.Py_TPFLAGS_IMMUTABLETYPE "Py_TPFLAGS_IMMUTABLETYPE")).
  Mutable types that do not override [`tp_call`](../c-api/typeobj.html#c.PyTypeObject.tp_call "PyTypeObject.tp_call") now
  inherit the `Py_TPFLAGS_HAVE_VECTORCALL` flag.
  (Contributed by Petr Viktorin in [gh-93274](https://github.com/python/cpython/issues/93274).)

  The [`Py_TPFLAGS_MANAGED_DICT`](../c-api/typeobj.html#c.Py_TPFLAGS_MANAGED_DICT "Py_TPFLAGS_MANAGED_DICT") and [`Py_TPFLAGS_MANAGED_WEAKREF`](../c-api/typeobj.html#c.Py_TPFLAGS_MANAGED_WEAKREF "Py_TPFLAGS_MANAGED_WEAKREF")
  flags have been added. This allows extensions classes to support object
  [`__dict__`](../reference/datamodel.html#object.__dict__ "object.__dict__") and weakrefs with less bookkeeping,
  using less memory and with faster access.
* API for performing calls using
  [the vectorcall protocol](../c-api/call.html#vectorcall) was added to the
  [Limited API](../c-api/stable.html#stable):

  + [`PyObject_Vectorcall()`](../c-api/call.html#c.PyObject_Vectorcall "PyObject_Vectorcall")
  + [`PyObject_VectorcallMethod()`](../c-api/call.html#c.PyObject_VectorcallMethod "PyObject_VectorcallMethod")
  + [`PY_VECTORCALL_ARGUMENTS_OFFSET`](../c-api/call.html#c.PY_VECTORCALL_ARGUMENTS_OFFSET "PY_VECTORCALL_ARGUMENTS_OFFSET")

  This means that both the incoming and outgoing ends of the vector call
  protocol are now available in the [Limited API](../c-api/stable.html#stable). (Contributed
  by Wenzel Jakob in [gh-98586](https://github.com/python/cpython/issues/98586).)
* Add two new public functions,
  [`PyEval_SetProfileAllThreads()`](../c-api/init.html#c.PyEval_SetProfileAllThreads "PyEval_SetProfileAllThreads") and
  [`PyEval_SetTraceAllThreads()`](../c-api/init.html#c.PyEval_SetTraceAllThreads "PyEval_SetTraceAllThreads"), that allow to set tracing and profiling
  functions in all running threads in addition to the calling one. (Contributed
  by Pablo Galindo in [gh-93503](https://github.com/python/cpython/issues/93503).)
* Add new function [`PyFunction_SetVectorcall()`](../c-api/function.html#c.PyFunction_SetVectorcall "PyFunction_SetVectorcall") to the C API
  which sets the vectorcall field of a given [`PyFunctionObject`](../c-api/function.html#c.PyFunctionObject "PyFunctionObject").
  (Contributed by Andrew Frost in [gh-92257](https://github.com/python/cpython/issues/92257).)
* The C API now permits registering callbacks via [`PyDict_AddWatcher()`](../c-api/dict.html#c.PyDict_AddWatcher "PyDict_AddWatcher"),
  [`PyDict_Watch()`](../c-api/dict.html#c.PyDict_Watch "PyDict_Watch") and related APIs to be called whenever a dictionary
  is modified. This is intended for use by optimizing interpreters, JIT
  compilers, or debuggers.
  (Contributed by Carl Meyer in [gh-91052](https://github.com/python/cpython/issues/91052).)
* Add [`PyType_AddWatcher()`](../c-api/type.html#c.PyType_AddWatcher "PyType_AddWatcher") and [`PyType_Watch()`](../c-api/type.html#c.PyType_Watch "PyType_Watch") API to register
  callbacks to receive notification on changes to a type.
  (Contributed by Carl Meyer in [gh-91051](https://github.com/python/cpython/issues/91051).)
* Add [`PyCode_AddWatcher()`](../c-api/code.html#c.PyCode_AddWatcher "PyCode_AddWatcher") and [`PyCode_ClearWatcher()`](../c-api/code.html#c.PyCode_ClearWatcher "PyCode_ClearWatcher")
  APIs to register callbacks to receive notification on creation and
  destruction of code objects.
  (Contributed by Itamar Oren in [gh-91054](https://github.com/python/cpython/issues/91054).)
* Add [`PyFrame_GetVar()`](../c-api/frame.html#c.PyFrame_GetVar "PyFrame_GetVar") and [`PyFrame_GetVarString()`](../c-api/frame.html#c.PyFrame_GetVarString "PyFrame_GetVarString") functions to
  get a frame variable by its name.
  (Contributed by Victor Stinner in [gh-91248](https://github.com/python/cpython/issues/91248).)
* Add [`PyErr_GetRaisedException()`](../c-api/exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException") and [`PyErr_SetRaisedException()`](../c-api/exceptions.html#c.PyErr_SetRaisedException "PyErr_SetRaisedException")
  for saving and restoring the current exception.
  These functions return and accept a single exception object,
  rather than the triple arguments of the now-deprecated
  [`PyErr_Fetch()`](../c-api/exceptions.html#c.PyErr_Fetch "PyErr_Fetch") and [`PyErr_Restore()`](../c-api/exceptions.html#c.PyErr_Restore "PyErr_Restore").
  This is less error prone and a bit more efficient.
  (Contributed by Mark Shannon in [gh-101578](https://github.com/python/cpython/issues/101578).)
* Add `_PyErr_ChainExceptions1`, which takes an exception instance,
  to replace the legacy-API `_PyErr_ChainExceptions`, which is now
  deprecated. (Contributed by Mark Shannon in [gh-101578](https://github.com/python/cpython/issues/101578).)
* Add [`PyException_GetArgs()`](../c-api/exceptions.html#c.PyException_GetArgs "PyException_GetArgs") and [`PyException_SetArgs()`](../c-api/exceptions.html#c.PyException_SetArgs "PyException_SetArgs")
  as convenience functions for retrieving and modifying
  the [`args`](../library/exceptions.html#BaseException.args "BaseException.args") passed to the exception’s constructor.
  (Contributed by Mark Shannon in [gh-101578](https://github.com/python/cpython/issues/101578).)
* Add [`PyErr_DisplayException()`](../c-api/exceptions.html#c.PyErr_DisplayException "PyErr_DisplayException"), which takes an exception instance,
  to replace the legacy-api `PyErr_Display()`. (Contributed by
  Irit Katriel in [gh-102755](https://github.com/python/cpython/issues/102755)).

* [**PEP 683**](https://peps.python.org/pep-0683/): Introduce *Immortal Objects*, which allows objects
  to bypass reference counts, and related changes to the C-API:

  + `_Py_IMMORTAL_REFCNT`: The reference count that defines an object
    :   as immortal.
  + `_Py_IsImmortal` Checks if an object has the immortal reference count.
  + `PyObject_HEAD_INIT` This will now initialize reference count to
    :   `_Py_IMMORTAL_REFCNT` when used with `Py_BUILD_CORE`.
  + `SSTATE_INTERNED_IMMORTAL` An identifier for interned unicode objects
    :   that are immortal.
  + `SSTATE_INTERNED_IMMORTAL_STATIC` An identifier for interned unicode
    :   objects that are immortal and static
  + `sys.getunicodeinternedsize` This returns the total number of unicode
    :   objects that have been interned. This is now needed for `refleak.py` to
        correctly track reference counts and allocated blocks

  (Contributed by Eddie Elizondo in [gh-84436](https://github.com/python/cpython/issues/84436).)
* [**PEP 684**](https://peps.python.org/pep-0684/): Add the new [`Py_NewInterpreterFromConfig()`](../c-api/init.html#c.Py_NewInterpreterFromConfig "Py_NewInterpreterFromConfig")
  function and [`PyInterpreterConfig`](../c-api/init.html#c.PyInterpreterConfig "PyInterpreterConfig"), which may be used
  to create sub-interpreters with their own GILs.
  (See [PEP 684: A Per-Interpreter GIL](#whatsnew312-pep684) for more info.)
  (Contributed by Eric Snow in [gh-104110](https://github.com/python/cpython/issues/104110).)
* In the limited C API version 3.12, [`Py_INCREF()`](../c-api/refcounting.html#c.Py_INCREF "Py_INCREF") and
  [`Py_DECREF()`](../c-api/refcounting.html#c.Py_DECREF "Py_DECREF") functions are now implemented as opaque function calls to
  hide implementation details.
  (Contributed by Victor Stinner in [gh-105387](https://github.com/python/cpython/issues/105387).)

### Porting to Python 3.12[¶](#id5 "Link to this heading")

* Legacy Unicode APIs based on `Py_UNICODE*` representation has been removed.
  Please migrate to APIs based on UTF-8 or `wchar_t*`.
* Argument parsing functions like [`PyArg_ParseTuple()`](../c-api/arg.html#c.PyArg_ParseTuple "PyArg_ParseTuple") doesn’t support
  `Py_UNICODE*` based format (e.g. `u`, `Z`) anymore. Please migrate
  to other formats for Unicode like `s`, `z`, `es`, and `U`.
* `tp_weaklist` for all static builtin types is always `NULL`.
  This is an internal-only field on `PyTypeObject`
  but we’re pointing out the change in case someone happens to be
  accessing the field directly anyway. To avoid breakage, consider
  using the existing public C-API instead, or, if necessary, the
  (internal-only) `_PyObject_GET_WEAKREFS_LISTPTR()` macro.
* This internal-only [`PyTypeObject.tp_subclasses`](../c-api/typeobj.html#c.PyTypeObject.tp_subclasses "PyTypeObject.tp_subclasses") may now not be
  a valid object pointer. Its type was changed to void\* to
  reflect this. We mention this in case someone happens to be accessing the
  internal-only field directly.

  To get a list of subclasses, call the Python method
  [`__subclasses__()`](../reference/datamodel.html#type.__subclasses__ "type.__subclasses__") (using [`PyObject_CallMethod()`](../c-api/call.html#c.PyObject_CallMethod "PyObject_CallMethod"),
  for example).
* Add support of more formatting options (left aligning, octals, uppercase
  hexadecimals, `intmax_t`, `ptrdiff_t`, `wchar_t` C
  strings, variable width and precision) in [`PyUnicode_FromFormat()`](../c-api/unicode.html#c.PyUnicode_FromFormat "PyUnicode_FromFormat") and
  [`PyUnicode_FromFormatV()`](../c-api/unicode.html#c.PyUnicode_FromFormatV "PyUnicode_FromFormatV").
  (Contributed by Serhiy Storchaka in [gh-98836](https://github.com/python/cpython/issues/98836).)
* An unrecognized format character in [`PyUnicode_FromFormat()`](../c-api/unicode.html#c.PyUnicode_FromFormat "PyUnicode_FromFormat") and
  [`PyUnicode_FromFormatV()`](../c-api/unicode.html#c.PyUnicode_FromFormatV "PyUnicode_FromFormatV") now sets a [`SystemError`](../library/exceptions.html#SystemError "SystemError").
  In previous versions it caused all the rest of the format string to be
  copied as-is to the result string, and any extra arguments discarded.
  (Contributed by Serhiy Storchaka in [gh-95781](https://github.com/python/cpython/issues/95781).)
* Fix wrong sign placement in [`PyUnicode_FromFormat()`](../c-api/unicode.html#c.PyUnicode_FromFormat "PyUnicode_FromFormat") and
  [`PyUnicode_FromFormatV()`](../c-api/unicode.html#c.PyUnicode_FromFormatV "PyUnicode_FromFormatV").
  (Contributed by Philip Georgi in [gh-95504](https://github.com/python/cpython/issues/95504).)
* Extension classes wanting to add a [`__dict__`](../reference/datamodel.html#object.__dict__ "object.__dict__") or weak reference slot
  should use [`Py_TPFLAGS_MANAGED_DICT`](../c-api/typeobj.html#c.Py_TPFLAGS_MANAGED_DICT "Py_TPFLAGS_MANAGED_DICT") and
  [`Py_TPFLAGS_MANAGED_WEAKREF`](../c-api/typeobj.html#c.Py_TPFLAGS_MANAGED_WEAKREF "Py_TPFLAGS_MANAGED_WEAKREF") instead of `tp_dictoffset` and
  `tp_weaklistoffset`, respectively.
  The use of `tp_dictoffset` and `tp_weaklistoffset` is still
  supported, but does not fully support multiple inheritance
  ([gh-95589](https://github.com/python/cpython/issues/95589)), and performance may be worse.
  Classes declaring [`Py_TPFLAGS_MANAGED_DICT`](../c-api/typeobj.html#c.Py_TPFLAGS_MANAGED_DICT "Py_TPFLAGS_MANAGED_DICT") should call
  `_PyObject_VisitManagedDict()` and `_PyObject_ClearManagedDict()`
  to traverse and clear their instance’s dictionaries.
  To clear weakrefs, call [`PyObject_ClearWeakRefs()`](../c-api/weakref.html#c.PyObject_ClearWeakRefs "PyObject_ClearWeakRefs"), as before.
* The [`PyUnicode_FSDecoder()`](../c-api/unicode.html#c.PyUnicode_FSDecoder "PyUnicode_FSDecoder") function no longer accepts bytes-like
  paths, like [`bytearray`](../library/stdtypes.html#bytearray "bytearray") and [`memoryview`](../library/stdtypes.html#memoryview "memoryview") types: only the exact
  [`bytes`](../library/stdtypes.html#bytes "bytes") type is accepted for bytes strings.
  (Contributed by Victor Stinner in [gh-98393](https://github.com/python/cpython/issues/98393).)
* The [`Py_CLEAR`](../c-api/refcounting.html#c.Py_CLEAR "Py_CLEAR"), [`Py_SETREF`](../c-api/refcounting.html#c.Py_SETREF "Py_SETREF") and [`Py_XSETREF`](../c-api/refcounting.html#c.Py_XSETREF "Py_XSETREF")
  macros now only evaluate their arguments once. If an argument has side
  effects, these side effects are no longer duplicated.
  (Contributed by Victor Stinner in [gh-98724](https://github.com/python/cpython/issues/98724).)
* The interpreter’s error indicator is now always normalized. This means
  that [`PyErr_SetObject()`](../c-api/exceptions.html#c.PyErr_SetObject "PyErr_SetObject"), [`PyErr_SetString()`](../c-api/exceptions.html#c.PyErr_SetString "PyErr_SetString") and the other
  functions that set the error indicator now normalize the exception
  before storing it. (Contributed by Mark Shannon in [gh-101578](https://github.com/python/cpython/issues/101578).)
* `_Py_RefTotal` is no longer authoritative and only kept around
  for ABI compatibility. Note that it is an internal global and only
  available on debug builds. If you happen to be using it then you’ll
  need to start using `_Py_GetGlobalRefTotal()`.
* The following functions now select an appropriate metaclass for the newly
  created type:

  + [`PyType_FromSpec()`](../c-api/type.html#c.PyType_FromSpec "PyType_FromSpec")
  + [`PyType_FromSpecWithBases()`](../c-api/type.html#c.PyType_FromSpecWithBases "PyType_FromSpecWithBases")
  + [`PyType_FromModuleAndSpec()`](../c-api/type.html#c.PyType_FromModuleAndSpec "PyType_FromModuleAndSpec")

  Creating classes whose metaclass overrides [`tp_new`](../c-api/typeobj.html#c.PyTypeObject.tp_new "PyTypeObject.tp_new")
  is deprecated, and in Python 3.14+ it will be disallowed.
  Note that these functions ignore `tp_new` of the metaclass, possibly
  allowing incomplete initialization.

  Note that [`PyType_FromMetaclass()`](../c-api/type.html#c.PyType_FromMetaclass "PyType_FromMetaclass") (added in Python 3.12)
  already disallows creating classes whose metaclass overrides `tp_new`
  ([`__new__()`](../reference/datamodel.html#object.__new__ "object.__new__") in Python).

  Since `tp_new` overrides almost everything `PyType_From*` functions do,
  the two are incompatible with each other.
  The existing behavior – ignoring the metaclass for several steps
  of type creation – is unsafe in general, since (meta)classes assume that
  `tp_new` was called.
  There is no simple general workaround. One of the following may work for you:

  + If you control the metaclass, avoid using `tp_new` in it:

    - If initialization can be skipped, it can be done in
      [`tp_init`](../c-api/typeobj.html#c.PyTypeObject.tp_init "PyTypeObject.tp_init") instead.
    - If the metaclass doesn’t need to be instantiated from Python,
      set its `tp_new` to `NULL` using
      the [`Py_TPFLAGS_DISALLOW_INSTANTIATION`](../c-api/typeobj.html#c.Py_TPFLAGS_DISALLOW_INSTANTIATION "Py_TPFLAGS_DISALLOW_INSTANTIATION") flag.
      This makes it acceptable for `PyType_From*` functions.
  + Avoid `PyType_From*` functions: if you don’t need C-specific features
    (slots or setting the instance size), create types by [calling](../c-api/call.html#call)
    the metaclass.
  + If you *know* the `tp_new` can be skipped safely, filter the deprecation
    warning out using [`warnings.catch_warnings()`](../library/warnings.html#warnings.catch_warnings "warnings.catch_warnings") from Python.
* [`PyOS_InputHook`](../c-api/veryhigh.html#c.PyOS_InputHook "PyOS_InputHook") and [`PyOS_ReadlineFunctionPointer`](../c-api/veryhigh.html#c.PyOS_ReadlineFunctionPointer "PyOS_ReadlineFunctionPointer") are no
  longer called in [subinterpreters](../c-api/init.html#sub-interpreter-support). This is
  because clients generally rely on process-wide global state (since these
  callbacks have no way of recovering extension module state).

  This also avoids situations where extensions may find themselves running in a
  subinterpreter that they don’t support (or haven’t yet been loaded in). See
  [gh-104668](https://github.com/python/cpython/issues/104668) for more info.
* [`PyLongObject`](../c-api/long.html#c.PyLongObject "PyLongObject") has had its internals changed for better performance.
  Although the internals of [`PyLongObject`](../c-api/long.html#c.PyLongObject "PyLongObject") are private, they are used
  by some extension modules.
  The internal fields should no longer be accessed directly, instead the API
  functions beginning `PyLong_...` should be used instead.
  Two new *unstable* API functions are provided for efficient access to the
  value of [`PyLongObject`](../c-api/long.html#c.PyLongObject "PyLongObject")s which fit into a single machine word:

  + [`PyUnstable_Long_IsCompact()`](../c-api/long.html#c.PyUnstable_Long_IsCompact "PyUnstable_Long_IsCompact")
  + [`PyUnstable_Long_CompactValue()`](../c-api/long.html#c.PyUnstable_Long_CompactValue "PyUnstable_Long_CompactValue")
* Custom allocators, set via [`PyMem_SetAllocator()`](../c-api/memory.html#c.PyMem_SetAllocator "PyMem_SetAllocator"), are now
  required to be thread-safe, regardless of memory domain. Allocators
  that don’t have their own state, including “hooks”, are not affected.
  If your custom allocator is not already thread-safe and you need
  guidance then please create a new GitHub issue
  and CC `@ericsnowcurrently`.

### Deprecated[¶](#id6 "Link to this heading")

* In accordance with [**PEP 699**](https://peps.python.org/pep-0699/), the `ma_version_tag` field in [`PyDictObject`](../c-api/dict.html#c.PyDictObject "PyDictObject")
  is deprecated for extension modules. Accessing this field will generate a compiler
  warning at compile time. This field will be removed in Python 3.14.
  (Contributed by Ramvikrams and Kumar Aditya in [gh-101193](https://github.com/python/cpython/issues/101193). PEP by Ken Jin.)
* Deprecate global configuration variable:

  + [`Py_DebugFlag`](../c-api/init.html#c.Py_DebugFlag "Py_DebugFlag"): use [`PyConfig.parser_debug`](../c-api/init_config.html#c.PyConfig.parser_debug "PyConfig.parser_debug")
  + [`Py_VerboseFlag`](../c-api/init.html#c.Py_VerboseFlag "Py_VerboseFlag"): use [`PyConfig.verbose`](../c-api/init_config.html#c.PyConfig.verbose "PyConfig.verbose")
  + [`Py_QuietFlag`](../c-api/init.html#c.Py_QuietFlag "Py_QuietFlag"): use [`PyConfig.quiet`](../c-api/init_config.html#c.PyConfig.quiet "PyConfig.quiet")
  + [`Py_InteractiveFlag`](../c-api/init.html#c.Py_InteractiveFlag "Py_InteractiveFlag"): use [`PyConfig.interactive`](../c-api/init_config.html#c.PyConfig.interactive "PyConfig.interactive")
  + [`Py_InspectFlag`](../c-api/init.html#c.Py_InspectFlag "Py_InspectFlag"): use [`PyConfig.inspect`](../c-api/init_config.html#c.PyConfig.inspect "PyConfig.inspect")
  + [`Py_OptimizeFlag`](../c-api/init.html#c.Py_OptimizeFlag "Py_OptimizeFlag"): use [`PyConfig.optimization_level`](../c-api/init_config.html#c.PyConfig.optimization_level "PyConfig.optimization_level")
  + [`Py_NoSiteFlag`](../c-api/init.html#c.Py_NoSiteFlag "Py_NoSiteFlag"): use [`PyConfig.site_import`](../c-api/init_config.html#c.PyConfig.site_import "PyConfig.site_import")
  + [`Py_BytesWarningFlag`](../c-api/init.html#c.Py_BytesWarningFlag "Py_BytesWarningFlag"): use [`PyConfig.bytes_warning`](../c-api/init_config.html#c.PyConfig.bytes_warning "PyConfig.bytes_warning")
  + [`Py_FrozenFlag`](../c-api/init.html#c.Py_FrozenFlag "Py_FrozenFlag"): use [`PyConfig.pathconfig_warnings`](../c-api/init_config.html#c.PyConfig.pathconfig_warnings "PyConfig.pathconfig_warnings")
  + [`Py_IgnoreEnvironmentFlag`](../c-api/init.html#c.Py_IgnoreEnvironmentFlag "Py_IgnoreEnvironmentFlag"): use [`PyConfig.use_environment`](../c-api/init_config.html#c.PyConfig.use_environment "PyConfig.use_environment")
  + [`Py_DontWriteBytecodeFlag`](../c-api/init.html#c.Py_DontWriteBytecodeFlag "Py_DontWriteBytecodeFlag"): use [`PyConfig.write_bytecode`](../c-api/init_config.html#c.PyConfig.write_bytecode "PyConfig.write_bytecode")
  + [`Py_NoUserSiteDirectory`](../c-api/init.html#c.Py_NoUserSiteDirectory "Py_NoUserSiteDirectory"): use [`PyConfig.user_site_directory`](../c-api/init_config.html#c.PyConfig.user_site_directory "PyConfig.user_site_directory")
  + [`Py_UnbufferedStdioFlag`](../c-api/init.html#c.Py_UnbufferedStdioFlag "Py_UnbufferedStdioFlag"): use [`PyConfig.buffered_stdio`](../c-api/init_config.html#c.PyConfig.buffered_stdio "PyConfig.buffered_stdio")
  + [`Py_HashRandomizationFlag`](../c-api/init.html#c.Py_HashRandomizationFlag "Py_HashRandomizationFlag"): use [`PyConfig.use_hash_seed`](../c-api/init_config.html#c.PyConfig.use_hash_seed "PyConfig.use_hash_seed")
    and [`PyConfig.hash_seed`](../c-api/init_config.html#c.PyConfig.hash_seed "PyConfig.hash_seed")
  + [`Py_IsolatedFlag`](../c-api/init.html#c.Py_IsolatedFlag "Py_IsolatedFlag"): use [`PyConfig.isolated`](../c-api/init_config.html#c.PyConfig.isolated "PyConfig.isolated")
  + [`Py_LegacyWindowsFSEncodingFlag`](../c-api/init.html#c.Py_LegacyWindowsFSEncodingFlag "Py_LegacyWindowsFSEncodingFlag"): use [`PyPreConfig.legacy_windows_fs_encoding`](../c-api/init_config.html#c.PyPreConfig.legacy_windows_fs_encoding "PyPreConfig.legacy_windows_fs_encoding")
  + [`Py_LegacyWindowsStdioFlag`](../c-api/init.html#c.Py_LegacyWindowsStdioFlag "Py_LegacyWindowsStdioFlag"): use [`PyConfig.legacy_windows_stdio`](../c-api/init_config.html#c.PyConfig.legacy_windows_stdio "PyConfig.legacy_windows_stdio")
  + `Py_FileSystemDefaultEncoding`: use [`PyConfig.filesystem_encoding`](../c-api/init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding")
  + `Py_HasFileSystemDefaultEncoding`: use [`PyConfig.filesystem_encoding`](../c-api/init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding")
  + `Py_FileSystemDefaultEncodeErrors`: use [`PyConfig.filesystem_errors`](../c-api/init_config.html#c.PyConfig.filesystem_errors "PyConfig.filesystem_errors")
  + `Py_UTF8Mode`: use [`PyPreConfig.utf8_mode`](../c-api/init_config.html#c.PyPreConfig.utf8_mode "PyPreConfig.utf8_mode") (see [`Py_PreInitialize()`](../c-api/init_config.html#c.Py_PreInitialize "Py_PreInitialize"))

  The [`Py_InitializeFromConfig()`](../c-api/init_config.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig") API should be used with
  [`PyConfig`](../c-api/init_config.html#c.PyConfig "PyConfig") instead.
  (Contributed by Victor Stinner in [gh-77782](https://github.com/python/cpython/issues/77782).)
* Creating [`immutable types`](../c-api/typeobj.html#c.Py_TPFLAGS_IMMUTABLETYPE "Py_TPFLAGS_IMMUTABLETYPE") with mutable
  bases is deprecated and will be disabled in Python 3.14. ([gh-95388](https://github.com/python/cpython/issues/95388))
* The `structmember.h` header is deprecated, though it continues to be
  available and there are no plans to remove it.

  Its contents are now available just by including `Python.h`,
  with a `Py` prefix added if it was missing:

  + [`PyMemberDef`](../c-api/structures.html#c.PyMemberDef "PyMemberDef"), [`PyMember_GetOne()`](../c-api/structures.html#c.PyMember_GetOne "PyMember_GetOne") and
    [`PyMember_SetOne()`](../c-api/structures.html#c.PyMember_SetOne "PyMember_SetOne")
  + Type macros like [`Py_T_INT`](../c-api/structures.html#c.Py_T_INT "Py_T_INT"), [`Py_T_DOUBLE`](../c-api/structures.html#c.Py_T_DOUBLE "Py_T_DOUBLE"), etc.
    (previously `T_INT`, `T_DOUBLE`, etc.)
  + The flags [`Py_READONLY`](../c-api/structures.html#c.Py_READONLY "Py_READONLY") (previously `READONLY`) and
    [`Py_AUDIT_READ`](../c-api/structures.html#c.Py_AUDIT_READ "Py_AUDIT_READ") (previously all uppercase)

  Several items are not exposed from `Python.h`:

  + [`T_OBJECT`](../c-api/structures.html#c.T_OBJECT "T_OBJECT") (use [`Py_T_OBJECT_EX`](../c-api/structures.html#c.Py_T_OBJECT_EX "Py_T_OBJECT_EX"))
  + [`T_NONE`](../c-api/structures.html#c.T_NONE "T_NONE") (previously undocumented, and pretty quirky)
  + The macro `WRITE_RESTRICTED` which does nothing.
  + The macros `RESTRICTED` and `READ_RESTRICTED`, equivalents of
    [`Py_AUDIT_READ`](../c-api/structures.html#c.Py_AUDIT_READ "Py_AUDIT_READ").
  + In some configurations, `<stddef.h>` is not included from `Python.h`.
    It should be included manually when using `offsetof()`.

  The deprecated header continues to provide its original
  contents under the original names.
  Your old code can stay unchanged, unless the extra include and non-namespaced
  macros bother you greatly.

  (Contributed in [gh-47146](https://github.com/python/cpython/issues/47146) by Petr Viktorin, based on
  earlier work by Alexander Belopolsky and Matthias Braun.)
* [`PyErr_Fetch()`](../c-api/exceptions.html#c.PyErr_Fetch "PyErr_Fetch") and [`PyErr_Restore()`](../c-api/exceptions.html#c.PyErr_Restore "PyErr_Restore") are deprecated.
  Use [`PyErr_GetRaisedException()`](../c-api/exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException") and
  [`PyErr_SetRaisedException()`](../c-api/exceptions.html#c.PyErr_SetRaisedException "PyErr_SetRaisedException") instead.
  (Contributed by Mark Shannon in [gh-101578](https://github.com/python/cpython/issues/101578).)
* `PyErr_Display()` is deprecated. Use [`PyErr_DisplayException()`](../c-api/exceptions.html#c.PyErr_DisplayException "PyErr_DisplayException")
  instead. (Contributed by Irit Katriel in [gh-102755](https://github.com/python/cpython/issues/102755)).
* `_PyErr_ChainExceptions` is deprecated. Use `_PyErr_ChainExceptions1`
  instead. (Contributed by Irit Katriel in [gh-102192](https://github.com/python/cpython/issues/102192).)
* Using [`PyType_FromSpec()`](../c-api/type.html#c.PyType_FromSpec "PyType_FromSpec"), [`PyType_FromSpecWithBases()`](../c-api/type.html#c.PyType_FromSpecWithBases "PyType_FromSpecWithBases")
  or [`PyType_FromModuleAndSpec()`](../c-api/type.html#c.PyType_FromModuleAndSpec "PyType_FromModuleAndSpec") to create a class whose metaclass
  overrides [`tp_new`](../c-api/typeobj.html#c.PyTypeObject.tp_new "PyTypeObject.tp_new") is deprecated.
  Call the metaclass instead.

#### Pending Removal in Python 3.14[¶](#id7 "Link to this heading")

* The `ma_version_tag` field in [`PyDictObject`](../c-api/dict.html#c.PyDictObject "PyDictObject") for extension modules
  ([**PEP 699**](https://peps.python.org/pep-0699/); [gh-101193](https://github.com/python/cpython/issues/101193)).
* Creating [`immutable types`](../c-api/typeobj.html#c.Py_TPFLAGS_IMMUTABLETYPE "Py_TPFLAGS_IMMUTABLETYPE") with mutable
  bases ([gh-95388](https://github.com/python/cpython/issues/95388)).
* Functions to configure Python’s initialization, deprecated in Python 3.11:

  + `PySys_SetArgvEx()`:
    Set [`PyConfig.argv`](../c-api/init_config.html#c.PyConfig.argv "PyConfig.argv") instead.
  + `PySys_SetArgv()`:
    Set [`PyConfig.argv`](../c-api/init_config.html#c.PyConfig.argv "PyConfig.argv") instead.
  + `Py_SetProgramName()`:
    Set [`PyConfig.program_name`](../c-api/init_config.html#c.PyConfig.program_name "PyConfig.program_name") instead.
  + `Py_SetPythonHome()`:
    Set [`PyConfig.home`](../c-api/init_config.html#c.PyConfig.home "PyConfig.home") instead.

  The [`Py_InitializeFromConfig()`](../c-api/init_config.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig") API should be used with
  [`PyConfig`](../c-api/init_config.html#c.PyConfig "PyConfig") instead.
* Global configuration variables:

  + [`Py_DebugFlag`](../c-api/init.html#c.Py_DebugFlag "Py_DebugFlag"):
    Use [`PyConfig.parser_debug`](../c-api/init_config.html#c.PyConfig.parser_debug "PyConfig.parser_debug") instead.
  + [`Py_VerboseFlag`](../c-api/init.html#c.Py_VerboseFlag "Py_VerboseFlag"):
    Use [`PyConfig.verbose`](../c-api/init_config.html#c.PyConfig.verbose "PyConfig.verbose") instead.
  + [`Py_QuietFlag`](../c-api/init.html#c.Py_QuietFlag "Py_QuietFlag"):
    Use [`PyConfig.quiet`](../c-api/init_config.html#c.PyConfig.quiet "PyConfig.quiet") instead.
  + [`Py_InteractiveFlag`](../c-api/init.html#c.Py_InteractiveFlag "Py_InteractiveFlag"):
    Use [`PyConfig.interactive`](../c-api/init_config.html#c.PyConfig.interactive "PyConfig.interactive") instead.
  + [`Py_InspectFlag`](../c-api/init.html#c.Py_InspectFlag "Py_InspectFlag"):
    Use [`PyConfig.inspect`](../c-api/init_config.html#c.PyConfig.inspect "PyConfig.inspect") instead.
  + [`Py_OptimizeFlag`](../c-api/init.html#c.Py_OptimizeFlag "Py_OptimizeFlag"):
    Use [`PyConfig.optimization_level`](../c-api/init_config.html#c.PyConfig.optimization_level "PyConfig.optimization_level") instead.
  + [`Py_NoSiteFlag`](../c-api/init.html#c.Py_NoSiteFlag "Py_NoSiteFlag"):
    Use [`PyConfig.site_import`](../c-api/init_config.html#c.PyConfig.site_import "PyConfig.site_import") instead.
  + [`Py_BytesWarningFlag`](../c-api/init.html#c.Py_BytesWarningFlag "Py_BytesWarningFlag"):
    Use [`PyConfig.bytes_warning`](../c-api/init_config.html#c.PyConfig.bytes_warning "PyConfig.bytes_warning") instead.
  + [`Py_FrozenFlag`](../c-api/init.html#c.Py_FrozenFlag "Py_FrozenFlag"):
    Use [`PyConfig.pathconfig_warnings`](../c-api/init_config.html#c.PyConfig.pathconfig_warnings "PyConfig.pathconfig_warnings") instead.
  + [`Py_IgnoreEnvironmentFlag`](../c-api/init.html#c.Py_IgnoreEnvironmentFlag "Py_IgnoreEnvironmentFlag"):
    Use [`PyConfig.use_environment`](../c-api/init_config.html#c.PyConfig.use_environment "PyConfig.use_environment") instead.
  + [`Py_DontWriteBytecodeFlag`](../c-api/init.html#c.Py_DontWriteBytecodeFlag "Py_DontWriteBytecodeFlag"):
    Use [`PyConfig.write_bytecode`](../c-api/init_config.html#c.PyConfig.write_bytecode "PyConfig.write_bytecode") instead.
  + [`Py_NoUserSiteDirectory`](../c-api/init.html#c.Py_NoUserSiteDirectory "Py_NoUserSiteDirectory"):
    Use [`PyConfig.user_site_directory`](../c-api/init_config.html#c.PyConfig.user_site_directory "PyConfig.user_site_directory") instead.
  + [`Py_UnbufferedStdioFlag`](../c-api/init.html#c.Py_UnbufferedStdioFlag "Py_UnbufferedStdioFlag"):
    Use [`PyConfig.buffered_stdio`](../c-api/init_config.html#c.PyConfig.buffered_stdio "PyConfig.buffered_stdio") instead.
  + [`Py_HashRandomizationFlag`](../c-api/init.html#c.Py_HashRandomizationFlag "Py_HashRandomizationFlag"):
    Use [`PyConfig.use_hash_seed`](../c-api/init_config.html#c.PyConfig.use_hash_seed "PyConfig.use_hash_seed")
    and [`PyConfig.hash_seed`](../c-api/init_config.html#c.PyConfig.hash_seed "PyConfig.hash_seed") instead.
  + [`Py_IsolatedFlag`](../c-api/init.html#c.Py_IsolatedFlag "Py_IsolatedFlag"):
    Use [`PyConfig.isolated`](../c-api/init_config.html#c.PyConfig.isolated "PyConfig.isolated") instead.
  + [`Py_LegacyWindowsFSEncodingFlag`](../c-api/init.html#c.Py_LegacyWindowsFSEncodingFlag "Py_LegacyWindowsFSEncodingFlag"):
    Use [`PyPreConfig.legacy_windows_fs_encoding`](../c-api/init_config.html#c.PyPreConfig.legacy_windows_fs_encoding "PyPreConfig.legacy_windows_fs_encoding") instead.
  + [`Py_LegacyWindowsStdioFlag`](../c-api/init.html#c.Py_LegacyWindowsStdioFlag "Py_LegacyWindowsStdioFlag"):
    Use [`PyConfig.legacy_windows_stdio`](../c-api/init_config.html#c.PyConfig.legacy_windows_stdio "PyConfig.legacy_windows_stdio") instead.
  + `Py_FileSystemDefaultEncoding`:
    Use [`PyConfig.filesystem_encoding`](../c-api/init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding") instead.
  + `Py_HasFileSystemDefaultEncoding`:
    Use [`PyConfig.filesystem_encoding`](../c-api/init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding") instead.
  + `Py_FileSystemDefaultEncodeErrors`:
    Use [`PyConfig.filesystem_errors`](../c-api/init_config.html#c.PyConfig.filesystem_errors "PyConfig.filesystem_errors") instead.
  + `Py_UTF8Mode`:
    Use [`PyPreConfig.utf8_mode`](../c-api/init_config.html#c.PyPreConfig.utf8_mode "PyPreConfig.utf8_mode") instead.
    (see [`Py_PreInitialize()`](../c-api/init_config.html#c.Py_PreInitialize "Py_PreInitialize"))

  The [`Py_InitializeFromConfig()`](../c-api/init_config.html#c.Py_InitializeFromConfig "Py_InitializeFromConfig") API should be used with
  [`PyConfig`](../c-api/init_config.html#c.PyConfig "PyConfig") instead.

#### Pending Removal in Python 3.15[¶](#id8 "Link to this heading")

* The bundled copy of `libmpdecimal`.
* The [`PyImport_ImportModuleNoBlock()`](../c-api/import.html#c.PyImport_ImportModuleNoBlock "PyImport_ImportModuleNoBlock"):
  Use [`PyImport_ImportModule()`](../c-api/import.html#c.PyImport_ImportModule "PyImport_ImportModule") instead.
* [`PyWeakref_GetObject()`](../c-api/weakref.html#c.PyWeakref_GetObject "PyWeakref_GetObject") and [`PyWeakref_GET_OBJECT()`](../c-api/weakref.html#c.PyWeakref_GET_OBJECT "PyWeakref_GET_OBJECT"):
  Use `PyWeakref_GetRef()` instead.
* [`Py_UNICODE`](../c-api/unicode.html#c.Py_UNICODE "Py_UNICODE") type and the `Py_UNICODE_WIDE` macro:
  Use `wchar_t` instead.
* Python initialization functions:

  + [`PySys_ResetWarnOptions()`](../c-api/sys.html#c.PySys_ResetWarnOptions "PySys_ResetWarnOptions"):
    Clear [`sys.warnoptions`](../library/sys.html#sys.warnoptions "sys.warnoptions") and `warnings.filters` instead.
  + [`Py_GetExecPrefix()`](../c-api/init.html#c.Py_GetExecPrefix "Py_GetExecPrefix"):
    Get [`sys.exec_prefix`](../library/sys.html#sys.exec_prefix "sys.exec_prefix") instead.
  + [`Py_GetPath()`](../c-api/init.html#c.Py_GetPath "Py_GetPath"):
    Get [`sys.path`](../library/sys.html#sys.path "sys.path") instead.
  + [`Py_GetPrefix()`](../c-api/init.html#c.Py_GetPrefix "Py_GetPrefix"):
    Get [`sys.prefix`](../library/sys.html#sys.prefix "sys.prefix") instead.
  + [`Py_GetProgramFullPath()`](../c-api/init.html#c.Py_GetProgramFullPath "Py_GetProgramFullPath"):
    Get [`sys.executable`](../library/sys.html#sys.executable "sys.executable") instead.
  + [`Py_GetProgramName()`](../c-api/init.html#c.Py_GetProgramName "Py_GetProgramName"):
    Get [`sys.executable`](../library/sys.html#sys.executable "sys.executable") instead.
  + [`Py_GetPythonHome()`](../c-api/init.html#c.Py_GetPythonHome "Py_GetPythonHome"):
    Get [`PyConfig.home`](../c-api/init_config.html#c.PyConfig.home "PyConfig.home")
    or the [`PYTHONHOME`](../using/cmdline.html#envvar-PYTHONHOME) environment variable instead.

#### Pending Removal in Future Versions[¶](#id9 "Link to this heading")

The following APIs are deprecated and will be removed,
although there is currently no date scheduled for their removal.

* [`Py_TPFLAGS_HAVE_FINALIZE`](../c-api/typeobj.html#c.Py_TPFLAGS_HAVE_FINALIZE "Py_TPFLAGS_HAVE_FINALIZE"):
  Unneeded since Python 3.8.
* [`PyErr_Fetch()`](../c-api/exceptions.html#c.PyErr_Fetch "PyErr_Fetch"):
  Use [`PyErr_GetRaisedException()`](../c-api/exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException") instead.
* [`PyErr_NormalizeException()`](../c-api/exceptions.html#c.PyErr_NormalizeException "PyErr_NormalizeException"):
  Use [`PyErr_GetRaisedException()`](../c-api/exceptions.html#c.PyErr_GetRaisedException "PyErr_GetRaisedException") instead.
* [`PyErr_Restore()`](../c-api/exceptions.html#c.PyErr_Restore "PyErr_Restore"):
  Use [`PyErr_SetRaisedException()`](../c-api/exceptions.html#c.PyErr_SetRaisedException "PyErr_SetRaisedException") instead.
* [`PyModule_GetFilename()`](../c-api/module.html#c.PyModule_GetFilename "PyModule_GetFilename"):
  Use [`PyModule_GetFilenameObject()`](../c-api/module.html#c.PyModule_GetFilenameObject "PyModule_GetFilenameObject") instead.
* [`PyOS_AfterFork()`](../c-api/sys.html#c.PyOS_AfterFork "PyOS_AfterFork"):
  Use [`PyOS_AfterFork_Child()`](../c-api/sys.html#c.PyOS_AfterFork_Child "PyOS_AfterFork_Child") instead.
* [`PySlice_GetIndicesEx()`](../c-api/slice.html#c.PySlice_GetIndicesEx "PySlice_GetIndicesEx"):
  Use [`PySlice_Unpack()`](../c-api/slice.html#c.PySlice_Unpack "PySlice_Unpack") and [`PySlice_AdjustIndices()`](../c-api/slice.html#c.PySlice_AdjustIndices "PySlice_AdjustIndices") instead.
* `PyUnicode_AsDecodedObject()`:
  Use [`PyCodec_Decode()`](../c-api/codec.html#c.PyCodec_Decode "PyCodec_Decode") instead.
* `PyUnicode_AsDecodedUnicode()`:
  Use [`PyCodec_Decode()`](../c-api/codec.html#c.PyCodec_Decode "PyCodec_Decode") instead.
* `PyUnicode_AsEncodedObject()`:
  Use [`PyCodec_Encode()`](../c-api/codec.html#c.PyCodec_Encode "PyCodec_Encode") instead.
* `PyUnicode_AsEncodedUnicode()`:
  Use [`PyCodec_Encode()`](../c-api/codec.html#c.PyCodec_Encode "PyCodec_Encode") instead.
* [`PyUnicode_READY()`](../c-api/unicode.html#c.PyUnicode_READY "PyUnicode_READY"):
  Unneeded since Python 3.12
* `PyErr_Display()`:
  Use [`PyErr_DisplayException()`](../c-api/exceptions.html#c.PyErr_DisplayException "PyErr_DisplayException") instead.
* `_PyErr_ChainExceptions()`:
  Use `_PyErr_ChainExceptions1()` instead.
* `PyBytesObject.ob_shash` member:
  call [`PyObject_Hash()`](../c-api/object.html#c.PyObject_Hash "PyObject_Hash") instead.
* `PyDictObject.ma_version_tag` member.
* Thread Local Storage (TLS) API:

  + [`PyThread_create_key()`](../c-api/init.html#c.PyThread_create_key "PyThread_create_key"):
    Use [`PyThread_tss_alloc()`](../c-api/init.html#c.PyThread_tss_alloc "PyThread_tss_alloc") instead.
  + [`PyThread_delete_key()`](../c-api/init.html#c.PyThread_delete_key "PyThread_delete_key"):
    Use [`PyThread_tss_free()`](../c-api/init.html#c.PyThread_tss_free "PyThread_tss_free") instead.
  + [`PyThread_set_key_value()`](../c-api/init.html#c.PyThread_set_key_value "PyThread_set_key_value"):
    Use [`PyThread_tss_set()`](../c-api/init.html#c.PyThread_tss_set "PyThread_tss_set") instead.
  + [`PyThread_get_key_value()`](../c-api/init.html#c.PyThread_get_key_value "PyThread_get_key_value"):
    Use [`PyThread_tss_get()`](../c-api/init.html#c.PyThread_tss_get "PyThread_tss_get") instead.
  + [`PyThread_delete_key_value()`](../c-api/init.html#c.PyThread_delete_key_value "PyThread_delete_key_value"):
    Use [`PyThread_tss_delete()`](../c-api/init.html#c.PyThread_tss_delete "PyThread_tss_delete") instead.
  + [`PyThread_ReInitTLS()`](../c-api/init.html#c.PyThread_ReInitTLS "PyThread_ReInitTLS"):
    Unneeded since Python 3.7.

### Removed[¶](#id10 "Link to this heading")

* Remove the `token.h` header file. There was never any public tokenizer C
  API. The `token.h` header file was only designed to be used by Python
  internals.
  (Contributed by Victor Stinner in [gh-92651](https://github.com/python/cpython/issues/92651).)
* Legacy Unicode APIs have been removed. See [**PEP 623**](https://peps.python.org/pep-0623/) for detail.

  + `PyUnicode_WCHAR_KIND`
  + `PyUnicode_AS_UNICODE()`
  + `PyUnicode_AsUnicode()`
  + `PyUnicode_AsUnicodeAndSize()`
  + `PyUnicode_AS_DATA()`
  + `PyUnicode_FromUnicode()`
  + `PyUnicode_GET_SIZE()`
  + `PyUnicode_GetSize()`
  + `PyUnicode_GET_DATA_SIZE()`
* Remove the `PyUnicode_InternImmortal()` function macro.
  (Contributed by Victor Stinner in [gh-85858](https://github.com/python/cpython/issues/85858).)

## Notable changes in 3.12.4[¶](#notable-changes-in-3-12-4 "Link to this heading")

### ipaddress[¶](#ipaddress "Link to this heading")

* Fixed `is_global` and `is_private` behavior in `IPv4Address`,
  `IPv6Address`, `IPv4Network` and `IPv6Network`.

## Notable changes in 3.12.5[¶](#notable-changes-in-3-12-5 "Link to this heading")

### email[¶](#email "Link to this heading")

* Headers with embedded newlines are now quoted on output.

  The [`generator`](../library/email.generator.html#module-email.generator "email.generator: Generate flat text email messages from a message structure.") will now refuse to serialize (write) headers
  that are improperly folded or delimited, such that they would be parsed as
  multiple headers or joined with adjacent data.
  If you need to turn this safety feature off,
  set [`verify_generated_headers`](../library/email.policy.html#email.policy.Policy.verify_generated_headers "email.policy.Policy.verify_generated_headers").
  (Contributed by Bas Bloemsaat and Petr Viktorin in [gh-121650](https://github.com/python/cpython/issues/121650).)

## Notable changes in 3.12.6[¶](#notable-changes-in-3-12-6 "Link to this heading")

### email[¶](#id11 "Link to this heading")

* [`email.utils.getaddresses()`](../library/email.utils.html#email.utils.getaddresses "email.utils.getaddresses") and [`email.utils.parseaddr()`](../library/email.utils.html#email.utils.parseaddr "email.utils.parseaddr") now return
  `('', '')` 2-tuples in more situations where invalid email addresses are
  encountered, instead of potentially inaccurate values.
  An optional *strict* parameter was added to these two functions:
  use `strict=False` to get the old behavior, accepting malformed inputs.
  `getattr(email.utils, 'supports_strict_parsing', False)` can be used to
  check if the *strict* paramater is available.
  (Contributed by Thomas Dwyer and Victor Stinner for [gh-102988](https://github.com/python/cpython/issues/102988) to improve
  the CVE-2023-27043 fix.)

## Notable changes in 3.12.8[¶](#notable-changes-in-3-12-8 "Link to this heading")

### sys[¶](#id12 "Link to this heading")

* The previously undocumented special function [`sys.getobjects()`](../library/sys.html#sys.getobjects "sys.getobjects"),
  which only exists in specialized builds of Python, may now return objects
  from other interpreters than the one it’s called in.

## Notable changes in 3.12.10[¶](#notable-changes-in-3-12-10 "Link to this heading")

### os.path[¶](#id13 "Link to this heading")

* The *strict* parameter to [`os.path.realpath()`](../library/os.path.html#os.path.realpath "os.path.realpath") accepts a new value,
  [`os.path.ALLOW_MISSING`](../library/os.path.html#os.path.ALLOW_MISSING "os.path.ALLOW_MISSING").
  If used, errors other than [`FileNotFoundError`](../library/exceptions.html#FileNotFoundError "FileNotFoundError") will be re-raised;
  the resulting path can be missing but it will be free of symlinks.
  (Contributed by Petr Viktorin for [**CVE 2025-4517**](https://www.cve.org/CVERecord?id=CVE-2025-4517).)

### tarfile[¶](#tarfile "Link to this heading")

* [`data_filter()`](../library/tarfile.html#tarfile.data_filter "tarfile.data_filter") now normalizes symbolic link targets in order to
  avoid path traversal attacks.
  (Contributed by Petr Viktorin in [gh-127987](https://github.com/python/cpython/issues/127987) and [**CVE 2025-4138**](https://www.cve.org/CVERecord?id=CVE-2025-4138).)
* [`extractall()`](../library/tarfile.html#tarfile.TarFile.extractall "tarfile.TarFile.extractall") now skips fixing up directory attributes
  when a directory was removed or replaced by another kind of file.
  (Contributed by Petr Viktorin in [gh-127987](https://github.com/python/cpython/issues/127987) and [**CVE 2024-12718**](https://www.cve.org/CVERecord?id=CVE-2024-12718).)
* [`extract()`](../library/tarfile.html#tarfile.TarFile.extract "tarfile.TarFile.extract") and [`extractall()`](../library/tarfile.html#tarfile.TarFile.extractall "tarfile.TarFile.extractall")
  now (re-)apply the extraction filter when substituting a link (hard or
  symbolic) with a copy of another archive member, and when fixing up
  directory attributes.
  The former raises a new exception, [`LinkFallbackError`](../library/tarfile.html#tarfile.LinkFallbackError "tarfile.LinkFallbackError").
  (Contributed by Petr Viktorin for [**CVE 2025-4330**](https://www.cve.org/CVERecord?id=CVE-2025-4330) and [**CVE 2024-12718**](https://www.cve.org/CVERecord?id=CVE-2024-12718).)
* [`extract()`](../library/tarfile.html#tarfile.TarFile.extract "tarfile.TarFile.extract") and [`extractall()`](../library/tarfile.html#tarfile.TarFile.extractall "tarfile.TarFile.extractall")
  no longer extract rejected members when
  [`errorlevel()`](../library/tarfile.html#tarfile.TarFile.errorlevel "tarfile.TarFile.errorlevel") is zero.
  (Contributed by Matt Prodani and Petr Viktorin in [gh-112887](https://github.com/python/cpython/issues/112887)
  and [**CVE 2025-4435**](https://www.cve.org/CVERecord?id=CVE-2025-4435).)

### [Table of Contents](../contents.html)

* [What’s New In Python 3.12](#)
  + [Summary – Release highlights](#summary-release-highlights)
  + [New Features](#new-features)
    - [PEP 695: Type Parameter Syntax](#pep-695-type-parameter-syntax)
    - [PEP 701: Syntactic formalization of f-strings](#pep-701-syntactic-formalization-of-f-strings)
    - [PEP 684: A Per-Interpreter GIL](#pep-684-a-per-interpreter-gil)
    - [PEP 669: Low impact monitoring for CPython](#pep-669-low-impact-monitoring-for-cpython)
    - [PEP 688: Making the buffer protocol accessible in Python](#pep-688-making-the-buffer-protocol-accessible-in-python)
    - [PEP 709: Comprehension inlining](#pep-709-comprehension-inlining)
    - [Improved Error Messages](#improved-error-messages)
  + [New Features Related to Type Hints](#new-features-related-to-type-hints)
    - [PEP 692: Using `TypedDict` for more precise `**kwargs` typing](#pep-692-using-typeddict-for-more-precise-kwargs-typing)
    - [PEP 698: Override Decorator for Static Typing](#pep-698-override-decorator-for-static-typing)
  + [Other Language Changes](#other-language-changes)
  + [New Modules](#new-modules)
  + [Improved Modules](#improved-modules)
    - [array](#array)
    - [asyncio](#asyncio)
    - [calendar](#calendar)
    - [csv](#csv)
    - [dis](#dis)
    - [fractions](#fractions)
    - [importlib.resources](#importlib-resources)
    - [inspect](#inspect)
    - [itertools](#itertools)
    - [math](#math)
    - [os](#os)
    - [os.path](#os-path)
    - [pathlib](#pathlib)
    - [platform](#platform)
    - [pdb](#pdb)
    - [random](#random)
    - [shutil](#shutil)
    - [sqlite3](#sqlite3)
    - [statistics](#statistics)
    - [sys](#sys)
    - [tempfile](#tempfile)
    - [threading](#threading)
    - [tkinter](#tkinter)
    - [tokenize](#tokenize)
    - [types](#types)
    - [typing](#typing)
    - [unicodedata](#unicodedata)
    - [unittest](#unittest)
    - [uuid](#uuid)
  + [Optimizations](#optimizations)
  + [CPython bytecode changes](#cpython-bytecode-changes)
  + [Demos and Tools](#demos-and-tools)
  + [Deprecated](#deprecated)
    - [Pending Removal in Python 3.13](#pending-removal-in-python-3-13)
    - [Pending Removal in Python 3.14](#pending-removal-in-python-3-14)
    - [Pending Removal in Python 3.15](#pending-removal-in-python-3-15)
    - [Pending Removal in Python 3.16](#pending-removal-in-python-3-16)
    - [Pending Removal in Future Versions](#pending-removal-in-future-versions)
  + [Removed](#removed)
    - [asynchat and asyncore](#asynchat-and-asyncore)
    - [configparser](#configparser)
    - [distutils](#distutils)
    - [ensurepip](#ensurepip)
    - [enum](#enum)
    - [ftplib](#ftplib)
    - [gzip](#gzip)
    - [hashlib](#hashlib)
    - [importlib](#importlib)
    - [imp](#imp)
    - [io](#io)
    - [locale](#locale)
    - [smtpd](#smtpd)
    - [sqlite3](#id2)
    - [ssl](#ssl)
    - [unittest](#id3)
    - [webbrowser](#webbrowser)
    - [xml.etree.ElementTree](#xml-etree-elementtree)
    - [zipimport](#zipimport)
    - [Others](#others)
  + [Porting to Python 3.12](#porting-to-python-3-12)
    - [Changes in the Python API](#changes-in-the-python-api)
  + [Build Changes](#build-changes)
  + [C API Changes](#c-api-changes)
    - [New Features](#id4)
    - [Porting to Python 3.12](#id5)
    - [Deprecated](#id6)
      * [Pending Removal in Python 3.14](#id7)
      * [Pending Removal in Python 3.15](#id8)
      * [Pending Removal in Future Versions](#id9)
    - [Removed](#id10)
  + [Notable changes in 3.12.4](#notable-changes-in-3-12-4)
    - [ipaddress](#ipaddress)
  + [Notable changes in 3.12.5](#notable-changes-in-3-12-5)
    - [email](#email)
  + [Notable changes in 3.12.6](#notable-changes-in-3-12-6)
    - [email](#id11)
  + [Notable changes in 3.12.8](#notable-changes-in-3-12-8)
    - [sys](#id12)
  + [Notable changes in 3.12.10](#notable-changes-in-3-12-10)
    - [os.path](#id13)
    - [tarfile](#tarfile)

#### Previous topic

[What’s New in Python](index.html "previous chapter")

#### Next topic

[What’s New In Python 3.11](3.11.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/whatsnew/3.12.rst)

«

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](3.11.html "What’s New In Python 3.11") |
* [previous](index.html "What’s New in Python") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [What’s New in Python](index.html) »
* What’s New In Python 3.12
* |
* Theme
  Auto
  Light
  Dark
   |

© [Copyright](../copyright.html) 2001-2026, Python Software Foundation.
  
This page is licensed under the Python Software Foundation License Version 2.
  
Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License.
  
See [History and License](/license.html) for more information.  
  
The Python Software Foundation is a non-profit corporation.
[Please donate.](https://www.python.org/psf/donations/)
  
  
Last updated on Mar 07, 2026 (17:44 UTC).
[Found a bug](/bugs.html)?
  
Created using [Sphinx](https://www.sphinx-doc.org/) 8.2.3.