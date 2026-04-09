Catalog of Patterns of Distributed Systems

* [Refactoring](https://refactoring.com)
* [Agile](/agile.html)
* [Architecture](/architecture)
* [About](/aboutMe.html)
* [Thoughtworks](https://www.thoughtworks.com/engineering)

## Topics

[Architecture](/architecture)

[Refactoring](https://refactoring.com)

[Agile](/agile.html)

[Delivery](/delivery.html)

[Microservices](/microservices)

[Data](/data)

[Testing](/testing)

[DSL](/dsl.html)

## about me

[About](/aboutMe.html)

[Books](/books)

[FAQ](/faq.html)

## content

[Videos](/videos.html)

[Content Index](/tags)

[Board Games](/boardgames)

[Photography](/photos)

## Thoughtworks

[Home](https://thoughtworks.com)

[Insights](https://thoughtworks.com/insights)

[Careers](https://thoughtworks.com/careers)

[Radar](https://thoughtworks.com/radar)

[Engineering](https://www.thoughtworks.com/engineering)

## follow

[RSS](/feed.atom)

[Mastodon](https://toot.thoughtworks.com/@mfowler)

[LinkedIn](https://www.linkedin.com/in/martin-fowler-com/)

[Bluesky](https://bsky.app/profile/martinfowler.com)

[X](https://www.twitter.com/martinfowler)

[BGG](https://boardgamegeek.com/blog/13064/martins-7th-decade)

# Catalog of Patterns of Distributed Systems

[Unmesh Joshi](https://twitter.com/unmeshjoshi)

23 November 2023

Distributed systems provide a particular challenge to program. They
often require us to have multiple copies of data, which need to keep
synchronized. Yet we cannot rely on processing nodes working reliably, and
network delays can easily lead to inconsistencies. Despite this, many
organizations rely on a range of core distributed software handling data
storage, messaging, system management, and compute capability. These
systems face common problems which they solve with similar solutions.

In 2020 I began collecting these solutions as patterns, publishing them
on this site as I developed them. In 2023 these were published in the book
[Patterns of Distributed
Systems](/books/patterns-distributed.html). On this site I now have short summaries of each pattern, with
deep links to the relevant chapters for the online eBook publication on
oreilly.com (marked on this page with [).](https://learning.oreilly.com/library/view/patterns-of-distributed/9780138222246)

## [Clock-Bound Wait](clock-bound-wait.html)

Wait to cover the uncertainty in time across cluster nodes before
reading and writing values so that values
can be correctly ordered across cluster nodes.

## [Consistent Core](consistent-core.html)

Maintain a smaller cluster providing stronger consistency to allow the large data cluster to coordinate server activities without implementing quorum-based algorithms.

## [Emergent Leader](emergent-leader.html)

Order cluster nodes based on their age within the cluster to allow
nodes to select a leader without running an explicit election.

## [Fixed Partitions](fixed-partitions.html)

Keep the number of partitions fixed to keep
the mapping of data to partition unchanged when
the size of a cluster changes.

## [Follower Reads](follower-reads.html)

Serve read requests from followers to achieve better throughput
and lower latency

## [Generation Clock](generation-clock.html)

A monotonically increasing number indicating the generation of the server.

## [Gossip Dissemination](gossip-dissemination.html)

Use a random selection of nodes to pass on information to ensure it reaches all
the nodes in the cluster without flooding the network

## [HeartBeat](heartbeat.html)

Show a server is available by periodically sending a message to all the other servers.

## [High-Water Mark](high-watermark.html)

An index in the write-ahead log showing the last successful replication.

## [Hybrid Clock](hybrid-clock.html)

Use a combination of system timestamp and logical timestamp to have versions as date and time, which can be ordered

## [Idempotent Receiver](idempotent-receiver.html)

Identify requests from clients uniquely so you can ignore duplicate requests when client retries

## [Key-Range Partitions](key-range-partitions.html)

Partition data in sorted key ranges to efficiently handle
range queries.

## [Lamport Clock](lamport-clock.html)

Use logical timestamps as a version for a value to allow ordering of values across servers

## [Leader and Followers](leader-follower.html)

Have a single server to coordinate replication across a set of servers.

## [Lease](lease.html)

Use time-bound leases for cluster nodes to coordinate their activities.

## [Low-Water Mark](low-watermark.html)

An index in the write-ahead log showing which portion of the log can be discarded.

## [Majority Quorum](majority-quorum.html)

Avoid two groups of servers making independent decisions
by requiring majority for taking every decision.

## [Paxos](paxos.html)

Use two consensus building phases to reach safe consensus even
when nodes disconnect

## [Replicated Log](replicated-log.html)

Keep the state of multiple nodes synchronized by using a write-ahead log that is replicated to all the cluster nodes.

## [Request Batch](request-batch.html)

Combine multiple requests to optimally utilise the network

## [Request Pipeline](request-pipeline.html)

Improve latency by sending multiple requests on the connection without waiting for the response of the previous requests.

## [Request Waiting List](request-waiting-list.html)

Track client requests which require responses after the
criteria to respond is met based on responses from
other cluster nodes.

## [Segmented Log](segmented-log.html)

Split log into multiple smaller files instead of a single large file for easier operations.

## [Single-Socket Channel](single-socket-channel.html)

Maintain the order of the requests sent to a server by using a single TCP connection

## [Singular Update Queue](singular-update-queue.html)

Use a single thread to process requests asynchronously to maintain order without blocking the caller.

## [State Watch](state-watch.html)

Notify clients when specific values change on the server

## [Two-Phase Commit](two-phase-commit.html)

Update resources on multiple nodes in one atomic operation

## [Version Vector](version-vector.html)

Maintain a list of counters, one per cluster node, to detect concurrent updates

## [Versioned Value](versioned-value.html)

Store every update to a value with a new version, to allow reading historical values.

## [Write-Ahead Log](write-ahead-log.html)

Provide durability guarantee without the storage data structures to be flushed to disk,
by persisting every state change as a command to the append only log.

## Topics

[Architecture](/architecture)

[Refactoring](https://refactoring.com)

[Agile](/agile.html)

[Delivery](/delivery.html)

[Microservices](/microservices)

[Data](/data)

[Testing](/testing)

[DSL](/dsl.html)

## about me

[About](/aboutMe.html)

[Books](/books)

[FAQ](/faq.html)

## content

[Videos](/videos.html)

[Content Index](/tags)

[Board Games](/boardgames)

[Photography](/photos)

## Thoughtworks

[Home](https://thoughtworks.com)

[Insights](https://thoughtworks.com/insights)

[Careers](https://thoughtworks.com/careers)

[Radar](https://thoughtworks.com/radar)

[Engineering](https://www.thoughtworks.com/engineering)

## follow

[RSS](/feed.atom)

[Mastodon](https://toot.thoughtworks.com/@mfowler)

[LinkedIn](https://www.linkedin.com/in/martin-fowler-com/)

[Bluesky](https://bsky.app/profile/martinfowler.com)

[X](https://www.twitter.com/martinfowler)

[BGG](https://boardgamegeek.com/blog/13064/martins-7th-decade)

© Martin Fowler | [Disclosures](/aboutMe.html#disclosures)