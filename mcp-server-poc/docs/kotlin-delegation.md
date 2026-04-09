(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Delegation | Kotlin Documentation[{"id":"overriding-a-member-of-an-interface-implemented-by-delegation","level":0,"title":"Overriding a member of an interface implemented by delegation","anchor":"#overriding-a-member-of-an-interface-implemented-by-delegation"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/delegation.html#webpage",
"url": "https://kotlinlang.org/docs/delegation.html",
"name": "Delegation | Kotlin",
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

# Delegation

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

[Interfaces](interfaces.html)[Inheritance](inheritance.html)