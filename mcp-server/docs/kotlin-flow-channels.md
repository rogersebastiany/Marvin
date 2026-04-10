# Kotlin Flow and Channels


---

## 1. Shared mutable state and concurrency

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
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
counter++
}
}
println("Counter = $counter")
}
//sampleEnd

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
fun main() = runBlocking {
withContext(Dispatchers.Default) {
massiveRun {
counter++
}
}
println("Counter = $counter")
}
//sampleEnd

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

The locking in this example is fine-grained, so it pays the price. However, it is a good choice for some situations where you absolutely must modify some shared state periodically, but there is no natural thread that this state is confined to.

27 September 2024

---

## 2. Channels

Deferred values provide a convenient way to transfer a single value between coroutines. Channels provide a way to transfer a stream of values.

## Channel basics

A [Channel](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel/index.html) is conceptually very similar to `BlockingQueue`. One key difference is that instead of a blocking `put` operation it has a suspending [send](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-send-channel/send.html), and instead of a blocking `take` operation it has a suspending [receive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/receive.html).

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking {
//sampleStart
val channel = Channel<Int>()
launch {
// this might be heavy CPU-consuming computation or async logic,
// we'll just send five squares
for (x in 1..5) channel.send(x \* x)
}
// here we print five received integers:
repeat(5) { println(channel.receive()) }
println("Done!")
//sampleEnd
}

The output of this code is:

1
4
9
16
25
Done!

## Closing and iteration over channels

Unlike a queue, a channel can be closed to indicate that no more elements are coming. On the receiver side it is convenient to use a regular `for` loop to receive elements from the channel.

Conceptually, a [close](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-send-channel/close.html) is like sending a special close token to the channel. The iteration stops as soon as this close token is received, so there is a guarantee that all previously sent elements before the close are received:

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking {
//sampleStart
val channel = Channel<Int>()
launch {
for (x in 1..5) channel.send(x \* x)
channel.close() // we're done sending
}
// here we print received values using `for` loop (until the channel is closed)
for (y in channel) println(y)
println("Done!")
//sampleEnd
}

## Building channel producers

The pattern where a coroutine is producing a sequence of elements is quite common. This is a part of producer-consumer pattern that is often found in concurrent code. You could abstract such a producer into a function that takes channel as its parameter, but this goes contrary to common sense that results must be returned from functions.

There is a convenient coroutine builder named [produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html) that makes it easy to do it right on producer side, and an extension function [consumeEach](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/consume-each.html), that replaces a `for` loop on the consumer side:

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
//sampleStart
fun CoroutineScope.produceSquares(): ReceiveChannel<Int> = produce {
for (x in 1..5) send(x \* x)
}
fun main() = runBlocking {
val squares = produceSquares()
squares.consumeEach { println(it) }
println("Done!")
//sampleEnd
}

## Pipelines

A pipeline is a pattern where one coroutine is producing, possibly infinite, stream of values:

fun CoroutineScope.produceNumbers() = produce<Int> {
while (true) send(x++) // infinite stream of integers starting from 1
}

And another coroutine or coroutines are consuming that stream, doing some processing, and producing some other results. In the example below, the numbers are just squared:

fun CoroutineScope.square(numbers: ReceiveChannel<Int>): ReceiveChannel<Int> = produce {
for (x in numbers) send(x \* x)
}

The main code starts and connects the whole pipeline:

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking {
//sampleStart
val numbers = produceNumbers() // produces integers from 1 and on
val squares = square(numbers) // squares integers
repeat(5) {
println(squares.receive()) // print first five
}
println("Done!") // we are done
coroutineContext.cancelChildren() // cancel children coroutines
//sampleEnd
}
fun CoroutineScope.produceNumbers() = produce<Int> {
while (true) send(x++) // infinite stream of integers starting from 1
}
fun CoroutineScope.square(numbers: ReceiveChannel<Int>): ReceiveChannel<Int> = produce {
for (x in numbers) send(x \* x)
}

## Prime numbers with pipeline

Let's take pipelines to the extreme with an example that generates prime numbers using a pipeline of coroutines. We start with an infinite sequence of numbers.

fun CoroutineScope.numbersFrom(start: Int) = produce<Int> {
while (true) send(x++) // infinite stream of integers from start
}

The following pipeline stage filters an incoming stream of numbers, removing all the numbers that are divisible by the given prime number:

fun CoroutineScope.filter(numbers: ReceiveChannel<Int>, prime: Int) = produce<Int> {
for (x in numbers) if (x % prime != 0) send(x)
}

Now we build our pipeline by starting a stream of numbers from 2, taking a prime number from the current channel, and launching new pipeline stage for each prime number found:

numbersFrom(2) -> filter(2) -> filter(3) -> filter(5) -> filter(7) ...

The following example prints the first ten prime numbers, running the whole pipeline in the context of the main thread. Since all the coroutines are launched in the scope of the main [runBlocking](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html) coroutine we don't have to keep an explicit list of all the coroutines we have started. We use [cancelChildren](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/cancel-children.html) extension function to cancel all the children coroutines after we have printed the first ten prime numbers.

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking {
//sampleStart
repeat(10) {
val prime = cur.receive()
println(prime)
cur = filter(cur, prime)
}
coroutineContext.cancelChildren() // cancel all children to let main finish
//sampleEnd
}
fun CoroutineScope.numbersFrom(start: Int) = produce<Int> {
while (true) send(x++) // infinite stream of integers from start
}
fun CoroutineScope.filter(numbers: ReceiveChannel<Int>, prime: Int) = produce<Int> {
for (x in numbers) if (x % prime != 0) send(x)
}

The output of this code is:

2
3
5
7
11
13
17
19
23
29

Note that you can build the same pipeline using [`iterator`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.sequences/iterator.html) coroutine builder from the standard library. Replace `produce` with `iterator`, `send` with `yield`, `receive` with `next`, `ReceiveChannel` with `Iterator`, and get rid of the coroutine scope. You will not need `runBlocking` either. However, the benefit of a pipeline that uses channels as shown above is that it can actually use multiple CPU cores if you run it in [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html) context.

Anyway, this is an extremely impractical way to find prime numbers. In practice, pipelines do involve some other suspending invocations (like asynchronous calls to remote services) and these pipelines cannot be built using `sequence`/`iterator`, because they do not allow arbitrary suspension, unlike `produce`, which is fully asynchronous.

