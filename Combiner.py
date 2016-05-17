# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *
import math,os, time

from EditWidget import EditWidget

__vers__= '0.2'
__dir__ = os.path.dirname(__file__)	


def createCombiner(name='My_Combiner',target=None,src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","source","Base","")
	obj.addProperty("App::PropertyLink","source2","Base","")
	obj.addProperty("App::PropertyLink","source3","Base","")
	obj.addProperty("App::PropertyLink","source4","Base","")
	obj.addProperty("App::PropertyLink","target","Base","")
	obj.addProperty("App::PropertyLink","target2","Base","")
	obj.addProperty("App::PropertyLink","target3","Base","")
	obj.addProperty("App::PropertyLink","target4","Base","")
	obj.target=target
	obj.addProperty("App::PropertyLinkList","targets","Base","")
	obj.addProperty("App::PropertyLinkList","followers","Base","")
	
	obj.addProperty("App::PropertyFloat","out","Results","")
	obj.addProperty("App::PropertyFloat","out2","Results","")
	obj.addProperty("App::PropertyFloat","out3","Results","")
	obj.addProperty("App::PropertyFloat","out4","Results","")
	
	obj.addProperty("App::PropertyFloat","time","Base","")
	obj.time=0

	obj.addProperty("App::PropertyString","trafo","Functions","")
	obj.addProperty("App::PropertyString","trafo2","Functions","")
	obj.addProperty("App::PropertyString","trafo3","Functions","")
	obj.addProperty("App::PropertyString","trafo4","Functions","")
	obj.trafo="time"
	obj.trafo2="2*time"
	obj.trafo3="30*time"
	obj.trafo4="400*time"
	
	obj.addProperty("App::PropertyFloat","a","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","b","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","c","FunctionParameter","")
	obj.addProperty("App::PropertyFloat","d","FunctionParameter","")

	obj.a=200
	obj.b=0.5
	obj.c=50

	_Combiner(obj)
	_ViewProviderCombiner(obj.ViewObject)
	obj.Proxy.updater=True
	return obj

class _Combiner(Animation._Actor):

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

		out=eval(self.obj2.trafo)
		out2=eval(self.obj2.trafo2)
		out3=eval(self.obj2.trafo3)
		out4=eval(self.obj2.trafo4)
		say([time,out,out2,out3,out4])

		self.obj2.out=out
		self.obj2.out2=out2
		self.obj2.out3=out3
		self.obj2.out4=out4

		tl=[self.obj2.target,self.obj2.target2,self.obj2.target3,self.obj2.target4]
		outl=[out,out2,out3,out4]
		for t in range(4):
			try:
				tl[t].Proxy.step(outl[t])
				tl[t].Proxy.update()
				say("combiner update " + str(tl[t].Label) +  " wert: " + str(outl[t])) 
			except:
				pass

	def step(self,now):
			self.obj2.time=float(now)/100


class _ViewProviderCombiner(Animation._ViewProviderActor):


	def attach(self,vobj):
		vobj.Proxy = self
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		icon='/icons/combiner.png'
		self.iconpath = __dir__ + icon
		self.vers=__vers__
		return

	def doubleClicked(self,vobj):
		return

	def setupContextMenu(self, obj, menu):
		return


if __name__ == '__main__':

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


	c=createCombiner("cmb")
	c.source=App.ActiveDocument.Cone

	c.trafo="source.Radius1.Value"
	c.target=s1

	c.trafo2="source.Radius2.Value"
	c.target2=s2

	c.trafo3="max(source.Radius1.Value,source.Radius2.Value)"
	c.target3=s3



