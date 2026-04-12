# Kotlin Advanced Features


---

## 1. Type aliases

Type aliases provide alternative names for existing types. If the type name is too long you can introduce a different shorter name and use the new one instead.

It's useful to shorten long generic types. For instance, it's often tempting to shrink collection types:

typealias NodeSet = Set<Network.Node>
typealias FileTable<K> = MutableMap<K, MutableList<File>>

You can provide different aliases for function types:

typealias MyHandler = (Int, String, Any) -> Unit
typealias Predicate<T> = (T) -> Boolean

You can have new names for inner and nested classes:

class A {
inner class Inner
}
class B {
inner class Inner
}
typealias AInner = A.Inner
typealias BInner = B.Inner

Type aliases do not introduce new types. They are equivalent to the corresponding underlying types. When you add `typealias Predicate<T>` and use `Predicate<Int>` in your code, the Kotlin compiler always expands it to `(Int) -> Boolean`. Thus you can pass a variable of your type whenever a general function type is required and vice versa:

typealias Predicate<T> = (T) -> Boolean
fun foo(p: Predicate<Int>) = p(42)
fun main() {
val f: (Int) -> Boolean = { it > 0 }
println(foo(f)) // prints "true"
val p: Predicate<Int> = { it > 0 }
println(listOf(1, -2).filter(p)) // prints "[1]"
}

## Nested type aliases

In Kotlin, you can define type aliases inside other declarations, as long as they don't capture type parameters from their outer class:

class Dijkstra {
typealias VisitedNodes = Set<Node>
private fun step(visited: VisitedNodes, ...) = ...
}

Capturing means that the type alias refers to a type parameter defined in the outer class:

class Graph<Node> {
// Incorrect because captures Node
typealias Path = List<Node>
}

To fix this issue, declare the type parameter directly in the type alias:

class Graph<Node> {
// Correct because Node is a type alias parameter
typealias Path<Node> = List<Node>
}

Nested type aliases allow for cleaner, more maintainable code by improving encapsulation, reducing package-level clutter, and simplifying internal implementations.

### Rules for nested type aliases

Nested type aliases follow specific rules to ensure clear and consistent behavior:

* Nested type aliases must follow all existing type alias rules.
* In terms of visibility, the alias can't expose more than its referenced types allow.
* Their scope is the same as [nested classes](nested-classes.html). You can define them inside classes, and they hide any parent type aliases with the same name as they don't override.
* Nested type aliases can be marked as `internal` or `private` to limit their visibility.
* Nested type aliases are not supported in Kotlin Multiplatform's [`expect/actual` declarations](/docs/multiplatform/multiplatform-expect-actual.html).

02 December 2025

---

## 2. Delegation

