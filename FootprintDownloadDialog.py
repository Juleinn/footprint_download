# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.1.0-0-g733bf3d)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class FootprintDownloadDialogFrame
###########################################################################

class FootprintDownloadDialogFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.serverStatusLabel = wx.StaticText( self, wx.ID_ANY, u"Server Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.serverStatusLabel.Wrap( -1 )

		bSizer1.Add( self.serverStatusLabel, 0, wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.startServerButton = wx.Button( self, wx.ID_ANY, u"Start Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.startServerButton, 0, wx.ALL, 5 )

		self.stopServerbutton = wx.Button( self, wx.ID_ANY, u"Stop Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.stopServerbutton, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


