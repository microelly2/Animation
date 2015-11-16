# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- animation workbench tracker
#--
#-- microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 

__vers__='0.2 16.11.2015'

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

def create(name,src=None,filename="/tmp/tracker_out.txt"):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyString","filename","Base","")
	obj.filename=filename
	obj.addProperty("App::PropertyLink","src","Base","")
	obj.src=src
	obj.addProperty("App::PropertyFloat","time","Base","")

	_Tracker(obj)
	_ViewProviderTracker(obj.ViewObject)
	return obj

class _Tracker():
	''' track the time/placement of src to filename '''

	def __init__(self,obj):
		obj.Proxy = self
		self.obj2 = obj 
		self.Lock=False
		self.Changed=False
		self.path=[]

	def execute(self,obj):
		if self.obj2.ViewObject.Visibility == False:
			return
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

	def update(self):
#		say(self.obj2.src.Placement)
		# reset if time == 0
		if (self.obj2.src.time==0):
			f = open(self.obj2.filename,'w')
			self.path=[]
		else:
			f = open(self.obj2.filename,'a')
		f.write("# " + str(self.obj2.src.time) +" " +str(self.obj2.src.Placement)+'\n') # python will convert \n to os.linesep
		b=self.obj2.src.Placement.Base
		r=self.obj2.src.Placement.Rotation.Axis
		a=self.obj2.src.Placement.Rotation.Angle
		l=' '.join(str(k) for k in [self.obj2.src.time,b.x,b.y,b.z,r.x,r.y,r.z,a])
		f.write(l +"\n")
		f.close()
		self.path.append(self.obj2.src.Placement.Base)

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


class _ViewProviderTracker(object):
 
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
		self.dialog=TWidget(self)
		self.dialog.show()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		self.setEdit(vobj,1)

	def setupContextMenu(self, obj, menu):
		action = menu.addAction("About Tracker")
		action.triggered.connect(self.showVersion)
		action = menu.addAction("Dialog ...")
		action.triggered.connect(self.edit)

	def edit(self):
		self.dialog=TWidget(self)
		self.dialog.show()

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About ", "Animation Tracker Node\n2015 microelly\nVersion " + __vers__ )

	def showpath(self):
		''' path as Part.polygon '''
		FreeCAD.s=self
		points=self.Object.Proxy.path
		for p in self.Object.Proxy.path:
			say(str(p))
		pp=Part.makePolygon(points)
		Part.show(pp)
		FreeCAD.ActiveDocument.recompute()


class TWidget(QtGui.QWidget):
	'''contextmenu for tracker'''

	def __init__(self, obj,*args):
		QtGui.QWidget.__init__(self, *args)
		obj.widget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

		self.vollabel = QtGui.QLabel(obj.Object.Label)

		self.pushButton01 = QtGui.QPushButton()
		self.pushButton01.setText("path")
		self.pushButton01.clicked.connect(obj.showpath)

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.setText("close")
		self.pushButton02.clicked.connect(self.hide)

		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 0)
		layout.addWidget(self.pushButton01, 1,4)
		layout.addWidget(self.pushButton02, 2,4)

		self.setLayout(layout)
		self.setWindowTitle(obj.Object.src.Label)


if __name__ == "__main__":

	ax= App.ActiveDocument.Anim_Circler
	t=create("Tracker "+ax.Label,ax, "/tmp/Circler_tracker_out.txt")
	bx= App.ActiveDocument.Anim_Bax
	t=create("Tracker "+bx.Label,bx,"/tmp/Bax_tracker_out.txt")


