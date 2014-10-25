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


#----------------------
def createMover(count=6,size_bottom = 4, height=10,name='My_Mover'):
	'''makePrism(baseobj,[facenr],[angle],[name]) : Makes a Prism based on a
	regular polygon with count(8) vertexes face and a name (default
	= Prism).'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_ViewProviderMover(obj.ViewObject)
	#obj.count=count
	#obj.size_bottom=size_bottom
	#obj.height=height
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
	   
class _Mover:

	def __init__(self,obj):
		obj.Proxy = self
		obj.addProperty("App::PropertyInteger","count","Base",
						translate("Arch","Anzahl Ecken"))
		obj.addProperty("App::PropertyInteger","size_bottom","Base",
						translate("Arch","Bodenmas"))
		obj.addProperty("App::PropertyInteger","height","Base",
						translate("Arch","hoch"))
		self.Type = "Mover_Prism"

	def execute(self,obj):
		say("erzeuge _Mover")



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
	obj.addProperty("App::PropertyPlacement","Placement","Arch",translate("Arch","The placement of this group"))
	obj.addProperty("App::PropertyInteger","intervall","intervall",
						"intervall")

	obj.addProperty("App::PropertyPythonObject","run","run",						"run")
	obj.addProperty("App::PropertyLinkList","targets","targets",						"targets")
	obj.addProperty("App::PropertyString","text","text",						"text")
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
		obj.targets=[FreeCAD.ActiveDocument.My_Mover]
#		obj.fn=''
		obj.text=''
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
		say(self.obj.targets)
		for nw in range(intervall):	
			say(nw)
			for obj in self.obj.targets:
				obj.step(nw)
			#Draft.move(helper,sk,copy=False)
			FreeCADGui.Selection.clearSelection()
			FreeCADGui.updateGui() 
#			self.genOutput(nw)
			self.showTime(nw)


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









