# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench  vertex tracker
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
import Part
import Draft


#----------


import math,os

import FreeCAD, Animation, PySide
from Animation import say,sayErr,sayexc
from  EditWidget import EditNoDialWidget
import Toucher
reload(Toucher)

__vers__='0.1 06.12.2015'
__dir__ = os.path.dirname(__file__)	


def createVertexTracker(name,src=None,filename="/tmp/tracker"):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyString","filename","Base","").filename=filename
	obj.addProperty("App::PropertyLink","src","Base","").src=src
	obj.addProperty("App::PropertyFloat","time","Base","").time=0

	_VertexTracker(obj)
	_ViewProviderVertexTracker(obj.ViewObject)
	return obj

class _VertexTracker(Animation._Actor):
	''' track the time/placement of src to filename '''

	def update(self):
		print "update VERTEX Tracker "
		self.run(self.obj2.src)
		print "done"

	def step(self,now):
		say("step "+str(now) + str(self))
		self.obj2.time=float(now)/100


	#-----------------------------------------

	def addpoint(self,point):
		try:
			self.threads
		except:
			self.threads={}
		fcount=len(self.threads)
		dist=1.5
		for f in self.threads:
			print f, self.threads[f]
			t=self.threads[f]
			if point.distanceToPoint(t[-1]) < dist:
				print "found"
				self.threads[f].append(point)
				return self.threads[f]
		print "not found"
		self.threads[fcount]=[point]
		return self.threads[fcount]


	def run(self,s):
		print s.Label
		print s.Shape
		print s.Shape.Vertexes
		for v in s.Shape.Vertexes:
			print "Point: ", v.Point
			self.addpoint(v.Point)
# 		print threads

	def show(self):
		for f in self.threads:
			print f
			for p in self.threads[f]:
				print "       ",p

	def gen(self):
		for f in self.threads:
			print f
			if  self.isOnePoint(self.threads[f]):
				p=FreeCAD.ActiveDocument.addObject("Part::Vertex","Vertex")
				p.Placement.Base=self.threads[f][0]
			else:
				Draft.makeWire(self.threads[f])

	def isOnePoint(self,f):
			if len(f)==0:
				return False
			sp=f[0]
			for p in f:
				if p <> sp:
					return False
			return True

	#----------------------------------------




class _ViewProviderVertexTracker(Animation._ViewProviderActor):

	def __init__(self,vobj):
		say(self)
		Animation._ViewProviderActor.__init__(self,vobj)
		self.attach(vobj)
 
	def getIcon(self):
		return '/usr/lib/freecad/Mod/Animation/' +'/icons/icon2.svg'
		return __dir__ +'/icons/icon2.svg'

	def attach(self,vobj):
		self.emenu=[["Show Path Data",self.Object.Proxy.show],["Generate Path",self.Object.Proxy.gen]]
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




