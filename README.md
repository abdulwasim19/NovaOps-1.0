# 🚀 NovaOps 1.0

> **A Cloud & DevOps Operations Dashboard for managing projects, infrastructure, deployments, and operational resources from a centralized platform.**

NovaOps is a full-stack **Cloud & DevOps Operations Dashboard** designed to provide a centralized interface for managing infrastructure resources and monitoring operational information.

The project is being developed as a practical learning and portfolio project to understand how modern backend applications, databases, infrastructure concepts, and DevOps workflows work together in a real-world environment.

---

## 📌 What is NovaOps?

In real-world software and cloud environments, teams manage multiple projects, servers, deployments, and infrastructure resources.

Managing these resources separately can become difficult as the infrastructure grows.

**NovaOps aims to solve this problem by providing a centralized operations dashboard where users can:**

* Manage projects
* Register and manage infrastructure servers
* Track server information
* Monitor operational statistics
* Manage resources through a web interface
* Establish relationships between projects and infrastructure
* Eventually integrate cloud and DevOps automation

The long-term goal is to evolve NovaOps into a practical **Cloud & DevOps Operations Platform**.

---

# 🎯 Why NovaOps?

Modern applications depend heavily on cloud infrastructure and DevOps practices.

A development team may have:

```text
Multiple Projects
       ↓
Multiple Servers
       ↓
Cloud Infrastructure
       ↓
Deployments
       ↓
Monitoring
       ↓
Logs & Health
```

Without centralized management, handling these resources becomes difficult.

NovaOps is designed to provide a single dashboard for these operational activities.

### The main objectives are:

* Centralized infrastructure management
* Better visibility into resources
* Simplified server management
* Understanding backend development
* Practicing database design
* Learning cloud infrastructure concepts
* Applying DevOps principles
* Building a production-style portfolio project

---

# ✨ Current Features

## 📊 Dashboard

NovaOps provides a centralized dashboard containing important operational statistics such as:

* Total Projects
* Total Servers
* Deployment information
* System health
* Recently created projects

The dashboard provides a quick overview of the infrastructure environment.

---

## 📁 Project Management

NovaOps currently supports complete project management.

### Available operations:

* Create project
* View projects
* Edit project
* Delete project
* View project status
* View project descriptions

Projects are stored in the SQLite database through SQLAlchemy.

---

## 🖥️ Server Management

NovaOps provides infrastructure server management.

Each server can contain information such as:

* Server name
* IP address
* Cloud provider
* Region
* Server status

### Server operations:

* Add server
* View servers
* Edit server
* Delete server

Supported infrastructure providers currently include:

* AWS
* Azure
* GCP
* On-Premise

---

# 🏗️ Project Architecture

NovaOps currently follows a simple full-stack web application architecture:

```text
                ┌──────────────────────┐
                │       Browser        │
                │   HTML + CSS + Jinja │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │      Flask App       │
                │      app.py          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Flask-SQLAlchemy    │
                │    ORM / Models      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │       SQLite         │
                │      Database        │
                └──────────────────────┘
```

---

# 🛠️ Technologies Used

## Backend

### Python

Python is used as the primary programming language.

It is responsible for:

* Application logic
* Routes
* Database operations
* Form processing
* Server management
* Business logic

---

### Flask

Flask is the web framework used to build the NovaOps backend.

It handles:

* HTTP requests
* Routing
* Rendering templates
* Form submissions
* Application structure

---

### Flask-SQLAlchemy

Flask-SQLAlchemy is used as the ORM layer.

Instead of writing raw SQL for every database operation, SQLAlchemy allows NovaOps to work with Python models.

Example:

```python
server = Server(
    name="Production Server",
    ip_address="192.168.1.10",
    provider="AWS",
    region="ap-south-1",
    status="Running"
)
```

---

## Frontend

### HTML

HTML provides the structure of NovaOps pages.

It is used for:

* Forms
* Tables
* Cards
* Navigation
* Dashboard components

### CSS

CSS is used to create the NovaOps interface and provide:

* Layout
* Responsive design
* Buttons
* Cards
* Tables
* Forms
* Hover effects
* Status indicators

### Jinja2

Jinja2 is Flask's template engine.

It allows dynamic Python data to be displayed inside HTML.

For example:

```html
{{ server.name }}
```

and:

```html
{% for server in servers %}
```

---

## Database

### SQLite

SQLite is currently used as the database for NovaOps.

It stores:

* Projects
* Servers
* Project information
* Server information

SQLite is useful during development because it is lightweight and requires no separate database server.

As NovaOps grows, the project can be migrated to a production database such as:

* PostgreSQL
* MySQL

---

## Development Tools

### Git

Git is used for version control.

It allows NovaOps development to be tracked through meaningful commits.

Example:

```text
Complete server management CRUD
```

### GitHub

GitHub is used to:

* Store the source code
* Track development
* Maintain project history
* Share the project
* Build a professional portfolio

### VS Code

Visual Studio Code is used as the primary development environment.

---

# 📂 Project Structure

