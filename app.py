
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


# =========================================
# DASHBOARD
# =========================================

@app.route("/")
def dashboard():

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

    # Server health

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

    # Recent data

    recent_projects = Project.query.order_by(
        Project.id.desc()
    ).limit(5).all()

    recent_deployments = Deployment.query.order_by(
        Deployment.deployed_at.desc()
    ).limit(5).all()

    # Dashboard data

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
        recent_deployments=recent_deployments
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


@app.route("/projects/new", methods=["GET", "POST"])
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

        db.session.commit()

        return redirect(
            url_for("projects")
        )

    return render_template(
        "new_project.html"
    )


@app.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    if request.method == "POST":

        project.name = request.form["name"]

        project.description = request.form["description"]

        project.status = request.form["status"]

        db.session.commit()

        return redirect(
            url_for("projects")
        )

    return render_template(
        "edit_project.html",
        project=project
    )


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    db.session.delete(project)

    db.session.commit()

    return redirect(
        url_for("projects")
    )


# =========================================
# PROJECT DETAIL
# =========================================

@app.route("/projects/<int:project_id>")
def project_detail(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    # Project servers

    servers = Server.query.filter_by(
        project_id=project.id
    ).order_by(
        Server.name.asc()
    ).all()

    # Server health

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

    # Deployment statistics

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

    # Recent deployments

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

    # Search

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

    # Provider filter

    if provider:

        query = query.filter(
            Server.provider == provider
        )

    # Status filter

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


@app.route("/servers/new", methods=["GET", "POST"])
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

        db.session.commit()

        return redirect(
            url_for("servers")
        )

    return render_template(
        "new_server.html",
        projects=projects
    )


@app.route("/servers/edit/<int:server_id>", methods=["GET", "POST"])
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

        db.session.commit()

        return redirect(
            url_for("servers")
        )

    return render_template(
        "edit_server.html",
        server=server,
        projects=projects
    )


@app.route("/servers/delete/<int:server_id>", methods=["POST"])
def delete_server(server_id):

    server = Server.query.get_or_404(
        server_id
    )

    db.session.delete(server)

    db.session.commit()

    return redirect(
        url_for("servers")
    )


# =========================================
# PROJECT SERVERS API
# =========================================

@app.route("/api/projects/<int:project_id>/servers")
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

    # Search

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

    # Project filter

    if project_id:

        query = query.filter(
            Deployment.project_id == int(
                project_id
            )
        )

    # Environment filter

    if environment:

        query = query.filter(
            Deployment.environment == environment
        )

    # Status filter

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


@app.route("/deployments/new", methods=["GET", "POST"])
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

        # Required fields

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

        # Find server

        server = Server.query.get_or_404(
            server_id
        )

        # Validate project-server relationship

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

        # Create deployment

        deployment = Deployment(
            project_id=project_id,
            server_id=server_id,
            environment=environment,
            version=version,
            status=status
        )

        db.session.add(deployment)

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

        # =========================================
        # VALIDATE REQUIRED FIELDS
        # =========================================

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

        # =========================================
        # FIND SERVER
        # =========================================

        server = Server.query.get_or_404(
            server_id
        )

        # =========================================
        # VALIDATE PROJECT-SERVER RELATIONSHIP
        # =========================================

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

        # =========================================
        # UPDATE DEPLOYMENT
        # =========================================

        deployment.project_id = project_id

        deployment.server_id = server_id

        deployment.environment = environment

        deployment.version = version

        deployment.status = status

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


@app.route("/deployments/delete/<int:deployment_id>", methods=["POST"])
def delete_deployment(deployment_id):

    deployment = Deployment.query.get_or_404(
        deployment_id
    )

    db.session.delete(deployment)

    db.session.commit()

    return redirect(
        url_for("deployments")
    )


# =========================================
# DATABASE
# =========================================

with app.app_context():
    db.create_all()


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(debug=True)
