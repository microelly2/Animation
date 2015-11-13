#***************************************************************************
#*																		*
#*   Copyright (c) 2014													 *  
#*   <microelly2@freecadbuch.de>										 * 
#*																		 *
#*   This program is free software; you can redistribute it and/or modify*
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	*
#*   the License, or (at your option) any later version.				*
#*   for detail see the LICENCE text file.								*
#*																		*
#*   This program is distributed in the hope that it will be useful,	*
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		*
#*   GNU Library General Public License for more details.				*
#*																		*
#*   You should have received a copy of the GNU Library General Public	*
#*   License along with this program; if not, write to the Free Software*
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#*   USA																*
#*																		*
#************************************************************************

__title__="FreeCAD Animation Toolkit"
__author__ = "Thomas Gundermann"
__url__ = "http://www.freecadbuch.de"

import FreeCAD , FreeCADGui , Part, Draft, math, Drawing , PySide, os,sys
from FreeCAD import Vector
import math
import Draft, Part, FreeCAD, math, PartGui, FreeCADGui, PySide
from math import sqrt, pi, sin, cos, asin
from PySide import QtGui,QtCore
from FreeCAD import Base

import Inspector
App=FreeCAD

if FreeCAD.GuiUp:
	import FreeCADGui
	FreeCADGui.updateLocale()

def sayd(s):
	if hasattr(FreeCAD,'animation_debug'):
		pass
		FreeCAD.Console.PrintMessage(str(s)+"\n")

def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")

def sayErr(s):
		FreeCAD.Console.PrintError(str(s)+"\n")


def errorDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()

if FreeCAD.GuiUp:
	import FreeCADGui
	from PySide import QtCore, QtGui

import os
__dir__ = os.path.dirname(__file__)	
#---------------------------------------------------------------

class _Actor(object):

	def __init__(self,obj,start=10,end=20):
		sayd(obj)
		sayd(self.obj.Label)


	def initPlacement(self,tp):
		self.obj.initPlace=tp
		self.obj.obj2.Placement=tp

	def initialize(self):
		sayd("initialize ...")
	
	def getObject(self,name):
		if  isinstance(name,str):
#			obj=FreeCAD.ActiveDocument.getObject(name)
			objl=App.ActiveDocument.getObjectsByLabel(name)
			obj=objl[0]
			sayd('obj found')
		else:
			obj=name
		sayd(obj)
		return obj

	def toInitialPlacement(self):
		self.obj.obj2.Placement=self.obj.initPlace
	def setIntervall(self,s,e):
		self.obj.start=s
		self.obj.end=e
	def step(self,now):
		sayd("Step" + str(now))
	def stepsub(self,now):
		say("runsub ...")
		say(self)
		FreeCAD.yy=self
		g=self.obj2.Group
		#say(g)
		for sob in g:
				FreeCAD.ty=sob
				say(sob.Label)
				sob.Proxy.step(now)
		
	def move(self,vec=FreeCAD.Vector(0,0,0)):
		FreeCAD.uu=self
		say("move " + str(self.obj2.Label) + " vector=" +str(vec))
	def rot(self,angle=0):
		FreeCAD.uu=self
		say("rotate " + str(self.obj2.Label) + " angle=" +str(angle))
		

		
	def execute(self,obj):
		pass

	
	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


class _CommandActor:
	def GetResources(self): 
		return {'Pixmap' : __dir__+ '/icons/mover.png', 'MenuText': 'Mover', 'ToolTip': 'Mover Dialog'} 


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
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return


class _ViewProviderActor(object):
 
	def getIcon(self):
		return __dir__ + '/icons/mover.png'
   
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
#--------------------------------------

import Draft

#-------------------------


