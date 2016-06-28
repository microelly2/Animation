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

# force=flowlib.force
# damper=flowlib.damper

#
# end of user function 
#


def lineCircleCommon(x0,y0,x1,y1,r):
	''' schnittpunkt kreis mit strecke'''

	v1=x1-x0
	v2=y1-y0

	rv2=v1**2+v2**2

	zz=-(x0*v1+y0*v2)/rv2
	D=zz**2 - (x0**2+y0**2-r**2)/rv2
	if D<0:
		print "Fehler Diskriminante r=", r
		print zz
		print (x0**2+y0**2-r**2)/rv2
		print rv2
		print "D=",D
		print (x0,y0)
		print np.sqrt(x0**2+y0**2)
		print (x1,y1)
		print np.sqrt(x1**2+y1**2)
		if D>-20: D=0
	t=zz + np.sqrt(D)

	x2=x0+v1*t
	y2=y0+v2*t
	x2=0.95*x2
	y2=0.95*y2
	# print np.sqrt(x2**2+y2**2)
	return(x2,y2)


def mirrorCircle(x0,y0,x2,y2):
#	base=M
#	dir=P2.sub(M)
	dir=FreeCAD.Vector(x2,y2,0)

	pnt=FreeCAD.Vector(x0,y0,0)
	diff = FreeCAD.Vector() # this will be the vector from pnt to the projection of pnt
	diff.projectToLine(pnt,dir)
	proj = pnt + diff # proj now lies on the line
	mirr = proj + diff
#	print proj
#	print diff
#	print mirr
	return (mirr.x,mirr.y)


def velocity(self,ix,mytime):

	force=self.force
	damper=self.damper
	
	(x,y,z)=self.ptslix[ix]

	xy=ix%(self.obj2.dimU*self.obj2.dimV)
#	xp=xy//self.obj2.dimU
#	yp=xy%self.obj2.dimV

	xp=xy//self.obj2.dimV
	yp=xy%self.obj2.dimV


	# geschwindkeit anpassen -- kraft am ort x,y,z addieren

#	print "vor ",self.pvs[xp,yp]
	self.pvs[xp,yp] += force(x,y,z,self.pvs[xp,yp],mytime)
	print (ix,xy, xp,yp,force(x,y,z,self.pvs[xp,yp],mytime))
#	print "nach ",self.pvs[xp,yp]

	tt=self.pvs[xp,yp]

	(dx,dy,dz) =damper(x,y,z,self.pvs[xp,yp],mytime)
	self.pvs[xp,yp]  *= damper(x,y,z,self.pvs[xp,yp],mytime)

	xn,yn,zn=x+tt[0],y+tt[1],z+tt[2]

	ddx,ddy,ddz=self.obj2.damperWall.x,self.obj2.damperWall.y,self.obj2.damperWall.z

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


	elif self.obj2.boundMode=='Bound Cylinder':

		r=40
		r=max(self.xmax,self.ymax)
		
		if xn**2+yn**2>r**2:
			try:
				(x2,y2)=lineCircleCommon(x,y,xn,yn,r)
				try:
					(x2,y2)=mirrorCircle(x,y,x2,y2)
				except:
					sayexc("")

				xn,yn=x2,y2

				self.pvs[xp,yp][0]  = -0.5*xn
				self.pvs[xp,yp][1]  = -0.5*yn


			except:
				pass

		if zn<self.zmin:
			zn=self.zmin -ddz*(zn-self.zmin)
			self.pvs[xp,yp][2]  *= -1 


	elif self.obj2.boundMode=='no Bounds':
		pass
	else:
		sayErr("nont implemented mode" + self.obj2.boundMode)

	rr=1
	rr=self.obj2.noise
	if zn <-5:
		xn,yn,zn=xn+rr*(0.5-random.random()),yn+rr*(0.5-random.random()),zn+rr*(0.5-random.random())
	
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
			self.ptslix[y*self.obj2.dimU+x]=[self.obj2.lengthStartCloud*(x-0.5*self.obj2.dimU)/self.obj2.dimU,
					self.obj2.widthStartCloud*(y-0.5*self.obj2.dimV)/self.obj2.dimV,0]


def createStartPtsCircle(self):
	''' create the starting cloud filled circle/cone '''
	for x in range(self.obj2.dimU):
		for y in range(self.obj2.dimV):
			self.ptslix[y*self.obj2.dimU+x]=[self.obj2.lengthStartCloud*(10+y)/(10+self.obj2.dimV)*np.cos(np.pi*2*x/self.obj2.dimU),
					self.obj2.widthStartCloud*(10+y)/(10+self.obj2.dimV)*np.sin(np.pi*2*x/self.obj2.dimU),0]


