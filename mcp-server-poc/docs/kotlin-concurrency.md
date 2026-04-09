(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Shared mutable state and concurrency | Kotlin Documentation[{"id":"the-problem","level":0,"title":"The problem","anchor":"#the-problem"},{"id":"volatiles-are-of-no-help","level":0,"title":"Volatiles are of no help","anchor":"#volatiles-are-of-no-help"},{"id":"thread-safe-data-structures","level":0,"title":"Thread-safe data structures","anchor":"#thread-safe-data-structures"},{"id":"thread-confinement-fine-grained","level":0,"title":"Thread confinement fine-grained","anchor":"#thread-confinement-fine-grained"},{"id":"thread-confinement-coarse-grained","level":0,"title":"Thread confinement coarse-grained","anchor":"#thread-confinement-coarse-grained"},{"id":"mutual-exclusion","level":0,"title":"Mutual exclusion","anchor":"#mutual-exclusion"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html#webpage",
"url": "https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html",
"name": "Shared mutable state and concurrency | Kotlin",
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

# Shared mutable state and concurrency

Coroutines can be executed parallelly using a multi-threaded dispatcher like the [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html). It presents all the usual parallelism problems. The main problem being synchronization of access to shared mutable state. Some solutions to this problem in the land of coroutines are similar to the solutions in the multi-threaded world, but others are unique.

## The problem

Let us launch a hundred coroutines all doing the same action a thousand times. We'll also measure their completion time for further comparisons:

suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}

We start with a very simple action that increments a shared mutable variable using multi-threaded [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html).

import kotlinx.coroutines.\*
import kotlin.system.\*
suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}
//sampleStart
var counter = 0
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
counter++
}
}
println("Counter = $counter")
}
//sampleEnd

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-sync-01.kt).

What does it print at the end? It is highly unlikely to ever print "Counter = 100000", because a hundred coroutines increment the `counter` concurrently from multiple threads without any synchronization.

## Volatiles are of no help

There is a common misconception that making a variable `volatile` solves concurrency problem. Let us try it:

import kotlinx.coroutines.\*
import kotlin.system.\*
suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}
//sampleStart
@Volatile // in Kotlin `volatile` is an annotation
var counter = 0
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
counter++
}
}
println("Counter = $counter")
}
//sampleEnd

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-sync-02.kt).

This code works slower, but we still don't always get "Counter = 100000" at the end, because volatile variables guarantee linearizable (this is a technical term for "atomic") reads and writes to the corresponding variable, but do not provide atomicity of larger actions (increment in our case).

## Thread-safe data structures

The general solution that works both for threads and for coroutines is to use a thread-safe (aka synchronized, linearizable, or atomic) data structure that provides all the necessary synchronization for the corresponding operations that needs to be performed on a shared state. In the case of a simple counter we can use `AtomicInteger` class which has atomic `incrementAndGet` operations:

import kotlinx.coroutines.\*
import java.util.concurrent.atomic.\*
import kotlin.system.\*
suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}
//sampleStart
val counter = AtomicInteger()
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
counter.incrementAndGet()
}
}
println("Counter = $counter")
}
//sampleEnd

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-sync-03.kt).

This is the fastest solution for this particular problem. It works for plain counters, collections, queues and other standard data structures and basic operations on them. However, it does not easily scale to complex state or to complex operations that do not have ready-to-use thread-safe implementations.

## Thread confinement fine-grained

Thread confinement is an approach to the problem of shared mutable state where all access to the particular shared state is confined to a single thread. It is typically used in UI applications, where all UI state is confined to the single event-dispatch/application thread. It is easy to apply with coroutines by using a single-threaded context.

import kotlinx.coroutines.\*
import kotlin.system.\*
suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}
//sampleStart
val counterContext = newSingleThreadContext("CounterContext")
var counter = 0
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
// confine each increment to a single-threaded context
withContext(counterContext) {
counter++
}
}
}
println("Counter = $counter")
}
//sampleEnd

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-sync-04.kt).

This code works very slowly, because it does fine-grained thread-confinement. Each individual increment switches from multi-threaded [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html) context to the single-threaded context using [withContext(counterContext)](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html) block.

## Thread confinement coarse-grained

In practice, thread confinement is performed in large chunks, e.g. big pieces of state-updating business logic are confined to the single thread. The following example does it like that, running each coroutine in the single-threaded context to start with.

import kotlinx.coroutines.\*
import kotlin.system.\*
suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}
//sampleStart
val counterContext = newSingleThreadContext("CounterContext")
var counter = 0
fun main() = runBlocking {
// confine everything to a single-threaded context
withContext(counterContext) {
massiveRun {
counter++
}
}
println("Counter = $counter")
}
//sampleEnd

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-sync-05.kt).

This now works much faster and produces correct result.

## Mutual exclusion

Mutual exclusion solution to the problem is to protect all modifications of the shared state with a critical section that is never executed concurrently. In a blocking world you'd typically use `synchronized` or `ReentrantLock` for that. Coroutine's alternative is called [Mutex](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/-mutex/index.html). It has [lock](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/-mutex/lock.html) and [unlock](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/-mutex/unlock.html) functions to delimit a critical section. The key difference is that `Mutex.lock()` is a suspending function. It does not block a thread.

There is also [withLock](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.sync/with-lock.html) extension function that conveniently represents `mutex.lock(); try { ... } finally { mutex.unlock() }` pattern:

import kotlinx.coroutines.\*
import kotlinx.coroutines.sync.\*
import kotlin.system.\*
suspend fun massiveRun(action: suspend () -> Unit) {
val n = 100 // number of coroutines to launch
val k = 1000 // times an action is repeated by each coroutine
val time = measureTimeMillis {
coroutineScope { // scope for coroutines
repeat(n) {
launch {
repeat(k) { action() }
}
}
}
}
println("Completed ${n \* k} actions in $time ms")
}
//sampleStart
val mutex = Mutex()
var counter = 0
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
// protect each increment with lock
mutex.withLock {
counter++
}
}
}
println("Counter = $counter")
}
//sampleEnd

You can get the full code [here](https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-core/jvm/test/guide/example-sync-06.kt).

The locking in this example is fine-grained, so it pays the price. However, it is a good choice for some situations where you absolutely must modify some shared state periodically, but there is no natural thread that this state is confined to.

27 September 2024

[Coroutine exceptions handling](exception-handling.html)[Select expression (experimental)](select-expression.html)