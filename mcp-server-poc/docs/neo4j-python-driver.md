(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-WK23PSS');
Build applications with Neo4j and Python - Neo4j Python Driver Manual

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

Neo4j Python Driver Manual

Product Version

Version 6 (Current)

Version 5

Version 4.4

* + [Quickstart](./)
  + **Regular workflow**
  + [Installation](install/)
  + [Connect to the database](connect/)
  + [Query the database](query-simple/)
  + [Manipulate query results](transformers/)
  + **Advanced usage**
  + [Run your own transactions](transactions/)
  + [Explore the query execution summary](result-summary/)
  + [Coordinate parallel transactions](bookmarks/)
  + [Run concurrent transactions](concurrency/)
  + [Further query mechanisms](query-advanced/)
  + [Performance recommendations](performance/)
  + **Reference**
  + [Advanced connection information](connect-advanced/)
  + [Data types and mapping to Cypher types](data-types/)
  + [Upgrade from older versions](upgrade/)
  + [API documentation](https://neo4j.com/docs/api/python-driver/6.0/)
  + **GraphAcademy courses**
  + [Graph Data Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/?ref=docs-python)
  + [Intermediate Cypher Queries](https://graphacademy.neo4j.com/courses/cypher-intermediate-queries/?ref=docs-python)
  + [Building Neo4j Applications with Python](https://graphacademy.neo4j.com/courses/app-python/?ref=docs-python)

**Is this page helpful?**

* [Neo4j Python Driver Manual](./)
* [Quickstart](./)

[Raise an issue](https://github.com/neo4j/docs-drivers/issues/new/?title=Docs%20Feedback%20python-manual/modules/ROOT/pages/index.adoc%20(ref:%206.x)&body=%3E%20Do%20not%20include%20confidential%20information,%20personal%20data,%20sensitive%20data,%20or%20other%20regulated%20data.)

# Build applications with Neo4j and Python

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

[Installation](install/)

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