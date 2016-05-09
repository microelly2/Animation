# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import math,os, time

import FreeCAD, FreeCADGui, Animation, PySide
from Animation import say,sayErr,sayexc
from EditWidget import EditWidget
from PySide import QtCore, QtGui


__vers__= '0.1'
__dir__ = os.path.dirname(__file__)	


Gui=FreeCADGui
App=FreeCAD


def createAnimationControlPanel(name='My_AnimationControlPanel',line1=[],line2=[],line3=[]):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyStringList","line1","Lines","").line1=line1
	obj.addProperty("App::PropertyStringList","line2","Lines","").line2=line2
	obj.addProperty("App::PropertyStringList","line3","Lines","").line3=line3
	
	# hide info
	#obj.setEditorMode("expressiontrafo", 2)
	_AnimationControlPanel(obj)
	_ViewProviderAnimationControlPanel(obj.ViewObject)
	return obj

class _AnimationControlPanel(Animation._Actor):

	def update(self):
		pass

	def step(self,now):
		pass


def controlPanelWidget(obj):

	w=QtGui.QWidget()
	w.setStyleSheet("QWidget { background-color: lightblue}\
			QDial { background-color: white}\
			QLabel { color: ;}\
			QPushButton { margin-right:0px;margin-left:0px;margin:0 px;padding:0px;;\
			background-color: lightblue;text-align:left;;padding:6px;padding-left:4px;color:brown; }")

	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	label=QtGui.QLabel("<center><big><b>*** Animation Control Panel ***</b></big></center>")
	layout = QtGui.QVBoxLayout()
	layout.addWidget(label)

	Wid= QtGui.QWidget()
	l2 = QtGui.QGridLayout()
	layout.addLayout(l2)

	lc=1
	rc=1
	for r in obj.line1:
		t= Gui.activeDocument().getObject(r)
		dd=t.Proxy.dialog(True)
		# dd.setStyleSheet("QLabel { color: #0000ff;}")
		l2.addWidget(dd,lc,rc)
		rc += 1
	lc=2
	rc=1
	for r in obj.line2:
		t= Gui.activeDocument().getObject(r)
		dd=t.Proxy.dialog(True)
		l2.addWidget(dd,lc,rc)
		rc += 1
	lc=3
	rc=1
	for r in obj.line3:
		t= Gui.activeDocument().getObject(r)
		dd=t.Proxy.dialog(True)
		l2.addWidget(dd,lc,rc)
		rc += 1

	pushButton02 = QtGui.QPushButton("close")
	pushButton02.clicked.connect(w.hide)
	layout.addWidget(pushButton02)
	w.setLayout(layout)
	return w

class _ViewProviderAnimationControlPanel(Animation._ViewProviderActor):

	def attach(self,vobj):
		say("VO attach " + str(vobj.Object.Label))
		vobj.Proxy = self
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		icon='/icons/controlpanel.png'
		self.iconpath = __dir__ + icon
		self.vers=__vers__
		return

	def setupContextMenu(self, obj, menu):
		cl=self.Object.Proxy.__class__.__name__
		action = menu.addAction("About " + cl)
		action.triggered.connect(self.showVersion)
		action = menu.addAction("Edit ...")
		action.triggered.connect(self.edit)

	def edit(self):
		say(self)
		self.dialog=controlPanelWidget(self.Object)
		self.dialog.show()

