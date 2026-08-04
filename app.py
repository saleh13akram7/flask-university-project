from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)


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
    


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Database tables created successfully!"


if __name__ == "__main__":
    app.run(debug=True)