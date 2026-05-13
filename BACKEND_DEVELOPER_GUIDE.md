# Backend Developer Guide

## Purpose

This document is a practical map of what a strong backend developer should know.
It is written from high level to low level so you can use it as a learning roadmap,
review checklist, and long-term reference.

Frontend excellence usually means things like rendering performance, memory leaks,
state correctness, bundle size, UX, and developer ergonomics.

Backend excellence is similar in spirit, but the focus shifts to:

- correctness under load
- data integrity
- security
- API contract reliability
- scalability
- observability
- failure handling
- maintainability over time

---

## 1. Core Backend Mindset

A strong backend developer thinks in terms of systems, not just endpoints.

Key mindset areas:

- The backend is a source of truth, not just a data pipe.
- Every request is part of a larger workflow.
- Data consistency matters more than short-term convenience.
- Security is default, not optional.
- Failures are normal and should be expected.
- Logs, metrics, and traces are part of the product.
- APIs are contracts. Breaking them carelessly causes real system damage.
- Performance is not only speed. It is also resource usage, scalability, and stability.

---

## 2. High-Level Architecture Knowledge

You should understand how to structure a backend beyond just writing route handlers.

### 2.1 Layers and Separation of Concerns

A healthy backend usually separates:

- router layer: HTTP request/response mapping
- controller/service layer: business logic
- data access layer: database queries and persistence
- domain/model layer: entities and contracts
- infrastructure layer: external integrations, caching, queues, storage

You should know:

- what logic belongs in routers vs services
- why database code should not be mixed into every endpoint
- how to avoid fat controllers and duplicated logic

### 2.2 Architectural Styles

You should understand when and why teams use:

- monoliths
- modular monoliths
- microservices
- event-driven systems
- background jobs / worker systems
- API gateways / BFFs

Do not blindly chase microservices. Most teams do better with a clean modular monolith until scale or organizational boundaries truly demand more.

### 2.3 Data Flow Thinking

Always think in workflows:

- request comes in
- validation happens
- authorization happens
- business logic runs
- database changes happen
- external systems may be called
- side effects may happen
- response returns
- logs/metrics capture the result

If you cannot clearly explain the workflow of an endpoint, the codebase is not yet well understood.

---

## 3. API Design Fundamentals

Backend developers must design APIs that are predictable, stable, and easy to integrate.

### 3.1 Request and Response Design

You should know how to design:

- clear request schemas
- consistent response shapes
- proper status codes
- pagination
- filtering and sorting
- error response structure
- backward-compatible changes

Good APIs are:

- explicit
- consistent
- well validated
- hard to misuse

### 3.2 REST and Beyond

You should understand:

- REST basics
- when GraphQL makes sense
- RPC-style APIs
- webhooks
- streaming responses
- SSE / WebSockets if needed

### 3.3 Validation

Validation should happen close to the input boundary.

Examples:

- request body validation
- query param validation
- path param validation
- enum/constant validation
- file type validation
- size and content limits

Principle:

- reject bad input early
- never trust frontend validation alone

### 3.4 API Versioning and Compatibility

You should know how to evolve APIs safely:

- additive changes are safer than breaking changes
- keep old clients in mind
- deprecate before removing
- document contract changes clearly

---

## 4. Authentication and Authorization

This is one of the most important backend areas.

### 4.1 Authentication

You should know:

- sessions vs JWT
- token expiry
- refresh tokens
- password hashing
- OAuth basics
- SSO concepts
- API keys for service-to-service auth

Never store plain text passwords.

You should understand:

- hashing
- salting
- bcrypt / argon2 style algorithms
- secure token creation and validation

### 4.2 Authorization

You should know the difference between:

- authentication: who are you
- authorization: what are you allowed to do

Common models:

- role-based access control
- permission-based access control
- resource-level authorization
- attribute-based access control

Important principle:

- authorization should be enforced on the backend even if the UI hides buttons

---

## 5. Data Modeling and Database Design

Backend quality depends heavily on data design.

### 5.1 Schema Design

You should know:

- entities and relationships
- normalization vs denormalization
- unique constraints
- foreign keys
- indexes
- nullable vs required fields
- enum-like controlled values
- audit fields like created_at and updated_at

### 5.2 Query Thinking

You should be able to reason about:

