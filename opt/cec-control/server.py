from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import subprocess
import time
import hmac

TOKEN = "GENERATE_A_SECURE_RANDOM_TOKEN_AND_PLACE_IT_HERE"
PORT = 8765
CEC_DEVICE = "/dev/cec0"

COMMANDS = {
    "on": ["cec-ctl", "-d", CEC_DEVICE, "--active-source", "phys-addr=4.1.0.0"],
    "off": ["cec-ctl", "-d", CEC_DEVICE, "--to", "5", "--standby"],
    "volume_up": ["cec-ctl", "-d", CEC_DEVICE, "--to", "5", "--user-control-pressed=ui-cmd=volume-up"],
    "volume_down": ["cec-ctl", "-d", CEC_DEVICE, "--to", "5", "--user-control-pressed=ui-cmd=volume-down"],
    "mute": ["cec-ctl", "-d", CEC_DEVICE, "--to", "5", "--user-control-pressed=ui-cmd=mute"],
}

UI_COMMANDS = {"volume_up", "volume_down", "mute"}


class CECHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/command":
            self.send_error(404)
            return

        supplied_token = self.headers.get("Authorization", "")
        if not hmac.compare_digest(supplied_token, f"Bearer {TOKEN}"):
            self.send_error(401)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length))
            command = data.get("command")

            if command not in COMMANDS:
                self.send_error(400, "Unknown command")
                return

            subprocess.run(
                COMMANDS[command],
                check=True,
                timeout=5,
                capture_output=True,
                text=True
            )

            if command in UI_COMMANDS:
                time.sleep(0.15)
                subprocess.run(
                    ["cec-ctl", "-d", CEC_DEVICE, "--to", "5", "--user-control-released"],
                    check=True,
                    timeout=5,
                    capture_output=True,
                    text=True
                )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')

        except Exception as error:
            print(f"CEC error: {error}")
            self.send_error(500, "CEC command failed")

    def log_message(self, format, *args):
        print(format % args)


server = ThreadingHTTPServer(("0.0.0.0", PORT), CECHandler)
print(f"CEC control listening on port {PORT}")
server.serve_forever()
