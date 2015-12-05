
# testcase manager and placer


def isequal(a,b):
	return abs(a-b)<1e-6


import Animation
from Animation import *
reload(Animation)

import Placer
reload(Placer)

d=App.newDocument("Unbenannt")
b=App.activeDocument().addObject("Part::Box","Box")


r=Placer.createPlacer("BoxPlacer",b)

m=createManager()
m.intervall = 10
m.sleeptime = 0.01
m.addObject(r)
m.Proxy.run()

assert(isequal(b.Placement.Rotation.Angle,0.5654866776461628))
assert(isequal(b.Placement.Base.x,21.45749434738491))

#App.closeDocument("Unbenannt")
