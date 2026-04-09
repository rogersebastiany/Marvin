concurrent.futures — Launching parallel tasks — Python 3.12.13 documentation

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

* [`concurrent.futures` — Launching parallel tasks](#)
  + [Executor Objects](#executor-objects)
  + [ThreadPoolExecutor](#threadpoolexecutor)
    - [ThreadPoolExecutor Example](#threadpoolexecutor-example)
  + [ProcessPoolExecutor](#processpoolexecutor)
    - [ProcessPoolExecutor Example](#processpoolexecutor-example)
  + [Future Objects](#future-objects)
  + [Module Functions](#module-functions)
  + [Exception classes](#exception-classes)

#### Previous topic

[The `concurrent` package](concurrent.html "previous chapter")

#### Next topic

[`subprocess` — Subprocess management](subprocess.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/concurrent.futures.rst)

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](subprocess.html "subprocess — Subprocess management") |
* [previous](concurrent.html "The concurrent package") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Concurrent Execution](concurrency.html) »
* `concurrent.futures` — Launching parallel tasks
* |
* Theme
  Auto
  Light
  Dark
   |

# `concurrent.futures` — Launching parallel tasks[¶](#module-concurrent.futures "Link to this heading")

Added in version 3.2.

**Source code:** [Lib/concurrent/futures/thread.py](https://github.com/python/cpython/tree/3.12/Lib/concurrent/futures/thread.py)
and [Lib/concurrent/futures/process.py](https://github.com/python/cpython/tree/3.12/Lib/concurrent/futures/process.py)

---

The [`concurrent.futures`](#module-concurrent.futures "concurrent.futures: Execute computations concurrently using threads or processes.") module provides a high-level interface for
asynchronously executing callables.

The asynchronous execution can be performed with threads, using
[`ThreadPoolExecutor`](#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor"), or separate processes, using
[`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor"). Both implement the same interface, which is
defined by the abstract [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") class.

[Availability](intro.html#availability): not Emscripten, not WASI.

This module does not work or is not available on WebAssembly platforms
`wasm32-emscripten` and `wasm32-wasi`. See
[WebAssembly platforms](intro.html#wasm-availability) for more information.

## Executor Objects[¶](#executor-objects "Link to this heading")

*class* concurrent.futures.Executor[¶](#concurrent.futures.Executor "Link to this definition")
:   An abstract class that provides methods to execute calls asynchronously. It
    should not be used directly, but through its concrete subclasses.

    submit(*fn*, */*, *\*args*, *\*\*kwargs*)[¶](#concurrent.futures.Executor.submit "Link to this definition")
    :   Schedules the callable, *fn*, to be executed as `fn(*args, **kwargs)`
        and returns a [`Future`](#concurrent.futures.Future "concurrent.futures.Future") object representing the execution of the
        callable.

        ```
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(pow, 323, 1235)
            print(future.result())
        ```

    map(*fn*, *\*iterables*, *timeout=None*, *chunksize=1*)[¶](#concurrent.futures.Executor.map "Link to this definition")
    :   Similar to [`map(fn, *iterables)`](functions.html#map "map") except:

        * the *iterables* are collected immediately rather than lazily;
        * *fn* is executed asynchronously and several calls to
          *fn* may be made concurrently.

        The returned iterator raises a [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError")
        if [`__next__()`](stdtypes.html#iterator.__next__ "iterator.__next__") is called and the result isn’t available
        after *timeout* seconds from the original call to [`Executor.map()`](#concurrent.futures.Executor.map "concurrent.futures.Executor.map").
        *timeout* can be an int or a float. If *timeout* is not specified or
        `None`, there is no limit to the wait time.

        If a *fn* call raises an exception, then that exception will be
        raised when its value is retrieved from the iterator.

        When using [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor"), this method chops *iterables*
        into a number of chunks which it submits to the pool as separate
        tasks. The (approximate) size of these chunks can be specified by
        setting *chunksize* to a positive integer. For very long iterables,
        using a large value for *chunksize* can significantly improve
        performance compared to the default size of 1. With
        [`ThreadPoolExecutor`](#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor"), *chunksize* has no effect.

        Changed in version 3.5: Added the *chunksize* argument.

    shutdown(*wait=True*, *\**, *cancel\_futures=False*)[¶](#concurrent.futures.Executor.shutdown "Link to this definition")
    :   Signal the executor that it should free any resources that it is using
        when the currently pending futures are done executing. Calls to
        [`Executor.submit()`](#concurrent.futures.Executor.submit "concurrent.futures.Executor.submit") and [`Executor.map()`](#concurrent.futures.Executor.map "concurrent.futures.Executor.map") made after shutdown will
        raise [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError").

        If *wait* is `True` then this method will not return until all the
        pending futures are done executing and the resources associated with the
        executor have been freed. If *wait* is `False` then this method will
        return immediately and the resources associated with the executor will be
        freed when all pending futures are done executing. Regardless of the
        value of *wait*, the entire Python program will not exit until all
        pending futures are done executing.

        If *cancel\_futures* is `True`, this method will cancel all pending
        futures that the executor has not started running. Any futures that
        are completed or running won’t be cancelled, regardless of the value
        of *cancel\_futures*.

        If both *cancel\_futures* and *wait* are `True`, all futures that the
        executor has started running will be completed prior to this method
        returning. The remaining futures are cancelled.

        You can avoid having to call this method explicitly if you use the
        [`with`](../reference/compound_stmts.html#with) statement, which will shutdown the [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor")
        (waiting as if [`Executor.shutdown()`](#concurrent.futures.Executor.shutdown "concurrent.futures.Executor.shutdown") were called with *wait* set to
        `True`):

        ```
        import shutil
        with ThreadPoolExecutor(max_workers=4) as e:
            e.submit(shutil.copy, 'src1.txt', 'dest1.txt')
            e.submit(shutil.copy, 'src2.txt', 'dest2.txt')
            e.submit(shutil.copy, 'src3.txt', 'dest3.txt')
            e.submit(shutil.copy, 'src4.txt', 'dest4.txt')
        ```

        Changed in version 3.9: Added *cancel\_futures*.

## ThreadPoolExecutor[¶](#threadpoolexecutor "Link to this heading")

[`ThreadPoolExecutor`](#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor") is an [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") subclass that uses a pool of
threads to execute calls asynchronously.

Deadlocks can occur when the callable associated with a [`Future`](#concurrent.futures.Future "concurrent.futures.Future") waits on
the results of another [`Future`](#concurrent.futures.Future "concurrent.futures.Future"). For example:

```
import time
def wait_on_b():
    time.sleep(5)
    print(b.result())  # b will never complete because it is waiting on a.
    return 5

def wait_on_a():
    time.sleep(5)
    print(a.result())  # a will never complete because it is waiting on b.
    return 6

executor = ThreadPoolExecutor(max_workers=2)
a = executor.submit(wait_on_b)
b = executor.submit(wait_on_a)
```

And:

```
def wait_on_future():
    f = executor.submit(pow, 5, 2)
    # This will never complete because there is only one worker thread and
    # it is executing this function.
    print(f.result())

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(wait_on_future)
```

*class* concurrent.futures.ThreadPoolExecutor(*max\_workers=None*, *thread\_name\_prefix=''*, *initializer=None*, *initargs=()*)[¶](#concurrent.futures.ThreadPoolExecutor "Link to this definition")
:   An [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") subclass that uses a pool of at most *max\_workers*
    threads to execute calls asynchronously.

    All threads enqueued to `ThreadPoolExecutor` will be joined before the
    interpreter can exit. Note that the exit handler which does this is
    executed *before* any exit handlers added using `atexit`. This means
    exceptions in the main thread must be caught and handled in order to
    signal threads to exit gracefully. For this reason, it is recommended
    that `ThreadPoolExecutor` not be used for long-running tasks.

    *initializer* is an optional callable that is called at the start of
    each worker thread; *initargs* is a tuple of arguments passed to the
    initializer. Should *initializer* raise an exception, all currently
    pending jobs will raise a [`BrokenThreadPool`](#concurrent.futures.thread.BrokenThreadPool "concurrent.futures.thread.BrokenThreadPool"),
    as well as any attempt to submit more jobs to the pool.

    Changed in version 3.5: If *max\_workers* is `None` or
    not given, it will default to the number of processors on the machine,
    multiplied by `5`, assuming that [`ThreadPoolExecutor`](#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor") is often
    used to overlap I/O instead of CPU work and the number of workers
    should be higher than the number of workers
    for [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor").

    Changed in version 3.6: Added the *thread\_name\_prefix* parameter to allow users to
    control the [`threading.Thread`](threading.html#threading.Thread "threading.Thread") names for worker threads created by
    the pool for easier debugging.

    Changed in version 3.7: Added the *initializer* and *initargs* arguments.

    Changed in version 3.8: Default value of *max\_workers* is changed to `min(32, os.cpu_count() + 4)`.
    This default value preserves at least 5 workers for I/O bound tasks.
    It utilizes at most 32 CPU cores for CPU bound tasks which release the GIL.
    And it avoids using very large resources implicitly on many-core machines.

    ThreadPoolExecutor now reuses idle worker threads before starting
    *max\_workers* worker threads too.

### ThreadPoolExecutor Example[¶](#threadpoolexecutor-example "Link to this heading")

```
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://nonexistant-subdomain.python.org/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
```

## ProcessPoolExecutor[¶](#processpoolexecutor "Link to this heading")

The [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor") class is an [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") subclass that
uses a pool of processes to execute calls asynchronously.
[`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor") uses the [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") module, which
allows it to side-step the [Global Interpreter Lock](../glossary.html#term-global-interpreter-lock) but also means that
only picklable objects can be executed and returned.

The `__main__` module must be importable by worker subprocesses. This means
that [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor") will not work in the interactive interpreter.

Calling [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") or [`Future`](#concurrent.futures.Future "concurrent.futures.Future") methods from a callable submitted
to a [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor") will result in deadlock.

*class* concurrent.futures.ProcessPoolExecutor(*max\_workers=None*, *mp\_context=None*, *initializer=None*, *initargs=()*, *max\_tasks\_per\_child=None*)[¶](#concurrent.futures.ProcessPoolExecutor "Link to this definition")
:   An [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") subclass that executes calls asynchronously using a pool
    of at most *max\_workers* processes. If *max\_workers* is `None` or not
    given, it will default to the number of processors on the machine.
    If *max\_workers* is less than or equal to `0`, then a [`ValueError`](exceptions.html#ValueError "ValueError")
    will be raised.
    On Windows, *max\_workers* must be less than or equal to `61`. If it is not
    then [`ValueError`](exceptions.html#ValueError "ValueError") will be raised. If *max\_workers* is `None`, then
    the default chosen will be at most `61`, even if more processors are
    available.
    *mp\_context* can be a [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") context or `None`. It will be
    used to launch the workers. If *mp\_context* is `None` or not given, the
    default [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") context is used.
    See [Contexts and start methods](multiprocessing.html#multiprocessing-start-methods).

    *initializer* is an optional callable that is called at the start of
    each worker process; *initargs* is a tuple of arguments passed to the
    initializer. Should *initializer* raise an exception, all currently
    pending jobs will raise a [`BrokenProcessPool`](#concurrent.futures.process.BrokenProcessPool "concurrent.futures.process.BrokenProcessPool"),
    as well as any attempt to submit more jobs to the pool.

    *max\_tasks\_per\_child* is an optional argument that specifies the maximum
    number of tasks a single process can execute before it will exit and be
    replaced with a fresh worker process. By default *max\_tasks\_per\_child* is
    `None` which means worker processes will live as long as the pool. When
    a max is specified, the “spawn” multiprocessing start method will be used by
    default in absence of a *mp\_context* parameter. This feature is incompatible
    with the “fork” start method.

    Changed in version 3.3: When one of the worker processes terminates abruptly, a
    [`BrokenProcessPool`](#concurrent.futures.process.BrokenProcessPool "concurrent.futures.process.BrokenProcessPool") error is now raised.
    Previously, behaviour
    was undefined but operations on the executor or its futures would often
    freeze or deadlock.

    Changed in version 3.7: The *mp\_context* argument was added to allow users to control the
    start\_method for worker processes created by the pool.

    Added the *initializer* and *initargs* arguments.

    Note

    The default [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") start method
    (see [Contexts and start methods](multiprocessing.html#multiprocessing-start-methods)) will change away from
    *fork* in Python 3.14. Code that requires *fork* be used for their
    [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor") should explicitly specify that by
    passing a `mp_context=multiprocessing.get_context("fork")`
    parameter.

    Changed in version 3.11: The *max\_tasks\_per\_child* argument was added to allow users to
    control the lifetime of workers in the pool.

    Changed in version 3.12: On POSIX systems, if your application has multiple threads and the
    [`multiprocessing`](multiprocessing.html#module-multiprocessing "multiprocessing: Process-based parallelism.") context uses the `"fork"` start method:
    The [`os.fork()`](os.html#os.fork "os.fork") function called internally to spawn workers may raise a
    [`DeprecationWarning`](exceptions.html#DeprecationWarning "DeprecationWarning"). Pass a *mp\_context* configured to use a
    different start method. See the [`os.fork()`](os.html#os.fork "os.fork") documentation for
    further explanation.

### ProcessPoolExecutor Example[¶](#processpoolexecutor-example "Link to this heading")

```
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    main()
```

## Future Objects[¶](#future-objects "Link to this heading")

The [`Future`](#concurrent.futures.Future "concurrent.futures.Future") class encapsulates the asynchronous execution of a callable.
[`Future`](#concurrent.futures.Future "concurrent.futures.Future") instances are created by [`Executor.submit()`](#concurrent.futures.Executor.submit "concurrent.futures.Executor.submit").

*class* concurrent.futures.Future[¶](#concurrent.futures.Future "Link to this definition")
:   Encapsulates the asynchronous execution of a callable. [`Future`](#concurrent.futures.Future "concurrent.futures.Future")
    instances are created by [`Executor.submit()`](#concurrent.futures.Executor.submit "concurrent.futures.Executor.submit") and should not be created
    directly except for testing.

    cancel()[¶](#concurrent.futures.Future.cancel "Link to this definition")
    :   Attempt to cancel the call. If the call is currently being executed or
        finished running and cannot be cancelled then the method will return
        `False`, otherwise the call will be cancelled and the method will
        return `True`.

    cancelled()[¶](#concurrent.futures.Future.cancelled "Link to this definition")
    :   Return `True` if the call was successfully cancelled.

    running()[¶](#concurrent.futures.Future.running "Link to this definition")
    :   Return `True` if the call is currently being executed and cannot be
        cancelled.

    done()[¶](#concurrent.futures.Future.done "Link to this definition")
    :   Return `True` if the call was successfully cancelled or finished
        running.

    result(*timeout=None*)[¶](#concurrent.futures.Future.result "Link to this definition")
    :   Return the value returned by the call. If the call hasn’t yet completed
        then this method will wait up to *timeout* seconds. If the call hasn’t
        completed in *timeout* seconds, then a
        [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") will be raised. *timeout* can be
        an int or float. If *timeout* is not specified or `None`, there is no
        limit to the wait time.

        If the future is cancelled before completing then [`CancelledError`](#concurrent.futures.CancelledError "concurrent.futures.CancelledError")
        will be raised.

        If the call raised an exception, this method will raise the same exception.

    exception(*timeout=None*)[¶](#concurrent.futures.Future.exception "Link to this definition")
    :   Return the exception raised by the call. If the call hasn’t yet
        completed then this method will wait up to *timeout* seconds. If the
        call hasn’t completed in *timeout* seconds, then a
        [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") will be raised. *timeout* can be
        an int or float. If *timeout* is not specified or `None`, there is no
        limit to the wait time.

        If the future is cancelled before completing then [`CancelledError`](#concurrent.futures.CancelledError "concurrent.futures.CancelledError")
        will be raised.

        If the call completed without raising, `None` is returned.

    add\_done\_callback(*fn*)[¶](#concurrent.futures.Future.add_done_callback "Link to this definition")
    :   Attaches the callable *fn* to the future. *fn* will be called, with the
        future as its only argument, when the future is cancelled or finishes
        running.

        Added callables are called in the order that they were added and are
        always called in a thread belonging to the process that added them. If
        the callable raises an [`Exception`](exceptions.html#Exception "Exception") subclass, it will be logged and
        ignored. If the callable raises a [`BaseException`](exceptions.html#BaseException "BaseException") subclass, the
        behavior is undefined.

        If the future has already completed or been cancelled, *fn* will be
        called immediately.

    The following [`Future`](#concurrent.futures.Future "concurrent.futures.Future") methods are meant for use in unit tests and
    [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") implementations.

    set\_running\_or\_notify\_cancel()[¶](#concurrent.futures.Future.set_running_or_notify_cancel "Link to this definition")
    :   This method should only be called by [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") implementations
        before executing the work associated with the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") and by unit
        tests.

        If the method returns `False` then the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") was cancelled,
        i.e. [`Future.cancel()`](#concurrent.futures.Future.cancel "concurrent.futures.Future.cancel") was called and returned `True`. Any threads
        waiting on the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") completing (i.e. through
        [`as_completed()`](#concurrent.futures.as_completed "concurrent.futures.as_completed") or [`wait()`](#concurrent.futures.wait "concurrent.futures.wait")) will be woken up.

        If the method returns `True` then the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") was not cancelled
        and has been put in the running state, i.e. calls to
        [`Future.running()`](#concurrent.futures.Future.running "concurrent.futures.Future.running") will return `True`.

        This method can only be called once and cannot be called after
        [`Future.set_result()`](#concurrent.futures.Future.set_result "concurrent.futures.Future.set_result") or [`Future.set_exception()`](#concurrent.futures.Future.set_exception "concurrent.futures.Future.set_exception") have been
        called.

    set\_result(*result*)[¶](#concurrent.futures.Future.set_result "Link to this definition")
    :   Sets the result of the work associated with the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") to
        *result*.

        This method should only be used by [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") implementations and
        unit tests.

        Changed in version 3.8: This method raises
        [`concurrent.futures.InvalidStateError`](#concurrent.futures.InvalidStateError "concurrent.futures.InvalidStateError") if the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") is
        already done.

    set\_exception(*exception*)[¶](#concurrent.futures.Future.set_exception "Link to this definition")
    :   Sets the result of the work associated with the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") to the
        [`Exception`](exceptions.html#Exception "Exception") *exception*.

        This method should only be used by [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") implementations and
        unit tests.

        Changed in version 3.8: This method raises
        [`concurrent.futures.InvalidStateError`](#concurrent.futures.InvalidStateError "concurrent.futures.InvalidStateError") if the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") is
        already done.

## Module Functions[¶](#module-functions "Link to this heading")

concurrent.futures.wait(*fs*, *timeout=None*, *return\_when=ALL\_COMPLETED*)[¶](#concurrent.futures.wait "Link to this definition")
:   Wait for the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") instances (possibly created by different
    [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") instances) given by *fs* to complete. Duplicate futures
    given to *fs* are removed and will be returned only once. Returns a named
    2-tuple of sets. The first set, named `done`, contains the futures that
    completed (finished or cancelled futures) before the wait completed. The
    second set, named `not_done`, contains the futures that did not complete
    (pending or running futures).

    *timeout* can be used to control the maximum number of seconds to wait before
    returning. *timeout* can be an int or float. If *timeout* is not specified
    or `None`, there is no limit to the wait time.

    *return\_when* indicates when this function should return. It must be one of
    the following constants:

    | Constant | Description |
    | --- | --- |
    | concurrent.futures.FIRST\_COMPLETED[¶](#concurrent.futures.FIRST_COMPLETED "Link to this definition") | The function will return when any future finishes or is cancelled. |
    | concurrent.futures.FIRST\_EXCEPTION[¶](#concurrent.futures.FIRST_EXCEPTION "Link to this definition") | The function will return when any future finishes by raising an exception. If no future raises an exception then it is equivalent to [`ALL_COMPLETED`](#concurrent.futures.ALL_COMPLETED "concurrent.futures.ALL_COMPLETED"). |
    | concurrent.futures.ALL\_COMPLETED[¶](#concurrent.futures.ALL_COMPLETED "Link to this definition") | The function will return when all futures finish or are cancelled. |

concurrent.futures.as\_completed(*fs*, *timeout=None*)[¶](#concurrent.futures.as_completed "Link to this definition")
:   Returns an iterator over the [`Future`](#concurrent.futures.Future "concurrent.futures.Future") instances (possibly created by
    different [`Executor`](#concurrent.futures.Executor "concurrent.futures.Executor") instances) given by *fs* that yields futures as
    they complete (finished or cancelled futures). Any futures given by *fs* that
    are duplicated will be returned once. Any futures that completed before
    [`as_completed()`](#concurrent.futures.as_completed "concurrent.futures.as_completed") is called will be yielded first. The returned iterator
    raises a [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError") if [`__next__()`](stdtypes.html#iterator.__next__ "iterator.__next__")
    is called and the result isn’t available after *timeout* seconds from the
    original call to [`as_completed()`](#concurrent.futures.as_completed "concurrent.futures.as_completed"). *timeout* can be an int or float. If
    *timeout* is not specified or `None`, there is no limit to the wait time.

See also

[**PEP 3148**](https://peps.python.org/pep-3148/) – futures - execute computations asynchronously
:   The proposal which described this feature for inclusion in the Python
    standard library.

## Exception classes[¶](#exception-classes "Link to this heading")

*exception* concurrent.futures.CancelledError[¶](#concurrent.futures.CancelledError "Link to this definition")
:   Raised when a future is cancelled.

*exception* concurrent.futures.TimeoutError[¶](#concurrent.futures.TimeoutError "Link to this definition")
:   A deprecated alias of [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError"),
    raised when a future operation exceeds the given timeout.

    Changed in version 3.11: This class was made an alias of [`TimeoutError`](exceptions.html#TimeoutError "TimeoutError").

*exception* concurrent.futures.BrokenExecutor[¶](#concurrent.futures.BrokenExecutor "Link to this definition")
:   Derived from [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError"), this exception class is raised
    when an executor is broken for some reason, and cannot be used
    to submit or execute new tasks.

    Added in version 3.7.

*exception* concurrent.futures.InvalidStateError[¶](#concurrent.futures.InvalidStateError "Link to this definition")
:   Raised when an operation is performed on a future that is not allowed
    in the current state.

    Added in version 3.8.

*exception* concurrent.futures.thread.BrokenThreadPool[¶](#concurrent.futures.thread.BrokenThreadPool "Link to this definition")
:   Derived from [`BrokenExecutor`](#concurrent.futures.BrokenExecutor "concurrent.futures.BrokenExecutor"), this exception
    class is raised when one of the workers
    of a [`ThreadPoolExecutor`](#concurrent.futures.ThreadPoolExecutor "concurrent.futures.ThreadPoolExecutor")
    has failed initializing.

    Added in version 3.7.

*exception* concurrent.futures.process.BrokenProcessPool[¶](#concurrent.futures.process.BrokenProcessPool "Link to this definition")
:   Derived from [`BrokenExecutor`](#concurrent.futures.BrokenExecutor "concurrent.futures.BrokenExecutor") (formerly
    [`RuntimeError`](exceptions.html#RuntimeError "RuntimeError")), this exception class is raised when one of the
    workers of a [`ProcessPoolExecutor`](#concurrent.futures.ProcessPoolExecutor "concurrent.futures.ProcessPoolExecutor")
    has terminated in a non-clean
    fashion (for example, if it was killed from the outside).

    Added in version 3.3.

### [Table of Contents](../contents.html)

* [`concurrent.futures` — Launching parallel tasks](#)
  + [Executor Objects](#executor-objects)
  + [ThreadPoolExecutor](#threadpoolexecutor)
    - [ThreadPoolExecutor Example](#threadpoolexecutor-example)
  + [ProcessPoolExecutor](#processpoolexecutor)
    - [ProcessPoolExecutor Example](#processpoolexecutor-example)
  + [Future Objects](#future-objects)
  + [Module Functions](#module-functions)
  + [Exception classes](#exception-classes)

#### Previous topic

[The `concurrent` package](concurrent.html "previous chapter")

#### Next topic

[`subprocess` — Subprocess management](subprocess.html "next chapter")

### This Page

* [Report a Bug](../bugs.html)
* [Show Source](https://github.com/python/cpython/blob/main/Doc/library/concurrent.futures.rst)

«

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](subprocess.html "subprocess — Subprocess management") |
* [previous](concurrent.html "The concurrent package") |
* [Python](https://www.python.org/) »

* [3.12.13 Documentation](../index.html) »
* [The Python Standard Library](index.html) »
* [Concurrent Execution](concurrency.html) »
* `concurrent.futures` — Launching parallel tasks
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