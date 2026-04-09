The Twelve-Factor App 

try{Typekit.load();}catch(e){}

(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TK5QTP');

# [The Twelve-Factor App](/ "The Twelve-Factor App")

* [Blog](/blog)
* [Community](/community)
* [GitHub](https://github.com/twelve-factor/twelve-factor)

# Introduction

In the modern era, software is commonly delivered as a service: called *web apps*, or *software-as-a-service*. The twelve-factor app is a methodology for building software-as-a-service apps that:

* Use **declarative** formats for setup automation, to minimize time and cost for new developers joining the project;
* Have a **clean contract** with the underlying operating system, offering **maximum portability** between execution environments;
* Are suitable for **deployment** on modern **cloud platforms**, obviating the need for servers and systems administration;
* **Minimize divergence** between development and production, enabling **continuous deployment** for maximum agility;
* And can **scale up** without significant changes to tooling, architecture, or development practices.

The twelve-factor methodology can be applied to apps written in any programming language, and which use any combination of backing services (database, queue, memory cache, etc).

# Background

The contributors to this document have been directly involved in the development and deployment of hundreds of apps, and indirectly witnessed the development, operation, and scaling of hundreds of thousands of apps via our work on the [Heroku](http://www.heroku.com/) platform.

This document synthesizes all of our experience and observations on a wide variety of software-as-a-service apps in the wild. It is a triangulation on ideal practices for app development, paying particular attention to the dynamics of the organic growth of an app over time, the dynamics of collaboration between developers working on the app’s codebase, and [avoiding the cost of software erosion](http://blog.heroku.com/archives/2011/6/28/the_new_heroku_4_erosion_resistance_explicit_contracts/).

Our motivation is to raise awareness of some systemic problems we’ve seen in modern application development, to provide a shared vocabulary for discussing those problems, and to offer a set of broad conceptual solutions to those problems with accompanying terminology. The format is inspired by Martin Fowler’s books *[Patterns of Enterprise Application Architecture](https://books.google.com/books/about/Patterns_of_enterprise_application_archi.html?id=FyWZt5DdvFkC)* and *[Refactoring](https://books.google.com/books/about/Refactoring.html?id=1MsETFPD3I0C)*.

# Who should read this document?

Any developer building applications which run as a service. Ops engineers who deploy or manage such applications.

# The Twelve Factors

## [I. Codebase](./codebase)

### One codebase tracked in revision control, many deploys

## [II. Dependencies](./dependencies)

### Explicitly declare and isolate dependencies

## [III. Config](./config)

### Store config in the environment

## [IV. Backing services](./backing-services)

### Treat backing services as attached resources

## [V. Build, release, run](./build-release-run)

### Strictly separate build and run stages

## [VI. Processes](./processes)

### Execute the app as one or more stateless processes

## [VII. Port binding](./port-binding)

### Export services via port binding

## [VIII. Concurrency](./concurrency)

### Scale out via the process model

## [IX. Disposability](./disposability)

### Maximize robustness with fast startup and graceful shutdown

## [X. Dev/prod parity](./dev-prod-parity)

### Keep development, staging, and production as similar as possible

## [XI. Logs](./logs)

### Treat logs as event streams

## [XII. Admin processes](./admin-processes)

### Run admin/management tasks as one-off processes

[Česky (cs)](/cs/) | [Deutsch (de)](/de/) | [Ελληνικά (el)](/el/) | English (en) | [Español (es)](/es/) | [فارسی (fa)](/fa/) | [Français (fr)](/fr/) | [Italiano (it)](/it/) | [日本語 (ja)](/ja/) | [한국어 (ko)](/ko/) | [Polski (pl)](/pl/) | [Português do Brasil (pt\_br)](/pt_br/) | [Русский (ru)](/ru/) | [Slovensky (sk)](/sk/) | [ภาษาไทย (th)](/th/) | [Türkçe (tr)](/tr/) | [Українська (uk)](/uk/) | [Tiếng Việt (vi)](/vi/) | [简体中文 (zh\_cn)](/zh_cn/)

Written by Adam Wiggins • Last updated 2017 • [Sourcecode](https://github.com/heroku/12factor) • [Download ePub Book](/12factor.epub)

© Copyright 2026 Salesforce, Inc. All rights reserved. Various trademarks held by their respective owners. Salesforce Tower, 415 Mission Street, 3rd Floor, San Francisco, CA 94105, United States

[Legal](https://www.salesforce.com/company/legal/) [Terms of Service](https://www.salesforce.com/company/legal/sfdc-website-terms-of-service/) [Privacy Information](https://www.salesforce.com/company/privacy/) [Responsible Disclosure](https://www.salesforce.com/company/disclosure/) [Trust](https://trust.salesforce.com/en/) [Contact](https://www.salesforce.com/form/contact/contactme/?d=70130000000EeYa) [Your Privacy Choices](https://www.salesforce.com/form/other/privacy-request/) [Cookie Preferences](#)