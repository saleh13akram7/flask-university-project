from app.extensions import db
from app.models import Student


class StudentRepository:

    @staticmethod
    def get_all():
        return db.session.execute(
            db.select(Student)
            .where(Student.is_deleted.is_(False))
            .order_by(Student.id)
        ).scalars().all()

    @staticmethod
    def get_by_id(student_id):
        return db.session.execute(
            db.select(Student).where(
                Student.id == student_id,
                Student.is_deleted.is_(False)
            )
        ).scalar_one_or_none()

    @staticmethod
    def add(student):
        db.session.add(student)

    @staticmethod
    def delete(student):
        student.is_deleted = True