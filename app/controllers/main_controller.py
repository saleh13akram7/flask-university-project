from flask import Blueprint, jsonify


main_controller = Blueprint(
    "main",
    __name__
)


@main_controller.get("/")
def home():
    return jsonify({
        "message": "University API is running"
    }), 200


@main_controller.get("/health")
def health():
    return jsonify({
        "status": "ok"
    }), 200