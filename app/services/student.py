from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Student
from ..repositories.major import MajorRepository
from ..repositories.student import StudentRepository


class StudentNotFoundError(Exception):
    pass


class MajorNotFoundError(Exception):
    pass


class NoFieldsToUpdateError(Exception):
    pass


class StudentHasRegistrationsError(Exception):
    pass


class StudentService:

    @staticmethod
    def get_all_students():
        return StudentRepository.get_all()

    @staticmethod
    def get_student(student_id):
        student = StudentRepository.get_by_id(
            student_id
        )

        if student is None:
            raise StudentNotFoundError()

        return student

    @staticmethod
    def create_student(student_dto):
        major = MajorRepository.get_by_id(
            student_dto.major_id
        )

        if major is None:
            raise MajorNotFoundError()

        student = Student(
            **student_dto.model_dump()
        )

        try:
            StudentRepository.add(student)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return student

    @staticmethod
    def update_student(
        student_id,
        update_dto
    ):
        student = StudentService.get_student(
            student_id
        )

        updates = update_dto.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        if not updates:
            raise NoFieldsToUpdateError()

        if "major_id" in updates:
            major = MajorRepository.get_by_id(
                updates["major_id"]
            )

            if major is None:
                raise MajorNotFoundError()

        try:
            for field, value in updates.items():
                setattr(student, field, value)

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return student

    @staticmethod
    def delete_student(student_id):
        student = StudentService.get_student(
            student_id
        )

        try:
            StudentRepository.delete(student)
            db.session.commit()

        except IntegrityError as error:
            db.session.rollback()

            raise StudentHasRegistrationsError() from error

        except Exception:
            db.session.rollback()
            raise