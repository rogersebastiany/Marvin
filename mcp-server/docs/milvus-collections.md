---
id: manage-collections.md
title: Manage Collections
---
# Manage Collections
This guide walks you through creating and managing collections using the SDK of your choice.
## Before you start
- You have installed [Milvus standalone](https://milvus.io/docs/install\_standalone-docker.md) or [Milvus cluster](https://milvus.io/docs/install\_cluster-milvusoperator.md).
- You have installed preferred SDKs. You can choose among various languages, including [Python](https://milvus.io/docs/install-pymilvus.md), [Java](https://milvus.io/docs/install-java.md), [Go](https://milvus.io/docs/install-go.md), and [Node.js](https://milvus.io/docs/install-node.md).
## Overview
In Milvus, you store your vector embeddings in collections. All vector embeddings within a collection share the same dimensionality and distance metric for measuring similarity.
Milvus collections support dynamic fields (i.e., fields not pre-defined in the schema) and automatic incrementation of primary keys.
To accommodate different preferences, Milvus offers two methods for creating a collection. One provides a quick setup, while the other allows for detailed customization of the collection schema and index parameters.
Additionally, you can view, load, release, and drop a collection when necessary.
## Create Collection
You can create a collection in either of the following manners:
- \_\_Quick setup\_\_
In this manner, you can create a collection by simply giving it a name and specifying the number of dimensions of the vector embeddings to be stored in this collection. For details, refer to [Quick setup](manage-collections.md).
- \_\_Customized setup\_\_
Instead of letting In Milvus decide almost everything for your collection, you can determine the \_\_schema\_\_ and \_\_index parameters\_\_ of the collection on your own. For details, refer to [Customized setup](manage-collections.md).
### Quick setup
Against the backdrop of the great leap in the AI industry, most developers just need a simple yet dynamic collection to start with. Milvus allows a quick setup of such a collection with just three arguments:
- Name of the collection to create,
- Dimension of the vector embeddings to insert, and
- Metric type used to measure similarities between vector embeddings.

For quick setup, use the [`create\_collection()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create\_collection.md) method of the [`MilvusClient`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Client/MilvusClient.md) class to create a collection with the specified name and dimension.

For quick setup, use the [`createCollection()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/createCollection.md) method of the [`MilvusClientV2`](https://milvus.io/api-reference/java/v2.4.x/v2/Client/MilvusClientV2.md) class to create a collection with the specified name and dimension.

For quick setup, use the [`createCollection()`](https://milvus.io/api-reference/node/v2.4.x/Collections/createCollection.md) method of the [`MilvusClient`](https://milvus.io/api-reference/node/v2.4.x/Client/MilvusClient.md) class to create a collection with the specified name and dimension.

For quick setup, use the [`CreateCollection()`](https://milvus.io/api-reference/go/v2.4.x/Collection/CreateCollection.md) on an instance of the `Client` interface using [`NewClient()`](https://milvus.io/api-reference/go/v2.4.x/Connections/NewClient.md) method, to create a collection with the specified name and dimension.

For quick setup, use the [`POST /v2/vectordb/collections/create`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Create.md) API endpoint to create a collection with the specified name and dimension.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
from pymilvus import MilvusClient, DataType
# 1. Set up a Milvus client
client = MilvusClient(
uri="http://localhost:19530"
)
# 2. Create a collection in quick setup mode
client.create\_collection(
collection\_name="quick\_setup",
dimension=5
)
res = client.get\_load\_state(
collection\_name="quick\_setup"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
```java
import io.milvus.v2.client.ConnectConfig;
import io.milvus.v2.client.MilvusClientV2;
import io.milvus.v2.service.collection.request.GetLoadStateReq;
import io.milvus.v2.service.collection.request.CreateCollectionReq;
String CLUSTER\_ENDPOINT = "http://localhost:19530";
// 1. Connect to Milvus server
ConnectConfig connectConfig = ConnectConfig.builder()
.uri(CLUSTER\_ENDPOINT)
.build();
MilvusClientV2 client = new MilvusClientV2(connectConfig);
// 2. Create a collection in quick setup mode
CreateCollectionReq quickSetupReq = CreateCollectionReq.builder()
.collectionName("quick\_setup")
.dimension(5)
.build();
client.createCollection(quickSetupReq);
// Thread.sleep(5000);
GetLoadStateReq quickSetupLoadStateReq = GetLoadStateReq.builder()
.collectionName("quick\_setup")
.build();
Boolean res = client.getLoadState(quickSetupLoadStateReq);
System.out.println(res);
// Output:
// true
```
```javascript
address = "http://localhost:19530"
// 1. Set up a Milvus Client
client = new MilvusClient({address});
// 2. Create a collection in quick setup mode
let res = await client.createCollection({
collection\_name: "quick\_setup",
dimension: 5,
});
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.getLoadState({
collection\_name: "quick\_setup"
})
console.log(res.state)
// Output
//
// LoadStateLoaded
//
```
```Go
import (
"context"
"fmt"
"log"
"time"
milvusClient "github.com/milvus-io/milvus-sdk-go/v2/client" // milvusClient is an alias for milvus client package
"github.com/milvus-io/milvus-sdk-go/v2/entity"
)
func main() {
ctx := context.Background()
ctx, cancel := context.WithTimeout(ctx, 2\*time.Second)
defer cancel()
// 1. Set up a Milvus client
client, err := milvusClient.NewClient(ctx, milvusClient.Config{
Address: "localhost:19530",
})
if err != nil {
log.Fatal("failed to connect to milvus:", err.Error())
}
defer client.Close()
// 2. Create a collection in quick setup mode
err = client.NewCollection(ctx, "quick\_setup", 5)
if err != nil {
log.Fatal("failed to create collection:", err.Error())
}
stateLoad, err := client.GetLoadState(context.Background(), "quick\_setup", []string{})
if err != nil {
log.Fatal("failed to get load state:", err.Error())
}
fmt.Println(stateLoad)
// Output
// 3
// LoadStateNotExist -> LoadState = 0
// LoadStateNotLoad -> LoadState = 1
// LoadStateLoading -> LoadState = 2
// LoadStateLoaded -> LoadState = 3
}
```
```shell
$ export MILVUS\_URI="localhost:19530"
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/create" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "quick\_setup",
"dimension": 5
}'
# Output
#
# {
# "code": 0,
# "data": {},
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/get\_load\_state" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "quick\_setup"
}'
# {
# "code": 0,
# "data": {
# "loadProgress": 100,
# "loadState": "LoadStateLoaded"
# }
# }
```
The collection generated in the above code contains only two fields: `id` (as the primary key) and `vector` (as the vector field), with `auto\_id` and `enable\_dynamic\_field` settings enabled by default.
- `auto\_id`
Enabling this setting ensures that the primary key increments automatically. There's no need for manual provision of primary keys during data insertion.
- `enable\_dynamic\_field`
When enabled, all fields, excluding `id` and `vector` in the data to be inserted, are treated as dynamic fields. These additional fields are saved as key-value pairs within a special field named `$meta`. This feature allows the inclusion of extra fields during data insertion.
The automatically indexed and loaded collection from the provided code is ready for immediate data insertions.
### Customized setup
Instead of letting Milvus decide almost everything for your collection, you can determine the \_\_schema\_\_ and \_\_index parameters\_\_ of the collection on your own.
#### Step 1: Set up schema
A schema defines the structure of a collection. Within the schema, you have the option to enable or disable `enable\_dynamic\_field`, add pre-defined fields, and set attributes for each field. For a detailed explanation of the concept and available data types, refer to [Schema Explained](schema.md).

To set up a schema, use [`create\_schema()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create\_schema.md) to create a schema object and [`add\_field()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/CollectionSchema/add\_field.md) to add fields to the schema.

To set up a schema, use [`createSchema()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/createSchema.md) to create a schema object and [`addField()`](https://milvus.io/api-reference/java/v2.4.x/v2/CollectionSchema/addField.md) to add fields to the schema.

To set up a schema, use [`createCollection()`](https://milvus.io/api-reference/node/v2.4.x/Collections/createCollection.md).

To set up a schema, use `entity.NewSchema()` to create a schema object and `schema.WithField()` to add fields to the schema.

To set up a schema, you need to define a JSON object that follows the schema format as displayed on the [`POST /v2/vectordb/collections/create`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Create.md) API endpoint reference page.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 3. Create a collection in customized setup mode
# 3.1. Create schema
schema = MilvusClient.create\_schema(
auto\_id=False,
enable\_dynamic\_field=True,
)
# 3.2. Add fields to schema
schema.add\_field(field\_name="my\_id", datatype=DataType.INT64, is\_primary=True)
schema.add\_field(field\_name="my\_vector", datatype=DataType.FLOAT\_VECTOR, dim=5)
```
```java
import io.milvus.v2.common.DataType;
import io.milvus.v2.service.collection.request.CreateCollectionReq;
// 3. Create a collection in customized setup mode
// 3.1 Create schema
CreateCollectionReq.CollectionSchema schema = client.createSchema();
// 3.2 Add fields to schema
schema.addField(AddFieldReq.builder()
.fieldName("my\_id")
.dataType(DataType.Int64)
.isPrimaryKey(true)
.autoID(false)
.build());
schema.addField(AddFieldReq.builder()
.fieldName("my\_vector")
.dataType(DataType.FloatVector)
.dimension(5)
.build());
```
```javascript
// 3. Create a collection in customized setup mode
// 3.1 Define fields
const fields = [
{
name: "my\_id",
data\_type: DataType.Int64,
is\_primary\_key: true,
auto\_id: false
},
{
name: "my\_vector",
data\_type: DataType.FloatVector,
dim: 5
},
]
```
```go
// 3. Create a collection in customized setup mode
// 3.1 Create schema
schema := entity.NewSchema()
// 3.2. Add fields to schema
schema.WithField(
entity.NewField().
WithName("my\_id").
WithDataType(entity.FieldTypeInt64).
WithIsPrimaryKey(false).
WithIsAutoID(true)).
WithField(
entity.NewField().
WithName("my\_vector").
WithDataType(entity.FieldTypeFloatVector).
WithDim(5))
```
```shell
export fields='[{ \
"fieldName": "my\_id", \
"dataType": "Int64", \
"isPrimary": true \
}, \
{ \
"fieldName": "my\_vector", \
"dataType": "FloatVector", \
"elementTypeParams": { \
"dim": 5 \
} \
}]'
```

| Parameter | Description |
| --- | --- |
| `auto_id` | Determines if the primary field automatically increments. Setting this to **True** makes the primary field automatically increment. In this case, the primary field should not be included in the data to insert to avoid errors. The auto-generated IDs have a fixed length and cannot be altered. |
| `enable_dynamic_field` | Determines if Milvus saves the values of undefined fields in a dynamic field if the data being inserted into the target collection includes fields that are not defined in the collection's schema. When you set this to **True**, Milvus will create a field called **$meta** to store any undefined fields and their values from the data that is inserted. |
| `field_name` | The name of the field. |
| `datatype` | The data type of the field. For a list of available data types, refer to [DataType](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/DataType.md). |
| `is_primary` | Whether the current field is the primary field in a collection. Each collection has only one primary field. A primary field should be of either the **DataType.INT64** type or the **DataType.VARCHAR** type. |
| `dim` | The dimension of the vector embeddings. This is mandatory for a field of the **DataType.FLOAT\_VECTOR**, **DataType.BINARY\_VECTOR**, **DataType.FLOAT16\_VECTOR**, or **DataType.BFLOAT16\_VECTOR** type. If you use **DataType.SPARSE\_FLOAT\_VECTOR**, omit this parameter. |

| Parameter | Description |
| --- | --- |
| `fieldName` | The name of the field. |
| `dataType` | The data type of the field. For a list of available data types, refer to [DataType](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/DataType.md). |
| `isPrimaryKey` | Whether the current field is the primary field in a collection. Each collection has only one primary field. A primary field should be of either the **DataType.Int64** type or the **DataType.VarChar** type. |
| `autoID` | Whether allows the primary field to automatically increment. Setting this to **true** makes the primary field automatically increment. In this case, the primary field should not be included in the data to insert to avoid errors. |
| `dimension` | The dimension of the vector embeddings. This is mandatory for a field of the **DataType.FloatVector**, **DataType.BinaryVector**, **DataType.Float16Vector**, or **DataType.BFloat16Vector** type. |

| Parameter | Description |
| --- | --- |
| `name` | The name of the field. |
| `data_type` | The data type of the field. For an enumeration of all available data types, refer to [DataType](https://milvus.io/api-reference/node/v2.4.x/Collections/DataType.md). |
| `is_primary_key` | Whether the current field is the primary field in a collection. Each collection has only one primary field. A primary field should be of either the **DataType.INT64** type or the **DataType.VARCHAR** type. |
| `auto_id` | Whether the primary field automatically increments upon data insertions into this collection. The value defaults to **False**. Setting this to **True** makes the primary field automatically increment. Skip this parameter if you need to set up a collection with a customized schema. |
| `dim` | The dimensionality of the collection field that holds vector embeddings. The value should be an integer greater than 1 and is usually determined by the model you use to generate vector embeddings. |

| Parameter | Description |
| --- | --- |
| `WithName()` | The name of the field. |
| `WithDataType()` | The data type of the field. |
| `WithIsPrimaryKey()` | Whether the current field is the primary field in a collection. Each collection has only one primary field. A primary field should be of either the **entity.FieldTypeInt64** type or the **entity.FieldTypeVarChar** type. |
| `WithIsAutoID()` | Whether the primary field automatically increments upon data insertions into this collection. The value defaults to **false**. Setting this to **true** makes the primary field automatically increment. Skip this parameter if you need to set up a collection with a customized schema. |
| `WithDim()` | The dimensionality of the collection field that holds vector embeddings. The value should be an integer greater than 1 and is usually determined by the model you use to generate vector embeddings. |

| Parameter | Description |
| --- | --- |
| `fieldName` | The name of the field to create in the target collection. |
| `dataType` | The data type of the field values. |
| `isPrimary` | Whether the current field is the primary field. Setting this to `True` makes the current field the primary field. |
| `elementTypeParams` | Extra field parameters. |
| `dim` | An optional parameter for FloatVector or BinaryVector fields that determines the vector dimension. |

#### Step 2: Set up index parameters
Index parameters dictate how Milvus organizes your data within a collection. You can tailor the indexing process for specific fields by adjusting their `metric\_type` and `index\_type`. For the vector field, you have the flexibility to select `COSINE`, `L2`, `IP`, `HAMMING`, or `JACCARD` as the `metric\_type`, depending on the type of vectors you are working with. For more information, refer to [Similarity Metrics](metric.md).

To set up index parameters, use [`prepare\_index\_params()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/prepare\_index\_params.md) to prepare index parameters and [`add\_index()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/add\_index.md) to add the index.

To set up index parameters, use [IndexParam](https://milvus.io/api-reference/java/v2.4.x/v2/Management/IndexParam.md).

To set up index parameters, use [`createIndex()`](https://milvus.io/api-reference/node/v2.4.x/Management/createIndex.md).

To set up index parameters, use [`CreateIndex()`](https://milvus.io/api-reference/go/v2.4.x/Index/CreateIndex.md).

To set up index parameters, you need to define a JSON object that follows the index parameters format as displayed on the [`POST /v2/vectordb/collections/create`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Create.md) API endpoint reference page.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 3.3. Prepare index parameters
index\_params = client.prepare\_index\_params()
# 3.4. Add indexes
index\_params.add\_index(
field\_name="my\_id",
index\_type="STL\_SORT"
)
index\_params.add\_index(
field\_name="my\_vector",
index\_type="IVF\_FLAT",
metric\_type="IP",
params={ "nlist": 128 }
)
```
```java
import io.milvus.v2.common.IndexParam;
// 3.3 Prepare index parameters
IndexParam indexParamForIdField = IndexParam.builder()
.fieldName("my\_id")
.indexType(IndexParam.IndexType.STL\_SORT)
.build();
IndexParam indexParamForVectorField = IndexParam.builder()
.fieldName("my\_vector")
.indexType(IndexParam.IndexType.IVF\_FLAT)
.metricType(IndexParam.MetricType.L2)
.extraParams(Map.of("nlist", 1024))
.build();
List indexParams = new ArrayList<>();
indexParams.add(indexParamForIdField);
indexParams.add(indexParamForVectorField);
```
```javascript
// 3.2 Prepare index parameters
const index\_params = [{
field\_name: "my\_id",
index\_type: "STL\_SORT"
},{
field\_name: "my\_vector",
index\_type: "IVF\_FLAT",
metric\_type: "IP",
params: { nlist: 1024}
}]
```
```go
// 3.3 Prepare index parameters
idxID := entity.NewScalarIndexWithType(entity.Sorted)
idxVector, err := entity.NewIndexIvfFlat(entity.IP, 1024)
if err != nil {
log.Fatal("failed to new index:", err.Error())
}
```
```shell
export indexParams='[{ \
"fieldName": "my\_id", \
"indexName": "my\_id", \
"params": { \
"index\_type": "SLT\_SORT" \
} \
}, { \
"fieldName": "my\_vector", \
"metricType": "COSINE", \
"indexName": "my\_vector", \
"params": { \
"index\_type": "IVF\_FLAT", \
"nlist": 1024 \
} \
}]'
```

| Parameter | Description |
| --- | --- |
| `field_name` | The name of the target file to apply this object applies. |
| `index_type` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `metric_type` | The algorithm that is used to measure similarity between vectors. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. This is available only when the specified field is a vector field. For more information, refer to [Indexes supported in Milvus](https://milvus.io/docs/index.md#Indexes-supported-in-Milvus). |
| `params` | The fine-tuning parameters for the specified index type. For details on possible keys and value ranges, refer to [In-memory Index](https://milvus.io/docs/index.md). |

| Parameter | Description |
| --- | --- |
| `fieldName` | The name of the target field to apply this IndexParam object applies. |
| `indexType` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `metricType` | The distance metric to use for the index. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. |
| `extraParams` | Extra index parameters. For details, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |

| Parameter | Description |
| --- | --- |
| `field_name` | The name of the target field on which an index is to be created. |
| `index_type` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `metric_type` | The algorithm that is used to measure similarity between vectors. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. This is available only when the specified field is a vector field. For more information, refer to [Indexes supported in Milvus](https://milvus.io/docs/index.md#Indexes-supported-in-Milvus). |
| `params` | The fine-tuning parameters for the specified index type. For details on possible keys and value ranges, refer to [In-memory Index](https://milvus.io/docs/index.md). |

| Parameter | Description |
| --- | --- |
| `index_type` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `metric_type` | The algorithm that is used to measure similarity between vectors. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. This is available only when the specified field is a vector field. For more information, refer to [Indexes supported in Milvus](https://milvus.io/docs/index.md#Indexes-supported-in-Milvus). |
| `nlist` | Number of cluster units. Cluster units are used in IVF (Inverted File) based indexes in Milvus. For IVF\_FLAT, the index divides vector data into `nlist` cluster units, and then compares distances between the target input vector and the center of each cluster1. Must be between 1 and 65536. |

| Parameter | Description |
| --- | --- |
| `fieldName` | The name of the target field on which an index is to be created. |
| `indexName` | The name of the index to create. The value defaults to the target field name. |
| `metricType` | The algorithm that is used to measure similarity between vectors. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. This is available only when the specified field is a vector field. For more information, refer to [Indexes supported in Milvus](https://milvus.io/docs/index.md#Indexes-supported-in-Milvus). |
| `params` | The index type and related settings. For details, refer to [In-memory Index](https://milvus.io/docs/index.md). |
| `params.index_type` | The type of the index to create. |
| `params.nlist` | The number of cluster units. This applies to IVF-related index types. |

The code snippet above demonstrates how to set up index parameters for the vector field and a scalar field, respectively. For the vector field, set both the metric type and the index type. For a scalar field, set only the index type. It is recommended to create an index for the vector field and any scalar fields that are frequently used for filtering.
#### Step 3: Create the collection
You have the option to create a collection and an index file separately or to create a collection with the index loaded simultaneously upon creation.

Use [create\_collection()](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create\_collection.md) to create a collection with the specified schema and index parameters and [get\_load\_state()](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/get\_load\_state.md) to check the load state of the collection.

Use [createCollection()](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/createCollection.md) to create a collection with the specified schema and index parameters and [getLoadState()](https://milvus.io/api-reference/java/v2.4.x/v2/Management/getLoadState.md) to check the load state of the collection.

Use [createCollection()](https://milvus.io/api-reference/node/v2.4.x/Collections/createCollection.md) to create a collection with the specified schema and index parameters and [getLoadState()](https://milvus.io/api-reference/node/v2.4.x/Management/getLoadState.md) to check the load state of the collection.

- \_\_Create a collection with the index loaded simultaneously upon creation.\_\_

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[cURL](#shell)

```python
# 3.5. Create a collection with the index loaded simultaneously
client.create\_collection(
collection\_name="customized\_setup\_1",
schema=schema,
index\_params=index\_params
)
time.sleep(5)
res = client.get\_load\_state(
collection\_name="customized\_setup\_1"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
```java
import io.milvus.v2.service.collection.request.CreateCollectionReq;
import io.milvus.v2.service.collection.request.GetLoadStateReq;
// 3.4 Create a collection with schema and index parameters
CreateCollectionReq customizedSetupReq1 = CreateCollectionReq.builder()
.collectionName("customized\_setup\_1")
.collectionSchema(schema)
.indexParams(indexParams)
.build();
client.createCollection(customizedSetupReq1);
// Thread.sleep(5000);
// 3.5 Get load state of the collection
GetLoadStateReq customSetupLoadStateReq1 = GetLoadStateReq.builder()
.collectionName("customized\_setup\_1")
.build();
res = client.getLoadState(customSetupLoadStateReq1);
System.out.println(res);
// Output:
// true
```
```javascript
// 3.3 Create a collection with fields and index parameters
res = await client.createCollection({
collection\_name: "customized\_setup\_1",
fields: fields,
index\_params: index\_params,
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.getLoadState({
collection\_name: "customized\_setup\_1"
})
console.log(res.state)
// Output
//
// LoadStateLoaded
//
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/create" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_1",
"schema": {
"autoId": false,
"enabledDynamicField": false,
"fields": [
{
"fieldName": "my\_id",
"dataType": "Int64",
"isPrimary": true
},
{
"fieldName": "my\_vector",
"dataType": "FloatVector",
"elementTypeParams": {
"dim": "5"
}
}
]
},
"indexParams": [
{
"fieldName": "my\_vector",
"metricType": "COSINE",
"indexName": "my\_vector",
"params": {
"index\_type": "IVF\_FLAT",
"nlist": "1024"
}
},
{
"fieldName": "my\_id",
"indexName": "my\_id",
"params": {
"index\_type": "STL\_SORT"
}
}
]
}'
# Output
#
# {
# "code": 0,
# "data": {},
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/get\_load\_state" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_1"
}'
# {
# "code": 0,
# "data": {
# "loadProgress": 100,
# "loadState": "LoadStateLoaded"
# }
# }
```
The collection created above is loaded automatically. To learn more about loading and releasing a collection, refer to [Load & Release Collection](manage-collections.md#Load--Release-Collection).
- \_\_Create a collection and an index file separately.\_\_

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 3.6. Create a collection and index it separately
client.create\_collection(
collection\_name="customized\_setup\_2",
schema=schema,
)
res = client.get\_load\_state(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
```java
// 3.6 Create a collection and index it separately
CreateCollectionReq customizedSetupReq2 = CreateCollectionReq.builder()
.collectionName("customized\_setup\_2")
.collectionSchema(schema)
.build();
client.createCollection(customizedSetupReq2);
```
```javascript
// 3.4 Create a collection and index it seperately
res = await client.createCollection({
collection\_name: "customized\_setup\_2",
fields: fields,
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.getLoadState({
collection\_name: "customized\_setup\_2"
})
console.log(res.state)
// Output
//
// LoadStateNotLoad
//
```
```go
// 3.4 Create a collection and index it seperately
schema.CollectionName = "customized\_setup\_2"
client.CreateCollection(ctx, schema, entity.DefaultShardNumber)
stateLoad, err := client.GetLoadState(context.Background(), "customized\_setup\_2", []string{})
if err != nil {
log.Fatal("failed to get load state:", err.Error())
}
fmt.Println(stateLoad)
// Output
// 1
// LoadStateNotExist -> LoadState = 0
// LoadStateNotLoad -> LoadState = 1
// LoadStateLoading -> LoadState = 2
// LoadStateLoaded -> LoadState = 3
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/create" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2",
"schema": {
"autoId": false,
"enabledDynamicField": false,
"fields": [
{
"fieldName": "my\_id",
"dataType": "Int64",
"isPrimary": true
},
{
"fieldName": "my\_vector",
"dataType": "FloatVector",
"elementTypeParams": {
"dim": "5"
}
}
]
}
}'
# Output
#
# {
# "code": 0,
# "data": {},
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/get\_load\_state" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": {
# "loadState": "LoadStateNotLoaded"
# }
# }
```
The collection created above is not loaded automatically. You can create an index for the collection as follows. Creating an index for the collection in a separate manner does not automatically load the collection. For details, refer to [Load & Release Collection](manage-collections.md#Load--Release-Collection).

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of the collection. |
| `schema` | The schema of this collection. Setting this to **None** indicates this collection will be created with default settings. To set up a collection with a customized schema, you need to create a **CollectionSchema** object and reference it here. In this case, Milvus ignores all other schema-related settings carried in the request. |
| `index_params` | The parameters for building the index on the vector field in this collection. To set up a collection with a customized schema and automatically load the collection to memory, you need to create an IndexParams object and reference it here. You should at least add an index for the vector field in this collection. You can also skip this parameter if you prefer to set up the index parameters later on. |

| Parameter | Description |
| --- | --- |
| `collectionName` | The name of the collection. |
| `collectionSchema` | The schema of this collection. Leaving it empty indicates this collection will be created with default settings. To set up a collection with a customized schema, you need to create a **CollectionSchema** object and reference it here. |
| `indexParams` | The parameters for building the index on the vector field in this collection. To set up a collection with a customized schema and automatically load the collection to memory, create an [IndexParams](https://milvus.io/api-reference/java/v2.4.x/v2/Management/IndexParam.md) object with a list of IndexParam objects and reference it here. |

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of the collection. |
| `fields` | The fields in the collection. |
| `index_params` | The index parameters for the collection to create. |

| Parameter | Description |
| --- | --- |
| `schema.CollectionName` | The name of the collection. |
| `schema` | The schema of this collection. |
| `index_params` | The index parameters for the collection to create. |

| Parameter | Description |
| --- | --- |
| `collectionName` | The name of the collection. |
| `schema` | The schema is responsible for organizing data in the target collection. A valid schema should have multiple fields, which must include a primary key, a vector field, and several scalar fields. |
| `schema.autoID` | Whether allows the primary field to automatically increment. Setting this to True makes the primary field automatically increment. In this case, the primary field should not be included in the data to insert to avoid errors. Set this parameter in the field with is\_primary set to True. |
| `schema.enableDynamicField` | Whether allows to use the reserved $meta field to hold non-schema-defined fields in key-value pairs. |
| `fields` | A list of field objects. |
| `fields.fieldName` | The name of the field to create in the target collection. |
| `fields.dataType` | The data type of the field values. |
| `fields.isPrimary` | Whether the current field is the primary field. Setting this to True makes the current field the primary field. |
| `fields.elementTypeParams` | Extra field parameters. |
| `fields.elementTypeParams.dim` | An optional parameter for FloatVector or BinaryVector fields that determines the vector dimension. |

The collection created above is not loaded automatically. You can create an index for the collection as follows. Creating an index for the collection in a separate manner does not automatically load the collection. For details, refer to [Load & Release Collection](manage-collections.md).

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 3.6 Create index
client.create\_index(
collection\_name="customized\_setup\_2",
index\_params=index\_params
)
res = client.get\_load\_state(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
```java
CreateIndexReq createIndexReq = CreateIndexReq.builder()
.collectionName("customized\_setup\_2")
.indexParams(indexParams)
.build();
client.createIndex(createIndexReq);
// Thread.sleep(1000);
// 3.7 Get load state of the collection
GetLoadStateReq customSetupLoadStateReq2 = GetLoadStateReq.builder()
.collectionName("customized\_setup\_2")
.build();
res = client.getLoadState(customSetupLoadStateReq2);
System.out.println(res);
// Output:
// false
```
```javascript
// 3.5 Create index
res = await client.createIndex({
collection\_name: "customized\_setup\_2",
field\_name: "my\_vector",
index\_type: "IVF\_FLAT",
metric\_type: "IP",
params: { nlist: 1024}
})
res = await client.getLoadState({
collection\_name: "customized\_setup\_2"
})
console.log(res.state)
// Output
//
// LoadStateNotLoad
//
```
```go
// 3.5 Create index
client.CreateIndex(ctx, "customized\_setup\_2", "my\_id", idxID, false)
client.CreateIndex(ctx, "customized\_setup\_2", "my\_vector", idxVector, false)
stateLoad, err = client.GetLoadState(context.Background(), "customized\_setup\_2", []string{})
if err != nil {
log.Fatal("failed to get load state:", err.Error())
}
fmt.Println(stateLoad)
// Output
// 1
// LoadStateNotExist -> LoadState = 0
// LoadStateNotLoad -> LoadState = 1
// LoadStateLoading -> LoadState = 2
// LoadStateLoaded -> LoadState = 3
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/indexes/create" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2",
"indexParams": [
{
"metricType": "L2",
"fieldName": "my\_vector",
"indexName": "my\_vector",
"indexConfig": {
"index\_type": "IVF\_FLAT",
"nlist": "1024"
}
}
]
}'
# Output
#
# {
# "code": 0,
# "data": {},
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/get\_load\_state" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": {
# "loadState": "LoadStateNotLoaded"
# }
# }
```

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of the collection. |
| `index_params` | An **IndexParams** object containing a list of **IndexParam** objects. |

| Parameter | Description |
| --- | --- |
| `collectionName` | The name of the collection. |
| `indexParams` | A list of **IndexParam** objects. |

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of the collection. |
| `field_name` | The name of the field in which to create an index. |
| `index_type` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `metric_type` | The algorithm that is used to measure similarity between vectors. Possible values are **IP**, **L2**, **COSINE**, **JACCARD**, **HAMMING**. This is available only when the specified field is a vector field. For more information, refer to [Indexes supported in Milvus](https://milvus.io/docs/index.md#Indexes-supported-in-Milvus). |
| `params` | The fine-tuning parameters for the specified index type. For details on possible keys and value ranges, refer to [In-memory Index](https://milvus.io/docs/index.md). |

| Parameter | Description |
| --- | --- |
| `collName` | The name of the collection. |
| `fieldName` | The name of the field in which to create an index. |
| `idx` | The name of the algorithm used to arrange data in the specific field. For applicable algorithms, refer to [In-memory Index](https://milvus.io/docs/index.md) and [On-disk Index](https://milvus.io/docs/disk_index.md). |
| `async` | Whether this operation is asynchronous. |
| `opts` | The fine-tuning parameters for the specified index type. You can include multiple `entity.IndexOption` in this request. For details on possible keys and value ranges, refer to [In-memory Index](https://milvus.io/docs/index.md). |

| Parameter | Description |
| --- | --- |
| `collectionName` | The name of the collection. |
| `indexParams` | The index parameters for the collection to create. |
| `indexParams.metricType` | The similarity metric type used to build the index. The value defaults to COSINE. |
| `indexParams.fieldName` | The name of the target field on which an index is to be created. |
| `indexParams.indexName` | The name of the index to create, the value defaults to the target field name. |
| `indexParams.indexConfig.index_type` | The type of the index to create. |
 `indexParams.indexConfig.nlist` | The number of cluster units. This applies to IVF-related index types. |

## View Collections

To check the details of an existing collection, use [describe\_collection()](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/describe\_collection.md).

To check the details of an existing collection, use [describeCollection()](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/describeCollection.md).

To check the details of an existing collection, use [describeCollection()](https://milvus.io/api-reference/node/v2.4.x/Collections/describeCollection.md).

To check the details of an existing collection, use [DescribeCollection()](https://milvus.io/api-reference/go/v2.4.x/Collection/DescribeCollection.md).

To view the definition of a collection, you can use the [`POST /v2/vectordb/collections/describe`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Describe.md) and the [`POST /v2/vectordb/collections/list`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/List.md) API endpoints.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 5. View Collections
res = client.describe\_collection(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "collection\_name": "customized\_setup\_2",
# "auto\_id": false,
# "num\_shards": 1,
# "description": "",
# "fields": [
# {
# "field\_id": 100,
# "name": "my\_id",
# "description": "",
# "type": 5,
# "params": {},
# "element\_type": 0,
# "is\_primary": true
# },
# {
# "field\_id": 101,
# "name": "my\_vector",
# "description": "",
# "type": 101,
# "params": {
# "dim": 5
# },
# "element\_type": 0
# }
# ],
# "aliases": [],
# "collection\_id": 448143479230158446,
# "consistency\_level": 2,
# "properties": {},
# "num\_partitions": 1,
# "enable\_dynamic\_field": true
# }
```
```java
import io.milvus.v2.service.collection.request.DescribeCollectionReq;
import io.milvus.v2.service.collection.response.DescribeCollectionResp;
// 4. View collections
DescribeCollectionReq describeCollectionReq = DescribeCollectionReq.builder()
.collectionName("customized\_setup\_2")
.build();
DescribeCollectionResp describeCollectionRes = client.describeCollection(describeCollectionReq);
System.out.println(JSONObject.toJSON(describeCollectionRes));
// Output:
// {
// "createTime": 449005822816026627,
// "collectionSchema": {"fieldSchemaList": [
// {
// "autoID": false,
// "dataType": "Int64",
// "name": "my\_id",
// "description": "",
// "isPrimaryKey": true,
// "maxLength": 65535,
// "isPartitionKey": false
// },
// {
// "autoID": false,
// "dataType": "FloatVector",
// "name": "my\_vector",
// "description": "",
// "isPrimaryKey": false,
// "dimension": 5,
// "maxLength": 65535,
// "isPartitionKey": false
// }
// ]},
// "vectorFieldName": ["my\_vector"],
// "autoID": false,
// "fieldNames": [
// "my\_id",
// "my\_vector"
// ],
// "description": "",
// "numOfPartitions": 1,
// "primaryFieldName": "my\_id",
// "enableDynamicField": true,
// "collectionName": "customized\_setup\_2"
// }
```
```javascript
// 5. View Collections
res = await client.describeCollection({
collection\_name: "customized\_setup\_2"
})
console.log(res)
// Output
//
// {
// virtual\_channel\_names: [ 'by-dev-rootcoord-dml\_13\_449007919953017716v0' ],
// physical\_channel\_names: [ 'by-dev-rootcoord-dml\_13' ],
// aliases: [],
// start\_positions: [],
// properties: [],
// status: {
// extra\_info: {},
// error\_code: 'Success',
// reason: '',
// code: 0,
// retriable: false,
// detail: ''
// },
// schema: {
// fields: [ [Object], [Object] ],
// properties: [],
// name: 'customized\_setup\_2',
// description: '',
// autoID: false,
// enable\_dynamic\_field: false
// },
// collectionID: '449007919953017716',
// created\_timestamp: '449024569603784707',
// created\_utc\_timestamp: '1712892797866',
// shards\_num: 1,
// consistency\_level: 'Bounded',
// collection\_name: 'customized\_setup\_2',
// db\_name: 'default',
// num\_partitions: '1'
// }
//
```
```Go
// 4. View collections
res, err := client.DescribeCollection(ctx, "customized\_setup\_2")
if err != nil {
log.Fatal("failed to describe collection:", err.Error())
}
fmt.Printf("ConsistencyLevel: %v\nID: %v\nLoaded: %v\nName: %v\nPhysicalChannels: %v\nProperties: %v\nSchemaField1: %v\nSchemaField2: %v\nShardNum: %v\nVirtualChannels: %v\nSchemaAutoID: %v\nSchemaCollectionName: %v\nSchemaDescription: %v",
res.ConsistencyLevel, res.ID, res.Loaded, res.Name, res.PhysicalChannels,
res.Properties, res.Schema.Fields[0], res.Schema.Fields[1], res.ShardNum,
res.VirtualChannels, res.Schema.AutoID, res.Schema.CollectionName, res.Schema.Description)
// Output:
// ConsistencyLevel: 2
// ID: 453858520413977280
// Loaded: false
// Name: customized\_setup\_2
// PhysicalChannels: [by-dev-rootcoord-dml\_14]
// Properties: map[]
// SchemaField1: &{100 my\_id true false int64 map[] map[] false false false undefined}
// SchemaField2: &{101 my\_vector false false []float32 map[dim:5] map[] false false false undefined}
// ShardNum: 1
// VirtualChannels: [by-dev-rootcoord-dml\_14\_453858520413977280v0]
// SchemaAutoID: false
// SchemaCollectionName: customized\_setup\_2
// SchemaDescription: 2024/11/12 14:06:53 my\_rag\_collection
```
```shell
curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/describe" \
-H "Content-Type: application/json" \
-d '{
"dbName": "default",
"collectionName": "test\_collection"
}'
# {
# "code": 0,
# "data": {
# "aliases": [],
# "autoId": false,
# "collectionID": 448707763883002014,
# "collectionName": "test\_collection",
# "consistencyLevel": "Bounded",
# "description": "",
# "enableDynamicField": true,
# "fields": [
# {
# "autoId": false,
# "description": "",
# "id": 100,
# "name": "id",
# "partitionKey": false,
# "primaryKey": true,
# "type": "Int64"
# },
# {
# "autoId": false,
# "description": "",
# "id": 101,
# "name": "vector",
# "params": [
# {
# "key": "dim",
# "value": "5"
# }
# ],
# "partitionKey": false,
# "primaryKey": false,
# "type": "FloatVector"
# }
# ],
# "indexes": [
# {
# "fieldName": "vector",
# "indexName": "vector",
# "metricType": "COSINE"
# }
# ],
# "load": "LoadStateLoaded",
# "partitionsNum": 1,
# "properties": [],
# "shardsNum": 1
# }
# }
```
To list all existing collections, you can do as follows:

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 6. List all collection names
res = client.list\_collections()
print(res)
# Output
#
# [
# "customized\_setup\_2",
# "quick\_setup",
# "customized\_setup\_1"
# ]
```
```java
import io.milvus.v2.service.collection.response.ListCollectionsResp;
// 5. List all collection names
ListCollectionsResp listCollectionsRes = client.listCollections();
System.out.println(listCollectionsRes.getCollectionNames());
// Output:
// [
// "customized\_setup\_2",
// "quick\_setup",
// "customized\_setup\_1"
// ]
```
```javascript
// 5. List all collection names
ListCollectionsResp listCollectionsRes = client.listCollections();
System.out.println(listCollectionsRes.getCollectionNames());
// Output:
// [
// "customized\_setup\_1",
// "quick\_setup",
// "customized\_setup\_2"
// ]
```
```Go
// 5. List all collection names
collections, err := client.ListCollections(ctx)
if err != nil {
log.Fatal("failed to list collection:", err.Error())
}
for \_, c := range collections {
log.Println(c.Name)
}
// Output:
// customized\_setup\_2
// quick\_setup
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/list" \
-H "Content-Type: application/json" \
-d '{
"dbName": "default"
}'
# {
# "code": 0,
# "data": [
# "quick\_setup",
# "customized\_setup\_1",
# "customized\_setup\_2"
# ]
# }
```
## Load & Release Collection
During the loading process of a collection, Milvus loads the collection's index file into memory. Conversely, when releasing a collection, Milvus unloads the index file from memory. Before conducting searches in a collection, ensure that the collection is loaded.
### Load a collection

To load a collection, use the [`load\_collection()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/load\_collection.md) method, specifying the collection name. You can also set `replica\_number` to determine how many in-memory replicas of data segments to create on query nodes when the collection is loaded.
- Milvus Standalone: The maximum allowed value for `replica\_number` is 1.
- Milvus Cluster: The maximum value should not exceed the `queryNode.replicas` set in your Milvus configurations. For additional details, refer to [Query Node-related Configurations](https://milvus.io/docs/configure\_querynode.md#Query-Node-related-Configurations).

To load a collection, use the [`loadCollection()`](https://milvus.io/api-reference/java/v2.4.x/v2/Management/loadCollection.md) method, specifying the collection name.

To load a collection, use the [`loadCollection()`](https://milvus.io/api-reference/node/v2.4.x/Management/loadCollection.md) method, specifying the collection name.

To load a collection, use the [`LoadCollection()`](https://milvus.io/api-reference/go/v2.4.x/Collection/LoadCollection.md) method, specifying the collection name.

To load a collection, you can use the [`POST /v2/vectordb/collections/load`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Load.md) and the [`POST /v2/vectordb/collections/get\_load\_state`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/GetLoadState.md) API endpoints.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 7. Load the collection
client.load\_collection(
collection\_name="customized\_setup\_2",
replica\_number=1 # Number of replicas to create on query nodes. Max value is 1 for Milvus Standalone, and no greater than `queryNode.replicas` for Milvus Cluster.
)
res = client.get\_load\_state(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
```java
import io.milvus.v2.service.collection.request.LoadCollectionReq;
// 6. Load the collection
LoadCollectionReq loadCollectionReq = LoadCollectionReq.builder()
.collectionName("customized\_setup\_2")
.build();
client.loadCollection(loadCollectionReq);
// Thread.sleep(5000);
// 7. Get load state of the collection
GetLoadStateReq loadStateReq = GetLoadStateReq.builder()
.collectionName("customized\_setup\_2")
.build();
res = client.getLoadState(loadStateReq);
System.out.println(res);
// Output:
// true
```
```javascript
// 7. Load the collection
res = await client.loadCollection({
collection\_name: "customized\_setup\_2"
})
console.log(res.error\_code)
// Output
//
// Success
//
await sleep(3000)
res = await client.getLoadState({
collection\_name: "customized\_setup\_2"
})
console.log(res.state)
// Output
//
// LoadStateLoaded
//
```
```go
// 6. Load the collection
err = client.LoadCollection(ctx, "customized\_setup\_2", false)
if err != nil {
log.Fatal("failed to laod collection:", err.Error())
}
// 7. Get load state of the collection
stateLoad, err := client.GetLoadState(context.Background(), "customized\_setup\_2", []string{})
if err != nil {
log.Fatal("failed to get load state:", err.Error())
}
fmt.Println(stateLoad)
// Output:
// 3
// LoadStateNotExist -> LoadState = 0
// LoadStateNotLoad -> LoadState = 1
// LoadStateLoading -> LoadState = 2
// LoadStateLoaded -> LoadState = 3
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/load" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# Output
#
# {
# "code": 0,
# "data": {},
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/get\_load\_state" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": {
# "loadProgress": 100,
# "loadState": "LoadStateLoaded"
# }
# }
```
### Load a collection partially (Public Preview)

This feature is currently in public preview. The API and functionality may change in the future.

Upon receiving your load request, Milvus loads all vector field indexes and all scalar field data into memory. If some fields are not to be involved in searches and queries, you can exclude them from loading to reduce memory usage, improving search performance.

```python
# 7. Load the collection
client.load\_collection(
collection\_name="customized\_setup\_2",
load\_fields=["my\_id", "my\_vector"], # Load only the specified fields
skip\_load\_dynamic\_field=True # Skip loading the dynamic field
)
res = client.get\_load\_state(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
Note that only the fields listed in `load\_fields` can be used as filtering conditions and output fields in searches and queries. You should always include the primary key in the list. The field names excluded from loading will not be available for filtering or output.
You can use `skip\_load\_dynamic\_field=True` to skip loading the dynamic field. Milvus treats the dynamic field as a single field, so all the keys in the dynamic field will be included or excluded together.

### Release a collection

To release a collection, use the [`release\_collection()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Management/release\_collection.md) method, specifying the collection name.

To release a collection, use the [`releaseCollection()`](https://milvus.io/api-reference/java/v2.4.x/v2/Management/releaseCollection.md) method, specifying the collection name.

To release a collection, use the [`releaseCollection()`](https://milvus.io/api-reference/node/v2.4.x/Management/releaseCollection.md) method, specifying the collection name.

To release a collection, use the [`ReleaseCollection()`](https://milvus.io/api-reference/go/v2.4.x/Collection/ReleaseCollection.md) method, specifying the collection name.

To release a collection, you can use the [`POST /v2/vectordb/collections/release`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Release.md) and the [`POST /v2/vectordb/collections/get\_load\_state`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/GetLoadState.md) API endpoints.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 8. Release the collection
client.release\_collection(
collection\_name="customized\_setup\_2"
)
res = client.get\_load\_state(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "state": ""
# }
```
```java
import io.milvus.v2.service.collection.request.ReleaseCollectionReq;
// 8. Release the collection
ReleaseCollectionReq releaseCollectionReq = ReleaseCollectionReq.builder()
.collectionName("customized\_setup\_2")
.build();
client.releaseCollection(releaseCollectionReq);
// Thread.sleep(1000);
res = client.getLoadState(loadStateReq);
System.out.println(res);
// Output:
// false
```
```javascript
// 8. Release the collection
res = await client.releaseCollection({
collection\_name: "customized\_setup\_2"
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.getLoadState({
collection\_name: "customized\_setup\_2"
})
console.log(res.state)
// Output
//
// LoadStateNotLoad
//
```
```go
// 8. Release the collection
errRelease := client.ReleaseCollection(context.Background(), "customized\_setup\_2")
if errRelease != nil {
log.Fatal("failed to release collection:", errRelease.Error())
}
fmt.Println(errRelease)
stateLoad, err = client.GetLoadState(context.Background(), "customized\_setup\_2", []string{})
if err != nil {
log.Fatal("failed to get load state:", err.Error())
}
fmt.Println(stateLoad)
// Output:
// 1
// meaning not loaded
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/release" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# Output
#
# {
# "code": 0,
# "data": {},
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/get\_load\_state" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": {
# "loadState": "LoadStateNotLoad"
# }
# }
```
## Set up aliases
You can assign aliases for collections to make them more meaningful in a specific context. You can assign multiple aliases for a collection, but multiple collections cannot share an alias.
### Create aliases

To create aliases, use the [`create\_alias()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create\_alias.md) method, specifying the collection name and the alias.

To create aliases, use the [`createAlias()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/createAlias.md) method, specifying the collection name and the alias.

To create aliases, use the [`createAlias()`](https://milvus.io/api-reference/node/v2.4.x/Collections/createAlias.md) method, specifying the collection name and the alias.

To create aliases for a collection, you can use the [`POST /v2/vectordb/aliases/create`](https://milvus.io/api-reference/restful/v2.4.x/v2/Alias%20(v2)/Create.md) API endpoint.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[cURL](#shell)

```python
# 9.1. Create aliases
client.create\_alias(
collection\_name="customized\_setup\_2",
alias="bob"
)
client.create\_alias(
collection\_name="customized\_setup\_2",
alias="alice"
)
```
```java
import io.milvus.v2.service.utility.request.CreateAliasReq;
// 9. Manage aliases
// 9.1 Create alias
CreateAliasReq createAliasReq = CreateAliasReq.builder()
.collectionName("customized\_setup\_2")
.alias("bob")
.build();
client.createAlias(createAliasReq);
createAliasReq = CreateAliasReq.builder()
.collectionName("customized\_setup\_2")
.alias("alice")
.build();
client.createAlias(createAliasReq);
```
```javascript
// 9. Manage aliases
// 9.1 Create aliases
res = await client.createAlias({
collection\_name: "customized\_setup\_2",
alias: "bob"
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.createAlias({
collection\_name: "customized\_setup\_2",
alias: "alice"
})
console.log(res.error\_code)
// Output
//
// Success
//
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/create" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2",
"aliasName": "bob"
}'
# Output
#
# {
# "code": 0,
# "data": {}
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/create" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2",
"aliasName": "alice"
}'
# Output
#
# {
# "code": 0,
# "data": {}
# }
```

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of the collection to create an alias for. |
| `alias` | The alias of the collection. Before this operation, ensure that the alias does not already exist. If it does, exceptions will occur. |

| Parameter | Description |
| --- | --- |
| `collectionName` | The name of the collection to create an alias for. |
| `alias` | The alias of the collection. Before this operation, ensure that the alias does not already exist. If it does, exceptions will occur. |

| Parameter | Description |
| --- | --- |
| `collection_name` | The name of the collection to create an alias for. |
| `alias` | The alias of the collection. Before this operation, ensure that the alias does not already exist. If it does, exceptions will occur. |

| Parameter | Description |
| --- | --- |
| `collectionName` | The name of the collection to create an alias for. |
| `aliasName` | The alias of the collection. Before this operation, ensure that the alias does not already exist. If it does, exceptions will occur. |

### List aliases

To list aliases, use the [`list\_aliases()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/list\_aliases.md) method, specifying the collection name.

To list aliases, use the [`listAliases()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/listAliases.md) method, specifying the collection name.

To list aliases, use the [`listAliases()`](https://milvus.io/api-reference/node/v2.4.x/Collections/listAliases.md) method, specifying the collection name.

To list aliases for a collection, you can use the [`POST /v2/vectordb/aliases/list`](https://milvus.io/api-reference/restful/v2.4.x/v2/Alias%20(v2)/List.md) API endpoint.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[cURL](#shell)

```python
# 9.2. List aliases
res = client.list\_aliases(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "aliases": [
# "bob",
# "alice"
# ],
# "collection\_name": "customized\_setup\_2",
# "db\_name": "default"
# }
```
```java
import io.milvus.v2.service.utility.request.ListAliasesReq;
import io.milvus.v2.service.utility.response.ListAliasResp;
// 9.2 List alises
ListAliasesReq listAliasesReq = ListAliasesReq.builder()
.collectionName("customized\_setup\_2")
.build();
ListAliasResp listAliasRes = client.listAliases(listAliasesReq);
System.out.println(listAliasRes.getAlias());
// Output:
// [
// "bob",
// "alice"
// ]
```
```javascript
// 9.2 List aliases
res = await client.listAliases({
collection\_name: "customized\_setup\_2"
})
console.log(res.aliases)
// Output
//
// [ 'bob', 'alice' ]
//
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/list" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": [
# "bob",
# "alice"
# ]
# }
```
### Describe aliases

To describe aliases, use the [`describe\_alias()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/describe\_alias.md) method, specifying the alias.

To describe aliases, use the [`describeAlias()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/describeAlias.md) method, specifying the alias.

To describe aliases, use the [`describeAlias()`](https://milvus.io/api-reference/node/v2.4.x/Collections/describeAlias.md) method, specifying the alias.

To describe aliases for a collection, you can use the [`POST /v2/vectordb/aliases/describe`](https://milvus.io/api-reference/restful/v2.4.x/v2/Alias%20(v2)/Describe.md) API endpoint.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[cURL](#shell)

```python
# 9.3. Describe aliases
res = client.describe\_alias(
alias="bob"
)
print(res)
# Output
#
# {
# "alias": "bob",
# "collection\_name": "customized\_setup\_2",
# "db\_name": "default"
# }
```
```java
import io.milvus.v2.service.utility.request.DescribeAliasReq;
import io.milvus.v2.service.utility.response.DescribeAliasResp;
// 9.3 Describe alias
DescribeAliasReq describeAliasReq = DescribeAliasReq.builder()
.alias("bob")
.build();
DescribeAliasResp describeAliasRes = client.describeAlias(describeAliasReq);
System.out.println(JSONObject.toJSON(describeAliasRes));
// Output:
// {
// "alias": "bob",
// "collectionName": "customized\_setup\_2"
// }
```
```javascript
// 9.3 Describe aliases
res = await client.describeAlias({
collection\_name: "customized\_setup\_2",
alias: "bob"
})
console.log(res)
// Output
//
// {
// status: {
// extra\_info: {},
// error\_code: 'Success',
// reason: '',
// code: 0,
// retriable: false,
// detail: ''
// },
// db\_name: 'default',
// alias: 'bob',
// collection: 'customized\_setup\_2'
// }
//
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/describe" \
-H "Content-Type: application/json" \
-d '{
"aliasName": "bob"
}'
# {
# "code": 0,
# "data": {
# "aliasName": "bob",
# "collectionName": "quick\_setup",
# "dbName": "default"
# }
# }
```
### Reassign aliases

To reassign aliases to other collections, use the [`alter\_alias()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/alter\_alias.md) method, specifying the collection name and the alias.

To reassign aliases to other collections, use the [`alterAlias()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/alterAlias.md) method, specifying the collection name and the alias.

To reassign aliases to other collections, use the [`alterAlias()`](https://milvus.io/api-reference/node/v2.4.x/Collections/alterAlias.md) method, specifying the collection name and the alias.

To reassign aliases to other collections, you can use the [`POST /v2/vectordb/aliases/alter`](https://milvus.io/api-reference/restful/v2.4.x/v2/Alias%20(v2)/Alter.md) API endpoint.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[cURL](#shell)

```python
# 9.4 Reassign aliases to other collections
client.alter\_alias(
collection\_name="customized\_setup\_1",
alias="alice"
)
res = client.list\_aliases(
collection\_name="customized\_setup\_1"
)
print(res)
# Output
#
# {
# "aliases": [
# "alice"
# ],
# "collection\_name": "customized\_setup\_1",
# "db\_name": "default"
# }
res = client.list\_aliases(
collection\_name="customized\_setup\_2"
)
print(res)
# Output
#
# {
# "aliases": [
# "bob"
# ],
# "collection\_name": "customized\_setup\_2",
# "db\_name": "default"
# }
```
```java
import io.milvus.v2.service.utility.request.AlterAliasReq;
// 9.4 Reassign alias to other collections
AlterAliasReq alterAliasReq = AlterAliasReq.builder()
.collectionName("customized\_setup\_1")
.alias("alice")
.build();
client.alterAlias(alterAliasReq);
listAliasesReq = ListAliasesReq.builder()
.collectionName("customized\_setup\_1")
.build();
listAliasRes = client.listAliases(listAliasesReq);
System.out.println(listAliasRes.getAlias());
// Output:
// ["alice"]
listAliasesReq = ListAliasesReq.builder()
.collectionName("customized\_setup\_2")
.build();
listAliasRes = client.listAliases(listAliasesReq);
System.out.println(listAliasRes.getAlias());
// Output:
// ["bob"]
```
```javascript
// 9.4 Reassign aliases to other collections
res = await client.alterAlias({
collection\_name: "customized\_setup\_1",
alias: "alice"
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.listAliases({
collection\_name: "customized\_setup\_1"
})
console.log(res.aliases)
// Output
//
// [ 'alice' ]
//
res = await client.listAliases({
collection\_name: "customized\_setup\_2"
})
console.log(res.aliases)
// Output
//
// [ 'bob' ]
//
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/alter" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_1",
"aliasName": "alice"
}'
# {
# "code": 0,
# "data": {}
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/list" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_1"
}'
# {
# "code": 0,
# "data": [
# "alice"
# ]
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/list" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": [
# "bob"
# ]
# }
```
### Drop aliases

To drop aliases, use the [`drop\_alias()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/drop\_alias.md) method, specifying the alias.

To drop aliases, use the [`dropAlias()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/dropAlias.md) method, specifying the alias.

To drop aliases, use the [`dropAlias()`](https://milvus.io/api-reference/node/v2.4.x/Collections/dropAlias.md) method, specifying the alias.

To drop aliases for a collection, you can use the [`POST /v2/vectordb/aliases/drop`](https://milvus.io/api-reference/restful/v2.4.x/v2/Alias%20(v2)/Drop.md) API endpoint.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)

```python
# 9.5 Drop aliases
client.drop\_alias(
alias="bob"
)
client.drop\_alias(
alias="alice"
)
```
```java
import io.milvus.v2.service.utility.request.DropAliasReq;
// 9.5 Drop alias
DropAliasReq dropAliasReq = DropAliasReq.builder()
.alias("bob")
.build();
client.dropAlias(dropAliasReq);
dropAliasReq = DropAliasReq.builder()
.alias("alice")
.build();
client.dropAlias(dropAliasReq);
```
```javascript
// 9.5 Drop aliases
res = await client.dropAlias({
alias: "bob"
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.dropAlias({
alias: "alice"
})
console.log(res.error\_code)
// Output
//
// Success
//
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/drop" \
-H "Content-Type: application/json" \
-d '{
"aliasName": "bob"
}'
# {
# "code": 0,
# "data": {}
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/aliases/drop" \
-H "Content-Type: application/json" \
-d '{
"aliasName": "alice"
}'
# {
# "code": 0,
# "data": {}
# }
```
## Set Properties
You can set properties for a collection, such as `ttl.seconds` and `mmap.enabled`. For more information, refer to [set\_properties()](https://milvus.io/api-reference/pymilvus/v2.4.x/ORM/Collection/set\_properties.md).

The code snippets in this section use the [PyMilvus ORM module](https://milvus.io/api-reference/pymilvus/v2.4.x/ORM/Connections/connect.md) to interact with Milvus. Code snippets with the new [MilvusClient SDK](https://milvus.io/api-reference/pymilvus/v2.4.x/About.md) will be available soon.

### Set TTL
Set the Time-To-Live (TTL) for the data in the collection, which specifies how long the data should be retained before it is automatically deleted.
```python
from pymilvus import Collection, connections
# Connect to Milvus server
connections.connect(host="localhost", port="19530") # Change to your Milvus server IP and port
# Get existing collection
collection = Collection("quick\_setup")
# Set the TTL for the data in the collection
collection.set\_properties(
properties={
"collection.ttl.seconds": 60
}
)
```
### Set MMAP
Configure the memory mapping (MMAP) property for the collection, which determines whether data is mapped into memory to improve query performance. For more information, refer to [Configure memory mapping
](https://milvus.io/docs/mmap.md#Configure-memory-mapping).

Before setting the MMAP property, release the collection first. Otherwise, an error will occur.

```python
from pymilvus import Collection, connections
# Connect to Milvus server
connections.connect(host="localhost", port="19530") # Change to your Milvus server IP and port
# Get existing collection
collection = Collection("quick\_setup")
# Before setting memory mapping property, we need to release the collection first.
collection.release()
# Set memory mapping property to True or Flase
collection.set\_properties(
properties={
"mmap.enabled": True
}
)
```
## Drop a Collection
If a collection is no longer needed, you can drop the collection.

To drop a collection, use the [`drop\_collection()`](https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/drop\_collection.md) method, specifying the collection name.

To drop a collection, use the [`dropCollection()`](https://milvus.io/api-reference/java/v2.4.x/v2/Collections/dropCollection.md) method, specifying the collection name.

To drop a collection, use the [`dropCollection()`](https://milvus.io/api-reference/node/v2.4.x/Collections/dropCollection.md) method, specifying the collection name.

To drop a collection, use the [`DropCollection()`](https://milvus.io/api-reference/go/v2.4.x/Collection/DropCollection.md) method, specifying the collection name.

To drop a collection, you can use the [`POST /v2/vectordb/collections/drop`](https://milvus.io/api-reference/restful/v2.4.x/v2/Collection%20(v2)/Drop.md) API endpoint.

[Python](#python) 
[Java](#java)
[Node.js](#javascript)
[Go](#go)
[cURL](#shell)

```python
# 10. Drop the collections
client.drop\_collection(
collection\_name="quick\_setup"
)
client.drop\_collection(
collection\_name="customized\_setup\_1"
)
client.drop\_collection(
collection\_name="customized\_setup\_2"
)
```
```java
import io.milvus.v2.service.collection.request.DropCollectionReq;
// 10. Drop collections
DropCollectionReq dropQuickSetupParam = DropCollectionReq.builder()
.collectionName("quick\_setup")
.build();
client.dropCollection(dropQuickSetupParam);
DropCollectionReq dropCustomizedSetupParam = DropCollectionReq.builder()
.collectionName("customized\_setup\_1")
.build();
client.dropCollection(dropCustomizedSetupParam);
dropCustomizedSetupParam = DropCollectionReq.builder()
.collectionName("customized\_setup\_2")
.build();
client.dropCollection(dropCustomizedSetupParam);
```
```javascript
// 10. Drop the collection
res = await client.dropCollection({
collection\_name: "customized\_setup\_2"
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.dropCollection({
collection\_name: "customized\_setup\_1"
})
console.log(res.error\_code)
// Output
//
// Success
//
res = await client.dropCollection({
collection\_name: "quick\_setup"
})
console.log(res.error\_code)
// Output
//
// Success
//
```
```go
// 10. Drop collections
err = client.DropCollection(ctx, "quick\_setup")
if err != nil {
log.Fatal("failed to drop collection:", err.Error())
}
err = client.DropCollection(ctx, "customized\_setup\_2")
if err != nil {
log.Fatal("failed to drop collection:", err.Error())
}
```
```shell
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/drop" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "quick\_setup"
}'
# {
# "code": 0,
# "data": {}
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/drop" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_1"
}'
# {
# "code": 0,
# "data": {}
# }
$ curl -X POST "http://${MILVUS\_URI}/v2/vectordb/collections/drop" \
-H "Content-Type: application/json" \
-d '{
"collectionName": "customized\_setup\_2"
}'
# {
# "code": 0,
# "data": {}
# }
```