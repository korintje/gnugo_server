# -*- coding:utf-8 -*-
import platform, json, threading
from subprocess import Popen, PIPE
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

# Check host OS
pf = platform.system()
if pf == "Windows":
  CMD = [".\gnugo.exe", "--mode", "gtp"]
elif pf == "Darwin":
  CMD = ["gnugo", "--mode", "gtp"]
elif pf == "Linux":
  CMD = ["gnugo", "--mode", "gtp"]
else:
  CMD = ["gnugo", "--mode", "gtp"]

# Launch GNU Go program
GNUGO = Popen(CMD, encoding='utf-8', stdin=PIPE, stdout=PIPE)


# Simple HTTP server to communicate with GNU Go
class GoHandler(BaseHTTPRequestHandler):
    """Modified from: https://qiita.com/komorin0521/items/dfc02444a60180688e43"""

    """Need to solve CORS"""
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-type")
        self.end_headers()


    def do_POST(self):
        try:
            content_len = int(self.headers.get('content-length'))
            requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
            print(f"RequestBody: {requestBody}")
            command = requestBody["command"]

            # Get GNU Go response
            GNUGO.stdin.write(command + "\n")
            GNUGO.stdin.flush()
            lines = []
            while True:
                line = GNUGO.stdout.readline()
                lines.append(line)
                if line == "\n":
                    break

            # Respond as success (status code = 200)
            response = { 'status': 200, 'output': "\n".join(lines) }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
            # self.send_header("Access-Control-Allow-Headers", "Content-type")
            self.send_header('Access-Control-Allow-Origin', '*')
            # self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.end_headers()
            responseBody = json.dumps(response)
            print(f"ResponseBody: {responseBody}")
            self.wfile.write(responseBody.encode('utf-8'))

        except Exception as e:
            print("An error occured")
            print("The information of error is as following")
            print(type(e))
            print(e.args)
            print(e)
            response = { 'status' : 500, 'output' : 'API server error' }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            responseBody = json.dumps(response)
            self.wfile.write(responseBody.encode('utf-8'))


# GNU Go API server process
def launch_api_server(port):
    with HTTPServer(("", port), GoHandler) as httpd:
        print("GNU Go API serving at port", port)
        httpd.serve_forever()


# Main process
if __name__ == '__main__':
    API_PORT = 8085
    FILE_PORT = 8080
    threading.Thread(target=launch_api_server, args=(API_PORT,)).start()
    with HTTPServer(("", FILE_PORT), SimpleHTTPRequestHandler) as httpd:
        print("Static file serving at port", FILE_PORT)
        httpd.serve_forever()
        