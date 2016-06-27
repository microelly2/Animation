
import flowNode
reload (flowNode)



if App.ActiveDocument==None:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")


# initialize scene
Gui.ActiveDocument.ActiveView.setAnimationEnabled(False)
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"
App.ActiveDocument.ActiveObject.Height=800
App.ActiveDocument.ActiveObject.Radius=40
App.ActiveDocument.ActiveObject.ViewObject.Transparency=70
App.ActiveDocument.ActiveObject.Placement.Base=App.Vector(-0,-0,-800)
App.ActiveDocument.ActiveObject.ViewObject.Selectable = False
# App.ActiveDocument.ActiveObject.ViewObject.hide()
c=App.ActiveDocument.ActiveObject


b=App.ActiveDocument.addObject("Part::Box","Box")
b.Length=100
b.Width=100
b.Height=10
b.Placement.Base=App.Vector(-50,-50,-2)
b.ViewObject.Transparency=0
b.ViewObject.Selectable = False



Gui.activeDocument().activeView().viewAxonometric()
App.activeDocument().recompute()

f=flowNode.createFlow()

f.boundMode='Bound Cylinder'

f.dimU=40
f.dimV=40

f.deltaPosition.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-2)
f.startPosition.Base=FreeCAD.Vector(-200,-200,0)

try:f.boundBox=App.ActiveDocument.Cylinder
except: pass

Gui.SendMsgToActiveView("ViewFit")
f.countSlices=500
f.count2Slides=8
f.count3Slides=18
f.count4Slides=24

f.period=50
f.sleep=0.05
f.noise=0
f.Proxy.main()




# run()

