# LanceDB Python API


---

## 1. Python API Reference

This section contains the API reference for the Python API of [LanceDB](https://github.com/lancedb/lancedb). Both synchronous and asynchronous APIs are available.

The general flow of using the API is:

1. Use [lancedb.connect](#lancedb.connect) or [lancedb.connect\_async](#lancedb.connect_async) to connect to a database.
2. Use the returned [lancedb.DBConnection](#lancedb.db.DBConnection) or [lancedb.AsyncConnection](#lancedb.db.AsyncConnection) to
   create or open tables.
3. Use the returned [lancedb.table.Table](#lancedb.table.Table) or [lancedb.AsyncTable](#lancedb.table.AsyncTable) to query
   or modify tables.

## Installation

```
pipinstalllancedb
```

The following methods describe the synchronous API client. There
is also an [asynchronous API client](#connections-asynchronous).

## Connections (Synchronous)

### lancedb.connect

```
connect(uri: Optional[URI] = None, *, api_key: Optional[str] = None, region: str = 'us-east-1', host_override: Optional[str] = None, read_consistency_interval: Optional[timedelta] = None, request_thread_pool: Optional[Union[int, ThreadPoolExecutor]] = None, client_config: Union[ClientConfig, Dict[str, Any], None] = None, storage_options: Optional[Dict[str, str]] = None, session: Optional[Session] = None, namespace_client_impl: Optional[str] = None, namespace_client_properties: Optional[Dict[str, str]] = None, namespace_client_pushdown_operations: Optional[List[str]] = None, **kwargs: Any) -> DBConnection
```

Connect to a LanceDB database.

Parameters:

* **`uri`**
  (`Optional[URI]`, default:
  `None`
  )
  –

  The uri of the database. When `namespace_client_impl` is provided you may
  omit `uri` and connect through a namespace client instead.
* **`api_key`**
  (`Optional[str]`, default:
  `None`
  )
  –

  If presented, connect to LanceDB cloud.
  Otherwise, connect to a database on file system or cloud storage.
  Can be set via environment variable `LANCEDB_API_KEY`.
* **`region`**
  (`str`, default:
  `'us-east-1'`
  )
  –

  The region to use for LanceDB Cloud.
* **`host_override`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The override url for LanceDB Cloud.
* **`read_consistency_interval`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  (For LanceDB OSS only)
  The interval at which to check for updates to the table from other
  processes. If None, then consistency is not checked. For performance
  reasons, this is the default. For strong consistency, set this to
  zero seconds. Then every read will check for updates from other
  processes. As a compromise, you can set this to a non-zero timedelta
  for eventual consistency. If more than that interval has passed since
  the last check, then the table will be checked for updates. Note: this
  consistency only applies to read operations. Write operations are
  always consistent.
* **`client_config`**
  (`Union[ClientConfig, Dict[str, Any], None]`, default:
  `None`
  )
  –

  Configuration options for the LanceDB Cloud HTTP client. If a dict, then
  the keys are the attributes of the ClientConfig class. If None, then the
  default configuration is used.
* **`storage_options`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Additional options for the storage backend. See available options at
  <https://lancedb.com/docs/storage/>
* **`session`**
  (`Optional[Session]`, default:
  `None`
  )
  –

  (For LanceDB OSS only)
  A session to use for this connection. Sessions allow you to configure
  cache sizes for index and metadata caches, which can significantly
  impact memory use and performance. They can also be re-used across
  multiple connections to share the same cache state.
* **`namespace_client_impl`**
  (`str`, default:
  `None`
  )
  –

  When provided along with `namespace_client_properties`, `connect`
  returns a namespace-backed connection by delegating to
  :func:`connect_namespace`. The value identifies which namespace
  implementation to load (e.g., `"dir"` or `"rest"`).
* **`namespace_client_properties`**
  (`dict`, default:
  `None`
  )
  –

  Configuration to pass to the namespace client implementation. Required
  when `namespace_client_impl` is set.
* **`namespace_client_pushdown_operations`**
  (`list[str]`, default:
  `None`
  )
  –

  Only used when `namespace_client_properties` is provided. Forwards to
  :func:`connect_namespace` to control which operations are executed on the
  namespace service (e.g., `["QueryTable", "CreateTable"]`).

Examples:

For a local directory, provide a path for the database:

```
>>> importlancedb
>>> db = lancedb.connect("~/.lancedb")
```

For object storage, use a URI prefix:

```
>>> db = lancedb.connect("s3://my-bucket/lancedb",
...                      storage_options={"aws_access_key_id": "***"})
```

Connect to LanceDB cloud:

```
>>> db = lancedb.connect("db://my_database", api_key="ldb_...",
...                      client_config={"retry_config": {"retries": 5}})
```

Connect to a namespace-backed database:

```
>>> db = lancedb.connect(namespace_client_impl="dir",
...                      namespace_client_properties={"root": "/tmp/ns"})
```

Returns:

* **`conn`** ( `DBConnection`
  ) –

  A connection to a LanceDB database.

### lancedb.db.DBConnection

Bases: `EnforceOverrides`

An active LanceDB connection interface.

#### uri

```
uri: str
```

#### list\_namespaces

```
list_namespaces(namespace_path: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListNamespacesResponse
```

List immediate child namespace names in the given namespace.

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The parent namespace to list namespaces in.
  Empty list represents root namespace.
* **`page_token`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Token for pagination. Use the token from a previous response
  to get the next page of results.
* **`limit`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of results to return.

Returns:

* `ListNamespacesResponse`
  –

  Response containing namespace names and optional page\_token for pagination.

#### create\_namespace

```
create_namespace(namespace_path: List[str], mode: Optional[str] = None, properties: Optional[Dict[str, str]] = None) -> CreateNamespaceResponse
```

Create a new namespace.

Parameters:

* **`namespace_path`**
  (`List[str]`)
  –

  The namespace identifier to create.
* **`mode`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Creation mode - "create" (fail if exists), "exist\_ok" (skip if exists),
  or "overwrite" (replace if exists). Case insensitive.
* **`properties`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Properties to set on the namespace.

Returns:

* `CreateNamespaceResponse`
  –

  Response containing the properties of the created namespace.

#### drop\_namespace

```
drop_namespace(namespace_path: List[str], mode: Optional[str] = None, behavior: Optional[str] = None) -> DropNamespaceResponse
```

Drop a namespace.

Parameters:

* **`namespace_path`**
  (`List[str]`)
  –

  The namespace identifier to drop.
* **`mode`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.
* **`behavior`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
  Case insensitive.

Returns:

* `DropNamespaceResponse`
  –

  Response containing properties and transaction\_id if applicable.

#### describe\_namespace

```
describe_namespace(namespace_path: List[str]) -> DescribeNamespaceResponse
```

Describe a namespace.

Parameters:

* **`namespace_path`**
  (`List[str]`)
  –

  The namespace identifier to describe.

Returns:

* `DescribeNamespaceResponse`
  –

  Response containing the namespace properties.

#### list\_tables

```
list_tables(namespace_path: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListTablesResponse
```

List all tables in this database with pagination support.

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to list tables in.
  None or empty list represents root namespace.
* **`page_token`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Token for pagination. Use the token from a previous response
  to get the next page of results.
* **`limit`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of results to return.

Returns:

* `ListTablesResponse`
  –

  Response containing table names and optional page\_token for pagination.

#### table\_names

```
table_names(page_token: Optional[str] = None, limit: int = 10, *, namespace_path: Optional[List[str]] = None) -> Iterable[str]
```

List all tables in this database, in sorted order

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to list tables in.
  Empty list represents root namespace.
* **`page_token`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The token to use for pagination. If not present, start from the beginning.
  Typically, this token is last table name from the previous page.
* **`limit`**
  (`int`, default:
  `10`
  )
  –

  The size of the page to return.

Returns:

* `Iterable of str`
  –

#### create\_table

```
create_table(name: str, data: Optional[DATA] = None, schema: Optional[Union[Schema, LanceModel]] = None, mode: str = 'create', exist_ok: bool = False, on_bad_vectors: str = 'error', fill_value: float = 0.0, embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None, *, namespace_path: Optional[List[str]] = None, storage_options: Optional[Dict[str, str]] = None, data_storage_version: Optional[str] = None, enable_v2_manifest_paths: Optional[bool] = None) -> Table
```

Create a [Table](#lancedb.table.Table) in the database.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the table.
* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to create the table in.
  Empty list represents root namespace.
* **`data`**
  (`Optional[DATA]`, default:
  `None`
  )
  –

  User must provide at least one of `data` or `schema`.
  Acceptable types are:

  + list-of-dict
  + pandas.DataFrame
  + pyarrow.Table or pyarrow.RecordBatch
* **`schema`**
  (`Optional[Union[Schema, LanceModel]]`, default:
  `None`
  )
  –

  Acceptable types are:

  + pyarrow.Schema
  + [LanceModel](#lancedb.pydantic.LanceModel)
* **`mode`**
  (`str`, default:
  `'create'`
  )
  –

  The mode to use when creating the table.
  Can be either "create" or "overwrite".
  By default, if the table already exists, an exception is raised.
  If you want to overwrite the table, use mode="overwrite".
* **`exist_ok`**
  (`bool`, default:
  `False`
  )
  –

  If a table by the same name already exists, then raise an exception
  if exist\_ok=False. If exist\_ok=True, then open the existing table;
  it will not add the provided data but will validate against any
  schema that's specified.
* **`on_bad_vectors`**
  (`str`, default:
  `'error'`
  )
  –

  What to do if any of the vectors are not the same size or contains NaNs.
  One of "error", "drop", "fill".
* **`fill_value`**
  (`float`, default:
  `0.0`
  )
  –

  The value to use when filling vectors. Only used if on\_bad\_vectors="fill".
* **`storage_options`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Additional options for the storage backend. Options already set on the
  connection will be inherited by the table, but can be overridden here.
  See available options at
  <https://lancedb.com/docs/storage/>

  To enable stable row IDs (row IDs remain stable after compaction,
  update, delete, and merges), set `new_table_enable_stable_row_ids`
  to `"true"` in storage\_options when connecting to the database.
* **`data_storage_version`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Deprecated. Set `storage_options` when connecting to the database and set
  `new_table_data_storage_version` in the options.
* **`enable_v2_manifest_paths`**
  (`Optional[bool]`, default:
  `None`
  )
  –

  Deprecated. Set `storage_options` when connecting to the database and set
  `new_table_enable_v2_manifest_paths` in the options.

Returns:

* `LanceTable`
  –

  A reference to the newly created table.
* `!!! note`
  –

  The vector index won't be created by default.
  To create the index, call the `create_index` method on the table.

Examples:

Can create with list of tuples or dictionaries:

```
>>> importlancedb
>>> db = lancedb.connect("./.lancedb")
>>> data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
...         {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
>>> db.create_table("my_table", data)
LanceTable(name='my_table', version=1, ...)
>>> db["my_table"].head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]
```

You can also pass a pandas DataFrame:

```
>>> importpandasaspd
>>> data = pd.DataFrame({
...    "vector": [[1.1, 1.2], [0.2, 1.8]],
...    "lat": [45.5, 40.1],
...    "long": [-122.7, -74.1]
... })
>>> db.create_table("table2", data)
LanceTable(name='table2', version=1, ...)
>>> db["table2"].head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]
```

Data is converted to Arrow before being written to disk. For maximum
control over how data is saved, either provide the PyArrow schema to
convert to or else provide a [PyArrow Table](pyarrow.Table) directly.

```
>>> importpyarrowaspa
>>> custom_schema = pa.schema([
...   pa.field("vector", pa.list_(pa.float32(), 2)),
...   pa.field("lat", pa.float32()),
...   pa.field("long", pa.float32())
... ])
>>> db.create_table("table3", data, schema = custom_schema)
LanceTable(name='table3', version=1, ...)
>>> db["table3"].head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: float
long: float
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]
```

It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

```
>>> importpyarrowaspa
>>> defmake_batches():
...     for i in range(5):
...         yield pa.RecordBatch.from_arrays(
...             [
...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
...                     pa.list_(pa.float32(), 2)),
...                 pa.array(["foo", "bar"]),
...                 pa.array([10.0, 20.0]),
...             ],
...             ["vector", "item", "price"],
...         )
>>> schema=pa.schema([
...     pa.field("vector", pa.list_(pa.float32(), 2)),
...     pa.field("item", pa.utf8()),
...     pa.field("price", pa.float32()),
... ])
>>> db.create_table("table4", make_batches(), schema=schema)
LanceTable(name='table4', version=1, ...)
```

#### open\_table

```
open_table(name: str, *, namespace_path: Optional[List[str]] = None, storage_options: Optional[Dict[str, str]] = None, index_cache_size: Optional[int] = None) -> Table
```

Open a Lance Table in the database.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the table.
* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to open the table from.
  None or empty list represents root namespace.
* **`index_cache_size`**
  (`Optional[int]`, default:
  `None`
  )
  –

  **Deprecated**: Use session-level cache configuration instead.
  Create a Session with custom cache sizes and pass it to lancedb.connect().

  Set the size of the index cache, specified as a number of entries

  The exact meaning of an "entry" will depend on the type of index:
  \* IVF - there is one entry for each IVF partition
  \* BTREE - there is one entry for the entire index

  This cache applies to the entire opened table, across all indices.
  Setting this value higher will increase performance on larger datasets
  at the expense of more RAM
* **`storage_options`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Additional options for the storage backend. Options already set on the
  connection will be inherited by the table, but can be overridden here.
  See available options at
  <https://lancedb.com/docs/storage/>

Returns:

* `A LanceTable object representing the table.`
  –

#### drop\_table

```
drop_table(name: str, namespace_path: Optional[List[str]] = None)
```

Drop a table from the database.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the table.
* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to drop the table from.
  Empty list represents root namespace.

#### rename\_table

```
rename_table(cur_name: str, new_name: str, cur_namespace_path: Optional[List[str]] = None, new_namespace_path: Optional[List[str]] = None)
```

Rename a table in the database.

Parameters:

* **`cur_name`**
  (`str`)
  –

  The current name of the table.
* **`new_name`**
  (`str`)
  –

  The new name of the table.
* **`cur_namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace of the current table.
  None or empty list represents root namespace.
* **`new_namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to move the table to.
  If not specified, defaults to the same as cur\_namespace.

#### drop\_database

```
drop_database()
```

Drop database
This is the same thing as dropping all the tables

#### drop\_all\_tables

```
drop_all_tables(namespace_path: Optional[List[str]] = None)
```

Drop all tables from the database

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to drop all tables from.
  None or empty list represents root namespace.

#### namespace\_client

```
namespace_client() -> LanceNamespace
```

Get the equivalent namespace client for this connection.

For native storage connections, this returns a DirectoryNamespace
pointing to the same root with the same storage options.

For namespace connections, this returns the backing namespace client.

For enterprise (remote) connections, this returns a RestNamespace
with the same URI and authentication headers.

Returns:

* `LanceNamespace`
  –

  The namespace client for this connection.

## Tables (Synchronous)

### lancedb.table.Table

Bases: `ABC`

A Table is a collection of Records in a LanceDB Database.

Examples:

Create using [DBConnection.create\_table](#lancedb.db.DBConnection.create_table)
(more examples in that method's documentation).

```
>>> importlancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data=[{"vector": [1.1, 1.2], "b": 2}])
>>> table.head()
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
b: int64
----
vector: [[[1.1,1.2]]]
b: [[2]]
```

Can append new data with [Table.add()](#lancedb.table.Table.add).

```
>>> table.add([{"vector": [0.5, 1.3], "b": 4}])
AddResult(version=2)
```

Can query the table with [Table.search](#lancedb.table.Table.search).

```
>>> table.search([0.4, 0.4]).select(["b", "vector"]).to_pandas()
   b      vector  _distance
0  4  [0.5, 1.3]       0.82
1  2  [1.1, 1.2]       1.13
```

Search queries are much faster when an index is created. See
[Table.create\_index](#lancedb.table.Table.create_index).

#### name

```
name: str
```

The name of this Table

#### version

```
version: int
```

The version of this Table

#### schema

```
schema: Schema
```

The [Arrow Schema](https://arrow.apache.org/docs/python/api/datatypes.html#)
of this Table

#### tags

```
tags: Tags
```

Tag management for the table.

Similar to Git, tags are a way to add metadata to a specific version of the
table.

.. warning::

```
Tagged versions are exempted from the :py:meth:`cleanup_old_versions()`
process.

To remove a version that has been tagged, you must first
:py:meth:`~Tags.delete` the associated tag.
```

Examples:

.. code-block:: python

```
table = db.open_table("my_table")
table.tags.create("v2-prod-20250203", 10)

tags = table.tags.list()
```

#### embedding\_functions

```
embedding_functions: Dict[str, EmbeddingFunctionConfig]
```

Get a mapping from vector column name to it's configured embedding function.

#### count\_rows

```
count_rows(filter: Optional[str] = None) -> int
```

Count the number of rows in the table.

Parameters:

* **`filter`**
  (`Optional[str]`, default:
  `None`
  )
  –

  A SQL where clause to filter the rows to count.

#### to\_pandas

```
to_pandas() -> 'pandas.DataFrame'
```

Return the table as a pandas DataFrame.

Returns:

* `DataFrame`
  –

#### to\_arrow

```
to_arrow() -> Table
```

Return the table as a pyarrow Table.

Returns:

* `Table`
  –

#### to\_lance

```
to_lance(**kwargs) -> LanceDataset
```

Return the table as a lance.LanceDataset.

Returns:

* `LanceDataset`
  –

#### to\_polars

```
to_polars(**kwargs) -> 'pl.DataFrame'
```

Return the table as a polars.DataFrame.

Returns:

* `DataFrame`
  –

#### create\_index

```
create_index(metric='l2', num_partitions=256, num_sub_vectors=96, vector_column_name: str = VECTOR_COLUMN_NAME, replace: bool = True, accelerator: Optional[str] = None, index_cache_size: Optional[int] = None, *, index_type: VectorIndexType = 'IVF_PQ', wait_timeout: Optional[timedelta] = None, num_bits: int = 8, max_iterations: int = 50, sample_rate: int = 256, m: int = 20, ef_construction: int = 300, name: Optional[str] = None, train: bool = True, target_partition_size: Optional[int] = None)
```

Create an index on the table.

Parameters:

* **`metric`**
  –

  The distance metric to use when creating the index.
  Valid values are "l2", "cosine", "dot", or "hamming".
  l2 is euclidean distance.
  Hamming is available only for binary vectors.
* **`num_partitions`**
  –

  The number of IVF partitions to use when creating the index.
  Default is 256.
* **`num_sub_vectors`**
  –

  The number of PQ sub-vectors to use when creating the index.
  Default is 96.
* **`vector_column_name`**
  (`str`, default:
  `VECTOR_COLUMN_NAME`
  )
  –

  The vector column name to create the index.
* **`replace`**
  (`bool`, default:
  `True`
  )
  –

  + If True, replace the existing index if it exists.
  + If False, raise an error if duplicate index exists.
* **`accelerator`**
  (`Optional[str]`, default:
  `None`
  )
  –

  If set, use the given accelerator to create the index.
  Only support "cuda" for now.
* **`index_cache_size`**
  (`int`, default:
  `None`
  )
  –

  The size of the index cache in number of entries. Default value is 256.
* **`num_bits`**
  (`int`, default:
  `8`
  )
  –

  The number of bits to encode sub-vectors. Only used with the IVF\_PQ index.
  Only 4 and 8 are supported.
* **`wait_timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The timeout to wait if indexing is asynchronous.
* **`name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The name of the index. If not provided, a default name will be generated.
* **`train`**
  (`bool`, default:
  `True`
  )
  –

  Whether to train the index with existing data. Vector indices always train
  with existing data.

#### drop\_index

```
drop_index(name: str) -> None
```

Drop an index from the table.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the index to drop.

Notes

This does not delete the index from disk, it just removes it from the table.
To delete the index, run [optimize](#lancedb.table.Table.optimize)
after dropping the index.

Use [list\_indices](#lancedb.table.Table.list_indices) to find the names of
the indices.

#### wait\_for\_index

```
wait_for_index(index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)) -> None
```

Wait for indexing to complete for the given index names.
This will poll the table until all the indices are fully indexed,
or raise a timeout exception if the timeout is reached.

Parameters:

* **`index_names`**
  (`Iterable[str]`)
  –

  The name of the indices to poll
* **`timeout`**
  (`timedelta`, default:
  `timedelta(seconds=300)`
  )
  –

  Timeout to wait for asynchronous indexing. The default is 5 minutes.

#### stats

```
stats() -> TableStatistics
```

Retrieve table and fragment statistics.

#### create\_scalar\_index

```
create_scalar_index(column: str, *, replace: bool = True, index_type: ScalarIndexType = 'BTREE', wait_timeout: Optional[timedelta] = None, name: Optional[str] = None)
```

Create a scalar index on a column.

Parameters:

* **`column`**
  (`str`)
  –

  The column to be indexed. Must be a boolean, integer, float,
  or string column.
* **`replace`**
  (`bool`, default:
  `True`
  )
  –

  Replace the existing index if it exists.
* **`index_type`**
  (`ScalarIndexType`, default:
  `'BTREE'`
  )
  –

  The type of index to create.
* **`wait_timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The timeout to wait if indexing is asynchronous.
* **`name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The name of the index. If not provided, a default name will be generated.

Examples:

Scalar indices, like vector indices, can be used to speed up scans. A scalar
index can speed up scans that contain filter expressions on the indexed column.
For example, the following scan will be faster if the column `my_col` has
a scalar index:

```
>>> importlancedb
>>> db = lancedb.connect("/data/lance")
>>> img_table = db.open_table("images")
>>> my_df = img_table.search().where("my_col = 7",
...                                  prefilter=True).to_pandas()
```

Scalar indices can also speed up scans containing a vector search and a
prefilter:

```
>>> importlancedb
>>> db = lancedb.connect("/data/lance")
>>> img_table = db.open_table("images")
>>> img_table.search([1, 2, 3, 4], vector_column_name="vector")
...     .where("my_col != 7", prefilter=True)
...     .to_pandas()
```

Scalar indices can only speed up scans for basic filters using
equality, comparison, range (e.g. `my_col BETWEEN 0 AND 100`), and set
membership (e.g. `my_col IN (0, 1, 2)`)

Scalar indices can be used if the filter contains multiple indexed columns and
the filter criteria are AND'd or OR'd together
(e.g. `my_col < 0 AND other_col> 100`)

Scalar indices may be used if the filter contains non-indexed columns but,
depending on the structure of the filter, they may not be usable. For example,
if the column `not_indexed` does not have a scalar index then the filter
`my_col = 0 OR not_indexed = 1` will not be able to use any scalar index on
`my_col`.

#### create\_fts\_index

```
create_fts_index(field_names: Union[str, List[str]], *, ordering_field_names: Optional[Union[str, List[str]]] = None, replace: bool = False, writer_heap_size: Optional[int] = 1024 * 1024 * 1024, use_tantivy: bool = False, tokenizer_name: Optional[str] = None, with_position: bool = False, base_tokenizer: BaseTokenizerType = 'simple', language: str = 'English', max_token_length: Optional[int] = 40, lower_case: bool = True, stem: bool = True, remove_stop_words: bool = True, ascii_folding: bool = True, ngram_min_length: int = 3, ngram_max_length: int = 3, prefix_only: bool = False, wait_timeout: Optional[timedelta] = None, name: Optional[str] = None)
```

Create a full-text search index on the table.

Warning - this API is highly experimental and is highly likely to change
in the future.

Parameters:

* **`field_names`**
  (`Union[str, List[str]]`)
  –

  The name(s) of the field to index.
  If `use_tantivy` is False (default), only a single field name
  (str) is supported. To index multiple fields, create a separate
  FTS index for each field.
* **`replace`**
  (`bool`, default:
  `False`
  )
  –

  If True, replace the existing index if it exists. Note that this is
  not yet an atomic operation; the index will be temporarily
  unavailable while the new index is being created.
* **`writer_heap_size`**
  (`Optional[int]`, default:
  `1024 * 1024 * 1024`
  )
  –

  Only available with use\_tantivy=True
* **`ordering_field_names`**
  (`Optional[Union[str, List[str]]]`, default:
  `None`
  )
  –

  A list of unsigned type fields to index to optionally order
  results on at search time.
  only available with use\_tantivy=True
* **`tokenizer_name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The tokenizer to use for the index. Can be "raw", "default" or the 2 letter
  language code followed by "\_stem". So for english it would be "en\_stem".
  For available languages see: https://docs.rs/tantivy/latest/tantivy/tokenizer/enum.Language.html
* **`use_tantivy`**
  (`bool`, default:
  `False`
  )
  –

  If True, use the legacy full-text search implementation based on tantivy.
  If False, use the new full-text search implementation based on lance-index.
* **`with_position`**
  (`bool`, default:
  `False`
  )
  –

  Only available with use\_tantivy=False
  If False, do not store the positions of the terms in the text.
  This can reduce the size of the index and improve indexing speed.
  But it will raise an exception for phrase queries.
* **`base_tokenizer`**
  (`str`, default:
  `"simple"`
  )
  –

  The base tokenizer to use for tokenization. Options are:
  - "simple": Splits text by whitespace and punctuation.
  - "whitespace": Split text by whitespace, but not punctuation.
  - "raw": No tokenization. The entire text is treated as a single token.
  - "ngram": N-Gram tokenizer.
* **`language`**
  (`str`, default:
  `"English"`
  )
  –

  The language to use for tokenization.
* **`max_token_length`**
  (`int`, default:
  `40`
  )
  –

  The maximum token length to index. Tokens longer than this length will be
  ignored.
* **`lower_case`**
  (`bool`, default:
  `True`
  )
  –

  Whether to convert the token to lower case. This makes queries
  case-insensitive.
* **`stem`**
  (`bool`, default:
  `True`
  )
  –

  Whether to stem the token. Stemming reduces words to their root form.
  For example, in English "running" and "runs" would both be reduced to "run".
* **`remove_stop_words`**
  (`bool`, default:
  `True`
  )
  –

  Whether to remove stop words. Stop words are common words that are often
  removed from text before indexing. For example, in English "the" and "and".
* **`ascii_folding`**
  (`bool`, default:
  `True`
  )
  –

  Whether to fold ASCII characters. This converts accented characters to
  their ASCII equivalent. For example, "café" would be converted to "cafe".
* **`ngram_min_length`**
  (`int`, default:
  `3`
  )
  –

  The minimum length of an n-gram.
* **`ngram_max_length`**
  (`int`, default:
  `3`
  )
  –

  The maximum length of an n-gram.
* **`prefix_only`**
  (`bool`, default:
  `False`
  )
  –

  Whether to only index the prefix of the token for ngram tokenizer.
* **`wait_timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The timeout to wait if indexing is asynchronous.
* **`name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The name of the index. If not provided, a default name will be generated.

#### add

```
add(data: DATA, mode: AddMode = 'append', on_bad_vectors: OnBadVectorsType = 'error', fill_value: float = 0.0, progress: Optional[Union[bool, Callable, Any]] = None) -> AddResult
```

Add more data to the <Table>.

Parameters:

* **`data`**
  (`DATA`)
  –

  The data to insert into the table. Acceptable types are:

  + list-of-dict
  + pandas.DataFrame
  + pyarrow.Table or pyarrow.RecordBatch
* **`mode`**
  (`AddMode`, default:
  `'append'`
  )
  –

  The mode to use when writing the data. Valid values are
  "append" and "overwrite".
* **`on_bad_vectors`**
  (`OnBadVectorsType`, default:
  `'error'`
  )
  –

  What to do if any of the vectors are not the same size or contains NaNs.
  One of "error", "drop", "fill".
* **`fill_value`**
  (`float`, default:
  `0.0`
  )
  –

  The value to use when filling vectors. Only used if on\_bad\_vectors="fill".
* **`progress`**
  (`Optional[Union[bool, Callable, Any]]`, default:
  `None`
  )
  –

  Progress reporting during the add operation. Can be:

  + `True` to automatically create and display a tqdm progress
    bar (requires `tqdm` to be installed)::

    table.add(data, progress=True)
  + A **callable** that receives a dict with keys `output_rows`,
    `output_bytes`, `total_rows`, `elapsed_seconds`,
    `active_tasks`, `total_tasks`, and `done`::

    def on\_progress(p):
    print(f"{p['output\_rows']}/{p['total\_rows']} rows, "
    f"{p['active\_tasks']}/{p['total\_tasks']} workers")
    table.add(data, progress=on\_progress)
  + A **tqdm-compatible** progress bar whose `total` and
    `update()` will be called automatically. The postfix shows
    write throughput (MB/s) and active worker count::

    with tqdm() as pbar:
    table.add(data, progress=pbar)

Returns:

* `AddResult`
  –

  An object containing the new version number of the table after adding data.

#### merge\_insert

```
merge_insert(on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder
```

Returns a [`LanceMergeInsertBuilder`](#lancedb.merge.LanceMergeInsertBuilder)
that can be used to create a "merge insert" operation

This operation can add rows, update rows, and remove rows all in a single
transaction. It is a very generic tool that can be used to create
behaviors like "insert if not exists", "update or insert (i.e. upsert)",
or even replace a portion of existing data with new data (e.g. replace
all data where month="january")

The merge insert operation works by combining new data from a
**source table** with existing data in a **target table** by using a
join. There are three categories of records.

"Matched" records are records that exist in both the source table and
the target table. "Not matched" records exist only in the source table
(e.g. these are new data) "Not matched by source" records exist only
in the target table (this is old data)

The builder returned by this method can be used to customize what
should happen for each category of data.

Please note that the data may appear to be reordered as part of this
operation. This is because updated rows will be deleted from the
dataset and then reinserted at the end with the new values.

Parameters:

* **`on`**
  (`Union[str, Iterable[str]]`)
  –

  A column (or columns) to join on. This is how records from the
  source table and target table are matched. Typically this is some
  kind of key or id column.

Examples:

```
>>> importlancedb
>>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
>>> # Perform a "upsert" operation
>>> res = table.merge_insert("a")     \
...      .when_matched_update_all()     \
...      .when_not_matched_insert_all() \
...      .execute(new_data)
>>> res
MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
>>> # The order of new rows is non-deterministic since we use
>>> # a hash-join as part of this operation and so we sort here
>>> table.to_arrow().sort_by("a").to_pandas()
   a  b
0  1  b
1  2  x
2  3  y
3  4  z
```

#### search

```
search(query: Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]] = None, vector_column_name: Optional[str] = None, query_type: QueryType = 'auto', ordering_field_name: Optional[str] = None, fts_columns: Optional[Union[str, List[str]]] = None) -> LanceQueryBuilder
```

Create a search query to find the nearest neighbors
of the given query vector. We currently support [vector search](../../js/classes/Table/#search)
and [full-text search][experimental-full-text-search].

All query options are defined in
[LanceQueryBuilder](#lancedb.query.LanceQueryBuilder).

Examples:

```
>>> importlancedb
>>> db = lancedb.connect("./.lancedb")
>>> data = [
...    {"original_width": 100, "caption": "bar", "vector": [0.1, 2.3, 4.5]},
...    {"original_width": 2000, "caption": "foo",  "vector": [0.5, 3.4, 1.3]},
...    {"original_width": 3000, "caption": "test", "vector": [0.3, 6.2, 2.6]}
... ]
>>> table = db.create_table("my_table", data)
>>> query = [0.4, 1.4, 2.4]
>>> (table.search(query)
...     .where("original_width > 1000", prefilter=True)
...     .select(["caption", "original_width", "vector"])
...     .limit(2)
...     .to_pandas())
  caption  original_width           vector  _distance
0     foo            2000  [0.5, 3.4, 1.3]   5.220000
1    test            3000  [0.3, 6.2, 2.6]  23.089996
```

Parameters:

* **`query`**
  (`Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]]`, default:
  `None`
  )
  –

  The targetted vector to search for.

  + *default None*.
    Acceptable types are: list, np.ndarray, PIL.Image.Image
  + If None then the select/where/limit clauses are applied to filter
    the table
* **`vector_column_name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The name of the vector column to search.

  The vector column needs to be a pyarrow fixed size list type

  + If not specified then the vector column is inferred from
    the table schema
  + If the table has multiple vector columns then the *vector\_column\_name*
    needs to be specified. Otherwise, an error is raised.
* **`query_type`**
  (`QueryType`, default:
  `'auto'`
  )
  –

  *default "auto"*.
  Acceptable types are: "vector", "fts", "hybrid", or "auto"

  + If "auto" then the query type is inferred from the query;

    - If `query` is a list/np.ndarray then the query type is
      "vector";
    - If `query` is a PIL.Image.Image then either do vector search,
      or raise an error if no corresponding embedding function is found.
  + If `query` is a string, then the query type is "vector" if the
    table has embedding functions else the query type is "fts"

Returns:

* `LanceQueryBuilder`
  –

  A query builder object representing the query.
  Once executed, the query returns

  + selected columns
  + the vector
  + and also the "\_distance" column which is the distance between the query
    vector and the returned vector.

#### take\_offsets

```
take_offsets(offsets: list[int], *, with_row_id: bool = False) -> LanceTakeQueryBuilder
```

Take a list of offsets from the table.

Offsets are 0-indexed and relative to the current version of the table. Offsets
are not stable. A row with an offset of N may have a different offset in a
different version of the table (e.g. if an earlier row is deleted).

Offsets are mostly useful for sampling as the set of all valid offsets is easily
known in advance to be [0, len(table)).

No guarantees are made regarding the order in which results are returned. If
you desire an output order that matches the order of the given offsets, you will
need to add the row offset column to the output and align it yourself.

Parameters:

* **`offsets`**
  (`list[int]`)
  –

  The offsets to take.

Returns:

* `RecordBatch`
  –

  A record batch containing the rows at the given offsets.

#### take\_row\_ids

```
take_row_ids(row_ids: list[int], *, with_row_id: bool = False) -> LanceTakeQueryBuilder
```

Take a list of row ids from the table.

Row ids are not stable and are relative to the current version of the table.
They can change due to compaction and updates.

No guarantees are made regarding the order in which results are returned. If
you desire an output order that matches the order of the given ids, you will
need to add the row id column to the output and align it yourself.

Unlike offsets, row ids are not 0-indexed and no assumptions should be made
about the possible range of row ids. In order to use this method you must
first obtain the row ids by scanning or searching the table.

Even so, row ids are more stable than offsets and can be useful in some
situations.

There is an ongoing effort to make row ids stable which is tracked at
https://github.com/lancedb/lancedb/issues/1120

Parameters:

* **`row_ids`**
  (`list[int]`)
  –

  The row ids to take.

Returns:

* `AsyncTakeQuery`
  –

  A query object that can be executed to get the rows.

#### delete

```
delete(where: str) -> DeleteResult
```

Delete rows from the table.

This can be used to delete a single row, many rows, all rows, or
sometimes no rows (if your predicate matches nothing).

Parameters:

* **`where`**
  (`str`)
  –

  The SQL where clause to use when deleting rows.

  + For example, 'x = 2' or 'x IN (1, 2, 3)'.

  The filter must not be empty, or it will error.

Returns:

* `DeleteResult`
  –

  An object containing the new version number of the table after deletion.

Examples:

```
>>> importlancedb
>>> data = [
...    {"x": 1, "vector": [1.0, 2]},
...    {"x": 2, "vector": [3.0, 4]},
...    {"x": 3, "vector": [5.0, 6]}
... ]
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  2  [3.0, 4.0]
2  3  [5.0, 6.0]
>>> table.delete("x = 2")
DeleteResult(num_deleted_rows=1, version=2)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  3  [5.0, 6.0]
```

If you have a list of values to delete, you can combine them into a
stringified list and use the `IN` operator:

```
>>> to_remove = [1, 5]
>>> to_remove = ", ".join([str(v) for v in to_remove])
>>> to_remove
'1, 5'
>>> table.delete(f"x IN ({to_remove})")
DeleteResult(num_deleted_rows=1, version=3)
>>> table.to_pandas()
   x      vector
0  3  [5.0, 6.0]
```

#### update

```
update(where: Optional[str] = None, values: Optional[dict] = None, *, values_sql: Optional[Dict[str, str]] = None) -> UpdateResult
```

This can be used to update zero to all rows depending on how many
rows match the where clause. If no where clause is provided, then
all rows will be updated.

Either `values` or `values_sql` must be provided. You cannot provide
both.

Parameters:

* **`where`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The SQL where clause to use when updating rows. For example, 'x = 2'
  or 'x IN (1, 2, 3)'. The filter must not be empty, or it will error.
* **`values`**
  (`Optional[dict]`, default:
  `None`
  )
  –

  The values to update. The keys are the column names and the values
  are the values to set.
* **`values_sql`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  The values to update, expressed as SQL expression strings. These can
  reference existing columns. For example, {"x": "x + 1"} will increment
  the x column by 1.

Returns:

* `UpdateResult`
  –

  + rows\_updated: The number of rows that were updated
  + version: The new version number of the table after the update

Examples:

```
>>> importlancedb
>>> importpandasaspd
>>> data = pd.DataFrame({"x": [1, 2, 3], "vector": [[1.0, 2], [3, 4], [5, 6]]})
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  2  [3.0, 4.0]
2  3  [5.0, 6.0]
>>> table.update(where="x = 2", values={"vector": [10.0, 10]})
UpdateResult(rows_updated=1, version=2)
>>> table.to_pandas()
   x        vector
0  1    [1.0, 2.0]
1  3    [5.0, 6.0]
2  2  [10.0, 10.0]
>>> table.update(values_sql={"x": "x + 1"})
UpdateResult(rows_updated=3, version=3)
>>> table.to_pandas()
   x        vector
0  2    [1.0, 2.0]
1  4    [5.0, 6.0]
2  3  [10.0, 10.0]
```

#### cleanup\_old\_versions

```
cleanup_old_versions(older_than: Optional[timedelta] = None, *, delete_unverified: bool = False) -> 'CleanupStats'
```

Clean up old versions of the table, freeing disk space.

Parameters:

* **`older_than`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The minimum age of the version to delete. If None, then this defaults
  to two weeks.
* **`delete_unverified`**
  (`bool`, default:
  `False`
  )
  –

  Because they may be part of an in-progress transaction, files newer
  than 7 days old are not deleted by default. If you are sure that
  there are no in-progress transactions, then you can set this to True
  to delete all files older than `older_than`.

Returns:

* `CleanupStats`
  –

  The stats of the cleanup operation, including how many bytes were
  freed.

See Also

[Table.optimize](#lancedb.table.Table.optimize): A more comprehensive
optimization operation that includes cleanup as well as other operations.

Notes

This function is not available in LanceDb Cloud (since LanceDB
Cloud manages cleanup for you automatically)

#### compact\_files

```
compact_files(*args, **kwargs)
```

Run the compaction process on the table.
This can be run after making several small appends to optimize the table
for faster reads.

Arguments are passed onto Lance's
[compact\_files][lance.dataset.DatasetOptimizer.compact\_files].
For most cases, the default should be fine.

See Also

[Table.optimize](#lancedb.table.Table.optimize): A more comprehensive
optimization operation that includes cleanup as well as other operations.

Notes

This function is not available in LanceDB Cloud (since LanceDB
Cloud manages compaction for you automatically)

#### optimize

```
optimize(*, cleanup_older_than: Optional[timedelta] = None, delete_unverified: bool = False, retrain: bool = False)
```

Optimize the on-disk data and indices for better performance.

Modeled after `VACUUM` in PostgreSQL.

Optimization covers three operations:

* Compaction: Merges small files into larger ones
* Prune: Removes old versions of the dataset
* Index: Optimizes the indices, adding new data to existing indices

Parameters:

* **`cleanup_older_than`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  All files belonging to versions older than this will be removed. Set
  to 0 days to remove all versions except the latest. The latest version
  is never removed.
* **`delete_unverified`**
  (`bool`, default:
  `False`
  )
  –

  Files leftover from a failed transaction may appear to be part of an
  in-progress operation (e.g. appending new data) and these files will not
  be deleted unless they are at least 7 days old. If delete\_unverified is True
  then these files will be deleted regardless of their age.

  .. warning::

  ```
  This should only be set to True if you can guarantee that no other
  process is currently working on this dataset. Otherwise the dataset
  could be put into a corrupted state.
  ```
* **`retrain`**
  (`bool`, default:
  `False`
  )
  –

  This parameter is no longer used and is deprecated.
* **`The`**
  –
* **`data`**
  –
* **`optimize`**
  –
* **`you`**
  –
* **`modification`**
  –

#### list\_indices

```
list_indices() -> Iterable[IndexConfig]
```

List all indices that have been created with
[Table.create\_index](#lancedb.table.Table.create_index)

#### index\_stats

```
index_stats(index_name: str) -> Optional[IndexStatistics]
```

Retrieve statistics about an index

Parameters:

* **`index_name`**
  (`str`)
  –

  The name of the index to retrieve statistics for

Returns:

* `IndexStatistics or None`
  –

  The statistics about the index. Returns None if the index does not exist.

#### add\_columns

```
add_columns(transforms: Dict[str, str] | Field | List[Field] | Schema)
```

Add new columns with defined values.

Parameters:

* **`transforms`**
  (`Dict[str, str] | Field | List[Field] | Schema`)
  –

  A map of column name to a SQL expression to use to calculate the
  value of the new column. These expressions will be evaluated for
  each row in the table, and can reference existing columns.
  Alternatively, a pyarrow Field or Schema can be provided to add
  new columns with the specified data types. The new columns will
  be initialized with null values.

Returns:

* `AddColumnsResult`
  –

  version: the new version number of the table after adding columns.

#### alter\_columns

```
alter_columns(*alterations: Iterable[Dict[str, str]])
```

Alter column names and nullability.

Parameters:

* **`alterations`**
  (`Iterable[Dict[str, Any]]`, default:
  `()`
  )
  –

  A sequence of dictionaries, each with the following keys:
  - "path": str
  The column path to alter. For a top-level column, this is the name.
  For a nested column, this is the dot-separated path, e.g. "a.b.c".
  - "rename": str, optional
  The new name of the column. If not specified, the column name is
  not changed.
  - "data\_type": pyarrow.DataType, optional
  The new data type of the column. Existing values will be casted
  to this type. If not specified, the column data type is not changed.
  - "nullable": bool, optional
  Whether the column should be nullable. If not specified, the column
  nullability is not changed. Only non-nullable columns can be changed
  to nullable. Currently, you cannot change a nullable column to
  non-nullable.

Returns:

* `AlterColumnsResult`
  –

  version: the new version number of the table after the alteration.

#### drop\_columns

```
drop_columns(columns: Iterable[str]) -> DropColumnsResult
```

Drop columns from the table.

Parameters:

* **`columns`**
  (`Iterable[str]`)
  –

  The names of the columns to drop.

Returns:

* `DropColumnsResult`
  –

  version: the new version number of the table dropping the columns.

#### checkout

```
checkout(version: Union[int, str])
```

Checks out a specific version of the Table

Any read operation on the table will now access the data at the checked out
version. As a consequence, calling this method will disable any read consistency
interval that was previously set.

This is a read-only operation that turns the table into a sort of "view"
or "detached head". Other table instances will not be affected. To make the
change permanent you can use the `[Self::restore]` method.

Any operation that modifies the table will fail while the table is in a checked
out state.

Parameters:

* **`version`**
  (`Union[int, str]`)
  –

  The version to check out. A version number (`int`) or a tag
  (`str`) can be provided.
* **`To`**
  –

#### checkout\_latest

```
checkout_latest()
```

Ensures the table is pointing at the latest version

This can be used to manually update a table when the read\_consistency\_interval
is None
It can also be used to undo a `[Self::checkout]` operation

#### restore

```
restore(version: Optional[Union[int, str]] = None)
```

Restore a version of the table. This is an in-place operation.

This creates a new version where the data is equivalent to the
specified previous version. Data is not copied (as of python-v0.2.1).

Parameters:

* **`version`**
  (`int or str`, default:
  `None`
  )
  –

  The version number or version tag to restore.
  If unspecified then restores the currently checked out version.
  If the currently checked out version is the
  latest version then this is a no-op.

#### list\_versions

```
list_versions() -> List[Dict[str, Any]]
```

List all versions of the table

#### uses\_v2\_manifest\_paths

```
uses_v2_manifest_paths() -> bool
```

Check if the table is using the new v2 manifest paths.

Returns:

* `bool`
  –

  True if the table is using the new v2 manifest paths, False otherwise.

#### migrate\_v2\_manifest\_paths

```
migrate_v2_manifest_paths()
```

Migrate the manifest paths to the new format.

This will update the manifest to use the new v2 format for paths.

This function is idempotent, and can be run multiple times without
changing the state of the object store.

Danger

This should not be run while other concurrent operations are happening.
And it should also run until completion before resuming other operations.

You can use
[Table.uses\_v2\_manifest\_paths](#lancedb.table.Table.uses_v2_manifest_paths)
to check if the table is already using the new path style.

### lancedb.table.FragmentStatistics

Statistics about fragments.

#### num\_fragments

```
num_fragments: int
```

#### num\_small\_fragments

```
num_small_fragments: int
```

#### lengths

```
lengths: FragmentSummaryStats
```

### lancedb.table.FragmentSummaryStats

Statistics about fragments sizes

#### min

```
min: int
```

#### max

```
max: int
```

#### mean

```
mean: int
```

#### p25

```
p25: int
```

#### p50

```
p50: int
```

#### p75

```
p75: int
```

#### p99

```
p99: int
```

### lancedb.table.Tags

Table tag manager.

#### list

```
list() -> Dict[str, Tag]
```

List all table tags.

Returns:

* `dict[str, Tag]`
  –

  A dictionary mapping tag names to version numbers.

#### get\_version

```
get_version(tag: str) -> int
```

Get the version of a tag.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to get the version for.

#### create

```
create(tag: str, version: int) -> None
```

Create a tag for a given table version.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to create. This name must be unique among all tag
  names for the table.
* **`version`**
  (`int`)
  –

  The table version to tag.

#### delete

```
delete(tag: str) -> None
```

Delete tag from the table.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to delete.

#### update

```
update(tag: str, version: int) -> None
```

Update tag to a new version.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to update.
* **`version`**
  (`int`)
  –

  The new table version to tag.

## Expressions

Type-safe expression builder for filters and projections. Use these instead
of raw SQL strings with [where](#lancedb.query.LanceQueryBuilder.where) and
[select](#lancedb.query.LanceQueryBuilder.select).

### lancedb.expr.Expr

A type-safe expression node.

Construct instances with :func:`col` and :func:`lit`, then combine them
using Python operators or the named methods below.

Examples:

```
>>> fromlancedb.exprimport col, lit
>>> filt = (col("age") > lit(18)) & (col("name").lower() == lit("alice"))
>>> proj = {"double": col("x") * lit(2)}
```

#### lower

```
lower() -> 'Expr'
```

Convert string column values to lowercase.

#### upper

```
upper() -> 'Expr'
```

Convert string column values to uppercase.

#### contains

```
contains(substr: 'ExprLike') -> 'Expr'
```

Return True where the string contains *substr*.

#### cast

```
cast(data_type: Union[str, 'pa.DataType']) -> 'Expr'
```

Cast values to *data\_type*.

Parameters:

* **`data_type`**
  (`Union[str, 'pa.DataType']`)
  –

  A PyArrow `DataType` (e.g. `pa.int32()`) or one of the type
  name strings: `"bool"`, `"int8"`, `"int16"`, `"int32"`,
  `"int64"`, `"uint8"`–`"uint64"`, `"float32"`,
  `"float64"`, `"string"`, `"date32"`, `"date64"`.

#### eq

```
eq(other: ExprLike) -> 'Expr'
```

Equal to.

#### ne

```
ne(other: ExprLike) -> 'Expr'
```

Not equal to.

#### lt

```
lt(other: ExprLike) -> 'Expr'
```

Less than.

#### lte

```
lte(other: ExprLike) -> 'Expr'
```

Less than or equal to.

#### gt

```
gt(other: ExprLike) -> 'Expr'
```

Greater than.

#### gte

```
gte(other: ExprLike) -> 'Expr'
```

Greater than or equal to.

#### and\_

```
and_(other: 'Expr') -> 'Expr'
```

Logical AND.

#### or\_

```
or_(other: 'Expr') -> 'Expr'
```

Logical OR.

#### to\_sql

```
to_sql() -> str
```

Render the expression as a SQL string (useful for debugging).

### lancedb.expr.col

```
col(name: str) -> Expr
```

Reference a table column by name.

Parameters:

* **`name`**
  (`str`)
  –

  The column name.

Examples:

```
>>> fromlancedb.exprimport col, lit
>>> col("age") > lit(18)
Expr((age > 18))
```

### lancedb.expr.lit

```
lit(value: Union[bool, int, float, str]) -> Expr
```

Create a literal (constant) value expression.

Parameters:

* **`value`**
  (`Union[bool, int, float, str]`)
  –

  A Python `bool`, `int`, `float`, or `str`.

Examples:

```
>>> fromlancedb.exprimport col, lit
>>> col("price") * lit(1.1)
Expr((price * 1.1))
```

### lancedb.expr.func

```
func(name: str, *args: ExprLike) -> Expr
```

Call an arbitrary SQL function by name.

Parameters:

* **`name`**
  (`str`)
  –

  The SQL function name (e.g. `"lower"`, `"upper"`).
* **`*args`**
  (`ExprLike`, default:
  `()`
  )
  –

  The function arguments as :class:`Expr` or plain Python literals.

Examples:

```
>>> fromlancedb.exprimport col, func
>>> func("lower", col("name"))
Expr(lower(name))
```

## Querying (Synchronous)

### lancedb.query.Query

Bases: `BaseModel`

A LanceDB Query

Queries are constructed by the `Table.search` method. This class is a
python representation of the query. Normally you will not need to interact
with this class directly. You can build up a query and execute it using
collection methods such as `to_batches()`, `to_arrow()`, `to_pandas()`,
etc.

However, you can use the `to_query()` method to get the underlying query object.
This can be useful for serializing a query or using it in a different context.

#### vector\_column

```
vector_column: Optional[str] = None
```

#### vector

```
vector: Annotated[Optional[Union[List[float], List[List[float]], Array, List[Array]]], ensure_vector_query] = None
```

#### filter

```
filter: Optional[Union[str, Expr]] = None
```

#### postfilter

```
postfilter: Optional[bool] = None
```

#### full\_text\_query

```
full_text_query: Optional[FullTextSearchQuery] = None
```

#### limit

```
limit: Optional[int] = None
```

#### distance\_type

```
distance_type: Optional[str] = None
```

#### columns

```
columns: Optional[Union[List[str], Dict[str, Union[str, Expr]]]] = None
```

#### minimum\_nprobes

```
minimum_nprobes: Optional[int] = None
```

#### maximum\_nprobes

```
maximum_nprobes: Optional[int] = None
```

#### lower\_bound

```
lower_bound: Optional[float] = None
```

#### upper\_bound

```
upper_bound: Optional[float] = None
```

#### refine\_factor

```
refine_factor: Optional[int] = None
```

#### with\_row\_id

```
with_row_id: Optional[bool] = None
```

#### offset

```
offset: Optional[int] = None
```

#### fast\_search

```
fast_search: Optional[bool] = None
```

#### ef

```
ef: Optional[int] = None
```

#### bypass\_vector\_index

```
bypass_vector_index: Optional[bool] = None
```

#### model\_config

```
model_config = {'arbitrary_types_allowed': True}
```

#### Config

##### arbitrary\_types\_allowed

```
arbitrary_types_allowed = True
```

#### from\_inner

```
from_inner(req: PyQueryRequest) -> Self
```

### lancedb.query.LanceQueryBuilder

Bases: `ABC`

An abstract query builder. Subclasses are defined for vector search,
full text search, hybrid, and plain SQL filtering.

#### create

```
create(table: 'Table', query: Optional[Union[ndarray, str, 'PIL.Image.Image', Tuple]], query_type: str, vector_column_name: str, ordering_field_name: Optional[str] = None, fts_columns: Optional[Union[str, List[str]]] = None, fast_search: bool = None) -> Self
```

Create a query builder based on the given query and query type.

Parameters:

* **`table`**
  (`'Table'`)
  –

  The table to query.
* **`query`**
  (`Optional[Union[ndarray, str, 'PIL.Image.Image', Tuple]]`)
  –

  The query to use. If None, an empty query builder is returned
  which performs simple SQL filtering.
* **`query_type`**
  (`str`)
  –

  The type of query to perform. One of "vector", "fts", "hybrid", or "auto".
  If "auto", the query type is inferred based on the query.
* **`vector_column_name`**
  (`str`)
  –

  The name of the vector column to use for vector search.
* **`fast_search`**
  (`bool`, default:
  `None`
  )
  –

  Skip flat search of unindexed data.

#### to\_df

```
to_df() -> 'pd.DataFrame'
```

*Deprecated alias for `to_pandas()`. Please use `to_pandas()` instead.*

Execute the query and return the results as a pandas DataFrame.
In addition to the selected columns, LanceDB also returns a vector
and also the "\_distance" column which is the distance between the query
vector and the returned vector.

#### to\_pandas

```
to_pandas(flatten: Optional[Union[int, bool]] = None, *, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'
```

Execute the query and return the results as a pandas DataFrame.
In addition to the selected columns, LanceDB also returns a vector
and also the "\_distance" column which is the distance between the query
vector and the returned vector.

Parameters:

* **`flatten`**
  (`Optional[Union[int, bool]]`, default:
  `None`
  )
  –

  If flatten is True, flatten all nested columns.
  If flatten is an integer, flatten the nested columns up to the
  specified depth.
  If unspecified, do not flatten the nested columns.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

#### to\_arrow

```
to_arrow(*, timeout: Optional[timedelta] = None) -> Table
```

Execute the query and return the results as an
[Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table).

In addition to the selected columns, LanceDB also returns a vector
and also the "\_distance" column which is the distance between the query
vector and the returned vectors.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

#### to\_batches

```
to_batches(batch_size: Optional[int] = None, *, timeout: Optional[timedelta] = None) -> RecordBatchReader
```

Execute the query and return the results as a pyarrow
[RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html)

Parameters:

* **`batch_size`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of selected records in a RecordBatch object.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

#### to\_list

```
to_list(*, timeout: Optional[timedelta] = None) -> List[dict]
```

Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "\_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

#### to\_pydantic

```
to_pydantic(model: type[T], *, timeout: Optional[timedelta] = None) -> list[T]
```

Return the table as a list of pydantic models.

Parameters:

* **`model`**
  (`type[T]`)
  –

  The pydantic model to use.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

Returns:

* `List[LanceModel]`
  –

#### to\_polars

```
to_polars(*, timeout: Optional[timedelta] = None) -> 'pl.DataFrame'
```

Execute the query and return the results as a Polars DataFrame.
In addition to the selected columns, LanceDB also returns a vector
and also the "\_distance" column which is the distance between the query
vector and the returned vector.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

#### limit

```
limit(limit: Union[int, None]) -> Self
```

Set the maximum number of results to return.

Parameters:

* **`limit`**
  (`Union[int, None]`)
  –

  The maximum number of results to return.
  The default query limit is 10 results.
  For ANN/KNN queries, you must specify a limit.
  For plain searches, all records are returned if limit not set.
  *WARNING* if you have a large dataset, setting
  the limit to a large number, e.g. the table size,
  can potentially result in reading a
  large amount of data into memory and cause
  out of memory issues.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### offset

```
offset(offset: int) -> Self
```

Set the offset for the results.

Parameters:

* **`offset`**
  (`int`)
  –

  The offset to start fetching results from.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### select

```
select(columns: Union[list[str], dict[str, Union[str, Expr]]]) -> Self
```

Set the columns to return.

Parameters:

* **`columns`**
  (`Union[list[str], dict[str, Union[str, Expr]]]`)
  –

  List of column names to be fetched.
  Or a dictionary of column names to SQL expressions or
  :class:`~lancedb.expr.Expr` objects.
  All columns are fetched if None or unspecified.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### where

```
where(where: Union[str, Expr], prefilter: bool = True) -> Self
```

Set the where clause.

Parameters:

* **`where`**
  (`Union[str, Expr]`)
  –

  The filter condition. Can be a SQL string or a type-safe
  :class:`~lancedb.expr.Expr` built with :func:`~lancedb.expr.col`
  and :func:`~lancedb.expr.lit`.
* **`prefilter`**
  (`bool`, default:
  `True`
  )
  –

  If True, apply the filter before vector search, otherwise the
  filter is applied on the result of vector search.
  This feature is **EXPERIMENTAL** and may be removed and modified
  without warning in the future.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### with\_row\_id

```
with_row_id(with_row_id: bool) -> Self
```

Set whether to return row ids.

Parameters:

* **`with_row_id`**
  (`bool`)
  –

  If True, return \_rowid column in the results.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### explain\_plan

```
explain_plan(verbose: Optional[bool] = False) -> str
```

Return the execution plan for this query.

Examples:

```
>>> importlancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
>>> query = [100, 100]
>>> plan = table.search(query).explain_plan(True)
>>> print(plan)
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...
```

Parameters:

* **`verbose`**
  (`bool`, default:
  `False`
  )
  –

  Use a verbose output format.

Returns:

* **`plan`** ( `str`
  ) –

#### analyze\_plan

```
analyze_plan() -> str
```

Run the query and return its execution plan with runtime metrics.

This returns detailed metrics for each step, such as elapsed time,
rows processed, bytes read, and I/O stats. It is useful for debugging
and performance tuning.

Examples:

```
>>> importlancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
>>> query = [100, 100]
>>> plan = table.search(query).analyze_plan()
>>> print(plan)
AnalyzeExec verbose=true, elapsed=..., metrics=...
  TracedExec, elapsed=..., metrics=...
    ProjectionExec: elapsed=..., expr=[...],
    metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
      GlobalLimitExec: elapsed=..., skip=0, fetch=10,
      metrics=[output_rows=..., elapsed_compute=..., output_bytes=...]
        FilterExec: elapsed=..., _distance@2 IS NOT NULL, metrics=[...]
          SortExec: elapsed=..., TopK(fetch=10), expr=[...],
          preserve_partitioning=[...],
          metrics=[output_rows=..., elapsed_compute=...,
          output_bytes=..., row_replacements=...]
            KNNVectorDistance: elapsed=..., metric=l2,
            metrics=[output_rows=..., elapsed_compute=...,
            output_bytes=..., output_batches=...]
              LanceRead: elapsed=..., uri=..., projection=[vector],
              num_fragments=..., range_before=None, range_after=None,
              row_id=true, row_addr=false,
              full_filter=--, refine_filter=--,
              metrics=[output_rows=..., elapsed_compute=..., output_bytes=...,
              fragments_scanned=..., ranges_scanned=1, rows_scanned=1,
              bytes_read=..., iops=..., requests=..., task_wait_time=...]
```

Returns:

* **`plan`** ( `str`
  ) –

  The physical query execution plan with runtime metrics.

#### vector

```
vector(vector: Union[ndarray, list]) -> Self
```

Set the vector to search for.

Parameters:

* **`vector`**
  (`Union[ndarray, list]`)
  –

  The vector to search for.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### text

```
text(text: str | FullTextQuery) -> Self
```

Set the text to search for.

Parameters:

* **`text`**
  (`str | FullTextQuery`)
  –

  If a string, it is treated as a MatchQuery.
  If a FullTextQuery object, it is used directly.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### rerank

```
rerank(reranker: Reranker) -> Self
```

Rerank the results using the specified reranker.

Parameters:

* **`reranker`**
  (`Reranker`)
  –

  The reranker to use.

Returns:

* `The LanceQueryBuilder object.`
  –

#### to\_query\_object

```
to_query_object() -> Query
```

Return a serializable representation of the query

Returns:

* `Query`
  –

  The serializable representation of the query

### lancedb.query.LanceVectorQueryBuilder

Bases: `LanceQueryBuilder`

Examples:

```
>>> importlancedb
>>> data = [{"vector": [1.1, 1.2], "b": 2},
...         {"vector": [0.5, 1.3], "b": 4},
...         {"vector": [0.4, 0.4], "b": 6},
...         {"vector": [0.4, 0.4], "b": 10}]
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data=data)
>>> (table.search([0.4, 0.4])
...       .distance_type("cosine")
...       .where("b < 10")
...       .select(["b", "vector"])
...       .limit(2)
...       .to_pandas())
   b      vector  _distance
0  6  [0.4, 0.4]   0.000000
1  2  [1.1, 1.2]   0.000944
```

#### metric

```
metric(metric: Literal['l2', 'cosine', 'dot']) -> LanceVectorQueryBuilder
```

Set the distance metric to use.

This is an alias for distance\_type() and may be deprecated in the future.
Please use distance\_type() instead.

Parameters:

* **`metric`**
  (`Literal['l2', 'cosine', 'dot']`)
  –

  The distance metric to use. By default "l2" is used.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### distance\_type

```
distance_type(distance_type: Literal['l2', 'cosine', 'dot']) -> 'LanceVectorQueryBuilder'
```

Set the distance metric to use.

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric. This parameter controls which distance metric
to use.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index. If this is not done then the
results will be invalid.

Parameters:

* **`distance_type`**
  (`Literal['l2', 'cosine', 'dot']`)
  –

  The distance metric to use. By default "l2" is used.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### nprobes

```
nprobes(nprobes: int) -> LanceVectorQueryBuilder
```

Set the number of probes to use.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

See discussion in [Querying an ANN Index][querying-an-ann-index] for
tuning advice.

This method sets both the minimum and maximum number of probes to the same
value. See `minimum_nprobes` and `maximum_nprobes` for more fine-grained
control.

Parameters:

* **`nprobes`**
  (`int`)
  –

  The number of probes to use.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### minimum\_nprobes

```
minimum_nprobes(minimum_nprobes: int) -> LanceVectorQueryBuilder
```

Set the minimum number of probes to use.

See `nprobes` for more details.

These partitions will be searched on every vector query and will increase recall
at the expense of latency.

#### maximum\_nprobes

```
maximum_nprobes(maximum_nprobes: int) -> LanceVectorQueryBuilder
```

Set the maximum number of probes to use.

See `nprobes` for more details.

If this value is greater than `minimum_nprobes` then the excess partitions
will be searched only if we have not found enough results.

This can be useful when there is a narrow filter to allow these queries to
spend more time searching and avoid potential false negatives.

If this value is 0 then no limit will be applied and all partitions could be
searched if needed to satisfy the limit.

#### distance\_range

```
distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> LanceVectorQueryBuilder
```

Set the distance range to use.

Only rows with distances within range [lower\_bound, upper\_bound)
will be returned.

Parameters:

* **`lower_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The lower bound of the distance range.
* **`upper_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The upper bound of the distance range.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### ef

```
ef(ef: int) -> LanceVectorQueryBuilder
```

Set the number of candidates to consider during search.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

This only applies to the HNSW-related index.
The default value is 1.5 \* limit.

Parameters:

* **`ef`**
  (`int`)
  –

  The number of candidates to consider during search.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### refine\_factor

```
refine_factor(refine_factor: int) -> LanceVectorQueryBuilder
```

Set the refine factor to use, increasing the number of vectors sampled.

As an example, a refine factor of 2 will sample 2x as many vectors as
requested, re-ranks them, and returns the top half most relevant results.

See discussion in [Querying an ANN Index][querying-an-ann-index] for
tuning advice.

Parameters:

* **`refine_factor`**
  (`int`)
  –

  The refine factor to use.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### output\_schema

```
output_schema() -> Schema
```

Return the output schema for the query

This does not execute the query.

#### to\_arrow

```
to_arrow(*, timeout: Optional[timedelta] = None) -> Table
```

Execute the query and return the results as an
[Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table).

In addition to the selected columns, LanceDB also returns a vector
and also the "\_distance" column which is the distance between the query
vector and the returned vectors.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

#### to\_query\_object

```
to_query_object() -> Query
```

Build a Query object

This can be used to serialize a query

#### to\_batches

```
to_batches(batch_size: Optional[int] = None, *, timeout: Optional[timedelta] = None) -> RecordBatchReader
```

Execute the query and return the result as a RecordBatchReader object.

Parameters:

* **`batch_size`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of selected records in a RecordBatch object.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

Returns:

* `RecordBatchReader`
  –

#### where

```
where(where: Union[str, Expr], prefilter: bool = None) -> LanceVectorQueryBuilder
```

Set the where clause.

Parameters:

* **`where`**
  (`Union[str, Expr]`)
  –

  The filter condition. Can be a SQL string or a type-safe
  :class:`~lancedb.expr.Expr` built with :func:`~lancedb.expr.col`
  and :func:`~lancedb.expr.lit`.
* **`prefilter`**
  (`bool`, default:
  `None`
  )
  –

  If True, apply the filter before vector search, otherwise the
  filter is applied on the result of vector search.

Returns:

* `LanceQueryBuilder`
  –

  The LanceQueryBuilder object.

#### rerank

```
rerank(reranker: Reranker, query_string: Optional[str] = None) -> LanceVectorQueryBuilder
```

Rerank the results using the specified reranker.

Parameters:

* **`reranker`**
  (`Reranker`)
  –

  The reranker to use.
* **`query_string`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The query to use for reranking. This needs to be specified explicitly here
  as the query used for vector search may already be vectorized and the
  reranker requires a string query.
  This is only required if the query used for vector search is not a string.
  Note: This doesn't yet support the case where the query is multimodal or a
  list of vectors.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### bypass\_vector\_index

```
bypass_vector_index() -> LanceVectorQueryBuilder
```

If this is called then any vector index is skipped

An exhaustive (flat) search will be performed. The query vector will
be compared to every vector in the table. At high scales this can be
expensive. However, this is often still useful. For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceVectorQueryBuilder object.

#### fast\_search

```
fast_search() -> LanceVectorQueryBuilder
```

Skip a flat search of unindexed data. This will improve
search performance but search results will not include unindexed data.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceVectorQueryBuilder object.

### lancedb.query.LanceFtsQueryBuilder

Bases: `LanceQueryBuilder`

A builder for full text search for LanceDB.

#### ordering\_field\_name

```
ordering_field_name = ordering_field_name
```

#### phrase\_query

```
phrase_query(phrase_query: bool = True) -> LanceFtsQueryBuilder
```

Set whether to use phrase query.

Parameters:

* **`phrase_query`**
  (`bool`, default:
  `True`
  )
  –

  If True, then the query will be wrapped in quotes and
  double quotes replaced by single quotes.

Returns:

* `LanceFtsQueryBuilder`
  –

  The LanceFtsQueryBuilder object.

#### fast\_search

```
fast_search() -> LanceFtsQueryBuilder
```

Skip a flat search of unindexed data. This will improve
search performance but search results will not include unindexed data.

Returns:

* `LanceFtsQueryBuilder`
  –

  The LanceFtsQueryBuilder object.

#### to\_query\_object

```
to_query_object() -> Query
```

#### output\_schema

```
output_schema() -> Schema
```

Return the output schema for the query

This does not execute the query.

#### to\_arrow

```
to_arrow(*, timeout: Optional[timedelta] = None) -> Table
```

#### to\_batches

```
to_batches(batch_size: Optional[int] = None, timeout: Optional[timedelta] = None)
```

#### tantivy\_to\_arrow

```
tantivy_to_arrow() -> Table
```

#### rerank

```
rerank(reranker: Reranker) -> LanceFtsQueryBuilder
```

Rerank the results using the specified reranker.

Parameters:

* **`reranker`**
  (`Reranker`)
  –

  The reranker to use.

Returns:

* `LanceFtsQueryBuilder`
  –

  The LanceQueryBuilder object.

### lancedb.query.LanceHybridQueryBuilder

Bases: `LanceQueryBuilder`

A query builder that performs hybrid vector and full text search.
Results are combined and reranked based on the specified reranker.
By default, the results are reranked using the RRFReranker, which
uses reciprocal rank fusion score for reranking.

To make the vector and fts results comparable, the scores are normalized.
Instead of normalizing scores, the `normalize` parameter can be set to "rank"
in the `rerank` method to convert the scores to ranks and then normalize them.

#### phrase\_query

```
phrase_query(phrase_query: bool = None) -> LanceHybridQueryBuilder
```

Set whether to use phrase query.

Parameters:

* **`phrase_query`**
  (`bool`, default:
  `None`
  )
  –

  If True, then the query will be wrapped in quotes and
  double quotes replaced by single quotes.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### to\_query\_object

```
to_query_object() -> Query
```

#### to\_arrow

```
to_arrow(*, timeout: Optional[timedelta] = None) -> Table
```

#### to\_batches

```
to_batches(batch_size: Optional[int] = None, timeout: Optional[timedelta] = None)
```

#### rerank

```
rerank(reranker: Reranker = RRFReranker(), normalize: str = 'score') -> LanceHybridQueryBuilder
```

Rerank the hybrid search results using the specified reranker. The reranker
must be an instance of Reranker class.

Parameters:

* **`reranker`**
  (`Reranker`, default:
  `RRFReranker()`
  )
  –

  The reranker to use. Must be an instance of Reranker class.
* **`normalize`**
  (`str`, default:
  `'score'`
  )
  –

  The method to normalize the scores. Can be "rank" or "score". If "rank",
  the scores are converted to ranks and then normalized. If "score", the
  scores are normalized directly.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### nprobes

```
nprobes(nprobes: int) -> LanceHybridQueryBuilder
```

Set the number of probes to use for vector search.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

Parameters:

* **`nprobes`**
  (`int`)
  –

  The number of probes to use.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### minimum\_nprobes

```
minimum_nprobes(minimum_nprobes: int) -> LanceHybridQueryBuilder
```

Set the minimum number of probes to use.

See `nprobes` for more details.

#### maximum\_nprobes

```
maximum_nprobes(maximum_nprobes: int) -> LanceHybridQueryBuilder
```

Set the maximum number of probes to use.

See `nprobes` for more details.

#### distance\_range

```
distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> LanceHybridQueryBuilder
```

Set the distance range to use.

Only rows with distances within range [lower\_bound, upper\_bound)
will be returned.

Parameters:

* **`lower_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The lower bound of the distance range.
* **`upper_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The upper bound of the distance range.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### ef

```
ef(ef: int) -> LanceHybridQueryBuilder
```

Set the number of candidates to consider during search.

Higher values will yield better recall (more likely to find vectors if
they exist) at the expense of latency.

This only applies to the HNSW-related index.
The default value is 1.5 \* limit.

Parameters:

* **`ef`**
  (`int`)
  –

  The number of candidates to consider during search.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### metric

```
metric(metric: Literal['l2', 'cosine', 'dot']) -> LanceHybridQueryBuilder
```

Set the distance metric to use.

This is an alias for distance\_type() and may be deprecated in the future.
Please use distance\_type() instead.

Parameters:

* **`metric`**
  (`Literal['l2', 'cosine', 'dot']`)
  –

  The distance metric to use. By default "l2" is used.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### distance\_type

```
distance_type(distance_type: Literal['l2', 'cosine', 'dot']) -> 'LanceHybridQueryBuilder'
```

Set the distance metric to use.

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric. This parameter controls which distance metric
to use.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index. If this is not done then the
results will be invalid.

Parameters:

* **`distance_type`**
  (`Literal['l2', 'cosine', 'dot']`)
  –

  The distance metric to use. By default "l2" is used.

Returns:

* `LanceVectorQueryBuilder`
  –

  The LanceQueryBuilder object.

#### refine\_factor

```
refine_factor(refine_factor: int) -> LanceHybridQueryBuilder
```

Refine the vector search results by reading extra elements and
re-ranking them in memory.

Parameters:

* **`refine_factor`**
  (`int`)
  –

  The refine factor to use.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### vector

```
vector(vector: Union[ndarray, list]) -> LanceHybridQueryBuilder
```

#### text

```
text(text: str | FullTextQuery) -> LanceHybridQueryBuilder
```

#### bypass\_vector\_index

```
bypass_vector_index() -> LanceHybridQueryBuilder
```

If this is called then any vector index is skipped

An exhaustive (flat) search will be performed. The query vector will
be compared to every vector in the table. At high scales this can be
expensive. However, this is often still useful. For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

Returns:

* `LanceHybridQueryBuilder`
  –

  The LanceHybridQueryBuilder object.

#### explain\_plan

```
explain_plan(verbose: Optional[bool] = False) -> str
```

Return the execution plan for this query.

Examples:

```
>>> importlancedb
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", [{"vector": [99.0, 99]}])
>>> query = [100, 100]
>>> plan = table.search(query).explain_plan(True)
>>> print(plan)
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...
```

Parameters:

* **`verbose`**
  (`bool`, default:
  `False`
  )
  –

  Use a verbose output format.

Returns:

* **`plan`** ( `str`
  ) –

#### analyze\_plan

```
analyze_plan()
```

Execute the query and display with runtime metrics.

Returns:

* **`plan`** ( `str`
  ) –

## Embeddings

### lancedb.embeddings.registry.EmbeddingFunctionRegistry

This is a singleton class used to register embedding functions
and fetch them by name. It also handles serializing and deserializing.
You can implement your own embedding function by subclassing EmbeddingFunction
or TextEmbeddingFunction and registering it with the registry.

NOTE: Here TEXT is a type alias for Union[str, List[str], pa.Array,
pa.ChunkedArray, np.ndarray]

Examples:

```
>>> registry = EmbeddingFunctionRegistry.get_instance()
>>> @registry.register("my-embedding-function")
... classMyEmbeddingFunction(EmbeddingFunction):
...     defndims(self) -> int:
...         return 128
...
...     defcompute_query_embeddings(self, query: str, *args, **kwargs):
...         return self.compute_source_embeddings(query, *args, **kwargs)
...
...     defcompute_source_embeddings(self, texts, *args, **kwargs):
...         return [np.random.rand(self.ndims()) for _ in range(len(texts))]
...
>>> registry.get("my-embedding-function")
<class 'lancedb.embeddings.registry.MyEmbeddingFunction'>
```

#### get\_instance

```
get_instance()
```

#### register

```
register(alias: Optional[str] = None)
```

This creates a decorator that can be used to register
an EmbeddingFunction.

Parameters:

* **`alias`**
  (`Optional[str]`, default:
  `None`
  )
  –

  a human friendly name for the embedding function. If not
  provided, the class name will be used.

#### reset

```
reset()
```

Reset the registry to its initial state

#### get

```
get(name: str) -> Type[EmbeddingFunction]
```

Fetch an embedding function class by name

Parameters:

* **`name`**
  (`str`)
  –

  The name of the embedding function to fetch
  Either the alias or the class name if no alias was provided
  during registration

#### parse\_functions

```
parse_functions(metadata: Optional[Dict[bytes, bytes]]) -> Dict[str, EmbeddingFunctionConfig]
```

Parse the metadata from an arrow table and
return a mapping of the vector column to the
embedding function and source column

Parameters:

* **`metadata`**
  (`Optional[Dict[bytes, bytes]]`)
  –

  The metadata from an arrow table. Note that
  the keys and values are bytes (pyarrow api)

Returns:

* **`functions`** ( `dict`
  ) –

  A mapping of vector column name to embedding function.
  An empty dict is returned if input is None or does not
  contain b"embedding\_functions".

#### function\_to\_metadata

```
function_to_metadata(conf: EmbeddingFunctionConfig)
```

Convert the given embedding function and source / vector column configs
into a config dictionary that can be serialized into arrow metadata

#### get\_table\_metadata

```
get_table_metadata(func_list)
```

Convert a list of embedding functions and source / vector configs
into a config dictionary that can be serialized into arrow metadata

#### set\_var

```
set_var(name: str, value: str) -> None
```

Set a variable. These can be accessed in embedding configuration using
the syntax `$var:variable_name`. If they are not set, an error will be
thrown letting you know which variable is missing. If you want to supply
a default value, you can add an additional part in the configuration
like so: `$var:variable_name:default_value`. Default values can be
used for runtime configurations that are not sensitive, such as
whether to use a GPU for inference.

The name must not contain a colon. Default values can contain colons.

#### get\_var

```
get_var(name: str) -> str
```

Get a variable.

### lancedb.embeddings.base.EmbeddingFunctionConfig

Bases: `BaseModel`

This model encapsulates the configuration for a embedding function
in a lancedb table. It holds the embedding function, the source column,
and the vector column

#### vector\_column

```
vector_column: str
```

#### source\_column

```
source_column: str
```

#### function

```
function: EmbeddingFunction
```

### lancedb.embeddings.base.EmbeddingFunction

Bases: `BaseModel`, `ABC`

An ABC for embedding functions.

All concrete embedding functions must implement the following methods:
1. compute\_query\_embeddings() which takes a query and returns a list of embeddings
2. compute\_source\_embeddings() which returns a list of embeddings for
the source column
For text data, the two will be the same. For multi-modal data, the source column
might be images and the vector column might be text.
3. ndims() which returns the number of dimensions of the vector column

#### max\_retries

```
max_retries: int = 7
```

#### create

```
create(**kwargs)
```

Create an instance of the embedding function

#### sensitive\_keys

```
sensitive_keys() -> List[str]
```

Return a list of keys that are sensitive and should not be allowed
to be set to hardcoded values in the config. For example, API keys.

#### compute\_query\_embeddings

```
compute_query_embeddings(*args, **kwargs) -> list[Union[array, None]]
```

Compute the embeddings for a given user query

Returns:

* `A list of embeddings for each input. The embedding of each input can be None`
  –
* `when the embedding is not valid.`
  –

#### compute\_source\_embeddings

```
compute_source_embeddings(*args, **kwargs) -> list[Union[array, None]]
```

Compute the embeddings for the source column in the database

Returns:

* `A list of embeddings for each input. The embedding of each input can be None`
  –
* `when the embedding is not valid.`
  –

#### compute\_query\_embeddings\_with\_retry

```
compute_query_embeddings_with_retry(*args, **kwargs) -> list[Union[array, None]]
```

Compute the embeddings for a given user query with retries

Returns:

* `A list of embeddings for each input. The embedding of each input can be None`
  –
* `when the embedding is not valid.`
  –

#### compute\_source\_embeddings\_with\_retry

```
compute_source_embeddings_with_retry(*args, **kwargs) -> list[Union[array, None]]
```

Compute the embeddings for the source column in the database with retries.

Returns:

* `A list of embeddings for each input. The embedding of each input can be None`
  –
* `when the embedding is not valid.`
  –

#### sanitize\_input

```
sanitize_input(texts: TEXT) -> Union[List[str], ndarray]
```

Sanitize the input to the embedding function.

#### safe\_model\_dump

```
safe_model_dump()
```

#### ndims

```
ndims() -> int
```

Return the dimensions of the vector column

#### SourceField

```
SourceField(**kwargs)
```

Creates a pydantic Field that can automatically annotate
the source column for this embedding function

#### VectorField

```
VectorField(**kwargs)
```

Creates a pydantic Field that can automatically annotate
the target vector column for this embedding function

### lancedb.embeddings.base.TextEmbeddingFunction

Bases: `EmbeddingFunction`

A callable ABC for embedding functions that take text as input

#### compute\_query\_embeddings

```
compute_query_embeddings(query: str, *args, **kwargs) -> list[Union[array, None]]
```

#### compute\_source\_embeddings

```
compute_source_embeddings(texts: TEXT, *args, **kwargs) -> list[Union[array, None]]
```

#### generate\_embeddings

```
generate_embeddings(texts: Union[List[str], ndarray], *args, **kwargs) -> list[Union[array, None]]
```

Generate the embeddings for the given texts

### lancedb.embeddings.sentence\_transformers.SentenceTransformerEmbeddings

Bases: `TextEmbeddingFunction`

An embedding function that uses the sentence-transformers library

https://huggingface.co/sentence-transformers

Parameters:

* **`name`**
  –

  The name of the model to use.
* **`device`**
  –

  The device to use for the model
* **`normalize`**
  –

  Whether to normalize the embeddings
* **`trust_remote_code`**
  –

  Whether to trust the remote code

#### name

```
name: str = 'all-MiniLM-L6-v2'
```

#### device

```
device: str = 'cpu'
```

#### normalize

```
normalize: bool = True
```

#### trust\_remote\_code

```
trust_remote_code: bool = True
```

#### embedding\_model

```
embedding_model
```

Get the sentence-transformers embedding model specified by the
name, device, and trust\_remote\_code. This is cached so that the
model is only loaded once per process.

#### ndims

```
ndims()
```

#### generate\_embeddings

```
generate_embeddings(texts: Union[List[str], ndarray]) -> List[array]
```

Get the embeddings for the given texts

Parameters:

* **`texts`**
  (`Union[List[str], ndarray]`)
  –

  The texts to embed

#### get\_embedding\_model

```
get_embedding_model()
```

Get the sentence-transformers embedding model specified by the
name, device, and trust\_remote\_code. This is cached so that the
model is only loaded once per process.

TODO: use lru\_cache instead with a reasonable/configurable maxsize

### lancedb.embeddings.openai.OpenAIEmbeddings

Bases: `TextEmbeddingFunction`

An embedding function that uses the OpenAI API

https://platform.openai.com/docs/guides/embeddings

This can also be used for open source models that
are compatible with the OpenAI API.

Notes

If you're running an Ollama server locally,
you can just override the `base_url` parameter
and provide the Ollama embedding model you want
to use (https://ollama.com/library):

```
fromlancedb.embeddingsimport get_registry
openai = get_registry().get("openai")
embedding_function = openai.create(
    name="<ollama-embedding-model-name>",
    base_url="http://localhost:11434",
    )
```

#### name

```
name: str = 'text-embedding-ada-002'
```

#### dim

```
dim: Optional[int] = None
```

#### base\_url

```
base_url: Optional[str] = None
```

#### default\_headers

```
default_headers: Optional[dict] = None
```

#### organization

```
organization: Optional[str] = None
```

#### api\_key

```
api_key: Optional[str] = None
```

#### use\_azure

```
use_azure: bool = False
```

#### ndims

```
ndims()
```

#### sensitive\_keys

```
sensitive_keys()
```

#### model\_names

```
model_names()
```

#### generate\_embeddings

```
generate_embeddings(texts: Union[List[str], ndarray]) -> List[array]
```

Get the embeddings for the given texts

Parameters:

* **`texts`**
  (`Union[List[str], ndarray]`)
  –

  The texts to embed

### lancedb.embeddings.open\_clip.OpenClipEmbeddings

Bases: `EmbeddingFunction`

An embedding function that uses the OpenClip API
For multi-modal text-to-image search

https://github.com/mlfoundations/open\_clip

#### name

```
name: str = 'ViT-B-32'
```

#### pretrained

```
pretrained: str = 'laion2b_s34b_b79k'
```

#### device

```
device: str = 'cpu'
```

#### batch\_size

```
batch_size: int = 64
```

#### normalize

```
normalize: bool = True
```

#### ndims

```
ndims()
```

#### compute\_query\_embeddings

```
compute_query_embeddings(query: Union[str, Image], *args, **kwargs) -> List[ndarray]
```

Compute the embeddings for a given user query

Parameters:

* **`query`**
  (`Union[str, Image]`)
  –

  The query to embed. A query can be either text or an image.

#### generate\_text\_embeddings

```
generate_text_embeddings(text: str) -> ndarray
```

#### sanitize\_input

```
sanitize_input(images: IMAGES) -> Union[List[bytes], ndarray]
```

Sanitize the input to the embedding function.

#### compute\_source\_embeddings

```
compute_source_embeddings(images: IMAGES, *args, **kwargs) -> List[array]
```

Get the embeddings for the given images

#### generate\_image\_embedding

```
generate_image_embedding(image: Union[str, bytes, Image]) -> ndarray
```

Generate the embedding for a single image

Parameters:

* **`image`**
  (`Union[str, bytes, Image]`)
  –

  The image to embed. If the image is a str, it is treated as a uri.
  If the image is bytes, it is treated as the raw image bytes.

## Remote configuration

### lancedb.remote.ClientConfig

Configuration for the LanceDB Cloud HTTP client.

#### user\_agent

```
user_agent: str = f'LanceDB-Python-Client/{__version__}'
```

#### retry\_config

```
retry_config: RetryConfig = field(default_factory=RetryConfig)
```

#### timeout\_config

```
timeout_config: Optional[TimeoutConfig] = field(default_factory=TimeoutConfig)
```

#### extra\_headers

```
extra_headers: Optional[dict] = None
```

#### id\_delimiter

```
id_delimiter: Optional[str] = None
```

#### tls\_config

```
tls_config: Optional[TlsConfig] = None
```

#### header\_provider

```
header_provider: Optional[HeaderProvider] = None
```

#### user\_id

```
user_id: Optional[str] = None
```

### lancedb.remote.TimeoutConfig

Timeout configuration for remote HTTP client.

#### timeout

```
timeout: Optional[timedelta] = None
```

#### connect\_timeout

```
connect_timeout: Optional[timedelta] = None
```

#### read\_timeout

```
read_timeout: Optional[timedelta] = None
```

#### pool\_idle\_timeout

```
pool_idle_timeout: Optional[timedelta] = None
```

### lancedb.remote.RetryConfig

Retry configuration for the remote HTTP client.

#### retries

```
retries: Optional[int] = None
```

#### connect\_retries

```
connect_retries: Optional[int] = None
```

#### read\_retries

```
read_retries: Optional[int] = None
```

#### backoff\_factor

```
backoff_factor: Optional[float] = None
```

#### backoff\_jitter

```
backoff_jitter: Optional[float] = None
```

#### statuses

```
statuses: Optional[List[int]] = None
```

## Context

### lancedb.context.contextualize

```
contextualize(raw_df: 'pd.DataFrame') -> Contextualizer
```

Create a Contextualizer object for the given DataFrame.

Used to create context windows. Context windows are rolling subsets of text
data.

The input text column should already be separated into rows that will be the
unit of the window. So to create a context window over tokens, start with
a DataFrame with one token per row. To create a context window over sentences,
start with a DataFrame with one sentence per row.

Examples:

```
>>> fromlancedb.contextimport contextualize
>>> importpandasaspd
>>> data = pd.DataFrame({
...    'token': ['The', 'quick', 'brown', 'fox', 'jumped', 'over',
...              'the', 'lazy', 'dog', 'I', 'love', 'sandwiches'],
...    'document_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
... })
```

`window` determines how many rows to include in each window. In our case
this how many tokens, but depending on the input data, it could be sentences,
paragraphs, messages, etc.

```
>>> contextualize(data).window(3).stride(1).text_col('token').to_pandas()
                token  document_id
0     The quick brown            1
1     quick brown fox            1
2    brown fox jumped            1
3     fox jumped over            1
4     jumped over the            1
5       over the lazy            1
6        the lazy dog            1
7          lazy dog I            1
8          dog I love            1
9   I love sandwiches            2
10    love sandwiches            2
>>> (contextualize(data).window(7).stride(1).min_window_size(7)
...   .text_col('token').to_pandas())
                                  token  document_id
0   The quick brown fox jumped over the            1
1  quick brown fox jumped over the lazy            1
2    brown fox jumped over the lazy dog            1
3        fox jumped over the lazy dog I            1
4       jumped over the lazy dog I love            1
5   over the lazy dog I love sandwiches            1
```

`stride` determines how many rows to skip between each window start. This can
be used to reduce the total number of windows generated.

```
>>> contextualize(data).window(4).stride(2).text_col('token').to_pandas()
                    token  document_id
0     The quick brown fox            1
2   brown fox jumped over            1
4    jumped over the lazy            1
6          the lazy dog I            1
8   dog I love sandwiches            1
10        love sandwiches            2
```

`groupby` determines how to group the rows. For example, we would like to have
context windows that don't cross document boundaries. In this case, we can
pass `document_id` as the group by.

```
>>> (contextualize(data)
...     .window(4).stride(2).text_col('token').groupby('document_id')
...     .to_pandas())
                   token  document_id
0    The quick brown fox            1
2  brown fox jumped over            1
4   jumped over the lazy            1
6           the lazy dog            1
9      I love sandwiches            2
```

`min_window_size` determines the minimum size of the context windows
that are generated.This can be used to trim the last few context windows
which have size less than `min_window_size`.
By default context windows of size 1 are skipped.

```
>>> (contextualize(data)
...     .window(6).stride(3).text_col('token').groupby('document_id')
...     .to_pandas())
                             token  document_id
0  The quick brown fox jumped over            1
3     fox jumped over the lazy dog            1
6                     the lazy dog            1
9                I love sandwiches            2
```

```
>>> (contextualize(data)
...     .window(6).stride(3).min_window_size(4).text_col('token')
...     .groupby('document_id')
...     .to_pandas())
                             token  document_id
0  The quick brown fox jumped over            1
3     fox jumped over the lazy dog            1
```

### lancedb.context.Contextualizer

Create context windows from a DataFrame.
See [lancedb.context.contextualize](#lancedb.context.contextualize).

#### window

```
window(window: int) -> Contextualizer
```

Set the window size. i.e., how many rows to include in each window.

Parameters:

* **`window`**
  (`int`)
  –

  The window size.

#### stride

```
stride(stride: int) -> Contextualizer
```

Set the stride. i.e., how many rows to skip between each window.

Parameters:

* **`stride`**
  (`int`)
  –

  The stride.

#### groupby

```
groupby(groupby: str) -> Contextualizer
```

Set the groupby column. i.e., how to group the rows.
Windows don't cross groups

Parameters:

* **`groupby`**
  (`str`)
  –

  The groupby column.

#### text\_col

```
text_col(text_col: str) -> Contextualizer
```

Set the text column used to make the context window.

Parameters:

* **`text_col`**
  (`str`)
  –

  The text column.

#### min\_window\_size

```
min_window_size(min_window_size: int) -> Contextualizer
```

Set the (optional) min\_window\_size size for the context window.

Parameters:

* **`min_window_size`**
  (`int`)
  –

  The min\_window\_size.

#### to\_df

```
to_df() -> 'pd.DataFrame'
```

#### to\_pandas

```
to_pandas() -> 'pd.DataFrame'
```

Create the context windows and return a DataFrame.

## Full text search

### lancedb.fts.create\_index

```
create_index(index_path: str, text_fields: List[str], ordering_fields: Optional[List[str]] = None, tokenizer_name: str = 'default') -> Index
```

Create a new Index (not populated)

Parameters:

* **`index_path`**
  (`str`)
  –

  Path to the index directory
* **`text_fields`**
  (`List[str]`)
  –

  List of text fields to index
* **`ordering_fields`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  List of unsigned type fields to order by at search time
* **`tokenizer_name`**
  (`str`, default:
  `"default"`
  )
  –

  The tokenizer to use

Returns:

* **`index`** ( `Index`
  ) –

  The index object (not yet populated)

### lancedb.fts.populate\_index

```
populate_index(index: Index, table: LanceTable, fields: List[str], writer_heap_size: Optional[int] = None, ordering_fields: Optional[List[str]] = None) -> int
```

Populate an index with data from a LanceTable

Parameters:

* **`index`**
  (`Index`)
  –

  The index object
* **`table`**
  (`LanceTable`)
  –

  The table to index
* **`fields`**
  (`List[str]`)
  –

  List of fields to index
* **`writer_heap_size`**
  (`int`, default:
  `None`
  )
  –

  The writer heap size in bytes, defaults to 1GB

Returns:

* `int`
  –

  The number of rows indexed

### lancedb.fts.search\_index

```
search_index(index: Index, query: str, limit: int = 10, ordering_field=None) -> Tuple[Tuple[int], Tuple[float]]
```

Search an index for a query

Parameters:

* **`index`**
  (`Index`)
  –

  The index object
* **`query`**
  (`str`)
  –

  The query string
* **`limit`**
  (`int`, default:
  `10`
  )
  –

  The maximum number of results to return

Returns:

* **`ids_and_score`** ( `list[tuple[int], tuple[float]]`
  ) –

  A tuple of two tuples, the first containing the document ids
  and the second containing the scores

## Utilities

### lancedb.schema.vector

```
vector(dimension: int, value_type: DataType = pa.float32()) -> DataType
```

A help function to create a vector type.

Parameters:

* **`dimension`**
  (`int`)
  –
* **`value_type`**
  (`DataType`, default:
  `float32()`
  )
  –

  The type of the value in the vector.

Returns:

* `A PyArrow DataType for vectors.`
  –

Examples:

```
>>> importpyarrowaspa
>>> importlancedb
>>> schema = pa.schema([
...     pa.field("id", pa.int64()),
...     pa.field("vector", lancedb.vector(756)),
... ])
```

### lancedb.merge.LanceMergeInsertBuilder

Bases: `object`

Builder for a LanceDB merge insert operation

See [`merge_insert`](#lancedb.table.Table.merge_insert) for
more context

#### when\_matched\_update\_all

```
when_matched_update_all(*, where: Optional[str] = None) -> LanceMergeInsertBuilder
```

Rows that exist in both the source table (new data) and
the target table (old data) will be updated, replacing
the old row with the corresponding matching row.

If there are multiple matches then the behavior is undefined.
Currently this causes multiple copies of the row to be created
but that behavior is subject to change.

#### when\_not\_matched\_insert\_all

```
when_not_matched_insert_all() -> LanceMergeInsertBuilder
```

Rows that exist only in the source table (new data) should
be inserted into the target table.

#### when\_not\_matched\_by\_source\_delete

```
when_not_matched_by_source_delete(condition: Optional[str] = None) -> LanceMergeInsertBuilder
```

Rows that exist only in the target table (old data) will be
deleted. An optional condition can be provided to limit what
data is deleted.

Parameters:

* **`condition`**
  (`Optional[str]`, default:
  `None`
  )
  –

  If None then all such rows will be deleted. Otherwise the
  condition will be used as an SQL filter to limit what rows
  are deleted.

#### use\_index

```
use_index(use_index: bool) -> LanceMergeInsertBuilder
```

Controls whether to use indexes for the merge operation.

When set to `True` (the default), the operation will use an index if available
on the join key for improved performance. When set to `False`, it forces a full
table scan even if an index exists. This can be useful for benchmarking or when
the query optimizer chooses a suboptimal path.

Parameters:

* **`use_index`**
  (`bool`)
  –

  Whether to use indices for the merge operation. Defaults to `True`.

#### execute

```
execute(new_data: DATA, on_bad_vectors: str = 'error', fill_value: float = 0.0, timeout: Optional[timedelta] = None) -> MergeInsertResult
```

Executes the merge insert operation

Nothing is returned but the [`Table`](#lancedb.table.Table) is updated

Parameters:

* **`new_data`**
  (`DATA`)
  –

  New records which will be matched against the existing records
  to potentially insert or update into the table. This parameter
  can be anything you use for [`add`](#lancedb.table.Table.add)
* **`on_bad_vectors`**
  (`str`, default:
  `'error'`
  )
  –

  What to do if any of the vectors are not the same size or contains NaNs.
  One of "error", "drop", "fill".
* **`fill_value`**
  (`float`, default:
  `0.0`
  )
  –

  The value to use when filling vectors. Only used if on\_bad\_vectors="fill".
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  Maximum time to run the operation before cancelling it.

  By default, there is a 30-second timeout that is only enforced after the
  first attempt. This is to prevent spending too long retrying to resolve
  conflicts. For example, if a write attempt takes 20 seconds and fails,
  the second attempt will be cancelled after 10 seconds, hitting the
  30-second timeout. However, a write that takes one hour and succeeds on the
  first attempt will not be cancelled.

  When this is set, the timeout is enforced on all attempts, including
  the first.

Returns:

* `MergeInsertResult`
  –

  version: the new version number of the table after doing merge insert.

## Integrations

## Pydantic

### lancedb.pydantic.pydantic\_to\_schema

```
pydantic_to_schema(model: Type[BaseModel]) -> Schema
```

Convert a [Pydantic Model](https://docs.pydantic.dev/latest/api/pydantic/base_model/#pydantic.BaseModel) to a
[PyArrow Schema](https://arrow.apache.org/docs/python/generated/pyarrow.Schema.html#pyarrow.Schema).

Parameters:

* **`model`**
  (`Type[BaseModel]`)
  –

  The Pydantic BaseModel to convert to Arrow Schema.

Returns:

* `Schema`
  –

  The Arrow Schema

Examples:

```
>>> fromtypingimport List, Optional
>>> importpydantic
>>> fromlancedb.pydanticimport pydantic_to_schema, Vector
>>> classFooModel(pydantic.BaseModel):
...     id: int
...     s: str
...     vec: Vector(1536)  # fixed_size_list<item: float32>[1536]
...     li: List[int]
...
>>> schema = pydantic_to_schema(FooModel)
>>> assert schema == pa.schema([
...     pa.field("id", pa.int64(), False),
...     pa.field("s", pa.utf8(), False),
...     pa.field("vec", pa.list_(pa.float32(), 1536)),
...     pa.field("li", pa.list_(pa.int64()), False),
... ])
```

### lancedb.pydantic.vector

```
vector(dim: int, value_type: DataType = pa.float32())
```

### lancedb.pydantic.LanceModel

Bases: `BaseModel`

A Pydantic Model base class that can be converted to a LanceDB Table.

Examples:

```
>>> importlancedb
>>> fromlancedb.pydanticimport LanceModel, Vector
>>>
>>> classTestModel(LanceModel):
...     name: str
...     vector: Vector(2)
...
>>> db = lancedb.connect("./example")
>>> table = db.create_table("test", schema=TestModel)
>>> table.add([
...     TestModel(name="test", vector=[1.0, 2.0])
... ])
AddResult(version=2)
>>> table.search([0., 0.]).limit(1).to_pydantic(TestModel)
[TestModel(name='test', vector=FixedSizeList(dim=2))]
```

#### to\_arrow\_schema

```
to_arrow_schema()
```

Get the Arrow Schema for this model.

#### field\_names

```
field_names() -> List[str]
```

Get the field names of this model.

#### safe\_get\_fields

```
safe_get_fields()
```

#### parse\_embedding\_functions

```
parse_embedding_functions() -> List['EmbeddingFunctionConfig']
```

Parse the embedding functions from this model.

## Reranking

### lancedb.rerankers.linear\_combination.LinearCombinationReranker

Bases: `Reranker`

Reranks the results using a linear combination of the scores from the
vector and FTS search. For missing scores, fill with `fill` value.

Parameters:

* **`weight`**
  (`float`, default:
  `0.7`
  )
  –

  The weight to give to the vector score. Must be between 0 and 1.
* **`fill`**
  (`float`, default:
  `1.0`
  )
  –

  The score to give to results that are only in one of the two result sets.
  This is treated as penalty, so a higher value means a lower score.
  TODO: We should just hardcode this--
  its pretty confusing as we invert scores to calculate final score
* **`return_score`**
  (`str`, default:
  `"relevance"`
  )
  –

  opntions are "relevance" or "all"
  The type of score to return. If "relevance", will return only the relevance
  score. If "all", will return all scores from the vector and FTS search along
  with the relevance score.

#### weight

```
weight = weight
```

#### fill

```
fill = fill
```

#### rerank\_hybrid

```
rerank_hybrid(query: str, vector_results: Table, fts_results: Table)
```

#### merge\_results

```
merge_results(vector_results: Table, fts_results: Table, fill: float)
```

### lancedb.rerankers.cohere.CohereReranker

Bases: `Reranker`

Reranks the results using the Cohere Rerank API.
https://docs.cohere.com/docs/rerank-guide

Parameters:

* **`model_name`**
  (`str`, default:
  `"rerank-english-v2.0"`
  )
  –

  The name of the cross encoder model to use. Available cohere models are:
  - rerank-english-v2.0
  - rerank-multilingual-v2.0
* **`column`**
  (`str`, default:
  `"text"`
  )
  –

  The name of the column to use as input to the cross encoder model.
* **`top_n`**
  (`str`, default:
  `None`
  )
  –

  The number of results to return. If None, will return all results.

#### model\_name

```
model_name = model_name
```

#### column

```
column = column
```

#### top\_n

```
top_n = top_n
```

#### api\_key

```
api_key = api_key
```

#### rerank\_hybrid

```
rerank_hybrid(query: str, vector_results: Table, fts_results: Table)
```

#### rerank\_vector

```
rerank_vector(query: str, vector_results: Table)
```

#### rerank\_fts

```
rerank_fts(query: str, fts_results: Table)
```

### lancedb.rerankers.colbert.ColbertReranker

Bases: `AnswerdotaiRerankers`

Reranks the results using the ColBERT model.

Parameters:

* **`model_name`**
  (`str`, default:
  `"colbert" (colbert-ir/colbert-v2.0)`
  )
  –

  The name of the cross encoder model to use.
* **`column`**
  (`str`, default:
  `"text"`
  )
  –

  The name of the column to use as input to the cross encoder model.
* **`return_score`**
  (`str`, default:
  `"relevance"`
  )
  –

  options are "relevance" or "all". Only "relevance" is supported for now.
* **`**kwargs`**
  –

  Additional keyword arguments to pass to the model, for example, 'device'.
  See AnswerDotAI/rerankers for more information.

### lancedb.rerankers.cross\_encoder.CrossEncoderReranker

Bases: `Reranker`

Reranks the results using a cross encoder model. The cross encoder model is
used to score the query and each result. The results are then sorted by the score.

Parameters:

* **`model_name`**
  (`str`, default:
  `"cross-encoder/ms-marco-TinyBERT-L-6"`
  )
  –

  The name of the cross encoder model to use. See the sentence transformers
  documentation for a list of available models.
* **`column`**
  (`str`, default:
  `"text"`
  )
  –

  The name of the column to use as input to the cross encoder model.
* **`device`**
  (`str`, default:
  `None`
  )
  –

  The device to use for the cross encoder model. If None, will use "cuda"
  if available, otherwise "cpu".
* **`return_score`**
  (`str`, default:
  `"relevance"`
  )
  –

  options are "relevance" or "all". Only "relevance" is supported for now.
* **`trust_remote_code`**
  (`bool`, default:
  `True`
  )
  –

  If True, will trust the remote code to be safe. If False, will not trust
  the remote code and will not run it

#### model\_name

```
model_name = model_name
```

#### column

```
column = column
```

#### device

```
device = device
```

#### trust\_remote\_code

```
trust_remote_code = trust_remote_code
```

#### model

```
model
```

#### rerank\_hybrid

```
rerank_hybrid(query: str, vector_results: Table, fts_results: Table)
```

#### rerank\_vector

```
rerank_vector(query: str, vector_results: Table)
```

#### rerank\_fts

```
rerank_fts(query: str, fts_results: Table)
```

### lancedb.rerankers.openai.OpenaiReranker

Bases: `Reranker`

Reranks the results using the OpenAI API.
WARNING: This is a prompt based reranker that uses chat model that is
not a dedicated reranker API. This should be treated as experimental.

Parameters:

* **`model_name`**
  (`str`, default:
  `"gpt-4-turbo-preview"`
  )
  –

  The name of the cross encoder model to use.
* **`column`**
  (`str`, default:
  `"text"`
  )
  –

  The name of the column to use as input to the cross encoder model.
* **`return_score`**
  (`str`, default:
  `"relevance"`
  )
  –

  options are "relevance" or "all". Only "relevance" is supported for now.
* **`api_key`**
  (`str`, default:
  `None`
  )
  –

  The API key to use. If None, will use the OPENAI\_API\_KEY environment variable.

#### model\_name

```
model_name = model_name
```

#### column

```
column = column
```

#### api\_key

```
api_key = api_key
```

#### rerank\_hybrid

```
rerank_hybrid(query: str, vector_results: Table, fts_results: Table)
```

#### rerank\_vector

```
rerank_vector(query: str, vector_results: Table)
```

#### rerank\_fts

```
rerank_fts(query: str, fts_results: Table)
```

## Connections (Asynchronous)

Connections represent a connection to a LanceDb database and
can be used to create, list, or open tables.

### lancedb.connect\_async

```
connect_async(uri: URI, *, api_key: Optional[str] = None, region: str = 'us-east-1', host_override: Optional[str] = None, read_consistency_interval: Optional[timedelta] = None, client_config: Optional[Union[ClientConfig, Dict[str, Any]]] = None, storage_options: Optional[Dict[str, str]] = None, session: Optional[Session] = None) -> AsyncConnection
```

Connect to a LanceDB database.

Parameters:

* **`uri`**
  (`URI`)
  –

  The uri of the database.
* **`api_key`**
  (`Optional[str]`, default:
  `None`
  )
  –

  If present, connect to LanceDB cloud.
  Otherwise, connect to a database on file system or cloud storage.
  Can be set via environment variable `LANCEDB_API_KEY`.
* **`region`**
  (`str`, default:
  `'us-east-1'`
  )
  –

  The region to use for LanceDB Cloud.
* **`host_override`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The override url for LanceDB Cloud.
* **`read_consistency_interval`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  (For LanceDB OSS only)
  The interval at which to check for updates to the table from other
  processes. If None, then consistency is not checked. For performance
  reasons, this is the default. For strong consistency, set this to
  zero seconds. Then every read will check for updates from other
  processes. As a compromise, you can set this to a non-zero timedelta
  for eventual consistency. If more than that interval has passed since
  the last check, then the table will be checked for updates. Note: this
  consistency only applies to read operations. Write operations are
  always consistent.
* **`client_config`**
  (`Optional[Union[ClientConfig, Dict[str, Any]]]`, default:
  `None`
  )
  –

  Configuration options for the LanceDB Cloud HTTP client. If a dict, then
  the keys are the attributes of the ClientConfig class. If None, then the
  default configuration is used.
* **`storage_options`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Additional options for the storage backend. See available options at
  <https://lancedb.com/docs/storage/>
* **`session`**
  (`Optional[Session]`, default:
  `None`
  )
  –

  (For LanceDB OSS only)
  A session to use for this connection. Sessions allow you to configure
  cache sizes for index and metadata caches, which can significantly
  impact memory use and performance. They can also be re-used across
  multiple connections to share the same cache state.

Examples:

```
>>> importlancedb
>>> async defdoctest_example():
...     # For a local directory, provide a path to the database
...     db = await lancedb.connect_async("~/.lancedb")
...     # For object storage, use a URI prefix
...     db = await lancedb.connect_async("s3://my-bucket/lancedb",
...                                      storage_options={
...                                          "aws_access_key_id": "***"})
...     # Connect to LanceDB cloud
...     db = await lancedb.connect_async("db://my_database", api_key="ldb_...",
...                                      client_config={
...                                          "retry_config": {"retries": 5}})
```

Returns:

* **`conn`** ( `AsyncConnection`
  ) –

  A connection to a LanceDB database.

### lancedb.db.AsyncConnection

Bases: `object`

An active LanceDB connection

To obtain a connection you can use the [connect\_async](#lancedb.connect_async)
function.

This could be a native connection (using lance) or a remote connection (e.g. for
connecting to LanceDb Cloud)

Local connections do not currently hold any open resources but they may do so in the
future (for example, for shared cache or connections to catalog services) Remote
connections represent an open connection to the remote server. The
[close](#lancedb.db.AsyncConnection.close) method can be used to release any
underlying resources eagerly. The connection can also be used as a context manager.

Connections can be shared on multiple threads and are expected to be long lived.
Connections can also be used as a context manager, however, in many cases a single
connection can be used for the lifetime of the application and so this is often
not needed. Closing a connection is optional. If it is not closed then it will
be automatically closed when the connection object is deleted.

Examples:

```
>>> importlancedb
>>> async defdoctest_example():
...   with await lancedb.connect_async("/tmp/my_dataset") as conn:
...     # do something with the connection
...     pass
...   # conn is closed here
```

#### uri

```
uri: str
```

#### is\_open

```
is_open()
```

Return True if the connection is open.

#### close

```
close()
```

Close the connection, releasing any underlying resources.

It is safe to call this method multiple times.

Any attempt to use the connection after it is closed will result in an error.

#### get\_read\_consistency\_interval

```
get_read_consistency_interval() -> Optional[timedelta]
```

#### list\_namespaces

```
list_namespaces(namespace_path: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListNamespacesResponse
```

List immediate child namespace names in the given namespace.

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The parent namespace to list namespaces in.
  None or empty list represents root namespace.
* **`page_token`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The token to use for pagination. If not present, start from the beginning.
* **`limit`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of results to return.

Returns:

* `ListNamespacesResponse`
  –

  Response containing namespace names and optional pagination token

#### create\_namespace

```
create_namespace(namespace_path: List[str], mode: Optional[str] = None, properties: Optional[Dict[str, str]] = None) -> CreateNamespaceResponse
```

Create a new namespace.

Parameters:

* **`namespace_path`**
  (`List[str]`)
  –

  The namespace identifier to create.
* **`mode`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Creation mode - "create", "exist\_ok", or "overwrite". Case insensitive.
* **`properties`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Properties to associate with the namespace

Returns:

* `CreateNamespaceResponse`
  –

  Response containing namespace properties

#### drop\_namespace

```
drop_namespace(namespace_path: List[str], mode: Optional[str] = None, behavior: Optional[str] = None) -> DropNamespaceResponse
```

Drop a namespace.

Parameters:

* **`namespace_path`**
  (`List[str]`)
  –

  The namespace identifier to drop.
* **`mode`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Whether to skip if not exists ("SKIP") or fail ("FAIL"). Case insensitive.
* **`behavior`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Whether to restrict drop if not empty ("RESTRICT") or cascade ("CASCADE").
  Case insensitive.

Returns:

* `DropNamespaceResponse`
  –

  Response containing properties and transaction\_id if applicable.

#### describe\_namespace

```
describe_namespace(namespace_path: List[str]) -> DescribeNamespaceResponse
```

Describe a namespace.

Parameters:

* **`namespace_path`**
  (`List[str]`)
  –

  The namespace identifier to describe.

Returns:

* `DescribeNamespaceResponse`
  –

  Response containing the namespace properties.

#### list\_tables

```
list_tables(namespace_path: Optional[List[str]] = None, page_token: Optional[str] = None, limit: Optional[int] = None) -> ListTablesResponse
```

List all tables in this database with pagination support.

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to list tables in.
  None or empty list represents root namespace.
* **`page_token`**
  (`Optional[str]`, default:
  `None`
  )
  –

  Token for pagination. Use the token from a previous response
  to get the next page of results.
* **`limit`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of results to return.

Returns:

* `ListTablesResponse`
  –

  Response containing table names and optional page\_token for pagination.

#### table\_names

```
table_names(*, namespace_path: Optional[List[str]] = None, start_after: Optional[str] = None, limit: Optional[int] = None) -> Iterable[str]
```

List all tables in this database, in sorted order

.. deprecated::
Use :meth:`list_tables` instead, which provides proper pagination support.

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to list tables in.
  None or empty list represents root namespace.
* **`start_after`**
  (`Optional[str]`, default:
  `None`
  )
  –

  If present, only return names that come lexicographically after the supplied
  value.

  This can be combined with limit to implement pagination by setting this to
  the last table name from the previous page.
* **`limit`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The number of results to return.

Returns:

* `Iterable of str`
  –

#### create\_table

```
create_table(name: str, data: Optional[DATA] = None, schema: Optional[Union[Schema, LanceModel]] = None, mode: Optional[Literal['create', 'overwrite']] = None, exist_ok: Optional[bool] = None, on_bad_vectors: Optional[str] = None, fill_value: Optional[float] = None, storage_options: Optional[Dict[str, str]] = None, *, namespace_path: Optional[List[str]] = None, embedding_functions: Optional[List[EmbeddingFunctionConfig]] = None, location: Optional[str] = None) -> AsyncTable
```

Create an [AsyncTable](#lancedb.table.AsyncTable) in the database.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the table.
* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to create the table in.
  Empty list represents root namespace.
* **`data`**
  (`Optional[DATA]`, default:
  `None`
  )
  –

  User must provide at least one of `data` or `schema`.
  Acceptable types are:

  + list-of-dict
  + pandas.DataFrame
  + pyarrow.Table or pyarrow.RecordBatch
* **`schema`**
  (`Optional[Union[Schema, LanceModel]]`, default:
  `None`
  )
  –

  Acceptable types are:

  + pyarrow.Schema
  + [LanceModel](#lancedb.pydantic.LanceModel)
* **`mode`**
  (`Optional[Literal['create', 'overwrite']]`, default:
  `None`
  )
  –

  The mode to use when creating the table.
  Can be either "create" or "overwrite".
  By default, if the table already exists, an exception is raised.
  If you want to overwrite the table, use mode="overwrite".
* **`exist_ok`**
  (`Optional[bool]`, default:
  `None`
  )
  –

  If a table by the same name already exists, then raise an exception
  if exist\_ok=False. If exist\_ok=True, then open the existing table;
  it will not add the provided data but will validate against any
  schema that's specified.
* **`on_bad_vectors`**
  (`Optional[str]`, default:
  `None`
  )
  –

  What to do if any of the vectors are not the same size or contains NaNs.
  One of "error", "drop", "fill".
* **`fill_value`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The value to use when filling vectors. Only used if on\_bad\_vectors="fill".
* **`storage_options`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Additional options for the storage backend. Options already set on the
  connection will be inherited by the table, but can be overridden here.
  See available options at
  <https://lancedb.com/docs/storage/>

  To enable stable row IDs (row IDs remain stable after compaction,
  update, delete, and merges), set `new_table_enable_stable_row_ids`
  to `"true"` in storage\_options when connecting to the database.

Returns:

* `AsyncTable`
  –

  A reference to the newly created table.
* `!!! note`
  –

  The vector index won't be created by default.
  To create the index, call the `create_index` method on the table.

Examples:

Can create with list of tuples or dictionaries:

```
>>> importlancedb
>>> async defdoctest_example():
...     db = await lancedb.connect_async("./.lancedb")
...     data = [{"vector": [1.1, 1.2], "lat": 45.5, "long": -122.7},
...             {"vector": [0.2, 1.8], "lat": 40.1, "long":  -74.1}]
...     my_table = await db.create_table("my_table", data)
...     print(await my_table.query().limit(5).to_arrow())
>>> importasyncio
>>> asyncio.run(doctest_example())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]
```

You can also pass a pandas DataFrame:

```
>>> importpandasaspd
>>> data = pd.DataFrame({
...    "vector": [[1.1, 1.2], [0.2, 1.8]],
...    "lat": [45.5, 40.1],
...    "long": [-122.7, -74.1]
... })
>>> async defpandas_example():
...     db = await lancedb.connect_async("./.lancedb")
...     my_table = await db.create_table("table2", data)
...     print(await my_table.query().limit(5).to_arrow())
>>> asyncio.run(pandas_example())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: double
long: double
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]
```

Data is converted to Arrow before being written to disk. For maximum
control over how data is saved, either provide the PyArrow schema to
convert to or else provide a [PyArrow Table](pyarrow.Table) directly.

```
>>> importpyarrowaspa
>>> custom_schema = pa.schema([
...   pa.field("vector", pa.list_(pa.float32(), 2)),
...   pa.field("lat", pa.float32()),
...   pa.field("long", pa.float32())
... ])
>>> async defwith_schema():
...     db = await lancedb.connect_async("./.lancedb")
...     my_table = await db.create_table("table3", data, schema = custom_schema)
...     print(await my_table.query().limit(5).to_arrow())
>>> asyncio.run(with_schema())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
lat: float
long: float
----
vector: [[[1.1,1.2],[0.2,1.8]]]
lat: [[45.5,40.1]]
long: [[-122.7,-74.1]]
```

It is also possible to create an table from `[Iterable[pa.RecordBatch]]`:

```
>>> importpyarrowaspa
>>> defmake_batches():
...     for i in range(5):
...         yield pa.RecordBatch.from_arrays(
...             [
...                 pa.array([[3.1, 4.1], [5.9, 26.5]],
...                     pa.list_(pa.float32(), 2)),
...                 pa.array(["foo", "bar"]),
...                 pa.array([10.0, 20.0]),
...             ],
...             ["vector", "item", "price"],
...         )
>>> schema=pa.schema([
...     pa.field("vector", pa.list_(pa.float32(), 2)),
...     pa.field("item", pa.utf8()),
...     pa.field("price", pa.float32()),
... ])
>>> async defiterable_example():
...     db = await lancedb.connect_async("./.lancedb")
...     await db.create_table("table4", make_batches(), schema=schema)
>>> asyncio.run(iterable_example())
```

#### open\_table

```
open_table(name: str, *, namespace_path: Optional[List[str]] = None, storage_options: Optional[Dict[str, str]] = None, index_cache_size: Optional[int] = None, location: Optional[str] = None, namespace_client: Optional[Any] = None, managed_versioning: Optional[bool] = None) -> AsyncTable
```

Open a Lance Table in the database.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the table.
* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to open the table from.
  None or empty list represents root namespace.
* **`storage_options`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  Additional options for the storage backend. Options already set on the
  connection will be inherited by the table, but can be overridden here.
  See available options at
  <https://lancedb.com/docs/storage/>
* **`index_cache_size`**
  (`Optional[int]`, default:
  `None`
  )
  –

  **Deprecated**: Use session-level cache configuration instead.
  Create a Session with custom cache sizes and pass it to lancedb.connect().

  Set the size of the index cache, specified as a number of entries

  The exact meaning of an "entry" will depend on the type of index:
  \* IVF - there is one entry for each IVF partition
  \* BTREE - there is one entry for the entire index

  This cache applies to the entire opened table, across all indices.
  Setting this value higher will increase performance on larger datasets
  at the expense of more RAM
* **`location`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The explicit location (URI) of the table. If provided, the table will be
  opened from this location instead of deriving it from the database URI
  and table name.
* **`managed_versioning`**
  (`Optional[bool]`, default:
  `None`
  )
  –

  Whether managed versioning is enabled for this table. If provided,
  avoids a redundant describe\_table call when namespace\_client is set.

Returns:

* `A LanceTable object representing the table.`
  –

#### clone\_table

```
clone_table(target_table_name: str, source_uri: str, *, target_namespace_path: Optional[List[str]] = None, source_version: Optional[int] = None, source_tag: Optional[str] = None, is_shallow: bool = True) -> AsyncTable
```

Clone a table from a source table.

A shallow clone creates a new table that shares the underlying data files
with the source table but has its own independent manifest. This allows
both the source and cloned tables to evolve independently while initially
sharing the same data, deletion, and index files.

Parameters:

* **`target_table_name`**
  (`str`)
  –

  The name of the target table to create.
* **`source_uri`**
  (`str`)
  –

  The URI of the source table to clone from.
* **`target_namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace for the target table.
  None or empty list represents root namespace.
* **`source_version`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The version of the source table to clone.
* **`source_tag`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The tag of the source table to clone.
* **`is_shallow`**
  (`bool`, default:
  `True`
  )
  –

  Whether to perform a shallow clone (True) or deep clone (False).
  Currently only shallow clone is supported.

Returns:

* `An AsyncTable object representing the cloned table.`
  –

#### rename\_table

```
rename_table(cur_name: str, new_name: str, cur_namespace_path: Optional[List[str]] = None, new_namespace_path: Optional[List[str]] = None)
```

Rename a table in the database.

Parameters:

* **`cur_name`**
  (`str`)
  –

  The current name of the table.
* **`new_name`**
  (`str`)
  –

  The new name of the table.
* **`cur_namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace of the current table.
  None or empty list represents root namespace.
* **`new_namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to move the table to.
  If not specified, defaults to the same as cur\_namespace.

#### drop\_table

```
drop_table(name: str, *, namespace_path: Optional[List[str]] = None, ignore_missing: bool = False)
```

Drop a table from the database.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the table.
* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to drop the table from.
  Empty list represents root namespace.
* **`ignore_missing`**
  (`bool`, default:
  `False`
  )
  –

  If True, ignore if the table does not exist.

#### drop\_all\_tables

```
drop_all_tables(namespace_path: Optional[List[str]] = None)
```

Drop all tables from the database.

Parameters:

* **`namespace_path`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The namespace to drop all tables from.
  None or empty list represents root namespace.

#### namespace\_client

```
namespace_client() -> LanceNamespace
```

Get the equivalent namespace client for this connection.

For native storage connections, this returns a DirectoryNamespace
pointing to the same root with the same storage options.

For namespace connections, this returns the backing namespace client.

For enterprise (remote) connections, this returns a RestNamespace
with the same URI and authentication headers.

Returns:

* `LanceNamespace`
  –

  The namespace client for this connection.

#### drop\_database

```
drop_database()
```

Drop database
This is the same thing as dropping all the tables

## Tables (Asynchronous)

Table hold your actual data as a collection of records / rows.

### lancedb.table.AsyncTable

An AsyncTable is a collection of Records in a LanceDB Database.

An AsyncTable can be obtained from the
[AsyncConnection.create\_table](#lancedb.db.AsyncConnection.create_table) and
[AsyncConnection.open\_table](#lancedb.db.AsyncConnection.open_table) methods.

An AsyncTable object is expected to be long lived and reused for multiple
operations. AsyncTable objects will cache a certain amount of index data in memory.
This cache will be freed when the Table is garbage collected. To eagerly free the
cache you can call the [close](#lancedb.table.AsyncTable.close) method. Once the
AsyncTable is closed, it cannot be used for any further operations.

An AsyncTable can also be used as a context manager, and will automatically close
when the context is exited. Closing a table is optional. If you do not close the
table, it will be closed when the AsyncTable object is garbage collected.

Examples:

Create using [AsyncConnection.create\_table](#lancedb.db.AsyncConnection.create_table)
(more examples in that method's documentation).

```
>>> importlancedb
>>> async defcreate_a_table():
...     db = await lancedb.connect_async("./.lancedb")
...     data = [{"vector": [1.1, 1.2], "b": 2}]
...     table = await db.create_table("my_table", data=data)
...     print(await table.query().limit(5).to_arrow())
>>> importasyncio
>>> asyncio.run(create_a_table())
pyarrow.Table
vector: fixed_size_list<item: float>[2]
  child 0, item: float
b: int64
----
vector: [[[1.1,1.2]]]
b: [[2]]
```

Can append new data with [AsyncTable.add()](#lancedb.table.AsyncTable.add).

```
>>> async defadd_to_table():
...     db = await lancedb.connect_async("./.lancedb")
...     table = await db.open_table("my_table")
...     await table.add([{"vector": [0.5, 1.3], "b": 4}])
>>> asyncio.run(add_to_table())
```

Can query the table with
[AsyncTable.vector\_search](#lancedb.table.AsyncTable.vector_search).

```
>>> async defsearch_table_for_vector():
...     db = await lancedb.connect_async("./.lancedb")
...     table = await db.open_table("my_table")
...     results = (
...       await table.vector_search([0.4, 0.4]).select(["b", "vector"]).to_pandas()
...     )
...     print(results)
>>> asyncio.run(search_table_for_vector())
   b      vector  _distance
0  4  [0.5, 1.3]       0.82
1  2  [1.1, 1.2]       1.13
```

Search queries are much faster when an index is created. See
[AsyncTable.create\_index](#lancedb.table.AsyncTable.create_index).

#### name

```
name: str
```

The name of the table.

#### tags

```
tags: AsyncTags
```

Tag management for the dataset.

Similar to Git, tags are a way to add metadata to a specific version of the
dataset.

.. warning::

```
Tagged versions are exempted from the
:py:meth:`optimize(cleanup_older_than)` process.

To remove a version that has been tagged, you must first
:py:meth:`~Tags.delete` the associated tag.
```

#### is\_open

```
is_open() -> bool
```

Return True if the table is open.

#### close

```
close()
```

Close the table and free any resources associated with it.

It is safe to call this method multiple times.

Any attempt to use the table after it has been closed will raise an error.

#### schema

```
schema() -> Schema
```

The [Arrow Schema](https://arrow.apache.org/docs/python/api/datatypes.html#)
of this Table

#### embedding\_functions

```
embedding_functions() -> Dict[str, EmbeddingFunctionConfig]
```

Get the embedding functions for the table

Returns:

* **`funcs`** ( `Dict[str, EmbeddingFunctionConfig]`
  ) –

  A mapping of the vector column to the embedding function
  or empty dict if not configured.

#### count\_rows

```
count_rows(filter: Optional[str] = None) -> int
```

Count the number of rows in the table.

Parameters:

* **`filter`**
  (`Optional[str]`, default:
  `None`
  )
  –

  A SQL where clause to filter the rows to count.

#### head

```
head(n=5) -> Table
```

Return the first `n` rows of the table.

Parameters:

* **`n`**
  –

  The number of rows to return.

#### query

```
query() -> AsyncQuery
```

Returns an [AsyncQuery](#lancedb.query.AsyncQuery) that can be used
to search the table.

Use methods on the returned query to control query behavior. The query
can be executed with methods like [to\_arrow](#lancedb.query.AsyncQuery.to_arrow),
[to\_pandas](#lancedb.query.AsyncQuery.to_pandas) and more.

#### to\_pandas

```
to_pandas() -> 'pd.DataFrame'
```

Return the table as a pandas DataFrame.

Returns:

* `DataFrame`
  –

#### to\_arrow

```
to_arrow() -> Table
```

Return the table as a pyarrow Table.

Returns:

* `Table`
  –

#### create\_index

```
create_index(column: str, *, replace: Optional[bool] = None, config: Optional[Union[IvfFlat, IvfPq, IvfRq, HnswPq, HnswSq, BTree, Bitmap, LabelList, FTS]] = None, wait_timeout: Optional[timedelta] = None, name: Optional[str] = None, train: bool = True)
```

Create an index to speed up queries

Indices can be created on vector columns or scalar columns.
Indices on vector columns will speed up vector searches.
Indices on scalar columns will speed up filtering (in both
vector and non-vector searches)

Parameters:

* **`column`**
  (`str`)
  –

  The column to index.
* **`replace`**
  (`Optional[bool]`, default:
  `None`
  )
  –

  Whether to replace the existing index

  If this is false, and another index already exists on the same columns
  and the same name, then an error will be returned. This is true even if
  that index is out of date.

  The default is True
* **`config`**
  (`Optional[Union[IvfFlat, IvfPq, IvfRq, HnswPq, HnswSq, BTree, Bitmap, LabelList, FTS]]`, default:
  `None`
  )
  –

  For advanced configuration you can specify the type of index you would
  like to create. You can also specify index-specific parameters when
  creating an index object.
* **`wait_timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The timeout to wait if indexing is asynchronous.
* **`name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The name of the index. If not provided, a default name will be generated.
* **`train`**
  (`bool`, default:
  `True`
  )
  –

  Whether to train the index with existing data. Vector indices always train
  with existing data.

#### drop\_index

```
drop_index(name: str) -> None
```

Drop an index from the table.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the index to drop.

Notes

This does not delete the index from disk, it just removes it from the table.
To delete the index, run [optimize](#lancedb.table.AsyncTable.optimize)
after dropping the index.

Use [list\_indices](#lancedb.table.AsyncTable.list_indices) to find the names
of the indices.

#### prewarm\_index

```
prewarm_index(name: str) -> None
```

Prewarm an index in the table.

This is a hint to the database that the index will be accessed in the
future and should be loaded into memory if possible. This can reduce
cold-start latency for subsequent queries.

This call initiates prewarming and returns once the request is accepted.
It is idempotent and safe to call from multiple clients concurrently.

It is generally wasteful to call this if the index does not fit into the
available cache. Not all index types support prewarming; unsupported
indices will silently ignore the request.

Parameters:

* **`name`**
  (`str`)
  –

  The name of the index to prewarm

#### prewarm\_data

```
prewarm_data(columns: Optional[List[str]] = None) -> None
```

Prewarm data for the table.

This is a hint to the database that the given columns will be accessed
in the future and the database should prefetch the data if possible.
Currently only supported on remote tables.

This call initiates prewarming and returns once the request is accepted.
It is idempotent and safe to call from multiple clients concurrently.

This operation has a large upfront cost but can speed up future queries
that need to fetch the given columns. Large columns such as embeddings
or binary data may not be practical to prewarm. This feature is intended
for workloads that issue many queries against the same columns.

Parameters:

* **`columns`**
  (`Optional[List[str]]`, default:
  `None`
  )
  –

  The columns to prewarm. If None, all columns are prewarmed.

#### wait\_for\_index

```
wait_for_index(index_names: Iterable[str], timeout: timedelta = timedelta(seconds=300)) -> None
```

Wait for indexing to complete for the given index names.
This will poll the table until all the indices are fully indexed,
or raise a timeout exception if the timeout is reached.

Parameters:

* **`index_names`**
  (`Iterable[str]`)
  –

  The name of the indices to poll
* **`timeout`**
  (`timedelta`, default:
  `timedelta(seconds=300)`
  )
  –

  Timeout to wait for asynchronous indexing. The default is 5 minutes.

#### stats

```
stats() -> TableStatistics
```

Retrieve table and fragment statistics.

#### uri

```
uri() -> str
```

Get the table URI (storage location).

For remote tables, this fetches the location from the server via describe.
For local tables, this returns the dataset URI.

Returns:

* `str`
  –

  The full storage location of the table (e.g., S3/GCS path).

#### initial\_storage\_options

```
initial_storage_options() -> Optional[Dict[str, str]]
```

Get the initial storage options that were passed in when opening this table.

For dynamically refreshed options (e.g., credential vending), use
:meth:`latest_storage_options`.

Warning: This is an internal API and the return value is subject to change.

Returns:

* `Optional[Dict[str, str]]`
  –

  The storage options, or None if no storage options were configured.

#### latest\_storage\_options

```
latest_storage_options() -> Optional[Dict[str, str]]
```

Get the latest storage options, refreshing from provider if configured.

This method is useful for credential vending scenarios where storage options
may be refreshed dynamically. If no dynamic provider is configured, this
returns the initial static options.

Warning: This is an internal API and the return value is subject to change.

Returns:

* `Optional[Dict[str, str]]`
  –

  The storage options, or None if no storage options were configured.

#### add

```
add(data: DATA, *, mode: Optional[Literal['append', 'overwrite']] = 'append', on_bad_vectors: Optional[OnBadVectorsType] = None, fill_value: Optional[float] = None, progress: Optional[Union[bool, Callable, Any]] = None) -> AddResult
```

Add more data to the <Table>.

Parameters:

* **`data`**
  (`DATA`)
  –

  The data to insert into the table. Acceptable types are:

  + list-of-dict
  + pandas.DataFrame
  + pyarrow.Table or pyarrow.RecordBatch
* **`mode`**
  (`Optional[Literal['append', 'overwrite']]`, default:
  `'append'`
  )
  –

  The mode to use when writing the data. Valid values are
  "append" and "overwrite".
* **`on_bad_vectors`**
  (`Optional[OnBadVectorsType]`, default:
  `None`
  )
  –

  What to do if any of the vectors are not the same size or contains NaNs.
  One of "error", "drop", "fill", "null".
* **`fill_value`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The value to use when filling vectors. Only used if on\_bad\_vectors="fill".
* **`progress`**
  (`Optional[Union[bool, Callable, Any]]`, default:
  `None`
  )
  –

  A callback or tqdm-compatible progress bar. See
  :meth:`Table.add` for details.

#### merge\_insert

```
merge_insert(on: Union[str, Iterable[str]]) -> LanceMergeInsertBuilder
```

Returns a [`LanceMergeInsertBuilder`](#lancedb.merge.LanceMergeInsertBuilder)
that can be used to create a "merge insert" operation

This operation can add rows, update rows, and remove rows all in a single
transaction. It is a very generic tool that can be used to create
behaviors like "insert if not exists", "update or insert (i.e. upsert)",
or even replace a portion of existing data with new data (e.g. replace
all data where month="january")

The merge insert operation works by combining new data from a
**source table** with existing data in a **target table** by using a
join. There are three categories of records.

"Matched" records are records that exist in both the source table and
the target table. "Not matched" records exist only in the source table
(e.g. these are new data) "Not matched by source" records exist only
in the target table (this is old data)

The builder returned by this method can be used to customize what
should happen for each category of data.

Please note that the data may appear to be reordered as part of this
operation. This is because updated rows will be deleted from the
dataset and then reinserted at the end with the new values.

Parameters:

* **`on`**
  (`Union[str, Iterable[str]]`)
  –

  A column (or columns) to join on. This is how records from the
  source table and target table are matched. Typically this is some
  kind of key or id column.

Examples:

```
>>> importlancedb
>>> data = pa.table({"a": [2, 1, 3], "b": ["a", "b", "c"]})
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> new_data = pa.table({"a": [2, 3, 4], "b": ["x", "y", "z"]})
>>> # Perform a "upsert" operation
>>> res = table.merge_insert("a")     \
...      .when_matched_update_all()     \
...      .when_not_matched_insert_all() \
...      .execute(new_data)
>>> res
MergeResult(version=2, num_updated_rows=2, num_inserted_rows=1, num_deleted_rows=0, num_attempts=1)
>>> # The order of new rows is non-deterministic since we use
>>> # a hash-join as part of this operation and so we sort here
>>> table.to_arrow().sort_by("a").to_pandas()
   a  b
0  1  b
1  2  x
2  3  y
3  4  z
```

#### search

```
search(query: Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]] = None, vector_column_name: Optional[str] = None, query_type: QueryType = 'auto', ordering_field_name: Optional[str] = None, fts_columns: Optional[Union[str, List[str]]] = None) -> Union[AsyncHybridQuery, AsyncFTSQuery, AsyncVectorQuery]
```

Create a search query to find the nearest neighbors
of the given query vector. We currently support [vector search](../../js/classes/Table/#search)
and [full-text search][experimental-full-text-search].

All query options are defined in [AsyncQuery](#lancedb.query.AsyncQuery).

Parameters:

* **`query`**
  (`Optional[Union[VEC, str, 'PIL.Image.Image', Tuple, FullTextQuery]]`, default:
  `None`
  )
  –

  The targetted vector to search for.

  + *default None*.
    Acceptable types are: list, np.ndarray, PIL.Image.Image
  + If None then the select/where/limit clauses are applied to filter
    the table
* **`vector_column_name`**
  (`Optional[str]`, default:
  `None`
  )
  –

  The name of the vector column to search.

  The vector column needs to be a pyarrow fixed size list type

  + If not specified then the vector column is inferred from
    the table schema
  + If the table has multiple vector columns then the *vector\_column\_name*
    needs to be specified. Otherwise, an error is raised.
* **`query_type`**
  (`QueryType`, default:
  `'auto'`
  )
  –

  *default "auto"*.
  Acceptable types are: "vector", "fts", "hybrid", or "auto"

  + If "auto" then the query type is inferred from the query;

    - If `query` is a list/np.ndarray then the query type is
      "vector";
    - If `query` is a PIL.Image.Image then either do vector search,
      or raise an error if no corresponding embedding function is found.
  + If `query` is a string, then the query type is "vector" if the
    table has embedding functions else the query type is "fts"

Returns:

* `LanceQueryBuilder`
  –

  A query builder object representing the query.

#### vector\_search

```
vector_search(query_vector: Union[VEC, Tuple]) -> AsyncVectorQuery
```

Search the table with a given query vector.
This is a convenience method for preparing a vector query and
is the same thing as calling `nearestTo` on the builder returned
by `query`. Seer [nearest\_to](#lancedb.query.AsyncQuery.nearest_to) for more
details.

#### delete

```
delete(where: str) -> DeleteResult
```

Delete rows from the table.

This can be used to delete a single row, many rows, all rows, or
sometimes no rows (if your predicate matches nothing).

Parameters:

* **`where`**
  (`str`)
  –

  The SQL where clause to use when deleting rows.

  + For example, 'x = 2' or 'x IN (1, 2, 3)'.

  The filter must not be empty, or it will error.

Examples:

```
>>> importlancedb
>>> data = [
...    {"x": 1, "vector": [1.0, 2]},
...    {"x": 2, "vector": [3.0, 4]},
...    {"x": 3, "vector": [5.0, 6]}
... ]
>>> db = lancedb.connect("./.lancedb")
>>> table = db.create_table("my_table", data)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  2  [3.0, 4.0]
2  3  [5.0, 6.0]
>>> table.delete("x = 2")
DeleteResult(num_deleted_rows=1, version=2)
>>> table.to_pandas()
   x      vector
0  1  [1.0, 2.0]
1  3  [5.0, 6.0]
```

If you have a list of values to delete, you can combine them into a
stringified list and use the `IN` operator:

```
>>> to_remove = [1, 5]
>>> to_remove = ", ".join([str(v) for v in to_remove])
>>> to_remove
'1, 5'
>>> table.delete(f"x IN ({to_remove})")
DeleteResult(num_deleted_rows=1, version=3)
>>> table.to_pandas()
   x      vector
0  3  [5.0, 6.0]
```

#### update

```
update(updates: Optional[Dict[str, Any]] = None, *, where: Optional[str] = None, updates_sql: Optional[Dict[str, str]] = None) -> UpdateResult
```

This can be used to update zero to all rows in the table.

If a filter is provided with `where` then only rows matching the
filter will be updated. Otherwise all rows will be updated.

Parameters:

* **`updates`**
  (`Optional[Dict[str, Any]]`, default:
  `None`
  )
  –

  The updates to apply. The keys should be the name of the column to
  update. The values should be the new values to assign. This is
  required unless updates\_sql is supplied.
* **`where`**
  (`Optional[str]`, default:
  `None`
  )
  –

  An SQL filter that controls which rows are updated. For example, 'x = 2'
  or 'x IN (1, 2, 3)'. Only rows that satisfy this filter will be udpated.
* **`updates_sql`**
  (`Optional[Dict[str, str]]`, default:
  `None`
  )
  –

  The updates to apply, expressed as SQL expression strings. The keys should
  be column names. The values should be SQL expressions. These can be SQL
  literals (e.g. "7" or "'foo'") or they can be expressions based on the
  previous value of the row (e.g. "x + 1" to increment the x column by 1)

Returns:

* `UpdateResult`
  –

  An object containing:
  - rows\_updated: The number of rows that were updated
  - version: The new version number of the table after the update

Examples:

```
>>> importasyncio
>>> importlancedb
>>> importpandasaspd
>>> async defdemo_update():
...     data = pd.DataFrame({"x": [1, 2], "vector": [[1, 2], [3, 4]]})
...     db = await lancedb.connect_async("./.lancedb")
...     table = await db.create_table("my_table", data)
...     # x is [1, 2], vector is [[1, 2], [3, 4]]
...     await table.update({"vector": [10, 10]}, where="x = 2")
...     # x is [1, 2], vector is [[1, 2], [10, 10]]
...     await table.update(updates_sql={"x": "x + 1"})
...     # x is [2, 3], vector is [[1, 2], [10, 10]]
>>> asyncio.run(demo_update())
```

#### add\_columns

```
add_columns(transforms: dict[str, str] | field | List[field] | Schema) -> AddColumnsResult
```

Add new columns with defined values.

Parameters:

* **`transforms`**
  (`dict[str, str] | field | List[field] | Schema`)
  –

  A map of column name to a SQL expression to use to calculate the
  value of the new column. These expressions will be evaluated for
  each row in the table, and can reference existing columns.
  Alternatively, you can pass a pyarrow field or schema to add
  new columns with NULLs.

Returns:

* `AddColumnsResult`
  –

  version: the new version number of the table after adding columns.

#### alter\_columns

```
alter_columns(*alterations: Iterable[dict[str, Any]]) -> AlterColumnsResult
```

Alter column names and nullability.

alterations : Iterable[Dict[str, Any]]
A sequence of dictionaries, each with the following keys:
- "path": str
The column path to alter. For a top-level column, this is the name.
For a nested column, this is the dot-separated path, e.g. "a.b.c".
- "rename": str, optional
The new name of the column. If not specified, the column name is
not changed.
- "data\_type": pyarrow.DataType, optional
The new data type of the column. Existing values will be casted
to this type. If not specified, the column data type is not changed.
- "nullable": bool, optional
Whether the column should be nullable. If not specified, the column
nullability is not changed. Only non-nullable columns can be changed
to nullable. Currently, you cannot change a nullable column to
non-nullable.

Returns:

* `AlterColumnsResult`
  –

  version: the new version number of the table after the alteration.

#### drop\_columns

```
drop_columns(columns: Iterable[str])
```

Drop columns from the table.

Parameters:

* **`columns`**
  (`Iterable[str]`)
  –

  The names of the columns to drop.

#### version

```
version() -> int
```

Retrieve the version of the table

LanceDb supports versioning. Every operation that modifies the table increases
version. As long as a version hasn't been deleted you can `[Self::checkout]`
that version to view the data at that point. In addition, you can
`[Self::restore]` the version to replace the current table with a previous
version.

#### list\_versions

```
list_versions()
```

List all versions of the table

#### checkout

```
checkout(version: int | str)
```

Checks out a specific version of the Table

Any read operation on the table will now access the data at the checked out
version. As a consequence, calling this method will disable any read consistency
interval that was previously set.

This is a read-only operation that turns the table into a sort of "view"
or "detached head". Other table instances will not be affected. To make the
change permanent you can use the `[Self::restore]` method.

Any operation that modifies the table will fail while the table is in a checked
out state.

Parameters:

* **`version`**
  (`int | str`)
  –

  The version to check out. A version number (`int`) or a tag
  (`str`) can be provided.
* **`To`**
  –

#### checkout\_latest

```
checkout_latest()
```

Ensures the table is pointing at the latest version

This can be used to manually update a table when the read\_consistency\_interval
is None
It can also be used to undo a `[Self::checkout]` operation

#### restore

```
restore(version: Optional[int | str] = None)
```

Restore the table to the currently checked out version

This operation will fail if checkout has not been called previously

This operation will overwrite the latest version of the table with a
previous version. Any changes made since the checked out version will
no longer be visible.

Once the operation concludes the table will no longer be in a checked
out state and the read\_consistency\_interval, if any, will apply.

#### take\_offsets

```
take_offsets(offsets: list[int]) -> AsyncTakeQuery
```

Take a list of offsets from the table.

Offsets are 0-indexed and relative to the current version of the table. Offsets
are not stable. A row with an offset of N may have a different offset in a
different version of the table (e.g. if an earlier row is deleted).

Offsets are mostly useful for sampling as the set of all valid offsets is easily
known in advance to be [0, len(table)).

Parameters:

* **`offsets`**
  (`list[int]`)
  –

  The offsets to take.

Returns:

* `RecordBatch`
  –

  A record batch containing the rows at the given offsets.

#### take\_row\_ids

```
take_row_ids(row_ids: list[int]) -> AsyncTakeQuery
```

Take a list of row ids from the table.

Row ids are not stable and are relative to the current version of the table.
They can change due to compaction and updates.

Unlike offsets, row ids are not 0-indexed and no assumptions should be made
about the possible range of row ids. In order to use this method you must
first obtain the row ids by scanning or searching the table.

Even so, row ids are more stable than offsets and can be useful in some
situations.

There is an ongoing effort to make row ids stable which is tracked at
https://github.com/lancedb/lancedb/issues/1120

Parameters:

* **`row_ids`**
  (`list[int]`)
  –

  The row ids to take.

Returns:

* `AsyncTakeQuery`
  –

  A query object that can be executed to get the rows.

#### optimize

```
optimize(*, cleanup_older_than: Optional[timedelta] = None, delete_unverified: bool = False, retrain=False) -> OptimizeStats
```

Optimize the on-disk data and indices for better performance.

Modeled after `VACUUM` in PostgreSQL.

Optimization covers three operations:

* Compaction: Merges small files into larger ones
* Prune: Removes old versions of the dataset
* Index: Optimizes the indices, adding new data to existing indices

Parameters:

* **`cleanup_older_than`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  All files belonging to versions older than this will be removed. Set
  to 0 days to remove all versions except the latest. The latest version
  is never removed.
* **`delete_unverified`**
  (`bool`, default:
  `False`
  )
  –

  Files leftover from a failed transaction may appear to be part of an
  in-progress operation (e.g. appending new data) and these files will not
  be deleted unless they are at least 7 days old. If delete\_unverified is True
  then these files will be deleted regardless of their age.

  .. warning::

  ```
  This should only be set to True if you can guarantee that no other
  process is currently working on this dataset. Otherwise the dataset
  could be put into a corrupted state.
  ```
* **`retrain`**
  –

  This parameter is no longer used and is deprecated.
* **`The`**
  –
* **`data`**
  –
* **`optimize`**
  –
* **`you`**
  –
* **`modification`**
  –

#### list\_indices

```
list_indices() -> Iterable[IndexConfig]
```

List all indices that have been created with Self::create\_index

#### index\_stats

```
index_stats(index_name: str) -> Optional[IndexStatistics]
```

Retrieve statistics about an index

Parameters:

* **`index_name`**
  (`str`)
  –

  The name of the index to retrieve statistics for

Returns:

* `IndexStatistics or None`
  –

  The statistics about the index. Returns None if the index does not exist.

#### uses\_v2\_manifest\_paths

```
uses_v2_manifest_paths() -> bool
```

Check if the table is using the new v2 manifest paths.

Returns:

* `bool`
  –

  True if the table is using the new v2 manifest paths, False otherwise.

#### migrate\_manifest\_paths\_v2

```
migrate_manifest_paths_v2()
```

Migrate the manifest paths to the new format.

This will update the manifest to use the new v2 format for paths.

This function is idempotent, and can be run multiple times without
changing the state of the object store.

Danger

This should not be run while other concurrent operations are happening.
And it should also run until completion before resuming other operations.

You can use
[AsyncTable.uses\_v2\_manifest\_paths](#lancedb.table.AsyncTable.uses_v2_manifest_paths)
to check if the table is already using the new path style.

#### replace\_field\_metadata

```
replace_field_metadata(field_name: str, new_metadata: dict[str, str])
```

Replace the metadata of a field in the schema

Parameters:

* **`field_name`**
  (`str`)
  –

  The name of the field to replace the metadata for
* **`new_metadata`**
  (`dict[str, str]`)
  –

  The new metadata to set

### lancedb.table.AsyncTags

Async table tag manager.

#### list

```
list() -> Dict[str, Tag]
```

List all table tags.

Returns:

* `dict[str, Tag]`
  –

  A dictionary mapping tag names to version numbers.

#### get\_version

```
get_version(tag: str) -> int
```

Get the version of a tag.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to get the version for.

#### create

```
create(tag: str, version: int) -> None
```

Create a tag for a given table version.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to create. This name must be unique among all tag
  names for the table.
* **`version`**
  (`int`)
  –

  The table version to tag.

#### delete

```
delete(tag: str) -> None
```

Delete tag from the table.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to delete.

#### update

```
update(tag: str, version: int) -> None
```

Update tag to a new version.

Parameters:

* **`tag`**
  (`str`)
  –

  The name of the tag to update.
* **`version`**
  (`int`)
  –

  The new table version to tag.

## Indices (Asynchronous)

Indices can be created on a table to speed up queries. This section
lists the indices that LanceDb supports.

### lancedb.index.BTree

Describes a btree index configuration

A btree index is an index on scalar columns. The index stores a copy of the
column in sorted order. A header entry is created for each block of rows
(currently the block size is fixed at 4096). These header entries are stored
in a separate cacheable structure (a btree). To search for data the header is
used to determine which blocks need to be read from disk.

For example, a btree index in a table with 1Bi rows requires
sizeof(Scalar) \* 256Ki bytes of memory and will generally need to read
sizeof(Scalar) \* 4096 bytes to find the correct row ids.

This index is good for scalar columns with mostly distinct values and does best
when the query is highly selective. It works with numeric, temporal, and string
columns.

The btree index does not currently have any parameters though parameters such as
the block size may be added in the future.

### lancedb.index.Bitmap

Describe a Bitmap index configuration.

A `Bitmap` index stores a bitmap for each distinct value in the column for
every row.

This index works best for low-cardinality numeric or string columns,
where the number of unique values is small (i.e., less than a few thousands).
`Bitmap` index can accelerate the following filters:

* `<`, `<=`, `=`, `>`, `>=`
* `IN (value1, value2, ...)`
* `between (value1, value2)`
* `is null`

For example, a bitmap index with a table with 1Bi rows, and 128 distinct values,
requires 128 / 8 \* 1Bi bytes on disk.

### lancedb.index.LabelList

Describe a LabelList index configuration.

`LabelList` is a scalar index that can be used on `List<T>` columns to
support queries with `array_contains_all` and `array_contains_any`
using an underlying bitmap index.

For example, it works with `tags`, `categories`, `keywords`, etc.

### lancedb.index.FTS

Describe a FTS index configuration.

`FTS` is a full-text search index that can be used on `String` columns

For example, it works with `title`, `description`, `content`, etc.

#### with\_position

```
with_position: bool = False
```

#### base\_tokenizer

```
base_tokenizer: Literal['simple', 'raw', 'whitespace'] = 'simple'
```

#### language

```
language: str = 'English'
```

#### max\_token\_length

```
max_token_length: Optional[int] = 40
```

#### lower\_case

```
lower_case: bool = True
```

#### stem

```
stem: bool = True
```

#### remove\_stop\_words

```
remove_stop_words: bool = True
```

#### ascii\_folding

```
ascii_folding: bool = True
```

#### ngram\_min\_length

```
ngram_min_length: int = 3
```

#### ngram\_max\_length

```
ngram_max_length: int = 3
```

#### prefix\_only

```
prefix_only: bool = False
```

### lancedb.index.IvfPq

Describes an IVF PQ Index

This index stores a compressed (quantized) copy of every vector. These vectors
are grouped into partitions of similar vectors. Each partition keeps track of
a centroid which is the average value of all vectors in the group.

During a query the centroids are compared with the query vector to find the
closest partitions. The compressed vectors in these partitions are then
searched to find the closest vectors.

The compression scheme is called product quantization. Each vector is divide
into subvectors and then each subvector is quantized into a small number of
bits. the parameters `num_bits` and `num_subvectors` control this process,
providing a tradeoff between index size (and thus search speed) and index
accuracy.

The partitioning process is called IVF and the `num_partitions` parameter
controls how many groups to create.

Note that training an IVF PQ index on a large dataset is a slow operation and
currently is also a memory intensive operation.

#### distance\_type

```
distance_type: Literal['l2', 'cosine', 'dot'] = 'l2'
```

#### num\_partitions

```
num_partitions: Optional[int] = None
```

#### num\_sub\_vectors

```
num_sub_vectors: Optional[int] = None
```

#### num\_bits

```
num_bits: int = 8
```

#### max\_iterations

```
max_iterations: int = 50
```

#### sample\_rate

```
sample_rate: int = 256
```

#### target\_partition\_size

```
target_partition_size: Optional[int] = None
```

### lancedb.index.HnswPq

Describe a HNSW-PQ index configuration.

HNSW-PQ stands for Hierarchical Navigable Small World - Product Quantization.
It is a variant of the HNSW algorithm that uses product quantization to compress
the vectors. To create an HNSW-PQ index, you can specify the following parameters:

Parameters:

* **`distance_type`**
  (`Literal['l2', 'cosine', 'dot']`, default:
  `'l2'`
  )
  –

  The distance metric used to train the index.

  The following distance types are available:

  "l2" - Euclidean distance. This is a very common distance metric that
  accounts for both magnitude and direction when determining the distance
  between vectors. l2 distance has a range of [0, ∞).

  "cosine" - Cosine distance. Cosine distance is a distance metric
  calculated from the cosine similarity between two vectors. Cosine
  similarity is a measure of similarity between two non-zero vectors of an
  inner product space. It is defined to equal the cosine of the angle
  between them. Unlike l2, the cosine distance is not affected by the
  magnitude of the vectors. Cosine distance has a range of [0, 2].

  "dot" - Dot product. Dot distance is the dot product of two vectors. Dot
  distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
  l2 norm is 1), then dot distance is equivalent to the cosine distance.
* **`num_partitions`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The number of IVF partitions to create.

  For HNSW, we recommend a small number of partitions. Setting this to 1 works
  well for most tables. For very large tables, training just one HNSW graph
  will require too much memory. Each partition becomes its own HNSW graph, so
  setting this value higher reduces the peak memory use of training.
* **`default`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The number of IVF partitions to create.

  For HNSW, we recommend a small number of partitions. Setting this to 1 works
  well for most tables. For very large tables, training just one HNSW graph
  will require too much memory. Each partition becomes its own HNSW graph, so
  setting this value higher reduces the peak memory use of training.
* **`num_sub_vectors`**
  (`Optional[int]`, default:
  `None`
  )
  –

  Number of sub-vectors of PQ.

  This value controls how much the vector is compressed during the
  quantization step. The more sub vectors there are the less the vector is
  compressed. The default is the dimension of the vector divided by 16.
  If the dimension is not evenly divisible by 16 we use the dimension
  divided by 8.

  The above two cases are highly preferred. Having 8 or 16 values per
  subvector allows us to use efficient SIMD instructions.

  If the dimension is not visible by 8 then we use 1 subvector. This is not
  ideal and will likely result in poor performance.

  num\_bits: int, default 8
  Number of bits to encode each sub-vector.

  This value controls how much the sub-vectors are compressed. The more bits
  the more accurate the index but the slower search. Only 4 and 8 are supported.
* **`default`**
  (`Optional[int]`, default:
  `None`
  )
  –

  Number of sub-vectors of PQ.

  This value controls how much the vector is compressed during the
  quantization step. The more sub vectors there are the less the vector is
  compressed. The default is the dimension of the vector divided by 16.
  If the dimension is not evenly divisible by 16 we use the dimension
  divided by 8.

  The above two cases are highly preferred. Having 8 or 16 values per
  subvector allows us to use efficient SIMD instructions.

  If the dimension is not visible by 8 then we use 1 subvector. This is not
  ideal and will likely result in poor performance.

  num\_bits: int, default 8
  Number of bits to encode each sub-vector.

  This value controls how much the sub-vectors are compressed. The more bits
  the more accurate the index but the slower search. Only 4 and 8 are supported.
* **`max_iterations`**
  (`int`, default:
  `50`
  )
  –

  Max iterations to train kmeans.

  When training an IVF index we use kmeans to calculate the partitions. This
  parameter controls how many iterations of kmeans to run.

  Increasing this might improve the quality of the index but in most cases the
  parameter is unused because kmeans will converge with fewer iterations. The
  parameter is only used in cases where kmeans does not appear to converge. In
  those cases it is unlikely that setting this larger will lead to the index
  converging anyways.
* **`default`**
  (`int`, default:
  `50`
  )
  –

  Max iterations to train kmeans.

  When training an IVF index we use kmeans to calculate the partitions. This
  parameter controls how many iterations of kmeans to run.

  Increasing this might improve the quality of the index but in most cases the
  parameter is unused because kmeans will converge with fewer iterations. The
  parameter is only used in cases where kmeans does not appear to converge. In
  those cases it is unlikely that setting this larger will lead to the index
  converging anyways.
* **`sample_rate`**
  (`int`, default:
  `256`
  )
  –

  The rate used to calculate the number of training vectors for kmeans.

  When an IVF index is trained, we need to calculate partitions. These are
  groups of vectors that are similar to each other. To do this we use an
  algorithm called kmeans.

  Running kmeans on a large dataset can be slow. To speed this up we
  run kmeans on a random sample of the data. This parameter controls the
  size of the sample. The total number of vectors used to train the index
  is `sample_rate * num_partitions`.

  Increasing this value might improve the quality of the index but in
  most cases the default should be sufficient.
* **`default`**
  (`int`, default:
  `256`
  )
  –

  The rate used to calculate the number of training vectors for kmeans.

  When an IVF index is trained, we need to calculate partitions. These are
  groups of vectors that are similar to each other. To do this we use an
  algorithm called kmeans.

  Running kmeans on a large dataset can be slow. To speed this up we
  run kmeans on a random sample of the data. This parameter controls the
  size of the sample. The total number of vectors used to train the index
  is `sample_rate * num_partitions`.

  Increasing this value might improve the quality of the index but in
  most cases the default should be sufficient.
* **`m`**
  (`int`, default:
  `20`
  )
  –

  The number of neighbors to select for each vector in the HNSW graph.

  This value controls the tradeoff between search speed and accuracy.
  The higher the value the more accurate the search but the slower it will be.
* **`default`**
  (`int`, default:
  `20`
  )
  –

  The number of neighbors to select for each vector in the HNSW graph.

  This value controls the tradeoff between search speed and accuracy.
  The higher the value the more accurate the search but the slower it will be.
* **`ef_construction`**
  (`int`, default:
  `300`
  )
  –

  The number of candidates to evaluate during the construction of the HNSW graph.

  This value controls the tradeoff between build speed and accuracy.
  The higher the value the more accurate the build but the slower it will be.
  150 to 300 is the typical range. 100 is a minimum for good quality search
  results. In most cases, there is no benefit to setting this higher than 500.
  This value should be set to a value that is not less than `ef` in the
  search phase.
* **`default`**
  (`int`, default:
  `300`
  )
  –

  The number of candidates to evaluate during the construction of the HNSW graph.

  This value controls the tradeoff between build speed and accuracy.
  The higher the value the more accurate the build but the slower it will be.
  150 to 300 is the typical range. 100 is a minimum for good quality search
  results. In most cases, there is no benefit to setting this higher than 500.
  This value should be set to a value that is not less than `ef` in the
  search phase.
* **`target_partition_size`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The target size of each partition.

  This value controls the tradeoff between search performance and accuracy.
  faster search but less accurate results as higher value.
* **`default`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The target size of each partition.

  This value controls the tradeoff between search performance and accuracy.
  faster search but less accurate results as higher value.

#### distance\_type

```
distance_type: Literal['l2', 'cosine', 'dot'] = 'l2'
```

#### num\_partitions

```
num_partitions: Optional[int] = None
```

#### num\_sub\_vectors

```
num_sub_vectors: Optional[int] = None
```

#### num\_bits

```
num_bits: int = 8
```

#### max\_iterations

```
max_iterations: int = 50
```

#### sample\_rate

```
sample_rate: int = 256
```

#### m

```
m: int = 20
```

#### ef\_construction

```
ef_construction: int = 300
```

#### target\_partition\_size

```
target_partition_size: Optional[int] = None
```

### lancedb.index.HnswSq

Describe a HNSW-SQ index configuration.

HNSW-SQ stands for Hierarchical Navigable Small World - Scalar Quantization.
It is a variant of the HNSW algorithm that uses scalar quantization to compress
the vectors.

Parameters:

* **`distance_type`**
  (`Literal['l2', 'cosine', 'dot']`, default:
  `'l2'`
  )
  –

  The distance metric used to train the index.

  The following distance types are available:

  "l2" - Euclidean distance. This is a very common distance metric that
  accounts for both magnitude and direction when determining the distance
  between vectors. l2 distance has a range of [0, ∞).

  "cosine" - Cosine distance. Cosine distance is a distance metric
  calculated from the cosine similarity between two vectors. Cosine
  similarity is a measure of similarity between two non-zero vectors of an
  inner product space. It is defined to equal the cosine of the angle
  between them. Unlike l2, the cosine distance is not affected by the
  magnitude of the vectors. Cosine distance has a range of [0, 2].

  "dot" - Dot product. Dot distance is the dot product of two vectors. Dot
  distance has a range of (-∞, ∞). If the vectors are normalized (i.e. their
  l2 norm is 1), then dot distance is equivalent to the cosine distance.
* **`num_partitions`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The number of IVF partitions to create.

  For HNSW, we recommend a small number of partitions. Setting this to 1 works
  well for most tables. For very large tables, training just one HNSW graph
  will require too much memory. Each partition becomes its own HNSW graph, so
  setting this value higher reduces the peak memory use of training.
* **`default`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The number of IVF partitions to create.

  For HNSW, we recommend a small number of partitions. Setting this to 1 works
  well for most tables. For very large tables, training just one HNSW graph
  will require too much memory. Each partition becomes its own HNSW graph, so
  setting this value higher reduces the peak memory use of training.
* **`max_iterations`**
  (`int`, default:
  `50`
  )
  –

  Max iterations to train kmeans.

  When training an IVF index we use kmeans to calculate the partitions.
  This parameter controls how many iterations of kmeans to run.

  Increasing this might improve the quality of the index but in most cases
  the parameter is unused because kmeans will converge with fewer iterations.
  The parameter is only used in cases where kmeans does not appear to converge.
  In those cases it is unlikely that setting this larger will lead to
  the index converging anyways.
* **`default`**
  (`int`, default:
  `50`
  )
  –

  Max iterations to train kmeans.

  When training an IVF index we use kmeans to calculate the partitions.
  This parameter controls how many iterations of kmeans to run.

  Increasing this might improve the quality of the index but in most cases
  the parameter is unused because kmeans will converge with fewer iterations.
  The parameter is only used in cases where kmeans does not appear to converge.
  In those cases it is unlikely that setting this larger will lead to
  the index converging anyways.
* **`sample_rate`**
  (`int`, default:
  `256`
  )
  –

  The rate used to calculate the number of training vectors for kmeans.

  When an IVF index is trained, we need to calculate partitions. These
  are groups of vectors that are similar to each other. To do this
  we use an algorithm called kmeans.

  Running kmeans on a large dataset can be slow. To speed this up we
  run kmeans on a random sample of the data. This parameter controls the
  size of the sample. The total number of vectors used to train the index
  is `sample_rate * num_partitions`.

  Increasing this value might improve the quality of the index but in
  most cases the default should be sufficient.
* **`default`**
  (`int`, default:
  `256`
  )
  –

  The rate used to calculate the number of training vectors for kmeans.

  When an IVF index is trained, we need to calculate partitions. These
  are groups of vectors that are similar to each other. To do this
  we use an algorithm called kmeans.

  Running kmeans on a large dataset can be slow. To speed this up we
  run kmeans on a random sample of the data. This parameter controls the
  size of the sample. The total number of vectors used to train the index
  is `sample_rate * num_partitions`.

  Increasing this value might improve the quality of the index but in
  most cases the default should be sufficient.
* **`m`**
  (`int`, default:
  `20`
  )
  –

  The number of neighbors to select for each vector in the HNSW graph.

  This value controls the tradeoff between search speed and accuracy.
  The higher the value the more accurate the search but the slower it will be.
* **`default`**
  (`int`, default:
  `20`
  )
  –

  The number of neighbors to select for each vector in the HNSW graph.

  This value controls the tradeoff between search speed and accuracy.
  The higher the value the more accurate the search but the slower it will be.
* **`ef_construction`**
  (`int`, default:
  `300`
  )
  –

  The number of candidates to evaluate during the construction of the HNSW graph.

  This value controls the tradeoff between build speed and accuracy.
  The higher the value the more accurate the build but the slower it will be.
  150 to 300 is the typical range. 100 is a minimum for good quality search
  results. In most cases, there is no benefit to setting this higher than 500.
  This value should be set to a value that is not less than `ef` in the search
  phase.
* **`default`**
  (`int`, default:
  `300`
  )
  –

  The number of candidates to evaluate during the construction of the HNSW graph.

  This value controls the tradeoff between build speed and accuracy.
  The higher the value the more accurate the build but the slower it will be.
  150 to 300 is the typical range. 100 is a minimum for good quality search
  results. In most cases, there is no benefit to setting this higher than 500.
  This value should be set to a value that is not less than `ef` in the search
  phase.
* **`target_partition_size`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The target size of each partition.

  This value controls the tradeoff between search performance and accuracy.
  faster search but less accurate results as higher value.
* **`default`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The target size of each partition.

  This value controls the tradeoff between search performance and accuracy.
  faster search but less accurate results as higher value.

#### distance\_type

```
distance_type: Literal['l2', 'cosine', 'dot'] = 'l2'
```

#### num\_partitions

```
num_partitions: Optional[int] = None
```

#### max\_iterations

```
max_iterations: int = 50
```

#### sample\_rate

```
sample_rate: int = 256
```

#### m

```
m: int = 20
```

#### ef\_construction

```
ef_construction: int = 300
```

#### target\_partition\_size

```
target_partition_size: Optional[int] = None
```

### lancedb.index.IvfFlat

Describes an IVF Flat Index

This index stores raw vectors.
These vectors are grouped into partitions of similar vectors.
Each partition keeps track of a centroid which is
the average value of all vectors in the group.

#### distance\_type

```
distance_type: Literal['l2', 'cosine', 'dot', 'hamming'] = 'l2'
```

#### num\_partitions

```
num_partitions: Optional[int] = None
```

#### max\_iterations

```
max_iterations: int = 50
```

#### sample\_rate

```
sample_rate: int = 256
```

#### target\_partition\_size

```
target_partition_size: Optional[int] = None
```

### lancedb.table.IndexStatistics

Statistics about an index.

#### num\_indexed\_rows

```
num_indexed_rows: int
```

#### num\_unindexed\_rows

```
num_unindexed_rows: int
```

#### index\_type

```
index_type: Literal['IVF_FLAT', 'IVF_SQ', 'IVF_PQ', 'IVF_RQ', 'IVF_HNSW_SQ', 'IVF_HNSW_PQ', 'FTS', 'BTREE', 'BITMAP', 'LABEL_LIST']
```

#### distance\_type

```
distance_type: Optional[Literal['l2', 'cosine', 'dot']] = None
```

#### num\_indices

```
num_indices: Optional[int] = None
```

#### loss

```
loss: Optional[float] = None
```

## Querying (Asynchronous)

Queries allow you to return data from your database. Basic queries can be
created with the [AsyncTable.query](#lancedb.table.AsyncTable.query) method
to return the entire (typically filtered) table. Vector searches return the
rows nearest to a query vector and can be created with the
[AsyncTable.vector\_search](#lancedb.table.AsyncTable.vector_search) method.

### lancedb.query.AsyncQuery

Bases: `AsyncStandardQuery`

#### to\_query\_object

```
to_query_object() -> Query
```

Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

#### select

```
select(columns: Union[List[str], dict[str, str]]) -> Self
```

Return only the specified columns.

By default a query will return all columns from the table. However, this can
have a very significant impact on latency. LanceDb stores data in a columnar
fashion. This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b". This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str]. A column will be
returned for each entry in the map. The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`. The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

#### with\_row\_id

```
with_row_id() -> Self
```

Include the \_rowid column in the results.

#### to\_batches

```
to_batches(*, max_batch_length: Optional[int] = None, timeout: Optional[timedelta] = None) -> AsyncRecordBatchReader
```

Execute the query and return the results as an Apache Arrow RecordBatchReader.

Parameters:

* **`max_batch_length`**
  (`Optional[int]`, default:
  `None`
  )
  –

  The maximum number of selected records in a single RecordBatch object.
  If not specified, a default batch length is used.
  It is possible for batches to be smaller than the provided length if the
  underlying data is stored in smaller chunks.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### output\_schema

```
output_schema() -> Schema
```

Return the output schema for the query

This does not execute the query.

#### to\_arrow

```
to_arrow(timeout: Optional[timedelta] = None) -> Table
```

Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning. If
you expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches)

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_list

```
to_list(timeout: Optional[timedelta] = None) -> List[dict]
```

Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "\_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_pandas

```
to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'
```

Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
pandas separately.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())
```

Parameters:

* **`flatten`**
  (`Optional[Union[int, bool]]`, default:
  `None`
  )
  –

  If flatten is True, flatten all nested columns.
  If flatten is an integer, flatten the nested columns up to the
  specified depth.
  If unspecified, do not flatten the nested columns.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_polars

```
to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'
```

Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
polars separately.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

Examples:

```
>>> importasyncio
>>> importpolarsaspl
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())
```

#### to\_pydantic

```
to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]
```

Convert results to a list of pydantic models.

Parameters:

* **`model`**
  (`Type[LanceModel]`)
  –

  The pydantic model to use.
* **`timeout`**
  (`timedelta`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

Returns:

* `list[LanceModel]`
  –

#### explain\_plan

```
explain_plan(verbose: Optional[bool] = False)
```

Return the execution plan for this query.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...
```

Parameters:

* **`verbose`**
  (`bool`, default:
  `False`
  )
  –

  Use a verbose output format.

Returns:

* **`plan`** ( `str`
  ) –

#### analyze\_plan

```
analyze_plan()
```

Execute the query and display with runtime metrics.

Returns:

* **`plan`** ( `str`
  ) –

#### where

```
where(predicate: Union[str, Expr]) -> Self
```

Only return rows matching the given predicate

The predicate can be a SQL string or a type-safe
:class:`~lancedb.expr.Expr` built with :func:`~lancedb.expr.col`
and :func:`~lancedb.expr.lit`.

Examples:

```
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"
```

Filtering performance can often be improved by creating a scalar index
on the filter column(s).

#### limit

```
limit(limit: int) -> Self
```

Set the maximum number of results to return.

By default, a plain search has no limit. If this method is not
called then every valid row from the table will be returned.

#### offset

```
offset(offset: int) -> Self
```

Set the offset for the results.

Parameters:

* **`offset`**
  (`int`)
  –

  The offset to start fetching results from.

#### fast\_search

```
fast_search() -> Self
```

Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
[AsyncTable.optimize](#lancedb.table.AsyncTable.optimize).

#### postfilter

```
postfilter() -> Self
```

If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search. This is how
filtering is typically understood to work. This prefilter step does add some
additional latency. Creating a scalar index on the filter column(s) can
often improve this latency. However, sometimes a filter is too complex or
scalar indices cannot be applied to the column. In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search. This
means we only run the filter on a much smaller set of data. However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}). This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

#### nearest\_to

```
nearest_to(query_vector: Union[VEC, Tuple, List[VEC]]) -> AsyncVectorQuery
```

Find the nearest vectors to the given query vector.

This converts the query from a plain query to a vector query.

This method will attempt to convert the input to the query vector
expected by the embedding model. If the input cannot be converted
then an error will be thrown.

By default, there is no embedding model, and the input should be
something that can be converted to a pyarrow array of floats. This
includes lists, numpy arrays, and tuples.

If there is only one vector column (a column whose data type is a
fixed size list of floats) then the column does not need to be specified.
If there is more than one vector column you must use
[AsyncVectorQuery.column](#lancedb.query.AsyncVectorQuery.column) to specify
which column you would like to compare with.

If no index has been created on the vector column then a vector query
will perform a distance comparison between the query vector and every
vector in the database and then sort the results. This is sometimes
called a "flat search"

For small databases, with tens of thousands of vectors or less, this can
be reasonably fast. In larger databases you should create a vector index
on the column. If there is a vector index then an "approximate" nearest
neighbor search (frequently called an ANN search) will be performed. This
search is much faster, but the results will be approximate.

The query can be further parameterized using the returned builder. There
are various ANN search parameters that will let you fine tune your recall
accuracy vs search latency.

Vector searches always have a [limit](../../js/interfaces/TableNamesOptions/#limit). If `limit` has not been called then
a default `limit` of 10 will be used.

Typically, a single vector is passed in as the query. However, you can also
pass in multiple vectors. When multiple vectors are passed in, if the vector
column is with multivector type, then the vectors will be treated as a single
query. Or the vectors will be treated as multiple queries, this can be useful
if you want to find the nearest vectors to multiple query vectors.
This is not expected to be faster than making multiple queries concurrently;
it is just a convenience method. If multiple vectors are passed in then
an additional column `query_index` will be added to the results. This column
will contain the index of the query vector that the result is nearest to.

#### nearest\_to\_text

```
nearest_to_text(query: str | FullTextQuery, columns: Union[str, List[str], None] = None) -> AsyncFTSQuery
```

Find the documents that are most relevant to the given text query.

This method will perform a full text search on the table and return
the most relevant documents. The relevance is determined by BM25.

The columns to search must be with native FTS index
(Tantivy-based can't work with this method).

By default, all indexed columns are searched,
now only one column can be searched at a time.

Parameters:

* **`query`**
  (`str | FullTextQuery`)
  –

  The text query to search for.
* **`columns`**
  (`Union[str, List[str], None]`, default:
  `None`
  )
  –

  The columns to search in. If None, all indexed columns are searched.
  For now only one column can be searched at a time.

### lancedb.query.AsyncVectorQuery

Bases: `AsyncStandardQuery`, `AsyncVectorQueryBase`

#### column

```
column(column: str) -> Self
```

Set the vector column to query

This controls which column is compared to the query vector supplied in
the call to [AsyncQuery.nearest\_to](#lancedb.query.AsyncQuery.nearest_to).

This parameter must be specified if the table has more than one column
whose data type is a fixed-size-list of floats.

#### nprobes

```
nprobes(nprobes: int) -> Self
```

Set the number of partitions to search (probe)

This argument is only used when the vector column has an IVF-based index.
If there is no index then this value is ignored.

The IVF stage of IVF PQ divides the input into partitions (clusters) of
related values.

The partition whose centroids are closest to the query vector will be
exhaustiely searched to find matches. This parameter controls how many
partitions should be searched.

Increasing this value will increase the recall of your query but will
also increase the latency of your query. The default value is 20. This
default is good for many cases but the best value to use will depend on
your data and the recall that you need to achieve.

For best results we recommend tuning this parameter with a benchmark against
your actual data to find the smallest possible value that will still give
you the desired recall.

#### minimum\_nprobes

```
minimum_nprobes(minimum_nprobes: int) -> Self
```

Set the minimum number of probes to use.

See `nprobes` for more details.

These partitions will be searched on every indexed vector query and will
increase recall at the expense of latency.

#### maximum\_nprobes

```
maximum_nprobes(maximum_nprobes: int) -> Self
```

Set the maximum number of probes to use.

See `nprobes` for more details.

If this value is greater than `minimum_nprobes` then the excess partitions
will be searched only if we have not found enough results.

This can be useful when there is a narrow filter to allow these queries to
spend more time searching and avoid potential false negatives.

If this value is 0 then no limit will be applied and all partitions could be
searched if needed to satisfy the limit.

#### distance\_range

```
distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> Self
```

Set the distance range to use.

Only rows with distances within range [lower\_bound, upper\_bound)
will be returned.

Parameters:

* **`lower_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The lower bound of the distance range.
* **`upper_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The upper bound of the distance range.

Returns:

* `AsyncVectorQuery`
  –

  The AsyncVectorQuery object.

#### ef

```
ef(ef: int) -> Self
```

Set the number of candidates to consider during search

This argument is only used when the vector column has an HNSW index.
If there is no index then this value is ignored.

Increasing this value will increase the recall of your query but will also
increase the latency of your query. The default value is 1.5 \* limit. This
default is good for many cases but the best value to use will depend on your
data and the recall that you need to achieve.

#### refine\_factor

```
refine_factor(refine_factor: int) -> Self
```

A multiplier to control how many additional rows are taken during the refine
step

This argument is only used when the vector column has an IVF PQ index.
If there is no index then this value is ignored.

An IVF PQ index stores compressed (quantized) values. They query vector is
compared against these values and, since they are compressed, the comparison is
inaccurate.

This parameter can be used to refine the results. It can improve both improve
recall and correct the ordering of the nearest results.

To refine results LanceDb will first perform an ANN search to find the nearest
`limit` \* `refine_factor` results. In other words, if `refine_factor` is 3 and
`limit` is the default (10) then the first 30 results will be selected. LanceDb
then fetches the full, uncompressed, values for these 30 results. The results
are then reordered by the true distance and only the nearest 10 are kept.

Note: there is a difference between calling this method with a value of 1 and
never calling this method at all. Calling this method with any value will have
an impact on your search latency. When you call this method with a
`refine_factor` of 1 then LanceDb still needs to fetch the full, uncompressed,
values so that it can potentially reorder the results.

Note: if this method is NOT called then the distances returned in the \_distance
column will be approximate distances based on the comparison of the quantized
query vector and the quantized result vectors. This can be considerably
different than the true distance between the query vector and the actual
uncompressed vector.

#### distance\_type

```
distance_type(distance_type: str) -> Self
```

Set the distance metric to use

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric. This parameter controls which distance metric
to use. See @see {@link IvfPqOptions.distanceType} for more details on the
different distance metrics available.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index. If this is not done then the
results will be invalid.

By default "l2" is used.

#### bypass\_vector\_index

```
bypass_vector_index() -> Self
```

If this is called then any vector index is skipped

An exhaustive (flat) search will be performed. The query vector will
be compared to every vector in the table. At high scales this can be
expensive. However, this is often still useful. For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

#### to\_query\_object

```
to_query_object() -> Query
```

Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

#### select

```
select(columns: Union[List[str], dict[str, str]]) -> Self
```

Return only the specified columns.

By default a query will return all columns from the table. However, this can
have a very significant impact on latency. LanceDb stores data in a columnar
fashion. This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b". This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str]. A column will be
returned for each entry in the map. The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`. The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

#### with\_row\_id

```
with_row_id() -> Self
```

Include the \_rowid column in the results.

#### output\_schema

```
output_schema() -> Schema
```

Return the output schema for the query

This does not execute the query.

#### to\_arrow

```
to_arrow(timeout: Optional[timedelta] = None) -> Table
```

Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning. If
you expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches)

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_list

```
to_list(timeout: Optional[timedelta] = None) -> List[dict]
```

Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "\_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_pandas

```
to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'
```

Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
pandas separately.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())
```

Parameters:

* **`flatten`**
  (`Optional[Union[int, bool]]`, default:
  `None`
  )
  –

  If flatten is True, flatten all nested columns.
  If flatten is an integer, flatten the nested columns up to the
  specified depth.
  If unspecified, do not flatten the nested columns.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_polars

```
to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'
```

Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
polars separately.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

Examples:

```
>>> importasyncio
>>> importpolarsaspl
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())
```

#### to\_pydantic

```
to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]
```

Convert results to a list of pydantic models.

Parameters:

* **`model`**
  (`Type[LanceModel]`)
  –

  The pydantic model to use.
* **`timeout`**
  (`timedelta`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

Returns:

* `list[LanceModel]`
  –

#### explain\_plan

```
explain_plan(verbose: Optional[bool] = False)
```

Return the execution plan for this query.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...
```

Parameters:

* **`verbose`**
  (`bool`, default:
  `False`
  )
  –

  Use a verbose output format.

Returns:

* **`plan`** ( `str`
  ) –

#### analyze\_plan

```
analyze_plan()
```

Execute the query and display with runtime metrics.

Returns:

* **`plan`** ( `str`
  ) –

#### where

```
where(predicate: Union[str, Expr]) -> Self
```

Only return rows matching the given predicate

The predicate can be a SQL string or a type-safe
:class:`~lancedb.expr.Expr` built with :func:`~lancedb.expr.col`
and :func:`~lancedb.expr.lit`.

Examples:

```
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"
```

Filtering performance can often be improved by creating a scalar index
on the filter column(s).

#### limit

```
limit(limit: int) -> Self
```

Set the maximum number of results to return.

By default, a plain search has no limit. If this method is not
called then every valid row from the table will be returned.

#### offset

```
offset(offset: int) -> Self
```

Set the offset for the results.

Parameters:

* **`offset`**
  (`int`)
  –

  The offset to start fetching results from.

#### fast\_search

```
fast_search() -> Self
```

Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
[AsyncTable.optimize](#lancedb.table.AsyncTable.optimize).

#### postfilter

```
postfilter() -> Self
```

If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search. This is how
filtering is typically understood to work. This prefilter step does add some
additional latency. Creating a scalar index on the filter column(s) can
often improve this latency. However, sometimes a filter is too complex or
scalar indices cannot be applied to the column. In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search. This
means we only run the filter on a much smaller set of data. However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}). This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

#### rerank

```
rerank(reranker: Reranker = RRFReranker(), query_string: Optional[str] = None) -> AsyncHybridQuery
```

#### nearest\_to\_text

```
nearest_to_text(query: str | FullTextQuery, columns: Union[str, List[str], None] = None) -> AsyncHybridQuery
```

Find the documents that are most relevant to the given text query,
in addition to vector search.

This converts the vector query into a hybrid query.

This search will perform a full text search on the table and return
the most relevant documents, combined with the vector query results.
The text relevance is determined by BM25.

The columns to search must be with native FTS index
(Tantivy-based can't work with this method).

By default, all indexed columns are searched,
now only one column can be searched at a time.

Parameters:

* **`query`**
  (`str | FullTextQuery`)
  –

  The text query to search for.
* **`columns`**
  (`Union[str, List[str], None]`, default:
  `None`
  )
  –

  The columns to search in. If None, all indexed columns are searched.
  For now only one column can be searched at a time.

#### to\_batches

```
to_batches(*, max_batch_length: Optional[int] = None, timeout: Optional[timedelta] = None) -> AsyncRecordBatchReader
```

### lancedb.query.AsyncFTSQuery

Bases: `AsyncStandardQuery`

A query for full text search for LanceDB.

#### to\_query\_object

```
to_query_object() -> Query
```

Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

#### select

```
select(columns: Union[List[str], dict[str, str]]) -> Self
```

Return only the specified columns.

By default a query will return all columns from the table. However, this can
have a very significant impact on latency. LanceDb stores data in a columnar
fashion. This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b". This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str]. A column will be
returned for each entry in the map. The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`. The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

#### with\_row\_id

```
with_row_id() -> Self
```

Include the \_rowid column in the results.

#### output\_schema

```
output_schema() -> Schema
```

Return the output schema for the query

This does not execute the query.

#### to\_arrow

```
to_arrow(timeout: Optional[timedelta] = None) -> Table
```

Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning. If
you expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches)

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_list

```
to_list(timeout: Optional[timedelta] = None) -> List[dict]
```

Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "\_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_pandas

```
to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'
```

Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
pandas separately.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())
```

Parameters:

* **`flatten`**
  (`Optional[Union[int, bool]]`, default:
  `None`
  )
  –

  If flatten is True, flatten all nested columns.
  If flatten is an integer, flatten the nested columns up to the
  specified depth.
  If unspecified, do not flatten the nested columns.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_polars

```
to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'
```

Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
polars separately.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

Examples:

```
>>> importasyncio
>>> importpolarsaspl
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())
```

#### to\_pydantic

```
to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]
```

Convert results to a list of pydantic models.

Parameters:

* **`model`**
  (`Type[LanceModel]`)
  –

  The pydantic model to use.
* **`timeout`**
  (`timedelta`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

Returns:

* `list[LanceModel]`
  –

#### explain\_plan

```
explain_plan(verbose: Optional[bool] = False)
```

Return the execution plan for this query.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0]}])
...     plan = await table.query().nearest_to([1.0, 2.0]).explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
ProjectionExec: expr=[vector@0 as vector, _distance@2 as _distance]
  GlobalLimitExec: skip=0, fetch=10
    FilterExec: _distance@2 IS NOT NULL
      SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
        KNNVectorDistance: metric=l2
          LanceRead: uri=..., projection=[vector], ...
```

Parameters:

* **`verbose`**
  (`bool`, default:
  `False`
  )
  –

  Use a verbose output format.

Returns:

* **`plan`** ( `str`
  ) –

#### analyze\_plan

```
analyze_plan()
```

Execute the query and display with runtime metrics.

Returns:

* **`plan`** ( `str`
  ) –

#### where

```
where(predicate: Union[str, Expr]) -> Self
```

Only return rows matching the given predicate

The predicate can be a SQL string or a type-safe
:class:`~lancedb.expr.Expr` built with :func:`~lancedb.expr.col`
and :func:`~lancedb.expr.lit`.

Examples:

```
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"
```

Filtering performance can often be improved by creating a scalar index
on the filter column(s).

#### limit

```
limit(limit: int) -> Self
```

Set the maximum number of results to return.

By default, a plain search has no limit. If this method is not
called then every valid row from the table will be returned.

#### offset

```
offset(offset: int) -> Self
```

Set the offset for the results.

Parameters:

* **`offset`**
  (`int`)
  –

  The offset to start fetching results from.

#### fast\_search

```
fast_search() -> Self
```

Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
[AsyncTable.optimize](#lancedb.table.AsyncTable.optimize).

#### postfilter

```
postfilter() -> Self
```

If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search. This is how
filtering is typically understood to work. This prefilter step does add some
additional latency. Creating a scalar index on the filter column(s) can
often improve this latency. However, sometimes a filter is too complex or
scalar indices cannot be applied to the column. In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search. This
means we only run the filter on a much smaller set of data. However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}). This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

#### get\_query

```
get_query() -> str
```

#### rerank

```
rerank(reranker: Reranker = RRFReranker()) -> AsyncFTSQuery
```

#### nearest\_to

```
nearest_to(query_vector: Union[VEC, Tuple, List[VEC]]) -> AsyncHybridQuery
```

In addition doing text search on the LanceDB Table, also
find the nearest vectors to the given query vector.

This converts the query from a FTS Query to a Hybrid query. Results
from the vector search will be combined with results from the FTS query.

This method will attempt to convert the input to the query vector
expected by the embedding model. If the input cannot be converted
then an error will be thrown.

By default, there is no embedding model, and the input should be
something that can be converted to a pyarrow array of floats. This
includes lists, numpy arrays, and tuples.

If there is only one vector column (a column whose data type is a
fixed size list of floats) then the column does not need to be specified.
If there is more than one vector column you must use
[AsyncVectorQuery.column](#lancedb.query.AsyncVectorQuery.column) to specify
which column you would like to compare with.

If no index has been created on the vector column then a vector query
will perform a distance comparison between the query vector and every
vector in the database and then sort the results. This is sometimes
called a "flat search"

For small databases, with tens of thousands of vectors or less, this can
be reasonably fast. In larger databases you should create a vector index
on the column. If there is a vector index then an "approximate" nearest
neighbor search (frequently called an ANN search) will be performed. This
search is much faster, but the results will be approximate.

The query can be further parameterized using the returned builder. There
are various ANN search parameters that will let you fine tune your recall
accuracy vs search latency.

Hybrid searches always have a [limit](../../js/interfaces/TableNamesOptions/#limit). If `limit` has not been called then
a default `limit` of 10 will be used.

Typically, a single vector is passed in as the query. However, you can also
pass in multiple vectors. This can be useful if you want to find the nearest
vectors to multiple query vectors. This is not expected to be faster than
making multiple queries concurrently; it is just a convenience method.
If multiple vectors are passed in then an additional column `query_index`
will be added to the results. This column will contain the index of the
query vector that the result is nearest to.

#### to\_batches

```
to_batches(*, max_batch_length: Optional[int] = None, timeout: Optional[timedelta] = None) -> AsyncRecordBatchReader
```

### lancedb.query.AsyncHybridQuery

Bases: `AsyncStandardQuery`, `AsyncVectorQueryBase`

A query builder that performs hybrid vector and full text search.
Results are combined and reranked based on the specified reranker.
By default, the results are reranked using the RRFReranker, which
uses reciprocal rank fusion score for reranking.

To make the vector and fts results comparable, the scores are normalized.
Instead of normalizing scores, the `normalize` parameter can be set to "rank"
in the `rerank` method to convert the scores to ranks and then normalize them.

#### column

```
column(column: str) -> Self
```

Set the vector column to query

This controls which column is compared to the query vector supplied in
the call to [AsyncQuery.nearest\_to](#lancedb.query.AsyncQuery.nearest_to).

This parameter must be specified if the table has more than one column
whose data type is a fixed-size-list of floats.

#### nprobes

```
nprobes(nprobes: int) -> Self
```

Set the number of partitions to search (probe)

This argument is only used when the vector column has an IVF-based index.
If there is no index then this value is ignored.

The IVF stage of IVF PQ divides the input into partitions (clusters) of
related values.

The partition whose centroids are closest to the query vector will be
exhaustiely searched to find matches. This parameter controls how many
partitions should be searched.

Increasing this value will increase the recall of your query but will
also increase the latency of your query. The default value is 20. This
default is good for many cases but the best value to use will depend on
your data and the recall that you need to achieve.

For best results we recommend tuning this parameter with a benchmark against
your actual data to find the smallest possible value that will still give
you the desired recall.

#### minimum\_nprobes

```
minimum_nprobes(minimum_nprobes: int) -> Self
```

Set the minimum number of probes to use.

See `nprobes` for more details.

These partitions will be searched on every indexed vector query and will
increase recall at the expense of latency.

#### maximum\_nprobes

```
maximum_nprobes(maximum_nprobes: int) -> Self
```

Set the maximum number of probes to use.

See `nprobes` for more details.

If this value is greater than `minimum_nprobes` then the excess partitions
will be searched only if we have not found enough results.

This can be useful when there is a narrow filter to allow these queries to
spend more time searching and avoid potential false negatives.

If this value is 0 then no limit will be applied and all partitions could be
searched if needed to satisfy the limit.

#### distance\_range

```
distance_range(lower_bound: Optional[float] = None, upper_bound: Optional[float] = None) -> Self
```

Set the distance range to use.

Only rows with distances within range [lower\_bound, upper\_bound)
will be returned.

Parameters:

* **`lower_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The lower bound of the distance range.
* **`upper_bound`**
  (`Optional[float]`, default:
  `None`
  )
  –

  The upper bound of the distance range.

Returns:

* `AsyncVectorQuery`
  –

  The AsyncVectorQuery object.

#### ef

```
ef(ef: int) -> Self
```

Set the number of candidates to consider during search

This argument is only used when the vector column has an HNSW index.
If there is no index then this value is ignored.

Increasing this value will increase the recall of your query but will also
increase the latency of your query. The default value is 1.5 \* limit. This
default is good for many cases but the best value to use will depend on your
data and the recall that you need to achieve.

#### refine\_factor

```
refine_factor(refine_factor: int) -> Self
```

A multiplier to control how many additional rows are taken during the refine
step

This argument is only used when the vector column has an IVF PQ index.
If there is no index then this value is ignored.

An IVF PQ index stores compressed (quantized) values. They query vector is
compared against these values and, since they are compressed, the comparison is
inaccurate.

This parameter can be used to refine the results. It can improve both improve
recall and correct the ordering of the nearest results.

To refine results LanceDb will first perform an ANN search to find the nearest
`limit` \* `refine_factor` results. In other words, if `refine_factor` is 3 and
`limit` is the default (10) then the first 30 results will be selected. LanceDb
then fetches the full, uncompressed, values for these 30 results. The results
are then reordered by the true distance and only the nearest 10 are kept.

Note: there is a difference between calling this method with a value of 1 and
never calling this method at all. Calling this method with any value will have
an impact on your search latency. When you call this method with a
`refine_factor` of 1 then LanceDb still needs to fetch the full, uncompressed,
values so that it can potentially reorder the results.

Note: if this method is NOT called then the distances returned in the \_distance
column will be approximate distances based on the comparison of the quantized
query vector and the quantized result vectors. This can be considerably
different than the true distance between the query vector and the actual
uncompressed vector.

#### distance\_type

```
distance_type(distance_type: str) -> Self
```

Set the distance metric to use

When performing a vector search we try and find the "nearest" vectors according
to some kind of distance metric. This parameter controls which distance metric
to use. See @see {@link IvfPqOptions.distanceType} for more details on the
different distance metrics available.

Note: if there is a vector index then the distance type used MUST match the
distance type used to train the vector index. If this is not done then the
results will be invalid.

By default "l2" is used.

#### bypass\_vector\_index

```
bypass_vector_index() -> Self
```

If this is called then any vector index is skipped

An exhaustive (flat) search will be performed. The query vector will
be compared to every vector in the table. At high scales this can be
expensive. However, this is often still useful. For example, skipping
the vector index can give you ground truth results which you can use to
calculate your recall to select an appropriate value for nprobes.

#### to\_query\_object

```
to_query_object() -> Query
```

Convert the query into a query object

This is currently experimental but can be useful as the query object is pure
python and more easily serializable.

#### select

```
select(columns: Union[List[str], dict[str, str]]) -> Self
```

Return only the specified columns.

By default a query will return all columns from the table. However, this can
have a very significant impact on latency. LanceDb stores data in a columnar
fashion. This
means we can finely tune our I/O to select exactly the columns we need.

As a best practice you should always limit queries to the columns that you need.
If you pass in a list of column names then only those columns will be
returned.

You can also use this method to create new "dynamic" columns based on your
existing columns. For example, you may not care about "a" or "b" but instead
simply want "a + b". This is often seen in the SELECT clause of an SQL query
(e.g. `SELECT a+b FROM my_table`).

To create dynamic columns you can pass in a dict[str, str]. A column will be
returned for each entry in the map. The key provides the name of the column.
The value is an SQL string used to specify how the column is calculated.

For example, an SQL query might state `SELECT a + b AS combined, c`. The
equivalent input to this method would be `{"combined": "a + b", "c": "c"}`.

Columns will always be returned in the order given, even if that order is
different than the order used when adding the data.

#### with\_row\_id

```
with_row_id() -> Self
```

Include the \_rowid column in the results.

#### output\_schema

```
output_schema() -> Schema
```

Return the output schema for the query

This does not execute the query.

#### to\_arrow

```
to_arrow(timeout: Optional[timedelta] = None) -> Table
```

Execute the query and collect the results into an Apache Arrow Table.

This method will collect all results into memory before returning. If
you expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches)

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_list

```
to_list(timeout: Optional[timedelta] = None) -> List[dict]
```

Execute the query and return the results as a list of dictionaries.

Each list entry is a dictionary with the selected column names as keys,
or all table columns if `select` is not called. The vector and the "\_distance"
fields are returned whether or not they're explicitly selected.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_pandas

```
to_pandas(flatten: Optional[Union[int, bool]] = None, timeout: Optional[timedelta] = None) -> 'pd.DataFrame'
```

Execute the query and collect the results into a pandas DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
pandas separately.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = batch.to_pandas()
>>> asyncio.run(doctest_example())
```

Parameters:

* **`flatten`**
  (`Optional[Union[int, bool]]`, default:
  `None`
  )
  –

  If flatten is True, flatten all nested columns.
  If flatten is an integer, flatten the nested columns up to the
  specified depth.
  If unspecified, do not flatten the nested columns.
* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

#### to\_polars

```
to_polars(timeout: Optional[timedelta] = None) -> 'pl.DataFrame'
```

Execute the query and collect the results into a Polars DataFrame.

This method will collect all results into memory before returning. If you
expect a large number of results, you may want to use
[to\_batches](#lancedb.query.AsyncQuery.to_batches) and convert each batch to
polars separately.

Parameters:

* **`timeout`**
  (`Optional[timedelta]`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If not specified, no timeout is applied. If the query does not
  complete within the specified time, an error will be raised.

Examples:

```
>>> importasyncio
>>> importpolarsaspl
>>> fromlancedbimport connect_async
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", data=[{"a": 1, "b": 2}])
...     async for batch in await table.query().to_batches():
...         batch_df = pl.from_arrow(batch)
>>> asyncio.run(doctest_example())
```

#### to\_pydantic

```
to_pydantic(model: Type[LanceModel], *, timeout: Optional[timedelta] = None) -> List[LanceModel]
```

Convert results to a list of pydantic models.

Parameters:

* **`model`**
  (`Type[LanceModel]`)
  –

  The pydantic model to use.
* **`timeout`**
  (`timedelta`, default:
  `None`
  )
  –

  The maximum time to wait for the query to complete.
  If None, wait indefinitely.

Returns:

* `list[LanceModel]`
  –

#### where

```
where(predicate: Union[str, Expr]) -> Self
```

Only return rows matching the given predicate

The predicate can be a SQL string or a type-safe
:class:`~lancedb.expr.Expr` built with :func:`~lancedb.expr.col`
and :func:`~lancedb.expr.lit`.

Examples:

```
>>> predicate = "x > 10"
>>> predicate = "y > 0 AND y < 100"
>>> predicate = "x > 5 OR y = 'test'"
```

Filtering performance can often be improved by creating a scalar index
on the filter column(s).

#### limit

```
limit(limit: int) -> Self
```

Set the maximum number of results to return.

By default, a plain search has no limit. If this method is not
called then every valid row from the table will be returned.

#### offset

```
offset(offset: int) -> Self
```

Set the offset for the results.

Parameters:

* **`offset`**
  (`int`)
  –

  The offset to start fetching results from.

#### fast\_search

```
fast_search() -> Self
```

Skip searching un-indexed data.

This can make queries faster, but will miss any data that has not been
indexed.

Tip

You can add new data into an existing index by calling
[AsyncTable.optimize](#lancedb.table.AsyncTable.optimize).

#### postfilter

```
postfilter() -> Self
```

If this is called then filtering will happen after the search instead of
before.
By default filtering will be performed before the search. This is how
filtering is typically understood to work. This prefilter step does add some
additional latency. Creating a scalar index on the filter column(s) can
often improve this latency. However, sometimes a filter is too complex or
scalar indices cannot be applied to the column. In these cases postfiltering
can be used instead of prefiltering to improve latency.
Post filtering applies the filter to the results of the search. This
means we only run the filter on a much smaller set of data. However, it can
cause the query to return fewer than `limit` results (or even no results) if
none of the nearest results match the filter.
Post filtering happens during the "refine stage" (described in more detail in
@see {@link VectorQuery#refineFactor}). This means that setting a higher refine
factor can often help restore some of the results lost by post filtering.

#### rerank

```
rerank(reranker: Reranker = RRFReranker(), normalize: str = 'score') -> AsyncHybridQuery
```

Rerank the hybrid search results using the specified reranker. The reranker
must be an instance of Reranker class.

Parameters:

* **`reranker`**
  (`Reranker`, default:
  `RRFReranker()`
  )
  –

  The reranker to use. Must be an instance of Reranker class.
* **`normalize`**
  (`str`, default:
  `'score'`
  )
  –

  The method to normalize the scores. Can be "rank" or "score". If "rank",
  the scores are converted to ranks and then normalized. If "score", the
  scores are normalized directly.

Returns:

* `AsyncHybridQuery`
  –

  The AsyncHybridQuery object.

#### to\_batches

```
to_batches(*, max_batch_length: Optional[int] = None, timeout: Optional[timedelta] = None) -> AsyncRecordBatchReader
```

#### explain\_plan

```
explain_plan(verbose: Optional[bool] = False)
```

Return the execution plan for this query.

The output includes both the vector and FTS search plans.

Examples:

```
>>> importasyncio
>>> fromlancedbimport connect_async
>>> fromlancedb.indeximport FTS
>>> async defdoctest_example():
...     conn = await connect_async("./.lancedb")
...     table = await conn.create_table("my_table", [{"vector": [99.0, 99.0], "text": "hello world"}])
...     await table.create_index("text", config=FTS(with_position=False))
...     plan = await table.query().nearest_to([1.0, 2.0]).nearest_to_text("hello").explain_plan(True)
...     print(plan)
>>> asyncio.run(doctest_example())
RRFReranker(K=60)
    ProjectionExec: expr=[vector@0 as vector, text@3 as text, _distance@2 as _distance]
      Take: columns="vector, _rowid, _distance, (text)"
        CoalesceBatchesExec: target_batch_size=1024
          GlobalLimitExec: skip=0, fetch=10
            FilterExec: _distance@2 IS NOT NULL
              SortExec: TopK(fetch=10), expr=[_distance@2 ASC NULLS LAST, _rowid@1 ASC NULLS LAST], preserve_partitioning=[false]
                KNNVectorDistance: metric=l2
                  LanceRead: uri=..., projection=[vector], ...
    ProjectionExec: expr=[vector@2 as vector, text@3 as text, _score@1 as _score]
      Take: columns="_rowid, _score, (vector), (text)"
        CoalesceBatchesExec: target_batch_size=1024
          GlobalLimitExec: skip=0, fetch=10
            MatchQuery: column=text, query=hello
```

Parameters:

* **`verbose`**
  (`bool`, default:
  `False`
  )
  –

  Use a verbose output format.

Returns:

* **`plan`** ( `str`
  ) –

#### analyze\_plan

```
analyze_plan()
```

Execute the query and return the physical execution plan with runtime metrics.

This runs both the vector and FTS (full-text search) queries and returns
detailed metrics for each step of execution—such as rows processed,
elapsed time, I/O stats, and more. It’s useful for debugging and
performance analysis.

Returns:

* **`plan`** ( `str`
  ) –

---

## Bibliography

1. [Python API Reference](https://lancedb.github.io/lancedb/python/python/)