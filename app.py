
# =========================================
# IMPORTS
# =========================================

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


# =========================================
# INDIA TIME
# =========================================

def india_now():
    """
    Return the current India local time (IST).

    SQLite stores this as a naive datetime representing
    the India local clock time.
    """

    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).replace(tzinfo=None)


# =========================================
# APP CONFIGURATION
# =========================================

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///novaops.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================
# MODELS
# =========================================

class Project(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    servers = db.relationship(
        "Server",
        backref="project",
        lazy=True
    )


class Server(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    ip_address = db.Column(
        db.String(50),
        nullable=False
    )

    provider = db.Column(
        db.String(50),
        nullable=False
    )

    region = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=True
    )


class Deployment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id"),
        nullable=False
    )

    server_id = db.Column(
        db.Integer,
        db.ForeignKey("server.id"),
        nullable=False
    )

    environment = db.Column(
        db.String(50),
        nullable=False
    )

    version = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False
    )

    deployed_at = db.Column(
        db.DateTime,
        default=india_now,
        nullable=False
    )

    project = db.relationship(
        "Project",
        backref="deployments"
    )

    server = db.relationship(
        "Server",
        backref="deployments"
    )


class AuditLog(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    action = db.Column(
        db.String(50),
        nullable=False
    )

    entity_type = db.Column(
        db.String(50),
        nullable=False
    )

    entity_id = db.Column(
        db.Integer,
        nullable=True
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=india_now,
        nullable=False
    )

# =========================================
# APPLICATION SETTINGS MODEL
# =========================================


class AppSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)


# =========================================
# SETTINGS HELPER FUNCTIONS
# =========================================

def get_app_setting(key, default):
    setting = AppSetting.query.filter_by(key=key).first()

    if setting:
        return setting.value

    return default


def save_app_setting(key, value):
    setting = AppSetting.query.filter_by(key=key).first()

    if setting:
        setting.value = value
    else:
        setting = AppSetting(key=key, value=value)
        db.session.add(setting)


# =========================================
# TEMPLATE CONTEXT PROCESSOR
# ADD YOUR CODE HERE
# =========================================

@app.context_processor
def inject_app_settings():
    stored_settings = {
        setting.key: setting.value
        for setting in AppSetting.query.all()
    }

    try:
        refresh_seconds = int(
            stored_settings.get("monitoring_refresh_seconds", "0")
        )
    except ValueError:
        refresh_seconds = 0

    return {
        "app_name": stored_settings.get("app_name", "NovaOps 1.0"),
        "environment_label": stored_settings.get(
            "environment_label", "Development"
        ),
        "monitoring_refresh_seconds": refresh_seconds
    }


# =========================================
# AUDIT LOG HELPER
# =========================================


def create_audit_log(
    action,
    entity_type,
    entity_id,
    message
):
    """
    Add an audit log entry to the current
    database transaction.
    """

    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        message=message
    )

    db.session.add(log)


def get_app_setting(key, default):
    setting = AppSetting.query.filter_by(key=key).first()

    if setting:
        return setting.value

    return default


def save_app_setting(key, value):
    setting = AppSetting.query.filter_by(key=key).first()

    if setting:
        setting.value = value
    else:
        setting = AppSetting(key=key, value=value)
        db.session.add(setting)

# =========================================
# BASELINE AUDIT LOGS
# =========================================


def seed_existing_audit_logs():
    """
    Create baseline entries for resources that
    existed before Audit Logs were introduced.

    These are NOT historical timestamps.
    They simply mark resources that already existed
    when the audit system was enabled.
    """

    # -----------------------------------------
    # EXISTING PROJECTS
    # -----------------------------------------

    projects = Project.query.all()

    for project in projects:

        existing_log = AuditLog.query.filter_by(
            action="BASELINE",
            entity_type="Project",
            entity_id=project.id
        ).first()

        if not existing_log:

            create_audit_log(
                "BASELINE",
                "Project",
                project.id,
                (
                    f"Existing project '{project.name}' "
                    "was present before audit logging "
                    "was enabled."
                )
            )

    # -----------------------------------------
    # EXISTING SERVERS
    # -----------------------------------------

    servers = Server.query.all()

    for server in servers:

        existing_log = AuditLog.query.filter_by(
            action="BASELINE",
            entity_type="Server",
            entity_id=server.id
        ).first()

        if not existing_log:

            create_audit_log(
                "BASELINE",
                "Server",
                server.id,
                (
                    f"Existing server '{server.name}' "
                    "was present before audit logging "
                    "was enabled."
                )
            )

    # -----------------------------------------
    # EXISTING DEPLOYMENTS
    # -----------------------------------------

    deployments = Deployment.query.all()

    for deployment in deployments:

        existing_log = AuditLog.query.filter_by(
            action="BASELINE",
            entity_type="Deployment",
            entity_id=deployment.id
        ).first()

        if not existing_log:

            create_audit_log(
                "BASELINE",
                "Deployment",
                deployment.id,
                (
                    f"Existing deployment "
                    f"'{deployment.version}' was present "
                    "before audit logging was enabled."
                )
            )

    db.session.commit()


