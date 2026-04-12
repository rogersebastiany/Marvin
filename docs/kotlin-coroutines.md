# Kotlin Coroutines


---

## 1. Coroutines

Applications often need to perform multiple tasks at the same time, such as responding to user input, loading data, or updating the screen. To support this, they rely on concurrency, which allows operations to run independently without blocking each other.

The most common way to run tasks concurrently is by using threads, which are independent paths of execution managed by the operating system. However, threads are relatively heavy, and creating many of them can lead to performance issues.

To support efficient concurrency, Kotlin uses asynchronous programming built around coroutines, which let you write asynchronous code in a natural, sequential style using suspending functions. Coroutines are lightweight alternatives to threads. They can suspend without blocking system resources and are resource-friendly, making them better suited for fine-grained concurrency.

Most coroutine features are provided by the [`kotlinx.coroutines`](https://github.com/Kotlin/kotlinx.coroutines) library, which includes tools for launching coroutines, handling concurrency, working with asynchronous streams, and more.

If you're new to coroutines in Kotlin, start with the [Coroutine basics](coroutines-basics.html) guide before diving into more complex topics. This guide introduces the key concepts of suspending functions, coroutine builders, and structured concurrency through simple examples:

## Coroutine concepts

The `kotlinx.coroutines` library provides the core building blocks for running tasks concurrently, structuring coroutine execution, and managing shared state.

### Suspending functions and coroutine builders

Coroutines in Kotlin are built on suspending functions, which allow code to pause and resume without blocking a thread. The `suspend` keyword marks functions that can perform long-running operations asynchronously.

To launch new coroutines, use coroutine builders like [`.launch()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html) and [`.async()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html). These builders are extension functions on [`CoroutineScope`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/), which defines the coroutine's lifecycle and provides the coroutine context.

You can learn more about these builders in [Coroutine basics](coroutines-basics.html) and [Composing suspend functions](coroutines-and-channels.html).

### Coroutine context and behavior

Launching a coroutine from a `CoroutineScope` creates a context that governs its execution. Builder functions like `.launch()` and `.async()` automatically create a set of elements that define how the coroutine behaves:

* The [`Job`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/) interface tracks the coroutine's lifecycle and enables structured concurrency.
* [`CoroutineDispatcher`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/) controls where the coroutine runs, such as on a background thread or the main thread in UI applications.
* [`CoroutineExceptionHandler`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/) handles uncaught exceptions.

These, along with other possible elements, make up the [coroutine context](coroutine-context-and-dispatchers.html), which is inherited by default from the coroutine's parent. This context forms a hierarchy that enables structured concurrency, where related coroutines can be [canceled](cancellation-and-timeouts.html) together or [handle exceptions](exception-handling.html) as a group.

### Asynchronous flow and shared mutable state

Kotlin provides several ways for coroutines to communicate. Use one of the following options based on how you want to share values between coroutines:

* [`Flow`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/) produces values only when a coroutine actively collects them.
* [`Channel`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel/) allows multiple coroutines to send and receive values, with each value delivered to exactly one coroutine.
* [`SharedFlow`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/) continuously shares every value with all active collecting coroutines.

When multiple coroutines need to access or update the same data, they share mutable state. Without coordination, this can lead to race conditions, where operations interfere with each other in unpredictable ways. To safely manage shared mutable state, use [`StateFlow`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/#) to wrap the shared data. Then, you can update it from one coroutine and collect its latest value from others.

For more information, see [Asynchronous flow](flow.html), [Channels](channels.html), and the [Coroutines and channels tutorial](coroutines-and-channels.html).

## What's next

* Learn the fundamentals of coroutines, suspending functions, and builders in the [Coroutine basics guide](coroutines-basics.html).
* Explore how to combine suspending functions and build coroutine pipelines in [Composing suspending functions](coroutine-context-and-dispatchers.html).
* Learn how to [debug coroutines](debug-coroutines-with-idea.html) using built-in tools in IntelliJ IDEA.
* For flow-specific debugging, see the [Debug Kotlin Flow using IntelliJ IDEA](debug-flow-with-idea.html) tutorial.
* Read the [Guide to UI programming with coroutines](https://github.com/Kotlin/kotlinx.coroutines/blob/master/ui/coroutines-guide-ui.md) to learn about coroutine-based UI development.
* Review [best practices for using coroutines in Android](https://developer.android.com/kotlin/coroutines/coroutines-best-practices).
* Check out the [`kotlinx.coroutines` API reference](https://kotlinlang.org/api/kotlinx.coroutines/).

26 August 2025

---

## 2. Coroutine exceptions handling

This section covers exception handling and cancellation on exceptions. We already know that a cancelled coroutine throws [CancellationException](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/index.html) in suspension points and that it is ignored by the coroutines' machinery. Here we look at what happens if an exception is thrown during cancellation or multiple children of the same coroutine throw an exception.

## Exception propagation

Coroutine builders come in two flavors: propagating exceptions automatically ([launch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html)) or exposing them to users ([async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) and [produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html)). When these builders are used to create a root coroutine, that is not a child of another coroutine, the former builders treat exceptions as uncaught exceptions, similar to Java's `Thread.uncaughtExceptionHandler`, while the latter are relying on the user to consume the final exception, for example via [await](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/await.html) or [receive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/receive.html) ([produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html) and [receive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/receive.html) are covered in [Channels](https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/channels.md) section).

It can be demonstrated by a simple example that creates root coroutines using the [GlobalScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/index.html):

import kotlinx.coroutines.\*
//sampleStart
@OptIn(DelicateCoroutinesApi::class)
fun main() = runBlocking {
val job = GlobalScope.launch { // root coroutine with launch
println("Throwing exception from launch")
throw IndexOutOfBoundsException() // Will be printed to the console by Thread.defaultUncaughtExceptionHandler
}
job.join()
println("Joined failed job")
val deferred = GlobalScope.async { // root coroutine with async
println("Throwing exception from async")
throw ArithmeticException() // Nothing is printed, relying on user to call await
}
try {
deferred.await()
println("Unreached")
} catch (e: ArithmeticException) {
println("Caught ArithmeticException")
}
}
//sampleEnd

The output of this code is (with [debug](https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/coroutine-context-and-dispatchers.md#debugging-coroutines-and-threads)):

Throwing exception from launch
Exception in thread "DefaultDispatcher-worker-1 @coroutine#2" java.lang.IndexOutOfBoundsException
Joined failed job
Throwing exception from async
Caught ArithmeticException

## CoroutineExceptionHandler

It is possible to customize the default behavior of printing uncaught exceptions to the console. [CoroutineExceptionHandler](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/index.html) context element on a root coroutine can be used as a generic `catch` block for this root coroutine and all its children where custom exception handling may take place. It is similar to [`Thread.uncaughtExceptionHandler`](https://docs.oracle.com/javase/8/docs/api/java/lang/Thread.html#setUncaughtExceptionHandler-java.lang.Thread.UncaughtExceptionHandler-). You cannot recover from the exception in the `CoroutineExceptionHandler`. The coroutine had already completed with the corresponding exception when the handler is called. Normally, the handler is used to log the exception, show some kind of error message, terminate, and/or restart the application.

`CoroutineExceptionHandler` is invoked only on uncaught exceptions — exceptions that were not handled in any other way. In particular, all children coroutines (coroutines created in the context of another [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html)) delegate handling of their exceptions to their parent coroutine, which also delegates to the parent, and so on until the root, so the `CoroutineExceptionHandler` installed in their context is never used. In addition to that, [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) builder always catches all exceptions and represents them in the resulting [Deferred](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/index.html) object, so its `CoroutineExceptionHandler` has no effect either.

import kotlinx.coroutines.\*
@OptIn(DelicateCoroutinesApi::class)
fun main() = runBlocking {
//sampleStart
val handler = CoroutineExceptionHandler { \_, exception ->
println("CoroutineExceptionHandler got $exception")
}
val job = GlobalScope.launch(handler) { // root coroutine, running in GlobalScope
throw AssertionError()
}
val deferred = GlobalScope.async(handler) { // also root, but async instead of launch
throw ArithmeticException() // Nothing will be printed, relying on user to call deferred.await()
}
joinAll(job, deferred)
//sampleEnd
}

The output of this code is:

CoroutineExceptionHandler got java.lang.AssertionError

## Cancellation and exceptions

Cancellation is closely related to exceptions. Coroutines internally use `CancellationException` for cancellation, these exceptions are ignored by all handlers, so they should be used only as the source of additional debug information, which can be obtained by `catch` block. When a coroutine is cancelled using [Job.cancel](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/cancel.html), it terminates, but it does not cancel its parent.

import kotlinx.coroutines.\*
fun main() = runBlocking {
//sampleStart
val job = launch {
val child = launch {
try {
delay(Long.MAX\_VALUE)
} finally {
println("Child is cancelled")
}
}
yield()
println("Cancelling child")
child.cancel()
child.join()
yield()
println("Parent is not cancelled")
}
job.join()
//sampleEnd
}

The output of this code is:

Cancelling child
Child is cancelled
Parent is not cancelled

If a coroutine encounters an exception other than `CancellationException`, it cancels its parent with that exception. This behaviour cannot be overridden and is used to provide stable coroutines hierarchies for [structured concurrency](https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/composing-suspending-functions.md#structured-concurrency-with-async). [CoroutineExceptionHandler](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/index.html) implementation is not used for child coroutines.

The original exception is handled by the parent only when all its children terminate, which is demonstrated by the following example.

import kotlinx.coroutines.\*
@OptIn(DelicateCoroutinesApi::class)
fun main() = runBlocking {
//sampleStart
val handler = CoroutineExceptionHandler { \_, exception ->
println("CoroutineExceptionHandler got $exception")
}
val job = GlobalScope.launch(handler) {
launch { // the first child
try {
delay(Long.MAX\_VALUE)
} finally {
withContext(NonCancellable) {
println("Children are cancelled, but exception is not handled until all children terminate")
delay(100)
println("The first child finished its non cancellable block")
}
}
}
launch { // the second child
delay(10)
println("Second child throws an exception")
throw ArithmeticException()
}
}
job.join()
//sampleEnd
}

The output of this code is:

Second child throws an exception
Children are cancelled, but exception is not handled until all children terminate
The first child finished its non cancellable block
CoroutineExceptionHandler got java.lang.ArithmeticException

## Exceptions aggregation

When multiple children of a coroutine fail with an exception, the general rule is "the first exception wins", so the first exception gets handled. All additional exceptions that happen after the first one are attached to the first exception as suppressed ones.

import kotlinx.coroutines.\*
import java.io.\*
@OptIn(DelicateCoroutinesApi::class)
fun main() = runBlocking {
val handler = CoroutineExceptionHandler { \_, exception ->
println("CoroutineExceptionHandler got $exception with suppressed ${exception.suppressed.contentToString()}")
}
val job = GlobalScope.launch(handler) {
launch {
try {
delay(Long.MAX\_VALUE) // it gets cancelled when another sibling fails with IOException
} finally {
throw ArithmeticException() // the second exception
}
}
launch {
delay(100)
throw IOException() // the first exception
}
delay(Long.MAX\_VALUE)
}
job.join()
}

The output of this code is:

CoroutineExceptionHandler got java.io.IOException with suppressed [java.lang.ArithmeticException]

Cancellation exceptions are transparent and are unwrapped by default:

import kotlinx.coroutines.\*
import java.io.\*
@OptIn(DelicateCoroutinesApi::class)
fun main() = runBlocking {
//sampleStart
val handler = CoroutineExceptionHandler { \_, exception ->
println("CoroutineExceptionHandler got $exception")
}
val job = GlobalScope.launch(handler) {
val innerJob = launch { // all this stack of coroutines will get cancelled
launch {
launch {
throw IOException() // the original exception
}
}
}
try {
innerJob.join()
} catch (e: CancellationException) {
println("Rethrowing CancellationException with original cause")
throw e // cancellation exception is rethrown, yet the original IOException gets to the handler
}
}
job.join()
//sampleEnd
}

The output of this code is:

Rethrowing CancellationException with original cause
CoroutineExceptionHandler got java.io.IOException

## Supervision

As we have studied before, cancellation is a bidirectional relationship propagating through the whole hierarchy of coroutines. Let us take a look at the case when unidirectional cancellation is required.

A good example of such a requirement is a UI component with the job defined in its scope. If any of the UI's child tasks have failed, it is not always necessary to cancel (effectively kill) the whole UI component, but if the UI component is destroyed (and its job is cancelled), then it is necessary to cancel all child jobs as their results are no longer needed.

Another example is a server process that spawns multiple child jobs and needs to supervise their execution, tracking their failures and only restarting the failed ones.

### Supervision job

The [SupervisorJob](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-supervisor-job.html) can be used for these purposes. It is similar to a regular [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job.html) with the only exception that cancellation is propagated only downwards. This can easily be demonstrated using the following example:

import kotlinx.coroutines.\*
fun main() = runBlocking {
//sampleStart
val supervisor = SupervisorJob()
with(CoroutineScope(coroutineContext + supervisor)) {
// launch the first child -- its exception is ignored for this example (don't do this in practice!)
val firstChild = launch(CoroutineExceptionHandler { \_, \_ -> }) {
println("The first child is failing")
throw AssertionError("The first child is cancelled")
}
// launch the second child
val secondChild = launch {
firstChild.join()
// Cancellation of the first child is not propagated to the second child
println("The first child is cancelled: ${firstChild.isCancelled}, but the second one is still active")
try {
delay(Long.MAX\_VALUE)
} finally {
// But cancellation of the supervisor is propagated
println("The second child is cancelled because the supervisor was cancelled")
}
}
// wait until the first child fails & completes
firstChild.join()
println("Cancelling the supervisor")
supervisor.cancel()
secondChild.join()
}
//sampleEnd
}

The output of this code is:

The first child is failing
The first child is cancelled: true, but the second one is still active
Cancelling the supervisor
The second child is cancelled because the supervisor was cancelled

### Supervision scope

Instead of [coroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html), we can use [supervisorScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html) for scoped concurrency. It propagates the cancellation in one direction only and cancels all its children only if it failed itself. It also waits for all children before completion just like [coroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html) does.

import kotlin.coroutines.\*
import kotlinx.coroutines.\*
fun main() = runBlocking {
//sampleStart
try {
supervisorScope {
val child = launch {
try {
println("The child is sleeping")
delay(Long.MAX\_VALUE)
} finally {
println("The child is cancelled")
}
}
// Give our child a chance to execute and print using yield
yield()
println("Throwing an exception from the scope")
throw AssertionError()
}
} catch(e: AssertionError) {
println("Caught an assertion error")
}
//sampleEnd
}

The output of this code is:

The child is sleeping
Throwing an exception from the scope
The child is cancelled
Caught an assertion error

#### Exceptions in supervised coroutines

Another crucial difference between regular and supervisor jobs is exception handling. Every child should handle its exceptions by itself via the exception handling mechanism. This difference comes from the fact that child's failure does not propagate to the parent. It means that coroutines launched directly inside the [supervisorScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html) do use the [CoroutineExceptionHandler](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/index.html) that is installed in their scope in the same way as root coroutines do (see the [CoroutineExceptionHandler](#coroutineexceptionhandler) section for details).

import kotlin.coroutines.\*
import kotlinx.coroutines.\*
fun main() = runBlocking {
//sampleStart
val handler = CoroutineExceptionHandler { \_, exception ->
println("CoroutineExceptionHandler got $exception")
}
supervisorScope {
val child = launch(handler) {
println("The child throws an exception")
throw AssertionError()
}
println("The scope is completing")
}
println("The scope is completed")
//sampleEnd
}

The output of this code is:

The scope is completing
The child throws an exception
CoroutineExceptionHandler got java.lang.AssertionError
The scope is completed

27 September 2024

---

## 3. Composing suspending functions

This section covers various approaches to composition of suspending functions.

## Sequential by default

Assume that we have two suspending functions defined elsewhere that do something useful like some kind of remote service call or computation. We just pretend they are useful, but actually each one just delays for a second for the purpose of this example:

suspend fun doSomethingUsefulOne(): Int {
delay(1000L) // pretend we are doing something useful here
return 13
}
suspend fun doSomethingUsefulTwo(): Int {
delay(1000L) // pretend we are doing something useful here, too
return 29
}

What do we do if we need them to be invoked sequentially — first `doSomethingUsefulOne` and then `doSomethingUsefulTwo`, and compute the sum of their results? In practice, we do this if we use the result of the first function to make a decision on whether we need to invoke the second one or to decide on how to invoke it.

We use a normal sequential invocation, because the code in the coroutine, just like in the regular code, is sequential by default. The following example demonstrates it by measuring the total time it takes to execute both suspending functions:

import kotlinx.coroutines.\*
import kotlin.system.\*
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
val one = doSomethingUsefulOne()
val two = doSomethingUsefulTwo()
println("The answer is ${one + two}")
}
println("Completed in $time ms")
//sampleEnd
}
suspend fun doSomethingUsefulOne(): Int {
delay(1000L) // pretend we are doing something useful here
return 13
}
suspend fun doSomethingUsefulTwo(): Int {
delay(1000L) // pretend we are doing something useful here, too
return 29
}

It produces something like this:

The answer is 42
Completed in 2017 ms

## Concurrent using async

What if there are no dependencies between invocations of `doSomethingUsefulOne` and `doSomethingUsefulTwo` and we want to get the answer faster, by doing both concurrently? This is where [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) comes to help.

Conceptually, [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) is just like [launch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html). It starts a separate coroutine which is a light-weight thread that works concurrently with all the other coroutines. The difference is that `launch` returns a [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html) and does not carry any resulting value, while `async` returns a [Deferred](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/index.html) — a light-weight non-blocking future that represents a promise to provide a result later. You can use `.await()` on a deferred value to get its eventual result, but `Deferred` is also a `Job`, so you can cancel it if needed.

import kotlinx.coroutines.\*
import kotlin.system.\*
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
val one = async { doSomethingUsefulOne() }
val two = async { doSomethingUsefulTwo() }
println("The answer is ${one.await() + two.await()}")
}
println("Completed in $time ms")
//sampleEnd
}
suspend fun doSomethingUsefulOne(): Int {
delay(1000L) // pretend we are doing something useful here
return 13
}
suspend fun doSomethingUsefulTwo(): Int {
delay(1000L) // pretend we are doing something useful here, too
return 29
}

It produces something like this:

The answer is 42
Completed in 1017 ms

This is twice as fast, because the two coroutines execute concurrently. Note that concurrency with coroutines is always explicit.

## Lazily started async

Optionally, [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) can be made lazy by setting its `start` parameter to [CoroutineStart.LAZY](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-start/-l-a-z-y/index.html). In this mode it only starts the coroutine when its result is required by [await](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/await.html), or if its `Job`'s [start](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/start.html) function is invoked. Run the following example:

import kotlinx.coroutines.\*
import kotlin.system.\*
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
val one = async(start = CoroutineStart.LAZY) { doSomethingUsefulOne() }
val two = async(start = CoroutineStart.LAZY) { doSomethingUsefulTwo() }
// some computation
one.start() // start the first one
two.start() // start the second one
println("The answer is ${one.await() + two.await()}")
}
println("Completed in $time ms")
//sampleEnd
}
suspend fun doSomethingUsefulOne(): Int {
delay(1000L) // pretend we are doing something useful here
return 13
}
suspend fun doSomethingUsefulTwo(): Int {
delay(1000L) // pretend we are doing something useful here, too
return 29
}

It produces something like this:

The answer is 42
Completed in 1017 ms

So, here the two coroutines are defined but not executed as in the previous example, but the control is given to the programmer on when exactly to start the execution by calling [start](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/start.html). We first start `one`, then start `two`, and then await for the individual coroutines to finish.

Note that if we just call [await](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/await.html) in `println` without first calling [start](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/start.html) on individual coroutines, this will lead to sequential behavior, since [await](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/await.html) starts the coroutine execution and waits for its finish, which is not the intended use-case for laziness. The use-case for `async(start = CoroutineStart.LAZY)` is a replacement for the standard [lazy](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/lazy.html) function in cases when computation of the value involves suspending functions.

## Async-style functions

We can define async-style functions that invoke `doSomethingUsefulOne` and `doSomethingUsefulTwo` asynchronously using the [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) coroutine builder using a [GlobalScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/index.html) reference to opt-out of the structured concurrency. We name such functions with the "...Async" suffix to highlight the fact that they only start asynchronous computation and one needs to use the resulting deferred value to get the result.

// The result type of somethingUsefulOneAsync is Deferred<Int>
@OptIn(DelicateCoroutinesApi::class)
fun somethingUsefulOneAsync() = GlobalScope.async {
doSomethingUsefulOne()
}
// The result type of somethingUsefulTwoAsync is Deferred<Int>
@OptIn(DelicateCoroutinesApi::class)
fun somethingUsefulTwoAsync() = GlobalScope.async {
doSomethingUsefulTwo()
}

Note that these `xxxAsync` functions are not suspending functions. They can be used from anywhere. However, their use always implies asynchronous (here meaning concurrent) execution of their action with the invoking code.

The following example shows their use outside of coroutine:

import kotlinx.coroutines.\*
import kotlin.system.\*
//sampleStart
// note that we don't have `runBlocking` to the right of `main` in this example
fun main() {
val time = measureTimeMillis {
// we can initiate async actions outside of a coroutine
val one = somethingUsefulOneAsync()
val two = somethingUsefulTwoAsync()
// but waiting for a result must involve either suspending or blocking.
// here we use `runBlocking { ... }` to block the main thread while waiting for the result
runBlocking {
println("The answer is ${one.await() + two.await()}")
}
}
println("Completed in $time ms")
}
//sampleEnd
@OptIn(DelicateCoroutinesApi::class)
fun somethingUsefulOneAsync() = GlobalScope.async {
doSomethingUsefulOne()
}
@OptIn(DelicateCoroutinesApi::class)
fun somethingUsefulTwoAsync() = GlobalScope.async {
doSomethingUsefulTwo()
}
suspend fun doSomethingUsefulOne(): Int {
delay(1000L) // pretend we are doing something useful here
return 13
}
suspend fun doSomethingUsefulTwo(): Int {
delay(1000L) // pretend we are doing something useful here, too
return 29
}

Consider what happens if between the `val one = somethingUsefulOneAsync()` line and `one.await()` expression there is some logic error in the code, and the program throws an exception, and the operation that was being performed by the program aborts. Normally, a global error-handler could catch this exception, log and report the error for developers, but the program could otherwise continue doing other operations. However, here we have `somethingUsefulOneAsync` still running in the background, even though the operation that initiated it was aborted. This problem does not happen with structured concurrency, as shown in the section below.

## Structured concurrency with async

Let's refactor the [Concurrent using async](#concurrent-using-async) example into a function that runs `doSomethingUsefulOne` and `doSomethingUsefulTwo` concurrently and returns their combined results. Since [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) is a [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) extension, we'll use the [coroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html) function to provide the necessary scope:

suspend fun concurrentSum(): Int = coroutineScope {
val one = async { doSomethingUsefulOne() }
val two = async { doSomethingUsefulTwo() }
one.await() + two.await()
}

This way, if something goes wrong inside the code of the `concurrentSum` function, and it throws an exception, all the coroutines that were launched in its scope will be cancelled.

import kotlinx.coroutines.\*
import kotlin.system.\*
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
println("The answer is ${concurrentSum()}")
}
println("Completed in $time ms")
//sampleEnd
}
suspend fun concurrentSum(): Int = coroutineScope {
val one = async { doSomethingUsefulOne() }
val two = async { doSomethingUsefulTwo() }
one.await() + two.await()
}
suspend fun doSomethingUsefulOne(): Int {
delay(1000L) // pretend we are doing something useful here
return 13
}
suspend fun doSomethingUsefulTwo(): Int {
delay(1000L) // pretend we are doing something useful here, too
return 29
}

We still have concurrent execution of both operations, as evident from the output of the above `main` function:

The answer is 42
Completed in 1017 ms

Cancellation is always propagated through coroutines hierarchy:

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
try {
failedConcurrentSum()
} catch(e: ArithmeticException) {
println("Computation failed with ArithmeticException")
}
}
suspend fun failedConcurrentSum(): Int = coroutineScope {
val one = async<Int> {
try {
delay(Long.MAX\_VALUE) // Emulates very long computation
42
} finally {
println("First child was cancelled")
}
}
val two = async<Int> {
println("Second child throws an exception")
throw ArithmeticException()
}
one.await() + two.await()
}

