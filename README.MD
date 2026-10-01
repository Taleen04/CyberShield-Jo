# CyberShield JO

> An intelligent cybersecurity platform designed to help users in Jordan detect, understand, and report digital fraud, phishing attacks, and online scams.

CyberShield JO is a mobile-based cybersecurity application developed to provide accessible threat analysis for **URLs, text messages, and phone numbers**. The platform combines machine-learning-assisted analysis, threat databases, and community reporting to help users identify potentially malicious content and make safer decisions online.

Developed as part of the **Crown Prince Award for the Best Government Services Application**.

---

## Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Key Features](#key-features)
* [How It Works](#how-it-works)
* [System Architecture](#system-architecture)
* [Technology Stack](#technology-stack)
* [Project Methodology](#project-methodology)
* [Development Plan](#development-plan)
* [Requirements](#requirements)
* [Testing](#testing)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
* [Limitations](#limitations)
* [Future Work](#future-work)
* [Team](#team)
* [Acknowledgments](#acknowledgments)
* [References](#references)
* [License](#license)

---

## Overview

The rapid growth of online banking, e-commerce, social media, and digital communication has increased users' exposure to phishing, fraud, malicious links, and scam messages.

Many users have difficulty determining whether an unfamiliar message, website, or phone number is legitimate. Existing tools are often specialized for a single type of threat, require technical knowledge, or do not provide an accessible mechanism for community reporting.

**CyberShield JO** addresses these challenges through a unified platform that allows users to:

* Analyze suspicious URLs.
* Analyze potentially fraudulent text messages.
* Check suspicious phone numbers.
* Receive an understandable risk classification.
* Review previous scans.
* Report suspicious content.
* Track submitted reports.
* Access cybersecurity awareness information.
* Access Cybercrime Unit contact information.

The platform also allows administrators to review community reports, verify threats, manage the threat database, and monitor system activity.

---

## Problem Statement

Users in Jordan increasingly interact with digital services and communications that may expose them to cyber fraud and social engineering.

CyberShield JO focuses on several challenges:

* Difficulty distinguishing legitimate and malicious content.
* Limited cybersecurity awareness among non-technical users.
* Lack of accessible tools for validating suspicious content.
* Fragmented solutions that address only specific threat types.
* Limited community-driven mechanisms for reporting and sharing threat information.
* Difficulty identifying suspicious communications before interacting with them.

CyberShield JO provides a single platform for **threat analysis, reporting, awareness, and community protection**.

---

## Key Features

### Threat Analysis

#### URL Analysis

Users can submit a URL for analysis. The system validates the input and evaluates it using available threat-detection mechanisms and verified threat information.

#### Text Message Analysis

Users can submit suspicious SMS or other text messages for analysis.

The system can:

* Detect the language of the message.
* Translate Arabic content when required.
* Extract URLs contained within the message.
* Analyze the message for potential scam indicators.
* Produce a unified risk classification.

#### Phone Number Analysis

Users can check suspicious phone numbers against administrator-verified reports and available threat information.

#### Unified Risk Assessment

Analysis results are presented using three risk categories:

| Risk Level     | Description                                                                         |
| -------------- | ----------------------------------------------------------------------------------- |
| **Safe**       | No significant indicators of malicious activity were identified.                    |
| **Suspicious** | Indicators were identified that require caution or further verification.            |
| **High Risk**  | Strong indicators suggest that the content may be malicious, fraudulent, or unsafe. |

Each result is accompanied by an explanation to help users understand why the content received its classification.

---

### User Features

* **Account Registration** — Create an account using an email address and password.
* **Email Verification** — Verify account ownership through email confirmation.
* **Secure Authentication** — Protected access using JWT-based authentication and secure password hashing.
* **Scan History** — Review previous analysis results across sessions and devices.
* **Report Suspicious Content** — Submit potentially malicious URLs, messages, or phone numbers for review.
* **Report Tracking** — Monitor the status of submitted reports.
* **Result Sharing** — Share threat information with others to help increase awareness.
* **Cybersecurity Awareness** — Access educational content and security recommendations.
* **Cybercrime Unit Directory** — Access relevant contact information for reporting cybercrime and seeking assistance.
* **Application Settings** — Manage supported application preferences such as language, theme, and notifications.

---

### Reporting System

CyberShield JO incorporates community reporting into the threat-detection workflow.

Users can submit suspicious content either:

1. Directly after receiving an analysis result.
2. Manually through the reporting interface.

Submitted reports can progress through statuses such as:

```text
Under Review
     │
     ├──► Safe
     │
     └──► Verified Scam
              │
              ▼
       Community Database
```

Verified threats can subsequently be added to the platform's threat database.

---

### Administration

Administrators have access to protected management functionality for:

* Reviewing user reports.
* Validating submitted threats.
* Updating report statuses.
* Adding verified threats to the blacklist.
* Reviewing recent scans.
* Monitoring aggregate system activity.
* Managing administrative functionality through role-based access control.

Administrative authorization is enforced at the API level.

---

## How It Works

The general analysis workflow is:

```text
┌─────────────────────┐
│     User Input      │
│ URL / Text / Phone  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Input Validation  │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│      Threat Analysis         │
│                              │
│  URL → Threat Analysis       │
│  Text → NLP / URL Extraction │
│  Phone → Verified Reports    │
└──────────┬───────────────────┘
           │
           ▼
┌─────────────────────┐
│ Risk Classification │
│                     │
│ Safe / Suspicious   │
│ / High Risk         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Explanation + Result│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Scan History      │
└─────────────────────┘
```

### URL Analysis

1. The user submits a URL.
2. The system validates the URL.
3. The system checks available verified threat information.
4. Additional analysis is performed where applicable.
5. The system determines the resulting risk classification.
6. The result is returned with an explanation.
7. The scan is stored in the user's history.

### Text Analysis

1. The user submits a text message.
2. The system detects the message language.
3. Arabic content can be translated for analysis where required.
4. URLs are extracted from the message.
5. The text and extracted URLs are analyzed.
6. The results are combined into a unified risk assessment.
7. The scan is stored in the user's history.

### Phone Number Analysis

1. The user submits a phone number.
2. The number is validated and normalized.
3. The system checks available verified reports.
4. The result is returned with the corresponding risk classification.
5. The scan is stored in the user's history.

---

## System Architecture

CyberShield JO follows a layered architecture centered around a **FastAPI backend**.

```text
┌─────────────────────────────────────────────────────┐
│                  Mobile Application                 │
│                  Android / Mobile UI                │
└──────────────────────────┬──────────────────────────┘
                           │
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────┐
│                    FastAPI Backend                   │
│                                                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────────┐ │
│  │    Auth    │ │    Scan    │ │     Report     │ │
│  │   Router   │ │   Router   │ │     Router     │ │
│  └────────────┘ └────────────┘ └────────────────┘ │
│                                                     │
│  ┌────────────────────────────────────────────────┐ │
│  │              Service Layer                    │ │
│  │ Auth │ Scan │ Report │ Administration         │ │
│  └────────────────────────────────────────────────┘ │
└───────────────┬─────────────────┬───────────────────┘
                │                 │
                ▼                 ▼
       ┌────────────────┐  ┌──────────────────┐
       │ ML / Analysis  │  │   PostgreSQL     │
       │    Services    │  │   Neon Cloud     │
       └────────────────┘  └──────────────────┘
```

### Backend Layers

| Layer             | Responsibility                           |
| ----------------- | ---------------------------------------- |
| **API / Routers** | Handles HTTP requests and responses      |
| **Schemas**       | Defines request and response validation  |
| **Services**      | Contains application and business logic  |
| **Models**        | Represents database entities             |
| **Core**          | Configuration and security functionality |
| **ML**            | Machine-learning and analysis components |

This separation allows the system to keep API handling, business logic, persistence, and analysis functionality independently organized.

---

## Technology Stack

### Backend

| Technology           | Purpose                         |
| -------------------- | ------------------------------- |
| **FastAPI**          | REST API framework              |
| **Uvicorn**          | ASGI server                     |
| **SQLAlchemy 1.4**   | Object-relational mapping       |
| **Alembic**          | Database migrations             |
| **PostgreSQL**       | Application database            |
| **Neon**             | Cloud PostgreSQL infrastructure |
| **python-jose**      | JWT authentication              |
| **passlib + bcrypt** | Password hashing                |
| **slowapi**          | API rate limiting               |
| **loguru**           | Application logging             |

### Machine Learning & Analysis

| Technology           | Purpose                                 |
| -------------------- | --------------------------------------- |
| **scikit-learn**     | Machine-learning training and inference |
| **pandas**           | Data processing                         |
| **NumPy**            | Numerical processing                    |
| **Hugging Face Hub** | Model hosting and retrieval             |
| **NLTK**             | Natural language processing             |
| **langdetect**       | Language detection                      |
| **deep-translator**  | Arabic-to-English translation           |
| **tldextract**       | Domain extraction and analysis          |
| **phonenumbers**     | Phone number validation                 |
| **urlextract**       | URL extraction from text                |

### Mobile Development

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| **Android Studio** | Android application development |
| **Figma**          | UI/UX design                    |

### DevOps & Development Tools

| Technology                | Purpose                           |
| ------------------------- | --------------------------------- |
| **Docker**                | Containerization                  |
| **Google Cloud Platform** | Cloud infrastructure              |
| **GitHub**                | Version control and collaboration |
| **Visual Studio Code**    | Development environment           |
| **Draw.io**               | Architecture and system diagrams  |

### Testing

| Technology         | Purpose                   |
| ------------------ | ------------------------- |
| **pytest**         | Automated testing         |
| **pytest-asyncio** | Asynchronous test support |
| **pytest-cov**     | Code coverage             |
| **httpx**          | HTTP/API testing          |

---

## Project Methodology

### Scrum

CyberShield JO was developed using an iterative **Scrum-based development process**.

Development was divided into four two-week sprints, allowing the team to incrementally implement functionality, test the system, identify issues, and incorporate feedback.

The development process emphasized:

* Incremental delivery.
* Continuous testing.
* Regular feedback.
* Early identification of defects.
* Collaborative development.
* Progressive integration of system components.

### Feasibility Study

The project was evaluated using the **TEOS feasibility framework**.

| Aspect          | Assessment                                                            |
| --------------- | --------------------------------------------------------------------- |
| **Technical**   | Feasible using available technologies and development tools           |
| **Economic**    | Low-cost implementation using open-source and affordable technologies |
| **Operational** | Designed to be accessible to both technical and non-technical users   |
| **Schedule**    | Designed to be completed within the planned development period        |

### Project Estimation

| Metric                     | Estimate   |
| -------------------------- | ---------- |
| Unadjusted Function Points | 135        |
| Adjusted Function Points   | 111        |
| Estimated Person-Hours     | 2,220      |
| Estimated Total Cost       | $6,672 USD |

---

## Development Plan

### Sprint 1 — Core System & Authentication

**Duration:** 2 weeks

**Goal:** Establish the application's core user and authentication functionality.

| ID    | User Story                                            |
| ----- | ----------------------------------------------------- |
| US-01 | Register an account with email and password           |
| US-02 | Verify an email address through a confirmation link   |
| US-03 | Log in with credentials and maintain a secure session |

### Sprint 2 — Threat Detection & Analysis

**Duration:** 2 weeks

**Goal:** Implement the core threat-analysis functionality.

| ID    | User Story                             |
| ----- | -------------------------------------- |
| US-04 | Access scan history across devices     |
| US-05 | Analyze URLs for safety                |
| US-06 | Analyze text messages and extract URLs |

### Sprint 3 — Reporting & User Experience

**Duration:** 2 weeks

**Goal:** Implement reporting functionality and improve the analysis experience.

| ID      | User Story                                      |
| ------- | ----------------------------------------------- |
| US-07   | Analyze phone numbers                           |
| US-08   | View unified risk results                       |
| US-09   | Keep the application responsive during analysis |
| US-10-A | Report suspicious content after analysis        |
| US-10-B | Submit reports manually                         |

### Sprint 4 — Administration & System Enhancement

**Duration:** 2 weeks

**Goal:** Complete administrative functionality and supporting features.

| ID    | User Story                               |
| ----- | ---------------------------------------- |
| US-11 | Track submitted reports                  |
| US-12 | Review and update reports                |
| US-13 | View recent scans                        |
| US-14 | Access the administrative panel          |
| US-15 | Update report statuses                   |
| US-16 | Add verified reports to the blacklist    |
| US-17 | Monitor system activity                  |
| US-18 | Display cybersecurity awareness messages |
| US-19 | Provide Cybercrime Unit information      |
| US-20 | Maintain cross-platform consistency      |

---

## Requirements

### Functional Requirements

| ID   | Requirement                                                   | Priority |
| ---- | ------------------------------------------------------------- | -------- |
| FR01 | Allow users to enter SMS, phone numbers, or URLs for analysis | High     |
| FR02 | Analyze submitted inputs for potential threats                | High     |
| FR03 | Display analysis results with a risk level and explanation    | High     |
| FR04 | Classify results as Safe, Suspicious, or High Risk            | High     |
| FR05 | Allow users to report suspicious content                      | High     |
| FR06 | Allow users to create and view reports with their status      | High     |
| FR07 | Allow users to share results and alert others                 | Medium   |
| FR08 | Allow users to access emergency support information           | High     |
| FR09 | Allow users to view recent checks and scan history            | Medium   |
| FR10 | Provide cybersecurity awareness information                   | Medium   |
| FR11 | Allow users to manage application settings                    | Medium   |
| FR12 | Provide navigation between application sections               | Medium   |
| FR13 | Display support and contact information                       | Low      |

### Non-Functional Requirements

| ID   | Requirement                                        | Priority |
| ---- | -------------------------------------------------- | -------- |
| NF01 | Return analysis results within a few seconds       | High     |
| NF02 | Maintain high availability                         | High     |
| NF03 | Provide a simple and user-friendly interface       | High     |
| NF04 | Protect user data from unauthorized access         | High     |
| NF05 | Operate consistently without unexpected failures   | High     |
| NF06 | Support increasing numbers of users and data       | Medium   |
| NF07 | Be maintainable and easy to update                 | Medium   |
| NF08 | Support different mobile devices and screen sizes  | Medium   |
| NF09 | Respond quickly to user interactions               | High     |
| NF10 | Store and process user data securely               | High     |
| NF11 | Remain accessible to different categories of users | Medium   |

---

## Testing

CyberShield JO uses an automated testing strategy centered around **pytest**.

Testing was organized into multiple levels:

1. **API Integration Testing** — Tests the primary FastAPI endpoints.
2. **Service Testing** — Tests business logic independently where applicable.
3. **Machine Learning Testing** — Tests analysis components with isolated test cases and mocks.
4. **Security Testing** — Verifies authentication and access control behavior.

### Test Results

| Metric           | Result           |
| ---------------- | ---------------- |
| Total Tests      | **65**           |
| Passed           | **65**           |
| Failed           | **0**            |
| Runtime          | **8.23 seconds** |
| Overall Coverage | **52%**          |

### API Coverage

| Module                      | Coverage |
| --------------------------- | -------- |
| `app/api/routers/auth.py`   | **100%** |
| `app/api/routers/scan.py`   | **100%** |
| `app/api/routers/report.py` | **100%** |
| Service Layer               | Partial  |
| ML Modules                  | Partial  |

The lower coverage of the service and ML layers was identified as an area for future test expansion.

### Security Testing

Security-related tests verify:

* Authentication requirements for protected endpoints.
* Rejection of missing credentials.
* Rejection of invalid credentials.
* Access-control behavior.
* Protected administrative routes.
* API-level authorization.

### Testing Model

The project followed a **V-Model testing structure**:

```text
Requirements ─────────────────────────► Acceptance Testing
     │                                        ▲
     ▼                                        │
System Design ────────────────────────► System Testing
     │                                        ▲
     ▼                                        │
Architecture Design ──────────────────► Integration Testing
     │                                        ▲
     ▼                                        │
Module Design ────────────────────────► Unit Testing
     │                                        ▲
     ▼                                        │
              Implementation ─────────────────┘
```

---

## Project Structure

```text
cybershield-jo/
│
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── scan.py
│   │       ├── report.py
│   │       └── admin.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── report.py
│   │   └── scan.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── report.py
│   │   └── scan.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── scan_service.py
│   │   ├── report_service.py
│   │   └── admin_service.py
│   │
│   └── ml/
│       ├── text_classifier.py
│       ├── url_analyzer.py
│       └── preprocessing.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_scan.py
│   ├── test_report.py
│   └── conftest.py
│
├── alembic/
│   └── ...
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

The backend requires:

* Python 3.x
* PostgreSQL-compatible database
* Git
* Docker *(optional)*

The mobile application requires:

* Android Studio
* Android SDK
* A compatible Android device or emulator

### Clone the Repository

```bash
git clone <repository-url>
cd cybershield-jo
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file based on the provided template:

```bash
cp .env.example .env
```

Configure the required database, authentication, and external-service settings.

> Do not commit `.env` or other files containing secrets to version control.

### Run Database Migrations

```bash
alembic upgrade head
```

### Start the Backend

```bash
uvicorn app.main:app --reload
```

FastAPI provides interactive API documentation through its automatically generated Swagger/OpenAPI interface.

> The exact commands and environment variables may vary depending on the deployment configuration.

---

## Limitations

CyberShield JO is a project prototype and has several limitations:

* The detection system cannot identify every existing or newly emerging scam.
* Some detection mechanisms rely on predefined patterns, rules, or available threat information.
* Access to real-time external threat-intelligence sources is currently limited.
* The system has not yet been evaluated with a large-scale production user base.
* Machine-learning and analysis components require further optimization.
* Some features require additional validation and refinement before production deployment.
* Detection results should be treated as guidance rather than an absolute guarantee that content is safe or malicious.

---

## Future Work

Future development may include:

### Advanced Machine Learning

* Improve model accuracy.
* Reduce false positives and false negatives.
* Expand training datasets.
* Evaluate additional classification approaches.
* Improve Arabic-language threat detection.

### Threat Intelligence

* Integrate additional external threat-intelligence providers.
* Add real-time threat feeds.
* Expand the verified threat database.
* Improve automated threat correlation.

### Platform Expansion

* Develop a complete web-based administrative dashboard.
* Expand multilingual support.
* Improve accessibility.
* Support additional mobile platforms where applicable.

### Scalability

* Optimize backend performance.
* Improve database scalability.
* Introduce additional caching and asynchronous processing where appropriate.
* Conduct large-scale performance and load testing.

### Partnerships

* Establish partnerships with cybersecurity organizations and relevant institutions.
* Improve mechanisms for continuously updating verified threat information.
* Explore integration opportunities with government and cybersecurity services.

---

## Team

### Students

* **Taleen Khalid Fawzi Abo-Khas**
* **Abdalrahman Omar Ibrahim Obeid**
* **Tasneem Zayed Salman Abu Snaineh**

### Supervisor

**Dr. Moath Tarawneh**

### Institution

**The World Islamic Sciences and Education University**
Faculty of Information Technology

---

## Acknowledgments

We would like to express our sincere gratitude to everyone who contributed to the development of CyberShield JO.

Special thanks to **Dr. Moath Tarawneh**, our project supervisor, for his guidance, continuous support, and valuable feedback throughout the development of the project.

We also thank the **World Islamic Sciences and Education University** and the **Faculty of Information Technology** for providing the academic environment, resources, and knowledge that supported the development of this project.

Our appreciation also goes to the **Cybercrime Unit** for their cooperation and support during our field visit and requirements-gathering activities.

Finally, we thank all members of the project team for their dedication, collaboration, and contribution throughout the development process.

---

## References

* **Cybercrime Unit Visit.** (2026, April). Field visit to the Cybercrime Unit – Jordan: observations on cyber fraud cases and investigation practices.
* **National Cyber Security Center (NCSC).** (2026). Meeting notes and consultation session with the National Cyber Security Center – Jordan on cyber threats and online fraud awareness.
* Additional academic and technical publications concerning phishing, online fraud, cybersecurity awareness, and machine-learning-based threat detection.

---

## License

This project was developed as part of the **Crown Prince Award for the Best Government Services Application**.

---

<div align="center">

**CyberShield JO**

*Protecting Jordan's Digital Community*

</div>
