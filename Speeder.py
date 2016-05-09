# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import math,os, time

import FreeCAD, FreeCADGui, Animation, PySide
from Animation import say,sayErr,sayexc
from EditWidget import EditWidget

Gui=FreeCADGui
App=FreeCAD

__vers__= '0.2'
__dir__ = os.path.dirname(__file__)	


def createSpeeder(name='My_Speeder',target=None,src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyLink","target","Base","")
	obj.target=target
	obj.addProperty("App::PropertyLinkList","targets","Base","")
	obj.addProperty("App::PropertyLinkList","followers","Base","")
	
	obj.addProperty("App::PropertyFloat","time","Base","")
	obj.time=0
	obj.addProperty("App::PropertyEnumeration","mode","Functions","").mode=['forward','backward','quadratic','sine wave','fade','ping pong','expression']
	obj.mode='expression'

	obj.addProperty("App::PropertyString","trafo","Functions","")
	obj.addProperty("App::PropertyFloat","a","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","b","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","c","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","d","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","m","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","g","FunctionParameter","")

	obj.a=200
	obj.b=0.5
	obj.c=50
	obj.m=5
	obj.g=1
	
	obj.addProperty("App::PropertyString","expressiontrafo","Functions","")
	# ping pong
	obj.expressiontrafo="100*2*time if time <0.5 else  100 - 100*2*(time-0.5)"
	# quadradic
	obj.expressiontrafo="a*(time-b)**2  + c"
	
	# hide info
	obj.setEditorMode("expressiontrafo", 2)
	_Speeder(obj)
	_ViewProviderSpeeder(obj.ViewObject)
	obj.Proxy.updater=True
	return obj

class _Speeder(Animation._Actor):

	def update(self):
		time=self.obj2.time
		try:
			say("update time=" + str(time) + ", "+ self.obj2.Label)
		except:
			say("update (ohne Label)")
		time==self.obj2.time
		
		a=self.obj2.a
		b=self.obj2.b
		c=self.obj2.c
		d=self.obj2.d
		newtime=eval(self.obj2.trafo)
		self.obj2.target.Proxy.step(newtime)
		self.obj2.target.Proxy.update()

	def t2nt(self,time):
		a=self.obj2.a
		b=self.obj2.b
		c=self.obj2.c
		d=self.obj2.d
		m=self.obj2.m
		g=self.obj2.g

		newtime=eval(self.obj2.trafo)
		say(str(time) +" " +self.obj2.trafo +" " + str(newtime))
		return newtime

	def t2ntderive(self,time):
		a=self.obj2.a
		b=self.obj2.b
		c=self.obj2.c
		d=self.obj2.d
		m=self.obj2.m
		g=self.obj2.g

		newtime1=eval(self.obj2.trafo)
		time += 0.01
		newtime2=eval(self.obj2.trafo)
		newtime=(newtime2-newtime1)*m
		
		say(str(time) +" " +self.obj2.trafo +" derive " + str(newtime))
		say(str(newtime1))
		say(str(newtime2))
		return newtime

	def t2ntforce(self,time):
		a=self.obj2.a
		b=self.obj2.b
		c=self.obj2.c
		d=self.obj2.d
		m=self.obj2.m
		g=self.obj2.g
		newtime1=eval(self.obj2.trafo)
		time += 0.01
		newtime2=eval(self.obj2.trafo)
		time -= 2*0.01
		newtime0=eval(self.obj2.trafo)
		
		newtime=(newtime2-2*newtime1+newtime0)/0.01*g
		
		say(str(time) +" " +self.obj2.trafo +" force " + str(newtime))
		return newtime



	def step(self,now):
#			say("step "+str(now) + str(self))
			self.obj2.time=float(now)/100

	def onChanged(self,obj,prop):
		if prop=='mode':
			say("onChanged  mode" + str(self))
			say(obj.mode)
			# hier formel tauschen
			if obj.mode== 'ping pong':
				obj.trafo="a*time/b if time <b else  2*a - a*time/b"
			elif obj.mode == 'forward':
				obj.trafo="a*time"
			elif obj.mode == 'backward':
				obj.trafo="a-a*time"
			elif obj.mode == "fade":
				obj.trafo="0 if time<b else a*(time-b)/(c-b) if time <c else a"
			elif obj.mode == 'sine wave':
				obj.trafo="a*math.sin(math.pi*b*time+c)"
			elif obj.mode == 'quadratic':
				obj.trafo="a*time**2+ b*time + c"
			elif obj.mode == 'expression':
				obj.trafo=obj.expressiontrafo
			else:
				FreeCAD.Console.PrintWarning("unknown mode for speeder " + str(obj.Label) +" :" + obj.mode)
				pass



class _ViewProviderSpeeder(Animation._ViewProviderActor):


	def attach(self,vobj):
		# items for edit dialog  and contextmenue
		self.emenu=[['A',self.funA],['Diagram',self.diagram],]
		self.cmenu=self.emenu
		
		say("VO attach " + str(vobj.Object.Label))
		vobj.Proxy = self
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		icon='/icons/animation.png'
		self.iconpath = __dir__ + icon
		self.vers=__vers__
		return

	def dialer(self):
		self.obj2.time=float(self.widget.dial.value())/100
		FreeCAD.ActiveDocument.recompute()
		self.obj2.target.touch()
		FreeCAD.ActiveDocument.recompute()

#	def dialog(self,noclose=False):
#		return EditWidget(self,self.emenu,noclose)

	def funA(self):
		say("ich bin FunA touch target")
		FreeCAD.ActiveDocument.recompute()
		self.obj2.target.touch()
		FreeCAD.ActiveDocument.recompute()
		say("ich war  FunA")

	def diagram(self):
		''' diagram of relative location, speed/impulse, acceleration/force'''
		points=[]
		for time in range(101):
			nt=self.Object.Proxy.t2nt(0.0+0.01*time)
			points.append(FreeCAD.Vector(time,nt,0))
		import Draft
		w=Draft.makeWire(points)
		w.Label=self.Object.trafo
		w.ViewObject.LineColor=(.0,.0,1.0)
		points=[]
		for time in range(101):
			nt=self.Object.Proxy.t2ntderive(0.0+0.01*time)
			points.append(FreeCAD.Vector(time,nt,0))
		import Draft
		w=Draft.makeWire(points)
		w.Label="derive/impulse of " + self.Object.trafo
		w.ViewObject.LineColor=(.0,1.0,.0)
		points=[]
		for time in range(101):
			nt=self.Object.Proxy.t2ntforce(0.0+0.01*time)
			points.append(FreeCAD.Vector(time,nt,0))
		import Draft
		w=Draft.makeWire(points)
		w.Label="2nd derive/force of " + self.Object.trafo
		w.ViewObject.LineColor=(1.0,.0,.0)




		pass

