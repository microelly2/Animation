# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import math,os
import numpy
from numpy import pi,cos,tan,arctan

import FreeCAD, FreeCADGui, Animation, PySide
from Animation import say,sayErr,sayexc
from  EditWidget import EditWidget

__vers__= '0.2'
__dir__ = os.path.dirname(__file__)	



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

	kart=FreeCAD.activeDocument().addObject("Part::Compound","Kartan")
	k1=FreeCAD.activeDocument().addObject("Part::Compound","Ka_x1")
	k2=FreeCAD.activeDocument().addObject("Part::Compound","Ka_x2")
	c1=FreeCAD.activeDocument().addObject("Part::Compound","Ka_c1")
	k3=FreeCAD.activeDocument().addObject("Part::Compound","Ka_x3")
	c2=FreeCAD.activeDocument().addObject("Part::Compound","Ka_c2")

	b=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	b1=FreeCAD.ActiveDocument.addObject("Part::Box","Box")
	b2=FreeCAD.ActiveDocument.addObject("Part::Box","Box")

	b.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	b1.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)
	b2.Placement.Base=FreeCAD.Vector(-5.0,-5.0,0.0)

	k1.Links=[b]
	k2.Links=[b1]
	c1.Links=[b2]
	obj.obj=kart
	obj.objAxis1=k1
	obj.objAxis2=k2
	obj.objCross=c1

	_Kartan(obj)
	_ViewProviderKartan(obj.ViewObject)
	return obj



def rotcross(part,alpha,phi):
	phi2=math.atan(math.cos(alpha*math.pi/180)*math.tan(phi*math.pi/180))*180/math.pi
	print (phi,phi2)

	rot = App.Rotation(App.Vector(0,0,1), phi)
	wy=rot.multVec(App.Vector(0,1,0))

	rot2 = App.Rotation(App.Vector(0,0,1), phi2)
	wx1=rot2.multVec(App.Vector(1,0,0))
	if phi <90 or phi>270:
		alpha=-alpha
	rotalpha=FreeCAD.Rotation(App.Vector(0,1,0), alpha)
	wx=rotalpha.multVec(wx1)

	r=(wx.x**2+wx.y**2)**0.5
	beta=math.acos(r)*180/math.pi

	p1=FreeCAD.Placement()
	phi2=phi
	p1.Rotation=FreeCAD.Rotation(App.Vector(0,0,1),phi2)
	p2=FreeCAD.Placement()
	if 90<phi and phi<270:
		beta=-beta
	p2.Rotation=FreeCAD.Rotation(wy,beta)
	part.Placement=p2.multiply(p1)
	App.ActiveDocument.recompute()


class _Kartan(Animation._Actor):

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
			p1=FreeCAD.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),phi))
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
			p1=FreeCAD.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),phi21))
			p2=FreeCAD.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),alpha))
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
		

class _ViewProviderKartan(Animation._ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/kardan.png'