## Fan-out

Multiple coroutines may receive from the same channel, distributing work between themselves. Let us start with a producer coroutine that is periodically producing integers (ten numbers per second):

fun CoroutineScope.produceNumbers() = produce<Int> {
while (true) {
send(x++) // produce next
delay(100) // wait 0.1s
}
}

Then we can have several processor coroutines. In this example, they just print their id and received number:

fun CoroutineScope.launchProcessor(id: Int, channel: ReceiveChannel<Int>) = launch {
for (msg in channel) {
println("Processor #$id received $msg")
}
}

Now let us launch five processors and let them work for almost a second. See what happens:

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking<Unit> {
//sampleStart
val producer = produceNumbers()
repeat(5) { launchProcessor(it, producer) }
delay(950)
producer.cancel() // cancel producer coroutine and thus kill them all
//sampleEnd
}
fun CoroutineScope.produceNumbers() = produce<Int> {
while (true) {
send(x++) // produce next
delay(100) // wait 0.1s
}
}
fun CoroutineScope.launchProcessor(id: Int, channel: ReceiveChannel<Int>) = launch {
for (msg in channel) {
println("Processor #$id received $msg")
}
}

The output will be similar to the following one, albeit the processor ids that receive each specific integer may be different:

Processor #2 received 1
Processor #4 received 2
Processor #0 received 3
Processor #1 received 4
Processor #3 received 5
Processor #2 received 6
Processor #4 received 7
Processor #0 received 8
Processor #1 received 9
Processor #3 received 10

Note that cancelling a producer coroutine closes its channel, thus eventually terminating iteration over the channel that processor coroutines are doing.

Also, pay attention to how we explicitly iterate over channel with `for` loop to perform fan-out in `launchProcessor` code. Unlike `consumeEach`, this `for` loop pattern is perfectly safe to use from multiple coroutines. If one of the processor coroutines fails, then others would still be processing the channel, while a processor that is written via `consumeEach` always consumes (cancels) the underlying channel on its normal or abnormal completion.

## Fan-in

Multiple coroutines may send to the same channel. For example, let us have a channel of strings, and a suspending function that repeatedly sends a specified string to this channel with a specified delay:

suspend fun sendString(channel: SendChannel<String>, s: String, time: Long) {
while (true) {
delay(time)
channel.send(s)
}
}

