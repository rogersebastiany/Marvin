.site-nav > .nav-list:nth-child(1):not(.nav-category-list) > .nav-list-item:not(.external):nth-child(1) > .nav-list-link { display: block; font-weight: 600; text-decoration: none; background-image: linear-gradient(-90deg, #ebedf5 0%, rgba(235, 237, 245, 0.8) 80%, rgba(235, 237, 245, 0) 100%); } .site-nav > .nav-list:nth-child(1):not(.nav-category-list) > .nav-list-item:not(.passive):nth-child(1) > .nav-list-expander svg { transform: rotate(-90deg); } .site-nav > .nav-list:nth-child(1):not(.nav-category-list) > .nav-list-item:not(.passive):nth-child(1) > .nav-list { display: block; } .site-nav > .nav-category-list > .nav-list-item:not(.passive) > .nav-list-expander svg { transform: rotate(-90deg); } .site-nav > .nav-category-list > .nav-list-item:not(.passive) > .nav-list { display: block; }      Home | C4 model             {"@context":"https://schema.org","@type":"WebSite","description":"C4 model","headline":"Home","name":"C4 model","url":"https://c4model.com/"}    [Skip to main content](#main-content)   Link      Menu      Expand       (external link)    Document      Search       Copy       Copied      

[C4 model](/)

* [Home](/)
* [Introduction](/introduction)
* [History](/history)
* [Abstractions](/abstractions)
  + [1. Software system](/abstractions/software-system)
  + [2. Container](/abstractions/container)
  + [3. Component](/abstractions/component)
  + [4. Code](/abstractions/code)
  + [Microservices](/abstractions/microservices)
  + [Queues and topics](/abstractions/queues-and-topics)
  + [FAQ](/abstractions/faq)
* [Diagrams](/diagrams)
  + [1. System context diagram](/diagrams/system-context)
  + [2. Container diagram](/diagrams/container)
  + [3. Component diagram](/diagrams/component)
  + [4. Code diagram](/diagrams/code)
  + [System landscape diagram](/diagrams/system-landscape)
  + [Dynamic diagram](/diagrams/dynamic)
  + [Deployment diagram](/diagrams/deployment)
  + [Notation](/diagrams/notation)
  + [Review checklist](/diagrams/checklist)
  + [FAQ](/diagrams/faq)
* [Tooling](/tooling)
* [FAQ](/faq)

* [Interactive example](https://c4model.com/example)
* [Book](https://www.oreilly.com/library/view/the-c4-model/9798341660113/)
* [Video](https://www.youtube.com/watch?v=x2-rSnhpw0g)
* [Training & workshops](https://simonbrown.je/workshops)
* [Patreon & Discord](https://www.patreon.com/c4model)
  This website and example diagrams are licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

# The C4 model for visualising software architecture

The C4 model is an easy to learn, developer friendly approach to software architecture diagramming:

1. A set of [hierarchical abstractions](/abstractions) - [software systems](/abstractions/software-system), [containers](/abstractions/container), [components](/abstractions/component), and [code](/abstractions/code).
2. A set of [hierarchical diagrams](/diagrams) - [system context](/diagrams/system-context), [containers](/diagrams/container), [components](/diagrams/component), and [code](/diagrams/code).
3. An additional set of supporting diagrams - [system landscape](/diagrams/system-landscape), [dynamic](/diagrams/dynamic), and [deployment](/diagrams/deployment).
4. [Notation independent](/diagrams/notation).
5. [Tooling independent](/tooling).

|  |  |
| --- | --- |
| **Visualising software architecture with the C4 model**   Recorded at "Agile on the Beach 2019", July 2019 | **The C4 model**  Simon Brown |

## About this website

This is the official website for the “C4 model for visualising software architecture”, written by its creator [Simon Brown](https://simonbrown.je).

 const links = { 'abstractions': '/abstractions', 'systemcontextdiagram': '/diagrams/system-context', 'containerdiagram': '/diagrams/container', 'componentdiagram': '/diagrams/component', 'codediagram': '/diagrams/code', 'systemlandscapediagram': '/diagrams/system-landscape', 'dynamicdiagram': '/diagrams/dynamic', 'deploymentdiagram': '/diagrams/deployment', 'notation': '/diagrams/notation', 'tooling': '/tooling', 'faq': '/faq', }; var hash = window.location.hash; if (hash && hash.length > 0) { hash = hash.substring(1).toLowerCase(); const link = links[hash]; if (link) { window.location.href = link; } }   

---

    showAd('main-content', 'c4model');