from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Course
from app.repositories.course import CourseRepository


class CourseNotFoundError(Exception):
    pass


class PrerequisiteCourseNotFoundError(Exception):
    pass


class CourseCannotBeOwnPrerequisiteError(Exception):
    pass


class CourseNoFieldsToUpdateError(Exception):
    pass


class CourseHasDependenciesError(Exception):
    pass


class CourseService:

    @staticmethod
    def get_all_courses():
        return CourseRepository.get_all()

    @staticmethod
    def get_course(course_id):
        course = CourseRepository.get_by_id(
            course_id
        )

        if course is None:
            raise CourseNotFoundError()

        return course

    @staticmethod
    def create_course(course_dto):
        if course_dto.pre_course_id is not None:
            prerequisite = CourseRepository.get_by_id(
                course_dto.pre_course_id
            )

            if prerequisite is None:
                raise PrerequisiteCourseNotFoundError()

        course = Course(
            **course_dto.model_dump()
        )

        try:
            CourseRepository.add(course)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return course

    @staticmethod
    def update_course(
        course_id,
        update_dto
    ):
        course = CourseService.get_course(
            course_id
        )

        updates = update_dto.model_dump(
            exclude_unset=True
        )

        if not updates:
            raise CourseNoFieldsToUpdateError()

        if "pre_course_id" in updates:
            pre_course_id = updates["pre_course_id"]

            if pre_course_id is not None:
                if pre_course_id == course_id:
                    raise CourseCannotBeOwnPrerequisiteError()

                prerequisite = CourseRepository.get_by_id(
                    pre_course_id
                )

                if prerequisite is None:
                    raise PrerequisiteCourseNotFoundError()

        try:
            for field, value in updates.items():
                setattr(course, field, value)

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return course

    @staticmethod
    def delete_course(course_id):
        course = CourseService.get_course(
            course_id
        )

        try:
            CourseRepository.delete(course)
            db.session.commit()

        except IntegrityError as error:
            db.session.rollback()

            raise CourseHasDependenciesError() from error

        except Exception:
            db.session.rollback()
            raise