(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-WK23PSS');
Predicate functions - Cypher Manual

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
  + [Values and types](../../values-and-types/)
    - [Property, structural, and constructed values](../../values-and-types/property-structural-constructed/)
    - [Boolean, numeric, and string literals](../../values-and-types/boolean-numeric-string/)
    - [Temporal values](../../values-and-types/temporal/)
    - [Spatial values](../../values-and-types/spatial/)
    - [Lists](../../values-and-types/lists/)
    - [Maps](../../values-and-types/maps/)
    - [Vectors](../../values-and-types/vector/)
    - [Graph references](../../values-and-types/graph-references/)
    - [Working with `null`](../../values-and-types/working-with-null/)
    - [Casting data values](../../values-and-types/casting-data/)
    - [Equality, ordering, and comparison of value types](../../values-and-types/ordering-equality-comparison/)
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
  + [Functions](../)
    - [Aggregating functions](../aggregating/)
    - [Database functions](../database/)
    - [Graph functions](../graph/)
    - [List functions](../list/)
    - [LOAD CSV functions](../load-csv/)
    - Mathematical functions
      * [Logarithmic functions](../mathematical-logarithmic/)
      * [Numeric functions](../mathematical-numeric/)
      * [Trigonometric functions](../mathematical-trigonometric/)
    - [Predicate functions](./)
    - [Scalar functions](../scalar/)
    - [Spatial functions](../spatial/)
    - [String functions](../string/)
    - Temporal functions
      * [Duration functions](../temporal/duration/)
      * [Instant type functions](../temporal/)
      * [Format functions](../temporal/format/)
    - [User-defined functions](../user-defined/)
    - [Vector functions](../vector/)
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
* [Functions](../)
* [Predicate functions](./)

[Raise an issue](https://github.com/neo4j/docs-cypher/issues/new/?title=Docs%20Feedback%20modules/ROOT/pages/functions/predicate.adoc%20(ref:%20cypher-25)&body=%3E%20Do%20not%20include%20confidential%20information,%20personal%20data,%20sensitive%20data,%20or%20other%20regulated%20data.)

# Predicate functions

## Introduction

Predicates are boolean functions that return `true` or `false` for a given set of non-`null` input.
They are most commonly used to filter out paths in the `WHERE` part of a query.

## Example graph

The following graph is used for the examples below:

To recreate it, run the following query against an empty Neo4j database:

```
CREATE
  (keanu:Person {name:'Keanu Reeves', age:58, nationality:'Canadian'}),
  (carrie:Person {name:'Carrie Anne Moss', age:55, nationality:'American'}),
  (liam:Person {name:'Liam Neeson', age:70, nationality:'Northern Irish'}),
  (guy:Person {name:'Guy Pearce', age:55, nationality:'Australian'}),
  (kathryn:Person {name:'Kathryn Bigelow', age:71, nationality:'American'}),
  (jessica:Person {name:'Jessica Chastain', age:45, address:''}),
  (theMatrix:Movie {title:'The Matrix'}),
  (keanu)-[:KNOWS {since: 1999}]->(carrie),
  (keanu)-[:KNOWS {since: 2005}]->(liam),
  (keanu)-[:KNOWS {since: 2010}]->(kathryn),
  (kathryn)-[:KNOWS {since: 2012}]->(jessica),
  (carrie)-[:KNOWS {since: 2008}]->(guy),
  (liam)-[:KNOWS {since: 2009}]->(guy),
  (keanu)-[:ACTED_IN]->(theMatrix),
  (carrie)-[:ACTED_IN]->(theMatrix)
```

## all()

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `all(variable IN list WHERE predicate)` | | |
| **Description** | Returns true if the predicate holds for all elements in the given `LIST<ANY>`. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `variable` | `ANY` | A variable that can be used within the `WHERE` clause. |
| `list` | `LIST<ANY>` | A predicate must hold for all elements in this list for the function to return `true`. |
| `predicate` | `ANY` | A predicate that is tested against all items in the given list. |
| **Returns** | `BOOLEAN` | | |

Considerations

|  |
| --- |
| `all()` differs from most Cypher® functions because it iterates over a list, evaluating an expression for each element, rather than returning a result from a single evaluation. |
| `null` is returned if the `list` is `null` or if the `predicate` evaluates to `null` for at least one element and does not evaluate to false for any other element. |
| `all()` returns `true` if `list` is empty because there are no elements to falsify the `predicate`. |

Example 1. all()

Find paths where all nodes meet a given property value

```
MATCH p = (a:Person {name: 'Keanu Reeves'})-[]-{2,}()
WHERE all(x IN nodes(p) WHERE x.age < 60)
RETURN [n IN nodes(p) | n.name] AS actorsList
```

All nodes in the returned paths have an `` age`property below `60 ``:

Result

| actorsList |
| --- |
| `["Keanu Reeves", "Carrie Anne Moss", "Guy Pearce"]` |
|  |
| --- |
| Rows: 2 |

`all()` on an empty `LIST`

```
WITH [] as emptyList
RETURN all(i in emptyList WHERE true) as allTrue, all(i in emptyList WHERE false) as allFalse
```

Result

| allTrue | allFalse |
| --- | --- |
| `TRUE` | `TRUE` |
|  |  |
| --- | --- |
| Rows: 1 | |

## allReduce() Cypher 25 onlyIntroduced in 2025.08

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `allReduce(accumulator = initial, stepVariable IN list | reductionFunction, predicate)` | | |
| **Description** | Returns true if, during the stepwise evaluation of a value across the elements in a given `LIST<ANY>`, the accumulated result satisfies a specified predicate at every step. If that list is a [group variable](../../patterns/variable-length-patterns/#group-variables) defined in a [quantified path pattern](../../patterns/variable-length-patterns/#quantified-path-patterns), its predicate is inlined where applicable. This inlining allows for early pruning of the search space by discarding paths as soon as the predicate is not satisfied. Note that `allReduce()` predicates are not inlined when used in a [shortest path pattern](../../patterns/shortest-paths/), and therefore do not benefit from this pruning. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `accumulator` | `ANY` | A variable that holds the result of the `reductionFunction` as the `list` is iterated. It is initialized with the value of `initial`. |
| `initial` | `ANY` | The value of the `accumulator` for the first evaluation of `reductionFunction`. |
| `stepVariable` | `ANY` | A variable that holds the value of each element of `list` during iteration. |
| `list` | `LIST<ANY>` | The list that is being iterated over. |
| `reductionFunction` | `ANY` | An expression whose return value becomes the next value of the `accumulator`. The return type must match the return type of `initial`. |
| `predicate` | `BOOLEAN` | A predicate that is evaluated for each iteration. It has access to both the `accumulator` and `stepVariable` variables. |
| **Returns** | `BOOLEAN` | | |

Considerations

|  |
| --- |
| `allReduce()` differs from most Cypher functions because it iterates over a list, evaluating an expression for each element, rather than returning a result from a single evaluation. |
| `allReduce()` combines the functionality of the [`all()`](#functions-all) and [`reduce()`](../list/#functions-reduce) functions. |
| If all evaluations of `predicate` are `true`, `allReduce()` will return `true`. |
| If any evaluations of `predicate` are `false`, `allReduce()` will return `false`. |
| `allReduce()` returns `true` if `list` is empty because there are no elements to falsify the `predicate`. |
| `null` is returned if the `list` is `null` or if the `predicate` evaluates to `null` for at least one element and does not evaluate to `false` for any other element. |

Example 2. allReduce()

The below query finds `KNOWS` paths with a length of `3` where the `accumulator` begins with first node’s `age` and the accumulated `age` values of all nodes in the path never exceeds `230`.
Paths that do not meet this requirement are excluded, such as the path with the sequence `["Keanu Reeves (58)", "Carrie Anne Moss (55)", "Guy Pearce (55)", "Liam Neeson (70)"]` which has an aggregated `age` value of `238`.

Find aggregated ages within a boundary

```
MATCH (s) (()-[:KNOWS]-(n)){3}
WHERE allReduce(
  acc = s.age,
  node IN n | acc + node.age,
  acc < 230
)
RETURN [i IN [s] + n | i.name || " (" + toString(i.age) || ")"] AS ageSequence,
      reduce(acc = 0, node IN [s] + n | acc + node.age) AS aggregatedAges
ORDER BY aggregatedAges
```

Result

| ageSequence | aggregatedAges |
| --- | --- |
| `["Carrie Anne Moss (55)", "Keanu Reeves (58)", "Kathryn Bigelow (71)", "Jessica Chastain (45)"]` | `229` |
| `["Jessica Chastain (45)", "Kathryn Bigelow (71)", "Keanu Reeves (58)", "Carrie Anne Moss (55)"]` | `229` |
|  |  |
| --- | --- |
| Rows: 2 | |

The next query uses `allReduce()` to compare neighboring relationships.
It finds `KNOWS` paths with a length of at least `3` where each relationship’s `since` value is greater than the previous one and above `2000`.

Find paths where a relationship property must be above a value and increase along a path

```
MATCH path = ()-[r:KNOWS]-{3,}()
WHERE allReduce(
  span = {},
  rel IN r | { previous: span.current, current: rel.since },
  (span.previous IS NULL OR span.previous < span.current) AND span.current > 2000
)
LET people = nodes(path)
RETURN [actor IN people | actor.name] AS connectedActors,
       [rel IN r | rel.since] AS sinceYears
ORDER BY sinceYears
```

Result

| connectedActors | sinceYears |
| --- | --- |
| `["Liam Neeson", "Keanu Reeves", "Kathryn Bigelow", "Jessica Chastain"]` | `[2005, 2010, 2012]` |
|  |  |
| --- | --- |
| Rows: 1 | |

## any()

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `any(variable IN list WHERE predicate)` | | |
| **Description** | Returns true if the predicate holds for at least one element in the given `LIST<ANY>`. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `variable` | `ANY` | A variable that can be used within the `WHERE` clause. |
| `list` | `LIST<ANY>` | A predicate must hold for all elements in this list for the function to return `true`. |
| `predicate` | `ANY` | A predicate that is tested against all items in the given list. |
| **Returns** | `BOOLEAN` | | |

Considerations

|  |
| --- |
| `any()` differs from most Cypher functions because it iterates over a list, evaluating an expression for each element, rather than returning a result from a single evaluation. |
| `null` is returned if the `list` is `null` or if the `predicate` evaluates to `null` for at least one element and does not evaluate to false for any other element. |
| `any()` returns `false` if `list` is empty because there are no elements to satisfy the `predicate`. |

Example 3. any()

Find paths where at least one relationship property is above a given threshold

```
MATCH p = (n:Person {name: 'Keanu Reeves'})-[:KNOWS]-{3}()
WHERE any(rel IN relationships(p) WHERE rel.since < 2000)
RETURN [person IN nodes(p) | person.name] AS connectedActors,
       [rel IN relationships(p) | rel.since] AS sinceYears
```

Result

| connectedActors | sinceYears |
| --- | --- |
| `["Keanu Reeves", "Carrie Anne Moss", "Guy Pearce", "Liam Neeson"]` | `[1999, 2008, 2009]` |
|  |  |
| --- | --- |
| Rows: 1 | |

`any()` on an empty `LIST`

```
WITH [] as emptyList
RETURN any(i IN emptyList WHERE true) as anyTrue, any(i IN emptyList WHERE false) as anyFalse
```

Result

| anyTrue | anyFalse |
| --- | --- |
| `false` | `false` |
|  |  |
| --- | --- |
| Rows: 1 | |

## exists()

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `exists(input)` | | |
| **Description** | Returns true if a match for the pattern exists in the graph. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `input` | `ANY` | A pattern to verify the existence of. |
| **Returns** | `BOOLEAN` | | |

Considerations

|  |
| --- |
| `null` is returned if `input` is `null`. |

|  |  |
| --- | --- |
|  | To check if a property is not `null` use the [`IS NOT NULL` predicate](../../expressions/predicates/comparison-operators/). |

Example 4. exists()

Query

```
MATCH (p:Person)
RETURN p.name AS name,
       exists((p)-[:ACTED_IN]->()) AS has_acted_in_rel
```

This query returns the `name` property of every `Person` node, along with a boolean (`true` or `false`) indicating if those nodes have an `ACTED_IN` relationship in the graph.

Result

| name | has\_acted\_in\_rel |
| --- | --- |
| `"Carrie Anne Moss"` | `true` |
| `"Keanu Reeves"` | `true` |
| `"Liam Neeson"` | `false` |
| `"Guy Pearce"` | `false` |
| `"Kathryn Bigelow"` | `false` |
| `"Jessica Chastain"` | `false` |
|  |  |
| --- | --- |
| Rows: 6 | |

|  |  |
| --- | --- |
|  | For information about the `EXISTS` subquery, which is more versatile than the `exists()` function, see [EXISTS subqueries](../../subqueries/existential/). |

## isEmpty()

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `isEmpty(input)` | | |
| **Description** | Checks whether a `STRING`, `MAP` or `LIST<ANY>` is empty. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `input` | `STRING | MAP | LIST<ANY>` | A value to be checked for emptiness. |
| **Returns** | `BOOLEAN` | | |

Example 5. isEmpty(list)

Query

```
MATCH (p:Person)
WHERE NOT isEmpty(p.nationality)
RETURN p.name, p.nationality
```

This query returns every `Person` node in the graph with a set `nationality` property value (i.e., all `Person` nodes except for `Jessica Chastain`):

Result

| p.name | p.nationality |
| --- | --- |
| `"Keanu Reeves"` | `"Canadian"` |
| `"Carrie Anne Moss"` | `"American"` |
| `"Liam Neeson"` | `"Northern Irish"` |
| `"Guy Pearce"` | `"Australian"` |
| `"Kathryn Bigelow"` | `"American"` |
|  |  |
| --- | --- |
| Rows: 5 | |

Example 6. isEmpty(map)

Query

```
MATCH (n)
WHERE isEmpty(properties(n))
RETURN n
```

Because the example graph contains no empty nodes, nothing is returned:

Result

```
(no changes, no records)
```

Example 7. isEmpty(string)

Query

```
MATCH (p:Person)
WHERE isEmpty(p.address)
RETURN p.name AS name
```

The `name` property of each node that has an empty `STRING` `address` property is returned:

Result

| name |
| --- |
| `"Jessica Chastain"` |
|  |
| --- |
| Rows: 1 |

|  |  |
| --- | --- |
|  | The function `isEmpty()`, like most other Cypher functions, returns `null` if `null` is passed in to the function. That means that a predicate `isEmpty(n.address)` will filter out all nodes where the `address` property is not set. Thus, `isEmpty()` is not suited to test for `null`-values. [`IS NULL` or `IS NOT NULL`](../../expressions/predicates/comparison-operators/) should be used for that purpose. |

## none()

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `none(variable IN list WHERE predicate)` | | |
| **Description** | Returns true if the predicate holds for no element in the given `LIST<ANY>`. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `variable` | `ANY` | A variable that can be used within the `WHERE` clause. |
| `list` | `LIST<ANY>` | A predicate must hold for all elements in this list for the function to return `true`. |
| `predicate` | `ANY` | A predicate that is tested against all items in the given list. |
| **Returns** | `BOOLEAN` | | |

Considerations

|  |
| --- |
| `none()` differs from most Cypher functions because it iterates over a list, evaluating an expression for each element, rather than returning a result from a single evaluation. |
| `null` is returned if the `list` is `null`, or if the `predicate` evaluates to `null` for at least one element and does not evaluate to `true` for any other element. |
| `none()` returns `true` if `list` is empty because there are no elements to violate the `predicate`. |

Example 8. none()

Find paths where no node exceeds a given property value

```
MATCH p = (n:Person {name: 'Keanu Reeves'})-[]-{2}()
WHERE none(x IN nodes(p) WHERE x.age > 60)
RETURN [x IN nodes(p) | x.name] AS connectedActors
```

No nodes in the returned paths have an `age` property with a greater value than `60`:

Result

| connectedActors |
| --- |
| `["Keanu Reeves", "Carrie Anne Moss", "Guy Pearce"]` |
|  |
| --- |
| Rows: 1 |

`none()` on an empty `LIST`

```
WITH [] as emptyList
RETURN none(i IN emptyList WHERE true) as noneTrue, none(i IN emptyList WHERE false) as noneFalse
```

Result

| noneTrue | noneFalse |
| --- | --- |
| `TRUE` | `TRUE` |
|  |  |
| --- | --- |
| Rows: 1 | |

## single()

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `single(variable IN list WHERE predicate)` | | |
| **Description** | Returns true if the predicate holds for exactly one of the elements in the given `LIST<ANY>`. | | |
| **Arguments** | **Name** | **Type** | **Description** |
| `variable` | `ANY` | A variable that can be used within the `WHERE` clause. |
| `list` | `LIST<ANY>` | A predicate must hold for all elements in this list for the function to return `true`. |
| `predicate` | `ANY` | A predicate that is tested against all items in the given list. |
| **Returns** | `BOOLEAN` | | |

Considerations

|  |
| --- |
| `single()` differs from most Cypher functions because it iterates over a list, evaluating an expression for each element, rather than returning a result from a single evaluation. |
| `null` is returned if the `list` is `null`, or if the `predicate` evaluates to `null` for at least one element and does not evaluate to `true` for any other element. |
| `single()` returns `false` if `list` is empty because there is not exactly one element satisfying the `predicate`. |

Example 9. single()

Find paths where exactly one node has a given property value

```
MATCH p = (n:Person {name: 'Keanu Reeves'})-[:KNOWS]-+(b)
WHERE single(x IN [b] WHERE x.nationality = 'Northern Irish')
RETURN [person IN nodes(p) | person.name + " (" + person.nationality + ")"] AS northernIrishPaths
ORDER BY length(p)
```

Result

| northernIrishPaths |
| --- |
| `["Keanu Reeves (Canadian)", "Liam Neeson (Northern Irish)"]` |
| `["Keanu Reeves (Canadian)", "Carrie Anne Moss (American)", "Guy Pearce (Australian)", "Liam Neeson (Northern Irish)"]` |
|  |
| --- |
| Rows: 2 |

`single()` on an empty `LIST`

```
WITH [] as emptyList
RETURN single(i IN emptyList WHERE true) as singleTrue, single(i IN emptyList WHERE false) as singleFalse
```

Result

| singleTrue | singleFalse |
| --- | --- |
| `false` | `false` |
|  |  |
| --- | --- |
| Rows: 1 | |

[Trigonometric functions](../mathematical-trigonometric/)
[Scalar functions](../scalar/)

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