```text
NovaOps-1.0/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── projects.html
│   ├── new_project.html
│   ├── edit_project.html
│   ├── servers.html
│   ├── new_server.html
│   └── edit_server.html
│
├── static/
│   └── css/
│       └── style.css
│
└── venv/
```

---

# 🗄️ Current Database Models

## Project

```text
Project
├── id
├── name
├── description
└── status
```

## Server

```text
Server
├── id
├── name
├── ip_address
├── provider
├── region
└── status
```

The next stage of NovaOps will establish a proper relationship between these models.

---

# 🔄 CRUD Operations

NovaOps follows the fundamental CRUD pattern:

```text
Create
   ↓
Read
   ↓
Update
   ↓
Delete
```

### Projects

| Operation | Status |
| --------- | ------ |
| Create    | ✅      |
| Read      | ✅      |
| Update    | ✅      |
| Delete    | ✅      |

### Servers

| Operation | Status |
| --------- | ------ |
| Create    | ✅      |
| Read      | ✅      |
| Update    | ✅      |
| Delete    | ✅      |

---

# ☁️ Cloud & DevOps Direction

NovaOps is designed to go beyond a basic Flask CRUD application.

The long-term vision is to integrate real Cloud and DevOps functionality.

Potential integrations include:

### Cloud

* AWS EC2
* AWS S3
* AWS RDS
* AWS VPC
* AWS CloudWatch
* AWS IAM

### DevOps

* Docker
* Kubernetes
* Terraform
* CI/CD
* GitHub Actions
* Infrastructure automation
* Deployment automation

### Monitoring

* Server health
* CPU utilization
* Memory usage
* Disk usage
* Availability
* Application health
* Logs

---

# 🗺️ Development Roadmap

## Phase 1 — Foundation

* [x] Flask application
* [x] Dashboard
* [x] Project CRUD
* [x] Server CRUD
* [x] SQLite database
* [x] SQLAlchemy ORM
* [x] Git/GitHub integration

## Phase 2 — Infrastructure Relationships

* [ ] Project ↔ Server relationship
* [ ] Foreign keys
* [ ] Server assignment to projects
* [ ] Project infrastructure view

## Phase 3 — Deployment Management

* [ ] Deployment model
* [ ] Deployment history
* [ ] Deployment status
* [ ] Deployment statistics
* [ ] Deployment dashboard

## Phase 4 — Monitoring

* [ ] Server health monitoring
* [ ] Resource utilization
* [ ] Health indicators
* [ ] Logs
* [ ] Monitoring dashboard

## Phase 5 — Cloud Integration

* [ ] AWS integration
* [ ] EC2 resource discovery
* [ ] Cloud resource information
* [ ] Cloud monitoring
* [ ] Infrastructure synchronization

## Phase 6 — DevOps Automation

* [ ] Docker integration
* [ ] CI/CD pipelines
* [ ] GitHub Actions
* [ ] Terraform integration
* [ ] Automated deployments

## Phase 7 — Production Improvements

* [ ] User authentication
* [ ] Role-based access control
* [ ] API layer
* [ ] PostgreSQL
* [ ] Application logging
* [ ] Error handling
* [ ] Security improvements
* [ ] Production deployment

---

# 🧠 What I Am Learning Through NovaOps

NovaOps is not only a software project. It is being developed to gain practical experience across multiple areas of software engineering and DevOps.

### Programming

* Python
* Object-Oriented Programming
* Functions
* Exception handling
* Modules
* Application structure

### Backend Development

* Flask
* Routing
* HTTP methods
* Forms
* Templates
* CRUD operations

### Database

* SQL
* SQLite
* ORM
* SQLAlchemy
* Database models
* Foreign keys
* Relationships

### Cloud

* AWS
* EC2
* VPC
* IAM
* RDS
* Infrastructure concepts

### DevOps

* Git
* GitHub
* Docker
* CI/CD
* Infrastructure as Code
* Automation

---

# 💡 Project Vision

The ultimate goal of NovaOps is to evolve from a simple infrastructure management dashboard into a practical **Cloud & DevOps Operations Platform**.

The vision is:

```text
                    NOVAOPS
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Projects       Servers       Deployments
        │              │              │
        └──────────────┼──────────────┘
                       │
                  Monitoring
                       │
                       ▼
                 Cloud Resources
                       │
                       ▼
                 DevOps Automation
```

NovaOps will gradually bring these components together into one centralized platform.

---

# 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/abdulwasim19/NovaOps-1.0.git
```

### 2. Enter the project

```bash
cd NovaOps-1.0
```

### 3. Create a virtual environment

```bash
python3 -m venv venv
```

### 4. Activate the virtual environment

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python3 app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000
```

---

# 👨‍💻 Developer

**Abdul Wasim**

B.Tech Computer Science & Engineering
Raipur Institute of Technology
CSVTU

### Interests

* Cloud Computing
* AWS
* DevOps
* Python
* Backend Development
* Infrastructure Automation

---

# ⭐ Project Status

**NovaOps 1.0 — Active Development**

This project is continuously evolving as new Cloud, DevOps, backend, database, monitoring, and automation capabilities are implemented.

> **Build it. Understand it. Automate it. Scale it.**

---
