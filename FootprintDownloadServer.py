# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
import json

hostName = "localhost"
serverPort = 8080

class FootprintDownloadServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)
        data = json.loads(data)
        print(data)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), FootprintDownloadServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()

    webServer.server_close()
    print("Server stopped.")
