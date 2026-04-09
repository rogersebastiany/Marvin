:root{--nextra-primary-hue:319deg;--nextra-primary-saturation:100%;--nextra-primary-lightness:44.1%;--nextra-navbar-height:64px;--nextra-menu-height:3.75rem;--nextra-banner-height:2.5rem;--nextra-bg:251,251,249;}.dark{--nextra-primary-hue:319deg;--nextra-primary-saturation:100%;--nextra-primary-lightness:90%;--nextra-bg:15,15,12;}Learn | GraphQL

html {
--font-sans: '\_\_hostGrotesk\_4b1926', '\_\_hostGrotesk\_Fallback\_4b1926';
--font-mono: '\_\_commitMono\_9d2e4e', '\_\_commitMono\_Fallback\_9d2e4e';
}((e,t,r,n,o,i,a,l)=>{let s=document.documentElement,u=["light","dark"];function c(t){(Array.isArray(e)?e:[e]).forEach(e=>{let r="class"===e,n=r&&i?o.map(e=>i[e]||e):o;r?(s.classList.remove(...n),s.classList.add(i&&i[t]?i[t]:t)):s.setAttribute(e,t)}),l&&u.includes(t)&&(s.style.colorScheme=t)}if(n)c(n);else try{let e=localStorage.getItem(t)||r,n=a&&"system"===e?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":e;c(n)}catch(e){}})("class","theme","system",null,["light","dark"],null,true,true)

document.documentElement.setAttribute('dir','ltr')

* [Learn](/learn/)
* Resource Hub
* Community
* [Blog](/blog/)
* [GraphQLConf 2026](/conf/2026/)
* [GraphQL.JS Tutorial](/graphql-js/)

light

light

.nextra-nav-container.sticky { position: fixed }

# Learn GraphQL

Get hands-on with the fundamentals of GraphQL. Start with the basics and see how it compares to other technologies.  
 Then move on to best practices for designing better APIs.

[Start with the basics](/learn/introduction/)

## What will you find here?

* [Learn GraphQL](#learn-graphql)
* [Tutorials](#tutorials)
* [Best Practices](#best-practices)
* [FAQ](#faq)

Learn GraphQL

## Getting started with GraphQL

In this tutorial-style introduction to GraphQL, you'll learn the core concepts that power every GraphQL API. Follow a step-by-step path from basic queries to advanced features.

[Start learning](/learn/introduction/)

* [Lesson 1Introduction

  Get a high-level overview of GraphQL and how it enables flexible, versionless APIs powered by a strong type system.](/learn/introduction)
* [Lesson 2Schemas and Types

  Learn how GraphQL’s schema language defines the shape of your data using types.](/learn/schema)
* [Lesson 3Queries

  Understand how to structure GraphQL queries to request exactly the data you need — including fields, variables and fragments.](/learn/queries)
* [Lesson 4Mutations

  Explore how to modify data with mutations, including how to update and remove records through your schema.](/learn/mutations)
* [Lesson 5Subscriptions

  Discover how GraphQL supports real-time data with subscriptions and how to use them effectively at scale.](/learn/subscriptions)
* [Lesson 6Validation

  See how GraphQL ensures query correctness through validation rules and how common errors are detected early.](/learn/validation)
* [Lesson 7Execution

  Learn how resolvers power GraphQL execution and how the server processes and returns data for each query.](/learn/execution)
* [Lesson 8Response

  Explore how GraphQL structures its responses, including data, errors and extensions for custom metadata.](/learn/response)
* [Lesson 9Introspection

  Use introspection to explore the schema itself — a powerful way to inspect types and fields dynamically.](/learn/introspection)

Show more

Best practices

## Practical guidelines

Here you'll explore real-world strategies for designing and operating GraphQL APIs. These guides will help you build for scale and safety.

[Explore all best practices](/learn/best-practices/)

* [Lesson 1Introduction

  Understand the context behind the GraphQL Best Practices lessons.](/learn/best-practices)
* [Lesson 2Thinking In Graphs

  Learn how to shift your mindset from RESTful endpoints to graph-based thinking, aligning your schema with business logic and legacy systems.](/learn/thinking-in-graphs)
* [Lesson 3Serving Over Http

  Explore how GraphQL operates over HTTP, including methods, headers, status codes and API endpoint design.](/learn/serving-over-http)
* [Lesson 4File Uploads

  Handle file uploads in GraphQL by wrapping them as mutations. Learn the recommended approach for integrating file handling into your API.](/learn/file-uploads)
* [Lesson 5Authorization

  Understand how to secure your GraphQL APIs with type- and field-level authorization patterns.](/learn/authorization)
* [Lesson 6Pagination

  Discover different pagination strategies in GraphQL, from simple slicing to fully connected edges and nodes.](/learn/pagination)
* [Lesson 7Schema Design

  Learn how to design clear, adaptable schemas — including versioning and thoughtful use of nullability.](/learn/schema-design)
* [Lesson 8Global Object Identification

  Use globally unique IDs and the Node interface to enable caching, refetching, and efficient schema traversal.](/learn/global-object-identification)
* [Lesson 9Caching

  Explore caching techniques and ID strategies that make client-side performance and object reuse more effective.](/learn/caching)
* [Lesson 10Performance

  Get practical tips for improving GraphQL performance — from preventing N+1 problems to monitoring and compression.](/learn/performance)
* [Lesson 11Security

  Protect your GraphQL API with best practices for query limits, input validation, introspection control and more.](/learn/security)
* [Lesson 12Federation

  Learn how GraphQL federation enables modular, scalable APIs by composing services into a unified schema.](/learn/federation)
* [Lesson 13Common GraphQL over HTTP Errors

  Learn about common 'graphql-http' errors and how to debug them.](/learn/debug-errors)

Show more

Tutorials

## Training Courses

Get started or level up your GraphQL skills with these trusted tutorials.

* [GraphQL-JS tutorial

  Step-by-step guide to building schemas and executing queries with GraphQL.js.](https://www.graphql-js.org/docs/)
* [Apollo Odyssey

  Interactive courses for building GraphQL applications with Apollo's toolset.](https://www.apollographql.com/tutorials/)
* [Yoga GraphQL Server Tutorial

  Open source tutorial for creating modern GraphQL Servers in Node, CF Workers, Deno and others.](https://the-guild.dev/graphql/yoga-server/tutorial/basic)
* [GraphQL Tutorials

  Real World Fullstack GraphQL tutorials for developers by Hasura.](https://hasura.io/learn/)

FAQ

## Common questions

Find answers to the most common questions about GraphQL — from getting started to advanced use cases. This also covers frontend concerns and info about the official specification.

* [Getting started](/faq/#getting-started)
* [General](/faq/#general)
* [Best practices](/faq/#best-practices)
* [Specification](/faq/#specification)
* [Frontend](/faq/#frontend)
* [Foundation](/faq/#foundation)

## Looking for more?

Learning is just the beginning. Discover tools and other resources — or connect with the GraphQL community around the world.

[Resources](/resources/)[Community](/community/)

light

### [Learn](/learn/)

[Introduction](/learn/)[Best Practices](/learn/best-practices/)[Frequently Asked QuestionsFAQ](/faq/)[Training Courses](/community/resources/training-courses/)

### Code

[GitHub](https://github.com/graphql)[Specification](https://spec.graphql.org)[Libraries & Tools](/code/)[Services & Vendors](/code/?tags=services)

### Community

[Resources](/community/resources/official-channels/)[Events](/community/events/)[Contribute to GraphQL](/community/contribute/essential-links/)[Landscape](https://landscape.graphql.org)[Shop](https://store.graphql.org/)

### & More

[Blog](/blog/)[GraphQL Foundation](/foundation/)[Community Grant](/foundation/community-grant/)[Brand Guidelines](/brand/)[Code of Conduct](/codeofconduct/)

[## Join GraphQLConf 2026

May 06–07  
Menlo Park, California](/conf/2026/)

light

Copyright © 2026 The GraphQL Foundation. All rights reserved.

{"props":{"pageProps":{}},"page":"/learn","query":{},"buildId":"ymvRHfLkfEIOW1aRGFfsW","nextExport":true,"autoExport":true,"isFallback":false,"scriptLoader":[]}if (window.navigator.platform.includes("Mac")) document.documentElement.classList.add("mac")