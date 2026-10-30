
import os
import hmac
import time
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

GPS_API_KEY = os.environ.get("GPS_API_KEY", "")
GPS_TIMEOUT = 15

latest_location = {
    "latitude": None,
    "longitude": None,
    "updated_at": None
}


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/gps", methods=["POST"])
def receive_gps():
    if not GPS_API_KEY:
        return jsonify({"error": "Server API key is not configured"}), 503

    supplied_key = request.headers.get("X-API-Key", "")

    if not hmac.compare_digest(supplied_key, GPS_API_KEY):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}

    try:
        lat = float(data["latitude"])
        lon = float(data["longitude"])

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("Invalid coordinates")

        latest_location["latitude"] = lat
        latest_location["longitude"] = lon
        latest_location["updated_at"] = int(time.time())

        print(f"GPS received: {lat}, {lon}")

        return jsonify({"success": True})

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid GPS coordinates"}), 400


@app.route("/location")
def get_location():
    updated_at = latest_location["updated_at"]

    if updated_at is None:
        age_seconds = None
        is_online = False
    else:
        age_seconds = max(0, int(time.time()) - updated_at)
        is_online = age_seconds <= GPS_TIMEOUT

    return jsonify({
        "latitude": latest_location["latitude"],
        "longitude": latest_location["longitude"],
        "updated_at": updated_at,
        "age_seconds": age_seconds,
        "is_online": is_online
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/manifest.webmanifest")
def manifest():
    response = send_from_directory(
        ".",
        "manifest.webmanifest",
        mimetype="application/manifest+json"
    )
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/sw.js")
def service_worker():
    response = send_from_directory(
        ".",
        "sw.js",
        mimetype="application/javascript"
    )
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/icons/<path:filename>")
def app_icons(filename):
    return send_from_directory("icons", filename)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
