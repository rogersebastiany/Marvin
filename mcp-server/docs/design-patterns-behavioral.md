Behavioral Design Patterns

window.defaultThemeColor = '#e74c3c';
(function() {
try {
var dismissed = JSON.parse(localStorage.getItem('dismissed-banners') || '[]');
var css = '';
for (var i = 0; i < dismissed.length; i++) {
if (/^[\w-]+$/.test(dismissed[i])) {
css += '#' + dismissed[i] + '{display:none!important}';
}
}
if (css) {
document.head.insertAdjacentHTML('beforeend', '<style>' + css + '</style>');
var meta = document.querySelector('meta[name="theme-color"]');
if (meta && window.defaultThemeColor !== undefined) {
meta.setAttribute('content', window.defaultThemeColor);
}
}
} catch(e) {}
})();

(function () {
if (typeof URLSearchParams === 'undefined') {
return;
}
var params = new URLSearchParams(window.location.search || '');
var attribution = {
utm\_source: params.get('utm\_source'),
utm\_medium: params.get('utm\_medium'),
utm\_campaign: params.get('utm\_campaign'),
utm\_term: params.get('utm\_term'),
utm\_content: params.get('utm\_content'),
gclid: params.get('gclid'),
fbclid: params.get('fbclid'),
msclkid: params.get('msclkid'),
};
var hasAny = false;
for (var key in attribution) {
if (attribution[key]) {
hasAny = true;
break;
}
}
if (!hasAny) {
return;
}
attribution.landing\_url = window.location.href;
attribution.referrer = document.referrer;
attribution.captured\_at = new Date().toISOString();
try {
localStorage.setItem('last\_attribution', JSON.stringify(attribution));
} catch (e) {
}
})();

.buy-widget-excl-local-taxes {
display: none;
}

@font-face{font-family:"PT Sans";font-style:normal;font-weight:400;font-display:swap;src:local("PT Sans"),local("PTSans-Regular"),url(/fonts/PTSans/ptsans-regular\_cyrillic-ext.woff2?1) format("woff2");unicode-range:U+0460-052F,U+1C80-1C88,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F}@font-face{font-family:"PT Sans";font-style:normal;font-weight:400;font-display:swap;src:local("PT Sans"),local("PTSans-Regular"),url(/fonts/PTSans/ptsans-regular\_cyrillic.woff2?1) format("woff2");unicode-range:U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}@font-face{font-family:"PT Sans";font-style:normal;font-weight:400;font-display:swap;src:local("PT Sans"),local("PTSans-Regular"),url(/fonts/PTSans/ptsans-regular\_latin-ext.woff2?1) format("woff2");unicode-range:U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}@font-face{font-family:"PT Sans";font-style:normal;font-weight:400;font-display:swap;src:local("PT Sans"),local("PTSans-Regular"),url(/fonts/PTSans/ptsans-regular\_latin.woff2?1) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}@font-face{font-family:"PT Sans";font-style:normal;font-weight:400;font-display:swap;src:local("PT Sans"),local("PTSans-Regular"),url(/fonts/PTSans/ptsans-regular\_en.woff2?1) format("woff2");unicode-range:U+0-FF,U+131,U+142,U+152,U+153,U+2BB,U+2BC,U+2C6,U+2DA,U+2DC,U+420,U+423,U+430,U+438-43A,U+43D,U+440,U+441,U+443,U+44C,U+457,U+2000-206F,U+2074,U+20AA-20AC,U+20B4,U+20B9,U+20BA,U+20BD,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}@font-face{font-family:"PT Sans";font-style:normal;font-weight:700;font-display:swap;src:local("PT Sans Bold"),local("PTSans-Bold"),url(/fonts/PTSans/ptsans-bold\_cyrillic-ext.woff2?1) format("woff2");unicode-range:U+0460-052F,U+1C80-1C88,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F}@font-face{font-family:"PT Sans";font-style:normal;font-weight:700;font-display:swap;src:local("PT Sans Bold"),local("PTSans-Bold"),url(/fonts/PTSans/ptsans-bold\_cyrillic.woff2?1) format("woff2");unicode-range:U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}@font-face{font-family:"PT Sans";font-style:normal;font-weight:700;font-display:swap;src:local("PT Sans Bold"),local("PTSans-Bold"),url(/fonts/PTSans/ptsans-bold\_latin-ext.woff2?1) format("woff2");unicode-range:U+0100-024F,U+0259,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}@font-face{font-family:"PT Sans";font-style:normal;font-weight:700;font-display:swap;src:local("PT Sans Bold"),local("PTSans-Bold"),url(/fonts/PTSans/ptsans-bold\_latin.woff2?1) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}@font-face{font-family:"PT Sans";font-style:normal;font-weight:700;font-display:swap;src:local("PT Sans Bold"),local("PTSans-Bold"),url(/fonts/PTSans/ptsans-bold\_en.woff2?1) format("woff2");unicode-range:U+0-FF,U+131,U+142,U+152,U+153,U+2BB,U+2BC,U+2C6,U+2DA,U+2DC,U+420,U+423,U+430,U+438-43A,U+43D,U+440,U+441,U+443,U+44C,U+457,U+2000-206F,U+2074,U+20AA-20AC,U+20B4,U+20B9,U+20BA,U+20BD,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}

