from app.extensions import db

class StudentSection(db.Model):
    __tablename__ = "student_section"

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        primary_key=True
    )

    section_id = db.Column(
        db.Integer,
        db.ForeignKey("section.id"),
        primary_key=True
    )

    total_grade = db.Column(
        db.Numeric(5, 2),
        nullable=True
    )

    student = db.relationship(
        "Student",
        backref="section_registrations"
    )

    section = db.relationship(
        "Section",
        backref="student_registrations"
    )