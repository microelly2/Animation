# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench trackreader
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
import math
import numpy as np
App,Gui=FreeCAD,FreeCADGui

import Draft,Part


import Animation

__vers__='0.1'


import math,os

import FreeCAD, Animation, PySide
from Animation import say,sayErr,sayexc
from  EditWidget import EditWidget

__vers__= '0.1'
__dir__ = os.path.dirname(__file__)	


import FreeCAD,os,time,sys,traceback

def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))

def interpol2(filename,show=True):
	''' interpolate data from filename_out.txt to filename_post.txt'''

	filename2=filename + "_out.txt"
	tv=[]
	xv=[]
	yv=[]
	zv=[]

	rx=[]
	ry=[]
	rz=[]
	ra=[]

	for line in open(filename + "_out.txt", "r"):
		line=line.rstrip('\r\n')
		ll= line.split(' ')
		if ll[0] == '#': 
			continue
		llf=[]
		for z in ll:
			llf.append(float(z))

		tv.append(llf[0])
		xv.append(llf[1])
		yv.append(llf[2])
		zv.append(llf[3])
		
		rx.append(llf[4])
		ry.append(llf[5])
		rz.append(llf[6])
		ra.append(llf[7])

	# interpolate
	import numpy as np
	import scipy
	from scipy.interpolate import interp1d
	#import matplotlib.pyplot as plt

	fx = interp1d(tv, xv, )
	fy = interp1d(tv, yv, )
	fz = interp1d(tv, zv, )
	frx = interp1d(tv, rx,)
	fry = interp1d(tv, ry, )
	frz = interp1d(tv, rz, )
	fra = interp1d(tv, ra, )

	xnew = np.linspace(0, 0.99, num=100, endpoint=True)
	#try:
	if show:
		plt.plot(tv, xv, 'o',tv,yv,'+',tv,zv,'*')
		plt.plot( xnew, fx(xnew), '-', xnew, fy(xnew), '--',xnew, fz(xnew), '.-', )
#		plt.legend(['aaa','x','y','z'], loc='best')
		plt.title('Placement Interpolation Data')
		plt.xlabel('time relative')
		plt.ylabel('Placement Base')
		plt.savefig(filename +'.png')
		# plt.show()
		import ImageGui
		ImageGui.open(filename +'.png')
	#except:
	#	pass

	# export data
	fout = open(filename + "_post.txt",'w')
	for t in xnew:
		try:
			l=' '.join(str(k) for k in [t,fx(t),fy(t),fz(t),frx(t),fry(t),frz(t),fra(t)])
			fout.write(l+'\n')
		except:
			pass
	fout.close()
	#return [fx,fy,fz]
	


def createTrackReader(name,target,filename):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	obj.addProperty("App::PropertyLink","target","Base","")
	obj.target=target
	obj.addProperty("App::PropertyString","filename","Base","")
	obj.filename=filename
	obj.addProperty("App::PropertyFloat","time","Base","")
	obj.time=0.0
	obj.addProperty("App::PropertyPlacement","Placement","Results","")
	obj.Placement=FreeCAD.Placement()

	_TrackReader(obj)
	_ViewProviderTrackReader(obj.ViewObject)
	return obj

