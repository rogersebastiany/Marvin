# AWS Bedrock Agents and Guardrails


---

## 1. How Amazon Bedrock Agents works

How Amazon Bedrock Agents works - Amazon Bedrock

# How Amazon Bedrock Agents works

|  |
| --- |
| *Accelerate agents to production with Amazon Bedrock AgentCore. AgentCore is an agentic platform to build, deploy, and operate highly capable agents securely at scale. For more information, see the [AgentCore developer guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html).* |

Amazon Bedrock Agents consists of the following two main sets of API operations to help you set up
and run an agent:

* [Build-time API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock.html) to create,
  configure, and manage your agents and their related resources
* [Runtime API operations](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Agents_for_Amazon_Bedrock_Runtime.html) to invoke your agent with user input and to
  initiate orchestration to carry out a task

## Build-time configuration

An agent consists of the following components:

* **Foundation model** – You choose a foundation model (FM) that the agent invokes to interpret user input and subsequent prompts in its orchestration process. The agent also invokes the FM to generate responses and follow-up steps in its process.
* **Instructions** – You write instructions that describe what the agent is designed to do. With advanced prompts, you can further customize instructions for the agent at every step of orchestration and include Lambda functions to parse each step's output.
* At least one of the following:

  + **Action groups** – You define the actions that the agent should perform for the user (through providing the following resources):

    - One of the following schemas to define the parameters that the agent needs to elicit from the user (each action group can use a different schema):

      * An OpenAPI schema to define the API operations that the agent can invoke to perform its tasks. The OpenAPI schema includes the parameters that need to be elicited from the user.
      * A function detail schema to define the parameters that the agent can elicit from the user. These parameters can then be used for further orchestration by the agent, or you can set up how to use them in your own application.
    - (Optional) A Lambda function with the following input and output:

      * Input – The API operation and/or parameters identified during orchestration.
      * Output – The response from the API invocation or the response from the function invocation.
  + **Knowledge bases** – Associate knowledge bases with an agent. The agent queries the knowledge base for extra context to augment response generation and input into steps of the orchestration process.
* **Prompt templates** – Prompt templates are the basis for creating prompts to be provided to the FM. Amazon Bedrock Agents exposes the default four base prompt templates that are used during the pre-processing, orchestration, knowledge base response generation, and post-processing. You can optionally edit these base prompt templates to customize your agent's behavior at each step of its sequence. You can also turn off steps for troubleshooting purposes or if you decide that a step is unnecessary. For more information, see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](./advanced-prompts.html).

At build-time, all these components are gathered to construct base prompts for the agent to perform orchestration until the user request is completed. With advanced prompts, you can modify these base prompts with additional logic and few-shot examples to improve accuracy for each step of agent invocation. The base prompt templates contain instructions, action descriptions, knowledge base descriptions, and conversation history, all of which you can customize to modify the agent to meet your needs. You then *prepare* your agent, which packages all the components of the agents, including security configurations. Preparing the agent brings it into a state where it can be tested in runtime. The following image shows how build-time API operations construct your agent.

## Runtime process

Runtime is managed by the [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) API operation. This operation starts the agent sequence, which consists of the following three main steps.

