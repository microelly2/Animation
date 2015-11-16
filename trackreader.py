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

def interpol2(filename):
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
		print llf
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
	import matplotlib.pyplot as plt

	fx = interp1d(tv, xv, )
	fy = interp1d(tv, yv, )
	fz = interp1d(tv, zv, )
	frx = interp1d(tv, rx,)
	fry = interp1d(tv, ry, )
	frz = interp1d(tv, rz, )
	fra = interp1d(tv, ra, )

	xnew = np.linspace(0, 1, num=101, endpoint=True)
	try:
		plt.plot(tv, xv, 'o',tv,yv,'+',tv,zv,'*')
		plt.plot( xnew, fx(xnew), '-', xnew, fy(xnew), '--',xnew, fz(xnew), '.-', )
		plt.legend(['xdata', 'x','y','z'], loc='best')
		plt.title('Placement Interpolation Data')
		plt.xlabel('time relative')
		plt.ylabel('Placement Base')
		plt.savefig(filename +'.png')
		plt.show()
		#import ImageGui
		#ImageGui.open(filename +'.png')
	except:
		pass

	# export data
	fout = open(filename + "_post.txt",'w')
	for t in xnew:
		try:
			l=' '.join(str(k) for k in [t,fx(t),fy(t),fz(t),frx(t),fry(t),frz(t),fra(t)])
			fout.write(l+'\n')
		except:
			pass
	fout.close()


def create(name,target,filename):
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

class _TrackReader():

	def __init__(self,obj):
		obj.Proxy = self
		self.obj2 = obj 
		self.Lock=False
		self.Changed=False
		self.path={}
		self.loadtrack()

	def loadtrack(self):
		interpol2(self.obj2.filename)
		for line in open(self.obj2.filename + "_post.txt", "r"):
			line=line.rstrip('\r\n')
			ll= line.split(' ')
			self.path[float(ll[0])]=FreeCAD.Placement(
				FreeCAD.Vector(float(ll[1]),float(ll[2]),float(ll[3])),
				FreeCAD.Vector(float(ll[4]),float(ll[5]),float(ll[6])),
				float(ll[7])*180/math.pi)
		print self.path

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

class _ViewProviderTrackReader(object):
 
	def getIcon(self):
		return __dir__ +'/icons/sun.png'

	def __init__(self,vobj):
		self.Object = vobj.Object
		vobj.Proxy = self

	def attach(self,vobj):
		say("attach " + str(vobj.Object.Label))
		self.Object = vobj.Object
		self.obj2=self.Object
		self.Object.Proxy.Lock=False
		self.Object.Proxy.Changed=False
		return

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def setEdit(self,vobj,mode=0):
		s=TRWidget(self)
		self.dialog=s
		self.dialog.show()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		self.setEdit(vobj,1)

	def setupContextMenu(self, obj, menu):
		action = menu.addAction("About VertexPlugger")
		action.triggered.connect(self.showVersion)
		action = menu.addAction("Track Reader ...")
		action.triggered.connect(self.edit)

	def edit(self):
		self.dialog=TRWidget(self)
		self.dialog.show()

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About ", "Animation Track Reader Node\n2015 microelly\nVersion " + __vers__ )

	def loadtrack(self):
		self.obj2.Proxy.loadtrack()

class TRWidget(QtGui.QWidget):
	def __init__(self, obj,*args):
		QtGui.QWidget.__init__(self, *args)
		obj.widget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.vollabel = QtGui.QLabel(obj.Object.Label)

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.setText("close")
		self.pushButton02.clicked.connect(self.hide)

		self.pushButton01 = QtGui.QPushButton()
		self.pushButton01.setText("Reload data")
		self.pushButton01.clicked.connect(obj.loadtrack)

		dial = QDial()
		dial.setNotchesVisible(True)
		self.dial=dial
		dial.setMaximum(100)
		dial.valueChanged.connect(obj.dreher);

		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 0)
		layout.addWidget(self.pushButton01, 1,0,)
		layout.addWidget(self.pushButton02, 4, 0,)
		layout.addWidget(dial,3,0)

		self.setLayout(layout)
		self.setWindowTitle(obj.Object.target.Label)


if __name__ == "__main__":

	box=App.ActiveDocument.Bax
	t=create("TrackReader Bax",box,"/tmp/Bax_tracker")


	box=App.ActiveDocument.Circler
	t=create("TrackReader Circler",box,"/tmp/Circler_tracker")
