from ..extensions import db


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    number_of_hours = db.Column(
        db.Integer,
        nullable=False
    )

    pre_course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=True
    )

    prerequisite = db.relationship(
        "Course",
        remote_side=[id],
        backref="next_courses"
    )