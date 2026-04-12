# Python subprocess, signal, and asyncio subprocess


---

## 1. Subprocesses

**Source code:** [Lib/asyncio/subprocess.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/subprocess.py),
[Lib/asyncio/base\_subprocess.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/base_subprocess.py)

---

This section describes high-level async/await asyncio APIs to
create and manage subprocesses.

Here’s an example of how asyncio can run a shell command and
obtain its result:

```
importasyncio

async defrun(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(run('ls /zzz'))
```

will print:

```
['ls /zzz' exited with 1]
[stderr]
ls: /zzz: No such file or directory
```

Because all asyncio subprocess functions are asynchronous and asyncio
provides many tools to work with such functions, it is easy to execute
and monitor multiple subprocesses in parallel. It is indeed trivial
to modify the above example to run several commands simultaneously:

```
async defmain():
    await asyncio.gather(
        run('ls /zzz'),
        run('sleep 1; echo "hello"'))

asyncio.run(main())
```

See also the [Examples](#examples) subsection.

## Creating Subprocesses

*async*asyncio.create\_subprocess\_exec(*program*, *\*args*, *stdin=None*, *stdout=None*, *stderr=None*, *limit=None*, *\*\*kwds*)
:   Create a subprocess.

    The *limit* argument sets the buffer limit for [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")
    wrappers for [`stdout`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") and [`stderr`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr")
    (if [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") is passed to *stdout* and *stderr* arguments).

    Return a [`Process`](#asyncio.subprocess.Process "asyncio.subprocess.Process") instance.

    See the documentation of [`loop.subprocess_exec()`](asyncio-eventloop.html#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec") for other
    parameters.

    If the process object is garbage collected while the process is still
    running, the child process will be killed.

    Changed in version 3.10: Removed the *loop* parameter.

*async*asyncio.create\_subprocess\_shell(*cmd*, *stdin=None*, *stdout=None*, *stderr=None*, *limit=None*, *\*\*kwds*)
:   Run the *cmd* shell command.

    The *limit* argument sets the buffer limit for [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")
    wrappers for [`stdout`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") and [`stderr`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr")
    (if [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") is passed to *stdout* and *stderr* arguments).

    Return a [`Process`](#asyncio.subprocess.Process "asyncio.subprocess.Process") instance.

    See the documentation of [`loop.subprocess_shell()`](asyncio-eventloop.html#asyncio.loop.subprocess_shell "asyncio.loop.subprocess_shell") for other
    parameters.

    If the process object is garbage collected while the process is still
    running, the child process will be killed.

    Important

    It is the application’s responsibility to ensure that all whitespace and
    special characters are quoted appropriately to avoid [shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection)
    vulnerabilities. The [`shlex.quote()`](shlex.html#shlex.quote "shlex.quote") function can be used to properly
    escape whitespace and special shell characters in strings that are going
    to be used to construct shell commands.

    Changed in version 3.10: Removed the *loop* parameter.

Note

Subprocesses are available for Windows if a [`ProactorEventLoop`](asyncio-eventloop.html#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") is
used. See [Subprocess Support on Windows](asyncio-platforms.html#asyncio-windows-subprocess)
for details.

See also

asyncio also has the following *low-level* APIs to work with subprocesses:
[`loop.subprocess_exec()`](asyncio-eventloop.html#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec"), [`loop.subprocess_shell()`](asyncio-eventloop.html#asyncio.loop.subprocess_shell "asyncio.loop.subprocess_shell"),
[`loop.connect_read_pipe()`](asyncio-eventloop.html#asyncio.loop.connect_read_pipe "asyncio.loop.connect_read_pipe"), [`loop.connect_write_pipe()`](asyncio-eventloop.html#asyncio.loop.connect_write_pipe "asyncio.loop.connect_write_pipe"),
as well as the [Subprocess Transports](asyncio-protocol.html#asyncio-subprocess-transports)
and [Subprocess Protocols](asyncio-protocol.html#asyncio-subprocess-protocols).

## Constants

asyncio.subprocess.PIPE
:   Can be passed to the *stdin*, *stdout* or *stderr* parameters.

    If *PIPE* is passed to *stdin* argument, the
    [`Process.stdin`](#asyncio.subprocess.Process.stdin "asyncio.subprocess.Process.stdin") attribute
    will point to a [`StreamWriter`](asyncio-stream.html#asyncio.StreamWriter "asyncio.StreamWriter") instance.

    If *PIPE* is passed to *stdout* or *stderr* arguments, the
    [`Process.stdout`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") and
    [`Process.stderr`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr")
    attributes will point to [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader") instances.

asyncio.subprocess.STDOUT
:   Special value that can be used as the *stderr* argument and indicates
    that standard error should be redirected into standard output.

asyncio.subprocess.DEVNULL
:   Special value that can be used as the *stdin*, *stdout* or *stderr* argument
    to process creation functions. It indicates that the special file
    [`os.devnull`](os.html#os.devnull "os.devnull") will be used for the corresponding subprocess stream.

## Interacting with Subprocesses

Both [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") and [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell")
functions return instances of the *Process* class. *Process* is a high-level
wrapper that allows communicating with subprocesses and watching for
their completion.

*class*asyncio.subprocess.Process
:   An object that wraps OS processes created by the
    [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") and [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell")
    functions.

    This class is designed to have a similar API to the
    [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen") class, but there are some
    notable differences:

    * unlike Popen, Process instances do not have an equivalent to
      the [`poll()`](subprocess.html#subprocess.Popen.poll "subprocess.Popen.poll") method;
    * the [`communicate()`](#asyncio.subprocess.Process.communicate "asyncio.subprocess.Process.communicate") and
      [`wait()`](#asyncio.subprocess.Process.wait "asyncio.subprocess.Process.wait") methods don’t have a
      *timeout* parameter: use the [`wait_for()`](asyncio-task.html#asyncio.wait_for "asyncio.wait_for") function;
    * the [`Process.wait()`](#asyncio.subprocess.Process.wait "asyncio.subprocess.Process.wait") method
      is asynchronous, whereas [`subprocess.Popen.wait()`](subprocess.html#subprocess.Popen.wait "subprocess.Popen.wait") method
      is implemented as a blocking busy loop;
    * the *universal\_newlines* parameter is not supported.

    This class is [not thread safe](asyncio-dev.html#asyncio-multithreading).

    See also the [Subprocess and Threads](#asyncio-subprocess-threads)
    section.

    *async*wait()
    :   Wait for the child process to terminate.

        Set and return the [`returncode`](#asyncio.subprocess.Process.returncode "asyncio.subprocess.Process.returncode") attribute.

        Note

        This method can deadlock when using `stdout=PIPE` or
        `stderr=PIPE` and the child process generates so much output
        that it blocks waiting for the OS pipe buffer to accept
        more data. Use the [`communicate()`](#asyncio.subprocess.Process.communicate "asyncio.subprocess.Process.communicate") method when using pipes
        to avoid this condition.

    *async*communicate(*input=None*)
    :   Interact with process:

        1. send data to *stdin* (if *input* is not `None`);
        2. closes *stdin*;
        3. read data from *stdout* and *stderr*, until EOF is reached;
        4. wait for process to terminate.

        The optional *input* argument is the data ([`bytes`](stdtypes.html#bytes "bytes") object)
        that will be sent to the child process.

        Return a tuple `(stdout_data, stderr_data)`.

        If either [`BrokenPipeError`](exceptions.html#BrokenPipeError "BrokenPipeError") or [`ConnectionResetError`](exceptions.html#ConnectionResetError "ConnectionResetError")
        exception is raised when writing *input* into *stdin*, the
        exception is ignored. This condition occurs when the process
        exits before all data are written into *stdin*.

        If it is desired to send data to the process’ *stdin*,
        the process needs to be created with `stdin=PIPE`. Similarly,
        to get anything other than `None` in the result tuple, the
        process has to be created with `stdout=PIPE` and/or
        `stderr=PIPE` arguments.

        Note, that the data read is buffered in memory, so do not use
        this method if the data size is large or unlimited.

        Changed in version 3.12: *stdin* gets closed when `input=None` too.

    send\_signal(*signal*)
    :   Sends the signal *signal* to the child process.

        Note

        On Windows, [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM") is an alias for [`terminate()`](#asyncio.subprocess.Process.terminate "asyncio.subprocess.Process.terminate").
        `CTRL_C_EVENT` and `CTRL_BREAK_EVENT` can be sent to processes
        started with a *creationflags* parameter which includes
        `CREATE_NEW_PROCESS_GROUP`.

    terminate()
    :   Stop the child process.

        On POSIX systems this method sends [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM") to the
        child process.

        On Windows the Win32 API function `TerminateProcess()` is
        called to stop the child process.

    kill()
    :   Kill the child process.

        On POSIX systems this method sends [`SIGKILL`](signal.html#signal.SIGKILL "signal.SIGKILL") to the child
        process.

        On Windows this method is an alias for [`terminate()`](#asyncio.subprocess.Process.terminate "asyncio.subprocess.Process.terminate").

    stdin
    :   Standard input stream ([`StreamWriter`](asyncio-stream.html#asyncio.StreamWriter "asyncio.StreamWriter")) or `None`
        if the process was created with `stdin=None`.

    stdout
    :   Standard output stream ([`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")) or `None`
        if the process was created with `stdout=None`.

    stderr
    :   Standard error stream ([`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader")) or `None`
        if the process was created with `stderr=None`.

    Warning

    Use the [`communicate()`](#asyncio.subprocess.Process.communicate "asyncio.subprocess.Process.communicate") method rather than
    [`process.stdin.write()`](#asyncio.subprocess.Process.stdin "asyncio.subprocess.Process.stdin"),
    [`await process.stdout.read()`](#asyncio.subprocess.Process.stdout "asyncio.subprocess.Process.stdout") or
    [`await process.stderr.read()`](#asyncio.subprocess.Process.stderr "asyncio.subprocess.Process.stderr").
    This avoids deadlocks due to streams pausing reading or writing
    and blocking the child process.

    pid
    :   Process identification number (PID).

        Note that for processes created by the [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell")
        function, this attribute is the PID of the spawned shell.

    returncode
    :   Return code of the process when it exits.

        A `None` value indicates that the process has not terminated yet.

        For processes created with [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec"), a negative
        value `-N` indicates that the child was terminated by signal `N`
        (POSIX only).

        For processes created with [`create_subprocess_shell()`](#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell"), the
        return code reflects the exit status of the shell itself (e.g. `/bin/sh`),
        which may map signals to codes such as `128+N`. See the
        documentation of the shell (for example, the Bash manual’s Exit Status)
        for details.

### Subprocess and Threads

Standard asyncio event loop supports running subprocesses from different threads by
default.

On Windows subprocesses are provided by [`ProactorEventLoop`](asyncio-eventloop.html#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") only (default),
[`SelectorEventLoop`](asyncio-eventloop.html#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") has no subprocess support.

Note that alternative event loop implementations might have own limitations;
please refer to their documentation.

See also

The [Concurrency and multithreading in asyncio](asyncio-dev.html#asyncio-multithreading) section.

### Examples

An example using the [`Process`](#asyncio.subprocess.Process "asyncio.subprocess.Process") class to
control a subprocess and the [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader") class to read from
its standard output.

The subprocess is created by the [`create_subprocess_exec()`](#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec")
function:

```
importasyncio
importsys

async defget_date():
    code = 'import datetime as dt; print(dt.datetime.now())'

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit.
    await proc.wait()
    return line

date = asyncio.run(get_date())
print(f"Current date: {date}")
```

See also the [same example](asyncio-protocol.html#asyncio-example-subprocess-proto)
written using low-level APIs.

---

## 2. `subprocess` — Subprocess management

**Source code:** [Lib/subprocess.py](https://github.com/python/cpython/tree/3.14/Lib/subprocess.py)

---

The `subprocess` module allows you to spawn new processes, connect to their
input/output/error pipes, and obtain their return codes. This module intends to
replace several older modules and functions:

```
os.system
os.spawn*
```

Information about how the `subprocess` module can be used to replace these
modules and functions can be found in the following sections.

See also

[**PEP 324**](https://peps.python.org/pep-0324/) – PEP proposing the subprocess module

[Availability](intro.html#availability): not Android, not iOS, not WASI.

This module is not supported on [mobile platforms](intro.html#mobile-availability)
or [WebAssembly platforms](intro.html#wasm-availability).

## Using the `subprocess` Module

The recommended approach to invoking subprocesses is to use the [`run()`](#subprocess.run "subprocess.run")
function for all use cases it can handle. For more advanced use cases, the
underlying [`Popen`](#subprocess.Popen "subprocess.Popen") interface can be used directly.

subprocess.run(*args*, *\**, *stdin=None*, *input=None*, *stdout=None*, *stderr=None*, *capture\_output=False*, *shell=False*, *cwd=None*, *timeout=None*, *check=False*, *encoding=None*, *errors=None*, *text=None*, *env=None*, *universal\_newlines=None*, *\*\*other\_popen\_kwargs*)
:   Run the command described by *args*. Wait for command to complete, then
    return a [`CompletedProcess`](#subprocess.CompletedProcess "subprocess.CompletedProcess") instance.

    The arguments shown above are merely the most common ones, described below
    in [Frequently Used Arguments](#frequently-used-arguments) (hence the use of keyword-only notation
    in the abbreviated signature). The full function signature is largely the
    same as that of the [`Popen`](#subprocess.Popen "subprocess.Popen") constructor - most of the arguments to
    this function are passed through to that interface. (*timeout*, *input*,
    *check*, and *capture\_output* are not.)

    If *capture\_output* is true, stdout and stderr will be captured.
    When used, the internal [`Popen`](#subprocess.Popen "subprocess.Popen") object is automatically created with
    *stdout* and *stderr* both set to [`PIPE`](#subprocess.PIPE "subprocess.PIPE").
    The *stdout* and *stderr* arguments may not be supplied at the same time as *capture\_output*.
    If you wish to capture and combine both streams into one,
    set *stdout* to `PIPE`
    and *stderr* to [`STDOUT`](#subprocess.STDOUT "subprocess.STDOUT"),
    instead of using *capture\_output*.

    A *timeout* may be specified in seconds, it is internally passed on to
    [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate"). If the timeout expires, the child process will be
    killed and waited for. The [`TimeoutExpired`](#subprocess.TimeoutExpired "subprocess.TimeoutExpired") exception will be
    re-raised after the child process has terminated. The initial process
    creation itself cannot be interrupted on many platform APIs so you are not
    guaranteed to see a timeout exception until at least after however long
    process creation takes.

    The *input* argument is passed to [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate") and thus to the
    subprocess’s stdin. If used it must be a byte sequence, or a string if
    *encoding* or *errors* is specified or *text* is true. When
    used, the internal [`Popen`](#subprocess.Popen "subprocess.Popen") object is automatically created with
    *stdin* set to [`PIPE`](#subprocess.PIPE "subprocess.PIPE"),
    and the *stdin* argument may not be used as well.

    If *check* is true, and the process exits with a non-zero exit code, a
    [`CalledProcessError`](#subprocess.CalledProcessError "subprocess.CalledProcessError") exception will be raised. Attributes of that
    exception hold the arguments, the exit code, and stdout and stderr if they
    were captured.

    If *encoding* or *errors* are specified, or *text* is true,
    file objects for stdin, stdout and stderr are opened in text mode using the
    specified *encoding* and *errors* or the [`io.TextIOWrapper`](io.html#io.TextIOWrapper "io.TextIOWrapper") default.
    The *universal\_newlines* argument is equivalent to *text* and is provided
    for backwards compatibility. By default, file objects are opened in binary mode.

    If *env* is not `None`, it must be a mapping that defines the environment
    variables for the new process; these are used instead of the default
    behavior of inheriting the current process’ environment. It is passed
    directly to [`Popen`](#subprocess.Popen "subprocess.Popen"). This mapping can be str to str on any platform
    or bytes to bytes on POSIX platforms much like [`os.environ`](os.html#os.environ "os.environ") or
    [`os.environb`](os.html#os.environb "os.environb").

    Examples:

    ```
    >>> subprocess.run(["ls", "-l"])  # doesn't capture output
    CompletedProcess(args=['ls', '-l'], returncode=0)

    >>> subprocess.run("exit 1", shell=True, check=True)
    Traceback (most recent call last):
    ...
    subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1

    >>> subprocess.run(["ls", "-l", "/dev/null"], capture_output=True)
    CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0,
    stdout=b'crw-rw-rw- 1 root root 1, 3 Jan 23 16:23 /dev/null\n', stderr=b'')
    ```

    Added in version 3.5.

    Changed in version 3.6: Added *encoding* and *errors* parameters

    Changed in version 3.7: Added the *text* parameter, as a more understandable alias of *universal\_newlines*.
    Added the *capture\_output* parameter.

    Changed in version 3.12: Changed Windows shell search order for `shell=True`. The current
    directory and `%PATH%` are replaced with `%COMSPEC%` and
    `%SystemRoot%\System32\cmd.exe`. As a result, dropping a
    malicious program named `cmd.exe` into a current directory no
    longer works.

*class*subprocess.CompletedProcess
:   The return value from [`run()`](#subprocess.run "subprocess.run"), representing a process that has finished.

    args
    :   The arguments used to launch the process. This may be a list or a string.

    returncode
    :   Exit status of the child process. Typically, an exit status of 0 indicates
        that it ran successfully.

        A negative value `-N` indicates that the child was terminated by signal
        `N` (POSIX only).

    stdout
    :   Captured stdout from the child process. A bytes sequence, or a string if
        [`run()`](#subprocess.run "subprocess.run") was called with an encoding, errors, or text=True.
        `None` if stdout was not captured.

        If you ran the process with `stderr=subprocess.STDOUT`, stdout and
        stderr will be combined in this attribute, and [`stderr`](#subprocess.CompletedProcess.stderr "subprocess.CompletedProcess.stderr") will be
        `None`.

    stderr
    :   Captured stderr from the child process. A bytes sequence, or a string if
        [`run()`](#subprocess.run "subprocess.run") was called with an encoding, errors, or text=True.
        `None` if stderr was not captured.

    check\_returncode()
    :   If [`returncode`](#subprocess.CompletedProcess.returncode "subprocess.CompletedProcess.returncode") is non-zero, raise a [`CalledProcessError`](#subprocess.CalledProcessError "subprocess.CalledProcessError").

    Added in version 3.5.

subprocess.DEVNULL
:   Special value that can be used as the *stdin*, *stdout* or *stderr* argument
    to [`Popen`](#subprocess.Popen "subprocess.Popen") and indicates that the special file [`os.devnull`](os.html#os.devnull "os.devnull")
    will be used.

    Added in version 3.3.

subprocess.PIPE
:   Special value that can be used as the *stdin*, *stdout* or *stderr* argument
    to [`Popen`](#subprocess.Popen "subprocess.Popen") and indicates that a pipe to the standard stream should be
    opened. Most useful with [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate").

subprocess.STDOUT
:   Special value that can be used as the *stderr* argument to [`Popen`](#subprocess.Popen "subprocess.Popen") and
    indicates that standard error should go into the same handle as standard
    output.

*exception*subprocess.SubprocessError
:   Base class for all other exceptions from this module.

    Added in version 3.3.

*exception*subprocess.TimeoutExpired
:   Subclass of [`SubprocessError`](#subprocess.SubprocessError "subprocess.SubprocessError"), raised when a timeout expires
    while waiting for a child process.

    cmd
    :   Command that was used to spawn the child process.

    timeout
    :   Timeout in seconds.

    output
    :   Output of the child process if it was captured by [`run()`](#subprocess.run "subprocess.run") or
        [`check_output()`](#subprocess.check_output "subprocess.check_output"). Otherwise, `None`. This is always
        [`bytes`](stdtypes.html#bytes "bytes") when any output was captured regardless of the
        `text=True` setting. It may remain `None` instead of `b''`
        when no output was observed.

    stdout
    :   Alias for output, for symmetry with [`stderr`](#subprocess.TimeoutExpired.stderr "subprocess.TimeoutExpired.stderr").

    stderr
    :   Stderr output of the child process if it was captured by [`run()`](#subprocess.run "subprocess.run").
        Otherwise, `None`. This is always [`bytes`](stdtypes.html#bytes "bytes") when stderr output
        was captured regardless of the `text=True` setting. It may remain
        `None` instead of `b''` when no stderr output was observed.

    Added in version 3.3.

    Changed in version 3.5: *stdout* and *stderr* attributes added

*exception*subprocess.CalledProcessError
:   Subclass of [`SubprocessError`](#subprocess.SubprocessError "subprocess.SubprocessError"), raised when a process run by
    [`check_call()`](#subprocess.check_call "subprocess.check_call"), [`check_output()`](#subprocess.check_output "subprocess.check_output"), or [`run()`](#subprocess.run "subprocess.run") (with `check=True`)
    returns a non-zero exit status.

    returncode
    :   Exit status of the child process. If the process exited due to a
        signal, this will be the negative signal number.

    cmd
    :   Command that was used to spawn the child process.

    output
    :   Output of the child process if it was captured by [`run()`](#subprocess.run "subprocess.run") or
        [`check_output()`](#subprocess.check_output "subprocess.check_output"). Otherwise, `None`.

    stdout
    :   Alias for output, for symmetry with [`stderr`](#subprocess.CalledProcessError.stderr "subprocess.CalledProcessError.stderr").

    stderr
    :   Stderr output of the child process if it was captured by [`run()`](#subprocess.run "subprocess.run").
        Otherwise, `None`.

    Changed in version 3.5: *stdout* and *stderr* attributes added

### Frequently Used Arguments

To support a wide variety of use cases, the [`Popen`](#subprocess.Popen "subprocess.Popen") constructor (and
the convenience functions) accept a large number of optional arguments. For
most typical use cases, many of these arguments can be safely left at their
default values. The arguments that are most commonly needed are:

> *args* is required for all calls and should be a string, or a sequence of
> program arguments. Providing a sequence of arguments is generally
> preferred, as it allows the module to take care of any required escaping
> and quoting of arguments (e.g. to permit spaces in file names). If passing
> a single string, either *shell* must be [`True`](constants.html#True "True") (see below) or else
> the string must simply name the program to be executed without specifying
> any arguments.
>
> *stdin*, *stdout* and *stderr* specify the executed program’s standard input,
> standard output and standard error file handles, respectively. Valid values
> are `None`, [`PIPE`](#subprocess.PIPE "subprocess.PIPE"), [`DEVNULL`](#subprocess.DEVNULL "subprocess.DEVNULL"), an existing file descriptor (a
> positive integer), and an existing [file object](../glossary.html#term-file-object) with a valid file
> descriptor. With the default settings of `None`, no redirection will
> occur. `PIPE` indicates that a new pipe to the child should be
> created. `DEVNULL` indicates that the special file [`os.devnull`](os.html#os.devnull "os.devnull")
> will be used. Additionally, *stderr* can be [`STDOUT`](#subprocess.STDOUT "subprocess.STDOUT"), which indicates
> that the stderr data from the child process should be captured into the same
> file handle as for *stdout*.
>
> If *encoding* or *errors* are specified, or *text* (also known as
> *universal\_newlines*) is true,
> the file objects *stdin*, *stdout* and *stderr* will be opened in text
> mode using the *encoding* and *errors* specified in the call or the
> defaults for [`io.TextIOWrapper`](io.html#io.TextIOWrapper "io.TextIOWrapper").
>
> For *stdin*, line ending characters `'\n'` in the input will be converted
> to the default line separator [`os.linesep`](os.html#os.linesep "os.linesep"). For *stdout* and *stderr*,
> all line endings in the output will be converted to `'\n'`. For more
> information see the documentation of the [`io.TextIOWrapper`](io.html#io.TextIOWrapper "io.TextIOWrapper") class
> when the *newline* argument to its constructor is `None`.
>
> If text mode is not used, *stdin*, *stdout* and *stderr* will be opened as
> binary streams. No encoding or line ending conversion is performed.
>
> Changed in version 3.6: Added the *encoding* and *errors* parameters.
>
> Changed in version 3.7: Added the *text* parameter as an alias for *universal\_newlines*.
>
> Note
>
> The newlines attribute of the file objects [`Popen.stdin`](#subprocess.Popen.stdin "subprocess.Popen.stdin"),
> [`Popen.stdout`](#subprocess.Popen.stdout "subprocess.Popen.stdout") and [`Popen.stderr`](#subprocess.Popen.stderr "subprocess.Popen.stderr") are not updated by
> the [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate") method.
>
> If *shell* is `True`, the specified command will be executed through
> the shell. This can be useful if you are using Python primarily for the
> enhanced control flow it offers over most system shells and still want
> convenient access to other shell features such as shell pipes, filename
> wildcards, environment variable expansion, and expansion of `~` to a
> user’s home directory. However, note that Python itself offers
> implementations of many shell-like features (in particular, [`glob`](glob.html#module-glob "glob: Unix shell style pathname pattern expansion."),
> [`fnmatch`](fnmatch.html#module-fnmatch "fnmatch: Unix shell style filename pattern matching."), [`os.walk()`](os.html#os.walk "os.walk"), [`os.path.expandvars()`](os.path.html#os.path.expandvars "os.path.expandvars"),
> [`os.path.expanduser()`](os.path.html#os.path.expanduser "os.path.expanduser"), and [`shutil`](shutil.html#module-shutil "shutil: High-level file operations, including copying.")).
>
> Changed in version 3.3: When *universal\_newlines* is `True`, the class uses the encoding
> [`locale.getpreferredencoding(False)`](locale.html#locale.getpreferredencoding "locale.getpreferredencoding")
> instead of `locale.getpreferredencoding()`. See the
> [`io.TextIOWrapper`](io.html#io.TextIOWrapper "io.TextIOWrapper") class for more information on this change.
>
> Note
>
> Read the [Security Considerations](#security-considerations) section before using `shell=True`.

These options, along with all of the other options, are described in more
detail in the [`Popen`](#subprocess.Popen "subprocess.Popen") constructor documentation.

### Popen Constructor

The underlying process creation and management in this module is handled by
the [`Popen`](#subprocess.Popen "subprocess.Popen") class. It offers a lot of flexibility so that developers
are able to handle the less common cases not covered by the convenience
functions.

*class*subprocess.Popen(*args*, *bufsize=-1*, *executable=None*, *stdin=None*, *stdout=None*, *stderr=None*, *preexec\_fn=None*, *close\_fds=True*, *shell=False*, *cwd=None*, *env=None*, *universal\_newlines=None*, *startupinfo=None*, *creationflags=0*, *restore\_signals=True*, *start\_new\_session=False*, *pass\_fds=()*, *\**, *group=None*, *extra\_groups=None*, *user=None*, *umask=-1*, *encoding=None*, *errors=None*, *text=None*, *pipesize=-1*, *process\_group=None*)
:   Execute a child program in a new process. On POSIX, the class uses
    [`os.execvpe()`](os.html#os.execvpe "os.execvpe")-like behavior to execute the child program. On Windows,
    the class uses the Windows `CreateProcess()` function. The arguments to
    `Popen` are as follows.

    *args* should be a sequence of program arguments or else a single string
    or [path-like object](../glossary.html#term-path-like-object).
    By default, the program to execute is the first item in *args* if *args* is
    a sequence. If *args* is a string, the interpretation is
    platform-dependent and described below. See the *shell* and *executable*
    arguments for additional differences from the default behavior. Unless
    otherwise stated, it is recommended to pass *args* as a sequence.

    Warning

    For maximum reliability, use a fully qualified path for the executable.
    To search for an unqualified name on `PATH`, use
    [`shutil.which()`](shutil.html#shutil.which "shutil.which"). On all platforms, passing [`sys.executable`](sys.html#sys.executable "sys.executable")
    is the recommended way to launch the current Python interpreter again,
    and use the `-m` command-line format to launch an installed module.

    Resolving the path of *executable* (or the first item of *args*) is
    platform dependent. For POSIX, see [`os.execvpe()`](os.html#os.execvpe "os.execvpe"), and note that
    when resolving or searching for the executable path, *cwd* overrides the
    current working directory and *env* can override the `PATH`
    environment variable. For Windows, see the documentation of the
    `lpApplicationName` and `lpCommandLine` parameters of WinAPI
    `CreateProcess`, and note that when resolving or searching for the
    executable path with `shell=False`, *cwd* does not override the
    current working directory and *env* cannot override the `PATH`
    environment variable. Using a full path avoids all of these variations.

    An example of passing some arguments to an external program
    as a sequence is:

    ```
    Popen(["/usr/bin/git", "commit", "-m", "Fixes a bug."])
    ```

    On POSIX, if *args* is a string, the string is interpreted as the name or
    path of the program to execute. However, this can only be done if not
    passing arguments to the program.

    Note

    It may not be obvious how to break a shell command into a sequence of arguments,
    especially in complex cases. [`shlex.split()`](shlex.html#shlex.split "shlex.split") can illustrate how to
    determine the correct tokenization for *args*:

    ```
    >>> importshlex,subprocess
    >>> command_line = input()
    /bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
    >>> args = shlex.split(command_line)
    >>> print(args)
    ['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
    >>> p = subprocess.Popen(args) # Success!
    ```

    Note in particular that options (such as *-input*) and arguments (such
    as *eggs.txt*) that are separated by whitespace in the shell go in separate
    list elements, while arguments that need quoting or backslash escaping when
    used in the shell (such as filenames containing spaces or the *echo* command
    shown above) are single list elements.

    On Windows, if *args* is a sequence, it will be converted to a string in a
    manner described in [Converting an argument sequence to a string on Windows](#converting-argument-sequence). This is because
    the underlying `CreateProcess()` operates on strings.

    Changed in version 3.6: *args* parameter accepts a [path-like object](../glossary.html#term-path-like-object) if *shell* is
    `False` and a sequence containing path-like objects on POSIX.

    Changed in version 3.8: *args* parameter accepts a [path-like object](../glossary.html#term-path-like-object) if *shell* is
    `False` and a sequence containing bytes and path-like objects
    on Windows.

    The *shell* argument (which defaults to `False`) specifies whether to use
    the shell as the program to execute. If *shell* is `True`, it is
    recommended to pass *args* as a string rather than as a sequence.

    On POSIX with `shell=True`, the shell defaults to `/bin/sh`. If
    *args* is a string, the string specifies the command
    to execute through the shell. This means that the string must be
    formatted exactly as it would be when typed at the shell prompt. This
    includes, for example, quoting or backslash escaping filenames with spaces in
    them. If *args* is a sequence, the first item specifies the command string, and
    any additional items will be treated as additional arguments to the shell
    itself. That is to say, `Popen` does the equivalent of:

    ```
    Popen(['/bin/sh', '-c', args[0], args[1], ...])
    ```

    On Windows with `shell=True`, the `COMSPEC` environment variable
    specifies the default shell. The only time you need to specify
    `shell=True` on Windows is when the command you wish to execute is built
    into the shell (e.g. **dir** or **copy**). You do not need
    `shell=True` to run a batch file or console-based executable.

    Note

    Read the [Security Considerations](#security-considerations) section before using `shell=True`.

    *bufsize* will be supplied as the corresponding argument to the
    [`open()`](functions.html#open "open") function when creating the stdin/stdout/stderr pipe
    file objects:

    * `0` means unbuffered (read and write are one
      system call and can return short)
    * `1` means line buffered
      (only usable if `text=True` or `universal_newlines=True`)
    * any other positive value means use a buffer of approximately that
      size
    * negative bufsize (the default) means the system default of
      io.DEFAULT\_BUFFER\_SIZE will be used.

    Changed in version 3.3.1: *bufsize* now defaults to -1 to enable buffering by default to match the
    behavior that most code expects. In versions prior to Python 3.2.4 and
    3.3.1 it incorrectly defaulted to `0` which was unbuffered
    and allowed short reads. This was unintentional and did not match the
    behavior of Python 2 as most code expected.

    The *executable* argument specifies a replacement program to execute. It
    is very seldom needed. When `shell=False`, *executable* replaces the
    program to execute specified by *args*. However, the original *args* is
    still passed to the program. Most programs treat the program specified
    by *args* as the command name, which can then be different from the program
    actually executed. On POSIX, the *args* name
    becomes the display name for the executable in utilities such as
    **ps**. If `shell=True`, on POSIX the *executable* argument
    specifies a replacement shell for the default `/bin/sh`.

    Changed in version 3.6: *executable* parameter accepts a [path-like object](../glossary.html#term-path-like-object) on POSIX.

    Changed in version 3.8: *executable* parameter accepts a bytes and [path-like object](../glossary.html#term-path-like-object)
    on Windows.

    Changed in version 3.12: Changed Windows shell search order for `shell=True`. The current
    directory and `%PATH%` are replaced with `%COMSPEC%` and
    `%SystemRoot%\System32\cmd.exe`. As a result, dropping a
    malicious program named `cmd.exe` into a current directory no
    longer works.

    *stdin*, *stdout* and *stderr* specify the executed program’s standard input,
    standard output and standard error file handles, respectively. Valid values
    are `None`, [`PIPE`](#subprocess.PIPE "subprocess.PIPE"), [`DEVNULL`](#subprocess.DEVNULL "subprocess.DEVNULL"), an existing file descriptor (a
    positive integer), and an existing [file object](../glossary.html#term-file-object) with a valid file
    descriptor. With the default settings of `None`, no redirection will
    occur. `PIPE` indicates that a new pipe to the child should be
    created. `DEVNULL` indicates that the special file [`os.devnull`](os.html#os.devnull "os.devnull")
    will be used. Additionally, *stderr* can be [`STDOUT`](#subprocess.STDOUT "subprocess.STDOUT"), which indicates
    that the stderr data from the applications should be captured into the same
    file handle as for *stdout*.

    If *preexec\_fn* is set to a callable object, this object will be called in the
    child process just before the child is executed.
    (POSIX only)

    Warning

    The *preexec\_fn* parameter is NOT SAFE to use in the presence of threads
    in your application. The child process could deadlock before exec is
    called.

    Note

    If you need to modify the environment for the child use the *env*
    parameter rather than doing it in a *preexec\_fn*.
    The *start\_new\_session* and *process\_group* parameters should take the place of
    code using *preexec\_fn* to call [`os.setsid()`](os.html#os.setsid "os.setsid") or [`os.setpgid()`](os.html#os.setpgid "os.setpgid") in the child.

    Changed in version 3.8: The *preexec\_fn* parameter is no longer supported in subinterpreters.
    The use of the parameter in a subinterpreter raises
    [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError"). The new restriction may affect applications that
    are deployed in mod\_wsgi, uWSGI, and other embedded environments.

    If *close\_fds* is true, all file descriptors except `0`, `1` and
    `2` will be closed before the child process is executed. Otherwise
    when *close\_fds* is false, file descriptors obey their inheritable flag
    as described in [Inheritance of File Descriptors](os.html#fd-inheritance).

    On Windows, if *close\_fds* is true then no handles will be inherited by the
    child process unless explicitly passed in the `handle_list` element of
    [`STARTUPINFO.lpAttributeList`](#subprocess.STARTUPINFO.lpAttributeList "subprocess.STARTUPINFO.lpAttributeList"), or by standard handle redirection.

    Changed in version 3.2: The default for *close\_fds* was changed from [`False`](constants.html#False "False") to
    what is described above.

    Changed in version 3.7: On Windows the default for *close\_fds* was changed from [`False`](constants.html#False "False") to
    [`True`](constants.html#True "True") when redirecting the standard handles. It’s now possible to
    set *close\_fds* to `True` when redirecting the standard handles.

    *pass\_fds* is an optional sequence of file descriptors to keep open
    between the parent and child. Providing any *pass\_fds* forces
    *close\_fds* to be [`True`](constants.html#True "True"). (POSIX only)

    Changed in version 3.2: The *pass\_fds* parameter was added.

    If *cwd* is not `None`, the function changes the working directory to
    *cwd* before executing the child. *cwd* can be a string, bytes or
    [path-like](../glossary.html#term-path-like-object) object. On POSIX, the function
    looks for *executable* (or for the first item in *args*) relative to *cwd*
    if the executable path is a relative path.

    Changed in version 3.6: *cwd* parameter accepts a [path-like object](../glossary.html#term-path-like-object) on POSIX.

    Changed in version 3.7: *cwd* parameter accepts a [path-like object](../glossary.html#term-path-like-object) on Windows.

    Changed in version 3.8: *cwd* parameter accepts a bytes object on Windows.

    If *restore\_signals* is true (the default) all signals that Python has set to
    SIG\_IGN are restored to SIG\_DFL in the child process before the exec.
    Currently this includes the SIGPIPE, SIGXFZ and SIGXFSZ signals.
    (POSIX only)

    Changed in version 3.2: *restore\_signals* was added.

    If *start\_new\_session* is true the `setsid()` system call will be made in the
    child process prior to the execution of the subprocess.

    [Availability](intro.html#availability): POSIX

    Changed in version 3.2: *start\_new\_session* was added.

    If *process\_group* is a non-negative integer, the `setpgid(0, value)` system call will
    be made in the child process prior to the execution of the subprocess.

    [Availability](intro.html#availability): POSIX

    Changed in version 3.11: *process\_group* was added.

    If *group* is not `None`, the setregid() system call will be made in the
    child process prior to the execution of the subprocess. If the provided
    value is a string, it will be looked up via [`grp.getgrnam()`](grp.html#grp.getgrnam "grp.getgrnam") and
    the value in `gr_gid` will be used. If the value is an integer, it
    will be passed verbatim. (POSIX only)

    [Availability](intro.html#availability): POSIX

    Added in version 3.9.

    If *extra\_groups* is not `None`, the setgroups() system call will be
    made in the child process prior to the execution of the subprocess.
    Strings provided in *extra\_groups* will be looked up via
    [`grp.getgrnam()`](grp.html#grp.getgrnam "grp.getgrnam") and the values in `gr_gid` will be used.
    Integer values will be passed verbatim. (POSIX only)

    [Availability](intro.html#availability): POSIX

    Added in version 3.9.

    If *user* is not `None`, the setreuid() system call will be made in the
    child process prior to the execution of the subprocess. If the provided
    value is a string, it will be looked up via [`pwd.getpwnam()`](pwd.html#pwd.getpwnam "pwd.getpwnam") and
    the value in `pw_uid` will be used. If the value is an integer, it will
    be passed verbatim. (POSIX only)

    Note

    Specifying *user* will not drop existing supplementary group memberships!
    The caller must also pass `extra_groups=()` to reduce the group membership
    of the child process for security purposes.

    [Availability](intro.html#availability): POSIX

    Added in version 3.9.

    If *umask* is not negative, the umask() system call will be made in the
    child process prior to the execution of the subprocess.

    [Availability](intro.html#availability): POSIX

    Added in version 3.9.

    If *env* is not `None`, it must be a mapping that defines the environment
    variables for the new process; these are used instead of the default
    behavior of inheriting the current process’ environment. This mapping can be
    str to str on any platform or bytes to bytes on POSIX platforms much like
    [`os.environ`](os.html#os.environ "os.environ") or [`os.environb`](os.html#os.environb "os.environb").

    Note

    If specified, *env* must provide any variables required for the program to
    execute. On Windows, in order to run a [side-by-side assembly](https://en.wikipedia.org/wiki/Side-by-Side_Assembly) the
    specified *env* **must** include a valid `%SystemRoot%`.

    If *encoding* or *errors* are specified, or *text* is true, the file objects
    *stdin*, *stdout* and *stderr* are opened in text mode with the specified
    *encoding* and *errors*, as described above in [Frequently Used Arguments](#frequently-used-arguments).
    The *universal\_newlines* argument is equivalent to *text* and is provided
    for backwards compatibility. By default, file objects are opened in binary mode.

    Added in version 3.6: *encoding* and *errors* were added.

    Added in version 3.7: *text* was added as a more readable alias for *universal\_newlines*.

    If given, *startupinfo* will be a [`STARTUPINFO`](#subprocess.STARTUPINFO "subprocess.STARTUPINFO") object, which is
    passed to the underlying `CreateProcess` function.

    If given, *creationflags*, can be one or more of the following flags:

    * [`CREATE_NEW_CONSOLE`](#subprocess.CREATE_NEW_CONSOLE "subprocess.CREATE_NEW_CONSOLE")
    * [`CREATE_NEW_PROCESS_GROUP`](#subprocess.CREATE_NEW_PROCESS_GROUP "subprocess.CREATE_NEW_PROCESS_GROUP")
    * [`ABOVE_NORMAL_PRIORITY_CLASS`](#subprocess.ABOVE_NORMAL_PRIORITY_CLASS "subprocess.ABOVE_NORMAL_PRIORITY_CLASS")
    * [`BELOW_NORMAL_PRIORITY_CLASS`](#subprocess.BELOW_NORMAL_PRIORITY_CLASS "subprocess.BELOW_NORMAL_PRIORITY_CLASS")
    * [`HIGH_PRIORITY_CLASS`](#subprocess.HIGH_PRIORITY_CLASS "subprocess.HIGH_PRIORITY_CLASS")
    * [`IDLE_PRIORITY_CLASS`](#subprocess.IDLE_PRIORITY_CLASS "subprocess.IDLE_PRIORITY_CLASS")
    * [`NORMAL_PRIORITY_CLASS`](#subprocess.NORMAL_PRIORITY_CLASS "subprocess.NORMAL_PRIORITY_CLASS")
    * [`REALTIME_PRIORITY_CLASS`](#subprocess.REALTIME_PRIORITY_CLASS "subprocess.REALTIME_PRIORITY_CLASS")
    * [`CREATE_NO_WINDOW`](#subprocess.CREATE_NO_WINDOW "subprocess.CREATE_NO_WINDOW")
    * [`DETACHED_PROCESS`](#subprocess.DETACHED_PROCESS "subprocess.DETACHED_PROCESS")
    * [`CREATE_DEFAULT_ERROR_MODE`](#subprocess.CREATE_DEFAULT_ERROR_MODE "subprocess.CREATE_DEFAULT_ERROR_MODE")
    * [`CREATE_BREAKAWAY_FROM_JOB`](#subprocess.CREATE_BREAKAWAY_FROM_JOB "subprocess.CREATE_BREAKAWAY_FROM_JOB")

    *pipesize* can be used to change the size of the pipe when
    [`PIPE`](#subprocess.PIPE "subprocess.PIPE") is used for *stdin*, *stdout* or *stderr*. The size of the pipe
    is only changed on platforms that support this (only Linux at this time of
    writing). Other platforms will ignore this parameter.

    Changed in version 3.10: Added the *pipesize* parameter.

    Popen objects are supported as context managers via the [`with`](../reference/compound_stmts.html#with) statement:
    on exit, standard file descriptors are closed, and the process is waited for.

    ```
    with Popen(["ifconfig"], stdout=PIPE) as proc:
        log.write(proc.stdout.read())
    ```

    Popen and the other functions in this module that use it raise an
    [auditing event](sys.html#auditing) `subprocess.Popen` with arguments
    `executable`, `args`, `cwd`, and `env`. The value for `args`
    may be a single string or a list of strings, depending on platform.

    Changed in version 3.2: Added context manager support.

    Changed in version 3.6: Popen destructor now emits a [`ResourceWarning`](exceptions.html#ResourceWarning "ResourceWarning") warning if the child
    process is still running.

    Changed in version 3.8: Popen can use [`os.posix_spawn()`](os.html#os.posix_spawn "os.posix_spawn") in some cases for better
    performance. On Windows Subsystem for Linux and QEMU User Emulation,
    Popen constructor using `os.posix_spawn()` no longer raise an
    exception on errors like missing program, but the child process fails
    with a non-zero [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode").

### Exceptions

Exceptions raised in the child process, before the new program has started to
execute, will be re-raised in the parent.

The most common exception raised is [`OSError`](exceptions.html#OSError "OSError"). This occurs, for example,
when trying to execute a non-existent file. Applications should prepare for
`OSError` exceptions. Note that, when `shell=True`, `OSError`
will be raised by the child only if the selected shell itself was not found.
To determine if the shell failed to find the requested application, it is
necessary to check the return code or output from the subprocess.

A [`ValueError`](exceptions.html#ValueError "ValueError") will be raised if [`Popen`](#subprocess.Popen "subprocess.Popen") is called with invalid
arguments.

[`check_call()`](#subprocess.check_call "subprocess.check_call") and [`check_output()`](#subprocess.check_output "subprocess.check_output") will raise
[`CalledProcessError`](#subprocess.CalledProcessError "subprocess.CalledProcessError") if the called process returns a non-zero return
code.

All of the functions and methods that accept a *timeout* parameter, such as
[`run()`](#subprocess.run "subprocess.run") and [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate") will raise [`TimeoutExpired`](#subprocess.TimeoutExpired "subprocess.TimeoutExpired") if
the timeout expires before the process exits.

Exceptions defined in this module all inherit from [`SubprocessError`](#subprocess.SubprocessError "subprocess.SubprocessError").

Added in version 3.3: The [`SubprocessError`](#subprocess.SubprocessError "subprocess.SubprocessError") base class was added.

## Security Considerations

Unlike some other popen functions, this library will not
implicitly choose to call a system shell. This means that all characters,
including shell metacharacters, can safely be passed to child processes.
If the shell is invoked explicitly, via `shell=True`, it is the application’s
responsibility to ensure that all whitespace and metacharacters are
quoted appropriately to avoid
[shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection)
vulnerabilities. On [some platforms](shlex.html#shlex-quote-warning), it is possible
to use [`shlex.quote()`](shlex.html#shlex.quote "shlex.quote") for this escaping.

On Windows, batch files (`*.bat` or `*.cmd`) may be launched by the
operating system in a system shell regardless of the arguments passed to this
library. This could result in arguments being parsed according to shell rules,
but without any escaping added by Python. If you are intentionally launching a
batch file with arguments from untrusted sources, consider passing
`shell=True` to allow Python to escape special characters. See [gh-114539](https://github.com/python/cpython/issues/114539)
for additional discussion.

## Popen Objects

Instances of the [`Popen`](#subprocess.Popen "subprocess.Popen") class have the following methods:

Popen.poll()
:   Check if child process has terminated. Set and return
    [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode") attribute. Otherwise, returns `None`.

Popen.wait(*timeout=None*)
:   Wait for child process to terminate. Set and return
    [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode") attribute.

    If the process does not terminate after *timeout* seconds, raise a
    [`TimeoutExpired`](#subprocess.TimeoutExpired "subprocess.TimeoutExpired") exception. It is safe to catch this exception and
    retry the wait.

    Note

    This will deadlock when using `stdout=PIPE` or `stderr=PIPE`
    and the child process generates enough output to a pipe such that
    it blocks waiting for the OS pipe buffer to accept more data.
    Use [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate") when using pipes to avoid that.

    Note

    When the `timeout` parameter is not `None`, then (on POSIX) the
    function is implemented using a busy loop (non-blocking call and short
    sleeps). Use the [`asyncio`](asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") module for an asynchronous wait: see
    [`asyncio.create_subprocess_exec`](asyncio-subprocess.html#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec").

    Changed in version 3.3: *timeout* was added.

Popen.communicate(*input=None*, *timeout=None*)
:   Interact with process: Send data to stdin. Read data from stdout and stderr,
    until end-of-file is reached. Wait for process to terminate and set the
    [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode") attribute. The optional *input* argument should be
    data to be sent to the child process, or `None`, if no data should be sent
    to the child. If streams were opened in text mode, *input* must be a string.
    Otherwise, it must be bytes.

    `communicate()` returns a tuple `(stdout_data, stderr_data)`.
    The data will be strings if streams were opened in text mode; otherwise,
    bytes.

    Note that if you want to send data to the process’s stdin, you need to create
    the Popen object with `stdin=PIPE`. Similarly, to get anything other than
    `None` in the result tuple, you need to give `stdout=PIPE` and/or
    `stderr=PIPE` too.

    If the process does not terminate after *timeout* seconds, a
    [`TimeoutExpired`](#subprocess.TimeoutExpired "subprocess.TimeoutExpired") exception will be raised. Catching this exception and
    retrying communication will not lose any output. Supplying *input* to a
    subsequent post-timeout `communicate()` call is in undefined behavior
    and may become an error in the future.

    The child process is not killed if the timeout expires, so in order to
    cleanup properly a well-behaved application should kill the child process and
    finish communication:

    ```
    proc = subprocess.Popen(...)
    try:
        outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    ```

    After a call to `communicate()` raises [`TimeoutExpired`](#subprocess.TimeoutExpired "subprocess.TimeoutExpired"), do
    not call [`wait()`](#subprocess.Popen.wait "subprocess.Popen.wait"). Use an additional `communicate()`
    call to finish handling pipes and populate the [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode")
    attribute.

    Note

    The data read is buffered in memory, so do not use this method if the data
    size is large or unlimited.

    Changed in version 3.3: *timeout* was added.

Popen.send\_signal(*signal*)
:   Sends the signal *signal* to the child.

    Do nothing if the process completed.

    Note

    On Windows, SIGTERM is an alias for [`terminate()`](#subprocess.Popen.terminate "subprocess.Popen.terminate"). CTRL\_C\_EVENT and
    CTRL\_BREAK\_EVENT can be sent to processes started with a *creationflags*
    parameter which includes `CREATE_NEW_PROCESS_GROUP`.

Popen.terminate()
:   Stop the child. On POSIX OSs the method sends [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM") to the
    child. On Windows the Win32 API function `TerminateProcess()` is called
    to stop the child.

Popen.kill()
:   Kills the child. On POSIX OSs the function sends SIGKILL to the child.
    On Windows `kill()` is an alias for [`terminate()`](#subprocess.Popen.terminate "subprocess.Popen.terminate").

The following attributes are also set by the class for you to access.
Reassigning them to new values is unsupported:

Popen.args
:   The *args* argument as it was passed to [`Popen`](#subprocess.Popen "subprocess.Popen") – a
    sequence of program arguments or else a single string.

    Added in version 3.3.

Popen.stdin
:   If the *stdin* argument was [`PIPE`](#subprocess.PIPE "subprocess.PIPE"), this attribute is a writeable
    stream object as returned by [`open()`](functions.html#open "open"). If the *encoding* or *errors*
    arguments were specified or the *text* or *universal\_newlines* argument
    was `True`, the stream is a text stream, otherwise it is a byte stream.
    If the *stdin* argument was not `PIPE`, this attribute is `None`.

Popen.stdout
:   If the *stdout* argument was [`PIPE`](#subprocess.PIPE "subprocess.PIPE"), this attribute is a readable
    stream object as returned by [`open()`](functions.html#open "open"). Reading from the stream provides
    output from the child process. If the *encoding* or *errors* arguments were
    specified or the *text* or *universal\_newlines* argument was `True`, the
    stream is a text stream, otherwise it is a byte stream. If the *stdout*
    argument was not `PIPE`, this attribute is `None`.

Popen.stderr
:   If the *stderr* argument was [`PIPE`](#subprocess.PIPE "subprocess.PIPE"), this attribute is a readable
    stream object as returned by [`open()`](functions.html#open "open"). Reading from the stream provides
    error output from the child process. If the *encoding* or *errors* arguments
    were specified or the *text* or *universal\_newlines* argument was `True`, the
    stream is a text stream, otherwise it is a byte stream. If the *stderr* argument
    was not `PIPE`, this attribute is `None`.

Warning

Use [`communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate") rather than [`.stdin.write`](#subprocess.Popen.stdin "subprocess.Popen.stdin"),
[`.stdout.read`](#subprocess.Popen.stdout "subprocess.Popen.stdout") or [`.stderr.read`](#subprocess.Popen.stderr "subprocess.Popen.stderr") to avoid
deadlocks due to any of the other OS pipe buffers filling up and blocking the
child process.

Popen.pid
:   The process ID of the child process.

    Note that if you set the *shell* argument to `True`, this is the process ID
    of the spawned shell.

Popen.returncode
:   The child return code. Initially `None`, [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode") is set by
    a call to the [`poll()`](#subprocess.Popen.poll "subprocess.Popen.poll"), [`wait()`](#subprocess.Popen.wait "subprocess.Popen.wait"), or [`communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate") methods
    if they detect that the process has terminated.

    A `None` value indicates that the process hadn’t yet terminated at the
    time of the last method call.

    A negative value `-N` indicates that the child was terminated by signal
    `N` (POSIX only).

    When `shell=True`, the return code reflects the exit status of the shell
    itself (e.g. `/bin/sh`), which may map signals to codes such as
    `128+N`. See the documentation of the shell (for example, the Bash
    manual’s Exit Status) for details.

## Windows Popen Helpers

The [`STARTUPINFO`](#subprocess.STARTUPINFO "subprocess.STARTUPINFO") class and following constants are only available
on Windows.

*class*subprocess.STARTUPINFO(*\**, *dwFlags=0*, *hStdInput=None*, *hStdOutput=None*, *hStdError=None*, *wShowWindow=0*, *lpAttributeList=None*)
:   Partial support of the Windows
    [STARTUPINFO](https://msdn.microsoft.com/en-us/library/ms686331(v=vs.85).aspx)
    structure is used for [`Popen`](#subprocess.Popen "subprocess.Popen") creation. The following attributes can
    be set by passing them as keyword-only arguments.

    Changed in version 3.7: Keyword-only argument support was added.

    dwFlags
    :   A bit field that determines whether certain `STARTUPINFO`
        attributes are used when the process creates a window.

        ```
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESTDHANDLES | subprocess.STARTF_USESHOWWINDOW
        ```

    hStdInput
    :   If [`dwFlags`](#subprocess.STARTUPINFO.dwFlags "subprocess.STARTUPINFO.dwFlags") specifies [`STARTF_USESTDHANDLES`](#subprocess.STARTF_USESTDHANDLES "subprocess.STARTF_USESTDHANDLES"), this attribute
        is the standard input handle for the process. If
        `STARTF_USESTDHANDLES` is not specified, the default for standard
        input is the keyboard buffer.

    hStdOutput
    :   If [`dwFlags`](#subprocess.STARTUPINFO.dwFlags "subprocess.STARTUPINFO.dwFlags") specifies [`STARTF_USESTDHANDLES`](#subprocess.STARTF_USESTDHANDLES "subprocess.STARTF_USESTDHANDLES"), this attribute
        is the standard output handle for the process. Otherwise, this attribute
        is ignored and the default for standard output is the console window’s
        buffer.

    hStdError
    :   If [`dwFlags`](#subprocess.STARTUPINFO.dwFlags "subprocess.STARTUPINFO.dwFlags") specifies [`STARTF_USESTDHANDLES`](#subprocess.STARTF_USESTDHANDLES "subprocess.STARTF_USESTDHANDLES"), this attribute
        is the standard error handle for the process. Otherwise, this attribute is
        ignored and the default for standard error is the console window’s buffer.

    wShowWindow
    :   If [`dwFlags`](#subprocess.STARTUPINFO.dwFlags "subprocess.STARTUPINFO.dwFlags") specifies [`STARTF_USESHOWWINDOW`](#subprocess.STARTF_USESHOWWINDOW "subprocess.STARTF_USESHOWWINDOW"), this attribute
        can be any of the values that can be specified in the `nCmdShow`
        parameter for the
        [ShowWindow](https://msdn.microsoft.com/en-us/library/ms633548(v=vs.85).aspx)
        function, except for `SW_SHOWDEFAULT`. Otherwise, this attribute is
        ignored.

        [`SW_HIDE`](#subprocess.SW_HIDE "subprocess.SW_HIDE") is provided for this attribute. It is used when
        [`Popen`](#subprocess.Popen "subprocess.Popen") is called with `shell=True`.

    lpAttributeList
    :   A dictionary of additional attributes for process creation as given in
        `STARTUPINFOEX`, see
        [UpdateProcThreadAttribute](https://msdn.microsoft.com/en-us/library/windows/desktop/ms686880(v=vs.85).aspx).

        Supported attributes:

        **handle\_list**
        :   Sequence of handles that will be inherited. *close\_fds* must be true if
            non-empty.

            The handles must be temporarily made inheritable by
            [`os.set_handle_inheritable()`](os.html#os.set_handle_inheritable "os.set_handle_inheritable") when passed to the [`Popen`](#subprocess.Popen "subprocess.Popen")
            constructor, else [`OSError`](exceptions.html#OSError "OSError") will be raised with Windows error
            `ERROR_INVALID_PARAMETER` (87).

            Warning

            In a multithreaded process, use caution to avoid leaking handles
            that are marked inheritable when combining this feature with
            concurrent calls to other process creation functions that inherit
            all handles such as [`os.system()`](os.html#os.system "os.system"). This also applies to
            standard handle redirection, which temporarily creates inheritable
            handles.

        Added in version 3.7.

### Windows Constants

The `subprocess` module exposes the following constants.

subprocess.STD\_INPUT\_HANDLE
:   The standard input device. Initially, this is the console input buffer,
    `CONIN$`.

subprocess.STD\_OUTPUT\_HANDLE
:   The standard output device. Initially, this is the active console screen
    buffer, `CONOUT$`.

subprocess.STD\_ERROR\_HANDLE
:   The standard error device. Initially, this is the active console screen
    buffer, `CONOUT$`.

subprocess.SW\_HIDE
:   Hides the window. Another window will be activated.

subprocess.STARTF\_USESTDHANDLES
:   Specifies that the [`STARTUPINFO.hStdInput`](#subprocess.STARTUPINFO.hStdInput "subprocess.STARTUPINFO.hStdInput"),
    [`STARTUPINFO.hStdOutput`](#subprocess.STARTUPINFO.hStdOutput "subprocess.STARTUPINFO.hStdOutput"), and [`STARTUPINFO.hStdError`](#subprocess.STARTUPINFO.hStdError "subprocess.STARTUPINFO.hStdError") attributes
    contain additional information.

subprocess.STARTF\_USESHOWWINDOW
:   Specifies that the [`STARTUPINFO.wShowWindow`](#subprocess.STARTUPINFO.wShowWindow "subprocess.STARTUPINFO.wShowWindow") attribute contains
    additional information.

subprocess.STARTF\_FORCEONFEEDBACK
:   A [`STARTUPINFO.dwFlags`](#subprocess.STARTUPINFO.dwFlags "subprocess.STARTUPINFO.dwFlags") parameter to specify that the
    *Working in Background* mouse cursor will be displayed while a
    process is launching. This is the default behavior for GUI
    processes.

    Added in version 3.13.

subprocess.STARTF\_FORCEOFFFEEDBACK
:   A [`STARTUPINFO.dwFlags`](#subprocess.STARTUPINFO.dwFlags "subprocess.STARTUPINFO.dwFlags") parameter to specify that the mouse
    cursor will not be changed when launching a process.

    Added in version 3.13.

subprocess.CREATE\_NEW\_CONSOLE
:   The new process has a new console, instead of inheriting its parent’s
    console (the default).

subprocess.CREATE\_NEW\_PROCESS\_GROUP
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    group will be created. This flag is necessary for using [`os.kill()`](os.html#os.kill "os.kill")
    on the subprocess.

    This flag is ignored if [`CREATE_NEW_CONSOLE`](#subprocess.CREATE_NEW_CONSOLE "subprocess.CREATE_NEW_CONSOLE") is specified.

subprocess.ABOVE\_NORMAL\_PRIORITY\_CLASS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will have an above average priority.

    Added in version 3.7.

subprocess.BELOW\_NORMAL\_PRIORITY\_CLASS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will have a below average priority.

    Added in version 3.7.

subprocess.HIGH\_PRIORITY\_CLASS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will have a high priority.

    Added in version 3.7.

subprocess.IDLE\_PRIORITY\_CLASS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will have an idle (lowest) priority.

    Added in version 3.7.

subprocess.NORMAL\_PRIORITY\_CLASS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will have a normal priority. (default)

    Added in version 3.7.

subprocess.REALTIME\_PRIORITY\_CLASS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will have realtime priority.
    You should almost never use REALTIME\_PRIORITY\_CLASS, because this interrupts
    system threads that manage mouse input, keyboard input, and background disk
    flushing. This class can be appropriate for applications that “talk” directly
    to hardware or that perform brief tasks that should have limited interruptions.

    Added in version 3.7.

subprocess.CREATE\_NO\_WINDOW
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will not create a window.

    Added in version 3.7.

subprocess.DETACHED\_PROCESS
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    will not inherit its parent’s console.
    This value cannot be used with CREATE\_NEW\_CONSOLE.

    Added in version 3.7.

subprocess.CREATE\_DEFAULT\_ERROR\_MODE
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    does not inherit the error mode of the calling process. Instead, the new
    process gets the default error mode.
    This feature is particularly useful for multithreaded shell applications
    that run with hard errors disabled.

    Added in version 3.7.

subprocess.CREATE\_BREAKAWAY\_FROM\_JOB
:   A [`Popen`](#subprocess.Popen "subprocess.Popen") `creationflags` parameter to specify that a new process
    is not associated with the job.

    Added in version 3.7.

## Older high-level API

Prior to Python 3.5, these three functions comprised the high level API to
subprocess. You can now use [`run()`](#subprocess.run "subprocess.run") in many cases, but lots of existing code
calls these functions.

subprocess.call(*args*, *\**, *stdin=None*, *stdout=None*, *stderr=None*, *shell=False*, *cwd=None*, *timeout=None*, *\*\*other\_popen\_kwargs*)
:   Run the command described by *args*. Wait for command to complete, then
    return the [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode") attribute.

    Code needing to capture stdout or stderr should use [`run()`](#subprocess.run "subprocess.run") instead:

    ```
    run(...).returncode
    ```

    To suppress stdout or stderr, supply a value of [`DEVNULL`](#subprocess.DEVNULL "subprocess.DEVNULL").

    The arguments shown above are merely some common ones.
    The full function signature is the
    same as that of the [`Popen`](#subprocess.Popen "subprocess.Popen") constructor - this function passes all
    supplied arguments other than *timeout* directly through to that interface.

    Note

    Do not use `stdout=PIPE` or `stderr=PIPE` with this
    function. The child process will block if it generates enough
    output to a pipe to fill up the OS pipe buffer as the pipes are
    not being read from.

    Changed in version 3.3: *timeout* was added.

    Changed in version 3.12: Changed Windows shell search order for `shell=True`. The current
    directory and `%PATH%` are replaced with `%COMSPEC%` and
    `%SystemRoot%\System32\cmd.exe`. As a result, dropping a
    malicious program named `cmd.exe` into a current directory no
    longer works.

subprocess.check\_call(*args*, *\**, *stdin=None*, *stdout=None*, *stderr=None*, *shell=False*, *cwd=None*, *timeout=None*, *\*\*other\_popen\_kwargs*)
:   Run command with arguments. Wait for command to complete. If the return
    code was zero then return, otherwise raise [`CalledProcessError`](#subprocess.CalledProcessError "subprocess.CalledProcessError"). The
    `CalledProcessError` object will have the return code in the
    [`returncode`](#subprocess.CalledProcessError.returncode "subprocess.CalledProcessError.returncode") attribute.
    If `check_call()` was unable to start the process it will propagate the exception
    that was raised.

    Code needing to capture stdout or stderr should use [`run()`](#subprocess.run "subprocess.run") instead:

    ```
    run(..., check=True)
    ```

    To suppress stdout or stderr, supply a value of [`DEVNULL`](#subprocess.DEVNULL "subprocess.DEVNULL").

    The arguments shown above are merely some common ones.
    The full function signature is the
    same as that of the [`Popen`](#subprocess.Popen "subprocess.Popen") constructor - this function passes all
    supplied arguments other than *timeout* directly through to that interface.

    Note

    Do not use `stdout=PIPE` or `stderr=PIPE` with this
    function. The child process will block if it generates enough
    output to a pipe to fill up the OS pipe buffer as the pipes are
    not being read from.

    Changed in version 3.3: *timeout* was added.

    Changed in version 3.12: Changed Windows shell search order for `shell=True`. The current
    directory and `%PATH%` are replaced with `%COMSPEC%` and
    `%SystemRoot%\System32\cmd.exe`. As a result, dropping a
    malicious program named `cmd.exe` into a current directory no
    longer works.

subprocess.check\_output(*args*, *\**, *stdin=None*, *stderr=None*, *shell=False*, *cwd=None*, *encoding=None*, *errors=None*, *universal\_newlines=None*, *timeout=None*, *text=None*, *\*\*other\_popen\_kwargs*)
:   Run command with arguments and return its output.

    If the return code was non-zero it raises a [`CalledProcessError`](#subprocess.CalledProcessError "subprocess.CalledProcessError"). The
    `CalledProcessError` object will have the return code in the
    [`returncode`](#subprocess.CalledProcessError.returncode "subprocess.CalledProcessError.returncode") attribute and any output in the
    [`output`](#subprocess.CalledProcessError.output "subprocess.CalledProcessError.output") attribute.

    This is equivalent to:

    ```
    run(..., check=True, stdout=PIPE).stdout
    ```

    The arguments shown above are merely some common ones.
    The full function signature is largely the same as that of [`run()`](#subprocess.run "subprocess.run") -
    most arguments are passed directly through to that interface.
    One API deviation from `run()` behavior exists: passing `input=None`
    will behave the same as `input=b''` (or `input=''`, depending on other
    arguments) rather than using the parent’s standard input file handle.

    By default, this function will return the data as encoded bytes. The actual
    encoding of the output data may depend on the command being invoked, so the
    decoding to text will often need to be handled at the application level.

    This behaviour may be overridden by setting *text*, *encoding*, *errors*,
    or *universal\_newlines* to `True` as described in
    [Frequently Used Arguments](#frequently-used-arguments) and [`run()`](#subprocess.run "subprocess.run").

    To also capture standard error in the result, use
    `stderr=subprocess.STDOUT`:

    ```
    >>> subprocess.check_output(
    ...     "ls non_existent_file; exit 0",
    ...     stderr=subprocess.STDOUT,
    ...     shell=True)
    'ls: non_existent_file: No such file or directory\n'
    ```

    Added in version 3.1.

    Changed in version 3.3: *timeout* was added.

    Changed in version 3.4: Support for the *input* keyword argument was added.

    Changed in version 3.6: *encoding* and *errors* were added. See [`run()`](#subprocess.run "subprocess.run") for details.

    Added in version 3.7: *text* was added as a more readable alias for *universal\_newlines*.

    Changed in version 3.12: Changed Windows shell search order for `shell=True`. The current
    directory and `%PATH%` are replaced with `%COMSPEC%` and
    `%SystemRoot%\System32\cmd.exe`. As a result, dropping a
    malicious program named `cmd.exe` into a current directory no
    longer works.

## Replacing Older Functions with the `subprocess` Module

In this section, “a becomes b” means that b can be used as a replacement for a.

Note

All “a” functions in this section fail (more or less) silently if the
executed program cannot be found; the “b” replacements raise [`OSError`](exceptions.html#OSError "OSError")
instead.

In addition, the replacements using [`check_output()`](#subprocess.check_output "subprocess.check_output") will fail with a
[`CalledProcessError`](#subprocess.CalledProcessError "subprocess.CalledProcessError") if the requested operation produces a non-zero
return code. The output is still available as the
[`output`](#subprocess.CalledProcessError.output "subprocess.CalledProcessError.output") attribute of the raised exception.

In the following examples, we assume that the relevant functions have already
been imported from the `subprocess` module.

### Replacing **/bin/sh** shell command substitution

```
output=$(mycmdmyarg)
```

becomes:

```
output = check_output(["mycmd", "myarg"])
```

### Replacing shell pipeline

```
output=$(dmesg|grephda)
```

becomes:

```
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
```

The `p1.stdout.close()` call after starting the p2 is important in order for
p1 to receive a SIGPIPE if p2 exits before p1.

Alternatively, for trusted input, the shell’s own pipeline support may still
be used directly:

```
output=$(dmesg|grephda)
```

becomes:

```
output = check_output("dmesg | grep hda", shell=True)
```

### Replacing [`os.system()`](os.html#os.system "os.system")

```
sts = os.system("mycmd" + " myarg")
# becomes
retcode = call("mycmd" + " myarg", shell=True)
```

Notes:

* Calling the program through the shell is usually not required.
* The [`call()`](#subprocess.call "subprocess.call") return value is encoded differently to that of
  [`os.system()`](os.html#os.system "os.system").
* The [`os.system()`](os.html#os.system "os.system") function ignores SIGINT and SIGQUIT signals while
  the command is running, but the caller must do this separately when
  using the `subprocess` module.

A more realistic example would look like this:

```
try:
    retcode = call("mycmd" + " myarg", shell=True)
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=sys.stderr)
    else:
        print("Child returned", retcode, file=sys.stderr)
except OSError as e:
    print("Execution failed:", e, file=sys.stderr)
```

### Replacing the [`os.spawn`](os.html#os.spawnl "os.spawnl") family

P\_NOWAIT example:

```
pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
==>
pid = Popen(["/bin/mycmd", "myarg"]).pid
```

P\_WAIT example:

```
retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
==>
retcode = call(["/bin/mycmd", "myarg"])
```

Vector example:

```
os.spawnvp(os.P_NOWAIT, path, args)
==>
Popen([path] + args[1:])
```

Environment example:

```
os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
==>
Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})
```

### Replacing [`os.popen()`](os.html#os.popen "os.popen")

Return code handling translates as follows:

```
pipe = os.popen(cmd, 'w')
...
rc = pipe.close()
if rc is not None and rc >> 8:
    print("There were some errors")
==>
process = Popen(cmd, stdin=PIPE)
...
process.stdin.close()
if process.wait() != 0:
    print("There were some errors")
```

## Legacy Shell Invocation Functions

This module also provides the following legacy functions from the 2.x
`commands` module. These operations implicitly invoke the system shell and
none of the guarantees described above regarding security and exception
handling consistency are valid for these functions.

subprocess.getstatusoutput(*cmd*, *\**, *encoding=None*, *errors=None*)
:   Return `(exitcode, output)` of executing *cmd* in a shell.

    Execute the string *cmd* in a shell with [`check_output()`](#subprocess.check_output "subprocess.check_output") and
    return a 2-tuple `(exitcode, output)`.
    *encoding* and *errors* are used to decode output;
    see the notes on [Frequently Used Arguments](#frequently-used-arguments) for more details.

    A trailing newline is stripped from the output.
    The exit code for the command can be interpreted as the return code
    of subprocess. Example:

    ```
    >>> subprocess.getstatusoutput('ls /bin/ls')
    (0, '/bin/ls')
    >>> subprocess.getstatusoutput('cat /bin/junk')
    (1, 'cat: /bin/junk: No such file or directory')
    >>> subprocess.getstatusoutput('/bin/junk')
    (127, 'sh: /bin/junk: not found')
    >>> subprocess.getstatusoutput('/bin/kill $$')
    (-15, '')
    ```

    [Availability](intro.html#availability): Unix, Windows.

    Changed in version 3.3.4: Windows support was added.

    The function now returns (exitcode, output) instead of (status, output)
    as it did in Python 3.3.3 and earlier. exitcode has the same value as
    [`returncode`](#subprocess.Popen.returncode "subprocess.Popen.returncode").

    Changed in version 3.11: Added the *encoding* and *errors* parameters.

subprocess.getoutput(*cmd*, *\**, *encoding=None*, *errors=None*)
:   Return output (stdout and stderr) of executing *cmd* in a shell.

    Like [`getstatusoutput()`](#subprocess.getstatusoutput "subprocess.getstatusoutput"), except the exit code is ignored and the return
    value is a string containing the command’s output. Example:

    ```
    >>> subprocess.getoutput('ls /bin/ls')
    '/bin/ls'
    ```

    [Availability](intro.html#availability): Unix, Windows.

    Changed in version 3.3.4: Windows support added

    Changed in version 3.11: Added the *encoding* and *errors* parameters.

## Notes

### Timeout Behavior

When using the `timeout` parameter in functions like [`run()`](#subprocess.run "subprocess.run"),
[`Popen.wait()`](#subprocess.Popen.wait "subprocess.Popen.wait"), or [`Popen.communicate()`](#subprocess.Popen.communicate "subprocess.Popen.communicate"),
users should be aware of the following behaviors:

1. **Process Creation Delay**: The initial process creation itself cannot be interrupted
   on many platform APIs. This means that even when specifying a timeout, you are not
   guaranteed to see a timeout exception until at least after however long process
   creation takes.
2. **Extremely Small Timeout Values**: Setting very small timeout values (such as a few
   milliseconds) may result in almost immediate [`TimeoutExpired`](#subprocess.TimeoutExpired "subprocess.TimeoutExpired") exceptions because
   process creation and system scheduling inherently require time.

### Converting an argument sequence to a string on Windows

On Windows, an *args* sequence is converted to a string that can be parsed
using the following rules (which correspond to the rules used by the MS C
runtime):

1. Arguments are delimited by white space, which is either a
   space or a tab.
2. A string surrounded by double quotation marks is
   interpreted as a single argument, regardless of white space
   contained within. A quoted string can be embedded in an
   argument.
3. A double quotation mark preceded by a backslash is
   interpreted as a literal double quotation mark.
4. Backslashes are interpreted literally, unless they
   immediately precede a double quotation mark.
5. If backslashes immediately precede a double quotation mark,
   every pair of backslashes is interpreted as a literal
   backslash. If the number of backslashes is odd, the last
   backslash escapes the next double quotation mark as
   described in rule 3.

See also

[`shlex`](shlex.html#module-shlex "shlex: Simple lexical analysis for Unix shell-like languages.")
:   Module which provides function to parse and escape command lines.

### Disable use of `posix_spawn()`

On Linux, `subprocess` defaults to using the `vfork()` system call
internally when it is safe to do so rather than `fork()`. This greatly
improves performance.

```
subprocess._USE_POSIX_SPAWN = False  # See CPython issue gh-NNNNNN.
```

It is safe to set this to false on any Python version. It will have no
effect on older or newer versions where unsupported. Do not assume the attribute
is available to read. Despite the name, a true value does not indicate the
corresponding function will be used, only that it may be.

Please file issues any time you have to use these private knobs with a way to
reproduce the issue you were seeing. Link to that issue from a comment in your
code.

Added in version 3.8: `_USE_POSIX_SPAWN`

---

## 3. `signal` — Set handlers for asynchronous events

**Source code:** [Lib/signal.py](https://github.com/python/cpython/tree/3.14/Lib/signal.py)

---

This module provides mechanisms to use signal handlers in Python.

## General rules

The [`signal.signal()`](#signal.signal "signal.signal") function allows defining custom handlers to be
executed when a signal is received. A small number of default handlers are
installed: [`SIGPIPE`](#signal.SIGPIPE "signal.SIGPIPE") is ignored (so write errors on pipes and sockets
can be reported as ordinary Python exceptions) and [`SIGINT`](#signal.SIGINT "signal.SIGINT") is
translated into a [`KeyboardInterrupt`](exceptions.html#KeyboardInterrupt "KeyboardInterrupt") exception if the parent process
has not changed it.

A handler for a particular signal, once set, remains installed until it is
explicitly reset (Python emulates the BSD style interface regardless of the
underlying implementation), with the exception of the handler for
[`SIGCHLD`](#signal.SIGCHLD "signal.SIGCHLD"), which follows the underlying implementation.

On WebAssembly platforms, signals are emulated and therefore behave
differently. Several functions and signals are not available on these
platforms.

### Execution of Python signal handlers

A Python signal handler does not get executed inside the low-level (C) signal
handler. Instead, the low-level signal handler sets a flag which tells the
[virtual machine](../glossary.html#term-virtual-machine) to execute the corresponding Python signal handler
at a later point (for example, at the next [bytecode](../glossary.html#term-bytecode) instruction).
This has consequences:

* It makes little sense to catch synchronous errors like [`SIGFPE`](#signal.SIGFPE "signal.SIGFPE") or
  [`SIGSEGV`](#signal.SIGSEGV "signal.SIGSEGV") that are caused by an invalid operation in C code. Python
  will return from the signal handler to the C code, which is likely to raise
  the same signal again, causing Python to apparently hang. From Python 3.3
  onwards, you can use the [`faulthandler`](faulthandler.html#module-faulthandler "faulthandler: Dump the Python traceback.") module to report on synchronous
  errors.
* A long-running calculation implemented purely in C (such as regular
  expression matching on a large body of text) may run uninterrupted for an
  arbitrary amount of time, regardless of any signals received. The Python
  signal handlers will be called when the calculation finishes.
* If the handler raises an exception, it will be raised “out of thin air” in
  the main thread. See the [note below](#handlers-and-exceptions) for a
  discussion.

### Signals and threads

Python signal handlers are always executed in the main Python thread of the main interpreter,
even if the signal was received in another thread. This means that signals
can’t be used as a means of inter-thread communication. You can use
the synchronization primitives from the [`threading`](threading.html#module-threading "threading: Thread-based parallelism.") module instead.

Besides, only the main thread of the main interpreter is allowed to set a new signal handler.

Warning

Synchronization primitives such as [`threading.Lock`](threading.html#threading.Lock "threading.Lock") should not be used
within signal handlers. Doing so can lead to unexpected deadlocks.

## Module contents

Changed in version 3.5: signal (SIG\*), handler ([`SIG_DFL`](#signal.SIG_DFL "signal.SIG_DFL"), [`SIG_IGN`](#signal.SIG_IGN "signal.SIG_IGN")) and sigmask
([`SIG_BLOCK`](#signal.SIG_BLOCK "signal.SIG_BLOCK"), [`SIG_UNBLOCK`](#signal.SIG_UNBLOCK "signal.SIG_UNBLOCK"), [`SIG_SETMASK`](#signal.SIG_SETMASK "signal.SIG_SETMASK"))
related constants listed below were turned into
[`enums`](enum.html#enum.IntEnum "enum.IntEnum") ([`Signals`](#signal.Signals "signal.Signals"), [`Handlers`](#signal.Handlers "signal.Handlers") and [`Sigmasks`](#signal.Sigmasks "signal.Sigmasks") respectively).
[`getsignal()`](#signal.getsignal "signal.getsignal"), [`pthread_sigmask()`](#signal.pthread_sigmask "signal.pthread_sigmask"), [`sigpending()`](#signal.sigpending "signal.sigpending") and
[`sigwait()`](#signal.sigwait "signal.sigwait") functions return human-readable
`enums` as `Signals` objects.

The signal module defines three enums:

*class*signal.Signals
:   [`enum.IntEnum`](enum.html#enum.IntEnum "enum.IntEnum") collection of SIG\* constants and the CTRL\_\* constants.

    Added in version 3.5.

*class*signal.Handlers
:   [`enum.IntEnum`](enum.html#enum.IntEnum "enum.IntEnum") collection of the constants [`SIG_DFL`](#signal.SIG_DFL "signal.SIG_DFL") and [`SIG_IGN`](#signal.SIG_IGN "signal.SIG_IGN").

    Added in version 3.5.

*class*signal.Sigmasks
:   [`enum.IntEnum`](enum.html#enum.IntEnum "enum.IntEnum") collection of the constants [`SIG_BLOCK`](#signal.SIG_BLOCK "signal.SIG_BLOCK"), [`SIG_UNBLOCK`](#signal.SIG_UNBLOCK "signal.SIG_UNBLOCK") and [`SIG_SETMASK`](#signal.SIG_SETMASK "signal.SIG_SETMASK").

    [Availability](intro.html#availability): Unix.

    See the man page *[sigprocmask(2)](https://manpages.debian.org/sigprocmask(2))* and
    *[pthread\_sigmask(3)](https://manpages.debian.org/pthread_sigmask(3))* for further information.

    Added in version 3.5.

The variables defined in the `signal` module are:

signal.SIG\_DFL
:   This is one of two standard signal handling options; it will simply perform
    the default function for the signal. For example, on most systems the
    default action for [`SIGQUIT`](#signal.SIGQUIT "signal.SIGQUIT") is to dump core and exit, while the
    default action for [`SIGCHLD`](#signal.SIGCHLD "signal.SIGCHLD") is to simply ignore it.

signal.SIG\_IGN
:   This is another standard signal handler, which will simply ignore the given
    signal.

signal.SIGABRT
:   Abort signal from *[abort(3)](https://manpages.debian.org/abort(3))*.

signal.SIGALRM
:   Timer signal from *[alarm(2)](https://manpages.debian.org/alarm(2))*.

    [Availability](intro.html#availability): Unix.

signal.SIGBREAK
:   Interrupt from keyboard (CTRL + BREAK).

    [Availability](intro.html#availability): Windows.

signal.SIGBUS
:   Bus error (bad memory access).

    [Availability](intro.html#availability): Unix.

signal.SIGCHLD
:   Child process stopped or terminated.

    [Availability](intro.html#availability): Unix.

signal.SIGCLD
:   Alias to [`SIGCHLD`](#signal.SIGCHLD "signal.SIGCHLD").

    [Availability](intro.html#availability): not macOS.

signal.SIGCONT
:   Continue the process if it is currently stopped

    [Availability](intro.html#availability): Unix.

signal.SIGFPE
:   Floating-point exception. For example, division by zero.

    See also

    [`ZeroDivisionError`](exceptions.html#ZeroDivisionError "ZeroDivisionError") is raised when the second argument of a division
    or modulo operation is zero.

signal.SIGHUP
:   Hangup detected on controlling terminal or death of controlling process.

    [Availability](intro.html#availability): Unix.

signal.SIGILL
:   Illegal instruction.

signal.SIGINT
:   Interrupt from keyboard (CTRL + C).

    Default action is to raise [`KeyboardInterrupt`](exceptions.html#KeyboardInterrupt "KeyboardInterrupt").

signal.SIGKILL
:   Kill signal.

    It cannot be caught, blocked, or ignored.

    [Availability](intro.html#availability): Unix.

signal.SIGPIPE
:   Broken pipe: write to pipe with no readers.

    Default action is to ignore the signal.

    [Availability](intro.html#availability): Unix.

signal.SIGPROF
:   Profiling timer expired.

    [Availability](intro.html#availability): Unix.

signal.SIGQUIT
:   Terminal quit signal.

    [Availability](intro.html#availability): Unix.

signal.SIGSEGV
:   Segmentation fault: invalid memory reference.

signal.SIGSTOP
:   Stop executing (cannot be caught or ignored).

    [Availability](intro.html#availability): Unix.

signal.SIGSTKFLT
:   Stack fault on coprocessor. The Linux kernel does not raise this signal: it
    can only be raised in user space.

    [Availability](intro.html#availability): Linux.

    On architectures where the signal is available. See
    the man page *[signal(7)](https://manpages.debian.org/signal(7))* for further information.

    Added in version 3.11.

signal.SIGTERM
:   Termination signal.

signal.SIGUSR1
:   User-defined signal 1.

    [Availability](intro.html#availability): Unix.

signal.SIGUSR2
:   User-defined signal 2.

    [Availability](intro.html#availability): Unix.

signal.SIGVTALRM
:   Virtual timer expired.

    [Availability](intro.html#availability): Unix.

signal.SIGWINCH
:   Window resize signal.

    [Availability](intro.html#availability): Unix.

signal.SIGXCPU
:   CPU time limit exceeded.

    [Availability](intro.html#availability): Unix.

SIG\*
:   All the signal numbers are defined symbolically. For example, the hangup signal
    is defined as [`signal.SIGHUP`](#signal.SIGHUP "signal.SIGHUP"); the variable names are identical to the
    names used in C programs, as found in `<signal.h>`. The Unix man page for
    ‘`signal`’ lists the existing signals (on some systems this is
    *[signal(2)](https://manpages.debian.org/signal(2))*, on others the list is in *[signal(7)](https://manpages.debian.org/signal(7))*). Note that
    not all systems define the same set of signal names; only those names defined by
    the system are defined by this module.

signal.CTRL\_C\_EVENT
:   The signal corresponding to the `Ctrl`+`C` keystroke event. This signal can
    only be used with [`os.kill()`](os.html#os.kill "os.kill").

    [Availability](intro.html#availability): Windows.

    Added in version 3.2.

signal.CTRL\_BREAK\_EVENT
:   The signal corresponding to the `Ctrl`+`Break` keystroke event. This signal can
    only be used with [`os.kill()`](os.html#os.kill "os.kill").

    [Availability](intro.html#availability): Windows.

    Added in version 3.2.

signal.NSIG
:   One more than the number of the highest signal number.
    Use [`valid_signals()`](#signal.valid_signals "signal.valid_signals") to get valid signal numbers.

signal.ITIMER\_REAL
:   Decrements interval timer in real time, and delivers [`SIGALRM`](#signal.SIGALRM "signal.SIGALRM") upon
    expiration.

signal.ITIMER\_VIRTUAL
:   Decrements interval timer only when the process is executing, and delivers
    SIGVTALRM upon expiration.

signal.ITIMER\_PROF
:   Decrements interval timer both when the process executes and when the
    system is executing on behalf of the process. Coupled with ITIMER\_VIRTUAL,
    this timer is usually used to profile the time spent by the application
    in user and kernel space. SIGPROF is delivered upon expiration.

signal.SIG\_BLOCK
:   A possible value for the *how* parameter to [`pthread_sigmask()`](#signal.pthread_sigmask "signal.pthread_sigmask")
    indicating that signals are to be blocked.

    Added in version 3.3.

signal.SIG\_UNBLOCK
:   A possible value for the *how* parameter to [`pthread_sigmask()`](#signal.pthread_sigmask "signal.pthread_sigmask")
    indicating that signals are to be unblocked.

    Added in version 3.3.

signal.SIG\_SETMASK
:   A possible value for the *how* parameter to [`pthread_sigmask()`](#signal.pthread_sigmask "signal.pthread_sigmask")
    indicating that the signal mask is to be replaced.

    Added in version 3.3.

The `signal` module defines one exception:

*exception*signal.ItimerError
:   Raised to signal an error from the underlying [`setitimer()`](#signal.setitimer "signal.setitimer") or
    [`getitimer()`](#signal.getitimer "signal.getitimer") implementation. Expect this error if an invalid
    interval timer or a negative time is passed to `setitimer()`.
    This error is a subtype of [`OSError`](exceptions.html#OSError "OSError").

    Added in version 3.3: This error used to be a subtype of [`IOError`](exceptions.html#IOError "IOError"), which is now an
    alias of [`OSError`](exceptions.html#OSError "OSError").

The `signal` module defines the following functions:

signal.alarm(*time*)
:   If *time* is non-zero, this function requests that a [`SIGALRM`](#signal.SIGALRM "signal.SIGALRM") signal be
    sent to the process in *time* seconds. Any previously scheduled alarm is
    canceled (only one alarm can be scheduled at any time). The returned value is
    then the number of seconds before any previously set alarm was to have been
    delivered. If *time* is zero, no alarm is scheduled, and any scheduled alarm is
    canceled. If the return value is zero, no alarm is currently scheduled.

    [Availability](intro.html#availability): Unix.

    See the man page *[alarm(2)](https://manpages.debian.org/alarm(2))* for further information.

signal.getsignal(*signalnum*)
:   Return the current signal handler for the signal *signalnum*. The returned value
    may be a callable Python object, or one of the special values
    [`signal.SIG_IGN`](#signal.SIG_IGN "signal.SIG_IGN"), [`signal.SIG_DFL`](#signal.SIG_DFL "signal.SIG_DFL") or [`None`](constants.html#None "None"). Here,
    `signal.SIG_IGN` means that the signal was previously ignored,
    `signal.SIG_DFL` means that the default way of handling the signal was
    previously in use, and `None` means that the previous signal handler was not
    installed from Python.

signal.strsignal(*signalnum*)
:   Returns the description of signal *signalnum*, such as “Interrupt”
    for [`SIGINT`](#signal.SIGINT "signal.SIGINT"). Returns [`None`](constants.html#None "None") if *signalnum* has no
    description. Raises [`ValueError`](exceptions.html#ValueError "ValueError") if *signalnum* is invalid.

    Added in version 3.8.

signal.valid\_signals()
:   Return the set of valid signal numbers on this platform. This can be
    less than `range(1, NSIG)` if some signals are reserved by the system
    for internal use.

    Added in version 3.8.

signal.pause()
:   Cause the process to sleep until a signal is received; the appropriate handler
    will then be called. Returns nothing.

    [Availability](intro.html#availability): Unix.

    See the man page *[signal(2)](https://manpages.debian.org/signal(2))* for further information.

    See also [`sigwait()`](#signal.sigwait "signal.sigwait"), [`sigwaitinfo()`](#signal.sigwaitinfo "signal.sigwaitinfo"), [`sigtimedwait()`](#signal.sigtimedwait "signal.sigtimedwait") and
    [`sigpending()`](#signal.sigpending "signal.sigpending").

signal.raise\_signal(*signum*)
:   Sends a signal to the calling process. Returns nothing.

    Added in version 3.8.

signal.pidfd\_send\_signal(*pidfd*, *sig*, *siginfo=None*, *flags=0*)
:   Send signal *sig* to the process referred to by file descriptor *pidfd*.
    Python does not currently support the *siginfo* parameter; it must be
    `None`. The *flags* argument is provided for future extensions; no flag
    values are currently defined.

    See the *[pidfd\_send\_signal(2)](https://manpages.debian.org/pidfd_send_signal(2))* man page for more information.

    [Availability](intro.html#availability): Linux >= 5.1, Android >= [`build-time`](sys.html#sys.getandroidapilevel "sys.getandroidapilevel") API level 31

    Added in version 3.9.

signal.pthread\_kill(*thread\_id*, *signalnum*)
:   Send the signal *signalnum* to the thread *thread\_id*, another thread in the
    same process as the caller. The target thread can be executing any code
    (Python or not). However, if the target thread is executing the Python
    interpreter, the Python signal handlers will be [executed by the main
    thread of the main interpreter](#signals-and-threads). Therefore, the only point of sending a
    signal to a particular Python thread would be to force a running system call
    to fail with [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError").

    Use [`threading.get_ident()`](threading.html#threading.get_ident "threading.get_ident") or the [`ident`](threading.html#threading.Thread.ident "threading.Thread.ident")
    attribute of [`threading.Thread`](threading.html#threading.Thread "threading.Thread") objects to get a suitable value
    for *thread\_id*.

    If *signalnum* is 0, then no signal is sent, but error checking is still
    performed; this can be used to check if the target thread is still running.

    Raises an [auditing event](sys.html#auditing) `signal.pthread_kill` with arguments `thread_id`, `signalnum`.

    [Availability](intro.html#availability): Unix.

    See the man page *[pthread\_kill(3)](https://manpages.debian.org/pthread_kill(3))* for further information.

    See also [`os.kill()`](os.html#os.kill "os.kill").

    Added in version 3.3.

signal.pthread\_sigmask(*how*, *mask*)
:   Fetch and/or change the signal mask of the calling thread. The signal mask
    is the set of signals whose delivery is currently blocked for the caller.
    Return the old signal mask as a set of signals.

    The behavior of the call is dependent on the value of *how*, as follows.

    * [`SIG_BLOCK`](#signal.SIG_BLOCK "signal.SIG_BLOCK"): The set of blocked signals is the union of the current
      set and the *mask* argument.
    * [`SIG_UNBLOCK`](#signal.SIG_UNBLOCK "signal.SIG_UNBLOCK"): The signals in *mask* are removed from the current
      set of blocked signals. It is permissible to attempt to unblock a
      signal which is not blocked.
    * [`SIG_SETMASK`](#signal.SIG_SETMASK "signal.SIG_SETMASK"): The set of blocked signals is set to the *mask*
      argument.

    *mask* is a set of signal numbers (e.g. {[`signal.SIGINT`](#signal.SIGINT "signal.SIGINT"),
    [`signal.SIGTERM`](#signal.SIGTERM "signal.SIGTERM")}). Use [`valid_signals()`](#signal.valid_signals "signal.valid_signals") for a full
    mask including all signals.

    For example, `signal.pthread_sigmask(signal.SIG_BLOCK, [])` reads the
    signal mask of the calling thread.

    [`SIGKILL`](#signal.SIGKILL "signal.SIGKILL") and [`SIGSTOP`](#signal.SIGSTOP "signal.SIGSTOP") cannot be blocked.

    [Availability](intro.html#availability): Unix.

    See the man page *[sigprocmask(2)](https://manpages.debian.org/sigprocmask(2))* and
    *[pthread\_sigmask(3)](https://manpages.debian.org/pthread_sigmask(3))* for further information.

    See also [`pause()`](#signal.pause "signal.pause"), [`sigpending()`](#signal.sigpending "signal.sigpending") and [`sigwait()`](#signal.sigwait "signal.sigwait").

    Added in version 3.3.

signal.setitimer(*which*, *seconds*, *interval=0.0*)
:   Sets given interval timer (one of [`signal.ITIMER_REAL`](#signal.ITIMER_REAL "signal.ITIMER_REAL"),
    [`signal.ITIMER_VIRTUAL`](#signal.ITIMER_VIRTUAL "signal.ITIMER_VIRTUAL") or [`signal.ITIMER_PROF`](#signal.ITIMER_PROF "signal.ITIMER_PROF")) specified
    by *which* to fire after *seconds* (float is accepted, different from
    [`alarm()`](#signal.alarm "signal.alarm")) and after that every *interval* seconds (if *interval*
    is non-zero). The interval timer specified by *which* can be cleared by
    setting *seconds* to zero.

    When an interval timer fires, a signal is sent to the process.
    The signal sent is dependent on the timer being used;
    [`signal.ITIMER_REAL`](#signal.ITIMER_REAL "signal.ITIMER_REAL") will deliver [`SIGALRM`](#signal.SIGALRM "signal.SIGALRM"),
    [`signal.ITIMER_VIRTUAL`](#signal.ITIMER_VIRTUAL "signal.ITIMER_VIRTUAL") sends [`SIGVTALRM`](#signal.SIGVTALRM "signal.SIGVTALRM"),
    and [`signal.ITIMER_PROF`](#signal.ITIMER_PROF "signal.ITIMER_PROF") will deliver [`SIGPROF`](#signal.SIGPROF "signal.SIGPROF").

    The old values are returned as a tuple: (delay, interval).

    Attempting to pass an invalid interval timer will cause an
    [`ItimerError`](#signal.ItimerError "signal.ItimerError").

    [Availability](intro.html#availability): Unix.

signal.getitimer(*which*)
:   Returns current value of a given interval timer specified by *which*.

    [Availability](intro.html#availability): Unix.

signal.set\_wakeup\_fd(*fd*, *\**, *warn\_on\_full\_buffer=True*)
:   Set the wakeup file descriptor to *fd*. When a signal your program has
    registered a signal handler for is received, the signal number is written as
    a single byte into the fd. If you haven’t registered a signal handler for
    the signals you care about, then nothing will be written to the wakeup fd.
    This can be used by a library to wakeup a poll or select call, allowing the
    signal to be fully processed.

    The old wakeup fd is returned (or -1 if file descriptor wakeup was not
    enabled). If *fd* is -1, file descriptor wakeup is disabled.
    If not -1, *fd* must be non-blocking. It is up to the library to remove
    any bytes from *fd* before calling poll or select again.

    When threads are enabled, this function can only be called
    from [the main thread of the main interpreter](#signals-and-threads);
    attempting to call it from other threads will cause a [`ValueError`](exceptions.html#ValueError "ValueError")
    exception to be raised.

    There are two common ways to use this function. In both approaches,
    you use the fd to wake up when a signal arrives, but then they
    differ in how they determine *which* signal or signals have
    arrived.

    In the first approach, we read the data out of the fd’s buffer, and
    the byte values give you the signal numbers. This is simple, but in
    rare cases it can run into a problem: generally the fd will have a
    limited amount of buffer space, and if too many signals arrive too
    quickly, then the buffer may become full, and some signals may be
    lost. If you use this approach, then you should set
    `warn_on_full_buffer=True`, which will at least cause a warning
    to be printed to stderr when signals are lost.

    In the second approach, we use the wakeup fd *only* for wakeups,
    and ignore the actual byte values. In this case, all we care about
    is whether the fd’s buffer is empty or non-empty; a full buffer
    doesn’t indicate a problem at all. If you use this approach, then
    you should set `warn_on_full_buffer=False`, so that your users
    are not confused by spurious warning messages.

    Changed in version 3.5: On Windows, the function now also supports socket handles.

    Changed in version 3.7: Added `warn_on_full_buffer` parameter.

signal.siginterrupt(*signalnum*, *flag*)
:   Change system call restart behaviour: if *flag* is [`False`](constants.html#False "False"), system
    calls will be restarted when interrupted by signal *signalnum*, otherwise
    system calls will be interrupted. Returns nothing.

    [Availability](intro.html#availability): Unix.

    See the man page *[siginterrupt(3)](https://manpages.debian.org/siginterrupt(3))* for further information.

    Note that installing a signal handler with [`signal()`](#module-signal "signal: Set handlers for asynchronous events.") will reset the
    restart behaviour to interruptible by implicitly calling
    `siginterrupt()` with a true *flag* value for the given signal.

signal.signal(*signalnum*, *handler*)
:   Set the handler for signal *signalnum* to the function *handler*. *handler* can
    be a callable Python object taking two arguments (see below), or one of the
    special values [`signal.SIG_IGN`](#signal.SIG_IGN "signal.SIG_IGN") or [`signal.SIG_DFL`](#signal.SIG_DFL "signal.SIG_DFL"). The previous
    signal handler will be returned (see the description of [`getsignal()`](#signal.getsignal "signal.getsignal")
    above). (See the Unix man page *[signal(2)](https://manpages.debian.org/signal(2))* for further information.)

    When threads are enabled, this function can only be called
    from [the main thread of the main interpreter](#signals-and-threads);
    attempting to call it from other threads will cause a [`ValueError`](exceptions.html#ValueError "ValueError")
    exception to be raised.

    The *handler* is called with two arguments: the signal number and the current
    stack frame (`None` or a frame object; for a description of frame objects,
    see the [description in the type hierarchy](../reference/datamodel.html#frame-objects) or see the
    attribute descriptions in the [`inspect`](inspect.html#module-inspect "inspect: Extract information and source code from live objects.") module).

    On Windows, `signal()` can only be called with [`SIGABRT`](#signal.SIGABRT "signal.SIGABRT"),
    [`SIGFPE`](#signal.SIGFPE "signal.SIGFPE"), [`SIGILL`](#signal.SIGILL "signal.SIGILL"), [`SIGINT`](#signal.SIGINT "signal.SIGINT"), [`SIGSEGV`](#signal.SIGSEGV "signal.SIGSEGV"),
    [`SIGTERM`](#signal.SIGTERM "signal.SIGTERM"), or [`SIGBREAK`](#signal.SIGBREAK "signal.SIGBREAK").
    A [`ValueError`](exceptions.html#ValueError "ValueError") will be raised in any other case.
    Note that not all systems define the same set of signal names; an
    [`AttributeError`](exceptions.html#AttributeError "AttributeError") will be raised if a signal name is not defined as
    `SIG*` module level constant.

signal.sigpending()
:   Examine the set of signals that are pending for delivery to the calling
    thread (i.e., the signals which have been raised while blocked). Return the
    set of the pending signals.

    [Availability](intro.html#availability): Unix.

    See the man page *[sigpending(2)](https://manpages.debian.org/sigpending(2))* for further information.

    See also [`pause()`](#signal.pause "signal.pause"), [`pthread_sigmask()`](#signal.pthread_sigmask "signal.pthread_sigmask") and [`sigwait()`](#signal.sigwait "signal.sigwait").

    Added in version 3.3.

signal.sigwait(*sigset*)
:   Suspend execution of the calling thread until the delivery of one of the
    signals specified in the signal set *sigset*. The function accepts the signal
    (removes it from the pending list of signals), and returns the signal number.

    [Availability](intro.html#availability): Unix.

    See the man page *[sigwait(3)](https://manpages.debian.org/sigwait(3))* for further information.

    See also [`pause()`](#signal.pause "signal.pause"), [`pthread_sigmask()`](#signal.pthread_sigmask "signal.pthread_sigmask"), [`sigpending()`](#signal.sigpending "signal.sigpending"),
    [`sigwaitinfo()`](#signal.sigwaitinfo "signal.sigwaitinfo") and [`sigtimedwait()`](#signal.sigtimedwait "signal.sigtimedwait").

    Added in version 3.3.

signal.sigwaitinfo(*sigset*)
:   Suspend execution of the calling thread until the delivery of one of the
    signals specified in the signal set *sigset*. The function accepts the
    signal and removes it from the pending list of signals. If one of the
    signals in *sigset* is already pending for the calling thread, the function
    will return immediately with information about that signal. The signal
    handler is not called for the delivered signal. The function raises an
    [`InterruptedError`](exceptions.html#InterruptedError "InterruptedError") if it is interrupted by a signal that is not in
    *sigset*.

    The return value is an object representing the data contained in the
    `siginfo_t` structure, namely: `si_signo`, `si_code`,
    `si_errno`, `si_pid`, `si_uid`, `si_status`, `si_band`.

    [Availability](intro.html#availability): Unix.

    See the man page *[sigwaitinfo(2)](https://manpages.debian.org/sigwaitinfo(2))* for further information.

    See also [`pause()`](#signal.pause "signal.pause"), [`sigwait()`](#signal.sigwait "signal.sigwait") and [`sigtimedwait()`](#signal.sigtimedwait "signal.sigtimedwait").

    Added in version 3.3.

    Changed in version 3.5: The function is now retried if interrupted by a signal not in *sigset*
    and the signal handler does not raise an exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for
    the rationale).

signal.sigtimedwait(*sigset*, *timeout*)
:   Like [`sigwaitinfo()`](#signal.sigwaitinfo "signal.sigwaitinfo"), but takes an additional *timeout* argument
    specifying a timeout. If *timeout* is specified as `0`, a poll is
    performed. Returns [`None`](constants.html#None "None") if a timeout occurs.

    [Availability](intro.html#availability): Unix.

    See the man page *[sigtimedwait(2)](https://manpages.debian.org/sigtimedwait(2))* for further information.

    See also [`pause()`](#signal.pause "signal.pause"), [`sigwait()`](#signal.sigwait "signal.sigwait") and [`sigwaitinfo()`](#signal.sigwaitinfo "signal.sigwaitinfo").

    Added in version 3.3.

    Changed in version 3.5: The function is now retried with the recomputed *timeout* if interrupted
    by a signal not in *sigset* and the signal handler does not raise an
    exception (see [**PEP 475**](https://peps.python.org/pep-0475/) for the rationale).

## Examples

Here is a minimal example program. It uses the [`alarm()`](#signal.alarm "signal.alarm") function to limit
the time spent waiting to open a file; this is useful if the file is for a
serial device that may not be turned on, which would normally cause the
[`os.open()`](os.html#os.open "os.open") to hang indefinitely. The solution is to set a 5-second alarm
before opening the file; if the operation takes too long, the alarm signal will
be sent, and the handler raises an exception.

```
importsignal,os

defhandler(signum, frame):
    signame = signal.Signals(signum).name
    print(f'Signal handler called with signal {signame} ({signum})')
    raise OSError("Couldn't open device!")

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# This open() may hang indefinitely
fd = os.open('/dev/ttyS0', os.O_RDWR)

signal.alarm(0)          # Disable the alarm
```

## Note on SIGPIPE

Piping output of your program to tools like *[head(1)](https://manpages.debian.org/head(1))* will
cause a [`SIGPIPE`](#signal.SIGPIPE "signal.SIGPIPE") signal to be sent to your process when the receiver
of its standard output closes early. This results in an exception
like `BrokenPipeError: [Errno 32] Broken pipe`. To handle this
case, wrap your entry point to catch this exception as follows:

```
importos
importsys

defmain():
    try:
        # simulate large output (your code replaces this loop)
        for x in range(10000):
            print("y")
        # flush output here to force SIGPIPE to be triggered
        # while inside this try block.
        sys.stdout.flush()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)  # Python exits with error code 1 on EPIPE

if     main()
```

Do not set [`SIGPIPE`](#signal.SIGPIPE "signal.SIGPIPE")’s disposition to [`SIG_DFL`](#signal.SIG_DFL "signal.SIG_DFL") in
order to avoid [`BrokenPipeError`](exceptions.html#BrokenPipeError "BrokenPipeError"). Doing that would cause
your program to exit unexpectedly whenever any socket
connection is interrupted while your program is still writing to
it.

## Note on Signal Handlers and Exceptions

If a signal handler raises an exception, the exception will be propagated to
the main thread and may be raised after any [bytecode](../glossary.html#term-bytecode) instruction. Most
notably, a [`KeyboardInterrupt`](exceptions.html#KeyboardInterrupt "KeyboardInterrupt") may appear at any point during execution.
Most Python code, including the standard library, cannot be made robust against
this, and so a `KeyboardInterrupt` (or any other exception resulting from
a signal handler) may on rare occasions put the program in an unexpected state.

To illustrate this issue, consider the following code:

```
classSpamContext:
    def__init__(self):
        self.lock = threading.Lock()

    def__enter__(self):
        # If KeyboardInterrupt occurs here, everything is fine
        self.lock.acquire()
        # If KeyboardInterrupt occurs here, __exit__ will not be called
        ...
        # KeyboardInterrupt could occur just before the function returns

    def__exit__(self, exc_type, exc_val, exc_tb):
        ...
        self.lock.release()
```

For many programs, especially those that merely want to exit on
[`KeyboardInterrupt`](exceptions.html#KeyboardInterrupt "KeyboardInterrupt"), this is not a problem, but applications that are
complex or require high reliability should avoid raising exceptions from signal
handlers. They should also avoid catching `KeyboardInterrupt` as a means
of gracefully shutting down. Instead, they should install their own
[`SIGINT`](#signal.SIGINT "signal.SIGINT") handler. Below is an example of an HTTP server that avoids
`KeyboardInterrupt`:

```
importsignal
importsocket
fromselectorsimport DefaultSelector, EVENT_READ
fromhttp.serverimport HTTPServer, SimpleHTTPRequestHandler

interrupt_read, interrupt_write = socket.socketpair()

defhandler(signum, frame):
    print('Signal handler called with signal', signum)
    interrupt_write.send(b'\0')
signal.signal(signal.SIGINT, handler)

defserve_forever(httpd):
    sel = DefaultSelector()
    sel.register(interrupt_read, EVENT_READ)
    sel.register(httpd, EVENT_READ)

    while True:
        for key, _ in sel.select():
            if key.fileobj == interrupt_read:
                interrupt_read.recv(1)
                return
            if key.fileobj == httpd:
                httpd.handle_request()

print("Serving on port 8000")
httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
serve_forever(httpd)
print("Shutdown...")
```

---

## Bibliography

1. [Subprocesses](https://docs.python.org/3/library/asyncio-subprocess.html)
2. [`subprocess` — Subprocess management](https://docs.python.org/3/library/subprocess.html)
3. [`signal` — Set handlers for asynchronous events](https://docs.python.org/3/library/signal.html)