{"@context":"http://schema.org","@graph":[{"@type":"Person","@id":"https://refactoring.guru/#founder","name":"Alexander Shvets"},{"@type":"Organization","@id":"https://refactoring.guru/#organization","name":"Refactoring.Guru","description":"Refactoring.Guru makes it easy for you to discover everything you need to know about refactoring, design patterns, SOLID principles, and other smart programming topics.","image":{"@type":"ImageObject","@id":"https://refactoring.guru/#organizationlogo","url":"https://refactoring.guru/images/content-public/logos/logo-plain.png","caption":"Refactoring.Guru"},"logo":{"@id":"https://refactoring.guru/#organizationlogo"},"founder":{"@id":"https://refactoring.guru/#founder"},"sameAs":["https://www.facebook.com/refactoring.guru","https://twitter.com/RefactoringGuru","https://github.com/RefactoringGuru"]},{"@type":"WebSite","@id":"https://refactoring.guru/#website","url":"https://refactoring.guru/","name":"Refactoring.Guru","description":"Refactoring.Guru makes it easy for you to discover everything you need to know about refactoring, design patterns, SOLID principles, and other smart programming topics.","author":{"@id":"https://refactoring.guru/#founder"},"publisher":{"@id":"https://refactoring.guru/#organization"},"copyrightYear":2014}]}

function extend(){var extended={};var deep=false;var i=0;var length=arguments["length"];if(Object["prototype"]["toString"]["call"](arguments[0])=== '[object Boolean]'){deep= arguments[0];i++};var merge=function(obj){for(var prop in obj){if(Object["prototype"]["hasOwnProperty"]["call"](obj,prop)){if(deep&& Object["prototype"]["toString"]["call"](obj[prop])=== '[object Object]'){extended[prop]= extend(true,extended[prop],obj[prop])}else {extended[prop]= obj[prop]}}}};for(;i< length;i++){var obj=arguments[i];merge(obj)};return extended}
function defer(method) {if (window.jQuery) {method();} else {setTimeout(function() { defer(method) }, 50);}}

+function(sd){sd = (typeof sd === "string") ? JSON.parse(atob(sd)) : sd;for(var property in sd){if(window[property]!== null&& typeof window[property]=== 'object'){window[property]= extend(true,window[property],sd[property])}else {window[property]= sd[property]}}}("eyJsb2NhbGUiOiJlbiIsImxvY2FsZV9wcmVmaXgiOiIiLCJsb2NhbGl6ZWRfdXJsX3ByZWZpeCI6Imh0dHBzOlwvXC9yZWZhY3RvcmluZy5ndXJ1XC8iLCJ1cmxfcHJlZml4IjoiaHR0cHM6XC9cL3JlZmFjdG9yaW5nLmd1cnVcLyIsImxvY2FsaXplZF91cmxfcHJlZml4X20iOiJodHRwczpcL1wvcmVmYWN0b3JpbmcuZ3VydVwvIiwidXJsX3ByZWZpeF9tIjoiaHR0cHM6XC9cL3JlZmFjdG9yaW5nLmd1cnVcLyIsInVzZXJfZWNob19hbGlhcyI6InJlZmFjdG9yaW5nIiwidXNlcl9lY2hvX2hvc3QiOiJmZWVkYmFjay5yZWZhY3RvcmluZy5ndXJ1IiwidXNlcl9lY2hvX3ByaXZhdGVfZm9ydW0iOiIyIiwidXNlcl9lY2hvX2xvY2FsZSI6ImVuIiwidXNlcl9lY2hvX3B1YmxpY19mb3J1bSI6IjMiLCJ1c2VyX2VjaG9fcHVibGljX2ZvcnVtX3VybCI6Imh0dHBzOlwvXC9mZWVkYmFjay5yZWZhY3RvcmluZy5ndXJ1XC8iLCJ1c2VyX2VjaG9fc3NvX3Rva2VuIjoiIn0=");

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('set', 'linker', {'domains': ["refactoring.guru,refactoringguru.cn"]});
gtag('config', 'G-SR8Y3GYQYC', {
// Disable default page view, because we're going to report them on our own.
// This is done to report traffic on localized domains as part of the main website traffic
// See the Chinese overrides below.
send\_page\_view: false,
});
// Needed to call gtag functions.
window.ga\_measurement\_id = 'G-SR8Y3GYQYC';

