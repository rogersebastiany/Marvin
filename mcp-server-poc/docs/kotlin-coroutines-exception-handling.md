(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Coroutine exceptions handling | Kotlin Documentation[{"id":"exception-propagation","level":0,"title":"Exception propagation","anchor":"#exception-propagation"},{"id":"coroutineexceptionhandler","level":0,"title":"CoroutineExceptionHandler","anchor":"#coroutineexceptionhandler"},{"id":"cancellation-and-exceptions","level":0,"title":"Cancellation and exceptions","anchor":"#cancellation-and-exceptions"},{"id":"exceptions-aggregation","level":0,"title":"Exceptions aggregation","anchor":"#exceptions-aggregation"},{"id":"supervision","level":0,"title":"Supervision","anchor":"#supervision"},{"id":"supervision-job","level":1,"title":"Supervision job","anchor":"#supervision-job"},{"id":"supervision-scope","level":1,"title":"Supervision scope","anchor":"#supervision-scope"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/exception-handling.html#webpage",
"url": "https://kotlinlang.org/docs/exception-handling.html",
"name": "Coroutine exceptions handling | Kotlin",
"description": "",
"image": "https://kotlinlang.org/assets/images/open-graph/docs.png",
"inLanguage":"en-US"
}{
"@type": "WebSite",
"@id": "https://kotlinlang.org/docs/#website",
"url": "https://kotlinlang.org/docs/",
"name": "Kotlin Help"
}a[href="test-page.html"] { visibility: hidden; }

### Kotlin Help

# Coroutine exceptions handling

This section covers exception handling and cancellation on exceptions. We already know that a cancelled coroutine throws [CancellationException](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/index.html) in suspension points and that it is ignored by the coroutines' machinery. Here we look at what happens if an exception is thrown during cancellation or multiple children of the same coroutine throw an exception.

## Exception propagation

Coroutine builders come in two flavors: propagating exceptions automatically ([launch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html)) or exposing them to users ([async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) and [produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html)). When these builders are used to create a root coroutine, that is not a child of another coroutine, the former builders treat exceptions as uncaught exceptions, similar to Java's `Thread.uncaughtExceptionHandler`, while the latter are relying on the user to consume the final exception, for example via [await](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/await.html) or [receive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/receive.html) ([produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html) and [receive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/receive.html) are covered in [Channels](https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/channels.md) section).

It can be demonstrated by a simple example that creates root coroutines using the [GlobalScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/index.html):

[GlobalScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/index.html) is a delicate API that can backfire in non-trivial ways. Creating a root coroutine for the whole application is one of the rare legitimate uses for `GlobalScope`, so you must explicitly opt-in into using `GlobalScope` with `@OptIn(DelicateCoroutinesApi::class)`.

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-exceptions-01.kt).

The output of this code is (with [debug](https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/coroutine-context-and-dispatchers.md#debugging-coroutines-and-threads)):

Throwing exception from launch
Exception in thread "DefaultDispatcher-worker-1 @coroutine#2" java.lang.IndexOutOfBoundsException
Joined failed job
Throwing exception from async
Caught ArithmeticException

## CoroutineExceptionHandler

It is possible to customize the default behavior of printing uncaught exceptions to the console. [CoroutineExceptionHandler](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/index.html) context element on a root coroutine can be used as a generic `catch` block for this root coroutine and all its children where custom exception handling may take place. It is similar to [`Thread.uncaughtExceptionHandler`](https://docs.oracle.com/javase/8/docs/api/java/lang/Thread.html#setUncaughtExceptionHandler-java.lang.Thread.UncaughtExceptionHandler-). You cannot recover from the exception in the `CoroutineExceptionHandler`. The coroutine had already completed with the corresponding exception when the handler is called. Normally, the handler is used to log the exception, show some kind of error message, terminate, and/or restart the application.

`CoroutineExceptionHandler` is invoked only on uncaught exceptions — exceptions that were not handled in any other way. In particular, all children coroutines (coroutines created in the context of another [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html)) delegate handling of their exceptions to their parent coroutine, which also delegates to the parent, and so on until the root, so the `CoroutineExceptionHandler` installed in their context is never used. In addition to that, [async](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html) builder always catches all exceptions and represents them in the resulting [Deferred](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/index.html) object, so its `CoroutineExceptionHandler` has no effect either.

Coroutines running in supervision scope do not propagate exceptions to their parent and are excluded from this rule. A further [Supervision](#supervision) section of this document gives more details.

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-exceptions-02.kt).

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-exceptions-03.kt).

The output of this code is:

Cancelling child
Child is cancelled
Parent is not cancelled

If a coroutine encounters an exception other than `CancellationException`, it cancels its parent with that exception. This behaviour cannot be overridden and is used to provide stable coroutines hierarchies for [structured concurrency](https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/composing-suspending-functions.md#structured-concurrency-with-async). [CoroutineExceptionHandler](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/index.html) implementation is not used for child coroutines.

In these examples, [CoroutineExceptionHandler](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/index.html) is always installed to a coroutine that is created in [GlobalScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/index.html). It does not make sense to install an exception handler to a coroutine that is launched in the scope of the main [runBlocking](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html), since the main coroutine is going to be always cancelled when its child completes with exception despite the installed handler.

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-exceptions-04.kt).

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-exceptions-05.kt).

The output of this code is:

CoroutineExceptionHandler got java.io.IOException with suppressed [java.lang.ArithmeticException]

Note that this mechanism currently only works on Java version 1.7+. The JS and Native restrictions are temporary and will be lifted in the future.

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-exceptions-06.kt).

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-supervision-01.kt).

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-supervision-02.kt).

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

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-supervision-03.kt).

The output of this code is:

The scope is completing
The child throws an exception
CoroutineExceptionHandler got java.lang.AssertionError
The scope is completed

27 September 2024

[Channels](channels.html)[Shared mutable state and concurrency](shared-mutable-state-and-concurrency.html)