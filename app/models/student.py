from ..extensions import db


class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    phone_number = db.Column(
        db.String(20),
        nullable=False
    )

    email_address = db.Column(
        db.String(150),
        nullable=False
    )

    major_id = db.Column(
        db.Integer,
        db.ForeignKey("major.id"),
        nullable=False
    )

    major = db.relationship(
        "Major",
        backref="students"
    )