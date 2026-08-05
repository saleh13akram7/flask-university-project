from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Major, Student
from pydantic import ValidationError

from ..dtos import (
    CreateStudentDTO,
    UpdateStudentDTO,
    StudentResponseDTO
)


student_controller = Blueprint(
    "students",
    __name__,
    url_prefix="/api/students"
)


def student_to_dict(student):
    return {
        "id": student.id,
        "name": student.name,
        "phone_number": student.phone_number,
        "email_address": student.email_address,
        "major_id": student.major_id
    }


# GET /api/students
@student_controller.get("")
def get_students():
    students = db.session.execute(
        db.select(Student).order_by(Student.id)
    ).scalars().all()

    return jsonify([
        student_to_dict(student)
        for student in students
    ]), 200


# GET /api/students/1
@student_controller.get("/<int:student_id>")
def get_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(
        student_to_dict(student)
    ), 200


# POST /api/students
@student_controller.post("")
def create_student():
    data = request.get_json(silent=True) or {}

    try:
        student_dto = CreateStudentDTO.model_validate(data)

    except ValidationError as error:
        return jsonify({
            "error": "Invalid student data",
            "details": error.errors(
                include_url=False,
                include_input=False
            )
        }), 400

    major = db.session.get(
        Major,
        student_dto.major_id
    )

    if major is None:
        return jsonify({
            "error": "Major not found"
        }), 404

    student = Student(
        **student_dto.model_dump()
    )

    db.session.add(student)
    db.session.commit()

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
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    data = request.get_json(silent=True) or {}

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    if "name" in data:
        student.name = data["name"]

    if "phone_number" in data:
        student.phone_number = data["phone_number"]

    if "email_address" in data:
        student.email_address = data["email_address"]

    if "major_id" in data:
        major = db.session.get(Major, data["major_id"])

        if major is None:
            return jsonify({
                "error": "Major not found"
            }), 404

        student.major_id = data["major_id"]

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": student_to_dict(student)
    }), 200


# DELETE /api/students/1
@student_controller.delete("/<int:student_id>")
def delete_student(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    try:
        db.session.delete(student)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        return jsonify({
            "error": "Student cannot be deleted because they have registrations"
        }), 409

    return jsonify({
        "message": "Student deleted successfully"
    }), 200