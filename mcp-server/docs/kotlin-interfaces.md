(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Interfaces | Kotlin Documentation[{"id":"implementing-interfaces","level":0,"title":"Implementing interfaces","anchor":"#implementing-interfaces"},{"id":"properties-in-interfaces","level":0,"title":"Properties in interfaces","anchor":"#properties-in-interfaces"},{"id":"interfaces-inheritance","level":0,"title":"Interfaces Inheritance","anchor":"#interfaces-inheritance"},{"id":"resolving-overriding-conflicts","level":0,"title":"Resolving overriding conflicts","anchor":"#resolving-overriding-conflicts"},{"id":"jvm-default-method-generation-for-interface-functions","level":0,"title":"JVM default method generation for interface functions","anchor":"#jvm-default-method-generation-for-interface-functions"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/interfaces.html#webpage",
"url": "https://kotlinlang.org/docs/interfaces.html",
"name": "Interfaces | Kotlin",
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

# Interfaces

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

[Extensions](extensions.html)[Delegation](delegation.html)