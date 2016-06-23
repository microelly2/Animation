#-*- coding: utf-8 -*-
#-------------------------------------------------
#-- Animation workbench
#--
#-- microelly 2016
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import math,os

import FreeCAD, FreeCADGui, Animation, PySide
from Animation import say,sayErr,sayexc
from  EditWidget import EditWidget

__vers__= '0.1'
# __dir__ = os.path.dirname(__file__)

__dir__="/home/thomas/.FreeCAD/Mod/Animation"


import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui

import Draft

import PySide
from PySide import QtCore, QtGui

import cProfile
import Points
import random
import time
import numpy as np



#-------
# user defined function 
#------

import flowlib
reload(flowlib)

force=flowlib.force
damper=flowlib.damper

#
# end of user function 
#


def velocity(self,ix,mytime):

	(x,y,z)=self.ptslix[ix]

	xy=ix%(self.obj2.dimU*self.obj2.dimV)
	xp=xy//self.obj2.dimV
	yp=xy%self.obj2.dimU

	# geschwindkeit anpassen -- kraft am ort x,y,z addieren
	self.pvs[xp,yp] += force(x,y,z,self.pvs[xp,yp],mytime)

	tt=self.pvs[xp,yp]

	(dx,dy,dz) =damper(x,y,z,self.pvs[xp,yp],mytime)
	self.pvs[xp,yp]  *= damper(x,y,z,self.pvs[xp,yp],mytime)

	xn,yn,zn=x+tt[0],y+tt[1],z+tt[2]

	ddx=1
	ddy=1
	ddz=0.1

	if self.obj2.boundMode=='Bound Box':
		if zn<=0:

			if xn>self.xmax:
				xn=self.xmax -ddx*(xn-self.xmax)
				self.pvs[xp,yp][0]  *= -1 
			if xn<self.xmin:
				xn=self.xmin -ddx*(xn-self.xmin)
				self.pvs[xp,yp][0]  *= -1 

			if yn>self.ymax:
				yn=self.ymax -ddy*(yn-self.ymax)
				self.pvs[xp,yp][1]  *= -1 
			if yn<self.ymin:
				yn=self.ymin -ddy*(yn-self.ymin)
				self.pvs[xp,yp][1]  *= -1 

			if zn>self.zmax:
				zn=self.zmax -ddz*(zn-self.zmax)
				self.pvs[xp,yp][2]  *= -1 
			if zn<self.zmin:
				zn=self.zmin -ddz*(zn-self.zmin)
				self.pvs[xp,yp][2]  *= -1 

	elif self.obj2.boundMode=='no Bounds':
		pass
	else:
		sayErr("nont implemented mode" + self.obj2.boundMode)

	self.ptslix[ix+self.obj2.dimU*self.obj2.dimV]=[xn,yn,zn]
	return self.ptslix[ix+self.obj2.dimU*self.obj2.dimV]



# vectorize the velocity function
velo=np.frompyfunc(velocity,3,1)

# why vectorize does not work ?#+#?
# velo=np.vectorize(velocity)


def createStartPtsSquare(self):
	''' create the starting cloud - square '''
	for x in range(self.obj2.dimU):
		for y in range(self.obj2.dimV):
			self.ptslix[y*self.obj2.dimU+x]=[x,y,3]


def createStartPtsCircle(self):
	''' create the starting cloud filled circle/cone '''
	for x in range(self.obj2.dimU):
		for y in range(self.obj2.dimV):
			self.ptslix[y*self.obj2.dimU+x]=[0.3*(10+y)*np.cos(np.pi*2*x/self.obj2.dimU),
					0.3*(10+1.2*y)*np.sin(np.pi*2*x/self.obj2.dimU),0]


def createStartPtsV2(self):
	if self.obj2.startFace == "Circle":
		createStartPtsCircle(self)
	elif self.obj2.startFace == "Rectangle":
		createStartPtsSquare(self)

def createStepPtsV2(self,i):
	velo(self,self.ptsl[i],i)



def createStepFC(self,i):
	objs=pclgroup()
	(la,lb)=self.ptsl[i].shape
	pts=[tuple(self.ptslix[self.ptsl[i][a][b]]) for a in range(la) for b in range(lb)]

	pcl=Points.Points(pts)
	Points.show(pcl)

	App.activeDocument().recompute()
	if i%25==0: Gui.SendMsgToActiveView("ViewFit")

	obj=App.ActiveDocument.ActiveObject
	obj.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	obj.Placement=self.obj2.startPosition
	objs.addObject(obj)

	return obj




