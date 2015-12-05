import Keyboard, Placer
reload(Keyboard)

App.newDocument("Keybord Sensor")
App.setActiveDocument("Keybord Sensor")
App.ActiveDocument=App.getDocument("Keybord Sensor")

# visualization point
V=App.ActiveDocument.addObject("Part::Vertex","Keybord Control Point")
V.ViewObject.PointSize=10
V.ViewObject.PointColor=(1.0,.0,.0)

# slaves
s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
b=App.ActiveDocument.addObject("Part::Box","Box")
t=App.ActiveDocument.addObject("Part::Torus","Torus")

s.ViewObject.ShapeColor=(1.0,1.0,.0)
b.ViewObject.ShapeColor=(.0,1.0,1.0)
t.ViewObject.ShapeColor=(1.0,.0,1.0)

# ACTOR #

# move the sphere relative (10,-5,0) to the control point
p=Placer.createPlacer("Sphere Mover",s)
p.src=V
p.x="sx+10"
p.y="sy-5"

# rotate the cube with rotation arc 20*sx along the default z-axis
p2=Placer.createPlacer("Box Rotator",b)
p2.src=V
p2.x="-50"
p2.y="-5"
p2.arc="20*sx"

# rotate the donat with rotation arc 10*sy  along the x-axis
p3=Placer.createPlacer("Torus Rotator",t)
p3.src=V
p3.x="50"
p3.y="0"
p3.arc="10*sy"
p3.RotAxis=FreeCAD.Vector(1,0,0)

# SENSOR #

kb=Keyboard.createKeyboard("Keybord",V)


# start up
kb.ViewObject.Proxy.edit()
App.activeDocument().recompute()
Gui.SendMsgToActiveView("ViewFit")
