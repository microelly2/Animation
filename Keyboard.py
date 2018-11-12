# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench keyboard sensor
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
import Part

from  EditWidget import EditNoDialWidget


import math,os

import FreeCAD, Animation, PySide
from Animation import say,sayErr,sayexc

__vers__='0.1 5.12.2015'
__dir__ = os.path.dirname(__file__)	


#----------------------


from PySide import QtGui,QtCore
import FreeCAD,tools,sys
from tools import *


App=FreeCAD
Gui=FreeCADGui

class EventFilter(QtCore.QObject):

	def __init__(self,ctl=None):
		QtCore.QObject.__init__(self)
		self.V=ctl.src
		self.ctl=ctl

		self.keypressed=False
		self.stack=[]
		self.editmode=False
		self.pos=None
		#self.debug=False
		self.debug=FreeCAD.ParamGet('User parameter:Plugins').GetBool('EventFilterDebug')
		self.debug=True
		
	def eventFilter(self, o, e):
		z=str(e.type())
		try:
			# not used events
			if z == 'PySide.QtCore.QEvent.Type.ChildAdded' or \
					z == 'PySide.QtCore.QEvent.Type.ChildRemoved'or \
					z == 'PySide.QtCore.QEvent.Type.User'  or \
					z == 'PySide.QtCore.QEvent.Type.Paint' or \
					z == 'PySide.QtCore.QEvent.Type.LayoutRequest' or\
					z == 'PySide.QtCore.QEvent.Type.UpdateRequest'   :
				return QtGui.QWidget.eventFilter(self, o, e)
			
			if z == 'PySide.QtCore.QEvent.Type.HoverMove' :
				self.pos=e.pos()
			if z == 'PySide.QtCore.QEvent.Type.KeyPress':
				# ignore editors
				if self.editmode:
					return QtGui.QWidget.eventFilter(self, o, e)
				
				# only first time key pressed
				if not self.keypressed:
					text=e.text()
					if 0 or text !='':
						self.keypressed=True
						key=''
						if e.modifiers() & QtCore.Qt.SHIFT:
							#FreeCAD.Console.PrintMessage("SHIFT ")
							key +="SHIFT+"
						if e.modifiers() & QtCore.Qt.CTRL:
							#FreeCAD.Console.PrintMessage("CTRL ")
							key +="CTRL+"
						if e.modifiers() & QtCore.Qt.ALT:
							#FreeCAD.Console.PrintMessage("ALT ")
							key +="ALT+"
						key +=PySide.QtGui.QKeySequence(e.key()).toString() 
						FreeCAD.Console.PrintMessage(" "+str(key)  +" \n" )
						
						pos=self.pos
						#if e.key()== QtCore.Qt.Key_F10:
						#	key += "F10#"

						if pos:
							if self.debug: FreeCAD.Console.PrintMessage( key + " at mouse position: " +str(pos) + "\n")
							say(pos.x())
							say(pos.y())
							step=1
							if key == 'F':
								self.V.Placement.Base.x -= step
							elif key == 'G':
								self.V.Placement.Base.x += step
							elif key == 'T':
								self.V.Placement.Base.y += step
							elif key == 'V':
								self.V.Placement.Base.y -= step
							elif key == 'Z':
								self.V.Placement.Base.x += step
								self.V.Placement.Base.y += step
							elif key == 'R':
								self.V.Placement.Base.x -= step
								self.V.Placement.Base.y += step
							elif key == 'B':
								self.V.Placement.Base.x += step
								self.V.Placement.Base.y -= step
							elif key == 'C':
								self.V.Placement.Base.x -= step
								self.V.Placement.Base.y -= step

								
							elif key == 'H':
								s=Gui.Selection.getSelection()
								try:
									ll=Gui.Selection.getSelectionEx()
									pts=ll[0].PickedPoints
									V.Placement.Base.x=pts[0].x
									V.Placement.Base.y=pts[0].y
								except:
									try:
										say("error 11")
										self.V.Placement.Base.x=s[0].Placement.Base.x
										self.V.Placement.Base.y=s[0].Placement.Base.y
									except:
										say("error 2")
										pass
							self.ctl.Placement=self.V.Placement
							App.ActiveDocument.recompute()
						else:
							self.keypressed=False
			if z == 'PySide.QtCore.QEvent.Type.KeyRelease':
				if self.keypressed:
					pass
				self.keypressed=False
		except:
			sayexc()
		try:
			return QtGui.QWidget.eventFilter(self, o, e)
		except:
			return None

def start(V=None):
	mw=QtGui.qApp
	ef=EventFilter(V)
	FreeCAD.keyfilter=ef
	mw.installEventFilter(ef)

def stop():
	mw=QtGui.qApp
	ef=FreeCAD.keyfilter
	mw.removeEventFilter(ef)

#------------------------

def createKeyboard(name,src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","src","Base","").src=src
	obj.addProperty("App::PropertyFloat","time","Base","").time=0
	obj.addProperty("App::PropertyLinkList","followers","Base","")
	obj.addProperty("App::PropertyPlacement","Placement","Results","")

	_Keyboard(obj)
	_ViewProviderKeyboard(obj.ViewObject)
	return obj

class _Keyboard(Animation._Actor):

	def update(self):
		return

	def step(self,now):
		return

class _ViewProviderKeyboard(Animation._ViewProviderActor):
 
	def getIcon(self):
		return __dir__ +'/icons/icon1.svg'

	def attach(self,vobj):
		self.emenu=[["start",self.start],["stop",self.stop]]
		self.cmenu=self.emenu
		say("attach " + str(vobj.Object.Label))
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		return

	def edit(self):
		self.dialog=EditNoDialWidget(self,self.emenu)
		self.dialog.show()

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "Animation" + cl +" Node\nVersion " + __vers__ )

	def dialer(self):
		self.obj2.time=float(self.widget.dial.value())/100
		FreeCAD.ActiveDocument.recompute()
	
	def start(self):
		say("start sensor")
		mw=QtGui.qApp
		
		ef=EventFilter(self.obj2)
		FreeCAD.keyfilter=ef
		mw.installEventFilter(ef)
	
	def stop(self):
		say("stop sensor")
		
		mw=QtGui.qApp
		ef=FreeCAD.keyfilter
		mw.removeEventFilter(ef)
		say("stopped")

		