The [Delegation pattern](https://en.wikipedia.org/wiki/Delegation_pattern) has proven to be a good alternative to implementation inheritance, and Kotlin supports it natively requiring zero boilerplate code.

A class `Derived` can implement an interface `Base` by delegating all of its public members to a specified object:

interface Base {
fun print()
}
class BaseImpl(val x: Int) : Base {
override fun print() { print(x) }
}
class Derived(b: Base) : Base by b
fun main() {
val base = BaseImpl(10)
Derived(base).print()
}

The `by`-clause in the supertype list for `Derived` indicates that `b` will be stored internally in objects of `Derived` and the compiler will generate all the methods of `Base` that forward to `b`.

## Overriding a member of an interface implemented by delegation

[Overrides](inheritance.html#overriding-methods) work as you expect: the compiler will use your `override` implementations instead of those in the delegate object. If you want to add `override fun printMessage() { print("abc") }` to `Derived`, the program would print abc instead of 10 when `printMessage` is called:

interface Base {
fun printMessage()
fun printMessageLine()
}
class BaseImpl(val x: Int) : Base {
override fun printMessage() { print(x) }
override fun printMessageLine() { println(x) }
}
class Derived(b: Base) : Base by b {
override fun printMessage() { print("abc") }
}
fun main() {
val base = BaseImpl(10)
Derived(base).printMessage()
Derived(base).printMessageLine()
}

Note, however, that members overridden in this way do not get called from the members of the delegate object, which can only access its own implementations of the interface members:

interface Base {
val message: String
fun print()
}
class BaseImpl(x: Int) : Base {
override val message = "BaseImpl: x = $x"
override fun print() { println(message) }
}
class Derived(b: Base) : Base by b {
// This property is not accessed from b's implementation of `print`
override val message = "Message of Derived"
}
fun main() {
val b = BaseImpl(10)
val derived = Derived(b)
derived.print()
println(derived.message)
}

Learn more about [delegated properties](delegated-properties.html).

29 May 2024

---

## 3. Serialization

Serialization is the process of converting data used by an application to a format that can be transferred over a network or stored in a database or a file. In turn, deserialization is the opposite process of reading data from an external source and converting it into a runtime object. Together, they are essential to most applications that exchange data with third parties.

Some data serialization formats, such as [JSON](https://www.json.org/json-en.html) and [protocol buffers](https://developers.google.com/protocol-buffers) are particularly common. Being language-neutral and platform-neutral, they enable data exchange between systems written in any modern language.

In Kotlin, data serialization tools are available in a separate component, [kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization). It consists of several parts: the `org.jetbrains.kotlin.plugin.serialization` Gradle plugin, [runtime libraries](#libraries), and compiler plugins.

Compiler plugins, `kotlinx-serialization-compiler-plugin` and `kotlinx-serialization-compiler-plugin-embeddable`, are published directly to Maven Central. The second plugin is designed for working with the `kotlin-compiler-embeddable` artifact, which is the default option for scripting artifacts. Gradle adds compiler plugins to your projects as compiler arguments.

## Libraries

`kotlinx.serialization` provides sets of libraries for all supported platforms – JVM, JavaScript, Native – and for various serialization formats – JSON, CBOR, protocol buffers, and others. You can find the complete list of supported serialization formats [below](#formats).

All Kotlin serialization libraries belong to the `org.jetbrains.kotlinx:` group. Their names start with `kotlinx-serialization-` and have suffixes that reflect the serialization format. Examples:

* `org.jetbrains.kotlinx:kotlinx-serialization-json` provides JSON serialization for Kotlin projects.
* `org.jetbrains.kotlinx:kotlinx-serialization-cbor` provides CBOR serialization.

Platform-specific artifacts are handled automatically; you don't need to add them manually. Use the same dependencies in JVM, JS, Native, and multiplatform projects.

Note that the `kotlinx.serialization` libraries use their own versioning structure, which doesn't match Kotlin's versioning. Check out the releases on [GitHub](https://github.com/Kotlin/kotlinx.serialization/releases) to find the latest versions.

## Formats

`kotlinx.serialization` includes libraries for various serialization formats:

* [JSON](https://www.json.org/): [`kotlinx-serialization-json`](https://github.com/Kotlin/kotlinx.serialization/blob/master/formats/README.md#json)
* [Protocol buffers](https://developers.google.com/protocol-buffers): [`kotlinx-serialization-protobuf`](https://github.com/Kotlin/kotlinx.serialization/blob/master/formats/README.md#protobuf)
* [CBOR](https://cbor.io/): [`kotlinx-serialization-cbor`](https://github.com/Kotlin/kotlinx.serialization/blob/master/formats/README.md#cbor)
* [Properties](https://en.wikipedia.org/wiki/.properties): [`kotlinx-serialization-properties`](https://github.com/Kotlin/kotlinx.serialization/blob/master/formats/README.md#properties)
* [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md): [`kotlinx-serialization-hocon`](https://github.com/Kotlin/kotlinx.serialization/blob/master/formats/README.md#hocon) (only on JVM)

Note that all libraries except JSON serialization (`kotlinx-serialization-json`) are [Experimental](components-stability.html), which means their API can be changed without notice.

There are also community-maintained libraries that support more serialization formats, such as [YAML](https://yaml.org/) or [Apache Avro](https://avro.apache.org/). For detailed information about available serialization formats, see the [`kotlinx.serialization` documentation](https://github.com/Kotlin/kotlinx.serialization/blob/master/formats/README.md).

## Example: JSON serialization

Let's take a look at how to serialize Kotlin objects into JSON.

### Add plugins and dependencies

Before starting, you must configure your build script so that you can use Kotlin serialization tools in your project:

1. Apply the Kotlin serialization Gradle plugin `org.jetbrains.kotlin.plugin.serialization` (or `kotlin("plugin.serialization")` in the Kotlin Gradle DSL).

   plugins {
   kotlin("jvm") version "2.3.20"
   kotlin("plugin.serialization") version "2.3.20"
   }

   plugins {
   id 'org.jetbrains.kotlin.jvm' version '2.3.20'
   id 'org.jetbrains.kotlin.plugin.serialization' version '2.3.20'
   }
2. Add the JSON serialization library dependency: `org.jetbrains.kotlinx:kotlinx-serialization-json:1.10.0`

   dependencies {
   implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.10.0")
   }

   dependencies {
   implementation 'org.jetbrains.kotlinx:kotlinx-serialization-json:1.10.0'
   }

Now you're ready to use the serialization API in your code. The API is located in the `kotlinx.serialization` package and its format-specific subpackages, such as `kotlinx.serialization.json`.

### Serialize and deserialize JSON

1. Make a class serializable by annotating it with `@Serializable`.

   import kotlinx.serialization.Serializable
   @Serializable
   data class Data(val a: Int, val b: String)
2. Serialize an instance of this class by calling `Json.encodeToString()`.

   import kotlinx.serialization.Serializable
   import kotlinx.serialization.json.Json
   import kotlinx.serialization.encodeToString
   @Serializable
   data class Data(val a: Int, val b: String)
   fun main() {
   val json = Json.encodeToString(Data(42, "str"))
   }

   As a result, you get a string containing the state of this object in the JSON format: `{"a": 42, "b": "str"}`
3. Use the `decodeFromString()` function to deserialize an object from JSON:

   import kotlinx.serialization.Serializable
   import kotlinx.serialization.json.Json
   import kotlinx.serialization.decodeFromString
   @Serializable
   data class Data(val a: Int, val b: String)
   fun main() {
   val obj = Json.decodeFromString<Data>("""{"a":42, "b": "str"}""")
   }

That's it! You have successfully serialized objects into JSON strings and deserialized them back into objects.

## What's next

For more information about serialization in Kotlin, see the [Kotlin Serialization Guide](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/serialization-guide.md).

You can explore different aspects of Kotlin serialization in the following resources:

* [Learn more about Kotlin serialization and its core concepts](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/basic-serialization.md)
* [Explore the built-in serializable classes of Kotlin](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/builtin-classes.md)
* [Look at serializers in more detail and learn how to create custom serializers](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/serializers.md)
* [Discover how polymorphic serialization is handled in Kotlin](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/polymorphism.md#open-polymorphism)
* [Look into the various JSON features handling Kotlin serialization](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/json.md#json-elements)
* [Learn more about the experimental serialization formats supported by Kotlin](https://github.com/Kotlin/kotlinx.serialization/blob/master/docs/formats.md)

26 August 2025

---

## 4. Destructuring declarations

Sometimes it is convenient to destructure an object into a number of variables, for example:

val (name, age) = person

This syntax is called a destructuring declaration. A destructuring declaration creates multiple variables at once. You have declared two new variables: `name` and `age`, and can use them independently:

println(name)
println(age)

A destructuring declaration is compiled down to the following code:

val name = person.component1()
val age = person.component2()

The `component1()` and `component2()` functions are another example of the principle of conventions widely used in Kotlin (see operators like `+` and `*`, `for`-loops as an example). Anything can be on the right-hand side of a destructuring declaration, as long as the required number of component functions can be called on it. And, of course, there can be `component3()` and `component4()` and so on.

Destructuring declarations also work in `for`-loops:

for ((a, b) in collection) { ... }

Variables `a` and `b` get the values returned by `component1()` and `component2()` called on elements of the collection.

## Example: returning two values from a function

Assume that you need to return two things from a function - for example, a result object and a status of some sort. A compact way of doing this in Kotlin is to declare a [data class](data-classes.html) and return its instance:

data class Result(val result: Int, val status: Status)
fun function(...): Result {
// computations
return Result(result, status)
}
// Now, to use this function:
val (result, status) = function(...)

Since data classes automatically declare `componentN()` functions, destructuring declarations work here.

## Example: destructuring declarations and maps

Probably the nicest way to traverse a map is this:

for ((key, value) in map) {
// do something with the key and the value
}

To make this work, you should

* Present the map as a sequence of values by providing an `iterator()` function.
* Present each of the elements as a pair by providing functions `component1()` and `component2()`.

And indeed, the standard library provides such extensions:

operator fun <K, V> Map<K, V>.iterator(): Iterator<Map.Entry<K, V>> = entrySet().iterator()
operator fun <K, V> Map.Entry<K, V>.component1() = getKey()
operator fun <K, V> Map.Entry<K, V>.component2() = getValue()

So you can freely use destructuring declarations in `for`-loops with maps (as well as collections of data class instances or similar).

## Underscore for unused variables

If you don't need a variable in the destructuring declaration, you can place an underscore instead of its name:

val (\_, status) = getResult()

The `componentN()` operator functions are not called for the components that are skipped in this way.

## Destructuring in lambdas

You can use the destructuring declarations syntax for lambda parameters. If a lambda has a parameter of the `Pair` type (or `Map.Entry`, or any other type that has the appropriate `componentN` functions), you can introduce several new parameters instead of one by putting them in parentheses:

map.mapValues { entry -> "${entry.value}!" }
map.mapValues { (key, value) -> "$value!" }

Note the difference between declaring two parameters and declaring a destructuring pair instead of a parameter:

{ a -> ... } // one parameter
{ a, b -> ... } // two parameters
{ (a, b) -> ... } // a destructured pair
{ (a, b), c -> ... } // a destructured pair and another parameter

If a component of the destructured parameter is unused, you can replace it with the underscore to avoid inventing its name:

map.mapValues { (\_, value) -> "$value!" }

You can specify the type for the whole destructured parameter or for a specific component separately:

map.mapValues { (\_, value): Map.Entry<Int, String> -> "$value!" }
map.mapValues { (\_, value: String) -> "$value!" }

## Name-based destructuring

Kotlin supports name-based destructuring declarations, where variables match properties by name instead of the position defined by `componentN()` functions in position-based destructuring.

In position-based destructuring, variables correspond to the order of `componentN()` functions, for example:

data class User(val username: String, val email: String)
fun main() {
val user = User("alice", "alice@example.com")
val (email, username) = user
println(email)
// alice
println(username)
// alice@example.com
}

In this example, because destructuring relies on the order of `componentN()` functions, `email` receives the value of `username`, and `username` receives the value of `email`.

With name-based destructuring, property names determine which values are extracted rather than the position of `componentN()` functions:

fun main() {
val user = User("alice", "alice@example.com")
// Uses name-based destructuring with explicit form
(val mail = email, val name = username) = user
println(name)
// alice
println(mail)
// alice@example.com
}

Name-based destructuring is [Experimental](components-stability.html#stability-levels-explained). When you enable this feature, it also introduces a new syntax for position-based destructuring using square brackets. Use this syntax for types where the order of elements matters, such as lists and other ordered collections, as well as unnamed tuples like `Pair` or `Triple`:

val point = Pair(10, 20)
// Uses position-based destructuring
val [x, y] = point

You can control how the compiler interprets destructuring declarations with the `-Xname-based-destructuring` compiler option.

It has the following modes:

* `only-syntax` enables the explicit form of name-based destructuring without changing the behavior of existing destructuring declarations.
* `name-mismatch` reports warnings when position-based destructuring in data classes uses variable names that don't match the property names.
* `complete` enables short-form name-based destructuring with parentheses and continues supporting position-based destructuring with square bracket syntax.

If you use `complete` mode, the short-form destructuring syntax with parentheses matches variables to property names instead of relying on position:

val (email, username) = user

To enable name-based destructuring in your project, add the compiler option to your build configuration file:

kotlin {
compilerOptions {
freeCompilerArgs.add("-Xname-based-destructuring=only-syntax")
}
}

<build>
<plugins>
<plugin>
<groupId>org.jetbrains.kotlin</groupId>
<artifactId>kotlin-maven-plugin</artifactId>
<configuration>
<args>
<arg>-Xname-based-destructuring=only-syntax</arg>
</args>
</configuration>
</plugin>
</plugins>
</build>

24 March 2026

---

## 5. Null safety

Null safety is a Kotlin feature designed to significantly reduce the risk of null references, also known as [The Billion-Dollar Mistake](https://en.wikipedia.org/wiki/Null_pointer#History).

One of the most common pitfalls in many programming languages, including Java, is that accessing a member of a null reference results in a null reference exception. In Java, this would be the equivalent of a `NullPointerException`, or an NPE for short.

Kotlin explicitly supports nullability as part of its type system, meaning you can explicitly declare which variables or properties are allowed to be `null`. Also, when you declare non-null variables, the compiler enforces that these variables cannot hold a `null` value, preventing an NPE.

Kotlin's null safety ensures safer code by catching potential null-related issues at compile time rather than runtime. This feature improves code robustness, readability, and maintainability by explicitly expressing `null` values, making the code easier to understand and manage.

The only possible causes of an NPE in Kotlin are:

* An explicit call to [`throw NullPointerException()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-null-pointer-exception/).
* Usage of the [not-null assertion operator `!!`](#not-null-assertion-operator).
* Data inconsistency during initialization, such as when:

  + An uninitialized `this` available in a constructor is used somewhere else ([a "leaking `this` "](https://youtrack.jetbrains.com/issue/KTIJ-9751)).
  + A [superclass constructor calling an open member](inheritance.html#derived-class-initialization-order) whose implementation in the derived class uses an uninitialized state.
* Java interoperation:

  + Attempts to access a member of a `null` reference of a [platform type](java-interop.html#null-safety-and-platform-types).
  + Nullability issues with generic types. For example, a piece of Java code adding `null` into a Kotlin `MutableList<String>`, which would require `MutableList<String?>` to handle it properly.
  + Other issues caused by external Java code.

## Nullable types and non-nullable types

In Kotlin, the type system distinguishes between types that can hold `null` (nullable types) and those that cannot (non-nullable types). For example, a regular variable of type `String` cannot hold `null`:

fun main() {
//sampleStart
// Assigns a non-null string to a variable
var a: String = "abc"
// Attempts to re-assign null to the non-nullable variable
a = null
print(a)
// Null can not be a value of a non-null type String
//sampleEnd
}

You can safely call a method or access a property on `a`. It's guaranteed not to cause an NPE because `a` is a non-nullable variable. The compiler ensures that `a` always holds a valid `String` value, so there's no risk of accessing its properties or methods when it's `null`:

fun main() {
//sampleStart
// Assigns a non-null string to a variable
val a: String = "abc"
// Returns the length of a non-nullable variable
val l = a.length
print(l)
// 3
//sampleEnd
}

To allow `null` values, declare a variable with a `?` sign right after the variable type. For example, you can declare a nullable string by writing `String?`. This expression makes `String` a type that can accept `null`:

fun main() {
//sampleStart
// Assigns a nullable string to a variable
var b: String? = "abc"
// Successfully re-assigns null to the nullable variable
b = null
print(b)
// null
//sampleEnd
}

If you try accessing `length` directly on `b`, the compiler reports an error. This is because `b` is declared as a nullable variable and can hold `null` values. Attempting to access properties on nullables directly leads to an NPE:

fun main() {
//sampleStart
// Assigns a nullable string to a variable
var b: String? = "abc"
// Re-assigns null to the nullable variable
b = null
// Tries to directly return the length of a nullable variable
val l = b.length
print(l)
// Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type String?
//sampleEnd
}

In the example above, the compiler requires you to use safe calls to check for nullability before accessing properties or performing operations. There are several ways to handle nullables:

* [Check for `null` with the `if` conditional](#check-for-null-with-the-if-conditional)
* [Safe call operator `?.`](#safe-call-operator)
* [Elvis operator `?:`](#elvis-operator)
* [Not-null assertion operator `!!`](#not-null-assertion-operator)
* [Nullable receiver](#nullable-receiver)
* [`let` function](#let-function)
* [Safe casts `as?`](#safe-casts)
* [Collections of a nullable type](#collections-of-a-nullable-type)

Read the next sections for details and examples of `null` handling tools and techniques.

## Check for null with the if conditional

When working with nullable types, you need to handle nullability safely to avoid an NPE. One way to handle this is checking for nullability explicitly with the `if` conditional expression.

For example, check whether `b` is `null` and then access `b.length`:

fun main() {
//sampleStart
// Assigns null to a nullable variable
val b: String? = null
// Checks for nullability first and then accesses length
val l = if (b != null) b.length else -1
print(l)
// -1
//sampleEnd
}

In the example above, the compiler performs a [smart cast](typecasts.html#smart-casts) to change the type from nullable `String?` to non-nullable `String`. It also tracks the information about the check you performed and allows the call to `length` inside the `if` conditional.

More complex conditions are supported as well:

fun main() {
//sampleStart
// Assigns a nullable string to a variable
val b: String? = "Kotlin"
// Checks for nullability first and then accesses length
if (b != null && b.length > 0) {
print("String of length ${b.length}")
// String of length 6
} else {
// Provides alternative if the condition is not met
print("Empty string")
}
//sampleEnd
}

Note that the example above only works when the compiler can guarantee that `b` doesn't change between the check and its usage, same as the [smart cast prerequisites](typecasts.html#smart-cast-prerequisites).

## Safe call operator

The safe call operator `?.` allows you to handle nullability safely in a shorter form. Instead of throwing an NPE, if the object is `null`, the `?.` operator simply returns `null`:

fun main() {
//sampleStart
// Assigns a nullable string to a variable
val a: String? = "Kotlin"
// Assigns null to a nullable variable
val b: String? = null
// Checks for nullability and returns length or null
println(a?.length)
// 6
println(b?.length)
// null
//sampleEnd
}

The `b?.length` expression checks for nullability and returns `b.length` if `b` is non-null, or `null` otherwise. The type of this expression is `Int?`.

You can use the `?.` operator with both [`var` and `val` variables](basic-syntax.html#variables) in Kotlin:

* A nullable `var` can hold a `null` (for example, `var nullableValue: String? = null`) or a non-null value (for example, `var nullableValue: String? = "Kotlin"`). If it's a non-null value, you can change it to `null` at any point.
* A nullable `val` can hold a `null` (for example, `val nullableValue: String? = null`) or a non-null value (for example, `val nullableValue: String? = "Kotlin"`). If it's a non-null value, you cannot change it to `null` subsequently.

Safe calls are useful in chains. For example, Bob is an employee who may be assigned to a department (or not). That department may, in turn, have another employee as a department head. To obtain the name of Bob's department head (if there is one), you write the following:

bob?.department?.head?.name

This chain returns `null` if any of its properties are `null`.

You can also place a safe call on the left side of an assignment:

person?.department?.head = managersPool.getManager()

In the example above, if one of the receivers in the safe call chain is `null`, the assignment is skipped, and the expression on the right is not evaluated at all. For example, if either `person` or `person.department` is `null`, the function is not called. Here's the equivalent of the same safe call but with the `if` conditional:

if (person != null && person.department != null) {
person.department.head = managersPool.getManager()
}

## Elvis operator

When working with nullable types, you can check for `null` and provide an alternative value. For example, if `b` is not `null`, access `b.length`. Otherwise, return an alternative value:

fun main() {
//sampleStart
// Assigns null to a nullable variable
val b: String? = null
// Checks for nullability. If not null, returns length. If null, returns 0
val l: Int = if (b != null) b.length else 0
println(l)
// 0
//sampleEnd
}

Instead of writing the complete `if` expression, you can handle this in a more concise way with the Elvis operator `?:`:

fun main() {
//sampleStart
// Assigns null to a nullable variable
val b: String? = null
// Checks for nullability. If not null, returns length. If null, returns a non-null value
val l = b?.length ?: 0
println(l)
// 0
//sampleEnd
}

If the expression to the left of `?:` is not `null`, the Elvis operator returns it. Otherwise, the Elvis operator returns the expression to the right. The expression on the right-hand side is evaluated only if the left-hand side is `null`.

Since `throw` and `return` are expressions in Kotlin, you can also use them on the right-hand side of the Elvis operator. This can be handy, for example, when checking function arguments:

fun foo(node: Node): String? {
// Checks for getParent(). If not null, it's assigned to parent. If null, returns null
val parent = node.getParent() ?: return null
// Checks for getName(). If not null, it's assigned to name. If null, throws exception
val name = node.getName() ?: throw IllegalArgumentException("name expected")
// ...
}

## Not-null assertion operator

The not-null assertion operator `!!` converts any value to a non-nullable type.

When you apply the `!!` operator to a variable whose value is not `null`, it's safely handled as a non-nullable type, and the code executes normally. However, if the value is `null`, the `!!` operator forces it to be treated as non-nullable, which results in an NPE.

When `b` is not `null` and the `!!` operator makes it return its non-null value (which is a `String` in this example), it accesses `length` correctly:

fun main() {
//sampleStart
// Assigns a nullable string to a variable
val b: String? = "Kotlin"
// Treats b as non-null and accesses its length
val l = b!!.length
println(l)
// 6
//sampleEnd
}

When `b` is `null` and the `!!` operator makes it return its non-null value, and an NPE occurs:

fun main() {
//sampleStart
// Assigns null to a nullable variable
val b: String? = null
// Treats b as non-null and tries to access its length
val l = b!!.length
println(l)
// Exception in thread "main" java.lang.NullPointerException
//sampleEnd
}

The `!!` operator is particularly useful when you are confident that a value is not `null` and there's no chance of getting an NPE, but the compiler cannot guarantee this due to certain rules. In such cases, you can use the `!!` operator to explicitly tell the compiler that the value is not `null`.

## Nullable receiver

You can use extension functions with a [nullable receiver type](extensions.html#nullable-receivers), allowing these functions to be called on variables that might be `null`.

By defining an extension function on a nullable receiver type, you can handle `null` values within the function itself instead of checking for `null` at every place where you call the function.

For example, the [`.toString()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/to-string.html) extension function can be called on a nullable receiver. When invoked on a `null` value, it safely returns the string `"null"` without throwing an exception:

//sampleStart
fun main() {
// Assigns null to a nullable Person object stored in the person variable
val person: Person? = null
// Applies .toString to the nullable person variable and prints a string
println(person.toString())
// null
}
// Defines a simple Person class
data class Person(val name: String)
//sampleEnd

In the example above, even though `person` is `null`, the `.toString()` function safely returns the string `"null"`. This can be helpful for debugging and logging.

If you expect the `.toString()` function to return a nullable string (either a string representation or `null`), use the [safe-call operator `?.`](#safe-call-operator). The `?.` operator calls `.toString()` only if the object is not `null`, otherwise it returns `null`:

//sampleStart
fun main() {
// Assigns a nullable Person object to a variable
val person1: Person? = null
val person2: Person? = Person("Alice")
// Prints "null" if person is null; otherwise prints the result of person.toString()
println(person1?.toString())
// null
println(person2?.toString())
// Person(name=Alice)
}
// Defines a Person class
data class Person(val name: String)
//sampleEnd

The `?.` operator allows you to safely handle potential `null` values while still accessing properties or functions of objects that might be `null`.

## Let function

To handle `null` values and perform operations only on non-null types, you can use the safe call operator `?.` together with the [`let` function](scope-functions.html#let).

This combination is useful for evaluating an expression, check the result for `null`, and execute code only if it's not `null`, avoiding manual null checks:

fun main() {
//sampleStart
// Declares a list of nullable strings
val listWithNulls: List<String?> = listOf("Kotlin", null)
// Iterates over each item in the list
for (item in listWithNulls) {
// Checks if the item is null and only prints non-null values
item?.let { println(it) }
//Kotlin
}
//sampleEnd
}

## Safe casts

The regular Kotlin operator for [type casts](typecasts.html#unsafe-cast-operator) is the `as` operator. However, regular casts can result in an exception if the object is not of the target type.

You can use the `as?` operator for safe casts. It tries to cast a value to the specified type and returns `null` if the value is not of that type:

fun main() {
//sampleStart
// Declares a variable of type Any, which can hold any type of value
val a: Any = "Hello, Kotlin!"
// Safe casts to Int using the 'as?' operator
val aInt: Int? = a as? Int
// Safe casts to String using the 'as?' operator
val aString: String? = a as? String
println(aInt)
// null
println(aString)
// "Hello, Kotlin!"
//sampleEnd
}

The code above prints `null` because `a` is not an `Int`, so the cast fails safely. It also prints `"Hello, Kotlin!"` because it matches the `String?` type, so the safe cast succeeds.

## Collections of a nullable type

If you have a collection of nullable elements and want to keep only the non-null ones, use the `filterNotNull()` function:

fun main() {
//sampleStart
// Declares a list containing some null and non-null integer values
val nullableList: List<Int?> = listOf(1, 2, null, 4)
// Filters out null values, resulting in a list of non-null integers
val intList: List<Int> = nullableList.filterNotNull()
println(intList)
// [1, 2, 4]
//sampleEnd
}

## What's next?

* Learn how to [handle nullability in Java and Kotlin](java-to-kotlin-nullability-guide.html).
* Learn about generic types that are [definitely non-nullable](generics.html#definitely-non-nullable-types).

28 August 2025

---

## 6. Collections overview

The Kotlin Standard Library provides a comprehensive set of tools for managing collections – groups of a variable number of items (possibly zero) that are significant to the problem being solved and are commonly operated on.

Collections are a common concept for most programming languages, so if you're familiar with, for example, Java or Python collections, you can skip this introduction and proceed to the detailed sections.

A collection usually contains a number of objects of the same type (and its subtypes). Objects in a collection are called elements or items. For example, all the students in a department form a collection that can be used to calculate their average age.

The following collection types are relevant for Kotlin:

* List is an ordered collection with access to elements by indices – integer numbers that reflect their position. Elements can occur more than once in a list. An example of a list is a telephone number: it's a group of digits, their order is important, and they can repeat.
* Set is a collection of unique elements. It reflects the mathematical abstraction of set: a group of objects without repetitions. Generally, the order of set elements has no significance. For example, the numbers on lottery tickets form a set: they are unique, and their order is not important.
* Map (or dictionary) is a set of key-value pairs. Keys are unique, and each of them maps to exactly one value. The values can be duplicates. Maps are useful for storing logical connections between objects, for example, an employee's ID and their position.

Kotlin lets you manipulate collections independently of the exact type of objects stored in them. In other words, you add a `String` to a list of `String`s the same way as you would do with `Int`s or a user-defined class. So, the Kotlin Standard Library offers generic interfaces, classes, and functions for creating, populating, and managing collections of any type.

The collection interfaces and related functions are located in the `kotlin.collections` package. Let's get an overview of its contents.

## Collection types

The Kotlin Standard Library provides implementations for basic collection types: sets, lists, and maps. A pair of interfaces represent each collection type:

* A read-only interface that provides operations for accessing collection elements.
* A mutable interface that extends the corresponding read-only interface with write operations: adding, removing, and updating its elements.

Note that a mutable collection doesn't have to be assigned to a [`var`](basic-syntax.html#variables). Write operations with a mutable collection are still possible even if it is assigned to a `val`. The benefit of assigning mutable collections to `val` is that you protect the reference to the mutable collection from modification. Over time, as your code grows and becomes more complex, it becomes even more important to prevent unintentional modification to references. Use `val` as much as possible for safer and more robust code. If you try to reassign a `val` collection, you get a compilation error:

fun main() {
//sampleStart
val numbers = mutableListOf("one", "two", "three", "four")
numbers.add("five") // this is OK
println(numbers)
//numbers = mutableListOf("six", "seven") // compilation error
//sampleEnd
}

The read-only collection types are [covariant](generics.html#variance). This means that, if a `Rectangle` class inherits from `Shape`, you can use a `List<Rectangle>` anywhere the `List<Shape>` is required. In other words, the collection types have the same subtyping relationship as the element types. Maps are covariant on the value type, but not on the key type.

In turn, mutable collections aren't covariant; otherwise, this would lead to runtime failures. If `MutableList<Rectangle>` was a subtype of `MutableList<Shape>`, you could insert other `Shape` inheritors (for example, `Circle`) into it, thus violating its `Rectangle` type argument.

Below is a diagram of the Kotlin collection interfaces:

Let's walk through the interfaces and their implementations. To learn about `Collection`, read the section below. To learn about `List`, `Set`, and `Map`, you can either read the corresponding sections or watch a video by Sebastian Aigner, Kotlin Developer Advocate:

### Collection

[`Collection<T>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-collection/index.html) is the root of the collection hierarchy. This interface represents the common behavior of a read-only collection: retrieving size, checking item membership, and so on. `Collection` inherits from the `Iterable<T>` interface that defines the operations for iterating elements. You can use `Collection` as a parameter of a function that applies to different collection types. For more specific cases, use the `Collection`'s inheritors: [`List`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-list/index.html) and [`Set`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-set/index.html).

fun printAll(strings: Collection<String>) {
for(s in strings) print("$s ")
println()
}
fun main() {
val stringList = listOf("one", "two", "one")
printAll(stringList)
val stringSet = setOf("one", "two", "three")
printAll(stringSet)
}

[`MutableCollection<T>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-mutable-collection/index.html) is a `Collection` with write operations, such as `add` and `remove`.

fun List<String>.getShortWordsTo(shortWords: MutableList<String>, maxLength: Int) {
this.filterTo(shortWords) { it.length <= maxLength }
// throwing away the articles
val articles = setOf("a", "A", "an", "An", "the", "The")
shortWords -= articles
}
fun main() {
val words = "A long time ago in a galaxy far far away".split(" ")
val shortWords = mutableListOf<String>()
words.getShortWordsTo(shortWords, 3)
println(shortWords)
}

### List

[`List<T>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-list/index.html) stores elements in a specified order and provides indexed access to them. Indices start from zero – the index of the first element – and go to `lastIndex` which is the `(list.size - 1)`.

fun main() {
//sampleStart
val numbers = listOf("one", "two", "three", "four")
println("Number of elements: ${numbers.size}")
println("Third element: ${numbers.get(2)}")
println("Fourth element: ${numbers[3]}")
println("Index of element \"two\" ${numbers.indexOf("two")}")
//sampleEnd
}

List elements (including nulls) can duplicate: a list can contain any number of equal objects or occurrences of a single object. Two lists are considered equal if they have the same sizes and [structurally equal](equality.html#structural-equality) elements at the same positions.

data class Person(var name: String, var age: Int)
fun main() {
//sampleStart
val bob = Person("Bob", 31)
val people = listOf(Person("Adam", 20), bob, bob)
val people2 = listOf(Person("Adam", 20), Person("Bob", 31), bob)
println(people == people2)
bob.age = 32
println(people == people2)
//sampleEnd
}

[`MutableList<T>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-mutable-list/index.html) is a `List` with list-specific write operations, for example, to add or remove an element at a specific position.

fun main() {
//sampleStart
val numbers = mutableListOf(1, 2, 3, 4)
numbers.add(5)
numbers.removeAt(1)
numbers[0] = 0
numbers.shuffle()
println(numbers)
//sampleEnd
}

As you see, in some aspects lists are very similar to arrays. However, there is one important difference: an array's size is defined upon initialization and is never changed; in turn, a list doesn't have a predefined size; a list's size can be changed as a result of write operations: adding, updating, or removing elements.

In Kotlin, the default implementation of `MutableList` is [`ArrayList`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-array-list/index.html) which you can think of as a resizable array.

### Set

[`Set<T>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-set/index.html) stores unique elements; their order is generally undefined. `null` elements are unique as well: a `Set` can contain only one `null`. Two sets are equal if they have the same size, and for each element of a set there is an equal element in the other set.

fun main() {
//sampleStart
val numbers = setOf(1, 2, 3, 4)
println("Number of elements: ${numbers.size}")
if (numbers.contains(1)) println("1 is in the set")
val numbersBackwards = setOf(4, 3, 2, 1)
println("The sets are equal: ${numbers == numbersBackwards}")
//sampleEnd
}

[`MutableSet`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-mutable-set/index.html) is a `Set` with write operations from `MutableCollection`.

The default implementation of `MutableSet` – [`LinkedHashSet`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-linked-hash-set/index.html) – preserves the order of elements insertion. Hence, the functions that rely on the order, such as `first()` or `last()`, return predictable results on such sets.

fun main() {
//sampleStart
val numbers = setOf(1, 2, 3, 4) // LinkedHashSet is the default implementation
val numbersBackwards = setOf(4, 3, 2, 1)
println(numbers.first() == numbersBackwards.first())
println(numbers.first() == numbersBackwards.last())
//sampleEnd
}

An alternative implementation – [`HashSet`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-hash-set/index.html) – says nothing about the elements order, so calling such functions on it returns unpredictable results. However, `HashSet` requires less memory to store the same number of elements.

### Map

[`Map<K, V>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-map/index.html) is not an inheritor of the `Collection` interface; however, it's a Kotlin collection type as well. A `Map` stores key-value pairs (or entries); keys are unique, but different keys can be paired with equal values. The `Map` interface provides specific functions, such as access to value by key, searching keys and values, and so on.

fun main() {
//sampleStart
val numbersMap = mapOf("key1" to 1, "key2" to 2, "key3" to 3, "key4" to 1)
println("All keys: ${numbersMap.keys}")
println("All values: ${numbersMap.values}")
if ("key2" in numbersMap) println("Value by key \"key2\": ${numbersMap["key2"]}")
if (1 in numbersMap.values) println("The value 1 is in the map")
if (numbersMap.containsValue(1)) println("The value 1 is in the map") // same as previous
//sampleEnd
}

Two maps containing the equal pairs are equal regardless of the pair order.

fun main() {
//sampleStart
val numbersMap = mapOf("key1" to 1, "key2" to 2, "key3" to 3, "key4" to 1)
val anotherMap = mapOf("key2" to 2, "key1" to 1, "key4" to 1, "key3" to 3)
println("The maps are equal: ${numbersMap == anotherMap}")
//sampleEnd
}

[`MutableMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-mutable-map/index.html) is a `Map` with map write operations, for example, you can add a new key-value pair or update the value associated with the given key.

fun main() {
//sampleStart
val numbersMap = mutableMapOf("one" to 1, "two" to 2)
numbersMap.put("three", 3)
numbersMap["one"] = 11
println(numbersMap)
//sampleEnd
}

The default implementation of `MutableMap` – [`LinkedHashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-linked-hash-map/index.html) – preserves the order of elements insertion when iterating the map. In turn, an alternative implementation – [`HashMap`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-hash-map/index.html) – says nothing about the elements order.

### ArrayDeque

[`ArrayDeque<T>`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.collections/-array-deque/) is an implementation of a double-ended queue, which allows you to add or remove elements both at the beginning or end of the queue. As such, `ArrayDeque` also fills the role of both a Stack and Queue data structure in Kotlin. Behind the scenes, `ArrayDeque` is realized using a resizable array that automatically adjusts in size when required:

fun main() {
val deque = ArrayDeque(listOf(1, 2, 3))
deque.addFirst(0)
deque.addLast(4)
println(deque) // [0, 1, 2, 3, 4]
println(deque.first()) // 0
println(deque.last()) // 4
deque.removeFirst()
deque.removeLast()
println(deque) // [1, 2, 3]
}

25 September 2024

---

## 7. Generics: in, out, where

Classes in Kotlin can have type parameters, just like in Java:

class Box<T>(t: T) {
}

To create an instance of such a class, simply provide the type arguments:

val box: Box<Int> = Box<Int>(1)

But if the parameters can be inferred, for example, from the constructor arguments, you can omit the type arguments:

val box = Box(1) // 1 has type Int, so the compiler figures out that it is Box<Int>

## Variance

One of the trickiest aspects of Java's type system is the wildcard types (see [Java Generics FAQ](http://www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html)). Kotlin doesn't have these. Instead, Kotlin has declaration-site variance and type projections.

### Variance and wildcards in Java

Let's think about why Java needs these mysterious wildcards. First, generic types in Java are invariant, meaning that `List<String>` is not a subtype of `List<Object>`. If `List` were not invariant, it would have been no better than Java's arrays, as the following code would have compiled but caused an exception at runtime:

// Java
List<String> strs = new ArrayList<String>();
// Java reports a type mismatch here at compile-time.
List<Object> objs = strs;
// What if it didn't?
// We would be able to put an Integer into a list of Strings.
objs.add(1);
// And then at runtime, Java would throw
// a ClassCastException: Integer cannot be cast to String
String s = strs.get(0);

Java prohibits such things to guarantee runtime safety. But this has implications. For example, consider the `addAll()` method from the `Collection` interface. What's the signature of this method? Intuitively, you'd write it this way:

// Java
interface Collection<E> ... {
void addAll(Collection<E> items);
}

But then, you would not be able to do the following (which is perfectly safe):

// Java
// The following would not compile with the naive declaration of addAll:
// Collection<String> is not a subtype of Collection<Object>
void copyAll(Collection<Object> to, Collection<String> from) {
to.addAll(from);
}

That's why the actual signature of `addAll()` is the following:

// Java
interface Collection<E> ... {
void addAll(Collection<? extends E> items);
}

The wildcard type argument `? extends E` indicates that this method accepts a collection of objects of `E` or a subtype of `E`, not just `E` itself. This means that you can safely read `E`'s from items (elements of this collection are instances of a subclass of E), but cannot write to it as you don't know what objects comply with that unknown subtype of `E`. In return for this limitation, you get the desired behavior: `Collection<String>` is a subtype of `Collection<? extends Object>`. In other words, the wildcard with an extends-bound (upper bound) makes the type covariant.

The key to understanding why this works is rather simple: if you can only take items from a collection, then using a collection of `String`s and reading `Object`s from it is fine. Conversely, if you can only put items into the collection, it's okay to take a collection of `Object`s and put `String`s into it: in Java there is `List<? super String>`, which accepts `String`s or any of its supertypes.

The latter is called contravariance, and you can only call methods that take `String` as an argument on `List<? super String>` (for example, you can call `add(String)` or `set(int, String)`). If you call something that returns `T` in `List<T>`, you don't get a `String`, but rather an `Object`.

Joshua Bloch, in his book [Effective Java, 3rd Edition](http://www.oracle.com/technetwork/java/effectivejava-136174.html), explains the problem well (Item 31: "Use bounded wildcards to increase API flexibility"). He gives the name Producers to objects you only read from and Consumers to those you only write to. He recommends:

He then proposes the following mnemonic: PECS stands for Producer-Extends, Consumer-Super.

### Declaration-site variance

Let's suppose that there is a generic interface `Source<T>` that does not have any methods that take `T` as a parameter, only methods that return `T`:

// Java
interface Source<T> {
T nextT();
}

Then, it would be perfectly safe to store a reference to an instance of `Source<String>` in a variable of type `Source<Object>` - there are no consumer-methods to call. But Java does not know this, and still prohibits it:

// Java
void demo(Source<String> strs) {
Source<Object> objects = strs; // !!! Not allowed in Java
// ...
}

To fix this, you should declare objects of type `Source<? extends Object>`. Doing so is meaningless, because you can call all the same methods on such a variable as before, so there's no value added by the more complex type. But the compiler does not know that.

In Kotlin, there is a way to explain this sort of thing to the compiler. This is called declaration-site variance: you can annotate the type parameter `T` of `Source` to make sure that it is only returned (produced) from members of `Source<T>`, and never consumed. To do this, use the `out` modifier:

interface Source<out T> {
fun nextT(): T
}
fun demo(strs: Source<String>) {
val objects: Source<Any> = strs // This is OK, since T is an out-parameter
// ...
}

The general rule is this: when a type parameter `T` of a class `C` is declared `out`, it may occur only in the out-position in the members of `C`, but in return `C<Base>` can safely be a supertype of `C<Derived>`.

In other words, you can say that the class `C` is covariant in the parameter `T`, or that `T` is a covariant type parameter. You can think of `C` as being a producer of `T`'s, and NOT a consumer of `T`'s.

The `out` modifier is called a variance annotation, and since it is provided at the type parameter declaration site, it provides declaration-site variance. This is in contrast with Java's use-site variance where wildcards in the type usages make the types covariant.

In addition to `out`, Kotlin provides a complementary variance annotation: `in`. It makes a type parameter contravariant, meaning it can only be consumed and never produced. A good example of a contravariant type is `Comparable`:

interface Comparable<in T> {
operator fun compareTo(other: T): Int
}
fun demo(x: Comparable<Number>) {
x.compareTo(1.0) // 1.0 has type Double, which is a subtype of Number
// Thus, you can assign x to a variable of type Comparable<Double>
val y: Comparable<Double> = x // OK!
}

The words in and out seem to be self-explanatory (as they've already been used successfully in C# for quite some time), and so the mnemonic mentioned above is not really needed. It can in fact be rephrased at a higher level of abstraction:

[The Existential](https://en.wikipedia.org/wiki/Existentialism) Transformation: Consumer in, Producer out!:-)

## Type projections

### Use-site variance: type projections

It is very easy to declare a type parameter `T` as `out` and avoid trouble with subtyping on the use site, but some classes can't actually be restricted to only return `T`'s! A good example of this is `Array`:

class Array<T>(val size: Int) {
operator fun get(index: Int): T { ... }
operator fun set(index: Int, value: T) { ... }
}

This class can be neither co- nor contravariant in `T`. And this imposes certain inflexibilities. Consider the following function:

fun copy(from: Array<Any>, to: Array<Any>) {
assert(from.size == to.size)
for (i in from.indices)
to[i] = from[i]
}

This function is supposed to copy items from one array to another. Let's try to apply it in practice:

val ints: Array<Int> = arrayOf(1, 2, 3)
val any = Array<Any>(3) { "" }
copy(ints, any)
// ^ type is Array<Int> but Array<Any> was expected

Here you run into the same familiar problem: `Array<T>` is invariant in `T`, and so neither `Array<Int>` nor `Array<Any>` is a subtype of the other. Why not? Again, this is because `copy` could have an unexpected behavior, for example, it may attempt to write a `String` to `from`, and if you actually pass an array of `Int` there, a `ClassCastException` will be thrown later.

To prohibit the `copy` function from writing to `from`, you can do the following:

fun copy(from: Array<out Any>, to: Array<Any>) { ... }

This is type projection, which means that `from` is not a simple array, but is rather a restricted (projected) one. You can only call methods that return the type parameter `T`, which in this case means that you can only call `get()`. This is our approach to use-site variance, and it corresponds to Java's `Array<? extends Object>` while being slightly simpler.

You can project a type with `in` as well:

fun fill(dest: Array<in String>, value: String) { ... }

`Array<in String>` corresponds to Java's `Array<? super String>`. This means that you can pass an array of `String`, `CharSequence`, or `Object` to the `fill()` function.

### Star-projections

Sometimes you want to say that you know nothing about the type argument, but you still want to use it in a safe way. The safe way here is to define such a projection of the generic type, that every concrete instantiation of that generic type will be a subtype of that projection.

Kotlin provides so-called star-projection syntax for this:

* For `Foo<out T : TUpper>`, where `T` is a covariant type parameter with the upper bound `TUpper`, `Foo<*>` is equivalent to `Foo<out TUpper>`. This means that when the `T` is unknown you can safely read values of `TUpper` from `Foo<*>`.
* For `Foo<in T>`, where `T` is a contravariant type parameter, `Foo<*>` is equivalent to `Foo<in Nothing>`. This means there is nothing you can write to `Foo<*>` in a safe way when `T` is unknown.
* For `Foo<T : TUpper>`, where `T` is an invariant type parameter with the upper bound `TUpper`, `Foo<*>` is equivalent to `Foo<out TUpper>` for reading values and to `Foo<in Nothing>` for writing values.

If a generic type has several type parameters, each of them can be projected independently. For example, if the type is declared as `interface Function<in T, out U>` you could use the following star-projections:

* `Function<*, String>` means `Function<in Nothing, String>`.
* `Function<Int, *>` means `Function<Int, out Any?>`.
* `Function<*, *>` means `Function<in Nothing, out Any?>`.

## Generic functions

Classes aren't the only declarations that can have type parameters. Functions can, too. Type parameters are placed before the name of the function:

fun <T> singletonList(item: T): List<T> {
// ...
}
fun <T> T.basicToString(): String { // extension function
// ...
}

To call a generic function, specify the type arguments at the call site after the name of the function:

val l = singletonList<Int>(1)

Type arguments can be omitted if they can be inferred from the context, so the following example works as well:

val l = singletonList(1)

## Generic constraints

The set of all possible types that can be substituted for a given type parameter may be restricted by generic constraints.

### Upper bounds

The most common type of constraint is an upper bound, which corresponds to Java's `extends` keyword:

fun <T : Comparable<T>> sort(list: List<T>) { ... }

The type specified after a colon is the upper bound, indicating that only a subtype of `Comparable<T>` can be substituted for `T`. For example:

sort(listOf(1, 2, 3)) // OK. Int is a subtype of Comparable<Int>
sort(listOf(HashMap<Int, String>())) // Error: HashMap<Int, String> is not a subtype of Comparable<HashMap<Int, String>>

The default upper bound (if there was none specified) is `Any?`. Only one upper bound can be specified inside the angle brackets. If the same type parameter needs more than one upper bound, you need a separate where-clause:

fun <T> copyWhenGreater(list: List<T>, threshold: T): List<String>
where T : CharSequence,
T : Comparable<T> {
return list.filter { it > threshold }.map { it.toString() }
}

The passed type must satisfy all conditions of the `where` clause simultaneously. In the above example, the `T` type must implement both `CharSequence` and `Comparable`.

## Definitely non-nullable types

To make interoperability with generic Java classes and interfaces easier, Kotlin supports declaring a generic type parameter as definitely non-nullable.

To declare a generic type `T` as definitely non-nullable, declare the type with `& Any`. For example: `T & Any`.

A definitely non-nullable type must have a nullable [upper bound](#upper-bounds).

The most common use case for declaring definitely non-nullable types is when you want to override a Java method that contains `@NotNull` as an argument. For example, consider the `load()` method:

import org.jetbrains.annotations.\*;
public interface Game<T> {
public T save(T x) {}
@NotNull
public T load(@NotNull T x) {}
}

To override the `load()` method in Kotlin successfully, you need `T1` to be declared as definitely non-nullable:

interface ArcadeGame<T1> : Game<T1> {
override fun save(x: T1): T1
// T1 is definitely non-nullable
override fun load(x: T1 & Any): T1 & Any
}

When working only with Kotlin, it's unlikely that you will need to declare definitely non-nullable types explicitly because Kotlin's type inference takes care of this for you.

## Type erasure

The type safety checks that Kotlin performs for generic declaration usages are done at compile time. At runtime, the instances of generic types do not hold any information about their actual type arguments. The type information is said to be erased. For example, the instances of `Foo<Bar>` and `Foo<Baz?>` are erased to just `Foo<*>`.

### Generics type checks and casts

Due to the type erasure, there is no general way to check whether an instance of a generic type was created with certain type arguments at runtime, and the compiler prohibits such `is`-checks such as `ints is List<Int>` or `list is T` (type parameter). However, you can check an instance against a star-projected type:

if (something is List<\*>) {
something.forEach { println(it) } // The items are typed as `Any?`
}

Similarly, when you already have the type arguments of an instance checked statically (at compile time), you can make an `is`-check or a cast that involves the non-generic part of the type. Note that angle brackets are omitted in this case:

fun handleStrings(list: MutableList<String>) {
if (list is ArrayList) {
// `list` is smart-cast to `ArrayList<String>`
}
}

The same syntax but with the type arguments omitted can be used for casts that do not take type arguments into account: `list as ArrayList`.

The type arguments of generic function calls are also only checked at compile time. Inside the function bodies, the type parameters cannot be used for type checks, and type casts to type parameters (`foo as T`) are unchecked. The only exclusion is inline functions with [reified type parameters](inline-functions.html#reified-type-parameters), which have their actual type arguments inlined at each call site. This enables type checks and casts for the type parameters. However, the restrictions described above still apply for instances of generic types used inside checks or casts. For example, in the type check `arg is T`, if `arg` is an instance of a generic type itself, its type arguments are still erased.

//sampleStart
inline fun <reified A, reified B> Pair<\*, \*>.asPairOf(): Pair<A, B>? {
if (first !is A || second !is B) return null
return first as A to second as B
}
val somePair: Pair<Any?, Any?> = "items" to listOf(1, 2, 3)
val stringToSomething = somePair.asPairOf<String, Any>()
val stringToInt = somePair.asPairOf<String, Int>()
val stringToList = somePair.asPairOf<String, List<\*>>()
val stringToStringList = somePair.asPairOf<String, List<String>>() // Compiles but breaks type safety!
// Expand the sample for more details
//sampleEnd
fun main() {
println("stringToSomething = " + stringToSomething)
println("stringToInt = " + stringToInt)
println("stringToList = " + stringToList)
println("stringToStringList = " + stringToStringList)
//println(stringToStringList?.second?.forEach() {it.length}) // This will throw ClassCastException as list items are not String
}

### Unchecked casts

Type casts to generic types with concrete type arguments such as `foo as List<String>` cannot be checked at runtime.   
 These unchecked casts can be used when type safety is implied by the high-level program logic but cannot be inferred directly by the compiler. See the example below.

fun readDictionary(file: File): Map<String, \*> = file.inputStream().use {
TODO("Read a mapping of strings to arbitrary elements.")
}
// We saved a map with `Int`s into this file
val intsFile = File("ints.dictionary")
// Warning: Unchecked cast: `Map<String, \*>` to `Map<String, Int>`
val intsDictionary: Map<String, Int> = readDictionary(intsFile) as Map<String, Int>

A warning appears for the cast in the last line. The compiler can't fully check it at runtime and provides no guarantee that the values in the map are `Int`.

To avoid unchecked casts, you can redesign the program structure. In the example above, you could use the `DictionaryReader<T>` and `DictionaryWriter<T>` interfaces with type-safe implementations for different types. You can introduce reasonable abstractions to move unchecked casts from the call site to the implementation details. Proper use of [generic variance](#variance) can also help.

For generic functions, using [reified type parameters](inline-functions.html#reified-type-parameters) makes casts like `arg as T` checked, unless `arg`'s type has its own type arguments that are erased.

An unchecked cast warning can be suppressed by [annotating](annotations.html) the statement or the declaration where it occurs with `@Suppress("UNCHECKED_CAST")`:

inline fun <reified T> List<\*>.asListOfType(): List<T>? =
if (all { it is T })
@Suppress("UNCHECKED\_CAST")
this as List<T> else
null

## Underscore operator for type arguments

The underscore operator `_` can be used for type arguments. Use it to automatically infer a type of the argument when other types are explicitly specified:

abstract class SomeClass<T> {
abstract fun execute() : T
}
class SomeImplementation : SomeClass<String>() {
override fun execute(): String = "Test"
}
class OtherImplementation : SomeClass<Int>() {
override fun execute(): Int = 42
}
object Runner {
inline fun <reified S: SomeClass<T>, T> run() : T {
return S::class.java.getDeclaredConstructor().newInstance().execute()
}
}
fun main() {
// T is inferred as String because SomeImplementation derives from SomeClass<String>
val s = Runner.run<SomeImplementation, \_>()
assert(s == "Test")
// T is inferred as Int because OtherImplementation derives from SomeClass<Int>
val n = Runner.run<OtherImplementation, \_>()
assert(n == 42)
}

17 December 2024

---

## Bibliography

1. [Type aliases](https://kotlinlang.org/docs/type-aliases.html)
2. [Delegation](https://kotlinlang.org/docs/delegation.html)
3. [Serialization](https://kotlinlang.org/docs/serialization.html)
4. [Destructuring declarations](https://kotlinlang.org/docs/destructuring-declarations.html)
5. [Null safety](https://kotlinlang.org/docs/null-safety.html)
6. [Collections overview](https://kotlinlang.org/docs/collections-overview.html)
7. [Generics: in, out, where](https://kotlinlang.org/docs/generics.html)