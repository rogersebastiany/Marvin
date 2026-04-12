# AWS Bedrock Knowledge Base S3 Setup


---

## 1. Turning data into a knowledge base

Turning data into a knowledge base - Amazon Bedrock

# Turning data into a knowledge base

To create a knowledge base, connect to a supported data source that you want your knowledge base to be able to access. Your knowledge base will be able to respond to user queries or generate responses based on the retrieved data.

Amazon Bedrock Knowledge Bases supports a variety of documents, including text, images, or multimodal documents that contain tables, charts, diagrams, and other images. *Multimodal* data refers to a combination of text and visual data. Examples of file types that contain unstructured data are text, markdown, HTML, and PDFs.

The following sections describe the types of data that Amazon Bedrock Knowledge Bases supports and the services that you can connect your knowledge base to for each type of data:

## Unstructured data

Unstructured data refers to data that isn't forced into a predefined structure. Amazon Bedrock Knowledge Bases supports connecting to the following services to add unstructured data to your knowledge base:

* Amazon S3
* Confluence (preview)
* Microsoft SharePoint (preview)
* Salesforce (preview)
* Web Crawler (preview)
* Custom data source (allows direct ingestion of data into knowledge bases without needing to sync)

A data source contains the raw form of your documents. To optimize the query process, a knowledge base converts your raw data into *vector embeddings*, a numerical representation of the data, to quantify similarity to queries that are also converted into vector embeddings. Amazon Bedrock Knowledge Bases uses the following resources in the process of converting your data source:

* Embedding model – A foundation model that converts your data into vector embeddings. For multimodal data containing both text and images, you can use multimodal embedding models like Amazon Titan Multimodal Embeddings G1 or Cohere Embed v3.
* Vector store – A service that stores the vector representation of your data. The following vector stores are supported:

  + Amazon OpenSearch Serverless
  + Amazon Neptune
  + Amazon Aurora (RDS)
  + Pinecone
  + Redis Enterprise Cloud
  + MongoDB Atlas

The process of converting your data into vector embeddings is called *ingestion*. The ingestion process that turns your data into a knowledge base involves the following steps:

###### Ingestion

1. The data is parsed by your chosen parser. For more information about parsing, see [Parsing options for your data source](./kb-advanced-parsing.html).
2. Each document in your data source is split into *chunks*, subdivisions of the data that can be defined by the number of tokens and other parameters. For more information about chunking, see [How content chunking works for knowledge bases](./kb-chunking.html).
3. Your chosen embedding model converts the data into vector embeddings. For multimodal content, images are embedded as visual vectors while text is embedded as text vectors, enabling search across both modalities.
4. The vector embeddings are written to a vector index in your chosen vector store.

After the ingestion process is complete, your knowledge base is ready to be queried. For information about how to query and retrieve information from your knowledge base, see [Retrieving information from data sources using Amazon Bedrock Knowledge Bases](./kb-how-retrieval.html).

If you make changes to a data sources, you must sync the changes to ingest additions, modifications, and deletions into the knowledge base. Some data sources support direct ingestion or deletion of files into the knowledge base, eliminating the need to treat data source modification and ingestion as separate steps and the need to always perform full syncs. To learn how to ingest documents directly into your knowledge base and the data sources that support it, see [Ingest changes directly into a knowledge base](./kb-direct-ingestion.html).

Amazon Bedrock Knowledge Bases offers various options to customize how your data is ingested. For more information about customizing this process, see [Customizing your knowledge base](./kb-how-customization.html).

## Structured data

Structured data refers to tabular data in a format that is predefined by the data store it exists in. Amazon Bedrock Knowledge Bases connects to supported structured data stores through the Amazon Redshift query engine. Amazon Bedrock Knowledge Bases provides a fully managed mechanism that analyzes query patterns, query history, and schema metadata to convert natural language queries into SQL queries. These converted queries are then used to retrieve relevant information from supported data sources.

Amazon Bedrock Knowledge Bases supports connecting to the following services to add structured data stores to your knowledge base:

* Amazon Redshift
* AWS Glue Data Catalog (AWS Lake Formation)

If you connect your knowledge base to a structured data store, you don't need to convert the data into vector embeddings. Instead, Amazon Bedrock Knowledge Bases can directly query the structured data store. During query, Amazon Bedrock Knowledge Bases can convert user queries into SQL queries to retrieve data that is relevant to the user query and generate more accurate responses. You can also generate SQL queries without retrieving data and use them in other workflows.

