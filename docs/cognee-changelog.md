Cognee releases with highlights and links to the full release notes on GitHub.

## [​](#v0-5-4-dev1) v0.5.4.dev1

**Released:** March 5, 2026  
**[View on GitHub](https://github.com/topoteretes/cognee/releases/tag/v0.5.4.dev1)**

### [​](#highlights) Highlights

* Developer preview release focused on quality, performance, and developer ergonomics
* Faster ingestion and sync
* Improved search relevance and new filtering options
* Stability fixes for memory creation, deletion, and CLI workflows
* Internal refactoring and dependency upgrades

### [​](#new-features) New Features

* Bulk import CLI for faster batched ingestion
* Search filters for tags and date ranges
* Optional per-collection ingestion throttling

### [​](#improvements) Improvements

* Lower latency for ingestion and sync
* Better search ranking
* More robust deletion and duplicate handling
* Clearer CLI messages and debug logs

### [​](#bug-fixes) Bug Fixes

* Fixed duplicate memories under concurrent ingestion
* Fixed partial state after deletion
* Fixed CLI export formatting issues
* Fixed intermittent retrieval failures under load

---

## [​](#v0-5-3) v0.5.3

**Released:** February 27, 2026  
**[View on GitHub](https://github.com/topoteretes/cognee/releases/tag/v0.5.3)**

### [​](#highlights-2) Highlights

* New graph visualization improvements
* Expanded permissions and user management work
* SessionManager and cache/session persistence work
* Search and graph retrieval improvements
* Multiple stability and CI/CD fixes

### [​](#notable-changes) Notable Changes

* Added role-based permission checks and permission endpoints
* Added graph visualization updates, including note set coloring
* Added return type hints to API functions
* Added chunk associations for the memify pipeline
* Added vector filtering based on node sets
* Fixed delete flow bugs, health check issues, MCP issues, and several config/integration issues

---

## [​](#v0-5-3-dev1) v0.5.3.dev1

**Released:** February 20, 2026  
**[View on GitHub](https://github.com/topoteretes/cognee/releases/tag/v0.5.3.dev1)**

### [​](#highlights-3) Highlights

* Added vector filtering based on node sets
* Added principal Cognee configuration
* Fixed health check issues
* Fixed FalkorDB adapter port bug
* Fixed Ollama image ingestion argument issue

### [​](#notes) Notes

* Includes a small set of targeted fixes and feature work on top of `v0.5.3.dev0`
* Introduced one new contributor in this release