def animateIntervall(pb=None,start=0,ende=None,objs=None):
	if objs==None: 
		objs=pclgroup().OutList
	if ende==None: ende=len(objs)
	if pb == None: 	pb=createProgressBar("animation ..")

	for u in objs: u.ViewObject.hide()

	k=3
	kk=10
	kkk=30

	for i in range(start,ende):

		pb.pb.setValue(i*100/(ende-start-1))

		try:
			objs[i-kkk].ViewObject.hide()
			for j in range(kkk):
				objs[i-j].ViewObject.ShapeColor=(.0,1.0,1.0)
		except: pass

		try:
			for j in range(kk):
				objs[i-j].ViewObject.ShapeColor=(1.0,.7,0.0)
		except: pass

		try:
			for j in range(k):
				objs[i-j].ViewObject.ShapeColor=(1.0,1.0,0.0)
		except: pass

		objs[i].ViewObject.ShapeColor=(1.0,0.0,0.0)
		objs[i].ViewObject.show()
		App.activeDocument().recompute()
		Gui.updateGui()
		time.sleep(0.1)

	App.activeDocument().recompute()
	Gui.updateGui()
	pb.hide()
	objs[i].ViewObject.hide()


def hideAll():
	objs=pclgroup().OutList
	cc=(random.random(),random.random(),random.random())
	for ob in objs:
		ob.ViewObject.ShapeColor=cc
		ob.ViewObject.hide()

def showAll():
	objs=pclgroup().OutList
	for ob in objs:
		ob.ViewObject.show()


def createProgressBar(label=None):
	w=QtGui.QWidget()
	hbox = QtGui.QHBoxLayout()
	w.setLayout(hbox)
	pb=QtGui.QProgressBar()
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	if label<>None:
		lab=QtGui.QLabel(label)
		hbox.addWidget(lab)
	hbox.addWidget(pb)
	w.show()
	FreeCAD.w=w
	pb.setValue(0)
	w.pb=pb
	return w





def createFCOs(self,anz,step=1):
	pb=createProgressBar("create FreeCAD objects")
	for i in range(anz-1):
		if i%step == 0: 
			createStepFC(self,i)
			pb.pb.setValue(i*100/(anz-2))
			Gui.updateGui()







def tgroup():
	try: return App.ActiveDocument.TrackGroup
	except: return   App.ActiveDocument.addObject("App::DocumentObjectGroup","TrackGroup")

def pclgroup():
	try: return App.ActiveDocument.PCLGroup
	except: return   App.ActiveDocument.addObject("App::DocumentObjectGroup","PCLGroup")




'''
anz=8000
anz=2
step=1
cProfile.run('main(%d)' %anz)
cProfile.run('createFCOs(%d,%d)' %(anz,step))
cProfile.run('hideAll()')
cProfile.run('showAll()')
cProfile.run('animateIntervall()')
dial=createSingleSliceViewer()
'''



