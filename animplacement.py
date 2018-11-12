# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- 
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 

__vers__='0.1'

try:
	__dir__ = os.path.dirname(__file__)
	say(__dir__)
except:
	__dir__='/usr/lib/freecad/Mod/mylib'

def say(s):
	FreeCAD.Console.PrintMessage(str(s)+"\n")

def saye(s):
	FreeCAD.Console.PrintError(str(s)+"\n")

import FreeCAD,os,time,sys,traceback

def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))

classname='AnimPlacement'

def create(name,target,src=None):
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

	_AnimPlacement(obj)
	_ViewProviderAnimPlacement(obj.ViewObject)
	c3.Proxy.updater=True
	return obj

class _AnimPlacement():

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_AnimPlacement"
		self.obj2 = obj 
		self.Lock=False
		self.Changed=False

	def execute(self,obj):
		if self.obj2.ViewObject.Visibility == False:
			return
			
		if self.Changed:
			say("self changed")
			# ignore self changes
			self.Changed=False
			return
		if not self.Lock:
			say("set Lock ----- " +str(obj.Label))
			self.obj2=obj
			self.Lock=True
			try:
				self.update()
			except:
				sayexc('update')
			self.Lock=False
			say("unset Lock +++ " +str(self.obj2.Label))

	def update(self):
		say("update ")
		import math
		time=self.obj2.time
		say(str(time))
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
			saye("keine src festgelegt")

		xv=eval(self.obj2.x)
		yv=eval(self.obj2.y)
		zv=eval(self.obj2.z)
		arcv=eval(self.obj2.arc)

		rot=FreeCAD.Rotation(self.obj2.RotAxis,arcv)
		pl=FreeCAD.Placement(FreeCAD.Vector(xv,yv,zv),rot,self.obj2.RotCenter)
		say(pl)
		if str(self.obj2.target.TypeId) == 'App::Annotation':
			self.obj2.target.Position=(xv,yv,zv)
		else:
			self.obj2.target.Placement=pl
		self.obj2.Placement=pl

	def __getstate__(self):
		say("getstate " + str(self))
		return None

	def __setstate__(self,state):
		say("setstate " + str(self) + str(state))
		return None

	def onChanged(self,obj,prop):
		pass
#		say("on Changed")
#		say(obj)
#		say(prop)

	def onBeforeChange(self,obj,prop):
		pass
#		say("on before change")
	
	def initialize(self):
			say("initialize")


	def step(self,now):
			say("step XX")
			say(now)
			self.obj2.time=float(now)/100
			say(self)

class _ViewProviderAnimPlacement(object):
 
	def getIcon(self):
		return __dir__ +'/icons/sun.png'
   
	def __init__(self,vobj):
		say("__init__" + str(self))
		self.Object = vobj.Object
		vobj.Proxy = self

	def attach(self,vobj):
		say("attach " + str(vobj.Object.Label))
		self.Object = vobj.Object
		self.obj2=self.Object
#		if not hasattr(self.Object.Proxy,"Lock"):
#				self.Object.Proxy.Lock=False
#				say("lock gesetzt")
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		return

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		say("getstate " + str(self))
		return None

	def __setstate__(self,state):
		say("setstate " + str(self) + str(state))
		return None
		
	def setEdit(self,vobj,mode=0):
		s=TimeWidget(self)
		self.dialog=s
		self.dialog.show()
		say("set Edit")
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		say("double clicked")
		self.setEdit(vobj,1)

	def setupContextMenu(self, obj, menu):
#		action = menu.addAction("About VertexPlugger")
#		action.triggered.connect(self.showVersion)

		action = menu.addAction("Animate ...")
		action.triggered.connect(self.edit)

	def edit(self):
		self.dialog=TimeWidget(self)
		self.dialog.show()

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About ", "Animation Placement Node\n2015 microelly\nVersion " + __vers__ +"\nstill alpha")

	def dreher(self):
		self.obj2.time=float(self.widget.dial.value())/100
		FreeCAD.ActiveDocument.recompute()