Now, let us see what happens if we launch a couple of coroutines sending strings (in this example we launch them in the context of the main thread as main coroutine's children):

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking {
//sampleStart
val channel = Channel<String>()
launch { sendString(channel, "foo", 200L) }
launch { sendString(channel, "BAR!", 500L) }
repeat(6) { // receive first six
println(channel.receive())
}
coroutineContext.cancelChildren() // cancel all children to let main finish
//sampleEnd
}
suspend fun sendString(channel: SendChannel<String>, s: String, time: Long) {
while (true) {
delay(time)
channel.send(s)
}
}

The output is:

foo
foo
BAR!
foo
foo
BAR!

## Buffered channels

The channels shown so far had no buffer. Unbuffered channels transfer elements when sender and receiver meet each other (aka rendezvous). If send is invoked first, then it is suspended until receive is invoked, if receive is invoked first, it is suspended until send is invoked.

Both [Channel()](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel.html) factory function and [produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html) builder take an optional `capacity` parameter to specify buffer size. Buffer allows senders to send multiple elements before suspending, similar to the `BlockingQueue` with a specified capacity, which blocks when buffer is full.

Take a look at the behavior of the following code:

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
fun main() = runBlocking<Unit> {
//sampleStart
val channel = Channel<Int>(4) // create buffered channel
val sender = launch { // launch sender coroutine
repeat(10) {
println("Sending $it") // print before sending each element
channel.send(it) // will suspend when buffer is full
}
}
// don't receive anything... just wait....
delay(1000)
sender.cancel() // cancel sender coroutine
//sampleEnd
}

It prints "sending" five times using a buffered channel with capacity of four:

Sending 0
Sending 1
Sending 2
Sending 3
Sending 4

The first four elements are added to the buffer and the sender suspends when trying to send the fifth one.

## Channels are fair

Send and receive operations to channels are fair with respect to the order of their invocation from multiple coroutines. They are served in first-in first-out order, e.g. the first coroutine to invoke `receive` gets the element. In the following example two coroutines "ping" and "pong" are receiving the "ball" object from the shared "table" channel.

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
//sampleStart
data class Ball(var hits: Int)
fun main() = runBlocking {
val table = Channel<Ball>() // a shared table
launch { player("ping", table) }
launch { player("pong", table) }
table.send(Ball(0)) // serve the ball
delay(1000) // delay 1 second
coroutineContext.cancelChildren() // game over, cancel them
}
suspend fun player(name: String, table: Channel<Ball>) {
for (ball in table) { // receive the ball in a loop
ball.hits++
println("$name $ball")
delay(300) // wait a bit
table.send(ball) // send the ball back
}
}
//sampleEnd

The "ping" coroutine is started first, so it is the first one to receive the ball. Even though "ping" coroutine immediately starts receiving the ball again after sending it back to the table, the ball gets received by the "pong" coroutine, because it was already waiting for it:

ping Ball(hits=1)
pong Ball(hits=2)
ping Ball(hits=3)
pong Ball(hits=4)

Note that sometimes channels may produce executions that look unfair due to the nature of the executor that is being used. See [this issue](https://github.com/Kotlin/kotlinx.coroutines/issues/111) for details.

## Ticker channels

Ticker channel is a special rendezvous channel that produces `Unit` every time given delay passes since last consumption from this channel. Though it may seem to be useless standalone, it is a useful building block to create complex time-based [produce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html) pipelines and operators that do windowing and other time-dependent processing. Ticker channel can be used in [select](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.selects/select.html) to perform "on tick" action.

To create such channel use a factory method [ticker](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/ticker.html). To indicate that no further elements are needed use [ReceiveChannel.cancel](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/cancel.html) method on it.

Now let's see how it works in practice:

import kotlinx.coroutines.\*
import kotlinx.coroutines.channels.\*
//sampleStart
fun main() = runBlocking<Unit> {
val tickerChannel = ticker(delayMillis = 200, initialDelayMillis = 0) // create a ticker channel
println("Initial element is available immediately: $nextElement") // no initial delay
nextElement = withTimeoutOrNull(100) { tickerChannel.receive() } // all subsequent elements have 200ms delay
println("Next element is not ready in 100 ms: $nextElement")
nextElement = withTimeoutOrNull(120) { tickerChannel.receive() }
println("Next element is ready in 200 ms: $nextElement")
// Emulate large consumption delays
println("Consumer pauses for 300ms")
delay(300)
// Next element is available immediately
nextElement = withTimeoutOrNull(1) { tickerChannel.receive() }
println("Next element is available immediately after large consumer delay: $nextElement")
// Note that the pause between `receive` calls is taken into account and next element arrives faster
nextElement = withTimeoutOrNull(120) { tickerChannel.receive() }
println("Next element is ready in 100ms after consumer pause in 300ms: $nextElement")
tickerChannel.cancel() // indicate that no more elements are needed
}
//sampleEnd

It prints following lines:

Initial element is available immediately: kotlin.Unit
Next element is not ready in 100 ms: null
Next element is ready in 200 ms: kotlin.Unit
Consumer pauses for 300ms
Next element is available immediately after large consumer delay: kotlin.Unit
Next element is ready in 100ms after consumer pause in 300ms: kotlin.Unit

Note that [ticker](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/ticker.html) is aware of possible consumer pauses and, by default, adjusts next produced element delay if a pause occurs, trying to maintain a fixed rate of produced elements.

Optionally, a `mode` parameter equal to [TickerMode.FIXED\_DELAY](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-ticker-mode/-f-i-x-e-d_-d-e-l-a-y/index.html) can be specified to maintain a fixed delay between elements.

27 September 2024

---

## 3. Asynchronous Flow

A suspending function asynchronously returns a single value, but how can we return multiple asynchronously computed values? This is where Kotlin Flows come in.

## Representing multiple values

Multiple values can be represented in Kotlin using [collections](/docs/reference/collections-overview.html). For example, we can have a `simple` function that returns a [List](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-list/) of three numbers and then print them all using [forEach](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/for-each.html):

fun simple(): List<Int> = listOf(1, 2, 3)
fun main() {
simple().forEach { value -> println(value) }
}

This code outputs:

1
2
3

### Sequences

If we are computing the numbers with some CPU-consuming blocking code (each computation taking 100ms), then we can represent the numbers using a [Sequence](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.sequences/):

fun simple(): Sequence<Int> = sequence { // sequence builder
for (i in 1..3) {
Thread.sleep(100) // pretend we are computing it
yield(i) // yield next value
}
}
fun main() {
simple().forEach { value -> println(value) }
}

This code outputs the same numbers, but it waits 100ms before printing each one.

### Suspending functions

However, this computation blocks the main thread that is running the code. When these values are computed by asynchronous code we can mark the `simple` function with a `suspend` modifier, so that it can perform its work without blocking and return the result as a list:

import kotlinx.coroutines.\*
//sampleStart
suspend fun simple(): List<Int> {
delay(1000) // pretend we are doing something asynchronous here
return listOf(1, 2, 3)
}
fun main() = runBlocking<Unit> {
simple().forEach { value -> println(value) }
}
//sampleEnd

This code prints the numbers after waiting for a second.

### Flows

Using the `List<Int>` result type, means we can only return all the values at once. To represent the stream of values that are being computed asynchronously, we can use a [`Flow<Int>`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/index.html) type just like we would use a `Sequence<Int>` type for synchronously computed values:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow { // flow builder
for (i in 1..3) {
delay(100) // pretend we are doing something useful here
emit(i) // emit next value
}
}
fun main() = runBlocking<Unit> {
// Launch a concurrent coroutine to check if the main thread is blocked
launch {
for (k in 1..3) {
println("I'm not blocked $k")
delay(100)
}
}
// Collect the flow
simple().collect { value -> println(value) }
}
//sampleEnd

This code waits 100ms before printing each number without blocking the main thread. This is verified by printing "I'm not blocked" every 100ms from a separate coroutine that is running in the main thread:

I'm not blocked 1
1
I'm not blocked 2
2
I'm not blocked 3
3

Notice the following differences in the code with the [Flow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/index.html) from the earlier examples:

* A builder function of [Flow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/index.html) type is called [flow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow.html).
* Code inside a `flow { ... }` builder block can suspend.
* The `simple` function is no longer marked with a `suspend` modifier.
* Values are emitted from the flow using an [emit](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow-collector/emit.html) function.
* Values are collected from the flow using a [collect](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect.html) function.

## Flows are cold

Flows are cold streams similar to sequences — the code inside a [flow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow.html) builder does not run until the flow is collected. This becomes clear in the following example:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow {
println("Flow started")
for (i in 1..3) {
delay(100)
emit(i)
}
}
fun main() = runBlocking<Unit> {
println("Calling simple function...")
val flow = simple()
println("Calling collect...")
flow.collect { value -> println(value) }
println("Calling collect again...")
flow.collect { value -> println(value) }
}
//sampleEnd

Which prints:

Calling simple function...
Calling collect...
Flow started
1
2
3
Calling collect again...
Flow started
1
2
3

This is a key reason the `simple` function (which returns a flow) is not marked with `suspend` modifier. The `simple()` call itself returns quickly and does not wait for anything. The flow starts afresh every time it is collected and that is why we see "Flow started" every time we call `collect` again.

## Flow cancellation basics

Flows adhere to the general cooperative cancellation of coroutines. As usual, flow collection can be cancelled when the flow is suspended in a cancellable suspending function (like [delay](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/delay.html)). The following example shows how the flow gets cancelled on a timeout when running in a [withTimeoutOrNull](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-timeout-or-null.html) block and stops executing its code:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
delay(100)
println("Emitting $i")
emit(i)
}
}
fun main() = runBlocking<Unit> {
withTimeoutOrNull(250) { // Timeout after 250ms
simple().collect { value -> println(value) }
}
println("Done")
}
//sampleEnd

Notice how only two numbers get emitted by the flow in the `simple` function, producing the following output:

Emitting 1
1
Emitting 2
2
Done

