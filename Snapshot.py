import FreeCAD
import Animation
from Animation import say,sayErr,sayexc
import os

__vers__= '0.2'
__dir__ = os.path.dirname(__file__)	


#---------------------------------------------------------------
# Snapshot
#---------------------------------------------------------------

class _Snapshot(Animation._Actor):
	''' creat a simple copy of the animated object each step '''

	def step(self,now):
		if now==0:
			self.g=FreeCAD.activeDocument().addObject("App::DocumentObjectGroup","Snapshots_"+ self.obj2.seqname)
		ss=FreeCAD.ActiveDocument.addObject('Part::Feature',self.obj2.seqname)
		ss.Shape=self.obj2.target.Shape
		ss.ViewObject.ShapeColor=(1.0,0.0,0.0)
		ss.ViewObject.Visibility=False
		self.g.addObject(ss)

class _ViewProviderSnapshot(Animation._ViewProviderActor):

	def getIcon(self):
		icon='/icons/mover.png'
		return __dir__ + icon

def createSnapshot(name='My_Snapshot',seqname='S',target=None,targets=[]):
	'''createSnapshot(name,seqname='S',target=None,targets=[]) returns an animation node for one target or a list of targets
	target: single object, targets: list of objects
	'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","target","Base","")
	obj.addProperty("App::PropertyLinkList","targets","Base","")
	obj.addProperty("App::PropertyString","seqname","Base","").seqname=seqname
	obj.target=target
	if targets: 
		obj.targets=targets
	_Snapshot(obj)
	_ViewProviderSnapshot(obj.ViewObject)
	return obj


#---------------------------------------------------------------
# View Sequence
#---------------------------------------------------------------

class _ViewSequence(Animation._Actor):
	''' shows a numbered list of parts'''

	def step(self,now):
		if now==0:
			sufi=''
		else:
			sufi=  "%03d" % (now) 
		if now > 0:
			try:
				ob=self.last
				ob.ViewObject.Visibility=False
			except:
				pass
			ob=FreeCAD.activeDocument().getObject(self.obj2.seqname + sufi)
			say(ob.Name)
			ob.ViewObject.Visibility=True
			self.last=ob

class _ViewProviderViewSequence(Animation._ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/rotator.png'

def createViewSequence(name='My_ViewSequence',seqname='S'):
	''' createViewSequence(name,sequencename) returns an animation node for a sequence list'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyString","seqname","Base","").seqname=seqname
	_ViewSequence(obj)
	_ViewProviderViewSequence(obj.ViewObject)
	return obj

