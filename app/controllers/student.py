from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.dtos import (
    CreateStudentDTO,
    UpdateStudentDTO,
    StudentResponseDTO
)
from app.services import StudentService

from app.exceptions.student import (
    StudentNotFoundError,
    MajorNotFoundError,
    NoFieldsToUpdateError
)


student_controller = Blueprint(
    "students",
    __name__,
    url_prefix="/api/students"
)


def validation_error_response(error):
    return jsonify({
        "error": "Invalid student data",
        "details": error.errors(
            include_url=False,
            include_input=False
        )
    }), 400


# GET /api/students
@student_controller.get("")
def get_students():
    students = StudentService.get_all_students()

    students_response = [
        StudentResponseDTO
        .model_validate(student)
        .model_dump()
        for student in students
    ]

    return jsonify(students_response), 200


# GET /api/students/1
@student_controller.get("/<int:student_id>")
def get_student(student_id):
    try:
        student = StudentService.get_student(
            student_id
        )

    except StudentNotFoundError:
        return jsonify({
            "error": "Student not found"
        }), 404

    response_dto = StudentResponseDTO.model_validate(
        student
    )

    return jsonify(
        response_dto.model_dump()
    ), 200


# POST /api/students
@student_controller.post("")
def create_student():
    data = request.get_json(silent=True) or {}

    try:
        student_dto = CreateStudentDTO.model_validate(
            data
        )

    except ValidationError as error:
        return validation_error_response(error)

    try:
        student = StudentService.create_student(
            student_dto
        )

    except MajorNotFoundError:
        return jsonify({
            "error": "Major not found"
        }), 404

    response_dto = StudentResponseDTO.model_validate(
        student
    )

    return jsonify({
        "message": "Student created successfully",
        "student": response_dto.model_dump()
    }), 201


# PATCH /api/students/1
@student_controller.patch("/<int:student_id>")
def update_student(student_id):
    data = request.get_json(silent=True) or {}

    try:
        update_dto = UpdateStudentDTO.model_validate(
            data
        )

    except ValidationError as error:
        return validation_error_response(error)

    try:
        student = StudentService.update_student(
            student_id,
            update_dto
        )

    except StudentNotFoundError:
        return jsonify({
            "error": "Student not found"
        }), 404

    except MajorNotFoundError:
        return jsonify({
            "error": "Major not found"
        }), 404

    except NoFieldsToUpdateError:
        return jsonify({
            "error": "No valid fields provided"
        }), 400

    response_dto = StudentResponseDTO.model_validate(
        student
    )

    return jsonify({
        "message": "Student updated successfully",
        "student": response_dto.model_dump()
    }), 200


# DELETE /api/students/1
@student_controller.delete("/<int:student_id>")
def delete_student(student_id):
    try:
        StudentService.delete_student(
            student_id
        )

    except StudentNotFoundError:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify({
        "message": "Student deleted successfully"
    }), 200