# app/routes/desk_routes.py

from flask import Blueprint, jsonify, request
from controllers.desk_controller import DeskController
from utils.height_changer import HeightChanger

# Create a Blueprint for the desk routes
desk_bp = Blueprint('desk', __name__)
desk_controller = DeskController()
height_changer = HeightChanger()

@desk_bp.route('/desk/height', methods=['GET'])
def get_height():
    result = desk_controller.get_current_height()
    return jsonify(result)

@desk_bp.route('/desk/move_up', methods=['POST'])
def move_up():
    data = request.get_json()
    increment = data.get('increment', 1)  # Default increment to 1 if not provided
    result = desk_controller.move_up(increment)
    return jsonify(result)

@desk_bp.route('/desk/move_down', methods=['POST'])
def move_down():
    data = request.get_json()
    decrement = data.get('decrement', 1)  # Default decrement to 1 if not provided
    result = desk_controller.move_down(decrement)
    return jsonify(result)

@desk_bp.route('/desk/set_height', methods=['POST'])
def set_height():
    data = request.get_json()
    height = data.get('height')
    if height is None:
        return jsonify({"error": "Height is required"}), 400

    result = height_changer.set_height(height)
    return jsonify(result)
