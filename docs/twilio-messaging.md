# Twilio Messaging and WhatsApp API


---

## 1. Messaging API Overview

Page toolsOn this page

Looking for more inspiration?Visit the

# Messaging API Overview

---

With the Programmable Messaging REST API, you can add messaging capabilities to your application.

---

## Base URLs

To ensure data privacy, Twilio serves its APIs over HTTPS.

Messaging-related APIs use three base URLs:

### Twilio API base URL

The following API resources that process SMS messages point to the Base URL of `https://api.twilio.com/2010-04-01`:

  + [Feedback subresource](/docs/messaging/api/message-feedback-resource "Feedback subresource")
  + [Media subresource](/docs/messaging/api/media-resource "Media subresource")

The following API resources that manage [Messaging Services](/docs/messaging/services "Messaging Services") point to `https://messaging.twilio.com/v1`:

  + [PhoneNumbers subresource](/docs/messaging/api/phonenumber-resource "PhoneNumbers subresource")
  + [Shortcodes subresource](/docs/messaging/api/services-shortcode-resource "Shortcodes subresource")
  + [AlphaSenders subresource](/docs/messaging/api/alphasender-resource "AlphaSenders subresource")
  + [DestinationAlphaSenders subresource](/docs/messaging/api/destination-alphasender-resource "DestinationAlphaSenders subresource")
  + [ChannelSenders subresource](/docs/messaging/api/messaging-service-channelsender-resource "ChannelSenders subresource")

The following API resources that report on deactivated phone numbers and process toll-free verification requests also point to `https://messaging.twilio.com/v1`:

The API resource that reports on [per-country SMS pricing](/docs/messaging/api/pricing "per-country SMS pricing") points to the `https://pricing.twilio.com/v1` base URL.

---

## Authentication

To authenticate requests to the Twilio APIs, Twilio supports [HTTP Basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication "HTTP Basic authentication"). Use your *API key* as the username and your *API key secret* as the password. You can create an API key either [in the Twilio Console](/docs/iam/api-keys/keys-in-console "in the Twilio Console") or [using the API](/docs/iam/api-keys/key-resource-v1 "using the API").