See [Flow cancellation checks](#flow-cancellation-checks) section for more details.

## Flow builders

The `flow { ... }` builder from the previous examples is the most basic one. There are other builders that allow flows to be declared:

* The [flowOf](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow-of.html) builder defines a flow that emits a fixed set of values.
* Various collections and sequences can be converted to flows using the `.asFlow()` extension function.

For example, the snippet that prints the numbers 1 to 3 from a flow can be rewritten as follows:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun main() = runBlocking<Unit> {
//sampleStart
// Convert an integer range to a flow
(1..3).asFlow().collect { value -> println(value) }
//sampleEnd
}

## Intermediate flow operators

Flows can be transformed using operators, in the same way as you would transform collections and sequences. Intermediate operators are applied to an upstream flow and return a downstream flow. These operators are cold, just like flows are. A call to such an operator is not a suspending function itself. It works quickly, returning the definition of a new transformed flow.

The basic operators have familiar names like [map](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/map.html) and [filter](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/filter.html). An important difference of these operators from sequences is that blocks of code inside these operators can call suspending functions.

For example, a flow of incoming requests can be mapped to its results with a [map](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/map.html) operator, even when performing a request is a long-running operation that is implemented by a suspending function:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
suspend fun performRequest(request: Int): String {
delay(1000) // imitate long-running asynchronous work
return "response $request"
}
fun main() = runBlocking<Unit> {
(1..3).asFlow() // a flow of requests
.map { request -> performRequest(request) }
.collect { response -> println(response) }
}
//sampleEnd

It produces the following three lines, each appearing one second after the previous:

response 1
response 2
response 3

### Transform operator

Among the flow transformation operators, the most general one is called [transform](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/transform.html). It can be used to imitate simple transformations like [map](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/map.html) and [filter](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/filter.html), as well as implement more complex transformations. Using the `transform` operator, we can [emit](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow-collector/emit.html) arbitrary values an arbitrary number of times.

For example, using `transform` we can emit a string before performing a long-running asynchronous request and follow it with a response:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
suspend fun performRequest(request: Int): String {
delay(1000) // imitate long-running asynchronous work
return "response $request"
}
fun main() = runBlocking<Unit> {
//sampleStart
(1..3).asFlow() // a flow of requests
.transform { request ->
emit("Making request $request")
emit(performRequest(request))
}
.collect { response -> println(response) }
//sampleEnd
}

The output of this code is:

Making request 1
response 1
Making request 2
response 2
Making request 3
response 3

### Size-limiting operators

Size-limiting intermediate operators like [take](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/take.html) cancel the execution of the flow when the corresponding limit is reached. Cancellation in coroutines is always performed by throwing an exception, so that all the resource-management functions (like `try { ... } finally { ... }` blocks) operate normally in case of cancellation:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun numbers(): Flow<Int> = flow {
try {
emit(1)
emit(2)
println("This line will not execute")
emit(3)
} finally {
println("Finally in numbers")
}
}
fun main() = runBlocking<Unit> {
numbers()
.take(2) // take only the first two
.collect { value -> println(value) }
}
//sampleEnd

The output of this code clearly shows that the execution of the `flow { ... }` body in the `numbers()` function stopped after emitting the second number:

1
2
Finally in numbers

## Terminal flow operators

Terminal operators on flows are suspending functions that start a collection of the flow. The [collect](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect.html) operator is the most basic one, but there are other terminal operators, which can make it easier:

* Conversion to various collections like [toList](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/to-list.html) and [toSet](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/to-set.html).
* Operators to get the [first](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/first.html) value and to ensure that a flow emits a [single](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/single.html) value.
* Reducing a flow to a value with [reduce](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/reduce.html) and [fold](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/fold.html).

For example:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun main() = runBlocking<Unit> {
//sampleStart
val sum = (1..5).asFlow()
.map { it \* it } // squares of numbers from 1 to 5
.reduce { a, b -> a + b } // sum them (terminal operator)
println(sum)
//sampleEnd
}

Prints a single number:

55

## Flows are sequential

Each individual collection of a flow is performed sequentially unless special operators that operate on multiple flows are used. The collection works directly in the coroutine that calls a terminal operator. No new coroutines are launched by default. Each emitted value is processed by all the intermediate operators from upstream to downstream and is then delivered to the terminal operator after.

See the following example that filters the even integers and maps them to strings:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun main() = runBlocking<Unit> {
//sampleStart
(1..5).asFlow()
.filter {
println("Filter $it")
it % 2 == 0
}
.map {
println("Map $it")
"string $it"
}.collect {
println("Collect $it")
}
//sampleEnd
}

Producing:

Filter 1
Filter 2
Map 2
Collect string 2
Filter 3
Filter 4
Map 4
Collect string 4
Filter 5

## Flow context

Collection of a flow always happens in the context of the calling coroutine. For example, if there is a `simple` flow, then the following code runs in the context specified by the author of this code, regardless of the implementation details of the `simple` flow:

withContext(context) {
simple().collect { value ->
println(value) // run in the specified context
}
}

This property of a flow is called context preservation.

So, by default, code in the `flow { ... }` builder runs in the context that is provided by a collector of the corresponding flow. For example, consider the implementation of a `simple` function that prints the thread it is called on and emits three numbers:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
//sampleStart
fun simple(): Flow<Int> = flow {
log("Started simple flow")
for (i in 1..3) {
emit(i)
}
}
fun main() = runBlocking<Unit> {
simple().collect { value -> log("Collected $value") }
}
//sampleEnd

Running this code produces:

[main @coroutine#1] Started simple flow
[main @coroutine#1] Collected 1
[main @coroutine#1] Collected 2
[main @coroutine#1] Collected 3

Since `simple().collect` is called from the main thread, the body of `simple`'s flow is also called in the main thread. This is the perfect default for fast-running or asynchronous code that does not care about the execution context and does not block the caller.

### A common pitfall when using withContext

However, the long-running CPU-consuming code might need to be executed in the context of [Dispatchers.Default](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-default.html) and UI-updating code might need to be executed in the context of [Dispatchers.Main](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/-main.html). Usually, [withContext](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html) is used to change the context in the code using Kotlin coroutines, but code in the `flow { ... }` builder has to honor the context preservation property and is not allowed to [emit](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow-collector/emit.html) from a different context.

Try running the following code:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow {
// The WRONG way to change context for CPU-consuming code in flow builder
kotlinx.coroutines.withContext(Dispatchers.Default) {
for (i in 1..3) {
Thread.sleep(100) // pretend we are computing it in CPU-consuming way
emit(i) // emit next value
}
}
}
fun main() = runBlocking<Unit> {
simple().collect { value -> println(value) }
}
//sampleEnd

This code produces the following exception:

Exception in thread "main" java.lang.IllegalStateException: Flow invariant is violated:
Flow was collected in [CoroutineId(1), "coroutine#1":BlockingCoroutine{Active}@5511c7f8, BlockingEventLoop@2eac3323],
but emission happened in [CoroutineId(1), "coroutine#1":DispatchedCoroutine{Active}@2dae0000, Dispatchers.Default].
Please refer to 'flow' documentation or use 'flowOn' instead
at ...

### flowOn operator

The exception refers to the [flowOn](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow-on.html) function that shall be used to change the context of the flow emission. The correct way to change the context of a flow is shown in the example below, which also prints the names of the corresponding threads to show how it all works:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun log(msg: String) = println("[${Thread.currentThread().name}] $msg")
//sampleStart
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
Thread.sleep(100) // pretend we are computing it in CPU-consuming way
log("Emitting $i")
emit(i) // emit next value
}
}.flowOn(Dispatchers.Default) // RIGHT way to change context for CPU-consuming code in flow builder
fun main() = runBlocking<Unit> {
simple().collect { value ->
log("Collected $value")
}
}
//sampleEnd

Notice how `flow { ... }` works in the background thread, while collection happens in the main thread:

[DefaultDispatcher-worker-1 @coroutine#2] Emitting 1
[main @coroutine#1] Collected 1
[DefaultDispatcher-worker-1 @coroutine#2] Emitting 2
[main @coroutine#1] Collected 2
[DefaultDispatcher-worker-1 @coroutine#2] Emitting 3
[main @coroutine#1] Collected 3

Another thing to observe here is that the [flowOn](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow-on.html) operator has changed the default sequential nature of the flow. Now collection happens in one coroutine ("coroutine#1") and emission happens in another coroutine ("coroutine#2") that is running in another thread concurrently with the collecting coroutine. The [flowOn](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow-on.html) operator creates another coroutine for an upstream flow when it has to change the [CoroutineDispatcher](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/index.html) in its context.

## Buffering

Running different parts of a flow in different coroutines can be helpful from the standpoint of the overall time it takes to collect the flow, especially when long-running asynchronous operations are involved. For example, consider a case when the emission by a `simple` flow is slow, taking 100 ms to produce an element; and collector is also slow, taking 300 ms to process an element. Let's see how long it takes to collect such a flow with three numbers:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
import kotlin.system.\*
//sampleStart
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
delay(100) // pretend we are asynchronously waiting 100 ms
emit(i) // emit next value
}
}
fun main() = runBlocking<Unit> {
val time = measureTimeMillis {
simple().collect { value ->
delay(300) // pretend we are processing it for 300 ms
println(value)
}
}
println("Collected in $time ms")
}
//sampleEnd

It produces something like this, with the whole collection taking around 1200 ms (three numbers, 400 ms for each):

1
2
3
Collected in 1220 ms

We can use a [buffer](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/buffer.html) operator on a flow to run emitting code of the `simple` flow concurrently with collecting code, as opposed to running them sequentially:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
import kotlin.system.\*
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
delay(100) // pretend we are asynchronously waiting 100 ms
emit(i) // emit next value
}
}
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
simple()
.buffer() // buffer emissions, don't wait
.collect { value ->
delay(300) // pretend we are processing it for 300 ms
println(value)
}
}
println("Collected in $time ms")
//sampleEnd
}

It produces the same numbers just faster, as we have effectively created a processing pipeline, having to only wait 100 ms for the first number and then spending only 300 ms to process each number. This way it takes around 1000 ms to run:

1
2
3
Collected in 1071 ms

### Conflation

When a flow represents partial results of the operation or operation status updates, it may not be necessary to process each value, but instead, only most recent ones. In this case, the [conflate](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/conflate.html) operator can be used to skip intermediate values when a collector is too slow to process them. Building on the previous example:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
import kotlin.system.\*
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
delay(100) // pretend we are asynchronously waiting 100 ms
emit(i) // emit next value
}
}
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
simple()
.conflate() // conflate emissions, don't process each one
.collect { value ->
delay(300) // pretend we are processing it for 300 ms
println(value)
}
}
println("Collected in $time ms")
//sampleEnd
}

