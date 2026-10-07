from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///novaops.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), nullable=False)


@app.route("/")
def dashboard():

    stats = {
        "projects": 4,
        "servers": 8,
        "deployments": 24,
        "health": 98
    }

    return render_template(
        "dashboard.html",
        stats=stats
    )


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

    projects = Project.query.all()

    return render_template(
        "projects.html",
        projects=projects
    )

    return render_template(
        "projects.html",
        projects=projects_data
    )

    return render_template(
        "projects.html",
        projects=projects_data
    )


with app.app_context():

    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
