from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)