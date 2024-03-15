import IPython
import json
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

    def read_config(self):
        pcb_filename = pcbnew.GetBoard().GetFileName()
        config_filename = os.path.dirname(pcb_filename) + "/.footprintdownloadrc"
        if not os.path.exists(config_filename):
            self.config = {
                "symbol_lib_filename":"",
                "footprint_lib_directory": "",
            }
        else:
            with open(config_filename, "r") as f:
                self.config = json.loads(f.read())

    def save_config(self):
        pcb_filename = pcbnew.GetBoard().GetFileName()
        config_filename = os.path.dirname(pcb_filename) + "/.footprintdownloadrc"
        print("writing config : ", self.config)
        with open(config_filename, "w") as f:
            f.write(json.dumps(self.config))

    def create_default_config(self):
        pcb_dir = os.path.dirname(pcbnew.GetBoard().GetFileName())
        # symbol file : check exist before create
        symbol_lib_filename = pcb_dir + "/footprint_download.kicad_sym"
        footprint_lib_directory = pcb_dir + "/footprint_download.pretty"
        if os.path.exists(symbol_lib_filename):
            wx.MessageBox(f"{symbol_lib_filename} already exists. Doing nothing")
        else: 
            symbol_lib_template = """(kicad_symbol_lib (version 20211014) (generator FootprintDownloader))"""
            with open(symbol_lib_filename, "w") as f:
                f.write(symbol_lib_template)

        if os.path.exists(footprint_lib_directory):
            wx.MessageBox(f"{footprint_lib_directory} already exists. Doing nothing")
        else:
            os.makedirs(footprint_lib_directory)

        # put only the relative paths in config
        self.config['symbol_lib_filename'] = "/footprint_download.kicad_sym"
        self.config['footprint_lib_directory'] = "/footprint_download.pretty"

    def Run(self):
        dialog = FootprintDownloadDialog(None)

        self.read_config()
        #IPython.embed(colors="neutral")
        dialog.symbolLibraryTextbox.SetValue(self.config["symbol_lib_filename"])
        dialog.footprintLibraryTextbox.SetValue(self.config["footprint_lib_directory"])

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
            # update config before serving data
            # we want full path here not relative
            pcbnew.footprintserver_config = {
                "symbol_lib_filename": os.path.dirname(pcbnew.GetBoard().GetFileName()) + self.config['symbol_lib_filename'],
                "footprint_lib_directory": os.path.dirname(pcbnew.GetBoard().GetFileName()) + self.config['footprint_lib_directory'],
            }
            if is_server_running():
                dialog.serverStatusLabel.SetLabel("Server is running")
                dialog.startServerButton.Enable(False)
                dialog.stopServerbutton.Enable(True)
                # disable configuration changes here 
                dialog.chooseFootprintLibraryButton.Enable(False)
                dialog.chooseSymbolLibraryButton.Enable(False)
                dialog.symbolLibraryTextbox.Enable(False)
                dialog.footprintLibraryTextbox.Enable(False)
                dialog.saveConfigButton.Enable(False)
                dialog.createDefaultConfigButton.Enable(False)

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
            # disable configuration changes here 
            dialog.chooseFootprintLibraryButton.Enable(True)
            dialog.chooseSymbolLibraryButton.Enable(True)
            dialog.symbolLibraryTextbox.Enable(True)
            dialog.footprintLibraryTextbox.Enable(True)
            dialog.saveConfigButton.Enable(True)
            dialog.createDefaultConfigButton.Enable(True)

        def save_config_handler(_):
            self.save_config()
            wx.MessageBox("Config saved")

        def create_default_config_handler(_):
            self.create_default_config()
            dialog.symbolLibraryTextbox.SetValue(self.config["symbol_lib_filename"])
            dialog.footprintLibraryTextbox.SetValue(self.config["footprint_lib_directory"])

            wx.MessageBox("Default config created. Don't forget to save")

        def choose_symbol_library_handler(_):
            wx.MessageBox("Not implemented")

        def choose_footprint_library_handler(_):
            wx.MessageBox("Not implemented")

        dialog.startServerButton.Bind(wx.EVT_BUTTON, start_server_handler)
        dialog.stopServerbutton.Bind(wx.EVT_BUTTON, stop_server_handler)
        dialog.saveConfigButton.Bind(wx.EVT_BUTTON, save_config_handler)
        dialog.createDefaultConfigButton.Bind(wx.EVT_BUTTON, create_default_config_handler)
        dialog.chooseFootprintLibraryButton.Bind(wx.EVT_BUTTON, choose_footprint_library_handler)
        dialog.chooseSymbolLibraryButton.Bind(wx.EVT_BUTTON, choose_symbol_library_handler)

        if is_server_running():
            dialog.serverStatusLabel.SetLabel("Server is running.")
            dialog.startServerButton.Enable(False)
            dialog.stopServerbutton.Enable(True)
            # disable configuration changes here 
            dialog.chooseFootprintLibraryButton.Enable(False)
            dialog.chooseSymbolLibraryButton.Enable(False)
            dialog.symbolLibraryTextbox.Enable(False)
            dialog.footprintLibraryTextbox.Enable(False)
            dialog.saveConfigButton.Enable(False)
            dialog.createDefaultConfigButton.Enable(False)
        else:
            dialog.serverStatusLabel.SetLabel("Server is not running")
            dialog.startServerButton.Enable(True)
            dialog.stopServerbutton.Enable(False)
            # disable configuration changes here 
            dialog.chooseFootprintLibraryButton.Enable(True)
            dialog.chooseSymbolLibraryButton.Enable(True)
            dialog.symbolLibraryTextbox.Enable(True)
            dialog.footprintLibraryTextbox.Enable(True)
            dialog.saveConfigButton.Enable(True)
            dialog.createDefaultConfigButton.Enable(True)

        dialog.Show()



print("registering plugin")
FootprintDownload().register()
