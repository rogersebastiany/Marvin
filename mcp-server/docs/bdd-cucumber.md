Behaviour-Driven Development | Cucumber{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Behaviour-Driven Development","item":"https://cucumber.io/docs/bdd/"}]}

function gtag(){dataLayer.push(arguments)}window.dataLayer=window.dataLayer||[],gtag("js",new Date),gtag("config","G-YY58V5DFE7",{anonymize\_ip:!0})

!function(){var t=function(){try{return new URLSearchParams(window.location.search).get("docusaurus-theme")}catch(t){}}()||function(){try{return window.localStorage.getItem("theme")}catch(t){}}();document.documentElement.setAttribute("data-theme",t||"light"),document.documentElement.setAttribute("data-theme-choice",t||"light")}(),function(){try{const c=new URLSearchParams(window.location.search).entries();for(var[t,e]of c)if(t.startsWith("docusaurus-data-")){var a=t.replace("docusaurus-data-","data-");document.documentElement.setAttribute(a,e)}}catch(t){}}()

[Skip to main content](#__docusaurus_skipToContent_fallback)

[**Cucumber**](/)[Documentation](/docs)[Learn](/learn)[Community](/community)[Blog](/blog)[Sponsor](/sponsors)

Search

* [Introduction](/docs/)
* [Installation](/docs/installation/)
* [Guides](/docs/guides/)
* [Cucumber](/docs/cucumber/)
* [Gherkin](/docs/gherkin/)
* [Behaviour-Driven Development](/docs/bdd/)

  + [Discovery workshop](/docs/bdd/discovery-workshop)
  + [Example Mapping](/docs/bdd/example-mapping)
  + [Examples](/docs/bdd/examples)
  + [History of BDD](/docs/bdd/history)
  + [Myths about BDD](/docs/bdd/myths)
  + [Who does what?](/docs/bdd/who-does-what)
  + [Writing better Gherkin](/docs/bdd/better-gherkin)
* [Tools](/docs/tools/)
* [Terminology](/docs/terms/)
* [Contributing](/docs/contributing)
* [FAQs](/docs/faq)

* Behaviour-Driven Development

On this page

# Behaviour-Driven Development

Behaviour-Driven Development (BDD) is the software development process that Cucumber was built to support.

There's much more to BDD than just using Cucumber.

## What is BDD?[​](#what-is-bdd "Direct link to What is BDD?")

BDD is a way for software teams to work that closes the gap between business people and technical people by:

* Encouraging collaboration across roles to build shared understanding of the problem to be solved
* Working in rapid, small iterations to increase feedback and the flow of value
* Producing system documentation that is automatically checked against the system's behaviour

We do this by focusing collaborative work around concrete, real-world examples that illustrate how we want the system to behave. We use those examples to guide us from concept through to implementation, in a process of continuous collaboration.

### BDD and agile[​](#bdd-and-agile "Direct link to BDD and agile")

We assume that your team are using some kind of agile methodology already, planning work in small increments of value like [User Stories](/docs/terms/user-story/). BDD does not replace your existing agile process, it enhances it.

Think of BDD as a set of plugins for your existing process that will make your team more able to deliver on the promises of agile: timely, reliable releases of working software that meets your organisation’s evolving needs, requiring some maintenance effort and discipline.

### Rapid iterations[​](#rapid-iterations "Direct link to Rapid iterations")

We assume you would like to be able to respond quickly to feedback from your users, and do only the minimal work necessary to meet those needs.

BDD encourages working in rapid iterations, continuously breaking down your user's problems into small pieces that can flow through your development process as quickly as possible.

## Three practices[​](#three-practices "Direct link to Three practices")

Essentially, day-to-day BDD activity is a three-step, iterative process:

1. First, take a small upcoming change to the system -- a [User Story](/docs/terms/user-story/) -- and talk about concrete examples of the new functionality to explore, discover and agree on the details of what's expected to be done.
2. Next, document those examples in a way that can be automated, and check for agreement.
3. Finally, implement the behaviour described by each documented example, starting with an automated test to guide the development of the code.

The idea is to make each change small and iterate rapidly, moving back up a level each time you need more information. Each time you automate and implement a new example, you've added something valuable to your system, and you're ready to respond to feedback.

We call these practices *Discovery*, *Formulation*, and *Automation*.

Discovery, Formulation and Automation

Over time, the documented examples become an asset that enables your team to continue confidently and rapidly making changes to the system. The code reflects the documentation, and the documentation reflects the team's shared understanding of the problem domain. This shared understanding is constantly evolving.

There's lots to learn about each of these practices. We'll summarise each of them below.

### Discovery: What it *could* do[​](#discovery-what-it-could-do "Direct link to discovery-what-it-could-do")

> The hardest single part of building a software system is deciding precisely what to build.
>
> -- Fred Brooks, The mythical man-month

Although documentation and automated tests are produced by a BDD team, you can think of them as nice side-effects. The real goal is valuable, working software, and the fastest way to get there is through conversations between the people who are involved in imagining and delivering that software.

BDD helps teams to have the right conversations at the right time so you minimise the amount of time spent in meetings and maximising the amount of valuable code you produce.

We use structured conversations, called [discovery workshops](/docs/bdd/discovery-workshop/), that focus around real-world examples of the system from the users' perspective. These conversations grow our team's shared understanding of the needs of our users, of the rules that govern how the system should function, and of the scope of what needs to be done.

It may also reveal gaps in our understanding, where we need more information before we know what to do.

The scrutiny of a discovery session often reveals low-priority functionality that can be deferred from the scope of a user story, helping the team to work in smaller increments, improving their flow.

If you're new to BDD, discovery is the right place to start. You won't get much joy from the other two practices until you've mastered discovery.

### Formulation: What it *should* do[​](#formulation-what-it-should-do "Direct link to formulation-what-it-should-do")

As soon as we have identified at least one valuable example from our discovery sessions, we can now formulate each example as structured documentation. This gives us a quick way to confirm that we really do have a shared understanding of what to build.

In contrast to traditional documentation, we use [a medium that can be read by both humans and computers](/docs/gherkin), so that:

* We can get feedback from the whole team about our shared vision of what we're building.
* We'll be able to automate these examples to guide our development of the implementation.

By writing this executable specification collaboratively, we establish a shared language for talking about the system. This helps us to use problem-domain terminology all the way down into the code.

### Automation: What it *actually does*[​](#automation-what-it-actually-does "Direct link to automation-what-it-actually-does")

Now that we have our executable specification, we can use it to guide our development of the implementation.

Taking one example at a time, we automate it by connecting it to the system as a test. The test fails because we have not implemented the behaviour it describes yet. Now we develop the implementation code, using [lower-level examples of the behaviour of internal system components](https://www.geepawhill.org/2020/06/12/microtest-tdd-more-definition/) to guide us as required.

The automated examples work like guide-rails, helping us to keep our development work on track.

When we need to come back and maintain the system later, the automated examples will help us to understand what the system is currently doing, and to make changes safely without unintentionally breaking anything.

This rapid, repeatable feedback reduces the burden of manual regression testing, freeing people up to do more interesting work, like exploratory testing.

## Learn more[​](#learn-more "Direct link to Learn more")

Read the topics below to dig deeper and learn more about BDD.

[Edit this page](https://github.com/cucumber/website/blob/main/docs/bdd/index.md)

Last updated on **Aug 25, 2025**

[Previous

Step organization](/docs/gherkin/step-organization)[Next

Discovery workshop](/docs/bdd/discovery-workshop)

* [What is BDD?](#what-is-bdd)
  + [BDD and agile](#bdd-and-agile)
  + [Rapid iterations](#rapid-iterations)
* [Three practices](#three-practices)
  + [Discovery: What it *could* do](#discovery-what-it-could-do)
  + [Formulation: What it *should* do](#formulation-what-it-should-do)
  + [Automation: What it *actually does*](#automation-what-it-actually-does)
* [Learn more](#learn-more)

Copyright © 2014-2026 The Cucumber Open Source Project