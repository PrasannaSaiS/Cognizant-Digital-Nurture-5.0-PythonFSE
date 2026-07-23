# Module 3: Database Integration — Student Course Registration System
This repository contains a comprehensive suite of database scripts and implementations developed for the Digital Nurture 5.0 Deep Skilling Program. The entire project is built around a single, cohesive, real-world scenario to demonstrate relational database engineering, query optimization, and performance tuning.

# Project Scenario
The core objective is to design, implement, and optimize a backend database engine for a college Student Course Registration System. The platform manages student enrollment tracking, course metrics, department budgeting, and staff assignments across multiple relational database environments (PostgreSQL / MySQL).Relational Database SchemaThe architecture relies on five closely integrated tables:

- **departments:** Tracks department names, budget allocations, and head of departments.
- **students:** Stores personal profiles, contact channels, and academic entry footprints.
- **courses:** Maintains unique alpha-numeric registry catalogs, course names, and credit metrics.
- **enrollments:** Connects students to specific courses with evaluation grades.
- **professors:** Manages instructor profiles, salary grades, and departmental tracking.

# Summary of Modules Covered
**[Hands-On 1] Schema Design & Core SQLDDL Implementation:**
- Baseline generation script constructing tables with PRIMARY KEY, UNIQUE, NOT NULL, and FOREIGN KEY constraints.
- Normalization Audit: Structured analytical review validating the data layer against 1NF, 2NF, and 3NF conditions.
- Schema Evolution: Operational safe alters implementing CHECK conditions and table renames without data mutation.

**[Hands-On 2] Writing SQL Queries - DML & AggregationsData Mutations:** 
- Seeding initial ledger rows and modifying records using standard INSERT, UPDATE, and DELETE commands.
- Relational Joins: Executing multi-table combinations (INNER JOIN, LEFT JOIN) to reveal missing relationships or track data flows.
- Aggregations & Grouping: Extracting analytical reports utilizing GROUP BY and HAVING filters on computed evaluation items.

**[Hands-On 3] Advanced SQL — Subqueries, Views & TransactionsSubqueries:** 
- Processing multi-tiered logic constraints with both nested non-correlated and correlated lookup queries.
- Database Views: Provisioning abstraction views to isolate calculated performance stats and exploring view mutability boundaries.
- Transaction Engine: Building programmatic validation functions, transfer operations, and fallback mechanisms using COMMIT, ROLLBACK, and SAVEPOINT bounds.

**[Hands-On 4] Query Optimization — Indexes & the N+1 Problem Execution Plan Diagnostics:** 
- Inspecting query bottlenecks using EXPLAIN to isolate sequential table scans.
- Indexing Strategies: Accelerating access latency by routing workflows through B-Tree, Composite, and targeted Conditional Partial Indexes.
- N+1 Anti-Pattern Remediation: Isolating programmatic loop inefficiencies and converting multi-trip network queries into a singular high-performance eager JOIN.
