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



def createGearing(name='My_Gearing'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyInteger","start","Base","start").start=10
	obj.addProperty("App::PropertyInteger","end","Base","end").end=110
	obj.addProperty("App::PropertyInteger","duration","Base","end").duration=100
	obj.addProperty("App::PropertyLink","obj","Base","Sketch")
	obj.addProperty("App::PropertyLink","objStar","Base","Sketch")
	obj.addProperty("App::PropertyLink","objPlanet","Base","Sketch")
	obj.addProperty("App::PropertyLink","objMoon","Base","Sketch")

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
	_ViewProviderGearing(obj.ViewObject)
	return obj



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


class _Gearing(Animation._Actor):

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
			print(s.Placement.Rotation.Angle)
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
		
		

class _ViewProviderGearing(Animation._ViewProviderActor):
	
	def getIcon(self):
		return __dir__ + '/icons/gearing.png'




#---------------------



if __name__ == '__main__' :
	pass