Note how both the first `async` and the awaiting parent are cancelled on failure of one of the children (namely, `two`):

Second child throws an exception
First child was cancelled
Computation failed with ArithmeticException

27 February 2025

---

## 4. Coroutine context and dispatchers

Coroutines always execute in some context represented by a value of the [CoroutineContext](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.coroutines/-coroutine-context/) type, defined in the Kotlin standard library.

The coroutine context is a set of various elements. The main elements are the [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html) of the coroutine, which we've seen before, and its dispatcher, which is covered in this section.

## Dispatchers and threads

The coroutine context includes a coroutine dispatcher (see [CoroutineDispatcher](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/index.html)) that determines what thread or threads the corresponding coroutine uses for its execution. The coroutine dispatcher can confine coroutine execution to a specific thread, dispatch it to a thread pool, or let it run unconfined.

All coroutine builders like [launch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html) and [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) accept an optional [CoroutineContext](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.coroutines/-coroutine-context/) parameter that can be used to explicitly specify the dispatcher for the new coroutine and other context elements.

Try the following example:

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
//sampleStart
launch { // context of the parent, main runBlocking coroutine
println("main runBlocking : I'm working in thread ${Thread.currentThread().name}")
}
launch(Dispatchers.Unconfined) { // not confined -- will work with main thread
println("Unconfined : I'm working in thread ${Thread.currentThread().name}")
}
launch(Dispatchers.Default) { // will get dispatched to DefaultDispatcher
println("Default : I'm working in thread ${Thread.currentThread().name}")
}
launch(newSingleThreadContext("MyOwnThread")) { // will get its own new thread
println("newSingleThreadContext: I'm working in thread ${Thread.currentThread().name}")
}
//sampleEnd
}

