#***************************************************************************
#*																		 *
#*   Copyright (c) 2014													*  
#*   <microelly2@freecadbuch.de>										   * 
#*																		 *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	 *
#*   the License, or (at your option) any later version.				   *
#*   for detail see the LICENCE text file.								 *
#*																		 *
#*   This program is distributed in the hope that it will be useful,	   *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		 *
#*   GNU Library General Public License for more details.				  *
#*																		 *
#*   You should have received a copy of the GNU Library General Public	 *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA																   *
#*																		 *
#***************************************************************************

__title__="FreeCAD Animation Toolkit"
__author__ = "Thomas Gundermann"
__url__ = "http://www.freecadbuch.de"

import FreeCAD
if FreeCAD.GuiUp:
	import FreeCADGui
	FreeCADGui.updateLocale()

# Einzelbeispiel 


def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")


import FreeCAD,Draft,ArchComponent, DraftVecUtils
from FreeCAD import Vector
import math
import Draft, Part, FreeCAD, math, PartGui, FreeCADGui, PyQt4
from math import sqrt, pi, sin, cos, asin
from FreeCAD import Base

if FreeCAD.GuiUp:
	import FreeCADGui
	from PySide import QtCore, QtGui
	from DraftTools import translate
else:
	def translate(ctxt,txt):
		return txt

__title__="FreeCAD Prism"
__author__ = "thomas gundermann"
__url__ = "http://www.freecadbuch.de"

#---------------------
def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")


#------------------------------------



class _Actor(object):

	def __init__(self,obj,start=10,end=20):
		say("71")
		say(obj)
		say(self.obj.Label)
		say("71a!")
		#self.obj.obj=self.obj.getObject(obj)
		say("got")
		self.obj.start=start
		self.obj.end=end
		if self.obj.obj2:
			self.obj.initPlace=	self.obj.obj2.Placement


	def initPlacement(self,tp):
		self.obj.initPlace=tp
		self.obj.obj2.Placement=tp
	def getObject(self,name):
		if  isinstance(name,str):
#			obj=FreeCAD.ActiveDocument.getObject(name)
			objl=App.ActiveDocument.getObjectsByLabel(name)
			obj=objl[0]
			say('obj found')
		else:
			obj=name
		say(obj)
		return obj

	def toInitialPlacement(self):
		self.obj.obj2.Placement=self.obj.initPlace
	def setIntervall(self,s,e):
		self.obj.start=s
		self.obj.end=e
	def step(self,now):
		say("Step" + str(now))


