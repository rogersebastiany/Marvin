(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Type aliases | Kotlin Documentation[{"id":"nested-type-aliases","level":0,"title":"Nested type aliases","anchor":"#nested-type-aliases"},{"id":"rules-for-nested-type-aliases","level":1,"title":"Rules for nested type aliases","anchor":"#rules-for-nested-type-aliases"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/type-aliases.html#webpage",
"url": "https://kotlinlang.org/docs/type-aliases.html",
"name": "Type aliases | Kotlin",
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

# Type aliases

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

[Type checks and casts](typecasts.html)[Conditions and loops](control-flow.html)