# Software Engineering Principles


---

## 1. [Domain Driven Design](DomainDrivenDesign.html)

22 April 2020

[Martin Fowler](/)

[evolutionary design](/tags/evolutionary%20design.html)

[domain driven design](/tags/domain%20driven%20design.html)

[application architecture](/tags/application%20architecture.html)

Domain-Driven Design is an approach to software development that centers
the development on programming a domain model that has a rich understanding of
the processes and rules of a domain. The name comes from a 2003 book by
Eric Evans that describes the approach through a catalog of patterns. Since
then a community of practitioners have further developed the ideas, spawning
various other books and training courses. The approach is particularly suited
to complex domains, where a lot of often-messy logic needs to be
organized.

The idea that software systems need to be based on a well-developed model
of a domain has been around for at least as long as I've been in the industry.
I learned much of this thinking from Jim Odell, who developed this style of
thinking with data modeling, information engineering, and object-oriented
analysis. Representing the underlying domain was a key part of much work in
the database and object-oriented communities throughout the 1980s and 1990s.

Eric Evans's great contribution to this, through his book, was developing a
vocabulary to talk about this approach, identifying key conceptual elements
that went beyond the various modeling notations that dominated the discussion
at the time. At the heart of this was the idea that to develop software for a
complex domain, we need to build [Ubiquitous Language](/bliki/UbiquitousLanguage.html) that
embeds domain terminology into the software systems that we build. While many
folks talked about developing such models, they were often only done on paper,
and usually expected to be done up-front. DDD stresses doing them in software,
and evolving them during the life of the software product. Eric is a strong
proponent of [Extreme Programming](/bliki/ExtremeProgramming.html) and sees Domain-Driven
Design as a natural component of an extreme programming approach - a view
shared by most XP practitioners I know.

The book introduced the notion of classifying objects into Entities, Value
Objects, and Service Objects - what I call the [Evans Classification](/bliki/EvansClassification.html) and identifying the concept of [Aggregates](/bliki/DDD_Aggregate.html). I found these filled an important
gap in thinking about objects which eluded both programming languages and
diagrammatic notations. A particularly important part of DDD is the notion of
Strategic Design - how to organize large domains into a network of [Bounded Contexts](/bliki/BoundedContext.html). Until that point, I'd not seen anyone
tackle this issue in any compelling way.

Although Eric's background is rooted in the Object-Oriented community, the
core notions of Domain-Driven Design are conceptual, and thus apply well with
any programming approach - a fact that's especially true of the strategic
design aspects.

## Further Reading