def createStartPtsV2(self):
	if self.obj2.startFace == "Circle":
		createStartPtsCircle(self)
	elif self.obj2.startFace == "Rectangle":
		createStartPtsSquare(self)

	for x in range(self.obj2.dimU):
		for y in range(self.obj2.dimV):
			[xn,yn,zn]=self.ptslix[y*self.obj2.dimU+x]
			if self.obj2.boundMode=='Bound Box':
				if xn>self.xmax or yn>self.ymax or xn<self.xmin or yn<self.ymin:
					self.ptslix[y*self.obj2.dimU+x]=[0,0,0]
			if self.obj2.boundMode=='Bound Cylinder':
				if xn>self.xmax or yn>self.ymax or xn<self.xmin or yn<self.ymin:
					self.ptslix[y*self.obj2.dimU+x]=[0,0,0]



def createStepPtsV2(self,i):
	velo(self,self.ptsl[i],i)



def createStepFC(self,i):
	objs=pclgroup()
	(la,lb)=self.ptsl[i].shape
#	pts=[tuple(self.ptslix[self.ptsl[i][a][b]]) for a in range(la) for b in range(lb)]

	pts=[]
	for a in range(la):
		for b in range(lb):
			t=tuple(self.ptslix[self.ptsl[i][a][b]])
			if np.isnan(t[0]) or np.isnan(t[1]) or np.isnan(t[2]):
				print "found error ", t
				print (a,b)
				
				pass
			else:
				pts.append(t)

	pcl=Points.Points(pts)
	Points.show(pcl)

	App.activeDocument().recompute()
	if i%25==0: Gui.SendMsgToActiveView("ViewFit")

	obj=App.ActiveDocument.ActiveObject
	obj.ViewObject.ShapeColor=(random.random(),random.random(),random.random())


	if len(objs.OutList)==0:
		obj.Placement=self.obj2.startPosition
	else:
		#movePosition=FreeCAD.Placement()
		#movePosition.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),10)
		movePosition=self.obj2.deltaPosition
		obj.Placement=objs.OutList[-1].Placement.multiply(movePosition)


	objs.addObject(obj)

	return obj




def animateIntervall(self,pb=None,start=0,ende=None,objs=None):
	Gui.ActiveDocument.ActiveView.setAnimationEnabled(False)
	
	if objs==None: 
		objs=pclgroup().OutList
	if ende==None: ende=len(objs)+ self.obj2.count4Slides
	if start+1<>ende and pb == None: 	pb=createProgressBar("animation ..")

	for u in objs: u.ViewObject.hide()

	k=3
	kk=10
	kkk=30
#	obj.addProperty("App::PropertyInteger","count4Slides","Base","").
#	kkk=self.obj2.count4Slides=14
#	obj.addProperty("App::PropertyInteger","color4Slides","Base","").
#	c4=self.obj2.color4Slides


	for i in range(start,ende):


		for u in objs: u.ViewObject.hide()


	for i0 in range(start,ende):
		# print "i0:",i0
		if pb<>None: pb.pb.setValue(i0*100/(ende-start-1))
		
		period=self.obj2.period
		if period<1: period=10000

		for u in objs: u.ViewObject.hide()


		for i in range(i0,0,-period):
			try:
				
			#	objs[i-kkk].ViewObject.hide()
				for j in range(self.obj2.count4Slides):
					if i-j>=0:
						objs[i-j].ViewObject.show()
						objs[i-j].ViewObject.ShapeColor=(.0,1.0,1.0)
						objs[i-j].ViewObject.ShapeColor=self.obj2.color4Slides
			except: pass

			try:
				for j in range(self.obj2.count3Slides):
					objs[i-j].ViewObject.ShapeColor=self.obj2.color3Slides
			except: pass

			try:
				for j in range(self.obj2.count2Slides):
					objs[i-j].ViewObject.ShapeColor=self.obj2.color2Slides
			except: pass
			try:
				objs[i].ViewObject.ShapeColor=self.obj2.colorSlides
				objs[i].ViewObject.show()
			except:
				pass
