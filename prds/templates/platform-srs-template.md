# Platform SRS: <Platform Name>

**Version**: 0.1
**Date**: <YYYY-MM-DD>
**Author**: <Name / role>
**Status**: Draft | Approved | Active | Superseded
**Supersedes**: <prior SRS or "none">
**Architecture Reference**: <link to canonical architecture doc>

> A System Requirements Specification (SRS) describes the platform as a whole - what it is, what it does, and the contracts between its parts. Distinct from a feature PRD, which scopes a specific change. Use this template once per platform; revise rather than duplicate.

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Stakeholders](#2-stakeholders)
3. [System Overview](#3-system-overview)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [External Interfaces](#6-external-interfaces)
7. [Data Architecture](#7-data-architecture)
8. [Deployment Model](#8-deployment-model)
9. [Operational Requirements](#9-operational-requirements)
10. [Security and Compliance](#10-security-and-compliance)
11. [Quality Attributes](#11-quality-attributes)
12. [Constraints and Assumptions](#12-constraints-and-assumptions)
13. [Glossary](#13-glossary)

---

## 1. Purpose and Scope

### 1.1 Purpose

<What this SRS exists to specify. The audience and the decisions it informs.>

### 1.2 Scope

<What systems, services, and capabilities are covered. What's explicitly excluded.>

### 1.3 Definitions, Acronyms, Abbreviations

See [Section 13: Glossary](#13-glossary).

### 1.4 References

- <Reference 1>
- <Reference 2>

---

## 2. Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| <Engineering> | Implementer | Architecture clarity, maintainability |
| <Product> | Owner | Capability fit, roadmap alignment |
| <SRE / Ops> | Operator | Reliability, observability, runbooks |
| <Security> | Reviewer | Threat surface, controls |
| <Compliance> | Auditor | Regulatory fit |

---

## 3. System Overview

### 3.1 Context Diagram

<External actors, systems, and the platform's place among them.>

```
TODO: context diagram
```

### 3.2 Component Diagram

<Internal components, services, data stores, message buses.>

```
TODO: component diagram
```

### 3.3 Operating Modes

<Online vs batch, peak vs off-peak, degraded modes if applicable.>

---

## 4. Functional Requirements

Each functional requirement has a stable ID for cross-reference (e.g. `FR-1.1`).

### 4.1 <Capability Group 1>

- **FR-1.1** - The system SHALL <action> when <condition>.
- **FR-1.2** - The system SHALL <action> when <condition>.

### 4.2 <Capability Group 2>

- **FR-2.1** - TODO
- **FR-2.2** - TODO

---

## 5. Non-Functional Requirements

| ID | Category | Requirement | Target |
|---|---|---|---|
| NFR-1 | Availability | Uptime per service | 99.9% per quarter |
| NFR-2 | Latency | API p95 | < 200ms |
| NFR-3 | Throughput | Concurrent users | TODO |
| NFR-4 | Scalability | Headroom from peak | 3x |

---

## 6. External Interfaces

### 6.1 User Interfaces

<Web, mobile, API surfaces.>

### 6.2 System Interfaces

<Other systems consumed or provided.>

### 6.3 Hardware Interfaces

<If applicable.>

### 6.4 Communication Interfaces

<Protocols, message formats, versioning.>

---

## 7. Data Architecture

### 7.1 Data Model

<Entities, relationships, ownership boundaries.>

### 7.2 Storage Layout

| Store | Purpose | Owner |
|---|---|---|
| TODO | TODO | TODO |

### 7.3 Data Lifecycle

<Creation, retention, archive, deletion. Backups and recovery.>

---

## 8. Deployment Model

### 8.1 Environments

| Environment | Purpose | Branch / tag |
|---|---|---|
| local-dev | Engineer workstations | <branch> |
| develop | Integration | <branch> |
| staging | Pre-production validation | <branch> |
| production | Live traffic | <branch> |

### 8.2 Multi-Region / Multi-Cloud

<Region strategy, failover, data residency.>

### 8.3 Configuration Management

<How configuration is defined, where it lives, how it propagates.>

---

## 9. Operational Requirements

### 9.1 Monitoring

<Metrics, logs, traces. Required dashboards.>

### 9.2 Alerting

<SLO-driven alerts. On-call rotation.>

### 9.3 Runbooks

<Pointers to runbooks for common operational tasks.>

### 9.4 Capacity Planning

<How capacity is forecast and provisioned.>

---

## 10. Security and Compliance

### 10.1 Authentication

### 10.2 Authorization

### 10.3 Encryption

<At rest, in transit.>

### 10.4 Audit Logging

### 10.5 Compliance Frameworks

<SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, SOX as applicable.>

### 10.6 Threat Model

<Link to canonical threat model doc.>

---

## 11. Quality Attributes

- **Reliability**: <fault tolerance, recovery>
- **Maintainability**: <code health, modular boundaries>
- **Portability**: <vendor / cloud lock-in posture>
- **Usability**: <UX targets>
- **Testability**: <coverage and test environment requirements>

---

## 12. Constraints and Assumptions

### 12.1 Constraints

- <Regulatory, technical, organizational constraints>

### 12.2 Assumptions

- <Assumptions about traffic, growth, operating environment>

---

## 13. Glossary

| Term | Definition |
|---|---|
| TODO | TODO |
