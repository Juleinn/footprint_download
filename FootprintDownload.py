import socket
import pcbnew
import os
from .FootprintDownloadDialog import FootprintDownloadDialogFrame
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import wx
from .FootprintDownloadServer import FootprintDownloadServer

HOSTNAME = "localhost"
PORT = 2222

class FootprintDownloadDialog(FootprintDownloadDialogFrame):
    def __init__(self, parent):
        super().__init__(parent)

def threadfunc():
    while True:
        print("threading hard")
        time.sleep(1)


def is_server_running():
    # this is a brittle and hacky way to persist information 
    # about the server thread running because we want to keep thread 
    # running when pcbnew is closed (for instance for working
    # in eeschema or for downloading footprints while pcbnew closed)
    try:
        if pcbnew.footprintdownload_server != None:
            print("server is running")
            return True
        else:
            print("Server is not running")
            return False
    except:
        print("server is not running")
        return False

class FootprintDownload(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "footprint_download"
        self.category = "import"
        self.show_toolbar_button = "true"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.description = "A tool for downloading footprints and symbols from distributor sites"

    def Run(self):
        dialog = FootprintDownloadDialog(None)

        def start_server_handler(_):
            if is_server_running():
                print("Server is already running. This is an error.")
                return 

            pcbnew.footprintdownload_server = HTTPServer((HOSTNAME, PORT), FootprintDownloadServer)
            def server_threadfunc():
                print("server started")
                pcbnew.footprintdownload_server.serve_forever()
                print("server stopped")

            threading.Thread(target=server_threadfunc).start()
            time.sleep(1) # give 1s for the server to start before updating UI accordingly
            pcbnew.footprintdownload_server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if is_server_running():
                dialog.serverStatusLabel.SetLabel("Server is running")
                dialog.startServerButton.Enable(False)
                dialog.stopServerbutton.Enable(True)

        def stop_server_handler(_):
            if not is_server_running():
                dialog.serverStatusLabel.SetLabel("Server is not running. This is an error")
                return 
            
            pcbnew.footprintdownload_server.shutdown()
            #
            # wipe the data to show server no longer running
            pcbnew.footprintdownload_server = None

            dialog.serverStatusLabel.SetLabel("Server stopped.")
            dialog.startServerButton.Enable(True)
            dialog.stopServerbutton.Enable(False)

        dialog.startServerButton.Bind(wx.EVT_BUTTON, start_server_handler)
        dialog.stopServerbutton.Bind(wx.EVT_BUTTON, stop_server_handler)

        if is_server_running():
            dialog.serverStatusLabel.SetLabel("Server is running.")
            dialog.startServerButton.Enable(False)
            dialog.stopServerbutton.Enable(True)
        else:
            dialog.serverStatusLabel.SetLabel("Server is not running")
            dialog.startServerButton.Enable(True)
            dialog.stopServerbutton.Enable(False)

        dialog.Show()



print("registering plugin")
FootprintDownload().register()