As an example, a database repository contains the following table with information about
customers and their purchases:

| Customer ID | Amount purchased in 2020 | Amount purchased in 2021 | Amount purchased in 2022 | Total purchased amount to date |
| --- | --- | --- | --- | --- |
| 1 | 200 | 300 | 500 | 1000 |
| 2 | 150 | 100 | 120 | 370 |
| 3 | 300 | 300 | 300 | 900 |
| 4 | 720 | 180 | 100 | 900 |
| 5 | 500 | 400 | 100 | 1000 |
| 6 | 900 | 800 | 1000 | 2700 |
| 7 | 470 | 420 | 400 | 1290 |
| 8 | 250 | 280 | 250 | 780 |
| 9 | 620 | 830 | 740 | 2190 |
| 10 | 300 | 200 | 300 | 800 |

If a user query says "give me a summary of the top 5
spending customers," the knowledge base can do the following:

* Convert the query into an SQL query.
* Return an excerpt from the table that contains the following:

  + Relevant table columns "Customer ID" and "Total Purchased Amount To Date"
  + Table rows containing the total purchase amount for the 10 highest spending customers
* Generate a response that states which customers were the top 5 spending customers and how much they purchased.

Other examples of queries that a knowledge base can generate a table excerpt for include:

* "top 5 customers by spending in 2020"
* "top customer by purchase amount in 2020"
* "top 5 customers by purchase amount from 2020-2022"
* "top 5 highest spending customers in 2020-2022"
* "customers with total purchase amount less than $10"
* "top 5 lowest spending customers"

The more specific or detailed a query is, the more the knowledge base can narrow down the exact information to return. For example, instead of the query "top 10 customers by spending in 2020", a more specific query is “find the 10 highest total purchased amount to date for customers in 2020". The specific query refers to the column name "Total Purchased Amount To Date" in the customers spending database table, and also indicates that the data should be sorted by "highest".

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 2. Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases

Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases - Amazon Bedrock

# Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases

When you create a knowledge base by connecting to a data source, you set up or specify the following:

* General information that defines and identifies the knowledge base
* The service role with permissions to the knowledge base.
* Configurations for the knowledge base, including the embeddings model to use when converting data from the data source, storage configurations for the service in which to store the embeddings, and, optionally, an S3 location to store multimodal data.

###### Note

You can’t create a knowledge base with a root user. Log in with an IAM user before starting these steps.

Expand the section that corresponds to your use case:

###### To set up a knowledge base

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at
   <https://console.aws.amazon.com/bedrock>.