# =========================================
# DASHBOARD
# =========================================

@app.route("/")
def dashboard():
    # Count resources
    project_count = Project.query.count()
    server_count = Server.query.count()
    deployment_count = Deployment.query.count()

    # Deployment statistics
    successful_deployments = Deployment.query.filter_by(
        status="Successful"
    ).count()

    in_progress_deployments = Deployment.query.filter_by(
        status="In Progress"
    ).count()

    failed_deployments = Deployment.query.filter_by(
        status="Failed"
    ).count()

    # Server statistics
    running_servers = Server.query.filter_by(
        status="Running"
    ).count()

    stopped_servers = Server.query.filter_by(
        status="Stopped"
    ).count()

    failed_servers = Server.query.filter_by(
        status="Failed"
    ).count()

    # Calculate infrastructure health
    health = (
        round((running_servers / server_count) * 100)
        if server_count > 0 else 0
    )

    # Recent resources and activity
    recent_projects = (
        Project.query
        .order_by(Project.id.desc())
        .limit(5)
        .all()
    )

    recent_deployments = (
        Deployment.query
        .order_by(Deployment.deployed_at.desc())
        .limit(5)
        .all()
    )

    recent_activity = (
        AuditLog.query
        .order_by(AuditLog.created_at.desc())
        .limit(8)
        .all()
    )

    # Dashboard summary
    stats = {
        "projects": project_count,
        "servers": server_count,
        "deployments": deployment_count,
        "health": health
    }

    deployment_stats = {
        "successful": successful_deployments,
        "in_progress": in_progress_deployments,
        "failed": failed_deployments
    }

    server_stats = {
        "running": running_servers,
        "stopped": stopped_servers,
        "failed": failed_servers
    }

    # IMPORTANT: Return the dashboard page
    return render_template(
        "dashboard.html",
        stats=stats,
        deployment_stats=deployment_stats,
        server_stats=server_stats,
        recent_projects=recent_projects,
        recent_deployments=recent_deployments,
        recent_activity=recent_activity
    )


@app.route("/monitoring")
def monitoring():
    # Get all servers
    servers = Server.query.order_by(Server.name.asc()).all()

    # Count servers by status
    total_servers = Server.query.count()
    running_servers = Server.query.filter_by(status="Running").count()
    stopped_servers = Server.query.filter_by(status="Stopped").count()
    failed_servers = Server.query.filter_by(status="Failed").count()

    # Calculate health percentage
    health = (
        round((running_servers / total_servers) * 100)
        if total_servers > 0 else 0
    )

    # Get failed deployments
    failed_deployments = (
        Deployment.query
        .filter_by(status="Failed")
        .order_by(Deployment.deployed_at.desc())
        .limit(10)
        .all()
    )

    # Get recent deployments
    recent_deployments = (
        Deployment.query
        .order_by(Deployment.deployed_at.desc())
        .limit(8)
        .all()
    )

    return render_template(
        "monitoring.html",
        servers=servers,
        total_servers=total_servers,
        running_servers=running_servers,
        stopped_servers=stopped_servers,
        failed_servers=failed_servers,
        health=health,
        failed_deployments=failed_deployments,
        recent_deployments=recent_deployments
    )

    # -----------------------------------------
    # DEPLOYMENT STATISTICS
    # -----------------------------------------

    successful_deployments = Deployment.query.filter_by(
        status="Successful"
    ).count()

    in_progress_deployments = Deployment.query.filter_by(
        status="In Progress"
    ).count()

    failed_deployments = Deployment.query.filter_by(
        status="Failed"
    ).count()

    # -----------------------------------------
    # SERVER HEALTH
    # -----------------------------------------

    running_servers = Server.query.filter_by(
        status="Running"
    ).count()

    stopped_servers = Server.query.filter_by(
        status="Stopped"
    ).count()

    failed_servers = Server.query.filter_by(
        status="Failed"
    ).count()

    if server_count > 0:

        health = round(
            (running_servers / server_count) * 100
        )

    else:

        health = 0

    # -----------------------------------------
    # RECENT PROJECTS
    # -----------------------------------------

    recent_projects = Project.query.order_by(
        Project.id.desc()
    ).limit(5).all()

    # -----------------------------------------
    # RECENT DEPLOYMENTS
    # -----------------------------------------

    recent_deployments = Deployment.query.order_by(
        Deployment.deployed_at.desc()
    ).limit(5).all()

    # -----------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------

    recent_activity = AuditLog.query.order_by(
        AuditLog.created_at.desc()
    ).limit(8).all()

    # -----------------------------------------
    # DASHBOARD DATA
    # -----------------------------------------

    stats = {
        "projects": project_count,
        "servers": server_count,
        "deployments": deployment_count,
        "health": health
    }

    deployment_stats = {
        "successful": successful_deployments,
        "in_progress": in_progress_deployments,
        "failed": failed_deployments
    }

    server_stats = {
        "running": running_servers,
        "stopped": stopped_servers,
        "failed": failed_servers
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        deployment_stats=deployment_stats,
        server_stats=server_stats,
        recent_projects=recent_projects,
        recent_deployments=recent_deployments,
        recent_activity=recent_activity
    )


