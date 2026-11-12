"""Local Sauti server for a datathon demo."""

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
from pathlib import Path
from threading import Lock

from sauti_model import load_responder


ROOT = Path(__file__).resolve().parent
ROUTES = {"/": ("index.html", "text/html; charset=utf-8"),
          "/app.js": ("app.js", "text/javascript; charset=utf-8"),
          "/app.css": ("app.css", "text/css; charset=utf-8")}


def handler_for(respond):
    inference_lock = Lock()

    class Handler(BaseHTTPRequestHandler):
        def send_content(self, status, content, content_type):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                self.wfile.write(content)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def send_json(self, status, data):
            self.send_content(status, json.dumps(data, ensure_ascii=False).encode(), "application/json")

        def do_GET(self):
            route = ROUTES.get(self.path)
            if route is None:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            name, content_type = route
            self.send_content(HTTPStatus.OK, (ROOT / "web" / name).read_bytes(), content_type)

        def do_POST(self):
            if self.path != "/api/reply":
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            if self.headers.get_content_type() != "application/json":
                self.send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Ombi halikupokelewa."})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 4096:
                    raise ValueError("Invalid request length")
                data = json.loads(self.rfile.read(length))
                message = data.get("message") if isinstance(data, dict) else None
                if not isinstance(message, str) or not 1 <= len(message.strip()) <= 280:
                    raise ValueError("Invalid message")
            except (ValueError, UnicodeError):
                self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Andika ombi lenye herufi 1 hadi 280."})
                return
            try:
                with inference_lock:
                    result = respond(message.strip())
            except Exception:
                logging.exception("Sauti inference failed")
                self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Jibu halipatikani kwa sasa. Jaribu tena."})
                return
            payload = result if isinstance(result, dict) else {"reply": result}
            self.send_json(HTTPStatus.OK, payload)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Datathon repository checkout")
    parser.add_argument("--checkpoint", type=Path, required=True, help="Team's trusted joint_model.pt")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if not (args.repo / "train_joint_intent_slot.py").is_file() or not args.checkpoint.is_file():
        parser.error("Provide the datathon repository and the downloaded checkpoint.")
    print("Loading Sauti model…", flush=True)
    respond = load_responder(args.repo.resolve(), args.checkpoint.resolve())
    with ThreadingHTTPServer((args.host, args.port), handler_for(respond)) as server:
        print(f"Sauti is ready at http://{args.host}:{args.port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
