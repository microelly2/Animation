
# testcase manager and placer, tracker


def isequal(a,b):
	return abs(a-b)<1e-6


import Animation
from Animation import *
reload(Animation)

import Placer
reload(Placer)

import Tracker
reload(Tracker)
 

d=App.newDocument("Unbenannt")
b=App.activeDocument().addObject("Part::Box","Box")


r=Placer.createPlacer("BoxPlacer",b)

t=Tracker.createTracker("BoxTracker",r)

m=createManager()
m.intervall = 100
m.sleeptime = 0.01
m.addObject(r)
m.addObject(t)
m.Proxy.run()


uu=t.ViewObject.Proxy.showpath()

assert(isequal(uu.Shape.Length,21.5495896498609))

#App.closeDocument("Unbenannt")