class TimeWidget(QtGui.QWidget):
	def __init__(self, obj,*args):
		QtGui.QWidget.__init__(self, *args)
		obj.widget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.vollabel = QtGui.QLabel(obj.Object.Label)

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.setText("close")
		self.pushButton02.clicked.connect(self.hide)

		dial = QDial()
		dial.setNotchesVisible(True)
		self.dial=dial
		dial.setMaximum(100)
		dial.valueChanged.connect(obj.dreher);
		layout = QHBoxLayout()

		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 0)

		layout.addWidget(self.pushButton02, 15, 0,1,4)
		layout.addWidget(dial,3,0)

		self.setLayout(layout)
		self.setWindowTitle(obj.Object.target.Label)


'''

The next generation of animation tools will support formulas and 
allow to move the timeline forward an backward by hand

'''

if __name__ == "__main__":

	# All examples from top view to the xy-plane

	# Example 1
	box=App.ActiveDocument.addObject("Part::Box","Bax")
	t=create("Anim "+box.Label,box)
	box.ViewObject.ShapeColor=(.0,1.0,.0)
	# linear function - left upper corner to right bottom 
	t.x0=-150
	t.x1=150
	t.y0=150
	t.y1=-150
	t.y="y0+(y1-y0)*time"
	t.z="100 - 400 * (0.5-time)**2"



	# Example 2
	box1=App.ActiveDocument.addObject("Part::Cone","Bux")
	box1.ViewObject.ShapeColor=(1.0,.0,.0)
	t1=create("Anim "+box1.Label,box1)
	t1.x0=-150
	t1.x1=150
	t1.y0=-150
	t1.y1=150
	# parabel - left bottom to right top
	t1.y="y0+(y1-y0)*time**2"
	t1.y
	t1.x



	# Example 3
	box3=App.ActiveDocument.addObject("Part::Cylinder","Circler")
	box3.ViewObject.ShapeColor=(1.0,.0,1.0)
	t3=create("Anim "+box3.Label,box3)
	# ellipse
	t3.y="80 * math.sin(math.pi*2*time)"
	t3.x="80 * math.cos(math.pi*2*time)"
	# t3.z="400 * (0.5-time)**2"
	t3.z="0"


	box3=App.ActiveDocument.addObject("Part::Sphere","Circler-helper")
	box3.ViewObject.ShapeColor=(1.0,.0,1.0)
	tt3=create("Anim "+box3.Label,box3,t3)
	# ellipse
	tt3.y="sx"
	tt3.x="sx"
	tt3.z="sz"

	# Example 4
	box4=App.ActiveDocument.addObject("Part::Cylinder","T1")
	box4.ViewObject.ShapeColor=(1.0,1.0,.0)
	t1=create("Anim "+box4.Label,box4,t3)
	# ellipse
	t1.y="87"
	t1.x="-50"
	t1.z="math.sqrt(195**2 - (sx+50)**2  - (sy-87)**2-5)"

	# Example 4
	box4=App.ActiveDocument.addObject("Part::Cylinder","T2")
	box4.ViewObject.ShapeColor=(1.0,1.0,.0)
	t1=create("Anim "+box4.Label,box4,t3)
	# ellipse
	t1.y="-87"
	t1.x="-50"
	t1.z="math.sqrt(195**2 - (sx+50)**2  - (sy+87)**2)-5"

	# Example 4
	box4=App.ActiveDocument.addObject("Part::Cylinder","T3")
	box4.ViewObject.ShapeColor=(1.0,1.0,.0)
	t1=create("Anim "+box4.Label,box4,t3)
	# ellipse
	t1.y="0"
	t1.x="100"
	t1.z="math.sqrt(195**2 - (sx-100)**2  - (sy)**2)-5"


#math.sqrt(195**2 - (sx-100)**2  - (sy)**2)
#math.sqrt(195**2 - (sx+50)**2  - (sy-87)**2)
#math.sqrt(195**2 - (sx+50)**2  - (sy+87)**2)



		

'''
# to use 
# 1. install latest version of animation workbench

# 2.  create objects (still without gui support)

import animplacement

box=App.ActiveDocument.addObject("Part::Box","My Box")
animator=animplacement.create("A"+box.Label,box)
animator.x ="time *100 + math.pi "  # formula as string with math support

# 3. double click the animator icon  ...
# and change time value with the dialer from 0 to 1

'''







