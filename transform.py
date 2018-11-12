# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- Transform Node: Cascaded coordinate systems 
#--
#-- (c) microelly 2015
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD,PySide,os,FreeCADGui
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 

__vers__='0.2'


try:
	__dir__ = os.path.dirname(__file__)
	say(__dir__)
except:
	__dir__='/usr/lib/freecad/Mod/mylib'

def say(s):
	FreeCAD.Console.PrintMessage(str(s)+"\n")

def saye(s):
	FreeCAD.Console.PrintError(str(s)+"\n")


class TransformWidget(QtGui.QWidget):
	def __init__(self, obj,*args):
		QtGui.QWidget.__init__(self, *args)
		self.obj2=obj
		FreeCAD.obj2=obj
		self.vollabel = QtGui.QLabel(obj.Object.Label)

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.clicked.connect(self.on_pushButton02_clicked) 
		self.pushButton02.setText("close")

		self.listWidget = QListWidget() 
		for tn in self.obj2.Object._targets:
			n=tn.Label
			item = QListWidgetItem(n)
			self.listWidget.addItem(item)
		self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

		self.combo = QtGui.QComboBox(self)
		for i in FreeCAD.ActiveDocument.Objects:
			self.combo.addItem(str(i.Label)+ " ")

		self.pushButton03 = QtGui.QPushButton()
		self.pushButton03.clicked.connect(self.on_pushButton03_clicked) 
		self.pushButton03.setText("add target")
		
		self.pushButton04 = QtGui.QPushButton()
		self.pushButton04.clicked.connect(self.on_pushButton04_clicked) 
		self.pushButton04.setText("remove selected targets")
		
		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 0)
		
		layout.addWidget(self.pushButton02, 15, 0,1,4)
		layout.addWidget(self.listWidget, 3, 0,1,4)
		layout.addWidget(self.pushButton04, 4, 0,1,4)
		
		layout.addWidget(self.combo, 5, 0,1,4)
		layout.addWidget(self.pushButton03, 6, 0,1,4)

		self.setLayout(layout)
		self.setWindowTitle("Edit Coordinate System")

	def on_pushButton02_clicked(self):
		self.hide()

	def on_pushButton03_clicked(self):
		col=self.combo.currentText()
		it=QListWidgetItem(col)
		self.listWidget.addItem(it)
		itemcount =self.listWidget.count()
		newlist=[]
		targets=[]
		for i in range(itemcount):
			y=self.listWidget.item(i).text()
			y=y.strip()
			newlist.append(y)
			l=FreeCAD.ActiveDocument.getObjectsByLabel(y)
			targets.append(l[0])
		self.obj2.Object._targets=targets

	def on_pushButton04_clicked(self):
		seli=[]
		for sel in self.listWidget.selectedItems():
			seli.append(sel.text())
		itemcount =self.listWidget.count()
		newlist=[]
		for i in range(itemcount):
			try:
				y=self.listWidget.item(i).text()
				y=y.strip()
				seli.index(y)
			except:
#				say("nicht gefunden")
				newlist.append(y)
		self.listWidget.clear()
		targets=[]
		for y in newlist:
			self.listWidget.addItem(y)
			l=FreeCAD.ActiveDocument.getObjectsByLabel(y)
			targets.append(l[0])
		self.obj2.Object._targets=targets




