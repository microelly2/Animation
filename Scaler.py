import math,os
import FreeCAD, FreeCADGui, Animation, PySide
from Animation import say,sayErr,sayexc,sayd
from  EditWidget import EditWidget

__vers__= '0.1'
__dir__ = os.path.dirname(__file__)	


def createScaler(name='My_Scaler'):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyInteger","start","Base","start").start=0
	obj.addProperty("App::PropertyInteger","end","Base","")
	obj.addProperty("App::PropertyInteger","duration","Base","")

	obj.addProperty("App::PropertyFloat","xScale","Scale","Rotationsachse Zentrum relativ").xScale=0
	obj.addProperty("App::PropertyFloat","xVa","Scale","Rotationsachse Zentrum relativ").xVa=1
	obj.addProperty("App::PropertyFloat","xVe","Scale","Rotationsachse Zentrum relativ").xVe=2

	obj.addProperty("App::PropertyFloat","yScale","Scale","Rotationsachse Zentrum relativ").yScale=0
	obj.addProperty("App::PropertyFloat","yVa","Scale","Rotationsachse Zentrum relativ").yVa=1
	obj.addProperty("App::PropertyFloat","yVe","Scale","Rotationsachse Zentrum relativ").yVe=2

	obj.addProperty("App::PropertyFloat","zScale","Scale","Rotationsachse Zentrum relativ").zScale=1
	obj.addProperty("App::PropertyFloat","zVa","Scale","Rotationsachse Zentrum relativ").zVa=1
	obj.addProperty("App::PropertyFloat","zVe","Scale","Rotationsachse Zentrum relativ").zVe=2

	obj.addProperty("App::PropertyLink","obj2","Object","rotating object ")

	_Scaler(obj)
	_ViewProviderScaler(obj.ViewObject)
	return obj


 
class _Scaler(Animation._Actor):

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
			self.obj2.obj2.Scale=newScale
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.Selection.clearSelection()


class _ViewProviderScaler(Animation._ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/scaler.png'
