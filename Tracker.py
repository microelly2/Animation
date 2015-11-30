# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench tracker
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
import Part

#----------


import math,os

import FreeCAD, Animation, PySide
from Animation import say,sayErr,sayexc
from  EditWidget import EditNoDialWidget

__vers__='0.3 30.11.2015'
__dir__ = os.path.dirname(__file__)	


def createTracker(name,src=None,filename="/tmp/tracker"):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyString","filename","Base","").filename=filename
	obj.addProperty("App::PropertyLink","src","Base","").src=src
	obj.addProperty("App::PropertyFloat","time","Base","").time=0

	_Tracker(obj)
	_ViewProviderTracker(obj.ViewObject)
	return obj

class _Tracker(Animation._Actor):
	''' track the time/placement of src to filename '''

	def update(self):
		try:
			self.path
		except:
			self.path=[]
		if (self.obj2.src.time==0):
			f = open(self.obj2.filename + "_out.txt",'w')
		else:
			f = open(self.obj2.filename + "_out.txt",'a')
		f.write("# " + str(self.obj2.src.time) +" " +str(self.obj2.src.Placement)+'\n') # python will convert \n to os.linesep
		b=self.obj2.src.Placement.Base
		r=self.obj2.src.Placement.Rotation.Axis
		a=self.obj2.src.Placement.Rotation.Angle
		l=' '.join(str(k) for k in [self.obj2.src.time,b.x,b.y,b.z,r.x,r.y,r.z,a])
		f.write(l +"\n")
		f.close()
		self.path.append(self.obj2.src.Placement.Base)


class _ViewProviderTracker(Animation._ViewProviderActor):
 
	def getIcon(self):
		return __dir__ +'/icons/icon2.svg'

	def attach(self,vobj):
		self.emenu=[["Show Path",self.showpath]]
		self.cmenu=[]
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

	def showpath(self):
		''' path as Part.polygon '''
		FreeCAD.s=self
		points=self.Object.Proxy.path
		for p in self.Object.Proxy.path:
			say(str(p))
		pp=Part.makePolygon(points)
		Part.show(pp)
		FreeCAD.ActiveDocument.recompute()
		return FreeCAD.activeDocument().ActiveObject


