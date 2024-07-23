# app/routes/desk_routes.py

from flask import Blueprint, jsonify, request
from controllers.desk_controller import DeskController
from utils.height_changer import HeightChanger

# Create a Blueprint for the desk routes
desk_bp = Blueprint("desk", __name__)
desk_controller = DeskController()
height_changer = HeightChanger()


@desk_bp.route("/desk/height", methods=["GET"])
def get_height():
    """
    get the current height of the desk
    """

    result = desk_controller.get_current_height()
    return jsonify(result)


@desk_bp.route("/desk/move", methods=["POST"])
def move_up():
    """
    Moves the desk to the given direction
    """

    data = request.get_json()
    increment = data.get("increment", 1)  # Default increment to 1 if not provided
    result = desk_controller.move_up(increment)
    return jsonify(result)
