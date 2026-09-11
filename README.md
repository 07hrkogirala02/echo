# Echo

## Every deployment leaves an echo.

**Echo is a Release Impact Intelligence platform that investigates what a software deployment actually changed across system, product, and business signals.**

[🚀 Live Demo](https://echo-frontend-1025625447297.us-central1.run.app) . [🚀 Medium Post](https://medium.com/@Harika_Ogirala/echo-every-deployment-leaves-an-echo-d04f7615a5cc) 

---

## The problem

A deployment succeeds.

The CI/CD pipeline is green.

The release is live.

Then something changes.

API latency increases.
Error rates rise.
Payment failures increase.
Users abandon checkout.
Revenue starts declining.

The difficult question isn't:

> **"What happened?"**

Modern engineering teams already have monitoring, observability, analytics and dashboards for that.

The difficult question is:

> **"Did the deployment actually cause it?"**

Echo is designed to investigate that question.

---

## What is Echo?

Echo connects a deployment with its downstream impact across three layers:

```text
                 DEPLOYMENT
                      │
                      ▼
              ┌───────────────┐
              │ System Impact │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Product Impact│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │Business Impact│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    Evidence   │
              │     Engine    │
              └───────┬───────┘
                      │
                      ▼
              Evidence Score
                      │
                      ▼
                Investigation
```

Instead of simply showing that a metric changed, Echo evaluates:

* How significant was the change?
* When did it happen relative to the deployment?
* Did multiple layers tell the same story?
* Were there competing events?
* How strong is the evidence connecting the deployment to the impact?

---

# Why Echo?

Production incidents rarely exist inside a single dashboard.

A deployment can create a chain of effects:

```text
Deployment
    ↓
Latency increases
    ↓
Errors increase
    ↓
Payment failures increase
    ↓
Checkout abandonment increases
    ↓
Conversion decreases
    ↓
Revenue decreases
```

Echo attempts to connect these signals into one investigation.

---

# Core capabilities

### 🔧 System Impact

Analyzes technical changes such as:

* API latency
* Error rate
* Payment failure rate
* Other deployment-related system metrics

### 📱 Product Impact

Analyzes user/product signals such as:

* Checkout abandonment
* Conversion
* Product behaviour

### 💰 Business Impact

Analyzes business outcomes such as:

* Revenue
* Business metric changes

### 🧠 Evidence Engine

Echo evaluates evidence using:

* Magnitude
* Temporal relationship
* Cross-layer consistency
* Directional consistency
* Competing events

The result is an **Evidence Score** and confidence classification.

---

# The key idea

## Correlation is not causation.

A metric changing after a deployment does not automatically mean the deployment caused it.

For example:

```text
09:55  Payment provider outage
10:00  Deployment
10:15  Payment failures increase
```

A simplistic system might blame the deployment.

Echo instead considers the payment-provider outage as a competing event and evaluates whether it provides a stronger explanation.

This is one of the core ideas behind the project:

> **Don't just look for evidence that supports the deployment. Look for evidence that challenges it too.**

---

# Example investigation

## DEP-4821 — Checkout V2

A production deployment of:

```text
Service:     checkout-service
Version:     v2.4.1
Feature:     Checkout V2
Environment: production
```

After the deployment, Echo identifies changes across multiple layers.

### System

| Metric               |    Before |     After |  Change |
| -------------------- | --------: | --------: | ------: |
| API latency          | 208.75 ms | 254.67 ms |  +22.0% |
| Error rate           |     0.85% |     1.68% | +97.39% |
| Payment failure rate |     2.05% |     3.07% | +49.59% |

### Business

Revenue changes from:

```text
₹4,200,000
      ↓
₹3,942,222
```

Approximately:

```text
-6.14%
```

### Evidence

```text
Evidence Score: 91.25
Confidence: VERY STRONG
```

The investigation finds strong temporal, cross-layer and directional consistency.

---

# Investigation logic

Echo's investigation engine follows this general process:

```text
Deployment
    ↓
Identify deployment timestamp
    ↓
Collect surrounding metrics
    ↓
Compare before vs after
    ↓
Measure magnitude
    ↓
Check temporal relationship
    ↓
Analyze system impact
    ↓
Analyze product impact
    ↓
Analyze business impact
    ↓
Check competing events
    ↓
Evaluate evidence
    ↓
Generate investigation result
```

---

# Architecture

```text
                         ECHO
                          │
                          ▼
                ┌──────────────────┐
                │    Frontend      │
                │   Web Application │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Backend API   │
                │      Python      │
                │     FastAPI      │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌──────────────┐     ┌──────────────┐
       │   BigQuery   │     │  AI / Gemini │
       │              │     │   (if enabled│
       │ Deployment   │     │    in build) │
       │ System       │     └──────────────┘
       │ Product      │
       │ Business     │
       └──────────────┘
```

The current application is deployed through **Render**.

---

# Technology

| Area           | Technology                        |
| -------------- | --------------------------------- |
| Frontend       | React / web frontend              |
| Backend        | Python                            |
| API            | FastAPI                           |
| Data           | Google BigQuery                   |
| Development    | AI-assisted / agentic development |
| Deployment     | Render                            |
| Source control | GitHub                            |

> Note: The exact AI/runtime services listed here should match the services actually used by the current implementation.

---

# Project structure

```text
echo/
│
├── frontend/
│   └── Web application
│
├── backend/
│   ├── investigations/
│   │   └── engine.py
│   └── API implementation
│
├── data/
│   └── Synthetic datasets
│
├── docs/
│   ├── architecture.md
│   ├── investigation-logic.md
│   └── demo.md
│
├── screenshots/
│   └── Product screenshots
│
├── scripts/
│   └── Data generation scripts
│
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

---

# Running Echo locally

## Prerequisites

You will need:

* Python 3.x
* Node.js
* npm
* Git
* A Google Cloud project if using BigQuery
* Appropriate Google Cloud credentials

---

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/echo.git
cd echo
```

---

## 2. Backend setup

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Add the required configuration.

Then start the backend:

```bash
uvicorn main:app --reload
```

---

## 3. Frontend setup

Open another terminal:

```bash
cd frontend

npm install
npm run dev
```

The frontend will then provide the local development URL.

---

# Data

Echo uses synthetic production-like data for demonstration.

The dataset includes signals representing:

```text
deployments
events
system metrics
product metrics
business metrics
```

This allows the project to reproduce realistic investigation scenarios without using confidential production data.

---

# Google Cloud

The data layer uses Google BigQuery.

The project contains an `echo_dataset` with investigation data used by the backend.

Before running the project locally, configure your Google Cloud credentials and project configuration according to the instructions in `docs/`.

---

# Deployment

The current application is deployed through Render.

The live application is available here:

**[Live Echo Application](YOUR_RENDER_URL)**

The deployed version demonstrates the complete investigation workflow without requiring the evaluator to configure the development environment.

---

# Demo scenario

For the quickest demonstration, investigate:

```text
DEP-4821
```

Recommended flow:

```text
DEP-4821
   ↓
Investigation
   ↓
System Impact
   ↓
Product Impact
   ↓
Business Impact
   ↓
Evidence
```

Look specifically for:

* API latency increase
* Error-rate increase
* Payment-failure increase
* Revenue impact
* Evidence Score
* Confidence classification

---

# Design principle

Echo is built around a simple principle:

> **Don't just show the signal. Connect the signals.**

Monitoring tells you what is happening.

Echo attempts to help explain how those changes relate to a deployment.

---

# Limitations

Echo is an investigation and decision-support system, not a mathematical proof of causality.

Its conclusions depend on:

* Data quality
* Metric coverage
* Temporal relationships
* Available events
* Evidence model assumptions

The Evidence Score represents the strength of the available evidence; it should not be interpreted as absolute causal certainty.

Human investigation and judgement remain important for high-impact production decisions.

---

# Future direction

Potential future capabilities include:

* Automated post-deployment monitoring
* More observability integrations
* CI/CD integrations
* Incident-management integrations
* Historical deployment comparison
* Release-risk scoring
* More sophisticated statistical causal analysis
* Automated incident narratives
* Human-approved rollback recommendations

The long-term vision is for Echo to become an intelligent layer between **deployment events and their real-world impact**.

---

# Built for Patchamomma 2026

Echo was built as part of **Patchamomma 2026**, exploring how Google Cloud, data, AI and rapid AI-assisted development can be combined to solve a practical engineering problem.

The project started with a simple question:

> **What does a deployment actually cause?**

It evolved into a working, deployed investigation platform.

---

# Author

**Harika Ogirala**

Product Designer · AI Products · B2B SaaS · Design Systems

---

# License

This project is open source under the MIT License.

See [LICENSE](LICENSE) for details.

---

## Every deployment leaves an echo.

### Echo helps you understand what that echo means.
