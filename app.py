from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from extensions import db
from models import Application

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobtrackr.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Dashboard
@app.route("/")
def dashboard():

    # Stats
    total_applications = Application.query.count()
    applied = Application.query.filter_by(status="Applied").count()
    interviews = Application.query.filter_by(status="Interview").count()
    offers = Application.query.filter_by(status="Offer").count()
    rejected = Application.query.filter_by(status="Rejected").count()

    # Recent Applications
    recent_applications = (
        Application.query.order_by(Application.applied_date.desc()).limit(5).all()
    )

    # Upcoming Interview's
    upcoming_interviews = (
        Application.query.filter(Application.interview_date >= date.today())
        .order_by(Application.interview_date.asc())
        .limit(3)
        .all()
    )

    return render_template(
        "dashboard/dashboard.html",
        total_applications=total_applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        recent_applications=recent_applications,
        upcoming_interviews=upcoming_interviews,
    )


# Applications
@app.route("/applications")
def applications():

    search = request.args.get("search")
    status = request.args.get("status")

    query = Application.query

    if search:
        query = query.filter(Application.company.contains(search))

    if status:
        query = query.filter(Application.status == status)

    applications = query.all()

    return render_template("applications/applications.html", applications=applications)


@app.route("/applications/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":
        company = request.form.get("company")
        role = request.form.get("role")
        status = request.form.get("status")
        applied_date = request.form.get("applied_date")
        location = request.form.get("location")
        source = request.form.get("source")
        interview_date = request.form.get("interview_date")
        interview_time = request.form.get("interview_time")
        notes = request.form.get("notes")

        if interview_date:
            interview_date = datetime.strptime(interview_date, "%Y-%m-%d").date()
        else:
            interview_date = None

        new_application = Application(
            company=company,
            role=role,
            status=status,
            applied_date=datetime.strptime(applied_date, "%Y-%m-%d").date(),
            location=location,
            source=source,
            interview_date=interview_date,
            interview_time=interview_time,
            notes=notes,
        )

        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for("applications"))

    return render_template("applications/add_application.html")


@app.route("/applications/delete/<int:id>", methods=["POST"])
def delete_application(id):

    application = Application.query.get_or_404(id)

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("applications"))


@app.route("/applications/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):

    application = Application.query.get_or_404(id)

    if request.method == "POST":
        application.company = request.form.get("company")
        application.role = request.form.get("role")
        application.status = request.form.get("status")

        application.applied_date = datetime.strptime(
            request.form.get("applied_date"), "%Y-%m-%d"
        ).date()

        application.location = request.form.get("location")
        application.source = request.form.get("source")

        interview_date = request.form.get("interview_date")

        if interview_date:
            application.interview_date = datetime.strptime(
                interview_date, "%Y-%m-%d"
            ).date()
        else:
            application.interview_date = None

            application.interview_time = request.form.get("interview_time")
            application.notes = request.form.get("notes")

        db.session.commit()

        return redirect(url_for("applications"))

    return render_template(
        "applications/edit_application.html", application=application
    )


# Analytics
@app.route("/analytics")
def analytics():

    total_applications = Application.query.count()
    applied = Application.query.filter_by(status="Applied").count()
    interviews = Application.query.filter_by(status="Interview").count()
    offers = Application.query.filter_by(status="Offer").count()
    rejected = Application.query.filter_by(status="Rejected").count()

    # Interview Rate
    if total_applications > 0:
        interview_rate = round((interviews / total_applications) * 100)
    else:
        interview_rate = 0


    # Source Breakdown
    all_applications = Application.query.all()

    source_breakdown = {}

    for application in all_applications:
        source = application.source

        if source:
            source_breakdown[source] = source_breakdown.get(source, 0) + 1


    # Activity Overview
    monthly_activity = {}
    
    for application in all_applications:
        month = application.applied_date.strftime("%b")

    monthly_activity[month] = monthly_activity.get(month, 0) + 1

    return render_template(
        "analytics/analytics.html",
        total_applications=total_applications,
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        interview_rate=interview_rate,
        source_breakdown=source_breakdown,
        monthly_activity=monthly_activity
    )


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
