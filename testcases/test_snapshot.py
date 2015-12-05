
# testcase manager


def isequal(a,b):
	return abs(a-b)<1e-6

import Animation
from Animation import *
# reload(Animation)

import Placer
reload(Placer)

import Snapshot
reload(Snapshot)

import Toucher
reload(Toucher)


d=App.newDocument("Unbenannt")
b=App.activeDocument().addObject("Part::Box","Box")
b.ViewObject.Visibility=False
t=App.ActiveDocument.addObject("Part::Torus","Torus")
t.Radius1=50

c=App.ActiveDocument.addObject("Part::Cone","Cone")
c.Radius1=50
c.Radius2=3
c.Placement.Base.x=14
c.ViewObject.Visibility=False

ss=App.activeDocument().addObject("Part::MultiCommon","Common")
ss.Shapes = [b,c]
ss.ViewObject.Visibility=False

FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)
FreeCAD.ActiveDocument.recompute()
FreeCADGui.SendMsgToActiveView("ViewFit")
FreeCADGui.updateGui() 
 

r=Placer.createPlacer("BoxPlacer",b)
to=Toucher.createToucher("Touch Common",b)

s=Snapshot.createSnapshot("Snaps ",'T',ss)
v=Snapshot.createViewSequence('VS','T')

m=createManager()
m2=createManager()

m.intervall = 30
m.sleeptime = 0
m.addObject(r)
m.addObject(to)
m.addObject(s)
m.Proxy.run()


m2.intervall = 30
m2.sleeptime = 0.1
m2.addObject(v)
m2.Proxy.run()
App.ActiveDocument.ActiveObject.ViewObject.Visibility=False

#App.closeDocument("Unbenannt")
