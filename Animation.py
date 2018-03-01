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

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

import FreeCAD, Part, PartGui, Draft, Drawing , PySide
from FreeCAD import Vector,Base
import math, os, sys
from math import sqrt, pi, sin, cos, asin
from PySide import QtGui,QtCore

from EditWidget import EditWidget

from time import *



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

import FreeCAD,os,time,sys,traceback

def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))


__dir__ = os.path.dirname(__file__)	

#---------------------------------------------------------------
# Actor
#---------------------------------------------------------------

class _Actor(object):

	def __init__(self,obj,icon='/icons/animation.png'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.Lock=False
		self.Changed=False
		# _ViewProviderActor(obj.ViewObject,icon) 


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
		self.obj2=obj
		if self.obj2.ViewObject.Visibility == False:
			return
			
		try:
			if self.Changed:
				# ignore self changes
				self.Changed=False
				return
		except:
			pass
		try: self.Lock
		except: self.Lock=False
		if not self.Lock:
			self.obj2=obj
			self.Lock=True
			try:
				self.update()
			except:
				sayexc('update error')
			self.Lock=False


	def attach(self,vobj):
		self.Object = vobj.Object


	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


	def onDocumentRestored(self, fp):
		say(["onDocumentRestored",str(fp.Label)+ ": "+str(fp.Proxy.__class__.__name__)])

class _ViewProviderActor():
 
	def __init__(self,vobj,icon='/icons/mover.png'):
		self.iconpath = __dir__ + icon
		self.Object = vobj.Object
		vobj.Proxy = self
		
 
	def getIcon(self):
		return self.iconpath

	def attach(self,vobj):
		self.cmenu=[]
		self.emenu=[]
		self.Object = vobj.Object
		icon='/icons/animation.png'
		self.iconpath = __dir__ + icon

	def anims(self):
		return [['forward',self.animforward],['backward',self.animbackward],['ping pong',self.animpingpong]]

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "Animation" + cl +" Node\nVersion " + self.vers)


	def setupContextMenu(self, obj, menu):
		cl=self.Object.Proxy.__class__.__name__
		action = menu.addAction("About " + cl)
		action.triggered.connect(self.showVersion)

		action = menu.addAction("Edit ...")
		action.triggered.connect(self.edit)

		for m in self.cmenu + self.anims():
			action = menu.addAction(m[0])
			action.triggered.connect(m[1])


	def edit(self):
		anims=self.anims()
		print anims
		
		self.dialog=EditWidget(self,self.emenu + anims,False)
		self.dialog.show()

	def setEdit(self,vobj,mode=0):
		self.edit()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False


	def doubleClicked(self,vobj):
		vobj.Visibility=True
		self.setEdit(vobj,1)

	def claimChildren(self):
		try:
			return self.Object.Group
		except:
			return None

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


	def dialog(self,noclose=False):
		say("huhu")
		say(EditWidget)
		return EditWidget(self,self.emenu + self.anims(),noclose)

	def animforward(self):
		FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)
		for i in range(101):
			self.obj2.time=float(i)/100
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.updateGui() 
			time.sleep(0.02)

	def animbackward(self):
		FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)
		for i in range(101):
			self.obj2.time=float(100-i)/100
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.updateGui() 
			time.sleep(0.02)

	def animpingpong(self):
		self.animforward()
		self.animbackward()


#---------------------------------------------------------------
# Bounder 
#---------------------------------------------------------------