#---------------------------------------------
def createTransform(name='MyTransform', targets=[],src=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	_Transform(obj)
	_ViewProviderTransform(obj.ViewObject)
	
	c3=obj
	c3.addProperty("App::PropertyStringList","execute3","2 MyCTL","")
	c3.execute3=['say("hallo")']
	c3.Proxy.updater=True
	c3.addProperty("App::PropertyStringList","propliste","2 MyCTL","")
	c3.propliste=[]
	c3.addProperty("App::PropertyLinkList","_targets","2 MyCTL","")
	c3._targets=targets
	c3.addProperty("App::PropertyLink","src","2 MyCTL","")
	c3.src=src
	c3.addProperty("App::PropertyPlacement","plOld","2 MyCTL","")
	c3.plOld=FreeCAD.Placement()
	c3.addProperty("App::PropertyPlacement","Placement","Base","")
	if src:
		c3.Placement=src.Placement
	else:
		c3.Placement=FreeCAD.Placement()
	objlinks=[]
	liste=[]
	while objlinks.__len__() > 1: 
		key=objlinks.pop(0)
		val=objlinks.pop(0)
		say(key)
		say(val)
		c3.addProperty("App::PropertyLink",key,"3 MyParts","")
		s='c3.'+key+'=FreeCAD.ActiveDocument.getObject(val)'
		say(s)
		exec(s)
	propliste=[]
	while liste.__len__() > 1: 
		key=liste.pop(0)
		val=liste.pop(0)
		say(key)
		say(val)
		propliste.append(key)
		say(propliste)
		#say(val.__class__)
		if val.__class__ == int:
			c3.addProperty("App::PropertyInteger",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			exec(s)
		elif val.__class__ ==  str:
			c3.addProperty("App::PropertyString",key,"1 MyProps","")
			s='c3.'+key + '="' + val + '"'
			exec(s)
		elif val.__class__ ==  float:
			c3.addProperty("App::PropertyFloat",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			#say(s)
			exec(s)
		else:
			say("nicht bearbeiteit")
			say(val.__class__)
	c3.propliste=propliste
	return obj

class _Transform():
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Transform"
		self.obj2 = obj 
		self.Lock=False
	def execute(self,obj):
		if not self.Lock:
			say("exec self=" +str(self) +' obj.Label= ' +str(obj.Label)) 
			say("set Lock ----- " +str(obj.Label))
			'''
			try:
				if not hasattr(self,"updater"):
					say("erzeuge updater")
					self.updater=True
					
				if self.updater:
					self.updater=False
					say("updater true!")
					#return
					# hack deaktiviert 
				else:
					self.updater=True
			except:
				pass
			'''
			self.obj2=obj
			self.Lock=True
			qalt=self.obj2.plOld
			source=self.obj2.src
			if source:
				qneu=source.Placement
			else:
				qneu=self.obj2.Placement
			qai=qalt.inverse()
			self.obj2.plOld=qneu
			for target in self.obj2._targets:
				palt=target.Placement
				t=qai.multiply(palt)
				pneu=qneu.multiply(t) 
				target.Placement=pneu
				try:
					target.Proxy.execute(target)
				except:
					pass
			self.Lock=False
			say("unset Lock +++ " +str(self.obj2.Label))


	def __getstate__(self):
		say("getstate " + str(self))
		return None

	def __setstate__(self,state):
		say("setstate " + str(self) + str(state))
		return None
		
	def addComponent(self,name='object'):
		say(name)
		self.obj2.addProperty("App::PropertyLink",name,"3 MyParts","")
	def addProperty(self,key,val):
		say(key)
		#propliste.append(key)
		#say(propliste)
		say(val.__class__)
		c3=self.obj2
		if val.__class__ == int:
			c3.addProperty("App::PropertyInteger",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			exec(s)
		elif val.__class__ ==  str:
			c3.addProperty("App::PropertyString",key,"1 MyProps","")
			s='c3.'+key + '="' + val + '"'
			exec(s)
		elif val.__class__ ==  float:
			c3.addProperty("App::PropertyFloat",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			#say(s)
			exec(s)
		else:
			say("nicht bearbeiteit")
			say(val.__class__)
		say(c3.propliste)
		t=c3.propliste
		t.append(key)
		c3.propliste=t
		say(c3.propliste)

	def onChanged(self,obj,prop):
		if prop=="Placement":
			if str(self.beforeP) != str(obj.Placement):
				say("Placement changed ...")
				say(self.beforeP)
				say(obj.Placement)

	def onBeforeChange(self,obj,prop):
		if prop=="Placement":
			self.beforeP=FreeCAD.Placement(obj.Placement)

class _ViewProviderTransform(object):
 
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
		#self.dialog=TransformWidget(self)
		#FreeCAD.t=self
		if not hasattr(self.Object,"Lock"):
				self.Object.Proxy.Lock=False
				say("lock gesetzt")
		FreeCAD.ty=self
		FreeCAD.tv=vobj
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
		s=TransformWidget(self)
		self.dialog=s
		self.dialog.show()
		say("set Edit")
		#s.show()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		self.setEdit(vobj)

	def setupContextMenu(self, obj, menu):
		action = menu.addAction("About Transform")
		action.triggered.connect(self.showVersion)

		action = menu.addAction("Edit ...")
		action.triggered.connect(self.edit)

	def edit(self):
		self.dialog=TransformWidget(self)
		self.dialog.show()
		

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About Transform", "Transform Node\n2015 microelly\nVersion " + __vers__ +"\nstill very alpha")



#-----------------------

class HingeWidget(QtGui.QWidget):
	def __init__(self, obj,*args):
		QtGui.QWidget.__init__(self, *args)

		self.Object=obj
		layout = QtGui.QGridLayout()
#		self.vollabel = QtGui.QLabel(obj.Object.Label)
#		layout.addWidget(self.vollabel, 0, 0)
		self.dial = QtGui.QDial()
		self.dial.setMaximum(360)
		self.dial.setSingleStep(1)
		self.dial.setNotchesVisible(True)
		self.dial.valueChanged.connect(self.paramValueCanged);
		layout.addWidget(self.dial, 10, 0,1,4)
		self.setLayout(layout)
		self.setWindowTitle("Hinge Joint")

	def paramValueCanged(self):
		say("Angel ValueCanged")
		# say(self.dial.value())
		v=self.dial.value()
		say(v)
		'''
		say(self.Object.Object.Placement.Rotation.Angle)
		say(self.Object.Object.Placement.Rotation.Axis)
		self.Object.Object.Placement.Rotation=FreeCAD.Rotation(self.Object.Object.axis,v)
		saye(self.Object.Object.Placement.Rotation.Angle)
		saye(self.Object.Object.Placement.Rotation.Axis)
		
		say(self.Object.Object.Placement)
		self.Object.Object.Proxy.execute(t)
		'''
		#---------------------------------------------
		
		FreeCAD.tt=self
#		say(self.Object.Object.Placement)
		if True:
			qalt=self.Object.Object.plOld
			qai=qalt.inverse()
#			say(qai)
			vt=self.Object.Object.axisAngle
			say("vt=")
			say(vt)
			qt=FreeCAD.Placement()
			qt.Rotation=FreeCAD.Rotation(self.Object.Object.axis,vt)
#			say(qt)
			vti=qt.inverse()
			# rest=vti.multiply(qalt)
			rest=qalt.multiply(vti)
			say("rest=")
			say(rest)
			qn=FreeCAD.Placement()
			#qn.Base=FreeCAD.Vector(self.Object.Object.direction).multiply(v)
			qn.Rotation=FreeCAD.Rotation(self.Object.Object.axis,v)
			say("neue pos einfach ... qn2=")
			qn2=FreeCAD.Placement(qn)
			rest2=FreeCAD.Placement(rest)
			say(qn2)
			
			say("qneu ... zz=")
			#FreeCAD.rest=rest
			#FreeCAD.qn=qn
			#zz=FreeCAD.rest.multiply(FreeCAD.qn)
			#say(zz)
			say("lokal berechnet:")
			zz=rest.multiply(qn)
			say(zz)
			
			self.Object.Object.axisAngle=v
			self.Object.Object.Placement=zz
			saye("fertig")
			FreeCAD.ActiveDocument.recompute()
		
		
		#----------------------------------------------
		FreeCAD.ActiveDocument.recompute()


class TelescopWidget(QtGui.QWidget):
	def __init__(self, obj,*args):
		QtGui.QWidget.__init__(self, *args)
		self.Object=obj
		layout = QtGui.QGridLayout()
#		self.vollabel = QtGui.QLabel("Telescopic boom")
#		layout.addWidget(self.vollabel, 0, 0)
		self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		self.slider.setMaximum(100)
		self.slider.valueChanged.connect(self.paramValueCanged);
		layout.addWidget(self.slider, 12, 0,1,4)
		self.setLayout(layout)
		self.setWindowTitle("Telecopic Boom")

	def paramValueCanged(self):
		saye("ValueCanged")
		say(self.slider.value())
		v=self.slider.value()
		FreeCAD.tt=self
#		say(self.Object.Object.Placement)
		if True:
			qalt=self.Object.Object.plOld
			qai=qalt.inverse()
#			say(qai)
			vt=self.Object.Object.axisScale
#			say("vt=")
#			say(vt)
			qt=FreeCAD.Placement()
			qt.Base=FreeCAD.Vector(self.Object.Object.direction).multiply(vt)
#			say(qt)
			vti=qt.inverse()
			# rest=vti.multiply(qalt)
			rest=qalt.multiply(vti)
			say("rest=")
			say(rest)
			qn=FreeCAD.Placement()
			qn.Base=FreeCAD.Vector(self.Object.Object.direction).multiply(v)
			say("neue pos einfach ... qn2=")
			qn2=FreeCAD.Placement(qn)
			rest2=FreeCAD.Placement(rest)
			say(qn2)
			
			say("qneu ... zz=")
			#FreeCAD.rest=rest
			#FreeCAD.qn=qn
			#zz=FreeCAD.rest.multiply(FreeCAD.qn)
			#say(zz)
			say("lokal berechnet:")
			zz=rest.multiply(qn)
			say(zz)
			
			self.Object.Object.axisScale=v
			self.Object.Object.Placement=zz
			saye("fertig")
			FreeCAD.ActiveDocument.recompute()


class _ViewProviderHinge(_ViewProviderTransform):
	def setupContextMenu(self, obj, menu):
#		action = menu.addAction("About Transform ")
#		action.triggered.connect(self.showVersion)
		action = menu.addAction("Edit ... ")
		action.triggered.connect(self.edit)
		action = menu.addAction("Config ... ")
		action.triggered.connect(self.config)

	def config(self):
		self.dialog=HingeWidget(self)
		# self.dialog.show()
		
		mw = FreeCADGui.getMainWindow()
		dock = QtGui.QDockWidget(self.Object.Label, mw)
		dock.setStyleSheet("background-color:lightblue;color:blue;")
		mw.centralWidget = QtGui.QWidget(dock)
		mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
		dock.setWidget(self.dialog)
		say("widget set")


	def doubleClicked(self,vobj):
		self.setEdit(vobj)

	def setEdit(self,vobj,mode=0):
		self.config()
		saye("edit ..")
		return True


class _ViewProviderTelescope(_ViewProviderTransform):

	def getIcon(self):
		return __dir__ +'/icons/mars.png'
 
	def setupContextMenu(self, obj, menu):
#		action = menu.addAction("About Transform B")
#		action.triggered.connect(self.showVersion)
		action = menu.addAction("Edit ... ")
		action.triggered.connect(self.edit)
		action = menu.addAction("Config ... ")
		action.triggered.connect(self.config)

	def config(self):
		self.dialog=TelescopWidget(self)
		#self.dialog.show()
		mw = FreeCADGui.getMainWindow()
		#dock = QtGui.QDockWidget("Mein Dock", mw)
		dock = QtGui.QDockWidget(self.Object.Label, mw)
		dock.setStyleSheet("background-color:yellow;color:brown;")
		mw.centralWidget = QtGui.QWidget(dock)
		mw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
		dock.setWidget(self.dialog)

	def doubleClicked(self,vobj):
		self.setEdit(vobj)

	def setEdit(self,vobj,mode=0):
		self.config()
		saye("edit ..")
		return True


def createHinge(name='MyHinge', targets=[],src=None):
	obj=createTransform(name, targets=[],src=None)
	obj.addProperty("App::PropertyVector","axis","2 MyCTL","")
	obj.axis=FreeCAD.Vector(0,0,1)
	obj.addProperty("App::PropertyFloat","axisAngle","2 MyCTL","")
	obj.axisAngle=0.0
	_ViewProviderHinge(obj.ViewObject)
	return obj

def createTelescope(name='MyTelescope', targets=[],src=None):
	obj=createTransform(name, targets=[],src=None)
	obj.addProperty("App::PropertyVector","direction","2 MyCTL","")
	obj.direction=FreeCAD.Vector(0,0,1)
	obj.addProperty("App::PropertyFloat","axisScale","2 MyCTL","")
	obj.axisScale=0.0

	_ViewProviderTelescope(obj.ViewObject)
	return obj

#---------------------------------

# vertexPlugger

App=FreeCAD

def createVertexPlugger(name='VertexPlugger', src=None, target=None, point=0):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	
	c3=obj
	

	#c3.addProperty("App::PropertyLinkList","_targets","3 MyCTL","")
	#c3._targets=targets
	
	c3.addProperty("App::PropertyLink","target","2 MyCTL","")
	c3.target=target
	c3.addProperty("App::PropertyLink","src","2 MyCTL","")
	c3.src=src
	c3.addProperty("App::PropertyInteger","point","2 MyCTL","")
	c3.point=point
	c3.addProperty("App::PropertyPlacement","plOld","2 MyCTL","")
	c3.plOld=FreeCAD.Placement()
	if src:
		c3.plOld=src.Placement
	c3.addProperty("App::PropertyVector","refOld","2 MyCTL","")
	c3.refOld=FreeCAD.Vector()
	if src:
		c3.refOld=FreeCAD.Vector(src.Shape.Vertexes[point].Point)

	for p in ['point','src','target','plOld','refOld']:
		obj.setEditorMode(p, 1) #ro
	_VertexPlugger(obj)
	_ViewProviderVertexPlugger(obj.ViewObject)
	c3.Proxy.updater=True
	return obj

class _VertexPlugger():

	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Transform"
		self.obj2 = obj 
		self.Lock=False
		self.Changed=False

	def execute(self,obj):
		if self.Changed:
			say("self changed")
			# ignore self changes
			self.Changed=False
			return
		if not self.Lock:
#			say("exec self=" +str(self))
			
			say("set Lock ----- " +str(obj.Label))
			self.obj2=obj

			self.Lock=True
			try:
				self.update()
			except:
				say("fehler update")
				pass
			self.Lock=False
			say("unset Lock +++ " +str(self.obj2.Label))

	def update(self):
		lastrefalt=FreeCAD.Placement()
		lastrefalt.Base=self.obj2.refOld
		
		koopalt=FreeCAD.Placement(self.obj2.src.Placement)
		refalt=FreeCAD.Vector(self.obj2.src.Shape.Vertexes[self.obj2.point].Point)
		
		refalt2=FreeCAD.Placement()
		refalt2.Base=refalt

		oldobinv=self.obj2.plOld.inverse()
		oldrelref=oldobinv.multiply(lastrefalt)
		oldrelrefinv=oldrelref.inverse()
		
		s1=oldobinv.multiply(self.obj2.target.Placement)
		s2=oldrelrefinv.multiply(s1)
		s3=refalt2.multiply(s2)
		self.obj2.target.Placement=s3
		
		self.obj2.plOld=koopalt
		self.obj2.refOld=refalt



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

class _ViewProviderVertexPlugger(object):
 
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
		#self.dialog=TransformWidget(self)
		#FreeCAD.t=self
		if not hasattr(self.Object,"Lock"):
				self.Object.Proxy.Lock=False
				say("lock gesetzt")
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
		##s=TransformWidget(self)
		say("still no editor")
		return
		# noc zu impl
		s=VertexPluggerWidget(self)
		self.dialog=s
		self.dialog.show()
		say("set Edit")
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		self.setEdit(vobj)

	def setupContextMenu(self, obj, menu):
		action = menu.addAction("About VertexPlugger")
		action.triggered.connect(self.showVersion)

		action = menu.addAction("Edit ...")
		action.triggered.connect(self.edit)

	def edit(self):
		self.dialog=VertexPluggerWidget(self)
		self.dialog.show()

	def showVersion(self):
		QtGui.QMessageBox.information(None, "About VertexPlugger", "Vertex Plugger Node\n2015 microelly\nVersion " + __vers__ +"\nstill very alpha")



