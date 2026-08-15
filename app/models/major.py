from app.extensions import db

class Major(db.Model):
    __tablename__ = "major"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    college = db.Column(
        db.String(100),
        nullable=False
    )

    number_of_hours = db.Column(
        db.Integer,
        nullable=False
    )