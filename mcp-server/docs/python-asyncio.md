# Python asyncio


---

## 1. Streams

**Source code:** [Lib/asyncio/streams.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/streams.py)

---

Streams are high-level async/await-ready primitives to work with
network connections. Streams allow sending and receiving data without
using callbacks or low-level protocols and transports.

Here is an example of a TCP echo client written using asyncio
streams:

```
importasyncio

async deftcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))
```

See also the [Examples](#examples) section below.

Stream Functions

The following top-level asyncio functions can be used to create
and work with streams:

*async*asyncio.open\_connection(*host=None*, *port=None*, *\**, *limit=None*, *ssl=None*, *family=0*, *proto=0*, *flags=0*, *sock=None*, *local\_addr=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *happy\_eyeballs\_delay=None*, *interleave=None*)
:   Establish a network connection and return a pair of
    `(reader, writer)` objects.

    The returned *reader* and *writer* objects are instances of
    [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") and [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") classes.

    *limit* determines the buffer size limit used by the
    returned [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") instance. By default the *limit*
    is set to 64 KiB.

    The rest of the arguments are passed directly to
    [`loop.create_connection()`](asyncio-eventloop.html#asyncio.loop.create_connection "asyncio.loop.create_connection").

    Note

    The *sock* argument transfers ownership of the socket to the
    [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") created. To close the socket, call its
    [`close()`](#asyncio.StreamWriter.close "asyncio.StreamWriter.close") method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.

    Changed in version 3.8: Added the *happy\_eyeballs\_delay* and *interleave* parameters.

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async*asyncio.start\_server(*client\_connected\_cb*, *host=None*, *port=None*, *\**, *limit=None*, *family=socket.AF\_UNSPEC*, *flags=socket.AI\_PASSIVE*, *sock=None*, *backlog=100*, *ssl=None*, *reuse\_address=None*, *reuse\_port=None*, *keep\_alive=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*)
:   Start a socket server.

    The *client\_connected\_cb* callback is called whenever a new client
    connection is established. It receives a `(reader, writer)` pair
    as two arguments, instances of the [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") and
    [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") classes.

    *client\_connected\_cb* can be a plain callable or a
    [coroutine function](asyncio-task.html#coroutine); if it is a coroutine function,
    it will be automatically scheduled as a [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    *limit* determines the buffer size limit used by the
    returned [`StreamReader`](#asyncio.StreamReader "asyncio.StreamReader") instance. By default the *limit*
    is set to 64 KiB.

    The rest of the arguments are passed directly to
    [`loop.create_server()`](asyncio-eventloop.html#asyncio.loop.create_server "asyncio.loop.create_server").

    Note

    The *sock* argument transfers ownership of the socket to the
    server created. To close the socket, call the server’s
    [`close()`](asyncio-eventloop.html#asyncio.Server.close "asyncio.Server.close") method.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* and *start\_serving* parameters.

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.13: Added the *keep\_alive* parameter.

Unix Sockets

*async*asyncio.open\_unix\_connection(*path=None*, *\**, *limit=None*, *ssl=None*, *sock=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Establish a Unix socket connection and return a pair of
    `(reader, writer)`.

    Similar to [`open_connection()`](#asyncio.open_connection "asyncio.open_connection") but operates on Unix sockets.

    See also the documentation of [`loop.create_unix_connection()`](asyncio-eventloop.html#asyncio.loop.create_unix_connection "asyncio.loop.create_unix_connection").

    Note

    The *sock* argument transfers ownership of the socket to the
    [`StreamWriter`](#asyncio.StreamWriter "asyncio.StreamWriter") created. To close the socket, call its
    [`close()`](#asyncio.StreamWriter.close "asyncio.StreamWriter.close") method.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.
    The *path* parameter can now be a [path-like object](../glossary.html#term-path-like-object)

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

*async*asyncio.start\_unix\_server(*client\_connected\_cb*, *path=None*, *\**, *limit=None*, *sock=None*, *backlog=100*, *ssl=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*, *cleanup\_socket=True*)
:   Start a Unix socket server.

    Similar to [`start_server()`](#asyncio.start_server "asyncio.start_server") but works with Unix sockets.

    If *cleanup\_socket* is true then the Unix socket will automatically
    be removed from the filesystem when the server is closed, unless the
    socket has been replaced after the server has been created.

    See also the documentation of [`loop.create_unix_server()`](asyncio-eventloop.html#asyncio.loop.create_unix_server "asyncio.loop.create_unix_server").

    Note

    The *sock* argument transfers ownership of the socket to the
    server created. To close the socket, call the server’s
    [`close()`](asyncio-eventloop.html#asyncio.Server.close "asyncio.Server.close") method.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* and *start\_serving* parameters.
    The *path* parameter can now be a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.13: Added the *cleanup\_socket* parameter.

## StreamReader

*class*asyncio.StreamReader
:   Represents a reader object that provides APIs to read data
    from the IO stream. As an [asynchronous iterable](../glossary.html#term-asynchronous-iterable), the
    object supports the [`async for`](../reference/compound_stmts.html#async-for) statement.

    It is not recommended to instantiate *StreamReader* objects
    directly; use [`open_connection()`](#asyncio.open_connection "asyncio.open_connection") and [`start_server()`](#asyncio.start_server "asyncio.start_server")
    instead.

    feed\_eof()
    :   Acknowledge the EOF.

    *async*read(*n=-1*)
    :   Read up to *n* bytes from the stream.

        If *n* is not provided or set to `-1`,
        read until EOF, then return all read [`bytes`](stdtypes.html#bytes "bytes").
        If EOF was received and the internal buffer is empty,
        return an empty `bytes` object.

        If *n* is `0`, return an empty `bytes` object immediately.

        If *n* is positive, return at most *n* available `bytes`
        as soon as at least 1 byte is available in the internal buffer.
        If EOF is received before any byte is read, return an empty
        `bytes` object.

    *async*readline()
    :   Read one line, where “line” is a sequence of bytes
        ending with `\n`.

        If EOF is received and `\n` was not found, the method
        returns partially read data.

        If EOF is received and the internal buffer is empty,
        return an empty `bytes` object.

    *async*readexactly(*n*)
    :   Read exactly *n* bytes.

        Raise an [`IncompleteReadError`](asyncio-exceptions.html#asyncio.IncompleteReadError "asyncio.IncompleteReadError") if EOF is reached before *n*
        can be read. Use the [`IncompleteReadError.partial`](asyncio-exceptions.html#asyncio.IncompleteReadError.partial "asyncio.IncompleteReadError.partial")
        attribute to get the partially read data.

    *async*readuntil(*separator=b'\n'*)
    :   Read data from the stream until *separator* is found.

        On success, the data and separator will be removed from the
        internal buffer (consumed). Returned data will include the
        separator at the end.

        If the amount of data read exceeds the configured stream limit, a
        [`LimitOverrunError`](asyncio-exceptions.html#asyncio.LimitOverrunError "asyncio.LimitOverrunError") exception is raised, and the data
        is left in the internal buffer and can be read again.

        If EOF is reached before the complete separator is found,
        an [`IncompleteReadError`](asyncio-exceptions.html#asyncio.IncompleteReadError "asyncio.IncompleteReadError") exception is raised, and the internal
        buffer is reset. The [`IncompleteReadError.partial`](asyncio-exceptions.html#asyncio.IncompleteReadError.partial "asyncio.IncompleteReadError.partial") attribute
        may contain a portion of the separator.

        The *separator* may also be a tuple of separators. In this
        case the return value will be the shortest possible that has any
        separator as the suffix. For the purposes of [`LimitOverrunError`](asyncio-exceptions.html#asyncio.LimitOverrunError "asyncio.LimitOverrunError"),
        the shortest possible separator is considered to be the one that
        matched.

        Added in version 3.5.2.

        Changed in version 3.13: The *separator* parameter may now be a [`tuple`](stdtypes.html#tuple "tuple") of
        separators.

    at\_eof()
    :   Return `True` if the buffer is empty and [`feed_eof()`](#asyncio.StreamReader.feed_eof "asyncio.StreamReader.feed_eof")
        was called.

## StreamWriter

*class*asyncio.StreamWriter
:   Represents a writer object that provides APIs to write data
    to the IO stream.

    It is not recommended to instantiate *StreamWriter* objects
    directly; use [`open_connection()`](#asyncio.open_connection "asyncio.open_connection") and [`start_server()`](#asyncio.start_server "asyncio.start_server")
    instead.

    write(*data*)
    :   The method attempts to write the *data* to the underlying socket immediately.
        If that fails, the data is queued in an internal write buffer until it can be
        sent.

        The *data* buffer should be a bytes, bytearray, or C-contiguous one-dimensional
        memoryview object.

        The method should be used along with the `drain()` method:

        ```
        stream.write(data)
        await stream.drain()
        ```

    writelines(*data*)
    :   The method writes a list (or any iterable) of bytes to the underlying socket
        immediately.
        If that fails, the data is queued in an internal write buffer until it can be
        sent.

        The method should be used along with the `drain()` method:

        ```
        stream.writelines(lines)
        await stream.drain()
        ```

    close()
    :   The method closes the stream and the underlying socket.

        The method should be used, though not mandatory,
        along with the `wait_closed()` method:

        ```
        stream.close()
        await stream.wait_closed()
        ```

    can\_write\_eof()
    :   Return `True` if the underlying transport supports
        the [`write_eof()`](#asyncio.StreamWriter.write_eof "asyncio.StreamWriter.write_eof") method, `False` otherwise.

    write\_eof()
    :   Close the write end of the stream after the buffered write
        data is flushed.

    transport
    :   Return the underlying asyncio transport.

    get\_extra\_info(*name*, *default=None*)
    :   Access optional transport information; see
        [`BaseTransport.get_extra_info()`](asyncio-protocol.html#asyncio.BaseTransport.get_extra_info "asyncio.BaseTransport.get_extra_info") for details.

    *async*drain()
    :   Wait until it is appropriate to resume writing to the stream.
        Example:

        ```
        writer.write(data)
        await writer.drain()
        ```

        This is a flow control method that interacts with the underlying
        IO write buffer. When the size of the buffer reaches
        the high watermark, *drain()* blocks until the size of the
        buffer is drained down to the low watermark and writing can
        be resumed. When there is nothing to wait for, the `drain()`
        returns immediately.

    *async*start\_tls(*sslcontext*, *\**, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
    :   Upgrade an existing stream-based connection to TLS.

        Parameters:

        * *sslcontext*: a configured instance of [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext").
        * *server\_hostname*: sets or overrides the host name that the target
          server’s certificate will be matched against.
        * *ssl\_handshake\_timeout* is the time in seconds to wait for the TLS
          handshake to complete before aborting the connection. `60.0` seconds
          if `None` (default).
        * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
          to complete before aborting the connection. `30.0` seconds if `None`
          (default).

        Added in version 3.11.

        Changed in version 3.12: Added the *ssl\_shutdown\_timeout* parameter.

    is\_closing()
    :   Return `True` if the stream is closed or in the process of
        being closed.

        Added in version 3.7.

    *async*wait\_closed()
    :   Wait until the stream is closed.

        Should be called after [`close()`](#asyncio.StreamWriter.close "asyncio.StreamWriter.close") to wait until the underlying
        connection is closed, ensuring that all data has been flushed
        before e.g. exiting the program.

        Added in version 3.7.

## Examples

### TCP echo client using streams

TCP echo client using the [`asyncio.open_connection()`](#asyncio.open_connection "asyncio.open_connection") function:

```
importasyncio

async deftcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))
```

See also

The [TCP echo client protocol](asyncio-protocol.html#asyncio-example-tcp-echo-client-protocol)
example uses the low-level [`loop.create_connection()`](asyncio-eventloop.html#asyncio.loop.create_connection "asyncio.loop.create_connection") method.

### TCP echo server using streams

TCP echo server using the [`asyncio.start_server()`](#asyncio.start_server "asyncio.start_server") function:

```
importasyncio

async defhandle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

async defmain():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
```

See also

The [TCP echo server protocol](asyncio-protocol.html#asyncio-example-tcp-echo-server-protocol)
example uses the [`loop.create_server()`](asyncio-eventloop.html#asyncio.loop.create_server "asyncio.loop.create_server") method.

### Register an open socket to wait for data using streams

Coroutine waiting until a socket receives data using the
[`open_connection()`](#asyncio.open_connection "asyncio.open_connection") function:

```
importasyncio
importsocket

async defwait_for_data():
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()

    # Register the open socket to wait for data.
    reader, writer = await asyncio.open_connection(sock=rsock)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = await reader.read(100)

    # Got data, we are done: close the socket
    print("Received:", data.decode())
    writer.close()
    await writer.wait_closed()

    # Close the second socket
    wsock.close()

asyncio.run(wait_for_data())
```

See also

The [register an open socket to wait for data using a protocol](asyncio-protocol.html#asyncio-example-create-connection) example uses a low-level protocol and
the [`loop.create_connection()`](asyncio-eventloop.html#asyncio.loop.create_connection "asyncio.loop.create_connection") method.

The [watch a file descriptor for read events](asyncio-eventloop.html#asyncio-example-watch-fd) example uses the low-level
[`loop.add_reader()`](asyncio-eventloop.html#asyncio.loop.add_reader "asyncio.loop.add_reader") method to watch a file descriptor.

---

## 2. Subprocesses

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

## 3. Event loop

**Source code:** [Lib/asyncio/events.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/events.py),
[Lib/asyncio/base\_events.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/base_events.py)

---

Preface

The event loop is the core of every asyncio application.
Event loops run asynchronous tasks and callbacks, perform network
IO operations, and run subprocesses.

Application developers should typically use the high-level asyncio functions,
such as [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run"), and should rarely need to reference the loop
object or call its methods. This section is intended mostly for authors
of lower-level code, libraries, and frameworks, who need finer control over
the event loop behavior.

Obtaining the Event Loop

The following low-level functions can be used to get, set, or create
an event loop:

asyncio.get\_running\_loop()
:   Return the running event loop in the current OS thread.

    Raise a [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if there is no running event loop.

    This function can only be called from a coroutine or a callback.

    Added in version 3.7.

asyncio.get\_event\_loop()
:   Get the current event loop.

    When called from a coroutine or a callback (e.g. scheduled with
    call\_soon or similar API), this function will always return the
    running event loop.

    If there is no running event loop set, the function will return
    the result of the `get_event_loop_policy().get_event_loop()` call.

    Because this function has rather complex behavior (especially
    when custom event loop policies are in use), using the
    [`get_running_loop()`](#asyncio.get_running_loop "asyncio.get_running_loop") function is preferred to `get_event_loop()`
    in coroutines and callbacks.

    As noted above, consider using the higher-level [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run") function,
    instead of using these lower level functions to manually create and close an
    event loop.

    Changed in version 3.14: Raises a [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if there is no current event loop.

    Note

    The `asyncio` policy system is deprecated and will be removed
    in Python 3.16; from there on, this function will return the current
    running event loop if present else it will return the
    loop set by [`set_event_loop()`](#asyncio.set_event_loop "asyncio.set_event_loop").

asyncio.set\_event\_loop(*loop*)
:   Set *loop* as the current event loop for the current OS thread.

asyncio.new\_event\_loop()
:   Create and return a new event loop object.

Note that the behaviour of [`get_event_loop()`](#asyncio.get_event_loop "asyncio.get_event_loop"), [`set_event_loop()`](#asyncio.set_event_loop "asyncio.set_event_loop"),
and [`new_event_loop()`](#asyncio.new_event_loop "asyncio.new_event_loop") functions can be altered by
[setting a custom event loop policy](asyncio-policy.html#asyncio-policies).

Contents

This documentation page contains the following sections:

* The [Event Loop Methods](#event-loop-methods) section is the reference documentation of
  the event loop APIs;
* The [Callback Handles](#callback-handles) section documents the [`Handle`](#asyncio.Handle "asyncio.Handle") and
  [`TimerHandle`](#asyncio.TimerHandle "asyncio.TimerHandle") instances which are returned from scheduling
  methods such as [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon") and [`loop.call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later");
* The [Server Objects](#server-objects) section documents types returned from
  event loop methods like [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server");
* The [Event Loop Implementations](#event-loop-implementations) section documents the
  [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") and [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") classes;
* The [Examples](#examples) section showcases how to work with some event
  loop APIs.

## Event loop methods

Event loops have **low-level** APIs for the following:

### 

loop.run\_until\_complete(*future*)
:   Run until the *future* (an instance of [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future")) has
    completed.

    If the argument is a [coroutine object](asyncio-task.html#coroutine) it
    is implicitly scheduled to run as a [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    Return the Future’s result or raise its exception.

loop.run\_forever()
:   Run the event loop until [`stop()`](#asyncio.loop.stop "asyncio.loop.stop") is called.

    If [`stop()`](#asyncio.loop.stop "asyncio.loop.stop") is called before `run_forever()` is called,
    the loop will poll the I/O selector once with a timeout of zero,
    run all callbacks scheduled in response to I/O events (and
    those that were already scheduled), and then exit.

    If [`stop()`](#asyncio.loop.stop "asyncio.loop.stop") is called while `run_forever()` is running,
    the loop will run the current batch of callbacks and then exit.
    Note that new callbacks scheduled by callbacks will not run in this
    case; instead, they will run the next time `run_forever()` or
    [`run_until_complete()`](#asyncio.loop.run_until_complete "asyncio.loop.run_until_complete") is called.

loop.stop()
:   Stop the event loop.

loop.is\_running()
:   Return `True` if the event loop is currently running.

loop.is\_closed()
:   Return `True` if the event loop was closed.

loop.close()
:   Close the event loop.

    The loop must not be running when this function is called.
    Any pending callbacks will be discarded.

    This method clears all queues and shuts down the executor, but does
    not wait for the executor to finish.

    This method is idempotent and irreversible. No other methods
    should be called after the event loop is closed.

*async*loop.shutdown\_asyncgens()
:   Schedule all currently open [asynchronous generator](../glossary.html#term-asynchronous-generator) objects to
    close with an [`aclose()`](../reference/expressions.html#agen.aclose "agen.aclose") call. After calling this method,
    the event loop will issue a warning if a new asynchronous generator
    is iterated. This should be used to reliably finalize all scheduled
    asynchronous generators.

    Note that there is no need to call this function when
    [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run") is used.

    Example:

    ```
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    ```

    Added in version 3.6.

*async*loop.shutdown\_default\_executor(*timeout=None*)
:   Schedule the closure of the default executor and wait for it to join all of
    the threads in the [`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor").
    Once this method has been called,
    using the default executor with [`loop.run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor")
    will raise a [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

    The *timeout* parameter specifies the amount of time
    (in [`float`](functions.html#float "float") seconds) the executor will be given to finish joining.
    With the default, `None`,
    the executor is allowed an unlimited amount of time.

    If the *timeout* is reached, a [`RuntimeWarning`](exceptions.html#RuntimeWarning "RuntimeWarning") is emitted
    and the default executor is terminated
    without waiting for its threads to finish joining.

    Note

    Do not call this method when using [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run"),
    as the latter handles default executor shutdown automatically.

    Added in version 3.9.

    Changed in version 3.12: Added the *timeout* parameter.

### 

loop.call\_soon(*callback*, *\*args*, *context=None*)
:   Schedule the *callback* [callback](../glossary.html#term-callback) to be called with
    *args* arguments at the next iteration of the event loop.

    Return an instance of [`asyncio.Handle`](#asyncio.Handle "asyncio.Handle"),
    which can be used later to cancel the callback.

    Callbacks are called in the order in which they are registered.
    Each callback will be called exactly once.

    The optional keyword-only *context* argument specifies a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *callback* to run in.
    Callbacks use the current context when no *context* is provided.

    Unlike [`call_soon_threadsafe()`](#asyncio.loop.call_soon_threadsafe "asyncio.loop.call_soon_threadsafe"), this method is not thread-safe.

loop.call\_soon\_threadsafe(*callback*, *\*args*, *context=None*)
:   A thread-safe variant of [`call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon"). When scheduling callbacks from
    another thread, this function *must* be used, since `call_soon()` is not
    thread-safe.

    This function is safe to be called from a reentrant context or signal handler,
    however, it is not safe or fruitful to use the returned handle in such contexts.

    Raises [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if called on a loop that’s been closed.
    This can happen on a secondary thread when the main application is
    shutting down.

    See the [concurrency and multithreading](asyncio-dev.html#asyncio-multithreading)
    section of the documentation.

    Changed in version 3.7: The *context* keyword-only parameter was added. See [**PEP 567**](https://peps.python.org/pep-0567/)
    for more details.

Note

Most [`asyncio`](asyncio.html#module-asyncio "asyncio: Asynchronous I/O.") scheduling functions don’t allow passing
keyword arguments. To do that, use [`functools.partial()`](functools.html#functools.partial "functools.partial"):

```
# will schedule "print("Hello", flush=True)"
loop.call_soon(
    functools.partial(print, "Hello", flush=True))
```

Using partial objects is usually more convenient than using lambdas,
as asyncio can render partial objects better in debug and error
messages.

### 

Event loop provides mechanisms to schedule callback functions
to be called at some point in the future. Event loop uses monotonic
clocks to track time.

loop.call\_later(*delay*, *callback*, *\*args*, *context=None*)
:   Schedule *callback* to be called after the given *delay*
    number of seconds (can be either an int or a float).

    An instance of [`asyncio.TimerHandle`](#asyncio.TimerHandle "asyncio.TimerHandle") is returned which can
    be used to cancel the callback.

    *callback* will be called exactly once. If two callbacks are
    scheduled for exactly the same time, the order in which they
    are called is undefined.

    The optional positional *args* will be passed to the callback when
    it is called. Use [`functools.partial()`](functools.html#functools.partial "functools.partial")
    [to pass keyword arguments](#asyncio-pass-keywords) to
    *callback*.

    An optional keyword-only *context* argument allows specifying a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *callback* to run in.
    The current context is used when no *context* is provided.

    Note

    For performance, callbacks scheduled with `loop.call_later()`
    may run up to one clock-resolution early (see
    `time.get_clock_info('monotonic').resolution`).

    Changed in version 3.7: The *context* keyword-only parameter was added. See [**PEP 567**](https://peps.python.org/pep-0567/)
    for more details.

    Changed in version 3.8: In Python 3.7 and earlier with the default event loop implementation,
    the *delay* could not exceed one day.
    This has been fixed in Python 3.8.

loop.call\_at(*when*, *callback*, *\*args*, *context=None*)
:   Schedule *callback* to be called at the given absolute timestamp
    *when* (an int or a float), using the same time reference as
    [`loop.time()`](#asyncio.loop.time "asyncio.loop.time").

    This method’s behavior is the same as [`call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later").

    An instance of [`asyncio.TimerHandle`](#asyncio.TimerHandle "asyncio.TimerHandle") is returned which can
    be used to cancel the callback.

    Note

    For performance, callbacks scheduled with `loop.call_at()`
    may run up to one clock-resolution early (see
    `time.get_clock_info('monotonic').resolution`).

    Changed in version 3.7: The *context* keyword-only parameter was added. See [**PEP 567**](https://peps.python.org/pep-0567/)
    for more details.

    Changed in version 3.8: In Python 3.7 and earlier with the default event loop implementation,
    the difference between *when* and the current time could not exceed
    one day. This has been fixed in Python 3.8.

loop.time()
:   Return the current time, as a [`float`](functions.html#float "float") value, according to
    the event loop’s internal monotonic clock.

Note

Changed in version 3.8: In Python 3.7 and earlier timeouts (relative *delay* or absolute *when*)
should not exceed one day. This has been fixed in Python 3.8.

See also

The [`asyncio.sleep()`](asyncio-task.html#asyncio.sleep "asyncio.sleep") function.

### 

loop.create\_future()
:   Create an [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") object attached to the event loop.

    This is the preferred way to create Futures in asyncio. This lets
    third-party event loops provide alternative implementations of
    the Future object (with better performance or instrumentation).

    Added in version 3.5.2.

loop.create\_task(*coro*, *\**, *name=None*, *context=None*, *eager\_start=None*, *\*\*kwargs*)
:   Schedule the execution of [coroutine](asyncio-task.html#coroutine) *coro*.
    Return a [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") object.

    Third-party event loops can use their own subclass of [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task")
    for interoperability. In this case, the result type is a subclass
    of `Task`.

    The full function signature is largely the same as that of the
    [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") constructor (or factory) - all of the keyword arguments to
    this function are passed through to that interface.

    If the *name* argument is provided and not `None`, it is set as
    the name of the task using [`Task.set_name()`](asyncio-task.html#asyncio.Task.set_name "asyncio.Task.set_name").

    An optional keyword-only *context* argument allows specifying a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *coro* to run in.
    The current context copy is created when no *context* is provided.

    An optional keyword-only *eager\_start* argument allows specifying
    if the task should execute eagerly during the call to create\_task,
    or be scheduled later. If *eager\_start* is not passed the mode set
    by [`loop.set_task_factory()`](#asyncio.loop.set_task_factory "asyncio.loop.set_task_factory") will be used.

    Changed in version 3.8: Added the *name* parameter.

    Changed in version 3.11: Added the *context* parameter.

    Changed in version 3.13.3: Added `kwargs` which passes on arbitrary extra parameters, including `name` and `context`.

    Changed in version 3.13.4: Rolled back the change that passes on *name* and *context* (if it is None),
    while still passing on other arbitrary keyword arguments (to avoid breaking backwards compatibility with 3.13.3).

    Changed in version 3.14: All *kwargs* are now passed on. The *eager\_start* parameter works with eager task factories.

loop.set\_task\_factory(*factory*)
:   Set a task factory that will be used by
    [`loop.create_task()`](#asyncio.loop.create_task "asyncio.loop.create_task").

    If *factory* is `None` the default task factory will be set.
    Otherwise, *factory* must be a *callable* with the signature matching
    `(loop, coro, **kwargs)`, where *loop* is a reference to the active
    event loop, and *coro* is a coroutine object. The callable
    must pass on all *kwargs*, and return a [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task")-compatible object.

    Changed in version 3.13.3: Required that all *kwargs* are passed on to [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task").

    Changed in version 3.13.4: *name* is no longer passed to task factories. *context* is no longer passed
    to task factories if it is `None`.

    Changed in version 3.14: *name* and *context* are now unconditionally passed on to task factories again.

loop.get\_task\_factory()
:   Return a task factory or `None` if the default one is in use.

### 

*async*loop.create\_connection(*protocol\_factory*, *host=None*, *port=None*, *\**, *ssl=None*, *family=0*, *proto=0*, *flags=0*, *sock=None*, *local\_addr=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *happy\_eyeballs\_delay=None*, *interleave=None*, *all\_errors=False*)
:   Open a streaming transport connection to a given
    address specified by *host* and *port*.

    The socket family can be either [`AF_INET`](socket.html#socket.AF_INET "socket.AF_INET") or
    [`AF_INET6`](socket.html#socket.AF_INET6 "socket.AF_INET6") depending on *host* (or the *family*
    argument, if provided).

    The socket type will be [`SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM").

    *protocol\_factory* must be a callable returning an
    [asyncio protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    This method will try to establish the connection in the background.
    When successful, it returns a `(transport, protocol)` pair.

    The chronological synopsis of the underlying operation is as follows:

    1. The connection is established and a [transport](asyncio-protocol.html#asyncio-transport)
       is created for it.
    2. *protocol\_factory* is called without arguments and is expected to
       return a [protocol](asyncio-protocol.html#asyncio-protocol) instance.
    3. The protocol instance is coupled with the transport by calling its
       [`connection_made()`](asyncio-protocol.html#asyncio.BaseProtocol.connection_made "asyncio.BaseProtocol.connection_made") method.
    4. A `(transport, protocol)` tuple is returned on success.

    The created transport is an implementation-dependent bidirectional
    stream.

    Other arguments:

    * *ssl*: if given and not false, a SSL/TLS transport is created
      (by default a plain TCP transport is created). If *ssl* is
      a [`ssl.SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") object, this context is used to create
      the transport; if *ssl* is [`True`](constants.html#True "True"), a default context returned
      from [`ssl.create_default_context()`](ssl.html#ssl.create_default_context "ssl.create_default_context") is used.

      See also

      [SSL/TLS security considerations](ssl.html#ssl-security)
    * *server\_hostname* sets or overrides the hostname that the target
      server’s certificate will be matched against. Should only be passed
      if *ssl* is not `None`. By default the value of the *host* argument
      is used. If *host* is empty, there is no default and you must pass a
      value for *server\_hostname*. If *server\_hostname* is an empty
      string, hostname matching is disabled (which is a serious security
      risk, allowing for potential man-in-the-middle attacks).
    * *family*, *proto*, *flags* are the optional address family, protocol
      and flags to be passed through to getaddrinfo() for *host* resolution.
      If given, these should all be integers from the corresponding
      [`socket`](socket.html#module-socket "socket: Low-level networking interface.") module constants.
    * *happy\_eyeballs\_delay*, if given, enables Happy Eyeballs for this
      connection. It should
      be a floating-point number representing the amount of time in seconds
      to wait for a connection attempt to complete, before starting the next
      attempt in parallel. This is the “Connection Attempt Delay” as defined
      in [**RFC 8305**](https://datatracker.ietf.org/doc/html/rfc8305.html). A sensible default value recommended by the RFC is `0.25`
      (250 milliseconds).
    * *interleave* controls address reordering when a host name resolves to
      multiple IP addresses.
      If `0` or unspecified, no reordering is done, and addresses are
      tried in the order returned by [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo"). If a positive integer
      is specified, the addresses are interleaved by address family, and the
      given integer is interpreted as “First Address Family Count” as defined
      in [**RFC 8305**](https://datatracker.ietf.org/doc/html/rfc8305.html). The default is `0` if *happy\_eyeballs\_delay* is not
      specified, and `1` if it is.
    * *sock*, if given, should be an existing, already connected
      [`socket.socket`](socket.html#socket.socket "socket.socket") object to be used by the transport.
      If *sock* is given, none of *host*, *port*, *family*, *proto*, *flags*,
      *happy\_eyeballs\_delay*, *interleave*
      and *local\_addr* should be specified.

      Note

      The *sock* argument transfers ownership of the socket to the
      transport created. To close the socket, call the transport’s
      [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") method.
    * *local\_addr*, if given, is a `(local_host, local_port)` tuple used
      to bind the socket locally. The *local\_host* and *local\_port*
      are looked up using `getaddrinfo()`, similarly to *host* and *port*.
    * *ssl\_handshake\_timeout* is (for a TLS connection) the time in seconds
      to wait for the TLS handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).
    * *all\_errors* determines what exceptions are raised when a connection cannot
      be created. By default, only a single `Exception` is raised: the first
      exception if there is only one or all errors have same message, or a single
      `OSError` with the error messages combined. When `all_errors` is `True`,
      an `ExceptionGroup` will be raised containing all exceptions (even if there
      is only one).

    Changed in version 3.5: Added support for SSL/TLS in [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop").

    Changed in version 3.6: The socket option [socket.TCP\_NODELAY](socket.html#socket-unix-constants) is set by default
    for all TCP connections.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.

    Changed in version 3.8: Added the *happy\_eyeballs\_delay* and *interleave* parameters.

    Happy Eyeballs Algorithm: Success with Dual-Stack Hosts.
    When a server’s IPv4 path and protocol are working, but the server’s
    IPv6 path and protocol are not working, a dual-stack client
    application experiences significant connection delay compared to an
    IPv4-only client. This is undesirable because it causes the
    dual-stack client to have a worse user experience. This document
    specifies requirements for algorithms that reduce this user-visible
    delay and provides an algorithm.

    For more information: <https://datatracker.ietf.org/doc/html/rfc6555>

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.12: *all\_errors* was added.

    See also

    The [`open_connection()`](asyncio-stream.html#asyncio.open_connection "asyncio.open_connection") function is a high-level alternative
    API. It returns a pair of ([`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader"), [`StreamWriter`](asyncio-stream.html#asyncio.StreamWriter "asyncio.StreamWriter"))
    that can be used directly in async/await code.

*async*loop.create\_datagram\_endpoint(*protocol\_factory*, *local\_addr=None*, *remote\_addr=None*, *\**, *family=0*, *proto=0*, *flags=0*, *reuse\_port=None*, *allow\_broadcast=None*, *sock=None*)
:   Create a datagram connection.

    The socket family can be either [`AF_INET`](socket.html#socket.AF_INET "socket.AF_INET"),
    [`AF_INET6`](socket.html#socket.AF_INET6 "socket.AF_INET6"), or [`AF_UNIX`](socket.html#socket.AF_UNIX "socket.AF_UNIX"),
    depending on *host* (or the *family* argument, if provided).

    The socket type will be [`SOCK_DGRAM`](socket.html#socket.SOCK_DGRAM "socket.SOCK_DGRAM").

    *protocol\_factory* must be a callable returning a
    [protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    A tuple of `(transport, protocol)` is returned on success.

    Other arguments:

    * *local\_addr*, if given, is a `(local_host, local_port)` tuple used
      to bind the socket locally. The *local\_host* and *local\_port*
      are looked up using [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo").

      Note

      On Windows, when using the proactor event loop with `local_addr=None`,
      an [`OSError`](exceptions.html#OSError "OSError") with `errno.WSAEINVAL` will be raised
      when running it.
    * *remote\_addr*, if given, is a `(remote_host, remote_port)` tuple used
      to connect the socket to a remote address. The *remote\_host* and
      *remote\_port* are looked up using [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo").
    * *family*, *proto*, *flags* are the optional address family, protocol
      and flags to be passed through to [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo") for *host*
      resolution. If given, these should all be integers from the
      corresponding [`socket`](socket.html#module-socket "socket: Low-level networking interface.") module constants.
    * *reuse\_port* tells the kernel to allow this endpoint to be bound to the
      same port as other existing endpoints are bound to, so long as they all
      set this flag when being created. This option is not supported on Windows
      and some Unixes. If the [socket.SO\_REUSEPORT](socket.html#socket-unix-constants) constant is not
      defined then this capability is unsupported.
    * *allow\_broadcast* tells the kernel to allow this endpoint to send
      messages to the broadcast address.
    * *sock* can optionally be specified in order to use a preexisting,
      already connected, [`socket.socket`](socket.html#socket.socket "socket.socket") object to be used by the
      transport. If specified, *local\_addr* and *remote\_addr* should be omitted
      (must be [`None`](constants.html#None "None")).

      Note

      The *sock* argument transfers ownership of the socket to the
      transport created. To close the socket, call the transport’s
      [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") method.

    See [UDP echo client protocol](asyncio-protocol.html#asyncio-udp-echo-client-protocol) and
    [UDP echo server protocol](asyncio-protocol.html#asyncio-udp-echo-server-protocol) examples.

    Changed in version 3.4.4: The *family*, *proto*, *flags*, *reuse\_address*, *reuse\_port*,
    *allow\_broadcast*, and *sock* parameters were added.

    Changed in version 3.8: Added support for Windows.

    Changed in version 3.8.1: The *reuse\_address* parameter is no longer supported, as using
    [socket.SO\_REUSEADDR](socket.html#socket-unix-constants)
    poses a significant security concern for
    UDP. Explicitly passing `reuse_address=True` will raise an exception.

    When multiple processes with differing UIDs assign sockets to an
    identical UDP socket address with `SO_REUSEADDR`, incoming packets can
    become randomly distributed among the sockets.

    For supported platforms, *reuse\_port* can be used as a replacement for
    similar functionality. With *reuse\_port*,
    [socket.SO\_REUSEPORT](socket.html#socket-unix-constants)
    is used instead, which specifically
    prevents processes with differing UIDs from assigning sockets to the same
    socket address.

    Changed in version 3.11: The *reuse\_address* parameter, disabled since Python 3.8.1,
    3.7.6 and 3.6.10, has been entirely removed.

*async*loop.create\_unix\_connection(*protocol\_factory*, *path=None*, *\**, *ssl=None*, *sock=None*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Create a Unix connection.

    The socket family will be [`AF_UNIX`](socket.html#socket.AF_UNIX "socket.AF_UNIX"); socket
    type will be [`SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM").

    A tuple of `(transport, protocol)` is returned on success.

    *path* is the name of a Unix domain socket and is required,
    unless a *sock* parameter is specified. Abstract Unix sockets,
    [`str`](stdtypes.html#str "str"), [`bytes`](stdtypes.html#bytes "bytes"), and [`Path`](pathlib.html#pathlib.Path "pathlib.Path") paths are
    supported.

    See the documentation of the [`loop.create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") method
    for information about arguments to this method.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.
    The *path* parameter can now be a [path-like object](../glossary.html#term-path-like-object).

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

### 

*async*loop.create\_server(*protocol\_factory*, *host=None*, *port=None*, *\**, *family=socket.AF\_UNSPEC*, *flags=socket.AI\_PASSIVE*, *sock=None*, *backlog=100*, *ssl=None*, *reuse\_address=None*, *reuse\_port=None*, *keep\_alive=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*)
:   Create a TCP server (socket type [`SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM")) listening
    on *port* of the *host* address.

    Returns a [`Server`](#asyncio.Server "asyncio.Server") object.

    Arguments:

    * *protocol\_factory* must be a callable returning a
      [protocol](asyncio-protocol.html#asyncio-protocol) implementation.
    * The *host* parameter can be set to several types which determine where
      the server would be listening:

      + If *host* is a string, the TCP server is bound to a single network
        interface specified by *host*.
      + If *host* is a sequence of strings, the TCP server is bound to all
        network interfaces specified by the sequence.
      + If *host* is an empty string or `None`, all interfaces are
        assumed and a list of multiple sockets will be returned (most likely
        one for IPv4 and another one for IPv6).
    * The *port* parameter can be set to specify which port the server should
      listen on. If `0` or `None` (the default), a random unused port will
      be selected (note that if *host* resolves to multiple network interfaces,
      a different random port will be selected for each interface).
    * *family* can be set to either [`socket.AF_INET`](socket.html#socket.AF_INET "socket.AF_INET") or
      [`AF_INET6`](socket.html#socket.AF_INET6 "socket.AF_INET6") to force the socket to use IPv4 or IPv6.
      If not set, the *family* will be determined from host name
      (defaults to [`AF_UNSPEC`](socket.html#socket.AF_UNSPEC "socket.AF_UNSPEC")).
    * *flags* is a bitmask for [`getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo").
    * *sock* can optionally be specified in order to use a preexisting
      socket object. If specified, *host* and *port* must not be specified.

      Note

      The *sock* argument transfers ownership of the socket to the
      server created. To close the socket, call the server’s
      [`close()`](#asyncio.Server.close "asyncio.Server.close") method.
    * *backlog* is the maximum number of queued connections passed to
      [`listen()`](socket.html#socket.socket.listen "socket.socket.listen") (defaults to 100).
    * *ssl* can be set to an [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") instance to enable
      TLS over the accepted connections.
    * *reuse\_address* tells the kernel to reuse a local socket in
      `TIME_WAIT` state, without waiting for its natural timeout to
      expire. If not specified will automatically be set to `True` on
      Unix.
    * *reuse\_port* tells the kernel to allow this endpoint to be bound to the
      same port as other existing endpoints are bound to, so long as they all
      set this flag when being created. This option is not supported on
      Windows.
    * *keep\_alive* set to `True` keeps connections active by enabling the
      periodic transmission of messages.

    Changed in version 3.13: Added the *keep\_alive* parameter.

    * *ssl\_handshake\_timeout* is (for a TLS server) the time in seconds to wait
      for the TLS handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).
    * *start\_serving* set to `True` (the default) causes the created server
      to start accepting connections immediately. When set to `False`,
      the user should await on [`Server.start_serving()`](#asyncio.Server.start_serving "asyncio.Server.start_serving") or
      [`Server.serve_forever()`](#asyncio.Server.serve_forever "asyncio.Server.serve_forever") to make the server to start accepting
      connections.

    Changed in version 3.5: Added support for SSL/TLS in [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop").

    Changed in version 3.5.1: The *host* parameter can be a sequence of strings.

    Changed in version 3.6: Added *ssl\_handshake\_timeout* and *start\_serving* parameters.
    The socket option [socket.TCP\_NODELAY](socket.html#socket-unix-constants) is set by default
    for all TCP connections.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    See also

    The [`start_server()`](asyncio-stream.html#asyncio.start_server "asyncio.start_server") function is a higher-level alternative API
    that returns a pair of [`StreamReader`](asyncio-stream.html#asyncio.StreamReader "asyncio.StreamReader") and [`StreamWriter`](asyncio-stream.html#asyncio.StreamWriter "asyncio.StreamWriter")
    that can be used in an async/await code.

*async*loop.create\_unix\_server(*protocol\_factory*, *path=None*, *\**, *sock=None*, *backlog=100*, *ssl=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*, *start\_serving=True*, *cleanup\_socket=True*)
:   Similar to [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") but works with the
    [`AF_UNIX`](socket.html#socket.AF_UNIX "socket.AF_UNIX") socket family.

    *path* is the name of a Unix domain socket, and is required,
    unless a *sock* argument is provided. Abstract Unix sockets,
    [`str`](stdtypes.html#str "str"), [`bytes`](stdtypes.html#bytes "bytes"), and [`Path`](pathlib.html#pathlib.Path "pathlib.Path") paths
    are supported.

    If *cleanup\_socket* is true then the Unix socket will automatically
    be removed from the filesystem when the server is closed, unless the
    socket has been replaced after the server has been created.

    See the documentation of the [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") method
    for information about arguments to this method.

    [Availability](intro.html#availability): Unix.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* and *start\_serving* parameters.
    The *path* parameter can now be a [`Path`](pathlib.html#pathlib.Path "pathlib.Path") object.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

    Changed in version 3.13: Added the *cleanup\_socket* parameter.

*async*loop.connect\_accepted\_socket(*protocol\_factory*, *sock*, *\**, *ssl=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Wrap an already accepted connection into a transport/protocol pair.

    This method can be used by servers that accept connections outside
    of asyncio but that use asyncio to handle them.

    Parameters:

    * *protocol\_factory* must be a callable returning a
      [protocol](asyncio-protocol.html#asyncio-protocol) implementation.
    * *sock* is a preexisting socket object returned from
      [`socket.accept`](socket.html#socket.socket.accept "socket.socket.accept").

      Note

      The *sock* argument transfers ownership of the socket to the
      transport created. To close the socket, call the transport’s
      [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") method.
    * *ssl* can be set to an [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext") to enable SSL over
      the accepted connections.
    * *ssl\_handshake\_timeout* is (for an SSL connection) the time in seconds to
      wait for the SSL handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).

    Returns a `(transport, protocol)` pair.

    Added in version 3.5.3.

    Changed in version 3.7: Added the *ssl\_handshake\_timeout* parameter.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

### 

*async*loop.sendfile(*transport*, *file*, *offset=0*, *count=None*, *\**, *fallback=True*)
:   Send a *file* over a *transport*. Return the total number of bytes
    sent.

    The method uses high-performance [`os.sendfile()`](os.html#os.sendfile "os.sendfile") if available.

    *file* must be a regular file object opened in binary mode.

    *offset* tells from where to start reading the file. If specified,
    *count* is the total number of bytes to transmit as opposed to
    sending the file until EOF is reached. File position is always updated,
    even when this method raises an error, and
    [`file.tell()`](io.html#io.IOBase.tell "io.IOBase.tell") can be used to obtain the actual
    number of bytes sent.

    *fallback* set to `True` makes asyncio to manually read and send
    the file when the platform does not support the sendfile system call
    (e.g. Windows or SSL socket on Unix).

    Raise [`SendfileNotAvailableError`](asyncio-exceptions.html#asyncio.SendfileNotAvailableError "asyncio.SendfileNotAvailableError") if the system does not support
    the *sendfile* syscall and *fallback* is `False`.

    Added in version 3.7.

### 

*async*loop.start\_tls(*transport*, *protocol*, *sslcontext*, *\**, *server\_side=False*, *server\_hostname=None*, *ssl\_handshake\_timeout=None*, *ssl\_shutdown\_timeout=None*)
:   Upgrade an existing transport-based connection to TLS.

    Create a TLS coder/decoder instance and insert it between the *transport*
    and the *protocol*. The coder/decoder implements both *transport*-facing
    protocol and *protocol*-facing transport.

    Return the created two-interface instance. After *await*, the *protocol*
    must stop using the original *transport* and communicate with the returned
    object only because the coder caches *protocol*-side data and sporadically
    exchanges extra TLS session packets with *transport*.

    In some situations (e.g. when the passed transport is already closing) this
    may return `None`.

    Parameters:

    * *transport* and *protocol* instances that methods like
      [`create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") and
      [`create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") return.
    * *sslcontext*: a configured instance of [`SSLContext`](ssl.html#ssl.SSLContext "ssl.SSLContext").
    * *server\_side* pass `True` when a server-side connection is being
      upgraded (like the one created by [`create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server")).
    * *server\_hostname*: sets or overrides the host name that the target
      server’s certificate will be matched against.
    * *ssl\_handshake\_timeout* is (for a TLS connection) the time in seconds to
      wait for the TLS handshake to complete before aborting the connection.
      `60.0` seconds if `None` (default).
    * *ssl\_shutdown\_timeout* is the time in seconds to wait for the SSL shutdown
      to complete before aborting the connection. `30.0` seconds if `None`
      (default).

    Added in version 3.7.

    Changed in version 3.11: Added the *ssl\_shutdown\_timeout* parameter.

### 

loop.add\_reader(*fd*, *callback*, *\*args*)
:   Start monitoring the *fd* file descriptor for read availability and
    invoke *callback* with the specified arguments once *fd* is available for
    reading.

    Any preexisting callback registered for *fd* is cancelled and replaced by
    *callback*.

loop.remove\_reader(*fd*)
:   Stop monitoring the *fd* file descriptor for read availability. Returns
    `True` if *fd* was previously being monitored for reads.

loop.add\_writer(*fd*, *callback*, *\*args*)
:   Start monitoring the *fd* file descriptor for write availability and
    invoke *callback* with the specified arguments *args* once *fd* is
    available for writing.

    Any preexisting callback registered for *fd* is cancelled and replaced by
    *callback*.

    Use [`functools.partial()`](functools.html#functools.partial "functools.partial") [to pass keyword arguments](#asyncio-pass-keywords) to *callback*.

loop.remove\_writer(*fd*)
:   Stop monitoring the *fd* file descriptor for write availability. Returns
    `True` if *fd* was previously being monitored for writes.

See also [Platform Support](asyncio-platforms.html#asyncio-platform-support) section
for some limitations of these methods.

### 

In general, protocol implementations that use transport-based APIs
such as [`loop.create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") and [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server")
are faster than implementations that work with sockets directly.
However, there are some use cases when performance is not critical, and
working with [`socket`](socket.html#socket.socket "socket.socket") objects directly is more
convenient.

*async*loop.sock\_recv(*sock*, *nbytes*)
:   Receive up to *nbytes* from *sock*. Asynchronous version of
    [`socket.recv()`](socket.html#socket.socket.recv "socket.socket.recv").

    Return the received data as a bytes object.

    *sock* must be a non-blocking socket.

    Changed in version 3.7: Even though this method was always documented as a coroutine
    method, releases before Python 3.7 returned a [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").
    Since Python 3.7 this is an `async def` method.

*async*loop.sock\_recv\_into(*sock*, *buf*)
:   Receive data from *sock* into the *buf* buffer. Modeled after the blocking
    [`socket.recv_into()`](socket.html#socket.socket.recv_into "socket.socket.recv_into") method.

    Return the number of bytes written to the buffer.

    *sock* must be a non-blocking socket.

    Added in version 3.7.

*async*loop.sock\_recvfrom(*sock*, *bufsize*)
:   Receive a datagram of up to *bufsize* from *sock*. Asynchronous version of
    [`socket.recvfrom()`](socket.html#socket.socket.recvfrom "socket.socket.recvfrom").

    Return a tuple of (received data, remote address).

    *sock* must be a non-blocking socket.

    Added in version 3.11.

*async*loop.sock\_recvfrom\_into(*sock*, *buf*, *nbytes=0*)
:   Receive a datagram of up to *nbytes* from *sock* into *buf*.
    Asynchronous version of
    [`socket.recvfrom_into()`](socket.html#socket.socket.recvfrom_into "socket.socket.recvfrom_into").

    Return a tuple of (number of bytes received, remote address).

    *sock* must be a non-blocking socket.

    Added in version 3.11.

*async*loop.sock\_sendall(*sock*, *data*)
:   Send *data* to the *sock* socket. Asynchronous version of
    [`socket.sendall()`](socket.html#socket.socket.sendall "socket.socket.sendall").

    This method continues to send to the socket until either all data
    in *data* has been sent or an error occurs. `None` is returned
    on success. On error, an exception is raised. Additionally, there is no way
    to determine how much data, if any, was successfully processed by the
    receiving end of the connection.

    *sock* must be a non-blocking socket.

    Changed in version 3.7: Even though the method was always documented as a coroutine
    method, before Python 3.7 it returned a [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").
    Since Python 3.7, this is an `async def` method.

*async*loop.sock\_sendto(*sock*, *data*, *address*)
:   Send a datagram from *sock* to *address*.
    Asynchronous version of
    [`socket.sendto()`](socket.html#socket.socket.sendto "socket.socket.sendto").

    Return the number of bytes sent.

    *sock* must be a non-blocking socket.

    Added in version 3.11.

*async*loop.sock\_connect(*sock*, *address*)
:   Connect *sock* to a remote socket at *address*.

    Asynchronous version of [`socket.connect()`](socket.html#socket.socket.connect "socket.socket.connect").

    *sock* must be a non-blocking socket.

    Changed in version 3.5.2: `address` no longer needs to be resolved. `sock_connect`
    will try to check if the *address* is already resolved by calling
    [`socket.inet_pton()`](socket.html#socket.inet_pton "socket.inet_pton"). If not,
    [`loop.getaddrinfo()`](#asyncio.loop.getaddrinfo "asyncio.loop.getaddrinfo") will be used to resolve the
    *address*.

    See also

    [`loop.create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection")
    and [`asyncio.open_connection()`](asyncio-stream.html#asyncio.open_connection "asyncio.open_connection").

*async*loop.sock\_accept(*sock*)
:   Accept a connection. Modeled after the blocking
    [`socket.accept()`](socket.html#socket.socket.accept "socket.socket.accept") method.

    The socket must be bound to an address and listening
    for connections. The return value is a pair `(conn, address)` where *conn*
    is a *new* socket object usable to send and receive data on the connection,
    and *address* is the address bound to the socket on the other end of the
    connection.

    *sock* must be a non-blocking socket.

    Changed in version 3.7: Even though the method was always documented as a coroutine
    method, before Python 3.7 it returned a [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future").
    Since Python 3.7, this is an `async def` method.

    See also

    [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") and [`start_server()`](asyncio-stream.html#asyncio.start_server "asyncio.start_server").

*async*loop.sock\_sendfile(*sock*, *file*, *offset=0*, *count=None*, *\**, *fallback=True*)
:   Send a file using high-performance [`os.sendfile`](os.html#os.sendfile "os.sendfile") if possible.
    Return the total number of bytes sent.

    Asynchronous version of [`socket.sendfile()`](socket.html#socket.socket.sendfile "socket.socket.sendfile").

    *sock* must be a non-blocking [`socket.SOCK_STREAM`](socket.html#socket.SOCK_STREAM "socket.SOCK_STREAM")
    [`socket`](socket.html#socket.socket "socket.socket").

    *file* must be a regular file object open in binary mode.

    *offset* tells from where to start reading the file. If specified,
    *count* is the total number of bytes to transmit as opposed to
    sending the file until EOF is reached. File position is always updated,
    even when this method raises an error, and
    [`file.tell()`](io.html#io.IOBase.tell "io.IOBase.tell") can be used to obtain the actual
    number of bytes sent.

    *fallback*, when set to `True`, makes asyncio manually read and send
    the file when the platform does not support the sendfile syscall
    (e.g. Windows or SSL socket on Unix).

    Raise [`SendfileNotAvailableError`](asyncio-exceptions.html#asyncio.SendfileNotAvailableError "asyncio.SendfileNotAvailableError") if the system does not support
    *sendfile* syscall and *fallback* is `False`.

    *sock* must be a non-blocking socket.

    Added in version 3.7.

### 

*async*loop.getaddrinfo(*host*, *port*, *\**, *family=0*, *type=0*, *proto=0*, *flags=0*)
:   Asynchronous version of [`socket.getaddrinfo()`](socket.html#socket.getaddrinfo "socket.getaddrinfo").

*async*loop.getnameinfo(*sockaddr*, *flags=0*)
:   Asynchronous version of [`socket.getnameinfo()`](socket.html#socket.getnameinfo "socket.getnameinfo").

Note

Both *getaddrinfo* and *getnameinfo* internally utilize their synchronous
versions through the loop’s default thread pool executor.
When this executor is saturated, these methods may experience delays,
which higher-level networking libraries may report as increased timeouts.
To mitigate this, consider using a custom executor for other user tasks,
or setting a default executor with a larger number of workers.

Changed in version 3.7: Both *getaddrinfo* and *getnameinfo* methods were always documented
to return a coroutine, but prior to Python 3.7 they were, in fact,
returning [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") objects. Starting with Python 3.7
both methods are coroutines.

### 

*async*loop.connect\_read\_pipe(*protocol\_factory*, *pipe*)
:   Register the read end of *pipe* in the event loop.

    *protocol\_factory* must be a callable returning an
    [asyncio protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    *pipe* is a [file-like object](../glossary.html#term-file-object).

    Return pair `(transport, protocol)`, where *transport* supports
    the [`ReadTransport`](asyncio-protocol.html#asyncio.ReadTransport "asyncio.ReadTransport") interface and *protocol* is an object
    instantiated by the *protocol\_factory*.

    With [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") event loop, the *pipe* is set to
    non-blocking mode.

*async*loop.connect\_write\_pipe(*protocol\_factory*, *pipe*)
:   Register the write end of *pipe* in the event loop.

    *protocol\_factory* must be a callable returning an
    [asyncio protocol](asyncio-protocol.html#asyncio-protocol) implementation.

    *pipe* is [file-like object](../glossary.html#term-file-object).

    Return pair `(transport, protocol)`, where *transport* supports
    [`WriteTransport`](asyncio-protocol.html#asyncio.WriteTransport "asyncio.WriteTransport") interface and *protocol* is an object
    instantiated by the *protocol\_factory*.

    With [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") event loop, the *pipe* is set to
    non-blocking mode.

Note

[`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") does not support the above methods on
Windows. Use [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") instead for Windows.

See also

The [`loop.subprocess_exec()`](#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec") and
[`loop.subprocess_shell()`](#asyncio.loop.subprocess_shell "asyncio.loop.subprocess_shell") methods.

### 

loop.add\_signal\_handler(*signum*, *callback*, *\*args*)
:   Set *callback* as the handler for the *signum* signal,
    passing *args* as positional arguments.

    The callback will be invoked by *loop*, along with other queued callbacks
    and runnable coroutines of that event loop. Unlike signal handlers
    registered using [`signal.signal()`](signal.html#signal.signal "signal.signal"), a callback registered with this
    function is allowed to interact with the event loop.

    Raise [`ValueError`](exceptions.html#ValueError "ValueError") if the signal number is invalid or uncatchable.
    Raise [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") if there is a problem setting up the handler.

    Use [`functools.partial()`](functools.html#functools.partial "functools.partial") [to pass keyword arguments](#asyncio-pass-keywords) to *callback*.

    Like [`signal.signal()`](signal.html#signal.signal "signal.signal"), this function must be invoked in the main
    thread.

loop.remove\_signal\_handler(*sig*)
:   Remove the handler for the *sig* signal.

    Return `True` if the signal handler was removed, or `False` if
    no handler was set for the given signal.

    [Availability](intro.html#availability): Unix.

See also

The [`signal`](signal.html#module-signal "signal: Set handlers for asynchronous events.") module.

### 

*awaitable* loop.run\_in\_executor(*executor*, *func*, *\*args*)
:   Arrange for *func* to be called in the specified executor
    passing *args* as positional arguments.

    The *executor* argument should be an [`concurrent.futures.Executor`](concurrent.futures.html#concurrent.futures.Executor "concurrent.futures.Executor")
    instance. The default executor is used if *executor* is `None`.
    The default executor can be set by [`loop.set_default_executor()`](#asyncio.loop.set_default_executor "asyncio.loop.set_default_executor"),
    otherwise, a [`concurrent.futures.ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor") will be
    lazy-initialized and used by [`run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor") if needed.

    Example:

    ```
    importasyncio
    importconcurrent.futures

    defblocking_io():
        # File operations (such as logging) can block the
        # event loop: run them in a thread pool.
        with open('/dev/urandom', 'rb') as f:
            return f.read(100)

    defcpu_bound():
        # CPU-bound operations will block the event loop:
        # in general it is preferable to run them in a
        # process pool.
        return sum(i * i for i in range(10 ** 7))

    async defmain():
        loop = asyncio.get_running_loop()

        ## Options:

        # 1. Run in the default loop's executor:
        result = await loop.run_in_executor(
            None, blocking_io)
        print('default thread pool', result)

        # 2. Run in a custom thread pool:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, blocking_io)
            print('custom thread pool', result)

        # 3. Run in a custom process pool:
        with concurrent.futures.ProcessPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, cpu_bound)
            print('custom process pool', result)

        # 4. Run in a custom interpreter pool:
        with concurrent.futures.InterpreterPoolExecutor() as pool:
            result = await loop.run_in_executor(
                pool, cpu_bound)
            print('custom interpreter pool', result)

    if         asyncio.run(main())
    ```

    Note that the entry point guard (`if     is required for option 3 due to the peculiarities of [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism."),
    which is used by [`ProcessPoolExecutor`](concurrent.futures.html#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor").
    See [Safe importing of main module](multiprocessing.html#multiprocessing-safe-main-import).

    This method returns a [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") object.

    Use [`functools.partial()`](functools.html#functools.partial "functools.partial") [to pass keyword arguments](#asyncio-pass-keywords) to *func*.

    Changed in version 3.5.3: `loop.run_in_executor()` no longer configures the
    `max_workers` of the thread pool executor it creates, instead
    leaving it up to the thread pool executor
    ([`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor")) to set the
    default.

loop.set\_default\_executor(*executor*)
:   Set *executor* as the default executor used by [`run_in_executor()`](#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor").
    *executor* must be an instance of
    [`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor"), which includes
    [`InterpreterPoolExecutor`](concurrent.futures.html#concurrent.futures.InterpreterPoolExecutor "concurrent.futures.InterpreterPoolExecutor").

    Changed in version 3.11: *executor* must be an instance of
    [`ThreadPoolExecutor`](concurrent.futures.html#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor").

### 

Allows customizing how exceptions are handled in the event loop.

loop.set\_exception\_handler(*handler*)
:   Set *handler* as the new event loop exception handler.

    If *handler* is `None`, the default exception handler will
    be set. Otherwise, *handler* must be a callable with the signature
    matching `(loop, context)`, where `loop`
    is a reference to the active event loop, and `context`
    is a `dict` object containing the details of the exception
    (see [`call_exception_handler()`](#asyncio.loop.call_exception_handler "asyncio.loop.call_exception_handler") documentation for details
    about context).

    If the handler is called on behalf of a [`Task`](asyncio-task.html#asyncio.Task "asyncio.Task") or
    [`Handle`](#asyncio.Handle "asyncio.Handle"), it is run in the
    [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") of that task or callback handle.

    Changed in version 3.12: The handler may be called in the [`Context`](contextvars.html#contextvars.Context "contextvars.Context")
    of the task or handle where the exception originated.

loop.get\_exception\_handler()
:   Return the current exception handler, or `None` if no custom
    exception handler was set.

    Added in version 3.5.2.

loop.default\_exception\_handler(*context*)
:   Default exception handler.

    This is called when an exception occurs and no exception
    handler is set. This can be called by a custom exception
    handler that wants to defer to the default handler behavior.

    *context* parameter has the same meaning as in
    [`call_exception_handler()`](#asyncio.loop.call_exception_handler "asyncio.loop.call_exception_handler").

loop.call\_exception\_handler(*context*)
:   Call the current event loop exception handler.

    *context* is a `dict` object containing the following keys
    (new keys may be introduced in future Python versions):

    * ‘message’: Error message;
    * ‘exception’ (optional): Exception object;
    * ‘future’ (optional): [`asyncio.Future`](asyncio-future.html#asyncio.Future "asyncio.Future") instance;
    * ‘task’ (optional): [`asyncio.Task`](asyncio-task.html#asyncio.Task "asyncio.Task") instance;
    * ‘handle’ (optional): [`asyncio.Handle`](#asyncio.Handle "asyncio.Handle") instance;
    * ‘protocol’ (optional): [Protocol](asyncio-protocol.html#asyncio-protocol) instance;
    * ‘transport’ (optional): [Transport](asyncio-protocol.html#asyncio-transport) instance;
    * ‘socket’ (optional): [`socket.socket`](socket.html#socket.socket "socket.socket") instance;
    * ‘source\_traceback’ (optional): Traceback of the source;
    * ‘handle\_traceback’ (optional): Traceback of the handle;
    * ‘asyncgen’ (optional): Asynchronous generator that caused
      :   the exception.

    Note

    This method should not be overloaded in subclassed
    event loops. For custom exception handling, use
    the [`set_exception_handler()`](#asyncio.loop.set_exception_handler "asyncio.loop.set_exception_handler") method.

### 

loop.get\_debug()
:   Get the debug mode ([`bool`](functions.html#bool "bool")) of the event loop.

    The default value is `True` if the environment variable
    [`PYTHONASYNCIODEBUG`](../using/cmdline.html#envvar-PYTHONASYNCIODEBUG) is set to a non-empty string, `False`
    otherwise.

loop.set\_debug(*enabled:[bool](functions.html#bool "bool")*)
:   Set the debug mode of the event loop.

    Changed in version 3.7: The new [Python Development Mode](devmode.html#devmode) can now also be used
    to enable the debug mode.

loop.slow\_callback\_duration
:   This attribute can be used to set the
    minimum execution duration in seconds that is considered “slow”.
    When debug mode is enabled, “slow” callbacks are logged.

    Default value is 100 milliseconds.

See also

The [debug mode of asyncio](asyncio-dev.html#asyncio-debug-mode).

### 

Methods described in this subsections are low-level. In regular
async/await code consider using the high-level
[`asyncio.create_subprocess_shell()`](asyncio-subprocess.html#asyncio.create_subprocess_shell "asyncio.create_subprocess_shell") and
[`asyncio.create_subprocess_exec()`](asyncio-subprocess.html#asyncio.create_subprocess_exec "asyncio.create_subprocess_exec") convenience functions instead.

Note

On Windows, the default event loop [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") supports
subprocesses, whereas [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") does not. See
[Subprocess Support on Windows](asyncio-platforms.html#asyncio-windows-subprocess) for
details.

*async*loop.subprocess\_exec(*protocol\_factory*, *\*args*, *stdin=subprocess.PIPE*, *stdout=subprocess.PIPE*, *stderr=subprocess.PIPE*, *\*\*kwargs*)
:   Create a subprocess from one or more string arguments specified by
    *args*.

    *args* must be a list of strings represented by:

    * [`str`](stdtypes.html#str "str");
    * or [`bytes`](stdtypes.html#bytes "bytes"), encoded to the
      [filesystem encoding](os.html#filesystem-encoding).

    The first string specifies the program executable,
    and the remaining strings specify the arguments. Together, string
    arguments form the `argv` of the program.

    This is similar to the standard library [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen")
    class called with `shell=False` and the list of strings passed as
    the first argument; however, where `Popen` takes
    a single argument which is list of strings, *subprocess\_exec*
    takes multiple string arguments.

    The *protocol\_factory* must be a callable returning a subclass of the
    [`asyncio.SubprocessProtocol`](asyncio-protocol.html#asyncio.SubprocessProtocol "asyncio.SubprocessProtocol") class.

    Other parameters:

    * *stdin* can be any of these:

      + a file-like object
      + an existing file descriptor (a positive integer), for example those created with [`os.pipe()`](os.html#os.pipe "os.pipe")
      + the [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") constant (default) which will create a new
        pipe and connect it,
      + the value `None` which will make the subprocess inherit the file
        descriptor from this process
      + the [`subprocess.DEVNULL`](subprocess.html#subprocess.DEVNULL "subprocess.DEVNULL") constant which indicates that the
        special [`os.devnull`](os.html#os.devnull "os.devnull") file will be used
    * *stdout* can be any of these:

      + a file-like object
      + the [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") constant (default) which will create a new
        pipe and connect it,
      + the value `None` which will make the subprocess inherit the file
        descriptor from this process
      + the [`subprocess.DEVNULL`](subprocess.html#subprocess.DEVNULL "subprocess.DEVNULL") constant which indicates that the
        special [`os.devnull`](os.html#os.devnull "os.devnull") file will be used
    * *stderr* can be any of these:

      + a file-like object
      + the [`subprocess.PIPE`](subprocess.html#subprocess.PIPE "subprocess.PIPE") constant (default) which will create a new
        pipe and connect it,
      + the value `None` which will make the subprocess inherit the file
        descriptor from this process
      + the [`subprocess.DEVNULL`](subprocess.html#subprocess.DEVNULL "subprocess.DEVNULL") constant which indicates that the
        special [`os.devnull`](os.html#os.devnull "os.devnull") file will be used
      + the [`subprocess.STDOUT`](subprocess.html#subprocess.STDOUT "subprocess.STDOUT") constant which will connect the standard
        error stream to the process’ standard output stream
    * All other keyword arguments are passed to [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen")
      without interpretation, except for *bufsize*, *universal\_newlines*,
      *shell*, *text*, *encoding* and *errors*, which should not be specified
      at all.

      The `asyncio` subprocess API does not support decoding the streams
      as text. [`bytes.decode()`](stdtypes.html#bytes.decode "bytes.decode") can be used to convert the bytes returned
      from the stream to text.

    If a file-like object passed as *stdin*, *stdout* or *stderr* represents a
    pipe, then the other side of this pipe should be registered with
    [`connect_write_pipe()`](#asyncio.loop.connect_write_pipe "asyncio.loop.connect_write_pipe") or [`connect_read_pipe()`](#asyncio.loop.connect_read_pipe "asyncio.loop.connect_read_pipe") for use
    with the event loop.

    See the constructor of the [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen") class
    for documentation on other arguments.

    Returns a pair of `(transport, protocol)`, where *transport*
    conforms to the [`asyncio.SubprocessTransport`](asyncio-protocol.html#asyncio.SubprocessTransport "asyncio.SubprocessTransport") base class and
    *protocol* is an object instantiated by the *protocol\_factory*.

    If the transport is closed or is garbage collected, the child process
    is killed if it is still running.

*async*loop.subprocess\_shell(*protocol\_factory*, *cmd*, *\**, *stdin=subprocess.PIPE*, *stdout=subprocess.PIPE*, *stderr=subprocess.PIPE*, *\*\*kwargs*)
:   Create a subprocess from *cmd*, which can be a [`str`](stdtypes.html#str "str") or a
    [`bytes`](stdtypes.html#bytes "bytes") string encoded to the
    [filesystem encoding](os.html#filesystem-encoding),
    using the platform’s “shell” syntax.

    This is similar to the standard library [`subprocess.Popen`](subprocess.html#subprocess.Popen "subprocess.Popen")
    class called with `shell=True`.

    The *protocol\_factory* must be a callable returning a subclass of the
    [`SubprocessProtocol`](asyncio-protocol.html#asyncio.SubprocessProtocol "asyncio.SubprocessProtocol") class.

    See [`subprocess_exec()`](#asyncio.loop.subprocess_exec "asyncio.loop.subprocess_exec") for more details about
    the remaining arguments.

    Returns a pair of `(transport, protocol)`, where *transport*
    conforms to the [`SubprocessTransport`](asyncio-protocol.html#asyncio.SubprocessTransport "asyncio.SubprocessTransport") base class and
    *protocol* is an object instantiated by the *protocol\_factory*.

    If the transport is closed or is garbage collected, the child process
    is killed if it is still running.

Note

It is the application’s responsibility to ensure that all whitespace
and special characters are quoted appropriately to avoid [shell injection](https://en.wikipedia.org/wiki/Shell_injection#Shell_injection)
vulnerabilities. The [`shlex.quote()`](shlex.html#shlex.quote "shlex.quote") function can be used to
properly escape whitespace and special characters in strings that
are going to be used to construct shell commands.

## Callback handles

*class*asyncio.Handle
:   A callback wrapper object returned by [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon"),
    [`loop.call_soon_threadsafe()`](#asyncio.loop.call_soon_threadsafe "asyncio.loop.call_soon_threadsafe").

    get\_context()
    :   Return the [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") object
        associated with the handle.

        Added in version 3.12.

    cancel()
    :   Cancel the callback. If the callback has already been canceled
        or executed, this method has no effect.

    cancelled()
    :   Return `True` if the callback was cancelled.

        Added in version 3.7.

*class*asyncio.TimerHandle
:   A callback wrapper object returned by [`loop.call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later"),
    and [`loop.call_at()`](#asyncio.loop.call_at "asyncio.loop.call_at").

    This class is a subclass of [`Handle`](#asyncio.Handle "asyncio.Handle").

    when()
    :   Return a scheduled callback time as [`float`](functions.html#float "float") seconds.

        The time is an absolute timestamp, using the same time
        reference as [`loop.time()`](#asyncio.loop.time "asyncio.loop.time").

        Added in version 3.7.

## Server objects

Server objects are created by [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server"),
[`loop.create_unix_server()`](#asyncio.loop.create_unix_server "asyncio.loop.create_unix_server"), [`start_server()`](asyncio-stream.html#asyncio.start_server "asyncio.start_server"),
and [`start_unix_server()`](asyncio-stream.html#asyncio.start_unix_server "asyncio.start_unix_server") functions.

Do not instantiate the [`Server`](#asyncio.Server "asyncio.Server") class directly.

*class*asyncio.Server
:   *Server* objects are asynchronous context managers. When used in an
    `async with` statement, it’s guaranteed that the Server object is
    closed and not accepting new connections when the `async with`
    statement is completed:

    ```
    srv = await loop.create_server(...)

    async with srv:
        # some code

    # At this point, srv is closed and no longer accepts new connections.
    ```

    Changed in version 3.7: Server object is an asynchronous context manager since Python 3.7.

    Changed in version 3.11: This class was exposed publicly as `asyncio.Server` in Python 3.9.11, 3.10.3 and 3.11.

    close()
    :   Stop serving: close listening sockets and set the [`sockets`](#asyncio.Server.sockets "asyncio.Server.sockets")
        attribute to `None`.

        The sockets that represent existing incoming client connections
        are left open.

        The server is closed asynchronously; use the [`wait_closed()`](#asyncio.Server.wait_closed "asyncio.Server.wait_closed")
        coroutine to wait until the server is closed (and no more
        connections are active).

    close\_clients()
    :   Close all existing incoming client connections.

        Calls [`close()`](asyncio-protocol.html#asyncio.BaseTransport.close "asyncio.BaseTransport.close") on all associated
        transports.

        [`close()`](#asyncio.Server.close "asyncio.Server.close") should be called before `close_clients()` when
        closing the server to avoid races with new clients connecting.

        Added in version 3.13.

    abort\_clients()
    :   Close all existing incoming client connections immediately,
        without waiting for pending operations to complete.

        Calls [`abort()`](asyncio-protocol.html#asyncio.WriteTransport.abort "asyncio.WriteTransport.abort") on all associated
        transports.

        [`close()`](#asyncio.Server.close "asyncio.Server.close") should be called before `abort_clients()` when
        closing the server to avoid races with new clients connecting.

        Added in version 3.13.

    get\_loop()
    :   Return the event loop associated with the server object.

        Added in version 3.7.

    *async*start\_serving()
    :   Start accepting connections.

        This method is idempotent, so it can be called when
        the server is already serving.

        The *start\_serving* keyword-only parameter to
        [`loop.create_server()`](#asyncio.loop.create_server "asyncio.loop.create_server") and
        [`asyncio.start_server()`](asyncio-stream.html#asyncio.start_server "asyncio.start_server") allows creating a Server object
        that is not accepting connections initially. In this case
        `Server.start_serving()`, or [`Server.serve_forever()`](#asyncio.Server.serve_forever "asyncio.Server.serve_forever") can be used
        to make the Server start accepting connections.

        Added in version 3.7.

    *async*serve\_forever()
    :   Start accepting connections until the coroutine is cancelled.
        Cancellation of `serve_forever` task causes the server
        to be closed.

        This method can be called if the server is already accepting
        connections. Only one `serve_forever` task can exist per
        one *Server* object.

        Example:

        ```
        async defclient_connected(reader, writer):
            # Communicate with the client with
            # reader/writer streams.  For example:
            await reader.readline()

        async defmain(host, port):
            srv = await asyncio.start_server(
                client_connected, host, port)
            await srv.serve_forever()

        asyncio.run(main('127.0.0.1', 0))
        ```

        Added in version 3.7.

    is\_serving()
    :   Return `True` if the server is accepting new connections.

        Added in version 3.7.

    *async*wait\_closed()
    :   Wait until the [`close()`](#asyncio.Server.close "asyncio.Server.close") method completes and all active
        connections have finished.

    sockets
    :   List of socket-like objects, `asyncio.trsock.TransportSocket`, which
        the server is listening on.

        Changed in version 3.7: Prior to Python 3.7 `Server.sockets` used to return an
        internal list of server sockets directly. In 3.7 a copy
        of that list is returned.

## Event loop implementations

asyncio ships with two different event loop implementations:
[`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") and [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop").

By default asyncio is configured to use [`EventLoop`](#asyncio.EventLoop "asyncio.EventLoop").

*class*asyncio.SelectorEventLoop
:   A subclass of [`AbstractEventLoop`](#asyncio.AbstractEventLoop "asyncio.AbstractEventLoop") based on the
    [`selectors`](selectors.html#module-selectors "selectors: High-level I/O multiplexing.") module.

    Uses the most efficient *selector* available for the given
    platform. It is also possible to manually configure the
    exact selector implementation to be used:

    ```
    importasyncio
    importselectors

    async defmain():
       ...

    loop_factory = lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
    asyncio.run(main(), loop_factory=loop_factory)
    ```

    [Availability](intro.html#availability): Unix, Windows.

*class*asyncio.ProactorEventLoop
:   A subclass of [`AbstractEventLoop`](#asyncio.AbstractEventLoop "asyncio.AbstractEventLoop") for Windows that uses “I/O Completion Ports” (IOCP).

    [Availability](intro.html#availability): Windows.

    See also

    [MSDN documentation on I/O Completion Ports](https://learn.microsoft.com/windows/win32/fileio/i-o-completion-ports).

*class*asyncio.EventLoop
:   > An alias to the most efficient available subclass of [`AbstractEventLoop`](#asyncio.AbstractEventLoop "asyncio.AbstractEventLoop") for the given
    > platform.
    >
    > It is an alias to [`SelectorEventLoop`](#asyncio.SelectorEventLoop "asyncio.SelectorEventLoop") on Unix and [`ProactorEventLoop`](#asyncio.ProactorEventLoop "asyncio.ProactorEventLoop") on Windows.

    Added in version 3.13.

*class*asyncio.AbstractEventLoop
:   Abstract base class for asyncio-compliant event loops.

    The [Event loop methods](#asyncio-event-loop-methods) section lists all
    methods that an alternative implementation of `AbstractEventLoop`
    should have defined.

## Examples

Note that all examples in this section **purposefully** show how
to use the low-level event loop APIs, such as [`loop.run_forever()`](#asyncio.loop.run_forever "asyncio.loop.run_forever")
and [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon"). Modern asyncio applications rarely
need to be written this way; consider using the high-level functions
like [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run").

### Hello World with call\_soon()

An example using the [`loop.call_soon()`](#asyncio.loop.call_soon "asyncio.loop.call_soon") method to schedule a
callback. The callback displays `"Hello World"` and then stops the
event loop:

```
importasyncio

defhello_world(loop):
"""A callback to print 'Hello World' and stop the event loop"""
    print('Hello World')
    loop.stop()

loop = asyncio.new_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world, loop)

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()
```

See also

A similar [Hello World](asyncio-task.html#coroutine)
example created with a coroutine and the [`run()`](asyncio-runner.html#asyncio.run "asyncio.run") function.

### Display the current date with call\_later()

An example of a callback displaying the current date every second. The
callback uses the [`loop.call_later()`](#asyncio.loop.call_later "asyncio.loop.call_later") method to reschedule itself
after 5 seconds, and then stops the event loop:

```
importasyncio
importdatetimeasdt

defdisplay_date(end_time, loop):
    print(dt.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

loop = asyncio.new_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
try:
    loop.run_forever()
finally:
    loop.close()
```

See also

A similar [current date](asyncio-task.html#asyncio-example-sleep) example
created with a coroutine and the [`run()`](asyncio-runner.html#asyncio.run "asyncio.run") function.

### Watch a file descriptor for read events

Wait until a file descriptor received some data using the
[`loop.add_reader()`](#asyncio.loop.add_reader "asyncio.loop.add_reader") method and then close the event loop:

```
importasyncio
fromsocketimport socketpair

# Create a pair of connected file descriptors
rsock, wsock = socketpair()

loop = asyncio.new_event_loop()

defreader():
    data = rsock.recv(100)
    print("Received:", data.decode())

    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)

    # Stop the event loop
    loop.stop()

# Register the file descriptor for read event
loop.add_reader(rsock, reader)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

try:
    # Run the event loop
    loop.run_forever()
finally:
    # We are done. Close sockets and the event loop.
    rsock.close()
    wsock.close()
    loop.close()
```

See also

* A similar [example](asyncio-protocol.html#asyncio-example-create-connection)
  using transports, protocols, and the
  [`loop.create_connection()`](#asyncio.loop.create_connection "asyncio.loop.create_connection") method.
* Another similar [example](asyncio-stream.html#asyncio-example-create-connection-streams)
  using the high-level [`asyncio.open_connection()`](asyncio-stream.html#asyncio.open_connection "asyncio.open_connection") function
  and streams.

### Set signal handlers for SIGINT and SIGTERM

(This `signal` example only works on Unix.)

Register handlers for signals [`SIGINT`](signal.html#signal.SIGINT "signal.SIGINT") and [`SIGTERM`](signal.html#signal.SIGTERM "signal.SIGTERM")
using the [`loop.add_signal_handler()`](#asyncio.loop.add_signal_handler "asyncio.loop.add_signal_handler") method:

```
importasyncio
importfunctools
importos
importsignal

defask_exit(signame, loop):
    print("got signal %s: exit" % signame)
    loop.stop()

async defmain():
    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame, loop))

    await asyncio.sleep(3600)

print("Event loop running for 1 hour, press Ctrl+C to interrupt.")
print(f"pid {os.getpid()}: send SIGINT or SIGTERM to exit.")

asyncio.run(main())
```

---

## 4. Coroutines and tasks

This section outlines high-level asyncio APIs to work with coroutines
and Tasks.

## 

**Source code:** [Lib/asyncio/coroutines.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/coroutines.py)

---

[Coroutines](../glossary.html#term-coroutine) declared with the async/await syntax is the
preferred way of writing asyncio applications. For example, the following
snippet of code prints “hello”, waits 1 second,
and then prints “world”:

```
>>> importasyncio

>>> async defmain():
...     print('hello')
...     await asyncio.sleep(1)
...     print('world')

>>> asyncio.run(main())
hello
world
```

Note that simply calling a coroutine will not schedule it to
be executed:

```
>>> main()
<coroutine object main at 0x1053bb7c8>
```

To actually run a coroutine, asyncio provides the following mechanisms:

* The [`asyncio.run()`](asyncio-runner.html#asyncio.run "asyncio.run") function to run the top-level
  entry point “main()” function (see the above example.)
* Awaiting on a coroutine. The following snippet of code will
  print “hello” after waiting for 1 second, and then print “world”
  after waiting for *another* 2 seconds:

  ```
  importasyncio
  importtime

  async defsay_after(delay, what):
      await asyncio.sleep(delay)
      print(what)

  async defmain():
      print(f"started at {time.strftime('%X')}")

      await say_after(1, 'hello')
      await say_after(2, 'world')

      print(f"finished at {time.strftime('%X')}")

  asyncio.run(main())
  ```

  Expected output:

  ```
  started at 17:13:52
  hello
  world
  finished at 17:13:55
  ```
* The [`asyncio.create_task()`](#asyncio.create_task "asyncio.create_task") function to run coroutines
  concurrently as asyncio [`Tasks`](#asyncio.Task "asyncio.Task").

  Let’s modify the above example and run two `say_after` coroutines
  *concurrently*:

  ```
  async defmain():
      task1 = asyncio.create_task(
          say_after(1, 'hello'))

      task2 = asyncio.create_task(
          say_after(2, 'world'))

      print(f"started at {time.strftime('%X')}")

      # Wait until both tasks are completed (should take
      # around 2 seconds.)
      await task1
      await task2

      print(f"finished at {time.strftime('%X')}")
  ```

  Note that expected output now shows that the snippet runs
  1 second faster than before:

  ```
  started at 17:14:32
  hello
  world
  finished at 17:14:34
  ```
* The [`asyncio.TaskGroup`](#asyncio.TaskGroup "asyncio.TaskGroup") class provides a more modern
  alternative to [`create_task()`](#asyncio.create_task "asyncio.create_task").
  Using this API, the last example becomes:

  ```
  async defmain():
      async with asyncio.TaskGroup() as tg:
          task1 = tg.create_task(
              say_after(1, 'hello'))

          task2 = tg.create_task(
              say_after(2, 'world'))

          print(f"started at {time.strftime('%X')}")

      # The await is implicit when the context manager exits.

      print(f"finished at {time.strftime('%X')}")
  ```

  The timing and output should be the same as for the previous version.

  Added in version 3.11: [`asyncio.TaskGroup`](#asyncio.TaskGroup "asyncio.TaskGroup").

## 

We say that an object is an **awaitable** object if it can be used
in an [`await`](../reference/expressions.html#await) expression. Many asyncio APIs are designed to
accept awaitables.

There are three main types of *awaitable* objects:
**coroutines**, **Tasks**, and **Futures**.

Coroutines

Python coroutines are *awaitables* and therefore can be awaited from
other coroutines:

```
importasyncio

async defnested():
    return 42

async defmain():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    nested()  # will raise a "RuntimeWarning".

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".

asyncio.run(main())
```

Important

In this documentation the term “coroutine” can be used for
two closely related concepts:

* a *coroutine function*: an [`async def`](../reference/compound_stmts.html#async-def) function;
* a *coroutine object*: an object returned by calling a
  *coroutine function*.

Tasks

*Tasks* are used to schedule coroutines *concurrently*.

When a coroutine is wrapped into a *Task* with functions like
[`asyncio.create_task()`](#asyncio.create_task "asyncio.create_task") the coroutine is automatically
scheduled to run soon:

```
importasyncio

async defnested():
    return 42

async defmain():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
```

Futures

A [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future") is a special **low-level** awaitable object that
represents an **eventual result** of an asynchronous operation.

When a Future object is *awaited* it means that the coroutine will
wait until the Future is resolved in some other place.

Future objects in asyncio are needed to allow callback-based code
to be used with async/await.

Normally **there is no need** to create Future objects at the
application level code.

Future objects, sometimes exposed by libraries and some asyncio
APIs, can be awaited:

```
async defmain():
    await function_that_returns_a_future_object()

    # this is also valid:
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )
```

A good example of a low-level function that returns a Future object
is [`loop.run_in_executor()`](asyncio-eventloop.html#asyncio.loop.run_in_executor "asyncio.loop.run_in_executor").

## 

**Source code:** [Lib/asyncio/tasks.py](https://github.com/python/cpython/tree/3.14/Lib/asyncio/tasks.py)

---

asyncio.create\_task(*coro*, *\**, *name=None*, *context=None*, *eager\_start=None*, *\*\*kwargs*)
:   Wrap the *coro* [coroutine](#coroutine) into a [`Task`](#asyncio.Task "asyncio.Task")
    and schedule its execution. Return the Task object.

    The full function signature is largely the same as that of the
    [`Task`](#asyncio.Task "asyncio.Task") constructor (or factory) - all of the keyword arguments to
    this function are passed through to that interface.

    An optional keyword-only *context* argument allows specifying a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *coro* to run in.
    The current context copy is created when no *context* is provided.

    An optional keyword-only *eager\_start* argument allows specifying
    if the task should execute eagerly during the call to create\_task,
    or be scheduled later. If *eager\_start* is not passed the mode set
    by [`loop.set_task_factory()`](asyncio-eventloop.html#asyncio.loop.set_task_factory "asyncio.loop.set_task_factory") will be used.

    The task is executed in the loop returned by [`get_running_loop()`](asyncio-eventloop.html#asyncio.get_running_loop "asyncio.get_running_loop"),
    [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError") is raised if there is no running loop in
    current thread.

    Note

    [`asyncio.TaskGroup.create_task()`](#asyncio.TaskGroup.create_task "asyncio.TaskGroup.create_task") is a new alternative
    leveraging structural concurrency; it allows for waiting
    for a group of related tasks with strong safety guarantees.

    Important

    Save a reference to the result of this function, to avoid
    a task disappearing mid-execution. The event loop only keeps
    weak references to tasks. A task that isn’t referenced elsewhere
    may get garbage collected at any time, even before it’s done.
    For reliable “fire-and-forget” background tasks, gather them in
    a collection:

    ```
    background_tasks = set()

    for i in range(10):
        task = asyncio.create_task(some_coro(param=i))

        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)

        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after
        # completion:
        task.add_done_callback(background_tasks.discard)
    ```

    Added in version 3.7.

    Changed in version 3.8: Added the *name* parameter.

    Changed in version 3.11: Added the *context* parameter.

    Changed in version 3.14: Added the *eager\_start* parameter by passing on all *kwargs*.

## 

Tasks can easily and safely be cancelled.
When a task is cancelled, [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") will be raised
in the task at the next opportunity.

It is recommended that coroutines use `try/finally` blocks to robustly
perform clean-up logic. In case [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError")
is explicitly caught, it should generally be propagated when
clean-up is complete. `asyncio.CancelledError` directly subclasses
[`BaseException`](exceptions.html#BaseException "BaseException") so most code will not need to be aware of it.

The asyncio components that enable structured concurrency, like
[`asyncio.TaskGroup`](#asyncio.TaskGroup "asyncio.TaskGroup") and [`asyncio.timeout()`](#asyncio.timeout "asyncio.timeout"),
are implemented using cancellation internally and might misbehave if
a coroutine swallows [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError"). Similarly, user code
should not generally call [`uncancel`](#asyncio.Task.uncancel "asyncio.Task.uncancel").
However, in cases when suppressing `asyncio.CancelledError` is
truly desired, it is necessary to also call `uncancel()` to completely
remove the cancellation state.

## 

Task groups combine a task creation API with a convenient
and reliable way to wait for all tasks in the group to finish.

*class*asyncio.TaskGroup
:   An [asynchronous context manager](../reference/datamodel.html#async-context-managers)
    holding a group of tasks.
    Tasks can be added to the group using [`create_task()`](#asyncio.create_task "asyncio.create_task").
    All tasks are awaited when the context manager exits.

    Added in version 3.11.

    create\_task(*coro*, *\**, *name=None*, *context=None*, *eager\_start=None*, *\*\*kwargs*)
    :   Create a task in this task group.
        The signature matches that of [`asyncio.create_task()`](#asyncio.create_task "asyncio.create_task").
        If the task group is inactive (e.g. not yet entered,
        already finished, or in the process of shutting down),
        we will close the given `coro`.

        Changed in version 3.13: Close the given coroutine if the task group is not active.

        Changed in version 3.14: Passes on all *kwargs* to [`loop.create_task()`](asyncio-eventloop.html#asyncio.loop.create_task "asyncio.loop.create_task")

Example:

```
async defmain():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(some_coro(...))
        task2 = tg.create_task(another_coro(...))
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
```

The `async with` statement will wait for all tasks in the group to finish.
While waiting, new tasks may still be added to the group
(for example, by passing `tg` into one of the coroutines
and calling `tg.create_task()` in that coroutine).
Once the last task has finished and the `async with` block is exited,
no new tasks may be added to the group.

The first time any of the tasks belonging to the group fails
with an exception other than [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError"),
the remaining tasks in the group are cancelled.
No further tasks can then be added to the group.
At this point, if the body of the `async with` statement is still active
(i.e., [`__aexit__()`](../reference/datamodel.html#object.__aexit__ "object.__aexit__") hasn’t been called yet),
the task directly containing the `async with` statement is also cancelled.
The resulting `asyncio.CancelledError` will interrupt an `await`,
but it will not bubble out of the containing `async with` statement.

Once all tasks have finished, if any tasks have failed
with an exception other than [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError"),
those exceptions are combined in an
[`ExceptionGroup`](exceptions.html#ExceptionGroup "ExceptionGroup") or [`BaseExceptionGroup`](exceptions.html#BaseExceptionGroup "BaseExceptionGroup")
(as appropriate; see their documentation)
which is then raised.

Two base exceptions are treated specially:
If any task fails with [`KeyboardInterrupt`](exceptions.html#KeyboardInterrupt "KeyboardInterrupt") or [`SystemExit`](exceptions.html#SystemExit "SystemExit"),
the task group still cancels the remaining tasks and waits for them,
but then the initial `KeyboardInterrupt` or `SystemExit`
is re-raised instead of [`ExceptionGroup`](exceptions.html#ExceptionGroup "ExceptionGroup") or [`BaseExceptionGroup`](exceptions.html#BaseExceptionGroup "BaseExceptionGroup").

If the body of the `async with` statement exits with an exception
(so [`__aexit__()`](../reference/datamodel.html#object.__aexit__ "object.__aexit__") is called with an exception set),
this is treated the same as if one of the tasks failed:
the remaining tasks are cancelled and then waited for,
and non-cancellation exceptions are grouped into an
exception group and raised.
The exception passed into `__aexit__()`,
unless it is [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError"),
is also included in the exception group.
The same special case is made for
[`KeyboardInterrupt`](exceptions.html#KeyboardInterrupt "KeyboardInterrupt") and [`SystemExit`](exceptions.html#SystemExit "SystemExit") as in the previous paragraph.

Task groups are careful not to mix up the internal cancellation used to
“wake up” their [`__aexit__()`](../reference/datamodel.html#object.__aexit__ "object.__aexit__") with cancellation requests
for the task in which they are running made by other parties.
In particular, when one task group is syntactically nested in another,
and both experience an exception in one of their child tasks simultaneously,
the inner task group will process its exceptions, and then the outer task group
will receive another cancellation and process its own exceptions.

In the case where a task group is cancelled externally and also must
raise an [`ExceptionGroup`](exceptions.html#ExceptionGroup "ExceptionGroup"), it will call the parent task’s
[`cancel()`](#asyncio.Task.cancel "asyncio.Task.cancel") method. This ensures that a
[`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") will be raised at the next
[`await`](../reference/expressions.html#await), so the cancellation is not lost.

Task groups preserve the cancellation count
reported by [`asyncio.Task.cancelling()`](#asyncio.Task.cancelling "asyncio.Task.cancelling").

Changed in version 3.13: Improved handling of simultaneous internal and external cancellations
and correct preservation of cancellation counts.

### Terminating a task group

While terminating a task group is not natively supported by the standard
library, termination can be achieved by adding an exception-raising task
to the task group and ignoring the raised exception:

```
importasyncio
fromasyncioimport TaskGroup

classTerminateTaskGroup(Exception):
"""Exception raised to terminate a task group."""

async defforce_terminate_task_group():
"""Used to force termination of a task group."""
    raise TerminateTaskGroup()

async defjob(task_id, sleep_time):
    print(f'Task {task_id}: start')
    await asyncio.sleep(sleep_time)
    print(f'Task {task_id}: done')

async defmain():
    try:
        async with TaskGroup() as group:
            # spawn some tasks
            group.create_task(job(1, 0.5))
            group.create_task(job(2, 1.5))
            # sleep for 1 second
            await asyncio.sleep(1)
            # add an exception-raising task to force the group to terminate
            group.create_task(force_terminate_task_group())
    except* TerminateTaskGroup:
        pass

asyncio.run(main())
```

Expected output:

```
Task 1: start
Task 2: start
Task 1: done
```

## 

*async*asyncio.sleep(*delay*, *result=None*)
:   Block for *delay* seconds.

    If *result* is provided, it is returned to the caller
    when the coroutine completes.

    `sleep()` always suspends the current task, allowing other tasks
    to run.

    Setting the delay to 0 provides an optimized path to allow other
    tasks to run. This can be used by long-running functions to avoid
    blocking the event loop for the full duration of the function call.

    Example of coroutine displaying the current date every second
    for 5 seconds:

    ```
    importasyncio
    importdatetimeasdt

    async defdisplay_date():
        loop = asyncio.get_running_loop()
        end_time = loop.time() + 5.0
        while True:
            print(dt.datetime.now())
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(1)

    asyncio.run(display_date())
    ```

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.13: Raises [`ValueError`](exceptions.html#ValueError "ValueError") if *delay* is [`nan`](math.html#math.nan "math.nan").

## 

*awaitable* asyncio.gather(*\*aws*, *return\_exceptions=False*)
:   Run [awaitable objects](#asyncio-awaitables) in the *aws*
    sequence *concurrently*.

    If any awaitable in *aws* is a coroutine, it is automatically
    scheduled as a Task.

    If all awaitables are completed successfully, the result is an
    aggregate list of returned values. The order of result values
    corresponds to the order of awaitables in *aws*.

    If *return\_exceptions* is `False` (default), the first
    raised exception is immediately propagated to the task that
    awaits on `gather()`. Other awaitables in the *aws* sequence
    **won’t be cancelled** and will continue to run.

    If *return\_exceptions* is `True`, exceptions are treated the
    same as successful results, and aggregated in the result list.

    If `gather()` is *cancelled*, all submitted awaitables
    (that have not completed yet) are also *cancelled*.

    If any Task or Future from the *aws* sequence is *cancelled*, it is
    treated as if it raised [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") – the `gather()`
    call is **not** cancelled in this case. This is to prevent the
    cancellation of one submitted Task/Future to cause other
    Tasks/Futures to be cancelled.

    Note

    A new alternative to create and run tasks concurrently and
    wait for their completion is [`asyncio.TaskGroup`](#asyncio.TaskGroup "asyncio.TaskGroup"). *TaskGroup*
    provides stronger safety guarantees than *gather* for scheduling a nesting of subtasks:
    if a task (or a subtask, a task scheduled by a task)
    raises an exception, *TaskGroup* will, while *gather* will not,
    cancel the remaining scheduled tasks.

    Example:

    ```
    importasyncio

    async deffactorial(name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({number}), currently i={i}...")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")
        return f

    async defmain():
        # Schedule three calls *concurrently*:
        L = await asyncio.gather(
            factorial("A", 2),
            factorial("B", 3),
            factorial("C", 4),
        )
        print(L)

    asyncio.run(main())

    # Expected output:
    #
    #     Task A: Compute factorial(2), currently i=2...
    #     Task B: Compute factorial(3), currently i=2...
    #     Task C: Compute factorial(4), currently i=2...
    #     Task A: factorial(2) = 2
    #     Task B: Compute factorial(3), currently i=3...
    #     Task C: Compute factorial(4), currently i=3...
    #     Task B: factorial(3) = 6
    #     Task C: Compute factorial(4), currently i=4...
    #     Task C: factorial(4) = 24
    #     [2, 6, 24]
    ```

    Note

    If *return\_exceptions* is false, cancelling gather() after it
    has been marked done won’t cancel any submitted awaitables.
    For instance, gather can be marked done after propagating an
    exception to the caller, therefore, calling `gather.cancel()`
    after catching an exception (raised by one of the awaitables) from
    gather won’t cancel any other awaitables.

    Changed in version 3.7: If the *gather* itself is cancelled, the cancellation is
    propagated regardless of *return\_exceptions*.

    Changed in version 3.10: Removed the *loop* parameter.

    Deprecated since version 3.10: Deprecation warning is emitted if no positional arguments are provided
    or not all positional arguments are Future-like objects
    and there is no running event loop.

## 

asyncio.eager\_task\_factory(*loop*, *coro*, *\**, *name=None*, *context=None*)
:   A task factory for eager task execution.

    When using this factory (via [`loop.set_task_factory(asyncio.eager_task_factory)`](asyncio-eventloop.html#asyncio.loop.set_task_factory "asyncio.loop.set_task_factory")),
    coroutines begin execution synchronously during [`Task`](#asyncio.Task "asyncio.Task") construction.
    Tasks are only scheduled on the event loop if they block.
    This can be a performance improvement as the overhead of loop scheduling
    is avoided for coroutines that complete synchronously.

    A common example where this is beneficial is coroutines which employ
    caching or memoization to avoid actual I/O when possible.

    Note

    Immediate execution of the coroutine is a semantic change.
    If the coroutine returns or raises, the task is never scheduled
    to the event loop. If the coroutine execution blocks, the task is
    scheduled to the event loop. This change may introduce behavior
    changes to existing applications. For example,
    the application’s task execution order is likely to change.

    Added in version 3.12.

asyncio.create\_eager\_task\_factory(*custom\_task\_constructor*)
:   Create an eager task factory, similar to [`eager_task_factory()`](#asyncio.eager_task_factory "asyncio.eager_task_factory"),
    using the provided *custom\_task\_constructor* when creating a new task instead
    of the default [`Task`](#asyncio.Task "asyncio.Task").

    *custom\_task\_constructor* must be a *callable* with the signature matching
    the signature of [`Task.__init__`](#asyncio.Task "asyncio.Task").
    The callable must return a [`asyncio.Task`](#asyncio.Task "asyncio.Task")-compatible object.

    This function returns a *callable* intended to be used as a task factory of an
    event loop via [`loop.set_task_factory(factory)`](asyncio-eventloop.html#asyncio.loop.set_task_factory "asyncio.loop.set_task_factory")).

    Added in version 3.12.

## 

*awaitable* asyncio.shield(*aw*)
:   Protect an [awaitable object](#asyncio-awaitables)
    from being [`cancelled`](#asyncio.Task.cancel "asyncio.Task.cancel").

    If *aw* is a coroutine it is automatically scheduled as a Task.

    The statement:

    ```
    task = asyncio.create_task(something())
    res = await shield(task)
    ```

    is equivalent to:

    ```
    res = await something()
    ```

    *except* that if the coroutine containing it is cancelled, the
    Task running in `something()` is not cancelled. From the point
    of view of `something()`, the cancellation did not happen.
    Although its caller is still cancelled, so the “await” expression
    still raises a [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError").

    If `something()` is cancelled by other means (i.e. from within
    itself) that would also cancel `shield()`.

    If it is desired to completely ignore cancellation (not recommended)
    the `shield()` function should be combined with a try/except
    clause, as follows:

    ```
    task = asyncio.create_task(something())
    try:
        res = await shield(task)
    except CancelledError:
        res = None
    ```

    Important

    Save a reference to tasks passed to this function, to avoid
    a task disappearing mid-execution. The event loop only keeps
    weak references to tasks. A task that isn’t referenced elsewhere
    may get garbage collected at any time, even before it’s done.

    Changed in version 3.10: Removed the *loop* parameter.

    Deprecated since version 3.10: Deprecation warning is emitted if *aw* is not Future-like object
    and there is no running event loop.

## 

asyncio.timeout(*delay*)
:   Return an [asynchronous context manager](../reference/datamodel.html#async-context-managers)
    that can be used to limit the amount of time spent waiting on
    something.

    *delay* can either be `None`, or a float/int number of
    seconds to wait. If *delay* is `None`, no time limit will
    be applied; this can be useful if the delay is unknown when
    the context manager is created.

    In either case, the context manager can be rescheduled after
    creation using [`Timeout.reschedule()`](#asyncio.Timeout.reschedule "asyncio.Timeout.reschedule").

    Example:

    ```
    async defmain():
        async with asyncio.timeout(10):
            await long_running_task()
    ```

    If `long_running_task` takes more than 10 seconds to complete,
    the context manager will cancel the current task and handle
    the resulting [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") internally, transforming it
    into a [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") which can be caught and handled.

    Note

    The [`asyncio.timeout()`](#asyncio.timeout "asyncio.timeout") context manager is what transforms
    the [`asyncio.CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") into a [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError"),
    which means the `TimeoutError` can only be caught
    *outside* of the context manager.

    Example of catching [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError"):

    ```
    async defmain():
        try:
            async with asyncio.timeout(10):
                await long_running_task()
        except TimeoutError:
            print("The long operation timed out, but we've handled it.")

        print("This statement will run regardless.")
    ```

    The context manager produced by [`asyncio.timeout()`](#asyncio.timeout "asyncio.timeout") can be
    rescheduled to a different deadline and inspected.

    *class*asyncio.Timeout(*when*)
    :   An [asynchronous context manager](../reference/datamodel.html#async-context-managers)
        for cancelling overdue coroutines.

        Prefer using [`asyncio.timeout()`](#asyncio.timeout "asyncio.timeout") or [`asyncio.timeout_at()`](#asyncio.timeout_at "asyncio.timeout_at")
        rather than instantiating `Timeout` directly.

        `when` should be an absolute time at which the context should time out,
        as measured by the event loop’s clock:

        * If `when` is `None`, the timeout will never trigger.
        * If `when < loop.time()`, the timeout will trigger on the next
          iteration of the event loop.

        > when() → [float](functions.html#float "float")|[None](constants.html#None "None")
        > :   Return the current deadline, or `None` if the current
        >     deadline is not set.
        >
        > reschedule(*when:[float](functions.html#float "float")|[None](constants.html#None "None")*)
        > :   Reschedule the timeout.
        >
        > expired() → [bool](functions.html#bool "bool")
        > :   Return whether the context manager has exceeded its deadline
        >     (expired).

    Example:

    ```
    async defmain():
        try:
            # We do not know the timeout when starting, so we pass ``None``.
            async with asyncio.timeout(None) as cm:
                # We know the timeout now, so we reschedule it.
                new_deadline = get_running_loop().time() + 10
                cm.reschedule(new_deadline)

                await long_running_task()
        except TimeoutError:
            pass

        if cm.expired():
            print("Looks like we haven't finished on time.")
    ```

    Timeout context managers can be safely nested.

    Added in version 3.11.

asyncio.timeout\_at(*when*)
:   Similar to [`asyncio.timeout()`](#asyncio.timeout "asyncio.timeout"), except *when* is the absolute time
    to stop waiting, or `None`.

    Example:

    ```
    async defmain():
        loop = get_running_loop()
        deadline = loop.time() + 20
        try:
            async with asyncio.timeout_at(deadline):
                await long_running_task()
        except TimeoutError:
            print("The long operation timed out, but we've handled it.")

        print("This statement will run regardless.")
    ```

    Added in version 3.11.

*async*asyncio.wait\_for(*aw*, *timeout*)
:   Wait for the *aw* [awaitable](#asyncio-awaitables)
    to complete with a timeout.

    If *aw* is a coroutine it is automatically scheduled as a Task.

    *timeout* can either be `None` or a float or int number of seconds
    to wait for. If *timeout* is `None`, block until the future
    completes.

    If a timeout occurs, it cancels the task and raises
    [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError").

    To avoid the task [`cancellation`](#asyncio.Task.cancel "asyncio.Task.cancel"),
    wrap it in [`shield()`](#asyncio.shield "asyncio.shield").

    The function will wait until the future is actually cancelled,
    so the total wait time may exceed the *timeout*. If an exception
    happens during cancellation, it is propagated.

    If the wait is cancelled, the future *aw* is also cancelled.

    Example:

    ```
    async defeternity():
        # Sleep for one hour
        await asyncio.sleep(3600)
        print('yay!')

    async defmain():
        # Wait for at most 1 second
        try:
            await asyncio.wait_for(eternity(), timeout=1.0)
        except TimeoutError:
            print('timeout!')

    asyncio.run(main())

    # Expected output:
    #
    #     timeout!
    ```

    Changed in version 3.7: When *aw* is cancelled due to a timeout, `wait_for` waits
    for *aw* to be cancelled. Previously, it raised
    [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") immediately.

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Raises [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") instead of [`asyncio.TimeoutError`](asyncio-exceptions.html#asyncio.TimeoutError "asyncio.TimeoutError").

## 

*async*asyncio.wait(*aws*, *\**, *timeout=None*, *return\_when=ALL\_COMPLETED*)
:   Run [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future") and [`Task`](#asyncio.Task "asyncio.Task") instances in the *aws*
    iterable concurrently and block until the condition specified
    by *return\_when*.

    The *aws* iterable must not be empty.

    Returns two sets of Tasks/Futures: `(done, pending)`.

    Usage:

    ```
    done, pending = await asyncio.wait(aws)
    ```

    *timeout* (a float or int), if specified, can be used to control
    the maximum number of seconds to wait before returning.

    Note that this function does not raise [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError").
    Futures or Tasks that aren’t done when the timeout occurs are simply
    returned in the second set.

    *return\_when* indicates when this function should return. It must
    be one of the following constants:

    | Constant | Description |
    | --- | --- |
    | asyncio.FIRST\_COMPLETED | The function will return when any future finishes or is cancelled. |
    | asyncio.FIRST\_EXCEPTION | The function will return when any future finishes by raising an exception. If no future raises an exception then it is equivalent to [`ALL_COMPLETED`](#asyncio.ALL_COMPLETED "asyncio.ALL_COMPLETED"). |
    | asyncio.ALL\_COMPLETED | The function will return when all futures finish or are cancelled. |

    Unlike [`wait_for()`](#asyncio.wait_for "asyncio.wait_for"), `wait()` does not cancel the
    futures when a timeout occurs.

    Changed in version 3.10: Removed the *loop* parameter.

    Changed in version 3.11: Passing coroutine objects to `wait()` directly is forbidden.

    Changed in version 3.12: Added support for generators yielding tasks.

asyncio.as\_completed(*aws*, *\**, *timeout=None*)
:   Run [awaitable objects](#asyncio-awaitables) in the *aws* iterable
    concurrently. The returned object can be iterated to obtain the results
    of the awaitables as they finish.

    The object returned by `as_completed()` can be iterated as an
    [asynchronous iterator](../glossary.html#term-asynchronous-iterator) or a plain [iterator](../glossary.html#term-iterator). When asynchronous
    iteration is used, the originally-supplied awaitables are yielded if they
    are tasks or futures. This makes it easy to correlate previously-scheduled
    tasks with their results. Example:

    ```
    ipv4_connect = create_task(open_connection("127.0.0.1", 80))
    ipv6_connect = create_task(open_connection("::1", 80))
    tasks = [ipv4_connect, ipv6_connect]

    async for earliest_connect in as_completed(tasks):
        # earliest_connect is done. The result can be obtained by
        # awaiting it or calling earliest_connect.result()
        reader, writer = await earliest_connect

        if earliest_connect is ipv6_connect:
            print("IPv6 connection established.")
        else:
            print("IPv4 connection established.")
    ```

    During asynchronous iteration, implicitly-created tasks will be yielded for
    supplied awaitables that aren’t tasks or futures.

    When used as a plain iterator, each iteration yields a new coroutine that
    returns the result or raises the exception of the next completed awaitable.
    This pattern is compatible with Python versions older than 3.13:

    ```
    ipv4_connect = create_task(open_connection("127.0.0.1", 80))
    ipv6_connect = create_task(open_connection("::1", 80))
    tasks = [ipv4_connect, ipv6_connect]

    for next_connect in as_completed(tasks):
        # next_connect is not one of the original task objects. It must be
        # awaited to obtain the result value or raise the exception of the
        # awaitable that finishes next.
        reader, writer = await next_connect
    ```

    A [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") is raised if the timeout occurs before all awaitables
    are done. This is raised by the `async for` loop during asynchronous
    iteration or by the coroutines yielded during plain iteration.

    Changed in version 3.10: Removed the *loop* parameter.

    Deprecated since version 3.10: Deprecation warning is emitted if not all awaitable objects in the *aws*
    iterable are Future-like objects and there is no running event loop.

    Changed in version 3.12: Added support for generators yielding tasks.

    Changed in version 3.13: The result can now be used as either an [asynchronous iterator](../glossary.html#term-asynchronous-iterator)
    or as a plain [iterator](../glossary.html#term-iterator) (previously it was only a plain iterator).

## 

*async*asyncio.to\_thread(*func*, */*, *\*args*, *\*\*kwargs*)
:   Asynchronously run function *func* in a separate thread.

    Any \*args and \*\*kwargs supplied for this function are directly passed
    to *func*. Also, the current [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") is propagated,
    allowing context variables from the event loop thread to be accessed in the
    separate thread.

    Return a coroutine that can be awaited to get the eventual result of *func*.

    This coroutine function is primarily intended to be used for executing
    IO-bound functions/methods that would otherwise block the event loop if
    they were run in the main thread. For example:

    ```
    defblocking_io():
        print(f"start blocking_io at {time.strftime('%X')}")
        # Note that time.sleep() can be replaced with any blocking
        # IO-bound operation, such as file operations.
        time.sleep(1)
        print(f"blocking_io complete at {time.strftime('%X')}")

    async defmain():
        print(f"started main at {time.strftime('%X')}")

        await asyncio.gather(
            asyncio.to_thread(blocking_io),
            asyncio.sleep(1))

        print(f"finished main at {time.strftime('%X')}")

    asyncio.run(main())

    # Expected output:
    #
    # started main at 19:50:53
    # start blocking_io at 19:50:53
    # blocking_io complete at 19:50:54
    # finished main at 19:50:54
    ```

    Directly calling `blocking_io()` in any coroutine would block the event loop
    for its duration, resulting in an additional 1 second of run time. Instead,
    by using `asyncio.to_thread()`, we can run it in a separate thread without
    blocking the event loop.

    Note

    Due to the [GIL](../glossary.html#term-GIL), `asyncio.to_thread()` can typically only be used
    to make IO-bound functions non-blocking. However, for extension modules
    that release the GIL or alternative Python implementations that don’t
    have one, `asyncio.to_thread()` can also be used for CPU-bound functions.

    Added in version 3.9.

## 

asyncio.run\_coroutine\_threadsafe(*coro*, *loop*)
:   Submit a coroutine to the given event loop. Thread-safe.

    Return a [`concurrent.futures.Future`](concurrent.futures.html#concurrent.futures.Future "concurrent.futures.Future") to wait for the result
    from another OS thread.

    This function is meant to be called from a different OS thread
    than the one where the event loop is running. Example:

    ```
    defin_thread(loop: asyncio.AbstractEventLoop) -> None:
        # Run some blocking IO
        pathlib.Path("example.txt").write_text("hello world", encoding="utf8")

        # Create a coroutine
        coro = asyncio.sleep(1, result=3)

        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)

        # Wait for the result with an optional timeout argument
        assert future.result(timeout=2) == 3

    async defamain() -> None:
        # Get the running loop
        loop = asyncio.get_running_loop()

        # Run something in a thread
        await asyncio.to_thread(in_thread, loop)
    ```

    It’s also possible to run the other way around. Example:

    ```
    @contextlib.contextmanager
    defloop_in_thread() -> Generator[asyncio.AbstractEventLoop]:
        loop_fut = concurrent.futures.Future[asyncio.AbstractEventLoop]()
        stop_event = asyncio.Event()

        async defmain() -> None:
            loop_fut.set_result(asyncio.get_running_loop())
            await stop_event.wait()

        with concurrent.futures.ThreadPoolExecutor(1) as tpe:
            complete_fut = tpe.submit(asyncio.run, main())
            for fut in concurrent.futures.as_completed((loop_fut, complete_fut)):
                if fut is loop_fut:
                    loop = loop_fut.result()
                    try:
                        yield loop
                    finally:
                        loop.call_soon_threadsafe(stop_event.set)
                else:
                    fut.result()

    # Create a loop in another thread
    with loop_in_thread() as loop:
        # Create a coroutine
        coro = asyncio.sleep(1, result=3)

        # Submit the coroutine to a given loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)

        # Wait for the result with an optional timeout argument
        assert future.result(timeout=2) == 3
    ```

    If an exception is raised in the coroutine, the returned Future
    will be notified. It can also be used to cancel the task in
    the event loop:

    ```
    try:
        result = future.result(timeout)
    except TimeoutError:
        print('The coroutine took too long, cancelling the task...')
        future.cancel()
    except Exception as exc:
        print(f'The coroutine raised an exception: {exc!r}')
    else:
        print(f'The coroutine returned: {result!r}')
    ```

    See the [concurrency and multithreading](asyncio-dev.html#asyncio-multithreading)
    section of the documentation.

    Unlike other asyncio functions this function requires the *loop*
    argument to be passed explicitly.

    Added in version 3.5.1.

## 

asyncio.current\_task(*loop=None*)
:   Return the currently running [`Task`](#asyncio.Task "asyncio.Task") instance, or `None` if
    no task is running.

    If *loop* is `None` [`get_running_loop()`](asyncio-eventloop.html#asyncio.get_running_loop "asyncio.get_running_loop") is used to get
    the current loop.

    Added in version 3.7.

asyncio.all\_tasks(*loop=None*)
:   Return a set of not yet finished [`Task`](#asyncio.Task "asyncio.Task") objects run by
    the loop.

    If *loop* is `None`, [`get_running_loop()`](asyncio-eventloop.html#asyncio.get_running_loop "asyncio.get_running_loop") is used for getting
    current loop.

    Added in version 3.7.

asyncio.iscoroutine(*obj*)
:   Return `True` if *obj* is a coroutine object.

    Added in version 3.4.

## 

*class*asyncio.Task(*coro*, *\**, *loop=None*, *name=None*, *context=None*, *eager\_start=False*)
:   A [`Future-like`](asyncio-future.html#asyncio.Future "asyncio.Future") object that runs a Python
    [coroutine](#coroutine). Not thread-safe.

    Tasks are used to run coroutines in event loops.
    If a coroutine awaits on a Future, the Task suspends
    the execution of the coroutine and waits for the completion
    of the Future. When the Future is *done*, the execution of
    the wrapped coroutine resumes.

    Event loops use cooperative scheduling: an event loop runs
    one Task at a time. While a Task awaits for the completion of a
    Future, the event loop runs other Tasks, callbacks, or performs
    IO operations.

    Use the high-level [`asyncio.create_task()`](#asyncio.create_task "asyncio.create_task") function to create
    Tasks, or the low-level [`loop.create_task()`](asyncio-eventloop.html#asyncio.loop.create_task "asyncio.loop.create_task") or
    [`ensure_future()`](asyncio-future.html#asyncio.ensure_future "asyncio.ensure_future") functions. Manual instantiation of Tasks
    is discouraged.

    To cancel a running Task use the [`cancel()`](#asyncio.Task.cancel "asyncio.Task.cancel") method. Calling it
    will cause the Task to throw a [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") exception into
    the wrapped coroutine. If a coroutine is awaiting on a Future
    object during cancellation, the Future object will be cancelled.

    [`cancelled()`](#asyncio.Task.cancelled "asyncio.Task.cancelled") can be used to check if the Task was cancelled.
    The method returns `True` if the wrapped coroutine did not
    suppress the [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") exception and was actually
    cancelled.

    [`asyncio.Task`](#asyncio.Task "asyncio.Task") inherits from [`Future`](asyncio-future.html#asyncio.Future "asyncio.Future") all of its
    APIs except [`Future.set_result()`](asyncio-future.html#asyncio.Future.set_result "asyncio.Future.set_result") and
    [`Future.set_exception()`](asyncio-future.html#asyncio.Future.set_exception "asyncio.Future.set_exception").

    An optional keyword-only *context* argument allows specifying a
    custom [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") for the *coro* to run in.
    If no *context* is provided, the Task copies the current context
    and later runs its coroutine in the copied context.

    An optional keyword-only *eager\_start* argument allows eagerly starting
    the execution of the [`asyncio.Task`](#asyncio.Task "asyncio.Task") at task creation time.
    If set to `True` and the event loop is running, the task will start
    executing the coroutine immediately, until the first time the coroutine
    blocks. If the coroutine returns or raises without blocking, the task
    will be finished eagerly and will skip scheduling to the event loop.

    Changed in version 3.7: Added support for the [`contextvars`](contextvars.html#module-contextvars "contextvars: Context Variables") module.

    Changed in version 3.8: Added the *name* parameter.

    Deprecated since version 3.10: Deprecation warning is emitted if *loop* is not specified
    and there is no running event loop.

    Changed in version 3.11: Added the *context* parameter.

    Changed in version 3.12: Added the *eager\_start* parameter.

    done()
    :   Return `True` if the Task is *done*.

        A Task is *done* when the wrapped coroutine either returned
        a value, raised an exception, or the Task was cancelled.

    result()
    :   Return the result of the Task.

        If the Task is *done*, the result of the wrapped coroutine
        is returned (or if the coroutine raised an exception, that
        exception is re-raised.)

        If the Task has been *cancelled*, this method raises
        a [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") exception.

        If the Task’s result isn’t yet available, this method raises
        an [`InvalidStateError`](asyncio-exceptions.html#asyncio.InvalidStateError "asyncio.InvalidStateError") exception.

    exception()
    :   Return the exception of the Task.

        If the wrapped coroutine raised an exception that exception
        is returned. If the wrapped coroutine returned normally
        this method returns `None`.

        If the Task has been *cancelled*, this method raises a
        [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") exception.

        If the Task isn’t *done* yet, this method raises an
        [`InvalidStateError`](asyncio-exceptions.html#asyncio.InvalidStateError "asyncio.InvalidStateError") exception.

    add\_done\_callback(*callback*, *\**, *context=None*)
    :   Add a callback to be run when the Task is *done*.

        This method should only be used in low-level callback-based code.

        See the documentation of [`Future.add_done_callback()`](asyncio-future.html#asyncio.Future.add_done_callback "asyncio.Future.add_done_callback")
        for more details.

    remove\_done\_callback(*callback*)
    :   Remove *callback* from the callbacks list.

        This method should only be used in low-level callback-based code.

        See the documentation of [`Future.remove_done_callback()`](asyncio-future.html#asyncio.Future.remove_done_callback "asyncio.Future.remove_done_callback")
        for more details.

    get\_stack(*\**, *limit=None*)
    :   Return the list of stack frames for this Task.

        If the wrapped coroutine is not done, this returns the stack
        where it is suspended. If the coroutine has completed
        successfully or was cancelled, this returns an empty list.
        If the coroutine was terminated by an exception, this returns
        the list of traceback frames.

        The frames are always ordered from oldest to newest.

        Only one stack frame is returned for a suspended coroutine.

        The optional *limit* argument sets the maximum number of frames
        to return; by default all available frames are returned.
        The ordering of the returned list differs depending on whether
        a stack or a traceback is returned: the newest frames of a
        stack are returned, but the oldest frames of a traceback are
        returned. (This matches the behavior of the traceback module.)

    print\_stack(*\**, *limit=None*, *file=None*)
    :   Print the stack or traceback for this Task.

        This produces output similar to that of the traceback module
        for the frames retrieved by [`get_stack()`](#asyncio.Task.get_stack "asyncio.Task.get_stack").

        The *limit* argument is passed to [`get_stack()`](#asyncio.Task.get_stack "asyncio.Task.get_stack") directly.

        The *file* argument is an I/O stream to which the output
        is written; by default output is written to [`sys.stdout`](sys.html#sys.stdout "sys.stdout").

    get\_coro()
    :   Return the coroutine object wrapped by the `Task`.

        Note

        This will return `None` for Tasks which have already
        completed eagerly. See the [Eager Task Factory](#eager-task-factory).

        Added in version 3.8.

        Changed in version 3.12: Newly added eager task execution means result may be `None`.

    get\_context()
    :   Return the [`contextvars.Context`](contextvars.html#contextvars.Context "contextvars.Context") object
        associated with the task.

        Added in version 3.12.

    get\_name()
    :   Return the name of the Task.

        If no name has been explicitly assigned to the Task, the default
        asyncio Task implementation generates a default name during
        instantiation.

        Added in version 3.8.

    set\_name(*value*)
    :   Set the name of the Task.

        The *value* argument can be any object, which is then
        converted to a string.

        In the default Task implementation, the name will be visible
        in the [`repr()`](functions.html#repr "repr") output of a task object.

        Added in version 3.8.

    cancel(*msg=None*)
    :   Request the Task to be cancelled.

        If the Task is already *done* or *cancelled*, return `False`,
        otherwise, return `True`.

        The method arranges for a [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") exception to be thrown
        into the wrapped coroutine on the next cycle of the event loop.

        The coroutine then has a chance to clean up or even deny the
        request by suppressing the exception with a [`try`](../reference/compound_stmts.html#try) …
        … `except CancelledError` … [`finally`](../reference/compound_stmts.html#finally) block.
        Therefore, unlike [`Future.cancel()`](asyncio-future.html#asyncio.Future.cancel "asyncio.Future.cancel"), `Task.cancel()` does
        not guarantee that the Task will be cancelled, although
        suppressing cancellation completely is not common and is actively
        discouraged. Should the coroutine nevertheless decide to suppress
        the cancellation, it needs to call [`Task.uncancel()`](#asyncio.Task.uncancel "asyncio.Task.uncancel") in addition
        to catching the exception.

        Changed in version 3.9: Added the *msg* parameter.

        Changed in version 3.11: The `msg` parameter is propagated from cancelled task to its awaiter.

        The following example illustrates how coroutines can intercept
        the cancellation request:

        ```
        async defcancel_me():
            print('cancel_me(): before sleep')

            try:
                # Wait for 1 hour
                await asyncio.sleep(3600)
            except asyncio.CancelledError:
                print('cancel_me(): cancel sleep')
                raise
            finally:
                print('cancel_me(): after sleep')

        async defmain():
            # Create a "cancel_me" Task
            task = asyncio.create_task(cancel_me())

            # Wait for 1 second
            await asyncio.sleep(1)

            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print("main(): cancel_me is cancelled now")

        asyncio.run(main())

        # Expected output:
        #
        #     cancel_me(): before sleep
        #     cancel_me(): cancel sleep
        #     cancel_me(): after sleep
        #     main(): cancel_me is cancelled now
        ```

    cancelled()
    :   Return `True` if the Task is *cancelled*.

        The Task is *cancelled* when the cancellation was requested with
        [`cancel()`](#asyncio.Task.cancel "asyncio.Task.cancel") and the wrapped coroutine propagated the
        [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") exception thrown into it.

    uncancel()
    :   Decrement the count of cancellation requests to this Task.

        Returns the remaining number of cancellation requests.

        Note that once execution of a cancelled task completed, further
        calls to `uncancel()` are ineffective.

        Added in version 3.11.

        This method is used by asyncio’s internals and isn’t expected to be
        used by end-user code. In particular, if a Task gets successfully
        uncancelled, this allows for elements of structured concurrency like
        [Task groups](#taskgroups) and [`asyncio.timeout()`](#asyncio.timeout "asyncio.timeout") to continue running,
        isolating cancellation to the respective structured block.
        For example:

        ```
        async defmake_request_with_timeout():
            try:
                async with asyncio.timeout(1):
                    # Structured block affected by the timeout:
                    await make_request()
                    await make_another_request()
            except TimeoutError:
                log("There was a timeout")
            # Outer code not affected by the timeout:
            await unrelated_code()
        ```

        While the block with `make_request()` and `make_another_request()`
        might get cancelled due to the timeout, `unrelated_code()` should
        continue running even in case of the timeout. This is implemented
        with `uncancel()`. [`TaskGroup`](#asyncio.TaskGroup "asyncio.TaskGroup") context managers use
        [`uncancel()`](#asyncio.Task.uncancel "asyncio.Task.uncancel") in a similar fashion.

        If end-user code is, for some reason, suppressing cancellation by
        catching [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError"), it needs to call this method to remove
        the cancellation state.

        When this method decrements the cancellation count to zero,
        the method checks if a previous [`cancel()`](#asyncio.Task.cancel "asyncio.Task.cancel") call had arranged
        for [`CancelledError`](asyncio-exceptions.html#asyncio.CancelledError "asyncio.CancelledError") to be thrown into the task.
        If it hasn’t been thrown yet, that arrangement will be
        rescinded (by resetting the internal `_must_cancel` flag).

    Changed in version 3.13: Changed to rescind pending cancellation requests upon reaching zero.

    cancelling()
    :   Return the number of pending cancellation requests to this Task, i.e.,
        the number of calls to [`cancel()`](#asyncio.Task.cancel "asyncio.Task.cancel") less the number of
        [`uncancel()`](#asyncio.Task.uncancel "asyncio.Task.uncancel") calls.

        Note that if this number is greater than zero but the Task is
        still executing, [`cancelled()`](#asyncio.Task.cancelled "asyncio.Task.cancelled") will still return `False`.
        This is because this number can be lowered by calling [`uncancel()`](#asyncio.Task.uncancel "asyncio.Task.uncancel"),
        which can lead to the task not being cancelled after all if the
        cancellation requests go down to zero.

        This method is used by asyncio’s internals and isn’t expected to be
        used by end-user code. See [`uncancel()`](#asyncio.Task.uncancel "asyncio.Task.uncancel") for more details.

        Added in version 3.11.

---

## Bibliography

1. [Streams](https://docs.python.org/3/library/asyncio-stream.html)
2. [Subprocesses](https://docs.python.org/3/library/asyncio-subprocess.html)
3. [Event loop](https://docs.python.org/3/library/asyncio-eventloop.html)
4. [Coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html)