- why a query is slow
- when indexes help
- N+1 query problems
- filtering in database vs filtering in memory
- full table scans
- join cost
- pagination efficiency

### 5.3 Transactions

You must understand transactions deeply.

Topics:

- atomicity
- consistency
- isolation
- rollback behavior
- when to commit
- when to avoid partial writes

Principle:

- if multiple data changes must succeed together, they belong in a transaction

### 5.4 Migrations

You should know the difference between:

- schema migration
- data migration

Examples:

- add table
- add column
- rename field
- update old rows to new allowed values
- backfill missing data

You should learn proper migration tooling such as Alembic when working seriously with SQLAlchemy-based systems.

---

## 6. Business Logic and Domain Modeling

A mature backend developer does not scatter business rules everywhere.

You should know how to:

- centralize important rules
- avoid duplicating logic in multiple routes
- keep rules near the domain
- express invariants clearly

Examples of business rules:

- only admin can upload docs
- only certain roles can access certain files
- department must be one of fixed values
- a document must always have at least one allowed role

Good backend code makes these rules obvious.

---

## 7. Performance and Scalability

Backend performance is broader than “this endpoint feels fast.”

### 7.1 Resource Thinking

You should think about:

- CPU usage
- memory usage
- database load
- file I/O
- network I/O
- external API latency
- queue backlog

### 7.2 Common Performance Topics

You should know:

- connection pooling
- caching strategies
- batching
- streaming large responses
- avoiding repeated heavy computation
- background processing for slow tasks
- load shedding / timeouts / retries

### 7.3 Caching

Learn:

- when to cache
- cache invalidation basics
- local memory cache vs Redis
- stale data tradeoffs
- cache key design

### 7.4 Async vs Threads vs Workers

Important distinction:

- async is useful for I/O-bound work
- threads can help for blocking operations depending on runtime limitations
- workers/background jobs are better for long-running tasks

Know when to use:

- request-time execution
- background tasks
- job queue

---

## 8. Reliability and Failure Handling

Real backend systems fail in production. Good backend developers build for that reality.

You should know how to handle:

- timeouts
- retries
- partial failures
- unavailable external services
- malformed data
- duplicate requests
- race conditions
- file not found cases
- expired tokens

Best practices:

- fail loudly but safely
- return meaningful error messages
- log enough context to debug
- avoid exposing sensitive internals to clients
- define retry boundaries carefully

Important concept:

- idempotency

Examples:

- retried payment requests should not charge twice
- retried upload completion should not create duplicates if designed carefully

---

## 9. Security Fundamentals

Security is not a separate phase. It is backend engineering.

You should know the basics of:

- password hashing
- JWT/session security
- CORS
- CSRF concepts
- SQL injection prevention
- path traversal risks
- insecure file serving
- secret management
- rate limiting
- input sanitization where relevant
- safe logging
- access control bypass risks

Golden rules:

- never trust input
- never expose secrets in code or logs
- never rely on frontend-only restrictions
- never serve protected files publicly without access checks

---

## 10. Observability: Logs, Metrics, Traces

A backend that cannot be observed is hard to operate.

### 10.1 Logging

Know how to log:

- request id / correlation id
- route
- user or actor id where safe
- failure reason
- important state transitions

Avoid logging:

- passwords
- raw tokens
- highly sensitive PII unless absolutely necessary and approved

### 10.2 Metrics

Useful backend metrics include:

- request count
- latency
- error rate
- DB query timing
- queue depth
- cache hit rate
- memory usage
- CPU usage

### 10.3 Tracing

You should understand distributed tracing concepts even if you are not yet using them heavily.

---

## 11. Testing Strategy

Backend developers must know how to test beyond manual Postman testing.

### 11.1 Types of Tests

- unit tests
- integration tests
- API tests
- database tests
- authorization tests
- contract tests
- load/performance tests

### 11.2 What to Test

- happy path
- invalid inputs
- auth failures
- permission failures
- edge cases
- DB state changes
- migration logic
- retry and failure cases

### 11.3 Good Testing Habits

- test business rules, not just syntax
- test critical workflows end to end
- isolate external dependencies where needed
- avoid flaky tests
- ensure test data setup is explicit

---

## 12. Code Quality and Maintainability

A strong backend developer writes code that remains understandable after six months.

You should know how to:

- name functions clearly
- keep modules focused
- reduce duplication
- avoid hidden side effects
- keep public contracts stable
- prefer explicitness over cleverness
- refactor safely

Code review mindset:

- correctness first
- security second
- maintainability third
- style last

---

## 13. Background Jobs and Async Processing

Backend work often should not happen inside the request cycle.

You should know when to move work into:

- background tasks
- message queues
- workers
- scheduled jobs

Common examples:

- sending emails
- indexing documents
- generating reports
- calling slow third-party systems
- image or file processing

Important concerns:

- retries
- dead-letter handling
- duplicate processing
- monitoring job failures

---

## 14. File Handling and Storage

Since many backend systems work with uploads, you should know:

- safe file naming
- file type validation
- size limits
- content-type issues
- local disk vs object storage
- access control for files
- signed URLs vs protected endpoints
- cleanup of orphaned files

Very important:

- public static serving is not the same as protected file access

---

## 15. External Integrations

You should know how to integrate safely with:

- third-party APIs
- email providers
- payment systems
- LLM providers
- cloud storage
- internal microservices

Required knowledge:

- timeouts
- retries
- backoff
- circuit breaker ideas
- rate limits
- schema drift
- external error mapping

---

## 16. Deployment and Runtime Basics

Even if you are not a DevOps engineer, you should understand:

- environment variables
- config separation by environment
- dev vs staging vs prod differences
- process management
- health checks
- readiness/liveness concepts
- reverse proxy basics
- HTTPS basics
- container basics
- CI/CD basics

You should be able to answer:

- how does this service start
- what config does it need
- how does it fail
- how do we know it is healthy

---

## 17. Data Privacy and Compliance Awareness

Depending on the product, a backend developer should be aware of:

- personally identifiable information
- data retention
- auditability
- deletion workflows
- access logs
- principle of least privilege

You do not need to be a lawyer, but you should understand when the system handles sensitive data.

---

## 18. Practical Backend Review Checklist

When reviewing a backend feature, ask:

- Is the request validated properly?
- Is authentication correct?
- Is authorization enforced?
- Are database writes safe and consistent?
- Are errors handled cleanly?
- Are logs useful and safe?
- Is there risk of duplicate side effects?
- Are performance bottlenecks obvious?
- Are constants/enums centralized?
- Does the API contract stay consistent?
- Are tests covering the important cases?
- Could a malicious user misuse this endpoint?

---

## 19. Low-Level Topics Worth Knowing Over Time

As you grow from good to strong backend engineer, learn these deeper topics:

- HTTP internals
- TCP basics
- DNS basics
- TLS basics
- process and thread model
- connection pooling internals
- garbage collection basics
- memory profiling basics
- Linux process/resource basics
- database isolation levels
- index internals at a high level
- queue semantics
- eventual consistency
- CAP tradeoffs at a conceptual level

You do not need to master all of them immediately, but they become valuable as system complexity grows.

---

## 20. Recommended Learning Order

If you are already strong in frontend, this order works well for backend growth:

### Stage 1: Core App Development

- routing
- request/response models
- controllers/services
- CRUD operations
- SQLAlchemy basics
- authentication and authorization
- validation
- error handling

### Stage 2: Data and Correctness

- schema design
- indexing
- transactions
- migrations
- consistency rules
- background tasks

### Stage 3: Production Readiness

- logging
- metrics
- retries/timeouts
- caching
- file handling
- external integrations
- performance analysis

### Stage 4: Advanced Systems Thinking

- distributed systems basics
- queues and workers
- tracing
- scaling strategies
- system design
- security hardening

---

## 21. How to Think Like a Strong Backend Developer

When you build a feature, ask yourself:

- What are the inputs?
- What are the invariants?
- What data is read?
- What data is written?
- What happens if this fails halfway?
- Who is allowed to do this?
- What happens under concurrency?
- What happens with duplicate requests?
- What logs and metrics will help later?
- What will break if the contract changes?

That habit is the backend equivalent of frontend thinking about rerenders, stale state, memory leaks, and user interaction edge cases.

---

## 22. Final Summary

To be a strong backend developer, you should be good at five things at the same time:

- designing clean APIs
- protecting data and access
- keeping systems reliable under failure
- modeling data correctly
- building code that scales operationally and conceptually

If you keep improving in these dimensions, you move from "someone who can build endpoints" to "someone who can own backend systems".
