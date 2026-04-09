(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Enum classes | Kotlin Documentation[{"id":"anonymous-classes","level":0,"title":"Anonymous classes","anchor":"#anonymous-classes"},{"id":"implementing-interfaces-in-enum-classes","level":0,"title":"Implementing interfaces in enum classes","anchor":"#implementing-interfaces-in-enum-classes"},{"id":"working-with-enum-constants","level":0,"title":"Working with enum constants","anchor":"#working-with-enum-constants"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/enum-classes.html#webpage",
"url": "https://kotlinlang.org/docs/enum-classes.html",
"name": "Enum classes | Kotlin",
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

# Enum classes

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

To reduce repetition when working with enum entries, try out context-sensitive resolution (currently in preview). This feature allows you to omit the enum class name when the expected type is known, such as in `when` expressions or when assigning to a typed variable.

For more information, see [Preview of context-sensitive resolution](whatsnew22.html#preview-of-context-sensitive-resolution) or the related [KEEP proposal](https://github.com/Kotlin/KEEP/blob/improved-resolution-expected-type/proposals/context-sensitive-resolution.md).

You can access the constants in an enum class in a generic way using the [`enumValues<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/enum-values.html) and [`enumValueOf<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/enum-value-of.html) functions. In Kotlin 2.0.0, the [`enumEntries<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.enums/enum-entries.html) function is introduced as a replacement for the [`enumValues<T>()`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/enum-values.html) function. The `enumEntries<T>()` function returns a list of all enum entries for the given enum type `T`.

The `enumValues<T>()` function is still supported, but we recommend that you use the `enumEntries<T>()` function instead because it has less performance impact. Every time you call `enumValues<T>()` a new array is created, whereas whenever you call `enumEntries<T>()` the same list is returned each time, which is far more efficient.

For example:

enum class RGB { RED, GREEN, BLUE }
inline fun <reified T : Enum<T>> printAllValues() {
println(enumEntries<T>().joinToString { it.name })
}
printAllValues<RGB>()
// RED, GREEN, BLUE

For more information about inline functions and reified type parameters, see [Inline functions](inline-functions.html).

23 June 2025

[Sealed classes and interfaces](sealed-classes.html)[Inline value classes](inline-classes.html)