def createFlow(name='My_Flow',target=None,src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyFloat","time","Base","")
	obj.addProperty("App::PropertyInteger","countSlices","Base","").countSlices=20
	obj.addProperty("App::PropertyInteger","dimU","Base","").dimU=50
	obj.addProperty("App::PropertyInteger","dimV","Base","").dimV=100
	obj.addProperty("App::PropertyLink","boundBox","Base","")
	obj.addProperty("App::PropertyEnumeration","boundMode","Base","")
	obj.boundMode=['no Bounds','Bound Box','Bound Cylinder','Bound Sphere']

	obj.addProperty("App::PropertyEnumeration","startFace","Base","")
	obj.startFace=['Circle','Rectangle']
	
	obj.addProperty("App::PropertyPlacement","startPosition","Base","")
	obj.startPosition.Base=FreeCAD.Vector(50,10,-30)

	obj.boundMode='Bound Box'

	try:obj.boundBox=App.ActiveDocument.Box
	except: pass


	_Flow(obj)
	_ViewProviderFlow(obj.ViewObject)
	return obj

class _Flow(Animation._Actor):

	def step(self,now):
			say("step "+str(now) + str(self))
			self.obj2.time=float(now)/100

	def update(self):
		time=self.obj2.time
		try:
			say("update time=" + str(time) + ", "+ self.obj2.Label)
		except:
			say("update (ohne Label)")
		objs=pclgroup().OutList
		for u in objs: u.ViewObject.hide()
		i=int(round(time*(len(objs)-1)))
		print i
		objs[i].ViewObject.show()


	def createTracks(self):

		t=tgroup()

		(zc,xc,yc)=self.ptsl.shape
		pb=createProgressBar("create tracks ..")

		for x in range(self.obj2.dimU):
			if x%10<>0: continue
			for y in range(self.obj2.dimV):
				if y%10<>0: continue
				pts=[]
				for z in range(zc):
					p=FreeCAD.Vector(tuple(self.ptslix[self.ptsl[z,x,y]]))
					pts.append(p)
				try:
					Draft.makeWire(pts)
					App.ActiveDocument.ActiveObject.ViewObject.LineColor = (.0,1.00,0.0)
					App.ActiveDocument.ActiveObject.ViewObject.PointColor = (.0,.0,1.00)
					App.ActiveDocument.ActiveObject.ViewObject.LineWidth= 1
					t.addObject(App.ActiveDocument.ActiveObject)
				except:
					pass
			pb.pb.setValue((50+x))
			Gui.updateGui()
		pb.hide()



	def m2(self,value):
		objs=pclgroup().OutList
		for u in objs:
			u.ViewObject.hide()
		objs[value].ViewObject.show()
		objs[value].ViewObject.PointSize=2
		objs[self.lastvalue].ViewObject.hide()
		self.lastvalue=value



	def createSingleSliceViewer(self,label=None):

		w=QtGui.QWidget()
		hbox = QtGui.QVBoxLayout()
		w.setLayout(hbox)

		if label<>None:
			lab=QtGui.QLabel(label)
			hbox.addWidget(lab)


		dial = QtGui.QDial()
		w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

		dial.setNotchesVisible(True)
		objs=pclgroup().OutList
		pc=len(objs)
		dial.setMaximum(pc-1)
		dial.setMinimum(0)

		self.lastvalue=0
		dial.valueChanged.connect(self.m2)
		hbox.addWidget(dial)

		bt=QtGui.QPushButton("animate loop")
		hbox.addWidget(bt)
		bt.clicked.connect(animateIntervall)

		w.show()
		hideAll()
		FreeCAD.ssv=w
		return w


	def main(self):

		anz=self.obj2.countSlices

		pb=createProgressBar("calculate Points")

		xc=self.obj2.dimU
		yc=self.obj2.dimV
		zc=anz

		# point index
		self.ptsl=np.arange(xc*yc*zc).reshape(zc,xc,yc)

		# anfangsgeschwindigkeiten der Teilchen
		self.pvs=np.zeros(xc*yc*3)
	#	self.pvs += 1
		self.pvs=self.pvs.reshape(xc,yc,3)
	# 	self.pvs[:,:] += [0,0,10]

		self.ptslix=np.zeros(xc*yc*zc*3).reshape(xc*yc*zc,3)


		bb=self.obj2.boundBox.Shape.BoundBox
		self.xmax=bb.XMax
		self.ymax=bb.YMax
		self.zmax=bb.ZMax
		self.xmin=bb.XMin
		self.ymin=bb.YMin
		self.zmin=bb.ZMin

		createStartPtsV2(self)

		for i in range(anz-1): 
			createStepPtsV2(self,i)
			pb.pb.setValue(i*100/(anz-2))

		createFCOs(self,anz,1)

		showAll()
		Gui.SendMsgToActiveView("ViewFit")
		hideAll()

		pb.hide()
		animateIntervall()





class _ViewProviderFlow(Animation._ViewProviderActor):

	def __init__(self,vobj):
		Animation._ViewProviderActor.__init__(self,vobj)
		self.attach(vobj)

	def attach(self,vobj):
		# items for edit dialog  and contextmenue
		self.emenu=[['(re)compute all data',self.funA],
					['create tracks',self.funB],
					['animate ',self.funC]]
		self.cmenu=self.emenu

		vobj.Proxy = self
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		self.touchTarget=True
		icon='/icons/placer.png'
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

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "Animation" + cl +" Node\nVersion " + __vers__ )

	def dialer(self):
		self.obj2.time=float(self.widget.dial.value())/100
		self.Object.Proxy.update()



	def funA(self):
		''' run complete calculation'''
		FreeCAD.ssv=None
		self.Object.Proxy.main()
		FreeCAD.ActiveDocument.recompute()

	def funB(self):
		''' create  some tracks '''
		self.Object.Proxy.createTracks()

	def funC(self):
		''' view menu for slices '''
		self.Object.Proxy.createSingleSliceViewer("Animation v.0")



def run():

	if App.ActiveDocument==None:
		App.newDocument("Unnamed")
		App.setActiveDocument("Unnamed")
		App.ActiveDocument=App.getDocument("Unnamed")
		Gui.ActiveDocument=Gui.getDocument("Unnamed")


	# initialize scene
	Gui.ActiveDocument.ActiveView.setAnimationEnabled(False)
	App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
	App.ActiveDocument.ActiveObject.Label = "Cylinder"
	App.ActiveDocument.ActiveObject.Height=50
	App.ActiveDocument.ActiveObject.Radius=10
	App.ActiveDocument.ActiveObject.ViewObject.Transparency=70

	b=App.ActiveDocument.addObject("Part::Box","Box")
	b.Length=40
	b.Width=50
	b.Height=200
	b.Placement.Base=App.Vector(-40,-60,-30)
	b.ViewObject.Transparency=70

	Gui.activeDocument().activeView().viewAxonometric()
	App.activeDocument().recompute()

	f=createFlow()


# run()