We see that while the first number was still being processed the second, and third were already produced, so the second one was conflated and only the most recent (the third one) was delivered to the collector:

1
3
Collected in 758 ms

### Processing the latest value

Conflation is one way to speed up processing when both the emitter and collector are slow. It does it by dropping emitted values. The other way is to cancel a slow collector and restart it every time a new value is emitted. There is a family of `xxxLatest` operators that perform the same essential logic of a `xxx` operator, but cancel the code in their block on a new value. Let's try changing [conflate](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/conflate.html) to [collectLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect-latest.html) in the previous example:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
import kotlin.system.\*
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
delay(100) // pretend we are asynchronously waiting 100 ms
emit(i) // emit next value
}
}
fun main() = runBlocking<Unit> {
//sampleStart
val time = measureTimeMillis {
simple()
.collectLatest { value -> // cancel & restart on the latest value
println("Collecting $value")
delay(300) // pretend we are processing it for 300 ms
println("Done $value")
}
}
println("Collected in $time ms")
//sampleEnd
}

Since the body of [collectLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect-latest.html) takes 300 ms, but new values are emitted every 100 ms, we see that the block is run on every value, but completes only for the last value:

Collecting 1
Collecting 2
Collecting 3
Done 3
Collected in 741 ms

## Composing multiple flows

There are lots of ways to compose multiple flows.

### Zip

Just like the [Sequence.zip](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.sequences/zip.html) extension function in the Kotlin standard library, flows have a [zip](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/zip.html) operator that combines the corresponding values of two flows:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun main() = runBlocking<Unit> {
//sampleStart
val nums = (1..3).asFlow() // numbers 1..3
val strs = flowOf("one", "two", "three") // strings
nums.zip(strs) { a, b -> "$a -> $b" } // compose a single string
.collect { println(it) } // collect and print
//sampleEnd
}

This example prints:

1 -> one
2 -> two
3 -> three

### Combine

