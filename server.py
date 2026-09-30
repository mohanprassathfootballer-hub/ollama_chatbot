import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
UI_FILE = Path(__file__).with_name("ollama-chatbot-ui.html")


class ChatBotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/ollama-chatbot-ui.html"):
            try:
                content = UI_FILE.read_bytes()
            except OSError:
                self.send_error(500, "Chat UI could not be loaded")
                return
            self._respond(200, "text/html; charset=utf-8", content)
        elif self.path == "/api/tags":
            self._proxy_ollama("GET", "/api/tags")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return
        self._proxy_ollama("POST", "/api/chat")

    def _proxy_ollama(self, method, path):
        body = None
        if method == "POST":
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length)

        request = Request(
            f"{OLLAMA_HOST}{path}",
            data=body,
            headers={"Content-Type": "application/json"},
            method=method,
        )
        try:
            with urlopen(request, timeout=300) as response:
                self._respond(
                    response.status,
                    response.headers.get("Content-Type", "application/json"),
                    response.read(),
                )
        except HTTPError as error:
            self._respond(
                error.code,
                error.headers.get("Content-Type", "application/json"),
                error.read(),
            )
        except URLError as error:
            self._send_json(502, {"error": f"Could not reach Ollama: {error.reason}"})

    def _send_json(self, status, data):
        content = json.dumps(data).encode("utf-8")
        self._respond(status, "application/json; charset=utf-8", content)

    def _respond(self, status, content_type, content):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), ChatBotHandler)
    print(f"Chat Bot listening on port {port}; Ollama host: {OLLAMA_HOST}")
    server.serve_forever()


if __name__ == "__main__":
    main()