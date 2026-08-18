from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.dtos import (
    CreateCourseDTO,
    UpdateCourseDTO,
    CourseResponseDTO
)
from app.services import CourseService

from app.exceptions.course import (
    CourseNotFoundError,
    PrerequisiteCourseNotFoundError,
    CourseCannotBeOwnPrerequisiteError,
    CourseNoFieldsToUpdateError,
    CourseHasDependenciesError
)


course_controller = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


def validation_error_response(error):
    return jsonify({
        "error": "Invalid course data",
        "details": error.errors(
            include_url=False,
            include_input=False
        )
    }), 400


# GET /api/courses
@course_controller.get("")
def get_courses():
    courses = CourseService.get_all_courses()

    courses_response = [
        CourseResponseDTO
        .model_validate(course)
        .model_dump()
        for course in courses
    ]

    return jsonify(courses_response), 200


# GET /api/courses/1
@course_controller.get("/<int:course_id>")
def get_course(course_id):
    try:
        course = CourseService.get_course(
            course_id
        )

    except CourseNotFoundError:
        return jsonify({
            "error": "Course not found"
        }), 404

    response_dto = CourseResponseDTO.model_validate(
        course
    )

    return jsonify(
        response_dto.model_dump()
    ), 200


# POST /api/courses
@course_controller.post("")
def create_course():
    data = request.get_json(silent=True) or {}

    try:
        course_dto = CreateCourseDTO.model_validate(
            data
        )

    except ValidationError as error:
        return validation_error_response(error)

    try:
        course = CourseService.create_course(
            course_dto
        )

    except PrerequisiteCourseNotFoundError:
        return jsonify({
            "error": "Prerequisite course not found"
        }), 404

    response_dto = CourseResponseDTO.model_validate(
        course
    )

    return jsonify({
        "message": "Course created successfully",
        "course": response_dto.model_dump()
    }), 201


# PATCH /api/courses/1
@course_controller.patch("/<int:course_id>")
def update_course(course_id):
    data = request.get_json(silent=True) or {}

    try:
        update_dto = UpdateCourseDTO.model_validate(
            data
        )

    except ValidationError as error:
        return validation_error_response(error)

    try:
        course = CourseService.update_course(
            course_id,
            update_dto
        )

    except CourseNotFoundError:
        return jsonify({
            "error": "Course not found"
        }), 404

    except PrerequisiteCourseNotFoundError:
        return jsonify({
            "error": "Prerequisite course not found"
        }), 404

    except CourseCannotBeOwnPrerequisiteError:
        return jsonify({
            "error": (
                "Course cannot be its own prerequisite"
            )
        }), 400

    except CourseNoFieldsToUpdateError:
        return jsonify({
            "error": "No valid fields provided"
        }), 400

    response_dto = CourseResponseDTO.model_validate(
        course
    )

    return jsonify({
        "message": "Course updated successfully",
        "course": response_dto.model_dump()
    }), 200


# DELETE /api/courses/1
@course_controller.delete("/<int:course_id>")
def delete_course(course_id):
    try:
        CourseService.delete_course(
            course_id
        )

    except CourseNotFoundError:
        return jsonify({
            "error": "Course not found"
        }), 404

    except CourseHasDependenciesError:
        return jsonify({
            "error": (
                "Course cannot be deleted because "
                "it has related records"
            )
        }), 409

    return jsonify({
        "message": "Course deleted successfully"
    }), 200