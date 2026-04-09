function OptanonWrapper(){}const callback=(e)=>{for(const t of e)t.type==="childList"&&t.addedNodes.forEach(e=>{e.nodeName==="IMG"&&document.querySelectorAll('img:not([src^="http"]):not([data-ot-ignore])').forEach(e=>{e.setAttribute("data-ot-ignore","")})})},config={attributes:!0,childList:!0,subtree:!0,attributeFilter:["src"]},observer=new MutationObserver(callback);observer.observe(document.documentElement,config)window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date),gtag("config","GTM-NJXWQL"),gtag("consent","default",{analytics\_storage:"granted",ad\_storage:"granted",functionality\_storage:"granted",wait\_for\_update:500}),gtag("consent","default",{analytics\_storage:"denied",ad\_storage:"denied",functionality\_storage:"denied",region:["AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE","IS","LI","NO","GB","PE","RU"],wait\_for\_update:500}),window.geofeed=e=>{dataLayer.push({event:"OneTrustCountryLoad",oneTrustCountryId:e.country.toString()})};const json=document.createElement("script");json.setAttribute("src","https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location/geofeed"),document.head.appendChild(json)Get started with GitLab CI/CD | GitLab Docs{"@context":"https://schema.org","@type":"WebSite","name":"GitLab Docs","url":"https://docs.gitlab.com/"}(function(){const p="gitlab-docs-theme",g="gitlab-docs-layout",e={LIGHT:"light",DARK:"dark",AUTO:"auto"},i={FIXED:"fixed",FLUID:"fluid"},d="light",f="fixed";let r=!1;const t=localStorage?.getItem(p),m=localStorage?.getItem(g),l=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches?e.DARK:e.LIGHT;function h(){return t&&(t===e.LIGHT||t===e.DARK)?t:(t===e.AUTO&&(r=!0),l||d)}function u(){return m===i.FLUID?i.FLUID:f}const s=h(),c=u(),n=document.documentElement;n.classList.remove("gl-dark","gl-light"),n.classList.add(s===e.DARK?"gl-dark":"gl-light"),c===i.FLUID&&(n.classList.add("fluid"),n.classList.remove("fixed"));const a=document.getElementById("syntax-dark-theme"),o=document.getElementById("syntax-light-theme");a&&o&&(s===e.DARK?(a.disabled=!1,o.disabled=!0):(a.disabled=!0,o.disabled=!1)),window.\_\_initialTheme=r?e.AUTO:s,window.\_\_initialLayout=c})()window.pageMetadata={trail:[{path:"user/",title:"Use GitLab"},{path:"topics/build\_your\_application/",title:"Use CI/CD to build your application"},{path:"ci/",title:"Getting started"}]}const ELASTIC\_CLOUD\_ID="gitlab-docs-website:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDQwZTQyYTQzMTJiZjQyMzNiMzBiZTg0MTU5YjlkNmE1JGMxODg4Y2U5OTY0YzQzZjc5ZjQ1YTk5NDZmMjI0ODg0",ELASTIC\_KEY="NndlZTY1c0JCLTRHU1gzUVBER2w6TVF5OEVIT2JvM1V1X0xjYVpnLVhzQQ==",ELASTIC\_INDEX="search-gitlab-docs-v3"const FS\_IDENTIFIER="AIzaSyCLdi3jHHjkmLji9D8uj\_RNPMHcdrYoIW4",RECAPTCHA\_PUBLIC\_KEY="6Le4R3UrAAAAALsIlK\_siq0\_UhPD-0rD-ImF1gfO"