When flow represents the most recent value of a variable or operation (see also the related section on [conflation](#conflation)), it might be needed to perform a computation that depends on the most recent values of the corresponding flows and to recompute it whenever any of the upstream flows emit a value. The corresponding family of operators is called [combine](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/combine.html).

For example, if the numbers in the previous example update every 300ms, but strings update every 400 ms, then zipping them using the [zip](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/zip.html) operator will still produce the same result, albeit results that are printed every 400 ms:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun main() = runBlocking<Unit> {
//sampleStart
val nums = (1..3).asFlow().onEach { delay(300) } // numbers 1..3 every 300 ms
val strs = flowOf("one", "two", "three").onEach { delay(400) } // strings every 400 ms
val startTime = System.currentTimeMillis() // remember the start time
nums.zip(strs) { a, b -> "$a -> $b" } // compose a single string with "zip"
.collect { value -> // collect and print
println("$value at ${System.currentTimeMillis() - startTime} ms from start")
}
//sampleEnd
}

However, when using a [combine](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/combine.html) operator here instead of a [zip](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/zip.html):

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun main() = runBlocking<Unit> {
//sampleStart
val nums = (1..3).asFlow().onEach { delay(300) } // numbers 1..3 every 300 ms
val strs = flowOf("one", "two", "three").onEach { delay(400) } // strings every 400 ms
val startTime = System.currentTimeMillis() // remember the start time
nums.combine(strs) { a, b -> "$a -> $b" } // compose a single string with "combine"
.collect { value -> // collect and print
println("$value at ${System.currentTimeMillis() - startTime} ms from start")
}
//sampleEnd
}

We get quite a different output, where a line is printed at each emission from either `nums` or `strs` flows:

1 -> one at 452 ms from start
2 -> one at 651 ms from start
2 -> two at 854 ms from start
3 -> two at 952 ms from start
3 -> three at 1256 ms from start

## Flattening flows

Flows represent asynchronously received sequences of values, and so it is quite easy to get into a situation where each value triggers a request for another sequence of values. For example, we can have the following function that returns a flow of two strings 500 ms apart:

fun requestFlow(i: Int): Flow<String> = flow {
emit("$i: First")
delay(500) // wait 500 ms
emit("$i: Second")
}

Now if we have a flow of three integers and call `requestFlow` on each of them like this:

(1..3).asFlow().map { requestFlow(it) }

Then we will end up with a flow of flows (`Flow<Flow<String>>`) that needs to be flattened into a single flow for further processing. Collections and sequences have [flatten](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.sequences/flatten.html) and [flatMap](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.sequences/flat-map.html) operators for this. However, due to the asynchronous nature of flows they call for different modes of flattening, and hence, a family of flattening operators on flows exists.

### flatMapConcat

Concatenation of flows of flows is provided by the [flatMapConcat](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-concat.html) and [flattenConcat](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flatten-concat.html) operators. They are the most direct analogues of the corresponding sequence operators. They wait for the inner flow to complete before starting to collect the next one as the following example shows:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun requestFlow(i: Int): Flow<String> = flow {
emit("$i: First")
delay(500) // wait 500 ms
emit("$i: Second")
}
fun main() = runBlocking<Unit> {
//sampleStart
val startTime = System.currentTimeMillis() // remember the start time
(1..3).asFlow().onEach { delay(100) } // emit a number every 100 ms
.flatMapConcat { requestFlow(it) }
.collect { value -> // collect and print
println("$value at ${System.currentTimeMillis() - startTime} ms from start")
}
//sampleEnd
}

The sequential nature of [flatMapConcat](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-concat.html) is clearly seen in the output:

1: First at 121 ms from start
1: Second at 622 ms from start
2: First at 727 ms from start
2: Second at 1227 ms from start
3: First at 1328 ms from start
3: Second at 1829 ms from start

### flatMapMerge

Another flattening operation is to concurrently collect all the incoming flows and merge their values into a single flow so that values are emitted as soon as possible. It is implemented by [flatMapMerge](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-merge.html) and [flattenMerge](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flatten-merge.html) operators. They both accept an optional `concurrency` parameter that limits the number of concurrent flows that are collected at the same time (it is equal to [DEFAULT\_CONCURRENCY](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-d-e-f-a-u-l-t_-c-o-n-c-u-r-r-e-n-c-y.html) by default).

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun requestFlow(i: Int): Flow<String> = flow {
emit("$i: First")
delay(500) // wait 500 ms
emit("$i: Second")
}
fun main() = runBlocking<Unit> {
//sampleStart
val startTime = System.currentTimeMillis() // remember the start time
(1..3).asFlow().onEach { delay(100) } // a number every 100 ms
.flatMapMerge { requestFlow(it) }
.collect { value -> // collect and print
println("$value at ${System.currentTimeMillis() - startTime} ms from start")
}
//sampleEnd
}

The concurrent nature of [flatMapMerge](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-merge.html) is obvious:

1: First at 136 ms from start
2: First at 231 ms from start
3: First at 333 ms from start
1: Second at 639 ms from start
2: Second at 732 ms from start
3: Second at 833 ms from start

### flatMapLatest

In a similar way to the [collectLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect-latest.html) operator, that was described in the section ["Processing the latest value"](#processing-the-latest-value), there is the corresponding "Latest" flattening mode where the collection of the previous flow is cancelled as soon as new flow is emitted. It is implemented by the [flatMapLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-latest.html) operator.

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun requestFlow(i: Int): Flow<String> = flow {
emit("$i: First")
delay(500) // wait 500 ms
emit("$i: Second")
}
fun main() = runBlocking<Unit> {
//sampleStart
val startTime = System.currentTimeMillis() // remember the start time
(1..3).asFlow().onEach { delay(100) } // a number every 100 ms
.flatMapLatest { requestFlow(it) }
.collect { value -> // collect and print
println("$value at ${System.currentTimeMillis() - startTime} ms from start")
}
//sampleEnd
}

The output here in this example is a good demonstration of how [flatMapLatest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flat-map-latest.html) works:

1: First at 142 ms from start
2: First at 322 ms from start
3: First at 425 ms from start
3: Second at 931 ms from start

## Flow exceptions

Flow collection can complete with an exception when an emitter or code inside the operators throw an exception. There are several ways to handle these exceptions.

### Collector try and catch

A collector can use Kotlin's [`try/catch`](/docs/reference/exceptions.html) block to handle exceptions:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
println("Emitting $i")
emit(i) // emit next value
}
}
fun main() = runBlocking<Unit> {
try {
simple().collect { value ->
println(value)
check(value <= 1) { "Collected $value" }
}
} catch (e: Throwable) {
println("Caught $e")
}
}
//sampleEnd

This code successfully catches an exception in [collect](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect.html) terminal operator and, as we see, no more values are emitted after that:

Emitting 1
1
Emitting 2
2
Caught java.lang.IllegalStateException: Collected 2

### Everything is caught

The previous example actually catches any exception happening in the emitter or in any intermediate or terminal operators. For example, let's change the code so that emitted values are [mapped](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/map.html) to strings, but the corresponding code produces an exception:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<String> =
flow {
for (i in 1..3) {
println("Emitting $i")
emit(i) // emit next value
}
}
.map { value ->
check(value <= 1) { "Crashed on $value" }
"string $value"
}
fun main() = runBlocking<Unit> {
try {
simple().collect { value -> println(value) }
} catch (e: Throwable) {
println("Caught $e")
}
}
//sampleEnd

This exception is still caught and collection is stopped:

Emitting 1
string 1
Emitting 2
Caught java.lang.IllegalStateException: Crashed on 2

## Exception transparency

But how can code of the emitter encapsulate its exception handling behavior?

Flows must be transparent to exceptions and it is a violation of the exception transparency to [emit](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow-collector/emit.html) values in the `flow { ... }` builder from inside of a `try/catch` block. This guarantees that a collector throwing an exception can always catch it using `try/catch` as in the previous example.

The emitter can use a [catch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html) operator that preserves this exception transparency and allows encapsulation of its exception handling. The body of the `catch` operator can analyze an exception and react to it in different ways depending on which exception was caught:

* Exceptions can be rethrown using `throw`.
* Exceptions can be turned into emission of values using [emit](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow-collector/emit.html) from the body of [catch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html).
* Exceptions can be ignored, logged, or processed by some other code.

For example, let us emit the text on catching an exception:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun simple(): Flow<String> =
flow {
for (i in 1..3) {
println("Emitting $i")
emit(i) // emit next value
}
}
.map { value ->
check(value <= 1) { "Crashed on $value" }
"string $value"
}
fun main() = runBlocking<Unit> {
//sampleStart
simple()
.catch { e -> emit("Caught $e") } // emit on exception
.collect { value -> println(value) }
//sampleEnd
}

The output of the example is the same, even though we do not have `try/catch` around the code anymore.

### Transparent catch

The [catch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html) intermediate operator, honoring exception transparency, catches only upstream exceptions (that is an exception from all the operators above `catch`, but not below it). If the block in `collect { ... }` (placed below `catch`) throws an exception then it escapes:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
println("Emitting $i")
emit(i)
}
}
fun main() = runBlocking<Unit> {
simple()
.catch { e -> println("Caught $e") } // does not catch downstream exceptions
.collect { value ->
check(value <= 1) { "Collected $value" }
println(value)
}
}
//sampleEnd