# =========================================
# PROJECT ROUTES
# =========================================

@app.route("/projects")
def projects():

    projects = Project.query.order_by(
        Project.id.desc()
    ).all()

    return render_template(
        "projects.html",
        projects=projects
    )


@app.route(
    "/projects/new",
    methods=["GET", "POST"]
)
def new_project():

    if request.method == "POST":

        name = request.form["name"]

        description = request.form["description"]

        status = request.form["status"]

        project = Project(
            name=name,
            description=description,
            status=status
        )

        db.session.add(project)

        # Generate ID before audit entry
        db.session.flush()

        create_audit_log(
            "CREATE",
            "Project",
            project.id,
            f"Project '{project.name}' was created."
        )

        db.session.commit()

        return redirect(
            url_for("projects")
        )

    return render_template(
        "new_project.html"
    )


@app.route(
    "/projects/edit/<int:project_id>",
    methods=["GET", "POST"]
)
def edit_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    if request.method == "POST":

        project.name = request.form["name"]

        project.description = request.form["description"]

        project.status = request.form["status"]

        create_audit_log(
            "UPDATE",
            "Project",
            project.id,
            f"Project '{project.name}' was updated."
        )

        db.session.commit()

        return redirect(
            url_for("projects")
        )

    return render_template(
        "edit_project.html",
        project=project
    )


@app.route(
    "/projects/delete/<int:project_id>",
    methods=["POST"]
)
def delete_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    project_name = project.name

    project_id_value = project.id

    db.session.delete(project)

    create_audit_log(
        "DELETE",
        "Project",
        project_id_value,
        f"Project '{project_name}' was deleted."
    )

    db.session.commit()

    return redirect(
        url_for("projects")
    )


# =========================================
# PROJECT DETAIL
# =========================================

