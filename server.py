from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json

HOST = "0.0.0.0"
PORT = 8000
WEBPAGE = Path(__file__).with_name("index.html")

# Latest GPS reading received from the ESP32
latest_location = {
    "latitude": None,
    "longitude": None
}


class BusTrackingHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        print("DEBUG GET PATH:", repr(self.path))
        if self.path.split("?")[0] == "/location":
            self.send_json(200, latest_location)
            return

        if self.path in ("/", "/index.html"):
            if not WEBPAGE.exists():
                message = (
                    "Server is running, but index.html has not been created yet."
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(message)))
                self.end_headers()
                self.wfile.write(message)
                return

            body = WEBPAGE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        global latest_location

        if self.path != "/gps":
            self.send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 4096:
                self.send_json(400, {"error": "Invalid request body size"})
                return

            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            latitude = float(payload["latitude"])
            longitude = float(payload["longitude"])

            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                self.send_json(400, {"error": "Coordinates out of range"})
                return

            latest_location = {
                "latitude": latitude,
                "longitude": longitude
            }

            print(
                f"GPS received: latitude={latitude}, longitude={longitude}"
            )
            self.send_json(200, {"status": "ok", "received": latest_location})

        except (ValueError, KeyError, json.JSONDecodeError):
            self.send_json(400, {"error": "Expected valid latitude and longitude"})
        except Exception as exc:
            print("Request error:", exc)
            self.send_json(500, {"error": "Internal server error"})

    def log_message(self, format_string, *args):
        print(f"{self.client_address[0]} - {format_string % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), BusTrackingHandler)
    print(f"Bus tracking server running on port {PORT}")
    print("On this laptop: http://127.0.0.1:8000")
    print("On your hotspot network: http://10.31.20.38:8000")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping bus tracking server...")
    finally:
        server.server_close()
