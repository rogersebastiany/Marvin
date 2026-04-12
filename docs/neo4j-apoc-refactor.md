# Neo4j APOC — graph refactoring, rename labels, types, properties


---

## 1. 

|  |  |
| --- | --- |
|  | This manual covers the documentation for APOC Core. For APOC Extended, go to the [APOC Extended manual](https://neo4j.com/labs/apoc/5/overview). |

The guide covers the following areas:

* [Introduction](introduction/) — An Introduction to the APOC library.
* [Installation](installation/) — Installation instructions for the library.
* [APOC and Cypher versions](cypher-versions/) — APOC and different Cypher versions.
* [Built-in Help](help/) — Built-in help in the library.
* [Configuration Options](config/) — Configuration options used by the library.
* [Security Guidelines](security-guidelines/) — Guidelines on securing the APOC library, and its environment.
* [Procedures & Functions](overview/) — A list of all APOC procedures and functions.
* [Import](import/) — A detailed guide to procedures that can be used to import data from different formats including JSON, CSV, and XLS.
* [Export](export/) — A detailed guide to procedures that can be used to export data to different formats including JSON, CSV, GraphML, and Gephi.
* [Graph Refactoring](graph-refactoring/) — A detailed guide to procedures that can be used to refactor graphs.
* [Graph updates](graph-updates/) — A detailed guide to procedures that can be used to apply graph updates.
* [Data Structures](data-structures/) — A detailed guide to procedures and functions, that can be used to work with data structures.
* [Temporal (Date Time)](temporal/) — A detailed guide to procedures that can be used to format temporal types.
* [Mathematical Operations](mathematical/) — A detailed guide to procedures and functions that can be used for mathematical operations.
* [Advanced Graph Querying](graph-querying/) — A detailed guide to procedures that can be used for advanced graph querying.
* [Comparing Graphs](comparing-graphs/) — A detailed guide to procedures that can be used to compare graphs.
* [Conditional Cypher Execution](conditionals/) — A detailed guide to procedures that can be used for to execute Cypher conditionally.
* [Cypher Execution](cypher-execution/) — A detailed guide to procedures that can be used for Cypher scripting.
* [Virtual Nodes & Relationships (Graph Projections)](virtual/) — A detailed guide to procedures that can be used to create virtual nodes and relationships.
* [Background Operations](background-operations/) — A detailed guide to procedures that can be used for background job management.
* [Cypher initializer](operational/) — A detailed guide to operational procedures.
* [Schema Information](schema/) — A detailed guide to indexing procedures.

---

## 2. 

|  |  |
| --- | --- |
|  | This procedure is deprecated. Use Cypher’s [`CREATE`](/docs/cypher-manual/current/clauses/create/#dynamic-create) and [`DELETE`](/docs/cypher-manual/current/clauses/delete/#delete-relationships-only) clauses instead.. |

Details

|  |  |  |  |
| --- | --- | --- | --- |
| **Syntax** | `apoc.refactor.rename.type(oldType, newType [, rels, config ]) :: (batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages, batch, operations, constraints, indexes)` | | |
| **Description** | Renames all `RELATIONSHIP` values with type `oldType` to `newType`. If a `LIST<RELATIONSHIP>` is provided, the renaming is applied to the `RELATIONSHIP` values within this `LIST<RELATIONSHIP>` only. | | |
| **Input arguments** | **Name** | **Type** | **Description** |
| `oldType` | `STRING` | The type to rename. |
| `newType` | `STRING` | The new type for the relationship. |
| `rels` | `LIST<RELATIONSHIP>` | The relationships to apply the new name to. If this list is empty, all relationships with the old type will be renamed. The default is: `[]`. |
| `config` | `MAP` | `{ batchSize = 100000 :: INTEGER, concurrency :: INTEGER, retries = 0 :: INTEGER, parallel = true :: BOOLEAN, batchMode = "BATCH" :: STRING }`. The default is: `{}`. |
| **Return arguments** | **Name** | **Type** | **Description** |
| `batches` | `INTEGER` | The number of batches the operation was run in. |
| `total` | `INTEGER` | The total number of renamings performed. |
| `timeTaken` | `INTEGER` | The time taken to complete the operation. |
| `committedOperations` | `INTEGER` | The total number of committed operations. |
| `failedOperations` | `INTEGER` | The total number of failed operations. |
| `failedBatches` | `INTEGER` | The total number of failed batches. |
| `retries` | `INTEGER` | The total number of retries. |
| `errorMessages` | `MAP` | The collected error messages. |
| `batch` | `MAP` | `{ total :: INTEGER, failed :: INTEGER, committed :: INTEGER, errors :: MAP }` |
| `operations` | `MAP` | `{ total :: INTEGER, failed :: INTEGER, committed :: INTEGER, errors :: MAP }` |
| `constraints` | `LIST<STRING>` | Constraints associated with the given label or type. |
| `indexes` | `LIST<STRING>` | Indexes associated with the given label or type. |

## Refactoring nodes using Cypher

Node labels and relationship types can be referenced dynamically in Cypher without using APOC.

Cypher syntax for creating, matching and merging labels and types dynamically

```
CREATE (n1:$(label))-[r:$(type)]->(n2:$(label))
MERGE (n1:$(label))-[r:$(type)]->(n2:$(label))
MATCH (n1:$(label))-[r:$(type)]->(n2:$(label))
```

The dynamically calculated type must evaluate to a `STRING` or `LIST<STRING>`.
For more information, see the [Cypher Manual → CREATE](/docs/cypher-manual/25/clauses/create/#dynamic-create),
[MERGE](/docs/cypher-manual/25/clauses/merge/#dynamic-merge), [MATCH](/docs/cypher-manual/25/clauses/match/#dynamic-match).

Batching, as well as parallel execution, can be achieved in Cypher using `CALL {…​} IN CONCURRENT TRANSACTIONS`.
For more information, see [CALL subqueries in transactions → Concurrent transactions](/docs/cypher-manual/25/subqueries/subqueries-in-transactions/#concurrent-transactions).

## Usage Examples

The examples in this section are based on the following sample graph:

```
CREATE (mark:Engineer {name: "Mark", city: "London"})
CREATE (jennifer:Engineer {name: "Jennifer", city: "St Louis"})
CREATE (michael:Engineer {name: "Michael", city: "Dresden"})
CREATE (jim:Engineer {name: "Jim", city: "London"})
CREATE (alistair:Engineer {name: "Alistair", city: "London"})

MERGE (jim)-[:COLLEAGUES {since: date("2006-05-01")}]->(alistair)
MERGE (mark)-[:COLLEAGUES {since: date("2018-02-01")}]->(jennifer)
MERGE (mark)-[:COLLEAGUES {since: date("2013-05-01")}]->(michael);
```

The following changes the relationship type between Jim and Alistair from `COLLEAGUES` to `FROLLEAGUES`:

apoc.refactor.rename.type

```
MATCH (:Engineer {name: "Jim"})-[rel]->(:Engineer {name: "Alistair"})
WITH collect(rel) AS rels
CALL apoc.refactor.rename.type("COLLEAGUES", "FROLLEAGUES", rels)
YIELD batches
RETURN count(*) AS count
```

Using Cypher

```
MATCH (a:Engineer {name: "Jim"})-[rel:COLLEAGUES]->(b:Engineer {name: "Alistair"})
MERGE (a)-[r:FROLLEAGUES]->(b)
SET r = properties(rel)
WITH rel, r
DELETE rel
RETURN count(*) AS count
```

Results

| count |  |
| --- | --- |
| 1 |  |

After this query has run, we’ll have the following graph:

|  |  |
| --- | --- |
|  | This procedure does not rename the relationship type; it creates a new relationship with the new type and copies over the properties from the original relationship, which is then deleted. |

[More documentation of apoc.refactor.rename.type](../../../graph-refactoring/rename-label-type-property/)

---

## 3. 

The APOC library contains procedures that can be used to rename labels, relationship types, and properties of nodes and relationships.

## Procedures for renaming labels, types, and properties

| Qualified Name | Type |
| --- | --- |
| [apoc.refactor.rename.label](../../overview/apoc.refactor/apoc.refactor.rename.label/)  `apoc.refactor.rename.label(oldLabel STRING, newLabel STRING, nodes LIST<NODE>)` - renames the given label from `oldLabel` to `newLabel` for all `NODE` values. If a `LIST<NODE>` is provided, the renaming is applied to the `NODE` values within this `LIST<NODE>` only. | Procedure Deprecated in Cypher 25 |
| [apoc.refactor.rename.nodeProperty](../../overview/apoc.refactor/apoc.refactor.rename.nodeProperty/)  `apoc.refactor.rename.nodeProperty(oldName STRING, newName STRING, nodes LIST<NODE>, config MAP<STRING, ANY>)` - renames the given property from `oldName` to `newName` for all `NODE` values. If a `LIST<NODE>` is provided, the renaming is applied to the `NODE` values within this `LIST<NODE>` only. | Procedure Deprecated in Cypher 25 |
| [apoc.refactor.rename.type](../../overview/apoc.refactor/apoc.refactor.rename.type/)  `apoc.refactor.rename.type(oldType STRING, newType STRING, rels LIST<RELATIONSHIP>, config MAP<STRING, ANY>)` - renames all `RELATIONSHIP` values with type `oldType` to `newType`. If a `LIST<RELATIONSHIP>` is provided, the renaming is applied to the `RELATIONSHIP` values within this `LIST<RELATIONSHIP>` only. | Procedure Deprecated in Cypher 25 |
| [apoc.refactor.rename.typeProperty](../../overview/apoc.refactor/apoc.refactor.rename.typeProperty/)  `apoc.refactor.rename.typeProperty(oldName STRING, newName STRING, rels LIST<RELATIONSHIP>, config MAP<STRING, ANY>)` - renames the given property from `oldName` to `newName` for all `RELATIONSHIP` values. If a `LIST<RELATIONSHIP>` is provided, the renaming is applied to the `RELATIONSHIP` values within this `LIST<RELATIONSHIP>` only. | Procedure Deprecated in Cypher 25 |

## Config parameters

As the collection of data is processed in batches using `apoc.periodic.iterate`, these procedures support the following config parameters:

Table 1. Config

| name | type | default | description |
| --- | --- | --- | --- |
| batchSize | INTEGER | 10000 | run the specified number of operation statements in a single tx - params: {\_count, \_batch} |
| parallel | BOOLEAN | true | run operation statements in parallel (note that statements might deadlock if conflicting)  Please note that, in case of `parallel: false`, APOC is designed to reuse the same `java.util.concurrent.ThreadPoolExecutor` with a maximum pool size equal 1, in order to prevent parallelism; this means that if you want to execute multiple apoc.periodic.iterate each one will be executed when the previous one has been completed. Instead, with `parallel: true`, APOC will use a `ThreadPoolExecutor` with a configurable maximum pool size via the `apoc.jobs.pool.num_threads` config or as default with the number of available processor \* 2. Therefore, if we execute multiple `apoc.periodic.iterate` each one will be executed in parallel if the queue pool size can accept new tasks. Furthermore, to be noted that running in parallel affects all databases, and not the single database you are using. So with e.g. 2 databases `db1` and `db2`, the `apoc.periodic.iterate` on `db1` will impact on performance if we execute an `apoc.periodic.iterate` on `db2`. |
| retries | INTEGER | 0 | if the operation statement fails with an error, sleep 100ms and retry until retries-count is reached - param {\_retry} |
| batchMode | STRING | "BATCH" | how data-driven statements should be processed by operation statement. Valid values are:  \* "BATCH" - execute operation statement once per batchSize. Operation statement is prefixed with the following, which extracts each field returned in the data-driven statement from the `$_batch` parameter: [source,cypher] ---- UNWIND $\_batch AS \_batch WITH \_batch.field1 AS field1, \_batch.field2 AS field2 ---- \* "SINGLE" - execute operation statement one at a time \* "BATCH\_SINGLE" - execute operation statement once per batchSize, but leaves unpacking of batch to the operation statement. The operation query can access the batched values via the `$_batch` parameter. |
| concurrency | INTEGER | Number of processors available | number of concurrent tasks are generated when using `parallel:true` |

## Examples

The below examples will further explain these procedures.

The following creates a graph contains nodes with the label `Engineer` connected by `COLLEAGUES` relationships:

```
CREATE (mark:Engineer {name: "Mark", city: "London"})
CREATE (jennifer:Engineer {name: "Jennifer", city: "St Louis"})
CREATE (michael:Engineer {name: "Michael", city: "Dresden"})
CREATE (jim:Engineer {name: "Jim", city: "London"})
CREATE (alistair:Engineer {name: "Alistair", city: "London"})

MERGE (jim)-[:COLLEAGUES {since: date("2006-05-01")}]->(alistair)
MERGE (mark)-[:COLLEAGUES {since: date("2018-02-01")}]->(jennifer)
MERGE (mark)-[:COLLEAGUES {since: date("2013-05-01")}]->(michael)
```

If the above query is run, it will result in the following graph:

### Renaming node labels

The following changes the label on Mark, Jennifer, and Michael from `Engineer` to `DevRel`:

```
MATCH (person:Engineer)
WHERE person.name IN ["Mark", "Jennifer", "Michael"]
WITH collect(person) AS people
CALL apoc.refactor.rename.label("Engineer", "DevRel", people)
YIELD committedOperations
RETURN committedOperations
```

If the above query is run, it will result in the following graph:

### Renaming relationship types

The following changes the relationship type between Jim and Alistair from `COLLEAGUES` to `FROLLEAGUES`:

```
MATCH (:Engineer {name: "Jim"})-[rel]->(:Engineer {name: "Alistair"})
WITH collect(rel) AS rels
CALL apoc.refactor.rename.type("COLLEAGUES", "FROLLEAGUES", rels)
YIELD committedOperations
RETURN committedOperations
```

### Renaming node properties

The following query changes the node property `city` to `location` for all nodes with the `DevRel` label:

```
MATCH (person:DevRel)
WITH collect(person) AS people
CALL apoc.refactor.rename.nodeProperty("city", "location", people)
YIELD committedOperations
RETURN committedOperations
```

The following query returns all the nodes in our graph after this refactoring has been done:

```
MATCH (n)
RETURN (n)
```

Table 2. Results

| n |
| --- |
| (:DevRel {name: "Jennifer", location: "St Louis"}) |
| (:DevRel {name: "Michael", location: "Dresden"}) |
| (:Engineer {city: "London", name: "Jim"}) |
| (:DevRel {name: "Mark", location: "London"}) |
| (:Engineer {city: "London", name: "Alistair"}) |

### Renaming relationship properties

The following query changes the relationship property `since` to `from` for all relationships:

```
MATCH ()-[rel]->()
WITH collect(rel) AS rels
CALL apoc.refactor.rename.typeProperty("since", "from", rels)
YIELD committedOperations
RETURN committedOperations
```

The following query returns all the paths in our graph after this refactoring has been done:

```
MATCH path = ()-[]->()
RETURN path
```

Table 3. Results

| path |
| --- |
| [{"name":"Mark","location":"London"},{"from":"2018-02-01"},{"name":"Jennifer","location":"St Louis"}] |
| [{"name":"Mark","location":"London"},{"from":"2013-05-01"},{"name":"Michael","location":"Dresden"}] |
| [{"name":"Jim","city":"London"},{"from":"2006-05-01"},{"name":"Alistair","city":"London"}] |

---

## Bibliography

1. [](https://neo4j.com/docs/apoc/current/)
2. [](https://neo4j.com/docs/apoc/current/overview/apoc.refactor/apoc.refactor.rename.type/)
3. [](https://neo4j.com/docs/apoc/current/graph-refactoring/rename-label-type-property/)