It produces the following output (maybe in different order):

Unconfined : I'm working in thread main
Default : I'm working in thread DefaultDispatcher-worker-1
newSingleThreadContext: I'm working in thread MyOwnThread
main runBlocking : I'm working in thread main

When `launch { ... }` is used without parameters, it inherits the context (and thus dispatcher) from the [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) it is being launched from. In this case, it inherits the context of the main `runBlocking` coroutine which runs in the `main` thread.

[Dispatchers.Unconfined](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-unconfined.html) is a special dispatcher that also appears to run in the `main` thread, but it is, in fact, a different mechanism that is explained later.

The default dispatcher is used when no other dispatcher is explicitly specified in the scope. It is represented by [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html) and uses a shared background pool of threads.

[newSingleThreadContext](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/new-single-thread-context.html) creates a thread for the coroutine to run. A dedicated thread is a very expensive resource. In a real application it must be either released, when no longer needed, using the [close](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-executor-coroutine-dispatcher/close.html) function, or stored in a top-level variable and reused throughout the application.

## Unconfined vs confined dispatcher

The [Dispatchers.Unconfined](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-unconfined.html) coroutine dispatcher starts a coroutine in the caller thread, but only until the first suspension point. After suspension it resumes the coroutine in the thread that is fully determined by the suspending function that was invoked. The unconfined dispatcher is appropriate for coroutines which neither consume CPU time nor update any shared data (like UI) confined to a specific thread.

On the other side, the dispatcher is inherited from the outer [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) by default. The default dispatcher for the [runBlocking](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html) coroutine, in particular, is confined to the invoker thread, so inheriting it has the effect of confining execution to this thread with predictable FIFO scheduling.

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
//sampleStart
launch(Dispatchers.Unconfined) { // not confined -- will work with main thread
println("Unconfined : I'm working in thread ${Thread.currentThread().name}")
delay(500)
println("Unconfined : After delay in thread ${Thread.currentThread().name}")
}
launch { // context of the parent, main runBlocking coroutine
println("main runBlocking: I'm working in thread ${Thread.currentThread().name}")
delay(1000)
println("main runBlocking: After delay in thread ${Thread.currentThread().name}")
}
//sampleEnd
}

Produces the output:

Unconfined : I'm working in thread main
main runBlocking: I'm working in thread main
Unconfined : After delay in thread kotlinx.coroutines.DefaultExecutor
main runBlocking: After delay in thread main

So, the coroutine with the context inherited from `runBlocking {...}` continues to execute in the `main` thread, while the unconfined one resumes in the default executor thread that the [delay](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/delay.html) function is using.

