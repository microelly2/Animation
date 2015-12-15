# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import math,os, time

import FreeCAD, FreeCADGui, Animation, PySide, Part
from Animation import say,sayErr,sayexc
from EditWidget import EditWidget

Gui=FreeCADGui
App=FreeCAD

__vers__= '0.2'
__dir__ = os.path.dirname(__file__)	
__dir__="/home/thomas/.FreeCAD/Mod/Animation/"

def _creategraphs(obj):

	obj.Proxy.data={}
	obj.Proxy.data2={}
	obj.Proxy.data3={}
	obj.Proxy.data4={}
	obj.Proxy.data5={}
	obj.Proxy.data6={}
	obj.Proxy.data7={}
	obj.Proxy.data8={}
	obj.Proxy.data9={}
	
	
	if obj.trafo:
		w=Part.makeSphere(0.1)
		Part.show(w)
		obj.graph=FreeCAD.activeDocument().ActiveObject
		obj.graph.ViewObject.LineColor=(1.0,0.0,.0)
		obj.graph.Label="Graph 1 "
	if obj.trafo2:
		w=Part.makeSphere(0.1)
		Part.show(w)
		obj.graph2=FreeCAD.activeDocument().ActiveObject
		obj.graph2.ViewObject.LineColor=(.0,1.0,.0)
		obj.graph2.Label="Graph 2 "
	if obj.trafo3:
		w=Part.makeSphere(0.1)
		Part.show(w)
		obj.graph3=FreeCAD.activeDocument().ActiveObject
		obj.graph3.ViewObject.LineColor=(.0,.0,1.0)
		obj.graph3.Label="Graph 3 "
	if obj.trafo4:
		w=Part.makeSphere(0.1)
		Part.show(w)
		obj.graph4=FreeCAD.activeDocument().ActiveObject
		obj.graph4.ViewObject.LineColor=(1.0,1.0,.0)
		obj.graph4.Label="Graph 4 "

	if obj.trafo5:
		w=Part.makeSphere(0.1)
		Part.show(w)
		obj.graph5=FreeCAD.activeDocument().ActiveObject
		obj.graph5.ViewObject.LineColor=(1.0,.0,1.0)
		obj.graph5.Label="Graph 5 "

	if obj.trafo6:
		w=Part.makeSphere(0.1)
		Part.show(w)
		obj.graph6=FreeCAD.activeDocument().ActiveObject
		obj.graph6.ViewObject.LineColor=(.0,1.0,1.0)
		obj.graph6.Label="Graph 6 "



