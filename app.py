from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# --------------------------------
# Flask Application
# --------------------------------

app = Flask(__name__)


# --------------------------------
# Database Configuration
# --------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///novaops.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --------------------------------
# Database Model
# --------------------------------

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


# --------------------------------
# Dashboard
# --------------------------------

@app.route("/")
def dashboard():
    project_count = Project.query.count()

    recent_projects = Project.query.order_by(
        Project.id.desc()
    ).limit(5).all()

    stats = {
        "projects": project_count,
        "servers": 8,
        "deployments": 24,
        "health": 98
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_projects=recent_projects
    )


# --------------------------------
# Projects - READ
# --------------------------------


@app.route("/projects")
def projects():

    projects = Project.query.all()

    return render_template(
        "projects.html",
        projects=projects
    )


# --------------------------------
# Projects - CREATE
# --------------------------------

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


# --------------------------------
# Projects - UPDATE / EDIT
# --------------------------------

@app.route(
    "/projects/edit/<int:project_id>",
    methods=["GET", "POST"]
)
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


# --------------------------------
# Projects - DELETE
# --------------------------------

@app.route(
    "/projects/delete/<int:project_id>",
    methods=["POST"]
)
def delete_project(project_id):

    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    return redirect(url_for("projects"))


# --------------------------------
# Create Database Tables
# --------------------------------

with app.app_context():
    db.create_all()


# --------------------------------
# Run Application
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)
