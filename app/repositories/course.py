from app.extensions import db
from app.models import Course


class CourseRepository:

    @staticmethod
    def get_all():
        return db.session.execute(
            db.select(Course).order_by(Course.id)
        ).scalars().all()

    @staticmethod
    def get_by_id(course_id):
        return db.session.get(
            Course,
            course_id
        )

    @staticmethod
    def add(course):
        db.session.add(course)

    @staticmethod
    def delete(course):
        db.session.delete(course)