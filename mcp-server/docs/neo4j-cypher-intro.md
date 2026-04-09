(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-WK23PSS');
What is Cypher - Getting Started

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

Getting Started

* + **Get started**
  + [Introduction](../)
  + [What is Neo4j](../whats-neo4j/)
  + [What is a graph database](../graph-database/)
    - [Graph database concepts](../appendix/graphdb-concepts/)
      * [Comparing relational to graph database](../appendix/graphdb-concepts/graphdb-vs-rdbms/)
      * [Transition from NoSQL to graph database](../appendix/graphdb-concepts/graphdb-vs-nosql/)
  + [What is Cypher®](./)
    - [Get started with Cypher®](intro-tutorial/)
    - [Comparing Cypher with SQL](cypher-sql/)
    - [Defining a schema](schema/)
    - [Updating the graph](updating/)
    - [Subqueries in Cypher](subqueries/)
    - [Dates, datetimes, and durations](dates-datetimes-durations/)
    - [Refining results](results/)
    - [How to extend Cypher](procedures-functions/)
    - [Cypher resources](resources/)
  + **Work with data**
  + [Model data](../data-modeling/)
    - [Create a data model](../data-modeling/tutorial-data-modeling/)
    - [Refactor your model](../data-modeling/tutorial-refactoring/)
    - [Modeling designs](../data-modeling/modeling-designs/)
    - [Versioning](../data-modeling/versioning/)
    - [Modeling: relational to graph](../data-modeling/relational-to-graph-modeling/)
    - [Graph modeling tips](../data-modeling/modeling-tips/)
    - [Data modeling tools](../data-modeling/data-modeling-tools/)
  + [Import data into Neo4j](../data-import/)
    - [Working with CSV files](../data-import/csv-files/)
    - [Using `LOAD CSV`](../data-import/csv-import/)
    - [Importing JSON data from a REST API into Neo4j](../data-import/json-rest-api-import/)
    - [Import: RDBMS to graph](../data-import/relational-to-graph-import/)
  + [Create an application](../languages-guides/)
    - [Using Neo4j from Java](../languages-guides/java/java-intro/)
      * [Spring Data Neo4j](../languages-guides/java/spring-data-neo4j/)
      * [Quarkus](../languages-guides/java/quarkus/)
      * [Helidon, Micronaut](../languages-guides/java/java-frameworks/)
      * [Procedures and Functions](../languages-guides/java/java-procedures/)
    - [Using Neo4j from .NET](/docs/dotnet-manual)
    - [Using Neo4j from JavaScript](/docs/javascript-manual)
    - [Using Neo4j from Python](/docs/python-manual)
    - [Using Neo4j from Go](/docs/go-manual)
    - [Neo4j OGM](/docs/ogm)
    - [Community-contributed libraries](../languages-guides/community-drivers/)
  + [Connect data sources](/docs/connectors)
  + [Get insights from data](../gds/)
  + [Create data visualizations](../graph-visualization/graph-visualization/)
    - [Graph visualization tools](../graph-visualization/graph-visualization-tools/)
  + **Reference**
  + [Example datasets](../appendix/example-data/)
  + [Tutorials](../appendix/tutorials/tutorials-overview/)
    - [Cypher® recommendation engine](../appendix/tutorials/guide-build-a-recommendation-engine/)
    - [Import data from a relational database into Neo4j](../data-import/import-relational-and-etl/)
  + [Resources](../appendix/getting-started-resources/)

**Is this page helpful?**

* [Getting Started](../)
* [What is Cypher®](./)

[Raise an issue](https://github.com/neo4j/docs-getting-started/issues/new/?title=Docs%20Feedback%20modules/ROOT/pages/cypher/index.adoc%20(ref:%20main)&body=%3E%20Do%20not%20include%20confidential%20information,%20personal%20data,%20sensitive%20data,%20or%20other%20regulated%20data.)

# What is Cypher

|  |  |
| --- | --- |
|  | This page covers the basics of Cypher®. For the complete documentation, refer to the [Cypher® Manual](/docs/cypher/). |

Figure 1. A visual representation of a Cypher query

Cypher® is Neo4j’s declarative and [GQL conformant](https://neo4j.com/docs/cypher-manual/current/appendix/gql-conformance/) query language.
Available as open source via [The openCypher project](http://openCypher®.org), Cypher is [similar to SQL](/docs/cypher-manual/current/introduction/cypher-overview/#_cypher_and_sql_key_differences), but optimized for graphs.

Intuitive and close to natural language, Cypher® provides a visual way of matching patterns and relationships by having its own design based on ASCII-art type of syntax:

```
(:nodes)-[:ARE_CONNECTED_TO]->(:otherNodes)
```

Round brackets are used to represent `(:Nodes)`, and square brackets `-[]→` to represent a relationship between the `(:Nodes)`.
With this query syntax, you can perform create, read, update, or delete (CRUD) operations on your graph.

|  |  |
| --- | --- |
|  | To try querying with Cypher®, get a free [Aura instance](https://neo4j.com/cloud/platform/aura-graph-database/), no installation required. Use the graduation cap icon on the top right section to access the interactive guides. The "Query fundamentals" gives you a hands-on introduction to Cypher®. |

## How does Cypher work?

The graph is composed of [nodes](#nodes) and [relationships](#relationships), which may also have assigned [properties](#properties).
With nodes and relationships, you can build a graph that can express both simple and complex patterns.

Pattern recognition is a key fundamental cognitive process.
With Cypher®, you can use pattern matching, which in turn makes the learning process more intuitive.

## Cypher syntax

Cypher®'s constructs are close to natural language and the syntax is designed to visually look like a graph.

Figure 2. A graph example involving four nodes and three relationships.

If you want to represent the data in this graph in English, it would read as something like: *"Sally likes Graphs. Sally is friends with John. Sally works for Neo4j."*

Now, if you were to write this same information in Cypher®, then it would look like this:

```
(:Sally)-[:LIKES]->(:Graphs)
(:Sally)-[:IS_FRIENDS_WITH]->(:John)
(:Sally)-[:WORKS_FOR]->(:Neo4j)
```

With this query, you turn the information into nodes and relationships, which are the core elements of Cypher®.

### Nodes

The main components in a graph are nodes and relationships.
Nodes are often used to represent nouns or objects in your data model.
In the previous example, `Sally`, `John`, `Graphs`, and `Neo4j` are the nodes:

Figure 3. A visual representation of nodes.

As mentioned previously, nodes are represented as round brackets `(node)` in Cypher®.
The parentheses are a representation of the circles that compose the nodes in the visualization.

#### Node labels

Nodes can be grouped together through a [label](#label), which works like a tag and allows you to specify certain types of entities in your queries.
Labels help Cypher® distinguish between nodes and optimize execution.

In the example, both `Sally` and `John` are persons, so they get a `Person` label, `Graphs` gets a `Technology` label, and `Neo4j` is a `Company`:

Figure 4. Nodes grouped by labels. Note that `Sally`, `John`, `Graphs`, and `Neo4j` are now [properties](#cypher-properties) instead.

In a relational database context, this would be the same as using SQL to refer to a particular row in a table.
The same way you can use SQL to query a person’s information from a `Person` table, you can also use the `Person` label for that information in Cypher®.

|  |  |
| --- | --- |
|  | If you do not specify a label for Cypher® to filter out non-matching node categories, the query will check all of the nodes in the database. This can affect performance in very large graphs. |

#### Node variables

If part of your query matches nodes that you need to reference in a later part of your query (i.e. in a [subclause](https://neo4j.com/docs/cypher-manual/current/clauses/#reading-sub-clauses)), you can use **node variables**.

Variables can be single letters or words, and should be written in lower-case.
For example, if you want to bind all nodes labeled `Person` to the variable `p`, you write `(p:Person)`.
If you want to use a full word as a variable, `(person:Person)` works exactly the same.

Retrieve all Person nodes

```
MATCH (p:Person)
RETURN p
```

### Relationships

In a graph database, both nodes and relationships are first-class citizens and they have equal value.
In a relational database, relationships are only implied via foreign keys and join tables.

In Cypher®, relationships are represented as square brackets with an optional arrow to indicate the direction (e.g. `(Node1)-[]→(Node2)`).

In the example, the arrows connecting the nodes represent the relationship between the nodes:

Figure 5. Graph featuring nodes and relationships.

#### Relationship directions

Relationships **always** have a direction which is indicated by an arrow.

They can go from left to right:

```
(p:Person)-[:LIKES]->(t:Technology)
```

From right to left:

```
(p:Person)<-[:LIKES]-(t:Technology)
```

Or be undirected (where the direction is **not** specified):

```
MATCH (p:Person)-[:LIKES]-(t:Technology)
```

#### Undirected relationships

An undirected relationship does not mean that it doesn’t have a direction, but that it can be traversed in **either** direction.
While you can’t **create** relationships without a direction, you can **query** them undirected (in the example, using the [`MATCH`](/docs/cypher-manual/current/clauses/match/) clause).

Since Cypher® won’t return anything if you write a query with the wrong direction, you can use undirected relationships in queries when you don’t know the direction.
This way, Cypher® will retrieve **all** nodes connected by the specified relationship type, regardless of direction.

|  |  |
| --- | --- |
|  | Because undirected relationships in queries are traversed twice (once for each direction), the same pattern will be returned twice. This may impact the performance of the query. |

#### Relationship types

Relationship types categorize and add meaning to a relationship, similar to how labels group nodes together.
It is considered best practice to use verbs or derivatives for the relationship type.
The type describes how the nodes relate to each other.
This way, Cypher® is almost like natural language, where nodes are the subjects and objects (nouns), and the relationships (verbs) are the predicates that relate them.

In the previous example, the relationship types are:

* `[:LIKES]` - communicates that Sally (a node) *likes* graphs (another node).
* `[:IS_FRIENDS_WITH]` - communicates that Sally *is friends with* John.
* `[:WORKS_FOR]` - communicates that Sally *works for* Neo4j.

|  |  |
| --- | --- |
|  | Remember to always put a colon in front of a relationship type. If you write `(Person)-[LIKES]→(Technology)`, `[LIKES]` will represent a relationship **variable**, not a relationship **type**. In this case, since no relationship type is declared, Cypher®'s `RETURN` clause will search for all types of relationships in order to retrieve a result to your query. |

#### Relationship variables

Variables can be used for relationships in the same way as for nodes.
Once you specify a variable, you can use it later in the query to reference the relationship.

Take this example:

```
MATCH (p:Person)-[r:LIKES]->(t:Technology)
RETURN p,r,t
```

This query specifies variables for both the node labels (`p` for `Person` and `t` for `Technology`) and the relationship type (`r` for `:LIKES`).
In the return clause, you can then use the variables (i.e. `p`, `r`, and `t`) to return the bound entities.

This would be your result:

Figure 6. Result for the example query using node and relationship variables.

Table 1. Result

| p | r | t |
| --- | --- | --- |
| `(:Person)` | `[:LIKES]` | `(:Technology)` |
|  |  |  |
| --- | --- | --- |
| Rows: 1 | | |

### Properties

Properties are used to store additional information and can be added both to nodes and relationships and be of a variety of data types.
For a full list of values and types, see [Cypher® manual → Values and types](/docs/cypher-manual/current/values-and-types/).

In the following example, `sally` and `john` are [variables](##_node_variables) for `Person` nodes which contain a `name` property with the **property values** "Sally" and "John":

Figure 7. Graph example with node and relationship properties.

To add this info to the graph, you can use the following query:

```
CREATE (sally:Person {name:'Sally'})-[r:IS_FRIENDS_WITH]->(john:Person {name:'John'})
RETURN sally, r, john
```

Properties are enclosed by curly brackets (`{}`), the key is followed by a colon, and the value is enclosed by single or double quotation marks.

In case you have already added Sally and John as node labels, but want to change them into node properties, you need to refactor your graph.
Refactoring is a strategy in [data modeling](/docs/model) that you can learn more about in [this tutorial](/docs/getting-started/data-modeling/graph-model-refactoring/).

### Patterns in Cypher

Graph pattern matching sits at the very core of Cypher®.
It is the mechanism used to navigate, describe, and extract data from a graph by applying a declarative pattern.

Consider this example:

```
(sally:Person {name:'Sally'})-[l:LIKES]->(g:Technology {type: "Graphs"})
```

This bit of Cypher® represents a pattern.
It expresses that a `Person` node with *Sally* as its `name` property has a `LIKES` relationship to the `Technology` node with *Graphs* as its `type` property.

You can use this pattern in different queries to the database by adding a keyword to make it a **clause**.

For example, you can add this information to the database with the [`CREATE`](/docs/cypher-manual/current/clauses/create/) clause:

```
CREATE (sally:Person {name: "Sally"})-[r:LIKES]->(t:Technology {type: "Graphs"})
```

And once this data is written to the database, you can retrieve it with this pattern:

```
MATCH (sally:Person {name: "Sally"})-[r:LIKES]->(t:Technology {type: "Graphs"})
RETURN sally,r,t
```

#### Pattern variables

In the same way as nodes and relationships, you can also use variables for patterns.
Considering the previous example, you can turn the whole pattern (`(Sally)-[:LIKES]→(Technology)`) into a variable (`p`):

```
MATCH p = (sally:Person {name: "Sally"})-[r:LIKES]->(t:Technology {type: "Graphs"})
RETURN p
```

For more information, refer to [Cypher® manual → Patterns → Syntax and Semantics](/docs/cypher-manual/current/patterns/reference/).

## Keep learning

If you want to learn more about writing Cypher® queries, you can take the tutorial on how to [Get started with Cypher](intro-tutorial/).
In the [Cypher® manual](/docs/cypher-manual), you can find more information on:

* How to write [basic queries](/docs/cypher-manual/current/queries/basic/) and what [clauses](/docs/cypher-manual/current/clauses/) you can use to read data from the database.
* How [patterns](/docs/cypher-manual/current/patterns/) work and how you can use them to navigate, describe and extract data from a graph.
* What [values and types](/docs/cypher-manual/current/values-and-types/), and [functions](/docs/cypher-manual/current/functions/) are available in Cypher®.

### From SQL to Cypher

In case you have a background in SQL and are new to graph databases, these are some resources for more information on the key differences and the transition to graphs:

* [Key differences between Cypher® and SQL](/docs/cypher-manual/current/introduction/cypher-overview/#_cypher_and_sql_key_differences)
* [Transition from relational to graph database](#appendix/graphdb-concepts/graphdb-vs-rdbms)
* [Reference: Comparing Cypher® with SQL](cypher-sql/)
* [How-to: Import from RDBMS into graph](../data-import/relational-to-graph-import/)
* [Tutorial: Import data from a relational database into Neo4j](../data-import/import-relational-and-etl/)
* [How-to: Model data from relational to graph](../data-modeling/relational-to-graph-modeling/)

### From NoSQL to Graphs

If you are familiar with NoSQL ("Not only SQL") system, you can also learn more on [how to make the transition](../appendix/graphdb-concepts/graphdb-vs-nosql/) to a graph database.

### GraphAcademy

With the [Cypher® Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/) course, you can learn Cypher in 60 minutes and practice using a sandbox.

### Other resources

For more suggestions on how to expand your knowledge about Cypher®, refer to [Resources](../appendix/getting-started-resources/).

## Glossary

label
:   Marks a node as a member of a named and indexed subset. A node may be assigned zero or more labels.

labels
:   A label marks a node as a member of a named and indexed subset. A node may be assigned zero or more labels.

node
:   A node represents an entity or discrete object in your graph data model. Nodes can be connected by relationships, hold data in properties, and are classified by labels.

nodes
:   A node represents an entity or discrete object in your graph data model. Nodes can be connected by relationships, hold data in properties, and are classified by labels.

relationship
:   A relationship represents a connection between nodes in your graph data model. Relationships connect a source node to a target node, hold data in properties, and are classified by type.

relationships
:   A relationship represents a connection between nodes in your graph data model. Relationships connect a source node to a target node, hold data in properties, and are classified by type.

property
:   Properties are key-value pairs that are used for storing data on nodes and relationships.

properties
:   Properties are key-value pairs that are used for storing data on nodes and relationships.

cluster
:   A Neo4j DBMS that spans multiple servers working together to increase fault tolerance and/or read scalability. Databases on a cluster may be configured to replicate across servers in the cluster thus achieving read scalability or high availability.

clusters
:   A Neo4j DBMS that spans multiple servers working together to increase fault tolerance and/or read scalability. Databases on a cluster may be configured to replicate across servers in the cluster thus achieving read scalability or high availability.

graph
:   A logical representation of a set of nodes where some pairs are connected by relationships.

graphs
:   A logical representation of a set of nodes where some pairs are connected by relationships.

schema
:   The prescribed property existence and datatypes for nodes and relationships.

schemas
:   The prescribed property existence and datatypes for nodes and relationships.

[[database schema]]database schema
:   The prescribed property existence and datatypes for nodes and relationships.

indexes
:   Data structure that improves read performance of a database. [Read more about supported categories of indexes](https://neo4j.com/docs/cypher-manual/current/indexes/).

indexed
:   Data structure that improves read performance of a database. [Read more about supported categories of indexes](https://neo4j.com/docs/cypher-manual/current/indexes/).

constraints
:   Constraints are sets of data modeling rules that ensure the data is consistent and reliable. [See what constraints are available in Cypher](https://neo4j.com/docs/cypher-manual/current/constraints/).

data model
:   A data model defines how information is organized in a database. A good data model will make querying and understanding your data easier. In Neo4j, the data models have a graph structure.

data models
:   A data model defines how information is organized in a database. A good data model will make querying and understanding your data easier. In Neo4j, the data models have a graph structure.

[Transition from NoSQL to graph database](../appendix/graphdb-concepts/graphdb-vs-nosql/)
[Get started with Cypher®](intro-tutorial/)

[## One Day of AI and Graphs on April 15, 2026

The Call for Papers is now open. Submit your talk by December 12, 2025

Submit your talk](https://sessionize.com/nodesai2026/)

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