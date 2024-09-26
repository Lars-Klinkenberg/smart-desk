import json
from bottle import Bottle, HTTPResponse, request

setting_server = Bottle()


@setting_server.put("/height/standing")
def change_default_standing_height():
    """
    changes the saved setting for standing height
    """
    standing_height = request.headers.get("standing_height", 115)

    if standing_height is None:
        return HTTPResponse(
            status=400,
            body=json.dumps({"error": "header standing_height is not defined"}),
        )

    return HTTPResponse(
        status=501,
        body=json.dumps({"error": "PUT /height/standing is not implemented"}),
    )


@setting_server.put("/height/sitting")
def change_default_sitting_height():
    """
    changes the saved setting for sitting height
    """
    sitting_height = request.headers.get("sitting_height", 115)

    if sitting_height is None:
        return HTTPResponse(
            status=400,
            body=json.dumps({"error": "header sitting_height is not defined"}),
        )
    return HTTPResponse(
        status=501, body=json.dumps({"error": "PUT /height/sitting is not implemented"})
    )


@setting_server.route("/heatmap")
def get_heatmap_steps():
    """
    returns the config of the heatmap steps
    """
    return HTTPResponse(
        status=501, body=json.dumps({"error": "GET /heatmap is not implemented"})
    )


@setting_server.put("/heatmap")
def change_heatmap_steps():
    """
    changes the saved setting for heatmap setps
    """
    heatmap_steps = request.headers.get("heatmap_steps", 60)

    if heatmap_steps is None:
        return HTTPResponse(
            status=400,
            body=json.dumps({"error": "header heatmap_steps is not defined"}),
        )

    return HTTPResponse(
        status=501, body=json.dumps({"error": "PUT /heatmap is not implemented"})
    )


@setting_server.get("/goal")
def get_daily_goal():
    """
    returns the daily goal
    """

    return HTTPResponse(
        status=501, body=json.dumps({"error": "GET /goal is not implemented"})
    )


@setting_server.put("/goal")
def change_daily_goal():
    """
    changes the saved daily goal
    """
    daily_goal = request.headers.get("daily_goal", None)

    if daily_goal is None:
        return HTTPResponse(
            status=400, body=json.dumps({"error": "header daily_goal is not defined"})
        )

    return HTTPResponse(
        status=501, body=json.dumps({"error": "PUT /goal is not implemented"})
    )


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

    return HTTPResponse(
        status=501, body=json.dumps({"error": "POST /profile is not implemented"})
    )


@setting_server.route("/profile")
def get_preset_by_name():
    """
    returns a profile by the preset_name
    """
    preset_name = request.headers.get("preset_name", None)

    if preset_name is None:
        return HTTPResponse(
            status=400, body=json.dumps({"error": "header preset_name is not defined"})
        )

    return HTTPResponse(
        status=501, body=json.dumps({"error": "POST /profile is not implemented"})
    )


@setting_server.route("/profile_list")
def get_profile_list():
    """
    returns a list of available profiles
    """

    return HTTPResponse(
        status=501, body=json.dumps({"error": "POST /profile is not implemented"})
    )
