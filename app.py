from flask import Flask, render_template

app = Flask(__name__)


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

    return render_template("projects.html")


if __name__ == "__main__":
    app.run(debug=True)
