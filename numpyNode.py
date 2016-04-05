# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__vers__="XX13.03.2016  0.0"


import sympy
from sympy import Point3D,Plane

import PySide
from PySide import QtCore, QtGui

import sys
import os
import random

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'


from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui


import numpy as np
import time

import FreeCAD



__dir__ = os.path.dirname(__file__)	

def sayd(s):
	if hasattr(FreeCAD,'animation_debug'):
		pass
		FreeCAD.Console.PrintMessage(str(s)+"\n")

def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")

def sayErr(s):
		FreeCAD.Console.PrintError(str(s)+"\n")



class _NP(object):

	def __init__(self,obj,icon='/icons/animation.png'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		_ViewProviderNP(obj.ViewObject,icon) 


	def initialize(self):
		say("initialize ...")

	def onChanged(self,obj,prop):
		say("onChanged " + str(self))
		say(obj)
		say(prop)
		say(obj.getPropertyByName(prop))

	def onBeforeChange(self,obj,prop):
		say("on Before Changed " )
		say(obj.Label)
		say(prop)
		say (obj.getPropertyByName(prop))


	def execute(self,obj):

		src=obj.sourceObject
		

		exec("inTime=np.array(src.sourceValues)")
		import numpy as np
		atts=[1,2,3]

		for i in atts:
			print i
			exec('in'+str(i)+"=np.array(src.source"+str(i)+"Values)")

		attos=range(10)
		for i in attos:
			try:
				print i
				r=eval(obj.getPropertyByName("expression" +str(i)))
				print r
				exec("obj.out" + str(i)+"=" +str(list(r)))
			except:
				pass

		r=eval(obj.getPropertyByName("expressionTime"))
		print r
		exec("obj.outTime=" +str(list(r)))


		return


	def attach(self,vobj):
		self.Object = vobj.Object

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def onDocumentRestored(self, fp):
		say(["onDocumentRestored",fp,fp.Label])

class _ViewProviderNP():
 
	def __init__(self,vobj,icon='/icons/icon1.svg'):
		print "viewwproergrger"
		self.iconpath = icon
		print self.iconpath
		self.Object = vobj.Object
		vobj.Proxy = self
		self.cmenu=[]
		self.emenu=[]

		self.vers=__vers__
 
	def getIcon(self):
		return  __dir__+ '/icons/icon2.svg'



def createNP(base=False):
	print "create Numpy Filter ..."
	obj=FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython','Numpy')

	obj.addProperty('App::PropertyBool','record',"Base",'true record, false no record data')
	obj.addProperty('App::PropertyLink','sourceObject',"Base")

	for i in range(10):
		obj.addProperty('App::PropertyString','label'+str(i),"out "+str(i))
		obj.addProperty('App::PropertyString','expression'+str(i),"out "+str(i))
		obj.addProperty('App::PropertyFloatList','out'+str(i),"out "+str(i))

	obj.addProperty('App::PropertyString','expressionTime',"Time")
	obj.addProperty('App::PropertyFloatList','outTime',"Time")
	obj.expressionTime='inTime'
	
	_NP(obj,'/icons/bounder.png')
	_ViewProviderNP(obj.ViewObject,__dir__+ '/icons/icon2.svg') 


	return obj







