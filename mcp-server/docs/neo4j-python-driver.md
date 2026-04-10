# Neo4j Python Driver


---

## 1. URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"

The Neo4j Python driver is the official library to interact with a Neo4j instance through a Python application.

At the hearth of Neo4j lies [Cypher](#Cypher), the query language to interact with a Neo4j database.
Although this guide does not *require* you to be a seasoned Cypher querier, it’s easier to focus on the Python-specific bits if you know some Cypher already.
You will also get a *gentle* introduction to Cypher in these pages, but check out [Getting started → Cypher](https://neo4j.com/docs/getting-started/cypher/) for a more detailed walkthrough of graph databases modelling and querying if this is your first approach.

## Install

Install the Neo4j Python driver with `pip`:

```
pip install neo4j
```

[More info on installing the driver](https://neo4j.com/docs/python-manual/current/install/)

## Connect to the database

Connect to a database by creating a `Driver` object and providing a URL and an authentication token.
Once you have a `Driver` instance, use the `.verify_connectivity()` method to ensure that a working connection can be established.

```
from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "<database-uri>"
AUTH = ("<username>", "<password>")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
```

[More info on connecting to a database](https://neo4j.com/docs/python-manual/current/connect/)

## Create an example graph

Run a Cypher query with the method `Driver.execute_query()`.
Do not hardcode or concatenate parameters: use placeholders and specify the parameters as keyword arguments.

Create two `Person` nodes and a `KNOWS` relationship between them

```
summary = driver.execute_query("""
    CREATE (a:Person {name: $name})
    CREATE (b:Person {name: $friendName})
    CREATE (a)-[:KNOWS]->(b)
    """,
    name="Alice", friendName="David",
    database_="<database-name>",
).summary
print("Created {nodes_created} nodes in {time} ms.".format(
    nodes_created=summary.counters.nodes_created,
    time=summary.result_available_after
))
```

[More info on querying the database](https://neo4j.com/docs/python-manual/current/query-simple/)

## Query a graph

To retrieve information from the database, use the Cypher clause `MATCH`:

Retrieve all `Person` nodes who know other persons

```
records, summary, keys = driver.execute_query("""
    MATCH (p:Person)-[:KNOWS]->(:Person)
    RETURN p.name AS name
    """,
    database_="<database-name>",
)

# Loop through results and do something with them
for record in records:
    print(record.data())  # obtain record as dict

# Summary information
print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after
))
```

[More info on querying the database](https://neo4j.com/docs/python-manual/current/query-simple/)

## Close connections and sessions

Unless you created them using the `with` statement, call the `.close()` method on all `Driver` and `Session` instances to release any resources still held by them.

```
from neo4j import GraphDatabase

driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session(database="<database-name>")

# session/driver usage

session.close()
driver.close()
```

## Glossary

LTS
:   A *Long Term Support* release is one guaranteed to be supported for a number of years.
    Neo4j 4.4 and 5.26 are LTS versions.

Aura
:   [Aura](https://neo4j.com/product/auradb/) is Neo4j’s fully managed cloud service.
    It comes with both free and paid plans.

Cypher
:   [Cypher](https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/) is Neo4j’s graph query language that lets you retrieve data from the database.
    It is like SQL, but for graphs.

APOC
:   [Awesome Procedures On Cypher (APOC)](/docs/apoc/current/) is a library of (many) functions that can not be easily expressed in Cypher itself.

Bolt
:   [Bolt](/docs/bolt/current/) is the protocol used for interaction between Neo4j instances and drivers.
    It listens on port 7687 by default.

ACID
:   Atomicity, Consistency, Isolation, Durability (ACID) are properties guaranteeing that database transactions are processed reliably.
    An ACID-compliant DBMS ensures that the data in the database remains accurate and consistent despite failures.

eventual consistency
:   A database is eventually consistent if it provides the guarantee that all cluster members will, *at some point in time*, store the latest version of the data.

causal consistency
:   A database is causally consistent if read and write queries are seen by every member of the cluster in the same order.
    This is stronger than *eventual consistency*.

NULL
:   The null marker is not a type but a placeholder for absence of value.
    For more information, see [Cypher → Working with `null`](/docs/cypher-manual/current/values-and-types/working-with-null/).

transaction
:   A transaction is a unit of work that is either *committed* in its entirety or *rolled back* on failure.
    An example is a bank transfer: it involves multiple steps, but they must *all* succeed or be reverted, to avoid money being subtracted from one account but not added to the other.

backpressure
:   Backpressure is a force opposing the flow of data. It ensures that the client is not being overwhelmed by data faster than it can handle.

bookmark
:   A *bookmark* is a token representing some state of the database. By passing one or multiple bookmarks along with a query, the server will make sure that the query does not get executed before the represented state(s) have been established.

transaction function
:   A transaction function is a callback executed by an `execute_read` or `execute_write` call. The driver automatically re-executes the callback in case of server failure.

Driver
:   A [`Driver`](/docs/api/python-driver/current/api.html#neo4j.Driver) object holds the details required to establish connections with a Neo4j database.

---

## 2. session usage

When [querying the database with `execute_query()`](../query-simple/), the driver automatically creates a *transaction*.
A transaction is a unit of work that is either *committed* in its entirety or *rolled back* on failure.
You can include multiple Cypher statements in a single query, as for example when using `MATCH` and `CREATE` in sequence to [update the database](../query-simple/#_update_the_database), but you cannot have multiple queries and interleave some client-logic in between them.

For these more advanced use-cases, the driver provides functions to manually control transactions.
The most common form is *managed transactions*, and you can think of them as a way of unwrapping the flow of `.execute_query()` and being able to specify its desired behavior in more places.

## Create a session

Before running a transaction, you need to obtain a *session*.
Sessions act as query channels between the driver and the server, and ensure [causal consistency](#causal_consistency) is enforced.

Sessions are created with the method [`Driver.session()`](/docs/api/python-driver/current/api.html#session), with the keyword argument `database` allowing to specify the [target database](#_database_selection).
For further parameters, see [Session configuration](#_session_configuration).

```
with driver.session(database="<database-name>") as session:
    ...
```

Creating a session is a lightweight operation, so sessions can be created and destroyed without significant cost.
Always [close sessions](#_close_sessions) when you are done with them.

**Sessions are *not* thread safe**: you can share the main `Driver` object across threads, but each thread should create its own sessions.

## Run a managed transaction

A transaction can contain multiple queries.
As Neo4j is [ACID](#ACID) compliant, **queries within a transaction will either be executed as a whole or not at all**: you cannot get a part of the transaction succeeding and another failing.
Use transactions to group together related queries which work together to achieve a single *logical* database operation.

You create a managed transaction with the methods [`Session.execute_read()`](/docs/api/python-driver/current/api.html#neo4j.Session.execute_read) and [`Session.execute_write()`](/docs/api/python-driver/current/api.html#neo4j.Session.execute_write), depending on whether you want to retrieve data from the database or alter it.
Both methods take a *transaction function* callback, which is responsible for carrying out the queries and processing the result.

Retrieve people whose name starts with `Al`.

```
def match_person_nodes(tx, name_filter): (3)
    result = tx.run(""" (4)
        MATCH (p:Person) WHERE p.name STARTS WITH $filter
        RETURN p.name AS name ORDER BY name
        """, filter=name_filter)
    return list(result)  # a list of Record objects (5)

with driver.session(database="<database-name>") as session:  (1)
    people = session.execute_read(  (2)
        match_person_nodes,
        "Al",
    )
    for person in people:
        print(person.data())  # obtain dict representation
```

|  |  |
| --- | --- |
| **1** | Create a session. A single session can be the container for multiple queries. Unless created using the `with` construct, remember to close it when done. |
| **2** | The `.execute_read()` (or `.execute_write()`) method is the entry point into a transaction. It takes a callback to a *transaction function* and an arbitrary number of positional and keyword arguments which are handed down to the transaction function. |
| **3** | The transaction function callback is responsible of running queries. |
| **4** | Use the method [`Transaction.run()`](/docs/api/python-driver/current/api.html#neo4j.Transaction.run) to run queries. Each query run returns a [`Result`](/docs/api/python-driver/current/api.html#neo4j.Result) object. |
| **5** | [Process the result](#process-result) using any of the methods on `Result`. |

**Do not hardcode or concatenate parameters directly into the query**.
Use [query parameters](../query-simple/#query-parameters) instead, both for performance and security reasons.

**Transaction functions should never return the `Result` object directly**.
Instead, always [process the result](#process-result) in some way; at minimum, cast it to list.
Within a transaction function, a `return` statement results in the transaction being committed, while the transaction is automatically rolled back if an exception is raised.

A transaction with multiple queries, client logic, and potential roll backs

```
from neo4j import GraphDatabase

URI = "<database-uri>"
AUTH = ("<username>", "<password>")
employee_threshold=10

def main():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        with driver.session(database="<database-name>") as session:
            for i in range(100):
                name = f"Thor{i}"
                org_id = session.execute_write(employ_person_tx, name)
                print(f"User {name} added to organization {org_id}")

def employ_person_tx(tx, name):
    # Create new Person node with given name, if not exists already
    result = tx.run("""
        MERGE (p:Person {name: $name})
        RETURN p.name AS name
        """, name=name
    )

    # Obtain most recent organization ID and the number of people linked to it
    result = tx.run("""
        MATCH (o:Organization)
        RETURN o.id AS id, COUNT{(p:Person)-[r:WORKS_FOR]->(o)} AS employees_n
        ORDER BY o.created_date DESC
        LIMIT 1
    """)
    org = result.single()

    if org is not None and org["employees_n"] == 0:
        raise Exception("Most recent organization is empty.")
        # Transaction will roll back -> not even Person is created!

    # If org does not have too many employees, add this Person to that
    if org is not None and org.get("employees_n") < employee_threshold:
        result = tx.run("""
            MATCH (o:Organization {id: $org_id})
            MATCH (p:Person {name: $name})
            MERGE (p)-[r:WORKS_FOR]->(o)
            RETURN $org_id AS id
            """, org_id=org["id"], name=name
        )

    # Otherwise, create a new Organization and link Person to it
    else:
        result = tx.run("""
            MATCH (p:Person {name: $name})
            CREATE (o:Organization {id: randomuuid(), created_date: datetime()})
            MERGE (p)-[r:WORKS_FOR]->(o)
            RETURN o.id AS id
            """, name=name
        )

    # Return the Organization ID to which the new Person ends up in
    return result.single()["id"]

if     main()
```

The driver automatically retries to run a failed transaction if the failure is deemed to be transient (for example due to temporary server unavailability).
An error will be raised if the operation keeps failing after the configured [maximum retry time](https://neo4j.com/docs/api/python-driver/current/api.html#max-transaction-retry-time).

Because the transaction might be re-run, **transaction functions must be *idempotent*** (i.e., they should produce the same effect when run several times), because you do not know upfront how many times they are going to be executed.
In practice, this means that you should not edit nor rely on globals, for example.
Note that although transactions functions might be executed multiple times, the database queries inside it will always run only once.

A session can chain multiple transactions, but **only one single transaction can be active within a session at any given time**.
To maintain multiple concurrent transactions, use multiple concurrent sessions.

### Transaction function configuration

The decorator [`unit_of_work()`](/docs/api/python-driver/current/api.html#neo4j.unit_of_work) gives further control on transaction functions.
It allows to specify:

* a transaction timeout (in seconds).
  Transactions that run longer will be terminated by the server.
  The default value is set on the server side.
  The minimum value is one millisecond (`0.001`).
* a dictionary of metadata that gets attached to the transaction.
  These metadata get logged in the server `query.log`, and are visible in the output of the `SHOW TRANSACTIONS` Cypher command.
  Use this to tag transactions.

```
from neo4j import unit_of_work

@unit_of_work(timeout=5, metadata={"app_name": "people_tracker"})
def count_people(tx):
    result = tx.run("MATCH (a:Person) RETURN count(a) AS people")
    record = result.single()
    return record["people"]

with driver.session(database="<database-name>") as session:
    people_n = session.execute_read(count_people)
```

## Run an explicit transaction

You can achieve full control over transactions by manually beginning one with the method [`Session.begin_transaction()`](/docs/api/python-driver/current/api.html#neo4j.Session.begin_transaction).
You may then run queries inside an explicit transaction with the method [`Transaction.run()`](/docs/api/python-driver/current/api.html#neo4j.Transaction.run).

```
with driver.session(database="<database-name>") as session:
    with session.begin_transaction() as tx:
        # use tx.run() to run queries and tx.commit() when done
        tx.run("<QUERY 1>")
        tx.run("<QUERY 2>")

        tx.commit()
```

An explicit transaction can be committed with [`Transaction.commit()`](https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Transaction.commit) or rolled back with [`Transaction.rollback()`](https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Transaction.rollback).
If no explicit action is taken, the driver will automatically roll back the transaction at the end of its lifetime.

|  |  |
| --- | --- |
|  | Queries run with `tx.run()` failing due to a transient server error can be retried without need to alter the original request. You can discover whether an error is transient via the method `Neo4jError.is_retryable()`, which gives insights into whether a further attempt might be successful. |

Explicit transactions are most useful for applications that need to distribute Cypher execution across multiple functions for the same transaction, or for applications that need to run multiple queries within a single transaction but without the automatic retries provided by managed transactions.

An explicit transaction example involving an external API

```
import neo4j

URI = "<database-uri>"
AUTH = ("<username>", "<password>")

def main():
    with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
        customer_id = create_customer(driver)
        other_bank_id = 42
        transfer_to_other_bank(driver, customer_id, other_bank_id, 999)

def create_customer(driver):
    result, _, _ = driver.execute_query("""
        MERGE (c:Customer {id: rand()})
        RETURN c.id AS id
    """, database_ = "<database-name>")
    return result[0]["id"]

def transfer_to_other_bank(driver, customer_id, other_bank_id, amount):
    with driver.session(database="<database-name>") as session:
        with session.begin_transaction() as tx:
            if not customer_balance_check(tx, customer_id, amount):
                # give up
                return

            other_bank_transfer_api(customer_id, other_bank_id, amount)
            # Now the money has been transferred => can't rollback anymore
            # (cannot rollback external services interactions)

            try:
                decrease_customer_balance(tx, customer_id, amount)
                tx.commit()
            except Exception as e:
                request_inspection(customer_id, other_bank_id, amount, e)
                raise  # roll back

def customer_balance_check(tx, customer_id, amount):
    query = ("""
        MATCH (c:Customer {id: $id})
        RETURN c.balance >= $amount AS sufficient
    """)
    result = tx.run(query, id=customer_id, amount=amount)
    record = result.single(strict=True)
    return record["sufficient"]

def other_bank_transfer_api(customer_id, other_bank_id, amount):
    # make some API call to other bank
    pass

def decrease_customer_balance(tx, customer_id, amount):
    query = ("""
        MATCH (c:Customer {id: $id})
        SET c.balance = c.balance - $amount
    """)
    result = tx.run(query, id=customer_id, amount=amount)
    result.consume()

def request_inspection(customer_id, other_bank_id, amount, e):
    # manual cleanup required; log this or similar
    print("WARNING: transaction rolled back due to exception:", repr(e))
    print("customer_id:", customer_id, "other_bank_id:", other_bank_id,
          "amount:", amount)

if     main()
```

## Process query results

The driver’s output of a query is a [`Result`](/docs/api/python-driver/current/api.html#neo4j.Result) object, which encapsulates the Cypher result in a rich data structure that requires some parsing on the client side.
There are two main points to be aware of:

* **The result records are not immediately and entirely fetched and returned by the server**.
  Instead, results come as a *lazy stream*.
  In particular, when the driver receives some records from the server, they are initially *buffered* in a background queue.
  Records stay in the buffer until they are *consumed* by the application, at which point they are *removed from the buffer*.
  When no more records are available, the result is *exhausted*.
* **The result acts as a *cursor***.
  This means that there is no way to retrieve a previous record from the stream, unless you saved it in an auxiliary data structure.

The animation below follows the path of a single query: it shows how the driver works with result records and how the application should handle results.

[!](../../../common-content/5/_images/result.mp4)

**The easiest way of processing a result is by casting it to list**, which yields a list of [`Record`](/docs/api/python-driver/current/api.html#neo4j.Record) objects.
Otherwise, a `Result` object implements a number of methods for processing records.
The most commonly needed ones are listed below.

| Name | Description |
| --- | --- |
| `value(key=0, default=None)` | Return the remainder of the result as a list. If `key` is specified, only the given property is included; `default` allows to specify a value for nodes lacking that property. |
| `fetch(n)` | Return up to `n` records from the result. |
| `single(strict=False)` | Return the next and only remaining record, or `None`. Calling this method always exhausts the result.  If more (or less) than one record is available,  * `strict==False` — a warning is generated and the first of these is returned (if any); * `strict==True` — a [`ResultNotSingleError`](https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.exceptions.ResultNotSingleError) is raised. |
| `peek()` | Return the next record without consuming it. This leaves the record in the buffer for further processing. |
| `data(*keys)` | Return a JSON-like dump . Only use it for debugging/prototyping purposes. |
| `consume()` | Return the query [result summary](../result-summary/). It exhausts the result, so should only be called when data processing is over. |
| `graph()` | Transform result into a collection of graph objects. See [Transform to graph](../transformers/#_transform_to_graph). |
| `to_df(expand, parse_dates)` | Transform result into a Pandas Dataframe. See [Transform to Pandas Dataframe](../transformers/#_transform_to_pandas_dataframe). |

For a complete list of `Result` methods, see [API documentation — Result](/docs/api/python-driver/current/api.html#result).

## Session configuration

### Database selection

**Always specify the database explicitly** with the `database` parameter, even on single-database instances.
This allows the driver to work more efficiently, as it saves a network round-trip to the server to resolve the home database.
If no database is given, the [user’s home database](/docs/operations-manual/current/database-administration/#manage-databases-default) is used.

```
with driver.session(
    database="<database-name>"
) as session:
    ...
```

|  |  |
| --- | --- |
|  | Specifying the database through the configuration method is preferred over the [`USE`](/docs/cypher-manual/current/clauses/use/) Cypher clause. If the server runs on a cluster, queries with `USE` require [server-side routing](https://neo4j.com/docs/operations-manual/current/clustering/setup/routing/#clustering-routing) to be enabled. Queries may also take longer to execute as they may not reach the right cluster member at the first attempt, and need to be routed to one containing the requested database. |

### Request routing

In a cluster environment, all sessions are opened in write mode, routing them to the leader.
You can change this by explicitly setting the `default_access_mode` parameter to `neo4j.READ_ACCESS`.
Note that `.execute_read()` and `.execute_write()` automatically override the session’s default access mode.

```
import neo4j

with driver.session(
    database="<database-name>",
    default_access_mode=neo4j.READ_ACCESS
) as session:
    ...
```

|  |  |
| --- | --- |
|  | Although executing a *write* query in read mode results in a runtime error, **you should not rely on this for access control.** The difference between the two modes is that *read* transactions will be routed to any node of a cluster, whereas *write* ones are directed to primaries. There is no security guarantee that a write query submitted in read mode will be rejected. |

### Run queries as a different user

You can execute a query through a different user with the parameter `auth`.
Switching user at the session level is cheaper than creating a new `Driver` object.
Queries are then run within the security context of the given user (i.e., home database, permissions, etc.).

```
with driver.session(
    database="<database-name>",
    auth=("<username>", "<password>")
) as session:
    ...
```

The parameter `impersonated_user` provides a similar functionality.
The difference is that you don’t need to know a user’s password to impersonate them, but the user under which the `Driver` was created needs to have the [appropriate permissions](https://neo4j.com/docs/operations-manual/current/authentication-authorization/dbms-administration/dbms-impersonate-privileges/).

```
with driver.session(
    database="<database-name>",
    impersonated_user="<username>"
) as session:
    ...
```

## Close sessions

Each connection pool has **a finite number of sessions**, so if you open sessions without ever closing them, your application could run out of them.
It is thus recommended to create sessions using the `with` statement, which automatically closes them when the application is done with them.
When a session is closed, it is returned to the connection pool to be later reused.

If you do not use `with`, remember to call the `.close()` method when you have finished using a session.

```
session = driver.session(database="<database-name>")

# session usage

session.close()
```

## Glossary

LTS
:   A *Long Term Support* release is one guaranteed to be supported for a number of years.
    Neo4j 4.4 and 5.26 are LTS versions.

Aura
:   [Aura](https://neo4j.com/product/auradb/) is Neo4j’s fully managed cloud service.
    It comes with both free and paid plans.

Cypher
:   [Cypher](https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/) is Neo4j’s graph query language that lets you retrieve data from the database.
    It is like SQL, but for graphs.

APOC
:   [Awesome Procedures On Cypher (APOC)](/docs/apoc/current/) is a library of (many) functions that can not be easily expressed in Cypher itself.

Bolt
:   [Bolt](/docs/bolt/current/) is the protocol used for interaction between Neo4j instances and drivers.
    It listens on port 7687 by default.

ACID
:   Atomicity, Consistency, Isolation, Durability (ACID) are properties guaranteeing that database transactions are processed reliably.
    An ACID-compliant DBMS ensures that the data in the database remains accurate and consistent despite failures.

eventual consistency
:   A database is eventually consistent if it provides the guarantee that all cluster members will, *at some point in time*, store the latest version of the data.

causal consistency
:   A database is causally consistent if read and write queries are seen by every member of the cluster in the same order.
    This is stronger than *eventual consistency*.

NULL
:   The null marker is not a type but a placeholder for absence of value.
    For more information, see [Cypher → Working with `null`](/docs/cypher-manual/current/values-and-types/working-with-null/).

transaction
:   A transaction is a unit of work that is either *committed* in its entirety or *rolled back* on failure.
    An example is a bank transfer: it involves multiple steps, but they must *all* succeed or be reverted, to avoid money being subtracted from one account but not added to the other.

backpressure
:   Backpressure is a force opposing the flow of data. It ensures that the client is not being overwhelmed by data faster than it can handle.

bookmark
:   A *bookmark* is a token representing some state of the database. By passing one or multiple bookmarks along with a query, the server will make sure that the query does not get executed before the represented state(s) have been established.

transaction function
:   A transaction function is a callback executed by an `execute_read` or `execute_write` call. The driver automatically re-executes the callback in case of server failure.

Driver
:   A [`Driver`](/docs/api/python-driver/current/api.html#neo4j.Driver) object holds the details required to establish connections with a Neo4j database.

---

## 3. Loop through results and do something with them

Once you have [connected to the database](../connect/), you can run queries using [Cypher](#Cypher) and the method `Driver.execute_query()`.

## Write to the database

To create two nodes representing persons named `Alice` and `David`, and a relationship `KNOWS` between them, use the Cypher clause [`CREATE`](/docs/cypher-manual/current/clauses/create/):

Create two nodes and a relationship

```
summary = driver.execute_query(""" (1)
    CREATE (a:Person {name: $name})
    CREATE (b:Person {name: $friendName})
    CREATE (a)-[:KNOWS]->(b)
    """,
    name="Alice", friendName="David",  (2)
    database_="<database-name>",  (3)
).summary
print("Created {nodes_created} nodes in {time} ms.".format(
    nodes_created=summary.counters.nodes_created,
    time=summary.result_available_after
))
```

|  |  |
| --- | --- |
| **1** | The Cypher query |
| **2** | The *query parameters*, as keyword arguments |
| **3** | The database to run the query on |

## Read from the database

To retrieve information from the database, use the Cypher clause [`MATCH`](/docs/cypher-manual/current/clauses/match/):

Retrieve all `Person` nodes who like other `Person` s

```
records, summary, keys = driver.execute_query("""
    MATCH (p:Person)-[:KNOWS]->(:Person)
    RETURN p.name AS name
    """,
    database_="<database-name>",
)

# Loop through results and do something with them
for record in records:  (1)
    print(record.data())  # get record as dict

# Summary information  (2)
print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after
))
```

|  |  |
| --- | --- |
| **1** | `records` contains the result as an array of `Record` objects |
| **2** | `summary` contains the [summary of execution](../result-summary/) returned by the server |

## Update the database

To update an entity’s information in the database, use the Cypher clauses [`MATCH`](/docs/cypher-manual/current/clauses/match/) and [`SET`](/docs/cypher-manual/current/clauses/set/):

Update node `Alice` to add an `age` property

```
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    SET p.age = $age
    """, name="Alice", age=42,
    database_="<database-name>",
)
print(f"Query counters: {summary.counters}.")
```

To create a new relationship, linking it to two already existing node, use a combination of the Cypher clauses `MATCH` and `CREATE`:

Create a relationship `:KNOWS` between `Alice` and `Bob`

```
records, summary, keys = driver.execute_query("""
    MATCH (alice:Person {name: $name})  (1)
    MATCH (bob:Person {name: $friend})  (2)
    CREATE (alice)-[:KNOWS]->(bob)  (3)
    """, name="Alice", friend="Bob",
    database_="<database-name>",
)
print(f"Query counters: {summary.counters}.")
```

|  |  |
| --- | --- |
| **1** | Retrieve the person node named `Alice` and bind it to a variable `alice` |
| **2** | Retrieve the person node named `Bob` and bind it to a variable `bob` |
| **3** | Create a new `:KNOWS` relationship outgoing from the node bound to `alice` and attach to it the `Person` node named `Bob` |

## Delete from the database

To remove a node and any relationship attached to it, use the Cypher clause [`DETACH DELETE`](/docs/cypher-manual/current/clauses/delete/):

Remove the `Alice` node

```
# This does not delete _only_ p, but also all its relationships!
records, summary, keys = driver.execute_query("""
    MATCH (p:Person {name: $name})
    DETACH DELETE p
    """, name="Alice",
    database_="<database-name>",
)
print(f"Query counters: {summary.counters}.")
```

## Query parameters

**Do not hardcode or concatenate parameters directly into queries**.
Instead, always use placeholders and provide dynamic data as [Cypher parameters](/docs/cypher-manual/current/syntax/parameters/).
This is for:

1. **performance benefits**: Neo4j compiles and caches queries, but can only do so if the query structure is unchanged;
2. **security reasons**: see [protecting against Cypher injection](https://neo4j.com/developer/kb/protecting-against-cypher-injection/).

Query parameters can be passed either as several keyword arguments, or grouped together in a dictionary passed as value to the `parameters_` keyword argument. In case of mix, keyword-argument parameters take precedence over dictionary ones.

Pass query parameters as keyword arguments

```
driver.execute_query(
    "MERGE (:Person {name: $name})",
    name="Alice", age=42,
    database_="<database-name>",
)
```

Pass query parameters in a dictionary

```
parameters = {
    "name": "Alice",
    "age": 42
}
driver.execute_query(
    "MERGE (:Person {name: $name})",
    parameters_=parameters,
    database_="<database-name>",
)
```

**None of your keyword query parameters may end with a single underscore.** This is to avoid collisions with the [keyword configuration parameters](#_query_configuration). If you need to use such parameter names, pass them in the `parameters_` dictionary.

|  |  |
| --- | --- |
|  | There can be circumstances where your query structure prevents the usage of parameters in all its parts. For those rare use cases, see [Dynamic values in property keys, relationship types, and labels](../query-advanced/#_dynamic_values_in_property_keys_relationship_types_and_labels). |

## Error handling

A query run may fail for a number of reasons, with different [exceptions](https://neo4j.com/docs/api/python-driver/current/api.html#errors) being raised.
When using `driver.execute_query()`, the driver automatically retries to run a failed query if the failure is deemed to be transient (for example due to temporary server unavailability).

An exception will be raised if the operation keeps failing after the configured [maximum retry time](https://neo4j.com/docs/api/python-driver/current/api.html#max-transaction-retry-time-ref).

All exceptions coming from the server are subclasses of [`Neo4jError`](https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.exceptions.Neo4jError).
You can use an exception’s code to stably identify a specific error; error messages are instead not stable markers, and should not be relied upon.

Basic error handling

```
# from neo4j.exceptions import Neo4jError

try:
    driver.execute_query('MATCH (p:Person) RETURN', database_='<database-name>')
except Neo4jError as e:
    print('Neo4j error code:', e.code)
    print('Exception message:', e.message)
'''
Neo4j error code: Neo.ClientError.Statement.SyntaxError
Exception message: Invalid input '': expected an expression, '*', 'ALL' or 'DISTINCT' (line 1, column 24 (offset: 23))
"MATCH (p:Person) RETURN"
                        ^
'''
```

Exception objects also expose errors as GQL-status objects.
The main difference between [Neo4j error codes](https://neo4j.com/docs/status-codes/current/errors/all-errors/) and [GQL error codes](https://neo4j.com/docs/status-codes/current/errors/gql-errors/) is that the GQL ones are more granular: a single Neo4j error code might be broken in several, more specific GQL error codes.

The actual *cause* that triggered an exception is sometimes found in the optional GQL-status object `__cause__`, which is itself an exception (or `None`).
You might need to recursively traverse the cause chain before reaching the root cause of the exception you caught.
In the example below, the exception’s GQL status code is `42001`, but the actual source of the error has status code `42I06`.

Usage of `Neo4jError` with GQL-related methods

```
# from neo4j.exceptions import Neo4jError

try:
    driver.execute_query('MATCH (p:Person) RETURN', database_='<database-name>')
except Neo4jError as e:
    print('Exception GQL status:', e.gql_status)
    print('Exception GQL status description:', e.gql_status_description)
    print('Exception GQL classification:', e.gql_classification)
    print('Exception GQL cause:', e.__cause__)
    print('Exception GQL diagnostic record:', e.diagnostic_record)
'''
Exception GQL status: 42001
Exception GQL status description: error: syntax error or access rule violation - invalid syntax
Exception GQL classification: GqlErrorClassification.CLIENT_ERROR
Exception GQL cause: {gql_status: 42I06} {gql_status_description: error: syntax error or access rule violation - invalid input. Invalid input '', expected: an expression, '*', 'ALL' or 'DISTINCT'.} {message: 42I06: Invalid input '', expected: an expression, '*', 'ALL' or 'DISTINCT'.} {diagnostic_record: {'_classification': 'CLIENT_ERROR', '_position': {'line': 1, 'column': 24, 'offset': 23}, 'OPERATION': '', 'OPERATION_CODE': '0', 'CURRENT_SCHEMA': '/'}} {raw_classification: CLIENT_ERROR}
Exception GQL diagnostic record: {'_classification': 'CLIENT_ERROR', '_position': {'line': 1, 'column': 24, 'offset': 23}, 'OPERATION': '', 'OPERATION_CODE': '0', 'CURRENT_SCHEMA': '/'}
'''
```

GQL status codes are particularly helpful when you want your application to behave differently depending on the exact error that was raised by the server.

Distinguishing between different error codes

```
# from neo4j.exceptions import Neo4jError

try:
    driver.execute_query('MATCH (p:Person) RETURN', database_='<database-name>')
except Neo4jError as e:
    if e.find_by_gql_status('42001'):
        # Neo.ClientError.Statement.SyntaxError
        # special handling of syntax error in query
        print(e.message)
    elif e.find_by_gql_status('42NFF'):
        # Neo.ClientError.Security.Forbidden
        # special handling of user not having CREATE permissions
        print(e.message)
    else:
        # handling of all other exceptions
        print(e.message)
```

|  |  |
| --- | --- |
|  | The GQL status code `50N42` is returned when an exception does not have a GQL-status object. This can happen if the driver is connected to an older Neo4j server. Don’t rely on this status code, as future Neo4j server versions might change it with a more appropriate one. |

|  |  |
| --- | --- |
|  | Transient server errors can be retried without need to alter the original request. You can discover whether an error is transient via the method `Neo4jError.is_retryable()`, which gives insights into whether a further attempt might be successful. This is particular useful when running queries in [explicit transactions](../transactions/#explicit-transactions), to know if a failed query is worth re-running. |

## Query configuration

You can supply further keyword arguments to alter the default behavior of `.execute_query()`.
Configuration parameters are suffixed with `_`.

### Database selection

**Always specify the database explicitly** with the `database_` parameter, even on single-database instances.
This allows the driver to work more efficiently, as it saves a network round-trip to the server to resolve the home database.
If no database is given, the [user’s home database](/docs/operations-manual/current/database-administration/#manage-databases-default) is used.

```
driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    database_="<database-name>",
)
```

|  |  |
| --- | --- |
|  | Specifying the database through the configuration method is preferred over the [`USE`](/docs/cypher-manual/current/clauses/use/) Cypher clause. If the server runs on a cluster, queries with `USE` require [server-side routing](https://neo4j.com/docs/operations-manual/current/clustering/setup/routing/#clustering-routing) to be enabled. Queries can also take longer to execute as they may not reach the right cluster member at the first attempt, and need to be routed to one containing the requested database. |

### Request routing

In a cluster environment, all queries are directed to the leader node by default.
To improve performance on read queries, you can use the argument `routing_="r"` to route a query to the read nodes.

```
driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    routing_="r",  # short for neo4j.RoutingControl.READ
    database_="<database-name>",
)
```

|  |  |
| --- | --- |
|  | Although executing a *write* query in read mode results in a runtime error, **you should not rely on this for access control.** The difference between the two modes is that *read* transactions will be routed to any node of a cluster, whereas *write* ones are directed to primaries. There is no security guarantee that a write query submitted in read mode will be rejected. |

### Run queries as a different user

You can execute a query through a different user with the parameter `auth_`.
Switching user at the query level is cheaper than creating a new `Driver` object.
The query is then run within the security context of the given user (i.e., home database, permissions, etc.).

```
driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    auth_=("<username>", "<password>"),
    database_="<database-name>",
)
```

The parameter `impersonated_user_` provides a similar functionality.
The difference is that you don’t need to know a user’s password to impersonate them, but the user under which the `Driver` was created needs to have the [appropriate permissions](https://neo4j.com/docs/operations-manual/current/authentication-authorization/dbms-administration/dbms-impersonate-privileges/).

```
driver.execute_query(
    "MATCH (p:Person) RETURN p.name",
    impersonated_user_="<username>",
    database_="<database-name>",
)
```

### Transform query result

You can transform a query’s result into a different data structure using the `result_transformer_` argument.
The driver provides built-in methods to transform the result into a pandas dataframe or into a graph, but you can also craft your own transformer.

For more information, see [Manipulate query results](../transformers/).

## A full example

```
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

URI = "<database-uri>"
AUTH = ("<username>", "<password>")

people = [{"name": "Alice", "age": 42, "friends": ["Bob", "Peter", "Anna"]},
          {"name": "Bob", "age": 19},
          {"name": "Peter", "age": 50},
          {"name": "Anna", "age": 30}]

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    try:
        # Create some nodes
        for person in people:
            records, summary, keys = driver.execute_query(
                "MERGE (p:Person {name: $person.name, age: $person.age})",
                person=person,
                database_="<database-name>",
            )

        # Create some relationships
        for person in people:
            if person.get("friends"):
                records, summary, keys = driver.execute_query("""
                    MATCH (p:Person {name: $person.name})
                    UNWIND $person.friends AS friend_name
                    MATCH (friend:Person {name: friend_name})
                    MERGE (p)-[:KNOWS]->(friend)
                    """, person=person,
                    database_="<database-name>",
                )

        # Retrieve Alice's friends who are under 40
        records, summary, keys = driver.execute_query("""
            MATCH (p:Person {name: $name})-[:KNOWS]-(friend:Person)
            WHERE friend.age < $age
            RETURN friend
            """, name="Alice", age=40,
            routing_="r",
            database_="<database-name>",
        )
        # Loop through results and do something with them
        for record in records:
            print(record)
        # Summary information
        print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

    except Neo4jError as e:
        print(e)
        # further logging/processing
```

For more information see [API documentation → Driver.execute\_query()](/docs/api/python-driver/current/api.html#neo4j.Driver.execute_query).

## Glossary

LTS
:   A *Long Term Support* release is one guaranteed to be supported for a number of years.
    Neo4j 4.4 and 5.26 are LTS versions.

Aura
:   [Aura](https://neo4j.com/product/auradb/) is Neo4j’s fully managed cloud service.
    It comes with both free and paid plans.

Cypher
:   [Cypher](https://neo4j.com/docs/cypher-manual/current/introduction/cypher-overview/) is Neo4j’s graph query language that lets you retrieve data from the database.
    It is like SQL, but for graphs.

APOC
:   [Awesome Procedures On Cypher (APOC)](/docs/apoc/current/) is a library of (many) functions that can not be easily expressed in Cypher itself.

Bolt
:   [Bolt](/docs/bolt/current/) is the protocol used for interaction between Neo4j instances and drivers.
    It listens on port 7687 by default.

ACID
:   Atomicity, Consistency, Isolation, Durability (ACID) are properties guaranteeing that database transactions are processed reliably.
    An ACID-compliant DBMS ensures that the data in the database remains accurate and consistent despite failures.

eventual consistency
:   A database is eventually consistent if it provides the guarantee that all cluster members will, *at some point in time*, store the latest version of the data.

causal consistency
:   A database is causally consistent if read and write queries are seen by every member of the cluster in the same order.
    This is stronger than *eventual consistency*.

NULL
:   The null marker is not a type but a placeholder for absence of value.
    For more information, see [Cypher → Working with `null`](/docs/cypher-manual/current/values-and-types/working-with-null/).

transaction
:   A transaction is a unit of work that is either *committed* in its entirety or *rolled back* on failure.
    An example is a bank transfer: it involves multiple steps, but they must *all* succeed or be reverted, to avoid money being subtracted from one account but not added to the other.

backpressure
:   Backpressure is a force opposing the flow of data. It ensures that the client is not being overwhelmed by data faster than it can handle.

bookmark
:   A *bookmark* is a token representing some state of the database. By passing one or multiple bookmarks along with a query, the server will make sure that the query does not get executed before the represented state(s) have been established.

transaction function
:   A transaction function is a callback executed by an `execute_read` or `execute_write` call. The driver automatically re-executes the callback in case of server failure.

Driver
:   A [`Driver`](/docs/api/python-driver/current/api.html#neo4j.Driver) object holds the details required to establish connections with a Neo4j database.

---

## Bibliography

1. [URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"](https://neo4j.com/docs/python-manual/current/)
2. [session usage](https://neo4j.com/docs/python-manual/current/transactions/)
3. [Loop through results and do something with them](https://neo4j.com/docs/python-manual/current/query-simple/)