Getting Started - Argo CD - Declarative GitOps CD for Kubernetes

:root{--md-text-font-family:"Work Sans";--md-code-font-family:""}

function gtag(){dataLayer.push(arguments)}window.dataLayer=window.dataLayer||[],gtag("js",new Date),gtag("config","G-5Z1VTPDL73"),document.addEventListener("DOMContentLoaded",function(){"undefined"!=typeof location$&&location$.subscribe(function(t){gtag("config","G-5Z1VTPDL73",{page\_path:t.pathname})})})

function \_\_prefix(e){return new URL("..",location).pathname+"."+e}function \_\_get(e,t=localStorage){return JSON.parse(t.getItem(\_\_prefix(e)))}
var palette=\_\_get("\_\_palette");if(null!==palette&&"object"==typeof palette.color)for(var key in palette.color)document.body.setAttribute("data-md-color-"+key,palette.color[key])

[Skip to content](#getting-started)

Argo CD - Declarative GitOps CD for Kubernetes

Getting Started

Initializing search

[GitHub](https://github.com/argoproj/argo-cd "Go to repository")

Argo CD - Declarative GitOps CD for Kubernetes

[GitHub](https://github.com/argoproj/argo-cd "Go to repository")

* [Overview](..)
* [Understand The Basics](../understand_the_basics/)
* [Core Concepts](../core_concepts/)
* Getting Started
  [Getting Started](./)

  Table of contents
  + [Requirements](#requirements)
  + [1. Install Argo CD](#1-install-argo-cd)
  + [2. Download Argo CD CLI](#2-download-argo-cd-cli)
  + [3. Access Argo CD](#3-access-argo-cd)

    - [Service Type Load Balancer](#service-type-load-balancer)
    - [Ingress](#ingress)
    - [Port Forwarding](#port-forwarding)
  + [4. Login Using The CLI](#4-login-using-the-cli)
  + [5. Register A Cluster To Deploy Apps To (Optional)](#5-register-a-cluster-to-deploy-apps-to-optional)
  + [6. Create An Application From A Git Repository](#6-create-an-application-from-a-git-repository)

    - [Creating Apps Via CLI](#creating-apps-via-cli)
    - [Creating Apps Via UI](#creating-apps-via-ui)
  + [7. Sync (Deploy) The Application](#7-sync-deploy-the-application)

    - [Syncing via CLI](#syncing-via-cli)
    - [Syncing via UI](#syncing-via-ui)
* Operator Manual

  Operator Manual
  + [Overview](../operator-manual/)
  + [Architectural Overview](../operator-manual/architecture/)
  + [Installation](../operator-manual/installation/)
  + [Feature Maturity](../operator-manual/feature-maturity/)
  + [Argo CD Core](../operator-manual/core/)
  + [Declarative Setup](../operator-manual/declarative-setup/)
  + [Applications in any namespace](../operator-manual/app-any-namespace/)
  + [Ingress Configuration](../operator-manual/ingress/)
  + High Availability

    High Availability
    - [Overview](../operator-manual/high_availability/)
    - [Dynamic Cluster Distribution](../operator-manual/dynamic-cluster-distribution/)
  + User Management

    User Management
    - [Overview](../operator-manual/user-management/)
    - [Auth0](../operator-manual/user-management/auth0/)
    - [Microsoft](../operator-manual/user-management/microsoft/)
    - [Okta](../operator-manual/user-management/okta/)
    - [OneLogin](../operator-manual/user-management/onelogin/)
    - [Keycloak](../operator-manual/user-management/keycloak/)
    - [OpenUnison](../operator-manual/user-management/openunison/)
    - [GitHub Actions](../operator-manual/user-management/github-actions/)
    - [Google](../operator-manual/user-management/google/)
    - [Zitadel](../operator-manual/user-management/zitadel/)
    - [Identity Center (AWS SSO)](../operator-manual/user-management/identity-center/)
    - [RBAC Configuration](../operator-manual/rbac/)
  + Security

    Security
    - [Overview](../operator-manual/security/)
    - [Snyk Scans](../snyk/)
    - [Verification of Argo CD Artifacts](../operator-manual/signed-release-assets/)
  + [TLS configuration](../operator-manual/tls/)
  + [Cluster Management](../operator-manual/cluster-management/)
  + [Cluster Bootstrapping](../operator-manual/cluster-bootstrapping/)
  + [Secret Management](../operator-manual/secret-management/)
  + [Disaster Recovery](../operator-manual/disaster_recovery/)
  + [Reconcile Optimization](../operator-manual/reconcile/)
  + [Git Webhook Configuration](../operator-manual/webhook/)
  + [Resource Health](../operator-manual/health/)
  + [Resource Actions](../operator-manual/resource_actions/)
  + [Custom Tooling](../operator-manual/custom_tools/)
  + [Custom Styles](../operator-manual/custom-styles/)
  + [UI Customization](../operator-manual/ui-customization/)
  + [Metrics](../operator-manual/metrics/)
  + [Web-based Terminal](../operator-manual/web_based_terminal/)
  + [Config Management Plugins](../operator-manual/config-management-plugins/)
  + [Deep Links](../operator-manual/deep_links/)
  + [Git Configuration](../operator-manual/git_configuration/)
  + [Managed By URL Annotation](../operator-manual/managed-by-url/)
  + Notifications

    Notifications
    - [Overview](../operator-manual/notifications/)
    - [Triggers](../operator-manual/notifications/triggers/)
    - [Templates](../operator-manual/notifications/templates/)
    - [Functions](../operator-manual/notifications/functions/)
    - [Triggers and Templates Catalog](../operator-manual/notifications/catalog/)
    - [Monitoring](../operator-manual/notifications/monitoring/)
    - [Subscriptions](../operator-manual/notifications/subscriptions/)
    - [Troubleshooting](../operator-manual/notifications/troubleshooting/)
    - [Troubleshooting commands](../operator-manual/notifications/troubleshooting-commands/)
    - [Troubleshooting errors](../operator-manual/notifications/troubleshooting-errors/)
    - [Examples](../operator-manual/notifications/examples/)
    - Notification Services

      Notification Services
      * [Alertmanager](../operator-manual/notifications/services/alertmanager/)
      * [AWS SQS](../operator-manual/notifications/services/awssqs/)
      * [Email](../operator-manual/notifications/services/email/)
      * [GitHub](../operator-manual/notifications/services/github/)
      * [Google Chat](../operator-manual/notifications/services/googlechat/)
      * [Grafana](../operator-manual/notifications/services/grafana/)
      * [Mattermost](../operator-manual/notifications/services/mattermost/)
      * [NewRelic](../operator-manual/notifications/services/newrelic/)
      * [Opsgenie](../operator-manual/notifications/services/opsgenie/)
      * [Overview](../operator-manual/notifications/services/overview/)
      * [PagerDuty](../operator-manual/notifications/services/pagerduty/)
      * [PagerDuty V2](../operator-manual/notifications/services/pagerduty_v2/)
      * [Pushover](../operator-manual/notifications/services/pushover/)
      * [Rocket.Chat](../operator-manual/notifications/services/rocketchat/)
      * [Slack](../operator-manual/notifications/services/slack/)
      * [Teams Workflows](../operator-manual/notifications/services/teams-workflows/)
      * [Teams (Office 365 Connectors)](../operator-manual/notifications/services/teams/)
      * [Telegram](../operator-manual/notifications/services/telegram/)
      * [Webex Teams](../operator-manual/notifications/services/webex/)
      * [Webhook](../operator-manual/notifications/services/webhook/)
  + [Troubleshooting Tools](../operator-manual/troubleshooting/)
  + ApplicationSet

    ApplicationSet
    - [Introduction](../operator-manual/applicationset/)
    - [Installations](../operator-manual/applicationset/Getting-Started/)
    - [Use Cases](../operator-manual/applicationset/Use-Cases/)
    - [Security](../operator-manual/applicationset/Security/)
    - [How ApplicationSet controller interacts with Argo CD](../operator-manual/applicationset/Argo-CD-Integration/)
    - Generators

      Generators
      * [Generators](../operator-manual/applicationset/Generators/)
      * [List Generator](../operator-manual/applicationset/Generators-List/)
      * [Cluster Generator](../operator-manual/applicationset/Generators-Cluster/)
      * [Git Generator](../operator-manual/applicationset/Generators-Git/)
      * [Matrix Generator](../operator-manual/applicationset/Generators-Matrix/)
      * [Merge Generator](../operator-manual/applicationset/Generators-Merge/)
      * [SCM Provider Generator](../operator-manual/applicationset/Generators-SCM-Provider/)
      * [Cluster Decision Resource Generator](../operator-manual/applicationset/Generators-Cluster-Decision-Resource/)
      * [Pull Request Generator](../operator-manual/applicationset/Generators-Pull-Request/)
      * [Post Selector all generators](../operator-manual/applicationset/Generators-Post-Selector/)
      * [Plugin Generator](../operator-manual/applicationset/Generators-Plugin/)
    - Template fields

      Template fields
      * [Templates](../operator-manual/applicationset/Template/)
      * [Go Template](../operator-manual/applicationset/GoTemplate/)
    - [Controlling Resource Modification](../operator-manual/applicationset/Controlling-Resource-Modification/)
    - [Application Pruning & Resource Deletion](../operator-manual/applicationset/Application-Deletion/)
    - [Progressive Syncs](../operator-manual/applicationset/Progressive-Syncs/)
    - [Git File Generator Globbing](../operator-manual/applicationset/Generators-Git-File-Globbing/)
    - [ApplicationSet Specification Reference](../operator-manual/applicationset/applicationset-specification/)
    - [ApplicationSet in any namespace](../operator-manual/applicationset/Appset-Any-Namespace/)
  + Server Configuration Parameters

    Server Configuration Parameters
    - [argocd-server Command Reference](../operator-manual/server-commands/argocd-server/)
    - [argocd-application-controller Command Reference](../operator-manual/server-commands/argocd-application-controller/)
    - [argocd-repo-server Command Reference](../operator-manual/server-commands/argocd-repo-server/)
    - [argocd-dex Command Reference](../operator-manual/server-commands/argocd-dex/)
    - [Additional configuration method](../operator-manual/server-commands/additional-configuration-method/)
  + Upgrading

    Upgrading
    - [Overview](../operator-manual/upgrading/overview/)
    - [v3.2 to 3.3](../operator-manual/upgrading/3.2-3.3/)
    - [v3.1 to 3.2](../operator-manual/upgrading/3.1-3.2/)
    - [v3.0 to 3.1](../operator-manual/upgrading/3.0-3.1/)
    - [v2.14 to 3.0](../operator-manual/upgrading/2.14-3.0/)
    - [v2.13 to 2.14](../operator-manual/upgrading/2.13-2.14/)
    - [v2.12 to 2.13](../operator-manual/upgrading/2.12-2.13/)
    - [v2.11 to 2.12](../operator-manual/upgrading/2.11-2.12/)
    - [v2.10 to 2.11](../operator-manual/upgrading/2.10-2.11/)
    - [v2.9 to 2.10](../operator-manual/upgrading/2.9-2.10/)
    - [v2.8 to 2.9](../operator-manual/upgrading/2.8-2.9/)
    - [v2.7 to 2.8](../operator-manual/upgrading/2.7-2.8/)
    - [v2.6 to 2.7](../operator-manual/upgrading/2.6-2.7/)
    - [v2.5 to 2.6](../operator-manual/upgrading/2.5-2.6/)
    - [v2.4 to 2.5](../operator-manual/upgrading/2.4-2.5/)
    - [v2.3 to 2.4](../operator-manual/upgrading/2.3-2.4/)
    - [v2.2 to 2.3](../operator-manual/upgrading/2.2-2.3/)
    - [v2.1 to 2.2](../operator-manual/upgrading/2.1-2.2/)
    - [v2.0 to 2.1](../operator-manual/upgrading/2.0-2.1/)
    - [v1.8 to 2.0](../operator-manual/upgrading/1.8-2.0/)
    - [v1.7 to 1.8](../operator-manual/upgrading/1.7-1.8/)
    - [v1.6 to 1.7](../operator-manual/upgrading/1.6-1.7/)
    - [v1.5 to 1.6](../operator-manual/upgrading/1.5-1.6/)
    - [v1.4 to 1.5](../operator-manual/upgrading/1.4-1.5/)
    - [v1.3 to 1.4](../operator-manual/upgrading/1.3-1.4/)
    - [v1.2 to 1.3](../operator-manual/upgrading/1.2-1.3/)
    - [v1.1 to 1.2](../operator-manual/upgrading/1.1-1.2/)
    - [v1.0 to 1.1](../operator-manual/upgrading/1.0-1.1/)
  + [Project Specification Reference](../operator-manual/project-specification/)
* User Guide

  User Guide
  + [Overview](../user-guide/)
  + [Tools](../user-guide/application_sources/)
  + [Kustomize](../user-guide/kustomize/)
  + [Helm](../user-guide/helm/)
  + [OCI](../user-guide/oci/)
  + [Importing Argo CD go packages](../user-guide/import/)
  + [Jsonnet](../user-guide/jsonnet/)
  + [Directory](../user-guide/directory/)
  + [Tool Detection](../user-guide/tool_detection/)
  + [Projects](../user-guide/projects/)
  + [Private Repositories](../user-guide/private-repositories/)
  + [Plugins](../user-guide/plugins/)
  + [Multiple Sources for an Application](../user-guide/multiple_sources/)
  + [GnuPG verification](../user-guide/gpg-verification/)
  + [Automated Sync Policy](../user-guide/auto_sync/)
  + Diffing

    Diffing
    - [Diff Strategies](../user-guide/diff-strategies/)
    - [Diff Customization](../user-guide/diffing/)
  + [Orphaned Resources Monitoring](../user-guide/orphaned-resources/)
  + [Compare Options](../user-guide/compare-options/)
  + [Sync Options](../user-guide/sync-options/)
  + [Parameter Overrides](../user-guide/parameters/)
  + [Environment Variables](../user-guide/environment-variables/)
  + [Build Environment](../user-guide/build-environment/)
  + [Tracking and Deployment Strategies](../user-guide/tracking_strategies/)
  + [Resource Tracking](../user-guide/resource_tracking/)
  + [Resource hooks](../user-guide/resource_hooks/)
  + [Selective Sync](../user-guide/selective_sync/)
  + [Sync Phases and Waves](../user-guide/sync-waves/)
  + [Sync Windows](../user-guide/sync_windows/)
  + [Sync Applications with Kubectl](../user-guide/sync-kubectl/)
  + [Skip Application Reconcile](../user-guide/skip_reconcile/)
  + [Generating Applications with ApplicationSet](../user-guide/application-set/)
  + [Automation from CI Pipelines](../user-guide/ci_automation/)
  + [App Deletion](../user-guide/app_deletion/)
  + [Best Practices](../user-guide/best_practices/)
  + [Status Badge](../user-guide/status-badge/)
  + [External URL Links](../user-guide/external-url/)
  + [Add extra Application info](../user-guide/extra_info/)
  + [Notification subscriptions](../user-guide/subscriptions/)
  + [Annotations and Labels used by Argo CD](../user-guide/annotations-and-labels/)
  + [Command Reference](../user-guide/commands/argocd/)
  + [Application Specification Reference](../user-guide/application-specification/)
* Developer Guide

  Developer Guide
  + [Overview](../developer-guide/)
  + [Development Environment](../developer-guide/development-environment/)
  + [Development Cycle](../developer-guide/development-cycle/)
  + [Submit Your PR](../developer-guide/submit-your-pr/)
  + Architecture

    Architecture
    - [Authentication and Authorization](../developer-guide/architecture/authz-authn/)
    - [Component Architecture](../developer-guide/architecture/components/)
  + [Code Contribution Guide](../developer-guide/code-contributions/)
  + [Toolchain Guide](../developer-guide/toolchain-guide/)
  + [MacOS users](../developer-guide/mac-users/)
  + [Release Process And Cadence](../developer-guide/release-process-and-cadence/)
  + [Running Argo CD locally](../developer-guide/running-locally/)
  + [Debugging a local Argo CD instance](../developer-guide/debugging-locally/)
  + [Debugging a Remote ArgoCD Environment](../developer-guide/debugging-remote-environment/)
  + [API Docs](../developer-guide/api-docs/)
  + [E2E Tests](../developer-guide/test-e2e/)
  + [Managing Dependencies](../developer-guide/dependencies/)
  + [Continuous Integration (CI)](../developer-guide/ci/)
  + [Releasing](../developer-guide/releasing/)
  + [Documentation Site](../developer-guide/docs-site/)
  + [Static Code Analysis](../developer-guide/static-code-analysis/)
  + Extensions

    Extensions
    - [UI Extensions](../developer-guide/extensions/ui-extensions/)
    - [Proxy Extensions](../developer-guide/extensions/proxy-extensions/)
  + [Contribution FAQ](../developer-guide/faq/)
  + [Tilt Development](../developer-guide/tilt/)
  + [Custom resource icons](../developer-guide/custom-resource-icons/)
  + [Maintaining Internal Argo CD Forks](../developer-guide/maintaining-internal-argo-cd-forks/)
* [FAQ](../faq/)
* [Security Considerations](../security_considerations/)
* [Support](../SUPPORT/)
* [Roadmap](../roadmap/)
* [Releases ⧉](https://github.com/argoproj/argo-cd/releases)
* [Blog ⧉](https://blog.argoproj.io/)

Table of contents

* [Requirements](#requirements)
* [1. Install Argo CD](#1-install-argo-cd)
* [2. Download Argo CD CLI](#2-download-argo-cd-cli)
* [3. Access Argo CD](#3-access-argo-cd)

  + [Service Type Load Balancer](#service-type-load-balancer)
  + [Ingress](#ingress)
  + [Port Forwarding](#port-forwarding)
* [4. Login Using The CLI](#4-login-using-the-cli)
* [5. Register A Cluster To Deploy Apps To (Optional)](#5-register-a-cluster-to-deploy-apps-to-optional)
* [6. Create An Application From A Git Repository](#6-create-an-application-from-a-git-repository)

  + [Creating Apps Via CLI](#creating-apps-via-cli)
  + [Creating Apps Via UI](#creating-apps-via-ui)
* [7. Sync (Deploy) The Application](#7-sync-deploy-the-application)

  + [Syncing via CLI](#syncing-via-cli)
  + [Syncing via UI](#syncing-via-ui)

# Getting Started[¶](#getting-started "Permanent link")

Tip

This guide assumes you have a grounding in the tools that Argo CD is based on. Please read [understanding the basics](../understand_the_basics/) to learn about these tools.

## Requirements[¶](#requirements "Permanent link")

* Installed [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) command-line tool.
* Have a [kubeconfig](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) file (default location is `~/.kube/config`).
* CoreDNS. Can be enabled for microk8s by `microk8s enable dns && microk8s stop && microk8s start`

## 1. Install Argo CD[¶](#1-install-argo-cd "Permanent link")

```
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

This will create a new `argocd` namespace where all Argo CD services and application resources will reside. It will also install Argo CD by applying the official manifests from the stable branch. Using a pinned version (like `v3.2.0`) is recommended for production.

Note

**Why `--server-side --force-conflicts`?**

The `--server-side` flag is required because some Argo CD CRDs (like ApplicationSet) exceed the 262KB annotation size limit imposed by client-side `kubectl apply`. Server-side apply avoids this limitation by not storing the `last-applied-configuration` annotation.

The `--force-conflicts` flag allows the apply operation to take ownership of fields that may have been previously managed by other tools (such as Helm or a previous `kubectl apply`). This is safe for fresh installs and necessary for upgrades. Note that any custom modifications you've made to fields that are defined in the Argo CD manifests (like `affinity`, `env`, or `probes`) will be overwritten. However, fields not specified in the manifests (like `resources` limits/requests or `tolerations`) will be preserved.

Warning

The installation manifests include `ClusterRoleBinding` resources that reference `argocd` namespace. If you are installing Argo CD into a different
namespace then make sure to update the namespace reference.

Tip

If you are not interested in UI, SSO, and multi-cluster features, then you can install only the [core](../operator-manual/core/#installing) Argo CD components.

This default installation will have a self-signed certificate and cannot be accessed without a bit of extra work.
Do one of:

* Follow the [instructions to configure a certificate](../operator-manual/tls/) (and ensure that the client OS trusts it).
* Configure the client OS to trust the self signed certificate.
* Use the --insecure flag on all Argo CD CLI operations in this guide.

Note

Default namespace for `kubectl` config must be set to `argocd`.
This is only needed for the following commands since the previous commands have -n argocd already:

```
kubectl config set-context --current --namespace=argocd
```

Use `argocd login --core` to [configure](../user-guide/commands/argocd_login/) CLI access and skip steps 3-5.

Note

This default installation for Redis is using password authentication. The Redis password is stored in Kubernetes secret `argocd-redis` with key `auth` in the namespace where Argo CD is installed.

If you are running Argo CD on Docker Desktop or another local Kubernetes environment, refer to the [Running Argo CD Locally](../developer-guide/running-locally/) guide for the full setup instructions and configuration steps tailored for local clusters.

## 2. Download Argo CD CLI[¶](#2-download-argo-cd-cli "Permanent link")

Download the latest Argo CD version from <https://github.com/argoproj/argo-cd/releases/latest>. More detailed installation instructions can be found via the [CLI installation documentation](../cli_installation/).

Also available in Mac, Linux and WSL Homebrew:

```
brew install argocd
```

## 3. Access Argo CD[¶](#3-access-argo-cd "Permanent link")

By default, Argo CD isn’t exposed outside the cluster. To access Argo CD from your browser or CLI, use one of the following methods:

### Service Type Load Balancer[¶](#service-type-load-balancer "Permanent link")

Change the argocd-server service type to `LoadBalancer`:

```
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

After a short wait, your cloud provider will assign an external IP address to the service. You can retrieve this IP with:

```
kubectl get svc argocd-server -n argocd -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### Ingress[¶](#ingress "Permanent link")

Follow the [ingress documentation](../operator-manual/ingress/) on how to configure Argo CD with ingress.

### Port Forwarding[¶](#port-forwarding "Permanent link")

Kubectl port-forwarding can also be used to connect to the API server without exposing the service.

```
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

The API server can then be accessed using https://localhost:8080

## 4. Login Using The CLI[¶](#4-login-using-the-cli "Permanent link")

The initial password for the `admin` account is auto-generated and stored as
clear text in the field `password` in a secret named `argocd-initial-admin-secret`
in your Argo CD installation namespace. You can simply retrieve this password
using the `argocd` CLI:

```
argocd admin initial-password -n argocd
```

Warning

You should delete the `argocd-initial-admin-secret` from the Argo CD
namespace once you changed the password. The secret serves no other
purpose than to store the initially generated password in clear and can
safely be deleted at any time. It will be re-created on demand by Argo CD
if a new admin password must be re-generated.

Using the username `admin` and the password from above, login to Argo CD's IP or hostname:

```
argocd login <ARGOCD_SERVER>
```

Note

The CLI environment must be able to communicate with the Argo CD API server. If it isn't directly accessible as described above in step 3, you can tell the CLI to access it using port forwarding through one of these mechanisms: 1) add `--port-forward-namespace argocd` flag to every CLI command; or 2) set `ARGOCD_OPTS` environment variable: `export ARGOCD_OPTS='--port-forward-namespace argocd'`.

Change the password using the command:

```
argocd account update-password
```

## 5. Register A Cluster To Deploy Apps To (Optional)[¶](#5-register-a-cluster-to-deploy-apps-to-optional "Permanent link")

This step registers a cluster's credentials to Argo CD, and is only necessary when deploying to
an external cluster. When deploying internally (to the same cluster that Argo CD is running in),
https://kubernetes.default.svc should be used as the application's K8s API server address.

First list all clusters contexts in your current kubeconfig:

```
kubectl config get-contexts -o name
```

Choose a context name from the list and supply it to `argocd cluster add CONTEXTNAME`. For example,
for docker-desktop context, run:

```
argocd cluster add docker-desktop
```

The above command installs a ServiceAccount (`argocd-manager`), into the kube-system namespace of
that kubectl context, and binds the service account to an admin-level ClusterRole. Argo CD uses this
service account token to perform its management tasks (i.e. deploy/monitoring).

Note

The rules of the `argocd-manager-role` role can be modified such that it only has `create`, `update`, `patch`, `delete` privileges to a limited set of namespaces, groups, kinds.
However `get`, `list`, `watch` privileges are required at the cluster-scope for Argo CD to function.

## 6. Create An Application From A Git Repository[¶](#6-create-an-application-from-a-git-repository "Permanent link")

An example repository containing a guestbook application is available at
<https://github.com/argoproj/argocd-example-apps.git> to demonstrate how Argo CD works.

Note

Note: The following example application may only be compatible with AMD64 architecture. If you are running on a different architecture (such as ARM64 or ARMv7), you may encounter issues with dependencies or container images that are not built for your platform. Consider verifying the compatibility of the application or building architecture-specific images if necessary.

### Creating Apps Via CLI[¶](#creating-apps-via-cli "Permanent link")

First we need to set the current namespace to argocd running the following command:

```
kubectl config set-context --current --namespace=argocd
```

Create the example guestbook application with the following command:

```
argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
```

### Creating Apps Via UI[¶](#creating-apps-via-ui "Permanent link")

Open a browser to the Argo CD external UI, and login by visiting the IP/hostname in a browser and use the credentials set in step 4 or locally as explained in [Try Argo CD Locally](../try_argo_cd_locally/).

After logging in, click the **+ New App** button as shown below:

Give your app the name `guestbook`, use the project `default`, and leave the sync policy as `Manual`:

Connect the <https://github.com/argoproj/argocd-example-apps.git> repo to Argo CD by setting repository url to the github repo url, leave revision as `HEAD`, and set the path to `guestbook`:

For **Destination**, set cluster URL to `https://kubernetes.default.svc` (or `in-cluster` for cluster name) and namespace to `default`:

After filling out the information above, click **Create** at the top of the UI to create the `guestbook` application:

## 7. Sync (Deploy) The Application[¶](#7-sync-deploy-the-application "Permanent link")

### Syncing via CLI[¶](#syncing-via-cli "Permanent link")

Once the guestbook application is created, you can now view its status:

```
$ argocd app get guestbook
Name:               guestbook
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://10.97.164.88/applications/guestbook
Repo:               https://github.com/argoproj/argocd-example-apps.git
Target:
Path:               guestbook
Sync Policy:        <none>
Sync Status:        OutOfSync from  (1ff8a67)
Health Status:      Missing

GROUP  KIND        NAMESPACE  NAME          STATUS     HEALTH
apps   Deployment  default    guestbook-ui  OutOfSync  Missing
       Service     default    guestbook-ui  OutOfSync  Missing
```

The application status is initially in `OutOfSync` state since the application has yet to be
deployed, and no Kubernetes resources have been created. To sync (deploy) the application, run:

```
argocd app sync guestbook
```

This command retrieves the manifests from the repository and performs a `kubectl apply` of the
manifests. The guestbook app is now running and you can now view its resource components, logs,
events, and assessed health status.

### Syncing via UI[¶](#syncing-via-ui "Permanent link")

On the Applications page, click on *Sync* button of the guestbook application:

A panel will be opened and then, click on *Synchronize* button.

You can see more details by clicking at the guestbook application:

[Previous
Core Concepts](../core_concepts/)
[Next
Overview](../operator-manual/)

Made with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

{"base": "..", "features": [], "search": "../assets/javascripts/workers/search.b0710199.min.js", "translations": {"clipboard.copied": "Copied to clipboard", "clipboard.copy": "Copy to clipboard", "search.config.lang": "en", "search.config.pipeline": "trimmer, stopWordFilter", "search.config.separator": "[\\s\\-]+", "search.placeholder": "Search", "search.result.more.one": "1 more on this page", "search.result.more.other": "# more on this page", "search.result.none": "No matching documents", "search.result.one": "1 matching document", "search.result.other": "# matching documents", "search.result.placeholder": "Type to start searching", "search.result.term.missing": "Missing", "select.version.title": "Select version"}, "version": null}