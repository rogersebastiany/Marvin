(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-WK23PSS');
MERGE - Cypher Manual

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
  + [Clauses](../)
    - [Clause composition](../clause-composition/)
    - [CALL procedure](../call/)
    - [CREATE](../create/)
    - [DELETE](../delete/)
    - [FILTER](../filter/)
    - [FINISH](../finish/)
    - [FOREACH](../foreach/)
    - [LET](../let/)
    - [LIMIT](../limit/)
    - [LOAD CSV](../load-csv/)
    - [MATCH](../match/)
    - [MERGE](./)
    - [OPTIONAL MATCH](../optional-match/)
    - [ORDER BY](../order-by/)
    - [REMOVE](../remove/)
    - [RETURN](../return/)
    - [SEARCH](../search/)
    - [SET](../set/)
    - [SHOW FUNCTIONS](../listing-functions/)
    - [SHOW PROCEDURES](../listing-procedures/)
    - [SHOW SETTINGS](../listing-settings/)
    - [SHOW TRANSACTIONS](../transaction-clauses/#query-listing-transactions)
    - [SKIP](../skip/)
    - [TERMINATE TRANSACTIONS](../transaction-clauses/#query-terminate-transactions)
    - [UNWIND](../unwind/)
    - [USE](../use/)
    - [WHERE](../where/)
    - [WITH](../with/)
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
* [Clauses](../)
* [MERGE](./)

[Raise an issue](https://github.com/neo4j/docs-cypher/issues/new/?title=Docs%20Feedback%20modules/ROOT/pages/clauses/merge.adoc%20(ref:%20cypher-25)&body=%3E%20Do%20not%20include%20confidential%20information,%20personal%20data,%20sensitive%20data,%20or%20other%20regulated%20data.)

# MERGE

## Introduction

The `MERGE` clause either matches existing node patterns in the graph and binds them or, if not present, creates new data and binds that.
In this way, it acts as a combination of `MATCH` and `CREATE` that allows for specific actions depending on whether the specified data was matched or created.

For example, `MERGE` can be used to specify that a graph must contain a node with a `Person` label and a specific `name` property.
If there isn’t a node with the specific `name` property, a new node will be created with that `name` property.

|  |  |
| --- | --- |
|  | For performance reasons, creating a schema index on the label or property is highly recommended when using `MERGE`. See [Create indexes](../../indexes/search-performance-indexes/create-indexes/) for more information. |

When using `MERGE` on full patterns, the behavior is that either the whole pattern matches, or the whole pattern is created.
`MERGE` will not partially use existing patterns.
If partial matches are needed, this can be accomplished by splitting a pattern into multiple `MERGE` clauses.

|  |  |
| --- | --- |
|  | Under concurrent updates, `MERGE` only guarantees the existence of the `MERGE` pattern, but not uniqueness. To guarantee uniqueness of nodes with certain properties, a [property uniqueness constraint](../../schema/constraints/create-constraints/#create-property-uniqueness-constraints) should be used. See [Using property uniqueness constraints with `MERGE`](#query-merge-using-unique-constraints). |

Similar to `MATCH`, `MERGE` can match multiple occurrences of a pattern.
If there are multiple matches, they will all be passed on to later stages of the query.

The last part of a `MERGE` clause is the `ON CREATE` and/or `ON MATCH` operators.
These allow a query to express additional changes to the properties of a node or relationship, depending on whether the element was matched (`MATCH`) in the database or if it was created (`CREATE`).

## Example graph

The following graph is used for the examples below:

To recreate the graph, run the following query in an empty Neo4j database:

```
CREATE
  (charlie:Person {name: 'Charlie Sheen', bornIn: 'New York', chauffeurName: 'John Brown'}),
  (martin:Person {name: 'Martin Sheen', bornIn: 'Ohio', chauffeurName: 'Bob Brown'}),
  (michael:Person {name: 'Michael Douglas', bornIn: 'New Jersey', chauffeurName: 'John Brown'}),
  (oliver:Person {name: 'Oliver Stone', bornIn: 'New York', chauffeurName: 'Bill White'}),
  (rob:Person {name: 'Rob Reiner', bornIn: 'New York', chauffeurName: 'Ted Green'}),
  (wallStreet:Movie {title: 'Wall Street'}),
  (theAmericanPresident:Movie {title: 'The American President'}),
  (charlie)-[:ACTED_IN]->(wallStreet),
  (martin)-[:ACTED_IN]->(wallStreet),
  (michael)-[:ACTED_IN]->(wallStreet),
  (martin)-[:ACTED_IN]->(theAmericanPresident),
  (michael)-[:ACTED_IN]->(theAmericanPresident),
  (oliver)-[:DIRECTED]->(wallStreet),
  (rob)-[:DIRECTED]->(theAmericanPresident)
```

## Merge nodes

### Merge single node with a label

Merge a node with a specific label:

Query

```
MERGE (robert:Critic)
RETURN labels(robert)
```

A new node is created because there are no nodes labeled `Critic` in the database:

Result

| labels(robert) |
| --- |
| ["Critic"] |

### Merge single node with multiple labels

Multiple labels are separated by colons:

Query

```
MERGE (robert:Critic:Viewer)
RETURN labels(robert)
```

A new node is created because there are no nodes labeled both `Critic` and `Viewer` in the database:

Result

| labels(robert) |
| --- |
| ["Critic","Viewer"] |

Multiple labels can also be separated by an ampersand `&`, in the same manner as it is used in [label expressions](../../patterns/reference/#label-expressions).
Separation by colon `:` and ampersand `&` cannot be mixed in the same clause.

Query

```
MERGE (robert:Critic&Viewer)
RETURN labels(robert)
```

No new node is created because there was already a node labeled both `Critic` and `Viewer` in the database:

Result

| labels(robert) |
| --- |
| ["Critic","Viewer"] |

### Merge single node with properties

Merging a node with properties that differ from the properties on existing nodes in the graph will create a new node:

Query

```
MERGE (charlie {name: 'Charlie Sheen', age: 10})
RETURN charlie
```

A new node with the name `Charlie Sheen` is created since not all properties matched those set to the pre-existing `Charlie Sheen` node:

Result

| charlie |
| --- |
| `(:Person {"name":"Charlie Sheen", "age":10})` |

|  |  |  |
| --- | --- | --- |
|  | `MERGE` cannot be used for nodes with property values that are `null`. For example, the following query will throw an error:  Query  ``` MERGE (martin:Person {name: 'Martin Sheen', age: null}) RETURN martin ```   GQLSTATUS error chain    |  | | --- | | [22N31](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22N31/): error: data exception - invalid properties in merge pattern. The node property `age` in '(:Person {age: null})' is invalid. 'MERGE' cannot be used with a graph element property value that is null.  [22G03](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22G03/): error: data exception - invalid value type | |

### Merge single node specifying both label and property

Merging a single node with both label and property matching an existing node will not create a new node:

Query

```
MERGE (michael:Person {name: 'Michael Douglas'})
RETURN michael.name, michael.bornIn
```

`Michael Douglas` is matched and the `name` and `bornIn` properties are returned:

Result

| michael.name | michael.bornIn |
| --- | --- |
| `"Michael Douglas"` | `"New Jersey"` |

### Merge single node derived from an existing node property

It is possible to merge nodes using existing node properties:

Query

```
MATCH (person:Person)
MERGE (location:Location {name: person.bornIn})
RETURN person.name, person.bornIn, location
```

In the above query, three nodes labeled `Location` are created, each of which contains a `name` property with the value of `New York`, `Ohio`, and `New Jersey` respectively.
Note that even though the `MATCH` clause results in three bound nodes having the value `New York` for the `bornIn` property, only a single `New York` node (i.e. a `Location` node with a name of `New York`) is created.
As the `New York` node is not matched for the first bound node, it is created.
However, the newly-created `New York` node is matched and bound for the second and third bound nodes.

Result

| person.name | person.bornIn | location |
| --- | --- | --- |
| `"Charlie Sheen"` | `"New York"` | `{name:"New York"}` |
| `"Martin Sheen"` | `"Ohio"` | `{name:"Ohio"}` |
| `"Michael Douglas"` | `"New Jersey"` | `{name:"New Jersey"}` |
| `"Oliver Stone"` | `"New York"` | `{name:"New York"}` |
| `"Rob Reiner"` | `"New York"` | `{name:"New York"}` |

## Use `ON CREATE` and `ON MATCH`

### Merge with `ON CREATE`

Merge a node and set properties if the node needs to be created:

Query

```
MERGE (keanu:Person {name: 'Keanu Reeves', bornIn: 'Beirut', chauffeurName: 'Eric Brown'})
ON CREATE
  SET keanu.created = timestamp()
RETURN keanu.name, keanu.created
```

The query creates the `Person` node named `Keanu Reeves`, with a `bornIn` property set to `Beirut` and a `chauffeurName` property set to `Eric Brown`.
It also sets a timestamp for the `created` property.

Result

| keanu.name | keanu.created |
| --- | --- |
| `"Keanu Reeves"` | `1655200898563` |

### Merge with `ON MATCH`

Merging nodes and setting properties on found nodes:

Query

```
MERGE (person:Person)
ON MATCH
  SET person.found = true
RETURN person.name, person.found
```

The query finds all the `Person` nodes, sets a property on them, and returns them:

Result

| person.name | person.found |
| --- | --- |
| `"Charlie Sheen"` | `true` |
| `"Martin Sheen"` | `true` |
| `"Michael Douglas"` | `true` |
| `"Oliver Stone"` | `true` |
| `"Rob Reiner"` | `true` |
| `"Keanu Reeves"` | `true` |

### Merge with `ON CREATE` and `ON MATCH`

Query

```
MERGE (keanu:Person {name: 'Keanu Reeves'})
ON CREATE
  SET keanu.created = timestamp()
ON MATCH
  SET keanu.lastSeen = timestamp()
RETURN keanu.name, keanu.created, keanu.lastSeen
```

Because the `Person` node named `Keanu Reeves` already exists, this query does not create a new node.
Instead, it adds a timestamp on the `lastSeen` property.

Result

| keanu.name | keanu.created | keanu.lastSeen |
| --- | --- | --- |
| `"Keanu Reeves"` | `1655200902354` | `1674655352124` |

### Merge with `ON MATCH` setting multiple properties

If multiple properties should be set, separate them with commas:

Query

```
MERGE (person:Person)
ON MATCH
  SET
    person.found = true,
    person.lastAccessed = timestamp()
RETURN person.name, person.found, person.lastAccessed
```

Result

| person.name | person.found | person.lastAccessed |
| --- | --- | --- |
| `"Charlie Sheen"` | `true` | `1655200903558` |
| `"Martin Sheen"` | `true` | `1655200903558` |
| `"Michael Douglas"` | `true` | `1655200903558` |
| `"Oliver Stone"` | `true` | `1655200903558` |
| `"Rob Reiner"` | `true` | `1655200903558` |
| `"Keanu Reeves"` | `true` | `1655200903558` |

## Merge relationships

### Merge on a relationship

`MERGE` can be used to match or create a relationship:

Query

```
MATCH
  (charlie:Person {name: 'Charlie Sheen'}),
  (wallStreet:Movie {title: 'Wall Street'})
MERGE (charlie)-[r:ACTED_IN]->(wallStreet)
RETURN charlie.name, type(r), wallStreet.title
```

`Charlie Sheen` had already been marked as acting in `Wall Street`, so the existing relationship is found and returned.
Note that in order to match or create a relationship when using `MERGE`, at least one bound node must be specified, which is done via the `MATCH` clause in the above example.

Result

| charlie.name | type(r) | wallStreet.title |
| --- | --- | --- |
| `"Charlie Sheen"` | `"ACTED_IN"` | `"Wall Street"` |

|  |  |  |
| --- | --- | --- |
|  | `MERGE` cannot be used for relationships with property values that are `null`. For example, the following query will throw an error:  Query  ``` MERGE (martin:Person {name: 'Martin Sheen'})-[r:FATHER_OF {since: null}]->(charlie:Person {name: 'Charlie Sheen'}) RETURN type(r) ```   GQLSTATUS error chain    |  | | --- | | [22N31](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22N31/): error: data exception - invalid properties in merge pattern. The relationship property `since` in '(martin)-[:FATHER\_OF {since: null}]→(charlie)' is invalid. 'MERGE' cannot be used with a graph element property value that is null.  [22G03](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22G03/): error: data exception - invalid value type | |

|  |  |  |
| --- | --- | --- |
|  | Specifying a property of an entity (node or relationship) by referring to the property of another entity within the same `MERGE` clause is not allowed.  For example, referring to `charlie.bornIn` in the property definition of `oliver.bornIn` is not allowed.  Query  ``` MERGE (charlie:Person {name: 'Charlie Sheen', bornIn: 'New York'})-[:ACTED_IN]->(movie:Movie)<-[:DIRECTED]-(oliver:Person {name: 'Oliver Stone', bornIn: charlie.bornIn}) RETURN movie ```   GQLSTATUS error chain    |  | | --- | | [42I58](https://neo4j.com/docs/status-codes/current/errors/gql-errors/42I58/): error: syntax error or access rule violation - invalid entity reference. Entity, 'charlie', cannot be created and referenced in the same clause.  [42001](https://neo4j.com/docs/status-codes/current/errors/gql-errors/42001/): error: syntax error or access rule violation - invalid syntax | |

### Merge on multiple relationships

Query

```
MATCH
  (oliver:Person {name: 'Oliver Stone'}),
  (reiner:Person {name: 'Rob Reiner'})
MERGE (oliver)-[:DIRECTED]->(movie:Movie)<-[:DIRECTED]-(reiner)
RETURN movie
```

In the example graph, `Oliver Stone` and `Rob Reiner` have never worked together.
When trying to `MERGE` a `Movie` node between them, Neo4j will not use any of the existing `Movie` nodes already connected to either person.
Instead, a new `Movie` node is created.

Result

| movie |
| --- |
| `(:Movie)` |

### Merge on an undirected relationship

`MERGE` can also be used without specifying the direction of a relationship.
Cypher® will first try to match the relationship in both directions.
If the relationship does not exist in either direction, it will create one left to right.

Query

```
MATCH
  (charlie:Person {name: 'Charlie Sheen'}),
  (oliver:Person {name: 'Oliver Stone'})
MERGE (charlie)-[r:KNOWS]-(oliver)
RETURN r
```

As `Charlie Sheen` and `Oliver Stone` do not know each other in the example graph, this `MERGE` query will create a `KNOWS` relationship between them.
The direction of the created relationship is left to right.

Result

| r |
| --- |
| `[:KNOWS]` |

### Merge on a relationship between two existing nodes

`MERGE` can be used in conjunction with preceding `MATCH` and `MERGE` clauses to create a relationship between two bound nodes `m` and `n`, where `m` is returned by `MATCH` and `n` is created or matched by the earlier `MERGE`.

Query

```
MATCH (person:Person)
MERGE (location:Location {name: person.bornIn})
MERGE (person)-[r:BORN_IN]->(location)
RETURN person.name, person.bornIn, location
```

This builds on the example from [Merge single node derived from an existing node property](#merge-merge-single-node-derived-from-an-existing-node-property).
The second `MERGE` creates a `BORN_IN` relationship between each person and a location corresponding to the value of the person’s `bornIn` property.
`Charlie Sheen`, `Rob Reiner`, and `Oliver Stone` all have a `BORN_IN` relationship to the *same* `Location` node (`New York`).

Result

| person.name | person.bornIn | location |
| --- | --- | --- |
| `"Charlie Sheen"` | `"New York"` | `(:Location {name:"New York"})` |
| `"Martin Sheen"` | `"Ohio"` | `(:Location {name:"Ohio"})` |
| `"Michael Douglas"` | `"New Jersey"` | `(:Location {name:"New Jersey"})` |
| `"Oliver Stone"` | `"New York"` | `(:Location {name:"New York"})` |
| `"Rob Reiner"` | `"New York"` | `(:Location {name:"New York"})` |
| `"Keanu Reeves"` | `"Beirut"` | `(:Location {name:"Beirut"})` |

### Merge on a relationship between an existing node and a merged node derived from a node property

`MERGE` can be used to simultaneously create both a new node `n` and a relationship between a bound node `m` and `n`:

Query

```
MATCH (person:Person)
MERGE (person)-[r:HAS_CHAUFFEUR]->(chauffeur:Chauffeur {name: person.chauffeurName})
RETURN person.name, person.chauffeurName, chauffeur
```

As `MERGE` found no matches — in the example graph, there are no nodes labeled with `Chauffeur` and no `HAS_CHAUFFEUR` relationships — `MERGE` creates six nodes labeled with `Chauffeur`, each of which contains a `name` property whose value corresponds to each matched `Person` node’s `chauffeurName` property value.
`MERGE` also creates a `HAS_CHAUFFEUR` relationship between each `Person` node and the newly-created corresponding `Chauffeur` node.
As `'Charlie Sheen'` and `'Michael Douglas'` both have a chauffeur with the same name — `'John Brown'` — a new node is created in each case, resulting in *two* `Chauffeur` nodes having a `name` of `'John Brown'`, correctly denoting the fact that even though the `name` property may be identical, these are two separate people.
This is in contrast to the example shown above in [Merge on a relationship between two existing nodes](#merge-merge-on-a-relationship-between-two-existing-nodes), where the first `MERGE` was used to bind the `Location` nodes and to prevent them from being recreated (and thus duplicated) on the second `MERGE`.

Result

| person.name | person.chauffeurName | chauffeur |
| --- | --- | --- |
| `"Charlie Sheen"` | `"John Brown"` | `(:Person {name:"John Brown"})` |
| `"Martin Sheen"` | `"Bob Brown"` | `(:Person {name:"Bob Brown"})` |
| `"Michael Douglas"` | `"John Brown"` | `(:Person {name:"John Brown"})` |
| `"Oliver Stone"` | `"Bill White"` | `(:Person {name:"Bill White"})` |
| `"Rob Reiner"` | `"Ted Green"` | `(:Person {name:"Ted Green"})` |
| `"Keanu Reeves"` | `"Eric Brown"` | `(:Person {name:"Eric Brown"})` |

## Using node property uniqueness constraints with `MERGE`

Cypher prevents getting conflicting results from `MERGE` when using patterns that involve [property uniqueness constraints](../../schema/constraints/create-constraints/#create-property-uniqueness-constraints).
In this case, there must be at most one node that matches that pattern.

For example, given two property node uniqueness constraints on `:Person(id)` and `:Person(ssn)`, a query such as `MERGE (n:Person {id: 12, ssn: 437})` will fail, if there are two different nodes (one with `id` 12 and one with `ssn` 437), or if there is only one node with only one of the properties.
In other words, there must be exactly one node that matches the pattern, or no matching nodes.

Note that the following examples assume the existence of property uniqueness constraints that have been created using:

```
CREATE CONSTRAINT FOR (n:Person) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:Person) REQUIRE n.role IS UNIQUE;
```

### Merge node using property uniqueness constraints creates a new node if no node is found

Given the node property uniqueness constraint on the `name` property for all `Person` nodes, the below query will create a new `Person` with the `name` property `Laurence Fishburne`.
If a `Laurence Fishburne` node had already existed, `MERGE` would match the existing node instead.

Query

```
MERGE (laurence:Person {name: 'Laurence Fishburne'})
RETURN laurence.name
```

Result

| laurence.name |
| --- |
| `"Laurence Fishburne"` |

### Merge using node property uniqueness constraints matches an existing node

Given property uniqueness constraint on the `name` property for all `Person` nodes, the below query will match the pre-existing `Person` node with the `name` property `Oliver Stone`.

Query

```
MERGE (oliver:Person {name: 'Oliver Stone'})
RETURN oliver.name, oliver.bornIn
```

Result

| oliver.name | oliver.bornIn |
| --- | --- |
| `"Oliver Stone"` | `"New York"` |

### Merge with property uniqueness constraints and partial matches

Merge using property uniqueness constraints fails when finding partial matches:

Query

```
MERGE (michael:Person {name: 'Michael Douglas', role: 'Gordon Gekko'})
RETURN michael
```

While there is a matching unique `Person` node with the name `Michael Douglas`, there is no unique node with the role of `Gordon Gekko` and `MERGE`, therefore, fails to match.

GQLSTATUS error chain

|  |
| --- |
| [22N41](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22N41/): error: data exception - merge node uniqueness constraint violation. The 'MERGE' clause did not find a matching node `michael` and cannot create a new node due to conflicts with existing uniqueness constraints.  [22G03](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22G03/): error: data exception - invalid value type |

To set the `role` of `Gordon Gekko` to `Michael Douglas`, use the `SET` clause instead:

Query

```
MERGE (michael:Person {name: 'Michael Douglas'})
SET michael.role = 'Gordon Gekko'
```

Result

```
Set 1 property
```

### Merge with property uniqueness constraints and conflicting matches

Merge using property uniqueness constraints fails when finding conflicting matches:

Query

```
MERGE (oliver:Person {name: 'Oliver Stone', role: 'Gordon Gekko'})
RETURN oliver
```

While there is a matching unique `Person` node with the name `Oliver Stone`, there is also another unique `Person` node with the role of `Gordon Gekko` and `MERGE` fails to match.

GQLSTATUS error chain

|  |
| --- |
| [22N41](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22N41/): error: data exception - merge node uniqueness constraint violation. The 'MERGE' clause did not find a matching node `oliver` and cannot create a new node due to conflicts with existing uniqueness constraints.  [22G03](https://neo4j.com/docs/status-codes/current/errors/gql-errors/22G03/): error: data exception - invalid value type |

## Using relationship property uniqueness constraints with `MERGE`

All that has been said above about node uniqueness constraints also applies to relationship uniqueness constraints.
However, for relationship uniqueness constraints there are some additional things to consider.

For example, if there exists a relationship uniqueness constraint on `()-[:ACTED_IN(year)]-()`, then the following query, in which not all nodes of the pattern are bound, would fail:

Query

```
MERGE (charlie:Person {name: 'Charlie Sheen'})-[r:ACTED_IN {year: 1987}]->(wallStreet:Movie {title: 'Wall Street'})
RETURN charlie.name, type(r), wallStreet.title
```

This is due to the all-or-nothing semantics of `MERGE`, which causes the query to fail if there exists a relationship with the given `year` property but there is no match for the full pattern.
In this example, since no match was found for the pattern, `MERGE` will try to create the full pattern including a relationship with `{year: 1987}`, which will lead to constraint violation error.

Therefore, it is advised - especially when relationship uniqueness constraints exist - to always use bound nodes in the `MERGE` pattern.
The following would, therefore, be a more appropriate composition of the query:

Query

```
MATCH
  (charlie:Person {name: 'Charlie Sheen'}),
  (wallStreet:Movie {title: 'Wall Street'})
MERGE (charlie)-[r:ACTED_IN {year: 1987}]->(wallStreet)
RETURN charlie.name, type(r), wallStreet.title
```

### Using map parameters with `MERGE`

`MERGE` does not support map parameters the same way that `CREATE` does.
To use map parameters with `MERGE`, it is necessary to explicitly use the expected properties, such as in the following example.
For more information on parameters, see [Parameters](../../syntax/parameters/).

Parameters

```
{
  "param": {
    "name": "Keanu Reeves",
    "bornIn": "Beirut",
    "chauffeurName": "Eric Brown"
  }
}
```

Query

```
MERGE (person:Person {name: $param.name, bornIn: $param.bornIn, chauffeurName: $param.chauffeurName})
RETURN person.name, person.bornIn, person.chauffeurName
```

Result

| person.name | person.bornIn | person.chauffeurName |
| --- | --- | --- |
| `"Keanu Reeves"` | `"Beirut"` | `"Eric Brown"` |

## MERGE using dynamic node labels and relationship types

Node labels and relationship types can be referenced dynamically in expressions, parameters, and variables when merging nodes and relationships.
This allows for more flexible queries and mitigates the risk of Cypher injection.
(For more information about Cypher injection, see [Neo4j Knowledge Base → Protecting against Cypher injection](https://neo4j.com/developer/kb/protecting-against-cypher-injection/)).

Syntax for merging nodes and relationships dynamically

```
MERGE (n:$(<expr>))
MERGE ()-[r:$(<expr>)]->()
```

The expression must evaluate to a `STRING NOT NULL | LIST<STRING NOT NULL> NOT NULL` value.
Using a `LIST<STRING>` with more than one item when merging a relationship using dynamic relationship types will fail.
This is because a relationship can only have exactly one type.

Parameters

```
{
  "nodeLabels": ["Person", "Director"],
  "relType": "DIRECTED",
  "movies": ["Ladybird", "Little Women", "Barbie"]
}
```

Merge nodes and relationships using dynamic node labels and relationship types

```
MERGE (greta:$($nodeLabels) {name: 'Greta Gerwig'})
WITH greta
UNWIND $movies AS movieTitle
MERGE (greta)-[rel:$($relType)]->(m:Movie {title: movieTitle})
RETURN greta.name AS name, labels(greta) AS labels, type(rel) AS relType, collect(m.title) AS movies
```

Result

| name | labels | relType | movies |
| --- | --- | --- | --- |
| `"Greta Gerwig"` | `["Person", "Director"]` | `"DIRECTED"` | `["Ladybird", "Little Women", "Barbie"]` |
|  |  |  |  |
| --- | --- | --- | --- |
| Rows: 1 | | | |

### Performance caveats

`MERGE` queries that use dynamic values may not perform as well as those with static values.
Neo4j is actively working to improve the performance of these queries.
The table below outlines performance caveats for specific Neo4j versions.

Neo4j versions and performance caveats

| Neo4j versions | Performance caveat |
| --- | --- |
| 5.26 — 2025.07 | The [Cypher planner](../../planning-and-tuning/execution-plans/) is not able to leverage [indexes](../../indexes/search-performance-indexes/) with [index scans or seeks](../../planning-and-tuning/operators/operators-detail/#leaf-operators) and must instead utilize the [`AllNodesScan`](../../planning-and-tuning/operators/operators-detail/#query-plan-all-nodes-scan) operator, which reads all nodes from the node store and is therefore more costly. |
| 2025.08 — 2025.10 | The Cypher planner is able to leverage [token lookup indexes](../../indexes/search-performance-indexes/using-indexes/#token-lookup-indexes) when matching node labels and relationship types dynamically. This is enabled by the introduction of three new query plan operators: [`DynamicLabelNodeLookup`](../../planning-and-tuning/operators/operators-detail/#query-plan-dynamic-label-node-lookup), [`DynamicDirectedRelationshipTypeLookup`](../../planning-and-tuning/operators/operators-detail/#query-plan-dynamic-directed-relationship-type-lookup), and [`DynamicUndirectedRelationshipTypeLookup`](../../planning-and-tuning/operators/operators-detail/#query-plan-dynamic-undirected-relationship-type-lookup). It is not, however, able to use indexes on property values. For example, `MERGE (n:$(Label) {foo: bar})` will not use any indexes on `n.foo` but can use a `DynamicLabelNodeLookup` on `$(label)`. |
| 2025.11 — current | The Cypher planner is able to leverage indexes on property values, however:  * It only supports exact seeks on range indexes (no full text or spatial). * The index order cannot be leveraged, so the planner must insert separate ordering if required later on in the query. * Parallel runtime seeks and scans are single-threaded. |

[MATCH](../match/)
[OPTIONAL MATCH](../optional-match/)

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