@app.route(
    "/projects/<int:project_id>"
)
def project_detail(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    # -----------------------------------------
    # PROJECT SERVERS
    # -----------------------------------------

    servers = Server.query.filter_by(
        project_id=project.id
    ).order_by(
        Server.name.asc()
    ).all()

    # -----------------------------------------
    # SERVER HEALTH
    # -----------------------------------------

    running_servers = Server.query.filter_by(
        project_id=project.id,
        status="Running"
    ).count()

    stopped_servers = Server.query.filter_by(
        project_id=project.id,
        status="Stopped"
    ).count()

    failed_servers = Server.query.filter_by(
        project_id=project.id,
        status="Failed"
    ).count()

    total_servers = len(servers)

    if total_servers > 0:

        health = round(
            (running_servers / total_servers) * 100
        )

    else:

        health = 0

    # -----------------------------------------
    # DEPLOYMENT STATISTICS
    # -----------------------------------------

    total_deployments = Deployment.query.filter_by(
        project_id=project.id
    ).count()

    successful_deployments = Deployment.query.filter_by(
        project_id=project.id,
        status="Successful"
    ).count()

    in_progress_deployments = Deployment.query.filter_by(
        project_id=project.id,
        status="In Progress"
    ).count()

    failed_deployments = Deployment.query.filter_by(
        project_id=project.id,
        status="Failed"
    ).count()

    # -----------------------------------------
    # RECENT DEPLOYMENTS
    # -----------------------------------------

    recent_deployments = Deployment.query.filter_by(
        project_id=project.id
    ).order_by(
        Deployment.deployed_at.desc()
    ).limit(10).all()

    deployment_stats = {
        "total": total_deployments,
        "successful": successful_deployments,
        "in_progress": in_progress_deployments,
        "failed": failed_deployments
    }

    server_stats = {
        "total": total_servers,
        "running": running_servers,
        "stopped": stopped_servers,
        "failed": failed_servers
    }

    return render_template(
        "project_detail.html",
        project=project,
        servers=servers,
        recent_deployments=recent_deployments,
        health=health,
        deployment_stats=deployment_stats,
        server_stats=server_stats
    )


# =========================================
# SERVER ROUTES
# =========================================

@app.route("/servers")
def servers():

    search = request.args.get(
        "search",
        ""
    ).strip()

    provider = request.args.get(
        "provider",
        ""
    ).strip()

    status = request.args.get(
        "status",
        ""
    ).strip()

    query = Server.query

    # -----------------------------------------
    # SEARCH
    # -----------------------------------------

    if search:

        query = query.filter(
            or_(
                Server.name.ilike(
                    f"%{search}%"
                ),
                Server.ip_address.ilike(
                    f"%{search}%"
                )
            )
        )

    # -----------------------------------------
    # PROVIDER FILTER
    # -----------------------------------------

    if provider:

        query = query.filter(
            Server.provider == provider
        )

    # -----------------------------------------
    # STATUS FILTER
    # -----------------------------------------

    if status:

        query = query.filter(
            Server.status == status
        )

    servers = query.order_by(
        Server.id.desc()
    ).all()

    return render_template(
        "servers.html",
        servers=servers,
        search=search,
        provider=provider,
        status=status
    )


@app.route(
    "/servers/new",
    methods=["GET", "POST"]
)
def new_server():

    projects = Project.query.order_by(
        Project.name.asc()
    ).all()

    if request.method == "POST":

        name = request.form["name"]

        ip_address = request.form["ip_address"]

        provider = request.form["provider"]

        region = request.form["region"]

        status = request.form["status"]

        project_id = request.form.get(
            "project_id"
        )

        if not project_id:

            return render_template(
                "new_server.html",
                projects=projects,
                error="Please select a project."
            )

        server = Server(
            name=name,
            ip_address=ip_address,
            provider=provider,
            region=region,
            status=status,
            project_id=int(project_id)
        )

        db.session.add(server)

        db.session.flush()

        create_audit_log(
            "CREATE",
            "Server",
            server.id,
            f"Server '{server.name}' was created."
        )

        db.session.commit()

        return redirect(
            url_for("servers")
        )

    return render_template(
        "new_server.html",
        projects=projects
    )


@app.route(
    "/servers/edit/<int:server_id>",
    methods=["GET", "POST"]
)
def edit_server(server_id):

    server = Server.query.get_or_404(
        server_id
    )

    projects = Project.query.order_by(
        Project.name.asc()
    ).all()

    if request.method == "POST":

        server.name = request.form["name"]

        server.ip_address = request.form["ip_address"]

        server.provider = request.form["provider"]

        server.region = request.form["region"]

        server.status = request.form["status"]

        project_id = request.form.get(
            "project_id"
        )

        if project_id:

            server.project_id = int(
                project_id
            )

        else:

            server.project_id = None

        create_audit_log(
            "UPDATE",
            "Server",
            server.id,
            f"Server '{server.name}' was updated."
        )

        db.session.commit()

        return redirect(
            url_for("servers")
        )

    return render_template(
        "edit_server.html",
        server=server,
        projects=projects
    )


@app.route(
    "/servers/delete/<int:server_id>",
    methods=["POST"]
)
def delete_server(server_id):

    server = Server.query.get_or_404(
        server_id
    )

    server_name = server.name

    server_id_value = server.id

    db.session.delete(server)

    create_audit_log(
        "DELETE",
        "Server",
        server_id_value,
        f"Server '{server_name}' was deleted."
    )

    db.session.commit()

    return redirect(
        url_for("servers")
    )


# =========================================
# PROJECT SERVERS API
# =========================================

@app.route(
    "/api/projects/<int:project_id>/servers"
)
def project_servers(project_id):

    servers = Server.query.filter_by(
        project_id=project_id
    ).order_by(
        Server.name.asc()
    ).all()

    return jsonify([
        {
            "id": server.id,
            "name": server.name
        }
        for server in servers
    ])


# =========================================
# DEPLOYMENT ROUTES
# =========================================

@app.route("/deployments")
def deployments():

    search = request.args.get(
        "search",
        ""
    ).strip()

    project_id = request.args.get(
        "project_id",
        ""
    ).strip()

    environment = request.args.get(
        "environment",
        ""
    ).strip()

    status = request.args.get(
        "status",
        ""
    ).strip()

    query = Deployment.query

    # -----------------------------------------
    # SEARCH
    # -----------------------------------------

    if search:

        query = query.join(
            Deployment.project
        ).join(
            Deployment.server
        ).filter(
            or_(
                Project.name.ilike(
                    f"%{search}%"
                ),
                Server.name.ilike(
                    f"%{search}%"
                ),
                Deployment.version.ilike(
                    f"%{search}%"
                )
            )
        )

    # -----------------------------------------
    # PROJECT FILTER
    # -----------------------------------------

    if project_id:

        query = query.filter(
            Deployment.project_id == int(
                project_id
            )
        )

    # -----------------------------------------
    # ENVIRONMENT FILTER
    # -----------------------------------------

    if environment:

        query = query.filter(
            Deployment.environment == environment
        )

    # -----------------------------------------
    # STATUS FILTER
    # -----------------------------------------

    if status:

        query = query.filter(
            Deployment.status == status
        )

    deployments = query.order_by(
        Deployment.deployed_at.desc()
    ).all()

    projects = Project.query.order_by(
        Project.name.asc()
    ).all()

    return render_template(
        "deployments.html",
        deployments=deployments,
        projects=projects,
        search=search,
        project_id=project_id,
        environment=environment,
        status=status
    )


@app.route(
    "/deployments/new",
    methods=["GET", "POST"]
)
def new_deployment():

    projects = Project.query.order_by(
        Project.name.asc()
    ).all()

    error = None

    if request.method == "POST":

        project_id = request.form.get(
            "project_id"
        )

        server_id = request.form.get(
            "server_id"
        )

        environment = request.form.get(
            "environment"
        )

        version = request.form.get(
            "version"
        )

        status = request.form.get(
            "status"
        )

        # -----------------------------------------
        # VALIDATE REQUIRED FIELDS
        # -----------------------------------------

        if not project_id or not server_id:

            error = (
                "Please select both a project and a server."
            )

            return render_template(
                "new_deployment.html",
                projects=projects,
                error=error
            )

        project_id = int(project_id)

        server_id = int(server_id)

        # -----------------------------------------
        # FIND SERVER
        # -----------------------------------------

        server = Server.query.get_or_404(
            server_id
        )

        # -----------------------------------------
        # VALIDATE RELATIONSHIP
        # -----------------------------------------

        if server.project_id != project_id:

            error = (
                "The selected server does not belong "
                "to the selected project."
            )

            return render_template(
                "new_deployment.html",
                projects=projects,
                error=error
            )

        # -----------------------------------------
        # CREATE DEPLOYMENT
        # -----------------------------------------

        deployment = Deployment(
            project_id=project_id,
            server_id=server_id,
            environment=environment,
            version=version,
            status=status
        )

        db.session.add(deployment)

        db.session.flush()

        create_audit_log(
            "CREATE",
            "Deployment",
            deployment.id,
            (
                f"Deployment '{deployment.version}' "
                f"was created for project "
                f"'{deployment.project.name}'."
            )
        )

        db.session.commit()

        return redirect(
            url_for("deployments")
        )

    return render_template(
        "new_deployment.html",
        projects=projects,
        error=error
    )


@app.route(
    "/deployments/edit/<int:deployment_id>",
    methods=["GET", "POST"]
)
def edit_deployment(deployment_id):

    deployment = Deployment.query.get_or_404(
        deployment_id
    )

    projects = Project.query.order_by(
        Project.name.asc()
    ).all()

    error = None

    if request.method == "POST":

        project_id = request.form.get(
            "project_id"
        )

        server_id = request.form.get(
            "server_id"
        )

        environment = request.form.get(
            "environment"
        )

        version = request.form.get(
            "version"
        )

        status = request.form.get(
            "status"
        )

        # -----------------------------------------
        # VALIDATE REQUIRED FIELDS
        # -----------------------------------------

        if not project_id or not server_id:

            error = (
                "Please select both a project and a server."
            )

            return render_template(
                "edit_deployment.html",
                deployment=deployment,
                projects=projects,
                error=error
            )

        project_id = int(project_id)

        server_id = int(server_id)

        # -----------------------------------------
        # FIND SERVER
        # -----------------------------------------

        server = Server.query.get_or_404(
            server_id
        )

        # -----------------------------------------
        # VALIDATE RELATIONSHIP
        # -----------------------------------------

        if server.project_id != project_id:

            error = (
                "The selected server does not belong "
                "to the selected project."
            )

            return render_template(
                "edit_deployment.html",
                deployment=deployment,
                projects=projects,
                error=error
            )

        # -----------------------------------------
        # UPDATE DEPLOYMENT
        # -----------------------------------------

        deployment.project_id = project_id

        deployment.server_id = server_id

        deployment.environment = environment

        deployment.version = version

        deployment.status = status

        create_audit_log(
            "UPDATE",
            "Deployment",
            deployment.id,
            (
                f"Deployment '{deployment.version}' "
                "was updated."
            )
        )

        db.session.commit()

        return redirect(
            url_for("deployments")
        )

    return render_template(
        "edit_deployment.html",
        deployment=deployment,
        projects=projects,
        error=error
    )


@app.route(
    "/deployments/delete/<int:deployment_id>",
    methods=["POST"]
)
def delete_deployment(deployment_id):

    deployment = Deployment.query.get_or_404(
        deployment_id
    )

    deployment_version = deployment.version

    deployment_id_value = deployment.id

    db.session.delete(deployment)

    create_audit_log(
        "DELETE",
        "Deployment",
        deployment_id_value,
        f"Deployment '{deployment_version}' was deleted."
    )

    db.session.commit()

    return redirect(
        url_for("deployments")
    )


# =========================================
# AUDIT LOG ROUTE
# =========================================

@app.route("/audit-logs")
def audit_logs():

    logs = AuditLog.query.order_by(
        AuditLog.created_at.desc()
    ).limit(100).all()

    return render_template(
        "audit_logs.html",
        logs=logs
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    allowed_environments = [
        "Development",
        "Staging",
        "Production"
    ]

    refresh_options = [
        ("0", "Disabled"),
        ("15", "Every 15 seconds"),
        ("30", "Every 30 seconds"),
        ("60", "Every 60 seconds"),
        ("300", "Every 5 minutes")
    ]

    current_settings = {
        "app_name": get_app_setting("app_name", "NovaOps 1.0"),
        "environment_label": get_app_setting(
            "environment_label", "Development"
        ),
        "monitoring_refresh_seconds": get_app_setting(
            "monitoring_refresh_seconds", "0"
        )
    }

    error = None

    if request.method == "POST":
        app_name = request.form.get("app_name", "").strip()
        environment_label = request.form.get(
            "environment_label", ""
        )
        refresh_seconds = request.form.get(
            "monitoring_refresh_seconds", "0"
        )

        current_settings = {
            "app_name": app_name,
            "environment_label": environment_label,
            "monitoring_refresh_seconds": refresh_seconds
        }

        allowed_refresh_values = [
            value for value, label in refresh_options
        ]

        if not app_name or len(app_name) > 40:
            error = "Application name must contain 1–40 characters."

        elif environment_label not in allowed_environments:
            error = "Please select a valid environment."

        elif refresh_seconds not in allowed_refresh_values:
            error = "Please select a valid monitoring refresh interval."

        else:
            save_app_setting("app_name", app_name)
            save_app_setting(
                "environment_label", environment_label
            )
            save_app_setting(
                "monitoring_refresh_seconds", refresh_seconds
            )

            create_audit_log(
                "UPDATE",
                "Settings",
                None,
                "Application settings were updated."
            )

            db.session.commit()

            return redirect(url_for("settings"))

    return render_template(
        "settings.html",
        settings=current_settings,
        environments=allowed_environments,
        refresh_options=refresh_options,
        error=error
    )

# =========================================
# DATABASE
# =========================================


with app.app_context():
    db.create_all()
    seed_existing_audit_logs()


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(debug=True)
