
import FreeCAD, os, unittest, FreeCADGui

def isequal(a,b):
	return abs(a-b)<1e-6


from Animation import *
reload(Animation)

import Placer
reload(Placer)


class AnimationTest(unittest.TestCase):

	def setUp(self):
		# setting a new document to hold the tests
		if FreeCAD.ActiveDocument:
			if FreeCAD.ActiveDocument.Name != "AnimTest":
				FreeCAD.newDocument("AnimTest")
		else:
			FreeCAD.newDocument("AnimTest")
		FreeCAD.setActiveDocument("AnimTest")

	def tearDown(self):
		FreeCAD.closeDocument("AnimTest")
		pass

	def testPlacer(self):
		FreeCAD.Console.PrintLog ('Checking Placer...\n')
		b=App.activeDocument().addObject("Part::Box","Box")
		r=Placer.createPlacer("BoxPlacer",b)
		m=createManager()
		m.intervall = 10
		m.sleeptime = 0.01
		m.addObject(r)
		m.Proxy.run()
		self.failUnless(isequal(b.Placement.Rotation.Angle,0.5654866776461628),"Rotation error")
		self.failUnless(isequal(b.Placement.Base.x,21.45749434738491),"Move error")




unittest.main()