A "Caught ..." message is not printed despite there being a `catch` operator:

Emitting 1
1
Emitting 2
Exception in thread "main" java.lang.IllegalStateException: Collected 2
at ...

### Catching declaratively

We can combine the declarative nature of the [catch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html) operator with a desire to handle all the exceptions, by moving the body of the [collect](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect.html) operator into [onEach](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-each.html) and putting it before the `catch` operator. Collection of this flow must be triggered by a call to `collect()` without parameters:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun simple(): Flow<Int> = flow {
for (i in 1..3) {
println("Emitting $i")
emit(i)
}
}
fun main() = runBlocking<Unit> {
//sampleStart
simple()
.onEach { value ->
check(value <= 1) { "Collected $value" }
println(value)
}
.catch { e -> println("Caught $e") }
.collect()
//sampleEnd
}

Now we can see that a "Caught ..." message is printed and so we can catch all the exceptions without explicitly using a `try/catch` block:

Emitting 1
1
Emitting 2
Caught java.lang.IllegalStateException: Collected 2

## Flow completion

When flow collection completes (normally or exceptionally) it may need to execute an action. As you may have already noticed, it can be done in two ways: imperative or declarative.

### Imperative finally block

In addition to `try`/`catch`, a collector can also use a `finally` block to execute an action upon `collect` completion.

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = (1..3).asFlow()
fun main() = runBlocking<Unit> {
try {
simple().collect { value -> println(value) }
} finally {
println("Done")
}
}
//sampleEnd

This code prints three numbers produced by the `simple` flow followed by a "Done" string:

1
2
3
Done

### Declarative handling

For the declarative approach, flow has [onCompletion](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-completion.html) intermediate operator that is invoked when the flow has completely collected.

The previous example can be rewritten using an [onCompletion](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-completion.html) operator and produces the same output:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
fun simple(): Flow<Int> = (1..3).asFlow()
fun main() = runBlocking<Unit> {
//sampleStart
simple()
.onCompletion { println("Done") }
.collect { value -> println(value) }
//sampleEnd
}

The key advantage of [onCompletion](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-completion.html) is a nullable `Throwable` parameter of the lambda that can be used to determine whether the flow collection was completed normally or exceptionally. In the following example the `simple` flow throws an exception after emitting the number 1:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = flow {
emit(1)
throw RuntimeException()
}
fun main() = runBlocking<Unit> {
simple()
.onCompletion { cause -> if (cause != null) println("Flow completed exceptionally") }
.catch { cause -> println("Caught exception") }
.collect { value -> println(value) }
}
//sampleEnd

As you may expect, it prints:

1
Flow completed exceptionally
Caught exception

The [onCompletion](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-completion.html) operator, unlike [catch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html), does not handle the exception. As we can see from the above example code, the exception still flows downstream. It will be delivered to further `onCompletion` operators and can be handled with a `catch` operator.

### Successful completion

Another difference with [catch](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html) operator is that [onCompletion](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-completion.html) sees all exceptions and receives a `null` exception only on successful completion of the upstream flow (without cancellation or failure).

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun simple(): Flow<Int> = (1..3).asFlow()
fun main() = runBlocking<Unit> {
simple()
.onCompletion { cause -> println("Flow completed with $cause") }
.collect { value ->
check(value <= 1) { "Collected $value" }
println(value)
}
}
//sampleEnd

