os — Miscellaneous operating system interfaces — Python 3.12.13 documentation

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

* [`os` — Miscellaneous operating system interfaces](#)
  + [File Names, Command Line Arguments, and Environment Variables](#file-names-command-line-arguments-and-environment-variables)
  + [Python UTF-8 Mode](#python-utf-8-mode)
  + [Process Parameters](#process-parameters)
  + [File Object Creation](#file-object-creation)
  + [File Descriptor Operations](#file-descriptor-operations)
    - [Querying the size of a terminal](#querying-the-size-of-a-terminal)
    - [Inheritance of File Descriptors](#inheritance-of-file-descriptors)
  + [Files and Directories](#files-and-directories)
    - [Linux extended attributes](#linux-extended-attributes)
  + [Process Management](#process-management)
  + [Interface to the scheduler](#interface-to-the-scheduler)
  + [Miscellaneous System Information](#miscellaneous-system-information)
  + [Random numbers](#random-numbers)

#### Previous topic

[Generic Operating System Services](allos.html "previous chapter")

#### Next topic

[`io` — Core tools for working with streams](io.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/os.rst)

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](io.html "io — Core tools for working with streams") |
* [previous](allos.html "Generic Operating System Services") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Generic Operating System Services](allos.html) »
* `os` — Miscellaneous operating system interfaces
* |
* Theme
  Auto
  Light
  Dark
   |

# `os` — Miscellaneous operating system interfaces[¶](#module-os "Link to this heading")

**Source code:** [Lib/os.py](https://github.com/python/cpython/tree/3.12/Lib/os.py)

---

This module provides a portable way of using operating system dependent
functionality. If you just want to read or write a file see [`open()`](functions.html#open "open"), if
you want to manipulate paths, see the [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.") module, and if you want to
read all the lines in all the files on the command line see the [`fileinput`](fileinput.html#module-fileinput "fileinput: Loop over standard input or a list of files.")
module. For creating temporary files and directories see the [`tempfile`](tempfile.html#module-tempfile "tempfile: Generate temporary files and directories.")
module, and for high-level file and directory handling see the [`shutil`](shutil.html#module-shutil "shutil: High-level file operations, including copying.")
module.

Notes on the availability of these functions:

* The design of all built-in operating system dependent modules of Python is
  such that as long as the same functionality is available, it uses the same
  interface; for example, the function `os.stat(path)` returns stat
  information about *path* in the same format (which happens to have originated
  with the POSIX interface).
* Extensions peculiar to a particular operating system are also available
  through the [`os`](#module-os "os: Miscellaneous operating system interfaces.") module, but using them is of course a threat to
  portability.
* All functions accepting path or file names accept both bytes and string
  objects, and result in an object of the same type, if a path or file name is
  returned.
* On VxWorks, os.popen, os.fork, os.execv and os.spawn\*p\* are not supported.
* On WebAssembly platforms `wasm32-emscripten` and `wasm32-wasi`, large
  parts of the [`os`](#module-os "os: Miscellaneous operating system interfaces.") module are not available or behave differently. API
  related to processes (e.g. [`fork()`](#os.fork "os.fork"), [`execve()`](#os.execve "os.execve")), signals
  (e.g. [`kill()`](#os.kill "os.kill"), [`wait()`](#os.wait "os.wait")), and resources
  (e.g. [`nice()`](#os.nice "os.nice")) are not available. Others like [`getuid()`](#os.getuid "os.getuid")
  and [`getpid()`](#os.getpid "os.getpid") are emulated or stubs.

Note

All functions in this module raise [`OSError`](exceptions.html#OSError "OSError") (or subclasses thereof) in
the case of invalid or inaccessible file names and paths, or other arguments
that have the correct type, but are not accepted by the operating system.

*exception* os.error[¶](#os.error "Link to this definition")
:   An alias for the built-in [`OSError`](exceptions.html#OSError "OSError") exception.

os.name[¶](#os.name "Link to this definition")
:   The name of the operating system dependent module imported. The following
    names have currently been registered: `'posix'`, `'nt'`,
    `'java'`.

    See also

    [`sys.platform`](sys.html#sys.platform "sys.platform") has a finer granularity. [`os.uname()`](#os.uname "os.uname") gives
    system-dependent version information.

    The [`platform`](platform.html#module-platform "platform: Retrieves as much platform identifying data as possible.") module provides detailed checks for the
    system’s identity.

## File Names, Command Line Arguments, and Environment Variables[¶](#file-names-command-line-arguments-and-environment-variables "Link to this heading")

In Python, file names, command line arguments, and environment variables are
represented using the string type. On some systems, decoding these strings to
and from bytes is necessary before passing them to the operating system. Python
uses the [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler) to perform this
conversion (see [`sys.getfilesystemencoding()`](sys.html#sys.getfilesystemencoding "sys.getfilesystemencoding")).

The [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler) are configured at Python
startup by the [`PyConfig_Read()`](../c-api/init_config.html#c.PyConfig_Read "PyConfig_Read") function: see
[`filesystem_encoding`](../c-api/init_config.html#c.PyConfig.filesystem_encoding "PyConfig.filesystem_encoding") and
[`filesystem_errors`](../c-api/init_config.html#c.PyConfig.filesystem_errors "PyConfig.filesystem_errors") members of [`PyConfig`](../c-api/init_config.html#c.PyConfig "PyConfig").

Changed in version 3.1: On some systems, conversion using the file system encoding may fail. In this
case, Python uses the [surrogateescape encoding error handler](codecs.html#surrogateescape), which means that undecodable bytes are replaced by a
Unicode character U+DC*xx* on decoding, and these are again
translated to the original byte on encoding.

The [file system encoding](../glossary.html#term-filesystem-encoding-and-error-handler) must
guarantee to successfully decode all bytes below 128. If the file system
encoding fails to provide this guarantee, API functions can raise
[`UnicodeError`](exceptions.html#UnicodeError "UnicodeError").

See also the [locale encoding](../glossary.html#term-locale-encoding).

## Python UTF-8 Mode[¶](#python-utf-8-mode "Link to this heading")

Added in version 3.7: See [**PEP 540**](https://peps.python.org/pep-0540/) for more details.

The Python UTF-8 Mode ignores the [locale encoding](../glossary.html#term-locale-encoding) and forces the usage
of the UTF-8 encoding:

* Use UTF-8 as the [filesystem encoding](../glossary.html#term-filesystem-encoding-and-error-handler).
* [`sys.getfilesystemencoding()`](sys.html#sys.getfilesystemencoding "sys.getfilesystemencoding") returns `'utf-8'`.
* [`locale.getpreferredencoding()`](locale.html#locale.getpreferredencoding "locale.getpreferredencoding") returns `'utf-8'` (the *do\_setlocale*
  argument has no effect).
* [`sys.stdin`](sys.html#sys.stdin "sys.stdin"), [`sys.stdout`](sys.html#sys.stdout "sys.stdout"), and [`sys.stderr`](sys.html#sys.stderr "sys.stderr") all use
  UTF-8 as their text encoding, with the `surrogateescape`
  [error handler](codecs.html#error-handlers) being enabled for [`sys.stdin`](sys.html#sys.stdin "sys.stdin")
  and [`sys.stdout`](sys.html#sys.stdout "sys.stdout") ([`sys.stderr`](sys.html#sys.stderr "sys.stderr") continues to use
  `backslashreplace` as it does in the default locale-aware mode)
* On Unix, [`os.device_encoding()`](#os.device_encoding "os.device_encoding") returns `'utf-8'` rather than the
  device encoding.

Note that the standard stream settings in UTF-8 mode can be overridden by
[`PYTHONIOENCODING`](../using/cmdline.html#envvar-PYTHONIOENCODING) (just as they can be in the default locale-aware
mode).

As a consequence of the changes in those lower level APIs, other higher
level APIs also exhibit different default behaviours:

* Command line arguments, environment variables and filenames are decoded
  to text using the UTF-8 encoding.
* [`os.fsdecode()`](#os.fsdecode "os.fsdecode") and [`os.fsencode()`](#os.fsencode "os.fsencode") use the UTF-8 encoding.
* [`open()`](functions.html#open "open"), [`io.open()`](io.html#io.open "io.open"), and [`codecs.open()`](codecs.html#codecs.open "codecs.open") use the UTF-8
  encoding by default. However, they still use the strict error handler by
  default so that attempting to open a binary file in text mode is likely
  to raise an exception rather than producing nonsense data.

The [Python UTF-8 Mode](#utf8-mode) is enabled if the LC\_CTYPE locale is
`C` or `POSIX` at Python startup (see the [`PyConfig_Read()`](../c-api/init_config.html#c.PyConfig_Read "PyConfig_Read")
function).

It can be enabled or disabled using the [`-X utf8`](../using/cmdline.html#cmdoption-X) command line
option and the [`PYTHONUTF8`](../using/cmdline.html#envvar-PYTHONUTF8) environment variable.

If the [`PYTHONUTF8`](../using/cmdline.html#envvar-PYTHONUTF8) environment variable is not set at all, then the
interpreter defaults to using the current locale settings, *unless* the current
locale is identified as a legacy ASCII-based locale (as described for
[`PYTHONCOERCECLOCALE`](../using/cmdline.html#envvar-PYTHONCOERCECLOCALE)), and locale coercion is either disabled or
fails. In such legacy locales, the interpreter will default to enabling UTF-8
mode unless explicitly instructed not to do so.

The Python UTF-8 Mode can only be enabled at the Python startup. Its value
can be read from [`sys.flags.utf8_mode`](sys.html#sys.flags "sys.flags").

See also the [UTF-8 mode on Windows](../using/windows.html#win-utf8-mode)
and the [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler).

See also

[**PEP 686**](https://peps.python.org/pep-0686/)
:   Python 3.15 will make [Python UTF-8 Mode](#utf8-mode) default.

## Process Parameters[¶](#process-parameters "Link to this heading")

These functions and data items provide information and operate on the current
process and user.

os.ctermid()[¶](#os.ctermid "Link to this definition")
:   Return the filename corresponding to the controlling terminal of the process.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.environ[¶](#os.environ "Link to this definition")
:   A [mapping](../glossary.html#term-mapping) object where keys and values are strings that represent
    the process environment. For example, `environ['HOME']` is the pathname
    of your home directory (on some platforms), and is equivalent to
    `getenv("HOME")` in C.

    This mapping is captured the first time the [`os`](#module-os "os: Miscellaneous operating system interfaces.") module is imported,
    typically during Python startup as part of processing `site.py`. Changes
    to the environment made after this time are not reflected in [`os.environ`](#os.environ "os.environ"),
    except for changes made by modifying [`os.environ`](#os.environ "os.environ") directly.

    This mapping may be used to modify the environment as well as query the
    environment. [`putenv()`](#os.putenv "os.putenv") will be called automatically when the mapping
    is modified.

    On Unix, keys and values use [`sys.getfilesystemencoding()`](sys.html#sys.getfilesystemencoding "sys.getfilesystemencoding") and
    `'surrogateescape'` error handler. Use [`environb`](#os.environb "os.environb") if you would like
    to use a different encoding.

    On Windows, the keys are converted to uppercase. This also applies when
    getting, setting, or deleting an item. For example,
    `environ['monty'] = 'python'` maps the key `'MONTY'` to the value
    `'python'`.

    Note

    Calling [`putenv()`](#os.putenv "os.putenv") directly does not change [`os.environ`](#os.environ "os.environ"), so it’s better
    to modify [`os.environ`](#os.environ "os.environ").

    Note

    On some platforms, including FreeBSD and macOS, setting `environ` may
    cause memory leaks. Refer to the system documentation for
    `putenv()`.

    You can delete items in this mapping to unset environment variables.
    [`unsetenv()`](#os.unsetenv "os.unsetenv") will be called automatically when an item is deleted from
    [`os.environ`](#os.environ "os.environ"), and when one of the `pop()` or `clear()` methods is
    called.

    Changed in version 3.9: Updated to support [**PEP 584**](https://peps.python.org/pep-0584/)’s merge (`|`) and update (`|=`) operators.

os.environb[¶](#os.environb "Link to this definition")
:   Bytes version of [`environ`](#os.environ "os.environ"): a [mapping](../glossary.html#term-mapping) object where both keys
    and values are [`bytes`](stdtypes.html#bytes "bytes") objects representing the process environment.
    [`environ`](#os.environ "os.environ") and [`environb`](#os.environb "os.environb") are synchronized (modifying
    [`environb`](#os.environb "os.environb") updates [`environ`](#os.environ "os.environ"), and vice versa).

    [`environb`](#os.environb "os.environb") is only available if [`supports_bytes_environ`](#os.supports_bytes_environ "os.supports_bytes_environ") is
    `True`.

    Added in version 3.2.

    Changed in version 3.9: Updated to support [**PEP 584**](https://peps.python.org/pep-0584/)’s merge (`|`) and update (`|=`) operators.

os.chdir(*path*)

os.fchdir(*fd*)

os.getcwd()
:   These functions are described in [Files and Directories](#os-file-dir).

os.fsencode(*filename*)[¶](#os.fsencode "Link to this definition")
:   Encode [path-like](../glossary.html#term-path-like-object) *filename* to the
    [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler); return [`bytes`](stdtypes.html#bytes "bytes")
    unchanged.

    [`fsdecode()`](#os.fsdecode "os.fsdecode") is the reverse function.

    Added in version 3.2.

    Changed in version 3.6: Support added to accept objects implementing the [`os.PathLike`](#os.PathLike "os.PathLike")
    interface.

os.fsdecode(*filename*)[¶](#os.fsdecode "Link to this definition")
:   Decode the [path-like](../glossary.html#term-path-like-object) *filename* from the
    [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler); return [`str`](stdtypes.html#str "str")
    unchanged.

    [`fsencode()`](#os.fsencode "os.fsencode") is the reverse function.

    Added in version 3.2.

    Changed in version 3.6: Support added to accept objects implementing the [`os.PathLike`](#os.PathLike "os.PathLike")
    interface.

os.fspath(*path*)[¶](#os.fspath "Link to this definition")
:   Return the file system representation of the path.

    If [`str`](stdtypes.html#str "str") or [`bytes`](stdtypes.html#bytes "bytes") is passed in, it is returned unchanged.
    Otherwise [`__fspath__()`](#os.PathLike.__fspath__ "os.PathLike.__fspath__") is called and its value is
    returned as long as it is a [`str`](stdtypes.html#str "str") or [`bytes`](stdtypes.html#bytes "bytes") object.
    In all other cases, [`TypeError`](exceptions.html#TypeError "TypeError") is raised.

    Added in version 3.6.

*class* os.PathLike[¶](#os.PathLike "Link to this definition")
:   An [abstract base class](../glossary.html#term-abstract-base-class) for objects representing a file system path,
    e.g. [`pathlib.PurePath`](pathlib.html#pathlib.PurePath "pathlib.PurePath").

    Added in version 3.6.

    *abstractmethod* \_\_fspath\_\_()[¶](#os.PathLike.__fspath__ "Link to this definition")
    :   Return the file system path representation of the object.

        The method should only return a [`str`](stdtypes.html#str "str") or [`bytes`](stdtypes.html#bytes "bytes") object,
        with the preference being for [`str`](stdtypes.html#str "str").

os.getenv(*key*, *default=None*)[¶](#os.getenv "Link to this definition")
:   Return the value of the environment variable *key* as a string if it exists, or
    *default* if it doesn’t. *key* is a string. Note that
    since [`getenv()`](#os.getenv "os.getenv") uses [`os.environ`](#os.environ "os.environ"), the mapping of [`getenv()`](#os.getenv "os.getenv") is
    similarly also captured on import, and the function may not reflect
    future environment changes.

    On Unix, keys and values are decoded with [`sys.getfilesystemencoding()`](sys.html#sys.getfilesystemencoding "sys.getfilesystemencoding")
    and `'surrogateescape'` error handler. Use [`os.getenvb()`](#os.getenvb "os.getenvb") if you
    would like to use a different encoding.

    [Availability](intro.html#availability): Unix, Windows.

os.getenvb(*key*, *default=None*)[¶](#os.getenvb "Link to this definition")
:   Return the value of the environment variable *key* as bytes if it exists, or
    *default* if it doesn’t. *key* must be bytes. Note that
    since [`getenvb()`](#os.getenvb "os.getenvb") uses [`os.environb`](#os.environb "os.environb"), the mapping of [`getenvb()`](#os.getenvb "os.getenvb") is
    similarly also captured on import, and the function may not reflect
    future environment changes.

    [`getenvb()`](#os.getenvb "os.getenvb") is only available if [`supports_bytes_environ`](#os.supports_bytes_environ "os.supports_bytes_environ")
    is `True`.

    [Availability](intro.html#availability): Unix.

    Added in version 3.2.

os.get\_exec\_path(*env=None*)[¶](#os.get_exec_path "Link to this definition")
:   Returns the list of directories that will be searched for a named
    executable, similar to a shell, when launching a process.
    *env*, when specified, should be an environment variable dictionary
    to lookup the PATH in.
    By default, when *env* is `None`, [`environ`](#os.environ "os.environ") is used.

    Added in version 3.2.

os.getegid()[¶](#os.getegid "Link to this definition")
:   Return the effective group id of the current process. This corresponds to the
    “set id” bit on the file being executed in the current process.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.geteuid()[¶](#os.geteuid "Link to this definition")
:   Return the current process’s effective user id.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.getgid()[¶](#os.getgid "Link to this definition")
:   Return the real group id of the current process.

    [Availability](intro.html#availability): Unix.

    The function is a stub on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

os.getgrouplist(*user*, *group*, */*)[¶](#os.getgrouplist "Link to this definition")
:   Return list of group ids that *user* belongs to. If *group* is not in the
    list, it is included; typically, *group* is specified as the group ID
    field from the password record for *user*, because that group ID will
    otherwise be potentially omitted.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.getgroups()[¶](#os.getgroups "Link to this definition")
:   Return list of supplemental group ids associated with the current process.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Note

    On macOS, [`getgroups()`](#os.getgroups "os.getgroups") behavior differs somewhat from
    other Unix platforms. If the Python interpreter was built with a
    deployment target of `10.5` or earlier, [`getgroups()`](#os.getgroups "os.getgroups") returns
    the list of effective group ids associated with the current user process;
    this list is limited to a system-defined number of entries, typically 16,
    and may be modified by calls to [`setgroups()`](#os.setgroups "os.setgroups") if suitably privileged.
    If built with a deployment target greater than `10.5`,
    [`getgroups()`](#os.getgroups "os.getgroups") returns the current group access list for the user
    associated with the effective user id of the process; the group access
    list may change over the lifetime of the process, it is not affected by
    calls to [`setgroups()`](#os.setgroups "os.setgroups"), and its length is not limited to 16. The
    deployment target value, `MACOSX_DEPLOYMENT_TARGET`, can be
    obtained with [`sysconfig.get_config_var()`](sysconfig.html#sysconfig.get_config_var "sysconfig.get_config_var").

os.getlogin()[¶](#os.getlogin "Link to this definition")
:   Return the name of the user logged in on the controlling terminal of the
    process. For most purposes, it is more useful to use
    [`getpass.getuser()`](getpass.html#getpass.getuser "getpass.getuser") since the latter checks the environment variables
    `LOGNAME` or `USERNAME` to find out who the user is, and
    falls back to `pwd.getpwuid(os.getuid())[0]` to get the login name of the
    current real user id.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

os.getpgid(*pid*)[¶](#os.getpgid "Link to this definition")
:   Return the process group id of the process with process id *pid*. If *pid* is 0,
    the process group id of the current process is returned.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.getpgrp()[¶](#os.getpgrp "Link to this definition")
:   Return the id of the current process group.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.getpid()[¶](#os.getpid "Link to this definition")
:   Return the current process id.

    The function is a stub on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

os.getppid()[¶](#os.getppid "Link to this definition")
:   Return the parent’s process id. When the parent process has exited, on Unix
    the id returned is the one of the init process (1), on Windows it is still
    the same id, which may be already reused by another process.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

    Changed in version 3.2: Added support for Windows.

os.getpriority(*which*, *who*)[¶](#os.getpriority "Link to this definition")
:   Get program scheduling priority. The value *which* is one of
    [`PRIO_PROCESS`](#os.PRIO_PROCESS "os.PRIO_PROCESS"), [`PRIO_PGRP`](#os.PRIO_PGRP "os.PRIO_PGRP"), or [`PRIO_USER`](#os.PRIO_USER "os.PRIO_USER"), and *who*
    is interpreted relative to *which* (a process identifier for
    [`PRIO_PROCESS`](#os.PRIO_PROCESS "os.PRIO_PROCESS"), process group identifier for [`PRIO_PGRP`](#os.PRIO_PGRP "os.PRIO_PGRP"), and a
    user ID for [`PRIO_USER`](#os.PRIO_USER "os.PRIO_USER")). A zero value for *who* denotes
    (respectively) the calling process, the process group of the calling process,
    or the real user ID of the calling process.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.PRIO\_PROCESS[¶](#os.PRIO_PROCESS "Link to this definition")

os.PRIO\_PGRP[¶](#os.PRIO_PGRP "Link to this definition")

os.PRIO\_USER[¶](#os.PRIO_USER "Link to this definition")
:   Parameters for the [`getpriority()`](#os.getpriority "os.getpriority") and [`setpriority()`](#os.setpriority "os.setpriority") functions.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.PRIO\_DARWIN\_THREAD[¶](#os.PRIO_DARWIN_THREAD "Link to this definition")

os.PRIO\_DARWIN\_PROCESS[¶](#os.PRIO_DARWIN_PROCESS "Link to this definition")

os.PRIO\_DARWIN\_BG[¶](#os.PRIO_DARWIN_BG "Link to this definition")

os.PRIO\_DARWIN\_NONUI[¶](#os.PRIO_DARWIN_NONUI "Link to this definition")
:   Parameters for the [`getpriority()`](#os.getpriority "os.getpriority") and [`setpriority()`](#os.setpriority "os.setpriority") functions.

    [Availability](intro.html#availability): macOS

    Added in version 3.12.

os.getresuid()[¶](#os.getresuid "Link to this definition")
:   Return a tuple (ruid, euid, suid) denoting the current process’s
    real, effective, and saved user ids.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.2.

os.getresgid()[¶](#os.getresgid "Link to this definition")
:   Return a tuple (rgid, egid, sgid) denoting the current process’s
    real, effective, and saved group ids.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.2.

os.getuid()[¶](#os.getuid "Link to this definition")
:   Return the current process’s real user id.

    [Availability](intro.html#availability): Unix.

    The function is a stub on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

os.initgroups(*username*, *gid*, */*)[¶](#os.initgroups "Link to this definition")
:   Call the system initgroups() to initialize the group access list with all of
    the groups of which the specified username is a member, plus the specified
    group id.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.2.

os.putenv(*key*, *value*, */*)[¶](#os.putenv "Link to this definition")
:   Set the environment variable named *key* to the string *value*. Such
    changes to the environment affect subprocesses started with [`os.system()`](#os.system "os.system"),
    [`popen()`](#os.popen "os.popen") or [`fork()`](#os.fork "os.fork") and [`execv()`](#os.execv "os.execv").

    Assignments to items in [`os.environ`](#os.environ "os.environ") are automatically translated into
    corresponding calls to [`putenv()`](#os.putenv "os.putenv"); however, calls to [`putenv()`](#os.putenv "os.putenv")
    don’t update [`os.environ`](#os.environ "os.environ"), so it is actually preferable to assign to items
    of [`os.environ`](#os.environ "os.environ"). This also applies to [`getenv()`](#os.getenv "os.getenv") and [`getenvb()`](#os.getenvb "os.getenvb"), which
    respectively use [`os.environ`](#os.environ "os.environ") and [`os.environb`](#os.environb "os.environb") in their implementations.

    Note

    On some platforms, including FreeBSD and macOS, setting `environ` may
    cause memory leaks. Refer to the system documentation for `putenv()`.

    Raises an [auditing event](sys.html#auditing) `os.putenv` with arguments `key`, `value`.

    Changed in version 3.9: The function is now always available.

os.setegid(*egid*, */*)[¶](#os.setegid "Link to this definition")
:   Set the current process’s effective group id.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.seteuid(*euid*, */*)[¶](#os.seteuid "Link to this definition")
:   Set the current process’s effective user id.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setgid(*gid*, */*)[¶](#os.setgid "Link to this definition")
:   Set the current process’ group id.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setgroups(*groups*, */*)[¶](#os.setgroups "Link to this definition")
:   Set the list of supplemental group ids associated with the current process to
    *groups*. *groups* must be a sequence, and each element must be an integer
    identifying a group. This operation is typically available only to the superuser.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Note

    On macOS, the length of *groups* may not exceed the
    system-defined maximum number of effective group ids, typically 16.
    See the documentation for [`getgroups()`](#os.getgroups "os.getgroups") for cases where it may not
    return the same group list set by calling setgroups().

os.setns(*fd*, *nstype=0*)[¶](#os.setns "Link to this definition")
:   Reassociate the current thread with a Linux namespace.
    See the *[setns(2)](https://manpages.debian.org/setns(2))* and *[namespaces(7)](https://manpages.debian.org/namespaces(7))* man pages for more
    details.

    If *fd* refers to a `/proc/pid/ns/` link, `setns()` reassociates the
    calling thread with the namespace associated with that link,
    and *nstype* may be set to one of the
    [CLONE\_NEW\* constants](#os-unshare-clone-flags)
    to impose constraints on the operation
    (`0` means no constraints).

    Since Linux 5.8, *fd* may refer to a PID file descriptor obtained from
    [`pidfd_open()`](#os.pidfd_open "os.pidfd_open"). In this case, `setns()` reassociates the calling thread
    into one or more of the same namespaces as the thread referred to by *fd*.
    This is subject to any constraints imposed by *nstype*,
    which is a bit mask combining one or more of the
    [CLONE\_NEW\* constants](#os-unshare-clone-flags),
    e.g. `setns(fd, os.CLONE_NEWUTS | os.CLONE_NEWPID)`.
    The caller’s memberships in unspecified namespaces are left unchanged.

    *fd* can be any object with a [`fileno()`](io.html#io.IOBase.fileno "io.IOBase.fileno") method, or a raw file descriptor.

    This example reassociates the thread with the `init` process’s network namespace:

    ```
    fd = os.open("/proc/1/ns/net", os.O_RDONLY)
    os.setns(fd, os.CLONE_NEWNET)
    os.close(fd)
    ```

    [Availability](intro.html#availability): Linux >= 3.0 with glibc >= 2.14.

    Added in version 3.12.

    See also

    The [`unshare()`](#os.unshare "os.unshare") function.

os.setpgrp()[¶](#os.setpgrp "Link to this definition")
:   Call the system call `setpgrp()` or `setpgrp(0, 0)` depending on
    which version is implemented (if any). See the Unix manual for the semantics.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setpgid(*pid*, *pgrp*, */*)[¶](#os.setpgid "Link to this definition")
:   Call the system call `setpgid()` to set the process group id of the
    process with id *pid* to the process group with id *pgrp*. See the Unix manual
    for the semantics.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setpriority(*which*, *who*, *priority*)[¶](#os.setpriority "Link to this definition")
:   Set program scheduling priority. The value *which* is one of
    [`PRIO_PROCESS`](#os.PRIO_PROCESS "os.PRIO_PROCESS"), [`PRIO_PGRP`](#os.PRIO_PGRP "os.PRIO_PGRP"), or [`PRIO_USER`](#os.PRIO_USER "os.PRIO_USER"), and *who*
    is interpreted relative to *which* (a process identifier for
    [`PRIO_PROCESS`](#os.PRIO_PROCESS "os.PRIO_PROCESS"), process group identifier for [`PRIO_PGRP`](#os.PRIO_PGRP "os.PRIO_PGRP"), and a
    user ID for [`PRIO_USER`](#os.PRIO_USER "os.PRIO_USER")). A zero value for *who* denotes
    (respectively) the calling process, the process group of the calling process,
    or the real user ID of the calling process.
    *priority* is a value in the range -20 to 19. The default priority is 0;
    lower priorities cause more favorable scheduling.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.setregid(*rgid*, *egid*, */*)[¶](#os.setregid "Link to this definition")
:   Set the current process’s real and effective group ids.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setresgid(*rgid*, *egid*, *sgid*, */*)[¶](#os.setresgid "Link to this definition")
:   Set the current process’s real, effective, and saved group ids.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.2.

os.setresuid(*ruid*, *euid*, *suid*, */*)[¶](#os.setresuid "Link to this definition")
:   Set the current process’s real, effective, and saved user ids.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.2.

os.setreuid(*ruid*, *euid*, */*)[¶](#os.setreuid "Link to this definition")
:   Set the current process’s real and effective user ids.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.getsid(*pid*, */*)[¶](#os.getsid "Link to this definition")
:   Call the system call `getsid()`. See the Unix manual for the semantics.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setsid()[¶](#os.setsid "Link to this definition")
:   Call the system call `setsid()`. See the Unix manual for the semantics.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.setuid(*uid*, */*)[¶](#os.setuid "Link to this definition")
:   Set the current process’s user id.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.strerror(*code*, */*)[¶](#os.strerror "Link to this definition")
:   Return the error message corresponding to the error code in *code*.
    On platforms where `strerror()` returns `NULL` when given an unknown
    error number, [`ValueError`](exceptions.html#ValueError "ValueError") is raised.

os.supports\_bytes\_environ[¶](#os.supports_bytes_environ "Link to this definition")
:   `True` if the native OS type of the environment is bytes (eg. `False` on
    Windows).

    Added in version 3.2.

os.umask(*mask*, */*)[¶](#os.umask "Link to this definition")
:   Set the current numeric umask and return the previous umask.

    The function is a stub on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

os.uname()[¶](#os.uname "Link to this definition")
:   Returns information identifying the current operating system.
    The return value is an object with five attributes:

    * `sysname` - operating system name
    * `nodename` - name of machine on network (implementation-defined)
    * `release` - operating system release
    * `version` - operating system version
    * `machine` - hardware identifier

    For backwards compatibility, this object is also iterable, behaving
    like a five-tuple containing `sysname`, `nodename`,
    `release`, `version`, and `machine`
    in that order.

    Some systems truncate `nodename` to 8 characters or to the
    leading component; a better way to get the hostname is
    [`socket.gethostname()`](socket.html#socket.gethostname "socket.gethostname") or even
    `socket.gethostbyaddr(socket.gethostname())`.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.3: Return type changed from a tuple to a tuple-like object
    with named attributes.

os.unsetenv(*key*, */*)[¶](#os.unsetenv "Link to this definition")
:   Unset (delete) the environment variable named *key*. Such changes to the
    environment affect subprocesses started with [`os.system()`](#os.system "os.system"), [`popen()`](#os.popen "os.popen") or
    [`fork()`](#os.fork "os.fork") and [`execv()`](#os.execv "os.execv").

    Deletion of items in [`os.environ`](#os.environ "os.environ") is automatically translated into a
    corresponding call to [`unsetenv()`](#os.unsetenv "os.unsetenv"); however, calls to [`unsetenv()`](#os.unsetenv "os.unsetenv")
    don’t update [`os.environ`](#os.environ "os.environ"), so it is actually preferable to delete items of
    [`os.environ`](#os.environ "os.environ").

    Raises an [auditing event](sys.html#auditing) `os.unsetenv` with argument `key`.

    Changed in version 3.9: The function is now always available and is also available on Windows.

os.unshare(*flags*)[¶](#os.unshare "Link to this definition")
:   Disassociate parts of the process execution context, and move them into a
    newly created namespace.
    See the *[unshare(2)](https://manpages.debian.org/unshare(2))*
    man page for more details.
    The *flags* argument is a bit mask, combining zero or more of the
    [CLONE\_\* constants](#os-unshare-clone-flags),
    that specifies which parts of the execution context should be
    unshared from their existing associations and moved to a new namespace.
    If the *flags* argument is `0`, no changes are made to the calling process’s
    execution context.

    [Availability](intro.html#availability): Linux >= 2.6.16.

    Added in version 3.12.

    See also

    The [`setns()`](#os.setns "os.setns") function.

Flags to the [`unshare()`](#os.unshare "os.unshare") function, if the implementation supports them.
See *[unshare(2)](https://manpages.debian.org/unshare(2))* in the Linux manual
for their exact effect and availability.

os.CLONE\_FILES[¶](#os.CLONE_FILES "Link to this definition")

os.CLONE\_FS[¶](#os.CLONE_FS "Link to this definition")

os.CLONE\_NEWCGROUP[¶](#os.CLONE_NEWCGROUP "Link to this definition")

os.CLONE\_NEWIPC[¶](#os.CLONE_NEWIPC "Link to this definition")

os.CLONE\_NEWNET[¶](#os.CLONE_NEWNET "Link to this definition")

os.CLONE\_NEWNS[¶](#os.CLONE_NEWNS "Link to this definition")

os.CLONE\_NEWPID[¶](#os.CLONE_NEWPID "Link to this definition")

os.CLONE\_NEWTIME[¶](#os.CLONE_NEWTIME "Link to this definition")

os.CLONE\_NEWUSER[¶](#os.CLONE_NEWUSER "Link to this definition")

os.CLONE\_NEWUTS[¶](#os.CLONE_NEWUTS "Link to this definition")

os.CLONE\_SIGHAND[¶](#os.CLONE_SIGHAND "Link to this definition")

os.CLONE\_SYSVSEM[¶](#os.CLONE_SYSVSEM "Link to this definition")

os.CLONE\_THREAD[¶](#os.CLONE_THREAD "Link to this definition")

os.CLONE\_VM[¶](#os.CLONE_VM "Link to this definition")

## File Object Creation[¶](#file-object-creation "Link to this heading")

These functions create new [file objects](../glossary.html#term-file-object). (See also
[`open()`](#os.open "os.open") for opening file descriptors.)

os.fdopen(*fd*, *\*args*, *\*\*kwargs*)[¶](#os.fdopen "Link to this definition")
:   Return an open file object connected to the file descriptor *fd*. This is an
    alias of the [`open()`](functions.html#open "open") built-in function and accepts the same arguments.
    The only difference is that the first argument of [`fdopen()`](#os.fdopen "os.fdopen") must always
    be an integer.

## File Descriptor Operations[¶](#file-descriptor-operations "Link to this heading")

These functions operate on I/O streams referenced using file descriptors.

File descriptors are small integers corresponding to a file that has been opened
by the current process. For example, standard input is usually file descriptor
0, standard output is 1, and standard error is 2. Further files opened by a
process will then be assigned 3, 4, 5, and so forth. The name “file descriptor”
is slightly deceptive; on Unix platforms, sockets and pipes are also referenced
by file descriptors.

The [`fileno()`](io.html#io.IOBase.fileno "io.IOBase.fileno") method can be used to obtain the file descriptor
associated with a [file object](../glossary.html#term-file-object) when required. Note that using the file
descriptor directly will bypass the file object methods, ignoring aspects such
as internal buffering of data.

os.close(*fd*)[¶](#os.close "Link to this definition")
:   Close file descriptor *fd*.

    Note

    This function is intended for low-level I/O and must be applied to a file
    descriptor as returned by [`os.open()`](#os.open "os.open") or [`pipe()`](#os.pipe "os.pipe"). To close a “file
    object” returned by the built-in function [`open()`](functions.html#open "open") or by [`popen()`](#os.popen "os.popen") or
    [`fdopen()`](#os.fdopen "os.fdopen"), use its [`close()`](io.html#io.IOBase.close "io.IOBase.close") method.

os.closerange(*fd\_low*, *fd\_high*, */*)[¶](#os.closerange "Link to this definition")
:   Close all file descriptors from *fd\_low* (inclusive) to *fd\_high* (exclusive),
    ignoring errors. Equivalent to (but much faster than):

    ```
    for fd in range(fd_low, fd_high):
        try:
            os.close(fd)
        except OSError:
            pass
    ```

os.copy\_file\_range(*src*, *dst*, *count*, *offset\_src=None*, *offset\_dst=None*)[¶](#os.copy_file_range "Link to this definition")
:   Copy *count* bytes from file descriptor *src*, starting from offset
    *offset\_src*, to file descriptor *dst*, starting from offset *offset\_dst*.
    If *offset\_src* is `None`, then *src* is read from the current position;
    respectively for *offset\_dst*.

    In Linux kernel older than 5.3, the files pointed to by *src* and *dst*
    must reside in the same filesystem, otherwise an [`OSError`](exceptions.html#OSError "OSError") is
    raised with [`errno`](exceptions.html#OSError.errno "OSError.errno") set to [`errno.EXDEV`](errno.html#errno.EXDEV "errno.EXDEV").

    This copy is done without the additional cost of transferring data
    from the kernel to user space and then back into the kernel. Additionally,
    some filesystems could implement extra optimizations, such as the use of
    reflinks (i.e., two or more inodes that share pointers to the same
    copy-on-write disk blocks; supported file systems include btrfs and XFS)
    and server-side copy (in the case of NFS).

    The function copies bytes between two file descriptors. Text options, like
    the encoding and the line ending, are ignored.

    The return value is the amount of bytes copied. This could be less than the
    amount requested.

    Note

    On Linux, [`os.copy_file_range()`](#os.copy_file_range "os.copy_file_range") should not be used for copying a
    range of a pseudo file from a special filesystem like procfs and sysfs.
    It will always copy no bytes and return 0 as if the file was empty
    because of a known Linux kernel issue.

    [Availability](intro.html#availability): Linux >= 4.5 with glibc >= 2.27.

    Added in version 3.8.

os.device\_encoding(*fd*)[¶](#os.device_encoding "Link to this definition")
:   Return a string describing the encoding of the device associated with *fd*
    if it is connected to a terminal; else return [`None`](constants.html#None "None").

    On Unix, if the [Python UTF-8 Mode](#utf8-mode) is enabled, return
    `'UTF-8'` rather than the device encoding.

    Changed in version 3.10: On Unix, the function now implements the Python UTF-8 Mode.

os.dup(*fd*, */*)[¶](#os.dup "Link to this definition")
:   Return a duplicate of file descriptor *fd*. The new file descriptor is
    [non-inheritable](#fd-inheritance).

    On Windows, when duplicating a standard stream (0: stdin, 1: stdout,
    2: stderr), the new file descriptor is [inheritable](#fd-inheritance).

    [Availability](intro.html#availability): not WASI.

    Changed in version 3.4: The new file descriptor is now non-inheritable.

os.dup2(*fd*, *fd2*, *inheritable=True*)[¶](#os.dup2 "Link to this definition")
:   Duplicate file descriptor *fd* to *fd2*, closing the latter first if
    necessary. Return *fd2*. The new file descriptor is [inheritable](#fd-inheritance) by default or non-inheritable if *inheritable*
    is `False`.

    [Availability](intro.html#availability): not WASI.

    Changed in version 3.4: Add the optional *inheritable* parameter.

    Changed in version 3.7: Return *fd2* on success. Previously, `None` was always returned.

os.fchmod(*fd*, *mode*)[¶](#os.fchmod "Link to this definition")
:   Change the mode of the file given by *fd* to the numeric *mode*. See the
    docs for [`chmod()`](#os.chmod "os.chmod") for possible values of *mode*. As of Python 3.3, this
    is equivalent to `os.chmod(fd, mode)`.

    Raises an [auditing event](sys.html#auditing) `os.chmod` with arguments `path`, `mode`, `dir_fd`.

    [Availability](intro.html#availability): Unix.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

os.fchown(*fd*, *uid*, *gid*)[¶](#os.fchown "Link to this definition")
:   Change the owner and group id of the file given by *fd* to the numeric *uid*
    and *gid*. To leave one of the ids unchanged, set it to -1. See
    [`chown()`](#os.chown "os.chown"). As of Python 3.3, this is equivalent to `os.chown(fd, uid,
    gid)`.

    Raises an [auditing event](sys.html#auditing) `os.chown` with arguments `path`, `uid`, `gid`, `dir_fd`.

    [Availability](intro.html#availability): Unix.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

os.fdatasync(*fd*)[¶](#os.fdatasync "Link to this definition")
:   Force write of file with filedescriptor *fd* to disk. Does not force update of
    metadata.

    [Availability](intro.html#availability): Unix.

    Note

    This function is not available on MacOS.

os.fpathconf(*fd*, *name*, */*)[¶](#os.fpathconf "Link to this definition")
:   Return system configuration information relevant to an open file. *name*
    specifies the configuration value to retrieve; it may be a string which is the
    name of a defined system value; these names are specified in a number of
    standards (POSIX.1, Unix 95, Unix 98, and others). Some platforms define
    additional names as well. The names known to the host operating system are
    given in the `pathconf_names` dictionary. For configuration variables not
    included in that mapping, passing an integer for *name* is also accepted.

    If *name* is a string and is not known, [`ValueError`](exceptions.html#ValueError "ValueError") is raised. If a
    specific value for *name* is not supported by the host system, even if it is
    included in `pathconf_names`, an [`OSError`](exceptions.html#OSError "OSError") is raised with
    [`errno.EINVAL`](errno.html#errno.EINVAL "errno.EINVAL") for the error number.

    As of Python 3.3, this is equivalent to `os.pathconf(fd, name)`.

    [Availability](intro.html#availability): Unix.

os.fstat(*fd*)[¶](#os.fstat "Link to this definition")
:   Get the status of the file descriptor *fd*. Return a [`stat_result`](#os.stat_result "os.stat_result")
    object.

    As of Python 3.3, this is equivalent to `os.stat(fd)`.

    See also

    The [`stat()`](#os.stat "os.stat") function.

os.fstatvfs(*fd*, */*)[¶](#os.fstatvfs "Link to this definition")
:   Return information about the filesystem containing the file associated with
    file descriptor *fd*, like [`statvfs()`](#os.statvfs "os.statvfs"). As of Python 3.3, this is
    equivalent to `os.statvfs(fd)`.

    [Availability](intro.html#availability): Unix.

os.fsync(*fd*)[¶](#os.fsync "Link to this definition")
:   Force write of file with filedescriptor *fd* to disk. On Unix, this calls the
    native `fsync()` function; on Windows, the MS `_commit()` function.

    If you’re starting with a buffered Python [file object](../glossary.html#term-file-object) *f*, first do
    `f.flush()`, and then do `os.fsync(f.fileno())`, to ensure that all internal
    buffers associated with *f* are written to disk.

    [Availability](intro.html#availability): Unix, Windows.

os.ftruncate(*fd*, *length*, */*)[¶](#os.ftruncate "Link to this definition")
:   Truncate the file corresponding to file descriptor *fd*, so that it is at
    most *length* bytes in size. As of Python 3.3, this is equivalent to
    `os.truncate(fd, length)`.

    Raises an [auditing event](sys.html#auditing) `os.truncate` with arguments `fd`, `length`.

    [Availability](intro.html#availability): Unix, Windows.

    Changed in version 3.5: Added support for Windows

os.get\_blocking(*fd*, */*)[¶](#os.get_blocking "Link to this definition")
:   Get the blocking mode of the file descriptor: `False` if the
    [`O_NONBLOCK`](#os.O_NONBLOCK "os.O_NONBLOCK") flag is set, `True` if the flag is cleared.

    See also [`set_blocking()`](#os.set_blocking "os.set_blocking") and [`socket.socket.setblocking()`](socket.html#socket.socket.setblocking "socket.socket.setblocking").

    [Availability](intro.html#availability): Unix, Windows.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

    On Windows, this function is limited to pipes.

    Added in version 3.5.

    Changed in version 3.12: Added support for pipes on Windows.

os.isatty(*fd*, */*)[¶](#os.isatty "Link to this definition")
:   Return `True` if the file descriptor *fd* is open and connected to a
    tty(-like) device, else `False`.

os.lockf(*fd*, *cmd*, *len*, */*)[¶](#os.lockf "Link to this definition")
:   Apply, test or remove a POSIX lock on an open file descriptor.
    *fd* is an open file descriptor.
    *cmd* specifies the command to use - one of [`F_LOCK`](#os.F_LOCK "os.F_LOCK"), [`F_TLOCK`](#os.F_TLOCK "os.F_TLOCK"),
    [`F_ULOCK`](#os.F_ULOCK "os.F_ULOCK") or [`F_TEST`](#os.F_TEST "os.F_TEST").
    *len* specifies the section of the file to lock.

    Raises an [auditing event](sys.html#auditing) `os.lockf` with arguments `fd`, `cmd`, `len`.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.F\_LOCK[¶](#os.F_LOCK "Link to this definition")

os.F\_TLOCK[¶](#os.F_TLOCK "Link to this definition")

os.F\_ULOCK[¶](#os.F_ULOCK "Link to this definition")

os.F\_TEST[¶](#os.F_TEST "Link to this definition")
:   Flags that specify what action [`lockf()`](#os.lockf "os.lockf") will take.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.login\_tty(*fd*, */*)[¶](#os.login_tty "Link to this definition")
:   Prepare the tty of which fd is a file descriptor for a new login session.
    Make the calling process a session leader; make the tty the controlling tty,
    the stdin, the stdout, and the stderr of the calling process; close fd.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.11.

os.lseek(*fd*, *pos*, *whence*, */*)[¶](#os.lseek "Link to this definition")
:   Set the current position of file descriptor *fd* to position *pos*, modified
    by *whence*, and return the new position in bytes relative to
    the start of the file.
    Valid values for *whence* are:

    * [`SEEK_SET`](#os.SEEK_SET "os.SEEK_SET") or `0` – set *pos* relative to the beginning of the file
    * [`SEEK_CUR`](#os.SEEK_CUR "os.SEEK_CUR") or `1` – set *pos* relative to the current file position
    * [`SEEK_END`](#os.SEEK_END "os.SEEK_END") or `2` – set *pos* relative to the end of the file
    * [`SEEK_HOLE`](#os.SEEK_HOLE "os.SEEK_HOLE") – set *pos* to the next data location, relative to *pos*
    * [`SEEK_DATA`](#os.SEEK_DATA "os.SEEK_DATA") – set *pos* to the next data hole, relative to *pos*

    Changed in version 3.3: Add support for `SEEK_HOLE` and `SEEK_DATA`.

os.SEEK\_SET[¶](#os.SEEK_SET "Link to this definition")

os.SEEK\_CUR[¶](#os.SEEK_CUR "Link to this definition")

os.SEEK\_END[¶](#os.SEEK_END "Link to this definition")
:   Parameters to the [`lseek()`](#os.lseek "os.lseek") function and the [`seek()`](io.html#io.IOBase.seek "io.IOBase.seek")
    method on [file-like objects](../glossary.html#term-file-object),
    for whence to adjust the file position indicator.

    [`SEEK_SET`](#os.SEEK_SET "os.SEEK_SET")
    :   Adjust the file position relative to the beginning of the file.

    [`SEEK_CUR`](#os.SEEK_CUR "os.SEEK_CUR")
    :   Adjust the file position relative to the current file position.

    [`SEEK_END`](#os.SEEK_END "os.SEEK_END")
    :   Adjust the file position relative to the end of the file.

    Their values are 0, 1, and 2, respectively.

os.SEEK\_HOLE[¶](#os.SEEK_HOLE "Link to this definition")

os.SEEK\_DATA[¶](#os.SEEK_DATA "Link to this definition")
:   Parameters to the [`lseek()`](#os.lseek "os.lseek") function and the [`seek()`](io.html#io.IOBase.seek "io.IOBase.seek")
    method on [file-like objects](../glossary.html#term-file-object),
    for seeking file data and holes on sparsely allocated files.

    `SEEK_DATA`
    :   Adjust the file offset to the next location containing data,
        relative to the seek position.

    `SEEK_HOLE`
    :   Adjust the file offset to the next location containing a hole,
        relative to the seek position.
        A hole is defined as a sequence of zeros.

    Note

    These operations only make sense for filesystems that support them.

    [Availability](intro.html#availability): Linux >= 3.1, macOS, Unix

    Added in version 3.3.

os.open(*path*, *flags*, *mode=0o777*, *\**, *dir\_fd=None*)[¶](#os.open "Link to this definition")
:   Open the file *path* and set various flags according to *flags* and possibly
    its mode according to *mode*. When computing *mode*, the current umask value
    is first masked out. Return the file descriptor for the newly opened file.
    The new file descriptor is [non-inheritable](#fd-inheritance).

    For a description of the flag and mode values, see the C run-time documentation;
    flag constants (like [`O_RDONLY`](#os.O_RDONLY "os.O_RDONLY") and [`O_WRONLY`](#os.O_WRONLY "os.O_WRONLY")) are defined in
    the [`os`](#module-os "os: Miscellaneous operating system interfaces.") module. In particular, on Windows adding
    [`O_BINARY`](#os.O_BINARY "os.O_BINARY") is needed to open files in binary mode.

    This function can support [paths relative to directory descriptors](#dir-fd) with the *dir\_fd* parameter.

    Raises an [auditing event](sys.html#auditing) `open` with arguments `path`, `mode`, `flags`.

    Changed in version 3.4: The new file descriptor is now non-inheritable.

    Note

    This function is intended for low-level I/O. For normal usage, use the
    built-in function [`open()`](functions.html#open "open"), which returns a [file object](../glossary.html#term-file-object) with
    `read()` and `write()` methods (and many more). To
    wrap a file descriptor in a file object, use [`fdopen()`](#os.fdopen "os.fdopen").

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.5: If the system call is interrupted and the signal handler does not raise an
    exception, the function now retries the system call instead of raising an
    [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError") exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for the rationale).

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

The following constants are options for the *flags* parameter to the
[`open()`](#os.open "os.open") function. They can be combined using the bitwise OR operator
`|`. Some of them are not available on all platforms. For descriptions of
their availability and use, consult the *[open(2)](https://manpages.debian.org/open(2))* manual page on Unix
or [the MSDN](https://msdn.microsoft.com/en-us/library/z0kc8e3z.aspx) on Windows.

os.O\_RDONLY[¶](#os.O_RDONLY "Link to this definition")

os.O\_WRONLY[¶](#os.O_WRONLY "Link to this definition")

os.O\_RDWR[¶](#os.O_RDWR "Link to this definition")

os.O\_APPEND[¶](#os.O_APPEND "Link to this definition")

os.O\_CREAT[¶](#os.O_CREAT "Link to this definition")

os.O\_EXCL[¶](#os.O_EXCL "Link to this definition")

os.O\_TRUNC[¶](#os.O_TRUNC "Link to this definition")
:   The above constants are available on Unix and Windows.

os.O\_DSYNC[¶](#os.O_DSYNC "Link to this definition")

os.O\_RSYNC[¶](#os.O_RSYNC "Link to this definition")

os.O\_SYNC[¶](#os.O_SYNC "Link to this definition")

os.O\_NDELAY[¶](#os.O_NDELAY "Link to this definition")

os.O\_NONBLOCK[¶](#os.O_NONBLOCK "Link to this definition")

os.O\_NOCTTY[¶](#os.O_NOCTTY "Link to this definition")

os.O\_CLOEXEC[¶](#os.O_CLOEXEC "Link to this definition")
:   The above constants are only available on Unix.

    Changed in version 3.3: Add [`O_CLOEXEC`](#os.O_CLOEXEC "os.O_CLOEXEC") constant.

os.O\_BINARY[¶](#os.O_BINARY "Link to this definition")

os.O\_NOINHERIT[¶](#os.O_NOINHERIT "Link to this definition")

os.O\_SHORT\_LIVED[¶](#os.O_SHORT_LIVED "Link to this definition")

os.O\_TEMPORARY[¶](#os.O_TEMPORARY "Link to this definition")

os.O\_RANDOM[¶](#os.O_RANDOM "Link to this definition")

os.O\_SEQUENTIAL[¶](#os.O_SEQUENTIAL "Link to this definition")

os.O\_TEXT[¶](#os.O_TEXT "Link to this definition")
:   The above constants are only available on Windows.

os.O\_EVTONLY[¶](#os.O_EVTONLY "Link to this definition")

os.O\_FSYNC[¶](#os.O_FSYNC "Link to this definition")

os.O\_SYMLINK[¶](#os.O_SYMLINK "Link to this definition")

os.O\_NOFOLLOW\_ANY[¶](#os.O_NOFOLLOW_ANY "Link to this definition")
:   The above constants are only available on macOS.

    Changed in version 3.10: Add [`O_EVTONLY`](#os.O_EVTONLY "os.O_EVTONLY"), [`O_FSYNC`](#os.O_FSYNC "os.O_FSYNC"), [`O_SYMLINK`](#os.O_SYMLINK "os.O_SYMLINK")
    and [`O_NOFOLLOW_ANY`](#os.O_NOFOLLOW_ANY "os.O_NOFOLLOW_ANY") constants.

os.O\_ASYNC[¶](#os.O_ASYNC "Link to this definition")

os.O\_DIRECT[¶](#os.O_DIRECT "Link to this definition")

os.O\_DIRECTORY[¶](#os.O_DIRECTORY "Link to this definition")

os.O\_NOFOLLOW[¶](#os.O_NOFOLLOW "Link to this definition")

os.O\_NOATIME[¶](#os.O_NOATIME "Link to this definition")

os.O\_PATH[¶](#os.O_PATH "Link to this definition")

os.O\_TMPFILE[¶](#os.O_TMPFILE "Link to this definition")

os.O\_SHLOCK[¶](#os.O_SHLOCK "Link to this definition")

os.O\_EXLOCK[¶](#os.O_EXLOCK "Link to this definition")
:   The above constants are extensions and not present if they are not defined by
    the C library.

    Changed in version 3.4: Add [`O_PATH`](#os.O_PATH "os.O_PATH") on systems that support it.
    Add [`O_TMPFILE`](#os.O_TMPFILE "os.O_TMPFILE"), only available on Linux Kernel 3.11
    or newer.

os.openpty()[¶](#os.openpty "Link to this definition")
:   Open a new pseudo-terminal pair. Return a pair of file descriptors
    `(master, slave)` for the pty and the tty, respectively. The new file
    descriptors are [non-inheritable](#fd-inheritance). For a (slightly) more
    portable approach, use the [`pty`](pty.html#module-pty "pty: Pseudo-Terminal Handling for Unix. (Unix)") module.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Changed in version 3.4: The new file descriptors are now non-inheritable.

os.pipe()[¶](#os.pipe "Link to this definition")
:   Create a pipe. Return a pair of file descriptors `(r, w)` usable for
    reading and writing, respectively. The new file descriptor is
    [non-inheritable](#fd-inheritance).

    [Availability](intro.html#availability): Unix, Windows.

    Changed in version 3.4: The new file descriptors are now non-inheritable.

os.pipe2(*flags*, */*)[¶](#os.pipe2 "Link to this definition")
:   Create a pipe with *flags* set atomically.
    *flags* can be constructed by ORing together one or more of these values:
    [`O_NONBLOCK`](#os.O_NONBLOCK "os.O_NONBLOCK"), [`O_CLOEXEC`](#os.O_CLOEXEC "os.O_CLOEXEC").
    Return a pair of file descriptors `(r, w)` usable for reading and writing,
    respectively.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.posix\_fallocate(*fd*, *offset*, *len*, */*)[¶](#os.posix_fallocate "Link to this definition")
:   Ensures that enough disk space is allocated for the file specified by *fd*
    starting from *offset* and continuing for *len* bytes.

    [Availability](intro.html#availability): Unix, not Emscripten.

    Added in version 3.3.

os.posix\_fadvise(*fd*, *offset*, *len*, *advice*, */*)[¶](#os.posix_fadvise "Link to this definition")
:   Announces an intention to access data in a specific pattern thus allowing
    the kernel to make optimizations.
    The advice applies to the region of the file specified by *fd* starting at
    *offset* and continuing for *len* bytes.
    *advice* is one of [`POSIX_FADV_NORMAL`](#os.POSIX_FADV_NORMAL "os.POSIX_FADV_NORMAL"), [`POSIX_FADV_SEQUENTIAL`](#os.POSIX_FADV_SEQUENTIAL "os.POSIX_FADV_SEQUENTIAL"),
    [`POSIX_FADV_RANDOM`](#os.POSIX_FADV_RANDOM "os.POSIX_FADV_RANDOM"), [`POSIX_FADV_NOREUSE`](#os.POSIX_FADV_NOREUSE "os.POSIX_FADV_NOREUSE"),
    [`POSIX_FADV_WILLNEED`](#os.POSIX_FADV_WILLNEED "os.POSIX_FADV_WILLNEED") or [`POSIX_FADV_DONTNEED`](#os.POSIX_FADV_DONTNEED "os.POSIX_FADV_DONTNEED").

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.POSIX\_FADV\_NORMAL[¶](#os.POSIX_FADV_NORMAL "Link to this definition")

os.POSIX\_FADV\_SEQUENTIAL[¶](#os.POSIX_FADV_SEQUENTIAL "Link to this definition")

os.POSIX\_FADV\_RANDOM[¶](#os.POSIX_FADV_RANDOM "Link to this definition")

os.POSIX\_FADV\_NOREUSE[¶](#os.POSIX_FADV_NOREUSE "Link to this definition")

os.POSIX\_FADV\_WILLNEED[¶](#os.POSIX_FADV_WILLNEED "Link to this definition")

os.POSIX\_FADV\_DONTNEED[¶](#os.POSIX_FADV_DONTNEED "Link to this definition")
:   Flags that can be used in *advice* in [`posix_fadvise()`](#os.posix_fadvise "os.posix_fadvise") that specify
    the access pattern that is likely to be used.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.pread(*fd*, *n*, *offset*, */*)[¶](#os.pread "Link to this definition")
:   Read at most *n* bytes from file descriptor *fd* at a position of *offset*,
    leaving the file offset unchanged.

    Return a bytestring containing the bytes read. If the end of the file
    referred to by *fd* has been reached, an empty bytes object is returned.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.preadv(*fd*, *buffers*, *offset*, *flags=0*, */*)[¶](#os.preadv "Link to this definition")
:   Read from a file descriptor *fd* at a position of *offset* into mutable
    [bytes-like objects](../glossary.html#term-bytes-like-object) *buffers*, leaving the file
    offset unchanged. Transfer data into each buffer until it is full and then
    move on to the next buffer in the sequence to hold the rest of the data.

    The flags argument contains a bitwise OR of zero or more of the following
    flags:

    * [`RWF_HIPRI`](#os.RWF_HIPRI "os.RWF_HIPRI")
    * [`RWF_NOWAIT`](#os.RWF_NOWAIT "os.RWF_NOWAIT")

    Return the total number of bytes actually read which can be less than the
    total capacity of all the objects.

    The operating system may set a limit ([`sysconf()`](#os.sysconf "os.sysconf") value
    `'SC_IOV_MAX'`) on the number of buffers that can be used.

    Combine the functionality of [`os.readv()`](#os.readv "os.readv") and [`os.pread()`](#os.pread "os.pread").

    [Availability](intro.html#availability): Linux >= 2.6.30, FreeBSD >= 6.0, OpenBSD >= 2.7, AIX >= 7.1.

    Using flags requires Linux >= 4.6.

    Added in version 3.7.

os.RWF\_NOWAIT[¶](#os.RWF_NOWAIT "Link to this definition")
:   Do not wait for data which is not immediately available. If this flag is
    specified, the system call will return instantly if it would have to read
    data from the backing storage or wait for a lock.

    If some data was successfully read, it will return the number of bytes read.
    If no bytes were read, it will return `-1` and set errno to
    [`errno.EAGAIN`](errno.html#errno.EAGAIN "errno.EAGAIN").

    [Availability](intro.html#availability): Linux >= 4.14.

    Added in version 3.7.

os.RWF\_HIPRI[¶](#os.RWF_HIPRI "Link to this definition")
:   High priority read/write. Allows block-based filesystems to use polling
    of the device, which provides lower latency, but may use additional
    resources.

    Currently, on Linux, this feature is usable only on a file descriptor opened
    using the [`O_DIRECT`](#os.O_DIRECT "os.O_DIRECT") flag.

    [Availability](intro.html#availability): Linux >= 4.6.

    Added in version 3.7.

os.pwrite(*fd*, *str*, *offset*, */*)[¶](#os.pwrite "Link to this definition")
:   Write the bytestring in *str* to file descriptor *fd* at position of
    *offset*, leaving the file offset unchanged.

    Return the number of bytes actually written.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.pwritev(*fd*, *buffers*, *offset*, *flags=0*, */*)[¶](#os.pwritev "Link to this definition")
:   Write the *buffers* contents to file descriptor *fd* at an offset *offset*,
    leaving the file offset unchanged. *buffers* must be a sequence of
    [bytes-like objects](../glossary.html#term-bytes-like-object). Buffers are processed in
    array order. Entire contents of the first buffer is written before
    proceeding to the second, and so on.

    The flags argument contains a bitwise OR of zero or more of the following
    flags:

    * [`RWF_DSYNC`](#os.RWF_DSYNC "os.RWF_DSYNC")
    * [`RWF_SYNC`](#os.RWF_SYNC "os.RWF_SYNC")
    * [`RWF_APPEND`](#os.RWF_APPEND "os.RWF_APPEND")

    Return the total number of bytes actually written.

    The operating system may set a limit ([`sysconf()`](#os.sysconf "os.sysconf") value
    `'SC_IOV_MAX'`) on the number of buffers that can be used.

    Combine the functionality of [`os.writev()`](#os.writev "os.writev") and [`os.pwrite()`](#os.pwrite "os.pwrite").

    [Availability](intro.html#availability): Linux >= 2.6.30, FreeBSD >= 6.0, OpenBSD >= 2.7, AIX >= 7.1.

    Using flags requires Linux >= 4.6.

    Added in version 3.7.

os.RWF\_DSYNC[¶](#os.RWF_DSYNC "Link to this definition")
:   Provide a per-write equivalent of the [`O_DSYNC`](#os.O_DSYNC "os.O_DSYNC") [`os.open()`](#os.open "os.open") flag.
    This flag effect applies only to the data range written by the system call.

    [Availability](intro.html#availability): Linux >= 4.7.

    Added in version 3.7.

os.RWF\_SYNC[¶](#os.RWF_SYNC "Link to this definition")
:   Provide a per-write equivalent of the [`O_SYNC`](#os.O_SYNC "os.O_SYNC") [`os.open()`](#os.open "os.open") flag.
    This flag effect applies only to the data range written by the system call.

    [Availability](intro.html#availability): Linux >= 4.7.

    Added in version 3.7.

os.RWF\_APPEND[¶](#os.RWF_APPEND "Link to this definition")
:   Provide a per-write equivalent of the [`O_APPEND`](#os.O_APPEND "os.O_APPEND") [`os.open()`](#os.open "os.open")
    flag. This flag is meaningful only for [`os.pwritev()`](#os.pwritev "os.pwritev"), and its
    effect applies only to the data range written by the system call. The
    *offset* argument does not affect the write operation; the data is always
    appended to the end of the file. However, if the *offset* argument is
    `-1`, the current file *offset* is updated.

    [Availability](intro.html#availability): Linux >= 4.16.

    Added in version 3.10.

os.read(*fd*, *n*, */*)[¶](#os.read "Link to this definition")
:   Read at most *n* bytes from file descriptor *fd*.

    Return a bytestring containing the bytes read. If the end of the file
    referred to by *fd* has been reached, an empty bytes object is returned.

    Note

    This function is intended for low-level I/O and must be applied to a file
    descriptor as returned by [`os.open()`](#os.open "os.open") or [`pipe()`](#os.pipe "os.pipe"). To read a
    “file object” returned by the built-in function [`open()`](functions.html#open "open") or by
    [`popen()`](#os.popen "os.popen") or [`fdopen()`](#os.fdopen "os.fdopen"), or [`sys.stdin`](sys.html#sys.stdin "sys.stdin"), use its
    `read()` or `readline()` methods.

    Changed in version 3.5: If the system call is interrupted and the signal handler does not raise an
    exception, the function now retries the system call instead of raising an
    [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError") exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for the rationale).

os.sendfile(*out\_fd*, *in\_fd*, *offset*, *count*)[¶](#os.sendfile "Link to this definition")

os.sendfile(*out\_fd*, *in\_fd*, *offset*, *count*, *headers=()*, *trailers=()*, *flags=0*)
:   Copy *count* bytes from file descriptor *in\_fd* to file descriptor *out\_fd*
    starting at *offset*.
    Return the number of bytes sent. When EOF is reached return `0`.

    The first function notation is supported by all platforms that define
    [`sendfile()`](#os.sendfile "os.sendfile").

    On Linux, if *offset* is given as `None`, the bytes are read from the
    current position of *in\_fd* and the position of *in\_fd* is updated.

    The second case may be used on macOS and FreeBSD where *headers* and
    *trailers* are arbitrary sequences of buffers that are written before and
    after the data from *in\_fd* is written. It returns the same as the first case.

    On macOS and FreeBSD, a value of `0` for *count* specifies to send until
    the end of *in\_fd* is reached.

    All platforms support sockets as *out\_fd* file descriptor, and some platforms
    allow other types (e.g. regular file, pipe) as well.

    Cross-platform applications should not use *headers*, *trailers* and *flags*
    arguments.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Note

    For a higher-level wrapper of [`sendfile()`](#os.sendfile "os.sendfile"), see
    [`socket.socket.sendfile()`](socket.html#socket.socket.sendfile "socket.socket.sendfile").

    Added in version 3.3.

    Changed in version 3.9: Parameters *out* and *in* was renamed to *out\_fd* and *in\_fd*.

os.SF\_NODISKIO[¶](#os.SF_NODISKIO "Link to this definition")

os.SF\_MNOWAIT[¶](#os.SF_MNOWAIT "Link to this definition")

os.SF\_SYNC[¶](#os.SF_SYNC "Link to this definition")
:   Parameters to the [`sendfile()`](#os.sendfile "os.sendfile") function, if the implementation supports
    them.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.SF\_NOCACHE[¶](#os.SF_NOCACHE "Link to this definition")
:   Parameter to the [`sendfile()`](#os.sendfile "os.sendfile") function, if the implementation supports
    it. The data won’t be cached in the virtual memory and will be freed afterwards.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.11.

os.set\_blocking(*fd*, *blocking*, */*)[¶](#os.set_blocking "Link to this definition")
:   Set the blocking mode of the specified file descriptor. Set the
    [`O_NONBLOCK`](#os.O_NONBLOCK "os.O_NONBLOCK") flag if blocking is `False`, clear the flag otherwise.

    See also [`get_blocking()`](#os.get_blocking "os.get_blocking") and [`socket.socket.setblocking()`](socket.html#socket.socket.setblocking "socket.socket.setblocking").

    [Availability](intro.html#availability): Unix, Windows.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

    On Windows, this function is limited to pipes.

    Added in version 3.5.

    Changed in version 3.12: Added support for pipes on Windows.

os.splice(*src*, *dst*, *count*, *offset\_src=None*, *offset\_dst=None*)[¶](#os.splice "Link to this definition")
:   Transfer *count* bytes from file descriptor *src*, starting from offset
    *offset\_src*, to file descriptor *dst*, starting from offset *offset\_dst*.
    At least one of the file descriptors must refer to a pipe. If *offset\_src*
    is `None`, then *src* is read from the current position; respectively for
    *offset\_dst*. The offset associated to the file descriptor that refers to a
    pipe must be `None`. The files pointed to by *src* and *dst* must reside in
    the same filesystem, otherwise an [`OSError`](exceptions.html#OSError "OSError") is raised with
    [`errno`](exceptions.html#OSError.errno "OSError.errno") set to [`errno.EXDEV`](errno.html#errno.EXDEV "errno.EXDEV").

    This copy is done without the additional cost of transferring data
    from the kernel to user space and then back into the kernel. Additionally,
    some filesystems could implement extra optimizations. The copy is done as if
    both files are opened as binary.

    Upon successful completion, returns the number of bytes spliced to or from
    the pipe. A return value of 0 means end of input. If *src* refers to a
    pipe, then this means that there was no data to transfer, and it would not
    make sense to block because there are no writers connected to the write end
    of the pipe.

    [Availability](intro.html#availability): Linux >= 2.6.17 with glibc >= 2.5

    Added in version 3.10.

os.SPLICE\_F\_MOVE[¶](#os.SPLICE_F_MOVE "Link to this definition")

os.SPLICE\_F\_NONBLOCK[¶](#os.SPLICE_F_NONBLOCK "Link to this definition")

os.SPLICE\_F\_MORE[¶](#os.SPLICE_F_MORE "Link to this definition")
:   Added in version 3.10.

os.readv(*fd*, *buffers*, */*)[¶](#os.readv "Link to this definition")
:   Read from a file descriptor *fd* into a number of mutable [bytes-like
    objects](../glossary.html#term-bytes-like-object) *buffers*. Transfer data into each buffer until
    it is full and then move on to the next buffer in the sequence to hold the
    rest of the data.

    Return the total number of bytes actually read which can be less than the
    total capacity of all the objects.

    The operating system may set a limit ([`sysconf()`](#os.sysconf "os.sysconf") value
    `'SC_IOV_MAX'`) on the number of buffers that can be used.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.tcgetpgrp(*fd*, */*)[¶](#os.tcgetpgrp "Link to this definition")
:   Return the process group associated with the terminal given by *fd* (an open
    file descriptor as returned by [`os.open()`](#os.open "os.open")).

    [Availability](intro.html#availability): Unix, not WASI.

os.tcsetpgrp(*fd*, *pg*, */*)[¶](#os.tcsetpgrp "Link to this definition")
:   Set the process group associated with the terminal given by *fd* (an open file
    descriptor as returned by [`os.open()`](#os.open "os.open")) to *pg*.

    [Availability](intro.html#availability): Unix, not WASI.

os.ttyname(*fd*, */*)[¶](#os.ttyname "Link to this definition")
:   Return a string which specifies the terminal device associated with
    file descriptor *fd*. If *fd* is not associated with a terminal device, an
    exception is raised.

    [Availability](intro.html#availability): Unix.

os.write(*fd*, *str*, */*)[¶](#os.write "Link to this definition")
:   Write the bytestring in *str* to file descriptor *fd*.

    Return the number of bytes actually written.

    Note

    This function is intended for low-level I/O and must be applied to a file
    descriptor as returned by [`os.open()`](#os.open "os.open") or [`pipe()`](#os.pipe "os.pipe"). To write a “file
    object” returned by the built-in function [`open()`](functions.html#open "open") or by [`popen()`](#os.popen "os.popen") or
    [`fdopen()`](#os.fdopen "os.fdopen"), or [`sys.stdout`](sys.html#sys.stdout "sys.stdout") or [`sys.stderr`](sys.html#sys.stderr "sys.stderr"), use its
    `write()` method.

    Changed in version 3.5: If the system call is interrupted and the signal handler does not raise an
    exception, the function now retries the system call instead of raising an
    [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError") exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for the rationale).

os.writev(*fd*, *buffers*, */*)[¶](#os.writev "Link to this definition")
:   Write the contents of *buffers* to file descriptor *fd*. *buffers* must be
    a sequence of [bytes-like objects](../glossary.html#term-bytes-like-object). Buffers are
    processed in array order. Entire contents of the first buffer is written
    before proceeding to the second, and so on.

    Returns the total number of bytes actually written.

    The operating system may set a limit ([`sysconf()`](#os.sysconf "os.sysconf") value
    `'SC_IOV_MAX'`) on the number of buffers that can be used.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

### Querying the size of a terminal[¶](#querying-the-size-of-a-terminal "Link to this heading")

Added in version 3.3.

os.get\_terminal\_size(*fd=STDOUT\_FILENO*, */*)[¶](#os.get_terminal_size "Link to this definition")
:   Return the size of the terminal window as `(columns, lines)`,
    tuple of type [`terminal_size`](#os.terminal_size "os.terminal_size").

    The optional argument `fd` (default `STDOUT_FILENO`, or standard
    output) specifies which file descriptor should be queried.

    If the file descriptor is not connected to a terminal, an [`OSError`](exceptions.html#OSError "OSError")
    is raised.

    [`shutil.get_terminal_size()`](shutil.html#shutil.get_terminal_size "shutil.get_terminal_size") is the high-level function which
    should normally be used, `os.get_terminal_size` is the low-level
    implementation.

    [Availability](intro.html#availability): Unix, Windows.

*class* os.terminal\_size[¶](#os.terminal_size "Link to this definition")
:   A subclass of tuple, holding `(columns, lines)` of the terminal window size.

    columns[¶](#os.terminal_size.columns "Link to this definition")
    :   Width of the terminal window in characters.

    lines[¶](#os.terminal_size.lines "Link to this definition")
    :   Height of the terminal window in characters.

### Inheritance of File Descriptors[¶](#inheritance-of-file-descriptors "Link to this heading")

Added in version 3.4.

A file descriptor has an “inheritable” flag which indicates if the file descriptor
can be inherited by child processes. Since Python 3.4, file descriptors
created by Python are non-inheritable by default.

On UNIX, non-inheritable file descriptors are closed in child processes at the
execution of a new program, other file descriptors are inherited.

On Windows, non-inheritable handles and file descriptors are closed in child
processes, except for standard streams (file descriptors 0, 1 and 2: stdin, stdout
and stderr), which are always inherited. Using [`spawn*`](#os.spawnl "os.spawnl") functions,
all inheritable handles and all inheritable file descriptors are inherited.
Using the [`subprocess`](subprocess.html#module-subprocess "subprocess: Subprocess management.") module, all file descriptors except standard
streams are closed, and inheritable handles are only inherited if the
*close\_fds* parameter is `False`.

On WebAssembly platforms `wasm32-emscripten` and `wasm32-wasi`, the file
descriptor cannot be modified.

os.get\_inheritable(*fd*, */*)[¶](#os.get_inheritable "Link to this definition")
:   Get the “inheritable” flag of the specified file descriptor (a boolean).

os.set\_inheritable(*fd*, *inheritable*, */*)[¶](#os.set_inheritable "Link to this definition")
:   Set the “inheritable” flag of the specified file descriptor.

os.get\_handle\_inheritable(*handle*, */*)[¶](#os.get_handle_inheritable "Link to this definition")
:   Get the “inheritable” flag of the specified handle (a boolean).

    [Availability](intro.html#availability): Windows.

os.set\_handle\_inheritable(*handle*, *inheritable*, */*)[¶](#os.set_handle_inheritable "Link to this definition")
:   Set the “inheritable” flag of the specified handle.

    [Availability](intro.html#availability): Windows.

## Files and Directories[¶](#files-and-directories "Link to this heading")

On some Unix platforms, many of these functions support one or more of these
features:

* **specifying a file descriptor:**
  Normally the *path* argument provided to functions in the [`os`](#module-os "os: Miscellaneous operating system interfaces.") module
  must be a string specifying a file path. However, some functions now
  alternatively accept an open file descriptor for their *path* argument.
  The function will then operate on the file referred to by the descriptor.
  (For POSIX systems, Python will call the variant of the function prefixed
  with `f` (e.g. call `fchdir` instead of `chdir`).)

  You can check whether or not *path* can be specified as a file descriptor
  for a particular function on your platform using [`os.supports_fd`](#os.supports_fd "os.supports_fd").
  If this functionality is unavailable, using it will raise a
  [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError").

  If the function also supports *dir\_fd* or *follow\_symlinks* arguments, it’s
  an error to specify one of those when supplying *path* as a file descriptor.

* **paths relative to directory descriptors:** If *dir\_fd* is not `None`, it
  should be a file descriptor referring to a directory, and the path to operate
  on should be relative; path will then be relative to that directory. If the
  path is absolute, *dir\_fd* is ignored. (For POSIX systems, Python will call
  the variant of the function with an `at` suffix and possibly prefixed with
  `f` (e.g. call `faccessat` instead of `access`).

  You can check whether or not *dir\_fd* is supported for a particular function
  on your platform using [`os.supports_dir_fd`](#os.supports_dir_fd "os.supports_dir_fd"). If it’s unavailable,
  using it will raise a [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError").

* **not following symlinks:** If *follow\_symlinks* is
  `False`, and the last element of the path to operate on is a symbolic link,
  the function will operate on the symbolic link itself rather than the file
  pointed to by the link. (For POSIX systems, Python will call the `l...`
  variant of the function.)

  You can check whether or not *follow\_symlinks* is supported for a particular
  function on your platform using [`os.supports_follow_symlinks`](#os.supports_follow_symlinks "os.supports_follow_symlinks").
  If it’s unavailable, using it will raise a [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError").

os.access(*path*, *mode*, *\**, *dir\_fd=None*, *effective\_ids=False*, *follow\_symlinks=True*)[¶](#os.access "Link to this definition")
:   Use the real uid/gid to test for access to *path*. Note that most operations
    will use the effective uid/gid, therefore this routine can be used in a
    suid/sgid environment to test if the invoking user has the specified access to
    *path*. *mode* should be [`F_OK`](#os.F_OK "os.F_OK") to test the existence of *path*, or it
    can be the inclusive OR of one or more of [`R_OK`](#os.R_OK "os.R_OK"), [`W_OK`](#os.W_OK "os.W_OK"), and
    [`X_OK`](#os.X_OK "os.X_OK") to test permissions. Return [`True`](constants.html#True "True") if access is allowed,
    [`False`](constants.html#False "False") if not. See the Unix man page *[access(2)](https://manpages.debian.org/access(2))* for more
    information.

    This function can support specifying [paths relative to directory
    descriptors](#dir-fd) and [not following symlinks](#follow-symlinks).

    If *effective\_ids* is `True`, [`access()`](#os.access "os.access") will perform its access
    checks using the effective uid/gid instead of the real uid/gid.
    *effective\_ids* may not be supported on your platform; you can check whether
    or not it is available using [`os.supports_effective_ids`](#os.supports_effective_ids "os.supports_effective_ids"). If it is
    unavailable, using it will raise a [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError").

    Note

    Using [`access()`](#os.access "os.access") to check if a user is authorized to e.g. open a file
    before actually doing so using [`open()`](functions.html#open "open") creates a security hole,
    because the user might exploit the short time interval between checking
    and opening the file to manipulate it. It’s preferable to use [EAFP](../glossary.html#term-EAFP)
    techniques. For example:

    ```
    if os.access("myfile", os.R_OK):
        with open("myfile") as fp:
            return fp.read()
    return "some default data"
    ```

    is better written as:

    ```
    try:
        fp = open("myfile")
    except PermissionError:
        return "some default data"
    else:
        with fp:
            return fp.read()
    ```

    Note

    I/O operations may fail even when [`access()`](#os.access "os.access") indicates that they would
    succeed, particularly for operations on network filesystems which may have
    permissions semantics beyond the usual POSIX permission-bit model.

    Changed in version 3.3: Added the *dir\_fd*, *effective\_ids*, and *follow\_symlinks* parameters.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.F\_OK[¶](#os.F_OK "Link to this definition")

os.R\_OK[¶](#os.R_OK "Link to this definition")

os.W\_OK[¶](#os.W_OK "Link to this definition")

os.X\_OK[¶](#os.X_OK "Link to this definition")
:   Values to pass as the *mode* parameter of [`access()`](#os.access "os.access") to test the
    existence, readability, writability and executability of *path*,
    respectively.

os.chdir(*path*)[¶](#os.chdir "Link to this definition")
:   Change the current working directory to *path*.

    This function can support [specifying a file descriptor](#path-fd). The
    descriptor must refer to an opened directory, not an open file.

    This function can raise [`OSError`](exceptions.html#OSError "OSError") and subclasses such as
    [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError"), [`PermissionError`](exceptions.html#PermissionError "PermissionError"), and [`NotADirectoryError`](exceptions.html#NotADirectoryError "NotADirectoryError").

    Raises an [auditing event](sys.html#auditing) `os.chdir` with argument `path`.

    Changed in version 3.3: Added support for specifying *path* as a file descriptor
    on some platforms.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.chflags(*path*, *flags*, *\**, *follow\_symlinks=True*)[¶](#os.chflags "Link to this definition")
:   Set the flags of *path* to the numeric *flags*. *flags* may take a combination
    (bitwise OR) of the following values (as defined in the [`stat`](stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") module):

    * [`stat.UF_NODUMP`](stat.html#stat.UF_NODUMP "stat.UF_NODUMP")
    * [`stat.UF_IMMUTABLE`](stat.html#stat.UF_IMMUTABLE "stat.UF_IMMUTABLE")
    * [`stat.UF_APPEND`](stat.html#stat.UF_APPEND "stat.UF_APPEND")
    * [`stat.UF_OPAQUE`](stat.html#stat.UF_OPAQUE "stat.UF_OPAQUE")
    * [`stat.UF_NOUNLINK`](stat.html#stat.UF_NOUNLINK "stat.UF_NOUNLINK")
    * [`stat.UF_COMPRESSED`](stat.html#stat.UF_COMPRESSED "stat.UF_COMPRESSED")
    * [`stat.UF_HIDDEN`](stat.html#stat.UF_HIDDEN "stat.UF_HIDDEN")
    * [`stat.SF_ARCHIVED`](stat.html#stat.SF_ARCHIVED "stat.SF_ARCHIVED")
    * [`stat.SF_IMMUTABLE`](stat.html#stat.SF_IMMUTABLE "stat.SF_IMMUTABLE")
    * [`stat.SF_APPEND`](stat.html#stat.SF_APPEND "stat.SF_APPEND")
    * [`stat.SF_NOUNLINK`](stat.html#stat.SF_NOUNLINK "stat.SF_NOUNLINK")
    * [`stat.SF_SNAPSHOT`](stat.html#stat.SF_SNAPSHOT "stat.SF_SNAPSHOT")

    This function can support [not following symlinks](#follow-symlinks).

    Raises an [auditing event](sys.html#auditing) `os.chflags` with arguments `path`, `flags`.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Changed in version 3.3: Added the *follow\_symlinks* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.chmod(*path*, *mode*, *\**, *dir\_fd=None*, *follow\_symlinks=True*)[¶](#os.chmod "Link to this definition")
:   Change the mode of *path* to the numeric *mode*. *mode* may take one of the
    following values (as defined in the [`stat`](stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") module) or bitwise ORed
    combinations of them:

    * [`stat.S_ISUID`](stat.html#stat.S_ISUID "stat.S_ISUID")
    * [`stat.S_ISGID`](stat.html#stat.S_ISGID "stat.S_ISGID")
    * [`stat.S_ENFMT`](stat.html#stat.S_ENFMT "stat.S_ENFMT")
    * [`stat.S_ISVTX`](stat.html#stat.S_ISVTX "stat.S_ISVTX")
    * [`stat.S_IREAD`](stat.html#stat.S_IREAD "stat.S_IREAD")
    * [`stat.S_IWRITE`](stat.html#stat.S_IWRITE "stat.S_IWRITE")
    * [`stat.S_IEXEC`](stat.html#stat.S_IEXEC "stat.S_IEXEC")
    * [`stat.S_IRWXU`](stat.html#stat.S_IRWXU "stat.S_IRWXU")
    * [`stat.S_IRUSR`](stat.html#stat.S_IRUSR "stat.S_IRUSR")
    * [`stat.S_IWUSR`](stat.html#stat.S_IWUSR "stat.S_IWUSR")
    * [`stat.S_IXUSR`](stat.html#stat.S_IXUSR "stat.S_IXUSR")
    * [`stat.S_IRWXG`](stat.html#stat.S_IRWXG "stat.S_IRWXG")
    * [`stat.S_IRGRP`](stat.html#stat.S_IRGRP "stat.S_IRGRP")
    * [`stat.S_IWGRP`](stat.html#stat.S_IWGRP "stat.S_IWGRP")
    * [`stat.S_IXGRP`](stat.html#stat.S_IXGRP "stat.S_IXGRP")
    * [`stat.S_IRWXO`](stat.html#stat.S_IRWXO "stat.S_IRWXO")
    * [`stat.S_IROTH`](stat.html#stat.S_IROTH "stat.S_IROTH")
    * [`stat.S_IWOTH`](stat.html#stat.S_IWOTH "stat.S_IWOTH")
    * [`stat.S_IXOTH`](stat.html#stat.S_IXOTH "stat.S_IXOTH")

    This function can support [specifying a file descriptor](#path-fd),
    [paths relative to directory descriptors](#dir-fd) and [not
    following symlinks](#follow-symlinks).

    Note

    Although Windows supports [`chmod()`](#os.chmod "os.chmod"), you can only set the file’s
    read-only flag with it (via the `stat.S_IWRITE` and `stat.S_IREAD`
    constants or a corresponding integer value). All other bits are ignored.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

    Raises an [auditing event](sys.html#auditing) `os.chmod` with arguments `path`, `mode`, `dir_fd`.

    Changed in version 3.3: Added support for specifying *path* as an open file descriptor,
    and the *dir\_fd* and *follow\_symlinks* arguments.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.chown(*path*, *uid*, *gid*, *\**, *dir\_fd=None*, *follow\_symlinks=True*)[¶](#os.chown "Link to this definition")
:   Change the owner and group id of *path* to the numeric *uid* and *gid*. To
    leave one of the ids unchanged, set it to -1.

    This function can support [specifying a file descriptor](#path-fd),
    [paths relative to directory descriptors](#dir-fd) and [not
    following symlinks](#follow-symlinks).

    See [`shutil.chown()`](shutil.html#shutil.chown "shutil.chown") for a higher-level function that accepts names in
    addition to numeric ids.

    Raises an [auditing event](sys.html#auditing) `os.chown` with arguments `path`, `uid`, `gid`, `dir_fd`.

    [Availability](intro.html#availability): Unix.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

    Changed in version 3.3: Added support for specifying *path* as an open file descriptor,
    and the *dir\_fd* and *follow\_symlinks* arguments.

    Changed in version 3.6: Supports a [path-like object](../glossary.html#term-path-like-object).

os.chroot(*path*)[¶](#os.chroot "Link to this definition")
:   Change the root directory of the current process to *path*.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.fchdir(*fd*)[¶](#os.fchdir "Link to this definition")
:   Change the current working directory to the directory represented by the file
    descriptor *fd*. The descriptor must refer to an opened directory, not an
    open file. As of Python 3.3, this is equivalent to `os.chdir(fd)`.

    Raises an [auditing event](sys.html#auditing) `os.chdir` with argument `path`.

    [Availability](intro.html#availability): Unix.

os.getcwd()[¶](#os.getcwd "Link to this definition")
:   Return a string representing the current working directory.

os.getcwdb()[¶](#os.getcwdb "Link to this definition")
:   Return a bytestring representing the current working directory.

    Changed in version 3.8: The function now uses the UTF-8 encoding on Windows, rather than the ANSI
    code page: see [**PEP 529**](https://peps.python.org/pep-0529/) for the rationale. The function is no longer
    deprecated on Windows.

os.lchflags(*path*, *flags*)[¶](#os.lchflags "Link to this definition")
:   Set the flags of *path* to the numeric *flags*, like [`chflags()`](#os.chflags "os.chflags"), but do
    not follow symbolic links. As of Python 3.3, this is equivalent to
    `os.chflags(path, flags, follow_symlinks=False)`.

    Raises an [auditing event](sys.html#auditing) `os.chflags` with arguments `path`, `flags`.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.lchmod(*path*, *mode*)[¶](#os.lchmod "Link to this definition")
:   Change the mode of *path* to the numeric *mode*. If path is a symlink, this
    affects the symlink rather than the target. See the docs for [`chmod()`](#os.chmod "os.chmod")
    for possible values of *mode*. As of Python 3.3, this is equivalent to
    `os.chmod(path, mode, follow_symlinks=False)`.

    `lchmod()` is not part of POSIX, but Unix implementations may have it if
    changing the mode of symbolic links is supported.

    Raises an [auditing event](sys.html#auditing) `os.chmod` with arguments `path`, `mode`, `dir_fd`.

    [Availability](intro.html#availability): Unix, not Linux, FreeBSD >= 1.3, NetBSD >= 1.3, not OpenBSD

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.lchown(*path*, *uid*, *gid*)[¶](#os.lchown "Link to this definition")
:   Change the owner and group id of *path* to the numeric *uid* and *gid*. This
    function will not follow symbolic links. As of Python 3.3, this is equivalent
    to `os.chown(path, uid, gid, follow_symlinks=False)`.

    Raises an [auditing event](sys.html#auditing) `os.chown` with arguments `path`, `uid`, `gid`, `dir_fd`.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.link(*src*, *dst*, *\**, *src\_dir\_fd=None*, *dst\_dir\_fd=None*, *follow\_symlinks=True*)[¶](#os.link "Link to this definition")
:   Create a hard link pointing to *src* named *dst*.

    This function can support specifying *src\_dir\_fd* and/or *dst\_dir\_fd* to
    supply [paths relative to directory descriptors](#dir-fd), and [not
    following symlinks](#follow-symlinks).

    Raises an [auditing event](sys.html#auditing) `os.link` with arguments `src`, `dst`, `src_dir_fd`, `dst_dir_fd`.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten.

    Changed in version 3.2: Added Windows support.

    Changed in version 3.3: Added the *src\_dir\_fd*, *dst\_dir\_fd*, and *follow\_symlinks* parameters.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *src* and *dst*.

os.listdir(*path='.'*)[¶](#os.listdir "Link to this definition")
:   Return a list containing the names of the entries in the directory given by
    *path*. The list is in arbitrary order, and does not include the special
    entries `'.'` and `'..'` even if they are present in the directory.
    If a file is removed from or added to the directory during the call of
    this function, whether a name for that file be included is unspecified.

    *path* may be a [path-like object](../glossary.html#term-path-like-object). If *path* is of type `bytes`
    (directly or indirectly through the [`PathLike`](#os.PathLike "os.PathLike") interface),
    the filenames returned will also be of type `bytes`;
    in all other circumstances, they will be of type `str`.

    This function can also support [specifying a file descriptor](#path-fd); the file descriptor must refer to a directory.

    Raises an [auditing event](sys.html#auditing) `os.listdir` with argument `path`.

    Note

    To encode `str` filenames to `bytes`, use [`fsencode()`](#os.fsencode "os.fsencode").

    See also

    The [`scandir()`](#os.scandir "os.scandir") function returns directory entries along with
    file attribute information, giving better performance for many
    common use cases.

    Changed in version 3.2: The *path* parameter became optional.

    Changed in version 3.3: Added support for specifying *path* as an open file descriptor.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.listdrives()[¶](#os.listdrives "Link to this definition")
:   Return a list containing the names of drives on a Windows system.

    A drive name typically looks like `'C:\\'`. Not every drive name
    will be associated with a volume, and some may be inaccessible for
    a variety of reasons, including permissions, network connectivity
    or missing media. This function does not test for access.

    May raise [`OSError`](exceptions.html#OSError "OSError") if an error occurs collecting the drive
    names.

    Raises an [auditing event](sys.html#auditing) `os.listdrives` with no arguments.

    [Availability](intro.html#availability): Windows

    Added in version 3.12.

os.listmounts(*volume*)[¶](#os.listmounts "Link to this definition")
:   Return a list containing the mount points for a volume on a Windows
    system.

    *volume* must be represented as a GUID path, like those returned by
    [`os.listvolumes()`](#os.listvolumes "os.listvolumes"). Volumes may be mounted in multiple locations
    or not at all. In the latter case, the list will be empty. Mount
    points that are not associated with a volume will not be returned by
    this function.

    The mount points return by this function will be absolute paths, and
    may be longer than the drive name.

    Raises [`OSError`](exceptions.html#OSError "OSError") if the volume is not recognized or if an error
    occurs collecting the paths.

    Raises an [auditing event](sys.html#auditing) `os.listmounts` with argument `volume`.

    [Availability](intro.html#availability): Windows

    Added in version 3.12.

os.listvolumes()[¶](#os.listvolumes "Link to this definition")
:   Return a list containing the volumes in the system.

    Volumes are typically represented as a GUID path that looks like
    `\\?\Volume{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}\`. Files can
    usually be accessed through a GUID path, permissions allowing.
    However, users are generally not familiar with them, and so the
    recommended use of this function is to retrieve mount points
    using [`os.listmounts()`](#os.listmounts "os.listmounts").

    May raise [`OSError`](exceptions.html#OSError "OSError") if an error occurs collecting the volumes.

    Raises an [auditing event](sys.html#auditing) `os.listvolumes` with no arguments.

    [Availability](intro.html#availability): Windows

    Added in version 3.12.

os.lstat(*path*, *\**, *dir\_fd=None*)[¶](#os.lstat "Link to this definition")
:   Perform the equivalent of an `lstat()` system call on the given path.
    Similar to [`stat()`](#os.stat "os.stat"), but does not follow symbolic links. Return a
    [`stat_result`](#os.stat_result "os.stat_result") object.

    On platforms that do not support symbolic links, this is an alias for
    [`stat()`](#os.stat "os.stat").

    As of Python 3.3, this is equivalent to `os.stat(path, dir_fd=dir_fd,
    follow_symlinks=False)`.

    This function can also support [paths relative to directory descriptors](#dir-fd).

    See also

    The [`stat()`](#os.stat "os.stat") function.

    Changed in version 3.2: Added support for Windows 6.0 (Vista) symbolic links.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.8: On Windows, now opens reparse points that represent another path
    (name surrogates), including symbolic links and directory junctions.
    Other kinds of reparse points are resolved by the operating system as
    for [`stat()`](#os.stat "os.stat").

os.mkdir(*path*, *mode=0o777*, *\**, *dir\_fd=None*)[¶](#os.mkdir "Link to this definition")
:   Create a directory named *path* with numeric mode *mode*.

    If the directory already exists, [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is raised. If a parent
    directory in the path does not exist, [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") is raised.

    On some systems, *mode* is ignored. Where it is used, the current umask
    value is first masked out. If bits other than the last 9 (i.e. the last 3
    digits of the octal representation of the *mode*) are set, their meaning is
    platform-dependent. On some platforms, they are ignored and you should call
    [`chmod()`](#os.chmod "os.chmod") explicitly to set them.

    On Windows, a *mode* of `0o700` is specifically handled to apply access
    control to the new directory such that only the current user and
    administrators have access. Other values of *mode* are ignored.

    This function can also support [paths relative to directory descriptors](#dir-fd).

    It is also possible to create temporary directories; see the
    [`tempfile`](tempfile.html#module-tempfile "tempfile: Generate temporary files and directories.") module’s [`tempfile.mkdtemp()`](tempfile.html#tempfile.mkdtemp "tempfile.mkdtemp") function.

    Raises an [auditing event](sys.html#auditing) `os.mkdir` with arguments `path`, `mode`, `dir_fd`.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.12.4: Windows now handles a *mode* of `0o700`.

os.makedirs(*name*, *mode=0o777*, *exist\_ok=False*)[¶](#os.makedirs "Link to this definition")
:   Recursive directory creation function. Like [`mkdir()`](#os.mkdir "os.mkdir"), but makes all
    intermediate-level directories needed to contain the leaf directory.

    The *mode* parameter is passed to [`mkdir()`](#os.mkdir "os.mkdir") for creating the leaf
    directory; see [the mkdir() description](#mkdir-modebits) for how it
    is interpreted. To set the file permission bits of any newly created parent
    directories you can set the umask before invoking [`makedirs()`](#os.makedirs "os.makedirs"). The
    file permission bits of existing parent directories are not changed.

    If *exist\_ok* is `False` (the default), a [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is
    raised if the target directory already exists.

    Note

    [`makedirs()`](#os.makedirs "os.makedirs") will become confused if the path elements to create
    include [`pardir`](#os.pardir "os.pardir") (eg. “..” on UNIX systems).

    This function handles UNC paths correctly.

    Raises an [auditing event](sys.html#auditing) `os.mkdir` with arguments `path`, `mode`, `dir_fd`.

    Changed in version 3.2: Added the *exist\_ok* parameter.

    Changed in version 3.4.1: Before Python 3.4.1, if *exist\_ok* was `True` and the directory existed,
    [`makedirs()`](#os.makedirs "os.makedirs") would still raise an error if *mode* did not match the
    mode of the existing directory. Since this behavior was impossible to
    implement safely, it was removed in Python 3.4.1. See [bpo-21082](https://bugs.python.org/issue?@action=redirect&bpo=21082).

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.7: The *mode* argument no longer affects the file permission bits of
    newly created intermediate-level directories.

os.mkfifo(*path*, *mode=0o666*, *\**, *dir\_fd=None*)[¶](#os.mkfifo "Link to this definition")
:   Create a FIFO (a named pipe) named *path* with numeric mode *mode*.
    The current umask value is first masked out from the mode.

    This function can also support [paths relative to directory descriptors](#dir-fd).

    FIFOs are pipes that can be accessed like regular files. FIFOs exist until they
    are deleted (for example with [`os.unlink()`](#os.unlink "os.unlink")). Generally, FIFOs are used as
    rendezvous between “client” and “server” type processes: the server opens the
    FIFO for reading, and the client opens it for writing. Note that [`mkfifo()`](#os.mkfifo "os.mkfifo")
    doesn’t open the FIFO — it just creates the rendezvous point.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.mknod(*path*, *mode=0o600*, *device=0*, *\**, *dir\_fd=None*)[¶](#os.mknod "Link to this definition")
:   Create a filesystem node (file, device special file or named pipe) named
    *path*. *mode* specifies both the permissions to use and the type of node
    to be created, being combined (bitwise OR) with one of `stat.S_IFREG`,
    `stat.S_IFCHR`, `stat.S_IFBLK`, and `stat.S_IFIFO` (those constants are
    available in [`stat`](stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().")). For `stat.S_IFCHR` and `stat.S_IFBLK`,
    *device* defines the newly created device special file (probably using
    [`os.makedev()`](#os.makedev "os.makedev")), otherwise it is ignored.

    This function can also support [paths relative to directory descriptors](#dir-fd).

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.major(*device*, */*)[¶](#os.major "Link to this definition")
:   Extract the device major number from a raw device number (usually the
    `st_dev` or `st_rdev` field from `stat`).

os.minor(*device*, */*)[¶](#os.minor "Link to this definition")
:   Extract the device minor number from a raw device number (usually the
    `st_dev` or `st_rdev` field from `stat`).

os.makedev(*major*, *minor*, */*)[¶](#os.makedev "Link to this definition")
:   Compose a raw device number from the major and minor device numbers.

os.pathconf(*path*, *name*)[¶](#os.pathconf "Link to this definition")
:   Return system configuration information relevant to a named file. *name*
    specifies the configuration value to retrieve; it may be a string which is the
    name of a defined system value; these names are specified in a number of
    standards (POSIX.1, Unix 95, Unix 98, and others). Some platforms define
    additional names as well. The names known to the host operating system are
    given in the `pathconf_names` dictionary. For configuration variables not
    included in that mapping, passing an integer for *name* is also accepted.

    If *name* is a string and is not known, [`ValueError`](exceptions.html#ValueError "ValueError") is raised. If a
    specific value for *name* is not supported by the host system, even if it is
    included in `pathconf_names`, an [`OSError`](exceptions.html#OSError "OSError") is raised with
    [`errno.EINVAL`](errno.html#errno.EINVAL "errno.EINVAL") for the error number.

    This function can support [specifying a file descriptor](#path-fd).

    [Availability](intro.html#availability): Unix.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.pathconf\_names[¶](#os.pathconf_names "Link to this definition")
:   Dictionary mapping names accepted by [`pathconf()`](#os.pathconf "os.pathconf") and [`fpathconf()`](#os.fpathconf "os.fpathconf") to
    the integer values defined for those names by the host operating system. This
    can be used to determine the set of names known to the system.

    [Availability](intro.html#availability): Unix.

os.readlink(*path*, *\**, *dir\_fd=None*)[¶](#os.readlink "Link to this definition")
:   Return a string representing the path to which the symbolic link points. The
    result may be either an absolute or relative pathname; if it is relative, it
    may be converted to an absolute pathname using
    `os.path.join(os.path.dirname(path), result)`.

    If the *path* is a string object (directly or indirectly through a
    [`PathLike`](#os.PathLike "os.PathLike") interface), the result will also be a string object,
    and the call may raise a UnicodeDecodeError. If the *path* is a bytes
    object (direct or indirectly), the result will be a bytes object.

    This function can also support [paths relative to directory descriptors](#dir-fd).

    When trying to resolve a path that may contain links, use
    [`realpath()`](os.path.html#os.path.realpath "os.path.realpath") to properly handle recursion and platform
    differences.

    [Availability](intro.html#availability): Unix, Windows.

    Changed in version 3.2: Added support for Windows 6.0 (Vista) symbolic links.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) on Unix.

    Changed in version 3.8: Accepts a [path-like object](../glossary.html#term-path-like-object) and a bytes object on Windows.

    Added support for directory junctions, and changed to return the
    substitution path (which typically includes `\\?\` prefix) rather
    than the optional “print name” field that was previously returned.

os.remove(*path*, *\**, *dir\_fd=None*)[¶](#os.remove "Link to this definition")
:   Remove (delete) the file *path*. If *path* is a directory, an
    [`OSError`](exceptions.html#OSError "OSError") is raised. Use [`rmdir()`](#os.rmdir "os.rmdir") to remove directories.
    If the file does not exist, a [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") is raised.

    This function can support [paths relative to directory descriptors](#dir-fd).

    On Windows, attempting to remove a file that is in use causes an exception to
    be raised; on Unix, the directory entry is removed but the storage allocated
    to the file is not made available until the original file is no longer in use.

    This function is semantically identical to [`unlink()`](#os.unlink "os.unlink").

    Raises an [auditing event](sys.html#auditing) `os.remove` with arguments `path`, `dir_fd`.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.removedirs(*name*)[¶](#os.removedirs "Link to this definition")
:   Remove directories recursively. Works like [`rmdir()`](#os.rmdir "os.rmdir") except that, if the
    leaf directory is successfully removed, [`removedirs()`](#os.removedirs "os.removedirs") tries to
    successively remove every parent directory mentioned in *path* until an error
    is raised (which is ignored, because it generally means that a parent directory
    is not empty). For example, `os.removedirs('foo/bar/baz')` will first remove
    the directory `'foo/bar/baz'`, and then remove `'foo/bar'` and `'foo'` if
    they are empty. Raises [`OSError`](exceptions.html#OSError "OSError") if the leaf directory could not be
    successfully removed.

    Raises an [auditing event](sys.html#auditing) `os.remove` with arguments `path`, `dir_fd`.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.rename(*src*, *dst*, *\**, *src\_dir\_fd=None*, *dst\_dir\_fd=None*)[¶](#os.rename "Link to this definition")
:   Rename the file or directory *src* to *dst*. If *dst* exists, the operation
    will fail with an [`OSError`](exceptions.html#OSError "OSError") subclass in a number of cases:

    On Windows, if *dst* exists a [`FileExistsError`](exceptions.html#FileExistsError "FileExistsError") is always raised.
    The operation may fail if *src* and *dst* are on different filesystems. Use
    [`shutil.move()`](shutil.html#shutil.move "shutil.move") to support moves to a different filesystem.

    On Unix, if *src* is a file and *dst* is a directory or vice-versa, an
    [`IsADirectoryError`](exceptions.html#IsADirectoryError "IsADirectoryError") or a [`NotADirectoryError`](exceptions.html#NotADirectoryError "NotADirectoryError") will be raised
    respectively. If both are directories and *dst* is empty, *dst* will be
    silently replaced. If *dst* is a non-empty directory, an [`OSError`](exceptions.html#OSError "OSError")
    is raised. If both are files, *dst* will be replaced silently if the user
    has permission. The operation may fail on some Unix flavors if *src* and
    *dst* are on different filesystems. If successful, the renaming will be an
    atomic operation (this is a POSIX requirement).

    This function can support specifying *src\_dir\_fd* and/or *dst\_dir\_fd* to
    supply [paths relative to directory descriptors](#dir-fd).

    If you want cross-platform overwriting of the destination, use [`replace()`](#os.replace "os.replace").

    Raises an [auditing event](sys.html#auditing) `os.rename` with arguments `src`, `dst`, `src_dir_fd`, `dst_dir_fd`.

    Changed in version 3.3: Added the *src\_dir\_fd* and *dst\_dir\_fd* parameters.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *src* and *dst*.

os.renames(*old*, *new*)[¶](#os.renames "Link to this definition")
:   Recursive directory or file renaming function. Works like [`rename()`](#os.rename "os.rename"), except
    creation of any intermediate directories needed to make the new pathname good is
    attempted first. After the rename, directories corresponding to rightmost path
    segments of the old name will be pruned away using [`removedirs()`](#os.removedirs "os.removedirs").

    Note

    This function can fail with the new directory structure made if you lack
    permissions needed to remove the leaf directory or file.

    Raises an [auditing event](sys.html#auditing) `os.rename` with arguments `src`, `dst`, `src_dir_fd`, `dst_dir_fd`.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *old* and *new*.

os.replace(*src*, *dst*, *\**, *src\_dir\_fd=None*, *dst\_dir\_fd=None*)[¶](#os.replace "Link to this definition")
:   Rename the file or directory *src* to *dst*. If *dst* is a non-empty directory,
    [`OSError`](exceptions.html#OSError "OSError") will be raised. If *dst* exists and is a file, it will
    be replaced silently if the user has permission. The operation may fail
    if *src* and *dst* are on different filesystems. If successful,
    the renaming will be an atomic operation (this is a POSIX requirement).

    This function can support specifying *src\_dir\_fd* and/or *dst\_dir\_fd* to
    supply [paths relative to directory descriptors](#dir-fd).

    Raises an [auditing event](sys.html#auditing) `os.rename` with arguments `src`, `dst`, `src_dir_fd`, `dst_dir_fd`.

    Added in version 3.3.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *src* and *dst*.

os.rmdir(*path*, *\**, *dir\_fd=None*)[¶](#os.rmdir "Link to this definition")
:   Remove (delete) the directory *path*. If the directory does not exist or is
    not empty, a [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") or an [`OSError`](exceptions.html#OSError "OSError") is raised
    respectively. In order to remove whole directory trees,
    [`shutil.rmtree()`](shutil.html#shutil.rmtree "shutil.rmtree") can be used.

    This function can support [paths relative to directory descriptors](#dir-fd).

    Raises an [auditing event](sys.html#auditing) `os.rmdir` with arguments `path`, `dir_fd`.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.scandir(*path='.'*)[¶](#os.scandir "Link to this definition")
:   Return an iterator of [`os.DirEntry`](#os.DirEntry "os.DirEntry") objects corresponding to the
    entries in the directory given by *path*. The entries are yielded in
    arbitrary order, and the special entries `'.'` and `'..'` are not
    included. If a file is removed from or added to the directory after
    creating the iterator, whether an entry for that file be included is
    unspecified.

    Using [`scandir()`](#os.scandir "os.scandir") instead of [`listdir()`](#os.listdir "os.listdir") can significantly
    increase the performance of code that also needs file type or file
    attribute information, because [`os.DirEntry`](#os.DirEntry "os.DirEntry") objects expose this
    information if the operating system provides it when scanning a directory.
    All [`os.DirEntry`](#os.DirEntry "os.DirEntry") methods may perform a system call, but
    [`is_dir()`](#os.DirEntry.is_dir "os.DirEntry.is_dir") and [`is_file()`](#os.DirEntry.is_file "os.DirEntry.is_file") usually only
    require a system call for symbolic links; [`os.DirEntry.stat()`](#os.DirEntry.stat "os.DirEntry.stat")
    always requires a system call on Unix but only requires one for
    symbolic links on Windows.

    *path* may be a [path-like object](../glossary.html#term-path-like-object). If *path* is of type `bytes`
    (directly or indirectly through the [`PathLike`](#os.PathLike "os.PathLike") interface),
    the type of the [`name`](#os.DirEntry.name "os.DirEntry.name") and [`path`](#os.DirEntry.path "os.DirEntry.path")
    attributes of each [`os.DirEntry`](#os.DirEntry "os.DirEntry") will be `bytes`; in all other
    circumstances, they will be of type `str`.

    This function can also support [specifying a file descriptor](#path-fd); the file descriptor must refer to a directory.

    Raises an [auditing event](sys.html#auditing) `os.scandir` with argument `path`.

    The [`scandir()`](#os.scandir "os.scandir") iterator supports the [context manager](../glossary.html#term-context-manager) protocol
    and has the following method:

    scandir.close()[¶](#os.scandir.close "Link to this definition")
    :   Close the iterator and free acquired resources.

        This is called automatically when the iterator is exhausted or garbage
        collected, or when an error happens during iterating. However it
        is advisable to call it explicitly or use the [`with`](../reference/compound_stmts.html#with)
        statement.

        Added in version 3.6.

    The following example shows a simple use of [`scandir()`](#os.scandir "os.scandir") to display all
    the files (excluding directories) in the given *path* that don’t start with
    `'.'`. The `entry.is_file()` call will generally not make an additional
    system call:

    ```
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                print(entry.name)
    ```

    Note

    On Unix-based systems, [`scandir()`](#os.scandir "os.scandir") uses the system’s
    [opendir()](https://pubs.opengroup.org/onlinepubs/009695399/functions/opendir.html)
    and
    [readdir()](https://pubs.opengroup.org/onlinepubs/009695399/functions/readdir_r.html)
    functions. On Windows, it uses the Win32
    [FindFirstFileW](https://msdn.microsoft.com/en-us/library/windows/desktop/aa364418(v=vs.85).aspx)
    and
    [FindNextFileW](https://msdn.microsoft.com/en-us/library/windows/desktop/aa364428(v=vs.85).aspx)
    functions.

    Added in version 3.5.

    Changed in version 3.6: Added support for the [context manager](../glossary.html#term-context-manager) protocol and the
    [`close()`](#os.scandir.close "os.scandir.close") method. If a [`scandir()`](#os.scandir "os.scandir") iterator is neither
    exhausted nor explicitly closed a [`ResourceWarning`](exceptions.html#ResourceWarning "ResourceWarning") will be emitted
    in its destructor.

    The function accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.7: Added support for [file descriptors](#path-fd) on Unix.

*class* os.DirEntry[¶](#os.DirEntry "Link to this definition")
:   Object yielded by [`scandir()`](#os.scandir "os.scandir") to expose the file path and other file
    attributes of a directory entry.

    [`scandir()`](#os.scandir "os.scandir") will provide as much of this information as possible without
    making additional system calls. When a `stat()` or `lstat()` system call
    is made, the `os.DirEntry` object will cache the result.

    `os.DirEntry` instances are not intended to be stored in long-lived data
    structures; if you know the file metadata has changed or if a long time has
    elapsed since calling [`scandir()`](#os.scandir "os.scandir"), call `os.stat(entry.path)` to fetch
    up-to-date information.

    Because the `os.DirEntry` methods can make operating system calls, they may
    also raise [`OSError`](exceptions.html#OSError "OSError"). If you need very fine-grained
    control over errors, you can catch [`OSError`](exceptions.html#OSError "OSError") when calling one of the
    `os.DirEntry` methods and handle as appropriate.

    To be directly usable as a [path-like object](../glossary.html#term-path-like-object), `os.DirEntry`
    implements the [`PathLike`](#os.PathLike "os.PathLike") interface.

    Attributes and methods on a `os.DirEntry` instance are as follows:

    name[¶](#os.DirEntry.name "Link to this definition")
    :   The entry’s base filename, relative to the [`scandir()`](#os.scandir "os.scandir") *path*
        argument.

        The [`name`](#os.name "os.name") attribute will be `bytes` if the [`scandir()`](#os.scandir "os.scandir")
        *path* argument is of type `bytes` and `str` otherwise. Use
        [`fsdecode()`](#os.fsdecode "os.fsdecode") to decode byte filenames.

    path[¶](#os.DirEntry.path "Link to this definition")
    :   The entry’s full path name: equivalent to `os.path.join(scandir_path,
        entry.name)` where *scandir\_path* is the [`scandir()`](#os.scandir "os.scandir") *path*
        argument. The path is only absolute if the [`scandir()`](#os.scandir "os.scandir") *path*
        argument was absolute. If the [`scandir()`](#os.scandir "os.scandir") *path*
        argument was a [file descriptor](#path-fd), the [`path`](os.path.html#module-os.path "os.path: Operations on pathnames.")
        attribute is the same as the [`name`](#os.name "os.name") attribute.

        The [`path`](os.path.html#module-os.path "os.path: Operations on pathnames.") attribute will be `bytes` if the [`scandir()`](#os.scandir "os.scandir")
        *path* argument is of type `bytes` and `str` otherwise. Use
        [`fsdecode()`](#os.fsdecode "os.fsdecode") to decode byte filenames.

    inode()[¶](#os.DirEntry.inode "Link to this definition")
    :   Return the inode number of the entry.

        The result is cached on the `os.DirEntry` object. Use
        `os.stat(entry.path, follow_symlinks=False).st_ino` to fetch up-to-date
        information.

        On the first, uncached call, a system call is required on Windows but
        not on Unix.

    is\_dir(*\**, *follow\_symlinks=True*)[¶](#os.DirEntry.is_dir "Link to this definition")
    :   Return `True` if this entry is a directory or a symbolic link pointing
        to a directory; return `False` if the entry is or points to any other
        kind of file, or if it doesn’t exist anymore.

        If *follow\_symlinks* is `False`, return `True` only if this entry
        is a directory (without following symlinks); return `False` if the
        entry is any other kind of file or if it doesn’t exist anymore.

        The result is cached on the `os.DirEntry` object, with a separate cache
        for *follow\_symlinks* `True` and `False`. Call [`os.stat()`](#os.stat "os.stat") along
        with [`stat.S_ISDIR()`](stat.html#stat.S_ISDIR "stat.S_ISDIR") to fetch up-to-date information.

        On the first, uncached call, no system call is required in most cases.
        Specifically, for non-symlinks, neither Windows or Unix require a system
        call, except on certain Unix file systems, such as network file systems,
        that return `dirent.d_type == DT_UNKNOWN`. If the entry is a symlink,
        a system call will be required to follow the symlink unless
        *follow\_symlinks* is `False`.

        This method can raise [`OSError`](exceptions.html#OSError "OSError"), such as [`PermissionError`](exceptions.html#PermissionError "PermissionError"),
        but [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") is caught and not raised.

    is\_file(*\**, *follow\_symlinks=True*)[¶](#os.DirEntry.is_file "Link to this definition")
    :   Return `True` if this entry is a file or a symbolic link pointing to a
        file; return `False` if the entry is or points to a directory or other
        non-file entry, or if it doesn’t exist anymore.

        If *follow\_symlinks* is `False`, return `True` only if this entry
        is a file (without following symlinks); return `False` if the entry is
        a directory or other non-file entry, or if it doesn’t exist anymore.

        The result is cached on the `os.DirEntry` object. Caching, system calls
        made, and exceptions raised are as per [`is_dir()`](#os.DirEntry.is_dir "os.DirEntry.is_dir").

    is\_symlink()[¶](#os.DirEntry.is_symlink "Link to this definition")
    :   Return `True` if this entry is a symbolic link (even if broken);
        return `False` if the entry points to a directory or any kind of file,
        or if it doesn’t exist anymore.

        The result is cached on the `os.DirEntry` object. Call
        [`os.path.islink()`](os.path.html#os.path.islink "os.path.islink") to fetch up-to-date information.

        On the first, uncached call, no system call is required in most cases.
        Specifically, neither Windows or Unix require a system call, except on
        certain Unix file systems, such as network file systems, that return
        `dirent.d_type == DT_UNKNOWN`.

        This method can raise [`OSError`](exceptions.html#OSError "OSError"), such as [`PermissionError`](exceptions.html#PermissionError "PermissionError"),
        but [`FileNotFoundError`](exceptions.html#FileNotFoundError "FileNotFoundError") is caught and not raised.

    is\_junction()[¶](#os.DirEntry.is_junction "Link to this definition")
    :   Return `True` if this entry is a junction (even if broken);
        return `False` if the entry points to a regular directory, any kind
        of file, a symlink, or if it doesn’t exist anymore.

        The result is cached on the `os.DirEntry` object. Call
        [`os.path.isjunction()`](os.path.html#os.path.isjunction "os.path.isjunction") to fetch up-to-date information.

        Added in version 3.12.

    stat(*\**, *follow\_symlinks=True*)[¶](#os.DirEntry.stat "Link to this definition")
    :   Return a [`stat_result`](#os.stat_result "os.stat_result") object for this entry. This method
        follows symbolic links by default; to stat a symbolic link add the
        `follow_symlinks=False` argument.

        On Unix, this method always requires a system call. On Windows, it
        only requires a system call if *follow\_symlinks* is `True` and the
        entry is a reparse point (for example, a symbolic link or directory
        junction).

        On Windows, the `st_ino`, `st_dev` and `st_nlink` attributes of the
        [`stat_result`](#os.stat_result "os.stat_result") are always set to zero. Call [`os.stat()`](#os.stat "os.stat") to
        get these attributes.

        The result is cached on the `os.DirEntry` object, with a separate cache
        for *follow\_symlinks* `True` and `False`. Call [`os.stat()`](#os.stat "os.stat") to
        fetch up-to-date information.

    Note that there is a nice correspondence between several attributes
    and methods of `os.DirEntry` and of [`pathlib.Path`](pathlib.html#pathlib.Path "pathlib.Path"). In
    particular, the `name` attribute has the same
    meaning, as do the `is_dir()`, `is_file()`, `is_symlink()`,
    `is_junction()`, and `stat()` methods.

    Added in version 3.5.

    Changed in version 3.6: Added support for the [`PathLike`](#os.PathLike "os.PathLike") interface. Added support
    for [`bytes`](stdtypes.html#bytes "bytes") paths on Windows.

    Changed in version 3.12: The `st_ctime` attribute of a stat result is deprecated on Windows.
    The file creation time is properly available as `st_birthtime`, and
    in the future `st_ctime` may be changed to return zero or the
    metadata change time, if available.

os.stat(*path*, *\**, *dir\_fd=None*, *follow\_symlinks=True*)[¶](#os.stat "Link to this definition")
:   Get the status of a file or a file descriptor. Perform the equivalent of a
    `stat()` system call on the given path. *path* may be specified as
    either a string or bytes – directly or indirectly through the [`PathLike`](#os.PathLike "os.PathLike")
    interface – or as an open file descriptor. Return a [`stat_result`](#os.stat_result "os.stat_result")
    object.

    This function normally follows symlinks; to stat a symlink add the argument
    `follow_symlinks=False`, or use [`lstat()`](#os.lstat "os.lstat").

    This function can support [specifying a file descriptor](#path-fd) and
    [not following symlinks](#follow-symlinks).

    On Windows, passing `follow_symlinks=False` will disable following all
    name-surrogate reparse points, which includes symlinks and directory
    junctions. Other types of reparse points that do not resemble links or that
    the operating system is unable to follow will be opened directly. When
    following a chain of multiple links, this may result in the original link
    being returned instead of the non-link that prevented full traversal. To
    obtain stat results for the final path in this case, use the
    [`os.path.realpath()`](os.path.html#os.path.realpath "os.path.realpath") function to resolve the path name as far as
    possible and call [`lstat()`](#os.lstat "os.lstat") on the result. This does not apply to
    dangling symlinks or junction points, which will raise the usual exceptions.

    Example:

    ```
    >>> import os
    >>> statinfo = os.stat('somefile.txt')
    >>> statinfo
    os.stat_result(st_mode=33188, st_ino=7876932, st_dev=234881026,
    st_nlink=1, st_uid=501, st_gid=501, st_size=264, st_atime=1297230295,
    st_mtime=1297230027, st_ctime=1297230027)
    >>> statinfo.st_size
    264
    ```

    See also

    [`fstat()`](#os.fstat "os.fstat") and [`lstat()`](#os.lstat "os.lstat") functions.

    Changed in version 3.3: Added the *dir\_fd* and *follow\_symlinks* parameters,
    specifying a file descriptor instead of a path.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.8: On Windows, all reparse points that can be resolved by the operating
    system are now followed, and passing `follow_symlinks=False`
    disables following all name surrogate reparse points. If the operating
    system reaches a reparse point that it is not able to follow, *stat* now
    returns the information for the original path as if
    `follow_symlinks=False` had been specified instead of raising an error.

*class* os.stat\_result[¶](#os.stat_result "Link to this definition")
:   Object whose attributes correspond roughly to the members of the
    `stat` structure. It is used for the result of [`os.stat()`](#os.stat "os.stat"),
    [`os.fstat()`](#os.fstat "os.fstat") and [`os.lstat()`](#os.lstat "os.lstat").

    Attributes:

    st\_mode[¶](#os.stat_result.st_mode "Link to this definition")
    :   File mode: file type and file mode bits (permissions).

    st\_ino[¶](#os.stat_result.st_ino "Link to this definition")
    :   Platform dependent, but if non-zero, uniquely identifies the
        file for a given value of `st_dev`. Typically:

        * the inode number on Unix,
        * the [file index](https://msdn.microsoft.com/en-us/library/aa363788) on
          Windows

    st\_dev[¶](#os.stat_result.st_dev "Link to this definition")
    :   Identifier of the device on which this file resides.

    st\_nlink[¶](#os.stat_result.st_nlink "Link to this definition")
    :   Number of hard links.

    st\_uid[¶](#os.stat_result.st_uid "Link to this definition")
    :   User identifier of the file owner.

    st\_gid[¶](#os.stat_result.st_gid "Link to this definition")
    :   Group identifier of the file owner.

    st\_size[¶](#os.stat_result.st_size "Link to this definition")
    :   Size of the file in bytes, if it is a regular file or a symbolic link.
        The size of a symbolic link is the length of the pathname it contains,
        without a terminating null byte.

    Timestamps:

    st\_atime[¶](#os.stat_result.st_atime "Link to this definition")
    :   Time of most recent access expressed in seconds.

    st\_mtime[¶](#os.stat_result.st_mtime "Link to this definition")
    :   Time of most recent content modification expressed in seconds.

    st\_ctime[¶](#os.stat_result.st_ctime "Link to this definition")
    :   Time of most recent metadata change expressed in seconds.

        Changed in version 3.12: `st_ctime` is deprecated on Windows. Use `st_birthtime` for
        the file creation time. In the future, `st_ctime` will contain
        the time of the most recent metadata change, as for other platforms.

    st\_atime\_ns[¶](#os.stat_result.st_atime_ns "Link to this definition")
    :   Time of most recent access expressed in nanoseconds as an integer.

        Added in version 3.3.

    st\_mtime\_ns[¶](#os.stat_result.st_mtime_ns "Link to this definition")
    :   Time of most recent content modification expressed in nanoseconds as an
        integer.

        Added in version 3.3.

    st\_ctime\_ns[¶](#os.stat_result.st_ctime_ns "Link to this definition")
    :   Time of most recent metadata change expressed in nanoseconds as an
        integer.

        Added in version 3.3.

        Changed in version 3.12: `st_ctime_ns` is deprecated on Windows. Use `st_birthtime_ns`
        for the file creation time. In the future, `st_ctime` will contain
        the time of the most recent metadata change, as for other platforms.

    st\_birthtime[¶](#os.stat_result.st_birthtime "Link to this definition")
    :   Time of file creation expressed in seconds. This attribute is not
        always available, and may raise [`AttributeError`](exceptions.html#AttributeError "AttributeError").

        Changed in version 3.12: `st_birthtime` is now available on Windows.

    st\_birthtime\_ns[¶](#os.stat_result.st_birthtime_ns "Link to this definition")
    :   Time of file creation expressed in nanoseconds as an integer.
        This attribute is not always available, and may raise
        [`AttributeError`](exceptions.html#AttributeError "AttributeError").

        Added in version 3.12.

    Note

    The exact meaning and resolution of the [`st_atime`](#os.stat_result.st_atime "os.stat_result.st_atime"),
    [`st_mtime`](#os.stat_result.st_mtime "os.stat_result.st_mtime"), [`st_ctime`](#os.stat_result.st_ctime "os.stat_result.st_ctime") and [`st_birthtime`](#os.stat_result.st_birthtime "os.stat_result.st_birthtime") attributes
    depend on the operating system and the file system. For example, on
    Windows systems using the FAT32 file systems, [`st_mtime`](#os.stat_result.st_mtime "os.stat_result.st_mtime") has
    2-second resolution, and [`st_atime`](#os.stat_result.st_atime "os.stat_result.st_atime") has only 1-day resolution.
    See your operating system documentation for details.

    Similarly, although [`st_atime_ns`](#os.stat_result.st_atime_ns "os.stat_result.st_atime_ns"), [`st_mtime_ns`](#os.stat_result.st_mtime_ns "os.stat_result.st_mtime_ns"),
    [`st_ctime_ns`](#os.stat_result.st_ctime_ns "os.stat_result.st_ctime_ns") and [`st_birthtime_ns`](#os.stat_result.st_birthtime_ns "os.stat_result.st_birthtime_ns") are always expressed in
    nanoseconds, many systems do not provide nanosecond precision. On
    systems that do provide nanosecond precision, the floating-point object
    used to store [`st_atime`](#os.stat_result.st_atime "os.stat_result.st_atime"), [`st_mtime`](#os.stat_result.st_mtime "os.stat_result.st_mtime"), [`st_ctime`](#os.stat_result.st_ctime "os.stat_result.st_ctime") and
    [`st_birthtime`](#os.stat_result.st_birthtime "os.stat_result.st_birthtime") cannot preserve all of it, and as such will be
    slightly inexact. If you need the exact timestamps you should always use
    [`st_atime_ns`](#os.stat_result.st_atime_ns "os.stat_result.st_atime_ns"), [`st_mtime_ns`](#os.stat_result.st_mtime_ns "os.stat_result.st_mtime_ns"), [`st_ctime_ns`](#os.stat_result.st_ctime_ns "os.stat_result.st_ctime_ns") and
    [`st_birthtime_ns`](#os.stat_result.st_birthtime_ns "os.stat_result.st_birthtime_ns").

    On some Unix systems (such as Linux), the following attributes may also be
    available:

    st\_blocks[¶](#os.stat_result.st_blocks "Link to this definition")
    :   Number of 512-byte blocks allocated for file.
        This may be smaller than [`st_size`](#os.stat_result.st_size "os.stat_result.st_size")/512 when the file has holes.

    st\_blksize[¶](#os.stat_result.st_blksize "Link to this definition")
    :   “Preferred” blocksize for efficient file system I/O. Writing to a file in
        smaller chunks may cause an inefficient read-modify-rewrite.

    st\_rdev[¶](#os.stat_result.st_rdev "Link to this definition")
    :   Type of device if an inode device.

    st\_flags[¶](#os.stat_result.st_flags "Link to this definition")
    :   User defined flags for file.

    On other Unix systems (such as FreeBSD), the following attributes may be
    available (but may be only filled out if root tries to use them):

    st\_gen[¶](#os.stat_result.st_gen "Link to this definition")
    :   File generation number.

    On Solaris and derivatives, the following attributes may also be
    available:

    st\_fstype[¶](#os.stat_result.st_fstype "Link to this definition")
    :   String that uniquely identifies the type of the filesystem that
        contains the file.

    On macOS systems, the following attributes may also be available:

    st\_rsize[¶](#os.stat_result.st_rsize "Link to this definition")
    :   Real size of the file.

    st\_creator[¶](#os.stat_result.st_creator "Link to this definition")
    :   Creator of the file.

    st\_type[¶](#os.stat_result.st_type "Link to this definition")
    :   File type.

    On Windows systems, the following attributes are also available:

    st\_file\_attributes[¶](#os.stat_result.st_file_attributes "Link to this definition")
    :   Windows file attributes: `dwFileAttributes` member of the
        `BY_HANDLE_FILE_INFORMATION` structure returned by
        `GetFileInformationByHandle()`.
        See the `FILE_ATTRIBUTE_* <stat.FILE_ATTRIBUTE_ARCHIVE>`
        constants in the [`stat`](stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") module.

        Added in version 3.5.

    st\_reparse\_tag[¶](#os.stat_result.st_reparse_tag "Link to this definition")
    :   When [`st_file_attributes`](#os.stat_result.st_file_attributes "os.stat_result.st_file_attributes") has the [`FILE_ATTRIBUTE_REPARSE_POINT`](stat.html#stat.FILE_ATTRIBUTE_REPARSE_POINT "stat.FILE_ATTRIBUTE_REPARSE_POINT")
        set, this field contains the tag identifying the type of reparse point.
        See the [`IO_REPARSE_TAG_*`](stat.html#stat.IO_REPARSE_TAG_SYMLINK "stat.IO_REPARSE_TAG_SYMLINK")
        constants in the [`stat`](stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") module.

    The standard module [`stat`](stat.html#module-stat "stat: Utilities for interpreting the results of os.stat(), os.lstat() and os.fstat().") defines functions and constants that are
    useful for extracting information from a `stat` structure. (On
    Windows, some items are filled with dummy values.)

    For backward compatibility, a [`stat_result`](#os.stat_result "os.stat_result") instance is also
    accessible as a tuple of at least 10 integers giving the most important (and
    portable) members of the `stat` structure, in the order
    [`st_mode`](#os.stat_result.st_mode "os.stat_result.st_mode"), [`st_ino`](#os.stat_result.st_ino "os.stat_result.st_ino"), [`st_dev`](#os.stat_result.st_dev "os.stat_result.st_dev"), [`st_nlink`](#os.stat_result.st_nlink "os.stat_result.st_nlink"),
    [`st_uid`](#os.stat_result.st_uid "os.stat_result.st_uid"), [`st_gid`](#os.stat_result.st_gid "os.stat_result.st_gid"), [`st_size`](#os.stat_result.st_size "os.stat_result.st_size"), [`st_atime`](#os.stat_result.st_atime "os.stat_result.st_atime"),
    [`st_mtime`](#os.stat_result.st_mtime "os.stat_result.st_mtime"), [`st_ctime`](#os.stat_result.st_ctime "os.stat_result.st_ctime"). More items may be added at the end by
    some implementations. For compatibility with older Python versions,
    accessing [`stat_result`](#os.stat_result "os.stat_result") as a tuple always returns integers.

    Changed in version 3.5: Windows now returns the file index as [`st_ino`](#os.stat_result.st_ino "os.stat_result.st_ino") when
    available.

    Changed in version 3.7: Added the [`st_fstype`](#os.stat_result.st_fstype "os.stat_result.st_fstype") member to Solaris/derivatives.

    Changed in version 3.8: Added the [`st_reparse_tag`](#os.stat_result.st_reparse_tag "os.stat_result.st_reparse_tag") member on Windows.

    Changed in version 3.8: On Windows, the [`st_mode`](#os.stat_result.st_mode "os.stat_result.st_mode") member now identifies special
    files as `S_IFCHR`, `S_IFIFO` or `S_IFBLK`
    as appropriate.

    Changed in version 3.12: On Windows, [`st_ctime`](#os.stat_result.st_ctime "os.stat_result.st_ctime") is deprecated. Eventually, it will
    contain the last metadata change time, for consistency with other
    platforms, but for now still contains creation time.
    Use [`st_birthtime`](#os.stat_result.st_birthtime "os.stat_result.st_birthtime") for the creation time.

    On Windows, [`st_ino`](#os.stat_result.st_ino "os.stat_result.st_ino") may now be up to 128 bits, depending
    on the file system. Previously it would not be above 64 bits, and
    larger file identifiers would be arbitrarily packed.

    On Windows, [`st_rdev`](#os.stat_result.st_rdev "os.stat_result.st_rdev") no longer returns a value. Previously
    it would contain the same as [`st_dev`](#os.stat_result.st_dev "os.stat_result.st_dev"), which was incorrect.

    Added the [`st_birthtime`](#os.stat_result.st_birthtime "os.stat_result.st_birthtime") member on Windows.

os.statvfs(*path*)[¶](#os.statvfs "Link to this definition")
:   Perform a `statvfs()` system call on the given path. The return value is
    an object whose attributes describe the filesystem on the given path, and
    correspond to the members of the `statvfs` structure, namely:
    `f_bsize`, `f_frsize`, `f_blocks`, `f_bfree`,
    `f_bavail`, `f_files`, `f_ffree`, `f_favail`,
    `f_flag`, `f_namemax`, `f_fsid`.

    Two module-level constants are defined for the `f_flag` attribute’s
    bit-flags: if `ST_RDONLY` is set, the filesystem is mounted
    read-only, and if `ST_NOSUID` is set, the semantics of
    setuid/setgid bits are disabled or not supported.

    Additional module-level constants are defined for GNU/glibc based systems.
    These are `ST_NODEV` (disallow access to device special files),
    `ST_NOEXEC` (disallow program execution), `ST_SYNCHRONOUS`
    (writes are synced at once), `ST_MANDLOCK` (allow mandatory locks on an FS),
    `ST_WRITE` (write on file/directory/symlink), `ST_APPEND`
    (append-only file), `ST_IMMUTABLE` (immutable file), `ST_NOATIME`
    (do not update access times), `ST_NODIRATIME` (do not update directory access
    times), `ST_RELATIME` (update atime relative to mtime/ctime).

    This function can support [specifying a file descriptor](#path-fd).

    [Availability](intro.html#availability): Unix.

    Changed in version 3.2: The `ST_RDONLY` and `ST_NOSUID` constants were added.

    Changed in version 3.3: Added support for specifying *path* as an open file descriptor.

    Changed in version 3.4: The `ST_NODEV`, `ST_NOEXEC`, `ST_SYNCHRONOUS`,
    `ST_MANDLOCK`, `ST_WRITE`, `ST_APPEND`,
    `ST_IMMUTABLE`, `ST_NOATIME`, `ST_NODIRATIME`,
    and `ST_RELATIME` constants were added.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.7: Added the `f_fsid` attribute.

os.supports\_dir\_fd[¶](#os.supports_dir_fd "Link to this definition")
:   A [`set`](stdtypes.html#set "set") object indicating which functions in the [`os`](#module-os "os: Miscellaneous operating system interfaces.")
    module accept an open file descriptor for their *dir\_fd* parameter.
    Different platforms provide different features, and the underlying
    functionality Python uses to implement the *dir\_fd* parameter is not
    available on all platforms Python supports. For consistency’s sake,
    functions that may support *dir\_fd* always allow specifying the
    parameter, but will throw an exception if the functionality is used
    when it’s not locally available. (Specifying `None` for *dir\_fd*
    is always supported on all platforms.)

    To check whether a particular function accepts an open file descriptor
    for its *dir\_fd* parameter, use the `in` operator on `supports_dir_fd`.
    As an example, this expression evaluates to `True` if [`os.stat()`](#os.stat "os.stat")
    accepts open file descriptors for *dir\_fd* on the local platform:

    ```
    os.stat in os.supports_dir_fd
    ```

    Currently *dir\_fd* parameters only work on Unix platforms;
    none of them work on Windows.

    Added in version 3.3.

os.supports\_effective\_ids[¶](#os.supports_effective_ids "Link to this definition")
:   A [`set`](stdtypes.html#set "set") object indicating whether [`os.access()`](#os.access "os.access") permits
    specifying `True` for its *effective\_ids* parameter on the local platform.
    (Specifying `False` for *effective\_ids* is always supported on all
    platforms.) If the local platform supports it, the collection will contain
    [`os.access()`](#os.access "os.access"); otherwise it will be empty.

    This expression evaluates to `True` if [`os.access()`](#os.access "os.access") supports
    `effective_ids=True` on the local platform:

    ```
    os.access in os.supports_effective_ids
    ```

    Currently *effective\_ids* is only supported on Unix platforms;
    it does not work on Windows.

    Added in version 3.3.

os.supports\_fd[¶](#os.supports_fd "Link to this definition")
:   A [`set`](stdtypes.html#set "set") object indicating which functions in the
    [`os`](#module-os "os: Miscellaneous operating system interfaces.") module permit specifying their *path* parameter as an open file
    descriptor on the local platform. Different platforms provide different
    features, and the underlying functionality Python uses to accept open file
    descriptors as *path* arguments is not available on all platforms Python
    supports.

    To determine whether a particular function permits specifying an open file
    descriptor for its *path* parameter, use the `in` operator on
    `supports_fd`. As an example, this expression evaluates to `True` if
    [`os.chdir()`](#os.chdir "os.chdir") accepts open file descriptors for *path* on your local
    platform:

    ```
    os.chdir in os.supports_fd
    ```

    Added in version 3.3.

os.supports\_follow\_symlinks[¶](#os.supports_follow_symlinks "Link to this definition")
:   A [`set`](stdtypes.html#set "set") object indicating which functions in the [`os`](#module-os "os: Miscellaneous operating system interfaces.") module
    accept `False` for their *follow\_symlinks* parameter on the local platform.
    Different platforms provide different features, and the underlying
    functionality Python uses to implement *follow\_symlinks* is not available
    on all platforms Python supports. For consistency’s sake, functions that
    may support *follow\_symlinks* always allow specifying the parameter, but
    will throw an exception if the functionality is used when it’s not locally
    available. (Specifying `True` for *follow\_symlinks* is always supported
    on all platforms.)

    To check whether a particular function accepts `False` for its
    *follow\_symlinks* parameter, use the `in` operator on
    `supports_follow_symlinks`. As an example, this expression evaluates
    to `True` if you may specify `follow_symlinks=False` when calling
    [`os.stat()`](#os.stat "os.stat") on the local platform:

    ```
    os.stat in os.supports_follow_symlinks
    ```

    Added in version 3.3.

os.symlink(*src*, *dst*, *target\_is\_directory=False*, *\**, *dir\_fd=None*)[¶](#os.symlink "Link to this definition")
:   Create a symbolic link pointing to *src* named *dst*.

    On Windows, a symlink represents either a file or a directory, and does not
    morph to the target dynamically. If the target is present, the type of the
    symlink will be created to match. Otherwise, the symlink will be created
    as a directory if *target\_is\_directory* is `True` or a file symlink (the
    default) otherwise. On non-Windows platforms, *target\_is\_directory* is ignored.

    This function can support [paths relative to directory descriptors](#dir-fd).

    Note

    On newer versions of Windows 10, unprivileged accounts can create symlinks
    if Developer Mode is enabled. When Developer Mode is not available/enabled,
    the *SeCreateSymbolicLinkPrivilege* privilege is required, or the process
    must be run as an administrator.

    [`OSError`](exceptions.html#OSError "OSError") is raised when the function is called by an unprivileged
    user.

    Raises an [auditing event](sys.html#auditing) `os.symlink` with arguments `src`, `dst`, `dir_fd`.

    [Availability](intro.html#availability): Unix, Windows.

    The function is limited on Emscripten and WASI, see
    [WebAssembly platforms](intro.html#wasm-availability) for more information.

    Changed in version 3.2: Added support for Windows 6.0 (Vista) symbolic links.

    Changed in version 3.3: Added the *dir\_fd* parameter, and now allow *target\_is\_directory*
    on non-Windows platforms.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *src* and *dst*.

    Changed in version 3.8: Added support for unelevated symlinks on Windows with Developer Mode.

os.sync()[¶](#os.sync "Link to this definition")
:   Force write of everything to disk.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

os.truncate(*path*, *length*)[¶](#os.truncate "Link to this definition")
:   Truncate the file corresponding to *path*, so that it is at most
    *length* bytes in size.

    This function can support [specifying a file descriptor](#path-fd).

    Raises an [auditing event](sys.html#auditing) `os.truncate` with arguments `path`, `length`.

    [Availability](intro.html#availability): Unix, Windows.

    Added in version 3.3.

    Changed in version 3.5: Added support for Windows

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.unlink(*path*, *\**, *dir\_fd=None*)[¶](#os.unlink "Link to this definition")
:   Remove (delete) the file *path*. This function is semantically
    identical to [`remove()`](#os.remove "os.remove"); the `unlink` name is its
    traditional Unix name. Please see the documentation for
    [`remove()`](#os.remove "os.remove") for further information.

    Raises an [auditing event](sys.html#auditing) `os.remove` with arguments `path`, `dir_fd`.

    Changed in version 3.3: Added the *dir\_fd* parameter.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.utime(*path*, *times=None*, *\**, [*ns*, ]*dir\_fd=None*, *follow\_symlinks=True*)[¶](#os.utime "Link to this definition")
:   Set the access and modified times of the file specified by *path*.

    [`utime()`](#os.utime "os.utime") takes two optional parameters, *times* and *ns*.
    These specify the times set on *path* and are used as follows:

    * If *ns* is specified,
      it must be a 2-tuple of the form `(atime_ns, mtime_ns)`
      where each member is an int expressing nanoseconds.
    * If *times* is not `None`,
      it must be a 2-tuple of the form `(atime, mtime)`
      where each member is an int or float expressing seconds.
    * If *times* is `None` and *ns* is unspecified,
      this is equivalent to specifying `ns=(atime_ns, mtime_ns)`
      where both times are the current time.

    It is an error to specify tuples for both *times* and *ns*.

    Note that the exact times you set here may not be returned by a subsequent
    [`stat()`](#os.stat "os.stat") call, depending on the resolution with which your operating
    system records access and modification times; see [`stat()`](#os.stat "os.stat"). The best
    way to preserve exact times is to use the *st\_atime\_ns* and *st\_mtime\_ns*
    fields from the [`os.stat()`](#os.stat "os.stat") result object with the *ns* parameter to
    [`utime()`](#os.utime "os.utime").

    This function can support [specifying a file descriptor](#path-fd),
    [paths relative to directory descriptors](#dir-fd) and [not
    following symlinks](#follow-symlinks).

    Raises an [auditing event](sys.html#auditing) `os.utime` with arguments `path`, `times`, `ns`, `dir_fd`.

    Changed in version 3.3: Added support for specifying *path* as an open file descriptor,
    and the *dir\_fd*, *follow\_symlinks*, and *ns* parameters.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.walk(*top*, *topdown=True*, *onerror=None*, *followlinks=False*)[¶](#os.walk "Link to this definition")
:   Generate the file names in a directory tree by walking the tree
    either top-down or bottom-up. For each directory in the tree rooted at directory
    *top* (including *top* itself), it yields a 3-tuple `(dirpath, dirnames,
    filenames)`.

    *dirpath* is a string, the path to the directory. *dirnames* is a list of the
    names of the subdirectories in *dirpath* (including symlinks to directories,
    and excluding `'.'` and `'..'`).
    *filenames* is a list of the names of the non-directory files in *dirpath*.
    Note that the names in the lists contain no path components. To get a full path
    (which begins with *top*) to a file or directory in *dirpath*, do
    `os.path.join(dirpath, name)`. Whether or not the lists are sorted
    depends on the file system. If a file is removed from or added to the
    *dirpath* directory during generating the lists, whether a name for that
    file be included is unspecified.

    If optional argument *topdown* is `True` or not specified, the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are generated top-down). If *topdown* is `False`, the triple
    for a directory is generated after the triples for all of its subdirectories
    (directories are generated bottom-up). No matter the value of *topdown*, the
    list of subdirectories is retrieved before the tuples for the directory and
    its subdirectories are generated.

    When *topdown* is `True`, the caller can modify the *dirnames* list in-place
    (perhaps using [`del`](../reference/simple_stmts.html#del) or slice assignment), and [`walk()`](#os.walk "os.walk") will only
    recurse into the subdirectories whose names remain in *dirnames*; this can be
    used to prune the search, impose a specific order of visiting, or even to inform
    [`walk()`](#os.walk "os.walk") about directories the caller creates or renames before it resumes
    [`walk()`](#os.walk "os.walk") again. Modifying *dirnames* when *topdown* is `False` has
    no effect on the behavior of the walk, because in bottom-up mode the directories
    in *dirnames* are generated before *dirpath* itself is generated.

    By default, errors from the [`scandir()`](#os.scandir "os.scandir") call are ignored. If optional
    argument *onerror* is specified, it should be a function; it will be called with
    one argument, an [`OSError`](exceptions.html#OSError "OSError") instance. It can report the error to continue
    with the walk, or raise the exception to abort the walk. Note that the filename
    is available as the `filename` attribute of the exception object.

    By default, [`walk()`](#os.walk "os.walk") will not walk down into symbolic links that resolve to
    directories. Set *followlinks* to `True` to visit directories pointed to by
    symlinks, on systems that support them.

    Note

    Be aware that setting *followlinks* to `True` can lead to infinite
    recursion if a link points to a parent directory of itself. [`walk()`](#os.walk "os.walk")
    does not keep track of the directories it visited already.

    Note

    If you pass a relative pathname, don’t change the current working directory
    between resumptions of [`walk()`](#os.walk "os.walk"). [`walk()`](#os.walk "os.walk") never changes the current
    directory, and assumes that its caller doesn’t either.

    This example displays the number of bytes taken by non-directory files in each
    directory under the starting directory, except that it doesn’t look under any
    `__pycache__` subdirectory:

    ```
    import os
    from os.path import join, getsize
    for root, dirs, files in os.walk('python/Lib/xml'):
        print(root, "consumes", end=" ")
        print(sum(getsize(join(root, name)) for name in files), end=" ")
        print("bytes in", len(files), "non-directory files")
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')  # don't visit __pycache__ directories
    ```

    In the next example (simple implementation of [`shutil.rmtree()`](shutil.html#shutil.rmtree "shutil.rmtree")),
    walking the tree bottom-up is essential, [`rmdir()`](#os.rmdir "os.rmdir") doesn’t allow
    deleting a directory before the directory is empty:

    ```
    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    import os
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)
    ```

    Raises an [auditing event](sys.html#auditing) `os.walk` with arguments `top`, `topdown`, `onerror`, `followlinks`.

    Changed in version 3.5: This function now calls [`os.scandir()`](#os.scandir "os.scandir") instead of [`os.listdir()`](#os.listdir "os.listdir"),
    making it faster by reducing the number of calls to [`os.stat()`](#os.stat "os.stat").

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.fwalk(*top='.'*, *topdown=True*, *onerror=None*, *\**, *follow\_symlinks=False*, *dir\_fd=None*)[¶](#os.fwalk "Link to this definition")
:   This behaves exactly like [`walk()`](#os.walk "os.walk"), except that it yields a 4-tuple
    `(dirpath, dirnames, filenames, dirfd)`, and it supports `dir_fd`.

    *dirpath*, *dirnames* and *filenames* are identical to [`walk()`](#os.walk "os.walk") output,
    and *dirfd* is a file descriptor referring to the directory *dirpath*.

    This function always supports [paths relative to directory descriptors](#dir-fd) and [not following symlinks](#follow-symlinks). Note however
    that, unlike other functions, the [`fwalk()`](#os.fwalk "os.fwalk") default value for
    *follow\_symlinks* is `False`.

    Note

    Since [`fwalk()`](#os.fwalk "os.fwalk") yields file descriptors, those are only valid until
    the next iteration step, so you should duplicate them (e.g. with
    [`dup()`](#os.dup "os.dup")) if you want to keep them longer.

    This example displays the number of bytes taken by non-directory files in each
    directory under the starting directory, except that it doesn’t look under any
    `__pycache__` subdirectory:

    ```
    import os
    for root, dirs, files, rootfd in os.fwalk('python/Lib/xml'):
        print(root, "consumes", end="")
        print(sum([os.stat(name, dir_fd=rootfd).st_size for name in files]),
              end="")
        print("bytes in", len(files), "non-directory files")
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')  # don't visit __pycache__ directories
    ```

    In the next example, walking the tree bottom-up is essential:
    [`rmdir()`](#os.rmdir "os.rmdir") doesn’t allow deleting a directory before the directory is
    empty:

    ```
    # Delete everything reachable from the directory named in "top",
    # assuming there are no symbolic links.
    # CAUTION:  This is dangerous!  For example, if top == '/', it
    # could delete all your disk files.
    import os
    for root, dirs, files, rootfd in os.fwalk(top, topdown=False):
        for name in files:
            os.unlink(name, dir_fd=rootfd)
        for name in dirs:
            os.rmdir(name, dir_fd=rootfd)
    ```

    Raises an [auditing event](sys.html#auditing) `os.fwalk` with arguments `top`, `topdown`, `onerror`, `follow_symlinks`, `dir_fd`.

    [Availability](intro.html#availability): Unix.

    Added in version 3.3.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.7: Added support for [`bytes`](stdtypes.html#bytes "bytes") paths.

os.memfd\_create(*name*[, *flags=os.MFD\_CLOEXEC*])[¶](#os.memfd_create "Link to this definition")
:   Create an anonymous file and return a file descriptor that refers to it.
    *flags* must be one of the `os.MFD_*` constants available on the system
    (or a bitwise ORed combination of them). By default, the new file
    descriptor is [non-inheritable](#fd-inheritance).

    The name supplied in *name* is used as a filename and will be displayed as
    the target of the corresponding symbolic link in the directory
    `/proc/self/fd/`. The displayed name is always prefixed with `memfd:`
    and serves only for debugging purposes. Names do not affect the behavior of
    the file descriptor, and as such multiple files can have the same name
    without any side effects.

    [Availability](intro.html#availability): Linux >= 3.17 with glibc >= 2.27.

    Added in version 3.8.

os.MFD\_CLOEXEC[¶](#os.MFD_CLOEXEC "Link to this definition")

os.MFD\_ALLOW\_SEALING[¶](#os.MFD_ALLOW_SEALING "Link to this definition")

os.MFD\_HUGETLB[¶](#os.MFD_HUGETLB "Link to this definition")

os.MFD\_HUGE\_SHIFT[¶](#os.MFD_HUGE_SHIFT "Link to this definition")

os.MFD\_HUGE\_MASK[¶](#os.MFD_HUGE_MASK "Link to this definition")

os.MFD\_HUGE\_64KB[¶](#os.MFD_HUGE_64KB "Link to this definition")

os.MFD\_HUGE\_512KB[¶](#os.MFD_HUGE_512KB "Link to this definition")

os.MFD\_HUGE\_1MB[¶](#os.MFD_HUGE_1MB "Link to this definition")

os.MFD\_HUGE\_2MB[¶](#os.MFD_HUGE_2MB "Link to this definition")

os.MFD\_HUGE\_8MB[¶](#os.MFD_HUGE_8MB "Link to this definition")

os.MFD\_HUGE\_16MB[¶](#os.MFD_HUGE_16MB "Link to this definition")

os.MFD\_HUGE\_32MB[¶](#os.MFD_HUGE_32MB "Link to this definition")

os.MFD\_HUGE\_256MB[¶](#os.MFD_HUGE_256MB "Link to this definition")

os.MFD\_HUGE\_512MB[¶](#os.MFD_HUGE_512MB "Link to this definition")

os.MFD\_HUGE\_1GB[¶](#os.MFD_HUGE_1GB "Link to this definition")

os.MFD\_HUGE\_2GB[¶](#os.MFD_HUGE_2GB "Link to this definition")

os.MFD\_HUGE\_16GB[¶](#os.MFD_HUGE_16GB "Link to this definition")
:   These flags can be passed to [`memfd_create()`](#os.memfd_create "os.memfd_create").

    [Availability](intro.html#availability): Linux >= 3.17 with glibc >= 2.27

    The `MFD_HUGE*` flags are only available since Linux 4.14.

    Added in version 3.8.

os.eventfd(*initval*[, *flags=os.EFD\_CLOEXEC*])[¶](#os.eventfd "Link to this definition")
:   Create and return an event file descriptor. The file descriptors supports
    raw [`read()`](#os.read "os.read") and [`write()`](#os.write "os.write") with a buffer size of 8,
    [`select()`](select.html#select.select "select.select"), [`poll()`](select.html#select.poll "select.poll") and similar. See man page
    *[eventfd(2)](https://manpages.debian.org/eventfd(2))* for more information. By default, the
    new file descriptor is [non-inheritable](#fd-inheritance).

    *initval* is the initial value of the event counter. The initial value
    must be a 32 bit unsigned integer. Please note that the initial value is
    limited to a 32 bit unsigned int although the event counter is an unsigned
    64 bit integer with a maximum value of 264-2.

    *flags* can be constructed from [`EFD_CLOEXEC`](#os.EFD_CLOEXEC "os.EFD_CLOEXEC"),
    [`EFD_NONBLOCK`](#os.EFD_NONBLOCK "os.EFD_NONBLOCK"), and [`EFD_SEMAPHORE`](#os.EFD_SEMAPHORE "os.EFD_SEMAPHORE").

    If [`EFD_SEMAPHORE`](#os.EFD_SEMAPHORE "os.EFD_SEMAPHORE") is specified and the event counter is non-zero,
    [`eventfd_read()`](#os.eventfd_read "os.eventfd_read") returns 1 and decrements the counter by one.

    If [`EFD_SEMAPHORE`](#os.EFD_SEMAPHORE "os.EFD_SEMAPHORE") is not specified and the event counter is
    non-zero, [`eventfd_read()`](#os.eventfd_read "os.eventfd_read") returns the current event counter value and
    resets the counter to zero.

    If the event counter is zero and [`EFD_NONBLOCK`](#os.EFD_NONBLOCK "os.EFD_NONBLOCK") is not
    specified, [`eventfd_read()`](#os.eventfd_read "os.eventfd_read") blocks.

    [`eventfd_write()`](#os.eventfd_write "os.eventfd_write") increments the event counter. Write blocks if the
    write operation would increment the counter to a value larger than
    264-2.

    Example:

    ```
    import os

    # semaphore with start value '1'
    fd = os.eventfd(1, os.EFD_SEMAPHORE | os.EFC_CLOEXEC)
    try:
        # acquire semaphore
        v = os.eventfd_read(fd)
        try:
            do_work()
        finally:
            # release semaphore
            os.eventfd_write(fd, v)
    finally:
        os.close(fd)
    ```

    [Availability](intro.html#availability): Linux >= 2.6.27 with glibc >= 2.8

    Added in version 3.10.

os.eventfd\_read(*fd*)[¶](#os.eventfd_read "Link to this definition")
:   Read value from an [`eventfd()`](#os.eventfd "os.eventfd") file descriptor and return a 64 bit
    unsigned int. The function does not verify that *fd* is an [`eventfd()`](#os.eventfd "os.eventfd").

    [Availability](intro.html#availability): Linux >= 2.6.27

    Added in version 3.10.

os.eventfd\_write(*fd*, *value*)[¶](#os.eventfd_write "Link to this definition")
:   Add value to an [`eventfd()`](#os.eventfd "os.eventfd") file descriptor. *value* must be a 64 bit
    unsigned int. The function does not verify that *fd* is an [`eventfd()`](#os.eventfd "os.eventfd").

    [Availability](intro.html#availability): Linux >= 2.6.27

    Added in version 3.10.

os.EFD\_CLOEXEC[¶](#os.EFD_CLOEXEC "Link to this definition")
:   Set close-on-exec flag for new [`eventfd()`](#os.eventfd "os.eventfd") file descriptor.

    [Availability](intro.html#availability): Linux >= 2.6.27

    Added in version 3.10.

os.EFD\_NONBLOCK[¶](#os.EFD_NONBLOCK "Link to this definition")
:   Set [`O_NONBLOCK`](#os.O_NONBLOCK "os.O_NONBLOCK") status flag for new [`eventfd()`](#os.eventfd "os.eventfd") file
    descriptor.

    [Availability](intro.html#availability): Linux >= 2.6.27

    Added in version 3.10.

os.EFD\_SEMAPHORE[¶](#os.EFD_SEMAPHORE "Link to this definition")
:   Provide semaphore-like semantics for reads from an [`eventfd()`](#os.eventfd "os.eventfd") file
    descriptor. On read the internal counter is decremented by one.

    [Availability](intro.html#availability): Linux >= 2.6.30

    Added in version 3.10.

### Linux extended attributes[¶](#linux-extended-attributes "Link to this heading")

Added in version 3.3.

These functions are all available on Linux only.

os.getxattr(*path*, *attribute*, *\**, *follow\_symlinks=True*)[¶](#os.getxattr "Link to this definition")
:   Return the value of the extended filesystem attribute *attribute* for
    *path*. *attribute* can be bytes or str (directly or indirectly through the
    [`PathLike`](#os.PathLike "os.PathLike") interface). If it is str, it is encoded with the filesystem
    encoding.

    This function can support [specifying a file descriptor](#path-fd) and
    [not following symlinks](#follow-symlinks).

    Raises an [auditing event](sys.html#auditing) `os.getxattr` with arguments `path`, `attribute`.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *path* and *attribute*.

os.listxattr(*path=None*, *\**, *follow\_symlinks=True*)[¶](#os.listxattr "Link to this definition")
:   Return a list of the extended filesystem attributes on *path*. The
    attributes in the list are represented as strings decoded with the filesystem
    encoding. If *path* is `None`, [`listxattr()`](#os.listxattr "os.listxattr") will examine the current
    directory.

    This function can support [specifying a file descriptor](#path-fd) and
    [not following symlinks](#follow-symlinks).

    Raises an [auditing event](sys.html#auditing) `os.listxattr` with argument `path`.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.removexattr(*path*, *attribute*, *\**, *follow\_symlinks=True*)[¶](#os.removexattr "Link to this definition")
:   Removes the extended filesystem attribute *attribute* from *path*.
    *attribute* should be bytes or str (directly or indirectly through the
    [`PathLike`](#os.PathLike "os.PathLike") interface). If it is a string, it is encoded
    with the [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler).

    This function can support [specifying a file descriptor](#path-fd) and
    [not following symlinks](#follow-symlinks).

    Raises an [auditing event](sys.html#auditing) `os.removexattr` with arguments `path`, `attribute`.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *path* and *attribute*.

os.setxattr(*path*, *attribute*, *value*, *flags=0*, *\**, *follow\_symlinks=True*)[¶](#os.setxattr "Link to this definition")
:   Set the extended filesystem attribute *attribute* on *path* to *value*.
    *attribute* must be a bytes or str with no embedded NULs (directly or
    indirectly through the [`PathLike`](#os.PathLike "os.PathLike") interface). If it is a str,
    it is encoded with the [filesystem encoding and error handler](../glossary.html#term-filesystem-encoding-and-error-handler). *flags* may be
    [`XATTR_REPLACE`](#os.XATTR_REPLACE "os.XATTR_REPLACE") or [`XATTR_CREATE`](#os.XATTR_CREATE "os.XATTR_CREATE"). If [`XATTR_REPLACE`](#os.XATTR_REPLACE "os.XATTR_REPLACE") is
    given and the attribute does not exist, `ENODATA` will be raised.
    If [`XATTR_CREATE`](#os.XATTR_CREATE "os.XATTR_CREATE") is given and the attribute already exists, the
    attribute will not be created and `EEXISTS` will be raised.

    This function can support [specifying a file descriptor](#path-fd) and
    [not following symlinks](#follow-symlinks).

    Note

    A bug in Linux kernel versions less than 2.6.39 caused the flags argument
    to be ignored on some filesystems.

    Raises an [auditing event](sys.html#auditing) `os.setxattr` with arguments `path`, `attribute`, `value`, `flags`.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object) for *path* and *attribute*.

os.XATTR\_SIZE\_MAX[¶](#os.XATTR_SIZE_MAX "Link to this definition")
:   The maximum size the value of an extended attribute can be. Currently, this
    is 64 KiB on Linux.

os.XATTR\_CREATE[¶](#os.XATTR_CREATE "Link to this definition")
:   This is a possible value for the flags argument in [`setxattr()`](#os.setxattr "os.setxattr"). It
    indicates the operation must create an attribute.

os.XATTR\_REPLACE[¶](#os.XATTR_REPLACE "Link to this definition")
:   This is a possible value for the flags argument in [`setxattr()`](#os.setxattr "os.setxattr"). It
    indicates the operation must replace an existing attribute.

## Process Management[¶](#process-management "Link to this heading")

These functions may be used to create and manage processes.

The various [`exec*`](#os.execl "os.execl") functions take a list of arguments for the new
program loaded into the process. In each case, the first of these arguments is
passed to the new program as its own name rather than as an argument a user may
have typed on a command line. For the C programmer, this is the `argv[0]`
passed to a program’s `main()`. For example, `os.execv('/bin/echo',
['foo', 'bar'])` will only print `bar` on standard output; `foo` will seem
to be ignored.

os.abort()[¶](#os.abort "Link to this definition")
:   Generate a `SIGABRT` signal to the current process. On Unix, the default
    behavior is to produce a core dump; on Windows, the process immediately returns
    an exit code of `3`. Be aware that calling this function will not call the
    Python signal handler registered for `SIGABRT` with
    [`signal.signal()`](signal.html#signal.signal "signal.signal").

os.add\_dll\_directory(*path*)[¶](#os.add_dll_directory "Link to this definition")
:   Add a path to the DLL search path.

    This search path is used when resolving dependencies for imported
    extension modules (the module itself is resolved through
    [`sys.path`](sys.html#sys.path "sys.path")), and also by [`ctypes`](ctypes.html#module-ctypes "ctypes: A foreign function library for Python.").

    Remove the directory by calling **close()** on the returned object
    or using it in a [`with`](../reference/compound_stmts.html#with) statement.

    See the [Microsoft documentation](https://msdn.microsoft.com/44228cf2-6306-466c-8f16-f513cd3ba8b5)
    for more information about how DLLs are loaded.

    Raises an [auditing event](sys.html#auditing) `os.add_dll_directory` with argument `path`.

    [Availability](intro.html#availability): Windows.

    Added in version 3.8: Previous versions of CPython would resolve DLLs using the default
    behavior for the current process. This led to inconsistencies,
    such as only sometimes searching `PATH` or the current
    working directory, and OS functions such as `AddDllDirectory`
    having no effect.

    In 3.8, the two primary ways DLLs are loaded now explicitly
    override the process-wide behavior to ensure consistency. See the
    [porting notes](../whatsnew/3.8.html#bpo-36085-whatsnew) for information on
    updating libraries.

os.execl(*path*, *arg0*, *arg1*, *...*)[¶](#os.execl "Link to this definition")

os.execle(*path*, *arg0*, *arg1*, *...*, *env*)[¶](#os.execle "Link to this definition")

os.execlp(*file*, *arg0*, *arg1*, *...*)[¶](#os.execlp "Link to this definition")

os.execlpe(*file*, *arg0*, *arg1*, *...*, *env*)[¶](#os.execlpe "Link to this definition")

os.execv(*path*, *args*)[¶](#os.execv "Link to this definition")

os.execve(*path*, *args*, *env*)[¶](#os.execve "Link to this definition")

os.execvp(*file*, *args*)[¶](#os.execvp "Link to this definition")

os.execvpe(*file*, *args*, *env*)[¶](#os.execvpe "Link to this definition")
:   These functions all execute a new program, replacing the current process; they
    do not return. On Unix, the new executable is loaded into the current process,
    and will have the same process id as the caller. Errors will be reported as
    [`OSError`](exceptions.html#OSError "OSError") exceptions.

    The current process is replaced immediately. Open file objects and
    descriptors are not flushed, so if there may be data buffered
    on these open files, you should flush them using
    `sys.stdout.flush()` or [`os.fsync()`](#os.fsync "os.fsync") before calling an
    [`exec*`](#os.execl "os.execl") function.

    The “l” and “v” variants of the [`exec*`](#os.execl "os.execl") functions differ in how
    command-line arguments are passed. The “l” variants are perhaps the easiest
    to work with if the number of parameters is fixed when the code is written; the
    individual parameters simply become additional parameters to the `execl*()`
    functions. The “v” variants are good when the number of parameters is
    variable, with the arguments being passed in a list or tuple as the *args*
    parameter. In either case, the arguments to the child process should start with
    the name of the command being run, but this is not enforced.

    The variants which include a “p” near the end ([`execlp()`](#os.execlp "os.execlp"),
    [`execlpe()`](#os.execlpe "os.execlpe"), [`execvp()`](#os.execvp "os.execvp"), and [`execvpe()`](#os.execvpe "os.execvpe")) will use the
    `PATH` environment variable to locate the program *file*. When the
    environment is being replaced (using one of the [`exec*e`](#os.execl "os.execl") variants,
    discussed in the next paragraph), the new environment is used as the source of
    the `PATH` variable. The other variants, [`execl()`](#os.execl "os.execl"), [`execle()`](#os.execle "os.execle"),
    [`execv()`](#os.execv "os.execv"), and [`execve()`](#os.execve "os.execve"), will not use the `PATH` variable to
    locate the executable; *path* must contain an appropriate absolute or relative
    path. Relative paths must include at least one slash, even on Windows, as
    plain names will not be resolved.

    For [`execle()`](#os.execle "os.execle"), [`execlpe()`](#os.execlpe "os.execlpe"), [`execve()`](#os.execve "os.execve"), and [`execvpe()`](#os.execvpe "os.execvpe") (note
    that these all end in “e”), the *env* parameter must be a mapping which is
    used to define the environment variables for the new process (these are used
    instead of the current process’ environment); the functions [`execl()`](#os.execl "os.execl"),
    [`execlp()`](#os.execlp "os.execlp"), [`execv()`](#os.execv "os.execv"), and [`execvp()`](#os.execvp "os.execvp") all cause the new process to
    inherit the environment of the current process.

    For [`execve()`](#os.execve "os.execve") on some platforms, *path* may also be specified as an open
    file descriptor. This functionality may not be supported on your platform;
    you can check whether or not it is available using [`os.supports_fd`](#os.supports_fd "os.supports_fd").
    If it is unavailable, using it will raise a [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError").

    Raises an [auditing event](sys.html#auditing) `os.exec` with arguments `path`, `args`, `env`.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

    Changed in version 3.3: Added support for specifying *path* as an open file descriptor
    for [`execve()`](#os.execve "os.execve").

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.\_exit(*n*)[¶](#os._exit "Link to this definition")
:   Exit the process with status *n*, without calling cleanup handlers, flushing
    stdio buffers, etc.

    Note

    The standard way to exit is [`sys.exit(n)`](sys.html#sys.exit "sys.exit"). `_exit()` should
    normally only be used in the child process after a [`fork()`](#os.fork "os.fork").

The following exit codes are defined and can be used with [`_exit()`](#os._exit "os._exit"),
although they are not required. These are typically used for system programs
written in Python, such as a mail server’s external command delivery program.

Note

Some of these may not be available on all Unix platforms, since there is some
variation. These constants are defined where they are defined by the underlying
platform.

os.EX\_OK[¶](#os.EX_OK "Link to this definition")
:   Exit code that means no error occurred. May be taken from the defined value of
    `EXIT_SUCCESS` on some platforms. Generally has a value of zero.

    [Availability](intro.html#availability): Unix, Windows.

os.EX\_USAGE[¶](#os.EX_USAGE "Link to this definition")
:   Exit code that means the command was used incorrectly, such as when the wrong
    number of arguments are given.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_DATAERR[¶](#os.EX_DATAERR "Link to this definition")
:   Exit code that means the input data was incorrect.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_NOINPUT[¶](#os.EX_NOINPUT "Link to this definition")
:   Exit code that means an input file did not exist or was not readable.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_NOUSER[¶](#os.EX_NOUSER "Link to this definition")
:   Exit code that means a specified user did not exist.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_NOHOST[¶](#os.EX_NOHOST "Link to this definition")
:   Exit code that means a specified host did not exist.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_UNAVAILABLE[¶](#os.EX_UNAVAILABLE "Link to this definition")
:   Exit code that means that a required service is unavailable.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_SOFTWARE[¶](#os.EX_SOFTWARE "Link to this definition")
:   Exit code that means an internal software error was detected.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_OSERR[¶](#os.EX_OSERR "Link to this definition")
:   Exit code that means an operating system error was detected, such as the
    inability to fork or create a pipe.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_OSFILE[¶](#os.EX_OSFILE "Link to this definition")
:   Exit code that means some system file did not exist, could not be opened, or had
    some other kind of error.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_CANTCREAT[¶](#os.EX_CANTCREAT "Link to this definition")
:   Exit code that means a user specified output file could not be created.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_IOERR[¶](#os.EX_IOERR "Link to this definition")
:   Exit code that means that an error occurred while doing I/O on some file.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_TEMPFAIL[¶](#os.EX_TEMPFAIL "Link to this definition")
:   Exit code that means a temporary failure occurred. This indicates something
    that may not really be an error, such as a network connection that couldn’t be
    made during a retryable operation.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_PROTOCOL[¶](#os.EX_PROTOCOL "Link to this definition")
:   Exit code that means that a protocol exchange was illegal, invalid, or not
    understood.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_NOPERM[¶](#os.EX_NOPERM "Link to this definition")
:   Exit code that means that there were insufficient permissions to perform the
    operation (but not intended for file system problems).

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_CONFIG[¶](#os.EX_CONFIG "Link to this definition")
:   Exit code that means that some kind of configuration error occurred.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.EX\_NOTFOUND[¶](#os.EX_NOTFOUND "Link to this definition")
:   Exit code that means something like “an entry was not found”.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.fork()[¶](#os.fork "Link to this definition")
:   Fork a child process. Return `0` in the child and the child’s process id in the
    parent. If an error occurs [`OSError`](exceptions.html#OSError "OSError") is raised.

    Note that some platforms including FreeBSD <= 6.3 and Cygwin have
    known issues when using `fork()` from a thread.

    Raises an [auditing event](sys.html#auditing) `os.fork` with no arguments.

    Warning

    If you use TLS sockets in an application calling `fork()`, see
    the warning in the [`ssl`](ssl.html#module-ssl "ssl: TLS/SSL wrapper for socket objects") documentation.

    Warning

    On macOS the use of this function is unsafe when mixed with using
    higher-level system APIs, and that includes using [`urllib.request`](urllib.request.html#module-urllib.request "urllib.request: Extensible library for opening URLs.").

    Changed in version 3.8: Calling `fork()` in a subinterpreter is no longer supported
    ([`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") is raised).

    Changed in version 3.12: If Python is able to detect that your process has multiple
    threads, [`os.fork()`](#os.fork "os.fork") now raises a [`DeprecationWarning`](exceptions.html#DeprecationWarning "DeprecationWarning").

    We chose to surface this as a warning, when detectable, to better
    inform developers of a design problem that the POSIX platform
    specifically notes as not supported. Even in code that
    *appears* to work, it has never been safe to mix threading with
    [`os.fork()`](#os.fork "os.fork") on POSIX platforms. The CPython runtime itself has
    always made API calls that are not safe for use in the child
    process when threads existed in the parent (such as `malloc` and
    `free`).

    Users of macOS or users of libc or malloc implementations other
    than those typically found in glibc to date are among those
    already more likely to experience deadlocks running such code.

    See [this discussion on fork being incompatible with threads](https://discuss.python.org/t/33555)
    for technical details of why we’re surfacing this longstanding
    platform compatibility problem to developers.

    [Availability](intro.html#availability): POSIX, not Emscripten, not WASI.

os.forkpty()[¶](#os.forkpty "Link to this definition")
:   Fork a child process, using a new pseudo-terminal as the child’s controlling
    terminal. Return a pair of `(pid, fd)`, where *pid* is `0` in the child, the
    new child’s process id in the parent, and *fd* is the file descriptor of the
    master end of the pseudo-terminal. For a more portable approach, use the
    [`pty`](pty.html#module-pty "pty: Pseudo-Terminal Handling for Unix. (Unix)") module. If an error occurs [`OSError`](exceptions.html#OSError "OSError") is raised.

    Raises an [auditing event](sys.html#auditing) `os.forkpty` with no arguments.

    Warning

    On macOS the use of this function is unsafe when mixed with using
    higher-level system APIs, and that includes using [`urllib.request`](urllib.request.html#module-urllib.request "urllib.request: Extensible library for opening URLs.").

    Changed in version 3.8: Calling `forkpty()` in a subinterpreter is no longer supported
    ([`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") is raised).

    Changed in version 3.12: If Python is able to detect that your process has multiple
    threads, this now raises a [`DeprecationWarning`](exceptions.html#DeprecationWarning "DeprecationWarning"). See the
    longer explanation on [`os.fork()`](#os.fork "os.fork").

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.kill(*pid*, *sig*, */*)[¶](#os.kill "Link to this definition")
:   Send signal *sig* to the process *pid*. Constants for the specific signals
    available on the host platform are defined in the [`signal`](signal.html#module-signal "signal: Set handlers for asynchronous events.") module.

    Windows: The [`signal.CTRL_C_EVENT`](signal.html#signal.CTRL_C_EVENT "signal.CTRL_C_EVENT") and
    [`signal.CTRL_BREAK_EVENT`](signal.html#signal.CTRL_BREAK_EVENT "signal.CTRL_BREAK_EVENT") signals are special signals which can
    only be sent to console processes which share a common console window,
    e.g., some subprocesses. Any other value for *sig* will cause the process
    to be unconditionally killed by the TerminateProcess API, and the exit code
    will be set to *sig*.

    See also [`signal.pthread_kill()`](signal.html#signal.pthread_kill "signal.pthread_kill").

    Raises an [auditing event](sys.html#auditing) `os.kill` with arguments `pid`, `sig`.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

    Changed in version 3.2: Added Windows support.

os.killpg(*pgid*, *sig*, */*)[¶](#os.killpg "Link to this definition")
:   Send the signal *sig* to the process group *pgid*.

    Raises an [auditing event](sys.html#auditing) `os.killpg` with arguments `pgid`, `sig`.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.nice(*increment*, */*)[¶](#os.nice "Link to this definition")
:   Add *increment* to the process’s “niceness”. Return the new niceness.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.pidfd\_open(*pid*, *flags=0*)[¶](#os.pidfd_open "Link to this definition")
:   Return a file descriptor referring to the process *pid* with *flags* set.
    This descriptor can be used to perform process management without races
    and signals.

    See the *[pidfd\_open(2)](https://manpages.debian.org/pidfd_open(2))* man page for more details.

    [Availability](intro.html#availability): Linux >= 5.3

    Added in version 3.9.

    os.PIDFD\_NONBLOCK[¶](#os.PIDFD_NONBLOCK "Link to this definition")
    :   This flag indicates that the file descriptor will be non-blocking.
        If the process referred to by the file descriptor has not yet terminated,
        then an attempt to wait on the file descriptor using *[waitid(2)](https://manpages.debian.org/waitid(2))*
        will immediately return the error [`EAGAIN`](errno.html#errno.EAGAIN "errno.EAGAIN") rather than blocking.

    [Availability](intro.html#availability): Linux >= 5.10

    Added in version 3.12.

os.plock(*op*, */*)[¶](#os.plock "Link to this definition")
:   Lock program segments into memory. The value of *op* (defined in
    `<sys/lock.h>`) determines which segments are locked.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.popen(*cmd*, *mode='r'*, *buffering=-1*)[¶](#os.popen "Link to this definition")
:   Open a pipe to or from command *cmd*.
    The return value is an open file object
    connected to the pipe, which can be read or written depending on whether *mode*
    is `'r'` (default) or `'w'`.
    The *buffering* argument have the same meaning as
    the corresponding argument to the built-in [`open()`](functions.html#open "open") function. The
    returned file object reads or writes text strings rather than bytes.

    The `close` method returns [`None`](constants.html#None "None") if the subprocess exited
    successfully, or the subprocess’s return code if there was an
    error. On POSIX systems, if the return code is positive it
    represents the return value of the process left-shifted by one
    byte. If the return code is negative, the process was terminated
    by the signal given by the negated value of the return code. (For
    example, the return value might be `- signal.SIGKILL` if the
    subprocess was killed.) On Windows systems, the return value
    contains the signed integer return code from the child process.

    On Unix, [`waitstatus_to_exitcode()`](#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the `close`
    method result (exit status) into an exit code if it is not `None`. On
    Windows, the `close` method result is directly the exit code
    (or `None`).

    This is implemented using [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen"); see that class’s
    documentation for more powerful ways to manage and communicate with
    subprocesses.

    [Availability](intro.html#availability): not Emscripten, not WASI.

    Note

    The [Python UTF-8 Mode](#utf8-mode) affects encodings used
    for *cmd* and pipe contents.

    [`popen()`](#os.popen "os.popen") is a simple wrapper around [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen").
    Use [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen") or [`subprocess.run()`](subprocess.html#subprocess.run "subprocess.run") to
    control options like encodings.

os.posix\_spawn(*path*, *argv*, *env*, *\**, *file\_actions=None*, *setpgroup=None*, *resetids=False*, *setsid=False*, *setsigmask=()*, *setsigdef=()*, *scheduler=None*)[¶](#os.posix_spawn "Link to this definition")
:   Wraps the `posix_spawn()` C library API for use from Python.

    Most users should use [`subprocess.run()`](subprocess.html#subprocess.run "subprocess.run") instead of [`posix_spawn()`](#os.posix_spawn "os.posix_spawn").

    The positional-only arguments *path*, *args*, and *env* are similar to
    [`execve()`](#os.execve "os.execve").

    The *path* parameter is the path to the executable file. The *path* should
    contain a directory. Use [`posix_spawnp()`](#os.posix_spawnp "os.posix_spawnp") to pass an executable file
    without directory.

    The *file\_actions* argument may be a sequence of tuples describing actions
    to take on specific file descriptors in the child process between the C
    library implementation’s `fork()` and `exec()` steps.
    The first item in each tuple must be one of the three type indicator
    listed below describing the remaining tuple elements:

    os.POSIX\_SPAWN\_OPEN[¶](#os.POSIX_SPAWN_OPEN "Link to this definition")
    :   (`os.POSIX_SPAWN_OPEN`, *fd*, *path*, *flags*, *mode*)

        Performs `os.dup2(os.open(path, flags, mode), fd)`.

    os.POSIX\_SPAWN\_CLOSE[¶](#os.POSIX_SPAWN_CLOSE "Link to this definition")
    :   (`os.POSIX_SPAWN_CLOSE`, *fd*)

        Performs `os.close(fd)`.

    os.POSIX\_SPAWN\_DUP2[¶](#os.POSIX_SPAWN_DUP2 "Link to this definition")
    :   (`os.POSIX_SPAWN_DUP2`, *fd*, *new\_fd*)

        Performs `os.dup2(fd, new_fd)`.

    These tuples correspond to the C library
    `posix_spawn_file_actions_addopen()`,
    `posix_spawn_file_actions_addclose()`, and
    `posix_spawn_file_actions_adddup2()` API calls used to prepare
    for the `posix_spawn()` call itself.

    The *setpgroup* argument will set the process group of the child to the value
    specified. If the value specified is 0, the child’s process group ID will be
    made the same as its process ID. If the value of *setpgroup* is not set, the
    child will inherit the parent’s process group ID. This argument corresponds
    to the C library `POSIX_SPAWN_SETPGROUP` flag.

    If the *resetids* argument is `True` it will reset the effective UID and
    GID of the child to the real UID and GID of the parent process. If the
    argument is `False`, then the child retains the effective UID and GID of
    the parent. In either case, if the set-user-ID and set-group-ID permission
    bits are enabled on the executable file, their effect will override the
    setting of the effective UID and GID. This argument corresponds to the C
    library `POSIX_SPAWN_RESETIDS` flag.

    If the *setsid* argument is `True`, it will create a new session ID
    for `posix_spawn`. *setsid* requires `POSIX_SPAWN_SETSID`
    or `POSIX_SPAWN_SETSID_NP` flag. Otherwise, [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError")
    is raised.

    The *setsigmask* argument will set the signal mask to the signal set
    specified. If the parameter is not used, then the child inherits the
    parent’s signal mask. This argument corresponds to the C library
    `POSIX_SPAWN_SETSIGMASK` flag.

    The *sigdef* argument will reset the disposition of all signals in the set
    specified. This argument corresponds to the C library
    `POSIX_SPAWN_SETSIGDEF` flag.

    The *scheduler* argument must be a tuple containing the (optional) scheduler
    policy and an instance of [`sched_param`](#os.sched_param "os.sched_param") with the scheduler parameters.
    A value of `None` in the place of the scheduler policy indicates that is
    not being provided. This argument is a combination of the C library
    `POSIX_SPAWN_SETSCHEDPARAM` and `POSIX_SPAWN_SETSCHEDULER`
    flags.

    Raises an [auditing event](sys.html#auditing) `os.posix_spawn` with arguments `path`, `argv`, `env`.

    Added in version 3.8.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.posix\_spawnp(*path*, *argv*, *env*, *\**, *file\_actions=None*, *setpgroup=None*, *resetids=False*, *setsid=False*, *setsigmask=()*, *setsigdef=()*, *scheduler=None*)[¶](#os.posix_spawnp "Link to this definition")
:   Wraps the `posix_spawnp()` C library API for use from Python.

    Similar to [`posix_spawn()`](#os.posix_spawn "os.posix_spawn") except that the system searches
    for the *executable* file in the list of directories specified by the
    `PATH` environment variable (in the same way as for `execvp(3)`).

    Raises an [auditing event](sys.html#auditing) `os.posix_spawn` with arguments `path`, `argv`, `env`.

    Added in version 3.8.

    [Availability](intro.html#availability): POSIX, not Emscripten, not WASI.

    See [`posix_spawn()`](#os.posix_spawn "os.posix_spawn") documentation.

os.register\_at\_fork(*\**, *before=None*, *after\_in\_parent=None*, *after\_in\_child=None*)[¶](#os.register_at_fork "Link to this definition")
:   Register callables to be executed when a new child process is forked
    using [`os.fork()`](#os.fork "os.fork") or similar process cloning APIs.
    The parameters are optional and keyword-only.
    Each specifies a different call point.

    * *before* is a function called before forking a child process.
    * *after\_in\_parent* is a function called from the parent process
      after forking a child process.
    * *after\_in\_child* is a function called from the child process.

    These calls are only made if control is expected to return to the
    Python interpreter. A typical [`subprocess`](subprocess.html#module-subprocess "subprocess: Subprocess management.") launch will not
    trigger them as the child is not going to re-enter the interpreter.

    Functions registered for execution before forking are called in
    reverse registration order. Functions registered for execution
    after forking (either in the parent or in the child) are called
    in registration order.

    Note that `fork()` calls made by third-party C code may not
    call those functions, unless it explicitly calls [`PyOS_BeforeFork()`](../c-api/sys.html#c.PyOS_BeforeFork "PyOS_BeforeFork"),
    [`PyOS_AfterFork_Parent()`](../c-api/sys.html#c.PyOS_AfterFork_Parent "PyOS_AfterFork_Parent") and [`PyOS_AfterFork_Child()`](../c-api/sys.html#c.PyOS_AfterFork_Child "PyOS_AfterFork_Child").

    There is no way to unregister a function.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.7.

os.spawnl(*mode*, *path*, *...*)[¶](#os.spawnl "Link to this definition")

os.spawnle(*mode*, *path*, *...*, *env*)[¶](#os.spawnle "Link to this definition")

os.spawnlp(*mode*, *file*, *...*)[¶](#os.spawnlp "Link to this definition")

os.spawnlpe(*mode*, *file*, *...*, *env*)[¶](#os.spawnlpe "Link to this definition")

os.spawnv(*mode*, *path*, *args*)[¶](#os.spawnv "Link to this definition")

os.spawnve(*mode*, *path*, *args*, *env*)[¶](#os.spawnve "Link to this definition")

os.spawnvp(*mode*, *file*, *args*)[¶](#os.spawnvp "Link to this definition")

os.spawnvpe(*mode*, *file*, *args*, *env*)[¶](#os.spawnvpe "Link to this definition")
:   Execute the program *path* in a new process.

    (Note that the [`subprocess`](subprocess.html#module-subprocess "subprocess: Subprocess management.") module provides more powerful facilities for
    spawning new processes and retrieving their results; using that module is
    preferable to using these functions. Check especially the
    [Replacing Older Functions with the subprocess Module](subprocess.html#subprocess-replacements) section.)

    If *mode* is [`P_NOWAIT`](#os.P_NOWAIT "os.P_NOWAIT"), this function returns the process id of the new
    process; if *mode* is [`P_WAIT`](#os.P_WAIT "os.P_WAIT"), returns the process’s exit code if it
    exits normally, or `-signal`, where *signal* is the signal that killed the
    process. On Windows, the process id will actually be the process handle, so can
    be used with the [`waitpid()`](#os.waitpid "os.waitpid") function.

    Note on VxWorks, this function doesn’t return `-signal` when the new process is
    killed. Instead it raises OSError exception.

    The “l” and “v” variants of the [`spawn*`](#os.spawnl "os.spawnl") functions differ in how
    command-line arguments are passed. The “l” variants are perhaps the easiest
    to work with if the number of parameters is fixed when the code is written; the
    individual parameters simply become additional parameters to the
    `spawnl*()` functions. The “v” variants are good when the number of
    parameters is variable, with the arguments being passed in a list or tuple as
    the *args* parameter. In either case, the arguments to the child process must
    start with the name of the command being run.

    The variants which include a second “p” near the end ([`spawnlp()`](#os.spawnlp "os.spawnlp"),
    [`spawnlpe()`](#os.spawnlpe "os.spawnlpe"), [`spawnvp()`](#os.spawnvp "os.spawnvp"), and [`spawnvpe()`](#os.spawnvpe "os.spawnvpe")) will use the
    `PATH` environment variable to locate the program *file*. When the
    environment is being replaced (using one of the [`spawn*e`](#os.spawnl "os.spawnl") variants,
    discussed in the next paragraph), the new environment is used as the source of
    the `PATH` variable. The other variants, [`spawnl()`](#os.spawnl "os.spawnl"),
    [`spawnle()`](#os.spawnle "os.spawnle"), [`spawnv()`](#os.spawnv "os.spawnv"), and [`spawnve()`](#os.spawnve "os.spawnve"), will not use the
    `PATH` variable to locate the executable; *path* must contain an
    appropriate absolute or relative path.

    For [`spawnle()`](#os.spawnle "os.spawnle"), [`spawnlpe()`](#os.spawnlpe "os.spawnlpe"), [`spawnve()`](#os.spawnve "os.spawnve"), and [`spawnvpe()`](#os.spawnvpe "os.spawnvpe")
    (note that these all end in “e”), the *env* parameter must be a mapping
    which is used to define the environment variables for the new process (they are
    used instead of the current process’ environment); the functions
    [`spawnl()`](#os.spawnl "os.spawnl"), [`spawnlp()`](#os.spawnlp "os.spawnlp"), [`spawnv()`](#os.spawnv "os.spawnv"), and [`spawnvp()`](#os.spawnvp "os.spawnvp") all cause
    the new process to inherit the environment of the current process. Note that
    keys and values in the *env* dictionary must be strings; invalid keys or
    values will cause the function to fail, with a return value of `127`.

    As an example, the following calls to [`spawnlp()`](#os.spawnlp "os.spawnlp") and [`spawnvpe()`](#os.spawnvpe "os.spawnvpe") are
    equivalent:

    ```
    import os
    os.spawnlp(os.P_WAIT, 'cp', 'cp', 'index.html', '/dev/null')

    L = ['cp', 'index.html', '/dev/null']
    os.spawnvpe(os.P_WAIT, 'cp', L, os.environ)
    ```

    Raises an [auditing event](sys.html#auditing) `os.spawn` with arguments `mode`, `path`, `args`, `env`.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

    [`spawnlp()`](#os.spawnlp "os.spawnlp"), [`spawnlpe()`](#os.spawnlpe "os.spawnlpe"), [`spawnvp()`](#os.spawnvp "os.spawnvp")
    and [`spawnvpe()`](#os.spawnvpe "os.spawnvpe") are not available on Windows. [`spawnle()`](#os.spawnle "os.spawnle") and
    [`spawnve()`](#os.spawnve "os.spawnve") are not thread-safe on Windows; we advise you to use the
    [`subprocess`](subprocess.html#module-subprocess "subprocess: Subprocess management.") module instead.

    Changed in version 3.6: Accepts a [path-like object](../glossary.html#term-path-like-object).

os.P\_NOWAIT[¶](#os.P_NOWAIT "Link to this definition")

os.P\_NOWAITO[¶](#os.P_NOWAITO "Link to this definition")
:   Possible values for the *mode* parameter to the [`spawn*`](#os.spawnl "os.spawnl") family of
    functions. If either of these values is given, the [`spawn*`](#os.spawnl "os.spawnl") functions
    will return as soon as the new process has been created, with the process id as
    the return value.

    [Availability](intro.html#availability): Unix, Windows.

os.P\_WAIT[¶](#os.P_WAIT "Link to this definition")
:   Possible value for the *mode* parameter to the [`spawn*`](#os.spawnl "os.spawnl") family of
    functions. If this is given as *mode*, the [`spawn*`](#os.spawnl "os.spawnl") functions will not
    return until the new process has run to completion and will return the exit code
    of the process the run is successful, or `-signal` if a signal kills the
    process.

    [Availability](intro.html#availability): Unix, Windows.

os.P\_DETACH[¶](#os.P_DETACH "Link to this definition")

os.P\_OVERLAY[¶](#os.P_OVERLAY "Link to this definition")
:   Possible values for the *mode* parameter to the [`spawn*`](#os.spawnl "os.spawnl") family of
    functions. These are less portable than those listed above. [`P_DETACH`](#os.P_DETACH "os.P_DETACH")
    is similar to [`P_NOWAIT`](#os.P_NOWAIT "os.P_NOWAIT"), but the new process is detached from the
    console of the calling process. If [`P_OVERLAY`](#os.P_OVERLAY "os.P_OVERLAY") is used, the current
    process will be replaced; the [`spawn*`](#os.spawnl "os.spawnl") function will not return.

    [Availability](intro.html#availability): Windows.

os.startfile(*path*[, *operation*][, *arguments*][, *cwd*][, *show\_cmd*])[¶](#os.startfile "Link to this definition")
:   Start a file with its associated application.

    When *operation* is not specified, this acts like double-clicking
    the file in Windows Explorer, or giving the file name as an argument to the
    **start** command from the interactive command shell: the file is opened
    with whatever application (if any) its extension is associated.

    When another *operation* is given, it must be a “command verb” that specifies
    what should be done with the file. Common verbs documented by Microsoft are `'open'`,
    `'print'` and `'edit'` (to be used on files) as well as `'explore'` and
    `'find'` (to be used on directories).

    When launching an application, specify *arguments* to be passed as a single
    string. This argument may have no effect when using this function to launch a
    document.

    The default working directory is inherited, but may be overridden by the *cwd*
    argument. This should be an absolute path. A relative *path* will be resolved
    against this argument.

    Use *show\_cmd* to override the default window style. Whether this has any
    effect will depend on the application being launched. Values are integers as
    supported by the Win32 `ShellExecute()` function.

    [`startfile()`](#os.startfile "os.startfile") returns as soon as the associated application is launched.
    There is no option to wait for the application to close, and no way to retrieve
    the application’s exit status. The *path* parameter is relative to the current
    directory or *cwd*. If you want to use an absolute path, make sure the first
    character is not a slash (`'/'`) Use [`pathlib`](pathlib.html#module-pathlib "pathlib: Object-oriented filesystem paths") or the
    [`os.path.normpath()`](os.path.html#os.path.normpath "os.path.normpath") function to ensure that paths are properly encoded for
    Win32.

    To reduce interpreter startup overhead, the Win32 `ShellExecute()`
    function is not resolved until this function is first called. If the function
    cannot be resolved, [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError") will be raised.

    Raises an [auditing event](sys.html#auditing) `os.startfile` with arguments `path`, `operation`.

    Raises an [auditing event](sys.html#auditing) `os.startfile/2` with arguments `path`, `operation`, `arguments`, `cwd`, `show_cmd`.

    [Availability](intro.html#availability): Windows.

    Changed in version 3.10: Added the *arguments*, *cwd* and *show\_cmd* arguments, and the
    `os.startfile/2` audit event.

os.system(*command*)[¶](#os.system "Link to this definition")
:   Execute the command (a string) in a subshell. This is implemented by calling
    the Standard C function `system()`, and has the same limitations.
    Changes to [`sys.stdin`](sys.html#sys.stdin "sys.stdin"), etc. are not reflected in the environment of
    the executed command. If *command* generates any output, it will be sent to
    the interpreter standard output stream. The C standard does not
    specify the meaning of the return value of the C function, so the return
    value of the Python function is system-dependent.

    On Unix, the return value is the exit status of the process encoded in the
    format specified for [`wait()`](#os.wait "os.wait").

    On Windows, the return value is that returned by the system shell after
    running *command*. The shell is given by the Windows environment variable
    `COMSPEC`: it is usually **cmd.exe**, which returns the exit
    status of the command run; on systems using a non-native shell, consult your
    shell documentation.

    The [`subprocess`](subprocess.html#module-subprocess "subprocess: Subprocess management.") module provides more powerful facilities for spawning
    new processes and retrieving their results; using that module is preferable
    to using this function. See the [Replacing Older Functions with the subprocess Module](subprocess.html#subprocess-replacements) section in
    the [`subprocess`](subprocess.html#module-subprocess "subprocess: Subprocess management.") documentation for some helpful recipes.

    On Unix, [`waitstatus_to_exitcode()`](#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the result
    (exit status) into an exit code. On Windows, the result is directly the exit
    code.

    Raises an [auditing event](sys.html#auditing) `os.system` with argument `command`.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

os.times()[¶](#os.times "Link to this definition")
:   Returns the current global process times.
    The return value is an object with five attributes:

    * `user` - user time
    * `system` - system time
    * `children_user` - user time of all child processes
    * `children_system` - system time of all child processes
    * `elapsed` - elapsed real time since a fixed point in the past

    For backwards compatibility, this object also behaves like a five-tuple
    containing `user`, `system`, `children_user`,
    `children_system`, and `elapsed` in that order.

    See the Unix manual page
    *[times(2)](https://manpages.debian.org/times(2))* and [times(3)](https://man.freebsd.org/cgi/man.cgi?time(3)) manual page on Unix or [the GetProcessTimes MSDN](https://docs.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes)
    on Windows. On Windows, only `user` and `system` are known; the other attributes are zero.

    [Availability](intro.html#availability): Unix, Windows.

    Changed in version 3.3: Return type changed from a tuple to a tuple-like object
    with named attributes.

os.wait()[¶](#os.wait "Link to this definition")
:   Wait for completion of a child process, and return a tuple containing its pid
    and exit status indication: a 16-bit number, whose low byte is the signal number
    that killed the process, and whose high byte is the exit status (if the signal
    number is zero); the high bit of the low byte is set if a core file was
    produced.

    If there are no children that could be waited for, [`ChildProcessError`](exceptions.html#ChildProcessError "ChildProcessError")
    is raised.

    [`waitstatus_to_exitcode()`](#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the exit status into an
    exit code.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    See also

    The other `wait*()` functions documented below can be used to wait for the
    completion of a specific child process and have more options.
    [`waitpid()`](#os.waitpid "os.waitpid") is the only one also available on Windows.

os.waitid(*idtype*, *id*, *options*, */*)[¶](#os.waitid "Link to this definition")
:   Wait for the completion of a child process.

    *idtype* can be [`P_PID`](#os.P_PID "os.P_PID"), [`P_PGID`](#os.P_PGID "os.P_PGID"), [`P_ALL`](#os.P_ALL "os.P_ALL"), or (on Linux) [`P_PIDFD`](#os.P_PIDFD "os.P_PIDFD").
    The interpretation of *id* depends on it; see their individual descriptions.

    *options* is an OR combination of flags. At least one of [`WEXITED`](#os.WEXITED "os.WEXITED"),
    [`WSTOPPED`](#os.WSTOPPED "os.WSTOPPED") or [`WCONTINUED`](#os.WCONTINUED "os.WCONTINUED") is required;
    [`WNOHANG`](#os.WNOHANG "os.WNOHANG") and [`WNOWAIT`](#os.WNOWAIT "os.WNOWAIT") are additional optional flags.

    The return value is an object representing the data contained in the
    `siginfo_t` structure with the following attributes:

    * `si_pid` (process ID)
    * `si_uid` (real user ID of the child)
    * `si_signo` (always [`SIGCHLD`](signal.html#signal.SIGCHLD "signal.SIGCHLD"))
    * `si_status` (the exit status or signal number, depending on `si_code`)
    * `si_code` (see [`CLD_EXITED`](#os.CLD_EXITED "os.CLD_EXITED") for possible values)

    If [`WNOHANG`](#os.WNOHANG "os.WNOHANG") is specified and there are no matching children in the
    requested state, `None` is returned.
    Otherwise, if there are no matching children
    that could be waited for, [`ChildProcessError`](exceptions.html#ChildProcessError "ChildProcessError") is raised.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Note

    This function is not available on macOS.

    Added in version 3.3.

os.waitpid(*pid*, *options*, */*)[¶](#os.waitpid "Link to this definition")
:   The details of this function differ on Unix and Windows.

    On Unix: Wait for completion of a child process given by process id *pid*, and
    return a tuple containing its process id and exit status indication (encoded as
    for [`wait()`](#os.wait "os.wait")). The semantics of the call are affected by the value of the
    integer *options*, which should be `0` for normal operation.

    If *pid* is greater than `0`, [`waitpid()`](#os.waitpid "os.waitpid") requests status information for
    that specific process. If *pid* is `0`, the request is for the status of any
    child in the process group of the current process. If *pid* is `-1`, the
    request pertains to any child of the current process. If *pid* is less than
    `-1`, status is requested for any process in the process group `-pid` (the
    absolute value of *pid*).

    *options* is an OR combination of flags. If it contains [`WNOHANG`](#os.WNOHANG "os.WNOHANG") and
    there are no matching children in the requested state, `(0, 0)` is
    returned. Otherwise, if there are no matching children that could be waited
    for, [`ChildProcessError`](exceptions.html#ChildProcessError "ChildProcessError") is raised. Other options that can be used are
    [`WUNTRACED`](#os.WUNTRACED "os.WUNTRACED") and [`WCONTINUED`](#os.WCONTINUED "os.WCONTINUED").

    On Windows: Wait for completion of a process given by process handle *pid*, and
    return a tuple containing *pid*, and its exit status shifted left by 8 bits
    (shifting makes cross-platform use of the function easier). A *pid* less than or
    equal to `0` has no special meaning on Windows, and raises an exception. The
    value of integer *options* has no effect. *pid* can refer to any process whose
    id is known, not necessarily a child process. The [`spawn*`](#os.spawnl "os.spawnl")
    functions called with [`P_NOWAIT`](#os.P_NOWAIT "os.P_NOWAIT") return suitable process handles.

    [`waitstatus_to_exitcode()`](#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the exit status into an
    exit code.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

    Changed in version 3.5: If the system call is interrupted and the signal handler does not raise an
    exception, the function now retries the system call instead of raising an
    [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError") exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for the rationale).

os.wait3(*options*)[¶](#os.wait3 "Link to this definition")
:   Similar to [`waitpid()`](#os.waitpid "os.waitpid"), except no process id argument is given and a
    3-element tuple containing the child’s process id, exit status indication,
    and resource usage information is returned. Refer to
    [`resource.getrusage()`](resource.html#resource.getrusage "resource.getrusage") for details on resource usage information. The
    *options* argument is the same as that provided to [`waitpid()`](#os.waitpid "os.waitpid") and
    [`wait4()`](#os.wait4 "os.wait4").

    [`waitstatus_to_exitcode()`](#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the exit status into an
    exitcode.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.wait4(*pid*, *options*)[¶](#os.wait4 "Link to this definition")
:   Similar to [`waitpid()`](#os.waitpid "os.waitpid"), except a 3-element tuple, containing the child’s
    process id, exit status indication, and resource usage information is
    returned. Refer to [`resource.getrusage()`](resource.html#resource.getrusage "resource.getrusage") for details on resource usage
    information. The arguments to [`wait4()`](#os.wait4 "os.wait4") are the same as those provided
    to [`waitpid()`](#os.waitpid "os.waitpid").

    [`waitstatus_to_exitcode()`](#os.waitstatus_to_exitcode "os.waitstatus_to_exitcode") can be used to convert the exit status into an
    exitcode.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.P\_PID[¶](#os.P_PID "Link to this definition")

os.P\_PGID[¶](#os.P_PGID "Link to this definition")

os.P\_ALL[¶](#os.P_ALL "Link to this definition")

os.P\_PIDFD[¶](#os.P_PIDFD "Link to this definition")
:   These are the possible values for *idtype* in [`waitid()`](#os.waitid "os.waitid"). They affect
    how *id* is interpreted:

    * `P_PID` - wait for the child whose PID is *id*.
    * `P_PGID` - wait for any child whose progress group ID is *id*.
    * `P_ALL` - wait for any child; *id* is ignored.
    * `P_PIDFD` - wait for the child identified by the file descriptor
      *id* (a process file descriptor created with [`pidfd_open()`](#os.pidfd_open "os.pidfd_open")).

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Note

    `P_PIDFD` is only available on Linux >= 5.4.

    Added in version 3.3.

    Added in version 3.9: The `P_PIDFD` constant.

os.WCONTINUED[¶](#os.WCONTINUED "Link to this definition")
:   This *options* flag for [`waitpid()`](#os.waitpid "os.waitpid"), [`wait3()`](#os.wait3 "os.wait3"), [`wait4()`](#os.wait4 "os.wait4"), and
    [`waitid()`](#os.waitid "os.waitid") causes child processes to be reported if they have been
    continued from a job control stop since they were last reported.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WEXITED[¶](#os.WEXITED "Link to this definition")
:   This *options* flag for [`waitid()`](#os.waitid "os.waitid") causes child processes that have terminated to
    be reported.

    The other `wait*` functions always report children that have terminated,
    so this option is not available for them.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.WSTOPPED[¶](#os.WSTOPPED "Link to this definition")
:   This *options* flag for [`waitid()`](#os.waitid "os.waitid") causes child processes that have been stopped
    by the delivery of a signal to be reported.

    This option is not available for the other `wait*` functions.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

os.WUNTRACED[¶](#os.WUNTRACED "Link to this definition")
:   This *options* flag for [`waitpid()`](#os.waitpid "os.waitpid"), [`wait3()`](#os.wait3 "os.wait3"), and [`wait4()`](#os.wait4 "os.wait4") causes
    child processes to also be reported if they have been stopped but their
    current state has not been reported since they were stopped.

    This option is not available for [`waitid()`](#os.waitid "os.waitid").

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WNOHANG[¶](#os.WNOHANG "Link to this definition")
:   This *options* flag causes [`waitpid()`](#os.waitpid "os.waitpid"), [`wait3()`](#os.wait3 "os.wait3"), [`wait4()`](#os.wait4 "os.wait4"), and
    [`waitid()`](#os.waitid "os.waitid") to return right away if no child process status is available
    immediately.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WNOWAIT[¶](#os.WNOWAIT "Link to this definition")
:   This *options* flag causes [`waitid()`](#os.waitid "os.waitid") to leave the child in a waitable state, so that
    a later `wait*()` call can be used to retrieve the child status information again.

    This option is not available for the other `wait*` functions.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.CLD\_EXITED[¶](#os.CLD_EXITED "Link to this definition")

os.CLD\_KILLED[¶](#os.CLD_KILLED "Link to this definition")

os.CLD\_DUMPED[¶](#os.CLD_DUMPED "Link to this definition")

os.CLD\_TRAPPED[¶](#os.CLD_TRAPPED "Link to this definition")

os.CLD\_STOPPED[¶](#os.CLD_STOPPED "Link to this definition")

os.CLD\_CONTINUED[¶](#os.CLD_CONTINUED "Link to this definition")
:   These are the possible values for `si_code` in the result returned by
    [`waitid()`](#os.waitid "os.waitid").

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

    Added in version 3.3.

    Changed in version 3.9: Added [`CLD_KILLED`](#os.CLD_KILLED "os.CLD_KILLED") and [`CLD_STOPPED`](#os.CLD_STOPPED "os.CLD_STOPPED") values.

os.waitstatus\_to\_exitcode(*status*)[¶](#os.waitstatus_to_exitcode "Link to this definition")
:   Convert a wait status to an exit code.

    On Unix:

    * If the process exited normally (if `WIFEXITED(status)` is true),
      return the process exit status (return `WEXITSTATUS(status)`):
      result greater than or equal to 0.
    * If the process was terminated by a signal (if `WIFSIGNALED(status)` is
      true), return `-signum` where *signum* is the number of the signal that
      caused the process to terminate (return `-WTERMSIG(status)`):
      result less than 0.
    * Otherwise, raise a [`ValueError`](exceptions.html#ValueError "ValueError").

    On Windows, return *status* shifted right by 8 bits.

    On Unix, if the process is being traced or if [`waitpid()`](#os.waitpid "os.waitpid") was called
    with [`WUNTRACED`](#os.WUNTRACED "os.WUNTRACED") option, the caller must first check if
    `WIFSTOPPED(status)` is true. This function must not be called if
    `WIFSTOPPED(status)` is true.

    See also

    [`WIFEXITED()`](#os.WIFEXITED "os.WIFEXITED"), [`WEXITSTATUS()`](#os.WEXITSTATUS "os.WEXITSTATUS"), [`WIFSIGNALED()`](#os.WIFSIGNALED "os.WIFSIGNALED"),
    [`WTERMSIG()`](#os.WTERMSIG "os.WTERMSIG"), [`WIFSTOPPED()`](#os.WIFSTOPPED "os.WIFSTOPPED"), [`WSTOPSIG()`](#os.WSTOPSIG "os.WSTOPSIG") functions.

    [Availability](intro.html#availability): Unix, Windows, not Emscripten, not WASI.

    Added in version 3.9.

The following functions take a process status code as returned by
[`system()`](#os.system "os.system"), [`wait()`](#os.wait "os.wait"), or [`waitpid()`](#os.waitpid "os.waitpid") as a parameter. They may be
used to determine the disposition of a process.

os.WCOREDUMP(*status*, */*)[¶](#os.WCOREDUMP "Link to this definition")
:   Return `True` if a core dump was generated for the process, otherwise
    return `False`.

    This function should be employed only if [`WIFSIGNALED()`](#os.WIFSIGNALED "os.WIFSIGNALED") is true.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WIFCONTINUED(*status*)[¶](#os.WIFCONTINUED "Link to this definition")
:   Return `True` if a stopped child has been resumed by delivery of
    [`SIGCONT`](signal.html#signal.SIGCONT "signal.SIGCONT") (if the process has been continued from a job
    control stop), otherwise return `False`.

    See [`WCONTINUED`](#os.WCONTINUED "os.WCONTINUED") option.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WIFSTOPPED(*status*)[¶](#os.WIFSTOPPED "Link to this definition")
:   Return `True` if the process was stopped by delivery of a signal,
    otherwise return `False`.

    [`WIFSTOPPED()`](#os.WIFSTOPPED "os.WIFSTOPPED") only returns `True` if the [`waitpid()`](#os.waitpid "os.waitpid") call was
    done using [`WUNTRACED`](#os.WUNTRACED "os.WUNTRACED") option or when the process is being traced (see
    *[ptrace(2)](https://manpages.debian.org/ptrace(2))*).

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WIFSIGNALED(*status*)[¶](#os.WIFSIGNALED "Link to this definition")
:   Return `True` if the process was terminated by a signal, otherwise return
    `False`.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WIFEXITED(*status*)[¶](#os.WIFEXITED "Link to this definition")
:   Return `True` if the process exited terminated normally, that is,
    by calling `exit()` or `_exit()`, or by returning from `main()`;
    otherwise return `False`.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WEXITSTATUS(*status*)[¶](#os.WEXITSTATUS "Link to this definition")
:   Return the process exit status.

    This function should be employed only if [`WIFEXITED()`](#os.WIFEXITED "os.WIFEXITED") is true.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WSTOPSIG(*status*)[¶](#os.WSTOPSIG "Link to this definition")
:   Return the signal which caused the process to stop.

    This function should be employed only if [`WIFSTOPPED()`](#os.WIFSTOPPED "os.WIFSTOPPED") is true.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

os.WTERMSIG(*status*)[¶](#os.WTERMSIG "Link to this definition")
:   Return the number of the signal that caused the process to terminate.

    This function should be employed only if [`WIFSIGNALED()`](#os.WIFSIGNALED "os.WIFSIGNALED") is true.

    [Availability](intro.html#availability): Unix, not Emscripten, not WASI.

## Interface to the scheduler[¶](#interface-to-the-scheduler "Link to this heading")

These functions control how a process is allocated CPU time by the operating
system. They are only available on some Unix platforms. For more detailed
information, consult your Unix manpages.

Added in version 3.3.

The following scheduling policies are exposed if they are supported by the
operating system.

os.SCHED\_OTHER[¶](#os.SCHED_OTHER "Link to this definition")
:   The default scheduling policy.

os.SCHED\_BATCH[¶](#os.SCHED_BATCH "Link to this definition")
:   Scheduling policy for CPU-intensive processes that tries to preserve
    interactivity on the rest of the computer.

os.SCHED\_IDLE[¶](#os.SCHED_IDLE "Link to this definition")
:   Scheduling policy for extremely low priority background tasks.

os.SCHED\_SPORADIC[¶](#os.SCHED_SPORADIC "Link to this definition")
:   Scheduling policy for sporadic server programs.

os.SCHED\_FIFO[¶](#os.SCHED_FIFO "Link to this definition")
:   A First In First Out scheduling policy.

os.SCHED\_RR[¶](#os.SCHED_RR "Link to this definition")
:   A round-robin scheduling policy.

os.SCHED\_RESET\_ON\_FORK[¶](#os.SCHED_RESET_ON_FORK "Link to this definition")
:   This flag can be OR’ed with any other scheduling policy. When a process with
    this flag set forks, its child’s scheduling policy and priority are reset to
    the default.

*class* os.sched\_param(*sched\_priority*)[¶](#os.sched_param "Link to this definition")
:   This class represents tunable scheduling parameters used in
    [`sched_setparam()`](#os.sched_setparam "os.sched_setparam"), [`sched_setscheduler()`](#os.sched_setscheduler "os.sched_setscheduler"), and
    [`sched_getparam()`](#os.sched_getparam "os.sched_getparam"). It is immutable.

    At the moment, there is only one possible parameter:

    sched\_priority[¶](#os.sched_param.sched_priority "Link to this definition")
    :   The scheduling priority for a scheduling policy.

os.sched\_get\_priority\_min(*policy*)[¶](#os.sched_get_priority_min "Link to this definition")
:   Get the minimum priority value for *policy*. *policy* is one of the
    scheduling policy constants above.

os.sched\_get\_priority\_max(*policy*)[¶](#os.sched_get_priority_max "Link to this definition")
:   Get the maximum priority value for *policy*. *policy* is one of the
    scheduling policy constants above.

os.sched\_setscheduler(*pid*, *policy*, *param*, */*)[¶](#os.sched_setscheduler "Link to this definition")
:   Set the scheduling policy for the process with PID *pid*. A *pid* of 0 means
    the calling process. *policy* is one of the scheduling policy constants
    above. *param* is a [`sched_param`](#os.sched_param "os.sched_param") instance.

os.sched\_getscheduler(*pid*, */*)[¶](#os.sched_getscheduler "Link to this definition")
:   Return the scheduling policy for the process with PID *pid*. A *pid* of 0
    means the calling process. The result is one of the scheduling policy
    constants above.

os.sched\_setparam(*pid*, *param*, */*)[¶](#os.sched_setparam "Link to this definition")
:   Set the scheduling parameters for the process with PID *pid*. A *pid* of 0 means
    the calling process. *param* is a [`sched_param`](#os.sched_param "os.sched_param") instance.

os.sched\_getparam(*pid*, */*)[¶](#os.sched_getparam "Link to this definition")
:   Return the scheduling parameters as a [`sched_param`](#os.sched_param "os.sched_param") instance for the
    process with PID *pid*. A *pid* of 0 means the calling process.

os.sched\_rr\_get\_interval(*pid*, */*)[¶](#os.sched_rr_get_interval "Link to this definition")
:   Return the round-robin quantum in seconds for the process with PID *pid*. A
    *pid* of 0 means the calling process.

os.sched\_yield()[¶](#os.sched_yield "Link to this definition")
:   Voluntarily relinquish the CPU. See *[sched\_yield(2)](https://manpages.debian.org/sched_yield(2))* for details.

os.sched\_setaffinity(*pid*, *mask*, */*)[¶](#os.sched_setaffinity "Link to this definition")
:   Restrict the process with PID *pid* (or the current process if zero) to a
    set of CPUs. *mask* is an iterable of integers representing the set of
    CPUs to which the process should be restricted.

os.sched\_getaffinity(*pid*, */*)[¶](#os.sched_getaffinity "Link to this definition")
:   Return the set of CPUs the process with PID *pid* is restricted to.

    If *pid* is zero, return the set of CPUs the calling thread of the current
    process is restricted to.

## Miscellaneous System Information[¶](#miscellaneous-system-information "Link to this heading")

os.confstr(*name*, */*)[¶](#os.confstr "Link to this definition")
:   Return string-valued system configuration values. *name* specifies the
    configuration value to retrieve; it may be a string which is the name of a
    defined system value; these names are specified in a number of standards (POSIX,
    Unix 95, Unix 98, and others). Some platforms define additional names as well.
    The names known to the host operating system are given as the keys of the
    `confstr_names` dictionary. For configuration variables not included in that
    mapping, passing an integer for *name* is also accepted.

    If the configuration value specified by *name* isn’t defined, `None` is
    returned.

    If *name* is a string and is not known, [`ValueError`](exceptions.html#ValueError "ValueError") is raised. If a
    specific value for *name* is not supported by the host system, even if it is
    included in `confstr_names`, an [`OSError`](exceptions.html#OSError "OSError") is raised with
    [`errno.EINVAL`](errno.html#errno.EINVAL "errno.EINVAL") for the error number.

    [Availability](intro.html#availability): Unix.

os.confstr\_names[¶](#os.confstr_names "Link to this definition")
:   Dictionary mapping names accepted by [`confstr()`](#os.confstr "os.confstr") to the integer values
    defined for those names by the host operating system. This can be used to
    determine the set of names known to the system.

    [Availability](intro.html#availability): Unix.

os.cpu\_count()[¶](#os.cpu_count "Link to this definition")
:   Return the number of logical CPUs in the system. Returns `None` if
    undetermined.

    This number is not equivalent to the number of logical CPUs the current
    process can use. `len(os.sched_getaffinity(0))` gets the number of logical
    CPUs the calling thread of the current process is restricted to

    Added in version 3.4.

os.getloadavg()[¶](#os.getloadavg "Link to this definition")
:   Return the number of processes in the system run queue averaged over the last
    1, 5, and 15 minutes or raises [`OSError`](exceptions.html#OSError "OSError") if the load average was
    unobtainable.

    [Availability](intro.html#availability): Unix.

os.sysconf(*name*, */*)[¶](#os.sysconf "Link to this definition")
:   Return integer-valued system configuration values. If the configuration value
    specified by *name* isn’t defined, `-1` is returned. The comments regarding
    the *name* parameter for [`confstr()`](#os.confstr "os.confstr") apply here as well; the dictionary that
    provides information on the known names is given by `sysconf_names`.

    [Availability](intro.html#availability): Unix.

os.sysconf\_names[¶](#os.sysconf_names "Link to this definition")
:   Dictionary mapping names accepted by [`sysconf()`](#os.sysconf "os.sysconf") to the integer values
    defined for those names by the host operating system. This can be used to
    determine the set of names known to the system.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.11: Add `'SC_MINSIGSTKSZ'` name.

The following data values are used to support path manipulation operations. These
are defined for all platforms.

Higher-level operations on pathnames are defined in the [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.") module.

os.curdir[¶](#os.curdir "Link to this definition")
:   The constant string used by the operating system to refer to the current
    directory. This is `'.'` for Windows and POSIX. Also available via
    [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.pardir[¶](#os.pardir "Link to this definition")
:   The constant string used by the operating system to refer to the parent
    directory. This is `'..'` for Windows and POSIX. Also available via
    [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.sep[¶](#os.sep "Link to this definition")
:   The character used by the operating system to separate pathname components.
    This is `'/'` for POSIX and `'\\'` for Windows. Note that knowing this
    is not sufficient to be able to parse or concatenate pathnames — use
    [`os.path.split()`](os.path.html#os.path.split "os.path.split") and [`os.path.join()`](os.path.html#os.path.join "os.path.join") — but it is occasionally
    useful. Also available via [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.altsep[¶](#os.altsep "Link to this definition")
:   An alternative character used by the operating system to separate pathname
    components, or `None` if only one separator character exists. This is set to
    `'/'` on Windows systems where `sep` is a backslash. Also available via
    [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.extsep[¶](#os.extsep "Link to this definition")
:   The character which separates the base filename from the extension; for example,
    the `'.'` in `os.py`. Also available via [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.pathsep[¶](#os.pathsep "Link to this definition")
:   The character conventionally used by the operating system to separate search
    path components (as in `PATH`), such as `':'` for POSIX or `';'` for
    Windows. Also available via [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.defpath[¶](#os.defpath "Link to this definition")
:   The default search path used by [`exec*p*`](#os.execl "os.execl") and
    [`spawn*p*`](#os.spawnl "os.spawnl") if the environment doesn’t have a `'PATH'`
    key. Also available via [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.linesep[¶](#os.linesep "Link to this definition")
:   The string used to separate (or, rather, terminate) lines on the current
    platform. This may be a single character, such as `'\n'` for POSIX, or
    multiple characters, for example, `'\r\n'` for Windows. Do not use
    *os.linesep* as a line terminator when writing files opened in text mode (the
    default); use a single `'\n'` instead, on all platforms.

os.devnull[¶](#os.devnull "Link to this definition")
:   The file path of the null device. For example: `'/dev/null'` for
    POSIX, `'nul'` for Windows. Also available via [`os.path`](os.path.html#module-os.path "os.path: Operations on pathnames.").

os.RTLD\_LAZY[¶](#os.RTLD_LAZY "Link to this definition")

os.RTLD\_NOW[¶](#os.RTLD_NOW "Link to this definition")

os.RTLD\_GLOBAL[¶](#os.RTLD_GLOBAL "Link to this definition")

os.RTLD\_LOCAL[¶](#os.RTLD_LOCAL "Link to this definition")

os.RTLD\_NODELETE[¶](#os.RTLD_NODELETE "Link to this definition")

os.RTLD\_NOLOAD[¶](#os.RTLD_NOLOAD "Link to this definition")

os.RTLD\_DEEPBIND[¶](#os.RTLD_DEEPBIND "Link to this definition")
:   Flags for use with the [`setdlopenflags()`](sys.html#sys.setdlopenflags "sys.setdlopenflags") and
    [`getdlopenflags()`](sys.html#sys.getdlopenflags "sys.getdlopenflags") functions. See the Unix manual page
    *[dlopen(3)](https://manpages.debian.org/dlopen(3))* for what the different flags mean.

    Added in version 3.3.

## Random numbers[¶](#random-numbers "Link to this heading")

os.getrandom(*size*, *flags=0*)[¶](#os.getrandom "Link to this definition")
:   Get up to *size* random bytes. The function can return less bytes than
    requested.

    These bytes can be used to seed user-space random number generators or for
    cryptographic purposes.

    `getrandom()` relies on entropy gathered from device drivers and other
    sources of environmental noise. Unnecessarily reading large quantities of
    data will have a negative impact on other users of the `/dev/random` and
    `/dev/urandom` devices.

    The flags argument is a bit mask that can contain zero or more of the
    following values ORed together: [`os.GRND_RANDOM`](#os.GRND_RANDOM "os.GRND_RANDOM") and
    [`GRND_NONBLOCK`](#os.GRND_NONBLOCK "os.GRND_NONBLOCK").

    See also the [Linux getrandom() manual page](https://man7.org/linux/man-pages/man2/getrandom.2.html).

    [Availability](intro.html#availability): Linux >= 3.17.

    Added in version 3.6.

os.urandom(*size*, */*)[¶](#os.urandom "Link to this definition")
:   Return a bytestring of *size* random bytes suitable for cryptographic use.

    This function returns random bytes from an OS-specific randomness source. The
    returned data should be unpredictable enough for cryptographic applications,
    though its exact quality depends on the OS implementation.

    On Linux, if the `getrandom()` syscall is available, it is used in
    blocking mode: block until the system urandom entropy pool is initialized
    (128 bits of entropy are collected by the kernel). See the [**PEP 524**](https://peps.python.org/pep-0524/) for
    the rationale. On Linux, the [`getrandom()`](#os.getrandom "os.getrandom") function can be used to get
    random bytes in non-blocking mode (using the [`GRND_NONBLOCK`](#os.GRND_NONBLOCK "os.GRND_NONBLOCK") flag) or
    to poll until the system urandom entropy pool is initialized.

    On a Unix-like system, random bytes are read from the `/dev/urandom`
    device. If the `/dev/urandom` device is not available or not readable, the
    [`NotImplementedError`](exceptions.html#NotImplementedError "NotImplementedError") exception is raised.

    On Windows, it will use `BCryptGenRandom()`.

    See also

    The [`secrets`](secrets.html#module-secrets "secrets: Generate secure random numbers for managing secrets.") module provides higher level functions. For an
    easy-to-use interface to the random number generator provided by your
    platform, please see [`random.SystemRandom`](random.html#random.SystemRandom "random.SystemRandom").

    Changed in version 3.5: On Linux 3.17 and newer, the `getrandom()` syscall is now used
    when available. On OpenBSD 5.6 and newer, the C `getentropy()`
    function is now used. These functions avoid the usage of an internal file
    descriptor.

    Changed in version 3.5.2: On Linux, if the `getrandom()` syscall blocks (the urandom entropy pool
    is not initialized yet), fall back on reading `/dev/urandom`.

    Changed in version 3.6: On Linux, `getrandom()` is now used in blocking mode to increase the
    security.

    Changed in version 3.11: On Windows, `BCryptGenRandom()` is used instead of `CryptGenRandom()`
    which is deprecated.

os.GRND\_NONBLOCK[¶](#os.GRND_NONBLOCK "Link to this definition")
:   By default, when reading from `/dev/random`, [`getrandom()`](#os.getrandom "os.getrandom") blocks if
    no random bytes are available, and when reading from `/dev/urandom`, it blocks
    if the entropy pool has not yet been initialized.

    If the [`GRND_NONBLOCK`](#os.GRND_NONBLOCK "os.GRND_NONBLOCK") flag is set, then [`getrandom()`](#os.getrandom "os.getrandom") does not
    block in these cases, but instead immediately raises [`BlockingIOError`](exceptions.html#BlockingIOError "BlockingIOError").

    Added in version 3.6.

os.GRND\_RANDOM[¶](#os.GRND_RANDOM "Link to this definition")
:   If this bit is set, then random bytes are drawn from the
    `/dev/random` pool instead of the `/dev/urandom` pool.

    Added in version 3.6.

### [Table of Contents](../contents.html)

* [`os` — Miscellaneous operating system interfaces](#)
  + [File Names, Command Line Arguments, and Environment Variables](#file-names-command-line-arguments-and-environment-variables)
  + [Python UTF-8 Mode](#python-utf-8-mode)
  + [Process Parameters](#process-parameters)
  + [File Object Creation](#file-object-creation)
  + [File Descriptor Operations](#file-descriptor-operations)
    - [Querying the size of a terminal](#querying-the-size-of-a-terminal)
    - [Inheritance of File Descriptors](#inheritance-of-file-descriptors)
  + [Files and Directories](#files-and-directories)
    - [Linux extended attributes](#linux-extended-attributes)
  + [Process Management](#process-management)
  + [Interface to the scheduler](#interface-to-the-scheduler)
  + [Miscellaneous System Information](#miscellaneous-system-information)
  + [Random numbers](#random-numbers)

#### Previous topic

[Generic Operating System Services](allos.html "previous chapter")

#### Next topic

[`io` — Core tools for working with streams](io.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/os.rst)

«

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](io.html "io — Core tools for working with streams") |
* [previous](allos.html "Generic Operating System Services") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Generic Operating System Services](allos.html) »
* `os` — Miscellaneous operating system interfaces
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