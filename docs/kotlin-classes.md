# Kotlin Classes and Types


---

## 1. Data classes

Data classes in Kotlin are primarily used to hold data. For each data class, the compiler automatically generates additional member functions that allow you to print an instance to readable output, compare instances, copy instances, and more. Data classes are marked with `data`:

data class User(val name: String, val age: Int)

The compiler automatically derives the following members from all properties declared in the primary constructor:

* `equals()`/`hashCode()` pair.
* `toString()` of the form `"User(name=John, age=42)"`.
* [`componentN()` functions](destructuring-declarations.html) corresponding to the properties in their order of declaration.
* [`copy()` function](#copying).

To ensure consistency and meaningful behavior of the generated code, data classes have to fulfill the following requirements:

* The primary constructor must have at least one parameter.
* All primary constructor parameters must be marked as `val` or `var`.
* Data classes can't be abstract, open, sealed, or inner.

Additionally, the generation of data class members follows these rules with regard to the members' inheritance:

* If there are explicit implementations of `equals()`, `hashCode()`, or `toString()` in the data class body or `final` implementations in a superclass, then these functions are not generated, and the existing implementations are used.
* If a supertype has `componentN()` functions that are `open` and return compatible types, the corresponding functions are generated for the data class and override those of the supertype. If the functions of the supertype cannot be overridden due to incompatible signatures or due to their being final, an error is reported.
* Providing explicit implementations for the `componentN()` and `copy()` functions is not allowed.

Data classes may extend other classes (see [Sealed classes](sealed-classes.html) for examples).

## Properties declared in the class body

The compiler only uses the properties defined inside the primary constructor for the automatically generated functions. To exclude a property from the generated implementations, declare it inside the class body:

data class Person(val name: String) {
var age: Int = 0
}

In the example below, only the `name` property is used by default inside the `toString()`, `equals()`, `hashCode()`, and `copy()` implementations, and there is only one component function, `component1()`. The `age` property is declared inside the class body and is excluded. Therefore, two `Person` objects with the same `name` but different `age` values are considered equal since `equals()` only evaluates properties from the primary constructor:

data class Person(val name: String) {
var age: Int = 0
}
fun main() {
//sampleStart
val person1 = Person("John")
val person2 = Person("John")
person1.age = 10
person2.age = 20
println("person1 == person2: ${person1 == person2}")
// person1 == person2: true
println("person1 with age ${person1.age}: ${person1}")
// person1 with age 10: Person(name=John)
println("person2 with age ${person2.age}: ${person2}")
// person2 with age 20: Person(name=John)
//sampleEnd
}

## Copying

Use the `copy()` function to copy an object, allowing you to alter some of its properties while keeping the rest unchanged. The implementation of this function for the `User` class above would be as follows:

fun copy(name: String = this.name, age: Int = this.age) = User(name, age)

You can then write the following:

val jack = User(name = "Jack", age = 1)
val olderJack = jack.copy(age = 2)

The `copy()` function creates a shallow copy of the instance. In other words, it doesn't copy components recursively. As a result, references to other objects are shared.

For example, if a property holds a mutable list, changes made through the "original" value are also visible through the copy, and changes made through the copy are visible through the original:

data class Employee(val name: String, val roles: MutableList<String>)
fun main() {
val original = Employee("Jamie", mutableListOf("developer"))
val duplicate = original.copy()
duplicate.roles.add("team lead")
println(original)
// Employee(name=Jamie, roles=[developer, team lead])
println(duplicate)
// Employee(name=Jamie, roles=[developer, team lead])
}

As you can see, modifying the `duplicate.roles` property also changes the `original.roles` property because both properties share the same list reference.

## Data classes and destructuring declarations

Component functions generated for data classes make it possible to use them in [destructuring declarations](destructuring-declarations.html):

val jane = User("Jane", 35)
val (name, age) = jane
println("$name, $age years of age")
// Jane, 35 years of age

## Standard data classes

The standard library provides the `Pair` and `Triple` classes. In most cases, though, named data classes are a better design choice because they make the code easier to read by providing meaningful names for the properties.

14 March 2026

---

## 2. Interfaces

Interfaces in Kotlin can contain declarations of abstract methods, as well as method implementations. What makes them different from abstract classes is that interfaces cannot store state. They can have properties, but these need to be abstract or provide accessor implementations.

An interface is defined using the keyword `interface`:

interface MyInterface {
fun bar()
fun foo() {
// optional body
}
}

## Implementing interfaces

A class or object can implement one or more interfaces:

class Child : MyInterface {
override fun bar() {
// body
}
}

## Properties in interfaces

You can declare properties in interfaces. A property declared in an interface can either be abstract or provide implementations for accessors. Properties declared in interfaces can't have backing fields, and therefore accessors declared in interfaces can't reference them:

interface MyInterface {
val prop: Int // abstract
val propertyWithImplementation: String
get() = "foo"
fun foo() {
print(prop)
}
}
class Child : MyInterface {
override val prop: Int = 29
}

## Interfaces Inheritance

An interface can derive from other interfaces, meaning it can both provide implementations for their members and declare new functions and properties. Quite naturally, classes implementing such an interface are only required to define the missing implementations:

interface Named {
val name: String
}
interface Person : Named {
val firstName: String
val lastName: String
override val name: String get() = "$firstName $lastName"
}
data class Employee(
// implementing 'name' is not required
override val firstName: String,
override val lastName: String,
val position: Position
) : Person

## Resolving overriding conflicts

When you declare many types in your supertype list, you may inherit more than one implementation of the same method:

interface A {
fun foo() { print("A") }
fun bar()
}
interface B {
fun foo() { print("B") }
fun bar() { print("bar") }
}
class C : A {
override fun bar() { print("bar") }
}
class D : A, B {
override fun foo() {
super<A>.foo()
super<B>.foo()
}
override fun bar() {
super<B>.bar()
}
}

Interfaces A and B both declare functions foo() and bar(). Both of them implement foo(), but only B implements bar() (bar() is not marked as abstract in A, because this is the default for interfaces if the function has no body). Now, if you derive a concrete class C from A, you have to override bar() and provide an implementation.

However, if you derive D from A and B, you need to implement all the methods that you have inherited from multiple interfaces, and you need to specify how exactly D should implement them. This rule applies both to methods for which you've inherited a single implementation (bar()) and to those for which you've inherited multiple implementations (foo()).

## JVM default method generation for interface functions

On the JVM, functions declared in interfaces are compiled to default methods. You can control this behavior using the `-jvm-default` compiler option with the following values:

* `enable` (default): generates default implementations in interfaces and includes bridge functions in subclasses and `DefaultImpls` classes. Use this mode to maintain binary compatibility with older Kotlin versions.
* `no-compatibility`: generates only default implementations in interfaces. This mode skips compatibility bridges and `DefaultImpls` classes, making it suitable for new Kotlin code.
* `disable`: skips default methods and generates only compatibility bridges and `DefaultImpls` classes.

To configure the `-jvm-default` compiler option, set the `jvmDefault` property in your Gradle Kotlin DSL:

kotlin {
compilerOptions {
jvmDefault = JvmDefaultMode.NO\_COMPATIBILITY
}
}

23 June 2025

---

## 3. Enum classes

The most basic use case for enum classes is the implementation of type-safe enums:

enum class Direction {
NORTH, SOUTH, WEST, EAST
}

Each enum constant is an object. Enum constants are separated by commas.

Since each enum is an instance of the enum class, it can be initialized as:

enum class Color(val rgb: Int) {
RED(0xFF0000),
GREEN(0x00FF00),
BLUE(0x0000FF)
}

## Anonymous classes

Enum constants can declare their own anonymous classes with their corresponding methods, as well as with overriding base methods.

enum class ProtocolState {
WAITING {
override fun signal() = TALKING
},
TALKING {
override fun signal() = WAITING
};
abstract fun signal(): ProtocolState
}

If the enum class defines any members, separate the constant definitions from the member definitions with a semicolon.

## Implementing interfaces in enum classes

An enum class can implement an interface (but it cannot derive from a class), providing either a common implementation of interface members for all the entries, or separate implementations for each entry within its anonymous class. This is done by adding the interfaces you want to implement to the enum class declaration as follows:

import java.util.function.BinaryOperator
import java.util.function.IntBinaryOperator
//sampleStart
enum class IntArithmetics : BinaryOperator<Int>, IntBinaryOperator {
PLUS {
override fun apply(t: Int, u: Int): Int = t + u
},
TIMES {
override fun apply(t: Int, u: Int): Int = t \* u
};
override fun applyAsInt(t: Int, u: Int) = apply(t, u)
}
//sampleEnd
fun main() {
val a = 13
val b = 31
for (f in IntArithmetics.entries) {
println("$f($a, $b) = ${f.apply(a, b)}")
}
}

All enum classes implement the [Comparable](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-comparable/index.html) interface by default. Constants in the enum class are defined in the natural order. For more information, see [Ordering](collection-ordering.html).

## Working with enum constants

Enum classes in Kotlin have synthetic properties and methods for listing the defined enum constants and getting an enum constant by its name. The signatures of these methods are as follows (assuming the name of the enum class is `EnumClass`):

EnumClass.valueOf(value: String): EnumClass
EnumClass.entries: EnumEntries<EnumClass> // specialized List<EnumClass>

Below is an example of them in action:

enum class RGB { RED, GREEN, BLUE }
fun main() {
for (color in RGB.entries) println(color.toString()) // prints RED, GREEN, BLUE
println("The first color is: ${RGB.valueOf("RED")}") // prints "The first color is: RED"
}

The `valueOf()` method throws an `IllegalArgumentException` if the specified name does not match any of the enum constants defined in the class.

Prior to the introduction of `entries` in Kotlin 1.9.0, the `values()` function was used to retrieve an array of enum constants.

Every enum constant also has properties: [`name`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-enum/name.html) and [`ordinal`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-enum/ordinal.html), for obtaining its name and position (starting from 0) in the enum class declaration:

enum class RGB { RED, GREEN, BLUE }
fun main() {
//sampleStart
println(RGB.RED.name) // prints RED
println(RGB.RED.ordinal) // prints 0
//sampleEnd
}

You can access the constants in an enum class in a generic way using the [`enumValues<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/enum-values.html) and [`enumValueOf<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/enum-value-of.html) functions. In Kotlin 2.0.0, the [`enumEntries<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.enums/enum-entries.html) function is introduced as a replacement for the [`enumValues<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/enum-values.html) function. The `enumEntries<T>()` function returns a list of all enum entries for the given enum type `T`.

The `enumValues<T>()` function is still supported, but we recommend that you use the `enumEntries<T>()` function instead because it has less performance impact. Every time you call `enumValues<T>()` a new array is created, whereas whenever you call `enumEntries<T>()` the same list is returned each time, which is far more efficient.

For example:

enum class RGB { RED, GREEN, BLUE }
inline fun <reified T : Enum<T>> printAllValues() {
println(enumEntries<T>().joinToString { it.name })
}
printAllValues<RGB>()
// RED, GREEN, BLUE

23 June 2025

---

## 4. Basic syntax overview

This is a collection of basic syntax elements with examples. At the end of every section, you'll find a link to a detailed description of the related topic.

You can also learn all the Kotlin essentials with the free [Kotlin Core track](https://hyperskill.org/tracks?category=4&utm_source=jbkotlin_hs&utm_medium=referral&utm_campaign=kotlinlang-docs&utm_content=button_1&utm_term=22.03.23) by JetBrains Academy.

## Package definition and imports

Package specification should be at the top of the source file:

package my.demo
import kotlin.text.\*
// ...

It is not required to match directories and packages: source files can be placed arbitrarily in the file system.

See [Packages](packages.html).

## Program entry point

An entry point of a Kotlin application is the `main` function:

fun main() {
println("Hello world!")
}

Another form of `main` accepts a variable number of `String` arguments:

fun main(args: Array<String>) {
println(args.contentToString())
}

## Print to the standard output

`print` prints its argument to the standard output:

fun main() {
//sampleStart
print("Hello ")
print("world!")
//sampleEnd
}

`println` prints its arguments and adds a line break, so that the next thing you print appears on the next line:

fun main() {
//sampleStart
println("Hello world!")
println(42)
//sampleEnd
}

## Read from the standard input

The `readln()` function reads from the standard input. This function reads the entire line the user enters as a string.

You can use the `println()`, `readln()`, and `print()` functions together to print messages requesting and showing user input:

// Prints a message to request input
println("Enter any word: ")
// Reads and stores the user input. For example: Happiness
val yourWord = readln()
// Prints a message with the input
print("You entered the word: ")
print(yourWord)
// You entered the word: Happiness

For more information, see [Read standard input](read-standard-input.html).

## Functions

A function with two `Int` parameters and `Int` return type:

//sampleStart
fun sum(a: Int, b: Int): Int {
return a + b
}
//sampleEnd
fun main() {
print("sum of 3 and 5 is ")
println(sum(3, 5))
}

A function body can be an expression. Its return type is inferred:

//sampleStart
fun sum(a: Int, b: Int) = a + b
//sampleEnd
fun main() {
println("sum of 19 and 23 is ${sum(19, 23)}")
}

A function that returns no meaningful value:

//sampleStart
fun printSum(a: Int, b: Int): Unit {
println("sum of $a and $b is ${a + b}")
}
//sampleEnd
fun main() {
printSum(-1, 8)
}

`Unit` return type can be omitted:

//sampleStart
fun printSum(a: Int, b: Int) {
println("sum of $a and $b is ${a + b}")
}
//sampleEnd
fun main() {
printSum(-1, 8)
}

See [Functions](functions.html).

## Variables

In Kotlin, you declare a variable starting with a keyword, `val` or `var`, followed by the name of the variable.

Use the `val` keyword to declare variables that are assigned a value only once. These are immutable, read-only local variables that can't be reassigned a different value after initialization:

fun main() {
//sampleStart
// Declares the variable x and initializes it with the value of 5
val x: Int = 5
// 5
//sampleEnd
println(x)
}

Use the `var` keyword to declare variables that can be reassigned. These are mutable variables, and you can change their values after initialization:

fun main() {
//sampleStart
// Declares the variable x and initializes it with the value of 5
var x: Int = 5
// Reassigns a new value of 6 to the variable x
x += 1
// 6
//sampleEnd
println(x)
}

Kotlin supports type inference and automatically identifies the data type of a declared variable. When declaring a variable, you can omit the type after the variable name:

fun main() {
//sampleStart
// Declares the variable x with the value of 5;`Int` type is inferred
val x = 5
// 5
//sampleEnd
println(x)
}

You can use variables only after initializing them. You can either initialize a variable at the moment of declaration or declare a variable first and initialize it later. In the second case, you must specify the data type:

fun main() {
//sampleStart
// Initializes the variable x at the moment of declaration; type is not required
val x = 5
// Declares the variable c without initialization; type is required
val c: Int
// Initializes the variable c after declaration
c = 3
// 5
// 3
//sampleEnd
println(x)
println(c)
}

You can declare variables at the top level:

//sampleStart
val PI = 3.14
fun incrementX() {
x += 1
}
// x = 0; PI = 3.14
// incrementX()
// x = 1; PI = 3.14
//sampleEnd
fun main() {
println("x = $x; PI = $PI")
incrementX()
println("incrementX()")
println("x = $x; PI = $PI")
}

For information about declaring properties, see [Properties](properties.html).

## Creating classes and instances

To define a class, use the `class` keyword:

class Shape

Properties of a class can be listed in its declaration or body:

class Rectangle(val height: Double, val length: Double) {
val perimeter = (height + length) \* 2
}

The default constructor with parameters listed in the class declaration is available automatically:

class Rectangle(val height: Double, val length: Double) {
val perimeter = (height + length) \* 2
}
fun main() {
val rectangle = Rectangle(5.0, 2.0)
println("The perimeter is ${rectangle.perimeter}")
}

Inheritance between classes is declared by a colon (`:`). Classes are `final` by default; to make a class inheritable, mark it as `open`:

open class Shape
class Rectangle(val height: Double, val length: Double): Shape() {
val perimeter = (height + length) \* 2
}

For more information about constructors and inheritance, see [Classes](classes.html) and [Objects and instances](object-declarations.html).

## Comments

Just like most modern languages, Kotlin supports single-line (or end-of-line) and multi-line (block) comments:

// This is an end-of-line comment
/\* This is a block comment
on multiple lines. \*/

Block comments in Kotlin can be nested:

/\* The comment starts here
/\* contains a nested comment \*​/
and ends here. \*/

See [Documenting Kotlin Code](kotlin-doc.html) for information on the documentation comment syntax.

## String templates

fun main() {
//sampleStart
// simple name in template:
val s1 = "a is $a"
a = 2
// arbitrary expression in template:
val s2 = "${s1.replace("is", "was")}, but now is $a"
//sampleEnd
println(s2)
}

See [String templates](strings.html#string-templates) for details.

## Conditional expressions

//sampleStart
fun maxOf(a: Int, b: Int): Int {
if (a > b) {
return a
} else {
return b
}
}
//sampleEnd
fun main() {
println("max of 0 and 42 is ${maxOf(0, 42)}")
}

In Kotlin, `if` can also be used as an expression:

//sampleStart
fun maxOf(a: Int, b: Int) = if (a > b) a else b
//sampleEnd
fun main() {
println("max of 0 and 42 is ${maxOf(0, 42)}")
}

See [`if`-expressions](control-flow.html#if-expression).

## for loop

fun main() {
//sampleStart
val items = listOf("apple", "banana", "kiwifruit")
for (item in items) {
println(item)
}
//sampleEnd
}

or:

fun main() {
//sampleStart
val items = listOf("apple", "banana", "kiwifruit")
for (index in items.indices) {
println("item at $index is ${items[index]}")
}
//sampleEnd
}

See [for loop](control-flow.html#for-loops).

## while loop

fun main() {
//sampleStart
val items = listOf("apple", "banana", "kiwifruit")
while (index < items.size) {
println("item at $index is ${items[index]}")
index++
}
//sampleEnd
}

See [while loop](control-flow.html#while-loops).

## when expression

//sampleStart
fun describe(obj: Any): String =
when (obj) {
1 -> "One"
"Hello" -> "Greeting"
is Long -> "Long"
!is String -> "Not a string"
else -> "Unknown"
}
//sampleEnd
fun main() {
println(describe(1))
println(describe("Hello"))
println(describe(1000L))
println(describe(2))
println(describe("other"))
}

See [when expressions and statements](control-flow.html#when-expressions-and-statements).

## Ranges

Check if a number is within a range using `in` operator:

fun main() {
//sampleStart
val x = 10
val y = 9
if (x in 1..y+1) {
println("fits in range")
}
//sampleEnd
}

Check if a number is out of range:

fun main() {
//sampleStart
val list = listOf("a", "b", "c")
if (-1 !in 0..list.lastIndex) {
println("-1 is out of range")
}
if (list.size !in list.indices) {
println("list size is out of valid list indices range, too")
}
//sampleEnd
}

Iterate over a range:

fun main() {
//sampleStart
for (x in 1..5) {
print(x)
}
//sampleEnd
}

Or over a progression:

fun main() {
//sampleStart
for (x in 1..10 step 2) {
print(x)
}
println()
for (x in 9 downTo 0 step 3) {
print(x)
}
//sampleEnd
}

See [Ranges and progressions](ranges.html).

## Collections

Iterate over a collection:

fun main() {
val items = listOf("apple", "banana", "kiwifruit")
//sampleStart
for (item in items) {
println(item)
}
//sampleEnd
}

Check if a collection contains an object using `in` operator:

fun main() {
val items = setOf("apple", "banana", "kiwifruit")
//sampleStart
when {
"orange" in items -> println("juicy")
"apple" in items -> println("apple is fine too")
}
//sampleEnd
}

Use [lambda expressions](lambdas.html) to filter and map collections:

fun main() {
//sampleStart
val fruits = listOf("banana", "avocado", "apple", "kiwifruit")
fruits
.filter { it.startsWith("a") }
.sortedBy { it }
.map { it.uppercase() }
.forEach { println(it) }
//sampleEnd
}

See [Collections overview](collections-overview.html).

## Nullable values and null checks

A reference must be explicitly marked as nullable when a `null` value is possible. Nullable type names have `?` at the end. For example, `Int?`.

Return `null` if `str` does not hold an integer:

fun parseInt(str: String): Int? {
return str.toIntOrNull()
}

Use a function returning nullable value:

fun parseInt(str: String): Int? {
return str.toIntOrNull()
}
//sampleStart
fun printProduct(arg1: String, arg2: String) {
val x = parseInt(arg1)
val y = parseInt(arg2)
// Using `x \* y` yields error because they may hold nulls.
if (x != null && y != null) {
// x and y are automatically cast to non-nullable after null check
println(x \* y)
}
else {
println("'$arg1' or '$arg2' is not a number")
}
}
//sampleEnd
fun main() {
printProduct("6", "7")
printProduct("a", "7")
printProduct("a", "b")
}

or:

fun parseInt(str: String): Int? {
return str.toIntOrNull()
}
fun printProduct(arg1: String, arg2: String) {
val x = parseInt(arg1)
val y = parseInt(arg2)
//sampleStart
// ...
if (x == null) {
println("Wrong number format in arg1: '$arg1'")
return
}
if (y == null) {
println("Wrong number format in arg2: '$arg2'")
return
}
// x and y are automatically cast to non-nullable after null check
println(x \* y)
//sampleEnd
}
fun main() {
printProduct("6", "7")
printProduct("a", "7")
printProduct("99", "b")
}

See [Null-safety](null-safety.html).

## Type checks and automatic casts

The `is` operator checks if an expression is an instance of a type. If an immutable local variable or property is checked for a specific type, there's no need to cast it explicitly:

//sampleStart
fun getStringLength(obj: Any): Int? {
if (obj is String) {
// `obj` is automatically cast to `String` in this branch
return obj.length
}
// `obj` is still of type `Any` outside of the type-checked branch
return null
}
//sampleEnd
fun main() {
fun printLength(obj: Any) {
println("Getting the length of '$obj'. Result: ${getStringLength(obj) ?: "Error: The object is not a string"} ")
}
printLength("Incomprehensibilities")
printLength(1000)
printLength(listOf(Any()))
}

or:

//sampleStart
fun getStringLength(obj: Any): Int? {
if (obj !is String) return null
// `obj` is automatically cast to `String` in this branch
return obj.length
}
//sampleEnd
fun main() {
fun printLength(obj: Any) {
println("Getting the length of '$obj'. Result: ${getStringLength(obj) ?: "Error: The object is not a string"} ")
}
printLength("Incomprehensibilities")
printLength(1000)
printLength(listOf(Any()))
}

or even:

//sampleStart
fun getStringLength(obj: Any): Int? {
// `obj` is automatically cast to `String` on the right-hand side of `&&`
if (obj is String && obj.length >= 0) {
return obj.length
}
return null
}
//sampleEnd
fun main() {
fun printLength(obj: Any) {
println("Getting the length of '$obj'. Result: ${getStringLength(obj) ?: "Error: The object is not a string"} ")
}
printLength("Incomprehensibilities")
printLength("")
printLength(1000)
}

See [Classes](classes.html) and [Type casts](typecasts.html).

01 April 2026

---

## 5. Object declarations and expressions

In Kotlin, objects allow you to define a class and create an instance of it in a single step. This is useful when you need either a reusable singleton instance or a one-time object. To handle these scenarios, Kotlin provides two key approaches: object declarations for creating singletons and object expressions for creating anonymous, one-time objects.

Object declarations and object expressions are best used for scenarios when:

* Using singletons for shared resources: You need to ensure that only one instance of a class exists throughout the application. For example, managing a database connection pool.
* Creating factory methods: You need a convenient way to create instances efficiently. [Companion objects](#companion-objects) allow you to define class-level functions and properties tied to a class, simplifying the creation and management of these instances.
* Modifying existing class behavior temporarily: You want to modify the behavior of an existing class without the need to create a new subclass. For example, adding temporary functionality to an object for a specific operation.
* Type-safe design is required: You require one-time implementations of interfaces or [abstract classes](classes.html#abstract-classes) using object expressions. This can be useful for scenarios like a button click handler.

## Object declarations

You can create single instances of objects in Kotlin using object declarations, which always have a name following the `object` keyword. This allows you to define a class and create an instance of it in a single step, which is useful for implementing singletons:

//sampleStart
// Declares a Singleton object to manage data providers
object DataProviderManager {
private val providers = mutableListOf<DataProvider>()
// Registers a new data provider
fun registerDataProvider(provider: DataProvider) {
providers.add(provider)
}
// Retrieves all registered data providers
val allDataProviders: Collection<DataProvider>
get() = providers
}
//sampleEnd
// Example data provider interface
interface DataProvider {
fun provideData(): String
}
// Example data provider implementation
class ExampleDataProvider : DataProvider {
override fun provideData(): String {
return "Example data"
}
}
fun main() {
// Creates an instance of ExampleDataProvider
val exampleProvider = ExampleDataProvider()
// To refer to the object, use its name directly
DataProviderManager.registerDataProvider(exampleProvider)
// Retrieves and prints all data providers
println(DataProviderManager.allDataProviders.map { it.provideData() })
// [Example data]
}

To refer to the `object`, use its name directly:

DataProviderManager.registerDataProvider(exampleProvider)

Object declarations can also have supertypes, similar to how [anonymous objects can inherit from existing classes or implement interfaces](#inherit-anonymous-objects-from-supertypes):

object DefaultListener : MouseAdapter() {
override fun mouseClicked(e: MouseEvent) { ... }
override fun mouseEntered(e: MouseEvent) { ... }
}

Like variable declarations, object declarations are not expressions, so they cannot be used on the right-hand side of an assignment statement:

// Syntax error: An object expression cannot bind a name.
val myObject = object MySingleton {
val name = "Singleton"
}

Object declarations cannot be local, which means they cannot be nested directly inside a function. However, they can be nested within other object declarations or non-inner classes.

### Data objects

When printing a plain object declaration in Kotlin, the string representation contains both its name and the hash of the `object`:

object MyObject
fun main() {
println(MyObject)
// MyObject@hashcode
}

However, by marking an object declaration with the `data` modifier, you can instruct the compiler to return the actual name of the object when calling `toString()`, the same way it works for [data classes](data-classes.html):

data object MyDataObject {
val number: Int = 3
}
fun main() {
println(MyDataObject)
// MyDataObject
}

Additionally, the compiler generates several functions for your `data object`:

* `toString()` returns the name of the data object
* `equals()`/`hashCode()` enables equality checks and hash-based collections

The `equals()` function for a `data object` ensures that all objects that have the type of your `data object` are considered equal. In most cases, you will only have a single instance of your `data object` at runtime, since a `data object` declares a singleton. However, in the edge case where another object of the same type is generated at runtime (for example, by using platform reflection with `java.lang.reflect` or a JVM serialization library that uses this API under the hood), this ensures that the objects are treated as being equal.

import java.lang.reflect.Constructor
data object MySingleton
fun main() {
val evilTwin = createInstanceViaReflection()
println(MySingleton)
// MySingleton
println(evilTwin)
// MySingleton
// Even when a library forcefully creates a second instance of MySingleton,
// its equals() function returns true:
println(MySingleton == evilTwin)
// true
// Don't compare data objects using ===
println(MySingleton === evilTwin)
// false
}
fun createInstanceViaReflection(): MySingleton {
// Kotlin reflection does not permit the instantiation of data objects.
// This creates a new MySingleton instance "by force" (using Java platform reflection)
// Don't do this yourself!
return (MySingleton.javaClass.declaredConstructors[0].apply { isAccessible = true } as Constructor<MySingleton>).newInstance()
}

The generated `hashCode()` function has a behavior that is consistent with the `equals()` function, so that all runtime instances of a `data object` have the same hash code.

#### Differences between data objects and data classes

While `data object` and `data class` declarations are often used together and have some similarities, there are some functions that are not generated for a `data object`:

* No `copy()` function. Because a `data object` declaration is intended to be used as singletons, no `copy()` function is generated. Singletons restrict the instantiation of a class to a single instance, which would be violated by allowing copies of the instance to be created.
* No `componentN()` function. Unlike a `data class`, a `data object` does not have any data properties. Since attempting to destructure such an object without data properties wouldn't make sense, no `componentN()` functions are generated.

#### Use data objects with sealed hierarchies

Data object declarations are particularly useful for sealed hierarchies like [sealed classes or sealed interfaces](sealed-classes.html). They allow you to maintain symmetry with any data classes you may have defined alongside the object.

In this example, declaring `EndOfFile` as a `data object` instead of a plain `object` means that it will get the `toString()` function without the need to override it manually:

sealed interface ReadResult
data class Number(val number: Int) : ReadResult
data class Text(val text: String) : ReadResult
data object EndOfFile : ReadResult
fun main() {
println(Number(7))
// Number(number=7)
println(EndOfFile)
// EndOfFile
}

### Companion objects

Companion objects allow you to define class-level functions and properties. This makes it easy to create factory methods, hold constants, and access shared utilities.

An object declaration inside a class can be marked with the `companion` keyword:

class MyClass {
companion object Factory {
fun create(): MyClass = MyClass()
}
}

Members of the `companion object` can be called simply by using the class name as the qualifier:

class User(val name: String) {
// Defines a companion object that acts as a factory for creating User instances
companion object Factory {
fun create(name: String): User = User(name)
}
}
fun main(){
// Calls the companion object's factory method using the class name as the qualifier.
// Creates a new User instance
val userInstance = User.create("John Doe")
println(userInstance.name)
// John Doe
}

The name of the `companion object` can be omitted, in which case the name `Companion` is used:

class User(val name: String) {
// Defines a companion object without a name
companion object { }
}
// Accesses the companion object
val companionUser = User.Companion

Class members can access `private` members of their corresponding `companion object`:

class User(val name: String) {
companion object {
private val defaultGreeting = "Hello"
}
fun sayHi() {
println(defaultGreeting)
}
}
User("Nick").sayHi()
// Hello

When a class name is used by itself, it acts as a reference to the companion object of the class, regardless of whether the companion object is named or not:

//sampleStart
class User1 {
// Defines a named companion object
companion object Named {
fun show(): String = "User1's Named Companion Object"
}
}
// References the companion object of User1 using the class name
val reference1 = User1
class User2 {
// Defines an unnamed companion object
companion object {
fun show(): String = "User2's Companion Object"
}
}
// References the companion object of User2 using the class name
val reference2 = User2
//sampleEnd
fun main() {
// Calls the show() function from the companion object of User1
println(reference1.show())
// User1's Named Companion Object
// Calls the show() function from the companion object of User2
println(reference2.show())
// User2's Companion Object
}

Although members of companion objects in Kotlin look like static members from other languages, they are actually instance members of the companion object, meaning they belong to the object itself. This allows companion objects to implement interfaces:

interface Factory<T> {
fun create(name: String): T
}
class User(val name: String) {
// Defines a companion object that implements the Factory interface
companion object : Factory<User> {
override fun create(name: String): User = User(name)
}
}
fun main() {
// Uses the companion object as a Factory
val userFactory: Factory<User> = User
val newUser = userFactory.create("Example User")
println(newUser.name)
// Example User
}

However, on the JVM, you can have members of companion objects generated as real static methods and fields if you use the `@JvmStatic` annotation. See the [Java interoperability](java-to-kotlin-interop.html#static-fields) section for more detail.

## Object expressions

Object expressions declare a class and create an instance of that class, but without naming either of them. These classes are useful for one-time use. They can either be created from scratch, inherit from existing classes, or implement interfaces. Instances of these classes are also called anonymous objects because they are defined by an expression, not a name.

### Create anonymous objects from scratch

Object expressions start with the `object` keyword.

If the object doesn't extend any classes or implement interfaces, you can define an object's members directly inside curly braces after the `object` keyword:

fun main() {
//sampleStart
val helloWorld = object {
val hello = "Hello"
val world = "World"
// Object expressions extend the Any class, which already has a toString() function,
// so it must be overridden
override fun toString() = "$hello $world"
}
print(helloWorld)
// Hello World
//sampleEnd
}

### Inherit anonymous objects from supertypes

To create an anonymous object that inherits from some type (or types), specify this type after `object` and a colon `:`. Then implement or override the members of this class as if you were [inheriting](inheritance.html) from it:

window.addMouseListener(object : MouseAdapter() {
override fun mouseClicked(e: MouseEvent) { /\*...\*/ }
override fun mouseEntered(e: MouseEvent) { /\*...\*/ }
})

If a supertype has a constructor, pass the appropriate constructor parameters to it. Multiple supertypes can be specified, separated by commas, after the colon:

//sampleStart
// Creates an open class BankAccount with a balance property
open class BankAccount(initialBalance: Int) {
open val balance: Int = initialBalance
}
// Defines an interface Transaction with an execute() function
interface Transaction {
fun execute()
}
// A function to perform a special transaction on a BankAccount
fun specialTransaction(account: BankAccount) {
// Creates an anonymous object that inherits from the BankAccount class and implements the Transaction interface
// The balance of the provided account is passed to the BankAccount superclass constructor
val temporaryAccount = object : BankAccount(account.balance), Transaction {
override val balance = account.balance + 500 // Temporary bonus
// Implements the execute() function from the Transaction interface
override fun execute() {
println("Executing special transaction. New balance is $balance.")
}
}
// Executes the transaction
temporaryAccount.execute()
}
//sampleEnd
fun main() {
// Creates a BankAccount with an initial balance of 1000
val myAccount = BankAccount(1000)
// Performs a special transaction on the created account
specialTransaction(myAccount)
// Executing special transaction. New balance is 1500.
}

### Use anonymous objects as return and value types

When you return an anonymous object from a local or [`private`](visibility-modifiers.html#packages) function or property, all the members of that anonymous object are accessible through that function or property:

//sampleStart
class UserPreferences {
private fun getPreferences() = object {
val theme: String = "Dark"
val fontSize: Int = 14
}
fun printPreferences() {
val preferences = getPreferences()
println("Theme: ${preferences.theme}, Font Size: ${preferences.fontSize}")
}
}
//sampleEnd
fun main() {
val userPreferences = UserPreferences()
userPreferences.printPreferences()
// Theme: Dark, Font Size: 14
}

This allows you to return an anonymous object with specific properties, offering a simple way to encapsulate data or behavior without creating a separate class.

If a function or property that returns an anonymous object has `public`, `protected`, or `internal` visibility, its actual type is:

* `Any` if the anonymous object doesn't have a declared supertype.
* The declared supertype of the anonymous object, if there is exactly one such type.
* The explicitly declared type if there is more than one declared supertype.

In all these cases, members added in the anonymous object are not accessible. Overridden members are accessible if they are declared in the actual type of the function or property. For example:

//sampleStart
interface Notification {
// Declares notifyUser() in the Notification interface
fun notifyUser()
}
interface DetailedNotification
class NotificationManager {
// The return type is Any. The message property is not accessible.
// When the return type is Any, only members of the Any class are accessible.
fun getNotification() = object {
val message: String = "General notification"
}
// The return type is Notification because the anonymous object implements only one interface
// The notifyUser() function is accessible because it is part of the Notification interface
// The message property is not accessible because it is not declared in the Notification interface
fun getEmailNotification() = object : Notification {
override fun notifyUser() {
println("Sending email notification")
}
val message: String = "You've got mail!"
}
// The return type is DetailedNotification. The notifyUser() function and the message property are not accessible
// Only members declared in the DetailedNotification interface are accessible
fun getDetailedNotification(): DetailedNotification = object : Notification, DetailedNotification {
override fun notifyUser() {
println("Sending detailed notification")
}
val message: String = "Detailed message content"
}
}
//sampleEnd
fun main() {
// This produces no output
val notificationManager = NotificationManager()
// The message property is not accessible here because the return type is Any
// This produces no output
val notification = notificationManager.getNotification()
// The notifyUser() function is accessible
// The message property is not accessible here because the return type is Notification
val emailNotification = notificationManager.getEmailNotification()
emailNotification.notifyUser()
// Sending email notification
// The notifyUser() function and message property are not accessible here because the return type is DetailedNotification
// This produces no output
val detailedNotification = notificationManager.getDetailedNotification()
}

### Access variables from anonymous objects

Code within the body of object expressions can access variables from the enclosing scope:

import java.awt.event.MouseAdapter
import java.awt.event.MouseEvent
fun countClicks(window: JComponent) {
// MouseAdapter provides default implementations for mouse event functions
// Simulates MouseAdapter handling mouse events
window.addMouseListener(object : MouseAdapter() {
override fun mouseClicked(e: MouseEvent) {
clickCount++
}
override fun mouseEntered(e: MouseEvent) {
enterCount++
}
})
// The clickCount and enterCount variables are accessible within the object expression
}

## Behavior difference between object declarations and expressions

There are differences in the initialization behavior between object declarations and object expressions:

* Object expressions are executed (and initialized) immediately, where they are used.
* Object declarations are initialized lazily, when accessed for the first time.
* A companion object is initialized when the corresponding class is loaded (resolved) that matches the semantics of a Java static initializer.

23 February 2025

---

## 6. Classes

Like other object-oriented languages, Kotlin uses classes to encapsulate data (properties) and behavior (functions) for reusable, structured code.

Classes are blueprints or templates for objects, which you create via [constructors](#constructors-and-initializer-blocks). When you [create an instance of a class](#creating-instances), you are creating a concrete object based on that blueprint.

Kotlin offers concise syntax for declaring classes. To declare a class, use the `class` keyword followed by the class name:

class Person { /\*...\*/ }

The class declaration consists of:

* Class header, including but not limited to:

  + `class` keyword
  + Class name
  + Type parameters (if any)
  + [Primary constructor](#primary-constructor) (optional)
* Class body (optional), surrounded by curly braces `{}`, and including class members such as:

  + [Secondary constructors](#secondary-constructors)
  + [Initializer blocks](#initializer-blocks)
  + [Functions](functions.html)
  + [Properties](properties.html)
  + [Nested and inner classes](nested-classes.html)
  + [Object declarations](object-declarations.html)

You can keep both the class header and body to a bare minimum. If the class doesn't have a body, you can omit the curly braces `{}`:

// Class with primary constructor, but without a body
class Person(val name: String, var age: Int)

Here's an example that declares a class with a header and body, then [creates an instance](#creating-instances) from it:

## Creating instances

An instance is created when you use the class as a blueprint to build a real object to work with in your program.

To create an instance of a class, use the class name followed by parentheses `()`, similar to calling a [function](functions.html):

// Creates an instance of the Person class
val anonymousUser = Person()

In Kotlin, you can create instances:

* Without arguments (`Person()`): creates an instance using the default values, if they are declared in the class.
* With arguments (`Person(value)`): creates an instance by passing specific values.

You can assign the created instance to a mutable (`var`) or read-only (`val`) [variable](basic-syntax.html#variables):

// Creates an instance using the default value
// and assigns it to a mutable variable
// Creates an instance by passing a specific value
// and assigns it to a read-only variable
val namedUser = Person("Joe")

It's possible to create instances wherever you need them, inside the [`main()` function](basic-syntax.html#program-entry-point), within other functions, or inside another class. Additionally, you can create instances inside another function and call that function from `main()`.

The following code declares a `Person` class with a property for storing a name. It also demonstrates how to create an instance with both the default constructor's value and a specific value:

// Class header with a primary constructor
// that initializes name with a default value
class Person(val name: String = "Sebastian")
fun main() {
// Creates an instance using the default constructor's value
val anonymousUser = Person()
// Creates an instance by passing a specific value
val namedUser = Person("Joe")
// Accesses the instances' name property
println(anonymousUser.name)
// Sebastian
println(namedUser.name)
// Joe
}

For information about creating instances of nested, inner, and anonymous inner classes, see the [Nested classes](nested-classes.html) section.

## Constructors and initializer blocks

When you create a class instance, you call one of its constructors. A class in Kotlin can have a [primary constructor](#primary-constructor) and one or more [secondary constructors](#secondary-constructors).

The primary constructor is the main way to initialize a class. You declare it in the class header. A secondary constructor provides additional initialization logic. You declare it in the class body.

Both primary and secondary constructors are optional, but a class must have at least one constructor.

### Primary constructor

The primary constructor sets up the initial state of an instance when [it's created](#creating-instances).

To declare a primary constructor, place it in the class header after the class name:

class Person constructor(name: String) { /\*...\*/ }

If the primary constructor doesn't have any [annotations](annotations.html) or [visibility modifiers](visibility-modifiers.html#constructors), you can omit the `constructor` keyword:

class Person(name: String) { /\*...\*/ }

The primary constructor can declare parameters as properties. Use the `val` keyword before the argument name to declare a read-only property and the `var` keyword for a mutable property:

class Person(val name: String, var age: Int) { /\*...\*/ }

These constructor parameter properties are stored as part of the instance and are accessible from outside the class.

It's also possible to declare primary constructor parameters that are not properties. These parameters don't have `val` or `var` in front of them, so they are not stored in the instance and are available only within the class body:

// Primary constructor parameter that is also a property
class PersonWithProperty(val name: String) {
fun greet() {
println("Hello, $name")
}
}
// Primary constructor parameter only (not stored as a property)
class PersonWithAssignment(name: String) {
// Must be assigned to a property to be usable later
val displayName: String = name
fun greet() {
println("Hello, $displayName")
}
}

Properties declared in the primary constructor are accessible by [member functions](functions.html) of the class:

// Class with a primary constructor declaring properties
class Person(val name: String, var age: Int) {
// Member function accessing class properties
fun introduce(): String {
return "Hi, I'm $name and I'm $age years old."
}
}

You can also assign default values to properties in the primary constructor:

class Person(val name: String = "John", var age: Int = 30) { /\*...\*/ }

If no value is passed to the constructor during [instance creation](#creating-instances), properties use their default value:

// Class with a primary constructor
// including default values for name and age
class Person(val name: String = "John", var age: Int = 30)
fun main() {
// Creates an instance using default values
val person = Person()
println("Name: ${person.name}, Age: ${person.age}")
// Name: John, Age: 30
}

You can use the primary constructor parameters to initialize additional class properties directly in the class body:

// Class with a primary constructor
// including default values for name and age
class Person(
val name: String = "John",
var age: Int = 30
) {
// Initializes the description property
// from the primary constructor parameters
val description: String = "Name: $name, Age: $age"
}
fun main() {
// Creates an instance of the Person class
val person = Person()
// Accesses the description property
println(person.description)
// Name: John, Age: 30
}

As with functions, you can use [trailing commas](coding-conventions.html#trailing-commas) in constructor declarations:

class Person(
val name: String,
val lastName: String,
var age: Int,
) { /\*...\*/ }

### Initializer blocks

The primary constructor initializes the class and sets its properties. In most cases, you can handle this with simple code.

If you need to perform more complex operations during [instance creation](#creating-instances), place that logic in initializer blocks inside the class body. These blocks run when the primary constructor executes.

Declare initializer blocks with the `init` keyword followed by curly braces `{}`. Write within the curly braces any code that you want to run during initialization:

// Class with a primary constructor that initializes name and age
class Person(val name: String, var age: Int) {
init {
// Initializer block runs when an instance is created
println("Person created: $name, age $age.")
}
}
fun main() {
// Creates an instance of the Person class
Person("John", 30)
// Person created: John, age 30.
}

Add as many initializer blocks (`init {}`) as you need. They run in the order in which they appear in the class body, along with property initializers:

//sampleStart
// Class with a primary constructor that initializes name and age
class Person(val name: String, var age: Int) {
// First initializer block
init {
// Runs first when an instance is created
println("Person created: $name, age $age.")
}
// Second initializer block
init {
// Runs after the first initializer block
if (age < 18) {
println("$name is a minor.")
} else {
println("$name is an adult.")
}
}
}
fun main() {
// Creates an instance of the Person class
Person("John", 30)
// Person created: John, age 30.
// John is an adult.
}
//sampleEnd

You can use primary constructor parameters in initializer blocks. For example, in the code above, the first and second initializers use the `name` and `age` parameters from the primary constructor.

A common use case for `init` blocks is data validation. For example, by calling the [`require` function](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/require.html):

class Person(val age: Int) {
init {
require(age > 0) { "age must be positive" }
}
}

### Secondary constructors

In Kotlin, secondary constructors are additional constructors that a class can have beyond its primary constructor. Secondary constructors are useful when you need multiple ways to initialize a class or for [Java interoperability](java-to-kotlin-interop.html).

To declare a secondary constructor, use the `constructor` keyword inside the class body with the constructor parameters within parentheses `()`. Add the constructor logic within curly braces `{}`:

// Class header with a primary constructor that initializes name and age
class Person(val name: String, var age: Int) {
// Secondary constructor that takes age as a
// String and converts it to an Int
constructor(name: String, age: String) : this(name, age.toIntOrNull() ?: 0) {
println("$name created with converted age: ${this.age}")
}
}
fun main() {
// Uses the secondary constructor with age as a String
Person("Bob", "8")
// Bob created with converted age: 8
}

In the code above, the secondary constructor delegates to the primary constructor via the `this` keyword, passing `name` and the `age` value converted to an integer.

In Kotlin, secondary constructors must delegate to the primary constructor. This delegation ensures that all primary constructor initialization logic is executed before any secondary constructor logic runs.

Constructor delegation can be:

* Direct, where the secondary constructor calls the primary constructor immediately.
* Indirect, where one secondary constructor calls another, which in turn delegates to the primary constructor.

Here's an example demonstrating how direct and indirect delegation works:

// Class header with a primary constructor that initializes name and age
class Person(
val name: String,
var age: Int
) {
// Secondary constructor with direct delegation
// to the primary constructor
constructor(name: String) : this(name, 0) {
println("Person created with default age: $age and name: $name.")
}
// Secondary constructor with indirect delegation:
// this("Bob") -> constructor(name: String) -> primary constructor
constructor() : this("Bob") {
println("New person created with default age: $age and name: $name.")
}
}
fun main() {
// Creates an instance based on the direct delegation
Person("Alice")
// Person created with default age: 0 and name: Alice.
// Creates an instance based on the indirect delegation
Person()
// Person created with default age: 0 and name: Bob.
// New person created with default age: 0 and name: Bob.
}

In classes with initializer blocks (`init {}`), the code within these blocks becomes part of the primary constructor. Given that secondary constructors delegate to the primary constructor first, all initializer blocks and property initializers run before the body of the secondary constructor. Even if the class has no primary constructor, the delegation still happens implicitly:

// Class header with no primary constructor
class Person {
// Initializer block runs when an instance is created
init {
// Runs before the secondary constructor
println("1. First initializer block runs")
}
// Secondary constructor that takes an integer parameter
constructor(i: Int) {
// Runs after the initializer block
println("2. Person $i is created")
}
}
fun main() {
// Creates an instance of the Person class
Person(1)
// 1. First initializer block runs
// 2. Person 1 created
}

### Classes without constructors

Classes that don't declare any constructors (primary or secondary) have an implicit primary constructor with no parameters:

// Class with no explicit constructors
class Person {
// No primary or secondary constructors declared
}
fun main() {
// Creates an instance of the Person class
// using the implicit primary constructor
val person = Person()
}

The visibility of this implicit primary constructor is public, meaning it can be accessed from anywhere. If you don't want your class to have a public constructor, declare an empty primary constructor with non-default visibility:

class Person private constructor() { /\*...\*/ }

## Inheritance

Class inheritance in Kotlin allows you to create a new class (derived class) from an existing class (base class), inheriting its properties and functions while adding or modifying behavior.

For detailed information about inheritance hierarchies and how to use of the `open` keyword, see the [Inheritance](inheritance.html) section.

## Abstract classes

In Kotlin, abstract classes are classes that can't be instantiated directly. They are designed to be inherited by other classes which define their actual behavior. This behavior is called an implementation.

An abstract class can declare abstract properties and functions, which must be implemented by subclasses.

Abstract classes can also have constructors. These constructors initialize class properties and enforce required parameters for subclasses. Declare an abstract class using the `abstract` keyword:

abstract class Person(val name: String, val age: Int)

An abstract class can have both abstract and non-abstract members (properties and functions). To declare a member as abstract, you must use the `abstract` keyword explicitly.

You don't need to annotate abstract classes or functions with the `open` keyword because they are implicitly inheritable by default. For more details about the `open` keyword, see [Inheritance](inheritance.html#open-keyword).

Abstract members don't have an implementation in the abstract class. You define the implementation in a subclass or inheriting class with an `override` function or property:

// Abstract class with a primary constructor that declares name and age
abstract class Person(
val name: String,
val age: Int
) {
// Abstract member
// Doesn't provide implementation,
// and it must be implemented by subclasses
abstract fun introduce()
// Non-abstract member (has an implementation)
fun greet() {
println("Hello, my name is $name.")
}
}
// Subclass that provides an implementation for the abstract member
class Student(
name: String,
age: Int,
val school: String
) : Person(name, age) {
override fun introduce() {
println("I am $name, $age years old, and I study at $school.")
}
}
fun main() {
// Creates an instance of the Student class
val student = Student("Alice", 20, "Engineering University")
// Calls the non-abstract member
student.greet()
// Hello, my name is Alice.
// Calls the overridden abstract member
student.introduce()
// I am Alice, 20 years old, and I study at Engineering University.
}

## Companion objects

In Kotlin, each class can have a [companion object](object-declarations.html#companion-objects). Companion objects are a type of object declaration that allows you to access its members using the class name without creating a class instance.

Suppose you need to write a function that can be called without creating an instance of a class, but it is still logically connected to the class (such as a factory function). In that case, you can declare it inside a companion [object declaration](object-declarations.html) within the class:

// Class with a primary constructor that declares the name property
class Person(
val name: String
) {
// Class body with a companion object
companion object {
fun createAnonymous() = Person("Anonymous")
}
}
fun main() {
// Calls the function without creating an instance of the class
val anonymous = Person.createAnonymous()
println(anonymous.name)
// Anonymous
}

If you declare a companion object inside your class, you can access its members using only the class name as a qualifier.

For more information, see [Companion objects](object-declarations.html#companion-objects).

12 February 2026

---

## 7. Sealed classes and interfaces

Sealed classes and interfaces provide controlled inheritance of your class hierarchies. All direct subclasses of a sealed class are known at compile time. No other subclasses may appear outside the module and package within which the sealed class is defined. The same logic applies to sealed interfaces and their implementations: once a module with a sealed interface is compiled, no new implementations can be created.

When you combine sealed classes and interfaces with the `when` expression, you can cover the behavior of all possible subclasses and ensure that no new subclasses are created to affect your code adversely.

Sealed classes are best used for scenarios when:

* Limited class inheritance is desired: You have a predefined, finite set of subclasses that extend a class, all of which are known at compile time.
* Type-safe design is required: Safety and pattern matching are crucial in your project. Particularly for state management or handling complex conditional logic. For an example, check out [Use sealed classes with when expressions](#use-sealed-classes-with-when-expression).
* Working with closed APIs: You want robust and maintainable public APIs for libraries that ensure that third-party clients use the APIs as intended.

For more detailed practical applications, see [Use case scenarios](#use-case-scenarios).

## Declare a sealed class or interface

To declare a sealed class or interface, use the `sealed` modifier:

// Create a sealed interface
sealed interface Error
// Create a sealed class that implements sealed interface Error
sealed class IOError(): Error
// Define subclasses that extend sealed class 'IOError'
class FileReadError(val file: File): IOError()
class DatabaseError(val source: DataSource): IOError()
// Create a singleton object implementing the 'Error' sealed interface
object RuntimeError : Error

This example could represent a library's API that contains error classes to let library users handle errors that it can throw. If the hierarchy of such error classes includes interfaces or abstract classes visible in the public API, then nothing prevents other developers from implementing or extending them in the client code. Since the library doesn't know about errors declared outside of it, it can't treat them consistently with its own classes. However, with a sealed hierarchy of error classes, library authors can be sure that they know all the possible error types and that other error types can't appear later.

The hierarchy of the example looks like this:

### Constructors

A sealed class itself is always an [abstract class](classes.html#abstract-classes), and as a result, can't be instantiated directly. However, it may contain or inherit constructors. These constructors aren't for creating instances of the sealed class itself but for its subclasses. Consider the following example with a sealed class called `Error` and its several subclasses, which we instantiate:

sealed class Error(val message: String) {
class NetworkError : Error("Network failure")
class DatabaseError : Error("Database cannot be reached")
class UnknownError : Error("An unknown error has occurred")
}
fun main() {
val errors = listOf(Error.NetworkError(), Error.DatabaseError(), Error.UnknownError())
errors.forEach { println(it.message) }
}
// Network failure
// Database cannot be reached
// An unknown error has occurred

You can use [`enum`](enum-classes.html) classes within your sealed classes to use enum constants to represent states and provide additional detail. Each enum constant exists only as a single instance, while subclasses of a sealed class may have multiple instances. In the example, the `sealed class Error` along with its several subclasses, employs an `enum` to denote error severity. Each subclass constructor initializes the `severity` and can alter its state:

enum class ErrorSeverity { MINOR, MAJOR, CRITICAL }
sealed class Error(val severity: ErrorSeverity) {
class FileReadError(val file: File): Error(ErrorSeverity.MAJOR)
class DatabaseError(val source: DataSource): Error(ErrorSeverity.CRITICAL)
object RuntimeError : Error(ErrorSeverity.CRITICAL)
// Additional error types can be added here
}

Constructors of sealed classes can have one of two [visibilities](visibility-modifiers.html): `protected` (by default) or `private`:

sealed class IOError {
// A sealed class constructor has protected visibility by default. It's visible inside this class and its subclasses
constructor() { /\*...\*/ }
// Private constructor, visible inside this class only.
// Using a private constructor in a sealed class allows for even stricter control over instantiation, enabling specific initialization procedures within the class.
private constructor(description: String): this() { /\*...\*/ }
// This will raise an error because public and internal constructors are not allowed in sealed classes
// public constructor(code: Int): this() {}
}

## Inheritance

Direct subclasses of sealed classes and interfaces must be declared in the same package. They may be top-level or nested inside any number of other named classes, named interfaces, or named objects. Subclasses can have any [visibility](visibility-modifiers.html) as long as they are compatible with normal inheritance rules in Kotlin.

Subclasses of sealed classes must have a properly qualified name. They can't be local or anonymous objects.

These restrictions don't apply to indirect subclasses. If a direct subclass of a sealed class is not marked as sealed, it can be extended in any way that its modifiers allow:

// Sealed interface 'Error' has implementations only in the same package and module
sealed interface Error
// Sealed class 'IOError' extends 'Error' and is extendable only within the same package
sealed class IOError(): Error
// Open class 'CustomError' extends 'Error' and can be extended anywhere it's visible
open class CustomError(): Error

### Inheritance in multiplatform projects

There is one more inheritance restriction in [multiplatform projects](/docs/multiplatform/get-started.html): direct subclasses of sealed classes must reside in the same [source set](/docs/multiplatform/multiplatform-discover-project.html#source-sets). It applies to sealed classes without the [expected and actual modifiers](/docs/multiplatform/multiplatform-expect-actual.html).

If a sealed class is declared as `expect` in a common source set and have `actual` implementations in platform source sets, both `expect` and `actual` versions can have subclasses in their source sets. Moreover, if you use a hierarchical structure, you can create subclasses in any source set between the `expect` and `actual` declarations.

[Learn more about the hierarchical structure of multiplatform projects](/docs/multiplatform/multiplatform-hierarchy.html).

## Use sealed classes with when expression

The key benefit of using sealed classes comes into play when you use them in a [`when`](control-flow.html#when-expressions-and-statements) expression. The `when` expression, used with a sealed class, allows the Kotlin compiler to check exhaustively that all possible cases are covered. In such cases, you don't need to add an `else` clause:

// Sealed class and its subclasses
sealed class Error {
class FileReadError(val file: String): Error()
class DatabaseError(val source: String): Error()
object RuntimeError : Error()
}
//sampleStart
// Function to log errors
fun log(e: Error) = when(e) {
is Error.FileReadError -> println("Error while reading file ${e.file}")
is Error.DatabaseError -> println("Error while reading from database ${e.source}")
Error.RuntimeError -> println("Runtime error")
// No `else` clause is required because all the cases are covered
}
//sampleEnd
// List all errors
fun main() {
val errors = listOf(
Error.FileReadError("example.txt"),
Error.DatabaseError("usersDatabase"),
Error.RuntimeError
)
errors.forEach { log(it) }
}

When using sealed classes with `when` expressions, you can also add guard conditions to include additional checks in a single branch. For more information, see [Guard conditions in when expressions](control-flow.html#guard-conditions-in-when-expressions).

## Use case scenarios

Let's explore some practical scenarios where sealed classes and interfaces can be particularly useful.

### State management in UI applications

You can use sealed classes to represent different UI states in an application. This approach allows for structured and safe handling of UI changes. This example demonstrates how to manage various UI states:

sealed class UIState {
data object Loading : UIState()
data class Success(val data: String) : UIState()
data class Error(val exception: Exception) : UIState()
}
fun updateUI(state: UIState) {
when (state) {
is UIState.Loading -> showLoadingIndicator()
is UIState.Success -> showData(state.data)
is UIState.Error -> showError(state.exception)
}
}

### Payment method handling

In practical business applications, handling various payment methods efficiently is a common requirement. You can use sealed classes with `when` expressions to implement such business logic. By representing different payment methods as subclasses of a sealed class, it establishes a clear and manageable structure for processing transactions:

sealed class Payment {
data class CreditCard(val number: String, val expiryDate: String) : Payment()
data class PayPal(val email: String) : Payment()
data object Cash : Payment()
}
fun processPayment(payment: Payment) {
when (payment) {
is Payment.CreditCard -> processCreditCardPayment(payment.number, payment.expiryDate)
is Payment.PayPal -> processPayPalPayment(payment.email)
is Payment.Cash -> processCashPayment()
}
}

`Payment` is a sealed class that represents different payment methods in an e-commerce system: `CreditCard`, `PayPal`, and `Cash`. Each subclass can have its specific properties, like `number` and `expiryDate` for `CreditCard`, and `email` for `PayPal`.

The `processPayment()` function demonstrates how to handle different payment methods. This approach ensures that all possible payment types are considered, and the system remains flexible for new payment methods to be added in the future.

### API request-response handling

You can use sealed classes and sealed interfaces to implement a user authentication system that handles API requests and responses. The user authentication system has login and logout functionalities. The `ApiRequest` sealed interface defines specific request types: `LoginRequest` for login, and `LogoutRequest` for logout operations. The sealed class, `ApiResponse`, encapsulates different response scenarios: `UserSuccess` with user data, `UserNotFound` for absent users, and `Error` for any failures. The `handleRequest` function processes these requests in a type-safe manner using a `when` expression, while `getUserById` simulates user retrieval:

// Import necessary modules
import io.ktor.server.application.\*
import io.ktor.server.resources.\*
import kotlinx.serialization.\*
// Define the sealed interface for API requests using Ktor resources
@Resource("api")
sealed interface ApiRequest
@Serializable
@Resource("login")
data class LoginRequest(val username: String, val password: String) : ApiRequest
@Serializable
@Resource("logout")
object LogoutRequest : ApiRequest
// Define the ApiResponse sealed class with detailed response types
sealed class ApiResponse {
data class UserSuccess(val user: UserData) : ApiResponse()
data object UserNotFound : ApiResponse()
data class Error(val message: String) : ApiResponse()
}
// User data class to be used in the success response
data class UserData(val userId: String, val name: String, val email: String)
// Function to validate user credentials (for demonstration purposes)
fun isValidUser(username: String, password: String): Boolean {
// Some validation logic (this is just a placeholder)
return username == "validUser" && password == "validPass"
}
// Function to handle API requests with detailed responses
fun handleRequest(request: ApiRequest): ApiResponse {
return when (request) {
is LoginRequest -> {
if (isValidUser(request.username, request.password)) {
ApiResponse.UserSuccess(UserData("userId", "userName", "userEmail"))
} else {
ApiResponse.Error("Invalid username or password")
}
}
is LogoutRequest -> {
// Assuming logout operation always succeeds for this example
ApiResponse.UserSuccess(UserData("userId", "userName", "userEmail")) // For demonstration
}
}
}
// Function to simulate a getUserById call
fun getUserById(userId: String): ApiResponse {
return if (userId == "validUserId") {
ApiResponse.UserSuccess(UserData("validUserId", "John Doe", "john@example.com"))
} else {
ApiResponse.UserNotFound
}
// Error handling would also result in an Error response.
}
// Main function to demonstrate the usage
fun main() {
val loginResponse = handleRequest(LoginRequest("user", "pass"))
println(loginResponse)
val logoutResponse = handleRequest(LogoutRequest)
println(logoutResponse)
val userResponse = getUserById("validUserId")
println(userResponse)
val userNotFoundResponse = getUserById("invalidId")
println(userNotFoundResponse)
}

01 October 2025

---

## Bibliography

1. [Data classes](https://kotlinlang.org/docs/data-classes.html)
2. [Interfaces](https://kotlinlang.org/docs/interfaces.html)
3. [Enum classes](https://kotlinlang.org/docs/enum-classes.html)
4. [Basic syntax overview](https://kotlinlang.org/docs/basic-syntax.html)
5. [Object declarations and expressions](https://kotlinlang.org/docs/object-declarations.html)
6. [Classes](https://kotlinlang.org/docs/classes.html)
7. [Sealed classes and interfaces](https://kotlinlang.org/docs/sealed-classes.html)