(() => {
// On first page view after returning from social network, we need to send the social login event.
(function detectSocialLogin() {
let getCookie = function (name) {
var nameEQ = name + "=";
var ca = document.cookie.split(';');
for (var i = 0; i < ca.length; i++) {
var c = ca[i];
while (c.charAt(0) == ' ') c = c.substring(1, c.length);
if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
}
return null;
};
window.social\_login\_provider = window.social\_login\_provider || getCookie('social\_login\_provider');
if (window.social\_login\_provider) {
gtag('set', {referrer: null});
gtag('event', 'login', {"method": window.social\_login\_provider});
// Delete cookie.
document.cookie = 'social\_login\_provider=; Path=/; Max-Age=-99999999;';
}
})();
function trackPageView(location, title) {
location = location || document.location.href;
title = title || document.title;
// This is show on https://refactoringguru.cn/ and alike.
if (typeof window.analytics\_path\_prefix === 'string') {
if (/^(https?:\/\/[^\/]+?)\/$/.test(location)) {
location = location.replace(/(https?:\/\/[^\/]+?)\//, '$1' + window.analytics\_path\_prefix);
} else {
location = location.replace(/(https?:\/\/[^\/]+?)\//, '$1' + window.analytics\_path\_prefix + '/');
}
gtag('set', {
'page\_location': location
});
}
// This is show on https://refactoring.guru/zh/login and alike.
if (typeof window.analytics\_location\_prefix === 'string') {
location = location.replace(/(https?:\/\/[^\/]+?)\//, window.analytics\_location\_prefix);
gtag('set', {
'page\_location': location
});
}
gtag('event', 'page\_view', {
page\_location: location,
page\_title: title,
locale: window.locale ?? 'en'
});
}
if (window.loadContent) {
window.onPageLoad = window.onPageLoad || [];
window.onPageLoad.push({
func: function (context) {
trackPageView(window.location.origin + context.canonicalPath, context.title);
},
afterAll: true,
});
}
else {
trackPageView();
}
})();

[Check out my new Git course!
Hey! Check out my new Git course!
Hey! Check out my new Git course on GitByBit.com!
Hey! Want a cool refresher on Git? Check out my new Git course on GitByBit.com!](https://gitbybit.com/)

/ [Design Patterns](/design-patterns)
/ [Catalog](/design-patterns/catalog)

# Behavioral Design Patterns

// Shorten examples titles for users.
var h1 = document.getElementsByTagName("H1")[0];
if (h1.offsetHeight > 160) {
h1.className += ' smaller';
}
// Small beautification for pattern examples.
var title = h1.innerHTML;
title = title.replace(/^(Java|C\+\+|C#|PHP|Python|Ruby|Delphi): (.\*)$/, '<strong>$1:</strong> $2');
h1.innerHTML = title;

Behavioral design patterns are concerned with algorithms and the assignment of responsibilities between objects.

[Chain of Responsibility

Lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain.](/design-patterns/chain-of-responsibility)
[Command

Turns a request into a stand-alone object that contains all information about the request. This transformation lets you pass requests as a method arguments, delay or queue a request's execution, and support undoable operations.](/design-patterns/command)
[Iterator

Lets you traverse elements of a collection without exposing its underlying representation (list, stack, tree, etc.).](/design-patterns/iterator)
[Mediator

Lets you reduce chaotic dependencies between objects. The pattern restricts direct communications between the objects and forces them to collaborate only via a mediator object.](/design-patterns/mediator)
[Memento

Lets you save and restore the previous state of an object without revealing the details of its implementation.](/design-patterns/memento)
[Observer

Lets you define a subscription mechanism to notify multiple objects about any events that happen to the object they're observing.](/design-patterns/observer)
[State

Lets an object alter its behavior when its internal state changes. It appears as if the object changed its class.](/design-patterns/state)
[Strategy

Lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.](/design-patterns/strategy)
[Template Method

Defines the skeleton of an algorithm in the superclass but lets subclasses override specific steps of the algorithm without changing its structure.](/design-patterns/template-method)
[Visitor

Lets you separate algorithms from the objects on which they operate.](/design-patterns/visitor)

#### Read next

[Chain of Responsibility](/design-patterns/chain-of-responsibility)

#### Return

[Proxy](/design-patterns/proxy)

* [Premium Content](/store)
  + [Design Patterns eBook](/design-patterns/book)
  + [Refactoring Course](/refactoring/course)
* [Refactoring](/refactoring)
  + [What is Refactoring](/refactoring/what-is-refactoring)
    - [Clean code](/refactoring/what-is-refactoring)
    - [Technical debt](/refactoring/technical-debt)
    - [When to refactor](/refactoring/when)
    - [How to refactor](/refactoring/how-to)
  + [Catalog](/refactoring/catalog)
  + [Code Smells](/refactoring/smells)
    - [Bloaters](/refactoring/smells/bloaters)
      * [Long Method](/smells/long-method)
      * [Large Class](/smells/large-class)
      * [Primitive Obsession](/smells/primitive-obsession)
      * [Long Parameter List](/smells/long-parameter-list)
      * [Data Clumps](/smells/data-clumps)
    - [Object-Orientation Abusers](/refactoring/smells/oo-abusers)
      * [Switch Statements](/smells/switch-statements)
      * [Temporary Field](/smells/temporary-field)
      * [Refused Bequest](/smells/refused-bequest)
      * [Alternative Classes with Different Interfaces](/smells/alternative-classes-with-different-interfaces)
    - [Change Preventers](/refactoring/smells/change-preventers)
      * [Divergent Change](/smells/divergent-change)
      * [Shotgun Surgery](/smells/shotgun-surgery)
      * [Parallel Inheritance Hierarchies](/smells/parallel-inheritance-hierarchies)
    - [Dispensables](/refactoring/smells/dispensables)
      * [Comments](/smells/comments)
      * [Duplicate Code](/smells/duplicate-code)
      * [Lazy Class](/smells/lazy-class)
      * [Data Class](/smells/data-class)
      * [Dead Code](/smells/dead-code)
      * [Speculative Generality](/smells/speculative-generality)
    - [Couplers](/refactoring/smells/couplers)
      * [Feature Envy](/smells/feature-envy)
      * [Inappropriate Intimacy](/smells/inappropriate-intimacy)
      * [Message Chains](/smells/message-chains)
      * [Middle Man](/smells/middle-man)
    - [Other Smells](/refactoring/smells/other)
      * [Incomplete Library Class](/smells/incomplete-library-class)
  + [Refactorings](/refactoring/techniques)
    - [Composing Methods](/refactoring/techniques/composing-methods)
      * [Extract Method](/extract-method)
      * [Inline Method](/inline-method)
      * [Extract Variable](/extract-variable)
      * [Inline Temp](/inline-temp)
      * [Replace Temp with Query](/replace-temp-with-query)
      * [Split Temporary Variable](/split-temporary-variable)
      * [Remove Assignments to Parameters](/remove-assignments-to-parameters)
      * [Replace Method with Method Object](/replace-method-with-method-object)
      * [Substitute Algorithm](/substitute-algorithm)
    - [Moving Features between Objects](/refactoring/techniques/moving-features-between-objects)
      * [Move Method](/move-method)
      * [Move Field](/move-field)
      * [Extract Class](/extract-class)
      * [Inline Class](/inline-class)
      * [Hide Delegate](/hide-delegate)
      * [Remove Middle Man](/remove-middle-man)
      * [Introduce Foreign Method](/introduce-foreign-method)
      * [Introduce Local Extension](/introduce-local-extension)
    - [Organizing Data](/refactoring/techniques/organizing-data)
      * [Self Encapsulate Field](/self-encapsulate-field)
      * [Replace Data Value with Object](/replace-data-value-with-object)
      * [Change Value to Reference](/change-value-to-reference)
      * [Change Reference to Value](/change-reference-to-value)
      * [Replace Array with Object](/replace-array-with-object)
      * [Duplicate Observed Data](/duplicate-observed-data)
      * [Change Unidirectional Association to Bidirectional](/change-unidirectional-association-to-bidirectional)
      * [Change Bidirectional Association to Unidirectional](/change-bidirectional-association-to-unidirectional)
      * [Replace Magic Number with Symbolic Constant](/replace-magic-number-with-symbolic-constant)
      * [Encapsulate Field](/encapsulate-field)
      * [Encapsulate Collection](/encapsulate-collection)
      * [Replace Type Code with Class](/replace-type-code-with-class)
      * [Replace Type Code with Subclasses](/replace-type-code-with-subclasses)
      * [Replace Type Code with State/Strategy](/replace-type-code-with-state-strategy)
      * [Replace Subclass with Fields](/replace-subclass-with-fields)
    - [Simplifying Conditional Expressions](/refactoring/techniques/simplifying-conditional-expressions)
      * [Decompose Conditional](/decompose-conditional)
      * [Consolidate Conditional Expression](/consolidate-conditional-expression)
      * [Consolidate Duplicate Conditional Fragments](/consolidate-duplicate-conditional-fragments)
      * [Remove Control Flag](/remove-control-flag)
      * [Replace Nested Conditional with Guard Clauses](/replace-nested-conditional-with-guard-clauses)
      * [Replace Conditional with Polymorphism](/replace-conditional-with-polymorphism)
      * [Introduce Null Object](/introduce-null-object)
      * [Introduce Assertion](/introduce-assertion)
    - [Simplifying Method Calls](/refactoring/techniques/simplifying-method-calls)
      * [Rename Method](/rename-method)
      * [Add Parameter](/add-parameter)
      * [Remove Parameter](/remove-parameter)
      * [Separate Query from Modifier](/separate-query-from-modifier)
      * [Parameterize Method](/parameterize-method)
      * [Replace Parameter with Explicit Methods](/replace-parameter-with-explicit-methods)
      * [Preserve Whole Object](/preserve-whole-object)
      * [Replace Parameter with Method Call](/replace-parameter-with-method-call)
      * [Introduce Parameter Object](/introduce-parameter-object)
      * [Remove Setting Method](/remove-setting-method)
      * [Hide Method](/hide-method)
      * [Replace Constructor with Factory Method](/replace-constructor-with-factory-method)
      * [Replace Error Code with Exception](/replace-error-code-with-exception)
      * [Replace Exception with Test](/replace-exception-with-test)
    - [Dealing with Generalization](/refactoring/techniques/dealing-with-generalization)
      * [Pull Up Field](/pull-up-field)
      * [Pull Up Method](/pull-up-method)
      * [Pull Up Constructor Body](/pull-up-constructor-body)
      * [Push Down Method](/push-down-method)
      * [Push Down Field](/push-down-field)
      * [Extract Subclass](/extract-subclass)
      * [Extract Superclass](/extract-superclass)
      * [Extract Interface](/extract-interface)
      * [Collapse Hierarchy](/collapse-hierarchy)
      * [Form Template Method](/form-template-method)
      * [Replace Inheritance with Delegation](/replace-inheritance-with-delegation)
      * [Replace Delegation with Inheritance](/replace-delegation-with-inheritance)
* [Design Patterns](/design-patterns)
  + [What is a Pattern](/design-patterns/what-is-pattern)
    - [What's a design pattern?](/design-patterns/what-is-pattern)
    - [History of patterns](/design-patterns/history)
    - [Why should I learn patterns?](/design-patterns/why-learn-patterns)
    - [Criticism of patterns](/design-patterns/criticism)
    - [Classification of patterns](/design-patterns/classification)
  + [Catalog](/design-patterns/catalog)
  + [Creational Patterns](/design-patterns/creational-patterns)
    - [Factory Method](/design-patterns/factory-method)
    - [Abstract Factory](/design-patterns/abstract-factory)
    - [Builder](/design-patterns/builder)
    - [Prototype](/design-patterns/prototype)
    - [Singleton](/design-patterns/singleton)
  + [Structural Patterns](/design-patterns/structural-patterns)
    - [Adapter](/design-patterns/adapter)
    - [Bridge](/design-patterns/bridge)
    - [Composite](/design-patterns/composite)
    - [Decorator](/design-patterns/decorator)
    - [Facade](/design-patterns/facade)
    - [Flyweight](/design-patterns/flyweight)
    - [Proxy](/design-patterns/proxy)
  + [Behavioral Patterns](/design-patterns/behavioral-patterns)
    - [Chain of Responsibility](/design-patterns/chain-of-responsibility)
    - [Command](/design-patterns/command)
    - [Iterator](/design-patterns/iterator)
    - [Mediator](/design-patterns/mediator)
    - [Memento](/design-patterns/memento)
    - [Observer](/design-patterns/observer)
    - [State](/design-patterns/state)
    - [Strategy](/design-patterns/strategy)
    - [Template Method](/design-patterns/template-method)
    - [Visitor](/design-patterns/visitor)
  + [Code Examples](/design-patterns/examples)
    - [C#](/design-patterns/csharp)
    - [C++](/design-patterns/cpp)
    - [Go](/design-patterns/go)
    - [Java](/design-patterns/java)
    - [PHP](/design-patterns/php)
    - [Python](/design-patterns/python)
    - [Ruby](/design-patterns/ruby)
    - [Rust](/design-patterns/rust)
    - [Swift](/design-patterns/swift)
    - [TypeScript](/design-patterns/typescript)

[Sign in](https://refactoring.guru/login "Sign in")
 [Contact us](https://feedback.refactoring.guru/ "Contact us")

[Shop Now!](/store)

* English

  [English](https://refactoring.guru/design-patterns/behavioral-patterns "English")
  [Español](https://refactoring.guru/es/design-patterns/behavioral-patterns "Español")
  [Français](https://refactoring.guru/fr/design-patterns/behavioral-patterns "Français")
  [日本語](https://refactoring.guru/ja/design-patterns/behavioral-patterns "日本語")
  [한국어](https://refactoring.guru/ko/design-patterns/behavioral-patterns "한국어")
  [Polski](https://refactoring.guru/pl/design-patterns/behavioral-patterns "Polski")
  [Português Brasileiro](https://refactoring.guru/pt-br/design-patterns/behavioral-patterns "Português Brasileiro")
  [Русский](https://refactoring.guru/ru/design-patterns/behavioral-patterns "Русский")
  [Українська](https://refactoring.guru/uk/design-patterns/behavioral-patterns "Українська")
  [中文](https://refactoringguru.cn/design-patterns/behavioral-patterns "中文")
* [Contact us](https://feedback.refactoring.guru/?show_feedback_form_private=true "Contact us")
* [Sign in](https://refactoring.guru/login "Sign in")

* [Home](/)
* [Refactoring](/refactoring)
* [Design Patterns](/design-patterns)
* [Premium Content](/store)
* [Git Course](https://gitbybit.com/)
* [Forum](https://refactoring.userecho.com/)
* [Contact us](https://refactoring.userecho.com/)

2014-2026 [Refactoring.Guru](/). All rights reserved.  
 Illustrations by [Dmitry Zhart](http://zhart.us/)

* [Terms & Conditions](/terms)
* [Privacy Policy](/privacy-policy)
* [Content Usage Policy](/content-usage-policy)
* [About us](/site-about)

**Ukrainian office:**  

 FOP Olga Skobeleva  
 Abolmasova 7  
Kyiv, Ukraine, 02002  
 Email: support@refactoring.guru

**Spanish office:**  

 Oleksandr Shvets  
 Avda Pamplona 64  
Pamplona, Spain, 31009  
 Email: support@refactoring.guru

var CodeMirrorScripts = ["/js/codemirror.min.js?id=cb07f7f6cc70c9951e1c0da6a3aae38b"];
window.loadContent = true;window.loadCart = true;