def createBounder(name='MyBounder'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=40
	obj.addProperty("App::PropertyInteger","duration","Base","end")

	obj.addProperty("App::PropertyLink","obj","Object","Objekt")

	obj.addProperty("App::PropertyBool","x","intervall","start").x=False
	obj.addProperty("App::PropertyFloat","xmin","intervall","va")
	obj.addProperty("App::PropertyFloat","xmax","intervall","ve")

	obj.addProperty("App::PropertyBool","y","intervall","start").y=False
	obj.addProperty("App::PropertyFloat","ymin","intervall","va")
	obj.addProperty("App::PropertyFloat","ymax","intervall","ve")

	obj.addProperty("App::PropertyBool","z","intervall","start").z=False
	obj.addProperty("App::PropertyFloat","zmin","intervall","va")
	obj.addProperty("App::PropertyFloat","zmax","intervall","ve")

## mod
	_Bounder(obj,'/icons/bounder.png')
	_ViewProviderActor(obj.ViewObject,'/icons/bounder.png') 
	return obj


class _Bounder(_Actor):

	def step(self,now):
		say("Bounder step!" + str(now))
		if now<=self.obj2.start or now>self.obj2.end:
			pass
		else:
			gob=FreeCAD.ActiveDocument.getObject(self.obj2.obj.Name)
			pm=gob.Placement.Base
			x, y, z = pm.x, pm.y, pm.z

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
			FreeCADGui.updateGui() 

	def setValues(self,va,ve):
		self.obj2.va=va
		self.obj2.ve=ve

	def execute(self,obj):
		sayd("execute _Bounder")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration


#----------------------------------------------------------------------------------------------------------
# Viewpoint
#----------------------------------------------------------------------------------------------------------

def createViewpoint(name='My_Viewpoint'):

	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","duration","Base","start").duration=10
	obj.addProperty("App::PropertyInteger","end","Base","end")

	obj.addProperty("App::PropertyVector","posCamera","Camera","sweep").posCamera=FreeCAD.Vector(10,50,30)
	obj.addProperty("App::PropertyLink","pathCamera","Camera","sweep")
	obj.addProperty("App::PropertyInteger","indexCamera","Camera","sweep").indexCamera=1
	obj.addProperty("App::PropertyEnumeration","modeCamera","Camera","Rotationsachse Zentrum relativ").modeCamera=['Vector','Path']
	obj.addProperty("App::PropertyEnumeration","typeCamera","Camera","extrusion").typeCamera=["Orthographic","Perspective"]
	obj.typeCamera="Orthographic"
	obj.modeCamera='Vector'

	obj.addProperty("App::PropertyEnumeration","dirMode","Direction","Rotationsachse Zentrum relativ").dirMode=['None','Vector','Object']
	obj.addProperty("App::PropertyVector","dirVector","Direction","richutng ")
	obj.addProperty("App::PropertyLink","dirTarget","Direction","richutng ")

	obj.addProperty("App::PropertyEnumeration","posMode","Position","Rotationsachse Zentrum relativ").posMode=['None','Vector','Object']
	obj.addProperty("App::PropertyVector","posVector","Position","sweep").posVector=FreeCAD.Vector(0,0,0)
	obj.addProperty("App::PropertyLink","posObject","Position","sweep")

	obj.addProperty("App::PropertyFloat","zoom","lens geometry","extrusion").zoom=1

	_Viewpoint(obj)
	return obj


class _Viewpoint(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Viewpoint"
		_ViewProviderActor(obj.ViewObject,'/icons/viewpoint.png') 

	def step(self,now):
		from pivy import coin
		camera = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()
		if self.obj2.typeCamera=="Orthographic":
			FreeCADGui.activeDocument().activeView().setCameraType("Orthographic")
		else:
			FreeCADGui.activeDocument().activeView().setCameraType("Perspective")

		campos=Base.Vector( 100, 50, 30)
		campos=self.obj2.posCamera

		if self.obj2.modeCamera == 'Path' :
			pos=-self.obj2.indexCamera
			t=FreeCAD.animCamera[pos]
			campos=t.pop()

		say("camera pos" + str(campos))
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
			camera.pointAt(coin.SbVec3f(pos3),coin.SbVec3f(0,0,1))

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.updateGui() 

	def execute(self,obj):
		say("execute Viewpoint")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration
		if obj.modeCamera == 'Path':
			if 1  or obj.indexCamera >= 0:
				obj.indexCamera=-1
				x=obj.pathCamera
				steps=obj.duration+1+1
				l=x.Shape.copy().discretize(steps)
				ll=[]
				for pp in range(len(l)):
					v=l[pp]
					ll.append(v)
				ll.reverse()

				if not hasattr(FreeCAD,'animCamera'):
					FreeCAD.animCamera=[]
					say ("FreeCAD.animCamera neu")

				pos=len(FreeCAD.animCamera)
				obj.indexCamera=-pos
				FreeCAD.animCamera.append(ll)
				say("!!!!!!!!!!!!!!!!!  haenge an pos:"+ str(pos))
				say(FreeCAD.animCamera)

#----------------------------------------------------------------------------------------------------------
# Extruder
#----------------------------------------------------------------------------------------------------------

def createExtruder(name='My_Extruder'):

	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","duration","Base","start").duration=10

	obj.addProperty("App::PropertyLink","path","Extrusion","path ")
	obj.addProperty("App::PropertyLink","sweep","Extrusion","sweep")
	obj.addProperty("App::PropertyLink","ext","Extrusion","extrusion")
	
	_Extruder(obj)
	return obj


class _Extruder(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Extruder"
		_ViewProviderActor(obj.ViewObject,'/icons/extruder.png') 

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
		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.updateGui() 

#----------------------------------------------------------------------------------------------------------
#  Movie Screen
#----------------------------------------------------------------------------------------------------------

def createMoviescreen(name='My_Moviescreen'):

	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyIntegerList","pictureStart","info","Rotationsachse Zentrum relativ").pictureStart=[0,50,100]
	obj.addProperty("App::PropertyPath","pictures","screen","text").pictures="/home/microelly2/pics/t%04.f.png"
	obj.addProperty("App::PropertyLink","rectangle","screen","moving object ")

	obj.rectangle = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython","Rectangle Moviescreen")
	Draft._Rectangle(obj.rectangle)
	obj.rectangle.Length = 64
	obj.rectangle.Height = 48
	obj.rectangle.MakeFace = True
	Draft._ViewProviderRectangle(obj.rectangle.ViewObject)
	tx=FreeCADGui.activeDocument().activeView()
	rx=tx.getCameraOrientation()
	obj.rectangle.Placement.Rotation=rx
	_Moviescreen(obj)
	return obj


class _Moviescreen(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Moviescreen"
		_ViewProviderActor(obj.ViewObject,'/icons/moviescreen.png') 

	def step(self,now):
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

#----------------------------------------------------------------------------------------------------------

def createBillboard(name='My_Billboard'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyBool","showFrame","info","Rotationsachse Zentrum relativ").showFrame=False
	obj.addProperty("App::PropertyBool","showFile","info","Rotationsachse Zentrum relativ").showFile=False
	obj.addProperty("App::PropertyBool","showDate","info","Rotationsachse Zentrum relativ").showDate=False
	obj.addProperty("App::PropertyStringList","text","info","text").text=["Animation can display","configurable Text Information","in a HUD"]
	obj.addProperty("App::PropertyPath","textFiles","info","text").textFiles="/home/microelly2/texts/t%04.f.txt"
	obj.addProperty("App::PropertyLink","textObj","info","moving object ")
	obj.textObj=FreeCAD.ActiveDocument.addObject("App::Annotation","Text Billboard")
	obj.textObj.LabelText=obj.text
	obj.textObj.Position=FreeCAD.Vector(0,0,0)
	_Billboard(obj)
	_ViewProviderBillboard(obj.ViewObject)
	return obj

class _Billboard(_Actor):

	def __init__(self,obj):
		self.obj2=obj
		obj.Proxy = self
		self.Type = "_Billboard"
		_ViewProviderActor(obj.ViewObject,'/icons/billboard.png') 
		self.Object.Proxy.Lock=False


	def step(self,now):
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

#----------------------
# Mover
#----------------------

def createMover(name='My_Mover'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=10
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=10
	obj.addProperty("App::PropertyEnumeration","ModeMotion","Motion","Modus").ModeMotion=['Vector','DLine','DWire','Shape.Edge','Path']
	obj.addProperty("App::PropertyVector","vectorMotion","Motion","motionVector").vectorMotion=FreeCAD.Vector(100,0,0)
	obj.addProperty("App::PropertyLink","sourceMotion","Motion","source objectfor the motion vector")
	obj.addProperty("App::PropertyInteger","indexMotion","Motion","position on the source").indexMotion=1
	obj.addProperty("App::PropertyBool","reverseMotion","Motion","recvers the direction fo the vector").reverseMotion=False
	obj.addProperty("App::PropertyPlacement","initPlaceMotion","Object","initPlace")
	obj.addProperty("App::PropertyLink","obj2","Object","moving object ")
	_Mover(obj)
	_ViewProviderMover(obj.ViewObject)
	return obj



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
		self.Type = "_Plugger"
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

#---------------------------------------------------------------

def createTranquillizer(name='My_Tranquillizer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyFloat","time","params","time").time=0.02
	_Tranquillizer(obj)
	_ViewProviderTranquillizer(obj.ViewObject)
	return obj


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

 
class _Adjuster(_Actor):
	
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Adjuster"
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
		if now==self.obj2.start+1 or now==self.obj2.end:
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


#---------------------------------------------------------------

def createPhotographer(name='My_Photographer'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","end").end=40000
	obj.addProperty("App::PropertyBool","preview","Base","end").preview=False
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=40000
	obj.addProperty("App::PropertyInteger","size_x","Output","start").size_x=640
	obj.addProperty("App::PropertyInteger","size_y","Output","end").size_y=480
	obj.addProperty("App::PropertyIntegerList","frameSelection",'',"only these frames")
	obj.addProperty("App::PropertyPath","fn","Output","outdir").fn="/tmp/animation/t"
	obj.addProperty("App::PropertyEnumeration","format","Output","Bildformat").format=["png","jpg","bmp"]
	obj.addProperty("App::PropertyEnumeration","camDirection","Camera","Sichtrichtung").camDirection=["Front","Top","Axometric","Left","View"]
	obj.addProperty("App::PropertyInteger","camHeight","Camera","Ausschnitt Hoehe").camHeight=100
	_Photographer(obj)
	_ViewProviderPhotographer(obj.ViewObject)
	return obj




class _Photographer(_Actor):

	def __init__(self,obj):
		self.obj2 = obj 
		obj.Proxy = self
		self.Type = "_Photographer"

	def execute(self,obj):
		sayd("execute _Photographer")
		obj.setEditorMode("end", 1) #ro
		obj.end=obj.start+obj.duration
		if obj.preview:
			if hasattr(self,"now"):
				self.step(self.now,True)

	def step(self,now,force=False):
		if hasattr(self.obj2,"frameSelection"):
			fsel=self.obj2.frameSelection
			if fsel<>[]: 
				if now not in fsel: 
					print "skip frame",now
					return

		if now<=self.obj2.start or now>self.obj2.end:
			pass
		else:
			st=FreeCADGui.Selection.getSelection()
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
			
			if not force:
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
			
			
			#fn='/home/thomas/Bilder/bp_111.png'
			self.now=now
			if self.obj2.preview:
				try:
					self.imager.run(fn)
					
				except:
					self.fn=fn
					self.imager=showimage(fn)
			for t in st:
				FreeCADGui.Selection.addSelection(t)

			#my_render(fn2)
	def  toInitialPlacement(self):
		pass


class _ViewProviderPhotographer(_ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/photographer.png'



#---------------------------------------------------------------

def createManager(name='My_Manager'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","intervall","Base","intervall").intervall=100
	obj.addProperty("App::PropertyFloat","step","Base","step").step=0.0
	obj.addProperty("App::PropertyFloat","sleeptime","params","sleep time between steps").sleeptime=0.02
	obj.addProperty("App::PropertyString","text","params","text").text="NO"
	_Manager(obj)
	_ViewProviderManager(obj.ViewObject)
	return obj



import os.path


class _Manager(_Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Manager"
		self.obj2=obj
		try: obj.step
		except: obj.addProperty("App::PropertyInteger","step","Base","step").step=0


	def execute(self,obj):
		sayd("execute _Manager")

	def register(self,obj):
		self.obj2.targets.append(obj)

	def step(self,nw):

		if self.obj2.start<=nw and   nw<=self.obj2.start + self.obj2.intervall:
			say("step  " + self.obj2.Label + "  " + str(nw))
			t=FreeCAD.ActiveDocument.getObject(self.obj2.Name)
			intervall=self.obj2.intervall
			if self.obj2.Label == self.obj2.Name:
				s= s=self.obj2.Label
			else:
				s=self.obj2.Label + ' ('+ self.obj2.Name +")"
			say(s +" ************************* manager run loop:" + str(nw-self.obj2.start) + "/" + str(intervall))
			
			self.obj2.step=nw
			#if os.path.exists("/tmp/stop"):
			if FreeCAD.ParamGet('User parameter:Plugins/animation').GetBool("stop"):
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
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.updateGui()
			time.sleep(self.obj2.sleeptime)



	def run(self,intervall=-1):
		sayd("run  intervall=" + str(intervall))
		FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)
		
		if (intervall<0):
			intervall=self.obj2.intervall

		if hasattr(self,'obj2'):
			t=FreeCAD.ActiveDocument.getObject(self.obj2.Name)
		else:
			raise Exception("obj2 not found --> reinit the file!")

		for ob in t.OutList:
			say(ob.Label)
			ob.Proxy.initialize()
			ob.Proxy.execute(ob)

		firstRun=True
		bigloop=0

		#while firstRun or os.path.exists("/tmp/loop"):
		while firstRun or FreeCAD.ParamGet('User parameter:Plugins/animation').GetBool("loop"):
			say("manager infinite loop #################################")
			firstRun=False
			bigloop += 1 

			for nw in range(self.obj2.start):
				say("---- manager before" + str(nw))

			for nw in range(intervall+1):
				self.step(nw)
				FreeCAD.ActiveDocument.recompute()
				FreeCADGui.updateGui()
				time.sleep(self.obj2.sleeptime)

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
	def __init__(self,vobj,fun,fun2,fun4,fun5, *args):
		QtGui.QWidget.__init__(self, *args)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.vobj=vobj
		self.fun=fun
		self.fun2=fun2
		self.fun4=fun4
		self.fun5=fun5
		self.vollabel = QtGui.QLabel(self.vobj.Object.Label)
		self.volvalue = QtGui.QLineEdit()
		self.checkBox = QtGui.QCheckBox()
		self.radioButton = QtGui.QRadioButton()
		self.pushButton = QtGui.QPushButton()
		self.pushButton.clicked.connect(self.on_pushButton_clicked)
		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 1)
		#layout.addWidget(self.volvalue, 0, 1)
		#layout.addWidget(self.checkBox, 1, 2)
		#layout.addWidget(self.radioButton, 1, 0)

		layout.addWidget(self.pushButton, 1,1)
		if fun2:
			self.pushButton2 = QtGui.QPushButton()
			self.pushButton2.clicked.connect(self.on_pushButton_clicked2)
			layout.addWidget(self.pushButton2, 2,1)
		if False:
			self.pushButton3 = QtGui.QPushButton()
			self.pushButton3.clicked.connect(self.on_pushButton_clicked3)
			layout.addWidget(self.pushButton3, 3,1)

		if True:
			self.pushButton4 = QtGui.QPushButton()
			self.pushButton4.clicked.connect(self.on_pushButton_clicked4)
			layout.addWidget(self.pushButton4, 4,1)

			self.pushButton5 = QtGui.QPushButton()
			self.pushButton5.clicked.connect(self.on_pushButton_clicked5)
			layout.addWidget(self.pushButton5, 5,1)

			self.pushButton6 = QtGui.QPushButton()
			self.pushButton6.clicked.connect(self.on_pushButton_clicked6)
			layout.addWidget(self.pushButton6, 6,1)

		dial = QtGui.QDial()
		dial.setNotchesVisible(True)
		self.dial=dial
		dial.setMaximum(100)
		dial.valueChanged.connect(self.dialer);
		layout.addWidget(dial,7,1)



		if 0:
			# close control dialog
			self.pushButton3 = QtGui.QPushButton()
			self.pushButton3.clicked.connect(self.on_pushButton_clicked)
			layout.addWidget(self.pushButton3, 3,1)
		
		self.setLayout(layout)
		self.setWindowTitle("Animation Manager Control Panel")

	def dialer(self):
		time=float(self.dial.value())/100
		nw=self.dial.value()
		t=self.vobj.Object
		
		t.step=self.dial.value()
		
		for ob in t.OutList:
			say("step " +  str(nw) + "fuer " + ob.Label)
			if ob.ViewObject.Visibility:
				ob.Proxy.step(nw)
		FreeCAD.ActiveDocument.recompute()

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
		#self.fun3(self.vobj)
		FreeCADGui.Control.closeDialog()

	def on_pushButton_clicked4(self):
		#FreeCAD.Console.PrintMessage("rt")
		#FreeCAD.zx=self
		#say(self)
		self.fun4(self.vobj)
		#FreeCADGui.Control.closeDialog()

	def on_pushButton_clicked5(self):
		#FreeCAD.Console.PrintMessage("rt")
		#FreeCAD.zx=self
		#say(self)
		self.fun5(self.vobj)
		#FreeCADGui.Control.closeDialog()

	def on_pushButton_clicked6(self):
		#self.fun6(self.vobj)
		self.dialer()




class AddMyTask():
	def __init__(self,vobj,fun,fun2,fun4,fun5):
		reinit()
		self.form = AddMyWidget(vobj,fun,fun2,fun4,fun5)
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
#	fname='/tmp/stop'
#	fhandle = open(fname, 'a')
#	fhandle.close()
	ta=FreeCAD.ParamGet('User parameter:Plugins/animation')
	ta.SetBool("stop",True)

def unlockManager(vobj=None):
#	import os
#	from os import remove
#	fname='/tmp/stop'
#	try:
#		os.remove(fname)
#	except:
#		pass
	ta=FreeCAD.ParamGet('User parameter:Plugins/animation')
	ta.SetBool("stop",False)


def loopManager(vobj=None):
#	fname='/tmp/loop'
#	fhandle = open(fname, 'a')
#	fhandle.close()
	ta=FreeCAD.ParamGet('User parameter:Plugins/animation')
	ta.SetBool("loop",True)



def unloopManager(vobj=None):
#	import os
#	from os import remove
#	fname='/tmp/loop'
#	try:
#		os.remove(fname)
#	except:
#		pass
	ta=FreeCAD.ParamGet('User parameter:Plugins/animation')
	ta.SetBool("loop",False)



class _ViewProviderManager(_ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/manager.png'
		
	def doubleClicked(self,vobj):
		FreeCAD.tt=self
		#say(self)
		#panel = AddMyTask(runManager,stopManager,unlockManager)
		panel = AddMyTask(self,runManager,stopManager,loopManager,unloopManager)
#		panel.form.volvalue.setText("VOL-VALUE")
#		panel.form.vollabel.setText("VOL-LABELLO")
		panel.form.pushButton.setText("Run ")
		panel.form.pushButton2.setText("Stop")
		panel.form.pushButton4.setText("Loop")
		panel.form.pushButton5.setText("Unloop")
		panel.form.pushButton6.setText("Refresh")

		# FreeCADGui.Control.showDialog(panel)
		
		self.dialog=panel.form
		self.dialog.show()


#---------------------------------------------------------------


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
					say("reinit __init__")
#					obj.Proxy.__init__(obj)
#					say(obj.Proxy.Type)
					obj.Proxy.obj2=obj

				# print("init " +obj.Name)
				if obj.Proxy.Type=='_Plugger':
					if not hasattr(obj,'status'):
						obj.addProperty("App::PropertyInteger","status","nummer","intern").status=0
					if not hasattr(obj,'offsetVector'):
						obj.addProperty("App::PropertyVector","offsetVector","3D Param","offsetVector").offsetVector=FreeCAD.Vector(0,0,0)
				if obj.Proxy.Type=='_Adjustor':
					if not hasattr(obj,'unit'):
						obj.addProperty("App::PropertyEnumeration","unit","3D Param","einheit").unit=['deg','mm']
				if obj.Proxy.Type=='_Photographer':
					if not hasattr(obj,'camDirection'):
						obj.addProperty("App::PropertyEnumeration","camDirection","Camera","Sichtrichtung").camDirection=["Front","Top","Axometric","Left"]
					if not hasattr(obj,'camHeight'):
						obj.addProperty("App::PropertyInteger","camHeight","Camera","Ausschnitt Hoehe").camHeight=100
				if obj.Proxy.Type=='_Rotator':
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
		panel.form.pushButton3.setText("Unlock")
		
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








import PySide
from PySide import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


import PySide
from PySide import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibWidget(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):

		super(MatplotlibWidget, self).__init__(Figure())


		self.setParent(parent)
		self.figure = Figure(figsize=(width, height), dpi=dpi) 
		self.canvas = FigureCanvas(self.figure)

		FigureCanvas.updateGeometry(self)
		self.axes = self.figure.add_subplot(111)

	def run(self,fn):
		mpl=self
		plt=mpl.figure
		plt.clf()

		img2=mpimg.imread(fn)

		plt.figimage(img2)
		l,b,c=img2.shape
		say((fn,l,b,c))
		mpl.draw()
		mpl.resize(b,l)


def showimage(fn):
	mpl=MatplotlibWidget()
	mpl.resize(100,100)
	mpl.show()

	plt=mpl.figure
	plt.clf()


	img2=mpimg.imread(fn)

	plt.figimage(img2)
	l,b,c=img2.shape
	mpl.draw()
	mpl.resize(b,l)
	return mpl


#fn='/home/thomas/Bilder/bp_111.png'
#rc=showimage(fn)
