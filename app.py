
import os
import hmac
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

GPS_API_KEY = os.environ.get("GPS_API_KEY", "")
latest_location = {
    "latitude": None,
    "longitude": None
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

        print(f"GPS received: {lat}, {lon}")
        return jsonify({"success": True})

    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid GPS coordinates"}), 400


@app.route("/location")
def get_location():
    return jsonify(latest_location)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
