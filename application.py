#!/usr/bin/python
from flask import Flask, json, jsonify, request, make_response

# Return an application/json request with jsonified response.
application = Flask(__name__)


def jsonify_response(result, status_code):
    response = make_response(jsonify(result))
    response.headers["Content-type"] = "application/json"
    response.status_code = status_code
    return response


def invalid_json():
    response = jsonify_response(
        {"error": "Could not decode request: JSON parsing failed"}, 400
    )
    response.headers["Content-Type"] = "application/json"
    return response


def valid_json(shows):
    response = jsonify_response({"response": shows}, 200)
    response.headers["Content-Type"] = "application/json"
    return response


list_of_shows = []
post_sent = 0


@application.route("/", methods=["GET", "POST"])
def homePage():

    global list_of_shows
    global post_sent

    if request.method == "POST":
        list_of_shows = []
        post_sent = 1

        try:
            data = json.loads(request.data)
        except ValueError as e:
            response = invalid_json()
            return response
        else:
            if data.get("payload"):
                for x in data["payload"]:
                    if x.get("drm"):
                        if x["episodeCount"] > 0:
                            show = {
                                "title": x["title"],
                                "image": x["image"]["showImage"],
                                "slug": x["slug"],
                            }
                            list_of_shows.insert(len(list_of_shows), show)
                response = valid_json(list_of_shows)
                return response
            else:
                response = invalid_json()
                return response
    else:
        if len(list_of_shows) == 0 and post_sent == 0:
            return "Waiting for POST request. Once the POST request is sent, refresh the page to see the results."
        else:
            response = valid_json(list_of_shows)
            return response


if __name__ == "__main__":
    application.run()
