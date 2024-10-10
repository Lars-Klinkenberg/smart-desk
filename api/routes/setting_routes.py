import json
from bottle import Bottle, HTTPResponse, request
from utils.enable_cors import add_cors_headers
from controllers.setting_controller import setting_controller

setting_server = Bottle()


@setting_server.route("/<:re:.*>", method="OPTIONS")
def enable_cors_generic_route():
    """
    This route takes priority over all others. So any request with an OPTIONS
    method will be handled by this function.

    See: https://github.com/bottlepy/bottle/issues/402

    NOTE: This means we won't 404 any invalid path that is an OPTIONS request.
    """
    add_cors_headers()


@setting_server.post("/profile")
def add_new_preset():
    """
    adds a new profile to the db
    """
    preset_name = request.headers.get("preset_name", None)
    heatmap_steps = request.headers.get("heatmap_steps", 60)
    daily_goal = request.headers.get("daily_goal", 120)
    standing_height = request.headers.get("standing_height", 115)
    sitting_height = request.headers.get("sitting_height", 74)

    if preset_name is None:
        return HTTPResponse(
            status=400, body=json.dumps({"error": "header preset_name is not defined"})
        )

    try:
        setting_controller.save_new_profile(
            preset_name, heatmap_steps, daily_goal, standing_height, sitting_height
        )
        return json.dumps({"success": "saved preset"})
    except Exception as e:
        return HTTPResponse(status=500, body=json.dumps({"error": str(e)}))


@setting_server.route("/profile")
def get_preset_by_name():
    """
    returns a profile by the preset_name

    Returns:
        string: serialized json either [{setting data}] or {"error":"..."}
    """
    preset_name = request.headers.get("preset_name", None)

    if preset_name is None:
        return HTTPResponse(
            status=400, body=json.dumps({"error": "header preset_name is not defined"})
        )

    return setting_controller.get_profile_by_name(preset_name)


@setting_server.put("/profile")
def update_preset():
    """
    updates an existing preset

    Returns:
        string: serialized json either {"success": "..."} or {"error":"..."}
    """
    preset_name = request.headers.get("preset_name", None)
    heatmap_steps = request.headers.get("heatmap_steps", None)
    daily_goal = request.headers.get("daily_goal", None)
    standing_height = request.headers.get("standing_height", None)
    sitting_height = request.headers.get("sitting_height", None)

    if preset_name is None:
        return HTTPResponse(
            status=400, body=json.dumps({"error": "header preset_name is not defined"})
        )

    return setting_controller.update_profile(
        preset_name, heatmap_steps, daily_goal, standing_height, sitting_height
    )


@setting_server.route("/profile_list")
def get_profile_list():
    """
    returns a list of available profiles

    Returns:
        string: serialized json either [{setting data}] or {"error":"..."}
    """

    return setting_controller.get_list_of_profiles()