[Eric's original book](https://www.amazon.com/gp/product/0321125215/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321125215&linkCode=as2&tag=martinfowlerc-20) has a reputation for
being a hard book to read, but I honestly believe that it repays the effort
and deserves a place on any serious developer's bookshelf. [Vaughn Vernon's
2013 book](https://www.amazon.com/gp/product/0321834577/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321834577&linkCode=as2&tag=martinfowlerc-20) is a good next step, describing some later thinking and focusing particularly on the
strategic design aspect.

---

## 2. [Continuous Delivery](ContinuousDelivery.html)

30 May 2013

[Martin Fowler](/)

[continuous delivery](/tags/continuous%20delivery.html)

[version control](/tags/version%20control.html)

Continuous Delivery is a software development discipline where
you build software in such a way that the software can be released
to production at any time.

You’re doing continuous delivery when: 1

1: 
These indicators were developed by the Continuous Delivery
working group at Thoughtworks

* Your software is deployable throughout its lifecycle
* Your team prioritizes keeping the software deployable over working on new features
* Anybody can get fast, automated feedback on the production readiness of their systems any time somebody makes a change to them
* You can perform push-button deployments of any version of the software to any environment on demand

You achieve continuous delivery by
continuously integrating the software done by the development team,
building executables, and running automated tests on those
executables to detect problems. Furthermore you push the executables
into increasingly production-like environments to ensure the
software will work in production. To do this you use a
[DeploymentPipeline](/bliki/DeploymentPipeline.html).

The key test is that a business sponsor could request that **the
current development version of the software can be deployed into
production at a moment's notice** - and nobody would bat an eyelid,
let alone panic.

To achieve continuous delivery you need:

* a close, collaborative working
  relationship between everyone involved in delivery (often referred
  to as a [DevOpsCulture](/bliki/DevOpsCulture.html)2).

2: 
Despite the name “devops” this should extend beyond developers
and operations to include testers, database teams, and anyone
else needed to get software into production.

* extensive automation of all possible parts of the delivery
  process, usually using a [DeploymentPipeline](/bliki/DeploymentPipeline.html)

Continuous Delivery is sometimes confused with Continuous
Deployment. **Continuous Deployment** means that every change goes
through the pipeline and automatically gets put into production,
resulting in many production deployments every day. Continuous
Delivery just means that you are able to do frequent deployments but
may choose not to do it, usually due to businesses preferring a
slower rate of deployment. In order to do Continuous Deployment you
must be doing Continuous Delivery.

[Continuous
Integration](/articles/continuousIntegration.html) usually refers to integrating, building, and testing
code within the development environment. Continuous Delivery builds
on this, dealing with the final stages required for production
deployment.

The principal benefits of continuous delivery are:

* **Reduced Deployment Risk:** since you are deploying smaller
  changes, there's less to go wrong and it's easier to fix should a
  problem appear.
* **Believable Progress:** many folks track progress by
  tracking work done. If “done” means “developers declare it to be
  done” that's much less believable than if it's deployed into a production
  (or production-like) environment.
* **User Feedback:** the biggest risk to any software effort
  is that you end up building something that isn't useful. The
  earlier and more frequently you get working software in front of
  real users, the quicker you get feedback to find out how valuable
  it really is (particularly if you use [ObservedRequirements](/bliki/ObservedRequirement.html)).

User feedback does require you to be doing continuous deployment.
If you want that, but don't fancy getting new software to your
entire user base, you can deploy to a subset of users. In a recent
project of ours, a retailer deployed its new online system first to
its employees, then to an invited set of premium customers, and
finally to all customers.

## Further Reading

For more information the best online source is Jez Humble's [Continuous Delivery](http://continuousdelivery.com/) page.
(In particular [Jez explains why](https://continuousdelivery.com/2010/08/continuous-delivery-vs-continuous-deployment/) he and Dave Farley chose
the name Continuous Delivery and contrasts it with Continuous Deployment.)
For more details, you
should go to [the book](/books/continuousDelivery.html). I also list some resources on my [guide page](/delivery.html).

## Acknowledgements

[Jez Humble](http://jezhumble.com) provided
detailed help with this page.

## Notes

1: 
These indicators were developed by the Continuous Delivery
working group at Thoughtworks

2: 
Despite the name “devops” this should extend beyond developers
and operations to include testers, database teams, and anyone
else needed to get software into production.

Updated on 12 August 2014 to add text on benefits and deploying
to a subset of users.

---

## 3. Introduction

In the modern era, software is commonly delivered as a service: called *web apps*, or *software-as-a-service*. The twelve-factor app is a methodology for building software-as-a-service apps that:

* Use **declarative** formats for setup automation, to minimize time and cost for new developers joining the project;
* Have a **clean contract** with the underlying operating system, offering **maximum portability** between execution environments;
* Are suitable for **deployment** on modern **cloud platforms**, obviating the need for servers and systems administration;
* **Minimize divergence** between development and production, enabling **continuous deployment** for maximum agility;
* And can **scale up** without significant changes to tooling, architecture, or development practices.

The twelve-factor methodology can be applied to apps written in any programming language, and which use any combination of backing services (database, queue, memory cache, etc).

---

## 4. [CQRS](CQRS.html)

14 July 2011

[Martin Fowler](/)

[domain driven design](/tags/domain%20driven%20design.html)

[application architecture](/tags/application%20architecture.html)

[API design](/tags/API%20design.html)

[event architectures](/tags/event%20architectures.html)

CQRS stands for **Command Query Responsibility Segregation**. It's a pattern that
I first heard described by [Greg Young](https://twitter.com/gregyoung). At its heart is the
notion that you can use a different model to update information than the model you use
to read information. For some situations, this separation can be valuable, but beware
that for most systems CQRS adds risky complexity.

The mainstream approach people use for interacting with an
information system is to treat it as a CRUD datastore. By this I
mean that we have mental model of some record structure where we can
**c**reate new records, **r**ead records, **u**pdate
existing records, and **d**elete records when we're done with
them. In the simplest case, our interactions are all about storing
and retrieving these records.

As our needs become more sophisticated we steadily move away from
that model. We may want to look at the information in a different
way to the record store, perhaps collapsing multiple records
into one, or forming virtual records by combining information for
different places. On the update side we may find validation rules
that only allow certain combinations of data to be stored, or may
even infer data to be stored that's different from that we
provide.

As this occurs we begin to see multiple representations of
information. When users interact with the information they use
various presentations of this information, each of which is a
different representation. Developers typically build their own
conceptual model which they use to manipulate the core elements of
the model. If you're using a Domain Model, then this is usually the
conceptual representation of the domain. You typically also make the
persistent storage as close to the conceptual model as you can.

This structure of multiple layers of representation can get quite
complicated, but when people do this they still resolve it down to a
single conceptual representation which acts as a conceptual
integration point between all the presentations.

The change that CQRS introduces is to split that conceptual model
into separate models for update and display, which it refers to as
Command and Query respectively following the vocabulary of
[CommandQuerySeparation](/bliki/CommandQuerySeparation.html). The rationale is that for many
problems, particularly in more complicated domains, having the same
conceptual model for commands and queries leads to a more complex model that
does neither well.

By separate models we most commonly mean different object models,
probably running in different logical processes, perhaps on separate
hardware. A web example would see a user looking at a web page
that's rendered using the query model. If they initiate a change
that change is routed to the separate command model for processing, the
resulting change is communicated to the query model to render the
updated state.

There's room for considerable variation here. The in-memory
models may share the same database, in which case the database acts
as the communication between the two models. However they may also
use separate databases, effectively making the query-side's database
into a real-time [ReportingDatabase](/bliki/ReportingDatabase.html). In this case there
needs to be some communication mechanism between the two models or
their databases.

The two models might not be separate object models, it could be
that the same objects have different interfaces for their command
side and their query side, rather like views in relational
databases. But usually when I hear of CQRS, they are clearly
separate models.

CQRS naturally fits with some other architectural
patterns.

* As we move away from a single representation that we interact
  with via CRUD, we can easily move to a task-based UI.
* CQRS fits well with [event-based
  programming models](/eaaDev/EventNarrative.html). It's common to see CQRS system split into separate services
  communicating with [Event
  Collaboration](/eaaDev/EventCollaboration.html). This allows these services to easily take advantage of [Event Sourcing](../eaaDev/EventSourcing.html).
* Having separate models raises questions about how hard to keep
  those models consistent, which raises the likelihood of using
  [eventual consistency](http://www.allthingsdistributed.com/2008/12/eventually_consistent.html).
* For many domains, much of the logic is needed when you're
  updating, so it may make sense to use
  [EagerReadDerivation](/bliki/EagerReadDerivation.html) to simplify your query-side models.
* If the write model generates events for all updates, you can structure read models
  as [EventPosters](/bliki/EventPoster.html), allowing them to be [MemoryImages](/bliki/MemoryImage.html) and thus
  avoiding a lot of database interactions.
* CQRS is suited to complex domains, the kind that also benefit
  from [Domain-Driven Design](https://www.amazon.com/gp/product/0321125215/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321125215&linkCode=as2&tag=martinfowlerc-20).

## When to use it

Like any pattern, CQRS is useful in some places, but not in
others. Many systems do fit a CRUD mental model, and so should be
done in that style. CQRS is a significant mental leap for all
concerned, so shouldn't be tackled unless the benefit is worth the
jump. While I have come across successful uses of CQRS, so far the
majority of cases I've run into have not been so good, with CQRS
seen as a significant force for getting a software system into
serious difficulties.

In particular CQRS should only be used on specific portions of a
system (a [BoundedContext](/bliki/BoundedContext.html) in DDD lingo) and not the system as a whole. In this
way of thinking, each Bounded Context needs its own decisions on how
it should be modeled.

So far I see benefits in two directions. Firstly is that a few
complex domains may be easier to tackle by using CQRS. I must
stress, however, that such suitability for CQRS is very much the
minority case. Usually there's enough overlap between the command and
query sides that sharing a model is easier. Using CQRS on a domain
that doesn't match it will add complexity, thus reducing
productivity and increasing risk.

The other main benefit is in handling high performance
applications. CQRS allows you to separate the load from reads and
writes allowing you to scale each independently. If your application
sees a big disparity between reads and writes this is very
handy. Even without that, you can apply different optimization
strategies to the two sides. An example of this is using different
database access techniques for read and update.

If your domain isn't suited to CQRS, but you have demanding
queries that add complexity or performance problems, remember that
you can still use a [ReportingDatabase](/bliki/ReportingDatabase.html). CQRS uses a
separate model for all queries. With a reporting database you still
use your main system for most queries, but offload the more
demanding ones to the reporting database.

Despite these benefits, **you should be very cautious about
using CQRS**. Many information systems fit well with the notion of
an information base that is updated in the same way that it's read,
adding CQRS to such a system can add significant complexity. I've
certainly seen cases where it's made a significant drag on
productivity, adding an unwarranted amount of risk to the project,
even in the hands of a capable team. So while CQRS is a pattern
that's good to have in the toolbox, beware that it is difficult to
use well and you can easily chop off important bits if you mishandle
it.

## Further Reading

* [Greg Young](http://codebetter.com/gregyoung/) was the first person I heard talking about this
  approach - this is [the summary from him](http://codebetter.com/gregyoung/2010/02/16/cqrs-task-based-uis-event-sourcing-agh/) that I like best.
* Udi Dahan is another advocate of CQRS, he has a [detailed
  description](http://www.udidahan.com/2009/12/09/clarified-cqrs/) of the technique.
* There is an [active mailing list](http://groups.google.com/group/dddcqrs) to
  discuss the approach.

---

## 5. [Test Pyramid](TestPyramid.html)

1 May 2012

[Martin Fowler](/)

[testing](/tags/testing.html)

The test pyramid is a way of thinking about how different kinds of automated
tests should be used to create a balanced portfolio. Its essential point is
that you should have many more low-level [UnitTests](/bliki/UnitTest.html) than high level
[BroadStackTests](/bliki/BroadStackTest.html) running through a GUI.

For much of my career test automation meant tests that drove an
application through its user-interface. Such tools would often
provide the facility to record an interaction with the application
and then allow you to play back that interaction, checking that the
application returned the same results. Such an approach works well
initially. It's easy to record tests, and the tests can be recorded
by people with no knowledge of programming.

But this kind of approach quickly runs into trouble, becoming an
[ice-cream cone](https://alisterscott.github.io/TestingPyramids.html). Testing
through the UI like this is slow, increasing build times. Often it
requires installed licences for the test automation software, which
means it can only be done on particular machines. Usually these cannot
easily be run in a “headless” mode, monitored by scripts to put in a
proper deployment pipeline.

Most importantly such tests are very brittle. An enhancement to
the system can easily end up breaking lots of such tests, which then
have to be re-recorded. You can reduce this problem by abandoning
record-playback tools, but that makes the tests harder to write.
1 Even with good practices on
writing them, end-to-end tests are more prone to [non-determinism problems](../articles/nonDeterminism.html),
which can undermine trust in them. In short, tests that run end-to-end through the UI are:
brittle, expensive to write, and time consuming to run. So the
pyramid argues that you should do much more automated testing
through unit tests than you should through traditional GUI based
testing. 2

1: 
Record-playback tools are almost always a bad idea for any kind
of automation, since they resist changeability and obstruct
useful abstractions. They are only worth having as a tool to
generate fragments of scripts which you can then edit as a
proper programming language, in the manner of the venerable [Emacs](http://www.gnu.org/software/emacs/manual/html_node/emacs/Save-Keyboard-Macro.html).

2: 
The pyramid is based on the assumption that broad-stack tests are expensive, slow,
and brittle compared to more focused tests, such as unit tests. While this is usually
true, there are exceptions. If my high level tests are fast, reliable, and cheap to
modify - then lower-level tests aren't needed.

The pyramid also argues for an intermediate layer of tests that
act through a service layer of an application, what I refer to as
[SubcutaneousTests](/bliki/SubcutaneousTest.html). These can provide many of the
advantages of end-to-end tests but avoid many of the complexities of
dealing with UI frameworks. In web applications this would correspond
to testing through an API layer while the top UI part of the pyramid
would correspond to tests using something like [Selenium](http://seleniumhq.org/) or Sahi.

The test pyramid comes up a lot in Agile testing circles and
while its core message is sound, there is much more to say
about building a well-balanced test portfolio. A
common problem is that teams conflate the concepts of end-to-end
tests, UI tests, and customer facing tests. These are all orthogonal
characteristics. For example a rich javascript UI should have most
of its UI behavior tested with javascript unit tests using something
like [Jasmine](http://jasmine.github.io/). A
complex set of business rules could have tests captured in a
customer-facing form, but run just on the relevant module much as
unit tests are.

I always argue that high-level tests are there as a
second line of test defense. If you get a failure in a high level
test, not just do you have a bug in your functional code, you also
have a missing or incorrect unit test. Thus I advise that before fixing a bug exposed by
a high level test, you should replicate the bug with a unit test. Then the unit test
ensures the bug stays dead.

## Further Reading

The [Google Testing Blog](http://googletesting.blogspot.co.uk/2015/04/just-say-no-to-more-end-to-end-tests.html) expands on why you shouldn't rely on
end-to-end tests.

Adrian Sutton explains LMAX's experience which shows that [end-to-end tests can play a large and valuable
role](https://www.symphonious.net/2015/04/30/making-end-to-end-tests-work/).

Some writers argue that the pyramid isn't a good test distribution,
preferring more integration tests and few unit tests. But difference is
probably illusory due to [different definitions of “unit test”](/articles/2021-test-shapes.html).

## Acknowledgements

Kevin Dishman gave me the idea of adding the cost and speed arrows to the illustration

## Etymology

Most people know about the the Test Pyramid due to [Mike Cohn](http://www.mountaingoatsoftware.com/), when he described it in his
2009 book [Succeeding with Agile](https://www.amazon.com/gp/product/0321579364/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321579364&linkCode=as2&tag=martinfowlerc-20). In the book he
refers to it as the “Test Automation Pyramid”, but in use it's generally referred to
as just the “test pyramid”. He originally drew it in conversation with Lisa Crispin
in 2003-4 and described it at a scrum gathering in 2004. Jason Huggins independently
came up with the same idea [around 2006](http://agiletesting.blogspot.com/2006/02/thoughts-on-giving-successful-talk.html).

## Revisions

7 Aug 2016: changed illustration

15 Nov 2017: added etymology

## Notes

1: 
Record-playback tools are almost always a bad idea for any kind
of automation, since they resist changeability and obstruct
useful abstractions. They are only worth having as a tool to
generate fragments of scripts which you can then edit as a
proper programming language, in the manner of the venerable [Emacs](http://www.gnu.org/software/emacs/manual/html_node/emacs/Save-Keyboard-Macro.html).

2: 
The pyramid is based on the assumption that broad-stack tests are expensive, slow,
and brittle compared to more focused tests, such as unit tests. While this is usually
true, there are exceptions. If my high level tests are fast, reliable, and cheap to
modify - then lower-level tests aren't needed.

---

## 6. Microservices

a definition of this new architectural term

*The term “Microservice Architecture” has sprung up over the
last few years to describe a particular way of designing software
applications as suites of independently deployable services. While
there is no precise definition of this architectural style, there
are certain common characteristics around organization around
business capability, automated deployment, intelligence in the
endpoints, and decentralized control of languages and data.*

25 March 2014

---

[James Lewis](https://twitter.com/boicy)

James Lewis is a Principal Consultant at Thoughtworks and
member of the Technology Advisory Board. James' interest in
building applications out of small collaborating services stems
from a background in integrating enterprise systems at scale.
He's built a number of systems using microservices and has been
an active participant in the growing community for a couple of
years.

[Martin Fowler](https://martinfowler.com)

Martin Fowler is an author, speaker, and general loud-mouth
on software development. He's long been puzzled by the problem
of how to componentize software systems, having heard more vague claims
than he's happy with. He hopes that microservices will live up
to the early promise its advocates have found.

[application architecture](/tags/application%20architecture.html)

[microservices](/tags/microservices.html)

## Contents

* [Characteristics of a Microservice Architecture](#CharacteristicsOfAMicroserviceArchitecture)
  + [Componentization via Services](#ComponentizationViaServices)
  + [Organized around Business Capabilities](#OrganizedAroundBusinessCapabilities)
  + [Products not Projects](#ProductsNotProjects)
  + [Smart endpoints and dumb pipes](#SmartEndpointsAndDumbPipes)
  + [Decentralized Governance](#DecentralizedGovernance)
  + [Decentralized Data Management](#DecentralizedDataManagement)
  + [Infrastructure Automation](#InfrastructureAutomation)
  + [Design for failure](#DesignForFailure)
  + [Evolutionary Design](#EvolutionaryDesign)
* [Are Microservices the Future?](#AreMicroservicesTheFuture)

### Sidebars

* [How big is a microservice?](#HowBigIsAMicroservice)
* [Microservices and SOA](#MicroservicesAndSoa)
* [Many languages, many options](#ManyLanguagesManyOptions)
* [Battle-tested standards and enforced standards](#Battle-testedStandardsAndEnforcedStandards)
* [Make it easy to do the right thing](#MakeItEasyToDoTheRightThing)
* [The circuit breaker and production ready code](#TheCircuitBreakerAndProductionReadyCode)
* [Synchronous calls considered harmful](#SynchronousCallsConsideredHarmful)

---

“Microservices” - yet another new term on the crowded streets
of software architecture. Although our natural inclination is to
pass such things by with a contemptuous glance, this bit of
terminology describes a style of software systems that we are
finding more and more appealing. We've seen many projects use this
style in the last few years, and results so far have been
positive, so much so that for many of our colleagues this is
becoming the default style for building enterprise
applications. Sadly, however, there's not much information that
outlines what the microservice style is and how to do it.

In short, the microservice architectural style 1 is an approach
to developing a single application as a suite of small services,
each running in its own process and communicating with lightweight
mechanisms, often an HTTP resource API. These services are built
around business capabilities and independently deployable by fully
automated deployment machinery. There is a bare minimum of
centralized management of these services, which may be written in
different programming languages and use different data storage
technologies.

1: 
The term “microservice” was discussed at a workshop of software
architects near Venice in May, 2011 to describe what the
participants saw as a common architectural style that many of
them had been recently exploring. In May 2012, the same group decided on
“microservices” as the most appropriate name. James presented some of these
ideas as a case study in March 2012 at 33rd Degree in Krakow in
[Microservices
- Java, the Unix Way](http://2012.33degree.org/talk/show/67) as did Fred George [about
the same time](http://www.slideshare.net/fredgeorge/micro-service-architecure). Adrian Cockcroft at Netflix, describing this
approach as “fine grained SOA” was pioneering the style at web
scale as were many of the others mentioned in this article - Joe
Walnes, Daniel Terhorst-North, Evan Botcher and
Graham Tackley.

To start explaining the microservice style it's useful to
compare it to the monolithic style: a monolithic application built
as a single unit. Enterprise Applications are often built in three main parts: a
client-side user interface (consisting of HTML pages and
javascript running in a browser on the user's machine) a database
(consisting of many tables inserted into a common, and usually
relational, database management system), and a server-side
application. The server-side application will handle HTTP
requests, execute domain logic, retrieve and update data from the
database, and select and populate HTML views to be sent to the
browser. This server-side application is a *monolith* - a single
logical executable2. Any changes to the
system involve building and deploying a new version of the
server-side application.

2: 
The term monolith has been in use by the Unix community for some
time. It appears in [The Art of Unix
Programming](https://www.amazon.com/gp/product/B003U2T5BA/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B003U2T5BA&linkCode=as2&tag=martinfowlerc-20) to describe systems that get too big.

Such a monolithic server is a natural way to approach building
such a system. All your logic for handling a request runs in a
single process, allowing you to use the basic features of your
language to divide up the application into classes, functions, and
namespaces. With some care, you can run and test the application
on a developer's laptop, and use a deployment pipeline to ensure
that changes are properly tested and deployed into production. You
can horizontally scale the monolith by running many instances
behind a load-balancer.

Monolithic applications can be successful, but increasingly
people are feeling frustrations with them - especially as more
applications are being deployed to the cloud . Change cycles are
tied together - a change made to a small part of the application,
requires the entire monolith to be rebuilt and deployed. Over time
it's often hard to keep a good modular structure, making it harder
to keep changes that ought to only affect one module within that
module. Scaling requires scaling of the entire application rather
than parts of it that require greater resource.

Figure 1: Monoliths
and Microservices

These frustrations have led to the microservice architectural
style: building applications as suites of services. As well as the
fact that services are independently deployable and scalable, each
service also provides a firm module boundary, even allowing for
different services to be written in different programming
languages. They can also be managed by different teams .

We do not claim that the microservice style is novel
or innovative, its roots go back at least to the design principles
of Unix. But we do think that not enough people consider a
microservice architecture and that many software developments
would be better off if they used it.

## Characteristics of a Microservice Architecture

We cannot say there is a formal definition of the
microservices architectural style, but we can attempt to
describe what we see as common characteristics for architectures
that fit the label. As with any definition that outlines common
characteristics, not all microservice architectures have all the
characteristics, but we do expect that most microservice
architectures exhibit most characteristics. While we authors
have been active members of this rather loose community, our
intention is to attempt a description of what we see in our own
work and in similar efforts by teams we know of. In particular
we are not laying down some definition to conform to.

### Componentization via Services

For as long as we've been involved in the software
industry, there's been a desire to build systems by plugging
together components, much in the way we see things are made in
the physical world. During the last couple of decades we've
seen considerable progress with large compendiums of common
libraries that are part of most language platforms.

When talking about components we run into the difficult
definition of what makes a component. [Our definition](/bliki/SoftwareComponent.html) is that a
**component** is a unit of software that is
independently replaceable and upgradeable.

Microservice architectures will use libraries, but their
primary way of componentizing their own software is by
breaking down into services. We define **libraries**
as components that are linked into a program and called using
in-memory function calls, while **services** are
out-of-process components who communicate with a mechanism such
as a web service request, or remote procedure call. (This is a
different concept to that of a service object in many OO
programs 3.)

3: 
Many object-oriented designers, including ourselves, use the
term service object in the [Domain-Driven
Design](https://www.amazon.com/gp/product/0321125215/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321125215&linkCode=as2&tag=martinfowlerc-20) sense for an object that carries out a significant
process that isn't tied to an entity. This is a different
concept to how we're using “service” in this article. Sadly the
term service has both meanings and we have to live with the
polyseme.

One main reason for using services as components (rather
than libraries) is that services are independently deployable.
If you have an application 4 that consists of a multiple
libraries in a single process, a change to any single component
results in having to redeploy the entire application. But if
that application is decomposed into multiple services, you can
expect many single service changes to only require
that service to be redeployed. That's not an absolute, some
changes will change service interfaces resulting in some
coordination, but the aim of a good microservice architecture is
to minimize these through cohesive service boundaries and
evolution mechanisms in the service contracts.

4: 
We consider [an application to be a social
construction](/bliki/ApplicationBoundary.html) that binds together a code base, group of
functionality, and body of funding.

Another consequence of using services as components is a
more explicit component interface. Most languages do not have
a good mechanism for defining an explicit [Published Interface](/bliki/PublishedInterface.html). Often it's only documentation and
discipline that prevents clients breaking a component's
encapsulation, leading to overly-tight coupling between
components. Services make it easier to avoid this by using
explicit remote call mechanisms.

Using services like this does have downsides. Remote calls
are more expensive than in-process calls, and thus remote APIs
need to be coarser-grained, which is often more awkward to
use. If you need to change the allocation of responsibilities
between components, such movements of behavior are harder to
do when you're crossing process boundaries.

At a first approximation, we can observe that services map
to runtime processes, but that is only a first approximation.
A service may consist of multiple processes that will always
be developed and deployed together, such as an application
process and a database that's only used by that service.

### Organized around Business Capabilities

When looking to split a large application into parts,
often management focuses on the technology layer, leading to
UI teams, server-side logic teams, and database teams. When
teams are separated along these lines, even simple changes can
lead to a cross-team project taking time and budgetary approval. A smart team will
optimise around this and plump for the lesser of two evils -
just force the logic into whichever application they have
access to. Logic everywhere in other words. This is an example
of [Conway's Law](/bliki/ConwaysLaw.html) in action.

> Any organization that designs a system (defined broadly)
> will produce a design whose structure is a copy of the
> organization's communication structure.
>
> -- Melvin Conway, 1968

Figure 2: Conway's
Law in action

The microservice approach to division is different,
splitting up into services organized around
**business capability**. Such services take a
broad-stack implementation of software for that business area,
including user-interface, persistant storage, and any external
collaborations. Consequently the teams are cross-functional,
including the full range of skills required for the
development: user-experience, database, and project
management.

Figure 3: Service
boundaries reinforced by team boundaries

One company organised in this way is [www.comparethemarket.com](http://www.comparethemarket.com).
Cross functional teams are responsible for building and operating
each product and each product is split out into a number of
individual services communicating via a message bus.

Large monolithic applications can always be modularized
around business capabilities too, although that's not the
common case. Certainly we would urge a large team building a
monolithic application to divide itself along business lines.
The main issue we have seen here, is that they tend to be
organised around *too many* contexts. If the monolith
spans many of these modular boundaries it can be difficult for individual
members of a team to fit them into their short-term
memory. Additionally we see that the modular
lines require a great deal of discipline to enforce. The
necessarily more explicit separation required by service
components makes it easier to keep the team boundaries clear.

### Products not Projects

Most application development efforts that we see use a
project model: where the aim is to deliver some piece of
software which is then considered to be completed. On
completion the software is handed over to a
maintenance organization and the project team that built it is
disbanded.

Microservice proponents tend to avoid this model,
preferring instead the notion that a team should own a product
over its full lifetime. A common inspiration for this is
Amazon's notion of [“you build, you
run it”](https://queue.acm.org/detail.cfm?id=1142065) where a development team takes full responsibility
for the software in production. This brings developers into
day-to-day contact with how their software behaves in
production and increases contact with their users, as they
have to take on at least some of the support burden.

The product mentality, ties in with the linkage to business
capabilities. Rather than looking at the software as a set of
functionality to be completed, there is an on-going
relationship where the question is how can software assist its
users to enhance the business capability.

There's no reason why this same approach can't be taken
with monolithic applications, but the smaller granularity of
services can make it easier to create the personal
relationships between service developers and their users.

### Smart endpoints and dumb pipes

When building communication structures between different
processes, we've seen many products and approaches that stress
putting significant smarts into the communication mechanism
itself. A good example of this is the Enterprise Service Bus
(ESB), where ESB products often include sophisticated
facilities for message routing, choreography, transformation,
and applying business rules.

The microservice community favours an alternative approach:
*smart endpoints and dumb pipes*. Applications
built from microservices aim to be as decoupled and as
cohesive as possible - they own their own domain logic and act
more as filters in the classical Unix sense - receiving a
request, applying logic as appropriate and producing a
response. These are choreographed using simple RESTish protocols rather
than complex protocols such as WS-Choreography or BPEL or
orchestration by a central tool.

The two protocols used most commonly are HTTP
request-response with resource API's and lightweight
messaging7. The best expression of
the first is

7: 
At extremes of scale, organisations often move to binary
protocols - [protobufs](https://code.google.com/p/protobuf/) for
example. Systems using these still exhibit the characteristic of
smart endpoints, dumb pipes - and trade off *transparency*
for scale. Most web properties and certainly the vast majority
of enterprises don't need to make this tradeoff - transparency
can be a big win.

> Be of the web, not behind the web
>
> -- [Ian Robinson](https://www.amazon.com/gp/product/0596805829/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0596805829&linkCode=as2&tag=martinfowlerc-20)

Microservice teams use the principles and
protocols that the world wide web (and to a large extent,
Unix) is built on. Often used resources can be cached with very
little effort on the part of developers or operations
folk.

The second approach in common use is messaging over a
lightweight message bus. The infrastructure chosen is
typically dumb (dumb as in acts as a message router only) -
simple implementations such as RabbitMQ or ZeroMQ don't do
much more than provide a reliable asynchronous fabric - the
smarts still live in the end points that are producing and
consuming messages; in the services.

In a monolith, the components are executing in-process and
communication between them is via either method invocation or
function call. The biggest issue in changing a monolith into
microservices lies in changing the communication pattern. A
naive conversion from in-memory method calls to RPC leads to
chatty communications which don't perform well. Instead you
need to replace the fine-grained communication with a coarser
-grained approach.

### Decentralized Governance

One of the consequences of centralised governance is the
tendency to standardise on single technology
platforms. Experience shows that this approach is constricting
- not every problem is a nail and not every solution a
hammer. We prefer using the right tool for the job and
while monolithic applications can take advantage of different
languages to a certain extent, it isn't that common.

Splitting the monolith's components out into services we
have a choice when building each of them. You want to use
Node.js to standup a simple reports page? Go for it. C++ for a
particularly gnarly near-real-time component? Fine. You want
to swap in a different flavour of database that better suits
the read behaviour of one component? We have the technology to
rebuild him.

Of course, just because you *can* do something,
doesn't mean you *should* - but partitioning your system
in this way means you have the option.

Teams building microservices prefer a different approach to
standards too. Rather than use a set of defined standards
written down somewhere on paper they prefer the idea of
producing useful tools that other developers can use to solve
similar problems to the ones they are facing. These tools are
usually harvested from implementations and shared with a wider
group, sometimes, but not exclusively using an internal open
source model. Now that git and github have become the de facto
version control system of choice, open source practices are
becoming more and more common in-house .

Netflix is a good example of an organisation that follows
this philosophy. Sharing useful and, above all, battle-tested
code as libraries encourages other developers to solve similar
problems in similar ways yet leaves the door open to picking a
different approach if required. Shared libraries tend to be
focused on common problems of data storage, inter-process
communication and as we discuss further below, infrastructure
automation.

For the microservice community, overheads are particularly
unattractive. That isn't to say that the community doesn't
value service contracts. Quite the opposite, since there tend
to be many more of them. It's just that they are looking at
different ways of managing those contracts. Patterns like
[Tolerant Reader](/bliki/TolerantReader.html) and [Consumer-Driven
Contracts](/articles/consumerDrivenContracts.html) are often applied to microservices. These aid
service contracts in evolving independently. Executing
consumer driven contracts as part of your build increases
confidence and provides fast feedback on whether your services
are functioning. Indeed we know of a team in Australia who
drive the build of new services with consumer driven
contracts. They use simple tools that allow them to define the
contract for a service. This becomes part of the automated
build before code for the new service is even written. The
service is then built out only to the point where it satisfies
the contract - an elegant approach to avoid the
'YAGNI'9 dilemma when building new
software. These techniques and the tooling growing up around
them, limit the need for central contract management by
decreasing the temporal coupling between services.

9: 
“YAGNI” or “You Aren't Going To Need It” is an [XP
principle](http://c2.com/cgi/wiki?YouArentGonnaNeedIt) and exhortation to not add features until you know
you need them.

Perhaps the apogee of decentralised governance is the build
it / run it ethos popularised by Amazon. Teams are responsible
for all aspects of the software they build including operating
the software 24/7. Devolution of this level of responsibility
is definitely not the norm but we do see more and more
companies pushing responsibility to the development
teams. Netflix is another organisation that has adopted this
ethos10. Being woken up at 3am
every night by your pager is certainly a powerful incentive to
focus on quality when writing your code. These ideas are about
as far away from the traditional centralized governance model
as it is possible to be.

10: 
Adrian Cockcroft specifically mentions “developer self-service”
and “Developers run what they wrote”(sic) in [this
excellent presentation](http://www.slideshare.net/adrianco/flowcon-added-to-for-cmg-keynote-talk-on-how-speed-wins-and-how-netflix-is-doing-continuous-delivery) delivered at Flowcon in November,
2013.

### Decentralized Data Management

Decentralization of data management presents in a number of
different ways. At the most abstract level, it means that the
conceptual model of the world will differ between systems.
This is a common issue when integrating across a large
enterprise, the sales view of a customer will differ from the
support view. Some things that are called customers in the
sales view may not appear at all in the support view. Those
that do may have different attributes and (worse) common
attributes with subtly different semantics.

This issue is common between applications, but can also
occur *within* applications, particular when that
application is divided into separate components. A useful way
of thinking about this is the Domain-Driven Design notion of
[Bounded Context](/bliki/BoundedContext.html). DDD divides a complex
domain up into multiple bounded contexts and maps out the
relationships between them. This process is useful
for both monolithic and microservice architectures, but there
is a natural correlation between service and context
boundaries that helps clarify, and as we describe in the
section on business capabilities, reinforce the
separations.

As well as decentralizing decisions about conceptual
models, microservices also decentralize data storage
decisions. While monolithic applications prefer a single logical
database for persistant data, enterprises often prefer a
single database across a range of applications - many of these
decisions driven through vendor's commercial models around
licensing. Microservices prefer letting each service manage
its own database, either different instances of the same
database technology, or entirely different database systems -
an approach called [Polyglot Persistence](/bliki/PolyglotPersistence.html). You
can use polyglot persistence in a monolith, but it appears
more frequently with microservices.

Decentralizing responsibility for data across microservices
has implications for managing updates. The common
approach to dealing with updates has been to use transactions
to guarantee consistency when updating multiple resources.
This approach is often used within monoliths.

Using transactions like this helps with consistency, but
imposes significant temporal coupling, which is problematic
across multiple services. Distributed transactions are
notoriously difficult to implement and as a consequence
microservice architectures [emphasize
transactionless coordination between services](http://www.eaipatterns.com/ramblings/18_starbucks.html), with
explicit recognition that consistency may only be eventual
consistency and problems are dealt with by compensating
operations.

Choosing to manage inconsistencies in this way is a new
challenge for many development teams, but it is one that often
matches business practice. Often businesses handle a degree of
inconsistency in order to respond quickly to demand, while
having some kind of reversal process to deal with
mistakes. The trade-off is worth it as long as the cost of
fixing mistakes is less than the cost of lost business under
greater consistency.

### Infrastructure Automation

Infrastructure automation techniques have evolved
enormously over the last few years - the evolution of the
cloud and AWS in particular has reduced the operational
complexity of building, deploying and operating
microservices.

Many of the products or systems being build with
microservices are being built by teams with extensive
experience of [Continuous Delivery](/bliki/ContinuousDelivery.html) and it's
precursor, [Continuous
Integration](/articles/continuousIntegration.html). Teams building software this way make
extensive use of infrastructure automation techniques. This is
illustrated in the build pipeline shown below.

Figure 5: basic
build pipeline

Since this isn't an article on Continuous Delivery we will
call attention to just a couple of key features here. We want
as much confidence as possible that our software is working,
so we run lots of **automated tests**. Promotion of working
software 'up' the pipeline means we **automate deployment**
to each new environment.

A monolithic application will be built, tested and pushed
through these environments quite happlily. It turns out that
once you have invested in automating the path to production
for a monolith, then deploying *more* applications
doesn't seem so scary any more. Remember, one of the aims of
CD is to make deployment boring, so whether its one or three
applications, as long as its still boring it doesn't
matter11.

11: 
We are being a little disengenuous here. Obviously deploying
more services, in more complex topologies is more difficult than
deploying a single monolith. Fortunately, patterns reduce this
complexity - investment in tooling is still a must though.

Another area where we see teams using extensive
infrastructure automation is when managing microservices in
production. In contrast to our assertion above that as long as
deployment is boring there isn't that much difference between
monoliths and microservices, the operational landscape for
each can be strikingly different.

Figure 6: Module
deployment often differs

### Design for failure

A consequence of using services as components, is that
applications need to be designed so that they can tolerate the
failure of services. Any service call could fail due to
unavailability of the supplier, the client has to respond to
this as gracefully as possible. This is a disadvantage
compared to a monolithic design as it introduces additional
complexity to handle it. The consequence is that microservice
teams constantly reflect on how service failures affect the
user experience. Netflix's [Simian Army](https://github.com/Netflix/SimianArmy)
induces failures of services and even datacenters during the
working day to test both the application's resilience and
monitoring.

This kind of automated testing in production would be
enough to give most operation groups the kind of shivers
usually preceding a week off work. This isn't to say that
monolithic architectural styles aren't capable of
sophisticated monitoring setups - it's just less common in our
experience.

Since services can fail at any time, it's important to be
able to detect the failures quickly and, if possible,
automatically restore service. Microservice applications put a
lot of emphasis on real-time monitoring of the application,
checking both architectural elements (how many requests per
second is the database getting) and business relevant metrics
(such as how many orders per minute are received). Semantic
monitoring can provide an early warning system of something
going wrong that triggers development teams to follow up and
investigate.

This is particularly important to a microservices
architecture because the microservice preference towards
choreography and [event collaboration](/eaaDev/EventCollaboration.html)
leads to emergent behavior. While many pundits praise the
value of serendipitous emergence, the truth is that emergent
behavior can sometimes be a bad thing. Monitoring is vital to
spot bad emergent behavior quickly so it can be fixed.

Monoliths can be built to be as transparent as a
microservice - in fact, they should be. The difference is that
you absolutely need to know when services running in different
processes are disconnected. With libraries within the same
process this kind of transparency is less likely to be
useful.

Microservice teams would expect to see sophisticated
monitoring and logging setups for each individual
service such as dashboards showing up/down status and a variety of
operational and business relevant metrics. Details on circuit
breaker status, current throughput and latency are other
examples we often encounter in the wild.

### Evolutionary Design

Microservice practitioners, usually have come from
an evolutionary design background and see service
decomposition as a further tool to enable application
developers to control changes in their application without
slowing down change. Change control doesn't necessarily mean
change reduction - with the right attitudes and tools you can
make frequent, fast, and well-controlled changes to
software.

Whenever you try to break a software system into
components, you're faced with the decision of how to divide up
the pieces - what are the principles on which we decide to
slice up our application? The key property of a component is
the notion of independent replacement and
upgradeability12 - which implies we look for
points where we can imagine rewriting a component without
affecting its collaborators. Indeed many microservice groups
take this further by explicitly expecting many services to be
scrapped rather than evolved in the longer term.

12: 
In fact, Daniel Terhorst-North refers to this style as *Replaceable
Component Architecture* rather than microservices. Since this
seems to talk to a subset of the characteristics we prefer the
latter.

The Guardian website is a good example of an application
that was designed and built as a monolith, but has been
evolving in a microservice direction. The monolith still is
the core of the website, but they prefer to add new features
by building microservices that use the monolith's API. This
approach is particularly handy for features that are
inherently temporary, such as specialized pages to handle a
sporting event. Such a part of the website can quickly be put
together using rapid development languages, and removed once
the event is over. We've seen similar approaches at a
financial institution where new services are added for a
market opportunity and discarded after a few months or even
weeks.

This emphasis on replaceability is a special case of a more
general principle of modular design, which is to drive
modularity through the pattern of change 13. You want to keep things that change
at the same time in the same module. Parts of a system that
change rarely should be in different services to those that
are currently undergoing lots of churn. If you find yourself
repeatedly changing two services together, that's a sign that
they should be merged.

13: 
Kent Beck highlights this as one his design principles in
[Implementation Patterns](https://www.amazon.com/gp/product/0321413091/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321413091&linkCode=as2&tag=martinfowlerc-20).

Putting components into services adds an opportunity for
more granular release planning. With a monolith any changes
require a full build and deployment of the entire
application. With microservices, however, you only need to
redeploy the service(s) you modified. This can simplify and
speed up the release process. The downside is that you have to
worry about changes to one service breaking its
consumers. The traditional integration approach is to try to deal
with this problem using versioning, but the preference in the
microservice world is to [only
use versioning as a last resort](/articles/enterpriseREST.html#versioning). We can avoid a lot of
versioning by designing services to be as tolerant as possible
to changes in their suppliers.

## Are Microservices the Future?

Our main aim in writing this article is to explain the major
ideas and principles of microservices. By taking the time to do
this we clearly think that the microservices architectural style
is an important idea - one worth serious consideration for
enterprise applications. We have recently built several systems
using the style and know of others who have used and favor this
approach.

Those we know about who are in some way pioneering the
architectural style include Amazon, Netflix, [The Guardian](http://www.theguardian.com), the [UK Government Digital Service](https://gds.blog.gov.uk/), <realestate.com.au>, Forward and [comparethemarket.com](http://www.comparethemarket.com/). The
conference circuit in 2013 was full of examples of companies
that are moving to something that would class as microservices -
including Travis CI. In addition there are plenty of
organizations that have long been doing what we would class as
microservices, but without ever using the name. (Often this is
labelled as SOA - although, as we've said, SOA comes in many
contradictory forms. 14)

14: 
And SOA is hardly the root of this history. I remember people saying
“we've been doing this for years” when the SOA term appeared at
the beginning of the century. One argument was that this style
sees its roots as the way COBOL programs communicated via data
files in the earliest days of enterprise computing. In another
direction, one could argue that microservices are the same thing
as the Erlang programming model, but applied to an enterprise
application context.

Despite these positive experiences, however, we aren't
arguing that we are certain that microservices are the future
direction for software architectures. While our experiences so
far are positive compared to monolithic applications, we're
conscious of the fact that not enough time has passed for us to
make a full judgement.

Often the true consequences of your architectural decisions
are only evident several years after you made them. We have seen
projects where a good team, with a strong desire for
modularity, has built a monolithic architecture that has
decayed over the years. Many people believe that such decay is
less likely with microservices, since the service boundaries are
explicit and hard to patch around. Yet until we see enough
systems with enough age, we can't truly assess how microservice
architectures mature.

There are certainly reasons why one might expect
microservices to mature poorly. In any effort at
componentization, success depends on how well the software fits
into components. It's hard to figure out exactly where the
component boundaries should lie. Evolutionary design recognizes
the difficulties of getting boundaries right and thus the
importance of it being easy to refactor them. But when your
components are services with remote communications, then
refactoring is much harder than with in-process libraries.
Moving code is difficult across service boundaries, any
interface changes need to be coordinated between participants,
layers of backwards compatibility need to be added, and testing
is made more complicated.

Another issue is If the components do not compose cleanly, then
all you are doing is shifting complexity from inside a component
to the connections between components. Not just does this just
move complexity around, it moves it to a place that's less
explicit and harder to control. It's easy to think things are
better when you are looking at the inside of a small, simple
component, while missing messy connections between services.

Finally, there is the factor of team skill. New techniques
tend to be adopted by more skillful teams. But a technique that
is more effective for a more skillful team isn't necessarily
going to work for less skillful teams. We've seen plenty of
cases of less skillful teams building messy monolithic
architectures, but it takes time to see what happens when this
kind of mess occurs with microservices. A poor team will always
create a poor system - it's very hard to tell if microservices
reduce the mess in this case or make it worse.

One reasonable argument we've heard is that you shouldn't
start with a microservices architecture. Instead
[begin with a monolith](/bliki/MonolithFirst.html),
keep it modular, and split it into microservices once the
monolith becomes a problem. (Although
[this advice isn't ideal](/articles/dont-start-monolith.html),
since a good in-process interface is usually not a good service interface.)

So we write this with cautious optimism. So far, we've seen
enough about the microservice style to feel that it can be
[a worthwhile road to tread](/microservices/).
We can't say for sure where we'll end
up, but one of the challenges of software development is that
you can only make decisions based on the imperfect information
that you currently have to hand.

---

## Footnotes

1: 
The term “microservice” was discussed at a workshop of software
architects near Venice in May, 2011 to describe what the
participants saw as a common architectural style that many of
them had been recently exploring. In May 2012, the same group decided on
“microservices” as the most appropriate name. James presented some of these
ideas as a case study in March 2012 at 33rd Degree in Krakow in
[Microservices
- Java, the Unix Way](http://2012.33degree.org/talk/show/67) as did Fred George [about
the same time](http://www.slideshare.net/fredgeorge/micro-service-architecure). Adrian Cockcroft at Netflix, describing this
approach as “fine grained SOA” was pioneering the style at web
scale as were many of the others mentioned in this article - Joe
Walnes, Daniel Terhorst-North, Evan Botcher and
Graham Tackley.

2: 
The term monolith has been in use by the Unix community for some
time. It appears in [The Art of Unix
Programming](https://www.amazon.com/gp/product/B003U2T5BA/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B003U2T5BA&linkCode=as2&tag=martinfowlerc-20) to describe systems that get too big.

3: 
Many object-oriented designers, including ourselves, use the
term service object in the [Domain-Driven
Design](https://www.amazon.com/gp/product/0321125215/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321125215&linkCode=as2&tag=martinfowlerc-20) sense for an object that carries out a significant
process that isn't tied to an entity. This is a different
concept to how we're using “service” in this article. Sadly the
term service has both meanings and we have to live with the
polyseme.

4: 
We consider [an application to be a social
construction](/bliki/ApplicationBoundary.html) that binds together a code base, group of
functionality, and body of funding.

5: 
We can't resist mentioning Jim Webber's statement that ESB
stands for [“Erroneous
Spaghetti Box”](http://www.infoq.com/presentations/soa-without-esb).

6: 
Netflix makes the link explicit - until recently referring to
their architectural style as fine-grained SOA.

7: 
At extremes of scale, organisations often move to binary
protocols - [protobufs](https://code.google.com/p/protobuf/) for
example. Systems using these still exhibit the characteristic of
smart endpoints, dumb pipes - and trade off *transparency*
for scale. Most web properties and certainly the vast majority
of enterprises don't need to make this tradeoff - transparency
can be a big win.

8: 
It's a little disengenuous of us to claim that monoliths are
single language - in order to build systems on todays web, you
probably need to know JavaScript and XHTML, CSS, your server
side language of choice, SQL and an ORM dialect. Hardly single
language, but you know what we mean.

9: 
“YAGNI” or “You Aren't Going To Need It” is an [XP
principle](http://c2.com/cgi/wiki?YouArentGonnaNeedIt) and exhortation to not add features until you know
you need them.

10: 
Adrian Cockcroft specifically mentions “developer self-service”
and “Developers run what they wrote”(sic) in [this
excellent presentation](http://www.slideshare.net/adrianco/flowcon-added-to-for-cmg-keynote-talk-on-how-speed-wins-and-how-netflix-is-doing-continuous-delivery) delivered at Flowcon in November,
2013.

11: 
We are being a little disengenuous here. Obviously deploying
more services, in more complex topologies is more difficult than
deploying a single monolith. Fortunately, patterns reduce this
complexity - investment in tooling is still a must though.

12: 
In fact, Daniel Terhorst-North refers to this style as *Replaceable
Component Architecture* rather than microservices. Since this
seems to talk to a subset of the characteristics we prefer the
latter.

13: 
Kent Beck highlights this as one his design principles in
[Implementation Patterns](https://www.amazon.com/gp/product/0321413091/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321413091&linkCode=as2&tag=martinfowlerc-20).

14: 
And SOA is hardly the root of this history. I remember people saying
“we've been doing this for years” when the SOA term appeared at
the beginning of the century. One argument was that this style
sees its roots as the way COBOL programs communicated via data
files in the earliest days of enterprise computing. In another
direction, one could argue that microservices are the same thing
as the Erlang programming model, but applied to an enterprise
application context.

## References

While this is not an exhaustive list, there are a number of sources
that practitioners have drawn inspiration from or which espouse a
similar philosophy to that described in this article.

Blogs and online articles

* [Clemens Vasters’ blog
  on cloud at microsoft](http://blogs.msdn.com/b/clemensv/)
* [David
  Morgantini’s introduction to the topic on his blog](http://davidmorgantini.blogspot.com/2013/08/micro-services-introduction.htm)
* [12 factor apps from Heroku](http://12factor.net/)
* [UK Government
  Digital Service design principles](https://www.gov.uk/design-principles)
* [Jimmy Nilsson’s blog](http://jimmynilsson.com/blog/)[and article
  on infoq about Cloud Chunk Computing](http://www.infoq.com/articles/CCC-Jimmy-Nilsson)
* [Alistair
  Cockburn on Hexagonal architectures](http://alistair.cockburn.us/Hexagonal+architecture)

Books

* [Release it](https://www.amazon.com/gp/product/0978739213/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0978739213&linkCode=as2&tag=martinfowlerc-20)
* [Rest in practice](https://www.amazon.com/gp/product/0596805829/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0596805829&linkCode=as2&tag=martinfowlerc-20)
* [Web
  API Design (free ebook)](https://pages.apigee.com/web-api-design-ebook.html). Brian Mulloy, Apigee.
* [Enterprise Integration
  Patterns](https://www.amazon.com/gp/product/0321200683/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321200683&linkCode=as2&tag=martinfowlerc-20)
* [Art of unix programming](https://www.amazon.com/gp/product/0131429019/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0131429019&linkCode=as2&tag=martinfowlerc-20)
* [Growing Object Oriented Software, Guided
  by Tests](https://www.amazon.com/gp/product/0321503627/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321503627&linkCode=as2&tag=martinfowlerc-20)
* [The Modern Firm: Organizational Design for
  Performance and Growth](https://www.amazon.com/gp/product/0198293755/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0198293755&linkCode=as2&tag=martinfowlerc-20)
* [Continuous Delivery: Reliable Software
  Releases through Build, Test, and Deployment Automation](https://www.amazon.com/gp/product/0321601912/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321601912&linkCode=as2&tag=martinfowlerc-20)
* [Domain-Driven Design: Tackling Complexity
  in the Heart of Software](https://www.amazon.com/gp/product/0321125215/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321125215&linkCode=as2&tag=martinfowlerc-20)

Presentations

* [Architecture
  without Architects](https://www.youtube.com/watch?v=qVyt3qQ_7TA). Erik Doernenburg.
* [Does
  my bus look big in this?](http://www.infoq.com/presentations/soa-without-esb). Jim Webber and Martin Fowler, QCon
  2008
* [Guerilla
  SOA](http://www.infoq.com/presentations/webber-guerilla-soa). Jim Webber, 2006
* [Patterns of Effective
  Delivery](http://vimeo.com/43659070). Daniel Terhorst-North, 2011.
* [Adrian Cockcroft's
  slideshare channel](http://www.slideshare.net/adrianco).
* [Hydras and Hypermedia](http://vimeo.com/28608667). Ian
  Robinson, JavaZone 2010
* Justice will take a million intricate
  moves. Leonard Richardson, Qcon 2008.
* [Java, the UNIX way](http://vimeo.com/74452550). James
  Lewis, JavaZone 2012
* [Micro
  services architecture](http://yow.eventer.com/yow-2012-1012/micro-services-architecture-by-fred-george-1286). Fred George, YOW! 2012
* [Democratising attention data
  at guardian.co.uk](http://gotocon.com/video#18). Graham Tackley, GOTO Aarhus 2013
* [Functional Reactive
  Programming with RxJava](http://gotocon.com/video#6). Ben Christensen, GOTO Aarhus 2013
  (registration required).
* [Breaking
  the Monolith](http://www.infoq.com/presentations/Breaking-the-Monolith). Stefan Tilkov, May 2012.

Papers

* L. Lamport, “The Implementation of Reliable Distributed
  Multiprocess Systems”, 1978 http://
  research.microsoft.com/en-us/um/people/lamport/pubs/implementation.pdf
* L. Lamport, R. Shostak, M. Pease, “The Byzantine Generals
  Problem”, 1982 (available at) http://
  www.cs.cornell.edu/courses/cs614/2004sp/papers/lsp82.pdf
* R.T. Fielding, “Architectural Styles and the Design of
  Network-based Software Architectures”, 2000
  http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
* E. A. Brewer, “Towards Robust Distributed Systems”, 2000
  http://www.cs.berkeley.edu/ ~brewer/cs262b-2004/PODC-keynote.pdf
* E. Brewer, “CAP Twelve Years Later: How the 'Rules' Have Changed”,
  2012, http://
  www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed

## Further Reading

The above list captures the references we used when we originally
wrote this article in early 2014. For an up to date list of sources
for more information, take a look at the [Microservice Resource Guide](/microservices).

Significant Revisions

*25 March 2014:* last installment on are microservices the future?

*24 March 2014:* added section on evolutionary design

*19 March 2014:* added sections on infrastructure
automation and design for failure

*18 March 2014:* added section on decentralized data

*17 March 2014:* added section on decentralized governance

*14 March 2014:* added section on smart endpoint and dumb pipes

*13 March 2014:* added section on products not projects

*12 March 2014:* added section on organizing around
business capabilities

*10 March 2014:* published first installment

---

## 7. Continuous Integration

*Continuous Integration is a software development practice where each member
of a team merges their changes into a codebase together with their
colleagues changes at least daily. Each of these integrations is verified by
an automated build (including test) to detect integration errors as quickly
as possible. Teams find that this approach reduces the risk of
delivery delays, reduces the effort of integration, and enables practices
that foster a healthy codebase for rapid enhancement with new features.*

18 January 2024

---

[Martin Fowler](/)

[agile](/tags/agile.html)

[continuous delivery](/tags/continuous%20delivery.html)

[extreme programming](/tags/extreme%20programming.html)

## Contents

* [Building a Feature with Continuous Integration](#BuildingAFeatureWithContinuousIntegration)
* [Practices of Continuous Integration](#PracticesOfContinuousIntegration)
  + [Put everything in a version controlled mainline](#PutEverythingInAVersionControlledMainline)
  + [Automate the Build](#AutomateTheBuild)
  + [Make the Build Self-Testing](#MakeTheBuildSelf-testing)
  + [Everyone Pushes Commits To the Mainline Every Day](#EveryonePushesCommitsToTheMainlineEveryDay)
  + [Every Push to Mainline Should Trigger a Build](#EveryPushToMainlineShouldTriggerABuild)
  + [Fix Broken Builds Immediately](#FixBrokenBuildsImmediately)
  + [Keep the Build Fast](#build-fast)
  + [Hide Work-in-Progress](#HideWork-in-progress)
  + [Test in a Clone of the Production Environment](#TestInACloneOfTheProductionEnvironment)
  + [Everyone can see what's happening](#EveryoneCanSeeWhatsHappening)
  + [Automate Deployment](#AutomateDeployment)
* [Styles of Integration](#StylesOfIntegration)
* [Benefits of Continuous Integration](#BenefitsOfContinuousIntegration)
  + [Reduced risk of delivery delays](#ReducedRiskOfDeliveryDelays)
  + [Less time wasted in integration](#LessTimeWastedInIntegration)
  + [Less Bugs](#LessBugs)
  + [Enables Refactoring for sustained productivity](#EnablesRefactoringForSustainedProductivity)
  + [Release to Production is a business decision](#ReleaseToProductionIsABusinessDecision)
* [When we should not use Continuous Integration](#WhenWeShouldNotUseContinuousIntegration)
* [Introducing Continuous Integration](#introducing)
* [Common Questions](#CommonQuestions)
  + [Where did Continuous Integration come from?](#WhereDidContinuousIntegrationComeFrom)
  + [What is the difference between Continuous Integration and Trunk-Based Development?](#trunk-based)
  + [Can we run a CI Service on our feature branches?](#CanWeRunACiServiceOnOurFeatureBranches)
  + [Can a team do both Continuous Integration and Feature Branching at
    the same time?](#both-ci-plus-fb)
  + [What is the difference between Continuous Integration and Continuous
    Delivery?](#WhatIsTheDifferenceBetweenContinuousIntegrationAndContinuousDelivery)
  + [How does Continuous Deployment fit in with all this?](#cont-deploy)
  + [How do we do pull requests and code reviews?](#HowDoWeDoPullRequestsAndCodeReviews)
  + [How do we handle databases?](#HowDoWeHandleDatabases)
* [Final Thoughts](#FinalThoughts)

### Sidebars

* [Semi-Integration (it isn't Continuous Integration)](#semi-integration)

---

I vividly remember one of my first sightings of a large software project.
I was taking a summer internship at a large English electronics company. My
manager, part of the QA group, gave me a tour of a site and we entered a
huge, depressing, windowless warehouse full of people working in cubicles.
I was told that these
programmers had been writing code for this software for a couple of years,
and while they were done programming, their separate units were now being
integrated together, and they had been integrating for several months. My
guide told me that nobody really knew how long it would take to finish
integrating. From this I learned a common story of software projects:
integrating the work of multiple developers is a long and unpredictable
process.

I haven't heard of a team trapped in such a long integration like this
for many years, but that doesn't mean that integration is a painless
process. A developer may have been working for several days on a new
feature, regularly pulling changes from a common main branch into her
feature branch. Just before she's ready to push her changes, a big change
lands on main, one that alters some code that she's interacting with. She
has to change from finishing off her feature to figuring out how to
integrate her work with this change, which while better for her colleague,
doesn't work so well for her. Hopefully the complexities of the change will
be in merging the source code, not an insidious fault that only shows when
she runs the application, forcing her to debug unfamiliar code.

At least in that scenario, she gets to find out before she submits her
pull request. Pull requests can be fraught enough while waiting for someone
to review a change. The review can take time, forcing her to context-switch
from her next feature. A difficult integration during that period can be very
disconcerting, dragging out the review process even longer. And that may not
even the be the end of story, since integration tests are often only run
after the pull request is merged.

In time, this team may learn that making significant changes to core code
causes this kind of problem, and thus stops doing it. But that, by
preventing regular refactoring, ends up allowing
cruft to grow throughout the codebase. Folks who encounter a crufty
code base wonder how it got into such a state, and often the answer lies in
an integration process with so much friction that it discourages people from
removing that cruft.

But this needn't be the way. Most projects done by my colleagues
at Thoughtworks, and by many others around the world, treat
integration as a non-event. Any individual developer's work is
only a few hours away from a shared project state and can be
integrated back into that state in minutes. Any integration errors
are found rapidly and can be fixed rapidly.

This contrast isn't the result of an expensive and complex
tool. The essence of it lies in the simple practice of everyone on
the team integrating frequently, at least daily, against a
controlled source code repository. This practice is called “Continuous
Integration” (or [in some circles](#trunk-based) it’s called “Trunk-Based Development”).

In this article, I explain what Continuous Integration is and how to do
it well. I've written it for two reasons. Firstly there are always new people
coming into the profession and I want to show them how they can avoid that
depressing warehouse. But secondly this topic needs clarity because
Continuous Integration is a much misunderstood concept. There are many
people who say that they are doing Continuous Integration, but once they describe
their workflow, it becomes clear that they are missing important pieces. A
clear understanding of Continuous Integration helps us communicate, so we know
what to expect when we describe our way of working. It also helps folks
realize that there are further things they can do to improve their experience.

I originally wrote this article in 2001, with an update in 2006. Since
then much has changed in usual expectations of software development teams.
The many-month integration that I saw in the 1980s is a distant memory,
technologies such as version control and build scripts have become
commonplace. I rewrote this article again in 2023 to better address the
development teams of that time, with twenty years of experience to
confirm the value of Continuous Integration.

## Building a Feature with Continuous Integration

The easiest way for me to explain what Continuous Integration is and how it works is to
show a quick example of how it works with the development of a small
feature. I'm currently working with a major manufacturer of magic potions, we
are extending their product quality system to calculate how long the
potion's effect will last. We already have a dozen potions supported in
the system, and we need to extend the logic for flying potions. (We've
learned that having them wear off too early severely impacts customer
retention.) Flying potions introduce a few new factors to take care of,
one of which is the moon phase during secondary mixing.

I begin by taking a copy of the latest product sources
onto my local development environment. I do this by checking out the
current mainline from the central repository with
`git pull`.

Once the source is in my environment, I execute a command to build
the product. This command checks that my environment is set up correctly, does
any compilation of the sources into an executable product, starts the
product, and runs a comprehensive suite of tests against it. This should
take only a few minutes, while I start poking around the code to
decide how to begin adding the new feature. This build hardly ever fails,
but I do it just in case, because if it does fail, I want to know before I
start making changes. If I make changes on top of a failing build, I'll
get confused thinking it was my changes that caused the failure.

Now I take my working copy and do whatever I need to do to deal with
the moon phases. This will consist of both altering the product code, and
also adding or changing some of the automated tests. During that time I
run the automated build and tests frequently. After an hour or so I have
the moon logic incorporated and tests updated.

I'm now ready to integrate my changes back into the central repository. My
first step for this is to pull again, because it's possible, indeed
likely, that my colleagues will have pushed changes into the mainline
while I've been working. Indeed there are a couple of such changes, which
I pull into my working copy. I combine my changes on top of them and run
the build again. Usually this feels superfluous, but this time a test
fails. The test gives me some clue about what's gone wrong, but I find it
more useful to look at the commits that I pulled to see what changed. It
seems that someone has made an adjustment to a function, moving some of its
logic out into its callers. They fixed all the callers in the mainline
code, but I added a new call in my changes that, of course, they couldn't
see yet. I make the same adjustment and rerun the build, which passes this
time.

Since I was a few minutes sorting that out, I pull again, and again
there's a new commit. However the build works fine with this one, so I'm
able to `git push` my change up to the central repository.

However my push doesn't mean I'm done. Once I've pushed to the mainline
a Continuous Integration Service notices my commit, checks out the changed
code onto a CI agent, and builds it there. Since the build was
fine in my environment I don't expect it to fail on the CI Service,
but there is a reason that “works on my machine” is a well-known
phrase in programmer circles. It's rare that something gets missed that
causes the CI Services build to fail, but rare is not the same
as never.

The integration machine's build doesn't take long, but it's long enough
that an eager developer would be starting to think about the next step in
calculating flight time. But I'm an old guy, so enjoy a few minutes to
stretch my legs and read an email. I soon get a notification from the CI
service that all is well, so I start the process again for the next part of
the change.

## Practices of Continuous Integration

The story above is an illustration of Continuous Integration that
hopefully gives you a feel of what it's like for an ordinary programmer to
work with. But, as with anything, there's quite a few things to sort out
when doing this in daily work. So now we'll go through the key practices
that we need to do.

### Automate the Build

Turning the source code into a running system can often be a
complicated process involving compilation, moving files around, loading
schemas into databases, and so on. However like most tasks in this
part of software development it can be automated - and as a result
should be automated. Asking people to type in strange commands or
clicking through dialog boxes is a waste of time and a breeding ground
for mistakes.

> Computers are designed to perform simple, repetitive tasks. As soon
> as you have humans doing repetitive tasks on behalf of computers, all
> the computers get together late at night and laugh at you.
>
> -- [Neal Ford](https://nealford.com/memeagora/2015/09/02/simple-repetitive-tasks.html)

Most modern programming environments include tooling for automating
builds, and such tools have been around for a long time. I first encountered
them with [make](https://en.wikipedia.org/wiki/Make_(software)), one of the earliest Unix
tools.

Any instructions for the build need to be stored in the repository,
in practice this means that we must use text representations. That way
we can easily inspect them to see how they work, and crucially, see
diffs when they change. Thus teams using Continuous Integration avoid
tools that require clicking around in UIs to perform a build or to
configure an environment.

It's possible to use a regular programming language to automate
builds, indeed simple builds are often captured as shell scripts. But as
builds get more complicated it's better to use a tool that's designed
with build automation in mind. Partly this is because such tools will
have built-in functions for common build tasks. But the main reason is
that build tools work best with a particular way to organize their logic
- an alternative computational model that I refer to as a [Dependency Network](/dslCatalog/dependencyNetwork.html). A dependency network organizes
its logic into tasks which are structured as a graph of dependencies.

A trivially simple dependency network might say that the “test” task is
dependent upon the “compile” task. If I invoke the test task, it will
look to see if the compile task needs to be run and if so invoke it
first. Should the compile task itself have dependencies, the network will look to see if
it needs to invoke them first, and so on backwards along the dependency
chain. A dependency network like this is useful for build scripts
because often tasks take a long time, which is wasted if they aren't
needed. If nobody has changed any source files since I last ran the
tests, then I can save doing a potentially long compilation.

To tell if a task needs to be run, the most common and
straightforward way is to look at the modification times of files. If any
of the input files to the compilation have been modified later than the
output, then we know the compilation needs to be executed if that task
is invoked.

A common mistake is not to include everything in the automated build.
The build should include getting the database schema out of the
repository and firing it up in the execution environment. I'll elaborate
my earlier rule of thumb: anyone should be able to bring in a clean
machine, check the sources out of the repository, issue a single
command, and have a running system on their own environment.

While a simple program may only need a line or two of script file to
build, complex systems often have a large graph of dependencies, finely
tuned to minimize the amount of time required to build things. This
website, for example, has over a thousand web pages. My build system
knows that should I alter the source for this page, I only have to build
this one page. But should I alter a core file in the publication
tool chain, then it needs to rebuild them all. Either way, I invoke the
same command in my editor, and the build system figures out how much to do.

Depending on what we need, we may need different kinds of things to
be built. We can build a system with or without test code, or with
different sets of tests. Some components can be built stand-alone. A
build script should allow us to build alternative targets for different
cases.

### Make the Build Self-Testing

Traditionally a build meant compiling, linking, and all the
additional stuff required to get a program to execute. A program may
run, but that doesn't mean it does the right thing. Modern statically
typed languages can catch many bugs, but far more slip through that net.
This is a critical issue if we want to integrate as frequently as
Continuous Integration demands. If bugs make their way into the product,
then we are faced with the daunting task of performing bug fixes on a
rapidly-changing code base. Manual testing is too slow to cope with the
frequency of change.

Faced with this, we need to ensure that bugs don't get into the
product in the first place. The main technique to do this is a
comprehensive test suite, one that is run before each integration to
flush out as many bugs as possible. Testing isn't perfect, of course,
but it can catch a lot of bugs - enough to be useful. Early computers I
used did a visible memory self-test when they were booting up, which led
me referring to this as [Self Testing Code](/bliki/SelfTestingCode.html).

Writing self-testing code affects a programmer's workflow. Any
programming task combines both modifying the functionality of the
program, and also augmenting the test suite to verify this changed
behavior. A programmer's job isn't done merely when the new
feature is working, but also when they have automated tests to prove it.

Over the two decades since the first version of this article, I've
seen programming environments increasingly embrace the need to provide
the tools for programmers to build such test suites. The biggest push
for this was JUnit, originally written by Kent Beck and Erich Gamma,
which had a marked impact on the Java community in the late 1990s. This
inspired similar testing frameworks for other languages, often referred
to as [Xunit](/bliki/Xunit.html) frameworks. These stressed a
light-weight, programmer-friendly mechanics that allowed a programmer to
easily build tests in concert with the product code. Often these tools
have some kind of graphical progress bar that is green if the tests pass,
but turns red should any fail - leading to phrases like “green build”,
or “red-bar”.

A sound test suite would never allow a mischievous imp to do
any damage without a test turning red.

The test of such a test suite is that we should be confident that if the
tests are green, then no significant bugs are in the product. I like to
imagine a mischievous imp that is able to make simple modifications to
the product code, such as commenting out lines, or reversing
conditionals, but is not able to change the tests. A sound test suite
would never allow the imp to do any damage without a test turning
red. And any test failing is enough to fail the build, 99.9% green is
still red.

Self-testing code is so important to Continuous Integration that it is a
necessary prerequisite. Often the biggest barrier to implementing
Continuous Integration is insufficient skill at testing.

That self-testing code and Continuous Integration are so tied
together is no surprise. Continuous Integration was originally developed
as part of [Extreme Programming](/bliki/ExtremeProgramming.html) and testing has always
been a core practice of Extreme Programming. This testing is often done
in the form of [Test Driven Development](/bliki/TestDrivenDevelopment.html) (TDD), a practice that
instructs us to never write new code unless it fixes a test that we've
written just before. TDD isn't essential for Continuous Integration, as
tests can be written after production code as long as they are done
before integration. But I do find that, most of the time, TDD is the best
way to write self-testing code.

The tests act as an automated check of the health of the code
base, and while tests are the key element of such an automated
verification of the code, many programming environments provide additional
verification tools. Linters can detect poor programming practices,
and ensure code follows a team's preferred formatting
style, vulnerability scanners can find security weaknesses. Teams should
evaluate these tools to include them in the verification process.

Of course we can't count on tests to find everything. As it's often
been said: tests don't prove the absence of bugs. However perfection
isn't the only point at which we get payback for a self-testing build.
Imperfect tests, run frequently, are much better than perfect tests that
are never written at all.

### Everyone Pushes Commits To the Mainline Every Day

> No code sits unintegrated for more than a couple of hours.
>
> -- [Kent Beck](https://www.amazon.com/gp/product/0201616416/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0201616416&linkCode=as2&tag=martinfowlerc-20)

Integration is primarily about communication. Integration
allows developers to tell other developers about the changes
they have made. Frequent communication allows people to know
quickly as changes develop.

The one prerequisite for a developer committing to the
mainline is that they can correctly build their code. This, of
course, includes passing the build tests. As with any commit
cycle the developer first updates their working copy to match
the mainline, resolves any conflicts with the mainline, then
builds on their local machine. If the build passes, then they
are free to push to the mainline.

If everyone pushes to the mainline frequently, developers quickly find out if
there's a conflict between two developers. The key to fixing problems
quickly is finding them quickly. With developers committing every few
hours a conflict can be detected within a few hours of it occurring, at
that point not much has happened and it's easy to resolve. Conflicts
that stay undetected for weeks can be very hard to resolve.

Conflicts in the codebase come in different forms. The easiest to
find and resolve are textual conflicts, often called “merge conflicts”,
when two developers edit the
same fragment of code in different ways. Version-control tools detect
these easily once the second developer pulls the updated mainline into
their working copy. The harder problem are [Semantic Conflicts](/bliki/SemanticConflict.html). If my colleague changes the
name of a function and I call that function in my newly added code,
the version-control system can't help us. In a statically typed language
we get a compilation failure, which is pretty easy to detect, but in a
dynamic language we get no such help. And even statically-typed
compilation doesn't help us when a colleague makes a change to the body
of a function that I call, making a subtle change to what it does. This
is why it's so important to have self-testing code.

A test failure alerts that there's a conflict between changes, but we
still have to figure out what the conflict is and how to resolve it.
Since there's only a few hours of changes between commits, there's only
so many places where the problem could be hiding. Furthermore since not
much has changed we can use [Diff Debugging](/bliki/DiffDebugging.html) to help us find the
bug.

My general rule of thumb is that every developer should commit to the
mainline every day. In practice, those experienced with Continuous
Integration integrate more frequently than that. The more frequently we
integrate, the less places we have to look for conflict errors, and the
more rapidly we fix conflicts.

Frequent commits encourage developers to break down their
work into small chunks of a few hours each. This helps
track progress and provides a sense of progress. Often people
initially feel they can't do something meaningful in just a few
hours, but we've found that mentoring and practice helps us learn.

### Every Push to Mainline Should Trigger a Build

If everyone on the team integrates at least daily, this ought to mean
that the mainline stays in a healthy state. In practice, however, things
still do go wrong. This may be due to lapses in discipline, neglecting
to update and build before a push, there may also be environmental
differences between developer workspaces.

We thus need to ensure that every commit is verified in a reference
environment. The usual way to do this is with a **Continuous Integration
Service (CI Service)** that monitors the mainline. (Examples of CI
Services are tools like Jenkins, GitHub Actions, Circle CI etc.) Every time
the mainline receives a commit, the CI service checks out the head of the
mainline into an integration environment and performs a full build. Only
once this integration build is green can the developer consider the
integration to be complete. By ensuring we have a build with every push,
should we get a failure, we know that the fault lies in that latest
push, narrowing down where have to look to fix it.

I want to stress here that when we use a CI Service, we only use it on
the mainline, which is the main branch on the reference instance of the
version control system. It's common to use a CI service to monitor and build
from multiple branches, but the whole point of integration is to have
all commits coexisting on a *single* branch. While it may be useful to use
CI service to do an automated build for different branches, that's not
the same as Continuous Integration, and teams using Continuous
Integration will only need the CI service to monitor a single branch of
the product.

While almost all teams use CI Services these days, it is
[perfectly
possible](https://www.jamesshore.com/v2/blog/2006/continuous-integration-on-a-dollar-a-day) to do Continuous Integration without one. Team members can
manually check out the head on the mainline onto an integration machine
and perform a build to verify the integration. But there's little point
in a manual process when automation is so freely available.

(This is an appropriate point to mention that my colleagues at
Thoughtworks, have contributed a lot of open-source tooling for
Continuous Integration, in particular Cruise Control - the first CI
Service.)

### Fix Broken Builds Immediately

Continuous Integration can only work if the mainline is kept in a
healthy state. Should the integration build fail, then it needs to be
fixed right away. As Kent Beck puts it: “nobody has a
higher priority task than fixing the build”. This doesn't mean
that everyone on the team has to stop what they are doing in
order to fix the build, usually it only needs a couple of
people to get things working again. It does mean a conscious
prioritization of a build fix as an urgent, high priority
task

Usually the best way to fix the build is to revert the
faulty commit from the mainline, allowing the rest of the team to
continue working.

Usually the best way to fix the build is to revert the latest commit
from the mainline, taking the system back to the last-known good build.
If the cause of the problem is immediately obvious then it can be fixed
directly with a new commit, but otherwise reverting the mainline allows
some folks to figure out the problem in a separate development
environment, allowing the rest of the team to continue to work with the
mainline.

Some teams prefer to remove all risk of breaking the mainline by
using a [Pending Head](/bliki/PendingHead.html) (also called Pre-tested, Delayed,
or Gated Commit.) To do this the CI service needs to set things up so that
commits pushed to the mainline for integration do not immediately go
onto the mainline. Instead they are placed on another branch until the
build completes and only migrated to the mainline after a green build.
While this technique avoids any danger to mainline breaking, an
effective team should rarely see a red mainline, and on the few times it
happens its very visibility encourages folks to learn how to avoid
it.

### Keep the Build Fast

The whole point of Continuous Integration is to provide rapid
feedback. Nothing sucks the blood of Continuous Integration
more than a build that takes a long time. Here I must admit a certain
crotchety old guy amusement at what's considered to be a long build.
Most of my colleagues consider a build that takes an hour to be totally
unreasonable. I remember teams dreaming that they could get it so fast -
and occasionally we still run into cases where it's very hard to get
builds to that speed.

For most projects, however, the XP guideline of a ten
minute build is perfectly within reason. Most of our modern
projects achieve this. It's worth putting in concentrated
effort to make it happen, because every minute chiseled off
the build time is a minute saved for each developer every time
they commit. Since Continuous Integration demands frequent commits, this adds up
to a lot of the time.

If we're staring at a one hour build time, then getting to
a faster build may seem like a daunting prospect. It can even
be daunting to work on a new project and think about how to
keep things fast. For enterprise applications, at least, we've
found the usual bottleneck is testing - particularly tests
that involve external services such as a database.

Probably the most crucial step is to start working
on setting up a [Deployment Pipeline](/bliki/DeploymentPipeline.html). The idea behind a
**deployment pipeline** (also known as **build
pipeline** or **staged build**) is that there are in fact
multiple builds done in sequence. The commit to the mainline triggers
the first build - what I call the commit build. The **commit
build** is the build that's needed when someone pushes commits to the
mainline. The commit build is the one that has to be done quickly, as a
result it will take a number of shortcuts that will reduce the ability
to detect bugs. The trick is to balance the needs of bug finding and
speed so that a good commit build is stable enough for other people to
work on.

Once the commit build is good then other people can work on
the code with confidence. However there are further, slower,
tests that we can start to do. Additional machines can run
further testing routines on the build that take longer to
do.

A simple example of this is a two stage deployment pipeline. The
first stage would do the compilation and run tests that are more
localized unit tests with slow services replaced by [Test Doubles](/bliki/TestDouble.html), such as a fake in-memory database or
a stub for an external service. Such
tests can run very fast, keeping within the ten minute guideline.
However any bugs that involve larger scale interactions, particularly
those involving the real database, won't be found. The second stage
build runs a different suite of tests that do hit a real database and
involve more end-to-end behavior. This suite might take a couple of
hours to run.

In this scenario people use the first stage as the commit build and
use this as their main CI cycle.
If the secondary build fails, then this may not have
the same 'stop everything' quality, but the team does aim to fix such
bugs as rapidly as possible, while keeping the commit build running.
Since the secondary build may be much slower, it may not run after every
commit. In that case it runs as often as it can, picking the last good
build from the commit stage.

If the secondary build detects a bug, that's a sign that the commit
build could do with another test. As much as possible we want to ensure
that any later-stage failure leads to new tests in the commit build that
would have caught the bug, so the bug stays fixed in the commit build.
This way the commit tests are strengthened whenever something gets past
them. There are cases where there's no way to build a fast-running test
that exposes the bug, so we may decide to only test for that condition
in the secondary build. Most of the time, fortunately, we can add suitable
tests to the commit build.

Another way to speed things up is to use parallelism and multiple
machines. Cloud environments, in particular, allow teams to easily spin
up a small fleet of servers for builds. Providing the tests can run
reasonably independently, which well-written tests can, then using such
a fleet can get very rapid build times. Such parallel cloud builds may
also be worthwhile to a developer's pre-integration build too.

While we're considering the broader build process, it's worth
mentioning another category of automation, interaction with
dependencies. Most software uses a large range of dependent software
produced by different organizations. Changes in these dependencies can
cause breakages in the product. A team should thus automatically check
for new versions of dependencies and integrate them into the build,
essentially as if they were another team member. This should be done
frequently, usually at least daily, depending on the rate of change of
the dependencies. A similar approach should be used with running
[Contract Tests](/bliki/ContractTest.html). If these dependency
interactions go red, they don't have the same “stop the line” effect as
regular build failures, but do require prompt action by the team to
investigate and fix.

### Hide Work-in-Progress

Continuous Integration means integrating as soon as there is a little
forward progress and the build is healthy. Frequently this suggests
integrating before a user-visible feature is fully formed and ready for
release. We thus need to consider how to deal with latent code: code
that's part of an unfinished feature that's present in a live
release.

Some people worry about latent code, because it's putting
non-production quality code into the released executable. Teams doing
Continuous Integration ensure that all code sent to the mainline is
production quality, together with the tests that
verify the code. Latent code may never be executed in
production, but that doesn't stop it from being exercised in tests.

We can prevent the code being executed in production by using a
[Keystone Interface](/bliki/KeystoneInterface.html) - ensuring the interface that
provides a path to the new feature is the last thing we add to the code
base. Tests can still check the code at all levels other than that final
interface. In a well-designed system, such interface elements should be
minimal and thus simple to add with a short programming episode.

Using [Dark Launching](/bliki/DarkLaunching.html) we can test some changes in
production before we make them visible to the user. This technique is
useful for assessing the impact on performance,

Keystones cover most cases of latent code, but for occasions where
that's not possible we use [Feature Flags](/bliki/FeatureFlag.html).
Feature flags are checked whenever we are about to execute latent code,
they are set as part of the environment, perhaps in an
environment-specific configuration file. That way the latent code can be
active for testing, but disabled in production. As well as enabling
Continuous Integration, feature flags also make it easier for runtime
switching for A/B testing and [Canary Releases](/bliki/CanaryRelease.html). We then make sure we remove this logic promptly once a
feature is fully released, so that the flags don't clutter the code
base.

[Branch By Abstraction](/bliki/BranchByAbstraction.html) is another technique for
managing latent code, which is particularly useful for large
infrastructural changes within a code base. Essentially this creates an
internal interface to the modules that are being changed. The interface
can then route between old and new logic, gradually replacing execution
paths over time. We've seen this done to switch such pervasive elements
as changing the persistence platform.

When introducing a new feature, we should always ensure that we can
rollback in case of problems. [Parallel Change](/bliki/ParallelChange.html) (aka
expand-contract) breaks a change into reversible steps. For example, if
we rename a database field, we first create a new field with the new
name, then write to both old and new fields, then copy data from the
exisitng old fields, then read from the new field, and only then remove
the old field. We can reverse any of these steps, which would not be
possible if we made such a change all at once. Teams using Continuous
Integration often look to break up changes in this way, keeping changes
small and easy to undo.

### Test in a Clone of the Production Environment

The point of testing is to flush out, under controlled
conditions, any problem that the system will have in
production. A significant part of this is the environment
within which the production system will run. If we test in a
different environment, every difference results in a risk that
what happens under test won't happen in production.

Consequently, we want to set up our test environment to be
as exact a mimic of our production environment as
possible. Use the same database software, with the same
versions, use the same version of the operating system. Put all
the appropriate libraries that are in the production
environment into the test environment, even if the system
doesn't actually use them. Use the same IP addresses and
ports, run it on the same hardware.

Virtual environments make it much easier than it was in the past to
do this. We run production software in containers, and reliably build
exactly the same containers for testing, even in a developer's
workspace. It's worth the effort and cost to do this, the price is
usually small compared to hunting down a single bug that crawled out of
the hole created by environment mismatches.

Some software is designed to run in multiple environments, such as
different operating systems and platform versions. The deployment
pipeline should arrange for testing in all of these environments in
parallel.

A point to take care of is when the production environment isn't as
good as the development environment. Will the production software be
running on machines connected with dodgy wifi, like smartphones? Then ensure a test
environment mimics poor network connections.

### Everyone can see what's happening

Continuous Integration is all about communication, so we
want to ensure that everyone can easily see the state of the
system and the changes that have been made to it.

One of the most important things to communicate is the
state of the mainline build. CI Services have dashboards that allow
everyone to see the state of any builds they are running. Often they
link with other tools to broadcast build information to internal social
media tools such as Slack. IDEs often have hooks into these mechanisms,
so developers can be alerted while still inside the tool they are using
for much of their work. Many teams only send out notifications for build
failures, but I think it's worth sending out messages on success too.
That way people get used to the regular signals and get a sense for the
length of the build. Not to mention the fact that it's nice to get a
“well done” every day, even if it's only from a CI server.

Teams that share a physical space often have some kind of always-on
physical display for the build. Usually this takes the form of a large
screen showing a simplified dashboard. This is particularly valuable to
alert everyone to a broken build, often using the red/green colors on
the mainline commit build.

One of the older physical displays I rather liked were the use of red
and green lava lamps. One of the features of a lava lamp is that after
they are turned on for a while they start to bubble. The idea was that
if the red lamp came on, the team should fix the build before it starts
to bubble. Physical displays for build status often got playful, adding
some quirky personality to a team's workspace. I have fond memories of a
dancing rabbit.

As well as the current state of the build, these displays can show
useful information about recent history, which can be an indicator of
project health. Back at the turn of the century I worked with a team who
had a history of being unable to create stable builds. We put a calendar
on the wall that showed a full year with a small square for each day.
Every day the QA group would put a green sticker on the day if they had
received one stable build that passed the commit tests, otherwise a red
square. Over time the calendar revealed the state of the build process
showing a steady improvement until green squares were so common that the
calendar disappeared - its purpose fulfilled.

### Automate Deployment

To do Continuous Integration we need multiple environments, one to
run commit tests, probably more to run further parts of the deployment
pipeline. Since we are moving executables between these environments
multiple times a day, we'll want to do this automatically. So it's
important to have scripts that will allow us to deploy the application
into any environment easily.

With modern tools for virtualization, containerization, and serverless we can go
further. Not just have scripts to deploy the product, but also scripts
to build the required environment from scratch. This way we can start
with a bare-bones environment that's available off-the-shelf, create the
environment we need for the product to run, install the product, and run
it - all entirely automatically. If we're using feature flags to hide
work-in-progress, then these environments can be set up with all the
feature-flags on, so these features can be tested with all immanent interactions.

A natural consequence of this is that these same scripts allow us to
deploy into production with similar ease. Many teams deploy new code
into production multiple times a day using these automations, but even
if we choose a less frequent cadence, automatic deployment helps speed
up the process and reduces errors. It's also a cheap option since it
just uses the same capabilities that we use to deploy into test
environments.

If we deploy into production automatically, one extra capability we find
handy is automated rollback. Bad things do happen from time to time, and
if smelly brown substances hit rotating metal, it's good to be able to
quickly go back to the last known good state. Being able to
automatically revert also reduces a lot of the tension of deployment,
encouraging people to deploy more frequently and thus get new features
out to users quickly. [Blue Green Deployment](/bliki/BlueGreenDeployment.html) allows us
to both make new versions live quickly, and to roll back equally quickly
if needed, by shifting traffic between deployed versions.

Automated Deployment make it easier to set up [Canary Releases](/bliki/CanaryRelease.html), deploying a new version of a
product to a subset of our users in order to flush out problems before
releasing to the full population.

Mobile applications are good examples of where it's essential to
automate deployment into test environments, in this case onto devices so
that a new version can be explored before invoking the guardians of the
App Store. Indeed any device-bound software needs ways to easily get new
versions on to test devices.

When deploying software like this, remember to ensure that version
information is visible. An about screen should contain a build id that
ties back to version control, logs should make it easy to see which version
of the software is running, there should be some API endpoint that will
give version information.

## Styles of Integration

Thus far, I've described one way to approach integration, but if it's
not universal, then there must be other ways. As with anything, any
classification I give has fuzzy boundaries, but I find it useful to think
of three styles of handling integration: Pre-Release Integration, Feature
Branches, and Continuous Integration.

The oldest is the one I saw in that warehouse in the 80's -
**Pre-Release Integration**. This sees integration as a phase of
a software project, a notion that is a natural part of a [Waterfall Process](/bliki/WaterfallProcess.html). In such a project work is divided into
units, which may be done by individuals or small teams. Each unit is
a portion of the software, with minimal interaction with other
units. These units are built and tested on their own (the original use of
the term “unit test”). Then once the units are ready, we integrate them
into the final product. This integration occurs once, and is followed by
integration testing, and on to a release. Thus if we think of the work, we
see two phases, one where everyone works in parallel on features,
followed by a single stream of effort at integration.

The frequency of integration in
this style is tied to the frequency of release, usually major versions of
the software, usually measured in months or years. These teams will use a
different process for urgent bug fixes, so they can be released
separately to the regular integration schedule.

One of the most popular approaches to integration these days is to use
**[Feature Branches](/bliki/FeatureBranch.html)**. In this style
features are assigned to individuals or small teams, much as units in the
older approach. However, instead of waiting until all the units are done
before integrating, developers integrate their feature into the mainline
as soon as it's done. Some teams will release to production after each
feature integration, others prefer to batch up a few features for
release.

Teams using feature branches will usually expect everyone to pull from
mainline regularly, but this is semi-integration. If Rebecca and I
are working on separate features, we might pull from mainline every day,
but we don't see each other's changes until one of us completes our
feature and integrates, pushing it to the mainline. Then the other will
see that code on their next pull, integrating it into their working copy.
Thus after each feature is pushed to mainline, every other developer will
then do integration work to combine this latest mainline push with
their own feature branch.

This is only semi-integration because each developer combines the
changes on mainline to their own local branch. Full integration can't
happen until a developer pushes their changes, causing another round of
semi-integrations. Even if Rebecca and I both pull the same changes from
mainline, we've only integrated with those changes, not with each other's
branches.

With **Continuous Integration**, every day we are all pushing our changes
to the mainline and pulling everyone else's changes into our own work.
This leads to many more bouts of integration work, but each bout is much
smaller. It's much easier to combine a few hours work on a code base than
to combine several days.

## Benefits of Continuous Integration

When discussing the relative merits of the three styles of integration,
most of the discussion is truly about the [frequency of integration](/articles/branching-patterns.html#integration-frequency). Both Pre-Release
Integration and Feature Branching can operate at different frequencies and
it's possible to change integration frequency without changing the style
of integration. If we're using Pre-Release Integration, there's a big
difference between monthly releases and annual releases. Feature Branching
usually works at a higher frequency, because integration occurs when each
feature is individually pushed to mainline, as opposed to waiting to batch
a bunch of units together. If a team is doing Feature Branching and all
its features are less than a day's work to build, then they are
effectively the same as Continuous Integration. But Continuous Integration
is different in that it's *defined* as a high-frequency style.
Continuous Integration makes a point of setting integration frequency as a
target in itself, and not binding it to feature completion or release
frequency.

It thus follows that most teams can see a useful improvement in the
factors I'll discuss below by increasing their frequency without changing
their style. There are significant benefits to reducing the size of
features from two months to two weeks. Continuous Integration has the
advantage of setting high-frequency integration as the baseline, setting
habits and practices that make it sustainable.

### Reduced risk of delivery delays

It's very hard to estimate how long it takes to do a complex
integration. Sometimes it can be a struggle to merge in git, but then
all works well. Other times it can be a quick merge, but a subtle
integration bug takes days to find and fix. The longer the time between
integrations, the more code to integrate, the longer it takes - but
what's worse is the increase in unpredictability.

This all makes pre-release integration a special form of nightmare.
Because the integration is one of the last steps before release, time is
already tight and the pressure is on. Having a hard-to-predict phase
late in the day means we have a significant risk that's very difficult
to mitigate. That was why my 80's memory is so strong, and it's hardly the
only time I've seen projects stuck in an integration hell, where every
time they fix an integration bug, two more pop up.

Any steps to increase integration frequency lowers this risk. The
less integration there is to do, the less unknown time there is before a
new release is ready. Feature Branching helps by pushing this
integration work to individual feature streams, so that, if left alone,
a stream can push to mainline as soon as the feature is ready.

But that *left alone* point is important. If anyone else pushes
to mainline, then we introduce some integration work before the feature
is done. Because the branches are isolated, a developer working on one
branch doesn't have much visibility about what other features may push,
and how much work would be involved to integrate them. While there is a
danger that high priority features can face integration delays, we can
manage this by preventing pushes of lower-priority features.

Continuous Integration effectively eliminates delivery risk. The
integrations are so small that they usually proceed without comment. An
awkward integration would be one that takes more than a few minutes to
resolve. The very worst case would be conflict that causes someone to
restart their work from scratch, but that would still be less than a
day's work to lose, and is thus not going to be something that's likely
to trouble a board of stakeholders. Furthermore we're doing integration
regularly as we develop the software, so we can face problems while we
have more time to deal with them and can practice how to resolve
them.

Even if a team isn't releasing to production regularly, Continuous
Integration is important because it allows everyone to see exactly what
the state of the product is. There's no hidden integration efforts that
need to be done before release, any effort in integration is already
baked in.

### Less time wasted in integration

I've not seen any serious studies that measure how time spent on
integration matches the size of integrations, but my anecdotal
evidence strongly suggests that the relationship isn't linear. If
there's twice as much code to integrate, it's more likely to be four
times as long to carry out the integration. It's rather like how we need
three lines to fully connect three nodes, but six lines to connect four
of them. Integration is all about connections, hence the non-linear
increase, one that's reflected in the experience of my colleagues.

In organizations that are using feature branches, much of this lost
time is felt by the individual. Several hours spent trying to rebase on
a big change to mainline is frustrating. A few days spent waiting for a
code review on a finished pull request, which another big mainline
change during the waiting period is even more frustrating. Having to put
work on a new feature aside to debug a problem found in an integration
test of feature finished two weeks ago saps productivity.

When we're doing Continuous Integration, integration is generally a
non-event. I pull down the mainline, run the build, and push. If
there is a conflict, the small amount of code I've written is fresh in
my mind, so it's usually easy to see. The workflow is regular, so we're
practiced at it, and we're incentives to automate it as much as
possible.

Like many of these non-linear effects, integration can easily become
a trap where people learn the wrong lesson. A difficult integration may
be so traumatic that a team decides it should do integrations less
often, which only exacerbates the problem in the future.

What's happening here is that we are seeing much closer collaboration
between the members of the team. Should two developers make decisions
that conflict, we find out when we integrate. So the less time
between integrations, the [less time before we detect the conflict](/articles/branching-patterns.html#compare-freq), and
we can deal with the conflict before it grows too big. With high-frequency
integration, our source control system becomes a communication channel,
one that can communicate things that can otherwise be unsaid.

### Less Bugs

Bugs - these are the nasty things that destroy confidence and mess up
schedules and reputations. Bugs in deployed software make users angry
with us. Bugs cropping up during regular development get in our way,
making it harder to get the rest of the software working correctly.

Continuous Integration doesn't get rid of bugs, but it does make them
dramatically easier to find and remove. This is less because of the
high-frequency integration and more due to the essential introduction of
self-testing code. Continuous Integration doesn't work without
self-testing code because without decent tests, we can't keep a healthy
mainline. Continuous Integration thus institutes a regular regimen of
testing. If the tests are inadequate, the team will quickly notice, and
can take corrective action. If a bug appears due to a semantic conflict,
it's easy to detect because there's only a small amount of code to be
integrated. Frequent integrations also work well with [Diff Debugging](/bliki/DiffDebugging.html), so even a bug noticed weeks later can be
narrowed down to a small change.

Bugs are also cumulative. The
more bugs we have, the harder it is to remove each one. This is partly
because we get bug interactions, where failures show as the result of
multiple faults - making each fault harder to find. It's also
psychological - people have less energy to find and get rid of bugs when
there are many of them. Thus self-testing code reinforced by Continuous
Integration has another exponential effect in reducing the problems
caused by defects.

This runs into another phenomenon that many
people find counter-intuitive. Seeing how often introducing a change
means introducing bugs, people conclude that to have high reliability
software they need to slow down the release rate. This was firmly
contradicted by the [DORA research
program](/bliki/StateOfDevOpsReport.html) led by Nicole Forsgren. They found that elite teams
deployed to production more rapidly, more frequently, and had a
dramatically lower incidence of failure when they made these changes.
The research also finds that teams have higher levels of performance
when they have three or fewer active branches in the application’s code
repository, merge branches to mainline at least once a day, and don’t have
code freezes or integration phases.

### Enables Refactoring for sustained productivity

Most teams observe that over time, codebases deteriorate. Early
decisions were good at the time, but are no longer optimal after six
month's work. But changing the code to incorporate what the team has
learned means introducing changes deep in the existing code,
which results in difficult merges which are both time-consuming and full
of risk. Everyone recalls that time someone made what would be a good
change for the future, but caused days of effort breaking other people's
work. Given that experience, nobody wants to rework the structure of
existing code, even though it's now awkward for everyone to build on,
thus slowing down delivery of new features.

Refactoring is an essential technique to attenuate and indeed reverse
this process of decay. A team that refactors regularly has a
disciplined technique to improve the structure of a code base by using
small, behavior-preserving transformations of the code. These
characteristics of the transformations
greatly reduce their chances of introducing bugs, and
they can be done quickly, especially when supported by a foundation of
self-testing code. Applying refactoring at every opportunity, a team can
improve the structure of an existing codebase, making it easier and
faster to add new capabilities.

But this happy story can be torpedoed by integration woes. A two week
refactoring session may greatly improve the code, but result in long
merges because everyone else has been spending the last two weeks
working with the old structure. This raises the costs of refactoring to
prohibitive levels. Frequent integration solves this dilemma by ensuring
that both those doing the refactoring and everyone else are regularly
synchronizing their work. When using Continuous Integration, if someone
makes intrusive changes to a core library I'm using, I only have to
adjust a few hours of programming to these changes. If they do something
that clashes with the direction of my changes, I know right away, so
have the opportunity to talk to them so we can figure out a better way
forward.

So far in this article I've raised several counter-intuitive notions about
the merits of high-frequency integration: that the more often we
integrate, the less time we spend integrating, and that frequent
integration leads to less bugs. Here is perhaps the most important
counter-intuitive notion in software development: that teams that spend a
lot of effort keeping their code base healthy [deliver features faster and cheaper](/articles/is-quality-worth-cost.html). Time
invested in writing tests and refactoring delivers impressive returns in
delivery speed, and Continuous Integration is a core part of making that
work in a team setting.

### Release to Production is a business decision

Imagine we are demonstrating some newly built feature to a
stakeholder, and she reacts by saying - “this is really cool, and would
make a big business impact. How long before we can make this live?” If
that feature is being shown on an unintegrated branch, then the answer
may be weeks or months, particularly if there is poor automation on the
path to production. Continuous Integration allows us to maintain a
[Release-Ready Mainline](/articles/branching-patterns.html#release-ready-mainline), which means the
decision to release the latest version of the product into production is
purely a business decision. If the stakeholders want the latest to go
live, it's a matter of minutes running an automated pipeline to make it
so. This allows the customers of the software greater control of when
features are released, and encourages them to collaborate more closely
with the development team

Continuous Integration and a Release-Ready Mainline removes one of the biggest
barriers to frequent deployment. Frequent deployment is valuable because
it allows our users to get new features more rapidly, to give more
rapid feedback on those features, and generally become more
collaborative in the development cycle. This helps break down the
barriers between customers and development - barriers which I believe
are the biggest barriers to successful software development.

## When we should *not* use Continuous Integration

All those benefits sound rather juicy. But folks as experienced (or
cynical) as I am are always suspicious of a bare list of benefits. Few
things come without a cost, and decisions about architecture and process
are usually a matter of trade-offs.

But I confess that Continuous Integration is one of those rare cases
where there's little downside for a committed and skillful team to utilize it. The cost
imposed by sporadic integration is so great, that almost any team can
benefit by increasing their integration frequency. There is some limit to
when the benefits stop piling up, but that limit sits at hours rather
than days, which is exactly the territory of Continuous Integration. The
interplay between self-testing code, Continuous Integration, and
Refactoring is particularly strong. We've been using this approach for two
decades at Thoughtworks, and our only question is how to do it more
effectively - the core approach is proven.

But that doesn't mean that Continuous Integration is for everyone. You
might notice that I said that “there’s little downside for a
*committed and skillful* team to utilize it”. Those two adjectives
indicate the contexts where Continuous Integration isn't a good fit.

By “committed”, I mean a team that's working full-time on a product. A
good counter-example to this is a classical open-source project, where
there is one or two maintainers and many contributors. In such a situation
even the maintainers are only doing a few hours a week on the project,
they don't know the contributors very well, and don't have good visibility
for when contributors contribute or the standards they should follow when
they do. This is the environment that led to a feature branch workflow and
pull-requests. In such a context Continuous Integration isn't plausible,
although efforts to increase the integration frequency can still be
valuable.

Continuous Integration is more suited for team working full-time on a
product, as is usually the case with commercial software. But there is
much middle ground between the classical open-source and the full-time
model. We need to use our judgment about what integration policy to use
that fits the commitment of the team.

The second adjective looks at the skill of the team in following the
necessary practices. If a team attempts Continuous
Integration without a strong test suite, they will run into all sorts of
trouble because they don't have a mechanism for screening out bugs. If they don't
automate, integration will take too long, interfering with the flow of
development. If folks aren't disciplined about ensuring their pushes to
mainline are done with green builds, then the mainline will end up
broken all the time, getting in the way of everyone's work.

Anyone who is considering introducing Continuous Integration has to
bear these skills in mind. Instituting Continuous Integration without
self-testing code won't work, and it will also give a inaccurate
impression of what Continuous Integration is like when it's done well.

That said, I don't think the skill demands are particularly hard. We don't
need rock-star developers to get this process working in a team. (Indeed
rock-star developers are often a barrier, as people who think of themselves
that way usually aren't very disciplined.) The skills for these technical practices
aren't that hard to learn, usually the problem is finding a good teacher,
and forming the habits that crystallize the discipline. Once the team gets
the hang of the flow, it usually feels comfortable, smooth - and fast.

## Introducing Continuous Integration

One of the hard things about describing how to introduce a practice
like Continuous Integration is that the path depends very much on where
you're starting. Writing this, I don't know what kind code you are working
on, what skills and habits your team possesses, let alone the broader
organizational context. All anyone like me can do is point out some common
signposts, in the hope that it will help you find your own path.

When introducing any new practice, it's important to be clear on why
we're doing it. My list of benefits above includes the most common
reasons, but different contexts lead to a different level of importance
for them. Some benefits are harder to appreciate than others. Reducing
waste in integration addresses a frustrating problem, and can be easily
sensed as we make progress. Enabling refactoring to reduce the cruft in a
system and improve overall productivity is more tricky to see. It takes
time before we see an effect, and it's hard to compare to the counter-factual. Yet
this is probably the most valuable benefit of Continuous Integration.

The list of practices above indicate the skills a team needs
to learn in order to make Continuous Integration work. Some of these can
bring value even before we get close to the high integration frequency.
Self-testing code adds stability to a system even with infrequent commits.

One target can be to double the integration frequency. If feature
branches typically run for ten days, figure out how to cut them down to
five. This may involve better build and test automation, and creative
thinking on how a large task can be split into smaller, independently
integrated tasks. If we use pre-integration reviews, we could include
explicit steps in those reviews to check test coverage and
encourage smaller commits.

If you are starting a new project, we can begin with Continuous
Integration from the beginning. We should keep an eye on build times and
take action as soon as we start going slower than the ten minute rule. By
acting quickly we'll make the necessary restructurings before the code
base gets so big that it becomes a major pain.

Above all we should get some help. We should find someone who has done
Continuous Integration before to help us. Like any new technique it's hard
to introduce it when we don't know what the final result looks like. It
may cost money to get this support, but we'll otherwise pay in lost time
and productivity. (Disclaimer / Advert - yes we at Thoughtworks do some
consultancy in this area. After all we've made most of the mistakes that
there are to make.)

## Common Questions

### Where did Continuous Integration come from?

Continuous Integration was developed as a practice by Kent Beck as
part of Extreme Programming in the 1990s. At that time pre-release
integration was the norm, with release frequencies often measured in
years. There had been a general push to iterative development, with
faster release cycles. But few teams were thinking in weeks between
releases. Kent defined the practice, developed it with projects he
worked on, and established how it interacted with the
other key practices upon which it relies.

Microsoft had been known for doing daily builds (usually
overnight), but without the testing regimen or the focus on fixing
defects that are such crucial elements of Continuous
Integration.

Some people credit Grady Booch for coining the term, but he only
used the phrase as an offhand description in a single sentence in his
object-oriented design book. He did not treat it as a defined practice,
indeed it didn't appear in the index.

### What is the difference between Continuous Integration and Trunk-Based Development?

As CI Services became popular, many people used
them to run regular builds on feature branches. This, as explained
above, isn't Continuous Integration at all, but it led to many people
saying (and thinking) they were doing Continuous Integration when they
were doing something significantly different, which causes a lot of confusion.

Some folks decided to tackle this [Semantic Diffusion](/bliki/SemanticDiffusion.html) by coining a new term: Trunk-Based
Development. In general I see this as a synonym to Continuous Integration
and acknowledge that it doesn't tend to suffer from confusion with
“running Jenkins on our feature branches”. I've read some people
trying to formulate some distinction between the two, but I find these
distinctions are neither consistent nor compelling.

I don't use the term Trunk-Based Development, partly because I don't
think coining a new name is a good way to counter semantic diffusion,
but mostly because renaming this technique rudely erases the work of
those, especially Kent Beck, who championed and developed Continuous
Integration in the beginning.

Despite me avoiding the term, there is a lot of good information
about Continuous Integration that's written under the flag of
Trunk-Based Development. In particular, Paul Hammant has written a lot
of excellent material on his [website](https://trunkbaseddevelopment.com).

### Can we run a CI Service on our feature branches?

The simple answer is “yes - but you're *not* doing Continuous
Integration”. The key principle here is that “Everyone Commits To the
Mainline Every Day”. Doing an automated build on feature branches is
useful, but it is only [semi-integration](#semi-integration).

However it is a common confusion that using a daemon build in this
way is what Continuous Integration is about. The confusion comes from
calling these tools Continuous Integration Services, a better term
would be something like “Continuous Build Services”. While using a CI
Service is a useful aid to doing Continuous Integration, we shouldn't
confuse a tool for the practice.

### Can a team do both Continuous Integration and Feature Branching at the same time?

In general, Continuous Integration and Feature Branching are
mutually exclusive approaches. Most folks who think they are doing
both are running a CI Service on their Feature Branches, which as I
explain in the previous question, isn't doing Continuous Integration.

There is one situation where it is possible to do both, that is
when all the features are so small they can be completed in less than
a day. But that seems to be a very rare case, and most people would
just call that Continuous Integration.

A secondary point here is that it's perfectly permissible to do
personal work on a separate branch, then merge it with main and push
when I integrate. I might do that if I were worried I'd fat-finger my
IDE and push a broken local main by accident. The key question is
whether I'm integrating continuously, not how I manage my personal
workspace.

### What is the difference between Continuous Integration and Continuous Delivery?

The early descriptions of Continuous Integration focused on the
cycle of developer integration with the mainline in the team's
development environment. Such descriptions didn't talk much about the
journey from an integrated mainline to a production release. That
doesn't mean they weren't in people's minds. Practices like “Automate
Deployment” and “Test in a Clone of the Production Environment” clearly
indicate a recognition of the path to production.

In some situations, there wasn't much else after mainline
integration. I recall Kent showing me a system he was working on in
Switzerland in the late 90's where they deployed to production, every
day, automatically. But this was a Smalltalk system, that didn't have
complicated steps for a production deploy. In the early 2000s at
Thoughtworks, we often had situations where that path to production was
much more complicated. This led to the notion that there was an
activity beyond Continuous Integration that addressed that path. That
activity came to knows as Continuous Delivery.

The aim of Continuous Delivery is that the product should always be
in a state where we can release the latest build. This is essentially
ensuring that the release to production is a business decision.

For many people these days, Continuous Integration is about
integrating code to the mainline in the development team's environment,
and Continuous Delivery is the rest of the deployment pipeline heading
to a production release. Some people treat Continuous Delivery as
encompassing Continuous Integration, others see them as closely linked
partners, often with the moniker CI/CD. Others argue that
Continuous Delivery is merely a synonym for Continuous Integration.

### How does Continuous Deployment fit in with all this?

Continuous Integration ensures everyone integrates their code at
least daily to the mainline in version control. Continuous Delivery
then carries out any steps required to ensure that the product is
releasable to product whenever anyone wishes. Continuous Deployment
means the product is automatically released to production whenever it
passes all the automated tests in the deployment pipeline.

With Continuous Deployment every commit pushed to mainline as part
of Continuous Integration will be automatically deployed to production
providing all of the verifications in the deployment pipeline are
green. Continuous Delivery just assures that this is possible (and is
thus a pre-requisite for Continuous Deployment).

### How do we do pull requests and code reviews?

[Pull Requests](/bliki/PullRequest.html), an artifact of GitHub,
are now widely used on software projects. Essentially they provide a
way to add some process to the push to mainline, usually involving a
[pre-integration code review](/articles/branching-patterns.html#reviewed-commits), requiring
another developer to approve before the push can be accepted into the
mainline. They developed mostly in the context of feature branching in
open-source projects, ensuring that the maintainers of a project can
review that a contribution fits properly into the style and future
intentions of the project.

The pre-integration code review can be problematic for Continuous
Integration because it usually adds significant friction to the
integration process. Instead of an automated process that can be done
within minutes, we have to find someone to do the code review,
schedule their time, and wait for feedback before the review is
accepted. Although some organizations may be able to get to flow
within minutes, this can easily end up being hours or days - breaking
the timing that makes Continuous Integration work.

Those who do Continuous Integration deal with this by reframing how
code review fits into their workflow. [Pair Programming](/bliki/PairProgramming.html) is popular because it creates a continuous
real-time code review as the code is being written, producing a much
faster feedback loop for the review. The [Ship / Show / Ask](/articles/ship-show-ask.html) process encourages teams
to use a blocking code review only when necessary, recognizing that
post-integration review is often a better bet as it doesn't interfere
with integration frequency. Many teams find that [Refinement Code Review](/bliki/RefinementCodeReview.html) is an important force to maintaining a
healthy code base, but works at its best when Continuous Integration
produces an environment friendly to refactoring.

We should remember that pre-integration review grew out of an
open-source context where contributions appear impromptu from weakly
connected developers. Practices that are effective in that environment
need to be reassessed for a full-time team of closely-knit staff.

### How do we handle databases?

Databases offer a specific challenge as we increase integration
frequency. It's easy to include database schema definitions and load
scripts for test data in the version-controlled sources. But that
doesn't help us with data outside of version-control, such as
production databases. If we change the database schema, we need to
know how to handle existing data.

With traditional pre-release integration, data migration
is a considerable challenge, often spinning up special teams just to
carry out the migration. At first blush, attempting high-frequency
integration would introduce an untenable amount of data migration work.

In practice, however, a change in perspective removes this problem.
We faced this issue in Thoughtworks on our early projects using
Continuous Integration, and solved it by shifting to an [Evolutionary Database Design](/articles/evodb.html) approach, developed
by my colleague Pramod Sadalage. The key to this methodology is to
define database schema and data through a series of migration scripts,
that alter both the database schema and data. Each migration is small,
so is easy to reason about and test. The migrations compose naturally,
so we can run hundreds of migrations in sequence to perform
significant schema changes and migrate the data as we go. We can store
these migrations in version-control in sync with the data access code
in the application, allowing us to build any version of the software,
with the correct schema and correctly structured data. These
migrations can be run on test data, and on production databases.

## Final Thoughts

Most software development is about changing existing code. The cost and
response time for adding new features to a code base depends greatly upon
the condition of that code base. [A crufty code
base is harder and more expensive to modify.](/articles/is-quality-worth-cost.html) To keep cruft to a
minimum a team needs to be able to regularly refactor the code, changing
its structure to reflect changing needs and incorporate lessons the team
learns from working on the product.

Continuous Integration is vital for a healthy product because it is a
key component of this kind of evolutionary design ecosystem. Together with
and supported by self-testing code, it's the underpinning for refactoring.
These technical practices, born together in Extreme Programming, can
enable a team to deliver regular enhancement of a product to take
advantage of changing needs and technological opportunities.

---

## Further Reading

An essay like this can only cover so much ground, but this is an
important topic so I've created a [guide
page](../delivery.html) on my website to point you to more information.

To explore Continuous Integration in more detail I suggest taking a
look at Paul Duvall's [appropriately titled
book](/books/duvall.html) on the subject (which won a Jolt award - more than I've ever
managed). For more on the broader process of Continuous Delivery, take a
look at [Jez Humble and Dave
Farley's book](/books/continuousDelivery.html) - which also beat me to a Jolt award.

My article on [Patterns
for Managing Source Code Branches](/articles/branching-patterns.html) looks at the broader context,
showing how Continuous Integration fits into the wider decision space of
choosing a branching strategy. As ever, the driver for choosing when to
branch is knowing you are going to integrate.

The  [original article
on Continuous Integration](originalContinuousIntegration.html) describes our
experiences as Matt helped put together
continuous integration on a Thoughtworks project in 2000.

As I [indicated earlier](#trunk-based), many people write
about Continuous Integration using the term “Trunk-Based Development”.
Paul Hammant's [website](https://trunkbaseddevelopment.com) contains a lot of
useful and practical information. Clare Sudbery recently wrote an [informative report](https://www.oreilly.com/library/view/what-is-trunk-based/9781098146658/) available through O'Reilly.

## Acknowledgments

First and foremost to Kent Beck and my many colleagues on the
Chrysler Comprehensive Compensation (C3) project. This was my
first chance to see Continuous Integration in action with a
meaningful amount of unit tests. It showed me what was possible
and gave me an inspiration that led me for many years.

Thanks to Matt Foemmel, Dave Rice, and everyone else who
built and maintained Continuous Integration on Atlas. That
project was a sign of CI on a larger scale and showed the
benefits it made to an existing project.

Paul Julius, Jason Yip, Owen Rodgers, Mike Roberts and many
other open source contributors have participated in building
some variant of CruiseControl, the first CI service. Although a CI service isn't
essential, most teams find it helpful. CruiseControl and other
CI services have played a big part in popularizing and enabling
software developers to use Continuous Integration.

In the fall of 2023, Michael Lihs emailed me with suggested revisions
to the article, which inspired me to
do a major overhaul. Birgitta
Böckeler, Camilla Crispim, Casey Lee, Chris Ford, Clare Sudbery, Evan Bottcher, Jez
Humble, Kent Beck, Kief Morris, Mike Roberts, Paul Hammant, Pete
Hodgson, Rafael Detoni, Rouan Wilsenach, and Trisha Gee
reviewed and commented on this revision.

One of the reasons I work at Thoughtworks is to get good
access to practical projects done by talented people. Nearly
every project I've visited has given tasty morsels of continuous
integration information.

Significant Revisions

*18 January 2024:* Published revised version

*18 October 2023:* Began rewrite to bring it up to date

*01 May 2006:* Complete rewrite of article to bring it
up to date and to clarify the description of the approach.

*10 September 2000:* Original version published.

---

## Bibliography

1. [[Domain Driven Design](DomainDrivenDesign.html)](https://martinfowler.com/bliki/DomainDrivenDesign.html)
2. [[Continuous Delivery](ContinuousDelivery.html)](https://martinfowler.com/bliki/ContinuousDelivery.html)
3. [Introduction](https://12factor.net/)
4. [[CQRS](CQRS.html)](https://martinfowler.com/bliki/CQRS.html)
5. [[Test Pyramid](TestPyramid.html)](https://martinfowler.com/bliki/TestPyramid.html)
6. [Microservices](https://martinfowler.com/articles/microservices.html)
7. [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)