We can see the completion cause is not null, because the flow was aborted due to downstream exception:

1
Flow completed with java.lang.IllegalStateException: Collected 2
Exception in thread "main" java.lang.IllegalStateException: Collected 2

## Imperative versus declarative

Now we know how to collect flow, and handle its completion and exceptions in both imperative and declarative ways. The natural question here is, which approach is preferred and why? As a library, we do not advocate for any particular approach and believe that both options are valid and should be selected according to your own preferences and code style.

## Launching flow

It is easy to use flows to represent asynchronous events that are coming from some source. In this case, we need an analogue of the `addEventListener` function that registers a piece of code with a reaction for incoming events and continues further work. The [onEach](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/on-each.html) operator can serve this role. However, `onEach` is an intermediate operator. We also need a terminal operator to collect the flow. Otherwise, just calling `onEach` has no effect.

If we use the [collect](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect.html) terminal operator after `onEach`, then the code after it will wait until the flow is collected:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
// Imitate a flow of events
fun events(): Flow<Int> = (1..3).asFlow().onEach { delay(100) }
fun main() = runBlocking<Unit> {
events()
.onEach { event -> println("Event: $event") }
.collect() // <--- Collecting the flow waits
println("Done")
}
//sampleEnd

As you can see, it prints:

Event: 1
Event: 2
Event: 3
Done

The [launchIn](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/launch-in.html) terminal operator comes in handy here. By replacing `collect` with `launchIn` we can launch a collection of the flow in a separate coroutine, so that execution of further code immediately continues:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
// Imitate a flow of events
fun events(): Flow<Int> = (1..3).asFlow().onEach { delay(100) }
//sampleStart
fun main() = runBlocking<Unit> {
events()
.onEach { event -> println("Event: $event") }
.launchIn(this) // <--- Launching the flow in a separate coroutine
println("Done")
}
//sampleEnd

It prints:

Done
Event: 1
Event: 2
Event: 3

The required parameter to `launchIn` must specify a [CoroutineScope](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-scope/index.html) in which the coroutine to collect the flow is launched. In the above example this scope comes from the [runBlocking](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html) coroutine builder, so while the flow is running, this [runBlocking](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html) scope waits for completion of its child coroutine and keeps the main function from returning and terminating this example.

In actual applications a scope will come from an entity with a limited lifetime. As soon as the lifetime of this entity is terminated the corresponding scope is cancelled, cancelling the collection of the corresponding flow. This way the pair of `onEach { ... }.launchIn(scope)` works like the `addEventListener`. However, there is no need for the corresponding `removeEventListener` function, as cancellation and structured concurrency serve this purpose.

Note that [launchIn](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/launch-in.html) also returns a [Job](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/index.html), which can be used to [cancel](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/cancel.html) the corresponding flow collection coroutine only without cancelling the whole scope or to [join](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/join.html) it.

### Flow cancellation checks

For convenience, the [flow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/flow.html) builder performs additional [ensureActive](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/ensure-active.html) checks for cancellation on each emitted value. It means that a busy loop emitting from a `flow { ... }` is cancellable:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun foo(): Flow<Int> = flow {
for (i in 1..5) {
println("Emitting $i")
emit(i)
}
}
fun main() = runBlocking<Unit> {
foo().collect { value ->
if (value == 3) cancel()
println(value)
}
}
//sampleEnd

We get only numbers up to 3 and a [CancellationException](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/index.html) after trying to emit number 4:

Emitting 1
1
Emitting 2
2
Emitting 3
3
Emitting 4
Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@6d7b4f4c

However, most other flow operators do not do additional cancellation checks on their own for performance reasons. For example, if you use [IntRange.asFlow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/as-flow.html) extension to write the same busy loop and don't suspend anywhere, then there are no checks for cancellation:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun main() = runBlocking<Unit> {
(1..5).asFlow().collect { value ->
if (value == 3) cancel()
println(value)
}
}
//sampleEnd

All numbers from 1 to 5 are collected and cancellation gets detected only before return from `runBlocking`:

1
2
3
4
5
Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@3327bd23

#### Making busy flow cancellable

In the case where you have a busy loop with coroutines you must explicitly check for cancellation. You can add `.onEach { currentCoroutineContext().ensureActive() }`, but there is a ready-to-use [cancellable](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/cancellable.html) operator provided to do that:

import kotlinx.coroutines.\*
import kotlinx.coroutines.flow.\*
//sampleStart
fun main() = runBlocking<Unit> {
(1..5).asFlow().cancellable().collect { value ->
if (value == 3) cancel()
println(value)
}
}
//sampleEnd

With the `cancellable` operator only the numbers from 1 to 3 are collected:

1
2
3
Exception in thread "main" kotlinx.coroutines.JobCancellationException: BlockingCoroutine was cancelled; job="coroutine#1":BlockingCoroutine{Cancelled}@5ec0a365

## Flow and Reactive Streams

For those who are familiar with [Reactive Streams](https://www.reactive-streams.org/) or reactive frameworks such as RxJava and project Reactor, design of the Flow may look very familiar.

Indeed, its design was inspired by Reactive Streams and its various implementations. But Flow main goal is to have as simple design as possible, be Kotlin and suspension friendly and respect structured concurrency. Achieving this goal would be impossible without reactive pioneers and their tremendous work. You can read the complete story in [Reactive Streams and Kotlin Flows](https://medium.com/@elizarov/reactive-streams-and-kotlin-flows-bfd12772cda4) article.

While being different, conceptually, Flow is a reactive stream and it is possible to convert it to the reactive (spec and TCK compliant) Publisher and vice versa. Such converters are provided by `kotlinx.coroutines` out-of-the-box and can be found in corresponding reactive modules (`kotlinx-coroutines-reactive` for Reactive Streams, `kotlinx-coroutines-reactor` for Project Reactor and `kotlinx-coroutines-rx2`/`kotlinx-coroutines-rx3` for RxJava2/RxJava3). Integration modules include conversions from and to `Flow`, integration with Reactor's `Context` and suspension-friendly ways to work with various reactive entities.

27 September 2024

---

## Bibliography

1. [Shared mutable state and concurrency](https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html)
2. [Channels](https://kotlinlang.org/docs/channels.html)
3. [Asynchronous Flow](https://kotlinlang.org/docs/flow.html)