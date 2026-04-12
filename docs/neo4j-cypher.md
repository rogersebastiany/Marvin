# Neo4j Cypher


---

## 1. 

Welcome to the Neo4j Cypher® Manual.

Cypher is Neo4j’s declarative query language, allowing users to unlock the full potential of property graph databases.

|  |  |
| --- | --- |
|  | This manual covers Cypher 25. As of Neo4j 2025.06, all new Cypher features are exclusively added to Cypher 25, while Cypher 5 is frozen. As of Neo4j 2026.02, new databases explicitly set Cypher 25 as their query language in their configuration file. For information about how to how to use Cypher 25, see [Select Cypher version](../queries/select-version/). For information about new features added to Cypher 25, see [Additions, deprecations, removals, and compatibility](../deprecations-additions-removals-compatibility/). |

The Cypher Manual aims to be as instructive as possible to readers from a variety of backgrounds and professions, such as developers, administrators, and academic researchers.

If you are new to Cypher and Neo4j, you can visit the [Getting Started Guide → Cypher](/docs/getting-started/cypher/) chapter.
Additionally, [Neo4j GraphAcademy](https://graphacademy.neo4j.com/) has a variety of free courses tailored for all levels of experience.

For a reference of all available Cypher features, see the [Cypher Cheat Sheet](/docs/cypher-cheat-sheet/25/all/).

For a downloadable PDF version of the Cypher Manual, visit the [Neo4j documentation archive](/docs/reference/docs-archive/#_cypher_query_language).

This introduction will cover the following topics:

* [Overview](cypher-overview/)
* [Cypher and Neo4j](cypher-neo4j/)
* [Cypher and Aura](cypher-aura/)

License: [Creative Commons 4.0](https://neo4j.com/docs/license/)

---

## 2. 

Search-performance indexes enable quicker retrieval of exact matches between an index and the primary data storage.
There are four different search-performance indexes available in Neo4j:

* [**Range indexes**](create-indexes/#create-range-index): Neo4j’s default index.
  Supports most types of predicates.
* [**Text indexes**](create-indexes/#create-text-index): solves predicates operating on `STRING` values.
  Optimized for queries filtering with the `STRING` operators `CONTAINS` and `ENDS WITH`.
* [**Point indexes**](create-indexes/#create-point-index): solves predicates on spatial `POINT` values.
  Optimized for queries filtering on distance or within bounding boxes.
* [**Token lookup indexes**](create-indexes/#create-lookup-index): only solves node label and relationship type predicates (i.e. they cannot solve any predicates filtering on properties).
  Two token lookup indexes (one for node labels and one for relationship types) are present when a database is created in Neo4j.

To learn more about creating, listing, and deleting these indexes, as well as more details about the predicates supported by each index type, see [Create indexes](create-indexes/), [Show indexes](list-indexes/) and [Drop indexes](drop-indexes/).

For information about how search-performance indexes are used in Cypher® queries, how they impact their performance, as well as some heuristics for when to use (and not to use) a search-performance index, see [The impact of indexes on query performance](using-indexes/).

Search-performance indexes are used automatically, and if several indexes are available, the [Cypher planner](../../planning-and-tuning/execution-plans/) tries to use the index (or indexes) that can most efficiently solve a particular predicate.
It is, however, possible to explicitly force a query to use a particular index with the `USING` keyword. For more information, see [Index hints for the Cypher planner](index-hints/).

---

## 3. 

The `MATCH` clause enables you to define specific patterns that the database will search for within its graph structure.
The `MATCH` clause can specify the nodes, relationships, and properties in a pattern, allowing for queries that traverse the graph to retrieve relevant data.

## Example graph

The following graph is used for the examples below:

To recreate the graph, run the following query against an empty Neo4j database:

```
CREATE (charlie:Person:Actor {name: 'Charlie Sheen'}),
       (martin:Person:Actor {name: 'Martin Sheen'}),
       (michael:Person:Actor {name: 'Michael Douglas'}),
       (oliver:Person:Director {name: 'Oliver Stone'}),
       (rob:Person:Director {name: 'Rob Reiner'}),
       (wallStreet:Movie {title: 'Wall Street'}),
       (charlie)-[:ACTED_IN {role: 'Bud Fox'}]->(wallStreet),
       (martin)-[:ACTED_IN {role: 'Carl Fox'}]->(wallStreet),
       (michael)-[:ACTED_IN {role: 'Gordon Gekko'}]->(wallStreet),
       (oliver)-[:DIRECTED]->(wallStreet),
       (thePresident:Movie {title: 'The American President'}),
       (martin)-[:ACTED_IN {role: 'A.J. MacInerney'}]->(thePresident),
       (michael)-[:ACTED_IN {role: 'President Andrew Shepherd'}]->(thePresident),
       (rob)-[:DIRECTED]->(thePresident)
```

## Find nodes

The `MATCH` clause allows you to specify node patterns of varying complexity to retrieve from a graph.
For more information about finding node patterns, see [Patterns → Node patterns](../../patterns/fixed-length-patterns/#node-patterns).

### Find all nodes

By specifying a pattern with a single node and no labels, all nodes in the graph will be returned.

Find all nodes in a graph

```
MATCH (n)
RETURN n
```

Result

| n |
| --- |
| `(:Person {"name":"Charlie Sheen"})` |
| `(:Person {"name":"Martin Sheen"})` |
| `(:Person {"name":"Michael Douglas"})` |
| `(:Person {"name":"Oliver Stone"})` |
| `(:Person {"name":"Rob Reiner"})` |
| `(:Movie {"title":"Wall Street"})` |
| `(:Movie {"title":"The American President"})` |
|  |
| --- |
| Rows: 7 |

### Find nodes with a specific label

Find all nodes with the `Movie` label

```
MATCH (movie:Movie)
RETURN movie.title
```

Result

| movie.title |
| --- |
| `"Wall Street"` |
| `"The American President"` |
|  |
| --- |
| Rows: 2 |

### MATCH using node label expressions

Node pattern using the `OR` (`|`) label expression

```
MATCH (n:Movie|Person)
RETURN n.name AS name, n.title AS title
```

Result

| name | title |
| --- | --- |
| `"Charlie Sheen"` | `<null>` |
| `"Martin Sheen"` | `<null>` |
| `"Michael Douglas"` | `<null>` |
| `"Oliver Stone"` | `<null>` |
| `"Rob Reiner"` | `<null>` |
| `<null>` | `"Wall Street"` |
| `<null>` | `"The American President"` |
|  |  |
| --- | --- |
| Rows: 7 | |

Node pattern using negation (`!`) label expression

```
MATCH (n:!Movie)
RETURN labels(n) AS label, count(n) AS labelCount
```

|  |  |
| --- | --- |
|  | The above query uses the [`labels()`](../../functions/list/#functions-labels) and [`count()`](../../functions/aggregating/#functions-count) functions. |

Result

| label | labelCount |
| --- | --- |
| `["Person", "Actor"]` | `3` |
| `["Person", "Director"]` | `2` |
|  |  |
| --- | --- |
| Rows: 2 | |

For a list of all label expressions supported by Cypher®, see [Patterns → Label expressions](../../patterns/reference/#label-expressions).

## Find relationships

The `MATCH` clause allows you to specify relationship patterns of varying complexity to retrieve from a graph.
Unlike a node pattern, a relationship pattern cannot be used in a `MATCH` clause without node patterns at both ends.
For more information about relationship patterns, see [Patterns → Relationship patterns](../../patterns/fixed-length-patterns/#relationship-patterns).

|  |  |
| --- | --- |
|  | Cypher default match mode, `DIFFERENT RELATIONSHIPS`, will only match a relationship once inside a single pattern. The same is not true for the `REPEATABLE ELEMENTS` match mode. For more information, see [Match modes](../../patterns/match-modes/) |

### Empty relationship patterns

By applying `--`, a pattern will be matched for a relationship with any direction and without any filtering on relationship types or properties.

Find connected nodes using an empty relationship pattern

```
MATCH (:Person {name: 'Oliver Stone'})--(n)
RETURN n AS connectedNodes
```

Result

| connectedNodes |
| --- |
| `(:Movie {title: "Wall Street"})` |
|  |
| --- |
| Rows: 1 |

### Directed relationship patterns

The direction of a relationship in a pattern is indicated by arrows: `-->` or `<--`.

Find all nodes connected to `Oliver Stone` by an outgoing relationship.

```
MATCH (:Person {name: 'Oliver Stone'})-->(movie:Movie)
RETURN movie.title AS movieTitle
```

Result

| movieTitle |
| --- |
| `"Wall Street"` |
|  |
| --- |
| Rows: 1 |

### Relationship variables

It is possible to introduce a variable to a pattern, either for filtering on relationship properties or to return a relationship.

Find the types of an aliased relationship

```
MATCH (:Person {name: 'Oliver Stone'})-[r]->()
RETURN type(r) AS relType
```

|  |  |
| --- | --- |
|  | The above query uses the [`type()` function](../../functions/scalar/#functions-type). |

Result

| relType |
| --- |
| `"DIRECTED"` |
|  |
| --- |
| Rows: 1 |

### MATCH on an undirected relationship

When a pattern contains a bound relationship, and that relationship pattern does not specify direction, Cypher will match the relationship in both directions.

Relationship pattern without direction

```
MATCH (a)-[:ACTED_IN {role: 'Bud Fox'}]-(b)
RETURN a, b
```

Result

| a | b |
| --- | --- |
| `(:Movie {"title":"Wall Street"})` | `(:Person {"name":"Charlie Sheen"})` |
| `(:Person {"name":"Charlie Sheen"})` | `(:Movie {"title":"Wall Street"})` |
|  |  |
| --- | --- |
| Rows: 2 | |

### Filter on relationship types

It is possible to specify the type of a relationship in a relationship pattern by using a colon (`:`) before the relationship type.

Relationship pattern filtering on the `ACTED_IN` relationship type

```
MATCH (:Movie {title: 'Wall Street'})<-[:ACTED_IN]-(actor:Person)
RETURN actor.name AS actor
```

Result

| actor |
| --- |
| `"Michael Douglas"` |
| `"Martin Sheen"` |
| `"Charlie Sheen"` |
|  |
| --- |
| Rows: 3 |

### MATCH using relationship type expressions

It is possible to match a pattern containing one of several relationship types using the `OR` symbol, `|`.

Relationship pattern including either `ACTED_IN` or `DIRECTED` relationship types

```
MATCH (:Movie {title: 'Wall Street'})<-[:ACTED_IN|DIRECTED]-(person:Person)
RETURN person.name AS person
```

Result

| person |
| --- |
| `"Oliver Stone"` |
| `"Michael Douglas"` |
| `"Martin Sheen"` |
| `"Charlie Sheen"` |
|  |
| --- |
| Rows: 4 |

As relationships can only have exactly one type each, `()-[:A&B]→()` will never match a relationship.

For a list of all relationship type expressions supported by Cypher, see [Patterns → Label expressions](../../patterns/reference/#label-expressions).

### Find multiple relationships

A graph pattern can contain several relationship patterns.

Graph pattern including several relationship patterns

```
MATCH (:Person {name: 'Charlie Sheen'})-[:ACTED_IN]->(movie:Movie)<-[:DIRECTED]-(director:Person)
RETURN movie.title AS movieTitle, director.name AS director
```

Result

| movieTitle | director |
| --- | --- |
| `"Wall Street"` | `"Oliver Stone"` |
|  |  |
| --- | --- |
| Rows: 1 | |

## MATCH with WHERE predicates

The `MATCH` clause is often paired with a `WHERE` sub-clause, which adds predicates to refine the patterns, making them more specific.
These predicates are part of the pattern itself, not just filters applied after matching.
Thus, always place the `WHERE` clause with its corresponding `MATCH` clause.

Simple `WHERE` predicate

```
MATCH (charlie:Person)-[:ACTED_IN]->(movie:Movie)
WHERE charlie.name = 'Charlie Sheen'
RETURN movie.title AS movieTitle
```

Result

| movieTitle |
| --- |
| `"Wall Street"` |
|  |
| --- |
| Rows: 1 |

More complex `WHERE` predicate

```
MATCH (martin:Person)-[:ACTED_IN]->(movie:Movie)
WHERE martin.name = 'Martin Sheen' AND NOT EXISTS {
    MATCH (movie)<-[:DIRECTED]-(director:Person {name: 'Oliver Stone'})
}
RETURN movie.title AS movieTitle
```

|  |  |
| --- | --- |
|  | The above query uses an [`EXISTS` subquery](../../subqueries/existential/). |

Result

| movieTitle |
| --- |
| `"The American President"` |
|  |
| --- |
| Rows: 1 |

For more information, see the [`WHERE`](../where/) page.

## MATCH with parameters

The `MATCH` clause can be used with parameters.

Parameters

```
{
  "movieTitle": "Wall Street",
  "actorRole": "Fox"
}
```

Find nodes using paramters

```
MATCH (:Movie {title: $movieTitle})<-[r:ACTED_IN]-(p:Person)
WHERE r.role CONTAINS $actorRole
RETURN p.name AS actor, r.role AS role
```

|  |  |
| --- | --- |
|  | The above query uses the [`CONTAINS` operator](../../expressions/predicates/string-operators/). |

Result

| actor | role |
| --- | --- |
| `"Charlie Sheen"` | `"Bud Fox"` |
| `"Martin Sheen"` | `"Carl Fox"` |
|  |  |
| --- | --- |
| Rows: 2 | |

For more information about how to set parameters, see [Syntax → Parameters](../../syntax/parameters/).

## Find paths

The `MATCH` clause can also be used to bind whole paths to variables.

Find all paths matching a pattern

```
MATCH path = ()-[:ACTED_IN]->(movie:Movie)
RETURN path
```

Result

| path |
| --- |
| `(:Person {name: "Charlie Sheen"})-[:ACTED_IN {role: "Bud Fox"}]→(:Movie {title: "Wall Street"})` |
| `(:Person {name: "Martin Sheen"})-[:ACTED_IN {role: "Carl Fox"}]→(:Movie {title: "Wall Street"})` |
| `(:Person {name: "Martin Sheen"})-[:ACTED_IN {role: "A.J. MacInerney"}]→(:Movie {title: "The American President"})` |
| `(:Person {name: "Michael Douglas"})-[:ACTED_IN {role: "Gordon Gekko"}]→(:Movie {title: "Wall Street"})` |
| `(:Person {name: "Michael Douglas"})-[:ACTED_IN {role: "President Andrew Shepherd"}]→(:Movie {title: "The American President"})` |
|  |
| --- |
| Rows: 5 |

Find paths matching a pattern including a `WHERE` predicate

```
MATCH path = (:Person)-[:ACTED_IN]->(movie:Movie)<-[:DIRECTED]-(:Person)
WHERE movie.title = 'Wall Street'
RETURN path
```

Result

| path |
| --- |
| `(:Person {name: "Charlie Sheen"})-[:ACTED_IN {role: "Bud Fox"}]→(:Movie {title: "Wall Street"})←[:DIRECTED]-(:Person {name: "Oliver Stone"})` |
| `(:Person {name: "Martin Sheen"})-[:ACTED_IN {role: "Carl Fox"}]→(:Movie {title: "Wall Street"})←[:DIRECTED]-(:Person {name: "Oliver Stone"})` |
| `(:Person {name: "Michael Douglas"})-[:ACTED_IN {role: "Gordon Gekko"}]→(:Movie {title: "Wall Street"})←[:DIRECTED]-(:Person {name: "Oliver Stone"})` |
|  |
| --- |
| Rows: 3 |

For more information about how `MATCH` is used to find patterns of varying complexity (including [quantified path patterns](../../patterns/variable-length-patterns/#quantified-path-patterns), [quantified relationships](../../patterns/variable-length-patterns/#quantified-relationships), and the [shortest paths](../../patterns/shortest-paths/) between nodes), see the section on [Patterns](../../patterns/).

## Multiple MATCH clauses, the WITH clause, and clause composition

In Cypher, the behavior of a query is defined by its clauses.
Each clause takes the current graph state and a table of intermediate results, processes them, and passes the updated graph state and results to the next clause.
The first clause starts with the graph’s initial state and an empty table, while the final clause produces the query result.

Chaining consecutive `MATCH` clauses

```
MATCH (:Person {name: 'Martin Sheen'})-[:ACTED_IN]->(movie:Movie) (1)
MATCH (director:Person)-[:DIRECTED]->(movie) (2)
RETURN director.name AS director, movie.title AS movieTitle
```

|  |  |
| --- | --- |
| **1** | The result of the first `MATCH` clause is the variable `movie` which holds all the `Movies` that `Martin Sheen` has `ACTED_IN`. |
| **2** | The second `MATCH` clause uses the `movie` variable to find any `Person` node with a `DIRECTED` relationship to those `Movie` nodes that `Martin Sheen` has `ACTED_IN`. |

Result

| director | movieTitle |
| --- | --- |
| `"Oliver Stone"` | `"Wall Street"` |
| `"Rob Reiner"` | `"The American President"` |
|  |  |
| --- | --- |
| Rows: 2 | |

A variable can be implicitly carried over to the following clause by being referenced in another operation.
A variable can also be explicitly passed to the following clause using the [`WITH`](../with/) clause.
If a variable is neither implicitly nor explicitly carried over to its following clause, it will be discarded and is not available for reference later in the query.

Using `WITH` and multiple `MATCH` clauses

```
MATCH (actors:Person)-[:ACTED_IN]->(movies:Movie) (1)
WITH actors, count(movies) AS movieCount (2)
ORDER BY movieCount DESC
LIMIT 1 (3)
MATCH (actors)-[:ACTED_IN]->(movies) (4)
RETURN actors.name AS actor, movieCount, collect(movies.title) AS movies
```

|  |  |
| --- | --- |
| **1** | The `Person` and `Movie` nodes matched in this step are stored in variables, which are then passed on to the second row of the query. |
| **2** | The `movies` variable is implicitly imported by its occurrence in the `count()` function. The `WITH` clause explicitly imports the `actors` variable. |
| **3** | An [`ORDER BY`](../order-by/) clause orders the results by `movieCount` in descending order, ensuring that the `Person` with the highest number of movies appears at the top, and [`LIMIT`](../limit/) `1` ensures that all other `Person` nodes are discarded. |
| **4** | The second `MATCH` clause finds all `Movie` nodes associated with the `Person` nodes currently bound to the `actors` variable. |

|  |  |
| --- | --- |
|  | The above query uses the [`collect()` function](../../functions/aggregating/#functions-collect). |

Result

| actor | movieCount | movies |
| --- | --- | --- |
| `"Martin Sheen"` | `2` | `["Wall Street", "The American President"]` |
|  |  |  |
| --- | --- | --- |
| Rows: 1 | | |

For more information about how Cypher queries work, see [Clause composition](../clause-composition/).

## MATCH using dynamic node labels and relationship types

Node labels and relationship types can be referenced dynamically in expressions, parameters, and variables when matching nodes and relationships.
This allows for more flexible queries and mitigates the risk of Cypher injection.
(For more information about Cypher injection, see [Neo4j Knowledge Base → Protecting against Cypher injection](https://neo4j.com/developer/kb/protecting-against-cypher-injection/)).

Syntax for matching node labels dynamically

```
MATCH (n:$(<expr>))
MATCH (n:$any(<expr>))
MATCH (n:$all(<expr>))
```

|  |  |
| --- | --- |
|  | `MATCH (n:$all(<expr>))` is functionally equivalent to `MATCH (n:$(<expr>))`. |

Syntax for matching relationship types dynamically

```
MATCH ()-[r:$(<expr>))]->()
MATCH ()-[r:$any(<expr>)]->()
MATCH ()-[r:$all(<expr>))]->()
```

The expression must evaluate to a `STRING NOT NULL | LIST<STRING NOT NULL> NOT NULL` value.
If you use a `LIST<STRING>` with more than one item in a relationship pattern with dynamic relationship types, no results will be returned.
This is because a relationship can only have exactly one type.

Match labels dynamically

```
WITH ["Person", "Director"] AS labels
MATCH (directors:$(labels))
RETURN directors
```

Result

| directors |
| --- |
| `(:Person:Director {name: "Oliver Stone"})` |
| `(:Person:Director {name: "Rob Reiner"})` |
|  |
| --- |
| Rows: 2 |

Match nodes dynamically using `any()`

```
MATCH (n:$any(["Movie", "Actor"]))
RETURN n AS nodes
```

Result

| nodes |
| --- |
| `(:Person:Actor {name: "Charlie Sheen"})` |
| `(:Person:Actor {name: "Martin Sheen"})` |
| `(:Person:Actor {name: "Michael Douglas"})` |
| `(:Movie {title: "Wall Street"})` |
| `(:Movie {title: "The American President"})` |
|  |
| --- |
| Rows: 5 |

Parameter

```
{
  "label": "Movie"
}
```

Match nodes dynamically using a parameter

```
MATCH (movie:$($label))
RETURN movie.title AS movieTitle
```

Result

| movieTitle |
| --- |
| `"Wall Street"` |
| `"The American President"` |
|  |
| --- |
| Rows: 2 |

Match relationships dynamically using a variable

```
CALL db.relationshipTypes()
YIELD relationshipType
MATCH ()-[r:$(relationshipType)]->()
RETURN relationshipType, count(r) AS relationshipCount
```

Result

| relationshipType | relationshipCount |
| --- | --- |
| `"ACTED_IN"` | `5` |
| `"DIRECTED"` | `2` |
|  |  |
| --- | --- |
| Rows: 2 | |

### Performance caveats

`MATCH` queries that use dynamic values may not perform as well as those with static values.
Neo4j is actively working to improve the performance of these queries.
The table below outlines performance caveats for specific Neo4j versions.

Neo4j versions and performance caveats

| Neo4j versions | Performance caveat |
| --- | --- |
| 5.26 — 2025.07 | The [Cypher planner](../../planning-and-tuning/execution-plans/) is not able to leverage [indexes](../../indexes/search-performance-indexes/) with [index scans or seeks](../../planning-and-tuning/operators/operators-detail/#leaf-operators) and must instead utilize the [`AllNodesScan`](../../planning-and-tuning/operators/operators-detail/#query-plan-all-nodes-scan) operator, which reads all nodes from the node store and is therefore more costly. |
| 2025.08 — 2025.10 | The Cypher planner is able to leverage [token lookup indexes](../../indexes/search-performance-indexes/using-indexes/#token-lookup-indexes) when matching node labels and relationship types dynamically. This is enabled by the introduction of three new query plan operators: [`DynamicLabelNodeLookup`](../../planning-and-tuning/operators/operators-detail/#query-plan-dynamic-label-node-lookup), [`DynamicDirectedRelationshipTypeLookup`](../../planning-and-tuning/operators/operators-detail/#query-plan-dynamic-directed-relationship-type-lookup), and [`DynamicUndirectedRelationshipTypeLookup`](../../planning-and-tuning/operators/operators-detail/#query-plan-dynamic-undirected-relationship-type-lookup). It is not, however, able to use indexes on property values. For example, `MATCH (n:$(Label) {foo: bar})` will not use any indexes on `n.foo` but can use a `DynamicLabelNodeLookup` on `$(label)`. |
| 2025.11 — current | The Cypher planner is able to leverage indexes on property values, however:  * It only supports exact seeks on range indexes (no full text or spatial). * The index order cannot be leveraged, so the planner must insert separate ordering if required later on in the query. * Parallel runtime seeks and scans are single-threaded. * The planner doesn’t combine multiple property index seeks when generating the results for the dynamic part of the query. For example, using `$any` in combination with multiple labels that share an index on a property result in the operator choosing one of the indexes based on selectivity and then stepping through the seek results and filtering for the remainder of the expression.   + Example:  ```   CREATE RANGE INDEX actor_has_birthyear FOR (a:Actor) ON (a.birthYear)   CREATE RANGE INDEX director_has_birthyear FOR (d:Director) ON (d.birthYear)    MATCH (p:$any(["Actor", "Director"]) { birthYear: 1983 }) RETURN p.name   ``` |

### Further reading

[Neo4j Developer Blog: Cypher Dynamism: A Step Toward Simpler and More Secure Queries](https://medium.com/neo4j/cypher-dynamism-a-step-toward-simpler-and-more-secure-queries-70fab8a815b2)

---

## 4. 

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

---

## 5. 

Neo4j offers several constraints to ensure the quality and integrity of data in a graph.
The following constraints are available in Neo4j:

* [Property uniqueness constraints](create-constraints/#create-property-uniqueness-constraints): ensure that the combined property values are unique for all nodes with a specific label or all relationships with a specific type.
* [Property existence constraints](create-constraints/#create-property-existence-constraints): ensure that a property exists either for all nodes with a specific label or for all relationships with a specific type. Enterprise Edition
* [Property type constraints](create-constraints/#create-property-type-constraints): ensure that a property has the required property type for all nodes with a specific label or for all relationships with a specific type. Enterprise Edition
* [Key constraints](create-constraints/#create-key-constraints): ensure that all properties exist and that the combined property values are unique for all nodes with a specific label or all relationships with a specific type.Enterprise Edition

For more information about index-backed constraints, constraint creation failures and data violation scenarios, as well as creating, listing and dropping constraints, see:

* [Create constraints](create-constraints/)
* [Show constraints](list-constraints/)
* [Drop constraints](drop-constraints/)

For reference material about the Cypher® commands used to manage constraints, see [Syntax → Constraints](../syntax/#constraints).

|  |  |
| --- | --- |
|  | All constraints created using the older [`CREATE CONSTRAINT`](create-constraints/) syntax will automatically be added to the graph type of a database. Not all constraint types can be created using this syntax, however, and maintaining individual constraints can become complicated over time as their number increases.  **It is, therefore, recommended to define a schema using a graph type, which offers both additional, more sophisticated constraint types and a more holistic and simplified approach for constraining and maintaining the shape of the data in a graph.**  For more information, see [Graph types](../graph-types/). |

---

## Bibliography

1. [](https://neo4j.com/docs/cypher-manual/current/introduction/)
2. [](https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/overview/)
3. [](https://neo4j.com/docs/cypher-manual/current/clauses/match/)
4. [](https://neo4j.com/docs/cypher-manual/current/clauses/merge/)
5. [](https://neo4j.com/docs/cypher-manual/current/constraints/)