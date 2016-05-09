# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__vers__="08.04.2016  0.2"

import say
reload(say)
from say import *

import sys
import os
import random
import numpy as np
import time

__dir__ = os.path.dirname(__file__)	

import Animation

class _NP(Animation._Actor):

	def __init__(self,obj,icon='/icons/animation.png'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		_ViewProviderNP(obj.ViewObject) 


	def execute(self,obj):

		src=obj.sourceObject
		if src.sourceValues<>[]:
			exec("inTime=np.array(src.sourceValues)")
		else:
			inTime=[]

		atts=[1,2,3]
		for i in atts:
			exec('in'+str(i)+"=np.array(src.source"+str(i)+"Values)")

		attos=range(10)
		for i in attos:
			try:
				e=obj.getPropertyByName("expression" +str(i))
				if e <>'':
					r=eval(e)
					exec("obj.out" + str(i)+"=" +str(list(r)))
				else:
					exec("obj.out" + str(i)+"=[]")
			except:
				sayexc(str(i)+ "!"+obj.getPropertyByName("expression" +str(i))+"!")

		r=eval(obj.getPropertyByName("expressionTime"))
		exec("obj.outTime=" +str(list(r)))



class _ViewProviderNP(Animation._ViewProviderActor):


	def __init__(self,vobj):
		self.attach(vobj)

	def attach(self,vobj):
		self.emenu=[]
		self.cmenu=[]
		self.Object = vobj.Object
		vobj.Proxy = self
		self.vers=__vers__

 
	def getIcon(self):
		return  __dir__+ '/icons/icon2.svg'

	def createDialog(self):
		pass

	def setupContextMenu(self, obj, menu):
		pass



def createNP(base=False):

	obj=FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython','Numpy')
	obj.addProperty('App::PropertyLink','sourceObject',"Base")

	for i in range(10):
		obj.addProperty('App::PropertyString','label'+str(i),"out "+str(i))
		obj.addProperty('App::PropertyString','expression'+str(i),"out "+str(i))
		obj.addProperty('App::PropertyFloatList','out'+str(i),"out "+str(i))

	obj.addProperty('App::PropertyString','expressionTime',"Time")
	obj.addProperty('App::PropertyFloatList','outTime',"Time")
	obj.expressionTime='inTime'

	_NP(obj)

	return obj

