import logging
logger = logging.getLogger(__name__)

from app.extensions import db
from app.models import Student
from app.repositories.major import MajorRepository
from app.repositories.student import StudentRepository

from app.exceptions.student import (
    StudentNotFoundError,
    MajorNotFoundError,
    NoFieldsToUpdateError
)

from app.dtos import (
    CreateStudentDTO,
    UpdateStudentDTO,
    StudentResponseDTO
)

class StudentService:


    @staticmethod
    def _get_student_model(
        student_id: int)   -> Student:
        student = StudentRepository.get_by_id(
            student_id
        )

        if student is None:
            logger.warning(
                "Student not found: student_id=%s",
                student_id
            )

            raise StudentNotFoundError(
                student_id
            )

        return student

    @staticmethod
    def get_all_students() -> list[StudentResponseDTO]:
        students = StudentRepository.get_all()

        students_response = []

        for student in students:
            try:
                student_id = student.id

                if not isinstance(student_id, int):
                    raise ValueError(
                        "Student id is invalid"
                    )

            except Exception as error:
                logger.error(
                    "Failed to process student row: %s",
                    error
                )

                continue

            try:
                name = student.name

                if name is not None and not isinstance(
                    name,
                    str
                ):
                    raise ValueError(
                        "Student name is invalid"
                    )

            except Exception as error:
                logger.error(
                    "Student id=%s has invalid name: %s",
                    student_id,
                    error
                )

                name = None

            try:
                phone_number = student.phone_number

                if (
                    phone_number is not None
                    and not isinstance(phone_number, str)
                ):
                    raise ValueError(
                        "Student phone number is invalid"
                    )

            except Exception as error:
                logger.error(
                    "Student id=%s has invalid phone number: %s",
                    student_id,
                    error
                )

                phone_number = None

            try:
                email_address = student.email_address

                if (
                    email_address is not None
                    and not isinstance(email_address, str)
                ):
                    raise ValueError(
                        "Student email address is invalid"
                    )

            except Exception as error:
                logger.error(
                    "Student id=%s has invalid email address: %s",
                    student_id,
                    error
                )

                email_address = None

            try:
                major_id = student.major_id

                if (
                    major_id is not None
                    and not isinstance(major_id, int)
                ):
                    raise ValueError(
                        "Student major id is invalid"
                    )

            except Exception as error:
                logger.error(
                    "Student id=%s has invalid major id: %s",
                    student_id,
                    error
                )

                major_id = None

            student_response_dto = StudentResponseDTO(
                id=student_id,
                name=name,
                phone_number=phone_number,
                email_address=email_address,
                major_id=major_id
            )

            students_response.append(
                student_response_dto
            )

        return students_response
    
    @staticmethod
    def get_student(
        student_id: int
    ) -> StudentResponseDTO:
        student = StudentService._get_student_model(
            student_id
        )

        return StudentResponseDTO.model_validate(
            student
        )

    @staticmethod
    def create_student(student_dto: CreateStudentDTO) -> StudentResponseDTO:
        major = MajorRepository.get_by_id(
            student_dto.major_id
        )

        if major is None:
            logger.warning(
                "Student creation failed: major_id=%s was not found",
                student_dto.major_id
            )

            raise MajorNotFoundError(
                student_dto.major_id
            )

        student = Student(
            **student_dto.model_dump()
        )

        try:
            StudentRepository.add(student)
            db.session.commit()

        except Exception:
            db.session.rollback()

            logger.exception(
                "Unexpected error while creating student"
            )

            raise

        return StudentResponseDTO.model_validate(student)


    @staticmethod
    def update_student(
        student_id: int,
        update_dto: UpdateStudentDTO
    ) -> StudentResponseDTO:
        student = StudentService._get_student_model(
            student_id
        )

        updates = update_dto.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        if not updates:
            logger.warning(
                "Student update failed: no fields provided for student_id=%s",
                student_id
            )

            raise NoFieldsToUpdateError(
                student_id
            )

        if "major_id" in updates:
            major = MajorRepository.get_by_id(
                updates["major_id"]
            )

            if major is None:
                logger.warning(
                    "Student update failed: student_id=%s, major_id=%s was not found",
                    student_id,
                    updates["major_id"]
                )

                raise MajorNotFoundError(
                    updates["major_id"]
                )

        try:
            for field, value in updates.items():
                setattr(
                    student,
                    field,
                    value
                )

            db.session.commit()

        except Exception:
            db.session.rollback()

            logger.exception(
                "Unexpected error while updating student_id=%s",
                student_id
            )

            raise

        return StudentResponseDTO.model_validate(
            student
        )


    @staticmethod
    def delete_student(
        student_id: int
    ) -> None:
        student = StudentService._get_student_model(
            student_id
        )

        try:
            StudentRepository.delete(
                student
            )

            db.session.commit()

        except Exception:
            db.session.rollback()

            logger.exception(
                "Unexpected error while deleting student_id=%s",
                student_id
            )

            raise