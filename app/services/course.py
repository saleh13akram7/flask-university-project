from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Course
from app.repositories.course import CourseRepository

from app.exceptions.course import (
    CourseNotFoundError,
    PrerequisiteCourseNotFoundError,
    CourseCannotBeOwnPrerequisiteError,
    CourseNoFieldsToUpdateError,
    CourseHasDependenciesError
)

from app.dtos import (
    CreateCourseDTO,
    UpdateCourseDTO,
    CourseResponseDTO
)

class CourseService:

    @staticmethod
    def _get_course_model(
        course_id: int
    ) -> Course:
        course = CourseRepository.get_by_id(
            course_id
        )

        if course is None:
            raise CourseNotFoundError(
                course_id
            )

        return course    

    @staticmethod
    def get_all_courses() -> list[CourseResponseDTO]:
        courses = CourseRepository.get_all()

        return [
            CourseResponseDTO.model_validate(course)
            for course in courses
        ]

    @staticmethod
    def get_course(
        course_id: int
    ) -> CourseResponseDTO:
        course = CourseService._get_course_model(
            course_id
        )

        return CourseResponseDTO.model_validate(
            course
        )

    @staticmethod
    def create_course(
        course_dto: CreateCourseDTO
    ) -> CourseResponseDTO:
        if course_dto.pre_course_id is not None:
            prerequisite = CourseRepository.get_by_id(
                course_dto.pre_course_id
            )

            if prerequisite is None:
                raise PrerequisiteCourseNotFoundError(course_dto.pre_course_id)

        course = Course(
            **course_dto.model_dump()
        )

        try:
            CourseRepository.add(course)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return CourseResponseDTO.model_validate(course)

    @staticmethod
    def update_course(course_id: int,update_dto: UpdateCourseDTO) -> CourseResponseDTO:
        
        course = CourseService._get_course_model(
            course_id
        )

        updates = update_dto.model_dump(
            exclude_unset=True
        )

        if not updates:
            raise CourseNoFieldsToUpdateError(course_id)

        if "pre_course_id" in updates:
            pre_course_id = updates["pre_course_id"]

            if pre_course_id is not None:
                if pre_course_id == course_id:
                    raise CourseCannotBeOwnPrerequisiteError(course_id,pre_course_id)

                prerequisite = CourseRepository.get_by_id(
                    pre_course_id
                )

                if prerequisite is None:
                    raise PrerequisiteCourseNotFoundError(pre_course_id)

        try:
            for field, value in updates.items():
                setattr(course, field, value)

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        return CourseResponseDTO.model_validate(course)

    @staticmethod
    def delete_course(course_id: int) -> None:
        course = CourseService._get_course_model(
            course_id
        )

        try:
            CourseRepository.delete(course)
            db.session.commit()

        except IntegrityError as error:
            db.session.rollback()

            raise CourseHasDependenciesError(course_id,["related records"]) from error

        except Exception:
            db.session.rollback()
            raise