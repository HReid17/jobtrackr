from extensions import db


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Applied")
    applied_date = db.Column(db.Date, nullable=False)

    location = db.Column(db.String(100))
    source = db.Column(db.String(100))

    interview_date = db.Column(db.Date)
    interview_time = db.Column(db.String(20))

    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<Application {self.company}>"