#---------------------------------------------------------------
def createBounder(name='MyBounder'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=40
	obj.addProperty("App::PropertyInteger","duration","Base","end")

	obj.addProperty("App::PropertyLink","obj","Object","Objekt")
#	obj.addProperty("App::PropertyInteger","nr","Object","nummer Datum").nr=1#
#	obj.addProperty("App::PropertyEnumeration","unit","3D Param","einheit").unit=['deg','mm']
#	# FreeCADGui.getDocument("Unnamed").getObject("Box").Transparency = 2

	obj.addProperty("App::PropertyBool","x","intervall","start").x=False
	obj.addProperty("App::PropertyFloat","xmin","intervall","va")
	obj.addProperty("App::PropertyFloat","xmax","intervall","ve")
	obj.addProperty("App::PropertyBool","y","intervall","start").y=False
	obj.addProperty("App::PropertyFloat","ymin","intervall","va")
	obj.addProperty("App::PropertyFloat","ymax","intervall","ve")

	obj.addProperty("App::PropertyBool","z","intervall","start").z=False
	obj.addProperty("App::PropertyFloat","zmin","intervall","va")
	obj.addProperty("App::PropertyFloat","zmax","intervall","ve")


	
#	obj.addProperty("App::PropertyInteger","transpaStart","Transparency","start").transpaStart=0
#	obj.addProperty("App::PropertyInteger","transpaEnd","Transparency","end").transpaEnd=40
#	obj.addProperty("App::PropertyEnumeration","DisplayStyle","Transparency","end").DisplayStyle=['Flat Lines','Shaded','Wireframe']
#	obj.addProperty("App::PropertyBool","visibility","Visibility","toggle visibility").visibility=False
#	obj.addProperty("App::PropertyInteger","transpaStart","transparency","start").transpaStart=0
#	obj.addProperty("App::PropertyInteger","transpaEnd","transparency","end").transpaEnd=40
	
	
	_Bounder(obj)
	_ViewProviderBounder(obj.ViewObject)
	return obj

class _CommandBounder(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__+ '/icons/bounder.png', 'MenuText': 'Bounder', 'ToolTip': 'Bounder Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Bounder")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createBounder()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Bounder(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Bounder"
		self.obj2 = obj 

		
	def step(self,now):
		FreeCAD.tt=self
		
		
		say("Bounder step!" + str(now))
		if now<=self.obj2.start or now>self.obj2.end:
			say("ausserhalb")
			pass
		else:
			pass
			gob=FreeCAD.ActiveDocument.getObject(self.obj2.obj.Name)
			pm=gob.Placement.Base
			say(pm)
			x=pm.x
			y=pm.y
			z=pm.z
			if self.obj2.x:
				if self.obj2.xmin>x:
					x=self.obj2.xmin
					say("xmin")
				if self.obj2.xmax<x:
					x=self.obj2.xmax
					say("xmax")

			if self.obj2.y:
				if self.obj2.ymin>y:
					y=self.obj2.ymin
				if self.obj2.ymax<y:
					y=self.obj2.ymax

			if self.obj2.z:
				if self.obj2.zmin>z:
					z=self.obj2.zmin
				if self.obj2.zmax<z:
					z=self.obj2.zmax
			gob.Placement.Base=FreeCAD.Vector(x,y,z)
			pm=gob.Placement.Base
			say(pm)
			FreeCADGui.updateGui() 
			
			

	def setValues(self,va,ve):
		self.obj2.va=va
		self.obj2.ve=ve

	def execute(self,obj):
		sayd("execute _Bounder")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration

class _ViewProviderBounder(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/bounder.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Bounder',_CommandBounder())

#---------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------
def createViewpoint(name='My_Viewpoint'):
	say("creat movie screen")
	
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","duration","Base","start").duration=10

	obj.addProperty("App::PropertyInteger","end","Base","end")

	obj.addProperty("App::PropertyVector","posCamera","Camera","sweep").posCamera=FreeCAD.Vector(10,50,30)
	obj.addProperty("App::PropertyLink","pathCamera","Camera","sweep")
	obj.addProperty("App::PropertyInteger","indexCamera","Camera","sweep")
	obj.addProperty("App::PropertyEnumeration","modeCamera","Camera","Rotationsachse Zentrum relativ").modeCamera=['Vector','Path']
	

	obj.addProperty("App::PropertyEnumeration","dirMode","Direction","Rotationsachse Zentrum relativ").dirMode=['None','Vector','Object']
	obj.addProperty("App::PropertyVector","dirVector","Direction","richutng ")
	obj.addProperty("App::PropertyLink","dirTarget","Direction","richutng ")
	
	obj.addProperty("App::PropertyEnumeration","posMode","Position","Rotationsachse Zentrum relativ").posMode=['None','Vector','Object']
	obj.addProperty("App::PropertyVector","posVector","Position","sweep").posVector=FreeCAD.Vector(0,0,0)
	obj.addProperty("App::PropertyLink","posObject","Position","sweep")
	obj.addProperty("App::PropertyFloat","zoom","lens geometry","extrusion").zoom=1
	obj.addProperty("App::PropertyEnumeration","typeCamera","Camera","extrusion").typeCamera=["Orthographic","Perspective"]
	obj.typeCamera="Orthographic"
	obj.modeCamera='Vector'
	obj.indexCamera=1
	
	_Viewpoint(obj)
	_ViewProviderViewpoint(obj.ViewObject)
	return obj

class _CommandViewpoint(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/viewpoint.png', 'MenuText': 'Viewpoint', 'ToolTip': 'Viewpoint Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create BB")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createViewpoint()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return



class _Viewpoint(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Viewpoint"

	def step(self,now):
		App=FreeCAD
		say("step " +str(now))
		
		from pivy import coin
		camera = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()

		Gui=FreeCADGui
		if self.obj2.typeCamera=="Orthographic":
			Gui.activeDocument().activeView().setCameraType("Orthographic")
		else:
			Gui.activeDocument().activeView().setCameraType("Perspective")


# ziel, aufrichtung - wo ist oben bei der kamera

		# camera.pointAt(coin.SbVec3f(0,0,0),coin.SbVec3f(0,0,1))
		campos=Base.Vector( 100, 50, 30)
		campos=self.obj2.posCamera
		# position neu bestimmen
		if self.obj2.modeCamera == 'Path' :
			pos=-self.obj2.indexCamera
			t=FreeCAD.animCamera[pos]
			campos=t.pop()

		say("camera pos")
		say(campos)
		camera.position.setValue( campos) 
		
	

		if now==self.obj2.start:
			pass
			
		if self.obj2.zoom <>1:
			if self.obj2.zoom <=0:
				sayErr("Zoom darf nicht <= NULL seinn")
				errorDialog("Zoom darf nicht <= NULL seinn")
			SS=1/(self.obj2.zoom)-1
			start=float(self.obj2.start)
			end=float(self.obj2.start + self.obj2.duration)
			if now>start and now<=end:
				s1=0.00+(1+(now-start)/(end-start)*SS)
				s2=0.00+(1+(now-1-start)/(end-start)*SS)
				s=s1/s2
				camera.scaleHeight(s)
		
		if self.obj2.dirMode=='Object':
			target=self.obj2.dirTarget
			say(target.Placement.Base)
			pos3=target.Placement.Base
			pos3.sub(campos)
			
			
			#pos=FreeCAD.Vector(campos)
			#pos2=pos.sub(target.Placement.Base)
			#say(pos)
			#say(pos3)
			camera.pointAt(coin.SbVec3f(pos3),coin.SbVec3f(0,0,1))
			say("redirected")
		
		App.ActiveDocument.recompute()
		FreeCADGui.updateGui() 

	def execute(self,obj):
		FreeCAD.ts=self
		FreeCAD.to=obj
		say("execute Viewpoint")
		say(self)
		say(obj)
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration
		if obj.modeCamera == 'Path':
			say("drin 1")
			if 1  or obj.indexCamera >= 0:
				say("drin")
				obj.indexCamera=-1
				##obj.vectorMotion=FreeCAD.Vector(0,0,0)
				# x=FreeCAD.ActiveDocument.DWire001
				x=obj.pathCamera

				steps=obj.duration+1+1
				l=x.Shape.copy().discretize(steps)
				ll=[]
				for pp in range(len(l)):
					print(pp)
					v=l[pp]
					ll.append(v)
					
					say(v)
				ll.reverse()


				if not hasattr(FreeCAD,'animCamera'):
					FreeCAD.animCamera=[]
					say ("FreeCAD.animCamera neu")

				# print (FreeCAD.animMover)

				#FreeCAD.animMover.append("start")
				#FreeCAD.animMover.append("start")
				pos=len(FreeCAD.animCamera)
				obj.indexCamera=-pos
				FreeCAD.animCamera.append(ll)
				say("!!!!!!!!!!!!!!!!!  haenge an pos:"+ str(pos))
				#FreeCAD.animMover.append("end")
				say(FreeCAD.animCamera)




class _ViewProviderViewpoint(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/viewpoint.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Viewpoint',_CommandViewpoint())

#----------------------







#----------------------------------------------------------------------------------------------------------
def createExtruder(name='My_Extruder'):
	say("creat movie screen")
	
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","duration","Base","start").duration=10

#	obj.addProperty("App::PropertyInteger","end","intervall","end").end=10
#	obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
#	obj.addProperty("App::PropertyBool","showFrame","info","Rotationsachse Zentrum relativ").showFrame=False
#	obj.addProperty("App::PropertyBool","showFile","info","Rotationsachse Zentrum relativ").showFile=False
#	obj.addProperty("App::PropertyString","movie","info","Rotationsachse Zentrum relativ").movie="/tmp/movie/"

	obj.addProperty("App::PropertyLink","path","Extrusion","path ")
	obj.addProperty("App::PropertyLink","sweep","Extrusion","sweep")
	obj.addProperty("App::PropertyLink","ext","Extrusion","extrusion")
	
	_Extruder(obj)
	_ViewProviderExtruder(obj.ViewObject)
	return obj

class _CommandExtruder(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/extruder.png', 'MenuText': 'Extruder', 'ToolTip': 'Extruder Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create BB")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createExtruder()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return



class _Extruder(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Extruder"

	def step(self,now):
		App=FreeCAD
		say("step " +str(now))
		s=self.obj2.ext.Spine
		ss=s[0]
		kk=s[1]
		if now==self.obj2.start:
			kk=[]
			steps=20
			steps=self.obj2.duration
			l=ss.Shape.copy().discretize(steps)
			f=Part.makePolygon(l)
			f1=Part.show(f)
			ss=FreeCAD.ActiveDocument.Objects[-1]
		kk.append("Edge"+str(now+1-self.obj2.start))
		if now<self.obj2.start:
			kk=["Edge1"]
			self.obj2.ext.ViewObject.Visibility=False
		else: 
			self.obj2.ext.ViewObject.Visibility=True
		self.obj2.ext.Spine=(ss,kk)
		App.ActiveDocument.recompute()
		FreeCADGui.updateGui() 


class _ViewProviderExtruder(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/extruder.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Extruder',_CommandExtruder())

#----------------------



#--------------------------






#----------------------------------------------------------------------------------------------------------
def createMoviescreen(name='My_Moviescreen'):
	say("creat movie screen")
	
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
#	obj.addProperty("App::PropertyInteger","start","intervall","start").start=0
#	obj.addProperty("App::PropertyInteger","end","intervall","end").end=10
#	obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
#	obj.addProperty("App::PropertyBool","showFrame","info","Rotationsachse Zentrum relativ").showFrame=False
#	obj.addProperty("App::PropertyBool","showFile","info","Rotationsachse Zentrum relativ").showFile=False
#	obj.addProperty("App::PropertyString","movie","info","Rotationsachse Zentrum relativ").movie="/tmp/movie/"
	obj.addProperty("App::PropertyIntegerList","pictureStart","info","Rotationsachse Zentrum relativ").pictureStart=[0,50,100]
	
	obj.addProperty("App::PropertyPath","pictures","screen","text").pictures="/home/microelly2/pics/t%04.f.png"
	# obj.addProperty("App::PropertyVector","text","3D Param","motionVector").motionVector=FreeCAD.Vector(100,0,0)
	obj.addProperty("App::PropertyLink","rectangle","screen","moving object ")
	obj.rectangle = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython","Rectangle Moviescreen")
	Draft._Rectangle(obj.rectangle)

	obj.rectangle.Length = 64
	obj.rectangle.Height = 48
	obj.rectangle.MakeFace = True
	
	_Moviescreen(obj)
	Draft._ViewProviderRectangle(obj.rectangle.ViewObject)
	_ViewProviderMoviescreen(obj.ViewObject)
	
	tx=FreeCADGui.activeDocument().activeView()
	rx=tx.getCameraOrientation()
	obj.rectangle.Placement.Rotation=rx

	return obj

class _CommandMoviescreen(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/moviescreen.png', 'MenuText': 'Moviescreen', 'ToolTip': 'Moviescreen Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create BB")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createMoviescreen()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return


from time import *
import os

class _Moviescreen(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Moviescreen"

	def step(self,now):
		sayd("step " +str(now))
		pfn=self.obj2.pictures%now
		if os.path.exists(pfn):
			self.obj2.rectangle.ViewObject.TextureImage = pfn
			say("image: " + pfn)
		tx=FreeCADGui.activeDocument().activeView()
		rx=tx.getCameraOrientation()
		r2=FreeCAD.Rotation(FreeCAD.Vector(1,0,0),180)
		r3=rx.multiply(r2)
		self.obj2.rectangle.Placement.Rotation=r3
		FreeCAD.ActiveDocument.recompute()
		# say(self)

class _ViewProviderMoviescreen(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/moviescreen.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Moviescreen',_CommandMoviescreen())

#----------------------

		
#----------------------------------------------------------------------------------------------------------
def createBillboard(name='My_Billboard'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
#	obj.addProperty("App::PropertyInteger","start","intervall","start").start=0
#	obj.addProperty("App::PropertyInteger","end","intervall","end").end=10
	# obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
	obj.addProperty("App::PropertyBool","showFrame","info","Rotationsachse Zentrum relativ").showFrame=False
	obj.addProperty("App::PropertyBool","showFile","info","Rotationsachse Zentrum relativ").showFile=False
	obj.addProperty("App::PropertyBool","showDate","info","Rotationsachse Zentrum relativ").showDate=False
	obj.addProperty("App::PropertyStringList","text","info","text").text=["Animation can display","configurable Text Information","in a HUD"]
	obj.addProperty("App::PropertyPath","textFiles","info","text").textFiles="/home/microelly2/texts/t%04.f.txt"
	obj.addProperty("App::PropertyLink","textObj","info","moving object ")
#	obj.addProperty("App::PropertyLink","anchor","info","moving object ")
#	obj.addProperty("App::PropertyVector","offsetAnchor","3D Param","motionVector").motionVector=FreeCAD.Vector(100,0,0)
	
	obj.textObj=FreeCAD.ActiveDocument.addObject("App::Annotation","Text Billboard")
	obj.textObj.LabelText=obj.text
	obj.textObj.Position=FreeCAD.Vector(0,0,0)
	_Billboard(obj)
	_ViewProviderBillboard(obj.ViewObject)
	return obj

class _CommandBillboard(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/billboard.png', 'MenuText': 'Billboard', 'ToolTip': 'Billboard Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create BB")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createBillboard()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return


from time import *
import os

class _Billboard(_Actor):
		
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Billboard"

	def step(self,now):
		sayd("step " +str(now))
		k=self.obj2.text
		fne=self.obj2.textFiles
		fn=fne%now
		if os.path.exists(fn):
			say("textfile: " + fn)
			data = [line.strip() for line in open(fn, 'r')]
			sayd(data)
			self.obj2.text=data
		k=self.obj2.text
		#--------------------------------
		kf= "%04.f"%now
		if self.obj2.showFrame:
			k.append("Frame: " + kf)
		lt = localtime()
		if self.obj2.showDate:
			tz=strftime("%d.%m.%Y", lt)
			ts=strftime("%H:%M:%S", lt)
			k.append(tz)
			k.append(ts)
		if self.obj2.showFile:
			k.append("File: "+ os.path.basename(FreeCAD.ActiveDocument.FileName))
			k.append("Author: "+ FreeCAD.ActiveDocument.LastModifiedBy)
		self.obj2.textObj.LabelText=k
		FreeCAD.ActiveDocument.recompute()



class _ViewProviderBillboard(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/billboard.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Billboard',_CommandBillboard())

#----------------------

def createMover(name='My_Mover'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=10
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=10
	obj.addProperty("App::PropertyPlacement","initPlaceMotion","Object","initPlace")
	obj.addProperty("App::PropertyEnumeration","ModeMotion","Motion","Modus").ModeMotion=['Vector','DLine','DWire','Shape.Edge','Path']

	##obj.addProperty("App::PropertyVector","motionVector","Motion","motionVector").motionVector=FreeCAD.Vector(100,0,0)
	obj.addProperty("App::PropertyVector","vectorMotion","Motion","motionVector").vectorMotion=FreeCAD.Vector(100,0,0)
	obj.addProperty("App::PropertyLink","sourceMotion","Motion","source objectfor the motion vector")
	obj.addProperty("App::PropertyInteger","indexMotion","Motion","position on the source").indexMotion=1
	obj.addProperty("App::PropertyBool","reverseMotion","Motion","recvers the direction fo the vector").reverseMotion=False
	
	obj.addProperty("App::PropertyLink","obj2","Object","moving object ")
	_Mover(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandMover(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/mover.png', 'MenuText': 'Mover', 'ToolTip': 'Mover Dialog'} 

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
		
	def __init__(self,obj,motion=FreeCAD.Vector(100,0,0) ,start=0,end=10):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Mover"

	def stepsub(self,now,vec):
		sayd("run mover step sub ...")
		
		FreeCAD.yy=self
		g=self.obj2.Group
		# say(g)
		for sob in g:
				FreeCAD.ty=sob
				# say(sob.Label)
				sob.Proxy.step(now)
				sob.Proxy.move(vec)
	
	def rot(self,angle=0):
		FreeCAD.uu=self
		#say("rotate " + str(self.obj2.Label) + " angle=" +str(angle))
		if self.obj2.ModeMotion =='Vector':
			#say(self.obj2.vectorMotion)
			
			a=FreeCAD.Placement()
			a.Base=self.obj2.vectorMotion
			zzz=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),angle)
			r=FreeCAD.Placement()
			r.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),angle)
			a2=r.multiply(a)
			
			self.obj2.vectorMotion=a2.Base
			FreeCAD.ActiveDocument.recompute()
					
			# self.obj2.vectorMotion=multiply(self.obj2.vectorMotion)
			#say(self.obj2.vectorMotion)


	def step(self,now):
		sayd("step XX")
		sayd(self)
		
		FreeCAD.zz=self
		#say(self.obj2)
		#say(self.obj2.ModeMotion)
		if not self.obj2.obj2:
			errorDialog("kein mover objekt zugeordnet")
			raise Exception(' self.obj2 nicht definiert')
		if self.obj2.obj2:
			sayd("Move it ");
			if now<=self.obj2.start or now>self.obj2.end:
				pass
			else:
				sayd("move steps")
				#if self.obj.ModeMotion == 'Path':
				if self.obj2.ModeMotion == 'Path' or  self.obj2.ModeMotion == 'DLine' or  self.obj2.ModeMotion == 'DWire':
					pos=-self.obj2.indexMotion
					t=FreeCAD.animMover[pos]
					v=t.pop()
					self.stepsub(now,v)
					Draft.move(self.obj2.obj2,v,copy=False)
				else:
					relativ=1.00/(self.obj2.end-self.obj2.start)
					v=FreeCAD.Vector(self.obj2.vectorMotion).multiply(relativ)
					self.stepsub(now,v)
					Draft.move(self.obj2.obj2,v,copy=False)
				FreeCADGui.Selection.clearSelection()
		else:
			say("kein Moveobjekt ausgewaehlt")
		
	def Xreverse(self):
		self.obj2.vectorMotion.multiply(-1)

	def initialize(self):
		sayd("initialize ...")
		if  self.obj2.ModeMotion == 'Path':
			self.obj2.indexMotion=1
			say("set indexMotion to 1 for Path")


	def execute(self,obj):
		sayd("execute  _Mover")
		sayd(self)
		sayd(obj)
		
		sayd("execute ..2 ")
		#if hasattr(self,'obj2'):
		#	self.initPlace=	self.obj2.Placement
		# anzeigewert neu berechnen
		if hasattr(obj,'obj2'):
			sayd(obj.obj2)
			pass
		
		FreeCAD.zu=obj
		# say(obj.ModeMotion)
		if obj.ModeMotion <> 'Vector':
			obj.setEditorMode("vectorMotion", 1) #ro
			obj.setEditorMode("reverseMotion", 1) #ro
		else: 
			obj.setEditorMode("vectorMotion", 0) #rw
			obj.setEditorMode("reverseMotion", 0) #rw
		obj.end=obj.start+obj.duration
		obj.setEditorMode("end", 1) #ro
		if obj.ModeMotion == 'Path' or  obj.ModeMotion == 'DLine' or  obj.ModeMotion == 'DWire':
			if obj.indexMotion>0:
				obj.indexMotion=-1
				obj.vectorMotion=FreeCAD.Vector(0,0,0)
				# x=FreeCAD.ActiveDocument.DWire001
				x=obj.sourceMotion

				steps=obj.duration
				
				l=x.Shape.copy().discretize(steps)
				ll=[]
				for pp in range(len(l)-1):
					
					v=FreeCAD.Vector(l[pp+1]).sub(l[pp])
					ll.append(v)
					
					print(v)
				ll.reverse()


				if not hasattr(FreeCAD,'animMover'):
					FreeCAD.animMover=[]
					print ("neu")

				# print (FreeCAD.animMover)

				#FreeCAD.animMover.append("start")
				#FreeCAD.animMover.append("start")
				pos=len(FreeCAD.animMover)
				obj.indexMotion=-pos
				FreeCAD.animMover.append(ll)
				say("!!!!!!!!!!!!!!!!!  haenge an pos:"+ str(pos))
				#FreeCAD.animMover.append("end")
				print(FreeCAD.animMover)
				
			else:
					say("Pfad bereits berechnet")



			
			
		


class _ViewProviderMover(_ViewProviderActor):
	"A View Provider for the Mover object"
 
	def getIcon(self):
		return __dir__ + '/icons/mover.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Mover',_CommandMover())

#-------------------------------------


def createRotator(name='My_Rotator'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=10
	obj.addProperty("App::PropertyInteger","duration","Base","end").end=10
	obj.addProperty("App::PropertyPlacement","initPlace","Object","initPlace")
	obj.addProperty("App::PropertyVector","rotationCentre","Motion","Rotationszentrum")
	obj.addProperty("App::PropertyVector","rotationAxis","Motion","Rotationsachse").rotationAxis=FreeCAD.Vector(0,0,1)
	obj.addProperty("App::PropertyBool","rotCenterRelative","Motion","Rotationsachse Zentrum relativ").rotCenterRelative=False
	
	obj.addProperty("App::PropertyFloat","angle","Motion","Dreh Winkel").angle=360
	
	obj.addProperty("App::PropertyLink","obj2","Object","rotating object ")

	_Rotator(obj)
	_ViewProviderRotator(obj.ViewObject)
	return obj

class _CommandRotator(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/rotator.png', 'MenuText': 'Rotator', 'ToolTip': 'Rotator Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Rotator")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createRotator()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Rotator(_Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Rotator"
		self.obj2=obj
		
	def execute(self,obj):
		sayd("execute _Rotator")
		if hasattr(obj,'obj2'):
			#say(obj.obj2)
			pass
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration

	def move(self,vec):
		self.obj2.rotationCentre=self.obj2.rotationCentre.add(vec)

	def stepsub(self,now,angle):
		sayd("run rotator step sub ...")
		
		FreeCAD.yy=self
		g=self.obj2.Group
		say(g)
		for sob in g:
				FreeCAD.ty=sob
				say(sob.Label)
				sob.Proxy.step(now)
				sob.Proxy.rot(angle)
	
	def step(self,now):
		if now<=self.obj2.start or now>self.obj2.end:
			pass
		else:
			relativ=1.00/(self.obj2.end-self.obj2.start)
			angle2=self.obj2.angle*relativ
			
			self.stepsub(now,angle2)
			
			rotCenter=self.obj2.rotationCentre
			
			FreeCAD.ActiveDocument.recompute()
			sayd("rotation")
			sayd(angle2)
			sayd("before");	sayd(self.obj2.obj2.Placement)
			
			zzz=FreeCAD.Rotation(self.obj2.rotationAxis,angle2)
			App=FreeCAD
			self.obj2.obj2.Placement=App.Placement(
			FreeCAD.Vector(0,0,0), 
			zzz,
			self.obj2.rotationCentre).multiply(self.obj2.obj2.Placement)
			FreeCAD.ActiveDocument.recompute()

			sayd("after");	sayd(self.obj2.obj2.Placement)
			FreeCADGui.Selection.clearSelection()
		sayd("ende")

	def  setRot(self,dwireName):
		import math
		obj=self.getObject(dwireName)
		t=obj
		a=t.Shape.Vertexes[0]
		b=t.Shape.Vertexes[1]
		c=t.Shape.Vertexes[2]
		v1=FreeCAD.Vector(a.X,a.Y,a.Z).sub(FreeCAD.Vector(b.X,b.Y,b.Z))
		v2=FreeCAD.Vector(c.X,c.Y,c.Z).sub(FreeCAD.Vector(b.X,b.Y,b.Z))
		
		axis=v1.cross(v2)
		dot=v1.dot(v2)

		cosAngle=dot/(v1.Length *v2.Length)
		angle=math.acos(cosAngle)/math.pi *180
		self.axisVector=axis
		self.angle=angle
		self.positionVector=FreeCAD.Vector(b.X,b.Y,b.Z)
	
	def reverse(self):
		self.angle =- self.angle
	def reverse2(self):
		self.angle =  self.angle - 180
	def reverse3(self):
		self.angle =   self.angle -180


class _ViewProviderRotator(_ViewProviderActor):
	def getIcon(self):
		return __dir__ + '/icons/rotator.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Rotator',_CommandRotator())


def createPlugger(name='My_Plugger'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","pin","Pin","pin")
	obj.addProperty("App::PropertyLink","obj","Object","objekt")
	obj.addProperty("App::PropertyInteger","ix","Pin","index 1").ix=3
	obj.addProperty("App::PropertyInteger","status","Pin","intern").status=0
	obj.addProperty("App::PropertyEnumeration","detail","Pin","art").detail=["Placement.Base","Vertex.Point","Sketch.Object.StartPoint","Sketch.Object.EndPoint","unklarmp"]
	obj.addProperty("App::PropertyEnumeration","trafoMode","Pin","start").trafoMode=["offset","yz","xz","matrix"]
	obj.addProperty("App::PropertyVector","offsetVector","Pin","offsetVector").offsetVector=FreeCAD.Vector(30,30,0)
	obj.addProperty("App::PropertyMatrix","trafoMatrix","Pin","offsetVector").trafoMatrix=FreeCAD.Matrix(1,0,0,0,1,0,0,0,0)

	obj.addProperty("App::PropertyEnumeration","mode","Base","start").mode=["always","intervall","signal"]

	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=10
	obj.addProperty("App::PropertyInteger","duration","Base","end").end=10

	obj.addProperty("App::PropertyEnumeration","pinMode","Base","start").pinMode=["none","2points"]
	obj.addProperty("App::PropertyInteger","ix2","Pin2","index 1").ix2=3
	obj.addProperty("App::PropertyEnumeration","detail2","Pin2","art").detail2=["Placement.Base","Vertex.Point","Sketch.Object.StartPoint","Sketch.Object.EndPoint","unklarmp"]
	obj.addProperty("App::PropertyFloat","offsetArc2","Pin2","index 1")
	obj.addProperty("App::PropertyFloat","factorArc2","Pin2","index 1")
	obj.addProperty("App::PropertyEnumeration","trafoMode2","Pin2","start").trafoMode2=["offset","yz","xz","matrix"]
	obj.addProperty("App::PropertyVector","offsetVector2","Pin2","offsetVector").offsetVector2=FreeCAD.Vector(30,30,0)
	obj.addProperty("App::PropertyMatrix","trafoMatrix2","Pin2","offsetVector").trafoMatrix2=FreeCAD.Matrix(1,0,0,0,1,0,0,0,0)
	
	
	obj.setEditorMode("trafoMode2", 2) #hide
	obj.setEditorMode("offsetVector2", 2) #hide
	obj.setEditorMode("trafoMatrix2", 2) #hide


#	obj.addProperty("App::PropertyLinkSub","subobj","3D Param1","Subobjekt")
#	obj.addProperty("App::PropertyLinkSub","subobj","3D Param1","Subobjekt")
#	obj.addProperty("App::PropertyLinkSub", "PartName", "Part", "Reference to name of part").PartName = (part, ['Name'])
#	obj.addProperty("App::PropertyLinkSub", "Volume", "Part", "Reference to volume of part").Volume = (part, ['Shape', 'Volume'])
#	obj.addProperty("App::PropertyLinkSub", "PartName", "Part", "Reference to name of part")
#	obj.addProperty("App::PropertyLinkSub", "Volume", "Part", "Reference to volume of part")
#	obj.PartName=(FreeCAD.ActiveDocument.Box,['Label'])

	_Plugger(obj)
	_ViewProviderPlugger(obj.ViewObject)
	return obj

class _CommandPlugger(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/plugger.png', 'MenuText': 'Plugger', 'ToolTip': 'Plugger Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Plugger")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createPlugger()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   

def findVertex(oldpos,sketch,offset):
	sayd("find Vertex")
	oldpos=FreeCAD.Vector(oldpos).sub(offset)
	lst=sketch.Vertexes
	dist=30
	mdist=99999
	oks=0
	ixok=-1
	try:
		ix=0
		for v in lst:
			say(v.Point)
			d=oldpos.distanceToPoint(v.Point)
			say(d)
			if (d<dist):
				say("naher punkt" + str(ix))
				oks += 1
				ixok=ix
				mdist=d
			ix +=1
	except:
		say("fehler")
	say ("---------------min dist =" + str(mdist))
	if oks>1:
		sayErr("distance of the sketcher points to small")
	if oks<1:
		sayErr("near radius is too small -slow down the animation dist=" +str(dist))
	return(ixok)


class _Plugger(_Actor):
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Plugger"
		self.obj2 = obj 

	def step(self,now):
		sayd("Plugger step :" + str(now))
		if not self.obj2.obj:
			errorDialog("kein ziel zugeordnet")
			raise Exception(' self.obj2.obj nicht definiert')
		if not self.obj2.pin:
			errorDialog("kein pin zugeordnet")
			raise Exception(' self.obj2.pin nicht definiert')
		sayd(self.obj2.ix)
		sayd(self.obj2.detail)
		
		if self.obj2.mode=="always" or ( self.obj2.mode=="intervall" and  self.obj2.start<=now and self.obj2.end>=now):

			if self.obj2.detail=="Placement.Base":
				sayd("Base")
				if self.obj2.obj.TypeId=='App::Annotation':
					p=FreeCAD.Vector(self.obj2.pin.Placement.Base)
					p2=p.add(self.obj2.offsetVector)
					self.obj2.obj.Position=p2
				else:
					p=FreeCAD.Vector(self.obj2.pin.Placement.Base)
					p2=p.add(self.obj2.offsetVector)
					self.obj2.obj.Placement.Base=p2
					
			elif self.obj2.detail=="Vertex.Point":
				sayd("set vertex")
				sayd("punkt index")
				sayd(self.obj2.ix)

				sayd("punkt alte koord")
				say(self.obj2.obj.Placement.Base)
				sayd("neue koords")
				# say(self.obj2.pin.Shape.Vertexes[self.obj2.ix].Point)
				if self.obj2.status>0:
					ixok=self.obj2.ix
				else:
					ixok=findVertex(self.obj2.obj.Placement.Base,self.obj2.pin.Shape,self.obj2.offsetVector)
				self.obj2.status += 1
				
				if ixok>=0:
					self.obj2.obj.Placement.Base=self.obj2.pin.Shape.Vertexes[ixok].Point
					
				else:
					self.obj2.obj.Placement.Base=self.obj2.pin.Shape.Vertexes[self.obj2.ix].Point
				sayd("offset addiert ...")
				sayd(self.obj2.obj.Placement.Base)
				self.obj2.obj.Placement.Base =FreeCAD.Vector(self.obj2.obj.Placement.Base).add(self.obj2.offsetVector)
				sayd(self.obj2.obj.Placement.Base)
			elif self.obj2.detail=="Sketch.Object.StartPoint":
				say( "Sketch.Object.StartPoint")
				if self.obj2.trafoMode == "matrix" or self.obj2.trafoMode == "yz" or self.obj2.trafoMode == "xz":
					FreeCAD.TT=self
					self.obj2.obj.Placement.Base= self.obj2.trafoMatrix.multiply(self.obj2.pin.Geometry[self.obj2.ix].StartPoint)
					say(self.obj2.obj.Placement.Base)
				else:
					self.obj2.obj.Placement.Base=self.obj2.pin.Geometry[self.obj2.ix].StartPoint
				
					
				self.obj2.obj.Placement.Base =FreeCAD.Vector(self.obj2.obj.Placement.Base).add(self.obj2.offsetVector)
			elif self.obj2.detail=="Sketch.Object.EndPoint":
				say( "Sketch.Object.EndPoint !!!")
				if self.obj2.obj.TypeId=='App::Annotation':
					p=self.obj2.pin.Geometry[self.obj2.ix].EndPoint
					p2=p.add(self.obj2.offsetVector)
					self.obj2.obj.Position=p2
				else:
					if self.obj2.trafoMode == "matrix" or self.obj2.trafoMode == "yz" or self.obj2.trafoMode == "xz":
						FreeCAD.TT=self
						self.obj2.obj.Placement.Base= self.obj2.trafoMatrix.multiply(self.obj2.pin.Geometry[self.obj2.ix].EndPoint)
						say(self.obj2.pin.Geometry[self.obj2.ix].EndPoint)
						say(self.obj2.obj.Placement.Base)
					else:
						self.obj2.obj.Placement.Base=self.obj2.pin.Geometry[self.obj2.ix].EndPoint
					self.obj2.obj.Placement.Base =FreeCAD.Vector(self.obj2.obj.Placement.Base).add(self.obj2.offsetVector)
			else:
				say("unerwartete zuordnung detail")
			if self.obj2.pinMode =="2points":
				FreeCAD.ww=self.obj2
				say("auswertung zwiter punkt")
				sp=self.obj2.obj.Placement.Base
				say(sp)
				ep=FreeCAD.Vector()
				if self.obj2.detail2=="Sketch.Object.EndPoint":
					say("EP")
					ep=self.obj2.pin.Geometry[self.obj2.ix2].EndPoint
				elif self.obj2.detail2=="Sketch.Object.StartPoint":
					say("SP")
					ep=self.obj2.pin.Geometry[self.obj2.ix2].StartPoint
				say(ep)
				mdir=ep.sub(sp)
				say(mdir)
				mdir.normalize()
				alpha=math.acos(mdir.x)
				##say(180*alpha/math.pi)
				beta=math.asin(mdir.y)
				if beta<0:
					alpha=2*math.pi-alpha 
				say(0.00+180.00*alpha/math.pi)
				r=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0.00+180.0/math.pi*alpha)
				
				self.obj2.obj.Placement.Rotation=r
				

	def setDetail(self,detailname,param1):
			self.obj2.detail=detailname
			self.obj2.param1=param1
	
	def execute(self,obj):
		sayd("execute _Plugger")
		self.obj2.status=0
		obj.end=obj.start+obj.duration
		if self.obj2.trafoMode == "yz":
			self.obj2.trafoMatrix=FreeCAD.Matrix(
				0,0,0,0,
				1,0,0,0,
				0,1,0,0,
				0,0,0,1);
		if self.obj2.trafoMode == "xz":
			self.obj2.trafoMatrix=FreeCAD.Matrix(
				1,0,0,0,
				0,0,0,0,
				0,1,0,0,
				0,0,0,1);
		obj.setEditorMode("end", 1) #ro


class _ViewProviderPlugger(_ViewProviderActor):
	def getIcon(self):
		return __dir__ + '/icons/plugger.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Plugger',_CommandPlugger())

#---------------------------------------------------------------

def createTranquillizer(name='My_Tranquillizer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyFloat","time","params","time").time=0.02
	_Tranquillizer(obj)
	_ViewProviderTranquillizer(obj.ViewObject)
	return obj

class _CommandTranquillizer(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/tranq.png', 'MenuText': 'Tranquillizer', 'ToolTip': 'Tranquillizer Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Tranquillizer")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createTranquillizer()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return

import time
from time import sleep
	   
class _Tranquillizer(_Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Tranquillizer"
		self.obj2 = obj 

	def execute(self,obj):
		sayd("execute _Tranquillizer")

	def step(self,now):
		sayd(self)
		FreeCAD.tt=self
		time.sleep(self.obj2.time)
		
	def  toInitialPlacement(self):
		pass

class _ViewProviderTranquillizer(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/tranq.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Tranquillizer',_CommandTranquillizer())

#-------------------------------------


def createAdjuster(name='My_Adjuster'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=40
	obj.addProperty("App::PropertyInteger","duration","Base","end").end=40
	obj.addProperty("App::PropertyFloat","va","intervall","va").va=0
	obj.addProperty("App::PropertyFloat","ve","intervall","ve").ve=40
	obj.addProperty("App::PropertyLink","obj","Object","Sketch")
	obj.addProperty("App::PropertyInteger","nr","Object","nummer Datum").nr=1
	obj.addProperty("App::PropertyEnumeration","unit","3D Param","einheit").unit=['deg','mm']
	_Adjuster(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandAdjuster(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/adjuster.png', 'MenuText': 'Adjuster', 'ToolTip': 'Adjuster Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Adjuster")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createAdjuster()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return


		
 
class _Adjuster(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Adjuster"
		self.obj2 = obj 

		
	def step(self,now):
		say("Adjustor step!" + str(now))

		if now<=self.obj2.start or now>self.obj2.end:
			sayd("ausserhalb")
			pass
		else:
			if not self.obj2.obj:
				errorDialog("kein Sketch zugeordnet")
				raise Exception(' self.obj2.obj nicht definiert')
	 
			##FreeCADGui.ActiveDocument.setEdit(self.obj2.obj.Name)
			
			#say(self.ve)
			#say(self.va)
			if 1:
				v=self.obj2.va +  (self.obj2.ve - self.obj2.va)*(now-self.obj2.start)/(self.obj2.end-self.obj2.start)
				say("value=" + str(v))
			try:
				#say("intern")	
				self.obj2.obj.setDatum(self.obj2.nr,FreeCAD.Units.Quantity(str(v) + " " + str(self.obj2.unit)))
				
			except:
				 say("ffehler") 
			#say("sett")
			###FreeCAD.ActiveDocument.recompute()
			##FreeCADGui.ActiveDocument.resetEdit()
			FreeCADGui.updateGui() 

	def setValues(self,va,ve):
		self.obj2.va=va
		self.obj2.ve=ve

	def execute(self,obj):
		say("execute _Adjuster")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration

class _ViewProviderAdjuster(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/adjuster.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Adjuster',_CommandAdjuster())

#---------------------------------------------------------------
def createStyler(name='MyStyler'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=40
	obj.addProperty("App::PropertyInteger","duration","Base","end")

#	obj.addProperty("App::PropertyFloat","va","intervall","va").va=0
#	obj.addProperty("App::PropertyFloat","ve","intervall","ve").ve=40
	obj.addProperty("App::PropertyLink","obj","Object","Objekt")
#	obj.addProperty("App::PropertyInteger","nr","Object","nummer Datum").nr=1#
#	obj.addProperty("App::PropertyEnumeration","unit","3D Param","einheit").unit=['deg','mm']
	# FreeCADGui.getDocument("Unnamed").getObject("Box").Transparency = 2
	obj.addProperty("App::PropertyBool","transparency","Transparency","start").transparency=False
	obj.addProperty("App::PropertyInteger","transpaStart","Transparency","start").transpaStart=0
	obj.addProperty("App::PropertyInteger","transpaEnd","Transparency","end").transpaEnd=40
	obj.addProperty("App::PropertyEnumeration","DisplayStyle","Transparency","end").DisplayStyle=['Flat Lines','Shaded','Wireframe']
	obj.addProperty("App::PropertyBool","visibility","Visibility","toggle visibility").visibility=False
#	obj.addProperty("App::PropertyInteger","transpaStart","transparency","start").transpaStart=0
#	obj.addProperty("App::PropertyInteger","transpaEnd","transparency","end").transpaEnd=40
	
	
	_Styler(obj)
	_ViewProviderStyler(obj.ViewObject)
	return obj

class _CommandStyler(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/styler.png', 'MenuText': 'Styler', 'ToolTip': 'Styler Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Adjuster")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createStyler()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Styler(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Styler"
		self.obj2 = obj 

		
	def step(self,now):
		sayd("Styler step!" + str(now))

		if now<=self.obj2.start or now>self.obj2.end:
			say("ausserhalb")
			pass
		else:
			gob=FreeCADGui.ActiveDocument.getObject(self.obj2.obj.Name)
			if not self.obj2.obj:
				errorDialog("kein Sketch zugeordnet")
				raise Exception(' self.obj2.obj nicht definiert')
			if self.obj2.transparency:

				gob.Transparency=90
				relativ=1.00/(self.obj2.end-self.obj2.start)
				gob.Transparency=  int(relativ* (self.obj2.transpaEnd -self.obj2.transpaStart)*(now-self.obj2.start)) + self.obj2.transpaStart
		if now==self.obj2.start or now==self.obj2.end:
			if self.obj2.visibility:
				gob=FreeCADGui.ActiveDocument.getObject(self.obj2.obj.Name)
				gob.Visibility = not gob.Visibility
		FreeCADGui.updateGui() 
			
			

	def setValues(self,va,ve):
		self.obj2.va=va
		self.obj2.ve=ve

	def execute(self,obj):
		sayd("execute _Styler")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration

class _ViewProviderStyler(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/styler.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Styler',_CommandStyler())

#---------------------------------------------------------------

def createPhotographer(name='My_Photographer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=40000
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=40000
	obj.addProperty("App::PropertyInteger","size_x","Output","start").size_x=640
	obj.addProperty("App::PropertyInteger","size_y","Output","end").size_y=480
	obj.addProperty("App::PropertyPath","fn","Output","outdir").fn="/tmp/animation/t"
	obj.addProperty("App::PropertyEnumeration","format","Output","Bildformat").format=["png","jpg","bmp"]
	obj.addProperty("App::PropertyEnumeration","camDirection","Camera","Sichtrichtung").camDirection=["Front","Top","Axometric","Left","View"]
	obj.addProperty("App::PropertyInteger","camHeight","Camera","Ausschnitt Hoehe").camHeight=100
	_Photographer(obj)
	_ViewProviderPhotographer(obj.ViewObject)
	return obj

class _CommandPhotographer:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/photographer.png', 'MenuText': 'Photographer', 'ToolTip': 'Photographer Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Photographer")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createPhotographer()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return




class _Photographer(_Actor):

	def __init__(self,obj):
		self.obj2 = obj 
		obj.Proxy = self
		self.Type = "Photographer"

	def execute(self,obj):
		sayd("execute _Photographer")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration

	def step(self,now):
		if now<=self.obj2.start or now>self.obj2.end:
			pass
		else:
			FreeCADGui.Selection.clearSelection()
			FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)

			cam= '#Inventor V2.1 ascii\n\n\nOrthographicCamera {\n  viewportMapping ADJUST_CAMERA\n         height ' + str(self.obj2.camHeight) +'\n\n}\n'
			#say(cam)
			if self.obj2.camDirection != 'View':
				FreeCADGui.activeDocument().activeView().setCamera(cam)
			#say(FreeCADGui.activeDocument().activeView().getCamera())
			
			if self.obj2.camDirection == 'Top':
					#FreeCADGui.ActiveDocument.ActiveView.viewTop()
					camt='#Inventor V2.1 ascii\n\n\nOrthographicCamera {\n  viewportMapping ADJUST_CAMERA\n  position 0 0 1\n  orientation 0 0 1  0\n  nearDistance -698.30103\n  farDistance 301.30103\n  aspectRatio 1\n  focalDistance 5\n  height 500\n\n}\n'
					camt='#Inventor V2.1 ascii\n\n\nOrthographicCamera {\n  viewportMapping ADJUST_CAMERA\n  position 0 0 1\n  orientation 0.0001 0 1  0.0001\n  nearDistance -698.30103\n  farDistance 301.30103\n  aspectRatio 1\n  focalDistance 5\n  height 500\n\n}\n'
					FreeCADGui.activeDocument().activeView().setCamera(camt)
			if self.obj2.camDirection == 'Front':
					# FreeCADGui.ActiveDocument.ActiveView.viewFront()
					camt='#Inventor V2.1 ascii\n\n\nOrthographicCamera {\n  viewportMapping ADJUST_CAMERA\n  position 0 -4.9999995 -3.9999998\n  orientation -1 0 0  4.712389\n  nearDistance -54.94503\n  farDistance 515.51514\n  aspectRatio 1\n  focalDistance 5\n  height 500\n\n}\n'
					camt='#Inventor V2.1 ascii\n\n\nOrthographicCamera {\n  viewportMapping ADJUST_CAMERA\n  position 0 -4.9999995 -3.9999998\n  orientation -1.002 0.002 -0.003  4.7123\n  nearDistance -54.94503\n  farDistance 515.51514\n  aspectRatio 1\n  focalDistance 5\n  height 500\n\n}\n'
					FreeCADGui.activeDocument().activeView().setCamera(camt)
			if self.obj2.camDirection == 'Axometric':
					FreeCADGui.ActiveDocument.ActiveView.viewAxometric()
			if self.obj2.camDirection == 'Left':
					FreeCADGui.ActiveDocument.ActiveView.viewLeft()
			
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.updateGui() 
			
			kf= "%04.f"%now
			fn=self.obj2.fn+kf+'.png'
			
			dir = os.path.dirname(fn)

			try:
				os.stat(dir)
			except:
				os.mkdir(dir)  
    
			fn=self.obj2.fn+kf+'.'+self.obj2.format 
			fn2=self.obj2.fn+'_XXX_' +kf+'.'+self.obj2.format 
			FreeCADGui.activeDocument().activeView().saveImage(fn,self.obj2.size_x,self.obj2.size_y,'Current')
			#my_render(fn2)
	def  toInitialPlacement(self):
		pass


class _ViewProviderPhotographer(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/photographer.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Photographer',_CommandPhotographer())

#---------------------------------------------------------------

def createManager(name='My_Manager'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","intervall","Base","intervall").intervall=10
	obj.addProperty("App::PropertyString","text","params","text").text="NO"
	_Manager(obj)
	_ViewProviderManager(obj.ViewObject)
	return obj

class _CommandManager(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/manager.png', 'MenuText': 'Manager', 'ToolTip': 'Manager Dialog'} 

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

import os.path
import Inspector

#--------------------------------------------

def col(actor,obstacles):
	
	av=actor.Shape.BoundBox
	for obl in obstacles:
		ov=obl.Shape.BoundBox
		if ov.XMin < av.XMax  and  ov.XMax > av.XMin and ov.YMin <= av.YMax and  ov.YMax >= av.YMin and  ov.ZMin <= av.ZMax and  ov.ZMax >= av.ZMin:
			print obl.Label
			obl.ViewObject.DiffuseColor=(1.0,0.0,0.0)
		else:
			obl.ViewObject.DiffuseColor=(1.0,1.0,0.0)  

def checkCollision():

	App=FreeCAD
	cy=App.ActiveDocument.Cylinder
	c=App.ActiveDocument.Cone
	gd=App.ActiveDocument.GeodesicDome
	b=App.ActiveDocument.Box
	col(b,[cy,c,gd,App.ActiveDocument.Torus])


#--------------------------------------------

class _Manager(_Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Manager"
		self.obj2=obj


	def execute(self,obj):
		sayd("execute _Manager")

	def register(self,obj):
		self.obj2.targets.append(obj)

	def run(self,intervall=-1):
		sayd("run  intervall=" + str(intervall))
		
		if (intervall<0):
			intervall=self.obj2.intervall
		sayd("x1")
		# else:
		if hasattr(self,'obj2'):
			t=FreeCAD.ActiveDocument.getObject(self.obj2.Name)
		else:
			raise Exception("obj2 not found --> reinit the file!")
		sayd("x2")
		for ob in t.OutList:
			say(ob.Label)
			ob.Proxy.initialize()
			ob.Proxy.execute(ob)
		
		
		for nw in range(intervall):	
			say("************************* manager run loop:" + str(nw) + "/" + str(intervall));
			
			try:
				st=FreeCAD.ActiveDocument.getObject('Common')
				## st.touch()
				FreeCADGui.Selection.clearSelection()
				
				FreeCAD.ActiveDocument.recompute()
			except:
				say("Fehler touch")
			
			#-----------------------
			# 
			## checkCollision()
			#
			#
			#-----------------------
			
			if os.path.exists("/tmp/stop"):
					say("notbremse gezogen")
					raise Exception("Notbremse Manager main loop")
			for ob in t.OutList:
				if 1: # fehler analysieren
					sayd("step fuer ")
					sayd(ob.Label)
					if ob.ViewObject.Visibility:
							ob.Proxy.step(nw)
				else:
					try:
						sayd(ob.Proxy)
						if ob.ViewObject.Visibility:
							ob.Proxy.step(nw)
					except:
						say("fehler step 2")
						raise Exception("step nicht ausfuerbar")

			#------
			if False:
				try:
					import assembly2solver
					try:
						assembly2solver.solveConstraints(App.ActiveDocument)
					except:
						say("problem assembly2solver.solveConstraints(App.ActiveDocument)")
				except:
					# no assembly available
					pass
			#------
					
			FreeCADGui.updateGui()
			Inspector.step(now=0)
			 
		FreeCADGui.Selection.clearSelection()
		FreeCADGui.Selection.addSelection(FreeCAD.ActiveDocument.getObject(self.obj2.Name))

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
#-------------------------

# testdialig in comboview task fenster
import FreeCAD
import FreeCADGui
import Part
from PySide import QtGui, QtCore


class AddMyWidget(QtGui.QWidget):
	def __init__(self,vobj,fun,fun2=None,fun3=None, *args):
		QtGui.QWidget.__init__(self, *args)
		self.vobj=vobj
		self.fun=fun
		self.fun2=fun2
		self.fun3=fun3
		self.vollabel = QtGui.QLabel('Volume')
		self.volvalue = QtGui.QLineEdit()
		self.checkBox = QtGui.QCheckBox()
		self.radioButton = QtGui.QRadioButton()
		self.pushButton = QtGui.QPushButton()
		self.pushButton.clicked.connect(self.on_pushButton_clicked)
		layout = QtGui.QGridLayout()
		#layout.addWidget(self.vollabel, 0, 0)
		#layout.addWidget(self.volvalue, 0, 1)
		#layout.addWidget(self.checkBox, 1, 2)
		#layout.addWidget(self.radioButton, 1, 0)

		layout.addWidget(self.pushButton, 1,1)
		if fun2:
			self.pushButton2 = QtGui.QPushButton()
			self.pushButton2.clicked.connect(self.on_pushButton_clicked2)
			layout.addWidget(self.pushButton2, 2,1)
		if fun3:
			self.pushButton3 = QtGui.QPushButton()
			self.pushButton3.clicked.connect(self.on_pushButton_clicked3)
			layout.addWidget(self.pushButton3, 3,1)

		if 0:
			# close control dialog
			self.pushButton3 = QtGui.QPushButton()
			self.pushButton3.clicked.connect(self.on_pushButton_clicked)
			layout.addWidget(self.pushButton3, 3,1)
		
		self.setLayout(layout)
		self.setWindowTitle("Animation Manager Control Panel")

	def on_pushButton_clicked(self):
		#FreeCAD.Console.PrintMessage("rt")
		#FreeCAD.zx=self
		#say(self)
		self.fun(self.vobj)
		FreeCADGui.Control.closeDialog()
		
	def on_pushButton_clicked2(self):
		#FreeCAD.Console.PrintMessage("rt")
		#FreeCAD.zx=self
		#say(self)
		self.fun2(self.vobj)
		FreeCADGui.Control.closeDialog()
	
	def on_pushButton_clicked3(self):
		#FreeCAD.Console.PrintMessage("rt")
		#FreeCAD.zx=self
		#say(self)
		self.fun3(self.vobj)
		FreeCADGui.Control.closeDialog()
	
		

class AddMyTask():
	def __init__(self,vobj,fun,fun2=None,fun3=None):
		reinit()
		self.form = AddMyWidget(vobj,fun,fun2,fun3)
		#FreeCAD.zz=vobj
		#FreeCAD.zy=self
		#say("Admm my task")
		#say(vobj)

	def getStandardButtons(self):
		return int(QtGui.QDialogButtonBox.Close)

	def isAllowedAlterSelection(self):
		return True

	def isAllowedAlterView(self):
		return True

	def isAllowedAlterDocument(self):
		return True


def runManager(vobj=None):
	#say(vobj)
	#FreeCAD.zz=vobj
	unlockManager()
	sayd("manager unlocked")
	if vobj:
		tt=vobj.Object
		FreeCAD.ActiveDocument.openTransaction("run Manager")
		tt.Proxy.run()
		FreeCAD.ActiveDocument.commitTransaction()
		FreeCAD.ActiveDocument.recompute()
	else:
		FreeCAD.ActiveDocument.openTransaction("run Manager")
		FreeCADGui.doCommand("import Animation")
		FreeCADGui.doCommand("M=FreeCADGui.Selection.getSelectionEx()")
		FreeCADGui.doCommand("tt=M[0].Object")
		FreeCADGui.doCommand("print(tt)")
		FreeCADGui.doCommand("tt.Proxy.run()")
		FreeCAD.ActiveDocument.commitTransaction()
		FreeCAD.ActiveDocument.recompute()
		#M = FreeCADGui.Selection.getSelectionEx()
		#tt=M[0].Object
		#sayd(tt)
	##tt.Proxy.run()
	say("done")

def stopManager(vobj=None):
	fname='/tmp/stop'
	fhandle = open(fname, 'a')
	fhandle.close()

def unlockManager(vobj=None):
	import os
	from os import remove
	fname='/tmp/stop'
	try:
		os.remove(fname)
	except:
		pass

class _ViewProviderManager(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/manager.png'
		
	def doubleClicked(self,vobj):
		FreeCAD.tt=self
		#say(self)
		#panel = AddMyTask(runManager,stopManager,unlockManager)
		panel = AddMyTask(self,runManager,stopManager)
#		panel.form.volvalue.setText("VOL-VALUE")
#		panel.form.vollabel.setText("VOL-LABELLO")
		panel.form.pushButton.setText("Run ")
		panel.form.pushButton2.setText("Stop")
#		panel.form.pushButton3.setText("Unlock ")
		FreeCADGui.Control.showDialog(panel)

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Manager',_CommandManager())

#---------------------------------------------------------------

def reinitxx():
	say("reinit deaktiverit")
	pass

def reinit():
	''' zum re initialisieren beim dateiload und bei alten dateien'''
	for obj in FreeCAD.ActiveDocument.Objects:
		try:
			if hasattr(obj,'Proxy'):
				say ("re init Proxy " + str(obj.Name))
				if hasattr(obj.Proxy,'Type'):
					##say("we")
					##say(obj.Proxy.Type)
					pass
				else:
					##say("reinit")
						obj.Proxy.__init__(obj)
					##say(obj.Proxy.Type)
				
				# print("init " +obj.Name)
				if obj.Proxy.Type=='Plugger':
					if not hasattr(obj,'status'):
						obj.addProperty("App::PropertyInteger","status","nummer","intern").status=0
					if not hasattr(obj,'offsetVector'):
						obj.addProperty("App::PropertyVector","offsetVector","3D Param","offsetVector").offsetVector=FreeCAD.Vector(0,0,0)
				if obj.Proxy.Type=='Adjustor':
					if not hasattr(obj,'unit'):
						obj.addProperty("App::PropertyEnumeration","unit","3D Param","einheit").unit=['deg','mm']
				if obj.Proxy.Type=='Photographer':
					if not hasattr(obj,'camDirection'):
						obj.addProperty("App::PropertyEnumeration","camDirection","Camera","Sichtrichtung").camDirection=["Front","Top","Axometric","Left"]
					if not hasattr(obj,'camHeight'):
						obj.addProperty("App::PropertyInteger","camHeight","Camera","Ausschnitt Hoehe").camHeight=100
				if obj.Proxy.Type=='Rotator':
					if not hasattr(obj,'rotCenterRelative'):
						obj.addProperty("App::PropertyBool","rotCenterRelative","3D Param","Rotationsachse Zentrum relativ").rotCenterRelative=False
				sayd(obj)
		except:
			pass

	FreeCAD.animationLock=False
	FreeCAD.animataionInit=False

#---------------------------------

class _Starter:
	''' Re initialisierung einer geladenen Datei'''
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/reset.png', 'MenuText': 'ReInitialize', 'ToolTip': 'Re-Initialize after Loading'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		reinit()

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('A_Starter',_Starter())


class _Runner:
	''' Manager als Transaktion laufen lassen'''
	def GetResources(self): 
		# return {'Pixmap' : __dir__ + '/icons/animation.png', 'MenuText': 'Run Manager', 'ToolTip': 'Run Manager'} 
		return {'Pixmap' : __dir__ + '/icons/animation.png', 'MenuText': 'Run Manager', 'ToolTip': 'Run Manager'} 
		return {'Pixmap' : '../Mod/Animation/icons/animation.png', 'MenuText': 'Run Manager', 'ToolTip': 'Run Manager'} 
		return False

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		reinit()
		M = FreeCADGui.Selection.getSelectionEx()
		say(M)
		if len(M)==0:
			FreeCAD.ActiveDocument.openTransaction("run Manager")
			FreeCADGui.doCommand("App.ActiveDocument.My_Manager.Proxy.run(-1)")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		elif M[0].Object.Proxy.Type <> '_Manager':
			errorDialog("Manager auswahlen")
		else:
			FreeCAD.ActiveDocument.openTransaction("run Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("M=FreeCADGui.Selection.getSelectionEx()")
			FreeCADGui.doCommand("tt=M[0].Object")
			FreeCADGui.doCommand("print(tt)")
			FreeCADGui.doCommand("tt.Proxy.run(-1)")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()



if FreeCAD.GuiUp:
	FreeCADGui.addCommand('A_Runner',_Runner())

# fast Helpers
# define  Activated !!
	
class _B1: 
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/icon1.svg', 'MenuText': 'B1', 'ToolTip': 'B1'} 
	def IsActive(self):
		return False
	def Activated(self):
		say("running _B1 dummy")

class _B2:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/icon2.svg', 'MenuText': 'B2', 'ToolTip': 'B2'} 
	def IsActive(self):
		return False
	def Activated(self):
		say("running B2  - dummy ")

class _B3:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/icon3.svg', 'MenuText': 'Edit Object', 'ToolTip': 'Edit Object'} 
	def IsActive(self):
		return False
	def Activated(self):
		say("runngi _B3")
		t=FreeCADGui.Selection.getSelection()
		FreeCADGui.ActiveDocument.setEdit(t[0].Name,0)


if FreeCAD.GuiUp:
	FreeCADGui.addCommand('B1',_B1())
	FreeCADGui.addCommand('B2',_B2())
	FreeCADGui.addCommand('EditObject',_B3())

#-------------------------------
#
# Action-Complex
#
#-------------------------------

class _ScriptAction(object):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_ScriptAction"
	def execute(self,obj):
			say(str(self) + " executed")
			say(obj)
	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def croak(self,index=0,debug=0,mode="",params=[]):
		intent="x-- " *index
		say(intent + "CROAK "+ self.Type)
		
	def run(self,index=0,debug=0,mode="",params=[]):
		#say("run" +str(self))
		FreeCAD.ttz=self
		#say(self.obj2.Name)
		#say(self.Object.Label)
		intent="x-- " *index
		#say(self.Type)
		#say(self.obj2.Label)
		self.croak(index,debug,mode,params)
		if debug:
			say(intent + self.Type + ": "+ self.obj2.Label)
		else:
			say(intent + self.obj2.Label) 
		#say("index="+ str(index))
		#say("subparts")
		t=FreeCAD.ActiveDocument.getObject(self.obj2.Name)
		for ob in t.OutList:
			# say(intent + ob.Label)
			FreeCAD.ttu=ob
			try:
				ob.Proxy.run(index+1,debug,mode,[self.obj2.Label])
			except:
				say("run sub fehlerhaft")
		#say("end subparts")
		

def runScript():
	say("run Skript")
	M = FreeCADGui.Selection.getSelectionEx()
	tt=M[0].Object
	say(tt)
	tt.Proxy.run()
	say("done")
	
class _ViewProviderScriptAction(object):
	"A View Provider for the Mover object"

	
	def getIcon(self):
		return __dir__ + '/icons/scriptaction.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		say("attach")
		return	
	
	def claimChildren(self):
		say ("claim Children")
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None
		
	def doubleClicked(self,vobj):
		FreeCAD.tt=self
		say(self)
		panel = AddMyTask(runScript,stopManager,unlockManager)
		panel.form.volvalue.setText("VOL-VALUE")
		panel.form.vollabel.setText("VOL-LABELLO")
		panel.form.pushButton.setText("Run ")
		panel.form.pushButton2.setText("Stop")
		panel.form.pushButton3.setText("Unlock ")
		FreeCADGui.Control.showDialog(panel)
		
def createScriptAction(name='My_ScriptAction'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","intervall","start").start=10
	obj.addProperty("App::PropertyInteger","end","intervall","end").end=40
	obj.addProperty("App::PropertyPlacement","initPlace","3D Param","initPlace")
	obj.addProperty("App::PropertyVector","motionVector","3D Param","motionVector").motionVector=FreeCAD.Vector(100,0,0)
	obj.addProperty("App::PropertyLink","obj2","3D Param","moving object ")
	_ScriptAction(obj)
	_ViewProviderScriptAction(obj.ViewObject)
	return obj

class _CommandScriptAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/scriptaction.png', 'MenuText': 'Script Action generic', 'ToolTip': 'SA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createScriptAction()")
			say("I create a Script-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return

#--------------------------------------------------------------------------
# start loop action

class _LoopAction(_ScriptAction):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_LoopAction"

class _ViewProviderLoopAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/loopaction.png'
   
		
def createLoopAction(name='My_LoopAction'):
	'''creatLoopAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_LoopAction(obj)
	_ViewProviderLoopAction(obj.ViewObject)
	return obj

class _CommandLoopAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/loopaction.png', 'MenuText': 'Loop', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createLoopAction()")
			say("I create a Loop-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end loop action
#-----------------------------------------------------------------------------------------------------------
# start While action
class _WhileAction(_ScriptAction):
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_WhileAction"

class _ViewProviderWhileAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/whileaction.png'
   
		
def createWhileAction(name='My_WhileAction'):
	'''creatWhileAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_WhileAction(obj)
	_ViewProviderWhileAction(obj.ViewObject)
	return obj

class _CommandWhileAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/whileaction.png', 'MenuText': 'while do', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createWhileAction()")
			say("I create a While-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end While action 
#--------------------------------------------------------------
# start Repeat action
class _RepeatAction(_ScriptAction):
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_RepeatAction"

class _ViewProviderRepeatAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/repeataction.png'
   
		
def createRepeatAction(name='My_RepeatAction'):
	'''creatRepeatAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_RepeatAction(obj)
	_ViewProviderRepeatAction(obj.ViewObject)
	return obj

class _CommandRepeatAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/repeataction.png', 'MenuText': 'Repeat until', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createRepeatAction()")
			say("I create a Repeat-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end Repeat action 
#--------------------------------------------------------------
# start False action
class _FalseAction(_ScriptAction):
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_FalseAction"

	def croak(self,index=0,debug=0,mode="",params=[]):
		intent="x-- " *index
		say(intent + "CROAK "+   " ELSE:")


class _ViewProviderFalseAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/falseaction.png'
   
		
def createFalseAction(name='My_FalseAction'):
	'''creatFalseAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_FalseAction(obj)
	_ViewProviderFalseAction(obj.ViewObject)
	return obj

class _CommandFalseAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/falseaction.png', 'MenuText': 'If else', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createFalseAction()")
			say("I create a False-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end False action 
#--------------------------------------------------------------
# start True action
class _TrueAction(_ScriptAction):
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_TrueAction"

	def croak(self,index=0,debug=0,mode="",params=[]):
		intent="x-- " *index
		say(intent + "CROAK "+   " IF " + params[0] + "?:")



class _ViewProviderTrueAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/trueaction.png'
   
		
def createTrueAction(name='My_TrueAction'):
	'''creatTrueAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_TrueAction(obj)
	_ViewProviderTrueAction(obj.ViewObject)
	return obj

class _CommandTrueAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/trueaction.png', 'MenuText': 'If then', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createTrueAction()")
			say("I create a True-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end True action 
#--------------------------------------------------------------
# start Case action
class _CaseAction(_ScriptAction):
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_CaseAction"

class _ViewProviderCaseAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/caseaction.png'
   
		
def createCaseAction(name='My_CaseAction'):
	'''creatCaseAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_CaseAction(obj)
	_ViewProviderCaseAction(obj.ViewObject)
	return obj

class _CommandCaseAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/caseaction.png', 'MenuText': 'Case', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createCaseAction()")
			say("I create a Case-Action")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end Case action 
#--------------------------------------------------------------
# start Query action
class _QueryAction(_ScriptAction):
	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_QueryAction"

class _ViewProviderQueryAction(_ViewProviderScriptAction):
	"A View Provider for the Mover object"

	def getIcon(self):
		return __dir__ + '/icons/queryaction.png'

def createQueryAction(name='My_QueryAction'):
	'''creatQueryAction(name)'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_QueryAction(obj)
	_ViewProviderQueryAction(obj.ViewObject)
	return obj

class _CommandQueryAction:
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/queryaction.png', 'MenuText': 'Question', 'ToolTip': 'LA-TT'} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Manager")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createQueryAction()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
# end Query action 
#--------------------------------------------------------------

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('ScriptAction',_CommandScriptAction())
	FreeCADGui.addCommand('LoopAction',_CommandLoopAction())
	FreeCADGui.addCommand('WhileAction',_CommandWhileAction())
	FreeCADGui.addCommand('RepeatAction',_CommandRepeatAction())
	FreeCADGui.addCommand('FalseAction',_CommandFalseAction())
	FreeCADGui.addCommand('TrueAction',_CommandTrueAction())
	FreeCADGui.addCommand('CaseAction',_CommandCaseAction())
	FreeCADGui.addCommand('QueryAction',_CommandQueryAction())



#------------------------------------------------


#-------------------------------------


def createFiller(name='My_Filler'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=110
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=100
	obj.addProperty("App::PropertyLink","obj","Base","Sketch")
	obj.addProperty("App::PropertyLink","objFiller","Base","Sketch")
	obj.addProperty("App::PropertyLink","objCommon","Base","Sketch")

	obj.addProperty("App::PropertyEnumeration","mode","Config","einheit").mode=['fill','slice']
	obj.addProperty("App::PropertyEnumeration","direction","Config","einheit").direction=['+z','-z','+x','-x','+y','-y']
	obj.addProperty("App::PropertyFloat","thickness","Config","ve").thickness=10.0
	obj.addProperty("App::PropertyFloat","transparency","Config","ve").transparency=80
	obj.addProperty("App::PropertyColor","color","Config","ve").color=(1.0,1.0,0.0)
	_Filler(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandFiller(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/filler.png', 'MenuText': 'Filler', 'ToolTip': 'Filler Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Filler")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createFiller()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Filler(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Filler"
		self.obj2 = obj
		# for the recursive execute problem 
		# - see http://forum.freecadweb.org/viewtopic.php?f=3&t=1894
		self.ignore=False 

		
	def step_fill(self,now):
		say("Filler step!" + str(now))
		self.ignore=True
		if now<=self.obj2.start:
			self.obj2.objCommon.ViewObject.Visibility=False
		if now<=self.obj2.start or now>self.obj2.end:
			sayd("ausserhalb")
			pass
		else:
			if not self.obj2.obj:
				errorDialog("kein Sketch zugeordnet")
				raise Exception(' self.obj2.obj nicht definiert')
			f=self.obj2.objFiller
#			maxz=12
			b=self.obj2.obj
			bb=b.Shape.BoundBox
			pim=FreeCAD.Vector(bb.XMin,bb.YMin,bb.ZMin)
			maxz=bb.ZMax-bb.ZMin

			# relative=rel
			say(now)
			say(self.obj2.start)
			say(self.obj2.duration)
			relative=float(now-self.obj2.start)/self.obj2.duration
			#if False:
			say(relative)
			f.Height= maxz*relative
			say(f.Height)
			FreeCAD.ActiveDocument.recompute()
			obj=self.obj2.objCommon
			if  f.Height<=0:
				obj.ViewObject.Visibility=False
			else:
				obj.ViewObject.Visibility=True
			#obj.ViewObject.ShapeColor=(1.0,.0,0.0)
			obj.ViewObject.ShapeColor=obj=self.obj2.color
			self.ignore=False

	def step_slice(self,now):
		say("Slicer step!" + str(now))
		self.ignore=True
		if now<=self.obj2.start:
			self.obj2.objCommon.ViewObject.Visibility=False
		if now<=self.obj2.start or now>self.obj2.end:
			sayd("ausserhalb")
			pass
		else:
			if not self.obj2.obj:
				errorDialog("kein Sketch zugeordnet")
				raise Exception(' self.obj2.obj nicht definiert')
			f=self.obj2.objFiller
			
			maxz=12
			# relative=rel
			say(now)
			say(self.obj2.start)
			say(self.obj2.duration)
			relative=float(now-self.obj2.start)/self.obj2.duration
			#if False:
			say(relative)
			#f.Height= maxz*relative
			#say(f.Height)
			#---------------------------------------------
			
			maxz=10
			minz=-2
			# relative=rel
			diff=1
			ba=f.Placement.Base
			f.Placement.Base=FreeCAD.Vector(ba.x,ba.y,minz+relative*(maxz-minz+diff)-diff)
			f.Height=diff
			FreeCAD.ActiveDocument.recompute()
			# obj=FreeCAD.getDocument("Unnamed").getObject("Common")
			obj=self.obj2.objCommon
			if relative <=0 or relative>=1:
				obj.ViewObject.Visibility=False
			else:
				obj.ViewObject.Visibility=True
#			obj.ViewObject.ShapeColor=(1.0,.0,0.0)

			#-------------------------
			FreeCAD.ActiveDocument.recompute()
			
#			if  f.Height<=0:
#				obj.ViewObject.Visibility=False
#			else:
#				obj.ViewObject.Visibility=True
			#obj.ViewObject.ShapeColor=(1.0,.0,0.0)
			obj.ViewObject.ShapeColor=obj=self.obj2.color
			self.ignore=False





	def step(self,now):
		if (self.obj2.mode=="fill"):
			self.step_fill(now)
		else:
			self.step_slice(now)


	def setValues(self,va,ve):
		self.obj2.va=va
		self.obj2.ve=ve

	def onChanged(self,obj,prop):
		say("onChanged " + str(self))
		say(obj)
		say(prop)
		FreeCAD.mytoc=[self,obj,prop]

	def onBeforeChange(self,obj,prop):
		say("on Before Changed " )
		say(arg)
		say(obj)
		say(prop)
		

	def execute(self,obj):
		obj.end=obj.start+obj.duration
		obj.setEditorMode("end", 1) #ro
		obj.setEditorMode("objFiller", 1) #ro
		obj.setEditorMode("objCommon", 1) #ro
		obj.setEditorMode("direction", 1) #ro
		say("execute _Filler")
		if self.ignore:
			say("ignore")
			return
		
		obj.end=obj.start+obj.duration
		
		# wenn noch keine zuordnung erfolgt ist
		App=FreeCAD
		#b=FreeCAD.getDocument("Unnamed").getObject("Fusion")
		FreeCAD.ff=self
		b=self.obj2.obj
		bb=b.Shape.BoundBox
		pim=FreeCAD.Vector(bb.XMin,bb.YMin,bb.ZMin)
		if not self.obj2.objFiller:
			say("erzeuge filler")
			f=FreeCAD.ActiveDocument.addObject("Part::Box","Filler")
			self.obj2.objFiller=f
		else:
			f=self.obj2.objFiller
		f.Placement.Base=pim
		f.Length=bb.XMax-bb.XMin
		f.Width=bb.YMax-bb.YMin
		f.Height=bb.ZMax-bb.ZMin
		if not self.obj2.objCommon:
			say("erzeuge common")
			c=FreeCAD.activeDocument().addObject("Part::MultiCommon","Common")
			self.obj2.objCommon=c
		else:
			c=self.obj2.objCommon

		say("erzeugt")
		c.Shapes = [b,f]
		 
		f.Height= 0.5*f.Height
	
		if False:
			FreeCAD.ActiveDocument.recompute()

			c.ViewObject.ShapeColor=(1.0,.0,0.0)
			c.ViewObject.Transparency=20
			b.ViewObject.Transparency=90
			b.ViewObject.Visibility=True
			c.ViewObject.DisplayMode = "Shaded"




		
		

class _ViewProviderFiller(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/filler.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Filler',_CommandFiller())




def createGearing(name='My_Gearing'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=110
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=100
	obj.addProperty("App::PropertyLink","obj","Base","Sketch")
	obj.addProperty("App::PropertyLink","objStar","Base","Sketch")
	obj.addProperty("App::PropertyLink","objPlanet","Base","Sketch")
	obj.addProperty("App::PropertyLink","objMoon","Base","Sketch")

#	obj.addProperty("App::PropertyEnumeration","mode","Config","einheit").mode=['fill','slice']
#	obj.addProperty("App::PropertyEnumeration","direction","Config","einheit").direction=['+z','-z','+x','-x','+y','-y']
	obj.addProperty("App::PropertyFloat","dayStar","Config","ve").dayStar=100
	obj.addProperty("App::PropertyFloat","dayPlanet","Config","ve").dayPlanet=-50
	obj.addProperty("App::PropertyFloat","dayMoon","Config","ve").dayMoon=10
	obj.addProperty("App::PropertyFloat","distStarPlanet","Config","ve").distStarPlanet=60
	obj.addProperty("App::PropertyFloat","distPlanetMoon","Config","ve").distPlanetMoon=30
	
	obj.addProperty("App::PropertyColor","color","Config","ve").color=(1.0,1.0,0.0)
	
	
	App=FreeCAD
	sp=App.activeDocument().addObject("Part::Compound","Ge_sp")
	s=App.activeDocument().addObject("Part::Compound","Ge_s")
	pm=App.activeDocument().addObject("Part::Compound","Ge_pm")
	p=App.activeDocument().addObject("Part::Compound","Ge_p")
	m=App.activeDocument().addObject("Part::Compound","Ge_m")
	b=App.ActiveDocument.addObject("Part::Box","Box")
	b1=App.ActiveDocument.addObject("Part::Box","Box")
	b2=App.ActiveDocument.addObject("Part::Box","Box")
	b.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	b1.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	b2.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	m.Placement.Base=FreeCAD.Vector(30,0,0.0)
	pm.Placement.Base=FreeCAD.Vector(60,0,0.0)
	p.Links=[b]
	s.Links=[b1]
	m.Links=[b2]
	pm.Links=[p,m]
	sp.Links=[s,pm]
	obj.obj=sp
	obj.objStar=b1
	obj.objPlanet=b
	obj.objMoon=b2
	
	
	
	_Gearing(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandGearing(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/gearing.png', 'MenuText': 'Gearing', 'ToolTip': 'Gearing Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Gearing")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createGearing()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return

def rotstep(s,day):
	an=	s.Placement.Rotation.Angle
	say("rotstep" + s.Label)
	say(an*180/math.pi)
	say("step" +str(360/day))
	if s.Placement.Rotation.Axis.z==-1 :
		an=	s.Placement.Rotation.Angle - math.pi * 2/day
		say("minus")
	else:
		an=	s.Placement.Rotation.Angle + math.pi * 2/day
		say("plus")
	if an <0:
		an += 2*math.pi
		say("add 360")
	if an > 2*math.pi:
		an -= 2*math.pi
		say("minus 360")
		
	s.Placement.Rotation.Angle = an
	say(an*180/math.pi)

	 
class _Gearing(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Gearing"
		self.obj2 = obj
		# for the recursive execute problem 
		# - see http://forum.freecadweb.org/viewtopic.php?f=3&t=1894
		self.ignore=False 

		
	def step(self,now):
		say("Gearing step!" + str(now))
		FreeCAD.R=self
		self.ignore=True
#		if now<=self.obj2.start:
#			self.obj2.objCommon.ViewObject.Visibility=False
		
			
		if now<self.obj2.start or now>self.obj2.end:
			sayd("ausserhalb")
			pass
		else:
			if not self.obj2.obj:
				errorDialog("kein Sketch zugeordnet")
				raise Exception(' self.obj2.obj nicht definiert')
			sys=self.obj2.obj
			s=sys.Links[0]
			pm=sys.Links[1]
			p=pm.Links[0]
			m=pm.Links[1]
			#say("sonne "+ s.Label)
			#say("planet "+ p.Label)
			#say("moinde" + m.Label)
			
			if now==self.obj2.start:
				s.Placement.Rotation.Axis=FreeCAD.Vector(0,0,1)
				p.Placement.Rotation.Axis=FreeCAD.Vector(0,0,1)
				m.Placement.Rotation.Axis=FreeCAD.Vector(0,0,1)
				
			# Eigenachsen Rotationen
			print (s.Placement.Rotation.Angle)
			an=s.Placement.Rotation.Angle
			ax=s.Placement.Rotation.Axis
			day_star=self.obj2.dayStar
			day_planet=self.obj2.dayPlanet
			day_moon=self.obj2.dayMoon

			rotstep(s,day_star)
			rotstep(p,day_planet)
			rotstep(m,day_moon)
			#p.Placement.Rotation.Angle += math.pi * 2/day_planet
			#m.Placement.Rotation.Angle += math.pi * 2/day_moon
			
			# Schenkel Rotationen
			sys.Placement.Rotation.Angle += 0
			pm.Placement.Rotation.Angle += 0
			
			FreeCAD.activeDocument().recompute()


		self.ignore=False



	def onChanged(self,obj,prop):
		say("**	onChanged ")
		if hasattr(FreeCAD,"animationLock"):
			if FreeCAD.animationLock:
				return
			
		FreeCAD.animationLock=True
		say("------------------------------***Lock EIN")
#		say(obj)
		say(obj.Label + " "  + prop)
		FreeCAD.mytoc=[self,obj,prop]
		oldval=FreeCAD.animation['changed'][2]
		val=obj.getPropertyByName(prop)
		say("old:" + str(oldval) + " new:" + str(val))

		
		# g=FreeCAD.getDocument("getriebe").getObject("My_Gearing")
		g=obj
		
			
		sys=g.obj
		
		s=sys.Links[0]
		pm=sys.Links[1]
		p=pm.Links[0]
		m=pm.Links[1]

		# lage planet-stern
		if prop=='distStarPlanet':
			pm.Placement.Base.x=obj.distStarPlanet

		# age moond stren
		if prop=='distPlanetMoon':
			m.Placement.Base.x=obj.distPlanetMoon
			
		if prop=='end':
			obj.end=obj.start+obj.duration
		
		say("begonnen")
		if prop=='objMoon':
			m.Links=[obj.objMoon]
		if prop=='objStar':
			s.Links=[obj.objStar]
		if prop=='objPlanet':
			p.Links=[obj.objPlanet]
		FreeCAD.animationLock=False
		FreeCAD.activeDocument().recompute()
		say("******************************Lock aus")
		say("fertig")
			
		
		
	def onBeforeChange(self,obj,prop):
		say("** on Before Changed " )
		FreeCAD.animationLock=False
#		say(obj)
		say(prop)
		FreeCAD.animation={}
		oldval=obj.getPropertyByName(prop)
		FreeCAD.animation['changed'] =[obj,prop,oldval]
		pass
		

	def execute(self,obj):
# 		obj.end=obj.start+obj.duration
		obj.setEditorMode("end", 1) #ro
		# obj.setEditorMode("obj", 1) #ro
		obj.setEditorMode("color", 2) #hidden
		say("execute _Gearing")
		if hasattr(self,'ignore'):
			if self.ignore:
				say("ignore")
				return
		
		
		# wenn noch keine zuordnung erfolgt ist
		App=FreeCAD
		
		

class _ViewProviderGearing(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/gearing.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Gearing',_CommandGearing())



#---------------------




def createKartan(name='My_Kartan'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=110
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=100
	obj.addProperty("App::PropertyLink","obj","Base","Sketch")
	obj.addProperty("App::PropertyLink","objAxis1","Base","Sketch")
	obj.addProperty("App::PropertyLink","objAxis2","Base","Sketch")
	obj.addProperty("App::PropertyLink","objCross","Base","Sketch")

	obj.addProperty("App::PropertyEnumeration","mode","Config","einheit").mode=['none','parallel','arc']
	obj.addProperty("App::PropertyLink","objAxis3","Base","Sketch")
	obj.addProperty("App::PropertyLink","objCross2","Base","Sketch")
	
	obj.addProperty("App::PropertyFloat","angleRotation","Config","ve").angleRotation=360
	obj.addProperty("App::PropertyFloat","angleZenit","Config","ve").angleZenit=30
	obj.addProperty("App::PropertyFloat","distance","Config","ve").distance=100
	
#	obj.addProperty("App::PropertyBool","_Z","Config","_Z")._Z=True
	#obj.addProperty("App::PropertyBool","_z","Config","_z")._z=True
#	obj.addProperty("App::PropertyBool","z","Config","z").z=True
	
	
	App=FreeCAD
	kart=App.activeDocument().addObject("Part::Compound","Kartan")
	k1=App.activeDocument().addObject("Part::Compound","Ka_x1")
	k2=App.activeDocument().addObject("Part::Compound","Ka_x2")
	c1=App.activeDocument().addObject("Part::Compound","Ka_c1")
	k3=App.activeDocument().addObject("Part::Compound","Ka_x3")
	c2=App.activeDocument().addObject("Part::Compound","Ka_c2")
	b=App.ActiveDocument.addObject("Part::Box","Box")
	b1=App.ActiveDocument.addObject("Part::Box","Box")
	b2=App.ActiveDocument.addObject("Part::Box","Box")
	b.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	b1.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	b2.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	# m.Placement.Base=FreeCAD.Vector(30,0,0.0)
	#pm.Placement.Base=FreeCAD.Vector(60,0,0.0)
	k1.Links=[b]
	k2.Links=[b1]
	c1.Links=[b2]
	obj.obj=kart
	obj.objAxis1=k1
	obj.objAxis2=k2
	obj.objCross=c1
	
	
	
	_Kartan(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj

class _CommandKartan(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/kardan.png', 'MenuText': 'Kartan', 'ToolTip': 'Kartan Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Kartan")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createKartan()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return



import numpy
from numpy import pi,cos,tan,arctan



def rotcross(part,alpha,phi):
	phi2=math.atan(math.cos(alpha*math.pi/180)*math.tan(phi*math.pi/180))*180/math.pi
	print (phi,phi2)

	rot = App.Rotation(App.Vector(0,0,1), phi)
	wy=rot.multVec(App.Vector(0,1,0))

	rot2 = App.Rotation(App.Vector(0,0,1), phi2)
	wx1=rot2.multVec(App.Vector(1,0,0))
	if phi <90 or phi>270:
		alpha=-alpha
	rotalpha=App.Rotation(App.Vector(0,1,0), alpha)
	wx=rotalpha.multVec(wx1)
	
	r=(wx.x**2+wx.y**2)**0.5
	beta=math.acos(r)*180/math.pi

	p1=App.Placement()
	phi2=phi
	p1.Rotation=App.Rotation(App.Vector(0,0,1),phi2)
	p2=App.Placement()
	if 90<phi and phi<270:
		beta=-beta
	p2.Rotation=App.Rotation(wy,beta)
	part.Placement=p2.multiply(p1)
	App.ActiveDocument.recompute()

	 
class _Kartan(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "Kartan"
		self.obj2 = obj
		say(" kardan init called")

	def step(self,now):
		say("Kardan step!" + str(now))
		FreeCAD.R=self
		
		if now<self.obj2.start or now>=self.obj2.end:
			say("ausserhalb")
			pass
		else:
			if not self.obj2.obj:
				errorDialog("kein Sketch zugeordnet")
				raise Exception(' self.obj2.obj nicht definiert')
			
			# alpha=60
			alpha=self.obj2.angleZenit
			phi=1
			
			# testfall
			phi=10

			# achse 1
			fa1=self.obj2.objAxis1
			p0=fa1.Placement
			phi0=p0.Rotation.Angle/pi*180
			# say("phi0 Basis " + str(phi0))
			p1=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),phi))
			r1=p1.multiply(p0)
			fa1.Placement=r1

			
			phi20=arctan(tan(phi0*pi/180)*cos(alpha*pi/180))*180/pi
			phi21=arctan(tan((phi0+phi)*pi/180)*cos(alpha*pi/180))*180/pi
			say("phi20 "+str(phi20))
			say("phi21 "+str(phi21))
			
			# achse 2
			timepos=now-self.obj2.start
			if 90/phi-1<=timepos and timepos<270/phi-1: 
				phi21=180+phi21
				say("*************** ! phi21 ="+str(phi21) + " now:" + str(now))

			fa2=self.obj2.objAxis2
			p1=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),phi21))
			p2=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),alpha))
			r3=p2.multiply(p1)
			fa2.Placement=r3

			# kreuz
			f=self.obj2.objCross
			rotcross(f,alpha,phi0+phi)
			FreeCAD.activeDocument().recompute()




	def onChanged(self,obj,prop):
		say("**	onChanged  " +str(obj.Label) + " " + prop)
		if prop=="Proxy":
				FreeCAD.animataionInit=True
				say("animation Init start!!!!!!!!!!!!!!!")
		if prop=="Label":
				FreeCAD.animataionInit=False
				say("Animation init beendet ---------------!!")
		if FreeCAD.animataionInit:
				say("erster Durchlauf - nix machen")
				return
		if hasattr(FreeCAD,"animationLock"):
			say(FreeCAD.animationLock)
			if FreeCAD.animationLock:
				say("Ende wegen Lock")
				return
		else:
			say("noch kein animation Lock")
			
		FreeCAD.animationLock=True
		say("------------------------------***Lock EIN")
		FreeCAD.mytoc=[self,obj,prop]
		if hasattr(FreeCAD,"animation"):
			oldval=FreeCAD.animation['changed'][2]
			val=obj.getPropertyByName(prop)
			say(prop + " old:" + str(oldval) + " new:" + str(val))

			if prop=='obj':
				obj.obj.Links=[obj.objAxis1,obj.objAxis2,obj.objCross]
			if prop=='duration' or prop=='start':
					obj.end=obj.start+obj.duration
			if prop=='angleZenit':
				obj.objAxis2.Placement.Rotation.Angle=obj.angleZenit/180*math.pi

		FreeCAD.animationLock=False
		FreeCAD.activeDocument().recompute()
		say("******************************Lock aus")

	def onBeforeChange(self,obj,prop):
		say("** on Before Changed " + str(obj.Label) + " " + prop)
		FreeCAD.animation={}
		oldval=obj.getPropertyByName(prop)
		FreeCAD.animation['changed'] =[obj,prop,oldval]

	def execute(self,obj):
		say("execute _Kardan")
		

class _ViewProviderKartan(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/kardan.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Kartan',_CommandKartan())



#-----------------------------





def createScaler(name='My_Scaler'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=10
	obj.addProperty("App::PropertyInteger","duration","Base","end").end=10
#	obj.addProperty("App::PropertyPlacement","initPlace","Object","initPlace")
#	obj.addProperty("App::PropertyVector","rotationCentre","Motion","Rotationszentrum")
#	obj.addProperty("App::PropertyVector","rotationAxis","Motion","Rotationsachse").rotationAxis=FreeCAD.Vector(0,0,1)
	obj.addProperty("App::PropertyFloat","xScale","Scale","Rotationsachse Zentrum relativ").xScale=0
	obj.addProperty("App::PropertyFloat","xVa","Scale","Rotationsachse Zentrum relativ").xVa=1
	obj.addProperty("App::PropertyFloat","xVe","Scale","Rotationsachse Zentrum relativ").xVe=2
	

	obj.addProperty("App::PropertyFloat","yScale","Scale","Rotationsachse Zentrum relativ").yScale=0
	obj.addProperty("App::PropertyFloat","yVa","Scale","Rotationsachse Zentrum relativ").yVa=1
	obj.addProperty("App::PropertyFloat","yVe","Scale","Rotationsachse Zentrum relativ").yVe=2

	obj.addProperty("App::PropertyFloat","zScale","Scale","Rotationsachse Zentrum relativ").zScale=1
	obj.addProperty("App::PropertyFloat","zVa","Scale","Rotationsachse Zentrum relativ").zVa=1
	obj.addProperty("App::PropertyFloat","zVe","Scale","Rotationsachse Zentrum relativ").zVe=2








	
#	obj.addProperty("App::PropertyFloat","angle","Motion","Dreh Winkel").angle=360
#	
	obj.addProperty("App::PropertyLink","obj2","Object","rotating object ")

	_Scaler(obj)
	_ViewProviderScaler(obj.ViewObject)
	return obj

class _CommandScaler(_CommandActor):
	def GetResources(self): 
		return {'Pixmap' : __dir__ + '/icons/scaler.png', 'MenuText': 'Scaler', 'ToolTip': 'Scaler Dialog'} 

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create Scaler")
			FreeCADGui.doCommand("import Animation")
			FreeCADGui.doCommand("Animation.createScaler()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
	   
class _Scaler(_Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Scaler"
		self.obj2=obj
		
	def execute(self,obj):
		sayd("execute _Scaler")
		if hasattr(obj,'obj2'):
			#say(obj.obj2)
			pass
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration

		
	
	def step(self,now):
		FreeCAD.yy=self

		if now<=self.obj2.start or now>self.obj2.end:
			pass
		else:
			relativ=1.00/(self.obj2.end-self.obj2.start)*(now-self.obj2.start)
			sc=self.obj2.obj2.Scale
			say(relativ)
			relativbase=self.obj2.xVe/self.obj2.xVa*relativ
			if relativ==0:
				nwx=self.obj2.xVa
				nwy=self.obj2.yVa
				nwz=self.obj2.zVa
			else:
			
				nwx=relativbase**self.obj2.xScale*self.obj2.xVe 
				nwy=relativbase**self.obj2.yScale*self.obj2.yVe 
				nwz=relativbase**self.obj2.zScale*self.obj2.zVe 
			
			newScale=(nwx,nwy,nwz)
			say(newScale)
			say(nwx*nwy*nwz)
			self.obj2.obj2.Scale=newScale
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.Selection.clearSelection()
		say("ende")



class _ViewProviderScaler(_ViewProviderActor):
	def getIcon(self):
		return __dir__ + '/icons/scaler.png'

if FreeCAD.GuiUp:
	FreeCADGui.addCommand('Anim_Scaler',_CommandScaler())

