
# testcase manager


def isequal(a,b):
	return abs(a-b)<1e-6


from Animation import *

App.newDocument("Unbenannt")
b=App.activeDocument().addObject("Part::Box","Box")

r=createRotator()
r.duration = 10
r.obj2=b

m=createManager()
m.intervall = 10
m.sleeptime = 0.01
m.addObject(r)
m.Proxy.run()

assert(isequal(b.Placement.Rotation.Angle,5.65486677646))

App.closeDocument("Unbenannt")
