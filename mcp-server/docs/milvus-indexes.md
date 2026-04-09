---
id: index-vector-fields.md
order: 1
summary: This guide walks you through the basic operations on creating and managing indexes on vector fields in a collection.
title: Index Vector Fields
---
# Index Vector Fields
This guide walks you through the basic operations on creating and managing indexes on vector fields in a collection.
## Overview
Leveraging the metadata stored in an index file, Milvus organizes your data in a specialized structure, facilitating rapid retrieval of requested information during searches or queries.
Milvus provides several index types and metrics to sort field values for efficient similarity searches. The following table lists the supported index types and metrics for different vector field types. Currently, Milvus supports various types of vector data, including floating point embeddings (often known as floating point vectors or dense vectors), binary embeddings (also known as binary vectors), and sparse embeddings (also known as sparse vectors). For details, refer to [In-memory Index](index.md) and [Similarity Metrics](metric.md).

[Floating point embeddings](#floating)
[Binary embeddings](#binary)
[Sparse embeddings](#sparse)

| Metric Types | Index Types |
| --- | --- |
| * Euclidean distance (L2) * Inner product (IP) * Cosine similarity (COSINE) | * FLAT * IVF\_FLAT * IVF\_SQ8 * IVF\_PQ * GPU\_IVF\_FLAT * GPU\_IVF\_PQ * HNSW * DISKANN |

| Metric Types | Index Types |
| --- | --- |
| * Jaccard (JACCARD) * Hamming (HAMMING) | * BIN\_FLAT * BIN\_IVF\_FLAT |

| Metric Types | Index Types |
| --- | --- |
| IP | * SPARSE\_INVERTED\_INDEX * SPARSE\_WAND |

It is recommended to create indexes for both the vector field and scalar fields that are frequently accessed.
## Preparations
As explained in [Manage Collections](manage-collections.md), Milvus automatically generates an index and loads it into memory when creating a collection if any of the following conditions are specified in the collection creation request:
- The dimensionality of the vector field and the metric type, or
- The schema and the index parameters.
The code snippet below repurposes the existing code to establish a connection to a Milvus instance and create a collection without specifying its index parameters. In this case, the collection lacks an index and remains unloaded.

To prepare for indexing, use [`MilvusClient`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Client/MilvusClient.md) to connect to the Milvus server and set up a collection by using [`create\_schema()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create\_schema.md), [`add\_field()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/CollectionSchema/add\_field.md), and [`create\_collection()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create\_collection.md).

To prepare for indexing, use [`MilvusClientV2`](https://milvus.io/api-reference/java/v2.4.x/v2/Client/MilvusClientV2.md) to connect to the Milvus server and set up a collection by using [`createSchema()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/createSchema.md), [`addField()`](https://milvus.io/api-reference/java/v2.4.x/v2/CollectionSchema/addField.md), and [`createCollection()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/createCollection.md).

To prepare for indexing, use [`MilvusClient`](https://milvus.io/api-reference/node/v2.4.x/Client/MilvusClient.md) to connect to the Milvus server and set up a collection by using [`createCollection()`](https://milvus.io/api-reference/node/v2.4.x/Collections/createCollection.md).

[Python](#python) 
[Java](#java)
[Node.js](#javascript)

```python
from pymilvus import MilvusClient, DataType
# 1. Set up a Milvus client
client = MilvusClient(
uri="http://localhost:19530"
)
# 2. Create schema
# 2.1. Create schema
schema = MilvusClient.create\_schema(
auto\_id=False,
enable\_dynamic\_field=True,
)
# 2.2. Add fields to schema
schema.add\_field(field\_name="id", datatype=DataType.INT64, is\_primary=True)
schema.add\_field(field\_name="vector", datatype=DataType.FLOAT\_VECTOR, dim=5)
# 3. Create collection
client.create\_collection(
collection\_name="customized\_setup",
schema=schema,
)
```
```java
import io.milvus.v2.client.ConnectConfig;
import io.milvus.v2.client.MilvusClientV2;
import io.milvus.v2.common.DataType;
import io.milvus.v2.service.collection.request.CreateCollectionReq;
String CLUSTER\_ENDPOINT = "http://localhost:19530";
// 1. Connect to Milvus server
ConnectConfig connectConfig = ConnectConfig.builder()
.uri(CLUSTER\_ENDPOINT)
.build();
MilvusClientV2 client = new MilvusClientV2(connectConfig);
// 2. Create a collection
// 2.1 Create schema
CreateCollectionReq.CollectionSchema schema = client.createSchema();
// 2.2 Add fields to schema
schema.addField(AddFieldReq.builder().fieldName("id").dataType(DataType.Int64).isPrimaryKey(true).autoID(false).build());
schema.addField(AddFieldReq.builder().fieldName("vector").dataType(DataType.FloatVector).dimension(5).build());
// 3 Create a collection without schema and index parameters
CreateCollectionReq customizedSetupReq = CreateCollectionReq.builder()
.collectionName("customized\_setup")
.collectionSchema(schema)
.build();
client.createCollection(customizedSetupReq);
```
```javascript
// 1. Set up a Milvus Client
client = new MilvusClient({address, token});
// 2. Define fields for the collection
const fields = [
{
name: "id",
data\_type: DataType.Int64,
is\_primary\_key: true,
autoID: false
},
{
name: "vector",
data\_type: DataType.FloatVector,
dim: 5
},
]
// 3. Create a collection
res = await client.createCollection({
collection\_name: "customized\_setup",
fields: fields,
})
console.log(res.error\_code)
// Output
//
// Success
//
```
## Index a Collection

To create an index for a collection or index a collection, use [`prepare\_index\_params()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/prepare\_index\_params.md) to prepare index parameters and [`create\_index()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/create\_index.md) to create the index.

To create an index for a collection or index a collection, use [`IndexParam`](https://milvus.io/api-reference/java/v2.4.x/v2/Management/IndexParam.md) to prepare index parameters and [`createIndex()`](https://milvus.io/api-reference/java/v2.4.x/v2/Management/createIndex.md) to create the index.

To create an index for a collection or index a collection, use [`createIndex()`](https://milvus.io/api-reference/node/v2.4.x/Management/createIndex.md).

[Python](#python) 
[Java](#java)
[Node.js](#javascript)

```python
# 4.1. Set up the index parameters
index\_params = MilvusClient.prepare\_index\_params()
# 4.2. Add an index on the vector field.
index\_params.add\_index(
field\_name="vector",
metric\_type="COSINE",
index\_type="IVF\_FLAT",
index\_name="vector\_index",
params={ "nlist": 128 }
)
# 4.3. Create an index file
client.create\_index(
collection\_name="customized\_setup",
index\_params=index\_params,
sync=False # Whether to wait for index creation to complete before returning. Defaults to True.
)
```
```java
import io.milvus.v2.common.IndexParam;
import io.milvus.v2.service.index.request.CreateIndexReq;
// 4 Prepare index parameters
// 4.2 Add an index for the vector field "vector"
IndexParam indexParamForVectorField = IndexParam.builder()
.fieldName("vector")
.indexName("vector\_index")
.indexType(IndexParam.IndexType.IVF\_FLAT)
.metricType(IndexParam.MetricType.COSINE)
.extraParams(Map.of("nlist", 128))
.build();
List indexParams = new ArrayList<>();
indexParams.add(indexParamForVectorField);
// 4.3 Crate an index file
CreateIndexReq createIndexReq = CreateIndexReq.builder()
.collectionName("customized\_setup")
.indexParams(indexParams)
.build();
client.createIndex(createIndexReq);
```
```javascript
// 4. Set up index for the collection
// 4.1. Set up the index parameters
res = await client.createIndex({
collection\_name: "customized\_setup",
field\_name: "vector",
index\_type: "AUTOINDEX",
metric\_type: "COSINE",
index\_name: "vector\_index",
params: { "nlist": 128 }
})
console.log(res.error\_code)
// Output
//
// Success
//
```

| Parameter | Description |
| --- | --- |
| `field_name` | The name of the target file to apply this object applies. |
| `metric_type` | The algorithm that is used to measure similarity between vectors. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. This is available only when the specified field is a vector field. For more information, refer to [Indexes supported in Milvus](https://milvus.io/docs/index.md#Indexes-supported-in-Milvus). |
| `index_type` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `index_name` | The name of the index file generated after this object has been applied. |
| `params` | The fine-tuning parameters for the specified index type. For details on possible keys and value ranges, refer to [In-memory Index](https://milvus.io/docs/index.md). |
| `collection_name` | The name of an existing collection. |
| `index_params` | An **IndexParams** object containing a list of **IndexParam** objects. |
| `sync` | Controls how the index is built in relation to the client’s request. Valid values:   * `True` (default): The client waits until the index is fully built before it returns. This means you will not get a response until the process is complete. * `False`: The client returns immediately after the request is received and the index is being built in the background. To find out if index creation has been completed, use the [describe\_index()](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/describe_index.md) method. |

| Parameter | Description |
| --- | --- |
| `fieldName` | The name of the target field to apply this IndexParam object applies. |
| `indexName` | The name of the index file generated after this object has been applied. |
| `indexType` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `metricType` | The distance metric to use for the index. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. |
| `extraParams` | Extra index parameters. For details, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of an existing collection. |
| `field_name` | The name of the field in which to create an index. |
| `index_type` | The type of the index to create. |
| `metric_type` | The metric type used to measure vector distance. |
| `index_name` | The name of the index to create. |
| `params` | Other index-specific parameters. |

**notes**

Currently, you can create only one index file for each field in a collection.

## Check Index Details
Once you have created an index, you can check its details.

To check the index details, use [`list\_indexes()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/list\_indexes.md) to list the index names and [`describe\_index()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/describe\_index.md) to get the index details.

To check the index details, use [`describeIndex()`](https://milvus.io/api-reference/java/v2.4.x/v2/Management/describeIndex.md) to get the index details.

To check the index details, use [`describeIndex()`](https://milvus.io/api-reference/node/v2.4.x/Management/describeIndex.md) to get the index details.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)

```python
# 5. Describe index
res = client.list\_indexes(
collection\_name="customized\_setup"
)
print(res)
# Output
#
# [
# "vector\_index",
# ]
res = client.describe\_index(
collection\_name="customized\_setup",
index\_name="vector\_index"
)
print(res)
# Output
#
# {
# "index\_type": ,
# "metric\_type": "COSINE",
# "field\_name": "vector",
# "index\_name": "vector\_index"
# }
```
```java
import io.milvus.v2.service.index.request.DescribeIndexReq;
import io.milvus.v2.service.index.response.DescribeIndexResp;
// 5. Describe index
// 5.1 List the index names
ListIndexesReq listIndexesReq = ListIndexesReq.builder()
.collectionName("customized\_setup")
.build();
List indexNames = client.listIndexes(listIndexesReq);
System.out.println(indexNames);
// Output:
// [
// "vector\_index"
// ]
// 5.2 Describe an index
DescribeIndexReq describeIndexReq = DescribeIndexReq.builder()
.collectionName("customized\_setup")
.indexName("vector\_index")
.build();
DescribeIndexResp describeIndexResp = client.describeIndex(describeIndexReq);
System.out.println(JSONObject.toJSON(describeIndexResp));
// Output:
// {
// "metricType": "COSINE",
// "indexType": "AUTOINDEX",
// "fieldName": "vector",
// "indexName": "vector\_index"
// }
```
```javascript
// 5. Describe the index
res = await client.describeIndex({
collection\_name: "customized\_setup",
index\_name: "vector\_index"
})
console.log(JSON.stringify(res.index\_descriptions, null, 2))
// Output
//
// [
// {
// "params": [
// {
// "key": "index\_type",
// "value": "AUTOINDEX"
// },
// {
// "key": "metric\_type",
// "value": "COSINE"
// }
// ],
// "index\_name": "vector\_index",
// "indexID": "449007919953063141",
// "field\_name": "vector",
// "indexed\_rows": "0",
// "total\_rows": "0",
// "state": "Finished",
// "index\_state\_fail\_reason": "",
// "pending\_index\_rows": "0"
// }
// ]
//
```
You can check the index file created on a specific field, and collect the statistics on the number of rows indexed using this index file.
## Drop an Index
You can simply drop an index if it is no longer needed.

Before dropping an index, make sure it has been released first.

To drop an index, use [`drop\_index()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/drop\_index.md).

To drop an index, use [`dropIndex()`](https://milvus.io/api-reference/java/v2.4.x/v2/Management/dropIndex.md).

To drop an index, use [`dropIndex()`](https://milvus.io/api-reference/node/v2.4.x/Management/dropIndex.md).

[Python](#python) 
[Java](#java)
[Node.js](#javascript)

```python
# 6. Drop index
client.drop\_index(
collection\_name="customized\_setup",
index\_name="vector\_index"
)
```
```java
// 6. Drop index
DropIndexReq dropIndexReq = DropIndexReq.builder()
.collectionName("customized\_setup")
.indexName("vector\_index")
.build();
client.dropIndex(dropIndexReq);
```
```javascript
// 6. Drop the index
res = await client.dropIndex({
collection\_name: "customized\_setup",
index\_name: "vector\_index"
})
console.log(res.error\_code)
// Output
//
// Success
//
```