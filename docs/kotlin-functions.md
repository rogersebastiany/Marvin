# Kotlin Functions and Lambdas


---

## 1. Extensions

Kotlin extensions let you extend a class or an interface with new functionality without using inheritance or design patterns like Decorator. They are useful when working with third-party libraries you can't modify directly. Once created, you call these extensions as if they were members of the original class or interface.

The most common forms of extensions are [extension functions](#extension-functions) and [extension properties](#extension-properties).

Importantly, extensions don't modify the classes or interfaces they extend. When you define an extension, you don't add new members. You make new functions callable or new properties accessible using the same syntax.

## Receivers

Extensions are always called on a receiver. The receiver has to have the same type as the class or interface being extended. To use an extension, prefix it with the receiver followed by a `.` and the function or property name.

For example, the [`.appendLine()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.text/append-line.html) extension function from the standard library extends the `StringBuilder` class. So in this case, the receiver is a `StringBuilder` instance, and the receiver type is `StringBuilder`:

fun main() {
//sampleStart
// builder is an instance of StringBuilder
val builder = StringBuilder()
// Calls .appendLine() extension function on builder
.appendLine("Hello")
.appendLine()
.appendLine("World")
println(builder.toString())
// Hello
//
// World
}
//sampleEnd

## Extension functions

Before creating your own extension functions, see if what you are looking for is already available in the Kotlin [standard library](https://kotlinlang.org/api/core/kotlin-stdlib/). The standard library provides many useful extension functions for:

* Operating on collections: [`.map()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/map.html), [`.filter()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/filter.html), [`.reduce()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/reduce.html), [`.fold()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/fold.html), [`.groupBy()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/group-by.html).
* Converting to strings: [`.joinToString()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/join-to-string.html).
* Working with null values: [`.filterNotNull()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/filter-not-null.html).

To create your own extension function, prefix its name with a receiver type followed by a `.`. In this example, the `.truncate()` function extends the `String` class, so the receiver type is `String`:

fun String.truncate(maxLength: Int): String {
return if (this.length <= maxLength) this else take(maxLength - 3) + "..."
}
fun main() {
val shortUsername = "KotlinFan42"
val longUsername = "JetBrainsLoverForever"
println("Short username: ${shortUsername.truncate(15)}")
// KotlinFan42
println("Long username: ${longUsername.truncate(15)}")
// JetBrainsLov...
}

The `.truncate()` function truncates any string that it's called on by the number in the `maxLength` argument and adds an ellipsis `...`. If the string is shorter than `maxLength`, the function returns the original string.

In this example, the `.displayInfo()` function extends the `User` interface:

interface User {
val name: String
val email: String
}
fun User.displayInfo(): String = "User(name=$name, email=$email)"
// Inherits from and implements the properties of the User interface
class RegularUser(override val name: String, override val email: String) : User
fun main() {
val user = RegularUser("Alice", "alice@example.com")
println(user.displayInfo())
// User(name=Alice, email=alice@example.com)
}

The `.displayInfo()` function returns a string containing the `name` and `email` of a `RegularUser` instance. Defining an extension on an interface like this is useful when you want to add functionality to all types that implement an interface only once.

In this example, the `.mostVoted()` function extends the `Map<String, Int>` class:

fun Map<String, Int>.mostVoted(): String? {
return maxByOrNull { (key, value) -> value }?.key
}
fun main() {
val poll = mapOf(
"Cats" to 37,
"Dogs" to 58,
"Birds" to 22
)
println("Top choice: ${poll.mostVoted()}")
// Dogs
}

The `.mostVoted()` function iterates through the key-value pairs of the map it's called on and uses the [`maxByOrNull()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/max-by-or-null.html) function to return the key of the pair containing the highest value. If the map is empty, the `maxByOrNull()` function returns `null`. The `mostVoted()` function uses a safe call `?.` to only access the `key` property when the `maxByOrNull()` function returns a non-null value.

### Generic extension functions

To create generic extension functions, declare the generic type parameter before the function name to make it available in the receiver type expression. In this example, the `.endpoints()` function extends `List<T>` where `T` can be any type:

fun <T> List<T>.endpoints(): Pair<T, T> {
return first() to last()
}
fun main() {
val cities = listOf("Paris", "London", "Berlin", "Prague")
val temperatures = listOf(21.0, 19.5, 22.3)
val cityEndpoints = cities.endpoints()
val tempEndpoints = temperatures.endpoints()
println("First and last cities: $cityEndpoints")
// (Paris, Prague)
println("First and last temperatures: $tempEndpoints")
// (21.0, 22.3)
}

The `.endpoints()` function returns a pair containing the first and last elements of the list that it's called on. Inside the function body, it calls the `first()` and `last()` functions and combines their returned values into a `Pair` using the `to` infix function.

For more information about generics, see [generic functions](generics.html).

### Nullable receivers

You can define extension functions with a nullable receiver type, which allows you to call them on a variable even if its value is null. When the receiver is `null`, `this` is also `null`. Make sure to handle nullability correctly within your functions. For example, use `this == null` checks inside function bodies, [safe calls `?.`](null-safety.html#safe-call-operator), or the [Elvis operator `?:`](null-safety.html#elvis-operator).

In this example, you can call the `.toString()` function without checking for `null` because the check already happens inside the extension function:

fun main() {
//sampleStart
// Extension function on nullable Any
fun Any?.toString(): String {
if (this == null) return "null"
// After null check, `this` is smart-cast to non-nullable Any
// So this call resolves to the regular toString() function
return toString()
}
val number: Int? = 42
val nothing: Any? = null
println(number.toString())
// 42
println(nothing.toString())
// null
//sampleEnd
}

### Extension or member functions?

Since extension and member function calls have the same notation, how does the compiler know which one to use? Extension functions are dispatched statically, meaning the compiler determines which function to call based on the receiver type at compile time. For example:

fun main() {
//sampleStart
open class Shape
class Rectangle: Shape()
fun Shape.getName() = "Shape"
fun Rectangle.getName() = "Rectangle"
fun printClassName(shape: Shape) {
println(shape.getName())
}
printClassName(Rectangle())
// Shape
//sampleEnd
}

In this example, the compiler calls the `Shape.getName()` extension function because the parameter `shape` is declared as type `Shape`. Because extension functions are resolved statically, the compiler chooses the function based on the declared type, not the actual instance.

So even though the example passes a `Rectangle` instance, the `.getName()` function resolves to `Shape.getName()` since the variable is declared as type `Shape`.

If a class has a member function and there's an extension function with the same receiver type, the same name, and compatible arguments, the member function takes precedence. For example:

fun main() {
//sampleStart
class Example {
fun printFunctionType() { println("Member function") }
}
fun Example.printFunctionType() { println("Extension function") }
Example().printFunctionType()
// Member function
//sampleEnd
}

However, extension functions can overload member functions that have the same name but a different signature:

fun main() {
//sampleStart
class Example {
fun printFunctionType() { println("Member function") }
}
// Same name but different signature
fun Example.printFunctionType(index: Int) { println("Extension function #$index") }
Example().printFunctionType(1)
// Extension function #1
//sampleEnd
}

In this example, since an `Int` is passed to the `.printFunctionType()` function, the compiler chooses the extension function because it matches the signature. The compiler ignores the member function, which takes no arguments.

### Anonymous extension functions

You can define extension functions without giving them a name. This is useful when you want to avoid cluttering the global namespace or when you need to pass some extension behavior as a parameter.

For example, suppose you want to extend a data class with a one-time function to calculate shipping, without giving it a name:

fun main() {
//sampleStart
data class Order(val weight: Double)
val calculateShipping = fun Order.(rate: Double): Double = this.weight \* rate
val order = Order(2.5)
val cost = order.calculateShipping(3.0)
println("Shipping cost: $cost")
// Shipping cost: 7.5
}

To pass extension behavior as a parameter, use a [lambda expression](lambdas.html#lambda-expression-syntax) with a type annotation. For example, let's say you want to check if a number is within a range without defining a named function:

fun main() {
val isInRange: Int.(min: Int, max: Int) -> Boolean = { min, max -> this in min..max }
println(5.isInRange(1, 10))
// true
println(20.isInRange(1, 10))
// false
}

In this example, the `isInRange` variable holds a function of type `Int.(min: Int, max: Int) -> Boolean`. The type is an extension function on the `Int` class that takes `min` and `max` parameters and returns a `Boolean`.

The lambda body `{ min, max -> this in min..max }` checks whether the `Int` value the function is called on falls within the range between `min` and `max` parameters. If the check is successful, the lambda returns `true`.

For more information, see [Lambda expressions and anonymous functions](lambdas.html).

## Extension properties

Kotlin supports extension properties, which are useful for performing data transformations or creating UI display helpers without cluttering the class you're working with.

To create an extension property, write the name of the class that you want to extend, followed by a `.` and the name of your property.

For example, suppose you have a data class that represents a user with a first and last name, and you want to create a property that returns an email-style username when accessed. Your code might look like this:

data class User(val firstName: String, val lastName: String)
// An extension property to get a username-style email handle
val User.emailUsername: String
get() = "${firstName.lowercase()}.${lastName.lowercase()}"
fun main() {
val user = User("Mickey", "Mouse")
// Calls extension property
println("Generated email username: ${user.emailUsername}")
// Generated email username: mickey.mouse
}

Since extensions don't actually add members to classes, there's no efficient way for an extension property to have a [backing field](properties.html#backing-fields). That's why initializers are not allowed for extension properties. You can define their behavior only by explicitly providing getters and setters. For example:

data class House(val streetName: String)
// Doesn't compile because there is no getter and setter
// var House.number = 1
// Error: Initializers are not allowed for extension properties
// Compiles successfully
val houseNumbers = mutableMapOf<House, Int>()
var House.number: Int
get() = houseNumbers[this] ?: 1
set(value) {
println("Setting house number for ${this.streetName} to $value")
houseNumbers[this] = value
}
fun main() {
val house = House("Maple Street")
// Shows the default
println("Default number: ${house.number} ${house.streetName}")
// Default number: 1 Maple Street
house.number = 99
// Setting house number for Maple Street to 99
// Shows the updated number
println("Updated number: ${house.number} ${house.streetName}")
// Updated number: 99 Maple Street
}

In this example, the getter uses the [Elvis operator](null-safety.html#elvis-operator) to return the house number if it exists in the `houseNumbers` map or `1`. To learn more about how to write getters and setters, see [Custom getters and setters](properties.html#custom-getters-and-setters).

## Companion object extensions

If a class defines a [companion object](object-declarations.html#companion-objects), you can also define extension functions and properties for the companion object. Just like regular members of the companion object, you can call them using only the class name as the qualifier. The compiler names the companion object `Companion` by default:

class Logger {
companion object { }
}
fun Logger.Companion.logStartupMessage() {
println("Application started.")
}
fun main() {
Logger.logStartupMessage()
// Application started.
}

## Declaring extensions as members

You can declare extensions for one class inside another. Extensions like this have multiple implicit receivers. An implicit receiver is an object whose members you can access without qualifying them with [`this`](this-expressions.html#qualified-this):

* The class where you declare the extension is the dispatch receiver.
* The extension function's receiver type is the extension receiver.

Consider this example where the `Connection` class has an extension function for the `Host` class called `printConnectionString()`:

class Host(val hostname: String) {
fun printHostname() { print(hostname) }
}
class Connection(val host: Host, val port: Int) {
fun printPort() { print(port) }
// Host is the extension receiver
fun Host.printConnectionString() {
// Calls Host.printHostname()
printHostname()
print(":")
// Calls Connection.printPort()
// Connection is the dispatch receiver
printPort()
}
fun connect() {
/\*...\*/
// Calls the extension function
host.printConnectionString()
}
}
fun main() {
Connection(Host("kotl.in"), 443).connect()
// kotl.in:443
// Triggers an error because the extension function isn't available outside Connection
// Host("kotl.in").printConnectionString()
// Unresolved reference 'printConnectionString'.
}

This example declares the `printConnectionString()` function inside the `Connection` class, so the `Connection` class is the dispatch receiver. The extension function's receiver type is the `Host` class, so the `Host` class is the extension receiver.

If the dispatch receiver and the extension receiver have members with the same name, the extension receiver's member takes precedence. To access the dispatch receiver explicitly, use the [qualified `this` syntax](this-expressions.html#qualified-this):

class Connection {
fun Host.getConnectionString() {
// Calls Host.toString()
toString()
// Calls Connection.toString()
this@Connection.toString()
}
}

### Overriding member extensions

You can declare member extensions as `open` and override them in subclasses, which is useful when you want to customize the extension's behavior for each subclass. The compiler handles each receiver type differently:

| Receiver type | Resolution time | Dispatch type |
| --- | --- | --- |
| Dispatch receiver | Runtime | Virtual |
| Extension receiver | Compile time | Static |

Consider this example, where the `User` class is `open` and the `Admin` class inherits from it. The `NotificationSender` class defines `sendNotification()` extension functions for both `User` and `Admin` classes, and the `SpecialNotificationSender` class overrides them:

open class User
class Admin : User()
open class NotificationSender {
open fun User.sendNotification() {
println("Sending user notification from normal sender")
}
open fun Admin.sendNotification() {
println("Sending admin notification from normal sender")
}
fun notify(user: User) {
user.sendNotification()
}
}
class SpecialNotificationSender : NotificationSender() {
override fun User.sendNotification() {
println("Sending user notification from special sender")
}
override fun Admin.sendNotification() {
println("Sending admin notification from special sender")
}
}
fun main() {
// Dispatch receiver is NotificationSender
// Extension receiver is User
// Resolves to User.sendNotification() in NotificationSender
NotificationSender().notify(User())
// Sending user notification from normal sender
// Dispatch receiver is SpecialNotificationSender
// Extension receiver is User
// Resolves to User.sendNotification() in SpecialNotificationSender
SpecialNotificationSender().notify(User())
// Sending user notification from special sender
// Dispatch receiver is SpecialNotificationSender
// Extension receiver is User NOT Admin
// The notify() function declares user as type User
// Statically resolves to User.sendNotification() in SpecialNotificationSender
SpecialNotificationSender().notify(Admin())
// Sending user notification from special sender
}

The dispatch receiver is resolved at runtime using virtual dispatch, which makes the behavior in the `main()` function easier to follow. What may surprise you is that when you call the `notify()` function on an `Admin` instance, the compiler chooses the extension based on the declared type: `user: User`, because it resolves the extension receiver statically.

## Extensions and visibility modifiers

Extensions use the same [visibility modifiers](visibility-modifiers.html) as regular functions declared in the same scope, including extensions declared as members of other classes.

For example, an extension declared at the top level of a file can access other `private` top-level declarations in the same file:

// File: StringUtils.kt
private fun removeWhitespace(input: String): String {
return input.replace("\\s".toRegex(), "")
}
fun String.cleaned(): String {
return removeWhitespace(this)
}
fun main() {
val rawEmail = " user @example. com "
val cleaned = rawEmail.cleaned()
println("Raw: '$rawEmail'")
// Raw: ' user @example. com '
println("Cleaned: '$cleaned'")
// Cleaned: 'user@example.com'
println("Looks like an email: ${cleaned.contains("@") && cleaned.contains(".")}")
// Looks like an email: true
}

And if an extension is declared outside its receiver type, it can't access the receiver's `private` or `protected` members:

class User(private val password: String) {
fun isLoggedIn(): Boolean = true
fun passwordLength(): Int = password.length
}
// Extension declared outside the class
fun User.isSecure(): Boolean {
// Can't access password because it's private:
// return password.length >= 8
// Instead, we rely on public members:
return passwordLength() >= 8 && isLoggedIn()
}
fun main() {
val user = User("supersecret")
println("Is user secure: ${user.isSecure()}")
// Is user secure: true
}

If an extension is marked as `internal`, it's only accessible within its [module](visibility-modifiers.html#modules):

// Networking module
// JsonParser.kt
internal fun String.parseJson(): Map<String, Any> {
return mapOf("fakeKey" to "fakeValue")
}

## Scope of extensions

In most cases, you define extensions on the top level, directly under packages:

package org.example.declarations
fun List<String>.getLongestString() { /\*...\*/}

To use an extension outside its declaring package, import it at the call site:

package org.example.usage
import org.example.declarations.getLongestString
fun main() {
val list = listOf("red", "green", "blue")
list.getLongestString()
}

For more information, see [Imports](packages.html#imports).

04 November 2025

---

## 2. Inline functions

Using [higher-order functions](lambdas.html) imposes certain runtime penalties: each function is an object, and it captures a closure. A closure is a scope of variables that can be accessed in the body of the function. Memory allocations (both for function objects and classes) and virtual calls introduce runtime overhead.

But it appears that in many cases this kind of overhead can be eliminated by inlining the lambda expressions. The functions shown below are good examples of this situation. The `lock()` function could be easily inlined at call-sites. Consider the following case:

lock(l) { foo() }

Instead of creating a function object for the parameter and generating a call, the compiler could emit the following code:

l.lock()
try {
foo()
} finally {
l.unlock()
}

To make the compiler do this, mark the `lock()` function with the `inline` modifier:

inline fun <T> lock(lock: Lock, body: () -> T): T { ... }

The `inline` modifier affects both the function itself and the lambdas passed to it: all of those will be inlined into the call site.

Inlining may cause the generated code to grow. However, if you do it in a reasonable way (avoiding inlining large functions), it will pay off in performance, especially at "megamorphic" call-sites inside loops.

## noinline

If you don't want all of the lambdas passed to an inline function to be inlined, mark some of your function parameters with the `noinline` modifier:

inline fun foo(inlined: () -> Unit, noinline notInlined: () -> Unit) { ... }

Inlinable lambdas can only be called inside inline functions or passed as inlinable arguments. `noinline` lambdas, however, can be manipulated in any way you like, including being stored in fields or passed around.

## Non-local jump expressions

### Returns

In Kotlin, you can only use a normal, unqualified `return` to exit a named function or an anonymous function. To exit a lambda, use a [label](returns.html#return-to-labels). A bare `return` is forbidden inside a lambda because a lambda cannot make the enclosing function `return`:

fun ordinaryFunction(block: () -> Unit) {
println("hi!")
}
//sampleStart
fun foo() {
ordinaryFunction {
return // ERROR: cannot make `foo` return here
}
}
//sampleEnd
fun main() {
foo()
}

But if the function the lambda is passed to is inlined, the return can be inlined, as well. So it is allowed:

inline fun inlined(block: () -> Unit) {
println("hi!")
}
//sampleStart
fun foo() {
inlined {
return // OK: the lambda is inlined
}
}
//sampleEnd
fun main() {
foo()
}

Such returns (located in a lambda, but exiting the enclosing function) are called non-local returns. This sort of construct usually occurs in loops, which inline functions often enclose:

fun hasZeros(ints: List<Int>): Boolean {
ints.forEach {
if (it == 0) return true // returns from hasZeros
}
return false
}

Note that some inline functions may call the lambdas passed to them as parameters not directly from the function body, but from another execution context, such as a local object or a nested function. In such cases, non-local control flow is also not allowed in the lambdas. To indicate that the lambda parameter of the inline function cannot use non-local returns, mark the lambda parameter with the `crossinline` modifier:

inline fun f(crossinline body: () -> Unit) {
val f = object: Runnable {
override fun run() = body()
}
// ...
}

### Break and continue

Similar to non-local `return`, you can apply `break` and `continue` [jump expressions](returns.html) in lambdas passed as arguments to an inline function that encloses a loop:

fun processList(elements: List<Int>): Boolean {
for (element in elements) {
val variable = element.nullableMethod() ?: run {
log.warning("Element is null or invalid, continuing...")
continue
}
if (variable == 0) return true
}
return false
}

## Reified type parameters

Sometimes you need to access a type passed as a parameter:

fun <T> TreeNode.findParentOfType(clazz: Class<T>): T? {
while (p != null && !clazz.isInstance(p)) {
p = p.parent
}
@Suppress("UNCHECKED\_CAST")
return p as T?
}

Here, you walk up a tree and use reflection to check whether a node has a certain type. It's all fine, but the call site is not very pretty:

treeNode.findParentOfType(MyTreeNode::class.java)

A better solution would be to simply pass a type to this function. You can call it as follows:

treeNode.findParentOfType<MyTreeNode>()

To enable this, inline functions support reified type parameters, so you can write something like this:

inline fun <reified T> TreeNode.findParentOfType(): T? {
while (p != null && p !is T) {
p = p.parent
}
return p as T?
}

The code above qualifies the type parameter with the `reified` modifier to make it accessible inside the function, almost as if it were a normal class. Since the function is inlined, no reflection is needed and normal operators like `!is` and `as` are now available for you to use. Also, you can call the function as shown above: `myTree.findParentOfType<MyTreeNodeType>()`.

Though reflection may not be needed in many cases, you can still use it with a reified type parameter:

inline fun <reified T> membersOf() = T::class.members
fun main(s: Array<String>) {
println(membersOf<StringBuilder>().joinToString("\n"))
}

Normal functions (not marked as inline) cannot have reified parameters. A type that does not have a run-time representation (for example, a non-reified type parameter or a fictitious type like `Nothing`) cannot be used as an argument for a reified type parameter.

## Inline properties

The `inline` modifier can be used on accessors of properties that don't have [backing fields](properties.html#backing-fields). You can annotate individual property accessors:

val foo: Foo
inline get() = Foo()
var bar: Bar
get() = ...
inline set(v) { ... }

You can also annotate an entire property, which marks both of its accessors as `inline`:

inline var bar: Bar
get() = ...
set(v) { ... }

At the call site, inline accessors are inlined as regular inline functions.

## Restrictions for public API inline functions

When an inline function is `public` or `protected` but is not a part of a `private` or `internal` declaration, it is considered a [module](visibility-modifiers.html#modules)'s public API. It can be called in other modules and is inlined at such call sites as well.

This imposes certain risks of binary incompatibility caused by changes in the module that declares an inline function in case the calling module is not re-compiled after the change.

To eliminate the risk of such incompatibility being introduced by a change in a non-public API of a module, public API inline functions are not allowed to use non-public-API declarations, i.e. `private` and `internal` declarations and their parts, in their bodies.

An `internal` declaration can be annotated with `@PublishedApi`, which allows its use in public API inline functions. When an `internal` inline function is marked as `@PublishedApi`, its body is checked too, as if it were public.

23 June 2025

---

## 3. Scope functions

The Kotlin standard library contains several functions whose sole purpose is to execute a block of code within the context of an object. When you call such a function on an object with a [lambda expression](lambdas.html) provided, it forms a temporary scope. In this scope, you can access the object without its name. Such functions are called scope functions. There are five of them: [`let`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/let.html), [`run`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/run.html), [`with`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/with.html), [`apply`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/apply.html), and [`also`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/also.html).

Basically, these functions all perform the same action: execute a block of code on an object. What's different is how this object becomes available inside the block and what the result of the whole expression is.

Here's a typical example of how to use a scope function:

data class Person(var name: String, var age: Int, var city: String) {
fun moveTo(newCity: String) { city = newCity }
fun incrementAge() { age++ }
}
fun main() {
//sampleStart
Person("Alice", 20, "Amsterdam").let {
println(it)
it.moveTo("London")
it.incrementAge()
println(it)
}
//sampleEnd
}

If you write the same without `let`, you'll have to introduce a new variable and repeat its name whenever you use it.

data class Person(var name: String, var age: Int, var city: String) {
fun moveTo(newCity: String) { city = newCity }
fun incrementAge() { age++ }
}
fun main() {
//sampleStart
val alice = Person("Alice", 20, "Amsterdam")
println(alice)
alice.moveTo("London")
alice.incrementAge()
println(alice)
//sampleEnd
}

Scope functions don't introduce any new technical capabilities, but they can make your code more concise and readable.

Due to the many similarities between scope functions, choosing the right one for your use case can be tricky. The choice mainly depends on your intent and the consistency of use in your project. Below, we provide detailed descriptions of the differences between scope functions and their conventions.

## Function selection

To help you choose the right scope function for your purpose, we provide this table that summarizes the key differences between them.

| Function | Object reference | Return value | Is extension function |
| --- | --- | --- | --- |
| [`let`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/let.html) | `it` | Lambda result | Yes |
| [`run`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/run.html) | `this` | Lambda result | Yes |
| [`run`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/run.html) | - | Lambda result | No: called without the context object |
| [`with`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/with.html) | `this` | Lambda result | No: takes the context object as an argument. |
| [`apply`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/apply.html) | `this` | Context object | Yes |
| [`also`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/also.html) | `it` | Context object | Yes |

Detailed information about these functions is provided in the dedicated sections below.

Here is a short guide for choosing scope functions depending on the intended purpose:

* Executing a lambda on non-nullable objects: `let`
* Introducing an expression as a variable in local scope: `let`
* Object configuration: `apply`
* Object configuration and computing the result: `run`
* Running statements where an expression is required: non-extension `run`
* Additional effects: `also`
* Grouping function calls on an object: `with`

The use cases of different scope functions overlap, so you can choose which functions to use based on the specific conventions used in your project or team.

Although scope functions can make your code more concise, avoid overusing them: it can make your code hard to read and lead to errors. We also recommend that you avoid nesting scope functions and be careful when chaining them because it's easy to get confused about the current context object and value of `this` or `it`.

## Distinctions

Because scope functions are similar in nature, it's important to understand the differences between them. There are two main differences between each scope function:

* The way they refer to the context object.
* Their return value.

### Context object: this or it

Inside the lambda passed to a scope function, the context object is available by a short reference instead of its actual name. Each scope function uses one of two ways to reference the context object: as a lambda [receiver](lambdas.html#function-literals-with-receiver) (`this`) or as a lambda argument (`it`). Both provide the same capabilities, so we describe the pros and cons of each for different use cases and provide recommendations for their use.

fun main() {
val str = "Hello"
// this
str.run {
println("The string's length: $length")
//println("The string's length: ${this.length}") // does the same
}
// it
str.let {
println("The string's length is ${it.length}")
}
}

#### this

`run`, `with`, and `apply` reference the context object as a lambda [receiver](lambdas.html#function-literals-with-receiver) - by keyword `this`. Hence, in their lambdas, the object is available as it would be in ordinary class functions.

In most cases, you can omit `this` when accessing the members of the receiver object, making the code shorter. On the other hand, if `this` is omitted, it can be hard to distinguish between the receiver members and external objects or functions. So having the context object as a receiver (`this`) is recommended for lambdas that mainly operate on the object's members by calling its functions or assigning values to properties.

data class Person(var name: String, var age: Int = 0, var city: String = "")
fun main() {
//sampleStart
val adam = Person("Adam").apply {
age = 20 // same as this.age = 20
city = "London"
}
println(adam)
//sampleEnd
}

#### it

In turn, `let` and `also` reference the context object as a lambda [argument](lambdas.html#lambda-expression-syntax). If the argument name is not specified, the object is accessed by the implicit default name `it`. `it` is shorter than `this` and expressions with `it` are usually easier to read.

However, when calling the object's functions or properties, you don't have the object available implicitly like `this`. Hence, accessing the context object via `it` is better when the object is mostly used as an argument in function calls. `it` is also better if you use multiple variables in the code block.

import kotlin.random.Random
fun writeToLog(message: String) {
println("INFO: $message")
}
fun main() {
//sampleStart
fun getRandomInt(): Int {
return Random.nextInt(100).also {
writeToLog("getRandomInt() generated value $it")
}
}
val i = getRandomInt()
println(i)
//sampleEnd
}

The example below demonstrates referencing the context object as a lambda argument with argument name: `value`.

import kotlin.random.Random
fun writeToLog(message: String) {
println("INFO: $message")
}
fun main() {
//sampleStart
fun getRandomInt(): Int {
return Random.nextInt(100).also { value ->
writeToLog("getRandomInt() generated value $value")
}
}
val i = getRandomInt()
println(i)
//sampleEnd
}

### Return value

Scope functions differ by the result they return:

* `apply` and `also` return the context object.
* `let`, `run`, and `with` return the lambda result.

You should consider carefully what return value you want based on what you want to do next in your code. This helps you to choose the best scope function to use.

#### Context object

The return value of `apply` and `also` is the context object itself. Hence, they can be included into call chains as side steps: you can continue chaining function calls on the same object, one after another.

fun main() {
//sampleStart
val numberList = mutableListOf<Double>()
numberList.also { println("Populating the list") }
.apply {
add(2.71)
add(3.14)
add(1.0)
}
.also { println("Sorting the list") }
.sort()
//sampleEnd
println(numberList)
}

They also can be used in return statements of functions returning the context object.

import kotlin.random.Random
fun writeToLog(message: String) {
println("INFO: $message")
}
fun main() {
//sampleStart
fun getRandomInt(): Int {
return Random.nextInt(100).also {
writeToLog("getRandomInt() generated value $it")
}
}
val i = getRandomInt()
//sampleEnd
}

#### Lambda result

`let`, `run`, and `with` return the lambda result. So you can use them when assigning the result to a variable, chaining operations on the result, and so on.

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three")
val countEndsWithE = numbers.run {
add("four")
add("five")
count { it.endsWith("e") }
}
println("There are $countEndsWithE elements that end with e.")
//sampleEnd
}

Additionally, you can ignore the return value and use a scope function to create a temporary scope for local variables.

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three")
with(numbers) {
val firstItem = first()
val lastItem = last()
println("First item: $firstItem, last item: $lastItem")
}
//sampleEnd
}

## Functions

To help you choose the right scope function for your use case, we describe them in detail and provide recommendations for use. Technically, scope functions are interchangeable in many cases, so the examples show conventions for using them.

### let

* The context object is available as an argument (`it`).
* The return value is the lambda result.

[`let`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/let.html) can be used to invoke one or more functions on results of call chains. For example, the following code prints the results of two operations on a collection:

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three", "four", "five")
val resultList = numbers.map { it.length }.filter { it > 3 }
println(resultList)
//sampleEnd
}

With `let`, you can rewrite the above example so that you're not assigning the result of the list operations to a variable:

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three", "four", "five")
numbers.map { it.length }.filter { it > 3 }.let {
println(it)
// and more function calls if needed
}
//sampleEnd
}

If the code block passed to `let` contains a single function with `it` as an argument, you can use the method reference (`::`) instead of the lambda argument:

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three", "four", "five")
numbers.map { it.length }.filter { it > 3 }.let(::println)
//sampleEnd
}

`let` is often used to execute a code block containing non-null values. To perform actions on a nullable object, use the [safe call operator `?.`](null-safety.html#safe-call-operator) on it and call `let` with the actions in its lambda.

fun processNonNullString(str: String) {}
fun main() {
//sampleStart
val str: String? = "Hello"
//processNonNullString(str) // compilation error: str can be null
val length = str?.let {
println("let() called on $it")
processNonNullString(it) // OK: 'it' is not null inside '?.let { }'
it.length
}
//sampleEnd
}

You can also use `let` to introduce local variables with a limited scope to make your code easier to read. To define a new variable for the context object, provide its name as the lambda argument so that it can be used instead of the default `it`.

fun main() {
//sampleStart
val numbers = listOf("one", "two", "three", "four")
val modifiedFirstItem = numbers.first().let { firstItem ->
println("The first item of the list is '$firstItem'")
if (firstItem.length >= 5) firstItem else "!" + firstItem + "!"
}.uppercase()
println("First item after modifications: '$modifiedFirstItem'")
//sampleEnd
}

### with

* The context object is available as a receiver (`this`).
* The return value is the lambda result.

As [`with`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/with.html) is not an extension function: the context object is passed as an argument, but inside the lambda, it's available as a receiver (`this`).

We recommend using `with` for calling functions on the context object when you don't need to use the returned result. In code, `with` can be read as " with this object, do the following. "

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three")
with(numbers) {
println("'with' is called with argument $this")
println("It contains $size elements")
}
//sampleEnd
}

You can also use `with` to introduce a helper object whose properties or functions are used for calculating a value.

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three")
val firstAndLast = with(numbers) {
"The first element is ${first()}," +
" the last element is ${last()}"
}
println(firstAndLast)
//sampleEnd
}

### run

* The context object is available as a receiver (`this`).
* The return value is the lambda result.

[`run`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/run.html) does the same as `with` but it is implemented as an extension function. So like `let`, you can call it on the context object using dot notation.

`run` is useful when your lambda both initializes objects and computes the return value.

class MultiportService(var url: String, var port: Int) {
fun prepareRequest(): String = "Default request"
fun query(request: String): String = "Result for query '$request'"
}
fun main() {
//sampleStart
val service = MultiportService("https://example.kotlinlang.org", 80)
val result = service.run {
port = 8080
query(prepareRequest() + " to port $port")
}
// the same code written with let() function:
val letResult = service.let {
it.port = 8080
it.query(it.prepareRequest() + " to port ${it.port}")
}
//sampleEnd
println(result)
println(letResult)
}

You can also invoke `run` as a non-extension function. The non-extension variant of `run` has no context object, but it still returns the lambda result. Non-extension `run` lets you execute a block of several statements where an expression is required. In code, non-extension `run` can be read as " run the code block and compute the result. "

fun main() {
//sampleStart
val hexNumberRegex = run {
val digits = "0-9"
val hexDigits = "A-Fa-f"
val sign = "+-"
Regex("[$sign]?[$digits$hexDigits]+")
}
for (match in hexNumberRegex.findAll("+123 -FFFF !%\*& 88 XYZ")) {
println(match.value)
}
//sampleEnd
}

### apply

* The context object is available as a receiver (`this`).
* The return value is the object itself.

As [`apply`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/apply.html) returns the context object itself, we recommend that you use it for code blocks that don't return a value and that mainly operate on the members of the receiver object. The most common use case for `apply` is for object configuration. Such calls can be read as " apply the following assignments to the object. "

data class Person(var name: String, var age: Int = 0, var city: String = "")
fun main() {
//sampleStart
val adam = Person("Adam").apply {
age = 32
city = "London"
}
println(adam)
//sampleEnd
}

Another use case for `apply` is to include `apply` in multiple call chains for more complex processing.

### also

* The context object is available as an argument (`it`).
* The return value is the object itself.

[`also`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/also.html) is useful for performing some actions that take the context object as an argument. Use `also` for actions that need a reference to the object rather than its properties and functions, or when you don't want to shadow the `this` reference from an outer scope.

When you see `also` in code, you can read it as " and also do the following with the object. "

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three")
numbers
.also { println("The list elements before adding new one: $it") }
.add("four")
//sampleEnd
}

## takeIf and takeUnless

In addition to scope functions, the standard library contains the functions [`takeIf`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/take-if.html) and [`takeUnless`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/take-unless.html). These functions let you embed checks of an object's state in call chains.

When called on an object along with a predicate, `takeIf` returns this object if it satisfies the given predicate. Otherwise, it returns `null`. So, `takeIf` is a filtering function for a single object.

`takeUnless` has the opposite logic of `takeIf`. When called on an object along with a predicate, `takeUnless` returns `null` if it satisfies the given predicate. Otherwise, it returns the object.

When using `takeIf` or `takeUnless`, the object is available as a lambda argument (`it`).

import kotlin.random.\*
fun main() {
//sampleStart
val number = Random.nextInt(100)
val evenOrNull = number.takeIf { it % 2 == 0 }
val oddOrNull = number.takeUnless { it % 2 == 0 }
println("even: $evenOrNull, odd: $oddOrNull")
//sampleEnd
}

fun main() {
//sampleStart
val str = "Hello"
val caps = str.takeIf { it.isNotEmpty() }?.uppercase()
//val caps = str.takeIf { it.isNotEmpty() }.uppercase() //compilation error
println(caps)
//sampleEnd
}

`takeIf` and `takeUnless` are especially useful in combination with scope functions. For example, you can chain `takeIf` and `takeUnless` with `let` to run a code block on objects that match the given predicate. To do this, call `takeIf` on the object and then call `let` with a safe call (`?`). For objects that don't match the predicate, `takeIf` returns `null` and `let` isn't invoked.

fun main() {
//sampleStart
fun displaySubstringPosition(input: String, sub: String) {
input.indexOf(sub).takeIf { it >= 0 }?.let {
println("The substring $sub is found in $input.")
println("Its start position is $it.")
}
}
displaySubstringPosition("010000011", "11")
displaySubstringPosition("010000011", "12")
//sampleEnd
}

For comparison, below is an example of how the same function can be written without using `takeIf` or scope functions:

fun main() {
//sampleStart
fun displaySubstringPosition(input: String, sub: String) {
val index = input.indexOf(sub)
if (index >= 0) {
println("The substring $sub is found in $input.")
println("Its start position is $index.")
}
}
displaySubstringPosition("010000011", "11")
displaySubstringPosition("010000011", "12")
//sampleEnd
}

05 November 2025

---

## 4. Type-safe builders

By using well-named functions as builders in combination with [function literals with receiver](lambdas.html#function-literals-with-receiver) it is possible to create type-safe, statically-typed builders in Kotlin.

Type-safe builders allow creating Kotlin-based domain-specific languages (DSLs) suitable for building complex hierarchical data structures in a semi-declarative way. Sample use cases for the builders are:

* Generating markup with Kotlin code, such as [HTML](https://github.com/Kotlin/kotlinx.html) or XML
* Configuring routes for a web server: [Ktor](https://ktor.io/docs/routing.html)

Consider the following code:

package html
fun main() {
//sampleStart
val result = html {
head {
title { +"HTML encoding with Kotlin" }
}
body {
h1 { +"HTML encoding with Kotlin" }
p {
+"this format can be used as an"
+"alternative markup to HTML"
}
// An element with attributes and text content
a(href = "http://kotlinlang.org") { +"Kotlin" }
// Mixed content
p {
+"This is some"
b { +"mixed" }
+"text. For more see the"
a(href = "http://kotlinlang.org") {
+"Kotlin"
}
+"project"
}
p {
+"some text"
ul {
for (i in 1..5)
li { +"${i}\*2 = ${i\*2}" }
}
}
}
}
//sampleEnd
println(result)
}
interface Element {
fun render(builder: StringBuilder, indent: String)
}
class TextElement(val text: String) : Element {
override fun render(builder: StringBuilder, indent: String) {
builder.append("$indent$text\n")
}
}
@DslMarker
annotation class HtmlTagMarker
@HtmlTagMarker
abstract class Tag(val name: String) : Element {
val children = arrayListOf<Element>()
val attributes = hashMapOf<String, String>()
protected fun <T : Element> initTag(tag: T, init: T.() -> Unit): T {
tag.init()
children.add(tag)
return tag
}
override fun render(builder: StringBuilder, indent: String) {
builder.append("$indent<$name${renderAttributes()}>\n")
for (c in children) {
c.render(builder, indent + " ")
}
builder.append("$indent</$name>\n")
}
private fun renderAttributes(): String {
val builder = StringBuilder()
for ((attr, value) in attributes) {
builder.append(" $attr=\"$value\"")
}
return builder.toString()
}
override fun toString(): String {
val builder = StringBuilder()
render(builder, "")
return builder.toString()
}
}
abstract class TagWithText(name: String) : Tag(name) {
operator fun String.unaryPlus() {
children.add(TextElement(this))
}
}
class HTML() : TagWithText("html") {
fun head(init: Head.() -> Unit) = initTag(Head(), init)
fun body(init: Body.() -> Unit) = initTag(Body(), init)
}
class Head() : TagWithText("head") {
fun title(init: Title.() -> Unit) = initTag(Title(), init)
}
class Title() : TagWithText("title")
abstract class BodyTag(name: String) : TagWithText(name) {
fun b(init: B.() -> Unit) = initTag(B(), init)
fun p(init: P.() -> Unit) = initTag(P(), init)
fun h1(init: H1.() -> Unit) = initTag(H1(), init)
fun ul(init: UL.() -> Unit) = initTag(UL(), init)
fun a(href: String, init: A.() -> Unit) {
val a = initTag(A(), init)
a.href = href
}
}
class Body() : BodyTag("body")
class UL() : BodyTag("ul") {
fun li(init: LI.() -> Unit) = initTag(LI(), init)
}
class B() : BodyTag("b")
class LI() : BodyTag("li")
class P() : BodyTag("p")
class H1() : BodyTag("h1")
class A : BodyTag("a") {
var href: String
get() = attributes["href"]!!
set(value) {
attributes["href"] = value
}
}
fun html(init: HTML.() -> Unit): HTML {
val html = HTML()
html.init()
return html
}

<html>
<head>
<title>
HTML encoding with Kotlin
</title>
</head>
<body>
<h1>
HTML encoding with Kotlin
</h1>
<p>
this format can be used as an
alternative markup to HTML
</p>
<a href="http://kotlinlang.org">
Kotlin
</a>
<p>
This is some
<b>
mixed
</b>
text. For more see the
<a href="http://kotlinlang.org">
Kotlin
</a>
project
</p>
<p>
some text
<ul>
<li>
1\*2 = 2
</li>
<li>
2\*2 = 4
</li>
<li>
3\*2 = 6
</li>
<li>
4\*2 = 8
</li>
<li>
5\*2 = 10
</li>
</ul>
</p>
</body>
</html>

## How it works

Assume that you need to implement a type-safe builder in Kotlin. First of all, define the model you want to build. In this case you need to model HTML tags. It is easily done with a bunch of classes. For example, `HTML` is a class that describes the `<html>` tag defining children like `<head>` and `<body>`. (See its declaration [below](#full-definition-of-the-com-example-html-package).)

Now, let's recall why you can say something like this in the code:

html {
// ...
}

`html` is actually a function call that takes a [lambda expression](lambdas.html) as an argument. This function is defined as follows:

fun html(init: HTML.() -> Unit): HTML {
val html = HTML()
html.init()
return html
}

This function takes one parameter named `init`, which is itself a function. The type of the function is `HTML.() -> Unit`, which is a function type with receiver. This means that you need to pass an instance of type `HTML` (a receiver) to the function, and you can call members of that instance inside the function.

The receiver can be accessed through the `this` keyword:

html {
this.head { ... }
this.body { ... }
}

(`head` and `body` are member functions of `HTML`.)

Now, `this` can be omitted, as usual, and you get something that looks very much like a builder already:

html {
head { ... }
body { ... }
}

So, what does this call do? Let's look at the body of `html` function as defined above. It creates a new instance of `HTML`, then it initializes it by calling the function that is passed as an argument (in this example this boils down to calling `head` and `body` on the `HTML` instance), and then it returns this instance. This is exactly what a builder should do.

The `head` and `body` functions in the `HTML` class are defined similarly to `html`. The only difference is that they add the built instances to the `children` collection of the enclosing `HTML` instance:

fun head(init: Head.() -> Unit): Head {
val head = Head()
head.init()
children.add(head)
return head
}
fun body(init: Body.() -> Unit): Body {
val body = Body()
body.init()
children.add(body)
return body
}

Actually these two functions do just the same thing, so you can have a generic version, `initTag`:

protected fun <T : Element> initTag(tag: T, init: T.() -> Unit): T {
tag.init()
children.add(tag)
return tag
}

So, now your functions are very simple:

fun head(init: Head.() -> Unit) = initTag(Head(), init)
fun body(init: Body.() -> Unit) = initTag(Body(), init)

And you can use them to build `<head>` and `<body>` tags.

One other thing to be discussed here is how you add text to tag bodies. In the example above you say something like:

html {
head {
title {+"XML encoding with Kotlin"}
}
// ...
}

So basically, you just put a string inside a tag body, but there is this little `+` in front of it, so it is a function call that invokes a prefix `unaryPlus()` operation. That operation is actually defined by an extension function `unaryPlus()` that is a member of the `TagWithText` abstract class (a parent of `Title`):

operator fun String.unaryPlus() {
children.add(TextElement(this))
}

So, what the prefix `+` does here is wrapping a string into an instance of `TextElement` and adding it to the `children` collection, so that it becomes a proper part of the tag tree.

All this is defined in a package `com.example.html` that is imported at the top of the builder example above. In the last section you can read through the full definition of this package.

## Scope control: @DslMarker

When using DSLs, one might have come across the problem that too many functions can be called in the context. You can call methods of every available [implicit receiver](lambdas.html#function-literals-with-receiver) inside a lambda and therefore get an inconsistent result, like the tag `head` inside another `head`:

html {
head {
head {} // should be forbidden
}
// ...
}

In this example only members of the nearest implicit receiver `this@head` must be available; `head()` is a member of the outer receiver `this@html`, so it must be illegal to call it.

To address this problem, there is a special mechanism to control receiver scope.

To make the compiler start controlling scopes you only have to annotate the types of all receivers used in the DSL with the same marker annotation. For instance, for HTML Builders you declare an annotation `@HtmlTagMarker`:

@DslMarker
@Target(AnnotationTarget.CLASS)
annotation class HtmlTagMarker

An annotation class is called a DSL marker if it is annotated with the `@DslMarker` annotation.

The `@Target` annotation restricts where `@HtmlTagMarker` can be applied. DSL markers only affect scope control when applied to:

* Type declarations (`CLASS`): classes or interfaces used as DSL receivers.
* Type usages (`TYPE`): receiver types in function type signatures.
* Type aliases (`TYPEALIAS`): type aliases that expand to DSL receiver types.

Applying a DSL marker to other targets (such as functions or properties) has no effect on scope control.

In our DSL all the tag classes extend the same superclass `Tag`. It's enough to annotate only the superclass with `@HtmlTagMarker` and after that the Kotlin compiler will treat all the inherited classes as annotated:

@HtmlTagMarker
abstract class Tag(val name: String) { ... }

You don't have to annotate the `HTML` or `Head` classes with `@HtmlTagMarker` because their superclass is already annotated:

class HTML() : Tag("html") { ... }
class Head() : Tag("head") { ... }

After you've added this annotation, the Kotlin compiler knows which implicit receivers are part of the same DSL and allows to call members of the nearest receivers only:

html {
head {
head { } // error: a member of outer receiver
}
// ...
}

Note that it's still possible to call the members of the outer receiver, but to do that you have to specify this receiver explicitly:

html {
head {
this@html.head { } // possible
}
// ...
}

You can also apply the `@DslMarker` annotation directly to [function types](lambdas.html#function-types). This requires including `AnnotationTarget.TYPE` in the annotation targets:

@DslMarker
@Target(AnnotationTarget.CLASS, AnnotationTarget.TYPE)
annotation class HtmlTagMarker

As a result, the `@DslMarker` annotation can be applied to function types, most commonly to lambdas with receivers. For example:

fun html(init: @HtmlTagMarker HTML.() -> Unit): HTML { ... }
fun HTML.head(init: @HtmlTagMarker Head.() -> Unit): Head { ... }
fun Head.title(init: @HtmlTagMarker Title.() -> Unit): Title { ... }

When you call these functions, the `@DslMarker` annotation restricts access to outer receivers in the body of a lambda marked with it unless you specify them explicitly:

html {
head {
title {
// Access to title, head or other functions of outer receivers is restricted here.
}
}
}

Only the nearest receiver's members and extensions are accessible within a lambda, preventing unintended interactions between nested scopes.

When both a member of an implicit receiver and a declaration from a [context parameter](context-parameters.html) are in a scope with the same name, the compiler reports a warning because the implicit receiver is shadowed by the context parameter. To resolve this, use a `this` qualifier to explicitly call the receiver, or use `contextOf<T>()` to call the context declaration:

interface HtmlTag {
fun setAttribute(name: String, value: String)
}
// Declares a top-level function with the same name,
// which is available through a context parameter
context(tag: HtmlTag)
fun setAttribute(name: String, value: String) { tag.setAttribute(name, value) }
fun test(head: HtmlTag, extraInfo: HtmlTag) {
with(head) {
// Introduces a context value of the same type in an inner scope
context(extraInfo) {
// Reports a warning:
// Uses an implicit receiver shadowed by a context parameter
setAttribute("user", "1234")
// Calls the receiver's member explicitly
this.setAttribute("user", "1234")
// Calls the context declaration explicitly
contextOf<HtmlTag>().setAttribute("user", "1234")
}
}
}

### Full definition of the com.example.html package

This is how the package `com.example.html` is defined (only the elements used in the example above). It builds an HTML tree. It makes heavy use of [extension functions](extensions.html) and [lambdas with receiver](lambdas.html#function-literals-with-receiver).

package com.example.html
interface Element {
fun render(builder: StringBuilder, indent: String)
}
class TextElement(val text: String) : Element {
override fun render(builder: StringBuilder, indent: String) {
builder.append("$indent$text\n")
}
}
@DslMarker
@Target(AnnotationTarget.CLASS, AnnotationTarget.TYPE)
annotation class HtmlTagMarker
@HtmlTagMarker
abstract class Tag(val name: String) : Element {
val children = arrayListOf<Element>()
val attributes = hashMapOf<String, String>()
protected fun <T : Element> initTag(tag: T, init: T.() -> Unit): T {
tag.init()
children.add(tag)
return tag
}
override fun render(builder: StringBuilder, indent: String) {
builder.append("$indent<$name${renderAttributes()}>\n")
for (c in children) {
c.render(builder, indent + " ")
}
builder.append("$indent</$name>\n")
}
private fun renderAttributes(): String {
val builder = StringBuilder()
for ((attr, value) in attributes) {
builder.append(" $attr=\"$value\"")
}
return builder.toString()
}
override fun toString(): String {
val builder = StringBuilder()
render(builder, "")
return builder.toString()
}
}
abstract class TagWithText(name: String) : Tag(name) {
operator fun String.unaryPlus() {
children.add(TextElement(this))
}
}
class HTML : TagWithText("html") {
fun head(init: Head.() -> Unit) = initTag(Head(), init)
fun body(init: Body.() -> Unit) = initTag(Body(), init)
}
class Head : TagWithText("head") {
fun title(init: Title.() -> Unit) = initTag(Title(), init)
}
class Title : TagWithText("title")
abstract class BodyTag(name: String) : TagWithText(name) {
fun b(init: B.() -> Unit) = initTag(B(), init)
fun p(init: P.() -> Unit) = initTag(P(), init)
fun h1(init: H1.() -> Unit) = initTag(H1(), init)
fun a(href: String, init: A.() -> Unit) {
val a = initTag(A(), init)
a.href = href
}
}
class Body : BodyTag("body")
class B : BodyTag("b")
class P : BodyTag("p")
class H1 : BodyTag("h1")
class A : BodyTag("a") {
var href: String
get() = attributes["href"]!!
set(value) {
attributes["href"] = value
}
}
fun html(init: HTML.() -> Unit): HTML {
val html = HTML()
html.init()
return html
}

02 February 2026

---

## 5. Higher-order functions and lambdas

Kotlin functions are [first-class](https://en.wikipedia.org/wiki/First-class_function), which means they can be stored in variables and data structures, and can be passed as arguments to and returned from other [higher-order functions](#higher-order-functions). You can perform any operations on functions that are possible for other non-function values.

To facilitate this, Kotlin, as a statically typed programming language, uses a family of [function types](#function-types) to represent functions, and provides a set of specialized language constructs, such as [lambda expressions](#lambda-expressions-and-anonymous-functions).

## Higher-order functions

A higher-order function is a function that takes functions as parameters, or returns a function.

A good example of a higher-order function is the [functional programming idiom `fold`](https://en.wikipedia.org/wiki/Fold_(higher-order_function)) for collections. It takes an initial accumulator value and a combining function and builds its return value by consecutively combining the current accumulator value with each collection element, replacing the accumulator value each time:

fun <T, R> Collection<T>.fold(
initial: R,
combine: (acc: R, nextElement: T) -> R
): R {
var accumulator: R = initial
for (element: T in this) {
accumulator = combine(accumulator, element)
}
return accumulator
}

In the code above, the `combine` parameter has the [function type](#function-types) `(R, T) -> R`, so it accepts a function that takes two arguments of types `R` and `T` and returns a value of type `R`. It is [invoked](#invoking-a-function-type-instance) inside the `for` loop, and the return value is then assigned to `accumulator`.

To call `fold`, you need to pass an [instance of the function type](#instantiating-a-function-type) to it as an argument, and lambda expressions ([described in more detail below](#lambda-expressions-and-anonymous-functions)) are widely used for this purpose at higher-order function call sites:

fun main() {
//sampleStart
val items = listOf(1, 2, 3, 4, 5)
// Lambdas are code blocks enclosed in curly braces.
items.fold(0, {
// When a lambda has parameters, they go first, followed by '->'
acc: Int, i: Int ->
print("acc = $acc, i = $i, ")
val result = acc + i
println("result = $result")
// The last expression in a lambda is considered the return value:
result
})
// Parameter types in a lambda are optional if they can be inferred:
val joinedToString = items.fold("Elements:", { acc, i -> acc + " " + i })
// Function references can also be used for higher-order function calls:
val product = items.fold(1, Int::times)
//sampleEnd
println("joinedToString = $joinedToString")
println("product = $product")
}

## Function types

Kotlin uses function types, such as `(Int) -> String`, for declarations that deal with functions: `val onClick: () -> Unit = ...`.

These types have a special notation that corresponds to the signatures of the functions - their parameters and return values:

* All function types have a parenthesized list of parameter types and a return type: `(A, B) -> C` denotes a type that represents functions that take two arguments of types `A` and `B` and return a value of type `C`. The list of parameter types may be empty, as in `() -> A`. The [`Unit` return type](functions.html#unit-returning-functions) cannot be omitted.
* Function types can optionally have an additional receiver type, which is specified before the dot in the notation: the type `A.(B) -> C` represents functions that can be called on a receiver object `A` with a parameter `B` and return a value `C`. [Function literals with receiver](#function-literals-with-receiver) are often used along with these types.
* [Suspending functions](coroutines-basics.html) belong to a special kind of function type that have a suspend modifier in their notation, such as `suspend () -> Unit` or `suspend A.(B) -> C`.

The function type notation can optionally include names for the function parameters: `(x: Int, y: Int) -> Point`. These names can be used for documenting the meaning of the parameters.

To specify that a function type is [nullable](null-safety.html#nullable-types-and-non-nullable-types), use parentheses as follows: `((Int, Int) -> Int)?`.

Function types can also be combined using parentheses: `(Int) -> ((Int) -> Unit)`.

You can also give a function type an alternative name by using [a type alias](type-aliases.html):

typealias ClickHandler = (Button, ClickEvent) -> Unit

### Instantiating a function type

There are several ways to obtain an instance of a function type:

* Use a code block within a function literal, in one of the following forms:

  + a [lambda expression](#lambda-expressions-and-anonymous-functions): `{ a, b -> a + b }`,
  + an [anonymous function](#anonymous-functions): `fun(s: String): Int { return s.toIntOrNull() ?: 0 }`

  [Function literals with receiver](#function-literals-with-receiver) can be used as values of function types with receiver.
* Use a callable reference to an existing declaration:

  + a top-level, local, member, or extension [function](reflection.html#function-references): `::isOdd`, `String::toInt`,
  + a top-level, member, or extension [property](reflection.html#property-references): `List<Int>::size`,
  + a [constructor](reflection.html#constructor-references): `::Regex`

  These include [bound callable references](reflection.html#bound-function-and-property-references) that point to a member of a particular instance: `foo::toString`.
* Use instances of a custom class that implements a function type as an interface:

class IntTransformer: (Int) -> Int {
override operator fun invoke(x: Int): Int = TODO()
}
val intFunction: (Int) -> Int = IntTransformer()

The compiler can infer the function types for variables if there is enough information:

val a = { i: Int -> i + 1 } // The inferred type is (Int) -> Int

Non-literal values of function types with and without a receiver are interchangeable, so the receiver can stand in for the first parameter, and vice versa. For instance, a value of type `(A, B) -> C` can be passed or assigned where a value of type `A.(B) -> C` is expected, and the other way around:

fun main() {
//sampleStart
val repeatFun: String.(Int) -> String = { times -> this.repeat(times) }
val twoParameters: (String, Int) -> String = repeatFun // OK
fun runTransformation(f: (String, Int) -> String): String {
return f("hello", 3)
}
val result = runTransformation(repeatFun) // OK
//sampleEnd
println("result = $result")
}

### Invoking a function type instance

A value of a function type can be invoked by using its [`invoke(...)` operator](operator-overloading.html#invoke-operator): `f.invoke(x)` or just `f(x)`.

If the value has a receiver type, the receiver object should be passed as the first argument. Another way to invoke a value of a function type with receiver is to prepend it with the receiver object, as if the value were an [extension function](extensions.html): `1.foo(2)`.

Example:

fun main() {
//sampleStart
val stringPlus: (String, String) -> String = String::plus
val intPlus: Int.(Int) -> Int = Int::plus
println(stringPlus.invoke("<-", "->"))
println(stringPlus("Hello, ", "world!"))
println(intPlus.invoke(1, 1))
println(intPlus(1, 2))
println(2.intPlus(3)) // extension-like call
//sampleEnd
}

### Inline functions

Sometimes it is beneficial to use [inline functions](inline-functions.html), which provide flexible control flow, for higher-order functions.

## Lambda expressions and anonymous functions

Lambda expressions and anonymous functions are function literals. Function literals are functions that are not declared but are passed immediately as an expression. Consider the following example:

max(strings, { a, b -> a.length < b.length })

The function `max` is a higher-order function, as it takes a function value as its second argument. This second argument is an expression that is itself a function, called a function literal, which is equivalent to the following named function:

fun compare(a: String, b: String): Boolean = a.length < b.length

You can also create a suspending lambda expression using the `suspend` keyword. A suspending lambda has the function type `suspend () -> Unit` and can call other suspending functions:

val suspendingTask = suspend { doSuspendingWork() }

### Lambda expression syntax

The full syntactic form of lambda expressions is as follows:

val sum: (Int, Int) -> Int = { x: Int, y: Int -> x + y }

* A lambda expression is always surrounded by curly braces.
* Parameter declarations in the full syntactic form go inside curly braces and have optional type annotations.
* The body goes after the `->`.
* If the inferred return type of the lambda is not `Unit`, the last (or possibly single) expression inside the lambda body is treated as the return value.

If you leave all the optional annotations out, what's left looks like this:

val sum = { x: Int, y: Int -> x + y }

### Passing trailing lambdas

According to Kotlin convention, if the last parameter of a function is a function, then a lambda expression passed as the corresponding argument can be placed outside the parentheses:

val product = items.fold(1) { acc, e -> acc \* e }

Such syntax is also known as trailing lambda.

If the lambda is the only argument in that call, the parentheses can be omitted entirely:

run { println("...") }

### it: implicit name of a single parameter

It's very common for a lambda expression to have only one parameter.

If the compiler can parse the signature without any parameters, the parameter does not need to be declared and `->` can be omitted. The parameter will be implicitly declared under the name `it`:

ints.filter { it > 0 } // this literal is of type '(it: Int) -> Boolean'

### Returning a value from a lambda expression

You can explicitly return a value from the lambda using the [qualified return](returns.html#return-to-labels) syntax. Otherwise, the value of the last expression is implicitly returned.

Therefore, the two following snippets are equivalent:

ints.filter {
val shouldFilter = it > 0
shouldFilter
}
ints.filter {
val shouldFilter = it > 0
return@filter shouldFilter
}

This convention, along with [passing a lambda expression outside of parentheses](#passing-trailing-lambdas), allows for [LINQ-style](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) code:

strings.filter { it.length == 5 }.sortedBy { it }.map { it.uppercase() }

### Underscore for unused variables

If the lambda parameter is unused, you can place an underscore instead of its name:

map.forEach { (\_, value) -> println("$value!") }

### Destructuring in lambdas

Destructuring in lambdas is described as a part of [destructuring declarations](destructuring-declarations.html#destructuring-in-lambdas).

### Anonymous functions

The lambda expression syntax above is missing one thing – the ability to specify the function's return type. In most cases, this is unnecessary because the return type can be inferred automatically. However, if you do need to specify it explicitly, you can use an alternative syntax: an anonymous function.

fun(x: Int, y: Int): Int = x + y

An anonymous function looks very much like a regular function declaration, except its name is omitted. Its body can be either an expression (as shown above) or a block:

fun(x: Int, y: Int): Int {
return x + y
}

The parameters and the return type are specified in the same way as for regular functions, except the parameter types can be omitted if they can be inferred from the context:

ints.filter(fun(item) = item > 0)

The return type inference for anonymous functions works just like for normal functions: the return type is inferred automatically for anonymous functions with an expression body, but it has to be specified explicitly (or is assumed to be `Unit`) for anonymous functions with a block body.

Another difference between lambda expressions and anonymous functions is the behavior of [non-local returns](inline-functions.html#returns). A `return` statement without a label always returns from the function declared with the `fun` keyword. This means that a `return` inside a lambda expression will return from the enclosing function, whereas a `return` inside an anonymous function will return from the anonymous function itself.

### Closures

A lambda expression or anonymous function (as well as a [local function](functions.html#local-functions) and an [object expression](object-declarations.html#object-expressions)) can access its closure, which includes the variables declared in the outer scope. The variables captured in the closure can be modified in the lambda:

ints.filter { it > 0 }.forEach {
sum += it
}
print(sum)

### Function literals with receiver

[Function types](#function-types) with receiver, such as `A.(B) -> C`, can be instantiated with a special form of function literals – function literals with receiver.

As mentioned above, Kotlin provides the ability [to call an instance](#invoking-a-function-type-instance) of a function type with receiver while providing the receiver object.

Inside the body of the function literal, the receiver object passed to a call becomes an implicit `this`, so that you can access the members of that receiver object without any additional qualifiers, or access the receiver object using a [`this` expression](this-expressions.html).

This behavior is similar to that of [extension functions](extensions.html), which also allow you to access the members of the receiver object inside the function body.

Here is an example of a function literal with receiver along with its type, where `plus` is called on the receiver object:

val sum: Int.(Int) -> Int = { other -> plus(other) }

The anonymous function syntax allows you to specify the receiver type of a function literal directly. This can be useful if you need to declare a variable of a function type with receiver, and then to use it later.

val sum = fun Int.(other: Int): Int = this + other

Lambda expressions can be used as function literals with receiver when the receiver type can be inferred from the context. One of the most important examples of their usage is [type-safe builders](type-safe-builders.html):

class HTML {
fun body() { ... }
}
fun html(init: HTML.() -> Unit): HTML {
val html = HTML() // create the receiver object
html.init() // pass the receiver object to the lambda
return html
}
html { // lambda with receiver begins here
body() // calling a method on the receiver object
}

18 November 2025

---

## 6. Functions

To declare a function in Kotlin:

* Use the `fun` keyword.
* Specify the parameters in parentheses `()`.
* Include the [return type](#return-types) if needed.

For example:

//sampleStart
// 'double' is the name of the function
// 'x' is a parameter of Int type
// The expected return value is of Int type too
fun double(x: Int): Int {
return 2 \* x
}
//sampleEnd
fun main() {
println(double(5))
// 10
}

## Function usage

Functions are called using the standard approach:

val result = double(2)

To call a [member](classes.html) or [extension function](extensions.html#extension-functions), use a period `.`:

// Creates an instance of the Stream class and calls read()
Stream().read()

### Parameters

Declare function parameters using Pascal notation: `name: Type`. You must separate parameters using commas and give each parameter a type explicitly:

fun powerOf(number: Int, exponent: Int): Int { /\*...\*/ }

Inside the body of a function, received arguments are read-only (implicitly declared as `val`):

fun powerOf(number: Int, exponent: Int): Int {
number = 2 // Error: 'val' cannot be reassigned.
}

You can use a [trailing comma](coding-conventions.html#trailing-commas) when declaring function parameters:

fun powerOf(
number: Int,
exponent: Int, // trailing comma
) { /\*...\*/ }

Trailing commas help with refactorings and code maintenance: you can move parameters within the declaration without worrying about which is going to be the last one.

### Parameters with default values

You can make a function parameter optional by specifying a default value for it. Kotlin uses the default value when you call the function without providing an argument that corresponds to that parameter. Parameters with default values are also known as optional parameters.

Optional parameters reduce the need for multiple overloads, since you don't have to declare different versions of a function just to allow skipping a parameter with a reasonable default.

Set a default value by appending `=` to the parameter declaration:

fun read(
b: ByteArray,
// The default value of 'off' is 0
off: Int = 0,
// The default value of 'len' is calculated
// as the size of the 'b' array
len: Int = b.size,
) { /\*...\*/ }

When you declare a parameter with a default value before a parameter without a default value, you can only use the default value by [naming the argument](#named-arguments):

fun greeting(
userId: Int = 0,
message: String,
) { /\*...\*/ }
fun main() {
// Uses 0 as the default value for 'userId'
greeting(message = "Hello!")
// Error: No value passed for parameter 'userId'
greeting("Hello!")
}

[Trailing lambdas](lambdas.html#passing-trailing-lambdas) are an exception to this rule, since the last parameter must correspond to the passed function:

fun main () {
//sampleStart
fun greeting(
userId: Int = 0,
message: () -> Unit,
)
{ println(userId)
message() }
// Uses the default value for 'userId'
greeting() { println ("Hello!") }
// 0
// Hello!
//sampleEnd
}

[Overriding methods](inheritance.html#overriding-methods) always use the base method's default parameter values. When you override a method that has default parameter values, you must omit the default parameter values from the signature:

open class Shape {
open fun draw(width: Int = 10, height: Int = 5) { /\*...\*/ }
}
class Rectangle : Shape() {
// It's not allowed to specify default values here
// but this function also uses 10 for 'width' and 5 for 'height'
// by default.
override fun draw(width: Int, height: Int) { /\*...\*/ }
}

#### Non-constant expressions as default values

You can assign a parameter a default value that isn't constant. For example, the default can be the result of a function call or a calculation that uses the values of other arguments, like the `len` parameter in this example:

fun read(
b: ByteArray,
off: Int = 0,
len: Int = b.size,
) { /\*...\*/ }

Parameters that refer to the values of other parameters must be declared later in the order. In this example, `len` must be declared after `b`.

In general, you can assign any expression as the default value of a parameter. However, default values are only evaluated when the function is called without the corresponding parameter and a default value needs to be assigned. For example, this function prints out a line only when it is called without the `print` parameter:

fun main() {
//sampleStart
fun read(
b: Int,
print: Unit? = println("No argument passed for 'print'")
) { println(b) }
// Prints "No argument passed for 'print'", then "1"
read(1)
// Prints only "1"
read(1, null)
//sampleEnd
}

If the last parameter in a function declaration has a functional type, you can pass the corresponding [lambda](lambdas.html#lambda-expression-syntax) argument either as a named argument or [outside the parentheses](lambdas.html#passing-trailing-lambdas):

fun main() {
//sampleStart
fun log(
level: Int = 0,
code: Int = 1,
action: () -> Unit,
) { println (level)
println (code)
action() }
// Passes 1 for 'level' and uses the default value 1 for 'code'
log(1) { println("Connection established") }
// Uses both default values, 0 for 'level' and 1 for 'code'
log(action = { println("Connection established") })
// Equivalent to the previous call, uses both default values
log { println("Connection established") }
//sampleEnd
}

### Named arguments

You can name one or more of a function's arguments when calling it. This can be helpful when a function call has many arguments. In such cases, it's difficult to associate a value with an argument, especially if it's `null` or a boolean value.

When you use named arguments in a function call, you can list them in any order.

Consider the `reformat()` function, which has 4 arguments with default values:

fun reformat(
str: String,
normalizeCase: Boolean = true,
upperCaseFirstLetter: Boolean = true,
divideByCamelHumps: Boolean = false,
wordSeparator: Char = ' ',
) { /\*...\*/ }

When calling this function, you can name some of the arguments:

reformat(
"String!",
normalizeCase = false,
upperCaseFirstLetter = false,
divideByCamelHumps = true,
'\_'
)

You can skip all the arguments with default values:

reformat("This is a long String!")

You can also skip some arguments with default values, rather than omitting them all. However, after the first skipped argument, you must name all subsequent arguments:

reformat(
"This is a short String!",
upperCaseFirstLetter = false,
wordSeparator = '\_'
)

You can pass a [variable number of arguments](#variable-number-of-arguments-varargs) (`vararg`) by naming the corresponding argument. In this example, it's an array:

fun mergeStrings(vararg strings: String) { /\*...\*/ }
mergeStrings(strings = arrayOf("a", "b", "c"))

### Return types

When you declare a function with a block body (by putting instructions within curly braces `{}`), you must always specify a return type explicitly. The only exception is when they return `Unit`, [in which case specifying the return type is optional](#unit-returning-functions).

Kotlin doesn't infer return types for functions with block bodies. Their control flow can be complex, which makes the return type unclear to the reader and sometimes even to the compiler. However, Kotlin can infer the return type for [single-expression functions](#single-expression-functions) if you don't specify it.

### Single-expression functions

When the function body consists of a single expression, you can omit the curly braces and specify the body after an `=` symbol:

fun double(x: Int): Int = x \* 2

Most of the time you don't have to explicitly declare [the return type](#return-types):

// Compiler infers that the function returns Int
fun double(x: Int) = x \* 2

The compiler can sometimes run into problems when inferring return types from single expressions. In such cases, you should add the return type explicitly. For example, functions that are recursive or mutually recursive (calling each other) and functions with typeless expressions like `fun empty() = null` always require a return type.

When you do use an inferred return type, make sure to check the actual result because the compiler may infer a type that is less useful to you. In the example above, if you want the `double()` function to return `Number` instead of `Int`, you have to declare this explicitly.

### Unit-returning functions

If a function has a block body (instructions within curly braces `{}`) and does not return a useful value, the compiler assumes its return type is `Unit`. `Unit` is a type that has only one value, also called `Unit`.

You don't have to specify `Unit` as a return type, except for functional type parameters. You never have to return `Unit` explicitly.

For example, you can declare a `printHello()` function without returning `Unit`:

// The declaration of the functional type parameter ('action') still
// needs an explicit return type
fun printHello(name: String?, action: () -> Unit) {
if (name != null)
println("Hello $name")
else
println("Hi there!")
action()
}
fun main() {
printHello("Kodee") {
println("This runs after the greeting.")
}
// Hello Kodee
// This runs after the greeting.
printHello(null) {
println("No name provided, but action still runs.")
}
// No name provided, but action still runs
}

Which is equivalent to this verbose declaration:

//sampleStart
fun printHello(name: String?, action: () -> Unit): Unit {
if (name != null)
println("Hello $name")
else
println("Hi there!")
action()
return Unit
}
//sampleEnd
fun main() {
printHello("Kodee") {
println("This runs after the greeting.")
}
// Hello Kodee
// This runs after the greeting.
printHello(null) {
println("No name provided, but action still runs.")
}
// No name provided, but action still runs
}

You can use a `return` statement inside an expression body if the function's return type is specified explicitly:

fun getDisplayNameOrDefault(userId: String?): String =
getDisplayName(userId ?: return "default")

### Variable number of arguments (varargs)

To pass a variable number of arguments to a function, you can mark one of its parameters (usually the last one) with the `vararg` modifier. Inside a function, you can use a `vararg`-parameter of type `T` as an array of `T`:

fun <T> asList(vararg ts: T): List<T> {
val result = ArrayList<T>()
for (t in ts) // ts is an Array
result.add(t)
return result
}

Then you can pass a variable number of arguments to the function:

fun <T> asList(vararg ts: T): List<T> {
val result = ArrayList<T>()
for (t in ts) // ts is an Array
result.add(t)
return result
}
fun main() {
//sampleStart
val list = asList(1, 2, 3)
println(list)
// [1, 2, 3]
//sampleEnd
}

Only one parameter can be marked as `vararg`. If you declare a `vararg` parameter anywhere other than last in the parameter list, you must pass values for the following parameters using named arguments. If a parameter has a function type, you can also pass its value by placing a lambda outside the parentheses.

When you call a `vararg`-function, you can pass arguments individually, as in the example of `asList(1, 2, 3)`. If you already have an array and want to pass its contents to a function as a `vararg` parameter or as a part of it, use the [spread operator](arrays.html#pass-variable-number-of-arguments-to-a-function) by prefixing the array name with `*`:

fun <T> asList(vararg ts: T): List<T> {
val result = ArrayList<T>()
for (t in ts)
result.add(t)
return result
}
fun main() {
//sampleStart
val a = arrayOf(1, 2, 3)
// The function receives the array [-1, 0, 1, 2, 3, 4]
list = asList(-1, 0, \*a, 4)
println(list)
// [-1, 0, 1, 2, 3, 4]
//sampleEnd
}

If you want to pass a [primitive type array](arrays.html#primitive-type-arrays) as `vararg`, you need to convert it to a regular (typed) array using the [`.toTypedArray()`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/to-typed-array.html) function:

// 'a' is an IntArray, which is a primitive type array
val a = intArrayOf(1, 2, 3)
val list = asList(-1, 0, \*a.toTypedArray(), 4)

### Infix notation

You can declare functions that can be called without parentheses or the period by using the `infix` keyword. This can help make simple function calls in your code easier to read.

infix fun Int.shl(x: Int): Int { /\*...\*/ }
// Calls the function using the general notation
1.shl(2)
// Calls the function using the infix notation
1 shl 2

Infix functions must meet the following requirements:

* They must be member functions of a class or [extension functions](extensions.html).
* They must have a single parameter.
* The parameter must not [accept a variable number of arguments](#variable-number-of-arguments-varargs) (`vararg`) and must have no [default value](#parameters-with-default-values).

Note that infix functions always require both the receiver and the parameter to be specified. When you call a method on the current receiver using the infix notation, use `this` explicitly. This ensures unambiguous parsing.

class MyStringCollection {
val items = mutableListOf<String>()
infix fun add(s: String) {
println("Adding: $s")
items += s
}
fun build() {
add("first") // Correct: ordinary function call
this add "second" // Correct: infix call with an explicit receiver
// add "third" // Compiler error: needs an explicit receiver
}
fun printAll() = println("Items = $items")
}
fun main() {
val myStrings = MyStringCollection()
// Adds "first" and "second" to the list twice
myStrings.build()
myStrings.printAll()
// Adding: first
// Adding: second
// Items = [first, second]
}

## Function scope

You can declare Kotlin functions at the top level in a file, meaning you do not need to create a class to hold a function. Functions can also be declared locally as member functions or extension functions.

### Local functions

Kotlin supports local functions, which are functions declared inside other functions. For example, the following code implements the Depth-first search algorithm for a given graph. The local `dfs()` function inside the outer `dfs()` function to hide the implementation and handle recursive calls:

class Person(val name: String) {
val friends = mutableListOf<Person>()
}
class SocialGraph(val people: List<Person>)
//sampleStart
fun dfs(graph: SocialGraph) {
fun dfs(current: Person, visited: MutableSet<Person>) {
if (!visited.add(current)) return
println("Visited ${current.name}")
for (friend in current.friends)
dfs(friend, visited)
}
dfs(graph.people[0], HashSet())
}
//sampleEnd
fun main() {
val alice = Person("Alice")
val bob = Person("Bob")
val charlie = Person("Charlie")
alice.friends += bob
bob.friends += charlie
charlie.friends += alice
val network = SocialGraph(listOf(alice, bob, charlie))
dfs(network)
}

A local function can access local variables of outer functions (the closure). In the case above, the `visited` function parameter can be a local variable:

class Person(val name: String) {
val friends = mutableListOf<Person>()
}
class SocialGraph(val people: List<Person>)
//sampleStart
fun dfs(graph: SocialGraph) {
val visited = HashSet<Person>()
fun dfs(current: Person) {
if (!visited.add(current)) return
println("Visited ${current.name}")
for (friend in current.friends)
dfs(friend)
}
dfs(graph.people[0])
}
//sampleEnd
fun main() {
val alice = Person("Alice")
val bob = Person("Bob")
val charlie = Person("Charlie")
alice.friends += bob
bob.friends += charlie
charlie.friends += alice
val network = SocialGraph(listOf(alice, bob, charlie))
dfs(network)
}

### Member functions

A member function is a function that is defined inside a class or object:

class Sample {
fun foo() { print("Foo") }
}

To call member functions, write the instance or object name, then add a `.` and write the function name:

// Creates an instance of the Stream class and calls read()
Stream().read()

For more information on classes and overriding members see [Classes](classes.html) and [Inheritance](classes.html#inheritance).

## Generic functions

You can specify generic parameters for a function by using angle brackets `<>` before the function name:

fun <T> singletonList(item: T): List<T> { /\*...\*/ }

For more information on generic functions, see [Generics](generics.html).

## Tail recursive functions

Kotlin supports a style of functional programming known as [tail recursion](https://en.wikipedia.org/wiki/Tail_call). For some algorithms that would normally use loops, you can use a recursive function instead without the risk of stack overflow. When a function is marked with the `tailrec` modifier and meets the required formal conditions, the compiler optimizes out the recursion, leaving behind a fast and efficient loop based version instead:

import kotlin.math.cos
import kotlin.math.abs
// An arbitrary "good enough" precision
val eps = 1E-10
tailrec fun findFixPoint(x: Double = 1.0): Double =
if (abs(x - cos(x)) < eps) x else findFixPoint(cos(x))

This code calculates the fixed point of cosine (a mathematical constant). The function calls `cos()` repeatedly starting at `1.0` until the result no longer changes, yielding a result of `0.7390851332151611` for the specified `eps` precision. The code is equivalent to this more traditional style:

import kotlin.math.cos
import kotlin.math.abs
// An arbitrary "good enough" precision
val eps = 1E-10
private fun findFixPoint(): Double {
while (true) {
val y = cos(x)
if (abs(x - y) < eps) return x
x = cos(x)
}
}

You can apply the `tailrec` modifier to a function only when it calls itself as its final operation. You cannot use tail recursion when there is more code after the recursive call, within [`try`/`catch`/`finally` blocks](exceptions.html#handle-exceptions-using-try-catch-blocks), or when the function is [open](inheritance.html).

See also:

* [Inline functions](inline-functions.html)
* [Extension functions](extensions.html)
* [Higher-order functions and lambdas](lambdas.html)

16 December 2025

---

## Bibliography

1. [Extensions](https://kotlinlang.org/docs/extensions.html)
2. [Inline functions](https://kotlinlang.org/docs/inline-functions.html)
3. [Scope functions](https://kotlinlang.org/docs/scope-functions.html)
4. [Type-safe builders](https://kotlinlang.org/docs/type-safe-builders.html)
5. [Higher-order functions and lambdas](https://kotlinlang.org/docs/lambdas.html)
6. [Functions](https://kotlinlang.org/docs/functions.html)