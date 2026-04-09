(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-WK23PSS');
Lists - Cypher Manual

(function(f,b){if(!b.\_\_SV){var e,g,i,h;window.mixpanel=b;b.\_i=[];b.init=function(e,f,c){function g(a,d){var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){a.push([d].concat(Array.prototype.slice.call(arguments,0)))}}var a=b;"undefined"!==typeof c?a=b[c]=[]:c="mixpanel";a.people=a.people||[];a.toString=function(a){var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");return d};a.people.toString=function(){return a.toString(1)+".people (stub)"};i="disable time\_event track track\_pageview track\_links track\_forms track\_with\_groups add\_group set\_group remove\_group register register\_once alias unregister identify name\_tag set\_config reset opt\_in\_tracking opt\_out\_tracking has\_opted\_in\_tracking has\_opted\_out\_tracking clear\_opt\_in\_out\_tracking start\_batch\_senders people.set people.set\_once people.unset people.increment people.append people.union people.track\_charge people.clear\_charges people.delete\_user people.remove".split(" ");
for(h=0;h<i.length;h++)g(a,i[h]);var j="set set\_once union unset remove delete".split(" ");a.get\_group=function(){function b(c){d[c]=function(){call2\_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2\_args,0));a.push([e,call2])}}for(var d={},e=["get\_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<j.length;c++)b(j[c]);return d};b.\_i.push([e,f,c])};b.\_\_SV=1.2;e=f.createElement("script");e.type="text/javascript";e.async=!0;e.src="undefined"!==typeof MIXPANEL\_CUSTOM\_LIB\_URL?
MIXPANEL\_CUSTOM\_LIB\_URL:"file:"===f.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";g=f.getElementsByTagName("script")[0];g.parentNode.insertBefore(e,g)}})(document,window.mixpanel||[]);
mixpanel.init("4bfb2414ab973c741b6f067bf06d5575", {batch\_requests: true})
mixpanel.track("Page View", {
pathname: window.location.origin + window.location.pathname,
search: window.location.search,
hash: window.location.hash,
referrer: document.referrer,
})

[Docs](/docs/)

[Docs](/docs/)

Neo4j DBMS

* [Getting Started](/docs/getting-started/current/)
* [Operations](/docs/operations-manual/current/)
* [Migration and Upgrade](/docs/migration-guide/current/)
* [Status Codes](/docs/status-codes/current/)
* [Java Reference](/docs/java-reference/current/)
* [Kerberos Add-on](/docs/kerberos-add-on/current/)

[Neo4j Aura](/docs/aura/)

Neo4j Tools

* [Neo4j Bloom](/docs/bloom-user-guide/current/)
* [Neo4j Browser](/docs/browser/)
* [Neo4j Data Importer](/docs/data-importer/current/)
* [Neo4j Desktop](/docs/desktop-manual/current/)
* [Neo4j Ops Manager](/docs/ops-manager/current/)
* [Neodash commercial](/docs/neodash-commercial/current/)

Neo4j Graph Data Science

* [Neo4j Graph Data Science Library](/docs/graph-data-science/current/)
* [Neo4j Graph Data Science Client](/docs/graph-data-science-client/current/)

Cypher Query Language

* [Cypher](/docs/cypher-manual/current/)
* [Cypher Cheat Sheet](/docs/cypher-cheat-sheet/current/)
* [APOC Library](/docs/apoc/current/)

Generative AI

* [Neo4j GraphRAG for Python](/docs/neo4j-graphrag-python/current/)
* [Embeddings and vector indexes tutorial](/docs/genai/tutorials/embeddings-vector-indexes/)
* [GenAI integrations](/docs/cypher-manual/current/genai-integrations/)
* [Vector search indexes](/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
* [Vector search functions](/docs/cypher-manual/current/functions/vector/)
* [GraphQL vector index search documentation](/docs/graphql/5/directives/indexes-and-constraints/#_vector_index_search)

Create applications

* [Python Driver](/docs/python-manual/current/)
* [Go Driver](/docs/go-manual/current/)
* [Java Driver](/docs/java-manual/current/)
* [JDBC Driver](/docs/jdbc-manual/current/)
* [JavaScript Driver](/docs/javascript-manual/current/)
* [.Net Driver](/docs/dotnet-manual/current/)
* [Neo4j GraphQL Library](/docs/graphql-manual/current/)
* [Neo4j Visualization Library](/docs/nvl/current/)
* [OGM Library](/docs/ogm-manual/current/)
* [Spring Data Neo4j](https://docs.spring.io/spring-data/neo4j/docs/current/reference/html/#reference)
* [HTTP API](/docs/http-api/current/)
* [Neo4j Query API](/docs/query-api/current/)
* [Bolt](/docs/bolt/current/)

Connect data sources

* [Neo4j Connector for Apache Spark](/docs/spark/current/)
* [Neo4j Connector for Apache Kafka](/docs/kafka/)
* [Change Data Capture (CDC)](/docs/cdc/)
* [BigQuery to Neo4j](/docs/dataflow-bigquery/)
* [Google Cloud to Neo4j](/docs/dataflow-google-cloud/)

[Labs](/labs/)

[GenAI Ecosystem](/labs/genai-ecosystem/)

* [LLM Knowledge Graph Builder](/labs/genai-ecosystem/llm-graph-builder/)
* [Vector Index & Search](/labs/genai-ecosystem/vector-search/)
* [LangChain](/labs/genai-ecosystem/langchain/)
* [LangChain.js](/labs/genai-ecosystem/langchain-js/)
* [LlamaIndex](/labs/genai-ecosystem/llamaindex/)
* [Haystack](/labs/genai-ecosystem/haystack/)
* [DSPy](/labs/genai-ecosystem/dspy/)

**Developer Tools**

* [APOC Extended](/labs/apoc/)
* [Aura CLI](/labs/aura-cli/)
* [arrows.app](/labs/arrows/)
* [Cypher Workbench](/labs/cypher-workbench/)
* [ETL Tool](/labs/etl-tool/)
* [NeoDash](/labs/neodash/)

**Frameworks & Integrations**

* [Needle Starter Kit](/labs/neo4j-needle-starterkit/)
* [Neo4j Plugin for Liquibase](/labs/liquibase/)
* [Neo4j Migrations](/labs/neo4j-migrations/)
* [neomodel](/labs/neomodel/)

[RDF & Linked Data](/labs/neosemantics/)

* [Neosemantics (Java)](/labs/neosemantics/)
* [RDFLib-Neo4j (Python)](/labs/rdflib-neo4j/)

[Get Help](/developer/resources/)

[Community Forum](https://dev.neo4j.com/forum)

[Discord Chat](https://dev.neo4j.com/chat)

[Product Support](http://support.neo4j.com)

[Neo4j Developer Blog](https://neo4j.com/blog/developer/)

[Neo4j Videos](/videos/)

[GraphAcademy](https://graphacademy.neo4j.com/?ref=docs-nav)

[Beginners Courses](https://graphacademy.neo4j.com/categories/beginners/?ref=docs-nav)

* [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/?ref=docs-nav)
* [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/?ref=docs-nav)
* [Importing Data Fundamentals](https://graphacademy.neo4j.com/courses/importing-fundamentals/?ref=docs-nav)
* [Importing CSV Data](https://graphacademy.neo4j.com/courses/importing-csv-data/?ref=docs-nav)
* [Graph Data Modeling](https://graphacademy.neo4j.com/courses/modeling-fundamentals/?ref=docs-nav)

[Data Scientist Courses](https://graphacademy.neo4j.com/categories/data-scientist/?ref=docs-nav)

* [Into to Graph Data Science](https://graphacademy.neo4j.com/courses/gds-product-introduction/?ref=docs-nav)
* [Graph Data Science Fundamentals](https://graphacademy.neo4j.com/courses/graph-data-science-fundamentals/?ref=docs-nav)
* [Path Finding](https://graphacademy.neo4j.com/courses/gds-shortest-paths/?ref=docs-nav)

[Generative AI Courses](https://graphacademy.neo4j.com/categories/llms/?ref=docs-nav)

* [Neo4j & LLM Fundamentals](https://graphacademy.neo4j.com/courses/llm-fundamentals/?ref=docs-nav)
* [Vector Indexes & Unstructured Data](https://graphacademy.neo4j.com/courses/llm-vectors-unstructured/?ref=docs-nav)
* [Build a Chatbot with Python](https://graphacademy.neo4j.com/courses/llm-chatbot-python/?ref=docs-nav)
* [Build a Chatbot with TypeScript](https://graphacademy.neo4j.com/courses/llm-chatbot-typescript/?ref=docs-nav)

[Neo4j Certification](https://graphacademy.neo4j.com/certification/?ref=docs-nav)

* [Neo4j Certified Professional](https://graphacademy.neo4j.com/certifications/neo4j-certification/?ref=docs-nav)
* [Neo4j Graph Data Science Certification](https://graphacademy.neo4j.com/certifications/gds-certification/?ref=docs-nav)

[Get Started Free](https://console.neo4j.io/?ref=docs-nav-get-started)

[Search](#search)

[Skip to content](#skip-to-content "Skip to content")

Cypher Manual

Product Version

Version 25

Version 5

Version 4.4

* + [Introduction](../../introduction/)
    - [Overview](../../introduction/cypher-overview/)
    - [Cypher and Neo4j](../../introduction/cypher-neo4j/)
    - [Cypher and Aura](../../introduction/cypher-aura/)
  + [Queries](../../queries/)
    - [Core concepts](../../queries/concepts/)
    - [Basic queries](../../queries/basic/)
    - [Select Cypher version](../../queries/select-version/)
    - [Composed queries](../../queries/composed-queries/)
      * [Combined queries (`UNION`)](../../queries/composed-queries/combined-queries/)
      * [Conditional queries (`WHEN`)](../../queries/composed-queries/conditional-queries/)
      * [Sequential queries (`NEXT`)](../../queries/composed-queries/sequential-queries/)
  + [Clauses](../../clauses/)
    - [Clause composition](../../clauses/clause-composition/)
    - [CALL procedure](../../clauses/call/)
    - [CREATE](../../clauses/create/)
    - [DELETE](../../clauses/delete/)
    - [FILTER](../../clauses/filter/)
    - [FINISH](../../clauses/finish/)
    - [FOREACH](../../clauses/foreach/)
    - [LET](../../clauses/let/)
    - [LIMIT](../../clauses/limit/)
    - [LOAD CSV](../../clauses/load-csv/)
    - [MATCH](../../clauses/match/)
    - [MERGE](../../clauses/merge/)
    - [OPTIONAL MATCH](../../clauses/optional-match/)
    - [ORDER BY](../../clauses/order-by/)
    - [REMOVE](../../clauses/remove/)
    - [RETURN](../../clauses/return/)
    - [SEARCH](../../clauses/search/)
    - [SET](../../clauses/set/)
    - [SHOW FUNCTIONS](../../clauses/listing-functions/)
    - [SHOW PROCEDURES](../../clauses/listing-procedures/)
    - [SHOW SETTINGS](../../clauses/listing-settings/)
    - [SHOW TRANSACTIONS](../../clauses/transaction-clauses/#query-listing-transactions)
    - [SKIP](../../clauses/skip/)
    - [TERMINATE TRANSACTIONS](../../clauses/transaction-clauses/#query-terminate-transactions)
    - [UNWIND](../../clauses/unwind/)
    - [USE](../../clauses/use/)
    - [WHERE](../../clauses/where/)
    - [WITH](../../clauses/with/)
  + [Subqueries](../../subqueries/)
    - [CALL subqueries](../../subqueries/call-subquery/)
    - [CALL subqueries in transactions](../../subqueries/subqueries-in-transactions/)
    - [COLLECT subqueries](../../subqueries/collect/)
    - [COUNT subqueries](../../subqueries/count/)
    - [EXISTS subqueries](../../subqueries/existential/)
  + [Patterns](../../patterns/)
    - [Primer](../../patterns/primer/)
    - [Fixed-length patterns](../../patterns/fixed-length-patterns/)
    - [Variable-length patterns](../../patterns/variable-length-patterns/)
    - [Shortest paths](../../patterns/shortest-paths/)
    - [Non-linear patterns](../../patterns/non-linear-patterns/)
    - [Match modes](../../patterns/match-modes/)
    - [Path modes](../../patterns/path-modes/)
    - [Syntax and semantics](../../patterns/reference/)
  + [Values and types](../)
    - [Property, structural, and constructed values](../property-structural-constructed/)
    - [Boolean, numeric, and string literals](../boolean-numeric-string/)
    - [Temporal values](../temporal/)
    - [Spatial values](../spatial/)
    - [Lists](./)
    - [Maps](../maps/)
    - [Vectors](../vector/)
    - [Graph references](../graph-references/)
    - [Working with `null`](../working-with-null/)
    - [Casting data values](../casting-data/)
    - [Equality, ordering, and comparison of value types](../ordering-equality-comparison/)
  + [Expressions](../../expressions/)
    - [Predicates](../../expressions/predicates/)
      * [Boolean operators](../../expressions/predicates/boolean-operators/)
      * [Comparison operators](../../expressions/predicates/comparison-operators/)
      * [List operators](../../expressions/predicates/list-operators/)
      * [String operators](../../expressions/predicates/string-operators/)
      * [Label expression predicates](../../expressions/predicates/label-expression-predicates/)
      * [Path pattern expressions](../../expressions/predicates/path-pattern-expressions/)
      * [Type predicate expressions](../../expressions/predicates/type-predicate-expressions/)
    - [Node and relationship operators](../../expressions/node-relationship-operators/)
    - [Mathematical operators](../../expressions/mathematical-operators/)
    - [String concatenation operators](../../expressions/string-operators/)
    - [Temporal operators](../../expressions/temporal-operators/)
    - [List expressions](../../expressions/list-expressions/)
    - [Map expressions](../../expressions/map-expressions/)
    - [Conditional expressions (CASE)](../../expressions/conditional-expressions/)
  + [Functions](../../functions/)
    - [Aggregating functions](../../functions/aggregating/)
    - [Database functions](../../functions/database/)
    - [Graph functions](../../functions/graph/)
    - [List functions](../../functions/list/)
    - [LOAD CSV functions](../../functions/load-csv/)
    - Mathematical functions
      * [Logarithmic functions](../../functions/mathematical-logarithmic/)
      * [Numeric functions](../../functions/mathematical-numeric/)
      * [Trigonometric functions](../../functions/mathematical-trigonometric/)
    - [Predicate functions](../../functions/predicate/)
    - [Scalar functions](../../functions/scalar/)
    - [Spatial functions](../../functions/spatial/)
    - [String functions](../../functions/string/)
    - Temporal functions
      * [Duration functions](../../functions/temporal/duration/)
      * [Instant type functions](../../functions/temporal/)
      * [Format functions](../../functions/temporal/format/)
    - [User-defined functions](../../functions/user-defined/)
    - [Vector functions](../../functions/vector/)
  + [Indexes](../../indexes/)
    - [Search-performance indexes](../../indexes/search-performance-indexes/)
      * [Create indexes](../../indexes/search-performance-indexes/create-indexes/)
      * [Show indexes](../../indexes/search-performance-indexes/list-indexes/)
      * [Drop indexes](../../indexes/search-performance-indexes/drop-indexes/)
      * [The impact of indexes on query performance](../../indexes/search-performance-indexes/using-indexes/)
      * [Index hints for the Cypher planner](../../indexes/search-performance-indexes/index-hints/)
    - [Semantic indexes](../../indexes/semantic-indexes/)
      * [Full-text indexes](../../indexes/semantic-indexes/full-text-indexes/)
      * [Vector indexes](../../indexes/semantic-indexes/vector-indexes/)
    - [Syntax](../../indexes/syntax/)
  + [Schema](../../schema/)
    - [Graph types (Preview feature)](../../schema/graph-types/)
      * [Set graph types](../../schema/graph-types/set-graph-types/)
      * [Extend graph types](../../schema/graph-types/extend-graph-types/)
      * [Alter element types](../../schema/graph-types/alter-element-types/)
      * [Show graph types](../../schema/graph-types/list-graph-types/)
      * [Drop graph type elements](../../schema/graph-types/drop-graph-type-elements/)
    - [Constraints](../../schema/constraints/)
      * [Create constraints](../../schema/constraints/create-constraints/)
      * [Show constraints](../../schema/constraints/list-constraints/)
      * [Drop constraints](../../schema/constraints/drop-constraints/)
    - [Syntax](../../schema/syntax/)
  + [Execution plans and query tuning](../../planning-and-tuning/)
    - [Understanding execution plans](../../planning-and-tuning/execution-plans/)
    - [Operators](../../planning-and-tuning/operators/)
      * [Operators in detail](../../planning-and-tuning/operators/operators-detail/)
    - [Cypher runtimes](../../planning-and-tuning/runtimes/)
      * [Concepts](../../planning-and-tuning/runtimes/concepts/)
      * [Parallel runtime: reference](../../planning-and-tuning/runtimes/reference/)
    - [Query tuning](../../planning-and-tuning/query-tuning/)
  + [Query caches](../../query-caches/)
    - [Unifying query caches](../../query-caches/unified-query-caches/)
  + [Administration](../../administration/)
  + [Syntax](../../syntax/)
    - [Parsing](../../syntax/parsing/)
    - [Naming rules and recommendations](../../syntax/naming/)
    - [Variables](../../syntax/variables/)
    - [Keywords](../../syntax/keywords/)
    - [Parameters](../../syntax/parameters/)
    - [Comments](../../syntax/comments/)
  + [Additions, deprecations, removals, and compatibility](../../deprecations-additions-removals-compatibility/)
  + Appendix
    - [Cypher styleguide](../../styleguide/)
    - [GQL conformance](../../appendix/gql-conformance/)
      * [Supported mandatory GQL features](../../appendix/gql-conformance/supported-mandatory/)
      * [Currently unsupported mandatory GQL features](../../appendix/gql-conformance/unsupported-mandatory/)
      * [Supported optional GQL features](../../appendix/gql-conformance/supported-optional/)
      * [Optional GQL features and analogous Cypher](../../appendix/gql-conformance/analogous-cypher/)
      * [Additional Cypher features](../../appendix/gql-conformance/additional-cypher/)
    - [Tutorials and extended examples](../../appendix/tutorials/)
      * [Basic query tuning example](../../appendix/tutorials/basic-query-tuning/)
      * [Advanced query tuning example](../../appendix/tutorials/advanced-query-tuning/)

**Is this page helpful?**

* [Cypher Manual](../../introduction/)
* [Values and types](../)
* [Lists](./)

[Raise an issue](https://github.com/neo4j/docs-cypher/issues/new/?title=Docs%20Feedback%20modules/ROOT/pages/values-and-types/lists.adoc%20(ref:%20cypher-25)&body=%3E%20Do%20not%20include%20confidential%20information,%20personal%20data,%20sensitive%20data,%20or%20other%20regulated%20data.)

# Lists

Cypher® includes comprehensive support for lists.

|  |  |
| --- | --- |
|  | For information about the list predicate operator `IN`, which checks for list membership, see [Expressions → Predicates → List operators](../../expressions/predicates/list-operators/). For information list concatenation (`+` and `||`), list element access and slicing (`[]`), as well as list and pattern comprehensions, see [List expressions](../../expressions/list-expressions/). |

## Lists in general

A literal list is created by using brackets and separating the elements in the list with commas.

Query

```
RETURN [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] AS list
```

Result

| list |
| --- |
| `[0,1,2,3,4,5,6,7,8,9]` |
|  |
| --- |
| Rows: 1 |

A list can consist of different value types.

Query

```
RETURN [0, "hello", 3.14, null] AS list
```

Result

| list |
| --- |
| `[0, "hello", 3.14, null]` |
|  |
| --- |
| Rows: 1 |

|  |  |
| --- | --- |
|  | Lists containing [`VECTOR`](../vector/) values as nested entries cannot be stored as properties. |

Lists are indexed by 0 in Cypher.
To access individual elements in a list, use square brackets.
This extracts from the start index and up to, but not including, the end index.

For example:

Query

```
WITH [5,1,7] AS list
RETURN list[2]
```

Result

| list[2] |
| --- |
| `7` |
|  |
| --- |
| Rows: 1 |

## List range and size

The below examples use the [`range`](../../functions/list/#functions-range) function to create lists.
This function returns a list containing all numbers between given start and end numbers.
The range is inclusive in both ends.

Query

```
RETURN range(0, 10)[3] AS element
```

Result

| element |
| --- |
| `3` |
|  |
| --- |
| Rows: 1 |

It is also possible to use negative numbers, to start from the end of the list instead.

Query

```
RETURN range(0, 10)[-3] AS element
```

Result

| element |
| --- |
| `8` |
|  |
| --- |
| Rows: 1 |

Finally, it is possible to use ranges inside the brackets to return ranges of the list.
The list range operator (`[]`) is inclusive of the first value, but exclusive of the last value.

Query

```
RETURN range(0, 10)[0..3] AS list
```

Result

| list |
| --- |
| `[0,1,2]` |
|  |
| --- |
| Rows: 1 |

Query

```
RETURN range(0, 10)[0..-5] AS list
```

Result

| list |
| --- |
| `[0,1,2,3,4,5]` |
|  |
| --- |
| Rows: 1 |

Query

```
RETURN range(0, 10)[-5..] AS list
```

Result

| list |
| --- |
| `[6,7,8,9,10]` |
|  |
| --- |
| Rows: 1 |

Query

```
RETURN range(0, 10)[..4] AS list
```

Result

| list |
| --- |
| `[0,1,2,3]` |
|  |
| --- |
| Rows: 1 |

Out-of-bound slices are simply truncated, but out-of-bound single elements return `null`.

Query

```
RETURN range(0, 10)[15] AS list
```

Result

| list |
| --- |
| `<null>` |
|  |
| --- |
| Rows: 1 |

Query

```
RETURN range(0, 10)[5..15] AS list
```

Result

| list |
| --- |
| `[5,6,7,8,9,10]` |
|  |
| --- |
| Rows: 1 |

The [`size`](../../functions/scalar/#functions-size) of a list can be obtained as follows:

Query

```
RETURN size(range(0, 10)[0..3]) AS list
```

Result

| list |
| --- |
| `3` |
|  |
| --- |
| Rows: 1 |

## Storing lists as properties

It is possible to store homogenous lists of simple values as properties.

Allowed - store homogenous list as a property

```
CREATE (n:Label)
SET n.listProperty = [1, 2, 3]
RETURN n.listProperty AS homogenousListProperty
```

Result

| homogenousListProperty |
| --- |
| `[1, 2, 3]` |
|  |
| --- |
| Rows: 1 |

It is not, however, possible to store heterogeneous lists as properties.

Not allowed - store heterogenous list as a property

```
CREATE (n:Label)
SET n.listProperty = [1, "hello", .45, date()]
RETURN n.listProperty AS heterogenousListProperty
```

GQLSTATUS error chain

|  |
| --- |
| [22N39](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22N39/): error: data exception - unsupported property value type. Value String("hello") cannot be stored in properties.  [22G03](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22G03/): error: data exception - invalid value type |

[Spatial values](../spatial/)
[Maps](../maps/)

[## Cypher Aggregations

Learn how to aggregate data in Cypher with hands-on courses from Neo4j GraphAcademy

Enroll now](https://graphacademy.neo4j.com/courses/cypher-aggregation/?ref=docs-ad-cypher-aggregations)

## Learn

* [Sandbox](https://neo4j.com/sandbox/?ref=developer-footer)
* [Neo4j Community Site](https://community.neo4j.com?ref=developer-footer)
* [Neo4j Developer Blog](https://medium.com/neo4j)
* [Neo4j Videos](https://www.youtube.com/neo4j)
* [GraphAcademy](https://neo4j.com/graphacademy/?ref=developer-footer)
* [Neo4j Labs](https://neo4j.com/labs/?ref=developer-footer)

## Social

* [Twitter](https://twitter.com/neo4j)
* [Meetups](https://www.meetup.com/Neo4j-Online-Meetup/)
* [Github](https://github.com/neo4j/neo4j)
* [Stack Overflow](https://stackoverflow.com/questions/tagged/neo4j)
* [Want to Speak?](https://docs.google.com/forms/d/e/1FAIpQLSdEcNnMruES5iwvOVYovmS1D_P1ZL_HdUOitFrwrvruv5PZvA/viewform)

## [Contact Us →](https://neo4j.com/contact-us/?ref=footer)

* US: 1-855-636-4532
* Sweden +46 171 480 113
* UK: +44 20 3868 3223
* France: +33 (0) 1 88 46 13 20

© 2026 Neo4j, Inc.  
[Terms](https://neo4j.com/terms/) | [Privacy](https://neo4j.com/privacy-policy/)  | [Sitemap](https://neo4j.com/sitemap/)

Neo4j®, Neo Technology®, Cypher®, Neo4j® Bloom™ and
Neo4j® Aura™ are registered trademarks
of Neo4j, Inc. All other marks are owned by their respective companies.

window.algoliaSearchOptions = {indexName: "docs",placeholder: "Search Documentation",template: "docs"}