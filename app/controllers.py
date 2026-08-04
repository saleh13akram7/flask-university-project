from flask import Blueprint, render_template


main_controller = Blueprint(
    "main",
    __name__
)


@main_controller.route("/")
def home():
    return render_template("home.html")