## Debugging coroutines and threads

Coroutines can suspend on one thread and resume on another thread. Even with a single-threaded dispatcher it might be hard to figure out what the coroutine was doing, where, and when if you don't have special tooling.

### Debugging with IDEA

The Coroutine Debugger of the Kotlin plugin simplifies debugging coroutines in IntelliJ IDEA.

The Debug tool window contains the Coroutines tab. In this tab, you can find information about both currently running and suspended coroutines. The coroutines are grouped by the dispatcher they are running on.

With the coroutine debugger, you can:

* Check the state of each coroutine.
* See the values of local and captured variables for both running and suspended coroutines.
* See a full coroutine creation stack, as well as a call stack inside the coroutine. The stack includes all frames with variable values, even those that would be lost during standard debugging.
* Get a full report that contains the state of each coroutine and its stack. To obtain it, right-click inside the Coroutines tab, and then click Get Coroutines Dump.

To start coroutine debugging, you just need to set breakpoints and run the application in debug mode.

Learn more about coroutines debugging in the [tutorial](/docs/tutorials/coroutines/debug-coroutines-with-idea.html).

### Debugging using logging

Another approach to debugging applications with threads without Coroutine Debugger is to print the thread name in the log file on each log statement. This feature is universally supported by logging frameworks. When using coroutines, the thread name alone does not give much of a context, so `kotlinx.coroutines` includes debugging facilities to make it easier.

Run the following code with `-Dkotlinx.coroutines.debug` JVM option:

import kotlinx.coroutines.\*
fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
fun main() = runBlocking<Unit> {
//sampleStart
val a = async {
log("I'm computing a piece of the answer")
6
}
val b = async {
log("I'm computing another piece of the answer")
7
}
log("The answer is ${a.await() \* b.await()}")
//sampleEnd
}

