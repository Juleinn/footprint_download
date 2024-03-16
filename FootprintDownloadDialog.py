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

class FootprintDownloadDialogFrame ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 755,368 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.serverStatusLabel = wx.StaticText( self, wx.ID_ANY, u"Server Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.serverStatusLabel.Wrap( -1 )

		bSizer10.Add( self.serverStatusLabel, 0, wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.startServerButton = wx.Button( self, wx.ID_ANY, u"Start Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.startServerButton, 0, wx.ALL, 5 )

		self.stopServerbutton = wx.Button( self, wx.ID_ANY, u"Stop Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.stopServerbutton, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer2, 0, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"symbol library   :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer21.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.symbolLibraryTextbox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.symbolLibraryTextbox, 1, wx.ALL, 5 )

		self.chooseSymbolLibraryButton = wx.Button( self, wx.ID_ANY, u"Choose", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.chooseSymbolLibraryButton, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer21, 0, wx.EXPAND, 5 )

		bSizer211 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"footprint library :", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer211.Add( self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.footprintLibraryTextbox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.footprintLibraryTextbox, 1, wx.ALL, 5 )

		self.chooseFootprintLibraryButton = wx.Button( self, wx.ID_ANY, u"Choose", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer211.Add( self.chooseFootprintLibraryButton, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer211, 0, wx.EXPAND, 5 )

		bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )

		self.createDefaultConfigButton = wx.Button( self, wx.ID_ANY, u"Create Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2111.Add( self.createDefaultConfigButton, 0, wx.ALL, 5 )

		self.saveConfigButton = wx.Button( self, wx.ID_ANY, u"Save Config", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2111.Add( self.saveConfigButton, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer2111, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer10.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( bSizer10, 1, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Server will run when window is closed", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer11.Add( self.m_staticText6, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.closeButton = wx.Button( self, wx.ID_CANCEL, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.closeButton, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer1.Add( bSizer11, 0, wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


