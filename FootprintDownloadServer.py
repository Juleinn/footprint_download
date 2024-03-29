# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
import json
from .SymbolLibraryMerge import *
import time
import pcbnew

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

        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)
        data = json.loads(data)

        # validate request
        if not hasattr(pcbnew, "footprintserver_config"):
            print("Missing server config")
            self.send_response(500)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes("Server configuration is lacking. Please reconfigure", "utf-8"))
            return
        else: 
            print("self does have atrtibute config")

        self.config = getattr(pcbnew, "footprintserver_config")
        print(self.config)
        
        if not "filename" in data.keys():
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

        # extract mouser archive
        # give some time for download to complete first
        time.sleep(1)
        filenames = extract_archive(data["filename"])
        if filenames == None:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes("No files could be extracted from archive", "utf-8"))
            return
            
        symbol_lib, footprints, model_3d = (filenames)

        print(f"extracted {symbol_lib}, {footprints}, {model_3d} from archive")
        try:
            # merge in place, no copy, yolo (also projects are meant to be version controlled for catastrophic failure)
            merge_symbol_libraries(self.config["symbol_lib_filename"], symbol_lib)
        except:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes("Could not merge footprint/symbol into libraries", "utf-8"))
            return

        # need to copy footprint file over and 3D file too maybe
        for footprint in footprints:
            if model_3d != "":
                print("Updating 3d model in place")
                update_3dmodel_inplace(footprint, model_3d)
            shutil.copy(footprint, self.config["footprint_lib_directory"])
        if model_3d != "":
            shutil.copy(model_3d, self.config["footprint_lib_directory"])

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), FootprintDownloadServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()

    webServer.server_close()
    print("Server stopped.")
