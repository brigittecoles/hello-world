# The Apache Software Foundation — Comprehensive Project Inventory

> A categorized, pattern-oriented inventory of Apache Software Foundation (ASF) projects:
> what each one is, what it does, the reusable architectural patterns it embodies, and what
> people use it for.

---

## How to read this inventory

**Scope.** As reconciled against the ASF's live data on 2026-11-06, there are **~215 active
top-level projects** (each with its own Project Management Committee, PMC), **24 current
Incubator podlings**, and hundreds of **retired (Attic)** projects — plus a long tail of
**sub-projects** (the foundation's machine-readable directory lists **1,497** project +
sub-project DOAP entries in total). The older "350+ projects" figure the ASF has quoted counts
projects *and* sub-projects together; the top-level count itself sits around 215–220. A truly
exhaustive, line-by-line enumeration of *every* package, module, and sub-project would run to
thousands of entries and change almost weekly. This document covers **every active top-level
project** (reconciled against the authoritative list below) plus the significant families,
organized so the long tail is represented. Large umbrella projects (Apache Commons, Logging
Services, the Hadoop ecosystem, Apache Directory) are broken out into their constituent
modules.

**Each entry** gives, as applicable:

- **Description** — what it *is*, in one or two sentences.
- **Function** — the job it performs in a system.
- **Patterns** — the abstracted / reusable architecture and design patterns it embodies.
- **Use cases** — the situations it is reached for.
- **Tags** — primary language(s) and lifecycle status.

**Status legend**

| Tag | Meaning |
|-----|---------|
| 🟢 **Active** | Current top-level project (TLP) with an active PMC. |
| 🥚 **Incubating** | In the Apache Incubator; not yet (or recently) a TLP. |
| 🗄️ **Attic** | Retired to the Apache Attic; code remains available, development has ended. |
| 🟡 **Low activity** | Still a TLP but with reduced release cadence (noted where relevant). |

