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


@desk_bp.route("/desk/move", methods=["GET"])
def move_up():
    """
    Moves the desk to the given direction. Path == ?direction=
    """
    direction = request.args.get("direction")

    if desk_controller.handle_moving_request(direction):
        return jsonify({"success": "moving desk to direction"})

    return jsonify({"error": "no valid direction given"})
