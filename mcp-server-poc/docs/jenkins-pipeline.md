Pipeline

window.addEventListener('DOMContentLoaded', function () {
for (var i = 1 ; i <= 6 ; i ++) {
anchors.add('.container .row .col-lg-9 h' + i);
}
})

[> User Documentation Home](/doc/)

##### User Handbook

* [User Handbook Overview](/doc/book/getting-started/)
* [Installing Jenkins](/doc/book/installing/)
* [Platform Information](/doc/book/platform-information/)
* [Using Jenkins](/doc/book/using/)
* [Pipeline](/doc/book/pipeline/)

  + [Getting started with Pipeline](/doc/book/pipeline/getting-started/)
  + [Using a Jenkinsfile](/doc/book/pipeline/jenkinsfile/)
  + [Running Pipelines](/doc/book/pipeline/running-pipelines/)
  + [Branches and Pull Requests](/doc/book/pipeline/multibranch/)
  + [Using Docker with Pipeline](/doc/book/pipeline/docker/)
  + [Extending with Shared Libraries](/doc/book/pipeline/shared-libraries/)
  + [Pipeline Development Tools](/doc/book/pipeline/development/)
  + [Pipeline Syntax](/doc/book/pipeline/syntax/)
  + [Pipeline as Code](/doc/book/pipeline/pipeline-as-code/)
  + [Pipeline Best Practices](/doc/book/pipeline/pipeline-best-practices/)
  + [Scaling Pipelines](/doc/book/pipeline/scaling-pipeline/)
  + [Pipeline CPS Method Mismatches](/doc/book/pipeline/cps-method-mismatches/)
* [Blue Ocean](/doc/book/blueocean/)
* [Managing Jenkins](/doc/book/managing/)
* [Securing Jenkins](/doc/book/security/)
* [System Administration](/doc/book/system-administration/)
* [Scaling Jenkins](/doc/book/scaling/)
* [Troubleshooting Jenkins](/doc/book/troubleshooting/)
* [Glossary](/doc/book/glossary/)

##### Tutorials

