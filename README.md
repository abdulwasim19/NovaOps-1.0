<div align="center">

# 🚀 NovaOps 1.0

### Cloud & DevOps Operations Dashboard

**One dashboard to organize projects, manage server records, track deployments, and monitor system resources.**

Built with Python, Flask, HTML, CSS, and SQLite.

<br>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-v1.0-blue?style=for-the-badge)

</div>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Project Objectives](#-project-objectives)
- [Key Features](#-key-features)
- [Application Screenshots](#-application-screenshots)
- [Technology Stack](#-technology-stack)
- [Application Architecture](#-application-architecture)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [How to Use](#-how-to-use)
- [Monitoring and API](#-monitoring-and-api)
- [Security Considerations](#-security-considerations)
- [Current Limitations](#-current-limitations)
- [Future Enhancements](#-future-enhancements)
- [What I Learned](#-what-i-learned)
- [Conclusion](#-conclusion)
- [Author](#-author)
- [Acknowledgements](#-acknowledgements)

---

## 📖 About the Project

**NovaOps 1.0** is a web-based Cloud and DevOps Operations Dashboard developed to provide a centralized interface for organizing project information, managing server records, tracking deployments, and viewing system resource usage.

The application brings several operational management features together in one place, reducing the need to manage these records separately.

NovaOps is built using Python and Flask for the backend, HTML and CSS for the frontend, and a database for storing application records. It also uses `psutil` to retrieve system resource information from the machine running the application.

This project represents my practical learning journey in Python development, web application development, database management, system monitoring, and DevOps-related concepts.

### 🎯 Project Goal

To develop a simple, organized, and extensible dashboard that demonstrates the fundamentals of Cloud and DevOps operations management.

---

## ❓ Problem Statement

Managing project information, server inventories, deployment records, and system resource information across separate tools can make operational tracking difficult.

A centralized dashboard can help organize this information and make it easier to review.

NovaOps addresses this need by providing a single interface for:

- Organizing projects.
- Maintaining server inventory records.
- Tracking deployment information.
- Viewing operational statistics.
- Monitoring local system resource usage.
- Reviewing audit logs and application settings.

The current version focuses on application-level management and local system monitoring, with cloud integrations planned for future releases.

---

## 🎯 Project Objectives

The main objectives of NovaOps 1.0 are:

1. Develop a web-based dashboard using Python and Flask.
2. Implement CRUD operations for projects, servers, and deployments.
3. Maintain relationships between projects, servers, and deployments.
4. Provide search and filtering functionality for server records.
5. Display CPU, memory, and disk usage for the local system.
6. Organize operational information through dashboard statistics.
7. Practice database integration and application error handling.
8. Maintain project code using Git and GitHub.
9. Establish a foundation for future cloud monitoring and deployment automation.

---

## ✨ Key Features

### 1. 📊 Dashboard

The dashboard provides a centralized overview of application records and operational information.

**Features:**
- Project statistics.
- Server statistics.
- Deployment statistics.
- Quick access to management sections.
- An organized overview of the application's data.

### 2. 📁 Project Management

Manage project information through the application.

**Features:**
- Create projects.
- View project records.
- Update project information.
- Delete projects where permitted.
- Organize project information in one place.

### 3. 🖥️ Server Management

Maintain a centralized inventory of server records.

**Features:**
- Add server records.
- View server information.
- Edit existing server records.
- Delete eligible server records.
- Search server records.
- Filter records by provider and status.
- Associate servers with projects.

**Note:** The server records in the current version are application-managed records. Adding a server does not automatically provision or connect to a real cloud server.

### 4. 🚀 Deployment Management

Maintain deployment records and their associated project and server information.

**Features:**
- Create deployment records.
- View deployment information.
- Update deployment records.
- Delete deployment records where permitted.
- Associate deployments with projects and servers.
- Maintain relationships between operational records.

NovaOps 1.0 tracks deployment information; it does not yet execute deployment pipelines automatically.

### 5. 📈 System Resource Monitoring

The monitoring section displays resource information for the machine running NovaOps.

Using the Python `psutil` library, the application can retrieve metrics such as:

- CPU utilization.
- Memory utilization.
- Disk utilization.

The monitoring interface periodically refreshes the available metrics.

**Important:** These are local machine metrics, not metrics collected from every server listed in the application or from AWS EC2 instances.

### 6. 🔍 Search and Filtering

The server management section supports searching and filtering to make records easier to find.

Depending on the available fields, users can narrow the server list by search terms, provider, and status.

### 7. 📝 Audit Logs

The application includes an audit logs section for reviewing available operational log records.

The completeness of audit history depends on which application actions are currently recorded.

### 8. ⚙️ Application Settings

The settings section provides an interface for managing the application's available configuration options.

The settings available depend on the current implementation.

---

## 🖼️ Application Screenshots

Screenshots help visitors understand the application before installing it.

Add screenshots of your actual running application to a folder named `screenshots/`.

### Dashboard

![NovaOps Dashboard](screenshots/dashboard.png)

*Overview of projects, servers, deployments, and dashboard statistics.*

### Server Management

![NovaOps Server Management](screenshots/servers.png)

*Server inventory with search, filtering, and management actions.*

### Deployment Management

![NovaOps Deployments](screenshots/deployments.png)

*Deployment records and their associated project and server information.*

### System Monitoring

![NovaOps Monitoring](screenshots/monitoring.png)

*Local CPU, memory, and disk utilization.*

> **Screenshot setup:** Create the `screenshots` folder and save your actual screenshots using the filenames shown above. Until you add those images, GitHub will display broken image links. Remove any screenshot section for which you do not have an image yet.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming and application logic |
| Flask | Web framework and HTTP request handling |
| HTML5 | Page structure |
| CSS3 | Styling and user interface |
| SQLite | Database storage, if configured as the application's database |
| SQLAlchemy | Database operations and ORM, if used by the current implementation |
| psutil | Local system resource monitoring |
| Jinja2 | Dynamic HTML templates through Flask |
| Git | Version control |
| GitHub | Source code hosting and project collaboration |
| Visual Studio Code | Development environment |

**Note:** The table describes the technologies used or expected in this project. Remove any technology that is not actually used in your implementation.

---

## 🏗️ Application Architecture

NovaOps follows a simple web application architecture.

```text
                 USER
                   |
                   v
          +------------------+
          |   Web Browser    |
          |   HTML and CSS   |
          +------------------+
                   |
                   v
          +------------------+
          |   Flask Server   |
          |  Python Backend  |
          +------------------+
                   |
          +--------+---------+
          |        |         |
          v        v         v
     +---------+ +---------+ +----------+
     | Projects| | Servers | |Deployment|
     |Management| |Management| |Management|
     +---------+ +---------+ +----------+
          |        |         |
          +--------+---------+
                   |
                   v
          +------------------+
          |     Database     |
          | Application Data |
          +------------------+

          +------------------+
          | Local Monitoring |
          |      psutil      |
          +------------------+
                   |
                   v
          CPU / Memory / Disk
          of the host machine
```

### How It Works

1. The user interacts with NovaOps through a web browser.
2. Flask receives HTTP requests and routes them to the appropriate backend functions.
3. The backend processes application logic and database operations.
4. The templates render the requested pages.
5. The monitoring functionality retrieves local system resource information through `psutil`.
6. The dashboard presents the available records and metrics to the user.

This architecture provides a foundation for adding integrations with cloud platforms and deployment tools in later versions.

---

## 📂 Project Structure

The following is a representative structure of the project. Your exact files may differ.

```text
NovaOps-1.0/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── projects.html
│   ├── servers.html
│   ├── deployments.html
│   └── ...
│
├── static/
│   ├── style.css
│   └── ...
│
├── screenshots/
│   ├── dashboard.png
│   ├── servers.png
│   ├── deployments.png
│   └── monitoring.png
│
└── venv/
```

**Note:** The `venv/` directory is a local development environment and should not be committed to GitHub. The database file may also be stored separately, depending on your configuration.

---

## 💻 Installation and Setup

Follow these steps to run NovaOps on your local machine.

### Prerequisites

Install the following:

- Python 3.12 or another version supported by the project's dependencies.
- Git.
- A code editor such as Visual Studio Code.
- A terminal.

### Step 1: Clone the Repository

```bash
git clone https://github.com/abdulwasim19/NovaOps-1.0.git
```

Navigate into the project directory:

```bash
cd NovaOps-1.0
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment

On Linux:

```bash
source venv/bin/activate
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing or incomplete, update it with the dependencies actually required by the application before publishing the repository.

### Step 5: Configure the Application

Set the required configuration values before running the application.

For local development, Flask needs a secret key for session functionality, including flash messages.

Generate a secret key using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Store the generated key in an environment variable rather than committing it to GitHub.

For example, on Linux:

```bash
export SECRET_KEY="paste-your-generated-secret-here"
```

Your Flask application must read that environment variable, for example:

```python
import os

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
```

Adapt this example to your existing configuration. Do not replace other application settings.

### Step 6: Run the Application

```bash
python app.py
```

Open the local address printed by Flask in your terminal. If the application uses Flask's default development server, the address is usually:

```text
http://127.0.0.1:5000
```

You should now be able to access the NovaOps dashboard.

> **Development server:** Flask's built-in development server is intended for local development, not production deployment.

---

## 🚦 How to Use

After starting NovaOps, follow this general workflow.

### 1. Open the Dashboard

Review the available statistics and navigate to the required section.

### 2. Manage Projects

Create or update project records as needed.

### 3. Manage Server Records

Add server inventory records, associate them with projects, and use the available search and filters.

### 4. Manage Deployments

Create deployment records and associate them with the appropriate project and server.

### 5. Review Monitoring

Open the monitoring page to view local CPU, memory, and disk metrics.

### 6. Review Logs and Settings

Use the available audit logs and settings sections to review application information and configuration.

---

## 📡 Monitoring and API

NovaOps includes an endpoint for retrieving local system metrics.

### System Metrics Endpoint

```http
GET /api/system-metrics
```

The endpoint returns system resource information in JSON format, according to the current implementation.

Example response structure:

```json
{
  "cpu_percent": 25.0,
  "memory_percent": 61.5,
  "disk_percent": 48.2
}
```

The values above are illustrative examples, not live readings from your application.

### How It Works

1. The backend collects metrics through `psutil`.
2. The endpoint returns the available values as JSON.
3. The monitoring interface requests updated metrics periodically.
4. The interface displays the latest returned readings.

**Scope:** The endpoint reports the local host's metrics. It is not currently a distributed monitoring agent for remote servers.

---

## 🔐 Security Considerations

Security is important for any application that manages operational information.

The following practices should be followed:

- Keep secret keys and credentials out of source control.
- Use environment variables for sensitive configuration.
- Exclude the virtual environment from Git.
- Do not publish private keys, access tokens, passwords, or AWS credentials.
- Review database contents before publishing a database file.
- Use authentication and authorization before exposing administrative functionality to multiple users.
- Apply appropriate input validation to forms and API endpoints.
- Protect state-changing requests against cross-site request forgery where applicable.
- Use a production-ready application server and HTTPS for a public deployment.

NovaOps 1.0 should be treated as a development and portfolio project until the necessary production security controls have been implemented and tested.

---

## ⚠️ Current Limitations

NovaOps 1.0 provides a foundation for operational management, but some capabilities are not yet implemented.

### 1. No Direct AWS Resource Integration

Server records are managed within the application. They do not automatically represent live AWS resources.

### 2. No Automated Deployment Pipeline

The application tracks deployment records but does not currently perform a complete automated deployment workflow.

### 3. Local System Monitoring

The current monitoring feature reports metrics from the machine running NovaOps, rather than collecting metrics from all registered servers.

### 4. Limited Historical Metrics

The current monitoring feature focuses on current resource readings. Persistent time-series metrics, historical graphs, and long-term analysis are future enhancements.

### 5. Production Readiness

Authentication, authorization, deployment hardening, and other production security requirements need further implementation and verification before the application is exposed as a production service.

---

## 🔮 Future Enhancements

The following improvements are planned for future versions of NovaOps.

### Phase 1: Application Improvements

- Improve form validation and error handling.
- Expand automated testing.
- Improve the user interface and dashboard layout.
- Improve audit logging.
- Add documentation for APIs and configuration.

### Phase 2: AWS Cloud Integration

- Integrate AWS APIs through the AWS SDK for Python (`boto3`).
- Retrieve information about authorized EC2 instances.
- Display instance states and selected instance details.
- Explore CloudWatch integration for AWS resource metrics.
- Add appropriate AWS IAM permissions and secure credential handling.

### Phase 3: Advanced Monitoring

- Introduce historical metrics storage.
- Display CPU, memory, and disk usage graphs over time.
- Add configurable monitoring thresholds.
- Explore alert notifications for selected conditions.
- Support monitoring multiple authorized hosts.

### Phase 4: DevOps Automation

- Explore automated deployment workflows.
- Integrate Git-based build and deployment pipelines.
- Introduce Docker-based packaging.
- Explore CI/CD using GitHub Actions.
- Investigate infrastructure provisioning with Terraform.

### Phase 5: Production and Security

- Implement user authentication.
- Add role-based access control.
- Strengthen API and form security.
- Add automated tests to the development workflow.
- Deploy using a production-ready application server.
- Introduce structured logging and application health checks.

These enhancements are a roadmap, not features currently included in NovaOps 1.0.

---

## 📚 What I Learned

Developing NovaOps provided practical experience with several software development and DevOps concepts.

### Python and Backend Development
- Writing Python application logic.
- Working with Flask routes and request handling.
- Rendering dynamic templates.
- Handling application errors.

### Database Management
- Performing create, read, update, and delete operations.
- Managing relationships between projects, servers, and deployments.
- Understanding database integrity constraints.
- Handling errors without unnecessarily damaging existing records.

### Frontend Development
- Structuring pages with HTML.
- Styling interfaces with CSS.
- Displaying application data in tables and dashboard components.
- Connecting frontend pages to backend routes.

### System Monitoring
- Collecting local system resource metrics.
- Using `psutil` to retrieve CPU, memory, and disk information.
- Returning monitoring information through a JSON endpoint.

### Development Tools
- Using Git for version control.
- Maintaining a project repository on GitHub.
- Managing Python dependencies through a virtual environment.
- Debugging application errors and improving existing functionality.

The project also helped me understand the difference between managing server information in an application and integrating that application with real cloud infrastructure.

---

## 🏁 Conclusion

NovaOps 1.0 is a practical Cloud and DevOps Operations Dashboard that brings project management, server inventory management, deployment tracking, and local system monitoring together in one web application.

Building this project strengthened my understanding of Python, Flask, database operations, frontend integration, system monitoring, error handling, and version control. It also provided practical experience in debugging application issues, maintaining data relationships, and organizing a multi-feature application.

Although the current version does not yet provide direct AWS resource management or automated deployment pipelines, it establishes a foundation for expanding the application into a more comprehensive operations platform.

**NovaOps 1.0 represents an important step in my journey toward becoming a Cloud and DevOps Engineer.** My next goal is to build on this foundation by learning and implementing AWS integration, containerization, CI/CD, infrastructure as code, and advanced monitoring.


---

## 📸 Screenshots

### 1. Dashboard
![NovaOps Dashboard](screenshots/dashboard.png)

### 2. Project Management
![NovaOps Projects](screenshots/projects.png)

### 3. Server Management
![NovaOps Servers](screenshots/servers.png)

### 4. Deployment Management
![NovaOps Deployments](screenshots/deployments.png)

### 5. System Monitoring
![NovaOps Monitoring](screenshots/monitoring.png)
---

## 👨‍💻 Author

**Abdul Wasim**

B.Tech Computer Science and Engineering

Aspiring Cloud and DevOps Engineer

- GitHub: [@abdulwasim19](https://github.com/abdulwasim19)
- LinkedIn: [Abdul Wasim](https://www.linkedin.com/in/abdulwasim1/)

I'm continuously learning and building practical projects to strengthen my skills in Python, cloud computing, Linux, and DevOps.

---

## 🙏 Acknowledgements

I acknowledge the developers and communities behind the open-source tools and technologies used in this project, including Python, Flask, and the broader open-source ecosystem.

---

<div align="center">

### ⭐ Thank you for visiting NovaOps 1.0!

**Learn. Build. Automate. Improve.**

</div>