#----------------------
def createMover(count=6,size_bottom = 4, height=10,name='My_Mover'):
	'''makePrism(baseobj,[facenr],[angle],[name]) : Makes a Prism based on a
	regular polygon with count(8) vertexes face and a name (default
	= Prism).'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	
	obj.addProperty("App::PropertyPythonObject","step","zzz","step")
	obj.addProperty("App::PropertyPythonObject","reverse","zzz","reverse")
	
	obj.addProperty("App::PropertyInteger","start","intervall","start")
	obj.addProperty("App::PropertyInteger","end","intervall","end")

	obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
	obj.addProperty("App::PropertyVector","motionVector","3D Param","motionVector")
	obj.addProperty("App::PropertyLink","obj2","3D Param","Tooltipp bew. Ob")
	# hack ...
	# obj.obj2=FreeCAD.ActiveDocument.Box
	_Mover(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandMover:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/mover.png', 'MenuText': 'Mover', 'ToolTip': 'Mover Dialog'} 


	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Mover")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createMover()")
			say("I create a mover")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Mover(_Actor):


		
	def __init__(self,obj,motion=FreeCAD.Vector(100,0,0) ,start=10,end=20):
		self.obj=obj
		super(type(self), self).__init__(self.obj,start,end)
		obj.Proxy = self
		self.Type = "_Mover"
		obj.step=self.step
		obj.reverse=self.reverse
		self.obj.motionVector=motion


	def step(self,now):
		if self.obj.obj2:
			if now<self.obj.start or now>self.obj.end:
				pass
			else:
				relativ=1.00/(self.obj.end-self.obj.start)
				v=FreeCAD.Vector(self.obj.motionVector).multiply(relativ)
				Draft.move(self.obj.obj2,v,copy=False)
		else:
			say("kein Moveobjekt ausgewaehlt")
			
	def reverse(self):
		self.obj.motionVector.multiply(-1)

	def execute(self,obj):
		say("execute  _Mover")
		if self.obj.obj2:
			self.obj.initPlace=	self.obj.obj2.Placements





class _ViewProviderMover(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

 
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/mover.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None



if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Mover',_CommandMover())
	
	
#-------------------------------------


def createRotator(name='My_Rotator'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_ViewProviderRotator(obj.ViewObject)
	return obj

class _CommandRotator:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/rotator.png', 'MenuText': 'Rotator', 'ToolTip': 'Rotator Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Rotator")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createRotator()")
			say("I create a rotator")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Rotator:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Rotator"

	def execute(self,obj):
		say("execute _Rotator")



class _ViewProviderRotator(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/rotator.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self

	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Rotator',_CommandRotator())

#---------------------------------------------------------------

	
#-------------------------------------


	
#-------------------------------------


def createPlugger(name='My_Plugger'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_Mover(obj)
	_ViewProviderPlugger(obj.ViewObject)
	return obj

class _CommandPlugger:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/plugger.png', 'MenuText': 'Plugger', 'ToolTip': 'Plugger Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Plugger")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createPlugger()")
			say("I create a Plugger")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Plugger:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Plugger"

	def execute(self,obj):
		say("execute _Plugger")



class _ViewProviderPlugger(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/plugger.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self

	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Plugger',_CommandPlugger())

#---------------------------------------------------------------


	
#-------------------------------------


def createTranquillizer(name='My_Tranquillizer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_Mover(obj)
	_ViewProviderTranquillizer(obj.ViewObject)
	return obj

class _CommandTranquillizer:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/tranq.png', 'MenuText': 'Tranquillizer', 'ToolTip': 'Tranquillizer Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Tranquillizer")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createTranquillizer()")
			say("I create a Tranquillizer")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Tranquillizer:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Tranquillizer"

	def execute(self,obj):
		say("execute _Tranquillizer")



class _ViewProviderTranquillizer(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/tranq.png'

	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Tranquillizer',_CommandTranquillizer())

#---------------------------------------------------------------

	
#-------------------------------------


def createAdjuster(name='My_Adjuster'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_Adjuster(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandAdjuster:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/adjuster.png', 'MenuText': 'Adjuster', 'ToolTip': 'Adjuster Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Adjuster")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createAdjuster()")
			say("I create a Adjuster")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Adjuster:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Adjuster"

	def execute(self,obj):
		say("execute _Adjuster")



class _ViewProviderAdjuster(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

 
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/adjuster.png'

	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Adjuster',_CommandAdjuster())

#---------------------------------------------------------------


	
#-------------------------------------


def createPhotographer(name='My_Photographer'):
	#obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	
	_Mover(obj)
	_ViewProviderManager(obj.ViewObject)
	return obj

class _CommandPhotographer:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/photographer.png', 'MenuText': 'Photographer', 'ToolTip': 'Photographer Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Photographer")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createPhotographer()")
			say("I create a Photographer")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Photographer:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Photographer"

	def execute(self,obj):
		say("execute _Photographer")



class _ViewProviderPhotographer(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

	
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/manager.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self

 #   def getIcon(self):
 #	   import Arch_rc
 #	   return ":/icons/Arch_Floor_Tree.svg"

	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def __init__(self,vobj):
		vobj.Proxy = self

	def getIcon2(self):
		return '/home/microelly2/animation_wb/icons/photographer.png'


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Photographer',_CommandPhotographer())

#---------------------------------------------------------------



	
#-------------------------------------


def createManager(name='My_Manager'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
#	obj.addProperty("App::PropertyPlacement","Placement","Arch",translate("Arch","The placement of this group"))
	obj.addProperty("App::PropertyInteger","intervall","params",
						"intervall")

	obj.addProperty("App::PropertyPythonObject","run","zzz",						"run")
	obj.addProperty("App::PropertyLinkList","targets","zzz",						"targets")
	obj.addProperty("App::PropertyString","text","params",						"text")
	#obj.run=


	_Manager(obj)

	_ViewProviderManager(obj.ViewObject)
	return obj

class _CommandManager:
	def GetResources(self): 
		return {'Pixmap' : '/home/microelly2/animation_wb/icons/manager.png', 'MenuText': 'Manager', 'ToolTip': 'Manager Dialog'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createManager()")
			say("I create a Manager")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Manager:

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Manager"
		obj.targets=[]
#		obj.targets=[FreeCAD.ActiveDocument.Box]
#		obj.fn=''
		obj.text='ausgabe erfolgt hier'
		obj.intervall=20
		obj.run=self.run
		self.obj=obj



	def execute(self,obj):
		say("execute _Manager")


	def register(self,obj):
		self.obj.targets.append(obj)

	
	def run(self,intervall):
		say("run #171")
		say(intervall)
		say(self.obj.Label)
		say(self.obj.Name)
		for nw in range(intervall):	
			say(nw)
			say(self.Outlist)
			say("self")
			say(self)
			for ob in self.OutList:
				say("ob ..")
				say(ob.Label)
				say(ob.obj2.Label)
				try:
					say("step")
					# ob.step(nw)
				except:
					say("fehler step")
			#Draft.move(helper,sk,copy=False)
#+#			FreeCADGui.Selection.clearSelection()
#+#			FreeCADGui.updateGui() 
#			self.genOutput(nw)
###			self.showTime(nw)


	def setShowTime(self,texter):
		self.obj.text=texter


	def showTime(self,nw1):
		if self.obj.text:
			kf= "%04.f"%nw1
			self.obj.text.LabelText = [unicode(str(kf), 'utf-8'),]

	def finalize(self,wait=5):
			for obj in self.obj.targets:
				obj.toInitialPlacement()
				FreeCADGui.updateGui() 
			time.sleep(wait)









class _ViewProviderManager(ArchComponent.ViewProviderComponent):
	"A View Provider for the Mover object"

	
	def getIcon(self):
		return '/home/microelly2/animation_wb/icons/manager.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None



if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Manager',_CommandManager())

#---------------------------------------------------------------









