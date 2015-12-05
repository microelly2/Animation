
# testcase manager 2


def isequal(a,b):
	return abs(a-b)<1e-6

import FreeCAD
import Animation
import Placer

FreeCAD.newDocument("Unbenannt")

# zwei zu animierende Objekte erzeugen und 
# ihrer Plazierer festlegen
b=FreeCAD.activeDocument().addObject("Part::Torus","Torus")
r=Placer.createPlacer("Torus Placer",b)
r.x='100'
r.RotAxis=FreeCAD.Vector(1.0,0,0)

b2=FreeCAD.activeDocument().addObject("Part::Box","Box")
k=Placer.createPlacer("Box Placer",b2)

m=Animation.createManager()
m.intervall = 100
m.sleeptime = 0.01

# die beiden Plazierer durch den Manager verwalten lassen
m.addObject(r)
m.addObject(k)

# den Manager starten
m.Proxy.run()


#FreeCAD.closeDocument("Unbenannt")