1. **Pre-processing** – Manages how the agent contextualizes and categorizes user input and can be used to validate input.
2. **Orchestration** – Interprets the user input, invokes action groups and queries knowledge bases, and returns output to the user or as input to continued orchestration. Orchestration consists of the following steps:

   1. The agent interprets the input with a foundation model and generates a *rationale* that lays out the logic for the next step it should take.
   2. The agent predicts which action in an action group it should invoke or which knowledge base it should query.
   3. If the agent predicts that it needs to invoke an action, the agent sends the parameters, determined from the user prompt, to the [Lambda function configured for the action group](./agents-lambda.html) or [returns control](./agents-returncontrol.html) by sending the parameters in the [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response. If the agent doesn't have enough information to invoke the action, it might do one of the following actions:

      * Query an associated knowledge base (**Knowledge base response generation**) to retrieve additional context and summarize the data to augment its generation.
      * Reprompt the user to gather all the required parameters for the action.
   4. The agent generates an output, known as an *observation*, from invoking an action and/or summarizing results from a knowledge base. The agent uses the observation to augment the base prompt, which is then interpreted with a foundation model. The agent then determines if it needs to reiterate the orchestration process.
   5. This loop continues until the agent returns a response to the user or until it needs to prompt the user for extra information.

   During orchestration, the base prompt template is augmented with the agent instructions, action groups, and knowledge bases that you added to the agent. Then, the augmented base prompt is used to invoke the FM. The FM predicts the best possible steps and trajectory to fulfill the user input. At each iteration of orchestration, the FM predicts the API operation to invoke or the knowledge base to query.
3. **Post-processing** – The agent formats the final response to return to the user. This step is turned off by default.

When you invoke your agent, you can turn on a **trace** at runtime. With the trace, you can track the agent's rationale, actions, queries, and observations at each step of the agent sequence. The trace includes the full prompt sent to the foundation model at each step and the outputs from the foundation model, API responses, and knowledge base queries. You can use the trace to understand the agent's reasoning at each step. For more information, see [Track agent's step-by-step reasoning process using trace](./trace-events.html).

As the user session with the agent continues through more `InvokeAgent` requests, the conversation history is preserved. The conversation history continually augments the orchestration base prompt template with context, helping improve the agent's accuracy and performance. The following diagram shows the agent's process during runtime:

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 2. Detect and filter harmful content by using Amazon Bedrock Guardrails

Detect and filter harmful content by using Amazon Bedrock Guardrails - Amazon Bedrock

# Detect and filter harmful content by using Amazon Bedrock Guardrails

Amazon Bedrock Guardrails provides configurable safeguards to help you build safe generative AI applications. With comprehensive safety and privacy controls across
foundation models (FMs), Amazon Bedrock Guardrails offers a consistent user experience to help detect and filter undesirable content and protect sensitive information that might be present in
user inputs or model responses (excluding reasoning content blocks).

You can use Amazon Bedrock Guardrails across multiple use cases and applications. Below are a few examples:

* A chatbot application to help filter harmful user inputs and
  toxic model responses.
* A banking application to help block user queries or model
  responses associated with seeking or providing illegal investment advice.
* A call center application to summarize conversation transcripts between users and
  agents can use guardrails to redact users’ personally identifiable information (PII)
  to protect user privacy.

Amazon Bedrock Guardrails provides the following safeguards (also known as filters) to detect and filter
undesirable content:

* **Content filters** – This filter helps you detect and filter harmful
  text or image content in input prompts or model responses. Filtering is done based
  on detection of certain predefined harmful content categories: Hate, Insults,
  Sexual, Violence, Misconduct and Prompt Attack. You can configure the filter
  strength for each of these categories based on your use cases. These categories are supported for both Classic
  and Standard [tiers](./guardrails-tiers.html). With Standard tier,
  detection of undesirable content is extended to protection against harmful content
  introduced within code elements including comments, variable and function names, and
  string literals.
* **Denied topics** – You can define a set of topics that
  are undesirable in the context of your application. The filter will help block them
  if detected in user queries or model responses. With [Standard tier](./guardrails-tiers.html), detection of undesirable content
  is extended to protection against harmful content introduced within code elements
  including comments, variables and function names, and string literals.
* **Word filters** – You can define a set of custom words or phrases (exact match)
  that you want to block in the interaction between end users and generative AI applications. For example, you can block
  profanity (use a ready-to-use option) as well as custom words such as competitor names.
* **Sensitive information filters** – You can configure
  this filter to help block or mask sensitive information, such as personally identifiable
  information (PII), in user inputs and model responses. Blocking or
  masking is done based on probabilistic detection of sensitive information in
  in entities such as SSN number, Date of Birth, address, etc. This filter
  also allows configuring regular expression based detection of patterns (custom regex).
* **Contextual grounding checks** – This filter helps you detect
  hallucinations in model responses if they are not grounded (factually inaccurate or add new information) in the source or are irrelevant to
  to the user's query. For example, you can block or flag responses in retrieval-augmented generation (RAG) applications. If the model responses deviate
  from the information in the retrieved source or doesn't answer the question from the user.
* **Automated Reasoning checks** – This filter helps you
  validate the accuracy of foundation model responses against a set of logical rules.
  You can use Automated Reasoning checks to detect hallucinations, suggest
  corrections, and highlight unstated assumptions in model responses.

In addition to the above filters, you can also configure the messages to be returned to
the user if a user input or model response is in violation of the filters defined in the
guardrail.

Experiment and benchmark with different configurations and use the built-in test window to
ensure that the results meet your use-case requirements. When you create a guardrail, a
working draft is automatically available for you to iteratively modify. Experiment with
different configurations and use the built-in test window to see whether they are
appropriate for your use-case. If you are satisfied with a set of configurations, you can
create a version of the guardrail and use it with supported foundation models.

Guardrails can be used directly with FMs during the inference API invocation by specifying
the guardrail ID and the version. Guardrails can also be used directly through the
`ApplyGuardrail` API without invoking the foundation models. If a guardrail
is used, it will evaluate the input prompts and the FM completions against the defined
filters.

For retrieval augmented generation (RAG) or conversational applications, you might need to
evaluate only user input prompts while discarding system instructions,
search results, conversation history, or a few short examples. To selectively evaluate a
section of the input prompt, see [Apply tags to user input to filter content](./guardrails-tagging.html) The ability to evaluate only a section of the input prompt is available
through the AWS SDK and not available on the management console including the Bedrock Playground and the Bedrock Guardrails management console.

###### Topics

* [How Amazon Bedrock Guardrails works](./guardrails-how.html)
* [Supported Regions and models for Amazon Bedrock Guardrails](./guardrails-supported.html)
* [Safeguard tiers for guardrails policies](./guardrails-tiers.html)
* [Languages supported by Amazon Bedrock Guardrails](./guardrails-supported-languages.html)
* [Prerequisites for using Amazon Bedrock Guardrails](./guardrails-prereq.html)
* [Set up permissions to use Amazon Bedrock Guardrails](./guardrails-permissions.html)
* [Create your guardrail](./guardrails-components.html)
* [Distribute guardrail inference across AWS Regions](./guardrails-cross-region.html)
* [Apply cross-account safeguards with Amazon Bedrock Guardrails enforcements](./guardrails-enforcements.html)
* [Test your guardrail](./guardrails-test.html)
* [View information about your guardrails](./guardrails-view.html)
* [Modify your guardrail](./guardrails-edit.html)
* [Delete your guardrail](./guardrails-delete.html)
* [Deploy your guardrail](./guardrails-deploy.html)
* [Use cases for Amazon Bedrock Guardrails](./guardrails-use.html)

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 3. Automate tasks in your application using AI agents

Automate tasks in your application using AI agents - Amazon Bedrock

# Automate tasks in your application using AI agents

Amazon Bedrock Agents offers you the ability to build and configure autonomous agents in your
application. An agent helps your end-users complete actions based on organization data and
user input. Agents orchestrate interactions between foundation models (FMs), data sources,
software applications, and user conversations. In addition, agents automatically call APIs
to take actions and invoke knowledge bases to supplement information for these actions.
By integrating agents, you can accelerate your development effort to deliver generative artificial intelligence (generative AI) applications.

With agents, you can automate tasks for your customers and answer questions for them. For
example, you can create an agent that helps customers process insurance claims or an agent
that helps customers make travel reservations. You don't have to provision capacity, manage
infrastructure, or write custom code. Amazon Bedrock manages prompt engineering, memory, monitoring,
encryption, user permissions, and API invocation.

Agents perform the following tasks:

* Extend foundation models to understand user requests and break down the tasks that
  the agent must perform into smaller steps.
* Collect additional information from a user through natural conversation.
* Take actions to fulfill a customer's request by making API calls to your company
  systems.
* Augment performance and accuracy by querying data sources.

To use an agent, you perform the following steps:

1. (Optional) Create a knowledge base to store your private data in that database. For more information, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](./knowledge-base.html).
2. Configure an agent for your use case and add at least one of the following components:

   * At least one action group that the agent can perform. To
     learn how to define the action group and how it's handled by the agent, see [Use action groups to define actions for your agent to perform](./agents-action-create.html).
   * Associate a knowledge base with the agent to augment the agent's performance. For
     more information, see [Augment response generation for your agent with knowledge base](./agents-kb-add.html).
3. (Optional) To customize the agent's behavior to your specific use-case, modify
   prompt templates for the pre-processing, orchestration, knowledge base response
   generation, and post-processing steps that the agent performs. For more information,
   see [Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock](./advanced-prompts.html).
4. Test your agent in the Amazon Bedrock console or through API calls to the
   `TSTALIASID`. Modify the configurations as necessary. Use traces to
   examine your agent's reasoning process at each step of its orchestration. For more
   information, see [Test and troubleshoot agent behavior](./agents-test.html) and [Track agent's step-by-step reasoning process using trace](./trace-events.html).
5. When you have sufficiently modified your agent and it's ready to be deployed to
   your application, create an alias to point to a version of your agent. For more
   information, see [Deploy and use an Amazon Bedrock agent in your application](./agents-deploy.html).
6. Set up your application to make API calls to your agent alias.
7. Iterate on your agent and create more versions and aliases as necessary.

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 4. Create and configure agent manually

Create and configure agent manually - Amazon Bedrock

# Create and configure agent manually

To create an agent with Amazon Bedrock, you set up the following components:

* The configuration of the agent, which defines the purpose of the agent
  and indicates the foundation model (FM) that it uses to generate prompts
  and responses.
* At least one of the following:

  + Action groups that define what actions the agent is designed to perform.
  + A knowledge base of data sources to augment the generative capabilities of the agent by allowing search and query.

You can minimally create an agent that only has a name. To **Prepare** an agent so that you can [test](./agents-test.html) or [deploy](./agents-deploy.html) it, you must minimally configure the following components:

| Configuration | Description |
| --- | --- |
| Agent resource role | The ARN of the [service role with permissions to call API operations on the agent](./agents-permissions.html) |
| Foundation model (FM) | An FM for the agent to invoke to perform orchestration |
| Instructions | Natural language describing what the agent should do and how it should interact with users |

You should also configure at least one action group or knowledge base for the agent. If you prepare an agent with no action groups or knowledge bases, it will return responses based only on the FM and instructions and [base prompt templates](./advanced-prompts.html).

To learn how to create an agent, choose the tab for your preferred method, and then follow the steps:

Console
:   ###### To create an agent

    1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at
       <https://console.aws.amazon.com/bedrock>.
    2. Select **Agents** from the left navigation pane.
    3. In the **Agents** section, choose **Create Agent**.
    4. (Optional) Change the automatically generated **Name** for the agent and provide an optional **Description** for it.
    5. Choose **Create**. Your agent is created and you will be taken to the **Agent builder** for your newly created agent, where you can configure your agent.
    6. You can continue to the following procedure to configure your agent or return to the Agent builder later.

    ###### To configure your agent

    1. If you're not already in the agent builder, do the following:

       1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at
          <https://console.aws.amazon.com/bedrock>.
       2. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.
       3. Choose **Edit in Agent builder**.
    2. In the **Agent details** section, you can set up the following configurations:

       1. Edit the **Agent name** or **Agent description**.
       2. For the **Agent resource role**, select one of the following options:

          * **Create and use a new service role** – Let Amazon Bedrock create the service role and set up the required permissions on your behalf.
          * **Use an existing service role** – Use a [custom role](./agents-permissions.html) that you set up previously.
       3. For **Select model**, select an FM for your agent to invoke during orchestration.

          By default, models optimized for agents are shown. To see all models supported by Amazon Bedrock Agents, clear **Bedrock Agents optimized**.
       4. In **Instructions for the Agent**, enter details to tell the agent what it should do and how it should interact with users. The instructions replace the $instructions$ placeholder in the [orchestration prompt template](./prompt-placeholders.html#placeholders-orchestration). Following is an example of instructions:

          ```
          You are an office assistant in an insurance agency. You are friendly and polite. You help with managing insurance claims and coordinating pending paperwork.
          ```
       5. If you expand **Additional settings**, you can modify the following configurations:

          * **Code Interpreter** –
            (Optional) Choose whether to enable agent to handle
            tasks that involve writing, running, testing, and
            troubleshooting code. For details, see [Generate, run, and test code with code interpretation](./agents-code-interpretation.html).
          * **User input** – (Optional)
            Choose whether to allow the agent to request more
            information from the user if it doesn't have enough
            information. For details, see [Configure agent to request information from user](./agents-user-input.html).
          * **KMS key selection** – (Optional) By default, AWS encrypts agent resources with an AWS managed key. To encrypt your agent with
            your own customer managed key, for the KMS key selection section, select **Customize encryption settings (advanced)**. To create a new key,
            select **Create an AWS KMS key** and then refresh this window. To use an existing key, select a key for **Choose an AWS KMS key**.

          * **Idle session timeout** – By default, if a user hasn't responded for 30 minutes in a session with an Amazon Bedrock agent, the agent no longer maintains the conversation history. Conversation history is used to both resume an interaction and to augment responses with context from the conversation. To change this default length of time, enter a number in the **Session timeout** field and choose a unit of time.
       6. For the **IAM permissions** section, for **Agent resource role**,
          choose a [service role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#iam-term-service-role). To let Amazon Bedrock create the service role on your behalf, choose **Create and use a new service role**. To use a [custom role](./agents-permissions.html) that you created previously, choose **Use an existing service role**.

          ###### Note

          The service role that Amazon Bedrock creates for you doesn't include permissions for features that are in preview. To use these features, [attach the correct permissions to the service role](./agents-permissions.html).
       7. (Optional) By default, AWS encrypts agent resources with an AWS managed key. To encrypt your agent with your own customer managed key, for the **KMS key selection** section, select **Customize encryption settings (advanced)**. To create a new key, select **Create an AWS KMS key** and then refresh this window. To use an existing key, select a key for **Choose an AWS KMS key**.
       8. (Optional) To associate tags with this agent, for the **Tags – optional** section, choose **Add new tag** and provide a key-value pair.
       9. When you are done setting up the agent configuration, select **Next**.
    3. In the **Action groups** section, you can choose **Add** to add action groups to your agent. For more information on setting up action groups, see [Use action groups to define actions for your agent to perform](./agents-action-create.html). To learn how to add action groups to your agent, see [Add an action group to your agent in Amazon Bedrock](./agents-action-add.html).
    4. In the **Knowledge bases** section, you can choose **Add** to associate knowledge groups with your agent. For more information on setting up knowledge bases, see [Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases](./knowledge-base.html). To learn how to associate knowledge bases with your agent, see [Augment response generation for your agent with knowledge base](./agents-kb-add.html).
    5. In the **Guardrails details** section, you can choose **Edit** to associate a guardrail with your agent to block and filter out harmful content. Select a guardrail you want to use from the drop down menu under **Select guardrail** and then choose the version to use under **Guardrail version**. You can select **View** to see your Guardrail settings. For more information, see [Detect and filter harmful content by using Amazon Bedrock Guardrails](./guardrails.html).
    6. In the **Orchestration strategy** section, you can choose **Edit** to customize your agent's orchestration. For more information about the orchestration strategy you can use for your agent, see [Customize agent orchestration strategy](./orch-strategy.html).
    7. In the **Multi-agent collaboration** section, you can choose **Edit** to create a multi-agent collaboration team. For more information about multi-agent collaboration, see [Use multi-agent collaboration with Amazon Bedrock Agents](./agents-multi-agent-collaboration.html).
    8. When you finish configuring your agent, select one of the following options:

       * To stay in the **Agent builder**, choose **Save**. You can then **Prepare** the agent in order to test it with your updated configurations in the test window. To learn how to test your agent, see [Test and troubleshoot agent behavior](./agents-test.html).
       * To return to the **Agent Details** page, choose **Save and exit**.

API
:   To create an agent, send a [CreateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_CreateAgent.html) request (see link for request and response formats and field details) with an
    [Agents for Amazon Bedrock build-time endpoint](https://docs.aws.amazon.com/general/latest/gr/bedrock.html#bra-bt).

    [See code examples](./bedrock-agent_example_bedrock-agent_CreateAgent_section.html)

    To prepare your agent and test or deploy it, so that you can [test](./agents-test.html) or [deploy](./agents-deploy.html) it, you must minimally include the following fields (if you prefer, you can skip these configurations and configure them later by sending an [UpdateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_UpdateAgent.html) request):

    | Field | Use case |
    | --- | --- |
    | agentResourceRoleArn | To specify an ARN of the service role with permissions to call API operations on the agent |
    | foundationModel | To specify a foundation model (FM) for the agent to orchestrate with |
    | instruction | To provide instructions to tell the agent what to do. Used in the $instructions$ placeholder of the orchestration prompt template. |

    The following fields are optional:

    | Field | Use case |
    | --- | --- |
    | description | Describes what the agent does |
    | idleSessionTTLInSeconds | Duration after which the agent ends the session and deletes any stored information. |
    | customerEncryptionKeyArn | ARN of a KMS key to encrypt agent resources |
    | tags | To associate [tags](./tagging.html) with your agent. |
    | promptOverrideConfiguration | To [customize the prompts](./advanced-prompts.html) sent to the FM at each step of orchestration. |
    | guardrailConfiguration | To add a [guardrail](./guardrails.html) to the agent. Specify the ID or ARN of the guardrail and the version to use. |
    | clientToken | To ensure the API request completes only once. For more information, see [Ensuring idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html). |
    | cachingState | To enable prompt caching of input to the agent. For more information, see [Prompt caching for faster model inference](./prompt-caching.html). |
    | reasoning\_config | To enable model reasoning so that the model explains how it reached its conclusions. Use inside of a `additionalModelRequestFields` field. You must specify the number of `budget_tokens` that are used for model reasoning, which are a subset of the output tokens. For more information, see [Enhance model responses with model reasoning](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-reasoning.html). |

    The response returns an [CreateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) object that contains details about your newly created agent. If your agent fails to be created, the [CreateAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_Agent.html) object in the response returns a list of `failureReasons` and a list of `recommendedActions` for you to troubleshoot.

    ```
        def create_agent(self, agent_name, foundation_model, role_arn, instruction):
            """
            Creates an agent that orchestrates interactions between foundation models,
            data sources, software applications, user conversations, and APIs to carry
            out tasks to help customers.

            :param agent_name: A name for the agent.
            :param foundation_model: The foundation model to be used for orchestration by the agent.
            :param role_arn: The ARN of the IAM role with permissions needed by the agent.
            :param instruction: Instructions that tell the agent what it should do and how it should
                                interact with users.
            :return: The response from Amazon Bedrock Agents if successful, otherwise raises an exception.
            """
            try:
                response = self.client.create_agent(
                    agentName=agent_name,
                    foundationModel=foundation_model,
                    agentResourceRoleArn=role_arn,
                    instruction=instruction,
                )
            except ClientError as e:
                logger.error(f"Error: Couldn't create agent. Here's why: {e}")
                raise
            else:
                return response["agent"]
    ```

    For more information, see [Hello Amazon Bedrock Agents](./bedrock-agent_example_bedrock-agent_Hello_section.html).

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## Bibliography

1. [How Amazon Bedrock Agents works](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-how.html)
2. [Detect and filter harmful content by using Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
3. [Automate tasks in your application using AI agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
4. [Create and configure agent manually](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-create.html)