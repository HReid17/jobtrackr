from flask import Flask, render_template
from extensions import db
from models import Application

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobtrackr.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# Applications
@app.route("/applications")
def applications():
    return render_template("applications.html")


# Analytics
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


with app.app_context():
    db.create_all()
    
    print(Application.query.all()) # Quick Test - Expecting [] to show as empty database

if __name__ == "__main__":
    app.run(debug=True)