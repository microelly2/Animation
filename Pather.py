# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench pather
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
import Part

from  EditWidget import EditWidget


import math,os

import FreeCAD, Animation, PySide
from Animation import say,sayErr,sayexc

__vers__='0.1 3.12.2015'
__dir__ = os.path.dirname(__file__)	


def createPather(name='My Pather',src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","src","Base","").src=src
	obj.addProperty("App::PropertyFloat","time","Base","").time=0

	obj.addProperty("App::PropertyLinkList","followers","Base","")
	obj.addProperty("App::PropertyPlacement","Placement","Results","")

	_Pather(obj)
	_ViewProviderPather(obj.ViewObject)
	return obj

class _Pather(Animation._Actor):
	''' placement from path '''

	def update(self):
		try:
			self.path
		except:
			self.path=[]
		
		# w=App.ActiveDocument.BSpline003
		#pl=[]
		#for n in range(101):
		#	kk=w.Shape.LastParameter/100*n
		#	p=w.Shape.valueAt(kk)
		#	pl.append(p)
		#
		#w=Draft.makeWire(pl)
		w=self.obj2.src
		kk=w.Shape.LastParameter*self.obj2.time
		p=w.Shape.valueAt(kk)
		self.obj2.Placement.Base=p
		if self.obj2.followers:
			for f in self.obj2.followers:
		#	FreeCAD.ActiveDocument.Ergebnis.Proxy.execute(FreeCAD.ActiveDocument.Ergebnis)
				f.Proxy.execute(f)

	def step(self,now):
			say("step "+str(now) + str(self))
			self.obj2.time=float(now)/100



class _ViewProviderPather(Animation._ViewProviderActor):
 
	def getIcon(self):
		return __dir__ +'/icons/pather.png'

	def attach(self,vobj):
		self.emenu=[]
		self.cmenu=[]
		say("attach " + str(vobj.Object.Label))
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		icon='/icons/combiner.png'
		self.iconpath = __dir__ + icon
		self.vers=__vers__
		return

	def edit(self):
		self.dialog=EditWidget(self,self.emenu)
		self.dialog.show()

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "Animation" + cl +" Node\nVersion " + __vers__ )

	def dialer(self):
		self.obj2.time=float(self.widget.dial.value())/100
		FreeCAD.ActiveDocument.recompute()


