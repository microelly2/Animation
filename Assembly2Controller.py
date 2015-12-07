import FreeCAD
import Animation
from Animation import say,sayErr,sayexc


import os

__vers__= '0.1'
__dir__ = os.path.dirname(__file__)



#---------------------------------------------------------------
# Assembly2
#---------------------------------------------------------------

class _Assembly2Controller(Animation._Actor):
	''' solve assemby2 constraints '''

	def update(self):
		pass

	def step(self,now):
		try:
			# https://github.com/hamish2014/FreeCAD_assembly2/issues/73
			import assembly2lib
			assembly2lib.debugPrint.level = 0 #the default is 2
			assembly2lib.debugPrint.level = self.obj2.debugLevel
			import assembly2solver
			try:
				constraintSystem = assembly2solver.solveConstraints(
						FreeCAD.ActiveDocument, showFailureErrorDialog=False, 
						printErrors=self.obj2.printErrors)
				if constraintSystem == None:
					sayErr('Solver failed to satisfy specified constraints')
				else:
					say("Solver step done " + str(now)) 
			except:
				sayErr("problem assembly2solver.solveConstraints(App.ActiveDocument)")
		except:
			sayErr("problem no assembly2 available")
			pass

class _ViewProviderAssembly2Controller(Animation._ViewProviderActor):

	def getIcon(self):
		return __dir__ + '/icons/assembly2SolveConstraints.svg'

def createAssembly2Controller(name='Assembly2'):
	''' createToucher(name,target,targets=None) returns an animation node for one target or a list of targets
	target: single object, targets: list of objects
	'''
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyFloat","time","Base","").time=0
	obj.addProperty("App::PropertyInteger","debugLevel","Assemby2","").debugLevel=0
	obj.addProperty("App::PropertyBool","printErrors","Assemby2","").printErrors=False

	_Assembly2Controller(obj)
	_ViewProviderAssembly2Controller(obj.ViewObject)
	return obj


if False:
	s=createAssembly2Controller()
	s.Proxy.step(6)