[Skip to main content](#skipTarget)
[Go to GitLab Docs homepage](/)

[What's new?](https://about.gitlab.com/releases/whats-new/)

window.languageData=window.languageData||{},window.languageData.languages=[{code:"en-US",name:"English",url:"/ci/",current:!0},{code:"ja-JP",name:"日本語",url:"/ja-jp/ci/",current:!1}],window.languageData.currentLang="en-US"

[What's new?](https://about.gitlab.com/releases/whats-new/)
[Get free trial](https://gitlab.com/-/trial_registrations/new?glm_source=docs.gitlab.com&amp;glm_content=navigation-cta-docs)

Toggle menu

* [Use GitLab](/user/)
* [GitLab Duo](/user/gitlab_duo/)
* [Extend](/api/)
* [Install](/install/)
* [Administer](/administration/)
* [Subscribe](/subscriptions/)
* [Contribute](/development/)
* [Solutions](/solutions/)

---

# Get started with GitLab CI/CD

* Tier: Free, Premium, Ultimate
* Offering: GitLab.com, GitLab Self-Managed, GitLab Dedicated

CI/CD is a continuous method of software development, where you continuously build,
test, deploy, and monitor iterative code changes.

This iterative process helps reduce the chance that you develop new code based on
buggy or failed previous versions. GitLab CI/CD can catch bugs early in the development cycle,
and help ensure that the code deployed to production complies with your established code standards.

This process is part of a larger workflow:

## Step 1: Configure your pipeline

To use GitLab CI/CD, you start with a `.gitlab-ci.yml` file at the root of your project.
This file specifies the stages, jobs, and scripts to be executed during your CI/CD pipeline.
It is a YAML file with its own custom syntax.

By default, the file is named `.gitlab-ci.yml`, but you can use any filename.

In this file, you define variables, dependencies between jobs, and specify when
and how each job should be executed.

A pipeline is defined in the `.gitlab-ci.yml` file,
and executes when the file runs on a runner.

Pipelines are made up of stages and jobs:

* Stages define the order of execution. Typical stages might be `build`, `test`, and `deploy`.
* Jobs specify the tasks to be performed in each stage. For example, a job can compile or test code.

Pipelines can be triggered by various events, like commits or merges, or can be on schedule.
In your pipeline, you can integrate with a wide range of tools and platforms.

For more information, see:

* [Tutorial: Create and run your first GitLab CI/CD pipeline](/ci/quick_start/)
* [Pipelines](/ci/pipelines/)

## Step 2: Find or create runners

Runners are the agents that run your jobs. These agents can run on physical machines or virtual instances.
In your `.gitlab-ci.yml` file, you can specify a container image you want to use when running the job.
The runner loads the image, clones your project, and runs the job either locally or in the container.

If you use GitLab.com, runners on Linux, Windows, and macOS are already available for use.
If needed, you can also register your own runners.

If you don’t use GitLab.com, you can:

* Register runners or use runners already registered for your GitLab Self-Managed instance.
* Create a runner on your local machine.

For more information, see:

* [Create, register, and run your own project runner](/tutorials/create_register_first_runner/)

## Step 3: Use CI/CD variables and expressions

GitLab CI/CD variables are key-value pairs you use to store and pass configuration settings
and sensitive information, like passwords or API keys, to jobs in a pipeline.

GitLab CI/CD expressions allow you to inject data dynamically into your pipeline configuration.
The data available depends on the expression context.
For example, the `inputs` context allows you to access information passed into the
configuration file from a parent file or when a pipeline is run.

### CI/CD variables

Use CI/CD variables to customize jobs by making values defined elsewhere accessible to jobs.
You can hard-code CI/CD variables in your `.gitlab-ci.yml` file, set them in your project settings,
or generate them dynamically. You can define them for the project, group, or instance.

The following types of variables are available:

* Custom variables: Variables that you create and manage in the UI, API, or configuration files.
* Predefined variables: Variables that GitLab automatically sets to provide information about the current job, pipeline, and environment.

You can configure variables with security settings:

* Protected variables: Restrict access to jobs running on protected branches or tags.
* Masked variables: Hide variable values in job logs to prevent sensitive information from being exposed.

For more information, see:

* [CI/CD variables](/ci/variables/)

### CI/CD expressions

CI/CD expressions use the `$[[ ]]` syntax and are validated when you create a pipeline.
You can also validate expressions in the pipeline editor before committing changes.

Expressions enable dynamic configuration based on different contexts:

* **Inputs context** (`$[[ inputs.INPUT_NAME ]]`): Access typed parameters passed into configuration files with `include:inputs` or when a new pipeline is run
* **Matrix context** (`$[[ matrix.IDENTIFIER ]]`): Access matrix values in job dependencies to create 1:1 mappings between matrix jobs

For more information, see:

* [CI expressions](/ci/yaml/expressions/)

## Step 4: Use CI/CD components

A CI/CD component is a reusable pipeline configuration unit.
Use a CI/CD component to compose an entire pipeline configuration or a small part of a larger pipeline.

You can add a component to your pipeline configuration with `include:component`.

Reusable components help reduce duplication, improve maintainability, and promote consistency across projects.
Create a component project and publish it to the CI/CD Catalog to share your component across multiple projects.

GitLab also has CI/CD component templates for common tasks and integrations.

For more information, see:

* [CI/CD components](/ci/components/)

* [Facebook](https://www.facebook.com/gitlab)
* [LinkedIn](https://www.linkedin.com/company/gitlab-com)
* [Twitter](https://twitter.com/gitlab)
* [YouTube](https://www.youtube.com/channel/UCnMGQ8QHMAnVIsI3xJrihhg)

Company

* [About GitLab](https://about.gitlab.com/company/)
* [View pricing](https://about.gitlab.com/pricing/)
* [Try GitLab for free](https://about.gitlab.com/free-trial/)

Feedback

* [View page source](https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/ci/_index.md)
* [Edit in Web IDE](https://gitlab.com/-/ide/project/gitlab-org/gitlab/edit/master/-/doc/ci/_index.md)
* [Contribute to GitLab](https://about.gitlab.com/community/contribute/)
* [Suggest updates](https://gitlab.com/gitlab-org/gitlab/-/issues/new?issuable_template=Documentation)

Help & Community

* [Get certified](https://university.gitlab.com/pages/certifications)
* [Get support](https://about.gitlab.com/support/)
* [Post on the GitLab forum](https://forum.gitlab.com/new-topic?title=topic%20title&body=topic%20body&tags=docs-feedback)

Resources

* [Terms](https://about.gitlab.com/terms/)
* [Privacy statement](https://about.gitlab.com/privacy/)
* [Use of generative AI](/legal/use_generative_ai/)
* [Acceptable use of user licenses](/legal/licensing_policy/)

(function(e,t,n,s,o){e[s]=e[s]||[],e[s].push({"gtm.start":(new Date).getTime(),event:"gtm.js"});var a=t.getElementsByTagName(n)[0],i=t.createElement(n),r=s!="dataLayer"?"&l="+s:"";i.async=!0,i.src="https://www.googletagmanager.com/gtm.js?id="+o+r,a.parentNode.insertBefore(i,a)})(window,document,"script","dataLayer","GTM-NJXWQL")(function(){var e,t=!1;function n(){t===!1&&(t=!0,Munchkin.init("194-VVC-221",{useBeaconAPI:!0}))}e=document.createElement("script"),e.type="text/javascript",e.async=!0,e.src="https://munchkin.marketo.net/munchkin.js",e.onreadystatechange=function(){(this.readyState=="complete"||this.readyState=="loaded")&&n()},e.onload=n,document.getElementsByTagName("head")[0].appendChild(e)})()\_linkedin\_partner\_id="30694",window.\_linkedin\_data\_partner\_ids=window.\_linkedin\_data\_partner\_ids||[],window.\_linkedin\_data\_partner\_ids.push(\_linkedin\_partner\_id),function(){var t=document.getElementsByTagName("script")[0],e=document.createElement("script");e.type="text/javascript",e.async=!0,e.src="https://snap.licdn.com/li.lms-analytics/insight.min.js",t.parentNode.insertBefore(e,t)}()