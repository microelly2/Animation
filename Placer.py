# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import math,os

import FreeCAD, Animation, PySide
from Animation import say,sayErr,sayexc
from  EditWidget import EditWidget

__vers__= '0.1'
__dir__ = os.path.dirname(__file__)	

def createPlacer(name='My_Placer',target=None,src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	c3=obj

	c3.addProperty("App::PropertyLink","target","Base","")
	c3.target=target
	c3.addProperty("App::PropertyLink","src","Base","")
	c3.src=src
	c3.addProperty("App::PropertyFloat","time","Base","")
	c3.time=0.3

	c3.addProperty("App::PropertyPlacement","Placement","Results","")
	c3.Placement=FreeCAD.Placement()


	# parameter
	c3.addProperty("App::PropertyFloat","x0","Parameter","")
	c3.x0=0
	c3.addProperty("App::PropertyFloat","x1","Parameter","")
	c3.x1=200

	c3.addProperty("App::PropertyFloat","y0","Parameter","")
	c3.y0=0
	c3.addProperty("App::PropertyFloat","y1","Parameter","")
	c3.y1=0

	c3.addProperty("App::PropertyFloat","z0","Parameter","")
	c3.z0=0
	c3.addProperty("App::PropertyFloat","z1","Parameter","")
	c3.z1=0

	c3.addProperty("App::PropertyFloat","arc0","Parameter","")
	c3.arc0=0
	c3.addProperty("App::PropertyFloat","arc1","Parameter","")
	c3.arc1=90

	c3.addProperty("App::PropertyVector","RotCenter","Parameter","")
	c3.RotCenter=FreeCAD.Vector(5,5,0)

	c3.addProperty("App::PropertyVector","RotAxis","Parameter","")
	c3.RotAxis=FreeCAD.Vector(0,0,1)

	# functions 
	c3.addProperty("App::PropertyString","x","Functions","")
	c3.x="x0+(x1-x0)*time"
	c3.addProperty("App::PropertyString","y","Functions","")
	c3.y="0"
	c3.addProperty("App::PropertyString","z","Functions","")
	c3.z="0"
	c3.addProperty("App::PropertyString","arc","Functions","")
	c3.arc="time*360"

	_Placer(obj)
	_ViewProviderPlacer(obj.ViewObject)
	c3.Proxy.updater=True
	return obj

class _Placer(Animation._Actor):

	def update(self):
		time=self.obj2.time
		try:
			say("update time=" + str(time) + ", "+ self.obj2.Label)
		except:
			say("update (ohne Label)")

		# get the parameters
		x0=self.obj2.x0
		x1=self.obj2.x1
		y0=self.obj2.y0
		y1=self.obj2.y1
		z0=self.obj2.z0
		z1=self.obj2.z1
		arc0=self.obj2.arc0
		arc1=self.obj2.arc1

		try:
			sx=self.obj2.src.Placement.Base.x
			sy=self.obj2.src.Placement.Base.y
			sz=self.obj2.src.Placement.Base.z
			srx=self.obj2.src.Placement.Rotation.Axis.x
			sry=self.obj2.src.Placement.Rotation.Axis.y
			srz=self.obj2.src.Placement.Rotation.Axis.z
			sarc=self.obj2.src.Placement.Rotation.Angle
		except:
			pass 
			# saye("keine src festgelegt")

		# compute the new placement
		xv=eval(self.obj2.x)
		yv=eval(self.obj2.y)
		zv=eval(self.obj2.z)
		arcv=eval(self.obj2.arc)

		rot=FreeCAD.Rotation(self.obj2.RotAxis,arcv)
		pl=FreeCAD.Placement(FreeCAD.Vector(xv,yv,zv),rot,self.obj2.RotCenter)
		#say(pl)
		if str(self.obj2.target.TypeId) == 'App::Annotation':
			self.obj2.target.Position=(xv,yv,zv)
		else:
			self.obj2.target.Placement=pl
		self.obj2.Placement=pl

	def step(self,now):
			say("step "+str(now) + str(self))
			self.obj2.time=float(now)/100

class _ViewProviderPlacer(Animation._ViewProviderActor):

	def __init__(self,vobj):
		say(self)
		Animation._ViewProviderActor.__init__(self,vobj)
		self.attach(vobj)

	def attach(self,vobj):
		# items for edit dialog  and contextmenue
		self.emenu=[['A',self.funA],['B',self.funB]]
		self.cmenu=[['AC',self.funA],['BC',self.funB]]
		
		say("VO attach " + str(vobj.Object.Label))
		vobj.Proxy = self
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		icon='/icons/animation.png'
		self.iconpath = __dir__ + icon
		return

	def setupContextMenu(self, obj, menu):
		cl=self.Object.Proxy.__class__.__name__
		action = menu.addAction("About " + cl)
		action.triggered.connect(self.showVersion)

		action = menu.addAction("Edit ...")
		action.triggered.connect(self.edit)

		for m in self.cmenu:
			action = menu.addAction(m[0])
			action.triggered.connect(m[1])

	def edit(self):
		self.dialog=EditWidget(self,self.emenu)
		self.dialog.show()

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "Animation" + cl +" Node\nVersion " + __vers__ )

	def dialer(self):
		self.obj2.time=float(self.widget.dial.value())/100
		FreeCAD.ActiveDocument.recompute()

	def funA(self):
		say("ich bin FunA")

	def funB(self):
		say("ich bin FunB")
