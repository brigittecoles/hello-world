# The Apache Software Foundation — Comprehensive Project Inventory

> A categorized, pattern-oriented inventory of Apache Software Foundation (ASF) projects:
> what each one is, what it does, the reusable architectural patterns it embodies, what
> people use it for — and, for reuse/composition decisions, how you connect to it, what it
> needs, and what it combines with.

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
- **Interfaces** — how you connect to it (protocols, APIs, SDK languages) and whether it is an
  *embeddable library*, a *standalone service*, or *both*. *(the #1 composability fact)*
- **Needs** — hard runtime dependencies and deployment footprint (the true cost of adoption).
- **Pairs with** — the projects/connectors it most commonly combines with.
- **Alternatives** — the closest substitutes, inside ASF and outside *(editorial)*.
- **Standards** — the open standards / formats / wire protocols it speaks (what makes it swappable).
- **Maturity** — a coarse adoption read, whether a **managed cloud service** exists, and any
  license nuance *(editorial; all ASF code is Apache-2.0 unless noted)*.
- **Tags** — primary language(s) and lifecycle status.

> The last six fields exist specifically to answer *"can I leverage this here, and what does it
> combine with?"* **Part 6** turns them into cross-cutting tools: stack recipes, a head-to-head
> selection matrix, a shared-dependency map, and a protocol/format index. Objective fields
> (Interfaces, Needs, Standards) track each project's documented design and can be re-verified
> against the DOAP data; *Alternatives* and *Maturity* are editorial judgment calls. Retired
> (Attic) entries get a single **Leverage note** instead, since they are not recommended for new
> work.

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
- [Part 6 — Composition & interoperability guide](#part-6--composition--interoperability-guide)
  - [6.1 ASF stack recipes](#61-asf-stack-recipes)
  - [6.2 Head-to-head selection matrix](#62-head-to-head-selection-matrix)
  - [6.3 Shared-substrate / dependency map](#63-shared-substrate--dependency-map)
  - [6.4 Protocol / format / standard index](#64-protocol--format--standard-index)
- [Appendix — Canonical sources](#appendix--canonical-sources)

---

## Part 0 — Understanding the ASF

The Apache Software Foundation is a US 501(c)(3) non-profit, founded in 1999, that provides
organizational, legal, and financial support for a large portfolio of open-source software
projects. A few structural facts frame the whole inventory:

- **Everything ships under the Apache License 2.0.** A permissive license with an explicit
  patent grant and a requirement to preserve notices. This is why ASF code is ubiquitous in
  commercial products — it can be embedded and redistributed with minimal obligations. (A few
  projects ship *optional* modules under other licenses, or depend on differently-licensed
  components; those are called out in entries' **Maturity** line where they matter.)
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
- **Interfaces:** HTTP/1.1 & /2, HTTPS; `mod_*` C module API; CGI/FastCGI, `mod_proxy`. Standalone service. · **Needs:** OS + APR; single process (scale behind a load balancer); no ASF deps.
- **Pairs with:** Tomcat/app servers (`mod_proxy`/`mod_jk`), Traffic Server at the edge, any backend. · **Alternatives:** Traffic Server (ASF); Nginx, Caddy, Envoy (external).
- **Standards:** HTTP/1.1 & /2, TLS, WebDAV, CGI. · **Maturity:** Ubiquitous, decades-mature; available on every host/cloud. Apache-2.0.

**Apache Tomcat** — *Java · 🟢 Active*
- **Description:** Servlet container and reference implementation of Jakarta Servlet/JSP/WebSocket/EL specs.
- **Function:** Runs Java web applications (WAR files); HTTP front end for servlet-based apps.
- **Patterns:** Container/lifecycle management, connector abstraction (BIO/NIO/APR), valve pipeline.
- **Use cases:** Backbone of countless Java web deployments; embedded in Spring Boot via embedded Tomcat.
- **Interfaces:** HTTP(S)/AJP; deploys WAR; Servlet/JSP/WebSocket APIs; JMX management. Both (server + embeddable). · **Needs:** JVM; no ASF deps.
- **Pairs with:** httpd front end, Spring Boot (embedded), TomEE (adds full EE). · **Alternatives:** TomEE (ASF, adds EE); Jetty, Undertow, WildFly (external).
- **Standards:** Jakarta Servlet/JSP/EL/WebSocket, JMX. · **Maturity:** Ubiquitous, mature; managed on most PaaS. Apache-2.0.

**Apache Traffic Server (ATS)** — *C++ · 🟢 Active*
- **Description:** High-performance caching proxy server (originated at Inktomi/Yahoo).
- **Function:** Forward/reverse caching proxy and CDN edge cache.
- **Patterns:** Event-driven async I/O, cache hierarchy, plugin SDK.
- **Use cases:** CDN edge, large-scale HTTP caching, traffic offload.
- **Interfaces:** HTTP(S) forward/reverse proxy; C/C++ plugin SDK + Lua; management API. Standalone service. · **Needs:** OS; multi-core host; no ASF deps.
- **Pairs with:** httpd/origin servers, Traffic Control (CDN control plane). · **Alternatives:** httpd `mod_cache` (ASF); Varnish, Nginx, Squid (external).
- **Standards:** HTTP/1.1 & /2, TLS, ESI. · **Maturity:** Mature; proven at CDN scale (Yahoo/Comcast/Verizon). Apache-2.0.

**Apache Traffic Control** — *Go/others · 🗄️ Attic (retiring 2025)*
- **Description:** Control plane to build and operate a CDN on top of Traffic Server.
- **Function:** CDN orchestration, cache assignment, health monitoring.
- **Patterns:** Control-plane/data-plane separation, declarative CDN topology.
- **Use cases:** Operating a private/telco CDN (built originally at Comcast).
- **Leverage note:** 🗄️ Retiring — avoid for new builds; run Traffic Server with a current control plane, or use a commercial/CDN-managed control plane instead.

**Apache APISIX** — *Lua/Nginx + etcd · 🟢 Active*
- **Description:** Dynamic, high-performance cloud-native API gateway.
- **Function:** API routing, auth, rate limiting, observability, and traffic management at the edge.
- **Patterns:** Gateway + plugin pipeline, hot-reloadable config via etcd, control/data-plane split.
- **Use cases:** Microservice API gateway, Kubernetes ingress, multi-protocol (gRPC/MQTT/Dubbo) gateway.
- **Interfaces:** Proxies HTTP/gRPC/TCP/UDP/MQTT/Dubbo; Admin REST API; Lua/WASM plugin runner; dashboard. Standalone service. · **Needs:** etcd (config store); runs on OpenResty/Nginx.
- **Pairs with:** etcd, Kubernetes (ingress), SkyWalking/OpenTelemetry, Dubbo backends. · **Alternatives:** ShenYu, Knox (ASF); Kong, Envoy Gateway, NGINX (external).
- **Standards:** HTTP/1.1/2/3, gRPC, MQTT, OpenID Connect, OpenTelemetry. · **Maturity:** Widely adopted; commercial/managed option from API7. Apache-2.0.

**Apache ShenYu** — *Java · 🟢 Active*
- **Description:** Reactive, high-performance API gateway.
- **Function:** Request routing, protocol conversion, flow control, and plugin-based mediation.
- **Patterns:** Reactive gateway, plugin chain, divide/selector/rule config model.
- **Use cases:** Microservice gateway for Dubbo/Spring Cloud/gRPC stacks.
- **Interfaces:** Proxies HTTP/gRPC/Dubbo/Spring Cloud/WebSocket; Admin API + dashboard; plugin SPI. Standalone service. · **Needs:** JVM; a config store (ZooKeeper/etcd/Nacos/HTTP).
- **Pairs with:** Dubbo, Spring Cloud, Nacos, SkyWalking. · **Alternatives:** APISIX (ASF); Spring Cloud Gateway, Kong (external).
- **Standards:** HTTP, gRPC, OIDC, Dubbo protocol. · **Maturity:** Growing; reactive (WebFlux) core. Apache-2.0.

**Apache Guacamole** — *Java + C · 🟢 Active*
- **Description:** Clientless remote desktop gateway accessed through a web browser.
- **Function:** Proxies RDP/VNC/SSH to HTML5 in the browser — no client plugin needed.
- **Patterns:** Protocol-translation gateway, stateless web tier + native proxy daemon (`guacd`).
- **Use cases:** Browser-based access to remote machines, jump-host/bastion portals, VDI front ends.
- **Interfaces:** Browser HTML5 client; `guacd` speaks RDP/VNC/SSH/Telnet/Kubernetes; REST + auth-extension API. Service (web app + native daemon). · **Needs:** JVM + servlet container (Tomcat) + `guacd` native daemon.
- **Pairs with:** Tomcat, Directory/LDAP & SSO (auth extensions). · **Alternatives:** fairly unique in ASF; (external) Teleport, commercial VDI.
- **Standards:** RDP, VNC/RFB, SSH, WebSocket. · **Maturity:** Mature, popular self-hosted bastion. Apache-2.0.

### 2. Application servers, Jakarta EE & OSGi runtimes

*Shared patterns: container-managed lifecycle, dependency injection/CDI, OSGi modularity, specification implementation.*

**Apache TomEE** — *Java · 🟢 Active*
- **Description:** Tomcat plus the Jakarta EE (formerly Java EE) stack — a lightweight certified EE server.
- **Function:** Runs enterprise Java apps needing CDI, JPA, JAX-RS, EJB, JMS on a Tomcat base.
- **Patterns:** Container + specification assembly, profile-based packaging.
- **Use cases:** Enterprise Java apps wanting EE features without a heavyweight server.
- **Interfaces:** HTTP(S)/AJP; deploys WAR/EAR; Jakarta EE APIs (CDI/JPA/JAX-RS/EJB/JMS). Both (server + embeddable). · **Needs:** JVM; bundles OpenWebBeans/OpenJPA/CXF/ActiveMQ.
- **Pairs with:** OpenWebBeans, OpenJPA, CXF, ActiveMQ, BVal, Johnzon (all bundled). · **Alternatives:** WildFly, Payara, Open Liberty, Quarkus (external).
- **Standards:** Jakarta EE (Web/MicroProfile profiles). · **Maturity:** Mature, certified; lighter than full EE servers. Apache-2.0.

**Apache Karaf** — *Java/OSGi · 🟢 Active*
- **Description:** Modular application runtime built on OSGi.
- **Function:** Hosts dynamic, hot-deployable modules ("features") with a shell, provisioning, and management.
- **Patterns:** OSGi modular runtime, feature descriptors, dynamic service registry.
- **Use cases:** Integration/middleware runtimes (often hosting Camel, CXF, ActiveMQ).
- **Interfaces:** SSH/console shell; JMX; feature/KAR deployment; OSGi service registry. Standalone runtime (embeddable). · **Needs:** JVM; OSGi framework (Felix or Equinox).
- **Pairs with:** Camel, CXF, ActiveMQ, Aries, Felix. · **Alternatives:** plain Felix/Equinox (ASF); Spring Boot "fat jar" model (external).
- **Standards:** OSGi, JMX. · **Maturity:** Mature; the default home for OSGi integration apps. Apache-2.0.

**Apache Felix** — *Java/OSGi · 🟢 Active*
- **Description:** Implementation of the OSGi core framework and companion services.
- **Function:** Provides the dynamic module system and service registry for OSGi apps.
- **Patterns:** OSGi bundle lifecycle, service-oriented component model (Declarative Services).
- **Use cases:** Embedded module systems; foundation under Karaf, Sling, and many products.
- **Interfaces:** OSGi framework + service registry; Gogo shell; embeddable JAR. Embeddable library/runtime. · **Needs:** JVM only.
- **Pairs with:** Karaf, Sling, Aries (built on Felix). · **Alternatives:** Eclipse Equinox (external OSGi); Celix (ASF, for C/C++).
- **Standards:** OSGi core & compendium. · **Maturity:** Mature reference-grade OSGi impl. Apache-2.0.

**Apache Aries** — *Java/OSGi · 🟢 Active*
- **Description:** Enterprise programming-model components for OSGi (Blueprint, JPA, JNDI, transactions).
- **Function:** Brings EE-style services into OSGi runtimes.
- **Patterns:** Blueprint IoC container, OSGi enterprise service abstractions.
- **Use cases:** Enterprise OSGi applications; used inside Karaf.
- **Interfaces:** Java/OSGi service APIs (Blueprint XML/annotations). Embeddable library set. · **Needs:** JVM + OSGi framework (Felix/Equinox).
- **Pairs with:** Karaf, Felix, CXF, OpenJPA. · **Alternatives:** Declarative Services/SCR (Felix); Spring DM (dead, external).
- **Standards:** OSGi Enterprise, JPA/JTA/JNDI. · **Maturity:** Stable, niche (OSGi enterprise). Apache-2.0.

**Apache OpenWebBeans** — *Java · 🟢 Active*
- **Description:** Implementation of Jakarta Contexts & Dependency Injection (CDI).
- **Function:** Managed-bean lifecycle, injection, events, interceptors.
- **Patterns:** Dependency injection/IoC, contextual instances, decorator/interceptor.
- **Use cases:** CDI engine inside TomEE and standalone CDI apps.
- **Interfaces:** CDI programming model (annotations); embeddable JAR. Embeddable library. · **Needs:** JVM.
- **Pairs with:** TomEE, DeltaSpike, Meecrowave. · **Alternatives:** JBoss Weld (external CDI reference impl).
- **Standards:** Jakarta CDI. · **Maturity:** Mature; the CDI engine in TomEE. Apache-2.0.

**Apache DeltaSpike** — *Java · 🟢 Active*
- **Description:** A collection of portable CDI extensions.
- **Function:** Adds config, data (repositories), security, scheduling, and test control on top of CDI.
- **Patterns:** CDI portable extension, repository pattern, cross-cutting concerns.
- **Use cases:** Reusable building blocks for CDI-based enterprise apps.
- **Interfaces:** CDI extension APIs; embeddable JARs (modular). Embeddable library. · **Needs:** JVM + a CDI impl (OpenWebBeans/Weld).
- **Pairs with:** OpenWebBeans/Weld, JPA providers, test frameworks. · **Alternatives:** framework-specific extensions; MicroProfile (external).
- **Standards:** Jakarta CDI. · **Maturity:** Mature but low cadence. Apache-2.0.

**Apache Johnzon** — *Java · 🟢 Active*
- **Description:** Implementation of JSON-P and JSON-B (Jakarta JSON Processing/Binding).
- **Function:** Parse/generate and bind JSON in Java.
- **Patterns:** Streaming + object-model parsing, mapper.
- **Use cases:** JSON handling in Jakarta EE stacks.
- **Interfaces:** JSON-P/JSON-B APIs; embeddable JAR. Embeddable library. · **Needs:** JVM.
- **Pairs with:** TomEE, CXF (JAX-RS payloads). · **Alternatives:** Jackson, Gson, Eclipse Yasson (external).
- **Standards:** Jakarta JSON-P / JSON-B. · **Maturity:** Mature, lightweight. Apache-2.0.

**Apache Geronimo** — *Java · 🟡 Low activity*
- **Description:** Java/Jakarta EE server and a set of EE spec API JARs.
- **Function:** Historically a full EE server; today mainly a trusted source of spec API artifacts.
- **Patterns:** Specification implementation, assembly of EE services.
- **Use cases:** EE spec JARs consumed by many other projects.
- **Interfaces:** Jakarta EE spec API JARs (Maven artifacts). Mostly consumed as libraries now. · **Needs:** JVM.
- **Pairs with:** TomEE and most JVM EE projects (consume its spec JARs). · **Alternatives:** Jakarta/EE4J spec artifacts (external).
- **Standards:** Jakarta/Java EE specs. · **Maturity:** Low activity as a server; spec JARs still widely used. Apache-2.0.

### 3. Java web / UI frameworks & templating

*Shared patterns: MVC/front-controller, component-based UI, server-side templating (template method).*

**Apache Struts** — *Java · 🟢 Active*
- **Description:** Action-based MVC web framework (Struts 2).
- **Function:** Maps HTTP requests to actions, handles validation, and renders results.
- **Patterns:** Front-controller MVC, interceptor stack, action/result model.
- **Use cases:** Traditional server-rendered Java web apps.
- **Interfaces:** Servlet-based web framework; JSP/FreeMarker views; plugin SPI. Library on a servlet container. · **Needs:** JVM + servlet container (Tomcat).
- **Pairs with:** Tomcat, Tiles/FreeMarker, Commons libraries. · **Alternatives:** Spring MVC, Jakarta Faces (external); Wicket/Tapestry (ASF).
- **Standards:** Jakarta Servlet/JSP. · **Maturity:** Mature but legacy-leaning; note historical RCE CVEs — keep patched. Apache-2.0.

**Apache Wicket** — *Java · 🟢 Active*
- **Description:** Component-based web framework using plain Java + HTML (no templating language).
- **Function:** Builds stateful web UIs as trees of Java components bound to markup.
- **Patterns:** Component-based UI, stateful server-side component tree.
- **Use cases:** Complex, form-heavy enterprise web apps written mostly in Java.
- **Interfaces:** Java component API + plain HTML; runs on a servlet container. Library. · **Needs:** JVM + servlet container.
- **Pairs with:** Tomcat, CDI/Spring, Bootstrap themes. · **Alternatives:** Tapestry, MyFaces (ASF); Vaadin (external).
- **Standards:** Jakarta Servlet. · **Maturity:** Mature, stable community. Apache-2.0.

**Apache Tapestry** — *Java · 🟢 Active*
- **Description:** Component-oriented web framework emphasizing live class reloading and convention.
- **Function:** Page/component-based web development with strong IoC.
- **Patterns:** Component-based UI, convention over configuration, DI container.
- **Use cases:** Productive Java web apps with fast dev feedback.
- **Interfaces:** Java component classes + templates; built-in IoC; servlet container. Library. · **Needs:** JVM + servlet container.
- **Pairs with:** Tomcat, Hibernate/JPA. · **Alternatives:** Wicket, MyFaces (ASF); Spring MVC (external).
- **Standards:** Jakarta Servlet. · **Maturity:** Mature, smaller community. Apache-2.0.

**Apache MyFaces** — *Java · 🟢 Active*
- **Description:** Implementation of Jakarta Server Faces (JSF).
- **Function:** Server-side, component-based UI framework with managed lifecycle.
- **Patterns:** Component tree, request lifecycle phases, renderer SPI.
- **Use cases:** JSF applications; alternative to the reference implementation.
- **Interfaces:** Jakarta Faces API; component/renderer SPI; servlet container. Library. · **Needs:** JVM + servlet container.
- **Pairs with:** Tomcat/TomEE, PrimeFaces component libs. · **Alternatives:** Eclipse Mojarra (external JSF RI).
- **Standards:** Jakarta Faces (JSF). · **Maturity:** Mature spec impl. Apache-2.0.

**Apache Velocity** — *Java · 🟢 Active*
- **Description:** Simple, general-purpose template engine with its own template language (VTL).
- **Function:** Merges a data model into text templates (HTML, source code, email, config).
- **Patterns:** Template method, model–view separation, pluggable resource loaders.
- **Use cases:** Email/report generation, code generation, server-side views.
- **Interfaces:** Java API; `.vm` templates; resource-loader SPI. Embeddable library. · **Needs:** JVM.
- **Pairs with:** Struts, Commons, codegen tools. · **Alternatives:** FreeMarker (ASF); Thymeleaf, Mustache (external).
- **Standards:** none (own VTL language). · **Maturity:** Mature, slow cadence. Apache-2.0.

**Apache FreeMarker** — *Java · 🟢 Active*
- **Description:** Rich, widely used Java template engine.
- **Function:** Generates text output (HTML, config, source) from templates + data model.
- **Patterns:** Template method, expression language, macro/library composition.
- **Use cases:** Web views, codegen, document and config generation.
- **Interfaces:** Java API; `.ftl` templates. Embeddable library. · **Needs:** JVM.
- **Pairs with:** Struts, Spring, codegen. · **Alternatives:** Velocity (ASF); Thymeleaf, Mustache, Handlebars (external).
- **Standards:** none (own FTL language). · **Maturity:** Mature, widely used. Apache-2.0.

**Apache Tiles** — *Java · 🗄️ Attic*
- **Description:** Templating/layout composition framework for web pages.
- **Function:** Assembles pages from reusable layout fragments.
- **Patterns:** Composite view, template inheritance.
- **Use cases:** Legacy Struts/JSP layout reuse.
- **Leverage note:** 🗄️ Retired — avoid for new work; use template inheritance in Thymeleaf/FreeMarker or a component framework instead.

**Apache Royale** — *ActionScript/MXML · 🟢 Active*
- **Description:** Successor to Adobe/Apache Flex; builds apps from MXML/ActionScript that compile to JS/HTML.
- **Function:** Cross-platform application UI without the Flash runtime.
- **Patterns:** Component-based UI, compile-to-JavaScript, MVC.
- **Use cases:** Migrating legacy Flex apps to the browser; rich internet applications.
- **Interfaces:** MXML/ActionScript source → JS/HTML; compiler toolchain. Build-time toolkit + runtime libs. · **Needs:** JDK (compiler); browser runtime output.
- **Pairs with:** legacy Flex codebases (migration target). · **Alternatives:** React/Angular/Vue, Flutter web (external).
- **Standards:** ECMAScript output, HTML/CSS. · **Maturity:** Niche; mainly a Flex-migration path. Apache-2.0.

**Apache Flex** — *ActionScript · 🗄️ Attic*
- **Description:** The original Flex SDK (donated by Adobe) for Flash-based RIAs.
- **Function:** Rich browser/desktop UIs on the Flash/AIR runtime.
- **Patterns:** Component-based UI, declarative MXML.
- **Use cases:** Legacy RIAs.
- **Leverage note:** 🗄️ Retired (Flash is EOL) — migrate to Apache Royale or a modern JS framework.

**Apache Turbine** — *Java · 🟡 Low activity*
- **Description:** Servlet-based web application framework and service container.
- **Function:** Page/action-based web apps with pluggable services.
- **Patterns:** Service locator, pull-MVC.
- **Use cases:** Older service-oriented Java web apps.
- **Interfaces:** Servlet framework + service manager; Java API. Library on servlet container. · **Needs:** JVM + servlet container.
- **Pairs with:** Torque (ORM), Fulcrum services, Velocity. · **Alternatives:** Spring MVC, Struts (ASF).
- **Standards:** Jakarta Servlet. · **Maturity:** Legacy, low activity. Apache-2.0.

### 4. Storage formats & serialization

*Shared patterns: schema/IDL + codegen, schema evolution, columnar layout, zero-copy/compression.*

**Apache Avro** — *Multi-language · 🟢 Active*
- **Description:** Compact binary row-oriented data serialization system with a JSON-defined schema.
- **Function:** Serialize records with embedded/evolvable schemas for storage and messaging.
- **Patterns:** Schema + IDL, schema evolution (reader/writer schemas), self-describing containers.
- **Use cases:** Kafka message payloads, Hadoop data interchange, RPC.
- **Interfaces:** Libraries for Java/C/C++/C#/Python/Ruby/Rust…; `.avsc`/IDL schemas; codegen. Embeddable library + wire format. · **Needs:** a host language runtime; no service.
- **Pairs with:** Kafka (+ Schema Registry), Hadoop, Parquet, Flink/Spark. · **Alternatives:** Protobuf, Thrift (ASF), JSON (external).
- **Standards:** Avro spec (own); JSON for schemas. · **Maturity:** Ubiquitous in streaming/Hadoop. Apache-2.0.

**Apache Parquet** — *Java/C++ · 🟢 Active*
- **Description:** Columnar on-disk storage format for analytics.
- **Function:** Stores tabular data by column with encoding/compression and predicate pushdown.
- **Patterns:** Columnar storage, nested (Dremel) encoding, metadata footers for pruning.
- **Use cases:** Data-lake tables, the physical format under Iceberg/Hudi/Hive/Spark.
- **Interfaces:** Java (`parquet-mr`) & C++ (Arrow) readers/writers; file format. Embeddable library + file format. · **Needs:** a host engine/runtime; object or file storage.
- **Pairs with:** Iceberg/Hudi/Paimon, Arrow, Spark/Flink/Trino/Impala. · **Alternatives:** ORC (ASF); Delta/Avro files (external/ASF).
- **Standards:** Parquet format spec. · **Maturity:** De-facto analytics file format. Apache-2.0.

**Apache ORC** — *Java/C++ · 🟢 Active*
- **Description:** Optimized Row Columnar file format, originally for Hive.
- **Function:** Columnar storage with lightweight indexes and ACID support hooks.
- **Patterns:** Columnar storage, stripe/stride indexing, built-in statistics.
- **Use cases:** Hive/Spark warehouse tables, especially in the Hadoop ecosystem.
- **Interfaces:** Java & C++ readers/writers; file format. Embeddable library + file format. · **Needs:** a host engine; file/object storage.
- **Pairs with:** Hive (ACID), Spark, Iceberg. · **Alternatives:** Parquet (ASF; more common outside Hive).
- **Standards:** ORC format spec. · **Maturity:** Mature; strongest in Hive-centric stacks. Apache-2.0.

**Apache Arrow** — *Multi-language · 🟢 Active*
- **Description:** Language-independent **in-memory** columnar format plus libraries.
- **Function:** Zero-copy columnar data sharing and fast analytical compute across languages/processes.
- **Patterns:** Columnar in-memory layout, zero-copy IPC, Flight (gRPC data transport).
- **Use cases:** Pandas/Polars/Spark interchange, query-engine internals, Flight data services.
- **Interfaces:** Libraries for C++/Java/Python/Rust/Go/JS…; Flight (gRPC); ADBC/Flight SQL. Embeddable library + optional Flight service. · **Needs:** a host language runtime.
- **Pairs with:** DataFusion, Gluten, Parquet, Spark, pandas/Polars. · **Alternatives:** in-house columnar buffers (external); none comparable in ASF.
- **Standards:** Arrow columnar + Flight/Flight SQL, ADBC. · **Maturity:** Foundational, very widely adopted. Apache-2.0.

**Apache Thrift** — *Multi-language · 🟢 Active*
- **Description:** Interface definition language + RPC framework (from Facebook).
- **Function:** Defines services/types in an IDL and generates clients/servers in many languages.
- **Patterns:** IDL + codegen, pluggable transport/protocol layers.
- **Use cases:** Polyglot RPC, cross-language data serialization.
- **Interfaces:** `.thrift` IDL → generated clients/servers in ~20 languages; pluggable transports. Embeddable library + RPC. · **Needs:** host language runtime.
- **Pairs with:** HBase/Cassandra (Thrift gateways, legacy), polyglot services. · **Alternatives:** gRPC/Protobuf, Avro (ASF) (external/ASF).
- **Standards:** Thrift IDL/protocol (own). · **Maturity:** Mature; gRPC now more common for new builds. Apache-2.0.

**Apache Fory (formerly Fury)** — *Java/Multi-language · 🟢 Active*
- **Description:** Blazing-fast multi-language serialization using JIT and zero-copy.
- **Function:** High-throughput object serialization as a drop-in for slower serializers.
- **Patterns:** Runtime code generation, schema-consistent/compatible modes, zero-copy.
- **Use cases:** RPC payloads, caching, data transfer hot paths.
- **Interfaces:** Libraries for Java/Python/C++/Go/JS/Rust; object (de)serialization API. Embeddable library. · **Needs:** host language runtime.
- **Pairs with:** RPC frameworks, caches, Spark/Flink (object ser). · **Alternatives:** Kryo, Protobuf, Avro/Thrift (ASF).
- **Standards:** own binary format (xlang mode). · **Maturity:** Newer TLP (renamed Fury→Fory 2025); fast-growing. Apache-2.0.

### 5. Batch & stream processing engines

*Shared patterns: DAG execution, master/worker, event-time windowing, checkpointing/exactly-once.*

**Apache Hadoop** — *Java · 🟢 Active*
- **Description:** Foundational big-data platform: **HDFS** (distributed file system), **YARN** (resource manager), and **MapReduce**.
- **Function:** Reliable storage and batch computation across commodity clusters.
- **Patterns:** Master/worker, MapReduce, data-locality scheduling, replicated block storage.
- **Use cases:** Data lakes, large-scale ETL, the substrate under Hive/HBase/Spark/Tez.
- **Interfaces:** HDFS API + `hadoop fs`/S3A; YARN REST/RPC; MapReduce API. Cluster service + client libs. · **Needs:** JVM; ZooKeeper (HA); a cluster of nodes.
- **Pairs with:** Hive, HBase, Spark, Tez, Ranger/Knox, Ambari, ZooKeeper. · **Alternatives:** object storage + Spark/Flink; cloud EMR/Dataproc (external).
- **Standards:** HDFS/S3A, YARN; Kerberos auth. · **Maturity:** Mature; managed as EMR/Dataproc/HDInsight. On-prem use declining vs object-store lakes. Apache-2.0.

**Apache Spark** — *Scala/JVM + Python · 🟢 Active*
- **Description:** Unified analytics engine for batch, SQL, streaming, ML, and graph.
- **Function:** In-memory distributed computation over RDD/DataFrame abstractions.
- **Patterns:** DAG execution, resilient distributed datasets (lineage-based recovery), Catalyst optimizer.
- **Use cases:** ETL, data science (PySpark), ML (MLlib), near-real-time (Structured Streaming).
- **Interfaces:** Scala/Java/Python/R APIs + Spark SQL; Spark Connect (gRPC); JDBC via Thrift server. Cluster service + client. · **Needs:** JVM; a scheduler (YARN/Kubernetes/standalone) + storage.
- **Pairs with:** Iceberg/Hudi/Paimon, Kafka, Hive Metastore, Celeborn/Uniffle (shuffle), Gluten (accel). · **Alternatives:** Flink (ASF, streaming-first); Dask, Ray, Trino (external).
- **Standards:** SQL, JDBC, Parquet/ORC/Arrow. · **Maturity:** Dominant batch/ETL engine; managed as Databricks/EMR/Dataproc. Apache-2.0.

**Apache Flink** — *Java/Scala · 🟢 Active*
- **Description:** Stateful stream-processing engine (with batch as bounded streaming).
- **Function:** Low-latency, exactly-once processing of unbounded data with large managed state.
- **Patterns:** Event-time + watermarks, checkpointing/savepoints, dataflow DAG.
- **Use cases:** Real-time analytics, fraud/anomaly detection, CEP, streaming ETL.
- **Interfaces:** Java/Scala/Python APIs + Flink SQL; REST job API. Cluster service + client. · **Needs:** JVM; scheduler (YARN/Kubernetes/standalone); state backend (RocksDB) + checkpoint storage.
- **Pairs with:** Kafka/Pulsar, Paimon/Iceberg/Hudi, Hive Metastore, Calcite (SQL). · **Alternatives:** Spark Structured Streaming, Kafka Streams, Storm/Samza (ASF); Beam runner.
- **Standards:** SQL, Parquet/Arrow; connectors to many systems. · **Maturity:** Leading streaming engine; managed (Ververica, AWS Managed Flink). Apache-2.0.

**Apache Beam** — *Java/Python/Go · 🟢 Active*
- **Description:** Unified programming model for batch + streaming, portable across runners.
- **Function:** Write pipelines once, run on Flink/Spark/Dataflow, etc.
- **Patterns:** Unified batch/stream model, pluggable runner SPI, windowing/triggers.
- **Use cases:** Portable data pipelines, multi-engine environments.
- **Interfaces:** Java/Python/Go SDKs; runner SPI; portability (Fn) API. Library (runs on a runner). · **Needs:** a runner (Flink/Spark/Dataflow) + its runtime.
- **Pairs with:** Flink/Spark runners, Kafka, Google Dataflow. · **Alternatives:** native Flink/Spark APIs (ASF) when portability isn't needed.
- **Standards:** own model; connectors to many IO systems. · **Maturity:** Mature; the open model behind Google Dataflow. Apache-2.0.

**Apache Storm** — *Clojure/Java · 🟢 Active*
- **Description:** Distributed real-time computation ("streaming before streaming was cool").
- **Function:** Processes unbounded tuple streams with at-least/exactly-once guarantees.
- **Patterns:** Spouts/bolts topology (DAG), record-at-a-time streaming.
- **Use cases:** Real-time ETL, continuous computation.
- **Interfaces:** Java/multi-lang topology API; Nimbus/UI REST. Cluster service. · **Needs:** JVM + ZooKeeper.
- **Pairs with:** Kafka, ZooKeeper, StormCrawler. · **Alternatives:** Flink, Samza, Spark Streaming (ASF) — generally preferred for new builds.
- **Standards:** none specific. · **Maturity:** Mature but largely succeeded by Flink. Apache-2.0.

**Apache Tez** — *Java · 🟢 Active*
- **Description:** DAG execution engine on YARN, a faster replacement for MapReduce.
- **Function:** Runs complex data-processing DAGs for higher-level tools.
- **Patterns:** DAG execution, dynamic graph reconfiguration, container reuse.
- **Use cases:** Execution engine under Hive and Pig.
- **Interfaces:** Java DAG API; runs as YARN application. Library/execution engine (not user-facing). · **Needs:** JVM + Hadoop YARN.
- **Pairs with:** Hive, Pig (as their engine). · **Alternatives:** Spark as Hive engine; MapReduce (ASF).
- **Standards:** YARN. · **Maturity:** Mature; tied to Hadoop/Hive deployments. Apache-2.0.

**Apache Samza** — *Java/Scala · 🟢 Active*
- **Description:** Stream-processing framework tightly integrated with Kafka (from LinkedIn).
- **Function:** Stateful stream processing with local state and changelog fault tolerance.
- **Patterns:** Partitioned local state + changelog, stream/table duality.
- **Use cases:** High-throughput Kafka-centric stream processing.
- **Interfaces:** Java/Scala API + Samza SQL; runs on YARN or standalone. Library/cluster. · **Needs:** JVM; Kafka; YARN (classic) or embedded.
- **Pairs with:** Kafka (tight), YARN, ZooKeeper. · **Alternatives:** Kafka Streams, Flink (ASF).
- **Standards:** Kafka protocol. · **Maturity:** Mature, niche (LinkedIn-scale heritage). Apache-2.0.

**Apache Gluten** — *C++/Java · 🟢 Active (TLP, 2026)*
- **Description:** "Middle layer" that offloads JVM SQL engines to native vectorized backends (Velox/ClickHouse).
- **Function:** Accelerates Spark SQL by executing operators natively instead of on the JVM.
- **Patterns:** Vectorized/native execution offload, columnar (Arrow) interchange, plugin backend.
- **Use cases:** Speeding up existing Spark workloads with little code change.
- **Interfaces:** Spark plugin (drop-in); native backend libraries. Library/plugin. · **Needs:** Spark; a native backend (Velox/ClickHouse); compatible CPU.
- **Pairs with:** Spark, Arrow, Velox, Celeborn. · **Alternatives:** Auron (ASF, incubating), Spark RAPIDS/Photon (external).
- **Standards:** Arrow; Spark SQL semantics. · **Maturity:** New TLP (2026), fast-moving; big performance wins. Apache-2.0.

**Apache Pig** — *Java · 🟡 Low activity*
- **Description:** High-level dataflow language ("Pig Latin") compiling to MapReduce/Tez.
- **Function:** Expresses ETL transformations more concisely than raw MapReduce.
- **Patterns:** Dataflow scripting, logical→physical plan compilation.
- **Use cases:** Legacy Hadoop ETL pipelines.
- **Interfaces:** Pig Latin scripts; UDFs (Java/Python); CLI. Runs on Hadoop. · **Needs:** JVM + Hadoop (MapReduce/Tez).
- **Pairs with:** Hadoop, Tez, HCatalog. · **Alternatives:** Spark/Flink SQL, dbt (external) — preferred for new work.
- **Standards:** none (own language). · **Maturity:** Legacy, low activity. Apache-2.0.

**Apache Celeborn** — *Scala/Java · 🟢 Active*
- **Description:** Intermediate data (remote shuffle) service for Spark/Flink/MapReduce.
- **Function:** Offloads shuffle/spill data to a dedicated service for stability at scale.
- **Patterns:** Disaggregated shuffle, push-based shuffle, storage/compute separation.
- **Use cases:** Large/elastic (Kubernetes) Spark clusters needing reliable shuffle.
- **Interfaces:** Spark/Flink/MR shuffle plugin; master/worker service. Service + client plugin. · **Needs:** JVM; its own master/worker cluster.
- **Pairs with:** Spark, Flink, Gluten, Kubernetes. · **Alternatives:** Uniffle (ASF); vendor remote-shuffle (external).
- **Standards:** engine shuffle SPIs. · **Maturity:** Growing; used for elastic Spark on k8s. Apache-2.0.

**Apache Uniffle** — *Java · 🟢 Active*
- **Description:** Unified remote shuffle service for distributed compute engines.
- **Function:** Externalizes shuffle data (similar goal to Celeborn).
- **Patterns:** Remote/disaggregated shuffle, pluggable storage.
- **Use cases:** Shuffle-heavy Spark/MapReduce/Tez jobs on elastic infrastructure.
- **Interfaces:** Shuffle plugins for Spark/MR/Tez; coordinator/shuffle-server service. Service + client plugin. · **Needs:** JVM; its own cluster; optional HDFS/object store for spill.
- **Pairs with:** Spark, MapReduce, Tez, HDFS/object storage. · **Alternatives:** Celeborn (ASF).
- **Standards:** engine shuffle SPIs. · **Maturity:** TLP (2024); production at Tencent-scale. Apache-2.0.

**Apache Crunch** — *Java · 🗄️ Attic*
- **Description:** Java library for writing MapReduce pipelines.
- **Function:** Typed pipeline API over MapReduce/Spark.
- **Patterns:** Pipeline combinators (FlumeJava-style).
- **Use cases:** Legacy Hadoop pipelines.
- **Leverage note:** 🗄️ Retired — use Spark/Beam DataFrames/pipelines for new work.

### 6. SQL engines, query frameworks & lakehouse

*Shared patterns: cost-based optimization, pluggable adapters, open table formats, catalog abstraction, MPP scatter-gather.*

**Apache Hive** — *Java · 🟢 Active*
- **Description:** SQL-on-Hadoop data warehouse with the de-facto **Hive Metastore**.
- **Function:** Compiles SQL (HiveQL) to distributed jobs; central metadata catalog.
- **Patterns:** SQL→DAG compilation, metastore catalog, partitioning.
- **Use cases:** Batch warehousing on data lakes; the Metastore underpins Spark/Trino/Presto.
- **Interfaces:** HiveQL; JDBC/ODBC via HiveServer2 (Thrift); Metastore Thrift API. Service + catalog. · **Needs:** JVM; Hadoop/YARN or Tez; a metastore DB (Derby/MySQL/Postgres).
- **Pairs with:** Spark/Trino/Flink (via Metastore), Tez, Ranger, ORC/Parquet. · **Alternatives:** Trino/Presto, Spark SQL (ASF/external); Polaris/Gravitino as newer catalogs.
- **Standards:** SQL, JDBC/ODBC, Hive Metastore API. · **Maturity:** Mature; the Metastore is near-universal even where HiveQL isn't. Apache-2.0.

**Apache Calcite** — *Java · 🟢 Active*
- **Description:** Framework for building SQL parsers, optimizers, and federated query engines.
- **Function:** Provides SQL parsing, relational algebra, and a cost-based optimizer as a library.
- **Patterns:** Volcano/cost-based optimizer, pluggable adapters, relational algebra IR.
- **Use cases:** The query brain inside Flink SQL, Druid, Hive, Beam SQL, and many engines.
- **Interfaces:** Java embedding API; JDBC (Avatica); adapter SPI. Embeddable library. · **Needs:** JVM.
- **Pairs with:** Flink, Druid, Beam, Hive, Phoenix, Kylin (all embed it). · **Alternatives:** write your own optimizer; Trino's planner (external).
- **Standards:** SQL, JDBC (Avatica). · **Maturity:** Mature; the standard "SQL brain" library in the JVM world. Apache-2.0.

**Apache Impala** — *C++/Java · 🟢 Active*
- **Description:** Massively parallel (MPP) SQL engine for Hadoop data.
- **Function:** Low-latency interactive SQL directly over HDFS/Kudu/object storage.
- **Patterns:** MPP scatter-gather, LLVM codegen, columnar scans.
- **Use cases:** Interactive BI/ad-hoc analytics on lake data.
- **Interfaces:** SQL; JDBC/ODBC; HiveServer2-compatible. Cluster service. · **Needs:** Hive Metastore; HDFS/Kudu/S3; a cluster.
- **Pairs with:** Kudu, Hive Metastore, Parquet, Ranger. · **Alternatives:** Trino/Presto, Spark SQL, Doris (ASF/external).
- **Standards:** SQL, JDBC/ODBC. · **Maturity:** Mature (Cloudera stacks). Apache-2.0.

**Apache Drill** — *Java · 🟢 Active*
- **Description:** Schema-free SQL query engine for files, NoSQL, and more.
- **Function:** Query JSON/Parquet/CSV/HBase without predefined schemas.
- **Patterns:** Schema-on-read, columnar execution, pluggable storage.
- **Use cases:** Ad-hoc exploration across heterogeneous sources.
- **Interfaces:** SQL; JDBC/ODBC/REST; storage plugin SPI. Service. · **Needs:** JVM; ZooKeeper (cluster).
- **Pairs with:** files/object stores, HBase, Hive Metastore. · **Alternatives:** Trino/Presto, DuckDB (external); Spark SQL (ASF).
- **Standards:** SQL, JDBC/ODBC. · **Maturity:** Mature, modest activity. Apache-2.0.

**Apache Phoenix** — *Java · 🟢 Active*
- **Description:** Relational SQL layer over Apache HBase.
- **Function:** Turns HBase into an OLTP-ish SQL store with secondary indexes.
- **Patterns:** SQL skin over key-value store, coprocessor pushdown.
- **Use cases:** Low-latency SQL access to HBase data.
- **Interfaces:** SQL; JDBC; thin (PQS) + thick drivers. Library/driver + query server. · **Needs:** HBase (+ HDFS + ZooKeeper).
- **Pairs with:** HBase, Spark (connector). · **Alternatives:** direct HBase API; Cassandra+CQL (ASF).
- **Standards:** SQL, JDBC. · **Maturity:** Mature within HBase shops. Apache-2.0.

**Apache Kylin** — *Java · 🟢 Active*
- **Description:** Distributed OLAP engine using precomputed cubes.
- **Function:** Sub-second multidimensional analytics over huge datasets.
- **Patterns:** Precomputed OLAP cube, dimensional modeling, materialization.
- **Use cases:** BI dashboards needing constant-time aggregate queries.
- **Interfaces:** SQL; JDBC/ODBC/REST; MDX (via Mondrian). Service. · **Needs:** JVM; Hive/Spark (build), HBase or Parquet (storage); Hadoop.
- **Pairs with:** Hive, Spark, Superset/Tableau (BI). · **Alternatives:** Druid/Pinot/Doris (ASF, no pre-build needed).
- **Standards:** SQL, JDBC/ODBC, MDX. · **Maturity:** Mature; cube-build model is heavier than newer OLAP stores. Apache-2.0.

**Apache Kyuubi** — *Scala · 🟢 Active*
- **Description:** Multi-tenant gateway for serverless SQL on Spark/Flink/Trino.
- **Function:** Provides JDBC/Thrift SQL endpoints with isolation and resource sharing.
- **Patterns:** Storage/compute separation, engine multiplexing, gateway.
- **Use cases:** Enterprise "SQL as a service" over lakehouse engines.
- **Interfaces:** JDBC/ODBC + Thrift/REST (HiveServer2-compatible). Gateway service. · **Needs:** JVM; a backing engine (Spark/Flink/Trino) + its cluster.
- **Pairs with:** Spark, Flink, Trino, Iceberg, Ranger. · **Alternatives:** Spark Thrift Server, Trino gateway (ASF/external).
- **Standards:** SQL, JDBC/ODBC, HiveServer2 Thrift. · **Maturity:** Growing; popular for multi-tenant lakehouse SQL. Apache-2.0.

**Apache DataFusion** — *Rust · 🟢 Active (TLP, 2024)*
- **Description:** Fast, extensible query engine and execution framework built on Arrow (a Rust library + the Ballista distributed engine).
- **Function:** Embeddable SQL/DataFrame engine with a vectorized columnar executor.
- **Patterns:** Columnar vectorized execution, extensible optimizer, embeddable engine.
- **Use cases:** Building custom databases/engines in Rust; fast in-process analytics.
- **Interfaces:** Rust crate (SQL + DataFrame API); Python bindings; Ballista for distributed. Embeddable library. · **Needs:** Rust runtime; no service.
- **Pairs with:** Arrow, Parquet, object stores; embedded in many Rust databases. · **Alternatives:** DuckDB, Polars, Velox (external).
- **Standards:** SQL, Arrow, Parquet. · **Maturity:** Fast-growing; the go-to embeddable Rust engine. Apache-2.0.

**Apache Iceberg** — *Java/Multi-language · 🟢 Active*
- **Description:** Open table format for huge analytic datasets.
- **Function:** Adds ACID snapshots, schema/partition evolution, and time travel over data-lake files.
- **Patterns:** Open table format, snapshot isolation (MVCC), hidden partitioning, catalog abstraction.
- **Use cases:** Lakehouse tables queried by Spark/Flink/Trino/Dremio/Snowflake.
- **Interfaces:** Table format + libraries (Java/Python/Rust/Go); REST catalog API. Library + catalog spec. · **Needs:** object/file storage; a catalog (Polaris/Gravitino/Hive/Glue); an engine.
- **Pairs with:** Spark/Flink/Trino, Parquet/ORC/Avro, Polaris/Gravitino. · **Alternatives:** Hudi, Paimon (ASF); Delta Lake (external).
- **Standards:** Iceberg table spec + REST catalog; Parquet/ORC/Avro. · **Maturity:** The emerging lakehouse standard; supported by every major engine/warehouse. Apache-2.0.

**Apache Hudi** — *Java · 🟢 Active*
- **Description:** Transactional data-lake storage with upserts and incremental processing.
- **Function:** Mutable lake tables (copy-on-write / merge-on-read) with record-level updates.
- **Patterns:** Open table format, LSM-like merge-on-read, incremental "pull" queries.
- **Use cases:** CDC/upsert pipelines into the lake, GDPR deletes, near-real-time tables.
- **Interfaces:** Table format + Spark/Flink libraries; DeltaStreamer ingestion. Library. · **Needs:** object/file storage; Spark or Flink; a metastore/catalog.
- **Pairs with:** Spark/Flink, Kafka (CDC), Hive Metastore, XTable. · **Alternatives:** Iceberg, Paimon (ASF); Delta Lake (external).
- **Standards:** Hudi table spec; Parquet/Avro. · **Maturity:** Mature; strongest for upsert/CDC lakes. Apache-2.0.

**Apache Paimon** — *Java · 🟢 Active*
- **Description:** Streaming lakehouse format (grew out of Flink Table Store).
- **Function:** Unified streaming + batch lake table with LSM storage and CDC ingestion.
- **Patterns:** LSM table on object store, streaming-first table format, changelog producing.
- **Use cases:** Real-time lakehouse with Flink; streaming updates + batch reads.
- **Interfaces:** Table format + Flink/Spark/Trino connectors. Library. · **Needs:** object/file storage; Flink (primary) or Spark; a catalog.
- **Pairs with:** Flink (tight), Spark/Trino, Kafka (CDC). · **Alternatives:** Hudi, Iceberg (ASF); Delta (external).
- **Standards:** Paimon table spec; Parquet/ORC/Avro. · **Maturity:** Newer TLP; strong Flink-native streaming lakehouse. Apache-2.0.

**Apache Polaris** — *Java · 🟢 Active (TLP, 2026)*
- **Description:** Open catalog for Apache Iceberg (donated by Snowflake/Dremio).
- **Function:** REST catalog + access control governing Iceberg tables across engines.
- **Patterns:** Catalog abstraction, Iceberg REST catalog API, RBAC over tables.
- **Use cases:** Vendor-neutral, multi-engine governance of lakehouse tables.
- **Interfaces:** Iceberg REST Catalog API; RBAC admin API. Standalone service. · **Needs:** JVM; a metadata DB; object storage (for the tables it governs).
- **Pairs with:** Iceberg, Spark/Flink/Trino, Snowflake/Dremio. · **Alternatives:** Gravitino, Hive Metastore (ASF); AWS Glue, Unity Catalog (external).
- **Standards:** Iceberg REST Catalog. · **Maturity:** New TLP (2026); backed by Snowflake/Dremio. Apache-2.0.

**Apache Gravitino** — *Java · 🟢 Active (TLP, 2025)*
- **Description:** Unified metadata lake / multi-catalog metadata management.
- **Function:** One API/governance layer across metastores, catalogs, and data sources.
- **Patterns:** Federated catalog, unified metadata model, governance plane.
- **Use cases:** Cataloging and governing data + AI assets across heterogeneous stores.
- **Interfaces:** REST + Iceberg REST catalog; connectors to Hive/JDBC/Kafka/filesets. Standalone service. · **Needs:** JVM; a metadata store; the underlying catalogs/sources.
- **Pairs with:** Iceberg, Hive Metastore, Spark/Flink/Trino, cloud catalogs. · **Alternatives:** Polaris (ASF, Iceberg-focused); Unity Catalog, DataHub (external).
- **Standards:** Iceberg REST, JDBC. · **Maturity:** TLP (2025); broader scope than a single-format catalog. Apache-2.0.

**Apache XTable** — *Java · 🥚 Incubating*
- **Description:** Cross-table interoperability between Iceberg, Hudi, and Delta Lake.
- **Function:** Translates table metadata so one dataset is readable as multiple formats.
- **Patterns:** Format interoperability/adapter, metadata translation (no data copy).
- **Use cases:** Avoiding lakehouse format lock-in; multi-engine access to one dataset.
- **Interfaces:** CLI + Java library; reads/writes Iceberg/Hudi/Delta metadata. Library/tool. · **Needs:** JVM; existing lake tables + storage.
- **Pairs with:** Iceberg, Hudi, Delta Lake, any engine reading those. · **Alternatives:** committing to one format (ASF); Unity/Delta UniForm (external).
- **Standards:** Iceberg/Hudi/Delta table specs. · **Maturity:** Incubating; solves real format lock-in. Apache-2.0.

### 7. Databases & data stores

*Shared patterns: sharding, LSM/WAL, tunable consistency, in-memory data grids, time-series compaction.*

**Apache Cassandra** — *Java · 🟢 Active*
- **Description:** Wide-column, masterless distributed NoSQL database.
- **Function:** Highly available, linearly scalable storage with tunable consistency.
- **Patterns:** Consistent-hashing ring, LSM storage, gossip membership, quorum reads/writes, Paxos LWTs.
- **Use cases:** Always-on, write-heavy workloads across data centers (messaging, IoT, time series).
- **Interfaces:** CQL over native protocol; drivers for most languages. Cluster service. · **Needs:** JVM; a multi-node cluster; no external coordinator (gossip).
- **Pairs with:** Spark (analytics connector), Kafka (sink), Solr/Lucene (search, via distros). · **Alternatives:** HBase, Accumulo (ASF); ScyllaDB, DynamoDB (external).
- **Standards:** CQL (own); native protocol. · **Maturity:** Very mature; managed as Astra/Keyspaces/Cosmos. Apache-2.0.

**Apache HBase** — *Java · 🟢 Active*
- **Description:** Distributed, sorted wide-column store on HDFS (a BigTable clone).
- **Function:** Random real-time read/write access to very large tables.
- **Patterns:** LSM + WAL, region sharding, master/region-server, ZooKeeper coordination.
- **Use cases:** Massive sparse tables, time-series, serving layers (often with Phoenix on top).
- **Interfaces:** Java client API; Thrift & REST gateways; shell. Cluster service (embeddable for tests). · **Needs:** HDFS + ZooKeeper; JVM; a cluster.
- **Pairs with:** Phoenix (SQL), Spark/MapReduce (bulk), Kafka (ingest), Ranger (authz). · **Alternatives:** Cassandra, Accumulo (ASF); Bigtable, ScyllaDB (external).
- **Standards:** none specific; Thrift/REST gateways. · **Maturity:** Mature; managed options on major clouds. Apache-2.0.

**Apache CouchDB** — *Erlang · 🟢 Active*
- **Description:** Document database with HTTP/JSON API and multi-master replication.
- **Function:** Stores JSON documents; syncs offline-first apps.
- **Patterns:** MVCC, append-only B-tree storage, eventual-consistency replication, map/reduce views.
- **Use cases:** Offline-first/mobile sync (with PouchDB), distributed document storage.
- **Interfaces:** HTTP/JSON REST API; replication protocol. Standalone service. · **Needs:** Erlang runtime (bundled); single node or cluster.
- **Pairs with:** PouchDB (browser sync), Mango queries. · **Alternatives:** MongoDB, Couchbase (external).
- **Standards:** HTTP, JSON; CouchDB replication protocol. · **Maturity:** Mature; Cloudant is a managed variant. Apache-2.0.

**Apache Derby** — *Java · 🟢 Active*
- **Description:** Lightweight, pure-Java embeddable relational database.
- **Function:** Full SQL/JDBC RDBMS that runs in-process or as a small server.
- **Patterns:** Embedded database, ACID transactions.
- **Use cases:** Embedded app storage, testing, prototyping (shipped in the JDK as JavaDB).
- **Interfaces:** JDBC; embedded or network-server mode. Embeddable library + optional server. · **Needs:** JVM only.
- **Pairs with:** any JVM app; Hive Metastore (default dev DB). · **Alternatives:** H2, HSQLDB, SQLite (external).
- **Standards:** SQL, JDBC. · **Maturity:** Mature; great for embedded/test. Apache-2.0.

**Apache Ignite** — *Java · 🟢 Active*
- **Description:** Distributed in-memory computing platform / data grid.
- **Function:** In-memory key-value + SQL store with compute, caching, and persistence.
- **Patterns:** In-memory data grid, affinity colocation, distributed SQL, durable memory.
- **Use cases:** Caching/acceleration layers, HTAP, in-memory compute.
- **Interfaces:** JDBC/ODBC SQL; key-value & compute APIs; thin clients (many langs); JCache. Cluster service + embeddable. · **Needs:** JVM; a cluster (optional native persistence).
- **Pairs with:** RDBMS (cache-through), Spark (integration), Kafka. · **Alternatives:** Geode (ASF); Hazelcast, Redis (external).
- **Standards:** SQL/JDBC, JCache (JSR-107). · **Maturity:** Mature; GridGain is the commercial/managed form. Apache-2.0.

**Apache Geode** — *Java · 🟢 Active*
- **Description:** In-memory data grid (the open-source core of GemFire).
- **Function:** Low-latency distributed data management with event notifications.
- **Patterns:** In-memory data grid, partitioned/replicated regions, continuous queries.
- **Use cases:** High-throughput, low-latency transactional caching (finance, trading).
- **Interfaces:** Java API; OQL; REST; memcached/Redis-ish protocols; Spring Data Geode. Cluster service + client. · **Needs:** JVM; a cluster.
- **Pairs with:** Spring (Spring Data), RDBMS (cache), Lucene (region indexing). · **Alternatives:** Ignite (ASF); Hazelcast, GemFire (external/commercial).
- **Standards:** JCache-like; OQL (own). · **Maturity:** Mature; VMware GemFire is the commercial twin. Apache-2.0.

**Apache Accumulo** — *Java · 🟢 Active*
- **Description:** Sorted, distributed key-value store (BigTable design) with cell-level security.
- **Function:** Secure large-scale storage with per-cell access labels.
- **Patterns:** LSM + WAL, iterators (server-side compute), cell-level visibility labels.
- **Use cases:** Security-sensitive big-data (originated at the NSA), fine-grained access control.
- **Interfaces:** Java client API; iterators (server-side); no SQL by default. Cluster service. · **Needs:** HDFS + ZooKeeper; JVM.
- **Pairs with:** Hadoop, Spark, Geomesa (geospatial). · **Alternatives:** HBase, Cassandra (ASF).
- **Standards:** none specific. · **Maturity:** Mature; strong in government/high-security settings. Apache-2.0.

**Apache Kudu** — *C++ · 🟢 Active*
- **Description:** Columnar storage engine for fast analytics on fast-changing data.
- **Function:** Combines low-latency random access with efficient columnar scans.
- **Patterns:** Hybrid row/columnar, Raft-replicated tablets, storage/compute separation (with Impala).
- **Use cases:** Real-time analytics where data mutates and must also scan fast.
- **Interfaces:** C++/Java/Python client APIs; Impala as SQL front end. Cluster service. · **Needs:** its own daemons (no HDFS); a cluster.
- **Pairs with:** Impala (SQL), Spark, NiFi (ingest). · **Alternatives:** HBase + Phoenix (ASF); ClickHouse, Pinot (external/ASF).
- **Standards:** none specific; Impala SQL. · **Maturity:** Mature (Cloudera). Apache-2.0.

**Apache IoTDB** — *Java · 🟢 Active*
- **Description:** Time-series database purpose-built for IoT device data.
- **Function:** Ingests and queries high-frequency sensor time series with heavy compression.
- **Patterns:** LSM-style TsFile storage, time-partitioned schema tree, edge-cloud collaboration.
- **Use cases:** Industrial IoT, telemetry, device monitoring at scale.
- **Interfaces:** SQL-like IoTDB query language; JDBC; MQTT/REST ingest; session API; cluster via Ratis. Service + embeddable (edge). · **Needs:** JVM; Ratis for clustering.
- **Pairs with:** Flink/Spark (analytics), Grafana, MQTT brokers, PLC4X. · **Alternatives:** InfluxDB, TimescaleDB, Prometheus (external).
- **Standards:** SQL-ish, JDBC, MQTT; TsFile format. · **Maturity:** Growing; strong in industrial IoT. Apache-2.0.

**Apache Doris** — *C++/Java · 🟢 Active*
- **Description:** Real-time MPP analytical (OLAP) database, MySQL-protocol compatible.
- **Function:** Sub-second analytics with high-concurrency serving.
- **Patterns:** MPP, columnar + vectorized execution, materialized views, tablet sharding.
- **Use cases:** Real-time dashboards, ad-hoc OLAP, user-facing analytics.
- **Interfaces:** MySQL wire protocol + JDBC/ODBC; stream/routine load; Flink/Spark connectors. Cluster service. · **Needs:** its own FE/BE daemons; a cluster.
- **Pairs with:** Flink/Spark (load), Kafka, BI tools (via MySQL protocol). · **Alternatives:** Druid, Pinot, Kylin (ASF); ClickHouse, StarRocks (external).
- **Standards:** MySQL protocol, SQL, JDBC/ODBC. · **Maturity:** Mature, fast-growing; SelectDB is the managed form. Apache-2.0.

**Apache ShardingSphere** — *Java · 🟢 Active*
- **Description:** Distributed database middleware ecosystem (JDBC driver + proxy).
- **Function:** Adds sharding, read/write splitting, encryption, and distributed transactions over existing databases.
- **Patterns:** Transparent sharding, SQL routing/rewriting, pluggable governance.
- **Use cases:** Scaling MySQL/PostgreSQL horizontally without rewriting apps.
- **Interfaces:** JDBC driver (in-app) or MySQL/PostgreSQL-protocol proxy; DistSQL admin. Library + proxy service. · **Needs:** JVM; backing databases; a registry (ZooKeeper/etcd) for the proxy.
- **Pairs with:** MySQL/PostgreSQL, ZooKeeper, Seata (distributed tx). · **Alternatives:** Vitess, Citus (external).
- **Standards:** MySQL/PostgreSQL wire protocols, JDBC, SQL. · **Maturity:** Mature; widely used for RDBMS scale-out. Apache-2.0.

### 8. Messaging, streaming platforms & integration

*Shared patterns: publish/subscribe, append-only log, EIP pipes-and-filters, broker/queue, protocol bridging.*

**Apache Kafka** — *Java/Scala · 🟢 Active*
- **Description:** Distributed event streaming platform (durable, partitioned commit log).
- **Function:** High-throughput pub/sub + storage of event streams; **Kafka Streams** and **Connect** add processing/integration.
- **Patterns:** Append-only partitioned log, consumer groups, pull-based consumption, log compaction; modern KRaft (Raft) metadata.
- **Use cases:** Event backbones, log aggregation, stream processing, CDC, microservice eventing.
- **Interfaces:** Kafka binary protocol; clients in most languages; Connect (connectors), Streams API, Schema Registry. Cluster service. · **Needs:** JVM; KRaft (modern) or ZooKeeper (legacy); a broker cluster.
- **Pairs with:** Flink/Spark/Samza, Connect (JDBC/Debezium), Avro/Schema Registry, Iceberg/Hudi sinks. · **Alternatives:** Pulsar, RocketMQ (ASF); Redpanda, AWS Kinesis (external).
- **Standards:** Kafka protocol (de-facto); many clients re-implement it. · **Maturity:** Industry-standard event backbone; managed as MSK/Confluent. Apache-2.0.

**Apache Pulsar** — *Java · 🟢 Active*
- **Description:** Cloud-native distributed messaging + streaming with tiered storage.
- **Function:** Unified queuing and streaming with multi-tenancy and geo-replication.
- **Patterns:** Broker/stateful-storage separation (BookKeeper), segment-centric storage, tiered offload.
- **Use cases:** Multi-tenant messaging, geo-replicated event streaming, unified queue+stream.
- **Interfaces:** Pulsar protocol + clients; Kafka-compat & AMQP/MQTT adapters; Functions; Pulsar SQL. Cluster service. · **Needs:** JVM; BookKeeper + ZooKeeper (or etcd); a cluster.
- **Pairs with:** BookKeeper (storage), Flink/Spark, Functions, tiered object storage. · **Alternatives:** Kafka, RocketMQ (ASF); NATS (external).
- **Standards:** own protocol; Kafka/AMQP/MQTT via adapters. · **Maturity:** Mature; managed by StreamNative. Apache-2.0.

**Apache ActiveMQ** — *Java · 🟢 Active*
- **Description:** Popular JMS message broker; **Artemis** is the high-performance next generation.
- **Function:** Reliable queue/topic messaging with many protocol connectors (AMQP, MQTT, STOMP).
- **Patterns:** Broker + queues/topics, store-and-forward, protocol gateways.
- **Use cases:** Enterprise messaging/JMS, IoT (MQTT), system integration.
- **Interfaces:** JMS; AMQP, MQTT, STOMP, OpenWire; management console. Broker service + client libs. · **Needs:** JVM; a broker (persistence store).
- **Pairs with:** Camel (routing), JMS apps, IoT (MQTT) devices. · **Alternatives:** RabbitMQ (external); Pulsar/RocketMQ (ASF) for streaming scale.
- **Standards:** JMS, AMQP 1.0, MQTT, STOMP. · **Maturity:** Mature; the default JMS broker (use Artemis for new). Apache-2.0.

**Apache RocketMQ** — *Java · 🟢 Active*
- **Description:** Low-latency, high-throughput distributed messaging (from Alibaba).
- **Function:** Transactional, ordered, and scheduled messaging plus streaming.
- **Patterns:** Append log storage, name-server discovery, transactional messages.
- **Use cases:** E-commerce-scale order/transaction eventing, financial messaging.
- **Interfaces:** RocketMQ clients (Java/C++/Go/…); gRPC (5.x); HTTP; connectors. Cluster service. · **Needs:** JVM; name servers + brokers.
- **Pairs with:** Flink/Spark connectors, EventMesh, Dubbo. · **Alternatives:** Kafka, Pulsar (ASF); RabbitMQ (external).
- **Standards:** own protocol; gRPC in 5.x. · **Maturity:** Mature; proven at Alibaba Singles-Day scale. Apache-2.0.

**Apache Qpid** — *Java/C++ · 🟢 Active*
- **Description:** Messaging built on the AMQP standard.
- **Function:** AMQP brokers and client libraries.
- **Patterns:** Standardized wire protocol (AMQP), broker + clients.
- **Use cases:** Interoperable, standards-based enterprise messaging.
- **Interfaces:** AMQP 1.0/0-10; JMS client; management. Broker service + client libs. · **Needs:** JVM (Broker-J) or C++ broker.
- **Pairs with:** JMS apps, Red Hat AMQ, any AMQP client. · **Alternatives:** ActiveMQ (ASF); RabbitMQ (external).
- **Standards:** AMQP (1.0 & 0-10), JMS. · **Maturity:** Mature; the reference for standards-pure AMQP. Apache-2.0.

**Apache Camel** — *Java · 🟢 Active*
- **Description:** The leading integration framework implementing the Enterprise Integration Patterns; includes **Camel K** (Kubernetes) and **Camel Quarkus**.
- **Function:** Routes and transforms messages between 300+ systems via a routing DSL.
- **Patterns:** Pipes-and-filters, EIP catalog, component/endpoint SPI, DSL-defined routes.
- **Use cases:** System-to-system integration, API/protocol mediation, ETL glue.
- **Interfaces:** Java/XML/YAML route DSL; 300+ component connectors; runs embedded, in Spring Boot, Quarkus, or Karaf. Library/framework. · **Needs:** JVM (or Quarkus native); a host runtime.
- **Pairs with:** ActiveMQ/Kafka, CXF, Karaf, Spring Boot, Quarkus. · **Alternatives:** Spring Integration, Mule, Kafka Connect (external/ASF).
- **Standards:** EIP; speaks dozens of protocols via components. · **Maturity:** Mature; the default JVM integration toolkit. Apache-2.0.

**Apache ServiceMix** — *Java · 🟡 Low activity*
- **Description:** OSGi-based enterprise service bus (ESB) assembling Karaf + Camel + CXF + ActiveMQ.
- **Function:** Integration container bundling ASF integration projects.
- **Patterns:** ESB, OSGi runtime assembly.
- **Use cases:** Legacy ESB deployments.
- **Interfaces:** Karaf console; deploys Camel routes/CXF services. Runtime assembly. · **Needs:** JVM + Karaf/OSGi.
- **Pairs with:** Camel, CXF, ActiveMQ, Karaf. · **Alternatives:** use Camel directly on Spring Boot/Quarkus (ASF) — preferred for new work.
- **Standards:** OSGi, JBI (historical). · **Maturity:** Low activity; superseded by Camel-on-Karaf. Apache-2.0.

**Apache Synapse** — *Java · 🟡 Low activity*
- **Description:** Lightweight ESB and XML/web-services mediation engine.
- **Function:** Routing, transformation, and mediation of SOAP/REST traffic.
- **Patterns:** Mediation sequences, EIP, proxy services.
- **Use cases:** Web-services mediation/gateway (historically under WSO2).
- **Interfaces:** XML mediation config; proxy services; HTTP/SOAP/JMS transports. Service. · **Needs:** JVM.
- **Pairs with:** Axis2, WSO2 stack. · **Alternatives:** Camel, APISIX (ASF).
- **Standards:** SOAP/WS-*, REST, JMS. · **Maturity:** Low activity. Apache-2.0.

**Apache EventMesh** — *Java · 🟢 Active*
- **Description:** Cloud-native event middleware / "event mesh."
- **Function:** Decouples producers/consumers across clouds with eventing, orchestration, and connectors.
- **Patterns:** Event mesh, pub/sub abstraction over multiple stores, serverless eventing.
- **Use cases:** Distributed, multi-cloud event-driven architectures.
- **Interfaces:** CloudEvents; gRPC/TCP/HTTP SDKs; connector SPI. Service + SDKs. · **Needs:** JVM; a backing store (RocketMQ/Kafka/Pulsar).
- **Pairs with:** RocketMQ/Kafka/Pulsar, Dubbo, serverless runtimes. · **Alternatives:** Knative Eventing, NATS (external).
- **Standards:** CloudEvents. · **Maturity:** Growing; useful as an eventing abstraction layer. Apache-2.0.

### 9. RPC, microservices & service frameworks

*Shared patterns: IDL + codegen, service discovery, client-side load balancing, circuit breaking.*

**Apache Dubbo** — *Java · 🟢 Active*
- **Description:** High-performance RPC and microservice framework (from Alibaba).
- **Function:** Remote service invocation with registry-based discovery and governance.
- **Patterns:** RPC proxy/stub, service discovery, client-side load balancing, SPI extensibility.
- **Use cases:** Large-scale Java microservice fabrics, service governance.
- **Interfaces:** Dubbo/Triple (gRPC-compatible) protocols; Java/Go SDKs; registry integrations. Library/framework. · **Needs:** JVM (or Go); a registry (ZooKeeper/Nacos).
- **Pairs with:** ZooKeeper/Nacos, ShenYu/APISIX (gateway), SkyWalking. · **Alternatives:** gRPC, Spring Cloud (external); ServiceComb (ASF).
- **Standards:** gRPC (Triple), own Dubbo protocol. · **Maturity:** Mature; huge in China-origin microservice stacks. Apache-2.0.

**Apache ServiceComb** — *Java · 🟢 Active*
- **Description:** Microservices framework (service center, config, contracts).
- **Function:** Service registration/discovery, contract-first APIs, resilience.
- **Patterns:** Service mesh/registry, contract-first (OpenAPI), circuit breaking.
- **Use cases:** Building and governing microservice systems.
- **Interfaces:** REST/gRPC; Java SDK; service-center & config-server. Framework + services. · **Needs:** JVM; service center (registry).
- **Pairs with:** its service center, SkyWalking, gateways. · **Alternatives:** Dubbo (ASF); Spring Cloud (external).
- **Standards:** OpenAPI, REST, gRPC. · **Maturity:** Mature, smaller community than Dubbo. Apache-2.0.

**Apache bRPC** — *C++ · 🟢 Active*
- **Description:** Industrial-grade C++ RPC framework (from Baidu).
- **Function:** High-concurrency RPC with rich protocol support and built-in profiling.
- **Patterns:** RPC with pluggable protocols, M:N threading, built-in observability.
- **Use cases:** Performance-critical C++ services (search, storage, ML serving).
- **Interfaces:** C++ API; speaks many protocols (Protobuf/HTTP/gRPC/Redis/Memcached/…); built-in `/vars` dashboards. Library. · **Needs:** C++ toolchain.
- **Pairs with:** Protobuf, braft (Raft), C++ backends. · **Alternatives:** gRPC C++ (external); Thrift (ASF).
- **Standards:** Protobuf, gRPC, HTTP. · **Maturity:** Mature; battle-tested at Baidu scale. Apache-2.0.

**Apache Avro RPC / Thrift** — *(see [§4](#4-storage-formats--serialization))*
- Both double as cross-language RPC frameworks via their IDL + codegen model. For composability details see their entries in §4; both are **embeddable libraries** needing only a host-language runtime and speaking their own IDL/wire protocols.

### 10. Coordination, consensus & cluster management

*Shared patterns: replicated state machine (Paxos/Raft/ZAB), leader election, distributed log, cluster scheduling.*

**Apache ZooKeeper** — *Java · 🟢 Active*
- **Description:** Centralized service for configuration, naming, synchronization, and group membership.
- **Function:** Provides a consistent, watchable hierarchical namespace (znodes) for coordination.
- **Patterns:** Replicated state machine (ZAB), leader election, watches/ephemeral nodes.
- **Use cases:** Coordination backbone for HBase, Kafka (legacy), Solr, and countless distributed systems.
- **Interfaces:** ZooKeeper client protocol; Java/C clients; `zkCli`. Standalone service (ensemble). · **Needs:** JVM; an odd-sized ensemble (3/5 nodes).
- **Pairs with:** HBase, Solr, Kafka (legacy), Accumulo, Helix — usually via **Curator**. · **Alternatives:** etcd, Consul (external); Ratis (ASF) for embedding Raft.
- **Standards:** none (own protocol). · **Maturity:** Ubiquitous coordination primitive; very mature. Apache-2.0.

**Apache Curator** — *Java · 🟢 Active*
- **Description:** High-level ZooKeeper client with recipes.
- **Function:** Robust connection handling plus ready-made distributed primitives (locks, leader election, queues).
- **Patterns:** Recipe library over ZooKeeper, retry/connection-state management.
- **Use cases:** Anything using ZooKeeper that wants correct, reusable coordination primitives.
- **Interfaces:** Java API (recipes); wraps the ZooKeeper client. Embeddable library. · **Needs:** JVM + a ZooKeeper ensemble.
- **Pairs with:** ZooKeeper (always), any ZK-based system. · **Alternatives:** raw ZooKeeper client (error-prone); etcd/Consul client libs (external).
- **Standards:** ZooKeeper protocol. · **Maturity:** Mature; the correct way to use ZooKeeper. Apache-2.0.

**Apache BookKeeper** — *Java · 🟢 Active*
- **Description:** Scalable, low-latency distributed storage for append-only logs ("ledgers"); includes **DistributedLog**.
- **Function:** Durable, replicated write-ahead log as a service.
- **Patterns:** Replicated append-only ledgers, quorum writes, segment storage.
- **Use cases:** Durable storage layer under Pulsar; WAL-as-a-service, stream storage.
- **Interfaces:** Java client (ledger API); DistributedLog API. Cluster service + client lib. · **Needs:** JVM; ZooKeeper (or etcd); bookie nodes.
- **Pairs with:** Pulsar (its storage layer), ZooKeeper. · **Alternatives:** Kafka's own log (ASF) for many use cases; cloud log services (external).
- **Standards:** none specific. · **Maturity:** Mature; proven under Pulsar. Apache-2.0.

**Apache Ratis** — *Java · 🟢 Active*
- **Description:** Java library implementing the Raft consensus protocol.
- **Function:** Embeddable consensus for building replicated state machines.
- **Patterns:** Raft (leader election + replicated log), pluggable state machine/transport.
- **Use cases:** Consensus inside Ozone, IoTDB, and other systems needing strong consistency.
- **Interfaces:** Java embedding API; pluggable RPC (gRPC/Netty). Embeddable library. · **Needs:** JVM.
- **Pairs with:** Ozone, IoTDB (embed it). · **Alternatives:** ZooKeeper (ASF, as a service); etcd/raft, braft (external).
- **Standards:** Raft. · **Maturity:** Mature embeddable Raft for the JVM. Apache-2.0.

**Apache Helix** — *Java · 🟢 Active*
- **Description:** Generic cluster-management framework (from LinkedIn).
- **Function:** Assigns partitions/replicas to nodes and manages state transitions and failover.
- **Patterns:** Declarative state model + constraints, controller-driven assignment.
- **Use cases:** Managing partitioned/replicated distributed systems (used by Pinot, Gobblin).
- **Interfaces:** Java API; runs a controller; uses ZooKeeper for state. Embeddable framework + controller. · **Needs:** JVM + ZooKeeper.
- **Pairs with:** Pinot, Gobblin, ZooKeeper. · **Alternatives:** Kubernetes operators, bespoke controllers (external).
- **Standards:** none specific. · **Maturity:** Mature, niche (build-your-own-distributed-system). Apache-2.0.

**Apache Ambari** — *Java · 🟢 Active (revived)*
- **Description:** Provisioning, management, and monitoring tool for Hadoop clusters.
- **Function:** Installs, configures, and monitors the Hadoop ecosystem via a web UI/REST API.
- **Patterns:** Agent/server management, blueprint-based provisioning, metrics aggregation.
- **Use cases:** Operating on-prem Hadoop clusters.
- **Interfaces:** Web UI + REST API; agents on each node; "stacks"/blueprints. Management service. · **Needs:** JVM; a DB; agents on managed hosts.
- **Pairs with:** Hadoop, Hive, HBase, Ranger, Bigtop. · **Alternatives:** Cloudera Manager (external); cloud-managed Hadoop.
- **Standards:** REST. · **Maturity:** Approached the Attic, then revived; tied to on-prem Hadoop. Apache-2.0.

**Apache Bigtop** — *Java/packaging · 🟢 Active*
- **Description:** Packaging, testing, and distribution of the Hadoop big-data stack.
- **Function:** Builds and integration-tests a coherent set of ecosystem components.
- **Patterns:** Build/packaging pipeline, smoke-test harness.
- **Use cases:** Creating a vendor-neutral Hadoop distribution.
- **Interfaces:** Build toolchain → OS packages (deb/rpm) + Docker images; test suites. Build/packaging project. · **Needs:** build hosts; Docker.
- **Pairs with:** Hadoop/Hive/HBase/Spark (packages them), Ambari (deploys them). · **Alternatives:** vendor distros (external); cloud managed stacks.
- **Standards:** OS packaging. · **Maturity:** Mature; the open Hadoop-distro builder. Apache-2.0.

**Apache Mesos** — *C++ · 🗄️ Attic*
- **Description:** Cluster resource manager abstracting CPU/memory across machines ("datacenter kernel").
- **Function:** Two-level scheduling offering resources to frameworks (Marathon, Aurora, Spark).
- **Patterns:** Two-level scheduling, resource offers, master/agent.
- **Use cases:** Large-scale cluster scheduling.
- **Leverage note:** 🗄️ Retired (2021) — use Kubernetes (optionally with YuniKorn, ASF) for new cluster scheduling.

### 11. Search & information retrieval

*Shared patterns: inverted index, scatter-gather distributed search, analysis/token pipelines, crawler frontier.*

**Apache Lucene** — *Java · 🟢 Active*
- **Description:** The foundational full-text search library.
- **Function:** Builds and queries inverted indexes with ranking, analysis, and (now) vector search.
- **Patterns:** Inverted index, segment-based immutable index + merge, analyzer pipeline, pluggable codecs.
- **Use cases:** Embedded search; the engine under Solr, Elasticsearch/OpenSearch.
- **Interfaces:** Java library API; index files on disk. Embeddable library. · **Needs:** JVM; local storage.
- **Pairs with:** Solr/Elasticsearch/OpenSearch (built on it), Tika (extraction), Geode (indexing). · **Alternatives:** Tantivy, Xapian (external); PyLucene/Lucene.NET (ASF ports).
- **Standards:** none (own index format); HNSW for vectors. · **Maturity:** Foundational; the most-used search library. Apache-2.0.

**Apache Solr** — *Java · 🟢 Active*
- **Description:** Distributed search platform built on Lucene.
- **Function:** REST/JSON search server with faceting, sharding, and replication (SolrCloud).
- **Patterns:** Scatter-gather distributed search, sharding/replication via ZooKeeper, schema + request handlers.
- **Use cases:** Site/enterprise search, faceted navigation, log/analytics search.
- **Interfaces:** REST/JSON + SolrJ client; admin UI. Standalone service. · **Needs:** JVM; ZooKeeper (SolrCloud); storage.
- **Pairs with:** Lucene (core), ManifoldCF (secure ingest), Tika, Nutch, ZooKeeper. · **Alternatives:** Elasticsearch/OpenSearch (external); plain Lucene (ASF, embedded).
- **Standards:** REST/JSON; Lucene index. · **Maturity:** Mature; strong in enterprise/site search. Apache-2.0.

**Apache Nutch** — *Java · 🟢 Active*
- **Description:** Scalable, extensible web crawler (Lucene/Hadoop lineage).
- **Function:** Crawls, parses, and indexes web content at scale.
- **Patterns:** Crawler frontier (generate/fetch/parse/update cycle), plugin architecture, MapReduce crawling.
- **Use cases:** Building search indexes, web-scale data harvesting (progenitor of Hadoop).
- **Interfaces:** CLI/jobs; plugin SPI; indexes to Solr/Elasticsearch. Batch application. · **Needs:** JVM; Hadoop (scale); a search backend.
- **Pairs with:** Solr/Elasticsearch, Hadoop, Tika. · **Alternatives:** StormCrawler (ASF, streaming); Scrapy, Heritrix (external).
- **Standards:** HTTP, robots.txt, WARC. · **Maturity:** Mature batch crawler. Apache-2.0.

**Apache StormCrawler** — *Java · 🟢 Active (TLP, 2025)*
- **Description:** SDK for building low-latency, scalable web crawlers on Apache Storm.
- **Function:** Stream-based crawling as configurable Storm topologies.
- **Patterns:** Streaming crawl pipeline, component SPI.
- **Use cases:** Continuous/near-real-time crawling and scraping.
- **Interfaces:** Java SDK (Storm bolts/spouts); indexes to Solr/Elasticsearch/OpenSearch. Library on Storm. · **Needs:** JVM + a Storm cluster.
- **Pairs with:** Storm, Solr/Elasticsearch, Tika. · **Alternatives:** Nutch (ASF, batch); Scrapy (external).
- **Standards:** HTTP, robots.txt, WARC. · **Maturity:** Mature; TLP 2025; preferred for low-latency crawling. Apache-2.0.

**Apache ManifoldCF** — *Java · 🟢 Active*
- **Description:** Connector framework for pulling content from repositories into search engines, honoring security.
- **Function:** Crawls SharePoint/filesystems/CMSes and propagates access controls to the index.
- **Patterns:** Connector SPI, security-token propagation, incremental crawl.
- **Use cases:** Secure enterprise content ingestion into Solr/Elasticsearch.
- **Interfaces:** Repository + output connector SPI; REST/UI; authority connectors. Service. · **Needs:** JVM; a DB; source repos + a search backend.
- **Pairs with:** Solr/Elasticsearch, Tika, SharePoint/filesystems/CMSes. · **Alternatives:** Connectors built into search vendors (external).
- **Standards:** connector-specific; propagates ACLs. · **Maturity:** Mature, niche (secure enterprise search ingest). Apache-2.0.

**Apache Lucene.NET** / **PyLucene** — *C#/Python · 🟢 Active*
- **Description:** .NET port and Python bindings of Lucene.
- **Use cases:** Lucene search in non-JVM applications.
- **Interfaces:** .NET API (Lucene.NET); Python-wrapped JVM Lucene (PyLucene). Embeddable libraries. · **Needs:** .NET runtime; or Python + a bundled JVM (PyLucene).
- **Pairs with:** .NET/Python apps needing embedded search. · **Alternatives:** native-language engines (Tantivy for Rust, etc., external).
- **Standards:** Lucene index format. · **Maturity:** Lucene.NET active; PyLucene stable. Apache-2.0.

### 12. Content, NLP & document processing

*Shared patterns: detector/parser chains, pluggable format handlers, statistical/ML models, streaming parse.*

**Apache Tika** — *Java · 🟢 Active*
- **Description:** Content detection and text/metadata extraction toolkit ("babelfish" for files).
- **Function:** Detects file type and extracts text + metadata from 1,000+ formats.
- **Patterns:** Detector + parser chain, SPI per format, SAX-style streaming.
- **Use cases:** Search ingestion pipelines, data-loss prevention, document analysis.
- **Interfaces:** Java API; CLI; `tika-server` (REST). Both (library + optional service). · **Needs:** JVM; bundles PDFBox/POI/etc.
- **Pairs with:** Solr/Elasticsearch (ingest), PDFBox/POI, Nutch. · **Alternatives:** Textract, unstructured.io (external).
- **Standards:** MIME detection; emits XHTML/metadata. · **Maturity:** Mature; the default extraction layer. Apache-2.0.

**Apache PDFBox** — *Java · 🟢 Active*
- **Description:** Library for creating, manipulating, and extracting from PDF documents.
- **Function:** Read/write PDFs, extract text, fill forms, sign, render pages.
- **Patterns:** Document object model, content-stream parsing.
- **Use cases:** PDF generation/parsing, text extraction (used by Tika), form processing.
- **Interfaces:** Java API; CLI tools. Embeddable library. · **Needs:** JVM.
- **Pairs with:** Tika (extraction), FOP (generation). · **Alternatives:** iText (AGPL/commercial), pdf.js (external).
- **Standards:** PDF/ISO 32000; PDF/A. · **Maturity:** Mature; the standard JVM PDF library. Apache-2.0.

**Apache POI** — *Java · 🟢 Active*
- **Description:** Pure-Java API for Microsoft Office formats (XLS/XLSX, DOC/DOCX, PPT/PPTX).
- **Function:** Read and write Office documents programmatically.
- **Patterns:** Format-specific object models (HSSF/XSSF, etc.), streaming (SXSSF) for large files.
- **Use cases:** Server-side spreadsheet/report generation, Office data extraction.
- **Interfaces:** Java API. Embeddable library. · **Needs:** JVM.
- **Pairs with:** Tika (extraction), reporting pipelines. · **Alternatives:** docx4j (external); cloud Office APIs.
- **Standards:** OOXML (ECMA-376), OLE2/CFB. · **Maturity:** Mature; the standard JVM Office library. Apache-2.0.

**Apache OpenNLP** — *Java · 🟢 Active*
- **Description:** Machine-learning toolkit for natural-language processing.
- **Function:** Tokenization, sentence detection, POS tagging, NER, parsing.
- **Patterns:** Statistical/ML models, pipeline of annotators, trainable components.
- **Use cases:** Text analytics, entity extraction, language processing pipelines.
- **Interfaces:** Java API; CLI; pretrained + trainable models. Embeddable library. · **Needs:** JVM; models.
- **Pairs with:** Tika, Solr, UIMA. · **Alternatives:** spaCy, Stanford CoreNLP, Hugging Face (external).
- **Standards:** none specific. · **Maturity:** Mature classic NLP (pre-transformer). Apache-2.0.

**Apache FOP (Formatting Objects Processor)** — *Java · 🟢 Active*
- **Description:** Print formatter driven by XSL-FO, part of **XML Graphics**.
- **Function:** Converts XSL-FO (and via XSLT, XML) into PDF, PS, and other print formats.
- **Patterns:** Declarative layout (XSL-FO), renderer SPI.
- **Use cases:** Server-side PDF/print generation from XML data.
- **Interfaces:** Java API; CLI; XSL-FO input. Embeddable library. · **Needs:** JVM; an XSLT processor (Xalan/Saxon) for XML→FO.
- **Pairs with:** Xalan/Saxon (XSLT), PDFBox, Batik (SVG in PDFs). · **Alternatives:** Weasyprint, wkhtmltopdf (external, HTML-based).
- **Standards:** XSL-FO, PDF, PostScript. · **Maturity:** Mature; the open XSL-FO engine. Apache-2.0.

**Apache Batik** — *Java · 🟢 Active*
- **Description:** Toolkit for Scalable Vector Graphics (SVG), part of **XML Graphics**.
- **Function:** Render, generate, and manipulate SVG; rasterize to images.
- **Patterns:** DOM-based graphics, renderer/transcoder.
- **Use cases:** SVG rendering, chart/image export, document graphics.
- **Interfaces:** Java API (SVG DOM, transcoders). Embeddable library. · **Needs:** JVM.
- **Pairs with:** FOP (SVG in PDF), charting libraries. · **Alternatives:** Apache ECharts (browser), resvg (external).
- **Standards:** SVG 1.1 (W3C). · **Maturity:** Mature. Apache-2.0.

**Apache cTAKES** — *Java · 🟢 Active*
- **Description:** Clinical NLP system for extracting information from electronic medical records.
- **Function:** Pipeline (on UIMA) that recognizes clinical entities and relations.
- **Patterns:** UIMA annotator pipeline, dictionary + ML extraction.
- **Use cases:** Healthcare/biomedical text mining.
- **Interfaces:** UIMA pipelines; Java API; needs UMLS dictionary access. Application/framework. · **Needs:** JVM + UIMA; a UMLS license for dictionaries.
- **Pairs with:** UIMA, OpenNLP, clinical data stores. · **Alternatives:** spaCy/medspaCy, Amazon Comprehend Medical (external).
- **Standards:** UMLS; HL7/FHIR (via integrations). · **Maturity:** Mature in clinical-NLP research. Apache-2.0.

**Apache UIMA** — *Java/C++ · 🟢 Active*
- **Description:** Unstructured Information Management Architecture — a framework for analyzing unstructured content.
- **Function:** Composes analysis engines that annotate text/audio/video with a common type system.
- **Patterns:** Annotator pipeline, common analysis structure (CAS), SPI.
- **Use cases:** NLP/content-analytics platforms (foundation under cTAKES; famously used in IBM Watson).
- **Interfaces:** Java/C++ component APIs; CAS; UIMA-AS (scaleout). Embeddable framework. · **Needs:** JVM (or C++); annotators.
- **Pairs with:** cTAKES, OpenNLP, custom annotators. · **Alternatives:** spaCy pipelines, GATE (external).
- **Standards:** UIMA (OASIS). · **Maturity:** Mature, niche. Apache-2.0.

### 13. Workflow orchestration & scheduling

*Shared patterns: DAG-of-tasks, scheduler + executor, declarative pipeline definition, dependency resolution.*

**Apache Airflow** — *Python · 🟢 Active*
- **Description:** The de-facto platform to programmatically author, schedule, and monitor workflows.
- **Function:** Defines pipelines as Python DAGs; schedules, retries, and tracks task runs.
- **Patterns:** DAG-of-tasks, scheduler/executor split, operator/provider plugin model.
- **Use cases:** Data-engineering ETL orchestration, ML pipelines, batch job scheduling.
- **Interfaces:** Python DAG API; web UI; REST API; 1,000+ provider operators. Standalone service. · **Needs:** Python; a metadata DB (Postgres); an executor (Celery/Kubernetes).
- **Pairs with:** Spark/Flink, dbt, cloud services (via providers), Kubernetes. · **Alternatives:** Dagster, Prefect, Argo Workflows (external); DolphinScheduler (ASF).
- **Standards:** REST; provider connectors. · **Maturity:** Dominant orchestrator; managed as MWAA/Cloud Composer/Astronomer. Apache-2.0.

**Apache DolphinScheduler** — *Java · 🟢 Active*
- **Description:** Visual, distributed workflow scheduler.
- **Function:** Drag-and-drop DAG authoring with distributed, HA execution.
- **Patterns:** DAG scheduling, decentralized master/worker, visual definition.
- **Use cases:** Data pipeline orchestration with a low-code UI; big-data task scheduling.
- **Interfaces:** Web UI (drag-and-drop) + REST API; task plugin SPI. Standalone service. · **Needs:** JVM; a DB; ZooKeeper (registry).
- **Pairs with:** Spark/Flink/Hive, SeaTunnel, big-data clusters. · **Alternatives:** Airflow (ASF, code-first); Azkaban (external).
- **Standards:** REST. · **Maturity:** Mature; popular where a low-code UI is wanted. Apache-2.0.

**Apache Oozie** — *Java · 🗄️ Attic*
- **Description:** Workflow scheduler for Hadoop jobs.
- **Function:** Coordinates MapReduce/Pig/Hive jobs by time and data availability.
- **Patterns:** XML-defined DAG + coordinators, data-trigger scheduling.
- **Use cases:** Legacy Hadoop job orchestration.
- **Leverage note:** 🗄️ Retired (2025) — migrate to Airflow or DolphinScheduler (ASF).

**Apache Liminal** — *Python · 🗄️ Attic*
- **Description:** End-to-end MLOps workflow DSL.
- **Use cases:** ML training/serving pipelines.
- **Leverage note:** 🗄️ Retired — use Airflow + an ML platform (Kubeflow/MLflow, external) instead.

### 14. Machine learning & AI

*Shared patterns: tensor dataflow graphs, distributed training (data/model parallelism), declarative ML pipelines, compiler IRs.*

**Apache SystemDS** — *Java/Scala · 🟢 Active*
- **Description:** ML systems platform for the end-to-end data-science lifecycle (successor to SystemML).
- **Function:** Declarative ML with automatic optimization across scales (single node → cluster).
- **Patterns:** Declarative linear algebra, cost-based execution-plan compilation.
- **Use cases:** Scalable ML pipelines, feature engineering, custom algorithms.
- **Interfaces:** DML (R/Python-like) scripts; Python/Java APIs; runs local or on Spark. Library/engine. · **Needs:** JVM; Spark (for scale-out).
- **Pairs with:** Spark, data lakes. · **Alternatives:** Spark MLlib, Dask-ML, Ray (external/ASF).
- **Standards:** none specific. · **Maturity:** Mature, research-strong, niche adoption. Apache-2.0.

**Apache SINGA** — *C++/Python · 🟢 Active*
- **Description:** Distributed deep-learning library.
- **Function:** Trains neural networks across devices/nodes.
- **Patterns:** Tensor dataflow, distributed training, device abstraction.
- **Use cases:** Deep learning (notably healthcare/medical imaging research).
- **Interfaces:** Python API (NumPy-like tensors). Library. · **Needs:** Python/C++; GPUs for scale.
- **Pairs with:** medical-imaging/research pipelines. · **Alternatives:** PyTorch, TensorFlow, JAX (external).
- **Standards:** ONNX (import/export). · **Maturity:** Niche vs mainstream DL frameworks. Apache-2.0.

**Apache Mahout** — *Java/Scala · 🟢 Active*
- **Description:** Distributed linear-algebra framework and the "Samsara" math DSL (originally classic MapReduce ML).
- **Function:** Mathematically expressive, scalable algebra for ML.
- **Patterns:** Distributed linear algebra, DSL over engines (Spark).
- **Use cases:** Recommenders, clustering, custom distributed math.
- **Interfaces:** Scala/Samsara DSL; runs on Spark. Library. · **Needs:** JVM + Spark.
- **Pairs with:** Spark. · **Alternatives:** Spark MLlib, SystemDS (ASF); scikit-learn/PyTorch (external).
- **Standards:** none specific. · **Maturity:** Mature but low momentum (the early Hadoop-ML project). Apache-2.0.

**Apache Submarine** — *Java/Python · 🗄️ Attic*
- **Description:** Cloud-native ML platform for running training/notebooks on Kubernetes/YARN.
- **Use cases:** ML platform-as-a-service.
- **Leverage note:** 🗄️ Retired (2025) — use Kubeflow/MLflow or a cloud ML platform (external).

**Apache MXNet** — *C++/Python · 🗄️ Attic*
- **Description:** Flexible, efficient deep-learning framework (once an AWS favorite).
- **Patterns:** Hybrid imperative/symbolic graphs, multi-GPU training.
- **Use cases:** Deep learning.
- **Leverage note:** 🗄️ Retired (2023) — use PyTorch/TensorFlow/JAX (external); TVM (ASF) for compilation.

**Apache PredictionIO** — *Scala · 🗄️ Attic*
- **Description:** ML server for building predictive engines on Spark.
- **Use cases:** Deployable recommendation/prediction services.
- **Leverage note:** 🗄️ Retired — use a current serving stack (MLflow/BentoML/KServe, external).

**Apache TVM** — *C++/Python · 🟢 Active*
- **Description:** End-to-end deep-learning compiler stack for CPUs, GPUs, and accelerators.
- **Function:** Compiles and optimizes trained models for efficient inference across diverse hardware.
- **Patterns:** Multi-level compiler IR (Relay/TIR), auto-tuning/auto-scheduling, hardware backend SPI.
- **Use cases:** Portable, optimized model deployment; edge/accelerator inference.
- **Interfaces:** Python/C++ API; imports ONNX/PyTorch/TF; emits deployable runtimes. Compiler + runtime library. · **Needs:** Python/C++; target hardware toolchains.
- **Pairs with:** PyTorch/TF/ONNX (front ends), edge/accelerator targets. · **Alternatives:** ONNX Runtime, TensorRT, MLIR/IREE (external).
- **Standards:** ONNX (import). · **Maturity:** Mature, widely used DL compiler. Apache-2.0.

### 15. Graph, geospatial & semantic web

*Shared patterns: graph traversal DSLs, BSP iteration, spatial indexing/partitioning, RDF triple stores + SPARQL.*

**Apache TinkerPop** — *Java · 🟢 Active*
- **Description:** Graph computing framework with the **Gremlin** traversal language.
- **Function:** Vendor-neutral API/DSL for querying property graphs (OLTP traversals + OLAP).
- **Patterns:** Graph traversal DSL, provider SPI (works across many graph databases).
- **Use cases:** Graph querying across JanusGraph, Neptune, etc.; fraud/recommendation graphs.
- **Interfaces:** Gremlin (Java/Groovy/Python/JS/.NET); Gremlin Server (WebSocket). Library + optional server. · **Needs:** JVM; a graph backend provider.
- **Pairs with:** JanusGraph, HugeGraph (ASF), Neptune, CosmosDB. · **Alternatives:** openCypher/GQL ecosystems (external).
- **Standards:** Gremlin; (GQL emerging). · **Maturity:** Mature; the vendor-neutral graph API. Apache-2.0.

**Apache Jena** — *Java · 🟢 Active*
- **Description:** Framework for building Semantic Web / Linked Data apps (RDF, SPARQL, OWL).
- **Function:** Store, reason over, and query RDF; **Fuseki** is its SPARQL server; **TDB** its triple store.
- **Patterns:** RDF triple store, SPARQL query engine, rule-based inference.
- **Use cases:** Knowledge graphs, ontologies, linked-data publishing.
- **Interfaces:** Java API; SPARQL endpoint (Fuseki, HTTP). Library + optional server. · **Needs:** JVM; storage (TDB).
- **Pairs with:** ontologies/OWL, linked-data publishers. · **Alternatives:** RDF4J, GraphDB, Blazegraph (external).
- **Standards:** RDF, SPARQL 1.1, OWL, SHACL. · **Maturity:** Mature; the reference JVM RDF toolkit. Apache-2.0.

**Apache Sedona** — *Java/Scala/Python · 🟢 Active*
- **Description:** Cluster computing system for processing large-scale spatial data.
- **Function:** Spatial SQL, indexing, and partitioning on Spark/Flink.
- **Patterns:** Spatial partitioning + indexing (R-tree/quadtree), distributed spatial joins.
- **Use cases:** Geospatial analytics at scale (mobility, GIS, earth observation).
- **Interfaces:** Spark/Flink extensions; Spatial SQL; Python/Scala/Java/R APIs. Library on an engine. · **Needs:** JVM + Spark or Flink.
- **Pairs with:** Spark/Flink, Parquet/GeoParquet, SIS. · **Alternatives:** GeoMesa, PostGIS (external).
- **Standards:** OGC Simple Features, WKT/WKB, GeoParquet. · **Maturity:** Mature; the standard big-geospatial engine. Apache-2.0.

**Apache SIS (Spatial Information System)** — *Java · 🟢 Active*
- **Description:** Library for geospatial metadata and referencing per OGC/ISO standards.
- **Function:** Coordinate reference systems, projections, and metadata handling.
- **Patterns:** Standards implementation (OGC/ISO), referencing engine.
- **Use cases:** GIS applications needing accurate coordinate transforms/metadata.
- **Interfaces:** Java API (implements GeoAPI). Embeddable library. · **Needs:** JVM.
- **Pairs with:** Sedona, GIS apps, GeoAPI consumers. · **Alternatives:** GeoTools, PROJ (external).
- **Standards:** OGC/ISO 19100 series, GeoAPI, EPSG. · **Maturity:** Mature, standards-focused. Apache-2.0.

**Apache Giraph** — *Java · 🗄️ Attic*
- **Description:** Iterative graph-processing system on Hadoop.
- **Patterns:** Bulk-synchronous parallel (Pregel model), vertex-centric computation.
- **Use cases:** Large-scale graph algorithms (historically Facebook's social graph).
- **Leverage note:** 🗄️ Retired — use Spark GraphX/GraphFrames, or GraphAr+engines (ASF, incubating) for new graph analytics.

### 16. IoT, edge & embedded / RTOS

*Shared patterns: real-time kernels, industrial protocol adapters, edge-to-cloud flow, flow-based programming.*

**Apache NuttX** — *C · 🟢 Active*
- **Description:** Mature real-time operating system (RTOS) with strong POSIX compliance.
- **Function:** Small-footprint OS for microcontrollers to microprocessors.
- **Patterns:** POSIX RTOS, modular driver model, scalable footprint.
- **Use cases:** Embedded/IoT devices, drones, wearables (notably in many consumer devices).
- **Interfaces:** POSIX/ANSI C APIs; NSH shell; driver model. Firmware/OS. · **Needs:** a supported MCU/SoC; C toolchain.
- **Pairs with:** PX4 (drones), BLE/networking stacks, device apps. · **Alternatives:** Zephyr, FreeRTOS, Mynewt (ASF) (external/ASF).
- **Standards:** POSIX. · **Maturity:** Mature; shipped in large consumer-device volumes. Apache-2.0 (+ BSD-licensed imports).

**Apache Mynewt** — *C · 🟢 Active*
- **Description:** Modular RTOS for constrained embedded devices, with a full BLE stack.
- **Function:** OS + package management + bootloader for MCUs.
- **Patterns:** RTOS + package manager, hardware abstraction layer.
- **Use cases:** Bluetooth Low Energy products, resource-constrained IoT.
- **Interfaces:** C APIs; `newt` tooling; NimBLE stack. Firmware/OS. · **Needs:** a supported MCU; C toolchain.
- **Pairs with:** NimBLE (BLE), MCUboot. · **Alternatives:** Zephyr, FreeRTOS, NuttX (ASF) (external/ASF).
- **Standards:** Bluetooth LE. · **Maturity:** Mature, niche (BLE-focused). Apache-2.0.

**Apache PLC4X** — *Java/Go/C · 🟢 Active*
- **Description:** Universal protocol adapters for industrial PLCs (Programmable Logic Controllers).
- **Function:** Uniform API to talk to Modbus/S7/OPC-UA/EtherNet-IP and more.
- **Patterns:** Driver SPI over industrial protocols, uniform read/write/subscribe API.
- **Use cases:** Industry 4.0 / IIoT data acquisition from factory equipment.
- **Interfaces:** Uniform read/write/subscribe API; drivers (Modbus/S7/OPC-UA/…); Java/Go/C/Python. Embeddable library. · **Needs:** a host runtime; network access to PLCs.
- **Pairs with:** NiFi/MiNiFi, Kafka, IoTDB, Camel. · **Alternatives:** vendor PLC SDKs, Eclipse Milo (OPC-UA, external).
- **Standards:** Modbus, S7, OPC-UA, EtherNet/IP, BACnet, etc. · **Maturity:** Mature; the open industrial-protocol bridge. Apache-2.0.

**Apache NiFi** — *Java · 🟢 Active*
- **Description:** Dataflow automation tool with a visual, flow-based programming UI; includes **MiNiFi** (edge agent) and **NiFi Registry**.
- **Function:** Routes, transforms, and tracks data between systems with full provenance.
- **Patterns:** Flow-based programming (processors + connections), back-pressure, data provenance lineage.
- **Use cases:** Edge-to-cloud ingestion, IoT collection, ETL, inter-system data logistics.
- **Interfaces:** Web UI (drag-and-drop) + REST API; 300+ processors; MiNiFi edge agents. Standalone service + edge agent. · **Needs:** JVM; storage for repositories.
- **Pairs with:** Kafka, HDFS/object stores, PLC4X, Kudu, databases (via processors). · **Alternatives:** Camel (code-first, ASF); StreamSets, Fivetran (external).
- **Standards:** many via processors; site-to-site protocol. · **Maturity:** Mature; strong for IoT/edge logistics. Apache-2.0.

**Apache StreamPipes** — *Java/TypeScript · 🟢 Active*
- **Description:** Self-service (I)IoT toolbox to connect, analyze, and explore streaming data.
- **Function:** Low-code pipelines over industrial data streams.
- **Patterns:** Pipeline composition, adapters + processing elements SPI.
- **Use cases:** Industrial IoT analytics for domain experts.
- **Interfaces:** Web UI (pipeline editor); adapter/processor SPI; REST. Standalone service. · **Needs:** JVM; Docker/K8s; a message broker.
- **Pairs with:** Kafka/MQTT, PLC4X, IoTDB, Flink. · **Alternatives:** NiFi (ASF); Node-RED (external).
- **Standards:** MQTT, OPC-UA, Kafka. · **Maturity:** Growing; domain-expert-friendly IIoT. Apache-2.0.

**Apache Edgent** — *Java · 🗄️ Attic*
- **Description:** Lightweight edge-analytics runtime (formerly Quarks).
- **Use cases:** On-device stream analytics.
- **Leverage note:** 🗄️ Retired — use MiNiFi (ASF) or a current edge runtime instead.

### 17. Security, identity & cryptography

*Shared patterns: pluggable realms/providers, policy decision/enforcement points, directory/LDAP, XML/crypto standards.*

**Apache Shiro** — *Java · 🟢 Active*
- **Description:** Simple, comprehensive application security framework.
- **Function:** Authentication, authorization, session management, and cryptography for apps.
- **Patterns:** Pluggable realms, subject/principal model, policy enforcement.
- **Use cases:** Securing Java applications without a heavyweight framework.
- **Interfaces:** Java API; realm SPI; servlet/filters. Embeddable library. · **Needs:** JVM.
- **Pairs with:** any JVM web app; LDAP/JDBC realms, Directory. · **Alternatives:** Spring Security (external).
- **Standards:** pluggable (LDAP, JWT via extensions). · **Maturity:** Mature; the lightweight alternative to Spring Security. Apache-2.0.

**Apache Ranger** — *Java · 🟢 Active*
- **Description:** Centralized security administration and fine-grained authorization for the Hadoop ecosystem.
- **Function:** Defines, enforces, and audits access policies across Hive, HBase, Kafka, etc.
- **Patterns:** Policy decision + enforcement points (plugins), centralized admin + audit.
- **Use cases:** Data-governance and access control across a big-data platform.
- **Interfaces:** Admin web UI + REST; enforcement plugins embedded in each service. Service + plugins. · **Needs:** JVM; a DB; Solr (audit); the services it governs.
- **Pairs with:** Hive, HBase, Kafka, HDFS, Trino, Knox. · **Alternatives:** Apache Sentry (retired, ASF); cloud IAM, OPA (external).
- **Standards:** service-specific; tag-based policies (with Atlas). · **Maturity:** Mature; the standard Hadoop authorization layer. Apache-2.0.

**Apache Knox** — *Java · 🟢 Active*
- **Description:** Application gateway for securely accessing Hadoop services.
- **Function:** Single, authenticated REST/HTTP entry point that proxies cluster services.
- **Patterns:** Reverse-proxy gateway, perimeter security, SSO integration.
- **Use cases:** Exposing Hadoop/analytics services safely outside the cluster.
- **Interfaces:** HTTP(S) reverse proxy; provider SPI (auth/federation). Gateway service. · **Needs:** JVM; the backend services; an identity provider.
- **Pairs with:** Hadoop/Hive/HBase/Ranger, LDAP/SAML/OIDC IdPs. · **Alternatives:** APISIX/general gateways (ASF/external) with custom config.
- **Standards:** HTTP, SAML, OIDC, Kerberos. · **Maturity:** Mature; standard Hadoop perimeter gateway. Apache-2.0.

**Apache Syncope** — *Java · 🟢 Active*
- **Description:** Identity management and governance (IdM/IGA) system.
- **Function:** Manages users/roles and provisions identities across connected systems.
- **Patterns:** Identity store + connectors (ConnId), workflow-driven provisioning, policy engine.
- **Use cases:** Enterprise identity lifecycle, provisioning/deprovisioning, governance.
- **Interfaces:** REST API; admin UI; ConnId connectors; SCIM. Standalone service. · **Needs:** JVM; a DB; target systems to provision.
- **Pairs with:** LDAP/AD, Directory, SAML/OIDC IdPs. · **Alternatives:** Keycloak (adjacent), midPoint, Okta (external).
- **Standards:** SCIM, REST; ConnId. · **Maturity:** Mature; open-source IGA. Apache-2.0.

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
- **Interfaces:** LDAP(S), Kerberos; Java LDAP API; Studio GUI. Both (embeddable server + client libs + tools). · **Needs:** JVM.
- **Pairs with:** Syncope/Shiro (consume it), Hadoop (Kerberos), any LDAP client. · **Alternatives:** OpenLDAP, 389-DS, FreeIPA, MIT Kerberos (external).
- **Standards:** LDAPv3, Kerberos v5, RBAC (ANSI INCITS 359). · **Maturity:** Mature; strongest as an embeddable test directory + LDAP API. Apache-2.0.

**Apache Santuario** — *Java/C++ · 🟢 Active*
- **Description:** Implementation of XML Digital Signature and XML Encryption standards.
- **Function:** Sign/verify and encrypt/decrypt XML.
- **Patterns:** Standards implementation (W3C XML Security).
- **Use cases:** SOAP/WS-Security, signed XML documents, SAML.
- **Interfaces:** Java & C++ APIs. Embeddable library. · **Needs:** JVM or C++.
- **Pairs with:** CXF/WSS4J (WS-Security), SAML stacks. · **Alternatives:** JDK XML-DSig (external).
- **Standards:** W3C XML Signature & XML Encryption. · **Maturity:** Mature; the reference XML-security library. Apache-2.0.

**Apache Teaclave** — *Rust · 🥚 Incubating*
- **Description:** Universal secure/confidential computing platform.
- **Function:** Runs computations inside trusted execution environments (e.g., SGX).
- **Patterns:** Confidential computing, function-as-a-service in enclaves, data isolation.
- **Use cases:** Privacy-preserving analytics, multi-party computation on sensitive data.
- **Interfaces:** FaaS API; SDKs; enclave runtime. Platform + SDKs. · **Needs:** TEE hardware (Intel SGX/TDX); Rust toolchain.
- **Pairs with:** confidential-computing deployments; secure multi-party workflows. · **Alternatives:** Confidential Containers, Occlum, Gramine (external).
- **Standards:** TEE-specific. · **Maturity:** Incubating; research-leaning. Apache-2.0.

### 18. Observability & monitoring

*Shared patterns: distributed tracing, metrics time series, agent + collector, topology/service maps.*

**Apache SkyWalking** — *Java · 🟢 Active*
- **Description:** Application performance monitoring (APM) and observability platform for distributed systems.
- **Function:** Distributed tracing, metrics, logs, and service topology (cloud-native, service mesh).
- **Patterns:** Agent + OAP collector, distributed tracing, service dependency maps, OpenTelemetry ingestion.
- **Use cases:** Microservice observability, latency/root-cause analysis.
- **Interfaces:** Language agents; OTLP/Zipkin/Jaeger ingestion; OAP backend; web UI; GraphQL/PromQL-ish queries. Service + agents. · **Needs:** JVM (backend); a storage backend (Elasticsearch/BanyanDB); agents.
- **Pairs with:** OpenTelemetry, APISIX/ShenYu, Dubbo, service meshes, BanyanDB. · **Alternatives:** Jaeger, Zipkin, Grafana/Tempo, Datadog (external).
- **Standards:** OpenTelemetry (OTLP), Zipkin/Jaeger. · **Maturity:** Mature; a leading open APM. Apache-2.0.

**Apache HertzBeat** — *Java · 🟢 Active*
- **Description:** Real-time monitoring system with agentless collection and alerting.
- **Function:** Monitors apps/databases/OS/network via configurable (YAML) protocols; threshold alerts.
- **Patterns:** Agentless pull collection, template-defined metrics, alert rules.
- **Use cases:** Infrastructure/service monitoring and alerting without installing agents.
- **Interfaces:** Web UI + REST; YAML metric templates; push webhooks/alert channels. Standalone service. · **Needs:** JVM; a time-series store (optional Victoria/TDengine/IoTDB).
- **Pairs with:** Grafana, alerting channels (Slack/email/DingTalk). · **Alternatives:** Prometheus+Grafana, Zabbix (external).
- **Standards:** SNMP, JMX, HTTP, JDBC, Prometheus exporters. · **Maturity:** Growing; agentless niche. Apache-2.0.

**Apache Flagon** — *JavaScript/Java · 🟢 Active*
- **Description:** User-behavior logging ("UserALE") for software usability analytics.
- **Function:** Captures fine-grained UI interaction telemetry.
- **Patterns:** Event instrumentation + collector.
- **Use cases:** UX research, usability/behavior analytics.
- **Interfaces:** UserALE.js browser library; log collector; Elastic/Kibana dashboards. Library + collector. · **Needs:** a log store (Elasticsearch) for analysis.
- **Pairs with:** Elasticsearch/Kibana, analytics pipelines. · **Alternatives:** product-analytics SaaS (external).
- **Standards:** JSON event logs. · **Maturity:** Niche (usability research). Apache-2.0.

### 19. Cloud, virtualization & container orchestration

*Shared patterns: cloud abstraction layers, control-plane orchestration, Kubernetes scheduling, portable provider APIs.*

**Apache CloudStack** — *Java · 🟢 Active*
- **Description:** Turnkey Infrastructure-as-a-Service (IaaS) cloud orchestration platform.
- **Function:** Manages compute/network/storage to deliver a full private/public cloud.
- **Patterns:** Control plane + hypervisor agents, multi-tenancy, pod/cluster/zone topology.
- **Use cases:** Running on-prem/hosted IaaS clouds (telcos, service providers).
- **Interfaces:** Web UI + REST/CloudStack & EC2-compatible API. Platform/service. · **Needs:** hypervisors (KVM/VMware/XCP-ng); a management DB; a cluster.
- **Pairs with:** KVM/VMware, storage/networking backends. · **Alternatives:** OpenStack, Proxmox (external).
- **Standards:** own API + partial EC2 compatibility. · **Maturity:** Mature; popular with service providers. Apache-2.0.

**Apache Libcloud** — *Python · 🟢 Active*
- **Description:** Python library providing one API across many cloud providers.
- **Function:** Abstracts compute/storage/DNS/load-balancer APIs of 50+ clouds.
- **Patterns:** Provider abstraction/adapter, uniform driver interface.
- **Use cases:** Multi-cloud/portable automation scripts and tools.
- **Interfaces:** Python API; provider drivers. Embeddable library. · **Needs:** Python.
- **Pairs with:** multi-cloud automation scripts. · **Alternatives:** Terraform, Pulumi, cloud SDKs (external).
- **Standards:** wraps each provider's API. · **Maturity:** Mature; stable. Apache-2.0.

**Apache jclouds** — *Java · 🗄️ Attic*
- **Description:** Multi-cloud toolkit for Java (compute + blobstore abstraction).
- **Patterns:** Provider abstraction/adapter.
- **Use cases:** Portable Java cloud automation.
- **Leverage note:** 🗄️ Retired — use provider SDKs or Terraform/Pulumi; for storage abstraction consider OpenDAL (ASF).

**Apache Brooklyn** — *Java · 🟢 Active*
- **Description:** Framework for modeling, deploying, and managing applications via blueprints.
- **Function:** Autonomic application management across clouds (policy-driven scaling/healing).
- **Patterns:** Declarative blueprints (YAML), autonomic policies, effectors/sensors.
- **Use cases:** Application orchestration and runtime management across infrastructure.
- **Interfaces:** YAML (CAMP) blueprints; REST API; web console. Service. · **Needs:** JVM; target clouds/machines (jclouds heritage).
- **Pairs with:** cloud providers, config-mgmt tools. · **Alternatives:** Terraform + operators, Kubernetes (external).
- **Standards:** OASIS CAMP. · **Maturity:** Mature, niche. Apache-2.0.

**Apache YuniKorn** — *Go · 🟢 Active*
- **Description:** Resource scheduler for big-data/ML workloads on Kubernetes (and YARN).
- **Function:** Rich hierarchical queue scheduling that Kubernetes' default scheduler lacks.
- **Patterns:** Hierarchical queues, gang scheduling, resource fairness.
- **Use cases:** Running Spark/Flink/ML batch workloads efficiently on Kubernetes.
- **Interfaces:** Kubernetes scheduler plugin; web UI + REST. Scheduler service. · **Needs:** Kubernetes (or YARN).
- **Pairs with:** Spark/Flink on k8s, Celeborn, Kubernetes. · **Alternatives:** Volcano, kube-scheduler, Kueue (external).
- **Standards:** Kubernetes scheduling. · **Maturity:** Mature; strong for batch-on-k8s. Apache-2.0.

**Apache Airavata** — *Java · 🟢 Active*
- **Description:** Framework for executing and managing computational jobs on distributed resources (science gateways).
- **Function:** Submits/monitors workflows across HPC clusters, grids, and clouds.
- **Patterns:** Science-gateway middleware, workflow + resource brokering.
- **Use cases:** Research computing portals bridging scientists to supercomputers.
- **Interfaces:** Thrift/REST APIs; Django-based gateway portal. Platform/service. · **Needs:** JVM; HPC/cloud resources; a DB.
- **Pairs with:** HPC schedulers (Slurm/PBS), campus clusters, clouds. · **Alternatives:** Pegasus WMS, Galaxy (external).
- **Standards:** job-submission protocols (SSH/Slurm/PBS). · **Maturity:** Mature in research-computing niche. Apache-2.0.

### 20. Build, dependency & release tooling

*Shared patterns: declarative build lifecycle, dependency resolution graph, convention over configuration, artifact repository.*

**Apache Maven** — *Java · 🟢 Active*
- **Description:** The dominant Java build and project-management tool.
- **Function:** Declarative builds with transitive dependency management and a plugin-driven lifecycle.
- **Patterns:** Convention over configuration, declarative lifecycle phases, dependency resolution graph, plugin SPI.
- **Use cases:** Building/packaging/publishing JVM projects; the Maven Central coordinate system.
- **Interfaces:** `pom.xml`; CLI; plugin & extension APIs; reads/writes Maven repositories. Build tool. · **Needs:** JDK.
- **Pairs with:** Maven Central, Archiva/Nexus, CI systems, nearly all JVM projects. · **Alternatives:** Gradle, Bazel, sbt (external); Ant+Ivy (ASF).
- **Standards:** Maven coordinates/repository layout (de-facto). · **Maturity:** Ubiquitous JVM build standard. Apache-2.0.

**Apache Ant** — *Java · 🟢 Active*
- **Description:** Original XML-driven Java build tool (imperative task runner).
- **Function:** Scripts arbitrary build steps as ordered targets/tasks.
- **Patterns:** Imperative task graph, target dependencies.
- **Use cases:** Legacy and highly customized builds; fine-grained control.
- **Interfaces:** `build.xml`; CLI; custom task API. Build tool. · **Needs:** JDK.
- **Pairs with:** Ivy (dependencies), legacy JVM projects. · **Alternatives:** Maven, Gradle (external/ASF).
- **Standards:** none (own XML). · **Maturity:** Mature, legacy-leaning. Apache-2.0.

**Apache Ivy** — *Java · 🟢 Active*
- **Description:** Dependency manager, typically paired with Ant.
- **Function:** Resolves and retrieves dependencies with flexible configuration.
- **Patterns:** Dependency resolution, pluggable resolvers.
- **Use cases:** Adding Maven-style dependency management to Ant builds.
- **Interfaces:** `ivy.xml`; Ant tasks; reads Maven/Ivy repositories. Library/Ant plugin. · **Needs:** JDK + Ant.
- **Pairs with:** Ant, Maven repositories. · **Alternatives:** Maven/Gradle built-in resolution (external/ASF).
- **Standards:** Maven repository layout. · **Maturity:** Mature; tied to Ant. Apache-2.0.

**Apache Archiva** — *Java · 🟡 Low activity*
- **Description:** Build-artifact repository manager.
- **Function:** Hosts/proxies/caches Maven artifact repositories.
- **Patterns:** Artifact repository + proxy cache.
- **Use cases:** Private internal Maven repositories.
- **Interfaces:** Maven repo HTTP layout; web UI; REST. Service. · **Needs:** JVM; storage.
- **Pairs with:** Maven/Ivy/Gradle clients. · **Alternatives:** Sonatype Nexus, JFrog Artifactory (external).
- **Standards:** Maven repository layout. · **Maturity:** Low activity; Nexus/Artifactory dominate. Apache-2.0.

**Apache Maven Doxia / plugins** — *Java · 🟢 Active*
- Sub-projects supplying site generation and the large catalog of core Maven plugins.
- **Interfaces:** Maven plugins + Doxia markup (APT/Markdown/XDoc). Build-time libraries. · **Needs:** Maven. · **Pairs with:** Maven (always). · **Standards:** Maven plugin API. · **Maturity:** Mature; part of the Maven ecosystem. Apache-2.0.

**Apache Gump** — *Python · 🟡 Low activity*
- **Description:** Continuous-integration tool that builds projects against the latest of their dependencies.
- **Patterns:** Integration-at-head CI.
- **Use cases:** Early detection of cross-project breakage (ASF-internal heritage).
- **Interfaces:** descriptor-driven CI runs. Tool. · **Needs:** Python; the projects' build tools. · **Pairs with:** ASF projects (historically). · **Alternatives:** GitHub Actions, Jenkins, dependency bots (external). · **Maturity:** Low activity. Apache-2.0.

### 21. Content management, collaboration & portals

*Shared patterns: content repository (JCR), resource-oriented rendering, portlet aggregation, project forge.*

**Apache Jackrabbit** & **Jackrabbit Oak** — *Java · 🟢 Active*
- **Description:** Implementations of the Java Content Repository (JCR) standard; **Oak** is the scalable modern core.
- **Function:** Hierarchical content storage with versioning, search, and fine-grained access.
- **Patterns:** Content repository, MVCC (Oak), pluggable node stores (Mongo/segment).
- **Use cases:** The repository under Adobe Experience Manager and many CMSes.
- **Interfaces:** JCR (JSR-283) API; WebDAV; pluggable node stores. Embeddable library + server. · **Needs:** JVM; a node store (segment/Document/Mongo/RDB).
- **Pairs with:** Sling, AEM, Lucene/Oak search. · **Alternatives:** ModeShape (external); plain RDBMS/S3 (external).
- **Standards:** JCR (JSR-170/283), WebDAV. · **Maturity:** Mature; Oak powers AEM at scale. Apache-2.0.

**Apache Sling** — *Java · 🟢 Active*
- **Description:** RESTful web framework for JCR content repositories.
- **Function:** Maps HTTP requests directly onto content nodes + rendering scripts.
- **Patterns:** Resource-oriented architecture, request→resource→renderer resolution, OSGi-based.
- **Use cases:** Content-centric web applications (basis of AEM).
- **Interfaces:** HTTP (resource mapping); scripting (JSP/HTL); OSGi services. Runtime/framework. · **Needs:** JVM; OSGi (Felix); a JCR repo (Oak).
- **Pairs with:** Jackrabbit Oak, Felix, AEM. · **Alternatives:** headless CMS, Spring Content (external).
- **Standards:** JCR, HTTP/REST. · **Maturity:** Mature; the engine under AEM. Apache-2.0.

**Apache Roller** — *Java · 🟢 Active*
- **Description:** Full-featured multi-user blog server.
- **Function:** Hosts many blogs with themes, feeds, and comments.
- **Patterns:** Templated rendering, multi-tenant content.
- **Use cases:** Enterprise/community blogging (long ran blogs.apache.org, Oracle internal).
- **Interfaces:** Web UI; Atom/RSS feeds; MetaWeblog API; deploys as WAR. Service. · **Needs:** JVM + servlet container + a DB.
- **Pairs with:** Tomcat, a relational DB. · **Alternatives:** WordPress, Ghost (external).
- **Standards:** Atom/RSS, MetaWeblog. · **Maturity:** Mature, niche. Apache-2.0.

**Apache Pluto** — *Java · 🟢 Active*
- **Description:** Reference implementation of the Java Portlet Specification.
- **Function:** Portlet container that renders and coordinates portlets.
- **Patterns:** Portlet container, portal aggregation.
- **Use cases:** Testing/running portlets; embedding portlet support.
- **Interfaces:** Jakarta Portlet API; servlet container. Library/container. · **Needs:** JVM + servlet container.
- **Pairs with:** portlet apps, JSF/MyFaces portlets. · **Alternatives:** Liferay (external).
- **Standards:** Jakarta Portlet (JSR-362). · **Maturity:** Mature spec RI, niche. Apache-2.0.

**Apache Allura** — *Python · 🟢 Active*
- **Description:** Project-hosting ("forge") platform — the software behind SourceForge.
- **Function:** Git/SVN hosting, tickets, wikis, discussions as pluggable tools.
- **Patterns:** Multi-tool forge, plugin tools per project, document-store backend.
- **Use cases:** Running a software forge / project-hosting site.
- **Interfaces:** Web UI + REST; tool plugin API. Service. · **Needs:** Python; MongoDB; Solr; a message queue.
- **Pairs with:** Solr (search), Git/SVN, MongoDB. · **Alternatives:** GitLab, Gitea (external).
- **Standards:** Git/SVN, REST. · **Maturity:** Mature; runs SourceForge. Apache-2.0.

**Apache Cocoon** — *Java · 🗄️ Attic*
- **Description:** XML-centric web development framework (pipeline-based publishing).
- **Patterns:** XML pipelines (SAX), separation of concerns by pipeline stage.
- **Use cases:** XML publishing.
- **Leverage note:** 🗄️ Retired (2025) — use a modern web framework or static-site/XSLT toolchain.

**Apache Jetspeed / Portals** — *Java · 🗄️ Attic*
- **Description:** Enterprise portal platform (the "Portals" umbrella).
- **Use cases:** Portal deployments.
- **Leverage note:** 🗄️ Retired (2025) — use Liferay or a modern SPA + API gateway instead.

**Apache Wookie** / **Apache Lenya** / **Apache Shindig** — *🗄️ Attic*
- Retired widget-engine, CMS, and OpenSocial-container projects respectively.
- **Leverage note:** 🗄️ All retired — avoid for new work; use current CMS/widget/identity stacks.

### 22. Mobile & rich client

**Apache Cordova** — *JavaScript/native · 🟢 Active*
- **Description:** Framework to build mobile apps with HTML/CSS/JS packaged as native apps.
- **Function:** Wraps web apps in a native WebView and exposes device APIs via plugins.
- **Patterns:** WebView bridge, plugin SPI to native capabilities, write-once/run-many.
- **Use cases:** Cross-platform mobile apps from web skills (basis of PhoneGap/Ionic).
- **Interfaces:** CLI + JS plugin API; builds iOS/Android apps. Toolkit. · **Needs:** Node.js; iOS/Android SDKs.
- **Pairs with:** Ionic, web frameworks, native plugin ecosystem. · **Alternatives:** React Native, Flutter, Capacitor (external).
- **Standards:** HTML/CSS/JS, WebView. · **Maturity:** Mature; losing ground to RN/Flutter/Capacitor. Apache-2.0.

**Apache Weex** — *JavaScript/native · 🗄️ Attic*
- **Description:** Framework for high-performance cross-platform mobile UIs.
- **Use cases:** Native-rendered mobile apps from a web-like syntax.
- **Leverage note:** 🗄️ Retired — use React Native, Flutter, or Cordova/Capacitor (ASF/external).

### 23. BI, data visualization & notebooks

*Shared patterns: declarative chart specs, pluggable datasource connectors, interactive notebook REPL, async job sessions.*

**Apache Superset** — *Python/TypeScript · 🟢 Active*
- **Description:** Modern data-exploration and business-intelligence web platform.
- **Function:** SQL IDE, no-code chart builder, and dashboards over any SQL database.
- **Patterns:** Pluggable SQLAlchemy datasources, declarative viz config, semantic layer.
- **Use cases:** Self-service BI, dashboards, data exploration.
- **Interfaces:** Web UI; REST API; SQLAlchemy/DB-API connectors; embeddable SDK. Standalone service. · **Needs:** Python; a metadata DB; Redis (cache); the databases it queries.
- **Pairs with:** Trino/Hive/Druid/Pinot/Doris, Postgres/Snowflake, any SQL DB. · **Alternatives:** Metabase, Grafana, Tableau/Looker (external).
- **Standards:** SQL via SQLAlchemy; ECharts for rendering. · **Maturity:** Mature; leading OSS BI; managed as Preset. Apache-2.0.

**Apache ECharts** — *JavaScript · 🟢 Active*
- **Description:** Powerful, interactive charting and visualization library for the browser.
- **Function:** Renders rich, animated charts (Canvas/SVG) from declarative options.
- **Patterns:** Declarative chart spec, component-based rendering, incremental rendering for big data.
- **Use cases:** Web dashboards, data viz in apps (hugely popular in the JS ecosystem).
- **Interfaces:** JavaScript/TS API (npm); wrappers for React/Vue/Angular/Python(pyecharts). Browser library. · **Needs:** a browser (or SSR).
- **Pairs with:** Superset (uses it), web apps. · **Alternatives:** D3, Chart.js, Plotly, Highcharts (external).
- **Standards:** Canvas/SVG. · **Maturity:** Very mature, hugely popular. Apache-2.0.

**Apache Zeppelin** — *Java/web · 🟢 Active*
- **Description:** Web-based notebook for interactive data analytics.
- **Function:** Multi-language notebooks (Spark/SQL/Python) with built-in visualization.
- **Patterns:** Notebook REPL, pluggable interpreters, paragraph dataflow.
- **Use cases:** Interactive big-data analysis, collaborative data science.
- **Interfaces:** Web notebook UI; REST API; interpreter SPI. Service. · **Needs:** JVM; backing engines (Spark/Flink/JDBC).
- **Pairs with:** Spark, Flink, JDBC sources, Livy. · **Alternatives:** Jupyter, Polynote (external).
- **Standards:** none specific. · **Maturity:** Mature; strong Spark integration. Apache-2.0.

**Apache Livy** — *Scala/Java · 🟡 Low activity*
- **Description:** REST service for submitting and managing Spark jobs/sessions.
- **Function:** Lets apps run Spark code remotely over REST without a local Spark context.
- **Patterns:** Session management, remote job submission, async REST.
- **Use cases:** Backing notebooks/apps with shared Spark sessions.
- **Interfaces:** REST API; manages Spark sessions. Gateway service. · **Needs:** JVM + a Spark cluster.
- **Pairs with:** Spark, Zeppelin/Jupyter. · **Alternatives:** Kyuubi (ASF), Spark Connect (ASF). · **Standards:** REST. · **Maturity:** Low activity; Kyuubi/Spark Connect are newer. Apache-2.0.

**Apache Answer** — *Go · 🟢 Active (TLP, 2024)*
- **Description:** Q&A platform software for building knowledge communities (Stack Overflow-style).
- **Function:** Questions/answers, voting, reputation, moderation.
- **Patterns:** Community Q&A, reputation/gamification, plugin extensibility.
- **Use cases:** Support communities, internal knowledge bases, help centers.
- **Interfaces:** Web UI; REST API; plugin system. Standalone service. · **Needs:** a DB (MySQL/Postgres/SQLite); single binary (Go).
- **Pairs with:** auth/SSO providers, help-center stacks. · **Alternatives:** Discourse, Stack Overflow for Teams (external).
- **Standards:** REST. · **Maturity:** TLP (2024); easy single-binary deploy. Apache-2.0.

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

**Composability profile (whole family).** *Interfaces:* plain Java libraries, Maven coordinates
under `org.apache.commons` / `commons-*`; embeddable, no services. *Needs:* a JVM; most components
have zero or minimal transitive dependencies. *Pairs with:* essentially every JVM project — pulled
in transitively by Spark, Hadoop, Camel, Tomcat, and countless others. *Alternatives:* Google Guava
and Eclipse Collections (external), or modern JDK built-ins (`java.nio.file`, `java.util.stream`)
for some needs. *Standards:* n/a (utility libraries). *Maturity:* among the most-depended-on JARs
in existence; Apache-2.0. **Security note:** some components have had serious CVEs (Commons
Collections deserialization "gadget chains"; Commons Text's `StringSubstitutor` "Text4Shell",
CVE-2022-42889) — pin current versions and avoid untrusted input to interpolation/deserialization.

### 25. Core libraries — Logging Services

*The Logging Services project maintains logging frameworks across languages.*

**Apache Log4j 2** — *Java · 🟢 Active*
- **Description:** High-performance, asynchronous logging framework (the Log4j 1.x successor).
- **Function:** Structured, configurable application logging with pluggable appenders/layouts.
- **Patterns:** Appender/layout/filter SPI, async (LMAX Disruptor) logging, plugin system.
- **Use cases:** Application logging across the Java world.
- **Interfaces:** Log4j API (or SLF4J facade); appender/layout plugin SPI; config (XML/JSON/YAML/properties). Embeddable library. · **Needs:** JVM.
- **Pairs with:** SLF4J, virtually every JVM app; JSON layouts → log aggregators. · **Alternatives:** Logback, `java.util.logging` (external); Commons Logging (ASF, facade).
- **Standards:** SLF4J binding; JSON/ECS layouts. · **Maturity:** Ubiquitous. **Security note:** the 2021 "Log4Shell" (CVE-2021-44228) JNDI RCE — keep ≥ 2.17.x; it reshaped OSS supply-chain security. Apache-2.0.

**Apache Log4net / Log4cxx** — *C#/C++ · 🟢 Active*
- Ports of the Log4j model to .NET and C++.
- **Interfaces:** native logging APIs (.NET / C++); appender config. Embeddable libraries. · **Needs:** .NET or C++ runtime. · **Pairs with:** .NET/C++ apps. · **Alternatives:** Serilog/NLog (.NET), spdlog (C++) (external). · **Maturity:** Mature, lower cadence. Apache-2.0.

**Apache Chainsaw** — *Java · 🟢 Active*
- GUI log viewer/analyzer for Log4j output.
- **Interfaces:** desktop GUI; reads Log4j log streams/files. Tool. · **Needs:** JVM (desktop). · **Pairs with:** Log4j. · **Alternatives:** Kibana/Grafana for centralized logs (external). · **Maturity:** Niche desktop tool. Apache-2.0.

### 26. Core libraries — XML, HTTP & utilities

*Shared patterns: standards implementations, streaming parsers, pluggable transport, client libraries.*

**Apache Xerces** — *Java/C++/Perl · 🟢 Active*
- **Description:** XML parsers (DOM, SAX, StAX) and schema validators.
- **Patterns:** Streaming + tree parsing, schema validation.
- **Use cases:** The default XML parsing engine in much of the Java world.
- **Interfaces:** JAXP (DOM/SAX/StAX) APIs. Embeddable library. · **Needs:** JVM (or C++). · **Pairs with:** Xalan/FOP, any XML-processing app. · **Alternatives:** Woodstox, JDK built-in (external). · **Standards:** XML, XML Schema, JAXP. · **Maturity:** Mature, foundational. Apache-2.0.

**Apache Xalan** — *Java/C++ · 🟡 Low activity*
- **Description:** XSLT processor for transforming XML.
- **Patterns:** XSLT transformation, XPath.
- **Use cases:** XML-to-XML/HTML/text transformation.
- **Interfaces:** JAXP `Transformer` API; CLI. Embeddable library. · **Needs:** JVM (or C++). · **Pairs with:** FOP, Xerces. · **Alternatives:** Saxon (XSLT 2/3, external). · **Standards:** XSLT 1.0, XPath 1.0. · **Maturity:** Low activity (stuck at XSLT 1.0; Saxon for 2/3). Apache-2.0.

**Apache HttpComponents** — *Java · 🟢 Active*
- **Description:** **HttpClient** and **HttpCore** — low-level HTTP client/server toolkit.
- **Function:** Robust, standards-compliant HTTP client (sync/async) and building blocks.
- **Patterns:** Connection pooling, pluggable protocol interceptors.
- **Use cases:** HTTP in Java apps where fine control is needed.
- **Interfaces:** Java HTTP client/core APIs (classic + async/HTTP2). Embeddable library. · **Needs:** JVM. · **Pairs with:** CXF, REST clients, many JVM libs. · **Alternatives:** JDK `HttpClient` (Java 11+), OkHetty/OkHttp, Jetty client (external). · **Standards:** HTTP/1.1 & /2. · **Maturity:** Mature; widely embedded. Apache-2.0.

**Apache MINA** — *Java · 🟢 Active*
- **Description:** Network application framework for high-performance, async I/O; includes **SSHD** and **FtpServer**.
- **Function:** Event-driven, non-blocking networking abstraction.
- **Patterns:** Reactor/event-driven I/O, filter chain, protocol codec SPI.
- **Use cases:** Custom network servers/clients, embedding SSH/SFTP (Apache SSHD).
- **Interfaces:** Java async-I/O framework API; SSHD & FtpServer as embeddable servers. Embeddable library. · **Needs:** JVM. · **Pairs with:** custom protocol servers; Git (JGit uses SSHD). · **Alternatives:** Netty (external, more popular). · **Standards:** SSH, FTP (via sub-projects). · **Maturity:** Mature; SSHD widely embedded. Apache-2.0.

**Apache CXF** — *Java · 🟢 Active*
- **Description:** Services framework for SOAP and REST (JAX-WS / JAX-RS).
- **Function:** Build and consume web services with WS-* and REST support.
- **Patterns:** Interceptor chains, front-end abstraction (JAX-WS/JAX-RS), transport SPI.
- **Use cases:** Enterprise web services, contract-first SOAP, JAX-RS REST endpoints.
- **Interfaces:** JAX-WS/JAX-RS APIs; WSDL tooling; runs standalone, in Tomcat/TomEE, Karaf, or Spring. Library/framework. · **Needs:** JVM; a host runtime.
- **Pairs with:** WSS4J/Santuario (WS-Security), Camel, Karaf, Spring. · **Alternatives:** Spring Web Services, Metro, Quarkus REST (external).
- **Standards:** SOAP/WSDL/WS-*, JAX-RS, JAX-WS. · **Maturity:** Mature; the main JVM SOAP+REST framework. Apache-2.0.

**Apache Axis2** — *Java/C · 🟡 Low activity*
- **Description:** Earlier-generation SOAP/web-services engine.
- **Patterns:** Message-flow phases, module extensibility.
- **Use cases:** Legacy SOAP services.
- **Interfaces:** SOAP/WSDL; deploy AAR services. Service engine. · **Needs:** JVM + servlet container. · **Pairs with:** Rampart (WS-Security), legacy SOAP. · **Alternatives:** CXF (ASF) for new work. · **Standards:** SOAP, WSDL, WS-*. · **Maturity:** Low activity; use CXF instead. Apache-2.0.

**Apache WSS4J** / **Woden** — *Java · 🟢 Active*
- WS-Security implementation and a WSDL object model, respectively (support CXF/Axis).
- **Interfaces:** Java libraries (security handlers; WSDL parsing). Embeddable. · **Needs:** JVM. · **Pairs with:** CXF, Axis2, Santuario. · **Standards:** WS-Security, WSDL. · **Maturity:** Mature, niche (SOAP security). Apache-2.0.

**Apache Commons** — *(see [§24](#24-core-libraries--apache-commons))*

### 27. Business applications

*Shared patterns: domain-driven design, entity/data-model engines, pluggable modules, naked-objects UIs.*

**Apache OFBiz** — *Java · 🟢 Active*
- **Description:** Open-source ERP suite and business-automation framework.
- **Function:** Pre-built CRM, e-commerce, order/inventory/accounting, manufacturing, plus a framework to extend them.
- **Patterns:** Entity engine (data abstraction), service engine (SOA), screen widget framework.
- **Use cases:** ERP/e-commerce platforms; a base to build custom business apps.
- **Interfaces:** Web UI; SOAP/REST services; entity & service engines. Full application + framework. · **Needs:** JVM; a relational DB.
- **Pairs with:** a relational DB; payment/shipping integrations. · **Alternatives:** Odoo, ERPNext (external).
- **Standards:** SOAP/REST; EDI via add-ons. · **Maturity:** Mature; heavyweight but complete. Apache-2.0.

**Apache Fineract** — *Java · 🟢 Active*
- **Description:** Core-banking platform for financial inclusion (digital financial services).
- **Function:** Accounts, loans, savings, and transactions for banks/microfinance/fintechs.
- **Patterns:** Multi-tenant core banking, double-entry accounting, REST API.
- **Use cases:** Microfinance institutions, neobanks, financial-inclusion providers.
- **Interfaces:** REST API; multi-tenant; web/mobile clients (Mifos community). Service. · **Needs:** JVM; MySQL/MariaDB.
- **Pairs with:** Mifos X web/mobile apps, payment rails. · **Alternatives:** Mambu, Thought Machine (external, commercial).
- **Standards:** REST; double-entry accounting. · **Maturity:** Mature; widely used in financial inclusion. Apache-2.0.

**Apache Causeway (formerly Isis)** — *Java · 🟢 Active*
- **Description:** Framework for rapidly building domain-driven line-of-business apps.
- **Function:** Generates a UI and REST API automatically from the domain object model.
- **Patterns:** Naked Objects, domain-driven design, convention-driven UI generation.
- **Use cases:** Internal enterprise apps where the domain model is the focus.
- **Interfaces:** auto-generated web UI + Restful Objects API from domain classes; on Spring Boot. Framework. · **Needs:** JVM; a JPA/JDO datastore.
- **Pairs with:** Spring Boot, JPA, Wicket (UI). · **Alternatives:** JHipster, low-code platforms (external).
- **Standards:** Restful Objects. · **Maturity:** Mature, niche (DDD/naked-objects). Apache-2.0.

**Apache Unomi** — *Java · 🟢 Active*
- **Description:** Customer data platform (CDP) / context server implementing the OASIS CXS standard.
- **Function:** Stores visitor profiles/events and manages consent for personalization.
- **Patterns:** Event/profile store, segmentation rules, privacy/consent management.
- **Use cases:** Personalization engines, consent-respecting customer analytics.
- **Interfaces:** REST API; context/events JSON; GraphQL (CXS). Standalone service. · **Needs:** JVM; Elasticsearch/OpenSearch.
- **Pairs with:** CMSes (Jahia), web front ends, analytics. · **Alternatives:** RudderStack, Segment (external).
- **Standards:** OASIS Context Server (CXS). · **Maturity:** Mature, niche (open CDP). Apache-2.0.

**Apache SeaTunnel** — *Java · 🟢 Active*
- **Description:** High-performance, distributed data-integration platform.
- **Function:** Syncs massive data between 100+ sources/sinks (batch + CDC streaming).
- **Patterns:** Connector SPI, unified batch/stream integration, pluggable engine (Zeta/Spark/Flink).
- **Use cases:** Large-scale data ingestion/CDC/ETL across heterogeneous systems.
- **Interfaces:** config-driven jobs; 100+ connectors; runs on its Zeta engine or Spark/Flink; REST. Service + connectors. · **Needs:** JVM; (optional) Spark/Flink; source/sink systems.
- **Pairs with:** Kafka, databases (CDC), Iceberg/Hudi/Paimon, DolphinScheduler. · **Alternatives:** Airbyte, Debezium+Kafka Connect, NiFi (external/ASF).
- **Standards:** connector-specific. · **Maturity:** Growing fast; broad connector catalog. Apache-2.0.

**Apache InLong** — *Java · 🟢 Active*
- **Description:** One-stop integration framework for massive data ("MQ + ingestion + sorting").
- **Patterns:** End-to-end ingestion pipeline, pluggable sources/sinks.
- **Use cases:** High-volume data collection and distribution (from Tencent).
- **Interfaces:** web console + REST; agents; Manager/DataProxy/Sort components. Platform. · **Needs:** JVM; a message queue (Pulsar/Kafka/TubeMQ); ZooKeeper.
- **Pairs with:** Pulsar/Kafka, Flink (sort), Hive/Iceberg sinks. · **Alternatives:** SeaTunnel (ASF); Flume (ASF, legacy); Kafka Connect (external).
- **Standards:** connector-specific. · **Maturity:** Mature at Tencent scale. Apache-2.0.

**Apache Linkis** — *Scala/Java · 🟢 Active*
- **Description:** Computation middleware decoupling apps from underlying engines.
- **Function:** Unified job-submission/governance gateway to Spark/Hive/Flink/Presto.
- **Patterns:** Engine abstraction/orchestration, context service, resource governance.
- **Use cases:** Data-platform layer connecting many tools to many engines.
- **Interfaces:** REST/JDBC; computation-governance services; engine plugins. Gateway service. · **Needs:** JVM; the backing engines + their clusters.
- **Pairs with:** Spark/Hive/Flink/Presto, DataSphere Studio, DolphinScheduler. · **Alternatives:** Kyuubi (ASF); Livy (ASF). · **Standards:** REST, JDBC. · **Maturity:** Mature; common in Chinese data platforms. Apache-2.0.

### 28. Languages, runtimes & actor systems

**Apache Groovy** — *Java/Groovy · 🟢 Active*
- **Description:** Dynamic + static JVM language with concise syntax and strong Java interop.
- **Function:** Scripting, DSLs, and full applications on the JVM.
- **Patterns:** Metaprogramming (MOP), builder DSLs, optional static compilation.
- **Use cases:** Build scripts (Gradle, Jenkins pipelines), testing (Spock), DSLs, scripting.
- **Interfaces:** JVM language; embeddable `GroovyShell`; compiles to bytecode. Language + embeddable library. · **Needs:** JVM.
- **Pairs with:** Gradle, Jenkins, Spock, Grails (ASF). · **Alternatives:** Kotlin, Scala, Clojure (external/JVM).
- **Standards:** JVM bytecode. · **Maturity:** Very mature; huge via Gradle/Jenkins. Apache-2.0.

**Apache Pekko** — *Scala/Java · 🟢 Active*
- **Description:** Toolkit for concurrent, distributed, resilient message-driven apps (open-source fork of Akka 2.6).
- **Function:** Actor model, streams, clustering, and persistence on the JVM.
- **Patterns:** Actor model, supervision hierarchies, reactive streams, event sourcing/CQRS.
- **Use cases:** High-concurrency backends, streaming, distributed stateful systems (a BSL-free Akka path).
- **Interfaces:** Scala & Java actor/stream APIs; HTTP & gRPC modules; cluster. Embeddable library/toolkit. · **Needs:** JVM.
- **Pairs with:** Kafka (Pekko Connectors/Alpakka), gRPC/HTTP services, event-sourced systems. · **Alternatives:** Akka (external, BSL-licensed), Vert.x, Project Reactor (external).
- **Standards:** Reactive Streams; gRPC/HTTP. · **Maturity:** Maturing fork; the Apache-2.0 path off Akka's BSL. Apache-2.0.

**Apache OpenWhisk** — *Scala/multi · 🟡 Low activity*
- **Description:** Open-source serverless / Function-as-a-Service platform.
- **Function:** Runs functions in containers in response to events/triggers.
- **Patterns:** FaaS, event trigger→rule→action, container-per-invocation.
- **Use cases:** Self-hosted serverless event processing.
- **Interfaces:** `wsk` CLI + REST; actions in many languages (Docker). Platform. · **Needs:** Kubernetes/Docker; CouchDB; Kafka.
- **Pairs with:** Kubernetes, Kafka, CouchDB. · **Alternatives:** Knative, OpenFaaS, AWS Lambda (external); OpenServerless (ASF incubating).
- **Standards:** container actions; REST. · **Maturity:** Low activity; Knative/managed FaaS lead. Apache-2.0.

**Apache River** — *Java · 🗄️ Attic*
- **Description:** Jini-based service-oriented/distributed computing.
- **Use cases:** Dynamic service networks.
- **Leverage note:** 🗄️ Retired — use modern RPC/service-discovery (gRPC, Dubbo (ASF), Consul) instead.

**Apache OpenOffice** — *C++/Java · 🟢 Active*
- **Description:** Full office productivity suite (Writer, Calc, Impress, Draw, Base, Math).
- **Function:** Desktop documents, spreadsheets, presentations; ODF-native.
- **Patterns:** Document component model, ODF standard, UNO component bridge.
- **Use cases:** Free desktop office suite (sibling to the LibreOffice fork).
- **Interfaces:** desktop apps; UNO automation API; command-line conversion. Desktop application + automation API. · **Needs:** a desktop OS install.
- **Pairs with:** ODF workflows; headless conversion in pipelines. · **Alternatives:** LibreOffice (external, more active fork); Microsoft Office.
- **Standards:** OpenDocument (ODF); reads OOXML. · **Maturity:** Mature but slower-moving than LibreOffice. Apache-2.0.

**Apache JMeter** — *Java · 🟢 Active*
- **Description:** Load- and performance-testing tool.
- **Function:** Simulates concurrent load against web/APIs/databases and measures performance.
- **Patterns:** Thread-group load modeling, sampler/listener plugins, assertion pipeline.
- **Use cases:** Performance/stress/regression testing of services.
- **Interfaces:** desktop GUI + CLI (non-GUI runs); plugin SPI; JMX test plans; HTML reports. Tool. · **Needs:** JVM.
- **Pairs with:** CI pipelines, Grafana (reporting), Taurus. · **Alternatives:** Gatling, k6, Locust (external).
- **Standards:** HTTP/JDBC/JMS/gRPC (via samplers). · **Maturity:** Mature; the classic JVM load tester. Apache-2.0.

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
- **Interfaces:** `svn`/`svnadmin` CLI; HTTP/WebDAV & `svn://` protocols; language bindings. Service + client. · **Needs:** a server (httpd + `mod_dav_svn`, or `svnserve`); Serf for HTTP.
- **Pairs with:** httpd (`mod_dav_svn`), Serf (ASF), CI systems. · **Alternatives:** Git, Mercurial, Perforce (external).
- **Standards:** WebDAV/DeltaV. · **Maturity:** Mature, stable; largely displaced by Git. Apache-2.0.

**Apache NetBeans** — *Java · 🟢 Active*
- **Description:** Full-featured IDE and application platform (donated by Oracle).
- **Function:** Develops Java/PHP/JS and more; the NetBeans Platform hosts modular desktop apps.
- **Patterns:** Modular IDE platform (module system), project/build abstraction, plugin SPI.
- **Use cases:** Polyglot development; building rich-client (RCP-style) desktop applications.
- **Interfaces:** desktop IDE; NetBeans Platform module API (RCP). Application + platform. · **Needs:** JDK.
- **Pairs with:** Maven/Gradle/Ant, the JDK, app servers. · **Alternatives:** IntelliJ IDEA, Eclipse, VS Code (external).
- **Standards:** JPMS; LSP (partial). · **Maturity:** Mature; solid Java/Maven IDE. Apache-2.0.

**Apache Yetus** — *Java/shell · 🟢 Active*
- **Description:** Libraries and tools for contribution testing and release documentation.
- **Function:** "Precommit" automation that tests patches/PRs and audits release artifacts.
- **Patterns:** Precommit CI orchestration, pluggable test/analysis plugins, release audit.
- **Use cases:** Automated patch validation and release-note/license checking for OSS projects.
- **Interfaces:** CLI tools (`test-patch`, `releasedocmaker`); CI integration. Tooling. · **Needs:** the project's build tools; Docker (optional).
- **Pairs with:** Git/GitHub/Jenkins, Maven/Gradle builds (many ASF big-data projects). · **Alternatives:** GitHub Actions + bespoke scripts (external).
- **Standards:** n/a. · **Maturity:** Mature; widely used inside the ASF. Apache-2.0.

**Apache BuildStream** — *Python · 🟢 Active*
- **Description:** Tool to integrate, build, and bundle software stacks from source.
- **Function:** Produces deployable artifacts/images reproducibly from declarative build plans.
- **Patterns:** Declarative build pipelines, sandboxed/reproducible builds, artifact caching.
- **Use cases:** Building whole software stacks or OS images with reproducibility guarantees.
- **Interfaces:** `bst` CLI; YAML `.bst` element files; sandboxed builds. Tool. · **Needs:** Linux + sandboxing (bubblewrap); Python.
- **Pairs with:** Flatpak/freedesktop SDKs; OCI image output. · **Alternatives:** Bazel, Yocto, Nix (external).
- **Standards:** OCI images (output). · **Maturity:** Mature in GNOME/freedesktop builds. Apache-2.0.

**Apache Serf** — *C · 🟢 Active*
- **Description:** High-performance asynchronous HTTP client library built on APR.
- **Function:** Non-blocking HTTP(S) client used by native applications.
- **Patterns:** Async HTTP client, bucket-based streaming I/O.
- **Use cases:** HTTP access in C programs (notably Subversion's HTTP/WebDAV layer).
- **Interfaces:** C library API (APR-based). Embeddable library. · **Needs:** C toolchain + APR.
- **Pairs with:** Subversion (its HTTP layer), APR-based C apps. · **Alternatives:** libcurl (external).
- **Standards:** HTTP/1.1. · **Maturity:** Mature, niche. Apache-2.0.

**Apache Magpie** — *Python/Java · 🟢 Active (TLP, 2026)*
- **Description:** Platform infrastructure for AI-/agent-assisted maintenance of open-source repositories.
- **Function:** Helps maintainers with issue/PR triage, security-issue handling, and routine upkeep via agents.
- **Patterns:** Agent-assisted maintainership, pluggable task agents, workflow automation (originated in Airflow).
- **Use cases:** Reducing maintainer load and response times on open-source projects.
- **Interfaces:** agent framework + forge/issue-tracker integrations; config-driven agents. Platform/service. · **Needs:** a runtime for agents; repo/issue API access; LLM backends.
- **Pairs with:** GitHub/Git forges, CI, Airflow (origin). · **Alternatives:** Dependabot/Renovate, bespoke bots (external).
- **Standards:** Git-forge APIs. · **Maturity:** New TLP (2026); early. Apache-2.0.

#### 29.2 ASF foundation infrastructure

**Apache Whimsy** — *Ruby · 🟢 Active*
- **Description:** Web tools that expose and automate ASF organizational data.
- **Function:** Board agendas, committee rosters, membership, and self-service governance tasks.
- **Patterns:** Data-driven admin tooling over authoritative records/LDAP.
- **Use cases:** Running ASF governance operations (meta-tooling for the foundation itself).
- **Interfaces:** web tools + CLI over ASF records/LDAP. Service (ASF-internal). · **Needs:** Ruby; access to ASF data/LDAP.
- **Pairs with:** ASF LDAP, board/committee processes. · **Alternatives:** bespoke org tooling (external).
- **Standards:** LDAP. · **Maturity:** Mature; ASF-specific. Apache-2.0.

**Apache STeVe** — *Python · 🟢 Active*
- **Description:** Online voting system used for ASF elections.
- **Function:** Collects and tallies ballots (including Single Transferable Vote).
- **Patterns:** Electronic ballot + tallying algorithms.
- **Use cases:** Board/member elections and other community votes.
- **Interfaces:** web voting UI + email ballots; tally tools. Service. · **Needs:** Python; a mail setup.
- **Pairs with:** ASF elections. · **Alternatives:** Helios, OpaVote (external).
- **Standards:** STV tallying. · **Maturity:** Niche (ASF governance). Apache-2.0.

**Apache Pony Mail** — *Java/JS · 🟢 Active*
- **Description:** Mail-archive browser and archiver with full-text search.
- **Function:** Turns mailing-list traffic into a searchable, linkable web archive.
- **Patterns:** Archived pub/sub indexing, searchable thread model.
- **Use cases:** Browsable/searchable mailing-list archives (the ASF runs its lists on it).
- **Interfaces:** web archive UI + search; ingests mbox/IMAP. Service. · **Needs:** Elasticsearch/Lucene; a mail source.
- **Pairs with:** mailing lists, Elasticsearch. · **Alternatives:** HyperKitty/Mailman 3 (external).
- **Standards:** mbox, IMAP. · **Maturity:** Mature (runs the ASF's own lists). Apache-2.0.

#### 29.3 Databases & persistence

**Apache AsterixDB** — *Java · 🟢 Active*
- **Description:** Parallel big-data management system for semistructured (NoSQL) data with the SQL++ language.
- **Function:** Ingests and queries large volumes of flexible-schema (JSON-like) records.
- **Patterns:** Shared-nothing parallel DBMS, LSM storage, declarative query over flexible schema, data feeds.
- **Use cases:** Large-scale analytics over semistructured data, continuous data ingestion.
- **Interfaces:** SQL++ over an HTTP API; data feeds. Cluster service. · **Needs:** JVM; a cluster; storage.
- **Pairs with:** streaming data feeds (social/IoT), BI tools. · **Alternatives:** MongoDB, Couchbase, Elasticsearch (external); Cassandra (ASF).
- **Standards:** SQL++ (own). · **Maturity:** Mature (research-grade BDMS). Apache-2.0.

**Apache Kvrocks** — *C++ · 🟢 Active*
- **Description:** Distributed key-value database that speaks the Redis protocol, built on RocksDB.
- **Function:** Redis-compatible storage for datasets larger than RAM, at lower cost.
- **Patterns:** Redis API over an LSM engine (RocksDB), disk-based KV, namespacing, replication.
- **Use cases:** Redis-API workloads needing persistence and large capacity.
- **Interfaces:** Redis wire protocol (RESP); any Redis client. Service. · **Needs:** its own daemon(s); disk (RocksDB).
- **Pairs with:** Redis clients/tooling; Sentinel-style HA. · **Alternatives:** Redis, Dragonfly, KeyDB (external).
- **Standards:** RESP (Redis protocol). · **Maturity:** Mature; cost-effective Redis-API store. Apache-2.0.

**Apache CarbonData** — *Java/Scala · 🟢 Active*
- **Description:** Indexed columnar data format for fast analytics on big-data platforms.
- **Function:** Stores huge datasets with multi-level indexing for both scans and point lookups.
- **Patterns:** Columnar storage + indexing, deep Spark integration, data skipping.
- **Use cases:** Interactive queries mixing full scans and selective lookups over large tables.
- **Interfaces:** Spark/Hive table format + SDK; SQL via Spark. Library/format. · **Needs:** Spark (primary); HDFS/object store.
- **Pairs with:** Spark, Hadoop, Presto/Trino (reader). · **Alternatives:** Iceberg/Hudi/ORC/Parquet (ASF).
- **Standards:** own columnar format. · **Maturity:** Mature; strongest in Spark+HDFS. Apache-2.0.

**Apache Cayenne** — *Java · 🟢 Active*
- **Description:** Object-relational mapping (ORM) framework with a visual modeler.
- **Function:** Maps Java objects to relational databases with an object-graph persistence context.
- **Patterns:** ORM, unit-of-work/object context, remote object persistence.
- **Use cases:** Database persistence for Java apps without hand-written SQL.
- **Interfaces:** Java ORM API + Modeler GUI. Embeddable library. · **Needs:** JVM; a JDBC database.
- **Pairs with:** any JVM app + RDBMS. · **Alternatives:** Hibernate/JPA, jOOQ (external); OpenJPA (ASF).
- **Standards:** JDBC. · **Maturity:** Mature, stable. Apache-2.0.

**Apache OpenJPA** — *Java · 🟢 Active*
- **Description:** Implementation of the Jakarta Persistence (JPA) specification.
- **Function:** Standard ORM persistence with bytecode enhancement.
- **Patterns:** ORM, persistence context, bytecode enhancement, spec implementation.
- **Use cases:** JPA persistence layer, embeddable in Jakarta EE servers (e.g., TomEE/Geronimo heritage).
- **Interfaces:** Jakarta Persistence (JPA) API; bytecode enhancer. Embeddable library. · **Needs:** JVM; a JDBC database.
- **Pairs with:** TomEE/Geronimo, Jakarta EE apps. · **Alternatives:** Hibernate, EclipseLink (external).
- **Standards:** Jakarta Persistence (JPA). · **Maturity:** Mature spec impl, lower cadence. Apache-2.0.

**Apache Empire-db** — *Java · 🟢 Active*
- **Description:** Lightweight, SQL-centric relational data-access library (an ORM alternative).
- **Function:** Type-safe, dynamically generated SQL defined in Java code rather than mapping files.
- **Patterns:** Code-defined type-safe SQL, DBMS abstraction.
- **Use cases:** Java database access where you want SQL control with compile-time safety.
- **Interfaces:** Java fluent SQL API; DBMS drivers. Embeddable library. · **Needs:** JVM; a JDBC database.
- **Pairs with:** JVM apps wanting SQL control. · **Alternatives:** jOOQ, MyBatis (external).
- **Standards:** JDBC, SQL. · **Maturity:** Mature, niche. Apache-2.0.

**Apache ResilientDB** — *C++ · 🟢 Active*
- **Description:** High-throughput, sustainable distributed-ledger / blockchain platform (research lineage, UC Davis).
- **Function:** Scalable permissioned ledger with parallelized, pipelined transaction processing.
- **Patterns:** Byzantine-fault-tolerant consensus, pipelined/parallel execution, modular consensus.
- **Use cases:** Permissioned blockchains, distributed-ledger research and applications.
- **Interfaces:** SDK/APIs; KV + smart-contract layer; HTTP. Platform. · **Needs:** C++ toolchain; a cluster.
- **Pairs with:** blockchain apps, academic research. · **Alternatives:** Hyperledger Fabric, CometBFT/Tendermint (external).
- **Standards:** own; BFT consensus. · **Maturity:** Research-grade; growing. Apache-2.0.

#### 29.4 Graph & analytics libraries

**Apache HugeGraph** — *Java · 🟢 Active*
- **Description:** Fast, scalable graph database (OLTP) with analytics tooling.
- **Function:** Stores and traverses large property graphs; Gremlin-compatible.
- **Patterns:** Property-graph store, TinkerPop/Gremlin API, pluggable storage backends.
- **Use cases:** Knowledge graphs, fraud/relationship analysis, graph OLTP + algorithms.
- **Interfaces:** Gremlin (TinkerPop) + REST; HugeGraph-Server. Service. · **Needs:** JVM; a storage backend (RocksDB/HBase/Cassandra/MySQL).
- **Pairs with:** TinkerPop tools, HBase/Cassandra (ASF), HugeGraph-Computer (analytics). · **Alternatives:** JanusGraph, Neo4j, NebulaGraph (external).
- **Standards:** TinkerPop/Gremlin. · **Maturity:** Growing; OLTP property graph. Apache-2.0.

**Apache DataSketches** — *Java/C++/Python · 🟢 Active*
- **Description:** Library of streaming, stochastic ("sketch") algorithms for approximate analytics.
- **Function:** Small, mergeable summaries for distinct counts, quantiles, and frequent items.
- **Patterns:** Probabilistic data structures, mergeable summaries, sublinear memory.
- **Use cases:** Fast approximate cardinality/quantiles at scale inside SQL engines and pipelines.
- **Interfaces:** Java/C++/Python libraries; SQL UDFs (Druid/Hive/Postgres/BigQuery). Embeddable library. · **Needs:** a host-language runtime.
- **Pairs with:** Druid, Hive, Pinot, Spark, Postgres (sketch UDFs). · **Alternatives:** stand-alone HyperLogLog/t-digest impls (external).
- **Standards:** cross-language-compatible sketch binary formats. · **Maturity:** Mature; reused across many engines. Apache-2.0.

#### 29.5 Data formats

**Apache Daffodil** — *Scala/Java · 🟢 Active*
- **Description:** Implementation of the Data Format Description Language (DFDL).
- **Function:** Parses complex binary/text formats into XML/JSON and serializes back ("unparse").
- **Patterns:** Declarative grammar-driven parsing (DFDL schema), bidirectional (un)parsing.
- **Use cases:** Converting legacy/industry formats (EDI, MIL-STD, financial, scientific) to structured data.
- **Interfaces:** Java/Scala API + CLI; DFDL schema → XML/JSON/SAX; VS Code debugger. Embeddable library + tool. · **Needs:** JVM.
- **Pairs with:** NiFi (processor), data pipelines, legacy feeds. · **Alternatives:** hand-written parsers, Kaitai Struct (external).
- **Standards:** DFDL (OGF); XML/JSON. · **Maturity:** Mature; the open DFDL implementation. Apache-2.0.

#### 29.6 Web frameworks, content & collaboration

**Apache Grails** — *Groovy · 🟢 Active*
- **Description:** Full-stack, convention-driven web framework on Groovy and Spring Boot.
- **Function:** Rapid web-application development (Rails-style) on the JVM.
- **Patterns:** Convention over configuration, MVC, GORM (ORM), plugin system.
- **Use cases:** Fast JVM web apps and REST backends.
- **Interfaces:** Groovy framework on Spring Boot; CLI; plugin system. Application framework. · **Needs:** JVM; a database (GORM).
- **Pairs with:** Spring Boot, GORM/Hibernate, Groovy (ASF). · **Alternatives:** Spring Boot, Micronaut, Rails (external).
- **Standards:** Servlet; REST. · **Maturity:** Mature; stable Groovy web stack. Apache-2.0.

**Apache Juneau** — *Java · 🟢 Active*
- **Description:** Toolkit to marshal POJOs across formats and build self-documenting REST APIs/microservices.
- **Function:** Serializes Java objects to JSON/XML/HTML/etc. and exposes them as REST.
- **Patterns:** Format-agnostic serialization SPI, REST interface proxies, HATEOAS.
- **Use cases:** Content negotiation, REST API layers, typed remote proxies, configuration.
- **Interfaces:** Java marshalling API + REST server/client; config store. Embeddable library. · **Needs:** JVM.
- **Pairs with:** REST microservices; config management. · **Alternatives:** Jackson + JAX-RS, Spring REST (external).
- **Standards:** JSON/XML/HTML/UON/…; HTTP; HATEOAS. · **Maturity:** Mature, niche. Apache-2.0.

**Apache JSPWiki** — *Java · 🟢 Active*
- **Description:** Feature-rich Java-based wiki engine.
- **Function:** Wiki content authoring/rendering with access control and plugins.
- **Patterns:** Wiki markup rendering, pluggable page providers, templating.
- **Use cases:** Team/project wikis and documentation sites.
- **Interfaces:** web wiki; deploys as WAR; plugin/filter API. Service. · **Needs:** JVM + servlet container; storage (files/DB).
- **Pairs with:** Tomcat, LDAP auth. · **Alternatives:** MediaWiki, Confluence, DokuWiki (external).
- **Standards:** wiki markup; JSP. · **Maturity:** Mature, niche. Apache-2.0.

**Apache OpenMeetings** — *Java · 🟢 Active*
- **Description:** Web conferencing and real-time collaboration server.
- **Function:** Video/audio meetings, chat, whiteboard, and document sharing.
- **Patterns:** Real-time media (WebRTC/Kurento), room/session model.
- **Use cases:** Self-hosted video meetings, online classrooms and webinars.
- **Interfaces:** web app (WebRTC); SOAP/REST API; deploys as WAR. Service. · **Needs:** JVM; a database; a media server (Kurento); OpenOffice (doc conversion).
- **Pairs with:** LDAP, calendar/LMS integrations. · **Alternatives:** Jitsi, BigBlueButton (external).
- **Standards:** WebRTC, SOAP/REST. · **Maturity:** Mature, niche self-hosted conferencing. Apache-2.0.

#### 29.7 Mail & anti-abuse

**Apache James** — *Java · 🟢 Active*
- **Description:** "Java Apache Mail Enterprise Server" — a modular mail server and email-processing framework.
- **Function:** SMTP/IMAP/POP3 server plus a programmable mail-processing pipeline.
- **Patterns:** Pipes-and-filters mail processing (Mailets/Matchers), protocol servers on Netty, pluggable mailbox stores.
- **Use cases:** Enterprise mail servers, programmable email gateways, anti-abuse processing.
- **Interfaces:** SMTP/IMAP/POP3/JMAP servers; Mailet/Matcher API; REST admin. Server + framework. · **Needs:** JVM; a mailbox store (Cassandra/JPA/file); optional ES for search.
- **Pairs with:** Cassandra (ASF), Lucene/ES, SpamAssassin (ASF). · **Alternatives:** Postfix + Dovecot, Zimbra (external).
- **Standards:** SMTP, IMAP, POP3, JMAP, Sieve. · **Maturity:** Mature; also a programmable mail framework. Apache-2.0.

**Apache SpamAssassin** — *Perl · 🟢 Active*
- **Description:** Extensible mail filter for identifying spam.
- **Function:** Scores messages with rules, Bayesian learning, and DNS blocklists.
- **Patterns:** Rule engine + weighted scoring, plugin filters, Bayesian classification.
- **Use cases:** Anti-spam filtering at mail servers and providers.
- **Interfaces:** `spamassassin`/`spamd` + `spamc`; milter; Perl API. Service/filter. · **Needs:** Perl; MTA integration; (optional) DNS blocklists.
- **Pairs with:** Postfix/Sendmail/Exim, James (ASF), amavis. · **Alternatives:** Rspamd (external).
- **Standards:** milter; DNSBL. · **Maturity:** Mature; long-standing anti-spam standard. Apache-2.0.

#### 29.8 OSGi, Jakarta EE & libraries

**Apache Celix** — *C/C++ · 🟢 Active*
- **Description:** Implementation of the OSGi specification for C and C++.
- **Function:** Brings a dynamic module system + service registry to native code.
- **Patterns:** OSGi modular runtime (native), service registry, dependency management.
- **Use cases:** Modular, dynamically composed C/C++ systems.
- **Interfaces:** C/C++ OSGi API; service registry; `celix` shell. Embeddable runtime/library. · **Needs:** C/C++ toolchain.
- **Pairs with:** native modular systems (robotics/DDS-adjacent). · **Alternatives:** Felix/Equinox (ASF, JVM); bespoke plugin systems (external).
- **Standards:** OSGi (C/C++ mapping). · **Maturity:** Mature, niche (native OSGi). Apache-2.0.

**Apache BVal** — *Java · 🟢 Active*
- **Description:** Implementation of the Jakarta Bean Validation specification.
- **Function:** Declarative, annotation-driven validation of Java objects.
- **Patterns:** Declarative constraint validation, constraint SPI, spec implementation.
- **Use cases:** Bean/data validation in Java apps (commonly with TomEE).
- **Interfaces:** Jakarta Bean Validation API; constraint SPI. Embeddable library. · **Needs:** JVM.
- **Pairs with:** TomEE, JAX-RS/JPA stacks. · **Alternatives:** Hibernate Validator (external).
- **Standards:** Jakarta Validation (JSR-380). · **Maturity:** Mature spec impl. Apache-2.0.

**Apache Tcl** — *C/Tcl · 🟢 Active*
- **Description:** Integration of the Tcl scripting language with the Apache HTTP Server (mod_tcl / Rivet lineage).
- **Function:** Embeds a Tcl interpreter for dynamic web content inside httpd.
- **Patterns:** httpd module, embedded interpreter.
- **Use cases:** Tcl-driven dynamic pages served directly by Apache httpd.
- **Interfaces:** httpd module (mod_tcl / Rivet); Tcl API. httpd module. · **Needs:** Apache httpd + Tcl.
- **Pairs with:** Apache httpd. · **Alternatives:** PHP, FastCGI/WSGI apps (external).
- **Standards:** Tcl; httpd module ABI. · **Maturity:** Niche, legacy-leaning. Apache-2.0.

**Apache Reqsign** — *Rust · 🟢 Active*
- **Description:** Library to sign API requests for many cloud providers (from the OpenDAL community).
- **Function:** Produces provider-specific request signatures (AWS SigV4, Azure, Google, etc.).
- **Patterns:** Credential/signing abstraction, provider adapter.
- **Use cases:** Signing cloud-service API calls in Rust (used by OpenDAL). *(Newly established, 2026.)*
- **Interfaces:** Rust crate; per-provider request-signing API. Embeddable library. · **Needs:** Rust.
- **Pairs with:** OpenDAL (ASF), Rust cloud clients. · **Alternatives:** provider SDK signers (external).
- **Standards:** AWS SigV4; Azure/Google signing schemes. · **Maturity:** New (2026); from the OpenDAL community. Apache-2.0.

#### 29.9 Cloud provisioning

**Apache VCL (Virtual Computing Lab)** — *Perl/Java · 🟢 Active*
- **Description:** Self-service provisioning and scheduling of dedicated compute environments on demand.
- **Function:** Reserves and images bare-metal/VM resources for time-boxed use.
- **Patterns:** Reservation/scheduling broker, image-based provisioning.
- **Use cases:** On-demand lab/VDI environments for education and enterprises.
- **Interfaces:** web portal + REST; provisioning backends (VMware/KVM/bare metal). Platform. · **Needs:** a management node; a DB; hypervisors/hardware.
- **Pairs with:** campus IT, image libraries. · **Alternatives:** OpenStack, commercial VDI (external).
- **Standards:** provisioning-backend specific. · **Maturity:** Mature in higher-ed. Apache-2.0.

#### 29.10 AI-era data governance

**Apache Sourcelume** — *multi · 🟢 Active (TLP, 2026)*
- **Description:** Attestation and registry layer for documenting the origins and permitted uses of AI training data.
- **Function:** Lets dataset provenance/consent metadata be cryptographically signed, published, and independently verified.
- **Patterns:** Attestation/registry over existing metadata standards, cryptographic signing, provenance chain.
- **Use cases:** Documenting and auditing AI training-data provenance and usage rights.
- **Interfaces:** spec + registry + CLI; signed attestations over dataset metadata. Spec + service/tooling. · **Needs:** signing keys; a registry; existing metadata standards.
- **Pairs with:** AI data pipelines; provenance/consent metadata (C2PA-adjacent). · **Alternatives:** C2PA, bespoke data cards (external).
- **Standards:** attestation over existing metadata standards; cryptographic signatures. · **Maturity:** New TLP (2026); early. Apache-2.0.

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
deleting a repo. **For leverage decisions, treat Attic projects as "read-only legacy":** safe to
keep running, unsafe to bet new work on (no security fixes) — each entry above names a current
alternative in its *Leverage note*.

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

> **Authoritative retired list:** `https://attic.apache.org/projects.html` (reconciled 2026-11-06).

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
- *OSGi modularity* → Felix, Karaf, Aries, Celix.
- *Component UI / front-controller* → Wicket, Tapestry, MyFaces, Struts.
- *Actor / reactive I/O* → Pekko, MINA.

---

## Part 6 — Composition & interoperability guide

This is the "can I leverage / combine it" layer. It reads *across* the per-entry **Interfaces /
Needs / Pairs-with / Standards** fields to answer three questions fast: *what snaps together into
a working stack* (6.1), *which of several close options to pick* (6.2), *what a choice drags in*
(6.3), and *who speaks a given protocol/format* (6.4).

### 6.1 ASF stack recipes

Canonical, battle-tested combinations. Read each as *stage → stage → …*; every name is an ASF
project unless marked *(ext)*.

- **Streaming lakehouse.** Kafka/Pulsar (ingest) → Flink (process, exactly-once) → Paimon or
  Iceberg on object storage (store) → Trino *(ext)* / Spark (query), governed by Polaris or
  Gravitino (catalog), scheduled by Airflow, traced by SkyWalking.
- **Batch data lake / warehouse.** Spark or Hive-on-Tez (compute) over HDFS or S3, tables in
  Iceberg with Parquet/ORC files, Hive Metastore or Polaris (catalog), Ranger + Knox (authz +
  perimeter), orchestrated by Airflow, explored in Superset.
- **Real-time analytics serving.** Kafka → Flink (enrich) → Druid / Pinot / Doris (OLAP store) →
  Superset or a custom app (sub-second dashboards).
- **CDC to the lake.** Debezium/Kafka Connect *(ext/ASF)* or SeaTunnel or InLong (capture) →
  Hudi or Paimon (upsert tables) → Spark/Flink (read) — for GDPR deletes and near-real-time.
- **Event-driven microservices.** Dubbo or ServiceComb (services) behind APISIX or ShenYu
  (gateway), events over Kafka or RocketMQ, EventMesh for multi-cluster eventing, ZooKeeper +
  Curator (coordination), Shiro/Ranger (authz), SkyWalking (tracing).
- **Enterprise search platform.** Nutch or StormCrawler (crawl) → Tika (extract) → Solr (index &
  serve), with ManifoldCF propagating source ACLs for secure enterprise search.
- **IoT / edge ingestion.** PLC4X or MQTT via ActiveMQ (field protocols) → MiNiFi/NiFi (edge
  routing + provenance) → Kafka → IoTDB (time-series store) or Flink (analytics) → dashboards.
- **Content / web experience (AEM-style).** Jackrabbit Oak (JCR repository) + Sling (resource
  rendering) on Felix/Karaf (OSGi), templated with HTL/FreeMarker, fronted by httpd/Traffic Server.
- **Classic on-prem Hadoop.** HDFS + YARN (base) + Hive-on-Tez + HBase (+ Phoenix for SQL) +
  ZooKeeper (coordination) + Ranger/Knox (security) + Spark, all provisioned by Ambari and
  packaged by Bigtop.
- **Durable messaging on shared log storage.** Pulsar (brokers) on BookKeeper (segment storage) +
  ZooKeeper/etcd — or Kafka with KRaft (no ZooKeeper) for a single-process log.
- **JVM enterprise application.** Tomcat/TomEE (container) + OpenWebBeans/DeltaSpike (CDI) +
  OpenJPA or Cayenne (persistence) + BVal (validation) + Shiro (security) + Log4j (logging) +
  Commons (utilities).
- **Elastic Spark on Kubernetes.** Spark + Gluten (native acceleration) + Celeborn or Uniffle
  (remote shuffle) + YuniKorn (queue scheduling), tables in Iceberg, catalog Gravitino.
- **Model deployment.** Train with Spark MLlib / SystemDS / Mahout → compile/optimize with TVM →
  serve; iterate in Zeppelin notebooks; orchestrate with Airflow.

### 6.2 Head-to-head selection matrix

When several ASF projects do "the same job," the differentiator matters. *(Pick-when guidance is
editorial.)*

| Decision | Options | Pick-when |
|----------|---------|-----------|
| **Event streaming / messaging** | Kafka · Pulsar · RocketMQ · ActiveMQ/Artemis · Qpid | **Kafka**: de-facto log, biggest ecosystem. **Pulsar**: multi-tenancy, geo-replication, tiered storage, unified queue+stream. **RocketMQ**: transactional/ordered messaging, financial/e-commerce. **ActiveMQ**: classic JMS + IoT protocols. **Qpid**: standards-pure AMQP. |
| **Stream processing** | Flink · Spark Structured Streaming · Kafka Streams · Samza · Storm | **Flink**: low-latency, large state, exactly-once. **Spark**: unify with existing batch. **Kafka Streams**: library, Kafka-only, no cluster. **Samza/Storm**: legacy/niche. |
| **Lakehouse table format** | Iceberg · Hudi · Paimon | **Iceberg**: broadest engine/vendor support, the emerging standard. **Hudi**: heavy upserts/CDC, record-level. **Paimon**: Flink-native streaming lakehouse. (Use **XTable** to interop among them.) |
| **Real-time OLAP store** | Druid · Pinot · Doris · Kylin | **Druid/Pinot**: user-facing sub-second over event streams. **Doris**: MySQL-protocol, simple ops, high concurrency. **Kylin**: precomputed cubes over Hadoop. |
| **Scalable NoSQL** | Cassandra · HBase · Accumulo | **Cassandra**: masterless multi-DC HA, no HDFS. **HBase**: strong consistency on HDFS, pairs with Phoenix. **Accumulo**: cell-level security. |
| **Search** | Lucene · Solr | **Lucene**: embed in your app. **Solr**: standalone distributed search server. |
| **API gateway** | APISIX · ShenYu · Knox | **APISIX**: high-performance, multi-protocol, etcd-driven. **ShenYu**: reactive JVM, Dubbo/Spring Cloud shops. **Knox**: specifically to front Hadoop services. |
| **Coordination** | ZooKeeper (+Curator) · Ratis · BookKeeper | **ZooKeeper**: coordination as a service (use via Curator). **Ratis**: embed Raft in your own system. **BookKeeper**: a durable replicated log. |
| **Serialization / IDL** | Avro · Thrift · Parquet · Fory · Arrow | **Avro**: streaming/Kafka records + schema evolution. **Thrift**: polyglot RPC + types. **Parquet**: on-disk columnar analytics. **Arrow**: in-memory columnar/interchange. **Fory**: fastest general object ser. |
| **JVM build** | Maven · Ant(+Ivy) | **Maven**: convention + dependency management (default). **Ant+Ivy**: fully custom/imperative or legacy. |
| **Logging (JVM)** | Log4j 2 · Commons Logging | **Log4j 2**: the implementation (via SLF4J). **Commons Logging**: a thin facade only (legacy). |
| **Workflow orchestration** | Airflow · DolphinScheduler | **Airflow**: code-first Python DAGs, huge provider ecosystem. **DolphinScheduler**: low-code visual DAGs, big-data task focus. |
| **Remote shuffle** | Celeborn · Uniffle | Both disaggregate Spark shuffle; choose by integration/perf testing in your environment. |
| **Spark native acceleration** | Gluten · Auron *(incubating)* | **Gluten**: mature, Velox/ClickHouse backends. **Auron**: DataFusion-based, newer. |

### 6.3 Shared-substrate / dependency map

What a choice *drags in*. Adopting a project on the left generally means also running the
substrate on the right.

- **Needs Apache ZooKeeper:** HBase, Solr (SolrCloud), Accumulo, Storm, Helix, Druid (default),
  Kafka *(legacy — KRaft removes it)*, Pulsar *(ZK or etcd)*, Hadoop HA, ShardingSphere-Proxy,
  DolphinScheduler, InLong. → usually consumed via **Curator**.
- **Needs HDFS or an object store (S3/GCS/ABFS):** HBase, Hive, Impala, Tez, Kylin, Hudi/Iceberg/
  Paimon tables, Spark/Flink checkpoints, Ozone-style workloads. (Object storage is abstracted by
  **OpenDAL** and, for Java, the Hadoop `S3A`/`FileSystem` API.)
- **Needs BookKeeper:** Pulsar, DistributedLog.
- **Embeds Raft via Ratis:** Ozone, IoTDB (cluster) — the "I need consensus inside my system" path.
- **Embeds Apache Calcite (SQL planner):** Flink SQL, Druid, Hive, Beam SQL, Kylin, Phoenix — so a
  team already knows "one" SQL dialect/optimizer across them.
- **Built on Apache Arrow (columnar memory):** DataFusion, Gluten, Parquet C++, Spark (interchange),
  many Python tools — Arrow is the lingua franca for zero-copy columnar data.
- **Built on Apache Lucene:** Solr (and non-ASF Elasticsearch/OpenSearch).
- **Runs on the JVM (the large majority):** Kafka, Spark, Flink, Hive, Cassandra, HBase, Lucene/
  Solr, Camel, NiFi, ZooKeeper, Maven, Groovy, Tomcat, and most of §2–§28. **Non-JVM exceptions**
  worth noting for polyglot shops: *C/C++* — httpd, Traffic Server, Kudu, Impala (backend), bRPC,
  Celix, Subversion, Serf, Kvrocks, ResilientDB; *Rust* — DataFusion, Teaclave, Reqsign, (Auron/
  Iggy incubating); *Go* — Answer, YuniKorn, Traffic Control; *Python* — Airflow, Libcloud,
  BuildStream, Superset (+TS); *Erlang* — CouchDB; *Perl* — SpamAssassin; *JS/TS* — ECharts,
  Cordova; *C (RTOS)* — NuttX, Mynewt.

### 6.4 Protocol / format / standard index

"Speaks X" → reach for these. Shared standards are what make two projects swappable or
composable without glue code.

- **JDBC / SQL endpoint:** Hive (HiveServer2), Impala, Drill, Phoenix, Kyuubi, Calcite (Avatica),
  Derby, Ignite, Kylin, Doris (also MySQL wire), ShardingSphere, Spark Thrift Server.
- **MySQL wire protocol:** Doris, ShardingSphere(-Proxy). **PostgreSQL wire:** ShardingSphere-Proxy.
- **Kafka protocol:** Kafka (and Pulsar's Kafka adapter).
- **AMQP:** Qpid, ActiveMQ. **MQTT:** ActiveMQ, BifroMQ *(incubating)*, PLC4X, EventMesh (+ IoTDB ingest).
- **JMS:** ActiveMQ/Artemis, Qpid (JMS client).
- **gRPC:** Arrow Flight, bRPC, Dubbo (Triple), RocketMQ 5.x, many services.
- **S3 / object-store API (consumers):** Spark, Flink, Iceberg/Hudi/Paimon, Hive, Druid; abstracted by OpenDAL.
- **Columnar data (Parquet / ORC / Arrow):** the whole analytics tier (§4–§6) interchanges through these.
- **JCR (content repository):** Jackrabbit/Oak, Sling.
- **LDAP / Kerberos:** Directory (ApacheDS/Kerby); consumed by Knox, Ranger, Hadoop, Syncope, Shiro.
- **SPARQL / RDF:** Jena (Fuseki).
- **Gremlin (graph traversal):** TinkerPop, HugeGraph (+ non-ASF JanusGraph/Neptune).
- **OGC geospatial (Simple Features / WKT / GeoParquet):** Sedona, SIS.
- **OpenTelemetry (OTLP):** SkyWalking (ingest); APISIX/ShenYu (export).
- **Jakarta EE / Servlet:** Tomcat, TomEE, MyFaces, Pluto; CDI via OpenWebBeans; JPA via OpenJPA; Validation via BVal.
- **OSGi:** Felix, Karaf, Aries (JVM); Celix (C/C++).
- **CloudEvents:** EventMesh.
- **DFDL (data format description):** Daffodil.
- **ODF / OOXML (office documents):** OpenOffice (ODF), POI (OOXML), PDFBox (PDF), FOP (XSL-FO→PDF).
- **WebDAV:** httpd (`mod_dav`), Subversion, Jackrabbit.

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
tags (TVM, Fory, DevLake → active; Amoro → incubating). Each entry then gained the six
composition fields (**Interfaces, Needs, Pairs with, Alternatives, Standards, Maturity**) that
power [Part 6](#part-6--composition--interoperability-guide). Descriptions, functions, patterns,
Interfaces/Needs/Standards reflect each project's documented design; *Alternatives*, *Maturity*,
and the Part 6 "pick-when" guidance are editorial judgment calls. The **status** tag is still the
field most likely to drift — re-verify against the sources above.

*With the reconciliation additions, this inventory now carries a card (or table row) for **every
active top-level project** in the ASF's live directory, plus the Commons/Logging sub-module
families, the 24 current podlings, and the notable Attic projects. It remains pattern-oriented
rather than a literal dump of all 1,497 DOAP entries and their sub-modules; sub-projects are
represented through their parent project's entry.*