2. In the left navigation pane, choose **Knowledge bases**.
3. In the **Knowledge bases** section, choose the create button and select to create a knowledge base with a vector store.
4. (Optional) Change the default name and provide a description for your knowledge base.
5. Choose an AWS Identity and Access Management (IAM) role that provides Amazon Bedrock
   permission to access other required AWS services. You can let Amazon Bedrock create the service role or
   choose to use your own [custom role that you created for
   Neptune Analytics](./kb-permissions.html#kb-permissions-neptune).
6. Choose a data source to connect your knowledge base to.
7. (Optional) Add tags to your knowledge base. For more information, see
   [Tagging Amazon Bedrock resources](./tagging.html).
8. (Optional) Configure services for which to deliver activity logs for your knowledge base.
9. Go to the next section and follow the steps at [Connect a data source to your knowledge base](./data-source-connectors.html) to configure a data source.
10. In the **Embeddings model** section, do the following:

    1. Choose an embeddings model to convert your data into vector embeddings. For multimodal data (images, audio, and video), select a multimodal embedding model such as Amazon Titan Multimodal Embeddings G1 or Cohere Embed v3.

       ###### Note

       When using Amazon Titan Multimodal Embeddings G1, you must provide an S3 content bucket and can only use the default parser. This model is optimized for image search use cases. For comprehensive guidance on choosing between multimodal approaches, see [Build a knowledge base for multimodal content](./kb-multimodal.html).
    2. (Optional) Expand the **Additional configurations** section to see the following configuration options (not all models support all configurations):

       * **Embeddings type** – Whether to convert the data to floating-point (float32) vector embeddings (more precise, but more costly) or binary vector embeddings (less precise, but less costly). To learn about which embeddings models support binary vectors, refer to [supported embeddings models](./knowledge-base-supported.html).
       * **Vector dimensions** – Higher values improve accuracy but increase cost and latency.
11. In the **Vector database** section, do the following:

    1. Choose a vector store to store the vector embeddings that will be used for query. You have the following options:

       * **Quick create a new vector store** – choose one of the available
         vector stores for Amazon Bedrock to create. You can also optionally configure AWS KMS key encryption for your
         vector store.

         ###### Note

         When using this option, Amazon Bedrock automatically handles the metadata placement for each vector store.

         + **Amazon OpenSearch Serverless** – Amazon Bedrock Knowledge Bases creates an Amazon OpenSearch Serverless vector search collection and index and configures it with the required fields for you.
         + **Amazon Aurora PostgreSQL Serverless** – Amazon Bedrock sets up an Amazon Aurora PostgreSQL Serverless vector store. This process takes unstructured text data from
           an Amazon S3 bucket, transforms it into text chunks and vectors, and then stores them in a PostgreSQL database. For more information, see [Quick create an Aurora PostgreSQL Knowledge Base for Amazon Bedrock](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.quickcreatekb.html).
         + **Amazon Neptune Analytics** – Amazon Bedrock uses Retrieval Augmented Generation (RAG) techniques combined with graphs to enhance generative AI applications so that end users can get more accurate and comprehensive responses.
         + **Amazon S3 Vectors** – Amazon Bedrock Knowledge Bases creates an S3 vector bucket and a vector index that will store the embeddings
           generated from your data sources.

           You can create a knowledge base for Amazon S3 Vectors in all AWS Regions where both Amazon Bedrock and
           Amazon S3 Vectors are available. For region availability information, see [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) in the *Amazon S3 User Guide*.

           ###### Note

           When using Amazon S3 Vectors with Amazon Bedrock Knowledge Bases, you can attach up to 1 KB of custom metadata (including both filterable and non-filterable metadata) and 35 metadata keys per vector. For detailed information about metadata limitations, see [Metadata support](./knowledge-base-setup.html#metadata-support) in [Prerequisites for using a vector store you created for a knowledge base](./knowledge-base-setup.html).
       * **Choose a vector store you have created** – Select a supported vector store and identify the vector field names and metadata
         field names in the vector index. For more information, see [Prerequisites for using a vector store you created for a knowledge base](./knowledge-base-setup.html).

         ###### Note

         If your data source is a Confluence, Microsoft SharePoint, or Salesforce instance, the only supported vector store service is Amazon OpenSearch Serverless.
    2. (Optional) Expand the **Additional configurations** section and modify any relevant configurations.
12. If your data source contains images, specify an Amazon S3 URI in which to store the images that the parser will extract from the data in the **Multimodal storage destination**. The images can be returned during query. You can also optionally choose a customer managed key instead of the default AWS managed key to encrypt your data.

    ###### Note

    Multimodal data is only supported with Amazon S3 and custom data sources.

    ###### Note

    When using multimodal embedding models:

    * Amazon Titan Multimodal Embeddings G1 requires an S3 content bucket and works best with image-only datasets using the default parser
    * Cohere Embed v3 supports mixed text and image datasets and can be used with any parser configuration
    * For image search use cases, avoid using Bedrock Data Automation (BDA) or foundation model parsers with Titan G1 due to token limitations
    * The multimodal storage destination creates file copies for retrieval purposes, which can incur additional storage charges
13. Choose **Next** and review the details of your knowledge base. You can edit any
    section before going ahead and creating your knowledge base.

    ###### Note

    The time it takes to create the knowledge base depends on your specific configurations.
    When the creation of the knowledge base has completed, the status of the knowledge base changes to
    either state it is ready or available.

    Once your knowledge base is ready and available, sync your data source
    for the first time and whenever you want to keep your content up to date.
    Select your knowledge base in the console and select **Sync** within
    the data source overview section.

To create a knowledge base, send a [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html) request with an [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

###### Note

If you prefer to let Amazon Bedrock create and manage a vector store for you, use the console. For more information, expand the **Use the console** section in this topic.

The following fields are required:

| Field | Basic description |
| --- | --- |
| name | A name for the knowledge base |
| roleArn | The ARN of an [Amazon Bedrock Knowledge Bases service role](./kb-permissions.html). |
| knowledgeBaseConfiguration | Contains configurations for the knowledge base. See details below. |
| storageConfiguration | (Only required if you're connecting to an unstructured data source). Contains configurations for the data source service that you choose. |

The following fields are optional:

| Field | Use case |
| --- | --- |
| description | A description for the knowledge base. |
| clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). |
| tags | To associate tags with the flow. For more information, see [Tagging Amazon Bedrock resources](./tagging.html). |

In the `knowledgeBaseConfiguration` field, which maps to a [KnowledgeBaseConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_KnowledgeBaseConfiguration.html) object, specify `VECTOR` in the `type` field and include a [VectorKnowledgeBaseConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_VectorKnowledgeBaseConfiguration.html) object. In the object, include the following fields:

* `embeddingModelArn` – The ARN of the embedding model to use.
* `embeddingModelConfiguration` – Configurations for the embedding model. To see the possible values you can specify for each supported model, see [Supported models and Regions for Amazon Bedrock knowledge bases](./knowledge-base-supported.html).
* (If you plan to include multimodal data, which includes images, figures, charts, or tables, in your knowledge base) `supplementalDataStorageConfiguration` – Maps to a [SupplementalDataStorageLocation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_SupplementalDataStorageLocation.html) object, in which you specify the S3 location in which to store the extracted data. For more information, see [Parsing options for your data source](./kb-advanced-parsing.html).

In the `storageConfiguration` field, which maps to a [StorageConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StorageConfiguration.html) object, specify the vector store that you plan to connect to in the `type` field and include the field that corresponds to that vector store. See each vector store configuration type at [StorageConfiguration](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StorageConfiguration.html) for details about the information you need to provide.

The following shows an example request to create a knowledge base connected to an Amazon OpenSearch Serverless collection. The data from connected data sources will be converted into binary vector embeddings with Amazon Titan Text Embeddings V2 and multimodal data extracted by the parser is set up to be stored in a bucket called `MyBucket`.

```
PUT /knowledgebases/ HTTP/1.1
Content-type: application/json

{
   "name": "MyKB",
   "description": "My knowledge base",
   "roleArn": "arn:aws:iam::111122223333:role/service-role/AmazonBedrockExecutionRoleForKnowledgeBase_123",
   "knowledgeBaseConfiguration": {
      "type": "VECTOR",
      "vectorKnowledgeBaseConfiguration": { 
         "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0",
         "embeddingModelConfiguration": { 
            "bedrockEmbeddingModelConfiguration": { 
               "dimensions": 1024,
               "embeddingDataType": "BINARY"
            }
         },
         "supplementalDataStorageConfiguration": { 
            "storageLocations": [ 
               { 
                  "s3Location": { 
                     "uri": "arn:aws:s3:::MyBucket"
                  },
                  "type": "S3"
               }
            ]
         }
      }
   },
   "storageConfiguration": { 
      "opensearchServerlessConfiguration": { 
         "collectionArn": "arn:aws:aoss:us-east-1:111122223333:collection/abcdefghij1234567890",
         "fieldMapping": { 
            "metadataField": "metadata",
            "textField": "text",
            "vectorField": "vector"
         },
         "vectorIndexName": "MyVectorIndex"
      }
   }
}
```

###### Topics

* [Connect a data source to your knowledge base](./data-source-connectors.html)
* [Customize ingestion for a data source](./kb-data-source-customize-ingestion.html)
* [Set up security configurations for your knowledge base](./kb-create-security.html)

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 3. Prerequisites for your Amazon Bedrock knowledge base data

Prerequisites for your Amazon Bedrock knowledge base data - Amazon Bedrock

# Prerequisites for your Amazon Bedrock knowledge base data

A data source contains files or content with information that can be retrieved when
your knowledge base is queried. You must store your documents or content in at least one
of the [supported data
sources](https://docs.aws.amazon.com/bedrock/latest/userguide/data-source-connectors.html).

## Supported document formats and limits for knowledge base data

When you connect to a [supported data
source](https://docs.aws.amazon.com/bedrock/latest/userguide/data-source-connectors.html), the content is ingested into your knowledge base.

If you use Amazon S3 to store your files or your data source includes attached files,
then you first must check that each source document file adheres to the
following:

* The source files are of the following supported formats:

  | Format | Extension |
  | --- | --- |
  | Plain text (ASCII only) | .txt |
  | Markdown | .md |
  | HyperText Markup Language | .html |
  | Microsoft Word document | .doc/.docx |
  | Comma-separated values | .csv |
  | Microsoft Excel spreadsheet | .xls/.xlsx |
  | Portable Document Format | .pdf |
* Each file size doesn't exceed the quota of 50 MB.

If you use an Amazon S3 or custom data source, you can use multimodal data, including
JPEG (.jpeg) or PNG (.png) images or files that contain tables, charts,
diagrams, or other images.

###### Note

The maximum size of .JPEG and .PNG files is 3.75 MB.

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 4. Connect to Amazon S3 for your knowledge base

Connect to Amazon S3 for your knowledge base - Amazon Bedrock

# Connect to Amazon S3 for your knowledge base

Amazon S3 is an object storage service that stores data as objects within buckets.
You can connect to your Amazon S3 bucket for your Amazon Bedrock knowledge base by using either
the [AWS Management Console for Amazon Bedrock](https://console.aws.amazon.com/bedrock/home)
or the [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html)
API (see Amazon Bedrock [supported SDKs and AWS CLI](https://docs.aws.amazon.com/bedrock/latest/APIReference/welcome.html)).

###### Multimodal content support

Amazon S3 data sources support multimodal content including images, audio, and video files. For comprehensive guidance on working with multimodal content, see [Build a knowledge base for multimodal content](./kb-multimodal.html).

You can upload a small batch of files to an Amazon S3 bucket using the Amazon S3 console or API.
You can alternatively use [AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html) to upload
multiple files to S3 continuously, and transfer files on a schedule from on-premises, edge,
other cloud, or AWS storage.

Currently only General Purpose S3 buckets are supported.

There are limits to how many files and MB per file that can be crawled. See [Quotas for knowledge bases](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html).

###### Topics

* [Supported features](#supported-features-s3-connector)
* [Prerequisites](#prerequisites-s3-connector)
* [Connection configuration](#configuration-s3-connector)

## Supported features

* Document metadata fields
* Inclusion prefixes
* Incremental content syncs for added, updated, deleted content

## Prerequisites

**In Amazon S3, make sure you**:

* Note the Amazon S3 bucket URI, Amazon Resource Name (ARN), and the AWS
  account ID for the owner of the bucket. You can find the URI and ARN
  in the properties section in the Amazon S3 console. Your bucket must be in the
  same Region as your Amazon Bedrock knowledge base. You must
  have permission to access the bucket.

**In your AWS account, make sure you**:

* Include the necessary permissions to connect to your data source in your
  AWS Identity and Access Management (IAM) role/permissions policy for your
  knowledge base. For information on the required permissions for this data source
  to add to your knowledge base IAM role, see
  [Permissions to access data sources](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html#kb-permissions-access-ds).

###### Note

If you use the console, the IAM role with all the required permissions
can be created for you as part of the steps for creating a knowledge base. After
you have configured your data source and other configurations, the IAM
role with all the required permissions are applied to your specific knowledge base.

## Connection configuration

To connect to your Amazon S3 bucket, you must provide the necessary configuration
information so that Amazon Bedrock can access and crawl your data. You must also follow the
[Prerequisites](#prerequisites-s3-connector).

An example of a configuration for this data source is included in this section.

For more information about inclusion filters,
document metadata fields, incremental syncing, and how these work, select
the following:

You can include a separate file that specifies the document metadata fields/attributes for each
file in your Amazon S3 data source and whether to include them in the embeddings when indexing the data source into the vector store. For example, you can
create a file in the following format, name it `fileName.extension.metadata.json` and upload it to your S3 bucket.

```
{
  "metadataAttributes": {
    "company": {
      "value": {
        "type": "STRING",
        "stringValue": "BioPharm Innovations"
      },
      "includeForEmbedding": true
    },
    "created_date": {
      "value": {
        "type": "NUMBER",
        "numberValue": 20221205
      },
      "includeForEmbedding": true
    },
    "author": {
      "value": {
        "type": "STRING",
        "stringValue": "Lisa Thompson"
      },
      "includeForEmbedding": true
    },
    "origin": {
      "value": {
        "type": "STRING",
        "stringValue": "Overview"
      },
      "includeForEmbedding": true
    }
  }
}
```

The metadata file must use the same name as its associated source document file,
with `.metadata.json` appended onto the end of the file name. The metadata file
must be stored in the same folder or location as the source file in your Amazon S3 bucket. The file
must not exceed the limit of 10 KB. For information on the supported attribute/field data types
and the filtering operators you can apply to your metadata fields, see [Metadata and filtering](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html).

You can specify an inclusion prefix, which is an Amazon S3 path prefix, where you can use an S3 file
or a folder instead of the entire bucket to create the S3 data source connector.

The data source connector crawls new, modified, and deleted content each time your data
source syncs with your knowledge base. Amazon Bedrock can use your data source’s mechanism
for tracking content changes and crawl content that changed since the last sync. When you sync
your data source with your knowledge base for the first time, all content is crawled by default.

To sync your data source with your knowledge base, use the [StartIngestionJob](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StartIngestionJob.html)
API or select your knowledge base in the console and select **Sync** within the
data source overview section.

###### Important

All data that you sync from your data source becomes available to anyone with
`bedrock:Retrieve` permissions to retrieve the data. This can also include any
data with controlled data source permissions. For more
information, see [Knowledge base permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html).

Console
:   ###### To connect an Amazon S3 bucket to your knowledge base

    1. Follow the steps at [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](./knowledge-base-create.html) and choose **Amazon S3** as the data source.
    2. Provide a name for the data source.
    3. Specify whether the Amazon S3 bucket is in your current AWS
       account or another AWS account. Your bucket must be in the
       same Region as the knowledge base.
    4. (Optional) If the Amazon S3 bucket is encrypted with a KMS key, include the key. For more information, see [Permissions to decrypt your AWS KMS key for your data sources in Amazon S3](./encryption-kb.html#encryption-kb-ds).
    5. (Optional) In the **Content parsing and chunking** section, you can customize how to parse and chunk your data. Refer to the following resources to learn more about these customizations:

       * For more information about parsing options, see [Parsing options for your data source](./kb-advanced-parsing.html).
       * For more information about chunking strategies, see [How content chunking works for knowledge bases](./kb-chunking.html).

         ###### Warning

         You can't change the chunking strategy after connecting to the data source.
       * For more information about how to customize chunking of your data and processing of your metadata with a Lambda function, see [Use a custom transformation Lambda function to define how your data is ingested](./kb-custom-transformation.html).
    6. In the **Advanced settings** section, you can optionally configure the following:

       * **KMS key for transient data storage.** – You can encrypt the transient data while converting your data into embeddings with the default AWS managed key or your own KMS key. For more information, see [Encryption of transient data storage during data ingestion](./encryption-kb.html#encryption-kb-ingestion).
       * **Data deletion policy** – You can delete the vector embeddings for your data source that are stored in the vector store by default, or choose to retain the vector store data.
    7. Continue to choose an embeddings model and vector store. To see the remaining steps, return to [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](./knowledge-base-create.html) and continue from the step after connecting your data source.

API
:   The following is an example of a configuration for connecting
    to Amazon S3 for your Amazon Bedrock knowledge base. You configure your data
    source using the API with the AWS CLI or supported SDK, such as Python.
    After you call [CreateKnowledgeBase](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateKnowledgeBase.html), you call [CreateDataSource](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateDataSource.html) to create your data
    source with your connection information in `dataSourceConfiguration`.

    To learn about customizations that you can apply to ingestion by including the optional
    `vectorIngestionConfiguration` field, see [Customize ingestion for a data source](./kb-data-source-customize-ingestion.html).

    **AWS Command Line Interface**

    ```
    aws bedrock-agent create-data-source \
     --name "S3-connector" \
     --description "S3 data source connector for Amazon Bedrock to use content in S3" \
     --knowledge-base-id "your-knowledge-base-id" \
     --data-source-configuration file://s3-bedrock-connector-configuration.json \
     --data-deletion-policy "DELETE" \
     --vector-ingestion-configuration '{"chunkingConfiguration":{"chunkingStrategy":"FIXED_SIZE","fixedSizeChunkingConfiguration":{"maxTokens":100,"overlapPercentage":10}}}'
                        
    s3-bedrock-connector-configuration.json
    {
        "s3Configuration": {
    	    "bucketArn": "arn:aws:s3:::bucket-name",
    	    "bucketOwnerAccountId": "000000000000",
    	    "inclusionPrefixes": [
    	        "documents/"
    	    ]
        },
        "type": "S3"	
    }
    ```

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## Bibliography

1. [Turning data into a knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-how-data.html)
2. [Create a knowledge base by connecting to a data source in Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html)
3. [Prerequisites for your Amazon Bedrock knowledge base data](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html)
4. [Connect to Amazon S3 for your knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/s3-data-source-connector.html)