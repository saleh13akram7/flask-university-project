from ..extensions import db
from ..models import Student


class StudentRepository:

    @staticmethod
    def get_all():
        return db.session.execute(
            db.select(Student).order_by(Student.id)
        ).scalars().all()

    @staticmethod
    def get_by_id(student_id):
        return db.session.get(
            Student,
            student_id
        )

    @staticmethod
    def add(student):
        db.session.add(student)

    @staticmethod
    def delete(student):
        db.session.delete(student)