def createDiagram(name='My_Diagram',trafo=None,trafo2=None,trafo3=None,trafo4=None,trafo5=None,trafo6=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","source","Base","")
	obj.addProperty("App::PropertyLink","source2","Base","")
	obj.addProperty("App::PropertyLink","source3","Base","")
	obj.addProperty("App::PropertyLink","source4","Base","")
	
	obj.addProperty("App::PropertyPlacement","graphPlacement","Base","")
	obj.addProperty("App::PropertyLink","graph","Base","")
	obj.addProperty("App::PropertyLink","graph2","Base","")
	obj.addProperty("App::PropertyLink","graph3","Base","")
	obj.addProperty("App::PropertyLink","graph4","Base","")
	obj.addProperty("App::PropertyLink","graph5","Base","")
	obj.addProperty("App::PropertyLink","graph6","Base","")

	
	obj.addProperty("App::PropertyFloat","out","Results","")
	obj.addProperty("App::PropertyFloat","out2","Results","")
	obj.addProperty("App::PropertyFloat","out3","Results","")
	obj.addProperty("App::PropertyFloat","out4","Results","")
	obj.addProperty("App::PropertyFloat","out5","Results","")
	obj.addProperty("App::PropertyFloat","out6","Results","")
	obj.addProperty("App::PropertyFloat","out7","Results","")
	obj.addProperty("App::PropertyFloat","out8","Results","")
	obj.addProperty("App::PropertyFloat","out9","Results","")
	
	obj.addProperty("App::PropertyFloat","time","Base","")
	obj.time=0
	obj.addProperty("App::PropertyString","timeExpression","Functions","")
	obj.addProperty("App::PropertyString","trafo","Functions","")
	obj.addProperty("App::PropertyString","trafo2","Functions","")
	obj.addProperty("App::PropertyString","trafo3","Functions","")
	obj.addProperty("App::PropertyString","trafo4","Functions","")
	obj.addProperty("App::PropertyString","trafo5","Functions","")
	obj.addProperty("App::PropertyString","trafo6","Functions","")
	obj.addProperty("App::PropertyString","trafo7","Functions","")
	obj.addProperty("App::PropertyString","trafo8","Functions","")
	obj.addProperty("App::PropertyString","trafo9","Functions","")
	obj.trafo=trafo
	obj.trafo2=trafo2
	obj.trafo3=trafo3
	obj.trafo4=trafo4
	obj.trafo5=trafo5
	obj.trafo6=trafo6
	
	obj.addProperty("App::PropertyFloat","a","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","b","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","c","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","d","FunctionParameter","")

	obj.a=200
	obj.b=0.5
	obj.c=50

	_Diagram(obj)
	_ViewProviderDiagram(obj.ViewObject)
	obj.Proxy.updater=True
	_creategraphs(obj)
	return obj

class _Diagram(Animation._Actor):

	def update(self):

		time=self.obj2.time
		try:
			say("update time=" + str(time) + ", "+ self.obj2.Label)
		except:
			say("update (ohne Label)")

		time=self.obj2.time
		
		a=self.obj2.a
		b=self.obj2.b
		c=self.obj2.c
		d=self.obj2.d
		source=self.obj2.source
		source2=self.obj2.source2
		source3=self.obj2.source3
		source4=self.obj2.source4
		if self.obj2.timeExpression<>"":
			say(["eval time Expression",time])
			time=eval(self.obj2.timeExpression)
			say(["time== ",time,self.obj2.timeExpression])
		
		out=0
		out1=0
		out2=0
		out3=0
		out4=0
		out5=0
		out6=0
		out7=0
		out8=0
		out9=0
		
		if self.obj2.trafo: out=eval(self.obj2.trafo)
		if self.obj2.trafo2: out2=eval(self.obj2.trafo2)
		if self.obj2.trafo3: out3=eval(self.obj2.trafo3)
		if self.obj2.trafo4: out4=eval(self.obj2.trafo4)
		if self.obj2.trafo5: out5=eval(self.obj2.trafo5)
		if self.obj2.trafo6: out6=eval(self.obj2.trafo6)
		if self.obj2.trafo7: out7=eval(self.obj2.trafo7)
		if self.obj2.trafo8: out8=eval(self.obj2.trafo8)
		if self.obj2.trafo9: out9=eval(self.obj2.trafo9) 
		
		say([time,out,out2,out3,out4])

		self.obj2.out=out
		self.obj2.out2=out2
		self.obj2.out3=out3
		self.obj2.out4=out4
		self.obj2.out5=out5
		self.obj2.out6=out6
		self.obj2.out7=out7
		self.obj2.out8=out8
		self.obj2.out9=out9

		if self.obj2.trafo:
			self.register(time,self.data,out,self.obj2.graph)

		if self.obj2.trafo2:
			self.register(time,self.data2,out2,self.obj2.graph2)

		if self.obj2.trafo3:
			self.register(time,self.data3,out3,self.obj2.graph3)

		if self.obj2.trafo4:
			self.register(time,self.data4,out4,self.obj2.graph4)

		if self.obj2.trafo5:
			self.register(time,self.data5,out5,self.obj2.graph5)

		if self.obj2.trafo6:
			self.register(time,self.data6,out6,self.obj2.graph6)



	def register(self,time,data,out,graph):

		data[time]=out
		ts=data.keys()
		ts.sort()
		pl=[]
		say("points")
		for t in ts:
			pl.append((t,data[t],1))
#		say(pl)
		if len(pl)>1:
			w=Part.makePolygon(pl)
		else:
			w=Part.makeSphere(0.1)
		try:
			graph.Shape=w
			graph.Placement=self.obj2.graphPlacement
		except:
			pass



	def step(self,now):
#			say("step "+str(now) + str(self))
			self.obj2.time=float(now)/100


class _ViewProviderDiagram(Animation._ViewProviderActor):


	def attach(self,vobj):
		say("VO attach " + str(vobj.Object.Label))
		vobj.Proxy = self
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		_creategraphs(self.Object)
		icon='/icons/animation.png'
		self.iconpath = __dir__ + icon
		self.vers=__vers__
		return

	def doubleClicked(self,vobj):
		return

	def setupContextMenu(self, obj, menu):
		return


if __name__ == '__main__':

	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")
	import Animation
	Animation.createManager()

	App.ActiveDocument.addObject("Part::Box","Box")
	App.ActiveDocument.addObject("Part::Box","Box")
	App.ActiveDocument.addObject("Part::Box","Box")
	App.ActiveDocument.addObject("Part::Box","Box")
	App.ActiveDocument.addObject("Part::Cone","Cone")


	import Placer

	s1=Placer.createPlacer("B1")
	s1.target=App.ActiveDocument.Box001

	s2=Placer.createPlacer("B2")
	s2.target=App.ActiveDocument.Box002
	s2.y="10"

	s3=Placer.createPlacer("B3")
	s3.target=App.ActiveDocument.Box003
	s3.y="20"


	import Diagram
	c=Diagram.createDiagram("dia","0.200*time","0.2*(0.01*time-0.5)**2","10+time+1","-10*time")
	c.source=s1
	c.trafo="source.Placement.Rotation.Angle"
	c.timeExpression="source.time*100"
	c.graphPlacement.Base.z=10
	

	m=App.ActiveDocument.My_Manager
	m.addObject(c)
	



