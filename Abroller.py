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

def updateData(obj,sk=None):

	if sk != None: 	obj.path=sk

	sk=obj.path
	sk.Placement.Rotation.Angle=0

	w=sk.Shape
	assert (abs(w.Vertexes[0].Point.y) <10**-2)
	if obj.countPoints<5:obj.countPoints=5
	if obj.densityPoints<1:obj.densityPoints=1

	c=w.Edges[0].Curve

	anz=obj.countPoints
	pts=w.discretize(anz+1)

	obj.pathName=sk.Name+'_Anim'

	cyy=App.ActiveDocument.getObject(obj.pathName)
	if cyy==None:
		cyy=App.ActiveDocument.addObject('Part::Feature',obj.pathName)


	pol=Part.makePolygon(w.discretize(anz+1))
#	obj.pola=w.discretize(200)
	cyy.Shape=pol


	obj.pola=w.discretize(anz+1)
	pol=Part.makePolygon(obj.pola)

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


	of=App.ActiveDocument.getObject(obj.pathName+"_Offset")
	if of==None:
		of=App.ActiveDocument.addObject("Part::Offset2D",obj.pathName+"_Offset")
	of.Source = obj.path
	of.Value = obj.offsetValue
	obj.offset=of



	App.activeDocument().recompute()
	Gui.updateGui()
	w2=of.Shape.Wires[0]

	ptsa=[]
	for e in w2.Edges:
		dian=int(round(e.Length*obj.densityPoints))
		ptsa +=  e.discretize(dian+1)[:-1]


	alphaq=[np.arctan2(p.y,p.x) for p in ptsa]

	alpha=[]

	for a in alphaq[:-1]:
		if a <0: a += 2*np.pi
		alpha += [a]

	alpha += [2*np.pi+alpha[0]]



	anz=len(alpha)
	ns=np.arange(len(alpha))
	
	#if obj.useBSpline:
	bc=Part.BSplineCurve()
	bc.approximate(ptsa,DegMin=1,DegMax=obj.degreeBSpline,Tolerance=obj.approxTolerance)




	cww=App.ActiveDocument.getObject(obj.pathName+"_OFFSET")
	if cww== None:
		cww=App.ActiveDocument.addObject('Part::Feature',obj.pathName+'_OFFSET')
	
	obj.polb=ptsa
	pol=Part.makePolygon(ptsa)
	cww.Shape=pol
	if obj.useBSpline:
		cww.Shape=bc.toShape()
	
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


	Gui.updateGui()
	if obj.circle==None:
		obj.circle=Draft.makeCircle(obj.offsetValue)
	if obj.circle2==None:
		obj.circle2=Draft.makeCircle(1)

	obj.kka=[FreeCAD.Vector(p) for p in kka]

	return pol


def runAnimation(obj=None,loop=False):

	cww=App.ActiveDocument.getObject(obj.pathName+"_OFFSET")
	cyy=App.ActiveDocument.getObject(obj.pathName)

	if loop: ixs=obj.kka
	else: ixs=[obj.kka[obj.anim]]

	for i,p in enumerate(ixs):

		pp=Part.Point(FreeCAD.Vector(p))

		if 0:
			w=App.ActiveDocument.Sketch.Shape
			dist=w.distToShape(pp.toShape())
			print dist[0]

		obj.circle.Placement.Base=FreeCAD.Vector(p.Length,0,0)
		obj.circle2.Placement.Base=FreeCAD.Vector(p.Length,0,0)

		alpha=np.arctan2(p.y,p.x)*180/np.pi

		cww.Shape=Part.makePolygon(obj.pola)
		cww.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-alpha)

		cyy.Shape=Part.makePolygon(obj.polb)
		cyy.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-alpha)

		print cyy.Placement

		if loop:
			App.activeDocument().recompute()
			Gui.updateGui()
			time.sleep(0.1)
			if i>10: return


	def step(self,now):
			self.obj2.time=float(now)


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
		pass

	def onChanged(self,obj,prop):
		print "prop",prop
		if prop=='anim':
			runAnimation(obj)
		if prop in ['offsetValue','path','densityPoints','countPoints','degreeBSpline','useBSpline']:
			updateData(obj)

	def step(self,now):
			self.Object.anim=int(round(now))

	def initialize(self):
		pass



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

	obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","MeinAbroller")
	obj.addProperty("App::PropertyLink", "circle", "_aux", "scooter")
	obj.addProperty("App::PropertyLink", "circle2", "_aux", "center of scooter")
	obj.addProperty("App::PropertyLink", "offset", "_aux", "end")
	obj.addProperty("App::PropertyLink", "path", "Base", "closed  single wire path for the scooter")
	obj.addProperty("App::PropertyInteger", "anim", "Base", "displayed frame number")
	obj.addProperty("App::PropertyInteger", "countPoints", "_aux", "number of points of the path to interpolate").countPoints=40
	obj.addProperty("App::PropertyInteger", "densityPoints", "_aux", "number of points of the generated curves per mm").densityPoints=3

	obj.addProperty("App::PropertyFloat", "offsetValue", "Base", "size of the scooter").offsetValue=10
	obj.addProperty("App::PropertyFloat", "approxTolerance", "_aux", "tolerance for BSpline Approximation").approxTolerance=3.
	obj.addProperty("App::PropertyInteger", "degreeBSpline", "_aux", "degree of the BSpline ").degreeBSpline=1

	obj.addProperty("App::PropertyBool", "useBSpline", "_aux", "use BSpline Approx for offset curve").useBSpline=True

	# helper data
	obj.addProperty("App::PropertyVectorList", "kka", "_comp", "end")
	obj.addProperty("App::PropertyVectorList", "pola", "_comp", "end")
	obj.addProperty("App::PropertyVectorList", "polb", "_comp", "end")
	obj.addProperty("App::PropertyString", "pathName", "_aux", "label for the path")

	print "create abroller"

	try: sk=Gui.Selection.getSelection()[0]
	except: sk= None
	try: m=Gui.Selection.getSelection()[1]
	except: m=None

	shape=updateData(obj,sk)
	Abroller(obj)
#	obj.Proxy.Shape=shape
	obj.Shape=Part.Shape()


	ViewProvider(obj.ViewObject)
	#if m != None:
	#	obj.setExpression('anim', m.Name+'.step')

	# runAnimation(obj,True)
