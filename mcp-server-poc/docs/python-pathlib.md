pathlib — Object-oriented filesystem paths — Python 3.12.13 documentation

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

* [`pathlib` — Object-oriented filesystem paths](#)
  + [Basic use](#basic-use)
  + [Pure paths](#pure-paths)
    - [General properties](#general-properties)
    - [Operators](#operators)
    - [Accessing individual parts](#accessing-individual-parts)
    - [Methods and properties](#methods-and-properties)
  + [Concrete paths](#concrete-paths)
    - [Expanding and resolving paths](#expanding-and-resolving-paths)
    - [Querying file type and status](#querying-file-type-and-status)
    - [Reading and writing files](#reading-and-writing-files)
    - [Reading directories](#reading-directories)
    - [Creating files and directories](#creating-files-and-directories)
    - [Renaming and deleting](#renaming-and-deleting)
    - [Permissions and ownership](#permissions-and-ownership)
  + [Correspondence to tools in the `os` module](#correspondence-to-tools-in-the-os-module)

#### Previous topic

[File and Directory Access](filesys.html "previous chapter")

#### Next topic

[`os.path` — Common pathname manipulations](os.path.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/pathlib.rst)

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](os.path.html "os.path — Common pathname manipulations") |
* [previous](filesys.html "File and Directory Access") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [File and Directory Access](filesys.html) »
* `pathlib` — Object-oriented filesystem paths
* |
* Theme
  Auto
  Light
  Dark
   |

# `pathlib` — Object-oriented filesystem paths[¶](#module-pathlib "Link to this heading")

Added in version 3.4.

**Source code:** [Lib/pathlib.py](https://github.com/python/cpython/tree/3.12/Lib/pathlib.py)

---

This module offers classes representing filesystem paths with semantics
appropriate for different operating systems. Path classes are divided
between [pure paths](#pure-paths), which provide purely computational
operations without I/O, and [concrete paths](#concrete-paths), which
inherit from pure paths but also provide I/O operations.

If you’ve never used this module before or just aren’t sure which class is
right for your task, [`Path`](#pathlib.Path "pathlib.Path") is most likely what you need. It instantiates
a [concrete path](#concrete-paths) for the platform the code is running on.

Pure paths are useful in some special cases; for example:

1. If you want to manipulate Windows paths on a Unix machine (or vice versa).
   You cannot instantiate a [`WindowsPath`](#pathlib.WindowsPath "pathlib.WindowsPath") when running on Unix, but you
   can instantiate [`PureWindowsPath`](#pathlib.PureWindowsPath "pathlib.PureWindowsPath").
2. You want to make sure that your code only manipulates paths without actually
   accessing the OS. In this case, instantiating one of the pure classes may be
   useful since those simply don’t have any OS-accessing operations.

See also

[**PEP 428**](https://peps.python.org/pep-0428/): The pathlib module – object-oriented filesystem paths.

See also

For low-level path manipulation on strings, you can also use the
[`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.") module.

## Basic use[¶](#basic-use "Link to this heading")

Importing the main class:

```
>>> from pathlib import Path
```

Listing subdirectories:

```
>>> p = Path('.')
>>> [x for x in p.iterdir() if x.is_dir()]
[PosixPath('.hg'), PosixPath('docs'), PosixPath('dist'),
 PosixPath('__pycache__'), PosixPath('build')]
```

Listing Python source files in this directory tree:

```
>>> list(p.glob('**/*.py'))
[PosixPath('test_pathlib.py'), PosixPath('setup.py'),
 PosixPath('pathlib.py'), PosixPath('docs/conf.py'),
 PosixPath('build/lib/pathlib.py')]
```

Navigating inside a directory tree:

```
>>> p = Path('/etc')
>>> q = p / 'init.d' / 'reboot'
>>> q
PosixPath('/etc/init.d/reboot')
>>> q.resolve()
PosixPath('/etc/rc.d/init.d/halt')
```

Querying path properties:

```
>>> q.exists()
True
>>> q.is_dir()
False
```

Opening a file:

```
>>> with q.open() as f: f.readline()
...
'#!/bin/bash\n'
```

## Pure paths[¶](#pure-paths "Link to this heading")

Pure path objects provide path-handling operations which don’t actually
access a filesystem. There are three ways to access these classes, which
we also call *flavours*:

*class* pathlib.PurePath(*\*pathsegments*)[¶](#pathlib.PurePath "Link to this definition")
:   A generic class that represents the system’s path flavour (instantiating
    it creates either a [`PurePosixPath`](#pathlib.PurePosixPath "pathlib.PurePosixPath") or a [`PureWindowsPath`](#pathlib.PureWindowsPath "pathlib.PureWindowsPath")):

    ```
    >>> PurePath('setup.py')      # Running on a Unix machine
    PurePosixPath('setup.py')
    ```

    Each element of *pathsegments* can be either a string representing a
    path segment, or an object implementing the [`os.PathLike`](os.html#os.PathLike "os.PathLike") interface
    where the [`__fspath__()`](os.html#os.PathLike.__fspath__ "os.PathLike.__fspath__") method returns a string,
    such as another path object:

    ```
    >>> PurePath('foo', 'some/path', 'bar')
    PurePosixPath('foo/some/path/bar')
    >>> PurePath(Path('foo'), Path('bar'))
    PurePosixPath('foo/bar')
    ```

    When *pathsegments* is empty, the current directory is assumed:

    ```
    >>> PurePath()
    PurePosixPath('.')
    ```

    If a segment is an absolute path, all previous segments are ignored
    (like [`os.path.join()`](os.path.html#os.path.join "os.path.join")):

    ```
    >>> PurePath('/etc', '/usr', 'lib64')
    PurePosixPath('/usr/lib64')
    >>> PureWindowsPath('c:/Windows', 'd:bar')
    PureWindowsPath('d:bar')
    ```

    On Windows, the drive is not reset when a rooted relative path
    segment (e.g., `r'\foo'`) is encountered:

    ```
    >>> PureWindowsPath('c:/Windows', '/Program Files')
    PureWindowsPath('c:/Program Files')
    ```

    Spurious slashes and single dots are collapsed, but double dots (`'..'`)
    and leading double slashes (`'//'`) are not, since this would change the
    meaning of a path for various reasons (e.g. symbolic links, UNC paths):

    ```
    >>> PurePath('foo//bar')
    PurePosixPath('foo/bar')
    >>> PurePath('//foo/bar')
    PurePosixPath('//foo/bar')
    >>> PurePath('foo/./bar')
    PurePosixPath('foo/bar')
    >>> PurePath('foo/../bar')
    PurePosixPath('foo/../bar')
    ```

    (a naïve approach would make `PurePosixPath('foo/../bar')` equivalent
    to `PurePosixPath('bar')`, which is wrong if `foo` is a symbolic link
    to another directory)

    Pure path objects implement the [`os.PathLike`](os.html#os.PathLike "os.PathLike") interface, allowing them
    to be used anywhere the interface is accepted.

    Changed in version 3.6: Added support for the [`os.PathLike`](os.html#os.PathLike "os.PathLike") interface.

*class* pathlib.PurePosixPath(*\*pathsegments*)[¶](#pathlib.PurePosixPath "Link to this definition")
:   A subclass of [`PurePath`](#pathlib.PurePath "pathlib.PurePath"), this path flavour represents non-Windows
    filesystem paths:

    ```
    >>> PurePosixPath('/etc/hosts')
    PurePosixPath('/etc/hosts')
    ```

    *pathsegments* is specified similarly to [`PurePath`](#pathlib.PurePath "pathlib.PurePath").

*class* pathlib.PureWindowsPath(*\*pathsegments*)[¶](#pathlib.PureWindowsPath "Link to this definition")
:   A subclass of [`PurePath`](#pathlib.PurePath "pathlib.PurePath"), this path flavour represents Windows
    filesystem paths, including [UNC paths](https://en.wikipedia.org/wiki/Path_(computing)#UNC):

    ```
    >>> PureWindowsPath('c:/', 'Users', 'Ximénez')
    PureWindowsPath('c:/Users/Ximénez')
    >>> PureWindowsPath('//server/share/file')
    PureWindowsPath('//server/share/file')
    ```

    *pathsegments* is specified similarly to [`PurePath`](#pathlib.PurePath "pathlib.PurePath").

Regardless of the system you’re running on, you can instantiate all of
these classes, since they don’t provide any operation that does system calls.

### General properties[¶](#general-properties "Link to this heading")

Paths are immutable and [hashable](../glossary.html#term-hashable). Paths of a same flavour are comparable
and orderable. These properties respect the flavour’s case-folding
semantics:

```
>>> PurePosixPath('foo') == PurePosixPath('FOO')
False
>>> PureWindowsPath('foo') == PureWindowsPath('FOO')
True
>>> PureWindowsPath('FOO') in { PureWindowsPath('foo') }
True
>>> PureWindowsPath('C:') < PureWindowsPath('d:')
True
```

Paths of a different flavour compare unequal and cannot be ordered:

```
>>> PureWindowsPath('foo') == PurePosixPath('foo')
False
>>> PureWindowsPath('foo') < PurePosixPath('foo')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: '<' not supported between instances of 'PureWindowsPath' and 'PurePosixPath'
```

### Operators[¶](#operators "Link to this heading")

The slash operator helps create child paths, like [`os.path.join()`](os.path.html#os.path.join "os.path.join").
If the argument is an absolute path, the previous path is ignored.
On Windows, the drive is not reset when the argument is a rooted
relative path (e.g., `r'\foo'`):

```
>>> p = PurePath('/etc')
>>> p
PurePosixPath('/etc')
>>> p / 'init.d' / 'apache2'
PurePosixPath('/etc/init.d/apache2')
>>> q = PurePath('bin')
>>> '/usr' / q
PurePosixPath('/usr/bin')
>>> p / '/an_absolute_path'
PurePosixPath('/an_absolute_path')
>>> PureWindowsPath('c:/Windows', '/Program Files')
PureWindowsPath('c:/Program Files')
```

A path object can be used anywhere an object implementing [`os.PathLike`](os.html#os.PathLike "os.PathLike")
is accepted:

```
>>> import os
>>> p = PurePath('/etc')
>>> os.fspath(p)
'/etc'
```

The string representation of a path is the raw filesystem path itself
(in native form, e.g. with backslashes under Windows), which you can
pass to any function taking a file path as a string:

```
>>> p = PurePath('/etc')
>>> str(p)
'/etc'
>>> p = PureWindowsPath('c:/Program Files')
>>> str(p)
'c:\\Program Files'
```

Similarly, calling [`bytes`](stdtypes.html#bytes "bytes") on a path gives the raw filesystem path as a
bytes object, as encoded by [`os.fsencode()`](os.html#os.fsencode "os.fsencode"):

```
>>> bytes(p)
b'/etc'
```

Note

Calling [`bytes`](stdtypes.html#bytes "bytes") is only recommended under Unix. Under Windows,
the unicode form is the canonical representation of filesystem paths.

### Accessing individual parts[¶](#accessing-individual-parts "Link to this heading")

To access the individual “parts” (components) of a path, use the following
property:

PurePath.parts[¶](#pathlib.PurePath.parts "Link to this definition")
:   A tuple giving access to the path’s various components:

    ```
    >>> p = PurePath('/usr/bin/python3')
    >>> p.parts
    ('/', 'usr', 'bin', 'python3')

    >>> p = PureWindowsPath('c:/Program Files/PSF')
    >>> p.parts
    ('c:\\', 'Program Files', 'PSF')
    ```

    (note how the drive and local root are regrouped in a single part)

### Methods and properties[¶](#methods-and-properties "Link to this heading")

Pure paths provide the following methods and properties:

PurePath.drive[¶](#pathlib.PurePath.drive "Link to this definition")
:   A string representing the drive letter or name, if any:

    ```
    >>> PureWindowsPath('c:/Program Files/').drive
    'c:'
    >>> PureWindowsPath('/Program Files/').drive
    ''
    >>> PurePosixPath('/etc').drive
    ''
    ```

    UNC shares are also considered drives:

    ```
    >>> PureWindowsPath('//host/share/foo.txt').drive
    '\\\\host\\share'
    ```

PurePath.root[¶](#pathlib.PurePath.root "Link to this definition")
:   A string representing the (local or global) root, if any:

    ```
    >>> PureWindowsPath('c:/Program Files/').root
    '\\'
    >>> PureWindowsPath('c:Program Files/').root
    ''
    >>> PurePosixPath('/etc').root
    '/'
    ```

    UNC shares always have a root:

    ```
    >>> PureWindowsPath('//host/share').root
    '\\'
    ```

    If the path starts with more than two successive slashes,
    [`PurePosixPath`](#pathlib.PurePosixPath "pathlib.PurePosixPath") collapses them:

    ```
    >>> PurePosixPath('//etc').root
    '//'
    >>> PurePosixPath('///etc').root
    '/'
    >>> PurePosixPath('////etc').root
    '/'
    ```

    Note

    This behavior conforms to *The Open Group Base Specifications Issue 6*,
    paragraph [4.11 Pathname Resolution](https://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap04.html#tag_04_11):

    *“A pathname that begins with two successive slashes may be interpreted in
    an implementation-defined manner, although more than two leading slashes
    shall be treated as a single slash.”*

PurePath.anchor[¶](#pathlib.PurePath.anchor "Link to this definition")
:   The concatenation of the drive and root:

    ```
    >>> PureWindowsPath('c:/Program Files/').anchor
    'c:\\'
    >>> PureWindowsPath('c:Program Files/').anchor
    'c:'
    >>> PurePosixPath('/etc').anchor
    '/'
    >>> PureWindowsPath('//host/share').anchor
    '\\\\host\\share\\'
    ```

PurePath.parents[¶](#pathlib.PurePath.parents "Link to this definition")
:   An immutable sequence providing access to the logical ancestors of
    the path:

    ```
    >>> p = PureWindowsPath('c:/foo/bar/setup.py')
    >>> p.parents[0]
    PureWindowsPath('c:/foo/bar')
    >>> p.parents[1]
    PureWindowsPath('c:/foo')
    >>> p.parents[2]
    PureWindowsPath('c:/')
    ```

    Changed in version 3.10: The parents sequence now supports [slices](../glossary.html#term-slice) and negative index values.

PurePath.parent[¶](#pathlib.PurePath.parent "Link to this definition")
:   The logical parent of the path:

    ```
    >>> p = PurePosixPath('/a/b/c/d')
    >>> p.parent
    PurePosixPath('/a/b/c')
    ```

    You cannot go past an anchor, or empty path:

    ```
    >>> p = PurePosixPath('/')
    >>> p.parent
    PurePosixPath('/')
    >>> p = PurePosixPath('.')
    >>> p.parent
    PurePosixPath('.')
    ```

    Note

    This is a purely lexical operation, hence the following behaviour:

    ```
    >>> p = PurePosixPath('foo/..')
    >>> p.parent
    PurePosixPath('foo')
    ```

    If you want to walk an arbitrary filesystem path upwards, it is
    recommended to first call [`Path.resolve()`](#pathlib.Path.resolve "pathlib.Path.resolve") so as to resolve
    symlinks and eliminate `".."` components.

PurePath.name[¶](#pathlib.PurePath.name "Link to this definition")
:   A string representing the final path component, excluding the drive and
    root, if any:

    ```
    >>> PurePosixPath('my/library/setup.py').name
    'setup.py'
    ```

    UNC drive names are not considered:

    ```
    >>> PureWindowsPath('//some/share/setup.py').name
    'setup.py'
    >>> PureWindowsPath('//some/share').name
    ''
    ```

PurePath.suffix[¶](#pathlib.PurePath.suffix "Link to this definition")
:   The file extension of the final component, if any:

    ```
    >>> PurePosixPath('my/library/setup.py').suffix
    '.py'
    >>> PurePosixPath('my/library.tar.gz').suffix
    '.gz'
    >>> PurePosixPath('my/library').suffix
    ''
    ```

PurePath.suffixes[¶](#pathlib.PurePath.suffixes "Link to this definition")
:   A list of the path’s file extensions:

    ```
    >>> PurePosixPath('my/library.tar.gar').suffixes
    ['.tar', '.gar']
    >>> PurePosixPath('my/library.tar.gz').suffixes
    ['.tar', '.gz']
    >>> PurePosixPath('my/library').suffixes
    []
    ```

PurePath.stem[¶](#pathlib.PurePath.stem "Link to this definition")
:   The final path component, without its suffix:

    ```
    >>> PurePosixPath('my/library.tar.gz').stem
    'library.tar'
    >>> PurePosixPath('my/library.tar').stem
    'library'
    >>> PurePosixPath('my/library').stem
    'library'
    ```

PurePath.as\_posix()[¶](#pathlib.PurePath.as_posix "Link to this definition")
:   Return a string representation of the path with forward slashes (`/`):

    ```
    >>> p = PureWindowsPath('c:\\windows')
    >>> str(p)
    'c:\\windows'
    >>> p.as_posix()
    'c:/windows'
    ```

PurePath.as\_uri()[¶](#pathlib.PurePath.as_uri "Link to this definition")
:   Represent the path as a `file` URI. [`ValueError`](exceptions.html#ValueError "ValueError") is raised if
    the path isn’t absolute.

    ```
    >>> p = PurePosixPath('/etc/passwd')
    >>> p.as_uri()
    'file:///etc/passwd'
    >>> p = PureWindowsPath('c:/Windows')
    >>> p.as_uri()
    'file:///c:/Windows'
    ```

PurePath.is\_absolute()[¶](#pathlib.PurePath.is_absolute "Link to this definition")
:   Return whether the path is absolute or not. A path is considered absolute
    if it has both a root and (if the flavour allows) a drive:

    ```
    >>> PurePosixPath('/a/b').is_absolute()
    True
    >>> PurePosixPath('a/b').is_absolute()
    False

    >>> PureWindowsPath('c:/a/b').is_absolute()
    True
    >>> PureWindowsPath('/a/b').is_absolute()
    False
    >>> PureWindowsPath('c:').is_absolute()
    False
    >>> PureWindowsPath('//some/share').is_absolute()
    True
    ```

PurePath.is\_relative\_to(*other*)[¶](#pathlib.PurePath.is_relative_to "Link to this definition")
:   Return whether or not this path is relative to the *other* path.

    ```
    >>> p = PurePath('/etc/passwd')
    >>> p.is_relative_to('/etc')
    True
    >>> p.is_relative_to('/usr')
    False
    ```

    This method is string-based; it neither accesses the filesystem nor treats
    “`..`” segments specially. The following code is equivalent:

    ```
    >>> u = PurePath('/usr')
    >>> u == p or u in p.parents
    False
    ```

    Added in version 3.9.

    Deprecated since version 3.12, will be removed in version 3.14: Passing additional arguments is deprecated; if supplied, they are joined
    with *other*.

PurePath.is\_reserved()[¶](#pathlib.PurePath.is_reserved "Link to this definition")
:   With [`PureWindowsPath`](#pathlib.PureWindowsPath "pathlib.PureWindowsPath"), return `True` if the path is considered
    reserved under Windows, `False` otherwise. With [`PurePosixPath`](#pathlib.PurePosixPath "pathlib.PurePosixPath"),
    `False` is always returned.

    ```
    >>> PureWindowsPath('nul').is_reserved()
    True
    >>> PurePosixPath('nul').is_reserved()
    False
    ```

    File system calls on reserved paths can fail mysteriously or have
    unintended effects.

PurePath.joinpath(*\*pathsegments*)[¶](#pathlib.PurePath.joinpath "Link to this definition")
:   Calling this method is equivalent to combining the path with each of
    the given *pathsegments* in turn:

    ```
    >>> PurePosixPath('/etc').joinpath('passwd')
    PurePosixPath('/etc/passwd')
    >>> PurePosixPath('/etc').joinpath(PurePosixPath('passwd'))
    PurePosixPath('/etc/passwd')
    >>> PurePosixPath('/etc').joinpath('init.d', 'apache2')
    PurePosixPath('/etc/init.d/apache2')
    >>> PureWindowsPath('c:').joinpath('/Program Files')
    PureWindowsPath('c:/Program Files')
    ```

PurePath.match(*pattern*, *\**, *case\_sensitive=None*)[¶](#pathlib.PurePath.match "Link to this definition")
:   Match this path against the provided glob-style pattern. Return `True`
    if matching is successful, `False` otherwise.

    If *pattern* is relative, the path can be either relative or absolute,
    and matching is done from the right:

    ```
    >>> PurePath('a/b.py').match('*.py')
    True
    >>> PurePath('/a/b/c.py').match('b/*.py')
    True
    >>> PurePath('/a/b/c.py').match('a/*.py')
    False
    ```

    If *pattern* is absolute, the path must be absolute, and the whole path
    must match:

    ```
    >>> PurePath('/a.py').match('/*.py')
    True
    >>> PurePath('a/b.py').match('/*.py')
    False
    ```

    The *pattern* may be another path object; this speeds up matching the same
    pattern against multiple files:

    ```
    >>> pattern = PurePath('*.py')
    >>> PurePath('a/b.py').match(pattern)
    True
    ```

    Note

    The recursive wildcard “`**`” isn’t supported by this method (it acts
    like non-recursive “`*`”.)

    Changed in version 3.12: Accepts an object implementing the [`os.PathLike`](os.html#os.PathLike "os.PathLike") interface.

    As with other methods, case-sensitivity follows platform defaults:

    ```
    >>> PurePosixPath('b.py').match('*.PY')
    False
    >>> PureWindowsPath('b.py').match('*.PY')
    True
    ```

    Set *case\_sensitive* to `True` or `False` to override this behaviour.

    Changed in version 3.12: The *case\_sensitive* parameter was added.

PurePath.relative\_to(*other*, *walk\_up=False*)[¶](#pathlib.PurePath.relative_to "Link to this definition")
:   Compute a version of this path relative to the path represented by
    *other*. If it’s impossible, [`ValueError`](exceptions.html#ValueError "ValueError") is raised:

    ```
    >>> p = PurePosixPath('/etc/passwd')
    >>> p.relative_to('/')
    PurePosixPath('etc/passwd')
    >>> p.relative_to('/etc')
    PurePosixPath('passwd')
    >>> p.relative_to('/usr')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pathlib.py", line 941, in relative_to
        raise ValueError(error_message.format(str(self), str(formatted)))
    ValueError: '/etc/passwd' is not in the subpath of '/usr' OR one path is relative and the other is absolute.
    ```

    When *walk\_up* is false (the default), the path must start with *other*.
    When the argument is true, `..` entries may be added to form the
    relative path. In all other cases, such as the paths referencing
    different drives, [`ValueError`](exceptions.html#ValueError "ValueError") is raised.:

    ```
    >>> p.relative_to('/usr', walk_up=True)
    PurePosixPath('../etc/passwd')
    >>> p.relative_to('foo', walk_up=True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pathlib.py", line 941, in relative_to
        raise ValueError(error_message.format(str(self), str(formatted)))
    ValueError: '/etc/passwd' is not on the same drive as 'foo' OR one path is relative and the other is absolute.
    ```

    Warning

    This function is part of [`PurePath`](#pathlib.PurePath "pathlib.PurePath") and works with strings.
    It does not check or access the underlying file structure.
    This can impact the *walk\_up* option as it assumes that no symlinks
    are present in the path; call [`resolve()`](#pathlib.Path.resolve "pathlib.Path.resolve") first if
    necessary to resolve symlinks.

    Changed in version 3.12: The *walk\_up* parameter was added (old behavior is the same as `walk_up=False`).

    Deprecated since version 3.12, will be removed in version 3.14: Passing additional positional arguments is deprecated; if supplied,
    they are joined with *other*.

PurePath.with\_name(*name*)[¶](#pathlib.PurePath.with_name "Link to this definition")
:   Return a new path with the [`name`](#pathlib.PurePath.name "pathlib.PurePath.name") changed. If the original path
    doesn’t have a name, ValueError is raised:

    ```
    >>> p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
    >>> p.with_name('setup.py')
    PureWindowsPath('c:/Downloads/setup.py')
    >>> p = PureWindowsPath('c:/')
    >>> p.with_name('setup.py')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/antoine/cpython/default/Lib/pathlib.py", line 751, in with_name
        raise ValueError("%r has an empty name" % (self,))
    ValueError: PureWindowsPath('c:/') has an empty name
    ```

PurePath.with\_stem(*stem*)[¶](#pathlib.PurePath.with_stem "Link to this definition")
:   Return a new path with the [`stem`](#pathlib.PurePath.stem "pathlib.PurePath.stem") changed. If the original path
    doesn’t have a name, ValueError is raised:

    ```
    >>> p = PureWindowsPath('c:/Downloads/draft.txt')
    >>> p.with_stem('final')
    PureWindowsPath('c:/Downloads/final.txt')
    >>> p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
    >>> p.with_stem('lib')
    PureWindowsPath('c:/Downloads/lib.gz')
    >>> p = PureWindowsPath('c:/')
    >>> p.with_stem('')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/antoine/cpython/default/Lib/pathlib.py", line 861, in with_stem
        return self.with_name(stem + self.suffix)
      File "/home/antoine/cpython/default/Lib/pathlib.py", line 851, in with_name
        raise ValueError("%r has an empty name" % (self,))
    ValueError: PureWindowsPath('c:/') has an empty name
    ```

    Added in version 3.9.

PurePath.with\_suffix(*suffix*)[¶](#pathlib.PurePath.with_suffix "Link to this definition")
:   Return a new path with the [`suffix`](#pathlib.PurePath.suffix "pathlib.PurePath.suffix") changed. If the original path
    doesn’t have a suffix, the new *suffix* is appended instead. If the
    *suffix* is an empty string, the original suffix is removed:

    ```
    >>> p = PureWindowsPath('c:/Downloads/pathlib.tar.gz')
    >>> p.with_suffix('.bz2')
    PureWindowsPath('c:/Downloads/pathlib.tar.bz2')
    >>> p = PureWindowsPath('README')
    >>> p.with_suffix('.txt')
    PureWindowsPath('README.txt')
    >>> p = PureWindowsPath('README.txt')
    >>> p.with_suffix('')
    PureWindowsPath('README')
    ```

PurePath.with\_segments(*\*pathsegments*)[¶](#pathlib.PurePath.with_segments "Link to this definition")
:   Create a new path object of the same type by combining the given
    *pathsegments*. This method is called whenever a derivative path is created,
    such as from [`parent`](#pathlib.PurePath.parent "pathlib.PurePath.parent") and [`relative_to()`](#pathlib.PurePath.relative_to "pathlib.PurePath.relative_to"). Subclasses may
    override this method to pass information to derivative paths, for example:

    ```
    from pathlib import PurePosixPath

    class MyPath(PurePosixPath):
        def __init__(self, *pathsegments, session_id):
            super().__init__(*pathsegments)
            self.session_id = session_id

        def with_segments(self, *pathsegments):
            return type(self)(*pathsegments, session_id=self.session_id)

    etc = MyPath('/etc', session_id=42)
    hosts = etc / 'hosts'
    print(hosts.session_id)  # 42
    ```

    Added in version 3.12.

## Concrete paths[¶](#concrete-paths "Link to this heading")

Concrete paths are subclasses of the pure path classes. In addition to
operations provided by the latter, they also provide methods to do system
calls on path objects. There are three ways to instantiate concrete paths:

*class* pathlib.Path(*\*pathsegments*)[¶](#pathlib.Path "Link to this definition")
:   A subclass of [`PurePath`](#pathlib.PurePath "pathlib.PurePath"), this class represents concrete paths of
    the system’s path flavour (instantiating it creates either a
    [`PosixPath`](#pathlib.PosixPath "pathlib.PosixPath") or a [`WindowsPath`](#pathlib.WindowsPath "pathlib.WindowsPath")):

    ```
    >>> Path('setup.py')
    PosixPath('setup.py')
    ```

    *pathsegments* is specified similarly to [`PurePath`](#pathlib.PurePath "pathlib.PurePath").

*class* pathlib.PosixPath(*\*pathsegments*)[¶](#pathlib.PosixPath "Link to this definition")
:   A subclass of [`Path`](#pathlib.Path "pathlib.Path") and [`PurePosixPath`](#pathlib.PurePosixPath "pathlib.PurePosixPath"), this class
    represents concrete non-Windows filesystem paths:

    ```
    >>> PosixPath('/etc/hosts')
    PosixPath('/etc/hosts')
    ```

    *pathsegments* is specified similarly to [`PurePath`](#pathlib.PurePath "pathlib.PurePath").

*class* pathlib.WindowsPath(*\*pathsegments*)[¶](#pathlib.WindowsPath "Link to this definition")
:   A subclass of [`Path`](#pathlib.Path "pathlib.Path") and [`PureWindowsPath`](#pathlib.PureWindowsPath "pathlib.PureWindowsPath"), this class
    represents concrete Windows filesystem paths:

    ```
    >>> WindowsPath('c:/', 'Users', 'Ximénez')
    WindowsPath('c:/Users/Ximénez')
    ```

    *pathsegments* is specified similarly to [`PurePath`](#pathlib.PurePath "pathlib.PurePath").

You can only instantiate the class flavour that corresponds to your system
(allowing system calls on non-compatible path flavours could lead to
bugs or failures in your application):

```
>>> import os
>>> os.name
'posix'
>>> Path('setup.py')
PosixPath('setup.py')
>>> PosixPath('setup.py')
PosixPath('setup.py')
>>> WindowsPath('setup.py')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pathlib.py", line 798, in __new__
    % (cls.__name__,))
NotImplementedError: cannot instantiate 'WindowsPath' on your system
```

Some concrete path methods can raise an [`OSError`](exceptions.html#OSError "OSError") if a system call fails
(for example because the path doesn’t exist).

### Expanding and resolving paths[¶](#expanding-and-resolving-paths "Link to this heading")

*classmethod* Path.home()[¶](#pathlib.Path.home "Link to this definition")
:   Return a new path object representing the user’s home directory (as
    returned by [`os.path.expanduser()`](os.path.html#os.path.expanduser "os.path.expanduser") with `~` construct). If the home
    directory can’t be resolved, [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") is raised.

    ```
    >>> Path.home()
    PosixPath('/home/antoine')
    ```

    Added in version 3.5.

Path.expanduser()[¶](#pathlib.Path.expanduser "Link to this definition")
:   Return a new path with expanded `~` and `~user` constructs,
    as returned by [`os.path.expanduser()`](os.path.html#os.path.expanduser "os.path.expanduser"). If a home directory can’t be
    resolved, [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") is raised.

    ```
    >>> p = PosixPath('~/films/Monty Python')
    >>> p.expanduser()
    PosixPath('/home/eric/films/Monty Python')
    ```

    Added in version 3.5.

*classmethod* Path.cwd()[¶](#pathlib.Path.cwd "Link to this definition")
:   Return a new path object representing the current directory (as returned
    by [`os.getcwd()`](os.html#os.getcwd "os.getcwd")):

    ```
    >>> Path.cwd()
    PosixPath('/home/antoine/pathlib')
    ```

Path.absolute()[¶](#pathlib.Path.absolute "Link to this definition")
:   Make the path absolute, without normalization or resolving symlinks.
    Returns a new path object:

    ```
    >>> p = Path('tests')
    >>> p
    PosixPath('tests')
    >>> p.absolute()
    PosixPath('/home/antoine/pathlib/tests')
    ```

Path.resolve(*strict=False*)[¶](#pathlib.Path.resolve "Link to this definition")
:   Make the path absolute, resolving any symlinks. A new path object is
    returned:

    ```
    >>> p = Path()
    >>> p
    PosixPath('.')
    >>> p.resolve()
    PosixPath('/home/antoine/pathlib')
    ```

    “`..`” components are also eliminated (this is the only method to do so):

    ```
    >>> p = Path('docs/../setup.py')
    >>> p.resolve()
    PosixPath('/home/antoine/pathlib/setup.py')
    ```

    If the path doesn’t exist and *strict* is `True`, [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError")
    is raised. If *strict* is `False`, the path is resolved as far as possible
    and any remainder is appended without checking whether it exists. If an
    infinite loop is encountered along the resolution path, [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError")
    is raised.

    Changed in version 3.6: The *strict* parameter was added (pre-3.6 behavior is strict).

Path.readlink()[¶](#pathlib.Path.readlink "Link to this definition")
:   Return the path to which the symbolic link points (as returned by
    [`os.readlink()`](os.html#os.readlink "os.readlink")):

    ```
    >>> p = Path('mylink')
    >>> p.symlink_to('setup.py')
    >>> p.readlink()
    PosixPath('setup.py')
    ```

    Added in version 3.9.

### Querying file type and status[¶](#querying-file-type-and-status "Link to this heading")

Changed in version 3.8: [`exists()`](#pathlib.Path.exists "pathlib.Path.exists"), [`is_dir()`](#pathlib.Path.is_dir "pathlib.Path.is_dir"), [`is_file()`](#pathlib.Path.is_file "pathlib.Path.is_file"),
[`is_mount()`](#pathlib.Path.is_mount "pathlib.Path.is_mount"), [`is_symlink()`](#pathlib.Path.is_symlink "pathlib.Path.is_symlink"),
[`is_block_device()`](#pathlib.Path.is_block_device "pathlib.Path.is_block_device"), [`is_char_device()`](#pathlib.Path.is_char_device "pathlib.Path.is_char_device"),
[`is_fifo()`](#pathlib.Path.is_fifo "pathlib.Path.is_fifo"), [`is_socket()`](#pathlib.Path.is_socket "pathlib.Path.is_socket") now return `False`
instead of raising an exception for paths that contain characters
unrepresentable at the OS level.

Path.stat(*\**, *follow\_symlinks=True*)[¶](#pathlib.Path.stat "Link to this definition")
:   Return an [`os.stat_result`](os.html#os.stat_result "os.stat_result") object containing information about this path, like [`os.stat()`](os.html#os.stat "os.stat").
    The result is looked up at each call to this method.

    This method normally follows symlinks; to stat a symlink add the argument
    `follow_symlinks=False`, or use [`lstat()`](#pathlib.Path.lstat "pathlib.Path.lstat").

    ```
    >>> p = Path('setup.py')
    >>> p.stat().st_size
    956
    >>> p.stat().st_mtime
    1327883547.852554
    ```

    Changed in version 3.10: The *follow\_symlinks* parameter was added.

Path.lstat()[¶](#pathlib.Path.lstat "Link to this definition")
:   Like [`Path.stat()`](#pathlib.Path.stat "pathlib.Path.stat") but, if the path points to a symbolic link, return
    the symbolic link’s information rather than its target’s.

Path.exists(*\**, *follow\_symlinks=True*)[¶](#pathlib.Path.exists "Link to this definition")
:   Return `True` if the path points to an existing file or directory.

    This method normally follows symlinks; to check if a symlink exists, add
    the argument `follow_symlinks=False`.

    ```
    >>> Path('.').exists()
    True
    >>> Path('setup.py').exists()
    True
    >>> Path('/etc').exists()
    True
    >>> Path('nonexistentfile').exists()
    False
    ```

    Changed in version 3.12: The *follow\_symlinks* parameter was added.

Path.is\_file()[¶](#pathlib.Path.is_file "Link to this definition")
:   Return `True` if the path points to a regular file (or a symbolic link
    pointing to a regular file), `False` if it points to another kind of file.

    `False` is also returned if the path doesn’t exist or is a broken symlink;
    other errors (such as permission errors) are propagated.

Path.is\_dir()[¶](#pathlib.Path.is_dir "Link to this definition")
:   Return `True` if the path points to a directory (or a symbolic link
    pointing to a directory), `False` if it points to another kind of file.

    `False` is also returned if the path doesn’t exist or is a broken symlink;
    other errors (such as permission errors) are propagated.

Path.is\_symlink()[¶](#pathlib.Path.is_symlink "Link to this definition")
:   Return `True` if the path points to a symbolic link, `False` otherwise.

    `False` is also returned if the path doesn’t exist; other errors (such
    as permission errors) are propagated.

Path.is\_junction()[¶](#pathlib.Path.is_junction "Link to this definition")
:   Return `True` if the path points to a junction, and `False` for any other
    type of file. Currently only Windows supports junctions.

    Added in version 3.12.

Path.is\_mount()[¶](#pathlib.Path.is_mount "Link to this definition")
:   Return `True` if the path is a *mount point*: a point in a
    file system where a different file system has been mounted. On POSIX, the
    function checks whether *path*’s parent, `path/..`, is on a different
    device than *path*, or whether `path/..` and *path* point to the same
    i-node on the same device — this should detect mount points for all Unix
    and POSIX variants. On Windows, a mount point is considered to be a drive
    letter root (e.g. `c:\`), a UNC share (e.g. `\\server\share`), or a
    mounted filesystem directory.

    Added in version 3.7.

    Changed in version 3.12: Windows support was added.

Path.is\_socket()[¶](#pathlib.Path.is_socket "Link to this definition")
:   Return `True` if the path points to a Unix socket (or a symbolic link
    pointing to a Unix socket), `False` if it points to another kind of file.

    `False` is also returned if the path doesn’t exist or is a broken symlink;
    other errors (such as permission errors) are propagated.

Path.is\_fifo()[¶](#pathlib.Path.is_fifo "Link to this definition")
:   Return `True` if the path points to a FIFO (or a symbolic link
    pointing to a FIFO), `False` if it points to another kind of file.

    `False` is also returned if the path doesn’t exist or is a broken symlink;
    other errors (such as permission errors) are propagated.

Path.is\_block\_device()[¶](#pathlib.Path.is_block_device "Link to this definition")
:   Return `True` if the path points to a block device (or a symbolic link
    pointing to a block device), `False` if it points to another kind of file.

    `False` is also returned if the path doesn’t exist or is a broken symlink;
    other errors (such as permission errors) are propagated.

Path.is\_char\_device()[¶](#pathlib.Path.is_char_device "Link to this definition")
:   Return `True` if the path points to a character device (or a symbolic link
    pointing to a character device), `False` if it points to another kind of file.

    `False` is also returned if the path doesn’t exist or is a broken symlink;
    other errors (such as permission errors) are propagated.

Path.samefile(*other\_path*)[¶](#pathlib.Path.samefile "Link to this definition")
:   Return whether this path points to the same file as *other\_path*, which
    can be either a Path object, or a string. The semantics are similar
    to [`os.path.samefile()`](os.path.html#os.path.samefile "os.path.samefile") and [`os.path.samestat()`](os.path.html#os.path.samestat "os.path.samestat").

    An [`OSError`](exceptions.html#OSError "OSError") can be raised if either file cannot be accessed for some
    reason.

    ```
    >>> p = Path('spam')
    >>> q = Path('eggs')
    >>> p.samefile(q)
    False
    >>> p.samefile('spam')
    True
    ```

    Added in version 3.5.

### Reading and writing files[¶](#reading-and-writing-files "Link to this heading")

Path.open(*mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*)[¶](#pathlib.Path.open "Link to this definition")
:   Open the file pointed to by the path, like the built-in [`open()`](functions.html#open "open")
    function does:

    ```
    >>> p = Path('setup.py')
    >>> with p.open() as f:
    ...     f.readline()
    ...
    '#!/usr/bin/env python3\n'
    ```

Path.read\_text(*encoding=None*, *errors=None*)[¶](#pathlib.Path.read_text "Link to this definition")
:   Return the decoded contents of the pointed-to file as a string:

    ```
    >>> p = Path('my_text_file')
    >>> p.write_text('Text file contents')
    18
    >>> p.read_text()
    'Text file contents'
    ```

    The file is opened and then closed. The optional parameters have the same
    meaning as in [`open()`](functions.html#open "open").

    Added in version 3.5.

Path.read\_bytes()[¶](#pathlib.Path.read_bytes "Link to this definition")
:   Return the binary contents of the pointed-to file as a bytes object:

    ```
    >>> p = Path('my_binary_file')
    >>> p.write_bytes(b'Binary file contents')
    20
    >>> p.read_bytes()
    b'Binary file contents'
    ```

    Added in version 3.5.

Path.write\_text(*data*, *encoding=None*, *errors=None*, *newline=None*)[¶](#pathlib.Path.write_text "Link to this definition")
:   Open the file pointed to in text mode, write *data* to it, and close the
    file:

    ```
    >>> p = Path('my_text_file')
    >>> p.write_text('Text file contents')
    18
    >>> p.read_text()
    'Text file contents'
    ```

    An existing file of the same name is overwritten. The optional parameters
    have the same meaning as in [`open()`](functions.html#open "open").

    Added in version 3.5.

    Changed in version 3.10: The *newline* parameter was added.

Path.write\_bytes(*data*)[¶](#pathlib.Path.write_bytes "Link to this definition")
:   Open the file pointed to in bytes mode, write *data* to it, and close the
    file:

    ```
    >>> p = Path('my_binary_file')
    >>> p.write_bytes(b'Binary file contents')
    20
    >>> p.read_bytes()
    b'Binary file contents'
    ```

    An existing file of the same name is overwritten.

    Added in version 3.5.

### Reading directories[¶](#reading-directories "Link to this heading")

Path.iterdir()[¶](#pathlib.Path.iterdir "Link to this definition")
:   When the path points to a directory, yield path objects of the directory
    contents:

    ```
    >>> p = Path('docs')
    >>> for child in p.iterdir(): child
    ...
    PosixPath('docs/conf.py')
    PosixPath('docs/_templates')
    PosixPath('docs/make.bat')
    PosixPath('docs/index.rst')
    PosixPath('docs/_build')
    PosixPath('docs/_static')
    PosixPath('docs/Makefile')
    ```

    The children are yielded in arbitrary order, and the special entries
    `'.'` and `'..'` are not included. If a file is removed from or added
    to the directory after creating the iterator, it is unspecified whether
    a path object for that file is included.

    If the path is not a directory or otherwise inaccessible, [`OSError`](exceptions.html#OSError "OSError") is
    raised.

Path.glob(*pattern*, *\**, *case\_sensitive=None*)[¶](#pathlib.Path.glob "Link to this definition")
:   Glob the given relative *pattern* in the directory represented by this path,
    yielding all matching files (of any kind):

    ```
    >>> sorted(Path('.').glob('*.py'))
    [PosixPath('pathlib.py'), PosixPath('setup.py'), PosixPath('test_pathlib.py')]
    >>> sorted(Path('.').glob('*/*.py'))
    [PosixPath('docs/conf.py')]
    ```

    Patterns are the same as for [`fnmatch`](fnmatch.html#module-fnmatch "fnmatch: Unix shell style filename pattern matching."), with the addition of “`**`”
    which means “this directory and all subdirectories, recursively”. In other
    words, it enables recursive globbing:

    ```
    >>> sorted(Path('.').glob('**/*.py'))
    [PosixPath('build/lib/pathlib.py'),
     PosixPath('docs/conf.py'),
     PosixPath('pathlib.py'),
     PosixPath('setup.py'),
     PosixPath('test_pathlib.py')]
    ```

    This method calls [`Path.is_dir()`](#pathlib.Path.is_dir "pathlib.Path.is_dir") on the top-level directory and
    propagates any [`OSError`](exceptions.html#OSError "OSError") exception that is raised. Subsequent
    [`OSError`](exceptions.html#OSError "OSError") exceptions from scanning directories are suppressed.

    By default, or when the *case\_sensitive* keyword-only argument is set to
    `None`, this method matches paths using platform-specific casing rules:
    typically, case-sensitive on POSIX, and case-insensitive on Windows.
    Set *case\_sensitive* to `True` or `False` to override this behaviour.

    Note

    Using the “`**`” pattern in large directory trees may consume
    an inordinate amount of time.

    Raises an [auditing event](sys.html#auditing) `pathlib.Path.glob` with arguments `self`, `pattern`.

    Changed in version 3.11: Return only directories if *pattern* ends with a pathname components
    separator ([`sep`](os.html#os.sep "os.sep") or [`altsep`](os.html#os.altsep "os.altsep")).

    Changed in version 3.12: The *case\_sensitive* parameter was added.

Path.rglob(*pattern*, *\**, *case\_sensitive=None*)[¶](#pathlib.Path.rglob "Link to this definition")
:   Glob the given relative *pattern* recursively. This is like calling
    [`Path.glob()`](#pathlib.Path.glob "pathlib.Path.glob") with “`**/`” added in front of the *pattern*, where
    *patterns* are the same as for [`fnmatch`](fnmatch.html#module-fnmatch "fnmatch: Unix shell style filename pattern matching."):

    ```
    >>> sorted(Path().rglob("*.py"))
    [PosixPath('build/lib/pathlib.py'),
     PosixPath('docs/conf.py'),
     PosixPath('pathlib.py'),
     PosixPath('setup.py'),
     PosixPath('test_pathlib.py')]
    ```

    By default, or when the *case\_sensitive* keyword-only argument is set to
    `None`, this method matches paths using platform-specific casing rules:
    typically, case-sensitive on POSIX, and case-insensitive on Windows.
    Set *case\_sensitive* to `True` or `False` to override this behaviour.

    Raises an [auditing event](sys.html#auditing) `pathlib.Path.rglob` with arguments `self`, `pattern`.

    Changed in version 3.11: Return only directories if *pattern* ends with a pathname components
    separator ([`sep`](os.html#os.sep "os.sep") or [`altsep`](os.html#os.altsep "os.altsep")).

    Changed in version 3.12: The *case\_sensitive* parameter was added.

Path.walk(*top\_down=True*, *on\_error=None*, *follow\_symlinks=False*)[¶](#pathlib.Path.walk "Link to this definition")
:   Generate the file names in a directory tree by walking the tree
    either top-down or bottom-up.

    For each directory in the directory tree rooted at *self* (including
    *self* but excluding ‘.’ and ‘..’), the method yields a 3-tuple of
    `(dirpath, dirnames, filenames)`.

    *dirpath* is a [`Path`](#pathlib.Path "pathlib.Path") to the directory currently being walked,
    *dirnames* is a list of strings for the names of subdirectories in *dirpath*
    (excluding `'.'` and `'..'`), and *filenames* is a list of strings for
    the names of the non-directory files in *dirpath*. To get a full path
    (which begins with *self*) to a file or directory in *dirpath*, do
    `dirpath / name`. Whether or not the lists are sorted is file
    system-dependent.

    If the optional argument *top\_down* is true (which is the default), the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are walked top-down). If *top\_down* is false, the triple
    for a directory is generated after the triples for all of its subdirectories
    (directories are walked bottom-up). No matter the value of *top\_down*, the
    list of subdirectories is retrieved before the triples for the directory and
    its subdirectories are walked.

    When *top\_down* is true, the caller can modify the *dirnames* list in-place
    (for example, using [`del`](../reference/simple_stmts.html#del) or slice assignment), and [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk")
    will only recurse into the subdirectories whose names remain in *dirnames*.
    This can be used to prune the search, or to impose a specific order of visiting,
    or even to inform [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") about directories the caller creates or
    renames before it resumes [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") again. Modifying *dirnames* when
    *top\_down* is false has no effect on the behavior of [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") since the
    directories in *dirnames* have already been generated by the time *dirnames*
    is yielded to the caller.

    By default, errors from [`os.scandir()`](os.html#os.scandir "os.scandir") are ignored. If the optional
    argument *on\_error* is specified, it should be a callable; it will be
    called with one argument, an [`OSError`](exceptions.html#OSError "OSError") instance. The callable can handle the
    error to continue the walk or re-raise it to stop the walk. Note that the
    filename is available as the `filename` attribute of the exception object.

    By default, [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") does not follow symbolic links, and instead adds them
    to the *filenames* list. Set *follow\_symlinks* to true to resolve symlinks
    and place them in *dirnames* and *filenames* as appropriate for their targets, and
    consequently visit directories pointed to by symlinks (where supported).

    Note

    Be aware that setting *follow\_symlinks* to true can lead to infinite
    recursion if a link points to a parent directory of itself. [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk")
    does not keep track of the directories it has already visited.

    Note

    [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") assumes the directories it walks are not modified during
    execution. For example, if a directory from *dirnames* has been replaced
    with a symlink and *follow\_symlinks* is false, [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") will
    still try to descend into it. To prevent such behavior, remove directories
    from *dirnames* as appropriate.

    Note

    Unlike [`os.walk()`](os.html#os.walk "os.walk"), [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") lists symlinks to directories in
    *filenames* if *follow\_symlinks* is false.

    This example displays the number of bytes used by all files in each directory,
    while ignoring `__pycache__` directories:

    ```
    from pathlib import Path
    for root, dirs, files in Path("cpython/Lib/concurrent").walk(on_error=print):
      print(
          root,
          "consumes",
          sum((root / file).stat().st_size for file in files),
          "bytes in",
          len(files),
          "non-directory files"
      )
      if '__pycache__' in dirs:
            dirs.remove('__pycache__')
    ```

    This next example is a simple implementation of [`shutil.rmtree()`](shutil.html#shutil.rmtree "shutil.rmtree").
    Walking the tree bottom-up is essential as [`rmdir()`](#pathlib.Path.rmdir "pathlib.Path.rmdir") doesn’t allow
    deleting a directory before it is empty:

    ```
    # Delete everything reachable from the directory "top".
    # CAUTION:  This is dangerous! For example, if top == Path('/'),
    # it could delete all of your files.
    for root, dirs, files in top.walk(top_down=False):
        for name in files:
            (root / name).unlink()
        for name in dirs:
            (root / name).rmdir()
    ```

    Added in version 3.12.

### Creating files and directories[¶](#creating-files-and-directories "Link to this heading")

Path.touch(*mode=0o666*, *exist\_ok=True*)[¶](#pathlib.Path.touch "Link to this definition")
:   Create a file at this given path. If *mode* is given, it is combined
    with the process’s `umask` value to determine the file mode and access
    flags. If the file already exists, the function succeeds when *exist\_ok*
    is true (and its modification time is updated to the current time),
    otherwise [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is raised.

    See also

    The [`open()`](#pathlib.Path.open "pathlib.Path.open"), [`write_text()`](#pathlib.Path.write_text "pathlib.Path.write_text") and
    [`write_bytes()`](#pathlib.Path.write_bytes "pathlib.Path.write_bytes") methods are often used to create files.

Path.mkdir(*mode=0o777*, *parents=False*, *exist\_ok=False*)[¶](#pathlib.Path.mkdir "Link to this definition")
:   Create a new directory at this given path. If *mode* is given, it is
    combined with the process’s `umask` value to determine the file mode
    and access flags. If the path already exists, [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError")
    is raised.

    If *parents* is true, any missing parents of this path are created
    as needed; they are created with the default permissions without taking
    *mode* into account (mimicking the POSIX `mkdir -p` command).

    If *parents* is false (the default), a missing parent raises
    [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError").

    If *exist\_ok* is false (the default), [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is
    raised if the target directory already exists.

    If *exist\_ok* is true, [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") will not be raised unless the given
    path already exists in the file system and is not a directory (same
    behavior as the POSIX `mkdir -p` command).

    Changed in version 3.5: The *exist\_ok* parameter was added.

Path.symlink\_to(*target*, *target\_is\_directory=False*)[¶](#pathlib.Path.symlink_to "Link to this definition")
:   Make this path a symbolic link pointing to *target*.

    On Windows, a symlink represents either a file or a directory, and does not
    morph to the target dynamically. If the target is present, the type of the
    symlink will be created to match. Otherwise, the symlink will be created
    as a directory if *target\_is\_directory* is true or a file symlink (the
    default) otherwise. On non-Windows platforms, *target\_is\_directory* is ignored.

    ```
    >>> p = Path('mylink')
    >>> p.symlink_to('setup.py')
    >>> p.resolve()
    PosixPath('/home/antoine/pathlib/setup.py')
    >>> p.stat().st_size
    956
    >>> p.lstat().st_size
    8
    ```

    Note

    The order of arguments (link, target) is the reverse
    of [`os.symlink()`](os.html#os.symlink "os.symlink")’s.

Path.hardlink\_to(*target*)[¶](#pathlib.Path.hardlink_to "Link to this definition")
:   Make this path a hard link to the same file as *target*.

    Note

    The order of arguments (link, target) is the reverse
    of [`os.link()`](os.html#os.link "os.link")’s.

    Added in version 3.10.

### Renaming and deleting[¶](#renaming-and-deleting "Link to this heading")

Path.rename(*target*)[¶](#pathlib.Path.rename "Link to this definition")
:   Rename this file or directory to the given *target*, and return a new
    `Path` instance pointing to *target*. On Unix, if *target* exists
    and is a file, it will be replaced silently if the user has permission.
    On Windows, if *target* exists, [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") will be raised.
    *target* can be either a string or another path object:

    ```
    >>> p = Path('foo')
    >>> p.open('w').write('some text')
    9
    >>> target = Path('bar')
    >>> p.rename(target)
    PosixPath('bar')
    >>> target.open().read()
    'some text'
    ```

    The target path may be absolute or relative. Relative paths are interpreted
    relative to the current working directory, *not* the directory of the
    `Path` object.

    It is implemented in terms of [`os.rename()`](os.html#os.rename "os.rename") and gives the same guarantees.

    Changed in version 3.8: Added return value, return the new `Path` instance.

Path.replace(*target*)[¶](#pathlib.Path.replace "Link to this definition")
:   Rename this file or directory to the given *target*, and return a new
    `Path` instance pointing to *target*. If *target* points to an
    existing file or empty directory, it will be unconditionally replaced.

    The target path may be absolute or relative. Relative paths are interpreted
    relative to the current working directory, *not* the directory of the
    `Path` object.

    Changed in version 3.8: Added return value, return the new `Path` instance.

Path.unlink(*missing\_ok=False*)[¶](#pathlib.Path.unlink "Link to this definition")
:   Remove this file or symbolic link. If the path points to a directory,
    use [`Path.rmdir()`](#pathlib.Path.rmdir "pathlib.Path.rmdir") instead.

    If *missing\_ok* is false (the default), [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") is
    raised if the path does not exist.

    If *missing\_ok* is true, [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") exceptions will be
    ignored (same behavior as the POSIX `rm -f` command).

    Changed in version 3.8: The *missing\_ok* parameter was added.

Path.rmdir()[¶](#pathlib.Path.rmdir "Link to this definition")
:   Remove this directory. The directory must be empty.

### Permissions and ownership[¶](#permissions-and-ownership "Link to this heading")

Path.owner()[¶](#pathlib.Path.owner "Link to this definition")
:   Return the name of the user owning the file. [`KeyError`](exceptions.html#KeyError "KeyError") is raised
    if the file’s user identifier (UID) isn’t found in the system database.

Path.group()[¶](#pathlib.Path.group "Link to this definition")
:   Return the name of the group owning the file. [`KeyError`](exceptions.html#KeyError "KeyError") is raised
    if the file’s group identifier (GID) isn’t found in the system database.

Path.chmod(*mode*, *\**, *follow\_symlinks=True*)[¶](#pathlib.Path.chmod "Link to this definition")
:   Change the file mode and permissions, like [`os.chmod()`](os.html#os.chmod "os.chmod").

    This method normally follows symlinks. Some Unix flavours support changing
    permissions on the symlink itself; on these platforms you may add the
    argument `follow_symlinks=False`, or use [`lchmod()`](#pathlib.Path.lchmod "pathlib.Path.lchmod").

    ```
    >>> p = Path('setup.py')
    >>> p.stat().st_mode
    33277
    >>> p.chmod(0o444)
    >>> p.stat().st_mode
    33060
    ```

    Changed in version 3.10: The *follow\_symlinks* parameter was added.

Path.lchmod(*mode*)[¶](#pathlib.Path.lchmod "Link to this definition")
:   Like [`Path.chmod()`](#pathlib.Path.chmod "pathlib.Path.chmod") but, if the path points to a symbolic link, the
    symbolic link’s mode is changed rather than its target’s.

## Correspondence to tools in the [`os`](os.html#module-os "os: Miscellaneous operating system interfaces.") module[¶](#correspondence-to-tools-in-the-os-module "Link to this heading")

Below is a table mapping various [`os`](os.html#module-os "os: Miscellaneous operating system interfaces.") functions to their corresponding
[`PurePath`](#pathlib.PurePath "pathlib.PurePath")/[`Path`](#pathlib.Path "pathlib.Path") equivalent.

| [`os`](os.html#module-os "os: Miscellaneous operating system interfaces.") and [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.") | [`pathlib`](#module-pathlib "pathlib: Object-oriented filesystem paths") |
| --- | --- |
| [`os.path.dirname()`](os.path.html#os.path.dirname "os.path.dirname") | [`PurePath.parent`](#pathlib.PurePath.parent "pathlib.PurePath.parent") |
| [`os.path.basename()`](os.path.html#os.path.basename "os.path.basename") | [`PurePath.name`](#pathlib.PurePath.name "pathlib.PurePath.name") |
| [`os.path.splitext()`](os.path.html#os.path.splitext "os.path.splitext") | [`PurePath.stem`](#pathlib.PurePath.stem "pathlib.PurePath.stem"), [`PurePath.suffix`](#pathlib.PurePath.suffix "pathlib.PurePath.suffix") |
| [`os.path.join()`](os.path.html#os.path.join "os.path.join") | [`PurePath.joinpath()`](#pathlib.PurePath.joinpath "pathlib.PurePath.joinpath") |
| [`os.path.isabs()`](os.path.html#os.path.isabs "os.path.isabs") | [`PurePath.is_absolute()`](#pathlib.PurePath.is_absolute "pathlib.PurePath.is_absolute") |
| [`os.path.relpath()`](os.path.html#os.path.relpath "os.path.relpath") | [`PurePath.relative_to()`](#pathlib.PurePath.relative_to "pathlib.PurePath.relative_to") [[1]](#id7) |
| [`os.path.expanduser()`](os.path.html#os.path.expanduser "os.path.expanduser") | [`Path.expanduser()`](#pathlib.Path.expanduser "pathlib.Path.expanduser") [[2]](#id8) |
| [`os.path.realpath()`](os.path.html#os.path.realpath "os.path.realpath") | [`Path.resolve()`](#pathlib.Path.resolve "pathlib.Path.resolve") |
| [`os.path.abspath()`](os.path.html#os.path.abspath "os.path.abspath") | [`Path.absolute()`](#pathlib.Path.absolute "pathlib.Path.absolute") [[3]](#id9) |
| [`os.path.exists()`](os.path.html#os.path.exists "os.path.exists") | [`Path.exists()`](#pathlib.Path.exists "pathlib.Path.exists") |
| [`os.path.isfile()`](os.path.html#os.path.isfile "os.path.isfile") | [`Path.is_file()`](#pathlib.Path.is_file "pathlib.Path.is_file") |
| [`os.path.isdir()`](os.path.html#os.path.isdir "os.path.isdir") | [`Path.is_dir()`](#pathlib.Path.is_dir "pathlib.Path.is_dir") |
| [`os.path.islink()`](os.path.html#os.path.islink "os.path.islink") | [`Path.is_symlink()`](#pathlib.Path.is_symlink "pathlib.Path.is_symlink") |
| [`os.path.isjunction()`](os.path.html#os.path.isjunction "os.path.isjunction") | [`Path.is_junction()`](#pathlib.Path.is_junction "pathlib.Path.is_junction") |
| [`os.path.ismount()`](os.path.html#os.path.ismount "os.path.ismount") | [`Path.is_mount()`](#pathlib.Path.is_mount "pathlib.Path.is_mount") |
| [`os.path.samefile()`](os.path.html#os.path.samefile "os.path.samefile") | [`Path.samefile()`](#pathlib.Path.samefile "pathlib.Path.samefile") |
| [`os.getcwd()`](os.html#os.getcwd "os.getcwd") | [`Path.cwd()`](#pathlib.Path.cwd "pathlib.Path.cwd") |
| [`os.stat()`](os.html#os.stat "os.stat") | [`Path.stat()`](#pathlib.Path.stat "pathlib.Path.stat") |
| [`os.lstat()`](os.html#os.lstat "os.lstat") | [`Path.lstat()`](#pathlib.Path.lstat "pathlib.Path.lstat") |
| [`os.listdir()`](os.html#os.listdir "os.listdir") | [`Path.iterdir()`](#pathlib.Path.iterdir "pathlib.Path.iterdir") |
| [`os.walk()`](os.html#os.walk "os.walk") | [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") [[4]](#id10) |
| [`os.mkdir()`](os.html#os.mkdir "os.mkdir"), [`os.makedirs()`](os.html#os.makedirs "os.makedirs") | [`Path.mkdir()`](#pathlib.Path.mkdir "pathlib.Path.mkdir") |
| [`os.link()`](os.html#os.link "os.link") | [`Path.hardlink_to()`](#pathlib.Path.hardlink_to "pathlib.Path.hardlink_to") |
| [`os.symlink()`](os.html#os.symlink "os.symlink") | [`Path.symlink_to()`](#pathlib.Path.symlink_to "pathlib.Path.symlink_to") |
| [`os.readlink()`](os.html#os.readlink "os.readlink") | [`Path.readlink()`](#pathlib.Path.readlink "pathlib.Path.readlink") |
| [`os.rename()`](os.html#os.rename "os.rename") | [`Path.rename()`](#pathlib.Path.rename "pathlib.Path.rename") |
| [`os.replace()`](os.html#os.replace "os.replace") | [`Path.replace()`](#pathlib.Path.replace "pathlib.Path.replace") |
| [`os.remove()`](os.html#os.remove "os.remove"), [`os.unlink()`](os.html#os.unlink "os.unlink") | [`Path.unlink()`](#pathlib.Path.unlink "pathlib.Path.unlink") |
| [`os.rmdir()`](os.html#os.rmdir "os.rmdir") | [`Path.rmdir()`](#pathlib.Path.rmdir "pathlib.Path.rmdir") |
| [`os.chmod()`](os.html#os.chmod "os.chmod") | [`Path.chmod()`](#pathlib.Path.chmod "pathlib.Path.chmod") |
| [`os.lchmod()`](os.html#os.lchmod "os.lchmod") | [`Path.lchmod()`](#pathlib.Path.lchmod "pathlib.Path.lchmod") |

Footnotes

[[1](#id3)]

[`os.path.relpath()`](os.path.html#os.path.relpath "os.path.relpath") calls [`abspath()`](os.path.html#os.path.abspath "os.path.abspath") to make paths
absolute and remove “`..`” parts, whereas [`PurePath.relative_to()`](#pathlib.PurePath.relative_to "pathlib.PurePath.relative_to")
is a lexical operation that raises [`ValueError`](exceptions.html#ValueError "ValueError") when its inputs’
anchors differ (e.g. if one path is absolute and the other relative.)

[[2](#id4)]

[`os.path.expanduser()`](os.path.html#os.path.expanduser "os.path.expanduser") returns the path unchanged if the home
directory can’t be resolved, whereas [`Path.expanduser()`](#pathlib.Path.expanduser "pathlib.Path.expanduser") raises
[`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

[[3](#id5)]

[`os.path.abspath()`](os.path.html#os.path.abspath "os.path.abspath") removes “`..`” components without resolving
symlinks, which may change the meaning of the path, whereas
[`Path.absolute()`](#pathlib.Path.absolute "pathlib.Path.absolute") leaves any “`..`” components in the path.

[[4](#id6)]

[`os.walk()`](os.html#os.walk "os.walk") always follows symlinks when categorizing paths into
*dirnames* and *filenames*, whereas [`Path.walk()`](#pathlib.Path.walk "pathlib.Path.walk") categorizes all
symlinks into *filenames* when *follow\_symlinks* is false (the default.)

### [Table of Contents](../contents.html)

* [`pathlib` — Object-oriented filesystem paths](#)
  + [Basic use](#basic-use)
  + [Pure paths](#pure-paths)
    - [General properties](#general-properties)
    - [Operators](#operators)
    - [Accessing individual parts](#accessing-individual-parts)
    - [Methods and properties](#methods-and-properties)
  + [Concrete paths](#concrete-paths)
    - [Expanding and resolving paths](#expanding-and-resolving-paths)
    - [Querying file type and status](#querying-file-type-and-status)
    - [Reading and writing files](#reading-and-writing-files)
    - [Reading directories](#reading-directories)
    - [Creating files and directories](#creating-files-and-directories)
    - [Renaming and deleting](#renaming-and-deleting)
    - [Permissions and ownership](#permissions-and-ownership)
  + [Correspondence to tools in the `os` module](#correspondence-to-tools-in-the-os-module)

#### Previous topic

[File and Directory Access](filesys.html "previous chapter")

#### Next topic

[`os.path` — Common pathname manipulations](os.path.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/pathlib.rst)

«

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](os.path.html "os.path — Common pathname manipulations") |
* [previous](filesys.html "File and Directory Access") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [File and Directory Access](filesys.html) »
* `pathlib` — Object-oriented filesystem paths
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