Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases - Amazon Bedrock 

Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases - Amazon Bedrock
{
"@context" : "https://schema.org",
"@type" : "BreadcrumbList",
"itemListElement" : [
{
"@type" : "ListItem",
"position" : 1,
"name" : "AWS",
"item" : "https://aws.amazon.com"
},
{
"@type" : "ListItem",
"position" : 2,
"name" : "Amazon Bedrock",
"item" : "https://docs.aws.amazon.com/bedrock/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/bedrock/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Additional Capabilities",
"item" : "https://docs.aws.amazon.com/bedrock/latest/userguide/additional-capabilities.html"
},
{
"@type" : "ListItem",
"position" : 5,
"name" : "Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases",
"item" : "https://docs.aws.amazon.com/bedrock/latest/userguide/additional-capabilities.html"
}
]
}

[Documentation](/index.html)[Amazon Bedrock](/bedrock/index.html)[User Guide](what-is-bedrock.html)

# Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases

While foundation models have general knowledge, you can further improve their responses by
using Retrieval Augmented Generation (RAG). RAG is a technique that uses information from
data sources to improve the relevancy and accuracy of generated responses. With Amazon Bedrock Knowledge Bases, you
can integrate proprietary information into your generative-AI applications. When a query is
made, a knowledge base searches your data to find relevant information to answer the query.
The retrieved information can then be used to improve generated responses. You can build
your own RAG-based application by using the capabilities of Amazon Bedrock Knowledge Bases.

With Amazon Bedrock Knowledge Bases, you can:

* Answer user queries by returning relevant information from data sources.
* Use retrieved information from data sources to help generate an accurate and
  relevant response to user queries.
* Augment your own prompts by feeding the returned relevant information into the
  prompt.
* Include citations in the generated response so the original data source can be
  referenced and accuracy can be checked.
* Include documents with copious visual resources, from which images can be
  extracted and retrieved in responses to queries. If you generate a response based on
  the retrieved data, the model can deliver additional insights based on these
  images.
* Search using images as queries to find visually similar content, or combine text and images in queries for more precise results using multimodal embedding models.
* Convert natural language into queries (such as SQL queries) that are customized
  for structured databases. These queries are used to retrieve data from structured
  data stores.
* Update your data sources and ingest the changes into the knowledge base directly
  so they can be immediately accessed.
* Use reranking models to influence the results that are retrieved from your data
  source.
* Include the knowledge base in an [Amazon Bedrock Agents](./agents.html)
  workflow.

To set up a knowledge base, you must complete the following general steps:

1. (Optional) If you connect your knowledge base to an unstructured data source, set
   up your own [supported vector
   store](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html) to index the vector embeddings representation of your data. You
   can skip this step if you plan to use the Amazon Bedrock console to create an Amazon OpenSearch Serverless vector
   store for you.
2. Connect your knowledge base to an unstructured or structured data
   source.
3. Sync your data source with your knowledge base.
4. Set up your application or agent to do the following:

   * Query the knowledge base and return relevant sources.
   * Query the knowledge base and generate natural language responses based on
     the retrieved results.
   * (If you query a knowledge base connected to a structured data store)
     Transform a query into a structured data language-specific query (such as an
     SQL query).

###### Topics

* [How knowledge bases work](./kb-how-it-works.html)
* [Supported models and Regions](./knowledge-base-supported.html)
* [Chat with your document with zero setup](./knowledge-base-chatdoc.html)
* [Set up permissions to create and manage knowledge bases](./knowledge-base-prereq-permissions-general.html)
* [Build a knowledge base by connecting to a data source](./knowledge-base-build.html)
* [Build a knowledge base for multimodal content](./kb-multimodal.html)
* [Build a knowledge base by connecting to a structured data store](./knowledge-base-build-structured.html)
* [Build a knowledge base
  with an Amazon Kendra GenAI index](./knowledge-base-build-kendra-genai-index.html)
* [Build a knowledge base with Amazon Neptune Analytics graphs](./knowledge-base-build-graphs.html)
* [Test your knowledge base with queries and responses](./knowledge-base-test.html)
* [Deploy your knowledge base for your application](./knowledge-base-deploy.html)
* [View information about a knowledge base](./kb-info.html)
* [Modify a knowledge base](./kb-update.html)
* [Delete a knowledge base](./kb-delete.html)

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Processing use cases

How knowledge bases work

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.