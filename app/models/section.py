from ..extensions import db


class Section(db.Model):
    __tablename__ = "section"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    number_of_student = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teacher.id"),
        nullable=False
    )

    course = db.relationship(
        "Course",
        backref="sections"
    )

    teacher = db.relationship(
        "Teacher",
        backref="sections"
    )