#			App.activeDocument().recompute()
#			Gui.updateGui()


		App.activeDocument().recompute()
		Gui.updateGui()
		time.sleep(self.obj2.sleep)
	if pb<>None: pb.hide()
		#objs[i].ViewObject.hide()


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
	obj.addProperty("App::PropertyFloat","time","Animation","")
	obj.addProperty("App::PropertyFloat","sleep","Animation","").sleep=0.0

	obj.addProperty("App::PropertyInteger","countSlices","Animation","").countSlices=20
	obj.addProperty("App::PropertyInteger","period","Animation","")


	obj.addProperty("App::PropertyInteger","dimU","Layout","").dimU=50
	obj.addProperty("App::PropertyInteger","dimV","Layout","").dimV=100

	obj.addProperty("App::PropertyLink","boundBox","Bounds","")
	obj.addProperty("App::PropertyEnumeration","boundMode","Bounds","")
	obj.boundMode=['no Bounds','Bound Box','Bound Cylinder','Bound Sphere']

	obj.addProperty("App::PropertyEnumeration","startFace","Layout","")
	obj.startFace=['Circle','Rectangle']
	
	obj.addProperty("App::PropertyPlacement","startPosition","Clouds","")
	obj.addProperty("App::PropertyPlacement","deltaPosition","Clouds","")
	# obj.deltaPosition.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-5)
	
	obj.addProperty("App::PropertyInteger","count2Slides","Clouds","").count2Slides=2
	obj.addProperty("App::PropertyInteger","count3Slides","Clouds","").count3Slides=6
	obj.addProperty("App::PropertyInteger","count4Slides","Clouds","").count4Slides=14
	obj.addProperty("App::PropertyColor","colorSlides","Clouds","").colorSlides=(1.0,0.0,0.0)
	obj.addProperty("App::PropertyColor","color2Slides","Clouds","").color2Slides=(1.0,1.0,0.0)
	obj.addProperty("App::PropertyColor","color3Slides","Clouds","").color3Slides=(1.0,.7,0.0)
	obj.addProperty("App::PropertyColor","color4Slides","Clouds","").color4Slides=(.0,1.0,1.0)

	obj.addProperty("App::PropertyVector","damperWall","Clouds","")
	obj.damperWall=FreeCAD.Vector(0.8,0.8,0.01)

	obj.addProperty("App::PropertyFloat","lengthStartCloud","Layout","").lengthStartCloud=100
	obj.addProperty("App::PropertyFloat","widthStartCloud","Layout","").widthStartCloud=100
	
	obj.addProperty("App::PropertyString","methodForce","Layout","").methodForce="myforce"
	obj.addProperty("App::PropertyString","methodDamper","Layout","").methodDamper="mydamper"

	#rr=1
	#rr=self.obj2.noise
	obj.addProperty("App::PropertyInteger","noise","Layout","").noise=5


	# obj.startPosition.Base=FreeCAD.Vector(50,10,-30)

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
		for u in objs: 
			u.ViewObject.hide()
			u.ViewObject.ShapeColor=(1.0,0.0,0.0)
		i=int(round(time*(len(objs)-1)))
		print i
		try:objs[i].ViewObject.show()
		except: pass


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
		animateIntervall(self,None,value,value+1)
		return
		
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
		bt.clicked.connect(lambda:animateIntervall(self))

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
		print "bounds ",bb
		self.xmax=bb.XMax
		self.ymax=bb.YMax
		self.zmax=bb.ZMax
		self.xmin=bb.XMin
		self.ymin=bb.YMin
		self.zmin=bb.ZMin

		createStartPtsV2(self)


#		self.obj2.forceMethod="myforce"
		reload(flowlib)
		force=eval("flowlib."+self.obj2.methodForce)
		self.force=force
		
		damper=eval("flowlib."+self.obj2.methodDamper)
		self.damper=damper


		for i in range(anz-1): 
			createStepPtsV2(self,i)
			pb.pb.setValue(i*100/(anz-2))

		createFCOs(self,anz,1)

		showAll()
		Gui.SendMsgToActiveView("ViewFit")
		hideAll()

		pb.hide()
		animateIntervall(self)





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
	App.ActiveDocument.ActiveObject.Height=800
	App.ActiveDocument.ActiveObject.Radius=40
	App.ActiveDocument.ActiveObject.ViewObject.Transparency=70
	App.ActiveDocument.ActiveObject.Placement.Base=App.Vector(-0,-0,-800)
	App.ActiveDocument.ActiveObject.ViewObject.Selectable = False
	App.ActiveDocument.ActiveObject.ViewObject.hide()

	b=App.ActiveDocument.addObject("Part::Box","Box")
	b.Length=400
	b.Width=500
	b.Height=8000
	b.Placement.Base=App.Vector(-200,-250,-8000)
	b.ViewObject.Transparency=70
	b.ViewObject.Selectable = False
	b.ViewObject.hide()

	Gui.activeDocument().activeView().viewAxonometric()
	App.activeDocument().recompute()

	f=createFlow()
	# f.startPosition.Base=FreeCAD.Vector(50,10,-30)

	f.boundMode='Bound Box'
	f.boundMode='Bound Cylinder'

	f.dimU=12
	f.dimV=3
	f.period=40
	# f.deltaPosition.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0.2,1),-5)
	#f.deltaPosition.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0.3,1),-5)
	#f.deltaPosition.Base=FreeCAD.Vector(10,5,20)
	try:f.boundBox=App.ActiveDocument.Box
	except: pass

	Gui.SendMsgToActiveView("ViewFit")
	f.countSlices=400
	f.count2Slides=3
	f.count3Slides=6
	f.count4Slides=20

	f.sleep=0.0
	f.noise=0
	
	#f.startFace='Rectangle'
	f.lengthStartCloud=100
	f.widthStartCloud=100

	f.methodDamper='nodamper'
	f.methodForce='simpleforce'
	f.Proxy.main()


# run()