**Note**: Twilio recommends using API keys for authentication in production apps. For local testing, you can use your Account SID as the username and your Auth token as the password. You can find your Account SID and Auth Token in the [Twilio Console](https://www.twilio.com/console "Twilio Console").

Learn more about [Twilio API authentication](/docs/usage/requests-to-twilio "Twilio API authentication").

Here's an example of authenticating with the API:

```
1

curl -G https://api.twilio.com/2010-04-01/Accounts \

2

-u $TWILIO_API_KEY:$TWILIO_API_KEY_SECRET
```

---

## Use the Programmable Messaging API

(information)

## Info

Twilio monitors messages to prevent content violating the [Acceptable Use Policy](https://www.twilio.com/en-us/legal/aup "Acceptable Use Policy") (AUP)*.* This helps to ensure that Twilio Messaging is seen as a trustworthy, high engagement channel and will not slow down the delivery of messages.

If a message you send has violated the AUP, it will be returned and you will receive an error code which identifies the necessary changes you need to make before sending it again.

### Send messages

To send an outbound message, send a `POST` request to the [Messages resource](/docs/messaging/api/message-resource "Messages resource").

* To [send media messages](/docs/messaging/tutorials/how-to-send-sms-messages "send media messages"), use the `MediaUrl` parameter in the request.
* To [schedule an outbound Message](/docs/messaging/features/message-scheduling "schedule an outbound Message") to be sent in the future, use the `ScheduleType` and `SendAt` parameters in the request.
* To [send messages with shortened links](/docs/messaging/features/link-shortening "send messages with shortened links"), use the `ShortenUrls` parameter in the request.
  + **Note**: This feature is available only if you use a [Messaging Service](/docs/messaging/services "Messaging Service").

To learn more about how to receive and reply to messages, see [Receive and Reply to Messages Guide](/docs/messaging/tutorials/how-to-receive-and-reply "Receive and Reply to Messages Guide").

### Fetch, list, update, and delete messages

Use the [Messages resources](/docs/messaging/api/message-resource "Messages resources") to fetch, list, and delete Messages associated with your account.

Redact messages by updating a Message resource.

### Fetch, list, and delete media

Twilio creates a [Media subresource](/docs/messaging/api/media-resource "Media subresource") when an incoming or outgoing Message resource contains media.

You can fetch, list, and delete Media subresources.

### Manage your short codes

Fetch, list, and update your Account's short codes with the [ShortCodes subresource](/docs/messaging/api/short-code-resource "ShortCodes subresource").

### Track message feedback

Track user-reported outcomes of Messages with the [Feedback subresource](/docs/messaging/api/message-feedback-resource "Feedback subresource").

### Manage your Messaging Services

Create, fetch, read, update, and delete Messaging Services with the [Services resource](/docs/messaging/api/service-resource "Services resource").

Manage your Messaging Services' senders with the following subresources:

### Check SMS pricing by country

Check inbound and outbound SMS message pricing with the [Messaging Countries subresources](/docs/messaging/api/pricing "Messaging Countries subresources") of the Pricing API.

### Retrieve a list of deactivated US phone numbers

Fetch a list of all US phone numbers that were deactivated on a given day with the [Deactivations resource](/docs/messaging/api/deactivations-resource "Deactivations resource").

### Verify that your toll-free number complies with regulations

Demonstrate that your toll-free number complies with US and Canadian SMS regulations. Submit, update, or delete toll-free verification (TFV) requests with the [Verifications resource](/docs/messaging/api/tollfree-verification-resource "Verifications resource").

---

## Additional resources

* For inspiration, read the [Twilio Blog](https://www.twilio.com/blog/search-results?search=sms "Twilio Blog") on building messaging applications with various languages and tools.
* Get started with [toll-free verification](/docs/messaging/compliance/toll-free/api-onboarding "toll-free verification").
* For help troubleshooting your Programmable Messaging application, check out the docs on [Debugging Common Issues](/docs/messaging/guides/debugging-common-issues "Debugging Common Issues") and [Debugging Tools](/docs/messaging/guides/debugging-tools "Debugging Tools").
* [Learn more about Twilio's Global Infrastructure](/docs/global-infrastructure "Learn more about Twilio's Global Infrastructure"), which allows you to control where your application's Twilio-related data is routed, processed, and stored.

---

## 2. WhatsApp Business Platform with Twilio

Send and receive [WhatsApp](https://www.whatsapp.com/ "WhatsApp") messages using the [WhatsApp Business Platform](https://business.whatsapp.com/products/business-platform "WhatsApp Business Platform") and Twilio APIs. Build any use case for your business, such as support, notifications, verification, or personalized promotions.

[Get started now](/docs/whatsapp#get-started-with-whatsapp)

Take the next steps with WhatsApp Business Platform with Twilio

[Get started with WhatsApp](/docs/whatsapp#get-started-with-whatsapp)[WhatsApp sender registration](/docs/whatsapp#whatsapp-sender-registration)[Messaging options](/docs/whatsapp#messaging-options)

1

Twilio servers

2

Your app

```
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const client = require('twilio')(accountSid, authToken);

client.messages
      .create({
        from: 'whatsapp:+14155238886',
        contentSid: 'HXb5b62575e6e4ff6129ad7c8efe1f983e',
        contentVariables: '{"1":"2025/7/15","2":"3:00p.m."}',
        to: 'whatsapp:+12345678901'
    })
    .then(message => console.log(message.sid))
```

3

Your appointment is coming up on 2025/7/15 at 3:00p.m.

Take the next steps with WhatsApp Business Platform with Twilio

[Get started with WhatsApp](/docs/whatsapp#get-started-with-whatsapp)[WhatsApp sender registration](/docs/whatsapp#whatsapp-sender-registration)[Messaging options](/docs/whatsapp#messaging-options)

---

## Get started with WhatsApp

Build an application in minutes that sends your first WhatsApp message using the Twilio Programmable Messaging API. You can use the Twilio Sandbox for WhatsApp to prototype your application and test sending and receiving messages.

[Send your first WhatsApp message](/docs/whatsapp/quickstart)[Guide to using the Twilio Sandbox for WhatsApp](/docs/whatsapp/sandbox)

---

## WhatsApp sender registration

A WhatsApp sender is a phone number associated with a [WhatsApp Business Account (WABA)](/docs/whatsapp/tutorial/whatsapp-business-account "WhatsApp Business Account (WABA)"). To send WhatsApp messages under your own brand, you need to register a WhatsApp sender with Twilio.

* If you're a direct customer, register a WhatsApp sender using WhatsApp Self Sign-up.
* If you're an [Independent Software Vendor (ISV)](https://help.twilio.com/articles/4402930862747 "Independent Software Vendor (ISV)"), register a WhatsApp sender through the WhatsApp Tech Provider Program.

[WhatsApp Self-Sign up](/docs/whatsapp/self-sign-up)[WhatsApp Tech Provider Program](/docs/whatsapp/isv/tech-provider-program)

---

## Messaging options

### One-way messaging and notifications

With the [Twilio Programmable Messaging API](/docs/messaging "Twilio Programmable Messaging API"), you can send one-way messages to your customers, such as notifications, alerts, and reminders.

Sending One-Time-Passcodes (OTP)?

WhatsApp is now a more cost-effective channel than SMS for sending OTPs in many regions. The [Verify WhatsApp API](/docs/verify/whatsapp "Verify WhatsApp API") delivers OTPs across WhatsApp, SMS, RCS, and other channels to maximize conversion and reduce cost. The same OTP code is sent across all channels in a single verification session, simplifying code validation.

[Verify WhatsApp](/docs/verify/whatsapp)

### Two-way conversational messaging

With the [Twilio Conversations API](/docs/conversations/using-whatsapp-conversations "Twilio Conversations API"), you can build conversational or back-and-forth messaging on WhatsApp. You can also build cross-channel customer experience across WhatsApp, SMS, MMS, and browser-based or mobile chat messages.

Find your use case

* [Customer support and chatbots](https://www.twilio.com//en-us/blog/ai-chatbot-whatsapp-python-twilio-openai "Customer support and chatbots")
* [Feedback and surveys](https://www.twilio.com/en-us/blog/create-whatsapp-survey-using-twilio-cakephp "Feedback and surveys")

API reference

Learn more

* [Simplify scaling and get more features with Messaging Services](https://www.twilio.com/docs/messaging/services "Simplify scaling and get more features with Messaging Services")

---

### Related products

Messaging

Send and receive SMS/MMS/WhatsApp messages with the Twilio Programmable Messaging API.

[Product documentation](/docs/messaging)

Verify

Fight fraud and protect user accounts. Verify users via SMS, Silent Network Auth, voice, WhatsApp, TOTP, push, Silent Device Approval, and email.

[Product documentation](/docs/verify)

Conversations

Build conversational messaging on multiple channels: web chat, WhatsApp, and SMS

[Product documentation](/docs/conversations)

Studio

Twilio's no-code/low-code application builder. Build your messaging app in your browser.

[Product documentation](/docs/studio)

Flex

Build your digital engagement center for sales and customer support teams.

[Product documentation](/docs/flex)

Engage

Personalize your customer interactions on every channel from a unified, data-first multichannel marketing solution.

[Product documentation](https://www.segment.com/product/twilio-engage)

---

## 3. Overview of the WhatsApp Business Platform with Twilio

Page toolsOn this page

Looking for more inspiration?Visit the

# Overview of the WhatsApp Business Platform with Twilio

---

(warning)

## Warning

Twilio is launching a new Console. Some screenshots on this page may show the Legacy Console and therefore may no longer be accurate. We are working to update all screenshots to reflect the new Console experience. [Learn more about the new Console](https://www.twilio.com/blog/new-and-improved-console-now-in-general-availability "Learn more about the new Console").

WhatsApp is the most popular messaging app in many parts of the world. With the [WhatsApp Business Platform with Twilio](https://www.twilio.com/en-us/messaging/channels/whatsapp "WhatsApp Business Platform with Twilio"), you can [send notifications](/docs/whatsapp/api#sending-notifications-with-whatsapp "send notifications"), have [two-way conversations](/docs/whatsapp/api#conversational-messaging-on-whatsapp "two-way conversations"), and build chatbots. If you're trying to reach and better converse with users in LATAM, EMEA, and APAC, then you need to consider using WhatsApp.

---

## What is the WhatsApp Business Platform?

WhatsApp has three messaging products:

* WhatsApp Consumer app, with users around the globe
* WhatsApp Business app, generally used by small businesses and micro businesses
* WhatsApp Business Platform, previously known as the WhatsApp Business API

Twilio offers access to the WhatsApp Business Platform. Developers can use WhatsApp with all of Twilio's products, including the Programmable Messaging API, Conversations API, Twilio Flex and Studio. For more information, see [WhatsApp Business Accounts with Twilio](/docs/whatsapp/tutorial/whatsapp-business-account "WhatsApp Business Accounts with Twilio").

---

## WhatsApp opt-in requirements

WhatsApp requires that your application implement [explicit user opt-ins](https://developers.facebook.com/docs/whatsapp/guides/opt-in/ "explicit user opt-ins") to deliver messages over WhatsApp. You may gather this opt-in information either via a web page or a mobile app, such as during your application's sign-up flow, in your application's account settings, via SMS, etc. WhatsApp also requires businesses to respect opt-out requests from end users to maintain high number quality.

(warning)

## Warning

Sending messages to end users without an opt-in may result in users blocking your business and may ultimately lead to the suspension of your WhatsApp Business account.

---

## Using Twilio Phone Numbers with WhatsApp

On WhatsApp, users message each other using their phone numbers as identifiers. To send and receive WhatsApp messages using the Twilio Programmable Messaging API, you'll need a phone number as well. The Twilio API addresses WhatsApp users and your numbers, using the following prefixed address format:

`whatsapp:<E.164 formatted phone number>`

([E.164 is an international telephone number format](/docs/glossary/what-e164 "E.164 is an international telephone number format"); you will see it often in the strings that represent Twilio phone numbers.)

### Enabling WhatsApp with a Twilio Number

To use WhatsApp messaging in production apps, you must enable WhatsApp on your Twilio number. For a step-by-step walkthrough of the process, visit our [Self-Signup Guide for WhatsApp](/docs/whatsapp/self-sign-up "Self-Signup Guide for WhatsApp"). If you're registering for WhatsApp on behalf of a third party, such as one of your clients, then you may be an Independent Software Vendor (ISV) and should follow the [WhatsApp Tech Provider Program guide](/docs/whatsapp/isv/tech-provider-program "WhatsApp Tech Provider Program guide").

For information about using a non-Twilio number with WhatsApp, check out our Support guide *[Can I activate my own phone number for WhatsApp on Twilio?](https://help.twilio.com/hc/en-us/articles/360052171393-Can-I-activate-my-own-phone-number-for-WhatsApp-on-Twilio- "Can I activate my own phone number for WhatsApp on Twilio?")*

### Connect your Meta Business Manager Account

WhatsApp uses your Meta Business Manager account to identify your business and associate your WhatsApp Business Account (WABA) with it. To scale with WhatsApp, you will also need to verify your Meta Business Manager account. You can create or connect your Meta Business Manager account through Twilio's Self-Signup process in the Console.

If you are an ISV, you will need to provide Twilio with your Meta Business Manager ID before you or your end clients begin onboarding. If you do not already have a Meta Business Manager account, [follow Facebook's instructions to create one](https://www.facebook.com/business/help/1710077379203657 "follow Facebook's instructions to create one"). Your Meta Business Manager ID can be found in the ["Business Info" section](https://business.facebook.com/settings/info "\"Business Info\" section") under *Business Settings*.

### Manage and configure your WhatsApp-enabled Twilio numbers

You can register new numbers for WhatsApp directly in the Twilio Console by following our [Self-Signup Guide for WhatsApp](/docs/whatsapp/self-sign-up "Self-Signup Guide for WhatsApp"). If you are an ISV following the [WhatsApp Tech Provider Program](/docs/whatsapp/isv/tech-provider-program "WhatsApp Tech Provider Program"), you'll need to request to have WhatsApp numbers registered by Twilio's Operations team. As part of the onboarding process, either you or Twilio's Operations team will create a WhatsApp Business Account (WABA) and associate it with your Twilio Account SID. Only one WABA is allowed per Twilio Account at this time.

As of January 2023, WhatsApp has imposed new limitations on phone numbers and WABAs:

* Phone Number limits applied across all WABAs per single Meta Business Manager

  + Businesses that don't have a verified Meta Business Manager are allowed a max of 2 phone numbers per Meta Business Manager across all WABAs.
  + Businesses with a verified Meta Business Manager account can have up to 20 phone numbers. An exception for up to 50 phone numbers can be requested by opening a support ticket. Higher limits may be made available with a second appeal and a valid use case justification, at WhatsApp's discretion.
* WABA limits:

  + Businesses with a verified Meta Business Manager can have a max of 20 WABAs across their Meta Business Manager.
  + Businesses that have an Official Business Account (OBA) are allowed up to 1000 WABAs.

Most businesses that onboarded prior to January 2023, and those with higher limits previously, are exempt from these limitations. WhatsApp reserves the right to restrict the numbers and WABAs for any reasons and if they see any evidence of scams or severe spam on an account, at their discretion.

Once your number has been enabled for WhatsApp, it can be used as a WhatsApp Sender. Clicking on a specific Sender takes you to its specific Configuration page. This includes the *Endpoint configuration* section, where you can specify what action Twilio should take when it receives a WhatsApp message at this number. You can configure this sender as part of a [Messaging Service](/docs/messaging/services "Messaging Service") or with an individual [webhook](/docs/glossary/what-is-a-webhook "webhook") URL.

You can also update all your profile details here.

---

## Sending notifications with WhatsApp

WhatsApp requires that business-initiated notifications sent by your application be templated and pre-registered, with the exception of messages sent as a reply to a user-initiated message. (See [Conversational Messaging on WhatsApp](/docs/whatsapp/api#conversational-messaging-on-whatsapp "Conversational Messaging on WhatsApp") for more details).

To manage your own WhatsApp profile, go to [Messaging > Senders > WhatsApp Senders in the Console](/console/sms/whatsapp/senders "Messaging > Senders > WhatsApp Senders in the Console"). There, you can see the list of your WhatsApp-enabled Twilio phone numbers (senders).

To see and manage [templates](/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates "templates") and their approvals, go to [Messaging > Content Template Builder](/docs/console/sms/content-template-builder "Messaging > Content Template Builder").

To learn more, consult our [Guide to Sending WhatsApp Notifications Using Message Templates](/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates "Guide to Sending WhatsApp Notifications Using Message Templates").

---

## Conversational Messaging on WhatsApp

To have 2-way conversations with end users, you need to be able to receive messages from them. Users can send your business messages either directly or in response to a templated notification.

### How to initiate a customer service window

A customer service window begins when a user sends a message to your app. Customer service windows are valid for 24 hours after the most recently received message, during which you can communicate with customers using free-form messages. To send a message outside the customer service window, you must use a pre-approved message template. (See our [Guide to WhatsApp Message Templates](/docs/whatsapp/tutorial/send-whatsapp-notification-messages-templates "Guide to WhatsApp Message Templates")).

### Configuring inbound message webhooks

When customers send you a WhatsApp message, Twilio sends a [webhook](/docs/glossary/what-is-a-webhook "webhook") (a request to a URL that you specify) to your application. You can configure the URL to which Twilio sends a webhook when it receives inbound messages in the Twilio Console:

* on [the Sandbox page](/console/messaging/whatsapp/sandbox "the Sandbox page")
* on the page for [WhatsApp-enabled numbers](/console/messaging/whatsapp/numbers "WhatsApp-enabled numbers")
* under the "**Integration**" section of your settings for a specific Messaging Service (Under the [Messaging Services section of the Console](/console/sms/services "Messaging Services section of the Console"))

### Configuring Fallback URLs for your WhatsApp-enabled Senders

Optionally, you can configure a Fallback URL in the same place that you set your default webhook URL. If a fatal error occurs while making a request to your primary webhook URL, Twilio "falls back" to this secondary *fallback* URL.

When making the request to your fallback URL, Twilio also submits the `ErrorCode` and `ErrorUrl` parameters, indicating the error code of the failure and the URL for which the failure occurred.

|  |  |
| --- | --- |
| Configuring Inbound Message Webhooks for Twilio Sandbox for WhatsApp | Configuring Inbound Message webhooks for your WhatsApp enabled Twilio number |

For details on the data provided in the request that Twilio makes to your application (via the webhook URL), read more about [Twilio's requests to your application](/docs/messaging/twiml#twilios-request-to-your-application "Twilio's requests to your application").

### Receiving a WhatsApp message

The webhook for inbound messages uses the same format as [incoming SMS and MMS messages](/docs/messaging/tutorials/how-to-receive-and-reply "incoming SMS and MMS messages"), with the exception that `To` and `From` addresses will be set to WhatsApp addresses (`whatsapp:<your E.164 number>` and `whatsapp:<User's E.164 phone number>`), respectively.

Incoming messages may include text or media. The `Body` field contains the message text, and the `MediaUrl0` field contains a link to the media file. You can learn how to download incoming media included in a message in the [Receive and Download Images on Incoming MMS Messages tutorial](/docs/messaging/tutorials/how-to-receive-and-download-images-incoming-mms "Receive and Download Images on Incoming MMS Messages tutorial"). Supported media include images (JPG, JPEG, PNG), audio files, and PDF files, with a size limit of 16MB per message.

### Responding to Incoming Messages with TwiML

WhatsApp incoming messages are fully supported by TwiML, allowing you to seamlessly use your existing SMS app with WhatsApp. For more information, check out [Documentation on How to Use TwiML](/docs/messaging/twiml "Documentation on How to Use TwiML").

### Sending a freeform WhatsApp message using the API

Within a WhatsApp session, you can send freeform messages using the Programmable Messaging API. Freeform messages may include text, media and certain rich messages created with [Content Templates](/docs/content "Content Templates").

### Web links in freeform WhatsApp messages

Freeform WhatsApp messages that include web links will display a web page snippet preview when received on the WhatsApp client.

Send an outbound freeform WhatsApp Message

```
1

// Download the helper library from https://www.twilio.com/docs/node/install

2

const twilio = require("twilio"); // Or, for ESM: import twilio from "twilio";

3

4

// Find your Account SID and Auth Token at twilio.com/console

5

// and set the environment variables. See http://twil.io/secure

6

const accountSid = process.env.TWILIO_ACCOUNT_SID;

7

const authToken = process.env.TWILIO_AUTH_TOKEN;

8

const client = twilio(accountSid, authToken);

9

10

async function createMessage() {

11

const message = await client.messages.create({

12

body: "Hello, there!",

13

from: "whatsapp:+14155238886",

14

to: "whatsapp:+15005550006",

15

});

16

17

console.log(message.body);

18

}

19

20

createMessage();
```

### Response

```
1

{

2

"account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

3

"api_version": "2010-04-01",

4

"body": "Hello, there!",

5

"date_created": "Thu, 24 Aug 2023 05:01:45 +0000",

6

"date_sent": "Thu, 24 Aug 2023 05:01:45 +0000",

7

"date_updated": "Thu, 24 Aug 2023 05:01:45 +0000",

8

"direction": "outbound-api",

9

"error_code": null,

10

"error_message": null,

11

"from": "whatsapp:+14155238886",

12

"num_media": "0",

13

"num_segments": "1",

14

"price": null,

15

"price_unit": null,

16

"messaging_service_sid": "MGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

17

"sid": "SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

18

"status": "queued",

19

"subresource_uris": {

20

"media": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Media.json"

21

},

22

"to": "whatsapp:+15005550006",

23

"uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json"

24

}
```

Send a freeform WhatsApp message with media

```
1

// Download the helper library from https://www.twilio.com/docs/node/install

2

const twilio = require("twilio"); // Or, for ESM: import twilio from "twilio";

3

4

// Find your Account SID and Auth Token at twilio.com/console

5

// and set the environment variables. See http://twil.io/secure

6

const accountSid = process.env.TWILIO_ACCOUNT_SID;

7

const authToken = process.env.TWILIO_AUTH_TOKEN;

8

const client = twilio(accountSid, authToken);

9

10

async function createMessage() {

11

const message = await client.messages.create({

12

body: "Here's that picture of an owl you requested.",

13

from: "whatsapp:+14155238886",

14

mediaUrl: ["https://demo.twilio.com/owl.png"],

15

to: "whatsapp:+15017122661",

16

});

17

18

console.log(message.body);

19

}

20

21

createMessage();
```

### Response

```
1

{

2

"account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

3

"api_version": "2010-04-01",

4

"body": "Here's that picture of an owl you requested.",

5

"date_created": "Thu, 24 Aug 2023 05:01:45 +0000",

6

"date_sent": "Thu, 24 Aug 2023 05:01:45 +0000",

7

"date_updated": "Thu, 24 Aug 2023 05:01:45 +0000",

8

"direction": "outbound-api",

9

"error_code": null,

10

"error_message": null,

11

"from": "whatsapp:+14155238886",

12

"num_media": "0",

13

"num_segments": "1",

14

"price": null,

15

"price_unit": null,

16

"messaging_service_sid": "MGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

17

"sid": "SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

18

"status": "queued",

19

"subresource_uris": {

20

"media": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Media.json"

21

},

22

"to": "whatsapp:+15017122661",

23

"uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json"

24

}
```

---

## Monitor the status of your WhatsApp outbound message

To receive real-time status updates for outbound messages, you can choose to **set a Status Callback URL**. Twilio sends a request to this URL each time your message status changes to one of the transition values in the [Message Status Callback Event Flow diagram](/docs/messaging/guides/outbound-message-status-in-status-callbacks#message-status-changes-triggering-status-callback-requests "Message Status Callback Event Flow diagram").

You can set the Status Callback URL in the Console, or when you send an individual outbound message, by including the StatusCallback parameter. You can set the status callback URL in different parts of the Twilio Console depending on your messaging setup:

* For the [WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1 "WhatsApp Sandbox") or an [individual WhatsApp Sender](https://www.twilio.com/console/sms/whatsapp/senders "individual WhatsApp Sender") -read [WhatsApp and other messaging channels](/docs/messaging/guides/track-outbound-message-status#whatsapp-and-other-messaging-channels "WhatsApp and other messaging channels") for additional properties that Twilio sends to your callback URL
* For a [Messaging Service](https://www.twilio.com/console/sms/services "Messaging Service") (under the **Integration** settings for a specific Messaging Service) - read the [status callback with a Messaging service guide](/docs/messaging/guides/track-outbound-message-status#scenario-2-messaging-service-used "status callback with a Messaging service guide") for configuration options

When you set the Status Callback URL, Twilio sends a `POST` request to that URL, including the message `sid` (the Message's Unique identifier) and other standard request parameters as well as a `status` and an associated `error_code` if any. Refer to the [API Reference for the Message Resource](/docs/messaging/api/message-resource "API Reference for the Message Resource") for a list of parameters that Twilio sends to your callback URL.

Send a WhatsApp Message and specify a StatusCallback URL

```
1

// Download the helper library from https://www.twilio.com/docs/node/install

2

const twilio = require("twilio"); // Or, for ESM: import twilio from "twilio";

3

4

// Find your Account SID and Auth Token at twilio.com/console

5

// and set the environment variables. See http://twil.io/secure

6

const accountSid = process.env.TWILIO_ACCOUNT_SID;

7

const authToken = process.env.TWILIO_AUTH_TOKEN;

8

const client = twilio(accountSid, authToken);

9

10

async function createMessage() {

11

const message = await client.messages.create({

12

body: "Hey, I just met you, and this is crazy...",

13

from: "whatsapp:+14155238886",

14

statusCallback: "http://postb.in/1234abcd",

15

to: "whatsapp:+15005550006",

16

});

17

18

console.log(message.body);

19

}

20

21

createMessage();
```

### Response

```
1

{

2

"account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

3

"api_version": "2010-04-01",

4

"body": "Hey, I just met you, and this is crazy...",

5

"date_created": "Thu, 24 Aug 2023 05:01:45 +0000",

6

"date_sent": "Thu, 24 Aug 2023 05:01:45 +0000",

7

"date_updated": "Thu, 24 Aug 2023 05:01:45 +0000",

8

"direction": "outbound-api",

9

"error_code": null,

10

"error_message": null,

11

"from": "whatsapp:+14155238886",

12

"num_media": "0",

13

"num_segments": "1",

14

"price": null,

15

"price_unit": null,

16

"messaging_service_sid": "MGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

17

"sid": "SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",

18

"status": "queued",

19

"subresource_uris": {

20

"media": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Media.json"

21

},

22

"to": "whatsapp:+15005550006",

23

"uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json"

24

}
```

---

## 4. SMS developer quickstart

Page toolsOn this page

Looking for more inspiration?Visit the

# SMS developer quickstart

---

In this quickstart, you'll build your first application to programmatically send and receive text messages with [Twilio Programmable Messaging](/docs/messaging "Twilio Programmable Messaging"). This quickstart uses the Programmable Messaging REST API, the Twilio SDKs, and the Twilio Virtual Phone.

For a no-code quickstart, see [No-code programmable messaging quickstart with Twilio Studio](/docs/messaging/quickstart/no-code-sms-studio-quickstart "No-code programmable messaging quickstart with Twilio Studio").

---

## Complete the prerequisites

Select your programming language and complete the prerequisites:

PythonNode.jsPHPC# (.NET Framework)C# (.NET Core)JavaGoRuby

* [Install Python](https://www.python.org/downloads/ "Install Python").
* [Install and set up ngrok](https://ngrok.com/docs/getting-started/ "Install and set up ngrok").
* Install [Flask](http://flask.pocoo.org/ "Flask") and [Twilio's Python SDK](https://github.com/twilio/twilio-python "Twilio's Python SDK"). To install using [pip](https://pip.pypa.io/en/latest/ "pip"), run:

  ```
  pip install flask twilio
  ```

---

## Sign up for Twilio and get a phone number

1. [Sign up for Twilio](https://www.twilio.com/try-twilio "Sign up for Twilio"). When prompted to select a plan, click **Continue with trial**.
2. To get a phone that has SMS capabilities, do either of the following:
   * In the **Account Dashboard**, click **Get a phone number**.
   * In the navigation menu, go to **Phone Numbers > Manage > Buy a number**.
3. In the **Account Dashboard**, copy your **Account SID** and **Auth Token** and paste them in a temporary local file for use later in this quickstart.

---

## Open the Twilio Virtual Phone

The [Twilio Virtual Phone](/docs/messaging/guides/guide-to-using-the-twilio-virtual-phone "Twilio Virtual Phone") lets you try Twilio quickly regardless of your country's regulations for messaging mobile handsets. To message a mobile handset, see [Send SMS and MMS messages](/docs/messaging/tutorials/how-to-send-sms-messages "Send SMS and MMS messages").

1. Open the [Send an SMS page in the Twilio Console](https://console.twilio.com/us1/develop/sms/try-it-out/send-an-sms "Send an SMS page in the Twilio Console").
2. On the **Send to Virtual Phone** tab, select the number that Twilio gave you from the **Phone number** list.
3. Click **Virtual Phone**. Messages you send with your application display on the Virtual Phone.

---

## Send an outbound SMS message

Follow these steps to send an SMS message from your Twilio phone number.

PythonNode.jsPHPC# (.NET Framework)C# (.NET Core)JavaGoRuby

1. Create and open a new file called `send_sms.py` anywhere on your machine and paste in the following code:

   Send an SMS Using Twilio with Python

   ```
   1

   # Download the helper library from https://www.twilio.com/docs/python/install

   2

   import os

   3

   from twilio.rest import Client

   4

   5

   # Find your Account SID and Auth Token at twilio.com/console

   6

   # and set the environment variables. See http://twil.io/secure

   7

   account_sid = os.environ["TWILIO_ACCOUNT_SID"]

   8

   auth_token = os.environ["TWILIO_AUTH_TOKEN"]

   9

   client = Client(account_sid, auth_token)

   10

   11

   message = client.messages.create(

   12

   body="Join Earth's mightiest heroes. Like Kevin Bacon.",

   13

   from_="+15017122661",

   14

   to="+15558675310",

   15

   )

   16

   17

   print(message.body)
   ```
2. In the `send_sms.py` file, replace the values for `account_sid` and `auth_token` with your Account SID and Auth Token surrounded by quotation marks.

   (error)

   ## Don't include credentials in production apps

   This quickstart hardcodes your credentials for faster setup. To keep credentials secret and control access when you deploy to production, use environment variables and [API keys](/docs/iam/api-keys "API keys").

   ```
   1

   // Using environment variables (recommended for production)

   2

   public static final String ACCOUNT_SID = System.getenv("TWILIO_ACCOUNT_SID");

   3

   public static final String AUTH_TOKEN = System.getenv("TWILIO_AUTH_TOKEN");

   4

   5

   // Initialize Twilio with environment variables

   6

   Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
   ```

   **To set environment variables:**

   **On macOS/Linux:**

   ```
   1

   export TWILIO_ACCOUNT_SID=your_account_sid_here

   2

   export TWILIO_AUTH_TOKEN=your_auth_token_here
   ```

   **On Windows (Command Prompt):**

   ```
   1

   set TWILIO_ACCOUNT_SID=your_account_sid_here

   2

   set TWILIO_AUTH_TOKEN=your_auth_token_here
   ```

   **On Windows (PowerShell):**

   ```
   1

   $env:TWILIO_ACCOUNT_SID="your_account_sid_here"

   2

   $env:TWILIO_AUTH_TOKEN="your_auth_token_here"
   ```
3. Replace the value for `from` with the phone number that Twilio gave you in [E.164 format](/docs/glossary/what-e164 "E.164 format").
4. Replace the value for `to` with the Twilio Virtual Phone number (`+18777804236`).
5. Save your changes and run this command from your terminal in the directory that contains `send_sms.py`:

   ```
   python send_sms.py
   ```

   After a few moments, you receive an SMS from your Twilio number on the Twilio Virtual Phone.

---

## Receive and reply to an inbound SMS message

Follow these steps to reply to an SMS message sent to your Twilio phone number.

PythonNode.jsPHPC# (.NET Framework)C# (.NET Core)JavaGoRuby

1. Create and open a new file called `reply_sms.py` anywhere on your machine and paste in the following code:

   ```
   1

   from flask import Flask, request, Response

   2

   from twilio.twiml.messaging_response import MessagingResponse

   3

   4

   app = Flask(__name__)

   5

   6

   @app.route("/reply_sms", methods=['POST'])

   7

   def reply_sms():

   8

   # Create a new Twilio MessagingResponse

   9

   resp = MessagingResponse()

   10

   resp.message("The Robots are coming! Head for the hills!")

   11

   12

   # Return the TwiML (as XML) response

   13

   return Response(str(resp), mimetype='text/xml')

   14

   15

   if 

   16

   app.run(port=3000)
   ```

   Save the file.
2. In a new terminal window, run the following command to start the Python development server on port 3000:

   ```
   python reply_sms.py
   ```
3. In a new terminal window, run the following command to start [ngrok](https://ngrok.com/docs/what-is-ngrok/ "ngrok") and create a tunnel to your localhost:

   ```
   ngrok http 3000
   ```

   (warning)

   ## Warning

   Use ngrok only for testing because it creates a temporary URL that exposes your local development machine to the internet. Host your application with a cloud provider or your public server when you deploy to production.
4. Set up a webhook that triggers when your Twilio phone number receives an SMS message:

   1. Open the [Active Numbers page in the Twilio Console](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming "Active Numbers page in the Twilio Console").
   2. Click your Twilio phone number.
   3. In the **Messaging Configuration** section, in the **URL** field for **A message comes in**, enter the temporary forwarding URL from your ngrok console with `/reply_sms` appended to the end.

      For example, if your ngrok console shows `Forwarding https://1aaa-123-45-678-910.ngrok-free.app`, enter `https://1aaa-123-45-678-910.ngrok-free.app/reply_sms`.
   4. Click **Save configuration**.
5. With the Python development server and ngrok running, send an SMS to your Twilio phone number:

   1. Enter a message in the **Click here to reply** field at the bottom of the Twilio Virtual Phone.
   2. Click the send icon.

   An HTTP request shows in your ngrok console, and you get the response back as an SMS on the Twilio Virtual Phone.

---

## Next steps

* [Upgrade your account in the Twilio Console](https://console.twilio.com/account/upgrade "Upgrade your account in the Twilio Console").
* Learn about [toll-free verification](/docs/messaging/compliance/toll-free/console-onboarding "toll-free verification") and [A2P 10DLC registration](/docs/messaging/compliance/a2p-10dlc "A2P 10DLC registration"). Regulations require:
  + Toll-free verification to send SMS messages from toll-free numbers to mobile phones in the US and Canada.
  + A2P 10DLC registration to send SMS messages from local numbers to mobile phones in the US.
* Browse the following developer resources:
  + [Messaging API Reference](/docs/messaging/api "Messaging API Reference")
  + [TwiML documentation](/docs/messaging/twiml "TwiML documentation")

---

## Bibliography

1. [Messaging API Overview](https://www.twilio.com/docs/messaging/api)
2. [WhatsApp Business Platform with Twilio](https://www.twilio.com/docs/whatsapp)
3. [Overview of the WhatsApp Business Platform with Twilio](https://www.twilio.com/docs/whatsapp/api)
4. [SMS developer quickstart](https://www.twilio.com/docs/messaging/quickstart/python)