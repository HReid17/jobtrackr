from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from extensions import db
from models import Application

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobtrackr.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard/dashboard.html")


# Applications
@app.route("/applications")
def applications():
    applications = Application.query.order_by(Application.applied_date.desc()).all()
    return render_template("applications/applications.html", applications=applications)


@app.route("/applications/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form.get("company")
        role = request.form.get("role")
        status = request.form.get("status")
        applied_date = request.form.get("applied_date")

        new_application = Application(
            company=company,
            role=role,
            status=status,
            applied_date=datetime.strptime(applied_date, "%Y-%m-%d").date(),
        )

        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for("applications"))

    return render_template("applications/add_application.html")


# Analytics
@app.route("/analytics")
def analytics():
    return render_template("analytics/analytics.html")


with app.app_context():
    db.create_all()

    print(
        Application.query.all()
    )  # Quick Test - Expecting [] to show as empty database

if __name__ == "__main__":
    app.run(debug=True)