There are three coroutines. The main coroutine (#1) inside `runBlocking` and two coroutines computing the deferred values `a` (#2) and `b` (#3). They are all executing in the context of `runBlocking` and are confined to the main thread. The output of this code is:

[main @coroutine#2] I'm computing a piece of the answer
[main @coroutine#3] I'm computing another piece of the answer
[main @coroutine#1] The answer is 42

The `log` function prints the name of the thread in square brackets, and you can see that it is the `main` thread with the identifier of the currently executing coroutine appended to it. This identifier is consecutively assigned to all created coroutines when the debugging mode is on.

## Jumping between threads

Run the following code with the `-Dkotlinx.coroutines.debug` JVM option (see [debug](#debugging-coroutines-and-threads)):

import kotlinx.coroutines.\*
fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
fun main() {
newSingleThreadContext("Ctx1").use { ctx1 ->
newSingleThreadContext("Ctx2").use { ctx2 ->
runBlocking(ctx1) {
log("Started in ctx1")
withContext(ctx2) {
log("Working in ctx2")
}
log("Back to ctx1")
}
}
}
}

The example above demonstrates new techniques in coroutine usage.

The first technique shows how to use [runBlocking](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html) with a specified context.   
 The second technique involves calling [withContext](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html), which may suspend the current coroutine and switch to a new context—provided the new context differs from the existing one. Specifically, if you specify a different [CoroutineDispatcher](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/index.html), extra dispatches are required: the block is scheduled on the new dispatcher, and once it finishes, execution returns to the original dispatcher.

As a result, the output of the above code is:

[Ctx1 @coroutine#1] Started in ctx1
[Ctx2 @coroutine#1] Working in ctx2
[Ctx1 @coroutine#1] Back to ctx1

The example above uses the `use` function from the Kotlin standard library to properly release thread resources created by [newSingleThreadContext](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/new-single-thread-context.html) when they're no longer needed.

## Job in the context

The coroutine's [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html) is part of its context, and can be retrieved from it using the `coroutineContext[Job]` expression:

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
//sampleStart
println("My job is ${coroutineContext[Job]}")
//sampleEnd
}

In [debug mode](#debugging-coroutines-and-threads), it outputs something like this:

My job is "coroutine#1":BlockingCoroutine{Active}@6d311334

Note that [isActive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/is-active.html) in [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) is just a convenient shortcut for `coroutineContext[Job]?.isActive == true`.

## Children of a coroutine

When a coroutine is launched in the [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) of another coroutine, it inherits its context via [CoroutineScope.coroutineContext](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/coroutine-context.html) and the [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html) of the new coroutine becomes a child of the parent coroutine's job. When the parent coroutine is cancelled, all its children are recursively cancelled, too.

However, this parent-child relation can be explicitly overridden in one of two ways:

1. When a different scope is explicitly specified when launching a coroutine (for example, `GlobalScope.launch`), it does not inherit a `Job` from the parent scope.
2. When a different `Job` object is passed as the context for the new coroutine (as shown in the example below), it overrides the `Job` of the parent scope.

In both cases, the launched coroutine is not tied to the scope it was launched from and operates independently.

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
//sampleStart
// launch a coroutine to process some kind of incoming request
val request = launch {
// it spawns two other jobs
launch(Job()) {
println("job1: I run in my own Job and execute independently!")
delay(1000)
println("job1: I am not affected by cancellation of the request")
}
// and the other inherits the parent context
launch {
delay(100)
println("job2: I am a child of the request coroutine")
delay(1000)
println("job2: I will not execute this line if my parent request is cancelled")
}
}
delay(500)
request.cancel() // cancel processing of the request
println("main: Who has survived request cancellation?")
delay(1000) // delay the main thread for a second to see what happens
//sampleEnd
}

The output of this code is:

job1: I run in my own Job and execute independently!
job2: I am a child of the request coroutine
main: Who has survived request cancellation?
job1: I am not affected by cancellation of the request

## Parental responsibilities

A parent coroutine always waits for the completion of all its children. A parent does not have to explicitly track all the children it launches, and it does not have to use [Job.join](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/join.html) to wait for them at the end:

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
//sampleStart
// launch a coroutine to process some kind of incoming request
val request = launch {
repeat(3) { i -> // launch a few children jobs
launch {
delay((i + 1) \* 200L) // variable delay 200ms, 400ms, 600ms
println("Coroutine $i is done")
}
}
println("request: I'm done and I don't explicitly join my children that are still active")
}
request.join() // wait for completion of the request, including all its children
println("Now processing of the request is complete")
//sampleEnd
}

The result is going to be:

request: I'm done and I don't explicitly join my children that are still active
Coroutine 0 is done
Coroutine 1 is done
Coroutine 2 is done
Now processing of the request is complete

## Naming coroutines for debugging

Automatically assigned ids are good when coroutines log often and you just need to correlate log records coming from the same coroutine. However, when a coroutine is tied to the processing of a specific request or doing some specific background task, it is better to name it explicitly for debugging purposes. The [CoroutineName](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-name/index.html) context element serves the same purpose as the thread name. It is included in the thread name that is executing this coroutine when the [debugging mode](#debugging-coroutines-and-threads) is turned on.

The following example demonstrates this concept:

import kotlinx.coroutines.\*
fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
fun main() = runBlocking(CoroutineName("main")) {
//sampleStart
log("Started main coroutine")
// run two background value computations
val v1 = async(CoroutineName("v1coroutine")) {
delay(500)
log("Computing v1")
6
}
val v2 = async(CoroutineName("v2coroutine")) {
delay(1000)
log("Computing v2")
7
}
log("The answer for v1 \* v2 = ${v1.await() \* v2.await()}")
//sampleEnd
}

The output it produces with `-Dkotlinx.coroutines.debug` JVM option is similar to:

[main @main#1] Started main coroutine
[main @v1coroutine#2] Computing v1
[main @v2coroutine#3] Computing v2
[main @main#1] The answer for v1 \* v2 = 42

## Combining context elements

Sometimes we need to define multiple elements for a coroutine context. We can use the `+` operator for that. For example, we can launch a coroutine with an explicitly specified dispatcher and an explicitly specified name at the same time:

import kotlinx.coroutines.\*
fun main() = runBlocking<Unit> {
//sampleStart
launch(Dispatchers.Default + CoroutineName("test")) {
println("I'm working in thread ${Thread.currentThread().name}")
}
//sampleEnd
}

The output of this code with the `-Dkotlinx.coroutines.debug` JVM option is:

I'm working in thread DefaultDispatcher-worker-1 @test#2

## Coroutine scope

Let us put our knowledge about contexts, children, and jobs together. Assume that our application has an object with a lifecycle, but that object is not a coroutine. For example, we are writing an Android application, and launching various coroutines in the context of an Android activity to perform asynchronous operations to fetch and update data, do animations, etc. These coroutines must be cancelled when the activity is destroyed to avoid memory leaks. We, of course, can manipulate contexts and jobs manually to tie the lifecycles of the activity and its coroutines, but `kotlinx.coroutines` provides an abstraction encapsulating that: [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html). You should be already familiar with the coroutine scope as all coroutine builders are declared as extensions on it.

We manage the lifecycles of our coroutines by creating an instance of [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) tied to the lifecycle of our activity. A `CoroutineScope` instance can be created by the [CoroutineScope()](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope.html) or [MainScope()](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-main-scope.html) factory functions. The former creates a general-purpose scope, while the latter creates a scope for UI applications and uses [Dispatchers.Main](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-main.html) as the default dispatcher:

class Activity {
private val mainScope = MainScope()
fun destroy() {
mainScope.cancel()
}
// to be continued ...

Now, we can launch coroutines in the scope of this `Activity` using the defined `mainScope`. For the demo, we launch ten coroutines that delay for a different time:

// class Activity continues
fun doSomething() {
// launch ten coroutines for a demo, each working for a different time
repeat(10) { i ->
mainScope.launch {
delay((i + 1) \* 200L) // variable delay 200ms, 400ms, ... etc
println("Coroutine $i is done")
}
}
}
} // class Activity ends

In our main function we create the activity, call our test `doSomething` function, and destroy the activity after 500ms. This cancels all the coroutines that were launched from `doSomething`. We can see that because after the destruction of the activity, no more messages are printed, even if we wait a little longer.

import kotlinx.coroutines.\*
class Activity {
private val mainScope = CoroutineScope(Dispatchers.Default) // use Default for test purposes
fun destroy() {
mainScope.cancel()
}
fun doSomething() {
// launch ten coroutines for a demo, each working for a different time
repeat(10) { i ->
mainScope.launch {
delay((i + 1) \* 200L) // variable delay 200ms, 400ms, ... etc
println("Coroutine $i is done")
}
}
}
} // class Activity ends
fun main() = runBlocking<Unit> {
//sampleStart
val activity = Activity()
activity.doSomething() // run test function
println("Launched coroutines")
delay(500L) // delay for half a second
println("Destroying activity!")
activity.destroy() // cancels all coroutines
delay(1000) // visually confirm that they don't work
//sampleEnd
}

The output of this example is:

Launched coroutines
Coroutine 0 is done
Coroutine 1 is done
Destroying activity!

As you can see, only the first two coroutines print a message and the others are cancelled by a single invocation of [`mainScope.cancel()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/cancel.html) in `Activity.destroy()`.

### Thread-local data

Sometimes it is convenient to be able to pass some thread-local data to or between coroutines. However, since they are not bound to any particular thread, this will likely lead to boilerplate if done manually.

For [`ThreadLocal`](https://docs.oracle.com/javase/8/docs/api/java/lang/ThreadLocal.html), the [asContextElement](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/as-context-element.html) extension function is here for the rescue. It creates an additional context element which keeps the value of the given `ThreadLocal` and restores it every time the coroutine switches its context.

It is easy to demonstrate it in action:

import kotlinx.coroutines.\*
val threadLocal = ThreadLocal<String?>() // declare thread-local variable
fun main() = runBlocking<Unit> {
//sampleStart
threadLocal.set("main")
println("Pre-main, current thread: ${Thread.currentThread()}, thread local value: '${threadLocal.get()}'")
val job = launch(Dispatchers.Default + threadLocal.asContextElement(value = "launch")) {
println("Launch start, current thread: ${Thread.currentThread()}, thread local value: '${threadLocal.get()}'")
yield()
println("After yield, current thread: ${Thread.currentThread()}, thread local value: '${threadLocal.get()}'")
}
job.join()
println("Post-main, current thread: ${Thread.currentThread()}, thread local value: '${threadLocal.get()}'")
//sampleEnd
}

In this example, we launch a new coroutine in a background thread pool using [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html), so it works on different threads from the thread pool, but it still has the value of the thread local variable that we specified using `threadLocal.asContextElement(value = "launch")`, no matter which thread the coroutine is executed on. Thus, the output (with [debug](#debugging-coroutines-and-threads)) is:

Pre-main, current thread: Thread[main @coroutine#1,5,main], thread local value: 'main'
Launch start, current thread: Thread[DefaultDispatcher-worker-1 @coroutine#2,5,main], thread local value: 'launch'
After yield, current thread: Thread[DefaultDispatcher-worker-2 @coroutine#2,5,main], thread local value: 'launch'
Post-main, current thread: Thread[main @coroutine#1,5,main], thread local value: 'main'

It's easy to forget to set the corresponding context element. The thread-local variable accessed from the coroutine may then have an unexpected value if the thread running the coroutine is different. To avoid such situations, it is recommended to use the [ensurePresent](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/ensure-present.html) method and fail-fast on improper usages.

`ThreadLocal` has first-class support and can be used with any primitive `kotlinx.coroutines` provides. It has one key limitation, though: when a thread-local is mutated, a new value is not propagated to the coroutine caller (because a context element cannot track all `ThreadLocal` object accesses), and the updated value is lost on the next suspension. Use [withContext](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html) to update the value of the thread-local in a coroutine, see [asContextElement](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/as-context-element.html) for more details.

Alternatively, a value can be stored in a mutable box like `class Counter(var i: Int)`, which is, in turn, stored in a thread-local variable. However, in this case, you are fully responsible to synchronize potentially concurrent modifications to the variable in this mutable box.

For advanced usage, for example, for integration with logging MDC, transactional contexts or any other libraries that internally use thread-locals for passing data, see the documentation of the [ThreadContextElement](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-thread-context-element/index.html) interface that should be implemented.

27 February 2025

---

## 5. Cancellation and timeouts

Cancellation lets you stop a coroutine before it completes. It stops work that's no longer needed, such as when a user closes a window or navigates away in a user interface while a coroutine is still running. You can also use it to release resources early and to stop a coroutine from accessing objects past their disposal.

Cancellation works through the [`Job`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/) handle, which represents the lifecycle of a coroutine and its parent-child relationships. `Job` allows you to check whether the coroutine is active and allows you to cancel it, along with its children, as defined by [structured concurrency](coroutines-basics.html#coroutine-scope-and-structured-concurrency).

## Cancel coroutines

A coroutine is canceled when the [`cancel()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/cancel.html) function is invoked on its `Job` handle. [Coroutine builder functions](coroutines-basics.html#coroutine-builder-functions) such as [`.launch()`](coroutines-basics.html#coroutinescope-launch) return a `Job`. The [`.async()`](coroutines-basics.html#coroutinescope-async) function returns a [`Deferred`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/), which implements `Job` and supports the same cancellation behavior.

You can call the `cancel()` function manually, or it can be invoked automatically through cancellation propagation when a parent coroutine is canceled.

When a coroutine is canceled, it throws a [`CancellationException`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/) the next time it checks for cancellation. For more information about how and when this happens, see [Suspension points and cancellation](#suspension-points-and-cancellation).

Here's an example on how to manually cancel coroutines:

import kotlinx.coroutines.\*
import kotlin.time.Duration
//sampleStart
suspend fun main() {
withContext(Dispatchers.Default) {
// Used as a signal that the coroutine has started running
val job1Started = CompletableDeferred<Unit>()
val job1: Job = launch {
println("The coroutine has started")
// Completes the CompletableDeferred,
// signaling that the coroutine has started running
job1Started.complete(Unit)
try {
// Suspends indefinitely
// Without cancellation, this call would never return
delay(Duration.INFINITE)
} catch (e: CancellationException) {
println("The coroutine was canceled: $e")
// Always rethrow cancellation exceptions!
throw e
}
println("This line will never be executed")
}
// Waits for job1 to start before canceling it
job1Started.await()
// Cancels the coroutine, so delay() throws a CancellationException
job1.cancel()
// async returns a Deferred handle, which inherits from Job
val job2 = async {
// If the coroutine is canceled before its body starts executing,
// this line may not be printed
println("The second coroutine has started")
try {
// Equivalent to delay(Duration.INFINITE)
// Suspends until this coroutine is canceled
awaitCancellation()
} catch (e: CancellationException) {
println("The second coroutine was canceled")
throw e
}
}
job2.cancel()
}
// Coroutine builders such as withContext() or coroutineScope()
// wait for all child coroutines to complete,
// even when the children are canceled
println("All coroutines have completed")
}
//sampleEnd

In this example, [`CompletableDeferred`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-completable-deferred/) is used as a signal that the coroutine has started running. The coroutine calls `complete()` when it starts executing, and `await()` only returns once that `CompletableDeferred` is completed. This way, cancellation happens only after the coroutine has started running. The coroutine created by `.async()` doesn't have this check, so it may be canceled before it can run the code inside its block.

### Cancellation propagation

[Structured concurrency](coroutines-basics.html#coroutine-scope-and-structured-concurrency) ensures that canceling a coroutine also cancels all of its children. This prevents child coroutines from working after the parent has already stopped.

Here's an example:

import kotlinx.coroutines.\*
import kotlin.time.Duration
//sampleStart
suspend fun main() {
withContext(Dispatchers.Default) {
// Used as a signal that the child coroutines have been launched
val childrenLaunched = CompletableDeferred<Unit>()
// Launches two child coroutines
val parentJob = launch {
launch {
println("Child coroutine 1 has started running")
try {
awaitCancellation()
} finally {
println("Child coroutine 1 has been canceled")
}
}
launch {
println("Child coroutine 2 has started running")
try {
awaitCancellation()
} finally {
println("Child coroutine 2 has been canceled")
}
}
// Completes the CompletableDeferred,
// signaling that the child coroutines have been launched
childrenLaunched.complete(Unit)
}
// Waits for the parent coroutine to signal that it has launched
// all of its children
childrenLaunched.await()
// Cancels the parent coroutine, which cancels all its children
parentJob.cancel()
}
}
//sampleEnd

In this example, each child coroutine uses a [`finally` block](exceptions.html#the-finally-block), so the code inside it runs when the coroutine is canceled. Here, `CompletableDeferred` signals that the child coroutines are launched before they are canceled, but it doesn't guarantee that they start running. If they are canceled first, nothing is printed.

## Make coroutines react to cancellation

In Kotlin, coroutine cancellation is cooperative. This means that coroutines only react to cancellation when they cooperate by [suspending](#suspension-points-and-cancellation) or [checking for cancellation explicitly](#check-for-cancellation-explicitly).

In this section, you can learn how to create cancelable coroutines.

### Suspension points and cancellation

When a coroutine is canceled, it continues running until it reaches a point in the code where it may suspend, also known as a suspension point. If the coroutine suspends there, the suspending function checks whether it has been canceled. If it has, the coroutine stops and throws `CancellationException`.

A call to a `suspend` function is a suspension point, but it doesn't always suspend. For example, when awaiting a `Deferred` result, the coroutine only suspends if that `Deferred` isn't completed yet.

Here's an example using common suspending functions that suspend, enabling the coroutine to check and stop when it's canceled:

import kotlinx.coroutines.\*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.channels.Channel
import kotlin.time.Duration.Companion.milliseconds
import kotlin.time.Duration
suspend fun main() {
withContext(Dispatchers.Default) {
val childJobs = listOf(
launch {
// Suspends until canceled
awaitCancellation()
},
launch {
// Suspends until canceled
delay(Duration.INFINITE)
},
launch {
val channel = Channel<Int>()
// Suspends while waiting for a value that is never sent
channel.receive()
},
launch {
val deferred = CompletableDeferred<Int>()
// Suspends while waiting for a value that is never completed
deferred.await()
},
launch {
val mutex = Mutex(locked = true)
// Suspends while waiting for a mutex that remains locked indefinitely
mutex.lock()
}
)
// Gives the child coroutines time to start and suspend
delay(100.milliseconds)
// Cancels all child coroutines
childJobs.forEach { it.cancel() }
}
println("All child jobs completed!")
}

### Check for cancellation explicitly

If a coroutine doesn't [suspend](#suspension-points-and-cancellation) for a long time, it doesn't stop when it's canceled unless it explicitly checks for cancellation.

To check for cancellation, use the following APIs:

* [`isActive`](#isactive) property is `false` when the coroutine is canceled.
* [`ensureActive()`](#ensureactive) function throws `CancellationException` immediately if the coroutine is canceled.
* [`yield()`](#yield) function suspends the coroutine, releasing the thread and giving other coroutines a chance to run on it. Suspending the coroutine lets it check for cancellation and throw `CancellationException` if it's canceled.

These APIs are useful when your coroutines run for a long time between suspension points or are unlikely to suspend at suspension points.

#### isActive

Use the [`isActive`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/is-active.html) property in long-running computations to periodically check for cancellation. This property is `false` when the coroutine is no longer active, which you can use to gracefully stop the coroutine when it no longer needs to continue the operation:

Here's an example:

import kotlinx.coroutines.\*
import kotlin.time.Duration.Companion.milliseconds
import kotlin.random.Random
//sampleStart
suspend fun main() {
withContext(Dispatchers.Default) {
val unsortedList = MutableList(10) { Random.nextInt() }
// Starts a long-running computation
val listSortingJob = launch {
// Repeatedly sorts the list while the coroutine remains active
while (isActive) {
unsortedList.sort()
++i
}
println(
"Stopped sorting the list after $i iterations"
)
}
// Sorts the list for 100 milliseconds, then considers it sorted enough
delay(100.milliseconds)
// Cancels the sorting when the result is good enough
listSortingJob.cancel()
// Waits until the sorting coroutine finishes
// before accessing the shared list to avoid data races
listSortingJob.join()
println("The list is probably sorted: $unsortedList")
}
}
//sampleEnd

In this example, the [`join()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/join.html) function suspends the coroutine until it finishes. This ensures that the list isn't accessed while the sorting coroutine is still running.

#### ensureActive()

Use the [`ensureActive()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/ensure-active.html) function to check for cancellation and stop the current computation by throwing `CancellationException` if the coroutine is canceled:

import kotlinx.coroutines.\*
import kotlin.time.Duration.Companion.milliseconds
suspend fun main() {
withContext(Dispatchers.Default) {
val childJob = launch {
try {
while (true) {
++start
// Checks the Collatz conjecture for the current number
while (n != 1) {
// Throws CancellationException if the coroutine is canceled
ensureActive()
n = if (n % 2 == 0) n / 2 else 3 \* n + 1
}
}
} finally {
println("Checked the Collatz conjecture for 0..${start-1}")
}
}
// Runs the computation for one second
delay(100.milliseconds)
// Cancels the coroutine
childJob.cancel()
}
}

#### yield()

The [`yield()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/yield.html) function suspends the coroutine and checks for cancellation before resuming. Without suspending, coroutines on the same thread run sequentially.

Use `yield` to allow other coroutines to run on the same thread or thread pool before one of them finishes:

import kotlinx.coroutines.\*
//sampleStart
fun main() {
// runBlocking uses the current thread for running all coroutines
runBlocking {
val coroutineCount = 5
repeat(coroutineCount) { coroutineIndex ->
launch {
val id = coroutineIndex + 1
repeat(5) { iterationIndex ->
val iteration = iterationIndex + 1
// Temporarily suspends to give other coroutines a chance to run
// Without this, the coroutines run sequentially
yield()
// Prints the coroutine index and iteration index
println("$id \* $iteration = ${id \* iteration}")
}
}
}
}
}
//sampleEnd

In this example, each coroutine uses `yield()` to let other coroutines run between iterations.

### Interrupt blocking code when coroutines are canceled

On the JVM, some functions, such as `Thread.sleep()` or `BlockingQueue.take()`, can block the current thread. These blocking functions can be interrupted, which stops them prematurely. However, when you call them from a coroutine, cancellation doesn't interrupt the thread.

To interrupt the thread when canceling a coroutine, use the [`runInterruptible()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-interruptible.html) function:

import kotlinx.coroutines.\*
//sampleStart
suspend fun main() {
withContext(Dispatchers.Default) {
val childStarted = CompletableDeferred<Unit>()
val childJob = launch {
try {
// Cancellation triggers a thread interruption
runInterruptible {
childStarted.complete(Unit)
try {
// Blocks the current thread for a very long time
Thread.sleep(Long.MAX\_VALUE)
} catch (e: InterruptedException) {
println("Thread interrupted (Java): $e")
throw e
}
}
} catch (e: CancellationException) {
println("Coroutine canceled (Kotlin): $e")
throw e
}
}
childStarted.await()
// Cancels the coroutine and interrupts the thread
// by running Thread.sleep()
childJob.cancel()
}
}
//sampleEnd

## Handle values safely when canceling coroutines

When a suspended coroutine is canceled, it resumes with a `CancellationException` instead of returning any values, even if those values are already available. This behavior is called prompt cancellation. It prevents your code from continuing in a canceled coroutine's scope, such as updating a screen that's already closed.

Here's an example:

import java.nio.file.\*
import java.nio.charset.\*
import kotlinx.coroutines.\*
import java.io.\*
// Defines a coroutine scope that uses the UI thread
class ScreenWithFileContents(private val scope: CoroutineScope) {
fun displayFile(path: Path) {
scope.launch {
val contents = withContext(Dispatchers.IO) {
Files.newBufferedReader(
path, Charset.forName("US-ASCII")
).use {
it.readLines()
}
}
// It's safe to call updateUi here,
// In case of cancellation, withContext() wouldn't return any values
updateUi(contents)
}
}
// Throws an exception if called after the user left the screen
private fun updateUi(contents: List<String>) {
contents.forEach { line -> addOneLineToUi(line) }
}
private fun addOneLineToUi(line: String) {
// Placeholder for code that adds one line to the UI
}
// Only callable from the UI thread
fun leaveScreen() {
// Cancels the scope when leaving the screen
// You can no longer update the UI
scope.cancel()
}
}

In this example, `withContext(Dispatchers.IO)` cooperates with cancellation and prevents `updateUI()` from running if the `leaveScreen()` function cancels the coroutine before it returns the contents of the file.

While prompt cancellation prevents using values after they are no longer valid, it can also stop your code while an important value is still in use, which might lead to losing that value. This can happen when a coroutine receives a value, such as an `AutoCloseable` resource, but is canceled before it can reach the part of the code that closes it. To prevent this, keep cleanup logic in a place that's guaranteed to run even when the coroutine receiving the value is canceled.

Here's an example:

import java.nio.file.\*
import java.nio.charset.\*
import kotlinx.coroutines.\*
import java.io.\*
// scope is a coroutine scope using the UI thread
class ScreenWithFileContents(private val scope: CoroutineScope) {
fun displayFile(path: Path) {
scope.launch {
// Stores the reader in a variable, so the finally block can close it
var reader: BufferedReader? = null
try {
withContext(Dispatchers.IO) {
reader = Files.newBufferedReader(
path, Charset.forName("US-ASCII")
)
}
// Uses the stored reader after withContext() completes
updateUi(reader!!)
} finally {
// Ensures the reader is closed even when the coroutine is canceled
reader?.close()
}
}
}
private suspend fun updateUi(reader: BufferedReader) {
// Shows the file contents
while (true) {
val line = withContext(Dispatchers.IO) {
reader.readLine()
}
if (line == null)
break
addOneLineToUi(line)
}
}
private fun addOneLineToUi(line: String) {
// Placeholder for code that adds one line to the UI
}
// Only callable from the UI thread
fun leaveScreen() {
// Cancels the scope when leaving the screen
// You can no longer update the UI
scope.cancel()
}
}

In this example, storing the `BufferedReader` in a variable and closing it in the `finally` block ensures the resource is released even if the coroutine is canceled.

### Run non-cancelable blocks

You can prevent cancellation from affecting certain parts of a coroutine. To do so, pass [`NonCancellable`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-non-cancellable/) as an argument to the `withContext()` coroutine builder function.

`NonCancellable` is useful when you need to ensure that certain operations, such as closing resources with a suspending `close()` function, complete even if the coroutine is canceled before they finish.

Here's an example:

import kotlinx.coroutines.\*
import kotlin.time.Duration.Companion.milliseconds
//sampleStart
val serviceStarted = CompletableDeferred<Unit>()
fun startService() {
println("Starting the service...")
serviceStarted.complete(Unit)
}
suspend fun shutdownServiceAndWait() {
println("Shutting down...")
delay(100.milliseconds)
println("Successfully shut down!")
}
suspend fun main() {
withContext(Dispatchers.Default) {
val childJob = launch {
startService()
try {
awaitCancellation()
} finally {
withContext(NonCancellable) {
// Without withContext(NonCancellable),
// This function doesn't complete because the coroutine is canceled
shutdownServiceAndWait()
}
}
}
serviceStarted.await()
childJob.cancel()
}
println("Exiting the program")
}
//sampleEnd

## Timeout

Timeouts allow you to automatically cancel a coroutine after a specified duration. They are useful for stopping operations that take too long, helping to keep your application responsive and avoid blocking threads unnecessarily.

To specify a timeout, use the [`withTimeoutOrNull()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-timeout-or-null.html) function with a `Duration`:

import kotlinx.coroutines.\*
import kotlin.time.Duration.Companion.milliseconds
//sampleStart
suspend fun slowOperation(): Int {
try {
delay(300.milliseconds)
return 5
} catch (e: CancellationException) {
println("The slow operation has been canceled: $e")
throw e
}
}
suspend fun fastOperation(): Int {
try {
delay(15.milliseconds)
return 14
} catch (e: CancellationException) {
println("The fast operation has been canceled: $e")
throw e
}
}
suspend fun main() {
withContext(Dispatchers.Default) {
val slow = withTimeoutOrNull(100.milliseconds) {
slowOperation()
}
println("The slow operation finished with $slow")
val fast = withTimeoutOrNull(100.milliseconds) {
fastOperation()
}
println("The fast operation finished with $fast")
}
}
//sampleEnd

If the timeout exceeds the specified `Duration`, `withTimeoutOrNull()` returns `null`.

29 January 2026

---

## 6. Coroutines basics

To create applications that perform multiple tasks at once, a concept known as concurrency, Kotlin uses coroutines. A coroutine is a suspendable computation that lets you write concurrent code in a clear, sequential style. Coroutines can run concurrently with other coroutines and potentially in parallel.

On the JVM and in Kotlin/Native, all concurrent code, such as coroutines, runs on threads, managed by the operating system. Coroutines can suspend their execution instead of blocking a thread. This allows one coroutine to suspend while waiting for some data to arrive and another coroutine to run on the same thread, ensuring effective resource utilization.

For more information about the differences between coroutines and threads, see [Comparing coroutines and JVM threads](#comparing-coroutines-and-jvm-threads).

## Suspending functions

The most basic building block of coroutines is the suspending function. It allows a running operation to pause and resume later without affecting the structure of your code.

To declare a suspending function, use the `suspend` keyword:

suspend fun greet() {
println("Hello world from a suspending function")
}

You can only call a suspending function from another suspending function. To call suspending functions at the entry point of a Kotlin application, mark the `main()` function with the `suspend` keyword:

suspend fun main() {
showUserInfo()
}
suspend fun showUserInfo() {
println("Loading user...")
greet()
println("User: John Smith")
}
suspend fun greet() {
println("Hello world from a suspending function")
}

This example doesn't use concurrency yet, but by marking the functions with the `suspend` keyword, you allow them to call other suspending functions and run concurrent code inside.

While the `suspend` keyword is part of the core Kotlin language, most coroutine features are available through the [`kotlinx.coroutines`](https://github.com/Kotlin/kotlinx.coroutines) library.

## Add the kotlinx.coroutines library to your project

To include the `kotlinx.coroutines` library in your project, add the corresponding dependency configuration based on your build tool:

// build.gradle.kts
repositories {
mavenCentral()
}
dependencies {
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2")
}

// build.gradle
repositories {
mavenCentral()
}
dependencies {
implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2'
}

<!-- pom.xml -->
<project>
<dependencies>
<dependency>
<groupId>org.jetbrains.kotlinx</groupId>
<artifactId>kotlinx-coroutines-core</artifactId>
<version>1.10.2</version>
</dependency>
</dependencies>
...
</project>

## Create your first coroutines

To create a coroutine in Kotlin, you need the following:

* A [suspending function](#suspending-functions).
* A [coroutine scope](#coroutine-scope-and-structured-concurrency) in which it can run, for example inside the `withContext()` function.
* A [coroutine builder](#coroutine-builder-functions) like `CoroutineScope.launch()` to start it.
* A [dispatcher](#coroutine-dispatchers) to control which threads it uses.

Let's look at an example that uses multiple coroutines in a multithreaded environment:

1. Import the `kotlinx.coroutines` library:

   import kotlinx.coroutines.\*
2. Mark functions that can pause and resume with the `suspend` keyword:

   suspend fun greet() {
   println("The greet() on the thread: ${Thread.currentThread().name}")
   }
   suspend fun main() {}
3. Add the [`delay()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/delay.html#) function to simulate a suspending task, such as fetching data or writing to a database:

   suspend fun greet() {
   println("The greet() on the thread: ${Thread.currentThread().name}")
   delay(1000L)
   }
4. Use [`withContext(Dispatchers.Default)`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html#) to define an entry point for multithreaded concurrent code that runs on a shared thread pool:

   suspend fun main() {
   withContext(Dispatchers.Default) {
   // Add the coroutine builders here
   }
   }
5. Use a [coroutine builder function](#coroutine-builder-functions) like [`CoroutineScope.launch()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html) to start the coroutine:

   suspend fun main() {
   withContext(Dispatchers.Default) { // this: CoroutineScope
   // Starts a coroutine inside the scope with CoroutineScope.launch()
   this.launch { greet() }
   println("The withContext() on the thread: ${Thread.currentThread().name}")
   }
   }
6. Combine these pieces to run multiple coroutines at the same time on a shared pool of threads:

   // Imports the coroutines library
   import kotlinx.coroutines.\*
   // Imports the kotlin.time.Duration to express duration in seconds
   import kotlin.time.Duration.Companion.seconds
   // Defines a suspending function
   suspend fun greet() {
   println("The greet() on the thread: ${Thread.currentThread().name}")
   // Suspends for 1 second and releases the thread
   delay(1.seconds)
   // The delay() function simulates a suspending API call here
   // You can add suspending API calls here like a network request
   }
   suspend fun main() {
   // Runs the code inside this block on a shared thread pool
   withContext(Dispatchers.Default) { // this: CoroutineScope
   this.launch() {
   greet()
   }
   // Starts another coroutine
   this.launch() {
   println("The CoroutineScope.launch() on the thread: ${Thread.currentThread().name}")
   delay(1.seconds)
   // The delay function simulates a suspending API call here
   // You can add suspending API calls here like a network request
   }
   println("The withContext() on the thread: ${Thread.currentThread().name}")
   }
   }

Try running the example multiple times. You may notice that the output order and thread names may change each time you run the program, because the OS decides when threads run.

## Coroutine scope and structured concurrency

When you run many coroutines in an application, you need a way to manage them as groups. Kotlin coroutines rely on a principle called structured concurrency to provide this structure.

According to this principle, coroutines form a tree hierarchy of parent and child tasks with linked lifecycles. A coroutine's lifecycle is the sequence of states from its creation until completion, failure, or cancellation.

A parent coroutine waits for its children to complete before it finishes. If the parent coroutine fails or gets canceled, all its child coroutines are recursively canceled too. Keeping coroutines connected this way makes cancellation and error handling predictable and safe.

To maintain structured concurrency, new coroutines can only be launched in a [`CoroutineScope`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/) that defines and manages their lifecycle. The `CoroutineScope` includes the coroutine context, which defines the dispatcher and other execution properties. When you start a coroutine inside another coroutine, it automatically becomes a child of its parent scope.

Calling a [coroutine builder function](#coroutine-builder-functions), such as `CoroutineScope.launch()` on a `CoroutineScope`, starts a child coroutine of the coroutine associated with that scope. Inside the builder's block, the [receiver](lambdas.html#function-literals-with-receiver) is a nested `CoroutineScope`, so any coroutines you launch there become its children.

### Create a coroutine scope with the `coroutineScope()` function

To create a new coroutine scope with the current coroutine context, use the [`coroutineScope()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html) function. This function creates a root coroutine of the coroutine subtree. It's the direct parent of coroutines launched inside the block and the indirect parent of any coroutines they launch. `coroutineScope()` executes the suspending block and waits until the block and any coroutines launched in it complete.

Here's an example:

// Imports the kotlin.time.Duration to express duration in seconds
import kotlin.time.Duration.Companion.seconds
import kotlinx.coroutines.\*
// If the coroutine context doesn't specify a dispatcher,
// CoroutineScope.launch() uses Dispatchers.Default
//sampleStart
suspend fun main() {
// Root of the coroutine subtree
coroutineScope { // this: CoroutineScope
this.launch {
this.launch {
delay(2.seconds)
println("Child of the enclosing coroutine completed")
}
println("Child coroutine 1 completed")
}
this.launch {
delay(1.seconds)
println("Child coroutine 2 completed")
}
}
// Runs only after all children in the coroutineScope have completed
println("Coroutine scope completed")
}
//sampleEnd

Since no [dispatcher](#coroutine-dispatchers) is specified in this example, the `CoroutineScope.launch()` builder functions in the `coroutineScope()` block inherit the current context. If that context doesn't have a specified dispatcher, `CoroutineScope.launch()` uses `Dispatchers.Default`, which runs on a shared pool of threads.

### Extract coroutine builders from the coroutine scope

In some cases, you may want to extract coroutine builder calls, such as [`CoroutineScope.launch()`](#coroutinescope-launch), into separate functions.

Consider the following example:

suspend fun main() {
coroutineScope { // this: CoroutineScope
// Calls CoroutineScope.launch() where CoroutineScope is the receiver
this.launch { println("1") }
this.launch { println("2") }
}
}

The `coroutineScope()` function takes a lambda with a `CoroutineScope` receiver. Inside this lambda, the implicit receiver is a `CoroutineScope`, so builder functions like `CoroutineScope.launch()` and [`CoroutineScope.async()`](#coroutinescope-async) resolve as [extension functions](extensions.html#extension-functions) on that receiver.

To extract the coroutine builders into another function, that function must declare a `CoroutineScope` receiver, otherwise a compilation error occurs:

import kotlinx.coroutines.\*
//sampleStart
suspend fun main() {
coroutineScope {
launchAll()
}
}
fun CoroutineScope.launchAll() { // this: CoroutineScope
// Calls .launch() on CoroutineScope
this.launch { println("1") }
this.launch { println("2") }
}
//sampleEnd
/\* -- Calling launch without declaring CoroutineScope as the receiver results in a compilation error --
fun launchAll() {
// Compilation error: this is not defined
this.launch { println("1") }
this.launch { println("2") }
}
\*/

## Coroutine builder functions

A coroutine builder function is a function that accepts a `suspend` [lambda](lambdas.html) that defines a coroutine to run. Here are some examples:

* [`CoroutineScope.launch()`](#coroutinescope-launch)
* [`CoroutineScope.async()`](#coroutinescope-async)
* [`runBlocking()`](#runblocking)
* [`withContext()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html)
* [`coroutineScope()`](#create-a-coroutine-scope-with-the-coroutinescope-function)

Coroutine builder functions require a `CoroutineScope` to run in. This can be an existing scope or one you create with helper functions such as `coroutineScope()`, [`runBlocking()`](#runblocking), or [`withContext()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html#). Each builder defines how the coroutine starts and how you interact with its result.

### `CoroutineScope.launch()`

The [`CoroutineScope.launch()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html#) coroutine builder function is an extension function on `CoroutineScope`. It starts a new coroutine without blocking the rest of the scope, inside an existing [coroutine scope](#coroutine-scope-and-structured-concurrency).

Use `CoroutineScope.launch()` to run a task alongside other work when the result isn't needed or you don't want to wait for it:

// Imports the kotlin.time.Duration to enable expressing duration in milliseconds
import kotlin.time.Duration.Companion.milliseconds
import kotlinx.coroutines.\*
suspend fun main() {
withContext(Dispatchers.Default) {
performBackgroundWork()
}
}
//sampleStart
suspend fun performBackgroundWork() = coroutineScope { // this: CoroutineScope
// Starts a coroutine that runs without blocking the scope
this.launch {
// Suspends to simulate background work
delay(100.milliseconds)
println("Sending notification in background")
}
// Main coroutine continues while a previous one suspends
println("Scope continues")
}
//sampleEnd

After running this example, you can see that the `main()` function isn't blocked by `CoroutineScope.launch()` and keeps running other code while the coroutine works in the background.

### `CoroutineScope.async()`

The [`CoroutineScope.async()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) coroutine builder function is an extension function on `CoroutineScope`. It starts a concurrent computation inside an existing [coroutine scope](#coroutine-scope-and-structured-concurrency) and returns a [`Deferred`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/) handle that represents an eventual result. Use the `.await()` function to suspend the code until the result is ready:

// Imports the kotlin.time.Duration to enable expressing duration in milliseconds
import kotlin.time.Duration.Companion.milliseconds
import kotlinx.coroutines.\*
//sampleStart
suspend fun main() = withContext(Dispatchers.Default) { // this: CoroutineScope
// Starts downloading the first page
val firstPage = this.async {
delay(50.milliseconds)
"First page"
}
// Starts downloading the second page in parallel
val secondPage = this.async {
delay(100.milliseconds)
"Second page"
}
// Awaits both results and compares them
val pagesAreEqual = firstPage.await() == secondPage.await()
println("Pages are equal: $pagesAreEqual")
}
//sampleEnd

### `runBlocking()`

The [`runBlocking()`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html) coroutine builder function creates a coroutine scope and blocks the current [thread](#comparing-coroutines-and-jvm-threads) until the coroutines launched in that scope finish.

Use `runBlocking()` only when there is no other option to call suspending code from non-suspending code:

import kotlin.time.Duration.Companion.milliseconds
import kotlinx.coroutines.\*
// A third-party interface you can't change
interface Repository {
fun readItem(): Int
}
object MyRepository : Repository {
override fun readItem(): Int {
// Bridges to a suspending function
return runBlocking {
myReadItem()
}
}
}
suspend fun myReadItem(): Int {
delay(100.milliseconds)
return 4
}

## Coroutine dispatchers

A [coroutine dispatcher](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/#) controls which thread or thread pool coroutines use for their execution. Coroutines aren't always tied to a single thread. They can pause on one thread and resume on another, depending on the dispatcher. This lets you run many coroutines at the same time without allocating a separate thread for every coroutine.

A dispatcher works together with the [coroutine scope](#coroutine-scope-and-structured-concurrency) to define when coroutines run and where they run. While the coroutine scope controls the coroutine's lifecycle, the dispatcher controls which threads are used for execution.

The `kotlinx.coroutines` library includes different dispatchers for different use cases. For example, [`Dispatchers.Default`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html) runs coroutines on a shared pool of threads, performing work in the background, separate from the main thread. This makes it an ideal choice for CPU-intensive operations like data processing.

To specify a dispatcher for a coroutine builder like `CoroutineScope.launch()`, pass it as an argument:

suspend fun runWithDispatcher() = coroutineScope { // this: CoroutineScope
this.launch(Dispatchers.Default) {
println("Running on ${Thread.currentThread().name}")
}
}

Alternatively, you can use a `withContext()` block to run all code in it on a specified dispatcher:

// Imports the kotlin.time.Duration to enable expressing duration in milliseconds
import kotlin.time.Duration.Companion.milliseconds
import kotlinx.coroutines.\*
//sampleStart
suspend fun main() = withContext(Dispatchers.Default) { // this: CoroutineScope
println("Running withContext block on ${Thread.currentThread().name}")
val one = this.async {
println("First calculation starting on ${Thread.currentThread().name}")
val sum = (1L..500\_000L).sum()
delay(200L)
println("First calculation done on ${Thread.currentThread().name}")
sum
}
val two = this.async {
println("Second calculation starting on ${Thread.currentThread().name}")
val sum = (500\_001L..1\_000\_000L).sum()
println("Second calculation done on ${Thread.currentThread().name}")
sum
}
// Waits for both calculations and prints the result
println("Combined total: ${one.await() + two.await()}")
}
//sampleEnd

To learn more about coroutine dispatchers and their uses, including other dispatchers like [`Dispatchers.IO`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-i-o.html) and [`Dispatchers.Main`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-main.html), see [Coroutine context and dispatchers](coroutine-context-and-dispatchers.html).

## Comparing coroutines and JVM threads

While coroutines are suspendable computations that run code concurrently like threads on the JVM, they work differently under the hood.

A thread is managed by the operating system. Threads can run tasks in parallel on multiple CPU cores and represent a standard approach to concurrency on the JVM. When you create a thread, the operating system allocates memory for its stack and uses the kernel to switch between threads. This makes threads powerful but also resource-intensive. Each thread usually needs a few megabytes of memory, and typically the JVM can only handle a few thousand threads at once.

On the other hand, a coroutine isn't bound to a specific thread. It can suspend on one thread and resume on another, so many coroutines can share the same thread pool. When a coroutine suspends, the thread isn't blocked and remains free to run other tasks. This makes coroutines much lighter than threads and allows running millions of them in one process without exhausting system resources.

Let's look at an example where 50,000 coroutines each wait five seconds and then print a period (`.`):

import kotlin.time.Duration.Companion.seconds
import kotlinx.coroutines.\*
suspend fun main() {
withContext(Dispatchers.Default) {
// Launches 50,000 coroutines that each wait five seconds, then print a period
printPeriods()
}
}
//sampleStart
suspend fun printPeriods() = coroutineScope { // this: CoroutineScope
// Launches 50,000 coroutines that each wait five seconds, then print a period
repeat(50\_000) {
this.launch {
delay(5.seconds)
print(".")
}
}
}
//sampleEnd

Now let's look at the same example using JVM threads:

import kotlin.concurrent.thread
fun main() {
repeat(50\_000) {
thread {
Thread.sleep(5000L)
print(".")
}
}
}

Running this version uses much more memory because each thread needs its own memory stack. For 50,000 threads, that can be up to 100 GB, compared to roughly 500 MB for the same number of coroutines.

Depending on your operating system, JDK version, and settings, the JVM thread version may throw an out-of-memory error or slow down thread creation to avoid running too many threads at once.

## What's next

* Discover more about combining suspending functions in [Composing suspending functions](composing-suspending-functions.html).
* Learn how to cancel coroutines and handle timeouts in [Cancellation and timeouts](cancellation-and-timeouts.html).
* Dive deeper into coroutine execution and thread management in [Coroutine context and dispatchers](coroutine-context-and-dispatchers.html).
* Learn how to return multiple asynchronously computed values in [Asynchronous flows](flow.html).

12 December 2025

---

## Bibliography

1. [Coroutines](https://kotlinlang.org/docs/coroutines-overview.html)
2. [Coroutine exceptions handling](https://kotlinlang.org/docs/exception-handling.html)
3. [Composing suspending functions](https://kotlinlang.org/docs/composing-suspending-functions.html)
4. [Coroutine context and dispatchers](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html)
5. [Cancellation and timeouts](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
6. [Coroutines basics](https://kotlinlang.org/docs/coroutines-basics.html)