* [Guided Tour](/doc/pipeline/tour/getting-started/)
* [Jenkins Pipeline](/doc/tutorials#pipeline)
* [Using Build Tools](/doc/tutorials#tools)

##### Resources

* [Pipeline Syntax reference](/doc/book/pipeline/syntax/)
* [Pipeline Steps reference](/doc/pipeline/steps/)
* [LTS Upgrade guides](/doc/upgrade-guide/)

[⇐ Using Jenkins](../using)

[Index](../)

[Getting started with Pipeline ⇒](getting-started)

# Pipeline

Chapter Sub-Sections

* [Getting started with Pipeline](getting-started)
* [Using a Jenkinsfile](jenkinsfile)
* [Running Pipelines](running-pipelines)
* [Branches and Pull Requests](multibranch)
* [Using Docker with Pipeline](docker)
* [Extending with Shared Libraries](shared-libraries)
* [Pipeline Development Tools](development)
* [Pipeline Syntax](syntax)
* [Pipeline as Code](pipeline-as-code)
* [Pipeline Best Practices](pipeline-best-practices)
* [Scaling Pipelines](scaling-pipeline)
* [Pipeline CPS Method Mismatches](cps-method-mismatches)

Table of Contents

* [What is Jenkins Pipeline?](#overview)
  + [Declarative versus Scripted Pipeline syntax](#declarative-versus-scripted-pipeline-syntax)
* [Why Pipeline?](#why)
* [Pipeline concepts](#pipeline-concepts)
  + [Pipeline](#pipeline)
  + [Node](#node)
  + [Stage](#stage)
  + [Step](#step)
* [Pipeline syntax overview](#pipeline-syntax-overview)
  + [Declarative Pipeline fundamentals](#declarative-pipeline-fundamentals)
  + [Scripted Pipeline fundamentals](#scripted-pipeline-fundamentals)
* [Pipeline example](#pipeline-example)

This chapter covers all recommended aspects of Jenkins Pipeline functionality,
including how to:

* [Get started with Pipeline](getting-started), which covers how to
  [define a Jenkins Pipeline](getting-started#defining-a-pipeline) (your
  `Pipeline`) through
  [Blue Ocean](getting-started#through-blue-ocean), through the
  [classic UI](getting-started#through-the-classic-ui) or in
  [SCM](getting-started#defining-a-pipeline-in-scm).
* [Create and use a `Jenkinsfile`](jenkinsfile), which covers use-case scenarios
  on how to craft and construct your `Jenkinsfile`.
* Work with [branches and pull requests](multibranch).
* [Use Docker with Pipeline](docker), covering how Jenkins can invoke Docker
  containers on agents/nodes (from a `Jenkinsfile`) to build your Pipeline
  projects.
* [Extend Pipeline with shared libraries](shared-libraries).
* Use different [development tools](development) to facilitate the creation
  of your Pipeline.
* Work with [Pipeline syntax](syntax), which provides a comprehensive
  reference of all Declarative Pipeline syntax.

For an overview of content in the Jenkins User Handbook, refer to the [User Handbook Overview](getting-started).

## What is Jenkins Pipeline?

Jenkins Pipeline (or simply "Pipeline" with a capital "P") is a suite of plugins
which supports implementing and integrating *continuous delivery pipelines* into
Jenkins.

A *continuous delivery (CD) pipeline* is an automated expression of your process
for getting software from version control right through to your users and
customers. Every change to your software (committed in source control) goes
through a complex process on its way to being released. This process involves
building the software in a reliable and repeatable manner, as well as
progressing the built software (called a "build") through multiple stages of
testing and deployment.

Pipeline provides an extensible set of tools for modeling simple-to-complex
delivery pipelines "as code" via the
[Pipeline domain-specific language (DSL) syntax](syntax).
[[1](#_footnotedef_1 "View footnote.")]

The definition of a Jenkins Pipeline is written into a text file (called a
[`Jenkinsfile`](jenkinsfile)) which in turn can be committed to a project’s
source control repository.
[[2](#_footnotedef_2 "View footnote.")]
This is the foundation of "Pipeline-as-code"; treating the CD pipeline as a part of
the application to be versioned and reviewed like any other code.

Creating a `Jenkinsfile` and committing it to source control provides a number
of immediate benefits:

* Automatically creates a Pipeline build process for all branches and pull
  requests.
* Code review/iteration on the Pipeline (along with the remaining source code).
* Audit trail for the Pipeline.
* Single source of truth
  [[3](#_footnotedef_3 "View footnote.")]
  for the Pipeline, which can be viewed and edited by multiple
  members of the project.

While the syntax for defining a Pipeline, either in the web UI or with a
`Jenkinsfile` is the same, it is generally considered best practice to define
the Pipeline in a `Jenkinsfile` and check that in to source control.

### Declarative versus Scripted Pipeline syntax

A `Jenkinsfile` can be written using two types of syntax — Declarative and
Scripted.

Declarative and Scripted Pipelines are constructed fundamentally differently.
Declarative Pipeline is designed to make writing and reading Pipeline code easier, and provides richer syntactical features over Scripted Pipeline syntax.

Many of the individual syntactical components (or "steps") written into a
`Jenkinsfile`, however, are common to both Declarative and Scripted Pipeline.
Read more about how these two types of syntax differ in [Pipeline concepts](#pipeline-concepts)
and [Pipeline syntax overview](#pipeline-syntax-overview) below.

## Why Pipeline?

Jenkins is, fundamentally, an automation engine which supports a number of
automation patterns. Pipeline adds a powerful set of automation tools onto
Jenkins, supporting use cases that span from simple continuous integration to
comprehensive CD pipelines. By modeling a series of related tasks, users can
take advantage of the many features of Pipeline:

* **Code**: Pipelines are implemented in code and typically checked into source
  control, giving teams the ability to edit, review, and iterate upon their
  delivery pipeline.
* **Durable**: Pipelines can survive both planned and unplanned restarts of the
  Jenkins controller.
* **Pausable**: Pipelines can optionally stop and wait for human input or approval
  before continuing the Pipeline run.
* **Versatile**: Pipelines support complex real-world CD requirements, including
  the ability to fork/join, loop, and perform work in parallel.
* **Extensible**: The Pipeline plugin supports custom extensions to its DSL
  [[1](#_footnotedef_1 "View footnote.")] and multiple options for integration with other plugins.

While Jenkins has always allowed rudimentary forms of chaining Freestyle Jobs
together to perform sequential tasks,
[[4](#_footnotedef_4 "View footnote.")] Pipeline makes this concept a first-class citizen in
Jenkins.

What is the difference between Freestyle and Pipeline in Jenkins

Building on the core Jenkins value of extensibility, Pipeline is also extensible
both by users with [Pipeline Shared Libraries](shared-libraries) and by
plugin developers.
[[5](#_footnotedef_5 "View footnote.")]

The flowchart below is an example of one CD scenario easily modeled in Jenkins
Pipeline:

## Pipeline concepts

The following concepts are key aspects of Jenkins Pipeline, which tie in closely
to Pipeline syntax (refer to the [overview](#pipeline-syntax-overview) below).

### Pipeline

A Pipeline is a user-defined model of a CD pipeline. A Pipeline’s code defines
your entire build process, which typically includes stages for building an
application, testing it and then delivering it.

Also, a `pipeline` block is a
[key part of Declarative Pipeline syntax](#declarative-pipeline-fundamentals).

### Node

A node is a machine which is part of the Jenkins environment and is capable of
executing a Pipeline.

Also, a `node` block is a
[key part of Scripted Pipeline syntax](#scripted-pipeline-fundamentals).

### Stage

A `stage` block defines a conceptually distinct subset of tasks performed
through the entire Pipeline (e.g. "Build", "Test" and "Deploy" stages),
which is used by many plugins to visualize or present Jenkins Pipeline
status/progress.
[[6](#_footnotedef_6 "View footnote.")]

### Step

A single task. Fundamentally, a step tells Jenkins *what* to do at a
particular point in time (or "step" in the process). For example, to execute
the shell command `make`, use the `sh` step: `sh 'make'`. When a plugin
extends the Pipeline DSL, [[1](#_footnotedef_1 "View footnote.")] that typically means the plugin has
implemented a new *step*.

## Pipeline syntax overview

The following Pipeline code skeletons illustrate the fundamental differences
between [Declarative Pipeline syntax](#declarative-pipeline-fundamentals) and
[Scripted Pipeline syntax](#scripted-pipeline-fundamentals).

Be aware that both [stages](#stage) and [steps](#step) (above) are common
elements of both Declarative and Scripted Pipeline syntax.

### Declarative Pipeline fundamentals

In Declarative Pipeline syntax, the `pipeline` block defines all the work done
throughout your entire Pipeline.

Jenkinsfile (Declarative Pipeline)

```
pipeline {
    agent any (1)
    stages {
        stage('Build') { (2)
            steps {
                // (3)
            }
        }
        stage('Test') { (4)
            steps {
                // (5)
            }
        }
        stage('Deploy') { (6)
            steps {
                // (7)
            }
        }
    }
}
```

|  |  |
| --- | --- |
| **1** | Execute this Pipeline or any of its stages, on any available agent. |
| **2** | Defines the "Build" stage. |
| **3** | Perform some steps related to the "Build" stage. |
| **4** | Defines the "Test" stage. |
| **5** | Perform some steps related to the "Test" stage. |
| **6** | Defines the "Deploy" stage. |
| **7** | Perform some steps related to the "Deploy" stage. |

### Scripted Pipeline fundamentals

In Scripted Pipeline syntax, one or more `node` blocks do the core work
throughout the entire Pipeline. Although this is not a mandatory requirement of
Scripted Pipeline syntax, confining your Pipeline’s work inside of a `node`
block does two things:

1. Schedules the steps contained within the block to run by adding an item
   to the Jenkins queue. As soon as an executor is free on a node, the
   steps will run.
2. Creates a workspace (a directory specific to that particular
   Pipeline) where work can be done on files checked out from source control.  
   **Caution:** Depending on your Jenkins configuration, some workspaces may
   not get automatically cleaned up after a period of inactivity. Refer to the tickets
   and discussion linked from
   [JENKINS-2111](https://issue-redirect.jenkins.io/issue/2111) for more
   information.

Jenkinsfile (Scripted Pipeline)

```
node {  (1)
    stage('Build') { (2)
        // (3)
    }
    stage('Test') { (4)
        // (5)
    }
    stage('Deploy') { (6)
        // (7)
    }
}
```

|  |  |
| --- | --- |
| **1** | Execute this Pipeline or any of its stages, on any available agent. |
| **2** | Defines the "Build" stage. `stage` blocks are optional in Scripted Pipeline syntax. However, implementing `stage` blocks in a Scripted Pipeline provides clearer visualization of each `stage`'s subset of tasks/steps in the Jenkins UI. |
| **3** | Perform some steps related to the "Build" stage. |
| **4** | Defines the "Test" stage. |
| **5** | Perform some steps related to the "Test" stage. |
| **6** | Defines the "Deploy" stage. |
| **7** | Perform some steps related to the "Deploy" stage. |

## Pipeline example

Here is an example of a `Jenkinsfile` using Declarative Pipeline syntax — its
Scripted syntax equivalent can be accessed by clicking the **Toggle Scripted
Pipeline** link below:

Jenkinsfile (Declarative Pipeline)

```
pipeline { (1)
    agent any (2)
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') { (3)
            steps { (4)
                sh 'make' (5)
            }
        }
        stage('Test'){
            steps {
                sh 'make check'
                junit 'reports/**/*.xml' (6)
            }
        }
        stage('Deploy') {
            steps {
                sh 'make publish' //
            }
        }
    }
}
```

[Toggle Scripted Pipeline](#)
*(Advanced)*

Jenkinsfile (Scripted Pipeline)

```
node { //
    stage('Build') { (3)
        sh 'make' (5)
    }
    stage('Test') {
        sh 'make check'
        junit 'reports/**/*.xml' (6)
    }
    if (currentBuild.currentResult == 'SUCCESS') {
        stage('Deploy') {
            sh 'make publish' //
        }
    }
}
```

|  |  |
| --- | --- |
| **1** | [`pipeline`](syntax#declarative-pipeline) is Declarative Pipeline-specific syntax that defines a "block" containing all content and instructions for executing the entire Pipeline. |
| **2** | [`agent`](syntax#agent) is Declarative Pipeline-specific syntax that instructs Jenkins to allocate an executor (on a node) and workspace for the entire Pipeline. |
| **3** | `stage` is a syntax block that describes a [stage of this Pipeline](#stage). Read more about `stage` blocks in Declarative Pipeline syntax on the [Pipeline syntax](syntax#stage) page. As mentioned [above](#scripted-pipeline-fundamentals), `stage` blocks are optional in Scripted Pipeline syntax. |
| **4** | [`steps`](syntax#steps) is Declarative Pipeline-specific syntax that describes the steps to be run in this `stage`. |
| **5** | `sh` is a Pipeline [step](syntax#steps) (provided by the [Pipeline: Nodes and Processes plugin](https://plugins.jenkins.io/workflow-durable-task-step)) that executes the given shell command. |
| **6** | `junit` is another Pipeline [step](syntax#steps) (provided by the [JUnit plugin](https://plugins.jenkins.io/junit)) for aggregating test reports. |

Read more about Pipeline syntax on the [Pipeline Syntax](syntax) page.

---

[1](#_footnoteref_1). [Domain-specific language](https://en.wikipedia.org/wiki/Domain-specific_language)

[2](#_footnoteref_2). [Source control management](https://en.wikipedia.org/wiki/Version_control)

[3](#_footnoteref_3). [Single source of truth](https://en.wikipedia.org/wiki/Single_source_of_truth)

[4](#_footnoteref_4). Additional plugins have been used to implement complex behaviors utilizing Freestyle Jobs such as the Copy Artifact, Parameterized Trigger, and Promoted Builds plugins

[5](#_footnoteref_5). [GitHub Branch Source plugin](https://plugins.jenkins.io/github-branch-source)

[6](#_footnoteref_6). [Blue Ocean](../blueocean), [Pipeline: Stage View plugin](https://plugins.jenkins.io/pipeline-stage-view)

---

[⇐ Using Jenkins](../using)

[Index](../)

[Getting started with Pipeline ⇒](getting-started)

---

var feedbackForm = {
formKey : 'e/1FAIpQLSfCEexH09x\_-ytEyE7wetizqOvE\_-06WkK89dpBLEJcYnOp8w'
};
$(document).ready(function() {
window.onload = feedbackForm.start(window.location.href);
});

[Was this page helpful?](#feedback)

Please submit your feedback about this page through this
[quick form](/doc/feedback-form/).

Alternatively, if you don't wish to complete the quick form, you can simply
indicate if you found this page helpful?

var submitted=false;

Yes    
No

Submit

See existing feedback [here](https://docs.google.com/spreadsheets/d/1IIdpVs39JDYKg0sLQIv-MNO928qcGApAIfdW5ohfD78).

$(function(){
var $body = $(document.body);
$body.on("keydown", function(){
$body.removeClass("no-outline");
})
const updateTheme = () => {
const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.dataset.theme = dark ? "dark" : "";
}
updateTheme();
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme);
})