(function (w, d, s, l, i) {
w[l] = w[l] || [];
w[l].push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l != 'dataLayer' ? '&amp;l=' + l : '';
j.async = true;
j.src = '//www.googletagmanager.com/gtm.js?id=' + i + dl;
f.parentNode.insertBefore(j, f);
})(window, document, 'script', 'dataLayer', 'GTM-5P98');

Inline functions | Kotlin Documentation[{"id":"noinline","level":0,"title":"noinline","anchor":"#noinline"},{"id":"non-local-jump-expressions","level":0,"title":"Non-local jump expressions","anchor":"#non-local-jump-expressions"},{"id":"returns","level":1,"title":"Returns","anchor":"#returns"},{"id":"break-and-continue","level":1,"title":"Break and continue","anchor":"#break-and-continue"},{"id":"reified-type-parameters","level":0,"title":"Reified type parameters","anchor":"#reified-type-parameters"},{"id":"inline-properties","level":0,"title":"Inline properties","anchor":"#inline-properties"},{"id":"restrictions-for-public-api-inline-functions","level":0,"title":"Restrictions for public API inline functions","anchor":"#restrictions-for-public-api-inline-functions"}]{
"@context": "http://schema.org",
"@type": "WebPage",
"@id": "https://kotlinlang.org/docs/inline-functions.html#webpage",
"url": "https://kotlinlang.org/docs/inline-functions.html",
"name": "Inline functions | Kotlin",
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

# Inline functions

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

If an inline function has no inlinable function parameters and no [reified type parameters](#reified-type-parameters), the compiler will issue a warning, since inlining such functions is very unlikely to be beneficial (you can use the `@Suppress("NOTHING_TO_INLINE")` annotation to suppress the warning if you are sure the inlining is needed).

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
var p = parent
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
var p = parent
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

[Context parameters](context-parameters.html)[Operator overloading](operator-overloading.html)