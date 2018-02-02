import FreeCAD
import FreeCADGui
import PySide
from PySide import QtGui
import os

App=FreeCAD
Gui=FreeCAD.Gui


import numpy as np
import Draft
import Part
import time

def updateData(obj,sk):
	print "huhu"
#	sk=App.ActiveDocument.Sketch
	obj.path=sk
	sk.Placement.Rotation.Angle=0




	w=sk.Shape
	assert (abs(w.Vertexes[0].Point.y) <10**-6)

#	w=App.ActiveDocument.Sketch.Shape
	c=w.Edges[0].Curve

	anz=10
	pts=w.discretize(anz+1)
#	dw=Draft.makeWire(w.discretize(200))

	obj.pathName=sk.Name+'_Anim'
	cyy=App.ActiveDocument.getObject(obj.pathName)
	if cyy==None:
		cyy=App.ActiveDocument.addObject('Part::Feature',obj.pathName)
		
	pol=Part.makePolygon(w.discretize(200))
	obj.pola=w.discretize(200)
	cyy.Shape=pol
#	App.ActiveDocument.removeObject(dw.Label)

	alphaq=[np.arctan2(p.y,p.x) for p in pts]
	ns=np.arange(anz+1)
	alpha=[]

	for a in alphaq[:-1]:
		if a <0: a += 2*np.pi
		alpha += [a]

	alpha += [2*np.pi]

	# jetzt die Animationsschritte
	anz2=10
	rra=np.arange(2*anz2+1)*np.pi*2/(2*anz2+1) 
	pos=np.interp(rra, alpha, ns)/(anz)

	kk=[]
	for p in pos:
		kk += [c.value(p),FreeCAD.Vector()]

	#dw=Draft.makeWire(kk)
	#dw.ViewObject.hide()



	of=App.ActiveDocument.addObject("Part::Offset2D","Offset2D")
	of.Source = obj.path
	of.Value = 10.0

	App.activeDocument().recompute()
	w2=of.Shape.Wires[0]

	ptsa=[]
	for e in w2.Edges:
		dian=int(round(e.Length*3))
		ptsa +=  e.discretize(dian+1)[:-1]

	#wa=Draft.makeWire(ptsa)


	alphaq=[np.arctan2(p.y,p.x) for p in ptsa]
	alphaq

	alpha=[]

	for a in alphaq[:-1]:
		if a <0: a += 2*np.pi
		alpha += [a]

	alpha += [2*np.pi+alpha[0]]

	anz=len(alpha)
	ns=np.arange(len(alpha))
	bc=Part.BSplineCurve()
	bc.approximate(ptsa,DegMax=3,Tolerance=.2)



	cww=App.ActiveDocument.getObject(obj.pathName+"_")
	if cww== None:
		cww=App.ActiveDocument.addObject('Part::Feature',obj.pathName+'_OFFSET')
		
	pol=Part.makePolygon(ptsa)
	cww.Shape=pol
	obj.polb=ptsa

	App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.,0.,0.)
	App.ActiveDocument.ActiveObject.ViewObject.LineWidth=8
	Gui.updateGui()


	# jetzt die Animationsschritte
	anz2=50
	rra=np.arange(2*anz2+1)*np.pi*2/(2*anz2+1) 
	pos=np.interp(rra, alpha, ns)/(anz)

	kk=[]
	kka=[]
	for p in pos:
		pp=bc.value(p)
		pp2=bc.value(p)
		pp2.normalize()

		kk += [pp,FreeCAD.Vector()]
		kka += [pp]

	#dw=Draft.makeWire(kk)
	#dw.ViewObject.hide()

	Gui.updateGui()
	obj.circle=Draft.makeCircle(10)
	obj.circle2=Draft.makeCircle(1)

	#dw=Draft.makeWire(kka)
	#dw.ViewObject.hide()
	obj.kka=[FreeCAD.Vector(p) for p in kka]
	return pol
	

def runAnimation(obj=None):


	cww=App.ActiveDocument.getObject(obj.pathName+"_OFFSET")
	cyy=App.ActiveDocument.getObject(obj.pathName)
	a=cww.Shape.copy()

	kka=obj.kka
	# print kka
	for i,p in enumerate(kka):
		pass
	
	if 1:
		i=obj.anim
		p=kka[i]
	#	if i >20: return

		pp=Part.Point(FreeCAD.Vector(p))

		if 0:
			w=App.ActiveDocument.Sketch.Shape
			dist=w.distToShape(pp.toShape())
			print dist[0]

		obj.circle.Placement.Base=FreeCAD.Vector(p.Length,0,0)
		obj.circle2.Placement.Base=FreeCAD.Vector(p.Length,0,0)
		
		alpha=np.arctan2(p.y,p.x)*180/np.pi
		print 
		print alpha
#		a=cww.Shape
		cww.Shape=Part.makePolygon(obj.pola)
		cww.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-alpha)

		# App.ActiveDocument.Sketch.Placement.Rotation.Angle=-alpha
		
		
		print cyy.Placement
		cyy.Shape=Part.makePolygon(obj.polb)
		cyy.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-alpha)
		print cyy.Placement

		#App.activeDocument().recompute()
		#Gui.updateGui()
		#time.sleep(0.1)



class Abroller:
	''' basic defs'''

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj

	def attach(self, vobj):
		self.Object = vobj.Object

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None

	def execute(self,obj):
		print "excute ..."
	
	def onChanged(self,obj,prop):
		print "prop",prop
		if prop=='anim':
			runAnimation(obj)


class ViewProvider:
	''' basic defs '''

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None

	def getIcon(self):
		__dir__ = os.path.dirname(__file__)	
		return  __dir__+ '/icons/abroller.png'

#-------------------------------







def createAbroller():

	obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython","MeinAbroller")
	obj.addProperty("App::PropertyLink", "circle", "Base", "end")
	obj.addProperty("App::PropertyLink", "circle2", "Base", "end")
	obj.addProperty("App::PropertyLink", "offset", "Base", "end")
	obj.addProperty("App::PropertyLink", "path", "Base", "end")
	obj.addProperty("App::PropertyString", "pathName", "Base", "end")
	obj.addProperty("App::PropertyInteger", "anim", "Base", "end")
	obj.addProperty("App::PropertyVectorList", "kka", "Base", "end")
	obj.addProperty("App::PropertyVectorList", "pola", "Base", "end")
	obj.addProperty("App::PropertyVectorList", "polb", "Base", "end")

	print "create abroller"
	sk=Gui.Selection.getSelection()[0]
	try:
		m=Gui.Selection.getSelection()[1]
	except: m=None
	shape=updateData(obj,sk)
	# runAnimation(obj)
	Abroller(obj)
	obj.Proxy.Shape=shape
	obj.Shape=Part.Shape()


	ViewProvider(obj.ViewObject)
	if m != None:
		obj.setExpression('anim', m.Name+'.step')
