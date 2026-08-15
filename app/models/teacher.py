from app.extensions import db

class Teacher(db.Model):
    __tablename__ = "teacher"

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