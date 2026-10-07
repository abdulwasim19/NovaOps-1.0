# Imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# App configuration
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///novaops.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODELS
# =========================

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)


# =========================
# DASHBOARD
# =========================

@app.route("/")
def dashboard():

    project_count = Project.query.count()
    server_count = Server.query.count()

    recent_projects = Project.query.order_by(
        Project.id.desc()
    ).limit(5).all()

    stats = {
        "projects": project_count,
        "servers": server_count,
        "deployments": 24,
        "health": 98
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_projects=recent_projects
    )


# =========================
# PROJECT ROUTES
# =========================

@app.route("/projects")
def projects():
    projects = Project.query.all()

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

        return redirect(url_for("projects"))

    return render_template("new_project.html")


@app.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    project = Project.query.get_or_404(project_id)

    if request.method == "POST":

        project.name = request.form["name"]
        project.description = request.form["description"]
        project.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("projects"))

    return render_template(
        "edit_project.html",
        project=project
    )


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):

    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for("projects"))


# =========================
# SERVER ROUTES
# =========================

@app.route("/servers")
def servers():

    servers = Server.query.all()

    return render_template(
        "servers.html",
        servers=servers
    )


@app.route("/servers/new", methods=["GET", "POST"])
def new_server():

    if request.method == "POST":

        name = request.form["name"]
        ip_address = request.form["ip_address"]
        provider = request.form["provider"]
        region = request.form["region"]
        status = request.form["status"]

        server = Server(
            name=name,
            ip_address=ip_address,
            provider=provider,
            region=region,
            status=status
        )

        db.session.add(server)
        db.session.commit()

        return redirect(url_for("servers"))

    return render_template("new_server.html")


@app.route("/servers/edit/<int:server_id>", methods=["GET", "POST"])
def edit_server(server_id):

    server = Server.query.get_or_404(server_id)

    if request.method == "POST":

        server.name = request.form["name"]
        server.ip_address = request.form["ip_address"]
        server.provider = request.form["provider"]
        server.region = request.form["region"]
        server.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("servers"))

    return render_template(
        "edit_server.html",
        server=server
    )


@app.route("/servers/delete/<int:server_id>", methods=["POST"])
def delete_server(server_id):

    server = Server.query.get_or_404(server_id)

    db.session.delete(server)
    db.session.commit()

    return redirect(url_for("servers"))


# =========================
# DATABASE
# =========================
with app.app_context():
    db.create_all()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)
