import FreeCAD
import Animation

import os

__vers__= '0.2'
__dir__ = os.path.dirname(__file__)	


#---------------------------------------------------------------
# Toucher
#---------------------------------------------------------------

class _Toucher(Animation._Actor):
	''' to touch object during animation '''

	def update(self):
		pass

	def step(self,now):
		self.obj2.target.touch()
		for t in self.obj2.targets:
			t.touch()

class _ViewProviderToucher(Animation._ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/animation.png'

def createToucher(name='My_Toucher',target=None,targets=None):
	''' createToucher(name,target,targets=None) returns an animation node for one target or a list of targets
	target: single object, targets: list of objects
	'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","target","Base","")
	obj.addProperty("App::PropertyLinkList","targets","Base","")
	obj.target=target
	if targets:
		obj.targets=targets
	_Toucher(obj)
	_ViewProviderToucher(obj.ViewObject)
	return obj