class _TrackReader(Animation._Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.obj2 = obj 
		self.Lock=False
		self.Changed=False
		self.path={}
		self.loadtrack()



	def loadtrack(self):
		interpol2(self.obj2.filename,False)
		for line in open(self.obj2.filename + "_post.txt", "r"):
			line=line.rstrip('\r\n')
			ll= line.split(' ')
			self.path[float(ll[0])]=FreeCAD.Placement(
				FreeCAD.Vector(float(ll[1]),float(ll[2]),float(ll[3])),
				FreeCAD.Vector(float(ll[4]),float(ll[5]),float(ll[6])),
				float(ll[7])*180/math.pi)
		print(self.path)

	def showtrack(self):
		interpol2(self.obj2.filename,True)
		for line in open(self.obj2.filename + "_post.txt", "r"):
			line=line.rstrip('\r\n')
			ll= line.split(' ')
			self.path[float(ll[0])]=FreeCAD.Placement(
				FreeCAD.Vector(float(ll[1]),float(ll[2]),float(ll[3])),
				FreeCAD.Vector(float(ll[4]),float(ll[5]),float(ll[6])),
				float(ll[7])*180/math.pi)
		print(self.path)


	def showtrack(self):
		interpol2(self.obj2.filename,True)
		for line in open(self.obj2.filename + "_post.txt", "r"):
			line=line.rstrip('\r\n')
			ll= line.split(' ')
			self.path[float(ll[0])]=FreeCAD.Placement(
				FreeCAD.Vector(float(ll[1]),float(ll[2]),float(ll[3])),
				FreeCAD.Vector(float(ll[4]),float(ll[5]),float(ll[6])),
				float(ll[7])*180/math.pi)
		print(self.path)


	def execute(self,obj):

		if self.Changed:
			say("self changed")
			self.Changed=False
			return
		if not self.Lock:
			self.obj2=obj
			self.Lock=True
			try:
				self.update()
			except:
				sayexc('update')
			self.Lock=False

#
# main execution detail
#
	def update(self):
		say("update ")
		import math
		time=self.obj2.time
		say(str(time))
		pl=self.path[time]
		self.obj2.target.Placement=pl
		self.obj2.Placement=pl

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def onChanged(self,obj,prop):
		pass

	def onBeforeChange(self,obj,prop):
		pass
	
	def initialize(self):
		pass

	def step(self,now):
			self.obj2.time=float(now)/100

class _ViewProviderTrackReader(Animation._ViewProviderActor):
 
	def getIcon(self):
		return __dir__ +'/icons/icon3.svg'

	def attach(self,vobj):
		say("attach " + str(vobj.Object.Label))
		self.emenu=[["Reload Track",self.loadtrack],["Show Track",self.showtrack]]
		self.cmenu=[]
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		return

	def setupContextMenu(self, obj, menu):
		action = menu.addAction("About ")
		action.triggered.connect(self.showVersion)
		action = menu.addAction("Track Reader ...")
		action.triggered.connect(self.edit)

	def edit(self):
		self.dialog=EditWidget(self,self.emenu)
		self.dialog.show()

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About ", "Animation Track Reader Node\n2015 microelly\nVersion " + __vers__ )

	def loadtrack(self):
		self.obj2.Proxy.loadtrack()

	def showtrack(self):
		self.obj2.Proxy.showtrack()

	def dialer(self):
		''' shows the position at the dialer time'''
		self.obj2.time=float(self.widget.dial.value())/100
		say("dialer self time:" + str(self.obj2.time))
		try:
			say(self.obj2.Proxy.path[round(self.obj2.time,2)])
			self.obj2.target.Placement=self.obj2.Proxy.path[round(self.obj2.time,2)]
		except:
			pass
		FreeCAD.ActiveDocument.recompute()




class _Function(Animation._Actor):

	def __init__(self,obj):
		obj.Proxy = self
		self.obj2 = obj 
		self.Lock=False
		self.Changed=False
		self.path={}
		self.loadtrack()


	def loadtrack(self):
		
		# interpolate
		import numpy as np
		import scipy
		from scipy.interpolate import interp1d
		#import matplotlib.pyplot as plt

		wire=self.obj2.source.Shape



		if self.obj2.target==None:
			self.obj2.target=Draft.makeCircle(5)
			self.obj2.target.Label ="anim target for "+ self.obj2.source.Label

		# hier andere modi einbauen z. B. Endpunkte der edges #+#
		
		if self.obj2.usePoints:
			w=wire
			pts=[v.Point for v in w.Vertexes]
		else:
			pts=wire.discretize(self.obj2.count)

		tx=[p.x for p in pts]
		ty=[p.y for p in pts]
		tz=[p.z for p in pts]
		self.obj2.xlist=tx
		self.obj2.ylist=ty
		self.obj2.zlist=tz
		xmin=min(tx)
		tx=(np.array(tx)-xmin)
		xmax=max(tx)
		tx /= xmax

#		zmin=min(tz)
#		tz=(np.array(tz)-zmin)
#		zmax=max(tz)
#		tz /= zmax

		# siehe https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.interp1d.html
		
		
		fx = interp1d(tx,ty,kind=self.obj2.kindInterpolation)
		fz = interp1d(tx,tz,kind=self.obj2.kindInterpolation)
		
		self.fx=fx
		self.xmin=xmin
		self.xmax=xmax
		ptsa=[FreeCAD.Vector((0.01*i*(xmax))+xmin,self.obj2.a*fx(0.01*i)+self.obj2.b,
					self.obj2.a*fz(0.01*i)+self.obj2.b,) for i in range(101)]
		#Draft.makeWire(ptsa)
		pol=Part.makePolygon(ptsa)
		try: self.k1.Shape=pol
		except: 
			Part.show(pol)
			self.k1=App.ActiveDocument.ActiveObject
			self.k1.Label="cartesian Map for "+ self.obj2.source.Label
		

		# polare Darstellung
		ptsa=[FreeCAD.Vector(np.cos(np.pi*i/180),np.sin(np.pi*i/180),0)*(self.obj2.a*fx(1.0/360*i)+self.obj2.b) for i in range(361)]
		#Draft.makeWire(ptsa)
		pol=Part.makePolygon(ptsa)
		try: self.k2.Shape=pol
		except: 
			Part.show(pol)
			self.k2=App.ActiveDocument.ActiveObject
			self.k2.Label="polar Map for "+ self.obj2.source.Label




	def execute(self,obj):

		if self.Changed:
			say("self changed")
			self.Changed=False
			return
		if not self.Lock:
			self.obj2=obj
			self.Lock=True
			try:
				self.update()
			except:
				sayexc('update')
			self.Lock=False

	def onChanged(self,obj,prop):
		if prop in ['source','count','a','b']:
			self.loadtrack()
		if prop in ['time','count']:
			self.update()

#
# main execution detail
#
	def update(self):
		say("update ")
		import math
		time=self.obj2.time/100
		say(str(time))
		if self.obj2.mode=='cartesian':
			pl=FreeCAD.Vector((time*self.xmax)+self.xmin,self.obj2.a*self.fx(time)+self.obj2.b)
		if self.obj2.mode=='polar':
			# pl=FreeCAD.Vector((time*self.xmax)+self.xmin,self.fx(time))
			pl=FreeCAD.Vector(np.cos(np.pi*time*2),np.sin(np.pi*time*2),0)*(self.obj2.a*self.fx(time)+self.obj2.b)
		if self.obj2.target != None:	
			self.obj2.target.Placement.Base=pl
			self.obj2.target.purgeTouched()
		#self.obj2.Placement=pl

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None



	def onBeforeChange(self,obj,prop):
		pass

	def initialize(self):
		pass

	def step(self,now):
			self.obj2.time=float(now)

class _ViewProviderFunction(Animation._ViewProviderActor):
 
	def getIcon(self):
		return __dir__ +'/icons/icon3.svg'

	def attach(self,vobj):
		say("attach " + str(vobj.Object.Label))
		self.emenu=[["Reload Track",self.loadtrack],["Show Track",self.showtrack]]
		self.cmenu=[]
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		return

	def setupContextMenu(self, obj, menu):
		action = menu.addAction("About ")
		action.triggered.connect(self.showVersion)
		action = menu.addAction("Update Graph ...")
		action.triggered.connect(self.Object.Proxy.loadtrack)

	def edit(self):
		self.dialog=EditWidget(self,self.emenu)
		self.dialog.show()

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About ", "Animation Track Reader Node\n2015 microelly\nVersion " + __vers__ )

	def loadtrack(self):
		self.obj2.Proxy.loadtrack()

	def showtrack(self):
		self.obj2.Proxy.showtrack()

	def dialer(self):
		''' shows the position at the dialer time'''
		self.obj2.time=float(self.widget.dial.value())/100
		say("dialer self time:" + str(self.obj2.time))
		try:
			say(self.obj2.Proxy.path[round(self.obj2.time,2)])
			self.obj2.target.Placement=self.obj2.Proxy.path[round(self.obj2.time,2)]
		except:
			pass
		FreeCAD.ActiveDocument.recompute()


def runTA():
	print("I'm TA") 
	name="MyFunction"


#def createTrackReader(name,target,filename):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)

	target=None
	obj.addProperty("App::PropertyLink","target","Base","")
	obj.addProperty("App::PropertyLink","source","Base","")
	
	#obj.source=App.ActiveDocument.Sketch
	obj.source=Gui.Selection.getSelection()[0]
#	obj.addProperty("App::PropertyLink","circle","Base","")
	obj.target=target
#	obj.addProperty("App::PropertyString","filename","Base","")
	#obj.filename=filename
	obj.addProperty("App::PropertyFloat","time","Base","")
	obj.time=0.0
	obj.addProperty("App::PropertyFloat","a","F=a*f+b","").a=1
	obj.addProperty("App::PropertyFloat","b","F=a*f+b","").b=0
	obj.addProperty("App::PropertyInteger","count","","").count=40
	
	obj.addProperty("App::PropertyPlacement","Placement","_comp","")
	obj.Placement=FreeCAD.Placement()
	obj.addProperty("App::PropertyEnumeration","mode","Base").mode=["cartesian","polar"]
	obj.addProperty("App::PropertyFloatList", "xlist", "_comp", "end")
	obj.addProperty("App::PropertyFloatList", "ylist", "_comp", "end")
	obj.addProperty("App::PropertyFloatList", "zlist", "_comp", "end")
	obj.addProperty("App::PropertyBool", "usePoints", "", "interpolate points").usePoints=True
	obj.addProperty("App::PropertyEnumeration","kindInterpolation","Base").kindInterpolation=['cubic','linear', 'nearest', 'zero', 'slinear', 'quadratic', ]
	


	_Function(obj)
	_ViewProviderFunction(obj.ViewObject)
	obj.Label="Interpolator for "+ obj.source.Label
	return obj
