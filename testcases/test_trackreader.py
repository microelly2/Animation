
# testcase manager and placer, tracker, trackreader


def isequal(a,b):
	return abs(a-b)<1e-6


import Animation
#from Animation import *
reload(Animation)

import Placer
reload(Placer)

import Tracker
reload(Tracker)

import Trackreader
reload(Trackreader)
 

d=App.newDocument("Unbenannt")
b=App.activeDocument().addObject("Part::Box","Box")


r=Placer.createPlacer("BoxPlacer",b)

t=Tracker.createTracker("BoxTracker",r,"/tmp/tracker")

m=Animation.createManager()

m.intervall = 100
m.sleeptime = 0.01
m.addObject(r)
m.addObject(t)
m.Proxy.run()


path=t.ViewObject.Proxy.showpath()


import Trackreader
reload(Trackreader)
tr=Trackreader.createTrackReader("TrackReader",b,"/tmp/tracker")

#App.closeDocument("Unbenannt")
