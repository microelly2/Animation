
import Animation
from Animation import *
reload(Animation)

import Placer
reload(Placer)

import Speeder
reload(Speeder)


# d=App.newDocument("Unbenannt")
import Draft
#r=Draft.makeRectangle(length=200,height=200)
#r.Placement.Base.z=-0.02

if False: 
	for x in range(101):
		points=[FreeCAD.Vector(2*x,-200,-0.1),FreeCAD.Vector(2*x,200,-0.1)]
		w=Draft.makeWire(points)
		w.ViewObject.LineWidth=1.0
		w.ViewObject.LineColor=(.0,1.0,.0)

	for y in range(101):
		points=[FreeCAD.Vector(0,2*y,-0.1),FreeCAD.Vector(200,2*y,-0.1)]
		w=Draft.makeWire(points)
		w.ViewObject.LineWidth=1.0
		w.ViewObject.LineColor=(1.0,.0,.0)



b=App.activeDocument().addObject("Part::Box","Box")
b.ViewObject.ShapeColor=(1.0,.0,.0)
r=Placer.createPlacer("Placer",b)
r.arc="0"

s=Speeder.createSpeeder("Speeder Ping Pong")
s.mode='ping pong'
s.m=50

s.target=r


s=Speeder.createSpeeder("Speeder Fade")
s.mode='fade'
s.b=0.3
s.c=0.8
s.m=50
s.g=0.5
s.target=r


s=Speeder.createSpeeder("Speeder Sine")
s.mode='sine wave'
s.b=3
s.c=0
s.m=10
s.target=r