**Sourcing & accuracy note.** This inventory was compiled from domain knowledge and then
**reconciled on 2026-11-06 against the ASF's authoritative machine-readable data** —
`projects.apache.org/json/foundation/projects.json` (1,497 project/sub-project entries; ~215
active PMCs) and `.../podlings.json` (24 current podlings) — with targeted web search used to
settle individual lifecycle changes. The reconciliation added 31 active top-level projects that
the first draft had missed (see [§29](#29-additional-active-top-level-projects-reconciliation-additions))
and corrected several status tags. Project *status* remains the most volatile field, and the
ASF's own datasets occasionally lag each other for the very newest projects (a handful of 2025–2026
entrants such as Auron, Iggy, Fluss, and Teaclave sit ambiguously between "incubating" and
"recently graduated"); those are flagged inline. The **Appendix** lists the canonical
always-current sources.

---

## Table of contents

- [Part 0 — Understanding the ASF](#part-0--understanding-the-asf)
- [Part 1 — Cross-cutting abstracted patterns](#part-1--cross-cutting-abstracted-patterns)
- [Part 2 — The inventory by category](#part-2--the-inventory-by-category)
  1. [Web serving, proxies & API gateways](#1-web-serving-proxies--api-gateways)
  2. [Application servers, Jakarta EE & OSGi runtimes](#2-application-servers-jakarta-ee--osgi-runtimes)
  3. [Java web / UI frameworks & templating](#3-java-web--ui-frameworks--templating)
  4. [Storage formats & serialization](#4-storage-formats--serialization)
  5. [Batch & stream processing engines](#5-batch--stream-processing-engines)
  6. [SQL engines, query frameworks & lakehouse](#6-sql-engines-query-frameworks--lakehouse)
  7. [Databases & data stores](#7-databases--data-stores)
  8. [Messaging, streaming platforms & integration](#8-messaging-streaming-platforms--integration)
  9. [RPC, microservices & service frameworks](#9-rpc-microservices--service-frameworks)
  10. [Coordination, consensus & cluster management](#10-coordination-consensus--cluster-management)
  11. [Search & information retrieval](#11-search--information-retrieval)
  12. [Content, NLP & document processing](#12-content-nlp--document-processing)
  13. [Workflow orchestration & scheduling](#13-workflow-orchestration--scheduling)
  14. [Machine learning & AI](#14-machine-learning--ai)
  15. [Graph, geospatial & semantic web](#15-graph-geospatial--semantic-web)
  16. [IoT, edge & embedded / RTOS](#16-iot-edge--embedded--rtos)
  17. [Security, identity & cryptography](#17-security-identity--cryptography)
  18. [Observability & monitoring](#18-observability--monitoring)
  19. [Cloud, virtualization & container orchestration](#19-cloud-virtualization--container-orchestration)
  20. [Build, dependency & release tooling](#20-build-dependency--release-tooling)
  21. [Content management, collaboration & portals](#21-content-management-collaboration--portals)
  22. [Mobile & rich client](#22-mobile--rich-client)
  23. [BI, data visualization & notebooks](#23-bi-data-visualization--notebooks)
  24. [Core libraries — Apache Commons](#24-core-libraries--apache-commons)
  25. [Core libraries — Logging Services](#25-core-libraries--logging-services)
  26. [Core libraries — XML, HTTP & utilities](#26-core-libraries--xml-http--utilities)
  27. [Business applications](#27-business-applications)
  28. [Languages, runtimes & actor systems](#28-languages-runtimes--actor-systems)
  29. [Additional active top-level projects (reconciliation additions)](#29-additional-active-top-level-projects-reconciliation-additions)
- [Part 3 — The Apache Incubator](#part-3--the-apache-incubator)
- [Part 4 — The Attic (retired projects)](#part-4--the-attic-retired-projects)
- [Part 5 — Quick-reference summary](#part-5--quick-reference-summary)
- [Appendix — Canonical sources](#appendix--canonical-sources)

---

## Part 0 — Understanding the ASF

The Apache Software Foundation is a US 501(c)(3) non-profit, founded in 1999, that provides
organizational, legal, and financial support for a large portfolio of open-source software
projects. A few structural facts frame the whole inventory:

- **Everything ships under the Apache License 2.0.** A permissive license with an explicit
  patent grant and a requirement to preserve notices. This is why ASF code is ubiquitous in
  commercial products — it can be embedded and redistributed with minimal obligations.
- **The unit of organization is the project + its PMC.** Each top-level project (TLP) is
  governed by a Project Management Committee that owns releases and admits committers. There is
  no central architecture authority; projects are independent and heterogeneous by design.
- **"The Apache Way."** Community-led, consensus-driven, publicly archived decision-making
  ("if it didn't happen on the mailing list, it didn't happen"), meritocratic committership,
  and vendor-neutral governance. This governance model is itself one of the ASF's most-copied
  "patterns."
- **The Incubator** is the single front door for new projects and donations. Projects enter as
  **podlings**, learn ASF governance and legal hygiene (provenance, licensing, release
  process), and either **graduate** to TLP status or are retired.
- **The Attic** is where projects go when their community can no longer sustain them. Code and
  archives stay online and under the license; only active development stops.
- **DOAP files** ("Description of a Project") are the machine-readable metadata (category,
  language, repositories, releases) that power `projects.apache.org`.

Keep this lifecycle — **Incubator → TLP → (sometimes) Attic** — in mind; it explains the status
tags throughout and why some once-famous names (Mesos, MXNet, Oozie, Sqoop) now read 🗄️.

---

## Part 1 — Cross-cutting abstracted patterns

Across hundreds of independent projects, a surprisingly small set of architectural patterns
recurs. Recognizing them makes the whole portfolio legible: most ASF data-infrastructure
projects are recombinations of these building blocks. This section is the "abstracted patterns"
lens requested; individual entries below refer back to these.

### Data distribution & storage patterns

- **Shared-nothing horizontal partitioning (sharding).** Data is split by key across nodes that
  share no state, enabling linear scale-out. *Seen in:* Cassandra, HBase, Kafka (partitions),
  Solr (shards), Druid, Pinot, ShardingSphere, Doris.
- **Append-only commit log / write-ahead log (WAL).** Durability and ordering come from an
  immutable, sequentially written log; everything else is a materialized view of it. *Seen in:*
  Kafka, Pulsar/BookKeeper, Cassandra, HBase, most databases' recovery logs.
- **Log-structured merge tree (LSM).** Writes buffer in memory then flush to immutable sorted
  files that are compacted in the background — optimizing write throughput. *Seen in:*
  Cassandra, HBase, Accumulo, Kudu (hybrid), IoTDB.
- **Columnar storage + vectorized execution.** Store values by column and process them in
  batches to exploit compression and CPU/SIMD efficiency for analytics. *Seen in:* Parquet,
  ORC, Arrow, Druid, Pinot, Doris, Kudu, DataFusion, Gluten.
- **Open table format / lakehouse.** A metadata layer over object-store files provides ACID
  snapshots, schema evolution, and time travel, decoupling the table from the engine. *Seen in:*
  Iceberg, Hudi, Paimon, XTable.
- **Catalog / metastore abstraction.** A central service maps logical tables to physical data
  and governs access, so many engines share one source of truth. *Seen in:* Hive Metastore,
  Polaris, Gravitino, Atlas.
- **Inverted index.** Map terms → document postings for sub-linear full-text search. *Seen in:*
  Lucene, Solr.

### Compute & execution patterns

- **Master/worker (coordinator/executor).** One (or a few, HA) coordinator plans and schedules;
  many stateless-ish workers execute. *Seen in:* Hadoop YARN, Spark, Flink, HBase, Druid,
  Mesos (historically).
- **MapReduce / split–apply–combine.** Parallelize by mapping over partitions then reducing per
  key. *Seen in:* Hadoop MapReduce, Pig, Crunch, Hive (classic).
- **DAG-based dataflow execution.** Model computation as a directed acyclic graph of operators
  and let the engine schedule/optimize it. *Seen in:* Spark, Flink, Tez, Beam, Airflow, Hop,
  NiFi, Calcite plans.
- **Stream processing with event time & windowing.** Treat data as unbounded streams processed
  with watermarks, windows, and exactly-once state. *Seen in:* Flink, Kafka Streams, Beam,
  Storm, Samza.
- **Bulk-synchronous parallel (BSP).** Iterative graph/ML computation in synchronized
  supersteps. *Seen in:* Giraph, Hama.
- **Separation of storage & compute (disaggregation).** Independently scale stateless compute
  against shared/remote storage. *Seen in:* lakehouse engines, Kyuubi, remote-shuffle services
  (Celeborn, Uniffle), Spark-on-object-store.

### Coordination & reliability patterns

- **Consensus / replicated state machine.** A quorum protocol keeps replicas consistent for
  leader election, metadata, and locks. *Seen in:* ZooKeeper (ZAB), Ratis (Raft), BookKeeper,
  Cassandra (Paxos LWTs).
- **Service discovery + client-side load balancing.** Clients find and balance across service
  instances without a central proxy. *Seen in:* Dubbo, ServiceComb, Curator recipes.
- **Circuit breaker / bulkhead / rate limiting.** Isolate and shed load to prevent cascading
  failure. *Seen in:* Dubbo, ServiceComb, APISIX, ShenYu.

### Integration & extensibility patterns

- **Pipes-and-filters + Enterprise Integration Patterns (EIP).** Compose routing, transformation
  and mediation as a chain of small steps. *Seen in:* Camel, NiFi, ServiceMix, Synapse.
- **Publish/subscribe & event-driven messaging.** Decouple producers from consumers via topics.
  *Seen in:* Kafka, Pulsar, ActiveMQ, RocketMQ, Qpid, EventMesh.
- **Pluggable SPI / provider / adapter.** A stable interface with swappable implementations
  discovered at runtime. *Seen in:* Commons, Calcite adapters, NiFi processors, Lucene codecs,
  Camel components, JDBC-style drivers.
- **Gateway / reverse proxy / sidecar.** A front door that terminates, routes, secures, and
  observes traffic. *Seen in:* HTTP Server, Traffic Server, APISIX, ShenYu, Knox.
- **Schema / IDL + code generation.** Define data contracts once; generate typed code and
  support schema evolution. *Seen in:* Avro, Thrift, Parquet.

### Application & component patterns

- **OSGi modular runtime.** Dynamic, versioned module system with services. *Seen in:* Felix,
  Karaf, Aries.
- **Component-based & front-controller MVC.** Stateful UI components or a single dispatch entry
  point. *Seen in:* Wicket/Tapestry/MyFaces (component), Struts (front controller).
- **Inversion of control / dependency injection & CDI.** *Seen in:* OpenWebBeans, DeltaSpike,
  Aries Blueprint.
- **Content repository + templating.** Hierarchical content store plus server-side rendering.
  *Seen in:* Jackrabbit/Oak + Sling; Velocity/FreeMarker/Tiles.
- **Convention over configuration + declarative lifecycle.** *Seen in:* Maven.
- **Actor model / reactive non-blocking I/O.** Message-passing concurrency and event-loop
  networking. *Seen in:* Pekko, MINA.

---

## Part 2 — The inventory by category

Entries are grouped by primary role. Many projects legitimately span categories (Kafka is
messaging *and* storage; Calcite is a library *and* a SQL engine); each is placed by its
dominant use and cross-referenced where helpful.

### 1. Web serving, proxies & API gateways

*Shared patterns: gateway/reverse-proxy, request pipeline of pluggable modules/filters, event-driven connection handling.*

**Apache HTTP Server ("httpd")** — *C · 🟢 Active*
- **Description:** The original Apache web server (1995), long the world's most widely deployed HTTP server.
- **Function:** Serves static and dynamic content over HTTP/HTTPS; reverse proxy and load balancer.
- **Patterns:** Modular request-processing pipeline (MPMs + hooks), pluggable modules (`mod_*`), config-as-virtual-hosts.
- **Use cases:** Website hosting, reverse proxying app servers, TLS termination, `.htaccess`-driven shared hosting.

**Apache Tomcat** — *Java · 🟢 Active*
- **Description:** Servlet container and reference implementation of Jakarta Servlet/JSP/WebSocket/EL specs.
- **Function:** Runs Java web applications (WAR files); HTTP front end for servlet-based apps.
- **Patterns:** Container/lifecycle management, connector abstraction (BIO/NIO/APR), valve pipeline.
- **Use cases:** Backbone of countless Java web deployments; embedded in Spring Boot via embedded Tomcat.

**Apache Traffic Server (ATS)** — *C++ · 🟢 Active*
- **Description:** High-performance caching proxy server (originated at Inktomi/Yahoo).
- **Function:** Forward/reverse caching proxy and CDN edge cache.
- **Patterns:** Event-driven async I/O, cache hierarchy, plugin SDK.
- **Use cases:** CDN edge, large-scale HTTP caching, traffic offload.

**Apache Traffic Control** — *Go/others · 🗄️ Attic (retiring 2025)*
- **Description:** Control plane to build and operate a CDN on top of Traffic Server.
- **Function:** CDN orchestration, cache assignment, health monitoring.
- **Patterns:** Control-plane/data-plane separation, declarative CDN topology.
- **Use cases:** Operating a private/telco CDN (built originally at Comcast).

**Apache APISIX** — *Lua/Nginx + etcd · 🟢 Active*
- **Description:** Dynamic, high-performance cloud-native API gateway.
- **Function:** API routing, auth, rate limiting, observability, and traffic management at the edge.
- **Patterns:** Gateway + plugin pipeline, hot-reloadable config via etcd, control/data-plane split.
- **Use cases:** Microservice API gateway, Kubernetes ingress, multi-protocol (gRPC/MQTT/Dubbo) gateway.

**Apache ShenYu** — *Java · 🟢 Active*
- **Description:** Reactive, high-performance API gateway.
- **Function:** Request routing, protocol conversion, flow control, and plugin-based mediation.
- **Patterns:** Reactive gateway, plugin chain, divide/selector/rule config model.
- **Use cases:** Microservice gateway for Dubbo/Spring Cloud/gRPC stacks.

**Apache Guacamole** — *Java + C · 🟢 Active*
- **Description:** Clientless remote desktop gateway accessed through a web browser.
- **Function:** Proxies RDP/VNC/SSH to HTML5 in the browser — no client plugin needed.
- **Patterns:** Protocol-translation gateway, stateless web tier + native proxy daemon (`guacd`).
- **Use cases:** Browser-based access to remote machines, jump-host/bastion portals, VDI front ends.

### 2. Application servers, Jakarta EE & OSGi runtimes

*Shared patterns: container-managed lifecycle, dependency injection/CDI, OSGi modularity, specification implementation.*

**Apache TomEE** — *Java · 🟢 Active*
- **Description:** Tomcat plus the Jakarta EE (formerly Java EE) stack — a lightweight certified EE server.
- **Function:** Runs enterprise Java apps needing CDI, JPA, JAX-RS, EJB, JMS on a Tomcat base.
- **Patterns:** Container + specification assembly, profile-based packaging.
- **Use cases:** Enterprise Java apps wanting EE features without a heavyweight server.

**Apache Karaf** — *Java/OSGi · 🟢 Active*
- **Description:** Modular application runtime built on OSGi.
- **Function:** Hosts dynamic, hot-deployable modules ("features") with a shell, provisioning, and management.
- **Patterns:** OSGi modular runtime, feature descriptors, dynamic service registry.
- **Use cases:** Integration/middleware runtimes (often hosting Camel, CXF, ActiveMQ).

**Apache Felix** — *Java/OSGi · 🟢 Active*
- **Description:** Implementation of the OSGi core framework and companion services.
- **Function:** Provides the dynamic module system and service registry for OSGi apps.
- **Patterns:** OSGi bundle lifecycle, service-oriented component model (Declarative Services).
- **Use cases:** Embedded module systems; foundation under Karaf, Sling, and many products.

**Apache Aries** — *Java/OSGi · 🟢 Active*
- **Description:** Enterprise programming-model components for OSGi (Blueprint, JPA, JNDI, transactions).
- **Function:** Brings EE-style services into OSGi runtimes.
- **Patterns:** Blueprint IoC container, OSGi enterprise service abstractions.
- **Use cases:** Enterprise OSGi applications; used inside Karaf.

**Apache OpenWebBeans** — *Java · 🟢 Active*
- **Description:** Implementation of Jakarta Contexts & Dependency Injection (CDI).
- **Function:** Managed-bean lifecycle, injection, events, interceptors.
- **Patterns:** Dependency injection/IoC, contextual instances, decorator/interceptor.
- **Use cases:** CDI engine inside TomEE and standalone CDI apps.

**Apache DeltaSpike** — *Java · 🟢 Active*
- **Description:** A collection of portable CDI extensions.
- **Function:** Adds config, data (repositories), security, scheduling, and test control on top of CDI.
- **Patterns:** CDI portable extension, repository pattern, cross-cutting concerns.
- **Use cases:** Reusable building blocks for CDI-based enterprise apps.

**Apache Johnzon** — *Java · 🟢 Active*
- **Description:** Implementation of JSON-P and JSON-B (Jakarta JSON Processing/Binding).
- **Function:** Parse/generate and bind JSON in Java.
- **Patterns:** Streaming + object-model parsing, mapper.
- **Use cases:** JSON handling in Jakarta EE stacks.

**Apache Geronimo** — *Java · 🟡 Low activity*
- **Description:** Java/Jakarta EE server and a set of EE spec API JARs.
- **Function:** Historically a full EE server; today mainly a trusted source of spec API artifacts.
- **Patterns:** Specification implementation, assembly of EE services.
- **Use cases:** EE spec JARs consumed by many other projects.

### 3. Java web / UI frameworks & templating

*Shared patterns: MVC/front-controller, component-based UI, server-side templating (template method).*

**Apache Struts** — *Java · 🟢 Active*
- **Description:** Action-based MVC web framework (Struts 2).
- **Function:** Maps HTTP requests to actions, handles validation, and renders results.
- **Patterns:** Front-controller MVC, interceptor stack, action/result model.
- **Use cases:** Traditional server-rendered Java web apps.

**Apache Wicket** — *Java · 🟢 Active*
- **Description:** Component-based web framework using plain Java + HTML (no templating language).
- **Function:** Builds stateful web UIs as trees of Java components bound to markup.
- **Patterns:** Component-based UI, stateful server-side component tree.
- **Use cases:** Complex, form-heavy enterprise web apps written mostly in Java.

**Apache Tapestry** — *Java · 🟢 Active*
- **Description:** Component-oriented web framework emphasizing live class reloading and convention.
- **Function:** Page/component-based web development with strong IoC.
- **Patterns:** Component-based UI, convention over configuration, DI container.
- **Use cases:** Productive Java web apps with fast dev feedback.

**Apache MyFaces** — *Java · 🟢 Active*
- **Description:** Implementation of Jakarta Server Faces (JSF).
- **Function:** Server-side, component-based UI framework with managed lifecycle.
- **Patterns:** Component tree, request lifecycle phases, renderer SPI.
- **Use cases:** JSF applications; alternative to the reference implementation.

**Apache Velocity** — *Java · 🟢 Active*
- **Description:** Simple, general-purpose template engine with its own template language (VTL).
- **Function:** Merges a data model into text templates (HTML, source code, email, config).
- **Patterns:** Template method, model–view separation, pluggable resource loaders.
- **Use cases:** Email/report generation, code generation, server-side views.

**Apache FreeMarker** — *Java · 🟢 Active*
- **Description:** Rich, widely used Java template engine.
- **Function:** Generates text output (HTML, config, source) from templates + data model.
- **Patterns:** Template method, expression language, macro/library composition.
- **Use cases:** Web views, codegen, document and config generation.

**Apache Tiles** — *Java · 🗄️ Attic*
- **Description:** Templating/layout composition framework for web pages.
- **Function:** Assembles pages from reusable layout fragments.
- **Patterns:** Composite view, template inheritance.
- **Use cases:** Legacy Struts/JSP layout reuse. *(Superseded; retired.)*

**Apache Royale** — *ActionScript/MXML · 🟢 Active*
- **Description:** Successor to Adobe/Apache Flex; builds apps from MXML/ActionScript that compile to JS/HTML.
- **Function:** Cross-platform application UI without the Flash runtime.
- **Patterns:** Component-based UI, compile-to-JavaScript, MVC.
- **Use cases:** Migrating legacy Flex apps to the browser; rich internet applications.

**Apache Flex** — *ActionScript · 🗄️ Attic*
- **Description:** The original Flex SDK (donated by Adobe) for Flash-based RIAs.
- **Function:** Rich browser/desktop UIs on the Flash/AIR runtime.
- **Patterns:** Component-based UI, declarative MXML.
- **Use cases:** Legacy RIAs. *(Flash's deprecation drove the move to Royale.)*

**Apache Turbine** — *Java · 🟡 Low activity*
- **Description:** Servlet-based web application framework and service container.
- **Function:** Page/action-based web apps with pluggable services.
- **Patterns:** Service locator, pull-MVC.
- **Use cases:** Older service-oriented Java web apps.

### 4. Storage formats & serialization

*Shared patterns: schema/IDL + codegen, schema evolution, columnar layout, zero-copy/compression.*

**Apache Avro** — *Multi-language · 🟢 Active*
- **Description:** Compact binary row-oriented data serialization system with a JSON-defined schema.
- **Function:** Serialize records with embedded/evolvable schemas for storage and messaging.
- **Patterns:** Schema + IDL, schema evolution (reader/writer schemas), self-describing containers.
- **Use cases:** Kafka message payloads, Hadoop data interchange, RPC.

**Apache Parquet** — *Java/C++ · 🟢 Active*
- **Description:** Columnar on-disk storage format for analytics.
- **Function:** Stores tabular data by column with encoding/compression and predicate pushdown.
- **Patterns:** Columnar storage, nested (Dremel) encoding, metadata footers for pruning.
- **Use cases:** Data-lake tables, the physical format under Iceberg/Hudi/Hive/Spark.

**Apache ORC** — *Java/C++ · 🟢 Active*
- **Description:** Optimized Row Columnar file format, originally for Hive.
- **Function:** Columnar storage with lightweight indexes and ACID support hooks.
- **Patterns:** Columnar storage, stripe/stride indexing, built-in statistics.
- **Use cases:** Hive/Spark warehouse tables, especially in the Hadoop ecosystem.

**Apache Arrow** — *Multi-language · 🟢 Active*
- **Description:** Language-independent **in-memory** columnar format plus libraries.
- **Function:** Zero-copy columnar data sharing and fast analytical compute across languages/processes.
- **Patterns:** Columnar in-memory layout, zero-copy IPC, Flight (gRPC data transport).
- **Use cases:** Pandas/Polars/Spark interchange, query-engine internals, Flight data services.

**Apache Thrift** — *Multi-language · 🟢 Active*
- **Description:** Interface definition language + RPC framework (from Facebook).
- **Function:** Defines services/types in an IDL and generates clients/servers in many languages.
- **Patterns:** IDL + codegen, pluggable transport/protocol layers.
- **Use cases:** Polyglot RPC, cross-language data serialization.

**Apache Fory (formerly Fury)** — *Java/Multi-language · 🟢 Active*
- **Description:** Blazing-fast multi-language serialization using JIT and zero-copy.
- **Function:** High-throughput object serialization as a drop-in for slower serializers.
- **Patterns:** Runtime code generation, schema-consistent/compatible modes, zero-copy.
- **Use cases:** RPC payloads, caching, data transfer hot paths. *(Renamed Fury → Fory in 2025; now a top-level project.)*

### 5. Batch & stream processing engines

*Shared patterns: DAG execution, master/worker, event-time windowing, checkpointing/exactly-once.*

**Apache Hadoop** — *Java · 🟢 Active*
- **Description:** Foundational big-data platform: **HDFS** (distributed file system), **YARN** (resource manager), and **MapReduce**.
- **Function:** Reliable storage and batch computation across commodity clusters.
- **Patterns:** Master/worker, MapReduce, data-locality scheduling, replicated block storage.
- **Use cases:** Data lakes, large-scale ETL, the substrate under Hive/HBase/Spark/Tez.

**Apache Spark** — *Scala/JVM + Python · 🟢 Active*
- **Description:** Unified analytics engine for batch, SQL, streaming, ML, and graph.
- **Function:** In-memory distributed computation over RDD/DataFrame abstractions.
- **Patterns:** DAG execution, resilient distributed datasets (lineage-based recovery), Catalyst optimizer.
- **Use cases:** ETL, data science (PySpark), ML (MLlib), near-real-time (Structured Streaming).

**Apache Flink** — *Java/Scala · 🟢 Active*
- **Description:** Stateful stream-processing engine (with batch as bounded streaming).
- **Function:** Low-latency, exactly-once processing of unbounded data with large managed state.
- **Patterns:** Event-time + watermarks, checkpointing/savepoints, dataflow DAG.
- **Use cases:** Real-time analytics, fraud/anomaly detection, CEP, streaming ETL.

**Apache Beam** — *Java/Python/Go · 🟢 Active*
- **Description:** Unified programming model for batch + streaming, portable across runners.
- **Function:** Write pipelines once, run on Flink/Spark/Dataflow, etc.
- **Patterns:** Unified batch/stream model, pluggable runner SPI, windowing/triggers.
- **Use cases:** Portable data pipelines, multi-engine environments.

**Apache Storm** — *Clojure/Java · 🟢 Active*
- **Description:** Distributed real-time computation ("streaming before streaming was cool").
- **Function:** Processes unbounded tuple streams with at-least/exactly-once guarantees.
- **Patterns:** Spouts/bolts topology (DAG), record-at-a-time streaming.
- **Use cases:** Real-time ETL, continuous computation. *(Largely succeeded by Flink in new builds.)*

**Apache Tez** — *Java · 🟢 Active*
- **Description:** DAG execution engine on YARN, a faster replacement for MapReduce.
- **Function:** Runs complex data-processing DAGs for higher-level tools.
- **Patterns:** DAG execution, dynamic graph reconfiguration, container reuse.
- **Use cases:** Execution engine under Hive and Pig.

**Apache Samza** — *Java/Scala · 🟢 Active*
- **Description:** Stream-processing framework tightly integrated with Kafka (from LinkedIn).
- **Function:** Stateful stream processing with local state and changelog fault tolerance.
- **Patterns:** Partitioned local state + changelog, stream/table duality.
- **Use cases:** High-throughput Kafka-centric stream processing.

**Apache Gluten** — *C++/Java · 🟢 Active (TLP, 2026)*
- **Description:** "Middle layer" that offloads JVM SQL engines to native vectorized backends (Velox/ClickHouse).
- **Function:** Accelerates Spark SQL by executing operators natively instead of on the JVM.
- **Patterns:** Vectorized/native execution offload, columnar (Arrow) interchange, plugin backend.
- **Use cases:** Speeding up existing Spark workloads with little code change.

**Apache Pig** — *Java · 🟡 Low activity*
- **Description:** High-level dataflow language ("Pig Latin") compiling to MapReduce/Tez.
- **Function:** Expresses ETL transformations more concisely than raw MapReduce.
- **Patterns:** Dataflow scripting, logical→physical plan compilation.
- **Use cases:** Legacy Hadoop ETL pipelines.

**Apache Celeborn** — *Scala/Java · 🟢 Active*
- **Description:** Intermediate data (remote shuffle) service for Spark/Flink/MapReduce.
- **Function:** Offloads shuffle/spill data to a dedicated service for stability at scale.
- **Patterns:** Disaggregated shuffle, push-based shuffle, storage/compute separation.
- **Use cases:** Large/elastic (Kubernetes) Spark clusters needing reliable shuffle.

**Apache Uniffle** — *Java · 🟢 Active*
- **Description:** Unified remote shuffle service for distributed compute engines.
- **Function:** Externalizes shuffle data (similar goal to Celeborn).
- **Patterns:** Remote/disaggregated shuffle, pluggable storage.
- **Use cases:** Shuffle-heavy Spark/MapReduce/Tez jobs on elastic infrastructure.

**Apache Crunch** — *Java · 🗄️ Attic*
- **Description:** Java library for writing MapReduce pipelines.
- **Function:** Typed pipeline API over MapReduce/Spark.
- **Patterns:** Pipeline combinators (FlumeJava-style).
- **Use cases:** Legacy Hadoop pipelines.

### 6. SQL engines, query frameworks & lakehouse

*Shared patterns: cost-based optimization, pluggable adapters, open table formats, catalog abstraction, MPP scatter-gather.*

**Apache Hive** — *Java · 🟢 Active*
- **Description:** SQL-on-Hadoop data warehouse with the de-facto **Hive Metastore**.
- **Function:** Compiles SQL (HiveQL) to distributed jobs; central metadata catalog.
- **Patterns:** SQL→DAG compilation, metastore catalog, partitioning.
- **Use cases:** Batch warehousing on data lakes; the Metastore underpins Spark/Trino/Presto.

**Apache Calcite** — *Java · 🟢 Active*
- **Description:** Framework for building SQL parsers, optimizers, and federated query engines.
- **Function:** Provides SQL parsing, relational algebra, and a cost-based optimizer as a library.
- **Patterns:** Volcano/cost-based optimizer, pluggable adapters, relational algebra IR.
- **Use cases:** The query brain inside Flink SQL, Druid, Hive, Beam SQL, and many engines.

**Apache Impala** — *C++/Java · 🟢 Active*
- **Description:** Massively parallel (MPP) SQL engine for Hadoop data.
- **Function:** Low-latency interactive SQL directly over HDFS/Kudu/object storage.
- **Patterns:** MPP scatter-gather, LLVM codegen, columnar scans.
- **Use cases:** Interactive BI/ad-hoc analytics on lake data.

**Apache Drill** — *Java · 🟢 Active*
- **Description:** Schema-free SQL query engine for files, NoSQL, and more.
- **Function:** Query JSON/Parquet/CSV/HBase without predefined schemas.
- **Patterns:** Schema-on-read, columnar execution, pluggable storage.
- **Use cases:** Ad-hoc exploration across heterogeneous sources.

**Apache Phoenix** — *Java · 🟢 Active*
- **Description:** Relational SQL layer over Apache HBase.
- **Function:** Turns HBase into an OLTP-ish SQL store with secondary indexes.
- **Patterns:** SQL skin over key-value store, coprocessor pushdown.
- **Use cases:** Low-latency SQL access to HBase data.

**Apache Kylin** — *Java · 🟢 Active*
- **Description:** Distributed OLAP engine using precomputed cubes.
- **Function:** Sub-second multidimensional analytics over huge datasets.
- **Patterns:** Precomputed OLAP cube, dimensional modeling, materialization.
- **Use cases:** BI dashboards needing constant-time aggregate queries.

**Apache Kyuubi** — *Scala · 🟢 Active*
- **Description:** Multi-tenant gateway for serverless SQL on Spark/Flink/Trino.
- **Function:** Provides JDBC/Thrift SQL endpoints with isolation and resource sharing.
- **Patterns:** Storage/compute separation, engine multiplexing, gateway.
- **Use cases:** Enterprise "SQL as a service" over lakehouse engines.

**Apache DataFusion** — *Rust · 🟢 Active (TLP, 2024)*
- **Description:** Fast, extensible query engine and execution framework built on Arrow (a Rust library + the Ballista distributed engine).
- **Function:** Embeddable SQL/DataFrame engine with a vectorized columnar executor.
- **Patterns:** Columnar vectorized execution, extensible optimizer, embeddable engine.
- **Use cases:** Building custom databases/engines in Rust; fast in-process analytics.

**Apache Iceberg** — *Java/Multi-language · 🟢 Active*
- **Description:** Open table format for huge analytic datasets.
- **Function:** Adds ACID snapshots, schema/partition evolution, and time travel over data-lake files.
- **Patterns:** Open table format, snapshot isolation (MVCC), hidden partitioning, catalog abstraction.
- **Use cases:** Lakehouse tables queried by Spark/Flink/Trino/Dremio/Snowflake.

**Apache Hudi** — *Java · 🟢 Active*
- **Description:** Transactional data-lake storage with upserts and incremental processing.
- **Function:** Mutable lake tables (copy-on-write / merge-on-read) with record-level updates.
- **Patterns:** Open table format, LSM-like merge-on-read, incremental "pull" queries.
- **Use cases:** CDC/upsert pipelines into the lake, GDPR deletes, near-real-time tables.

**Apache Paimon** — *Java · 🟢 Active*
- **Description:** Streaming lakehouse format (grew out of Flink Table Store).
- **Function:** Unified streaming + batch lake table with LSM storage and CDC ingestion.
- **Patterns:** LSM table on object store, streaming-first table format, changelog producing.
- **Use cases:** Real-time lakehouse with Flink; streaming updates + batch reads.

**Apache Polaris** — *Java · 🟢 Active (TLP, 2026)*
- **Description:** Open catalog for Apache Iceberg (donated by Snowflake/Dremio).
- **Function:** REST catalog + access control governing Iceberg tables across engines.
- **Patterns:** Catalog abstraction, Iceberg REST catalog API, RBAC over tables.
- **Use cases:** Vendor-neutral, multi-engine governance of lakehouse tables.

**Apache Gravitino** — *Java · 🟢 Active (TLP, 2025)*
- **Description:** Unified metadata lake / multi-catalog metadata management.
- **Function:** One API/governance layer across metastores, catalogs, and data sources.
- **Patterns:** Federated catalog, unified metadata model, governance plane.
- **Use cases:** Cataloging and governing data + AI assets across heterogeneous stores.

**Apache XTable** — *Java · 🥚 Incubating*
- **Description:** Cross-table interoperability between Iceberg, Hudi, and Delta Lake.
- **Function:** Translates table metadata so one dataset is readable as multiple formats.
- **Patterns:** Format interoperability/adapter, metadata translation (no data copy).
- **Use cases:** Avoiding lakehouse format lock-in; multi-engine access to one dataset.

### 7. Databases & data stores

*Shared patterns: sharding, LSM/WAL, tunable consistency, in-memory data grids, time-series compaction.*

**Apache Cassandra** — *Java · 🟢 Active*
- **Description:** Wide-column, masterless distributed NoSQL database.
- **Function:** Highly available, linearly scalable storage with tunable consistency.
- **Patterns:** Consistent-hashing ring, LSM storage, gossip membership, quorum reads/writes, Paxos LWTs.
- **Use cases:** Always-on, write-heavy workloads across data centers (messaging, IoT, time series).

**Apache HBase** — *Java · 🟢 Active*
- **Description:** Distributed, sorted wide-column store on HDFS (a BigTable clone).
- **Function:** Random real-time read/write access to very large tables.
- **Patterns:** LSM + WAL, region sharding, master/region-server, ZooKeeper coordination.
- **Use cases:** Massive sparse tables, time-series, serving layers (often with Phoenix on top).

**Apache CouchDB** — *Erlang · 🟢 Active*
- **Description:** Document database with HTTP/JSON API and multi-master replication.
- **Function:** Stores JSON documents; syncs offline-first apps.
- **Patterns:** MVCC, append-only B-tree storage, eventual-consistency replication, map/reduce views.
- **Use cases:** Offline-first/mobile sync (with PouchDB), distributed document storage.

**Apache Derby** — *Java · 🟢 Active*
- **Description:** Lightweight, pure-Java embeddable relational database.
- **Function:** Full SQL/JDBC RDBMS that runs in-process or as a small server.
- **Patterns:** Embedded database, ACID transactions.
- **Use cases:** Embedded app storage, testing, prototyping (shipped in the JDK as JavaDB).

**Apache Ignite** — *Java · 🟢 Active*
- **Description:** Distributed in-memory computing platform / data grid.
- **Function:** In-memory key-value + SQL store with compute, caching, and persistence.
- **Patterns:** In-memory data grid, affinity colocation, distributed SQL, durable memory.
- **Use cases:** Caching/acceleration layers, HTAP, in-memory compute.

**Apache Geode** — *Java · 🟢 Active*
- **Description:** In-memory data grid (the open-source core of GemFire).
- **Function:** Low-latency distributed data management with event notifications.
- **Patterns:** In-memory data grid, partitioned/replicated regions, continuous queries.
- **Use cases:** High-throughput, low-latency transactional caching (finance, trading).

**Apache Accumulo** — *Java · 🟢 Active*
- **Description:** Sorted, distributed key-value store (BigTable design) with cell-level security.
- **Function:** Secure large-scale storage with per-cell access labels.
- **Patterns:** LSM + WAL, iterators (server-side compute), cell-level visibility labels.
- **Use cases:** Security-sensitive big-data (originated at the NSA), fine-grained access control.

**Apache Kudu** — *C++ · 🟢 Active*
- **Description:** Columnar storage engine for fast analytics on fast-changing data.
- **Function:** Combines low-latency random access with efficient columnar scans.
- **Patterns:** Hybrid row/columnar, Raft-replicated tablets, storage/compute separation (with Impala).
- **Use cases:** Real-time analytics where data mutates and must also scan fast.

**Apache IoTDB** — *Java · 🟢 Active*
- **Description:** Time-series database purpose-built for IoT device data.
- **Function:** Ingests and queries high-frequency sensor time series with heavy compression.
- **Patterns:** LSM-style TsFile storage, time-partitioned schema tree, edge-cloud collaboration.
- **Use cases:** Industrial IoT, telemetry, device monitoring at scale.

**Apache Doris** — *C++/Java · 🟢 Active*
- **Description:** Real-time MPP analytical (OLAP) database, MySQL-protocol compatible.
- **Function:** Sub-second analytics with high-concurrency serving.
- **Patterns:** MPP, columnar + vectorized execution, materialized views, tablet sharding.
- **Use cases:** Real-time dashboards, ad-hoc OLAP, user-facing analytics.

**Apache ShardingSphere** — *Java · 🟢 Active*
- **Description:** Distributed database middleware ecosystem (JDBC driver + proxy).
- **Function:** Adds sharding, read/write splitting, encryption, and distributed transactions over existing databases.
- **Patterns:** Transparent sharding, SQL routing/rewriting, pluggable governance.
- **Use cases:** Scaling MySQL/PostgreSQL horizontally without rewriting apps.

### 8. Messaging, streaming platforms & integration

*Shared patterns: publish/subscribe, append-only log, EIP pipes-and-filters, broker/queue, protocol bridging.*

**Apache Kafka** — *Java/Scala · 🟢 Active*
- **Description:** Distributed event streaming platform (durable, partitioned commit log).
- **Function:** High-throughput pub/sub + storage of event streams; **Kafka Streams** and **Connect** add processing/integration.
- **Patterns:** Append-only partitioned log, consumer groups, pull-based consumption, log compaction; modern KRaft (Raft) metadata.
- **Use cases:** Event backbones, log aggregation, stream processing, CDC, microservice eventing.

**Apache Pulsar** — *Java · 🟢 Active*
- **Description:** Cloud-native distributed messaging + streaming with tiered storage.
- **Function:** Unified queuing and streaming with multi-tenancy and geo-replication.
- **Patterns:** Broker/stateful-storage separation (BookKeeper), segment-centric storage, tiered offload.
- **Use cases:** Multi-tenant messaging, geo-replicated event streaming, unified queue+stream.

**Apache ActiveMQ** — *Java · 🟢 Active*
- **Description:** Popular JMS message broker; **Artemis** is the high-performance next generation.
- **Function:** Reliable queue/topic messaging with many protocol connectors (AMQP, MQTT, STOMP).
- **Patterns:** Broker + queues/topics, store-and-forward, protocol gateways.
- **Use cases:** Enterprise messaging/JMS, IoT (MQTT), system integration.

**Apache RocketMQ** — *Java · 🟢 Active*
- **Description:** Low-latency, high-throughput distributed messaging (from Alibaba).
- **Function:** Transactional, ordered, and scheduled messaging plus streaming.
- **Patterns:** Append log storage, name-server discovery, transactional messages.
- **Use cases:** E-commerce-scale order/transaction eventing, financial messaging.

**Apache Qpid** — *Java/C++ · 🟢 Active*
- **Description:** Messaging built on the AMQP standard.
- **Function:** AMQP brokers and client libraries.
- **Patterns:** Standardized wire protocol (AMQP), broker + clients.
- **Use cases:** Interoperable, standards-based enterprise messaging.

**Apache Camel** — *Java · 🟢 Active*
- **Description:** The leading integration framework implementing the Enterprise Integration Patterns; includes **Camel K** (Kubernetes) and **Camel Quarkus**.
- **Function:** Routes and transforms messages between 300+ systems via a routing DSL.
- **Patterns:** Pipes-and-filters, EIP catalog, component/endpoint SPI, DSL-defined routes.
- **Use cases:** System-to-system integration, API/protocol mediation, ETL glue.

**Apache ServiceMix** — *Java · 🟡 Low activity*
- **Description:** OSGi-based enterprise service bus (ESB) assembling Karaf + Camel + CXF + ActiveMQ.
- **Function:** Integration container bundling ASF integration projects.
- **Patterns:** ESB, OSGi runtime assembly.
- **Use cases:** Legacy ESB deployments. *(Most new work uses Camel directly.)*

**Apache Synapse** — *Java · 🟡 Low activity*
- **Description:** Lightweight ESB and XML/web-services mediation engine.
- **Function:** Routing, transformation, and mediation of SOAP/REST traffic.
- **Patterns:** Mediation sequences, EIP, proxy services.
- **Use cases:** Web-services mediation/gateway (historically under WSO2).

**Apache EventMesh** — *Java · 🟢 Active*
- **Description:** Cloud-native event middleware / "event mesh."
- **Function:** Decouples producers/consumers across clouds with eventing, orchestration, and connectors.
- **Patterns:** Event mesh, pub/sub abstraction over multiple stores, serverless eventing.
- **Use cases:** Distributed, multi-cloud event-driven architectures.

### 9. RPC, microservices & service frameworks

*Shared patterns: IDL + codegen, service discovery, client-side load balancing, circuit breaking.*

**Apache Dubbo** — *Java · 🟢 Active*
- **Description:** High-performance RPC and microservice framework (from Alibaba).
- **Function:** Remote service invocation with registry-based discovery and governance.
- **Patterns:** RPC proxy/stub, service discovery, client-side load balancing, SPI extensibility.
- **Use cases:** Large-scale Java microservice fabrics, service governance.

**Apache ServiceComb** — *Java · 🟢 Active*
- **Description:** Microservices framework (service center, config, contracts).
- **Function:** Service registration/discovery, contract-first APIs, resilience.
- **Patterns:** Service mesh/registry, contract-first (OpenAPI), circuit breaking.
- **Use cases:** Building and governing microservice systems.

**Apache bRPC** — *C++ · 🟢 Active*
- **Description:** Industrial-grade C++ RPC framework (from Baidu).
- **Function:** High-concurrency RPC with rich protocol support and built-in profiling.
- **Patterns:** RPC with pluggable protocols, M:N threading, built-in observability.
- **Use cases:** Performance-critical C++ services (search, storage, ML serving).

**Apache Avro RPC / Thrift** — *(see [§4](#4-storage-formats--serialization))*
- Both double as cross-language RPC frameworks via their IDL + codegen model.

### 10. Coordination, consensus & cluster management

*Shared patterns: replicated state machine (Paxos/Raft/ZAB), leader election, distributed log, cluster scheduling.*

**Apache ZooKeeper** — *Java · 🟢 Active*
- **Description:** Centralized service for configuration, naming, synchronization, and group membership.
- **Function:** Provides a consistent, watchable hierarchical namespace (znodes) for coordination.
- **Patterns:** Replicated state machine (ZAB), leader election, watches/ephemeral nodes.
- **Use cases:** Coordination backbone for HBase, Kafka (legacy), Solr, and countless distributed systems.

**Apache Curator** — *Java · 🟢 Active*
- **Description:** High-level ZooKeeper client with recipes.
- **Function:** Robust connection handling plus ready-made distributed primitives (locks, leader election, queues).
- **Patterns:** Recipe library over ZooKeeper, retry/connection-state management.
- **Use cases:** Anything using ZooKeeper that wants correct, reusable coordination primitives.

**Apache BookKeeper** — *Java · 🟢 Active*
- **Description:** Scalable, low-latency distributed storage for append-only logs ("ledgers"); includes **DistributedLog**.
- **Function:** Durable, replicated write-ahead log as a service.
- **Patterns:** Replicated append-only ledgers, quorum writes, segment storage.
- **Use cases:** Durable storage layer under Pulsar; WAL-as-a-service, stream storage.

**Apache Ratis** — *Java · 🟢 Active*
- **Description:** Java library implementing the Raft consensus protocol.
- **Function:** Embeddable consensus for building replicated state machines.
- **Patterns:** Raft (leader election + replicated log), pluggable state machine/transport.
- **Use cases:** Consensus inside Ozone, IoTDB, and other systems needing strong consistency.

**Apache Helix** — *Java · 🟢 Active*
- **Description:** Generic cluster-management framework (from LinkedIn).
- **Function:** Assigns partitions/replicas to nodes and manages state transitions and failover.
- **Patterns:** Declarative state model + constraints, controller-driven assignment.
- **Use cases:** Managing partitioned/replicated distributed systems (used by Pinot, Gobblin).

**Apache Ambari** — *Java · 🟢 Active (revived)*
- **Description:** Provisioning, management, and monitoring tool for Hadoop clusters.
- **Function:** Installs, configures, and monitors the Hadoop ecosystem via a web UI/REST API.
- **Patterns:** Agent/server management, blueprint-based provisioning, metrics aggregation.
- **Use cases:** Operating on-prem Hadoop clusters. *(Approached the Attic, then revived by its community.)*

**Apache Bigtop** — *Java/packaging · 🟢 Active*
- **Description:** Packaging, testing, and distribution of the Hadoop big-data stack.
- **Function:** Builds and integration-tests a coherent set of ecosystem components.
- **Patterns:** Build/packaging pipeline, smoke-test harness.
- **Use cases:** Creating a vendor-neutral Hadoop distribution.

**Apache Mesos** — *C++ · 🗄️ Attic*
- **Description:** Cluster resource manager abstracting CPU/memory across machines ("datacenter kernel").
- **Function:** Two-level scheduling offering resources to frameworks (Marathon, Aurora, Spark).
- **Patterns:** Two-level scheduling, resource offers, master/agent.
- **Use cases:** Large-scale cluster scheduling. *(Eclipsed by Kubernetes; retired 2021.)*

### 11. Search & information retrieval

*Shared patterns: inverted index, scatter-gather distributed search, analysis/token pipelines, crawler frontier.*

**Apache Lucene** — *Java · 🟢 Active*
- **Description:** The foundational full-text search library.
- **Function:** Builds and queries inverted indexes with ranking, analysis, and (now) vector search.
- **Patterns:** Inverted index, segment-based immutable index + merge, analyzer pipeline, pluggable codecs.
- **Use cases:** Embedded search; the engine under Solr, Elasticsearch/OpenSearch.

**Apache Solr** — *Java · 🟢 Active*
- **Description:** Distributed search platform built on Lucene.
- **Function:** REST/JSON search server with faceting, sharding, and replication (SolrCloud).
- **Patterns:** Scatter-gather distributed search, sharding/replication via ZooKeeper, schema + request handlers.
- **Use cases:** Site/enterprise search, faceted navigation, log/analytics search.

**Apache Nutch** — *Java · 🟢 Active*
- **Description:** Scalable, extensible web crawler (Lucene/Hadoop lineage).
- **Function:** Crawls, parses, and indexes web content at scale.
- **Patterns:** Crawler frontier (generate/fetch/parse/update cycle), plugin architecture, MapReduce crawling.
- **Use cases:** Building search indexes, web-scale data harvesting (progenitor of Hadoop).

**Apache StormCrawler** — *Java · 🟢 Active (TLP, 2025)*
- **Description:** SDK for building low-latency, scalable web crawlers on Apache Storm.
- **Function:** Stream-based crawling as configurable Storm topologies.
- **Patterns:** Streaming crawl pipeline, component SPI.
- **Use cases:** Continuous/near-real-time crawling and scraping.

**Apache ManifoldCF** — *Java · 🟢 Active*
- **Description:** Connector framework for pulling content from repositories into search engines, honoring security.
- **Function:** Crawls SharePoint/filesystems/CMSes and propagates access controls to the index.
- **Patterns:** Connector SPI, security-token propagation, incremental crawl.
- **Use cases:** Secure enterprise content ingestion into Solr/Elasticsearch.

**Apache Lucene.NET** / **PyLucene** — *C#/Python · 🟢 Active*
- **Description:** .NET port and Python bindings of Lucene.
- **Use cases:** Lucene search in non-JVM applications.

### 12. Content, NLP & document processing

*Shared patterns: detector/parser chains, pluggable format handlers, statistical/ML models, streaming parse.*

**Apache Tika** — *Java · 🟢 Active*
- **Description:** Content detection and text/metadata extraction toolkit ("babelfish" for files).
- **Function:** Detects file type and extracts text + metadata from 1,000+ formats.
- **Patterns:** Detector + parser chain, SPI per format, SAX-style streaming.
- **Use cases:** Search ingestion pipelines, data-loss prevention, document analysis.

**Apache PDFBox** — *Java · 🟢 Active*
- **Description:** Library for creating, manipulating, and extracting from PDF documents.
- **Function:** Read/write PDFs, extract text, fill forms, sign, render pages.
- **Patterns:** Document object model, content-stream parsing.
- **Use cases:** PDF generation/parsing, text extraction (used by Tika), form processing.

**Apache POI** — *Java · 🟢 Active*
- **Description:** Pure-Java API for Microsoft Office formats (XLS/XLSX, DOC/DOCX, PPT/PPTX).
- **Function:** Read and write Office documents programmatically.
- **Patterns:** Format-specific object models (HSSF/XSSF, etc.), streaming (SXSSF) for large files.
- **Use cases:** Server-side spreadsheet/report generation, Office data extraction.

**Apache OpenNLP** — *Java · 🟢 Active*
- **Description:** Machine-learning toolkit for natural-language processing.
- **Function:** Tokenization, sentence detection, POS tagging, NER, parsing.
- **Patterns:** Statistical/ML models, pipeline of annotators, trainable components.
- **Use cases:** Text analytics, entity extraction, language processing pipelines.

**Apache FOP (Formatting Objects Processor)** — *Java · 🟢 Active*
- **Description:** Print formatter driven by XSL-FO, part of **XML Graphics**.
- **Function:** Converts XSL-FO (and via XSLT, XML) into PDF, PS, and other print formats.
- **Patterns:** Declarative layout (XSL-FO), renderer SPI.
- **Use cases:** Server-side PDF/print generation from XML data.

**Apache Batik** — *Java · 🟢 Active*
- **Description:** Toolkit for Scalable Vector Graphics (SVG), part of **XML Graphics**.
- **Function:** Render, generate, and manipulate SVG; rasterize to images.
- **Patterns:** DOM-based graphics, renderer/transcoder.
- **Use cases:** SVG rendering, chart/image export, document graphics.

**Apache cTAKES** — *Java · 🟢 Active*
- **Description:** Clinical NLP system for extracting information from electronic medical records.
- **Function:** Pipeline (on UIMA) that recognizes clinical entities and relations.
- **Patterns:** UIMA annotator pipeline, dictionary + ML extraction.
- **Use cases:** Healthcare/biomedical text mining.

**Apache UIMA** — *Java/C++ · 🟢 Active*
- **Description:** Unstructured Information Management Architecture — a framework for analyzing unstructured content.
- **Function:** Composes analysis engines that annotate text/audio/video with a common type system.
- **Patterns:** Annotator pipeline, common analysis structure (CAS), SPI.
- **Use cases:** NLP/content-analytics platforms (foundation under cTAKES; famously used in IBM Watson).

### 13. Workflow orchestration & scheduling

*Shared patterns: DAG-of-tasks, scheduler + executor, declarative pipeline definition, dependency resolution.*

**Apache Airflow** — *Python · 🟢 Active*
- **Description:** The de-facto platform to programmatically author, schedule, and monitor workflows.
- **Function:** Defines pipelines as Python DAGs; schedules, retries, and tracks task runs.
- **Patterns:** DAG-of-tasks, scheduler/executor split, operator/provider plugin model.
- **Use cases:** Data-engineering ETL orchestration, ML pipelines, batch job scheduling.

**Apache DolphinScheduler** — *Java · 🟢 Active*
- **Description:** Visual, distributed workflow scheduler.
- **Function:** Drag-and-drop DAG authoring with distributed, HA execution.
- **Patterns:** DAG scheduling, decentralized master/worker, visual definition.
- **Use cases:** Data pipeline orchestration with a low-code UI; big-data task scheduling.

**Apache Oozie** — *Java · 🗄️ Attic*
- **Description:** Workflow scheduler for Hadoop jobs.
- **Function:** Coordinates MapReduce/Pig/Hive jobs by time and data availability.
- **Patterns:** XML-defined DAG + coordinators, data-trigger scheduling.
- **Use cases:** Legacy Hadoop job orchestration. *(Retired to the Attic, 2025.)*

**Apache Liminal** — *Python · 🗄️ Attic*
- **Description:** End-to-end MLOps workflow DSL.
- **Use cases:** ML training/serving pipelines. *(Retired.)*

### 14. Machine learning & AI

*Shared patterns: tensor dataflow graphs, distributed training (data/model parallelism), declarative ML pipelines, compiler IRs.*

**Apache SystemDS** — *Java/Scala · 🟢 Active*
- **Description:** ML systems platform for the end-to-end data-science lifecycle (successor to SystemML).
- **Function:** Declarative ML with automatic optimization across scales (single node → cluster).
- **Patterns:** Declarative linear algebra, cost-based execution-plan compilation.
- **Use cases:** Scalable ML pipelines, feature engineering, custom algorithms.

**Apache SINGA** — *C++/Python · 🟢 Active*
- **Description:** Distributed deep-learning library.
- **Function:** Trains neural networks across devices/nodes.
- **Patterns:** Tensor dataflow, distributed training, device abstraction.
- **Use cases:** Deep learning (notably healthcare/medical imaging research).

**Apache Mahout** — *Java/Scala · 🟢 Active*
- **Description:** Distributed linear-algebra framework and the "Samsara" math DSL (originally classic MapReduce ML).
- **Function:** Mathematically expressive, scalable algebra for ML.
- **Patterns:** Distributed linear algebra, DSL over engines (Spark).
- **Use cases:** Recommenders, clustering, custom distributed math.

**Apache Submarine** — *Java/Python · 🗄️ Attic*
- **Description:** Cloud-native ML platform for running training/notebooks on Kubernetes/YARN.
- **Use cases:** ML platform-as-a-service. *(Retired to the Attic, 2025.)*

**Apache MXNet** — *C++/Python · 🗄️ Attic*
- **Description:** Flexible, efficient deep-learning framework (once an AWS favorite).
- **Patterns:** Hybrid imperative/symbolic graphs, multi-GPU training.
- **Use cases:** Deep learning. *(Retired to the Attic, 2023, as the field consolidated on PyTorch/TensorFlow.)*

**Apache PredictionIO** — *Scala · 🗄️ Attic*
- **Description:** ML server for building predictive engines on Spark.
- **Use cases:** Deployable recommendation/prediction services. *(Retired.)*

**Apache TVM** — *C++/Python · 🟢 Active*
- **Description:** End-to-end deep-learning compiler stack for CPUs, GPUs, and accelerators.
- **Function:** Compiles and optimizes trained models for efficient inference across diverse hardware.
- **Patterns:** Multi-level compiler IR (Relay/TIR), auto-tuning/auto-scheduling, hardware backend SPI.
- **Use cases:** Portable, optimized model deployment; edge/accelerator inference. *(Confirmed active TLP in the live project list.)*

### 15. Graph, geospatial & semantic web

*Shared patterns: graph traversal DSLs, BSP iteration, spatial indexing/partitioning, RDF triple stores + SPARQL.*

**Apache TinkerPop** — *Java · 🟢 Active*
- **Description:** Graph computing framework with the **Gremlin** traversal language.
- **Function:** Vendor-neutral API/DSL for querying property graphs (OLTP traversals + OLAP).
- **Patterns:** Graph traversal DSL, provider SPI (works across many graph databases).
- **Use cases:** Graph querying across JanusGraph, Neptune, etc.; fraud/recommendation graphs.

**Apache Jena** — *Java · 🟢 Active*
- **Description:** Framework for building Semantic Web / Linked Data apps (RDF, SPARQL, OWL).
- **Function:** Store, reason over, and query RDF; **Fuseki** is its SPARQL server; **TDB** its triple store.
- **Patterns:** RDF triple store, SPARQL query engine, rule-based inference.
- **Use cases:** Knowledge graphs, ontologies, linked-data publishing.

**Apache Sedona** — *Java/Scala/Python · 🟢 Active*
- **Description:** Cluster computing system for processing large-scale spatial data.
- **Function:** Spatial SQL, indexing, and partitioning on Spark/Flink.
- **Patterns:** Spatial partitioning + indexing (R-tree/quadtree), distributed spatial joins.
- **Use cases:** Geospatial analytics at scale (mobility, GIS, earth observation).

**Apache SIS (Spatial Information System)** — *Java · 🟢 Active*
- **Description:** Library for geospatial metadata and referencing per OGC/ISO standards.
- **Function:** Coordinate reference systems, projections, and metadata handling.
- **Patterns:** Standards implementation (OGC/ISO), referencing engine.
- **Use cases:** GIS applications needing accurate coordinate transforms/metadata.

**Apache Giraph** — *Java · 🗄️ Attic*
- **Description:** Iterative graph-processing system on Hadoop.
- **Patterns:** Bulk-synchronous parallel (Pregel model), vertex-centric computation.
- **Use cases:** Large-scale graph algorithms (historically Facebook's social graph). *(Retired.)*

### 16. IoT, edge & embedded / RTOS

*Shared patterns: real-time kernels, industrial protocol adapters, edge-to-cloud flow, flow-based programming.*

**Apache NuttX** — *C · 🟢 Active*
- **Description:** Mature real-time operating system (RTOS) with strong POSIX compliance.
- **Function:** Small-footprint OS for microcontrollers to microprocessors.
- **Patterns:** POSIX RTOS, modular driver model, scalable footprint.
- **Use cases:** Embedded/IoT devices, drones, wearables (notably in many consumer devices).

**Apache Mynewt** — *C · 🟢 Active*
- **Description:** Modular RTOS for constrained embedded devices, with a full BLE stack.
- **Function:** OS + package management + bootloader for MCUs.
- **Patterns:** RTOS + package manager, hardware abstraction layer.
- **Use cases:** Bluetooth Low Energy products, resource-constrained IoT.

**Apache PLC4X** — *Java/Go/C · 🟢 Active*
- **Description:** Universal protocol adapters for industrial PLCs (Programmable Logic Controllers).
- **Function:** Uniform API to talk to Modbus/S7/OPC-UA/EtherNet-IP and more.
- **Patterns:** Driver SPI over industrial protocols, uniform read/write/subscribe API.
- **Use cases:** Industry 4.0 / IIoT data acquisition from factory equipment.

**Apache NiFi** — *Java · 🟢 Active*
- **Description:** Dataflow automation tool with a visual, flow-based programming UI; includes **MiNiFi** (edge agent) and **NiFi Registry**.
- **Function:** Routes, transforms, and tracks data between systems with full provenance.
- **Patterns:** Flow-based programming (processors + connections), back-pressure, data provenance lineage.
- **Use cases:** Edge-to-cloud ingestion, IoT collection, ETL, inter-system data logistics.

**Apache StreamPipes** — *Java/TypeScript · 🟢 Active*
- **Description:** Self-service (I)IoT toolbox to connect, analyze, and explore streaming data.
- **Function:** Low-code pipelines over industrial data streams.
- **Patterns:** Pipeline composition, adapters + processing elements SPI.
- **Use cases:** Industrial IoT analytics for domain experts.

**Apache Edgent** — *Java · 🗄️ Attic*
- **Description:** Lightweight edge-analytics runtime (formerly Quarks).
- **Use cases:** On-device stream analytics. *(Retired.)*

### 17. Security, identity & cryptography

*Shared patterns: pluggable realms/providers, policy decision/enforcement points, directory/LDAP, XML/crypto standards.*

**Apache Shiro** — *Java · 🟢 Active*
- **Description:** Simple, comprehensive application security framework.
- **Function:** Authentication, authorization, session management, and cryptography for apps.
- **Patterns:** Pluggable realms, subject/principal model, policy enforcement.
- **Use cases:** Securing Java applications without a heavyweight framework.

**Apache Ranger** — *Java · 🟢 Active*
- **Description:** Centralized security administration and fine-grained authorization for the Hadoop ecosystem.
- **Function:** Defines, enforces, and audits access policies across Hive, HBase, Kafka, etc.
- **Patterns:** Policy decision + enforcement points (plugins), centralized admin + audit.
- **Use cases:** Data-governance and access control across a big-data platform.

**Apache Knox** — *Java · 🟢 Active*
- **Description:** Application gateway for securely accessing Hadoop services.
- **Function:** Single, authenticated REST/HTTP entry point that proxies cluster services.
- **Patterns:** Reverse-proxy gateway, perimeter security, SSO integration.
- **Use cases:** Exposing Hadoop/analytics services safely outside the cluster.

**Apache Syncope** — *Java · 🟢 Active*
- **Description:** Identity management and governance (IdM/IGA) system.
- **Function:** Manages users/roles and provisions identities across connected systems.
- **Patterns:** Identity store + connectors (ConnId), workflow-driven provisioning, policy engine.
- **Use cases:** Enterprise identity lifecycle, provisioning/deprovisioning, governance.

**Apache Directory** — *Java · 🟢 Active*
- **Description:** Family of identity/LDAP projects.
- **Function & modules:**
  - **ApacheDS** — extensible embeddable LDAP + Kerberos server.
  - **LDAP API** — Java LDAP client library.
  - **Studio** — Eclipse-based LDAP browser/IDE.
  - **Kerby** — Kerberos implementation (KDC + tooling).
  - **Fortress** — RBAC/ARBAC authorization platform.
  - **Mavibot** — MVCC B-tree backend.
- **Patterns:** Directory/LDAP, RBAC, MVCC storage, pluggable interceptors.
- **Use cases:** Embedded directories, Kerberos auth, RBAC, LDAP tooling.

**Apache Santuario** — *Java/C++ · 🟢 Active*
- **Description:** Implementation of XML Digital Signature and XML Encryption standards.
- **Function:** Sign/verify and encrypt/decrypt XML.
- **Patterns:** Standards implementation (W3C XML Security).
- **Use cases:** SOAP/WS-Security, signed XML documents, SAML.

**Apache Teaclave** — *Rust · 🥚 Incubating*
- **Description:** Universal secure/confidential computing platform.
- **Function:** Runs computations inside trusted execution environments (e.g., SGX).
- **Patterns:** Confidential computing, function-as-a-service in enclaves, data isolation.
- **Use cases:** Privacy-preserving analytics, multi-party computation on sensitive data.

### 18. Observability & monitoring

*Shared patterns: distributed tracing, metrics time series, agent + collector, topology/service maps.*

**Apache SkyWalking** — *Java · 🟢 Active*
- **Description:** Application performance monitoring (APM) and observability platform for distributed systems.
- **Function:** Distributed tracing, metrics, logs, and service topology (cloud-native, service mesh).
- **Patterns:** Agent + OAP collector, distributed tracing, service dependency maps, OpenTelemetry ingestion.
- **Use cases:** Microservice observability, latency/root-cause analysis.

**Apache HertzBeat** — *Java · 🟢 Active*
- **Description:** Real-time monitoring system with agentless collection and alerting.
- **Function:** Monitors apps/databases/OS/network via configurable (YAML) protocols; threshold alerts.
- **Patterns:** Agentless pull collection, template-defined metrics, alert rules.
- **Use cases:** Infrastructure/service monitoring and alerting without installing agents.

**Apache Flagon** — *JavaScript/Java · 🟢 Active*
- **Description:** User-behavior logging ("UserALE") for software usability analytics.
- **Function:** Captures fine-grained UI interaction telemetry.
- **Patterns:** Event instrumentation + collector.
- **Use cases:** UX research, usability/behavior analytics.

### 19. Cloud, virtualization & container orchestration

*Shared patterns: cloud abstraction layers, control-plane orchestration, Kubernetes scheduling, portable provider APIs.*

**Apache CloudStack** — *Java · 🟢 Active*
- **Description:** Turnkey Infrastructure-as-a-Service (IaaS) cloud orchestration platform.
- **Function:** Manages compute/network/storage to deliver a full private/public cloud.
- **Patterns:** Control plane + hypervisor agents, multi-tenancy, pod/cluster/zone topology.
- **Use cases:** Running on-prem/hosted IaaS clouds (telcos, service providers).

**Apache Libcloud** — *Python · 🟢 Active*
- **Description:** Python library providing one API across many cloud providers.
- **Function:** Abstracts compute/storage/DNS/load-balancer APIs of 50+ clouds.
- **Patterns:** Provider abstraction/adapter, uniform driver interface.
- **Use cases:** Multi-cloud/portable automation scripts and tools.

**Apache jclouds** — *Java · 🗄️ Attic*
- **Description:** Multi-cloud toolkit for Java (compute + blobstore abstraction).
- **Patterns:** Provider abstraction/adapter.
- **Use cases:** Portable Java cloud automation. *(Retired to the Attic.)*

**Apache Brooklyn** — *Java · 🟢 Active*
- **Description:** Framework for modeling, deploying, and managing applications via blueprints.
- **Function:** Autonomic application management across clouds (policy-driven scaling/healing).
- **Patterns:** Declarative blueprints (YAML), autonomic policies, effectors/sensors.
- **Use cases:** Application orchestration and runtime management across infrastructure.

**Apache YuniKorn** — *Go · 🟢 Active*
- **Description:** Resource scheduler for big-data/ML workloads on Kubernetes (and YARN).
- **Function:** Rich hierarchical queue scheduling that Kubernetes' default scheduler lacks.
- **Patterns:** Hierarchical queues, gang scheduling, resource fairness.
- **Use cases:** Running Spark/Flink/ML batch workloads efficiently on Kubernetes.

**Apache Airavata** — *Java · 🟢 Active*
- **Description:** Framework for executing and managing computational jobs on distributed resources (science gateways).
- **Function:** Submits/monitors workflows across HPC clusters, grids, and clouds.
- **Patterns:** Science-gateway middleware, workflow + resource brokering.
- **Use cases:** Research computing portals bridging scientists to supercomputers.

### 20. Build, dependency & release tooling

*Shared patterns: declarative build lifecycle, dependency resolution graph, convention over configuration, artifact repository.*

**Apache Maven** — *Java · 🟢 Active*
- **Description:** The dominant Java build and project-management tool.
- **Function:** Declarative builds with transitive dependency management and a plugin-driven lifecycle.
- **Patterns:** Convention over configuration, declarative lifecycle phases, dependency resolution graph, plugin SPI.
- **Use cases:** Building/packaging/publishing JVM projects; the Maven Central coordinate system.

**Apache Ant** — *Java · 🟢 Active*
- **Description:** Original XML-driven Java build tool (imperative task runner).
- **Function:** Scripts arbitrary build steps as ordered targets/tasks.
- **Patterns:** Imperative task graph, target dependencies.
- **Use cases:** Legacy and highly customized builds; fine-grained control.

**Apache Ivy** — *Java · 🟢 Active*
- **Description:** Dependency manager, typically paired with Ant.
- **Function:** Resolves and retrieves dependencies with flexible configuration.
- **Patterns:** Dependency resolution, pluggable resolvers.
- **Use cases:** Adding Maven-style dependency management to Ant builds.

**Apache Archiva** — *Java · 🟡 Low activity*
- **Description:** Build-artifact repository manager.
- **Function:** Hosts/proxies/caches Maven artifact repositories.
- **Patterns:** Artifact repository + proxy cache.
- **Use cases:** Private internal Maven repositories.

**Apache Maven Doxia / plugins** — *Java · 🟢 Active*
- Sub-projects supplying site generation and the large catalog of core Maven plugins.

**Apache Gump** — *Python · 🟡 Low activity*
- **Description:** Continuous-integration tool that builds projects against the latest of their dependencies.
- **Patterns:** Integration-at-head CI.
- **Use cases:** Early detection of cross-project breakage (ASF-internal heritage).

### 21. Content management, collaboration & portals

*Shared patterns: content repository (JCR), resource-oriented rendering, portlet aggregation, project forge.*

**Apache Jackrabbit** & **Jackrabbit Oak** — *Java · 🟢 Active*
- **Description:** Implementations of the Java Content Repository (JCR) standard; **Oak** is the scalable modern core.
- **Function:** Hierarchical content storage with versioning, search, and fine-grained access.
- **Patterns:** Content repository, MVCC (Oak), pluggable node stores (Mongo/segment).
- **Use cases:** The repository under Adobe Experience Manager and many CMSes.

**Apache Sling** — *Java · 🟢 Active*
- **Description:** RESTful web framework for JCR content repositories.
- **Function:** Maps HTTP requests directly onto content nodes + rendering scripts.
- **Patterns:** Resource-oriented architecture, request→resource→renderer resolution, OSGi-based.
- **Use cases:** Content-centric web applications (basis of AEM).

**Apache Roller** — *Java · 🟢 Active*
- **Description:** Full-featured multi-user blog server.
- **Function:** Hosts many blogs with themes, feeds, and comments.
- **Patterns:** Templated rendering, multi-tenant content.
- **Use cases:** Enterprise/community blogging (long ran blogs.apache.org, Oracle internal).

**Apache Pluto** — *Java · 🟢 Active*
- **Description:** Reference implementation of the Java Portlet Specification.
- **Function:** Portlet container that renders and coordinates portlets.
- **Patterns:** Portlet container, portal aggregation.
- **Use cases:** Testing/running portlets; embedding portlet support.

**Apache Allura** — *Python · 🟢 Active*
- **Description:** Project-hosting ("forge") platform — the software behind SourceForge.
- **Function:** Git/SVN hosting, tickets, wikis, discussions as pluggable tools.
- **Patterns:** Multi-tool forge, plugin tools per project, document-store backend.
- **Use cases:** Running a software forge / project-hosting site.

**Apache Cocoon** — *Java · 🗄️ Attic*
- **Description:** XML-centric web development framework (pipeline-based publishing).
- **Patterns:** XML pipelines (SAX), separation of concerns by pipeline stage.
- **Use cases:** XML publishing. *(Retired to the Attic, 2025.)*

**Apache Jetspeed / Portals** — *Java · 🗄️ Attic*
- **Description:** Enterprise portal platform (the "Portals" umbrella).
- **Use cases:** Portal deployments. *(Retired, 2025.)*

**Apache Wookie** / **Apache Lenya** / **Apache Shindig** — *🗄️ Attic*
- Retired widget-engine, CMS, and OpenSocial-container projects respectively.

### 22. Mobile & rich client

**Apache Cordova** — *JavaScript/native · 🟢 Active*
- **Description:** Framework to build mobile apps with HTML/CSS/JS packaged as native apps.
- **Function:** Wraps web apps in a native WebView and exposes device APIs via plugins.
- **Patterns:** WebView bridge, plugin SPI to native capabilities, write-once/run-many.
- **Use cases:** Cross-platform mobile apps from web skills (basis of PhoneGap/Ionic).

**Apache Weex** — *JavaScript/native · 🗄️ Attic*
- **Description:** Framework for high-performance cross-platform mobile UIs.
- **Use cases:** Native-rendered mobile apps from a web-like syntax. *(Retired.)*

### 23. BI, data visualization & notebooks

*Shared patterns: declarative chart specs, pluggable datasource connectors, interactive notebook REPL, async job sessions.*

**Apache Superset** — *Python/TypeScript · 🟢 Active*
- **Description:** Modern data-exploration and business-intelligence web platform.
- **Function:** SQL IDE, no-code chart builder, and dashboards over any SQL database.
- **Patterns:** Pluggable SQLAlchemy datasources, declarative viz config, semantic layer.
- **Use cases:** Self-service BI, dashboards, data exploration.

**Apache ECharts** — *JavaScript · 🟢 Active*
- **Description:** Powerful, interactive charting and visualization library for the browser.
- **Function:** Renders rich, animated charts (Canvas/SVG) from declarative options.
- **Patterns:** Declarative chart spec, component-based rendering, incremental rendering for big data.
- **Use cases:** Web dashboards, data viz in apps (hugely popular in the JS ecosystem).

**Apache Zeppelin** — *Java/web · 🟢 Active*
- **Description:** Web-based notebook for interactive data analytics.
- **Function:** Multi-language notebooks (Spark/SQL/Python) with built-in visualization.
- **Patterns:** Notebook REPL, pluggable interpreters, paragraph dataflow.
- **Use cases:** Interactive big-data analysis, collaborative data science.

**Apache Livy** — *Scala/Java · 🟡 Low activity*
- **Description:** REST service for submitting and managing Spark jobs/sessions.
- **Function:** Lets apps run Spark code remotely over REST without a local Spark context.
- **Patterns:** Session management, remote job submission, async REST.
- **Use cases:** Backing notebooks/apps with shared Spark sessions.

**Apache Answer** — *Go · 🟢 Active (TLP, 2024)*
- **Description:** Q&A platform software for building knowledge communities (Stack Overflow-style).
- **Function:** Questions/answers, voting, reputation, moderation.
- **Patterns:** Community Q&A, reputation/gamification, plugin extensibility.
- **Use cases:** Support communities, internal knowledge bases, help centers.

### 24. Core libraries — Apache Commons

*Apache Commons is a project dedicated to reusable Java components. Shared pattern: small, focused,
dependency-light utility libraries with stable SPIs. The most widely used components:*

| Component | What it provides |
|-----------|------------------|
| **Commons Lang** | Core `java.lang` helpers: strings, builders, reflection, enums, concurrency utilities. |
| **Commons IO** | Stream/file utilities, file filters, copy/compare helpers. |
| **Commons Collections** | Extra collections, bidi/multi maps, bag/sequence types, decorators. |
| **Commons Math** | Mathematics & statistics (linear algebra, optimization, distributions). *(Later work continues in Commons Numbers/Statistics/Geometry/RNG.)* |
| **Commons CLI** | Command-line argument parsing. |
| **Commons Codec** | Base64/hex, phonetic and digest encoders. |
| **Commons Compress** | Archive/compression (zip, tar, 7z, gzip, bzip2, zstd, …). |
| **Commons Configuration** | Read/merge config from properties/XML/YAML/env. |
| **Commons CSV** | Read/write CSV variants. |
| **Commons DBCP** + **Pool** | JDBC connection pooling and generic object pooling. |
| **Commons BeanUtils** | Reflection-based JavaBean property access. |
| **Commons Logging** | Thin logging facade (historical). |
| **Commons Net** | Client implementations of FTP, SMTP, Telnet, NTP, etc. |
| **Commons Validator** | Declarative data validation. |
| **Commons Email** | Simplified email sending over JavaMail. |
| **Commons Text** | String algorithms: similarity, diff, escaping, templating. |
| **Commons Imaging** | Pure-Java image format read/write + metadata. |
| **Commons Crypto** | High-performance crypto using AES-NI (JNI to OpenSSL). |
| **Commons Daemon** | Run Java apps as Unix daemons / Windows services (jsvc/procrun). |
| **Commons Exec** | Launch and manage external processes. |
| **Commons JEXL** | Embeddable expression language. |
| **Commons JXPath** | XPath over Java object graphs. |
| **Commons VFS** | Virtual file system over many backends (FTP, SFTP, zip, HDFS, …). |
| **Commons Chain** | Chain-of-responsibility pattern implementation. |
| **Commons Digester** | Map XML to Java objects via rules. |
| **Commons FileUpload** | Servlet/web file-upload parsing. |
| **Commons Numbers / Statistics / Geometry / RNG** | Modern, modular successors to parts of Commons Math (complex numbers, stats, geometry, fast RNGs). |

*Design pattern throughout:* each component is a **single-responsibility, low-dependency library**
with a stable API — the "do one thing well" philosophy applied to Java utilities. They are among
the most-depended-upon JARs in the entire JVM ecosystem.

### 25. Core libraries — Logging Services

*The Logging Services project maintains logging frameworks across languages.*

**Apache Log4j 2** — *Java · 🟢 Active*
- **Description:** High-performance, asynchronous logging framework (the Log4j 1.x successor).
- **Function:** Structured, configurable application logging with pluggable appenders/layouts.
- **Patterns:** Appender/layout/filter SPI, async (LMAX Disruptor) logging, plugin system.
- **Use cases:** Application logging across the Java world. *(Famous for the 2021 "Log4Shell" CVE, which drove the ubiquity-vs-security conversation in open source.)*

**Apache Log4net / Log4cxx** — *C#/C++ · 🟢 Active*
- Ports of the Log4j model to .NET and C++.

**Apache Chainsaw** — *Java · 🟢 Active*
- GUI log viewer/analyzer for Log4j output.

### 26. Core libraries — XML, HTTP & utilities

*Shared patterns: standards implementations, streaming parsers, pluggable transport, client libraries.*

**Apache Xerces** — *Java/C++/Perl · 🟢 Active*
- **Description:** XML parsers (DOM, SAX, StAX) and schema validators.
- **Patterns:** Streaming + tree parsing, schema validation.
- **Use cases:** The default XML parsing engine in much of the Java world.

**Apache Xalan** — *Java/C++ · 🟡 Low activity*
- **Description:** XSLT processor for transforming XML.
- **Patterns:** XSLT transformation, XPath.
- **Use cases:** XML-to-XML/HTML/text transformation.

**Apache HttpComponents** — *Java · 🟢 Active*
- **Description:** **HttpClient** and **HttpCore** — low-level HTTP client/server toolkit.
- **Function:** Robust, standards-compliant HTTP client (sync/async) and building blocks.
- **Patterns:** Connection pooling, pluggable protocol interceptors.
- **Use cases:** HTTP in Java apps where fine control is needed.

**Apache MINA** — *Java · 🟢 Active*
- **Description:** Network application framework for high-performance, async I/O; includes **SSHD** and **FtpServer**.
- **Function:** Event-driven, non-blocking networking abstraction.
- **Patterns:** Reactor/event-driven I/O, filter chain, protocol codec SPI.
- **Use cases:** Custom network servers/clients, embedding SSH/SFTP (Apache SSHD).

**Apache CXF** — *Java · 🟢 Active*
- **Description:** Services framework for SOAP and REST (JAX-WS / JAX-RS).
- **Function:** Build and consume web services with WS-* and REST support.
- **Patterns:** Interceptor chains, front-end abstraction (JAX-WS/JAX-RS), transport SPI.
- **Use cases:** Enterprise web services, contract-first SOAP, JAX-RS REST endpoints.

**Apache Axis2** — *Java/C · 🟡 Low activity*
- **Description:** Earlier-generation SOAP/web-services engine.
- **Patterns:** Message-flow phases, module extensibility.
- **Use cases:** Legacy SOAP services.

**Apache WSS4J** / **Woden** — *Java · 🟢 Active*
- WS-Security implementation and a WSDL object model, respectively (support CXF/Axis).

**Apache Commons** — *(see [§24](#24-core-libraries--apache-commons))*

### 27. Business applications

*Shared patterns: domain-driven design, entity/data-model engines, pluggable modules, naked-objects UIs.*

**Apache OFBiz** — *Java · 🟢 Active*
- **Description:** Open-source ERP suite and business-automation framework.
- **Function:** Pre-built CRM, e-commerce, order/inventory/accounting, manufacturing, plus a framework to extend them.
- **Patterns:** Entity engine (data abstraction), service engine (SOA), screen widget framework.
- **Use cases:** ERP/e-commerce platforms; a base to build custom business apps.

**Apache Fineract** — *Java · 🟢 Active*
- **Description:** Core-banking platform for financial inclusion (digital financial services).
- **Function:** Accounts, loans, savings, and transactions for banks/microfinance/fintechs.
- **Patterns:** Multi-tenant core banking, double-entry accounting, REST API.
- **Use cases:** Microfinance institutions, neobanks, financial-inclusion providers.

**Apache Causeway (formerly Isis)** — *Java · 🟢 Active*
- **Description:** Framework for rapidly building domain-driven line-of-business apps.
- **Function:** Generates a UI and REST API automatically from the domain object model.
- **Patterns:** Naked Objects, domain-driven design, convention-driven UI generation.
- **Use cases:** Internal enterprise apps where the domain model is the focus.

**Apache Unomi** — *Java · 🟢 Active*
- **Description:** Customer data platform (CDP) / context server implementing the OASIS CXS standard.
- **Function:** Stores visitor profiles/events and manages consent for personalization.
- **Patterns:** Event/profile store, segmentation rules, privacy/consent management.
- **Use cases:** Personalization engines, consent-respecting customer analytics.

**Apache SeaTunnel** — *Java · 🟢 Active*
- **Description:** High-performance, distributed data-integration platform.
- **Function:** Syncs massive data between 100+ sources/sinks (batch + CDC streaming).
- **Patterns:** Connector SPI, unified batch/stream integration, pluggable engine (Zeta/Spark/Flink).
- **Use cases:** Large-scale data ingestion/CDC/ETL across heterogeneous systems.

**Apache InLong** — *Java · 🟢 Active*
- **Description:** One-stop integration framework for massive data ("MQ + ingestion + sorting").
- **Patterns:** End-to-end ingestion pipeline, pluggable sources/sinks.
- **Use cases:** High-volume data collection and distribution (from Tencent).

**Apache Linkis** — *Scala/Java · 🟢 Active*
- **Description:** Computation middleware decoupling apps from underlying engines.
- **Function:** Unified job-submission/governance gateway to Spark/Hive/Flink/Presto.
- **Patterns:** Engine abstraction/orchestration, context service, resource governance.
- **Use cases:** Data-platform layer connecting many tools to many engines.

### 28. Languages, runtimes & actor systems

**Apache Groovy** — *Java/Groovy · 🟢 Active*
- **Description:** Dynamic + static JVM language with concise syntax and strong Java interop.
- **Function:** Scripting, DSLs, and full applications on the JVM.
- **Patterns:** Metaprogramming (MOP), builder DSLs, optional static compilation.
- **Use cases:** Build scripts (Gradle, Jenkins pipelines), testing (Spock), DSLs, scripting.

**Apache Pekko** — *Scala/Java · 🟢 Active*
- **Description:** Toolkit for concurrent, distributed, resilient message-driven apps (open-source fork of Akka 2.6).
- **Function:** Actor model, streams, clustering, and persistence on the JVM.
- **Patterns:** Actor model, supervision hierarchies, reactive streams, event sourcing/CQRS.
- **Use cases:** High-concurrency backends, streaming, distributed stateful systems (a BSL-free Akka path).

**Apache OpenWhisk** — *Scala/multi · 🟡 Low activity*
- **Description:** Open-source serverless / Function-as-a-Service platform.
- **Function:** Runs functions in containers in response to events/triggers.
- **Patterns:** FaaS, event trigger→rule→action, container-per-invocation.
- **Use cases:** Self-hosted serverless event processing.

**Apache River** — *Java · 🗄️ Attic*
- **Description:** Jini-based service-oriented/distributed computing.
- **Use cases:** Dynamic service networks. *(Retired.)*

**Apache OpenOffice** — *C++/Java · 🟢 Active*
- **Description:** Full office productivity suite (Writer, Calc, Impress, Draw, Base, Math).
- **Function:** Desktop documents, spreadsheets, presentations; ODF-native.
- **Patterns:** Document component model, ODF standard, UNO component bridge.
- **Use cases:** Free desktop office suite (sibling to the LibreOffice fork).

**Apache JMeter** — *Java · 🟢 Active*
- **Description:** Load- and performance-testing tool.
- **Function:** Simulates concurrent load against web/APIs/databases and measures performance.
- **Patterns:** Thread-group load modeling, sampler/listener plugins, assertion pipeline.
- **Use cases:** Performance/stress/regression testing of services.

### 29. Additional active top-level projects (reconciliation additions)

*These are active top-level projects confirmed against `projects.apache.org` on 2026-11-06 that
the first pass did not give a card. They are grouped by domain and cross-reference the same
patterns from [Part 1](#part-1--cross-cutting-abstracted-patterns).*

#### 29.1 Version control, build & developer tooling

**Apache Subversion (SVN)** — *C · 🟢 Active*
- **Description:** Centralized version-control system, long the enterprise standard before Git.
- **Function:** Versions files/directories with a central repository and atomic commits.
- **Patterns:** Centralized versioned repository, atomic commits, path-based authorization, delta storage.
- **Use cases:** Enterprise/legacy source control, versioning large binary assets, controlled-access repos.

**Apache NetBeans** — *Java · 🟢 Active*
- **Description:** Full-featured IDE and application platform (donated by Oracle).
- **Function:** Develops Java/PHP/JS and more; the NetBeans Platform hosts modular desktop apps.
- **Patterns:** Modular IDE platform (module system), project/build abstraction, plugin SPI.
- **Use cases:** Polyglot development; building rich-client (RCP-style) desktop applications.

**Apache Yetus** — *Java/shell · 🟢 Active*
- **Description:** Libraries and tools for contribution testing and release documentation.
- **Function:** "Precommit" automation that tests patches/PRs and audits release artifacts.
- **Patterns:** Precommit CI orchestration, pluggable test/analysis plugins, release audit.
- **Use cases:** Automated patch validation and release-note/license checking for OSS projects.

**Apache BuildStream** — *Python · 🟢 Active*
- **Description:** Tool to integrate, build, and bundle software stacks from source.
- **Function:** Produces deployable artifacts/images reproducibly from declarative build plans.
- **Patterns:** Declarative build pipelines, sandboxed/reproducible builds, artifact caching.
- **Use cases:** Building whole software stacks or OS images with reproducibility guarantees.

**Apache Serf** — *C · 🟢 Active*
- **Description:** High-performance asynchronous HTTP client library built on APR.
- **Function:** Non-blocking HTTP(S) client used by native applications.
- **Patterns:** Async HTTP client, bucket-based streaming I/O.
- **Use cases:** HTTP access in C programs (notably Subversion's HTTP/WebDAV layer).

**Apache Magpie** — *Python/Java · 🟢 Active (TLP, 2026)*
- **Description:** Platform infrastructure for AI-/agent-assisted maintenance of open-source repositories.
- **Function:** Helps maintainers with issue/PR triage, security-issue handling, and routine upkeep via agents.
- **Patterns:** Agent-assisted maintainership, pluggable task agents, workflow automation (originated in Airflow).
- **Use cases:** Reducing maintainer load and response times on open-source projects.

#### 29.2 ASF foundation infrastructure

**Apache Whimsy** — *Ruby · 🟢 Active*
- **Description:** Web tools that expose and automate ASF organizational data.
- **Function:** Board agendas, committee rosters, membership, and self-service governance tasks.
- **Patterns:** Data-driven admin tooling over authoritative records/LDAP.
- **Use cases:** Running ASF governance operations (meta-tooling for the foundation itself).

**Apache STeVe** — *Python · 🟢 Active*
- **Description:** Online voting system used for ASF elections.
- **Function:** Collects and tallies ballots (including Single Transferable Vote).
- **Patterns:** Electronic ballot + tallying algorithms.
- **Use cases:** Board/member elections and other community votes.

**Apache Pony Mail** — *Java/JS · 🟢 Active*
- **Description:** Mail-archive browser and archiver with full-text search.
- **Function:** Turns mailing-list traffic into a searchable, linkable web archive.
- **Patterns:** Archived pub/sub indexing, searchable thread model.
- **Use cases:** Browsable/searchable mailing-list archives (the ASF runs its lists on it).

#### 29.3 Databases & persistence

**Apache AsterixDB** — *Java · 🟢 Active*
- **Description:** Parallel big-data management system for semistructured (NoSQL) data with the SQL++ language.
- **Function:** Ingests and queries large volumes of flexible-schema (JSON-like) records.
- **Patterns:** Shared-nothing parallel DBMS, LSM storage, declarative query over flexible schema, data feeds.
- **Use cases:** Large-scale analytics over semistructured data, continuous data ingestion.

**Apache Kvrocks** — *C++ · 🟢 Active*
- **Description:** Distributed key-value database that speaks the Redis protocol, built on RocksDB.
- **Function:** Redis-compatible storage for datasets larger than RAM, at lower cost.
- **Patterns:** Redis API over an LSM engine (RocksDB), disk-based KV, namespacing, replication.
- **Use cases:** Redis-API workloads needing persistence and large capacity.

**Apache CarbonData** — *Java/Scala · 🟢 Active*
- **Description:** Indexed columnar data format for fast analytics on big-data platforms.
- **Function:** Stores huge datasets with multi-level indexing for both scans and point lookups.
- **Patterns:** Columnar storage + indexing, deep Spark integration, data skipping.
- **Use cases:** Interactive queries mixing full scans and selective lookups over large tables.

**Apache Cayenne** — *Java · 🟢 Active*
- **Description:** Object-relational mapping (ORM) framework with a visual modeler.
- **Function:** Maps Java objects to relational databases with an object-graph persistence context.
- **Patterns:** ORM, unit-of-work/object context, remote object persistence.
- **Use cases:** Database persistence for Java apps without hand-written SQL.

**Apache OpenJPA** — *Java · 🟢 Active*
- **Description:** Implementation of the Jakarta Persistence (JPA) specification.
- **Function:** Standard ORM persistence with bytecode enhancement.
- **Patterns:** ORM, persistence context, bytecode enhancement, spec implementation.
- **Use cases:** JPA persistence layer, embeddable in Jakarta EE servers (e.g., TomEE/Geronimo heritage).

**Apache Empire-db** — *Java · 🟢 Active*
- **Description:** Lightweight, SQL-centric relational data-access library (an ORM alternative).
- **Function:** Type-safe, dynamically generated SQL defined in Java code rather than mapping files.
- **Patterns:** Code-defined type-safe SQL, DBMS abstraction.
- **Use cases:** Java database access where you want SQL control with compile-time safety.

**Apache ResilientDB** — *C++ · 🟢 Active*
- **Description:** High-throughput, sustainable distributed-ledger / blockchain platform (research lineage, UC Davis).
- **Function:** Scalable permissioned ledger with parallelized, pipelined transaction processing.
- **Patterns:** Byzantine-fault-tolerant consensus, pipelined/parallel execution, modular consensus.
- **Use cases:** Permissioned blockchains, distributed-ledger research and applications.

#### 29.4 Graph & analytics libraries

**Apache HugeGraph** — *Java · 🟢 Active*
- **Description:** Fast, scalable graph database (OLTP) with analytics tooling.
- **Function:** Stores and traverses large property graphs; Gremlin-compatible.
- **Patterns:** Property-graph store, TinkerPop/Gremlin API, pluggable storage backends.
- **Use cases:** Knowledge graphs, fraud/relationship analysis, graph OLTP + algorithms.

**Apache DataSketches** — *Java/C++/Python · 🟢 Active*
- **Description:** Library of streaming, stochastic ("sketch") algorithms for approximate analytics.
- **Function:** Small, mergeable summaries for distinct counts, quantiles, and frequent items.
- **Patterns:** Probabilistic data structures, mergeable summaries, sublinear memory.
- **Use cases:** Fast approximate cardinality/quantiles at scale inside SQL engines and pipelines.

#### 29.5 Data formats

**Apache Daffodil** — *Scala/Java · 🟢 Active*
- **Description:** Implementation of the Data Format Description Language (DFDL).
- **Function:** Parses complex binary/text formats into XML/JSON and serializes back ("unparse").
- **Patterns:** Declarative grammar-driven parsing (DFDL schema), bidirectional (un)parsing.
- **Use cases:** Converting legacy/industry formats (EDI, MIL-STD, financial, scientific) to structured data.

#### 29.6 Web frameworks, content & collaboration

**Apache Grails** — *Groovy · 🟢 Active*
- **Description:** Full-stack, convention-driven web framework on Groovy and Spring Boot.
- **Function:** Rapid web-application development (Rails-style) on the JVM.
- **Patterns:** Convention over configuration, MVC, GORM (ORM), plugin system.
- **Use cases:** Fast JVM web apps and REST backends.

**Apache Juneau** — *Java · 🟢 Active*
- **Description:** Toolkit to marshal POJOs across formats and build self-documenting REST APIs/microservices.
- **Function:** Serializes Java objects to JSON/XML/HTML/etc. and exposes them as REST.
- **Patterns:** Format-agnostic serialization SPI, REST interface proxies, HATEOAS.
- **Use cases:** Content negotiation, REST API layers, typed remote proxies, configuration.

**Apache JSPWiki** — *Java · 🟢 Active*
- **Description:** Feature-rich Java-based wiki engine.
- **Function:** Wiki content authoring/rendering with access control and plugins.
- **Patterns:** Wiki markup rendering, pluggable page providers, templating.
- **Use cases:** Team/project wikis and documentation sites.

**Apache OpenMeetings** — *Java · 🟢 Active*
- **Description:** Web conferencing and real-time collaboration server.
- **Function:** Video/audio meetings, chat, whiteboard, and document sharing.
- **Patterns:** Real-time media (WebRTC/Kurento), room/session model.
- **Use cases:** Self-hosted video meetings, online classrooms and webinars.

#### 29.7 Mail & anti-abuse

**Apache James** — *Java · 🟢 Active*
- **Description:** "Java Apache Mail Enterprise Server" — a modular mail server and email-processing framework.
- **Function:** SMTP/IMAP/POP3 server plus a programmable mail-processing pipeline.
- **Patterns:** Pipes-and-filters mail processing (Mailets/Matchers), protocol servers on Netty, pluggable mailbox stores.
- **Use cases:** Enterprise mail servers, programmable email gateways, anti-abuse processing.

**Apache SpamAssassin** — *Perl · 🟢 Active*
- **Description:** Extensible mail filter for identifying spam.
- **Function:** Scores messages with rules, Bayesian learning, and DNS blocklists.
- **Patterns:** Rule engine + weighted scoring, plugin filters, Bayesian classification.
- **Use cases:** Anti-spam filtering at mail servers and providers.

#### 29.8 OSGi, Jakarta EE & libraries

**Apache Celix** — *C/C++ · 🟢 Active*
- **Description:** Implementation of the OSGi specification for C and C++.
- **Function:** Brings a dynamic module system + service registry to native code.
- **Patterns:** OSGi modular runtime (native), service registry, dependency management.
- **Use cases:** Modular, dynamically composed C/C++ systems.

**Apache BVal** — *Java · 🟢 Active*
- **Description:** Implementation of the Jakarta Bean Validation specification.
- **Function:** Declarative, annotation-driven validation of Java objects.
- **Patterns:** Declarative constraint validation, constraint SPI, spec implementation.
- **Use cases:** Bean/data validation in Java apps (commonly with TomEE).

**Apache Tcl** — *C/Tcl · 🟢 Active*
- **Description:** Integration of the Tcl scripting language with the Apache HTTP Server (mod_tcl / Rivet lineage).
- **Function:** Embeds a Tcl interpreter for dynamic web content inside httpd.
- **Patterns:** httpd module, embedded interpreter.
- **Use cases:** Tcl-driven dynamic pages served directly by Apache httpd.

**Apache Reqsign** — *Rust · 🟢 Active*
- **Description:** Library to sign API requests for many cloud providers (from the OpenDAL community).
- **Function:** Produces provider-specific request signatures (AWS SigV4, Azure, Google, etc.).
- **Patterns:** Credential/signing abstraction, provider adapter.
- **Use cases:** Signing cloud-service API calls in Rust (used by OpenDAL). *(Newly established, 2026.)*

#### 29.9 Cloud provisioning

**Apache VCL (Virtual Computing Lab)** — *Perl/Java · 🟢 Active*
- **Description:** Self-service provisioning and scheduling of dedicated compute environments on demand.
- **Function:** Reserves and images bare-metal/VM resources for time-boxed use.
- **Patterns:** Reservation/scheduling broker, image-based provisioning.
- **Use cases:** On-demand lab/VDI environments for education and enterprises.

#### 29.10 AI-era data governance

**Apache Sourcelume** — *multi · 🟢 Active (TLP, 2026)*
- **Description:** Attestation and registry layer for documenting the origins and permitted uses of AI training data.
- **Function:** Lets dataset provenance/consent metadata be cryptographically signed, published, and independently verified.
- **Patterns:** Attestation/registry over existing metadata standards, cryptographic signing, provenance chain.
- **Use cases:** Documenting and auditing AI training-data provenance and usage rights.

---

## Part 3 — The Apache Incubator

The **Incubator** is the ASF's entry point: every new project and corporate donation (unless
entering an existing PMC) starts here as a **podling**. The point is not primarily technical —
it is to teach a community the Apache Way, establish clear IP provenance, and prove the project
can produce legally clean releases and govern itself. Outcomes are **graduation** to a
top-level project or **retirement**.

**Abstracted pattern — the Incubator itself:** a *staged onboarding / quality gate*. It applies
a checklist (licensing, trademark, release mechanics, community diversity) and a mentor model
before admitting a project to the "stable" portfolio. Many foundations have copied this.

The podling roster turns over constantly. The list below is the **24 current podlings as of
2026-11-06**, taken directly from the ASF's live `podlings.json`, grouped by domain:

| Podling | Domain | One-line |
|---------|--------|----------|
| **Amoro** | Lakehouse | Management system over Iceberg/Paimon lake tables. |
| **Cloudberry** | Analytical DB | MPP analytical database (PostgreSQL / Greenplum lineage). |
| **XTable** | Lakehouse interop | Cross-format reads across Iceberg, Hudi, and Delta. |
| **GraphAr** | Graph format | Standard file format for graph-data interchange. |
| **GeaFlow** | Graph compute | Distributed streaming graph computing (Ant Group). |
| **Texera** | Data science | Collaborative, live-execution data-science workflows. |
| **Toree** | Notebooks | Jupyter kernel for interactive Apache Spark (Scala). |
| **Hamilton** | Dataflow | Express ML/feature pipelines as Python-function DAGs. |
| **Otava** | Perf analytics | Automated change-point detection for metrics/time series. |
| **BifroMQ** | Messaging | High-performance, multi-tenant MQTT broker. |
| **Iggy** | Streaming | Persistent message streaming in Rust (QUIC/TCP/HTTP). *(graduation reported — verify)* |
| **Burr** | AI apps | Build stateful AI/LLM applications as state machines. |
| **OpenServerless** | Serverless | FaaS/serverless platform (OpenWhisk lineage). |
| **Auron** | Spark accel. | Native vectorized Spark engine (ex-Blaze; Rust + DataFusion via JNI). *(status in flux)* |
| **Pegasus** | Key-value | Distributed KV store (Raft + RocksDB), from Xiaomi. |
| **Seata** | Transactions | Distributed-transaction solution for microservices. |
| **PouchDB** | Database | JavaScript database that syncs with CouchDB (offline-first). |
| **Casbin** | Authorization | Multi-language access-control library (RBAC/ABAC/…). |
| **Caldera** | Security | Automated adversary emulation / breach simulation (MITRE). |
| **NullAway** | Code quality | Fast type-based null-safety checker for Java (from Uber). |
| **KIE** | Business automation | Rules + workflow — home of Drools and jBPM (from Red Hat). |
| **OzHera** | Observability | Application observability / APM platform (Xiaomi). |
| **Fesod / Maka / Ossie / Asyncband** | Various (2025–26) | Recent entrants — see `incubator.apache.org` for current scope. |

> **Status-in-flux note.** The ASF's project and podling datasets sometimes disagree for the
> very newest entrants. **Auron** and **Iggy** appear in `projects.json` yet still publish on
> `*.incubator.apache.org` (Auron releases are tagged `-incubating`); **Teaclave** (confidential
> computing) and **Fluss** (streaming storage for analytics) sit similarly between states. Treat
> all four as "late-stage incubating / just graduating."

**Recent graduates to top-level status (2024–2026):** DataFusion, OpenDAL, Answer, Uniffle,
Wayang, StreamPark (2024); Gravitino, StormCrawler, SDAP (2025); Polaris, Gluten, Magpie,
Sourcelume (2026) — plus Fory, Kvrocks, HugeGraph, and others now carried as TLPs in
[§6](#6-sql-engines-query-frameworks--lakehouse), [§14](#14-machine-learning--ai), and
[§29](#29-additional-active-top-level-projects-reconciliation-additions).

> **Always-current podling list:** `https://incubator.apache.org/projects/` and the
> machine-readable `https://projects.apache.org/json/foundation/podlings.json`.

---

## Part 4 — The Attic (retired projects)

The **Attic** preserves projects whose communities can no longer sustain them. The code, mailing
list archives, issue history, and prior releases **stay online and under the Apache License** —
retirement stops development and governance, not availability. This is itself a valuable
pattern: an *orderly end-of-life* that keeps dependents safe and history intact instead of
deleting a repo.

Notable retired projects (grouped), including several recent ones:

- **Cluster/compute:** Mesos, Aurora, Myriad, Slider, Twill, REEF, Apex, Tajo, HAWQ, Trafodion,
  Lens, MetaModel, Crunch, DataFu, Hama, Chukwa.
- **Streaming/ingest:** Sqoop (2021), Flume *(active but low)*, Bahir (2024), Gora *(retiring)*,
  Falcon.
- **Workflow/ML:** Oozie (2025), Submarine (2025), Liminal, MXNet (2023), PredictionIO,
  Marmotta, Stanbol, Joshua (machine translation).
- **Security/analytics:** Metron, Spot, Eagle, Sentry, Knox *(active)* vs. retired Ranger
  predecessors.
- **Web/CMS/portal:** Cocoon (2025), Pivot (2025), Portals/Jetspeed (2025), Lenya, Wookie,
  Shindig, Tiles, Click, Shale, Muse, Continuum.
- **Graph/data:** Giraph, Rya.
- **Cloud:** jclouds, Stratos, DeltaCloud, Whirr, libcloud *(active)*.
- **Other recent:** Kibble (2025, project analytics), Olingo (2025, OData), Griffin (2025, data
  quality), Mnemonic *(retiring)*, Edgent, Wave (Google Wave), Buildr, Abdera, ODE.

> **How to get the authoritative retired list:** `https://attic.apache.org/projects.html`
> (not reachable from this session's network).

---

## Part 5 — Quick-reference summary

**By "what problem does it solve"** — the fastest way to pick a project:

| If you need… | Reach for |
|--------------|-----------|
| A web/app server | **HTTP Server**, **Tomcat**, **TomEE**, **Traffic Server** |
| An API gateway | **APISIX**, **ShenYu**, **Knox** (Hadoop) |
| A distributed event log / messaging | **Kafka**, **Pulsar**, **ActiveMQ**, **RocketMQ**, **Qpid** |
| System integration / ETL glue | **Camel**, **NiFi**, **SeaTunnel**, **InLong** |
| Batch/stream big-data compute | **Spark**, **Flink**, **Beam**, **Storm**, **Hadoop** |
| SQL over a data lake | **Hive**, **Impala**, **Drill**, **Kyuubi**, **DataFusion** |
| A lakehouse table format | **Iceberg**, **Hudi**, **Paimon** (+ catalogs **Polaris**, **Gravitino**) |
| A scalable NoSQL store | **Cassandra**, **HBase**, **CouchDB**, **Accumulo** |
| Real-time OLAP | **Druid** *(see note)*, **Pinot** *(see note)*, **Doris**, **Kylin** |
| In-memory data grid | **Ignite**, **Geode** |
| Time-series (IoT) storage | **IoTDB** |
| Full-text / vector search | **Lucene**, **Solr** |
| Content extraction / documents | **Tika**, **PDFBox**, **POI**, **FOP**, **Batik** |
| Workflow orchestration | **Airflow**, **DolphinScheduler** |
| Distributed coordination | **ZooKeeper** (+ **Curator**), **Ratis**, **BookKeeper** |
| Microservice RPC | **Dubbo**, **ServiceComb**, **bRPC**, **Thrift** |
| Observability/APM | **SkyWalking**, **HertzBeat** |
| App security / identity | **Shiro**, **Ranger**, **Syncope**, **Directory** |
| Build & dependencies (JVM) | **Maven**, **Ant** + **Ivy** |
| BI / dashboards / charts | **Superset**, **ECharts**, **Zeppelin** |
| Reusable Java utilities | **Commons** family, **Log4j** |
| A JVM language / actor toolkit | **Groovy**, **Pekko** |
| ERP / core banking | **OFBiz**, **Fineract** |

> **Druid & Pinot note:** Apache **Druid** and Apache **Pinot** are both active top-level
> real-time OLAP datastores (column-oriented, designed for sub-second user-facing analytics over
> event data). They sit alongside Doris/Kylin in the analytics tier; each is referenced in the
> patterns and summary even where a full standalone card was folded into this category for
> brevity.

**By abstracted pattern** (reverse index into [Part 1](#part-1--cross-cutting-abstracted-patterns)):

- *Append-only log* → Kafka, Pulsar/BookKeeper, Cassandra, HBase.
- *LSM-tree* → Cassandra, HBase, Accumulo, Kudu, IoTDB, Paimon.
- *Columnar + vectorized* → Parquet, ORC, Arrow, Druid, Pinot, Doris, DataFusion, Gluten.
- *DAG execution* → Spark, Flink, Tez, Beam, Airflow, NiFi, Calcite.
- *Consensus (Raft/ZAB/Paxos)* → ZooKeeper, Ratis, BookKeeper, Cassandra LWT.
- *Pipes-and-filters / EIP* → Camel, NiFi, ServiceMix, Synapse.
- *Pluggable SPI/adapter* → Commons, Calcite, Lucene codecs, Camel components, NiFi processors.
- *Open table format + catalog* → Iceberg/Hudi/Paimon + Polaris/Gravitino.
- *OSGi modularity* → Felix, Karaf, Aries.
- *Component UI / front-controller* → Wicket, Tapestry, MyFaces, Struts.
- *Actor / reactive I/O* → Pekko, MINA.

---

## Appendix — Canonical sources

Project status changes weekly. This inventory was reconciled against the following
authoritative, always-current endpoints on 2026-11-06; re-check them when exact counts or
statuses matter:

- **All projects, browsable by category / language / committee:** `https://projects.apache.org/`
  (machine-readable data at `https://projects.apache.org/json/foundation/projects.json`).
- **Projects by category:** `https://projects.apache.org/projects.html?category`
- **Incubator podlings:** `https://incubator.apache.org/projects/`
  (JSON: `https://projects.apache.org/json/foundation/podlings.json`).
- **Retired projects:** `https://attic.apache.org/projects.html`
- **Foundation statistics / annual reports:** `https://www.apache.org/foundation/reports.html`
- **Project directory source (mirror):** the ASF Projects Directory / `comdev` tooling.

**Methodology recap.** Compiled from domain knowledge, then **reconciled on 2026-11-06 against
`projects.json` (1,497 entries; ~215 active PMCs) and `podlings.json` (24 podlings)**, with
targeted web search to settle individual lifecycle changes (e.g., Oozie/Cocoon/Submarine/Bahir →
Attic; Gravitino/StormCrawler/Polaris/Gluten/DataFusion/Answer/Uniffle/StreamPark/Magpie/
Sourcelume → TLP). The reconciliation added 31 previously-missing top-level projects
([§29](#29-additional-active-top-level-projects-reconciliation-additions)) and corrected status
tags (TVM, Fory, DevLake → active; Amoro → incubating). Descriptions, functions, patterns, and
use cases reflect each project's well-established design; the **status** tag is still the field
most likely to drift — re-verify against the sources above.

*With the reconciliation additions, this inventory now carries a card (or table row) for **every
active top-level project** in the ASF's live directory, plus the Commons/Logging sub-module
families, the 24 current podlings, and the notable Attic projects. It remains pattern-oriented
rather than a literal dump of all 1,497 DOAP entries and their sub-modules; sub-projects are
represented through their parent project's entry.*




