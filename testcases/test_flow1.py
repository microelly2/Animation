
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
App.ActiveDocument.ActiveObject.Height=200
App.ActiveDocument.ActiveObject.Radius=40
App.ActiveDocument.ActiveObject.ViewObject.Transparency=70
App.ActiveDocument.ActiveObject.Placement.Base=App.Vector(-0,-0,-200)
App.ActiveDocument.ActiveObject.ViewObject.Selectable = False
# App.ActiveDocument.ActiveObject.ViewObject.hide()



b=App.ActiveDocument.addObject("Part::Box","Box")
b.Length=100
b.Width=40
b.Height=200
b.Placement.Base=App.Vector(-50,-20,-200)
b.ViewObject.Transparency=70
b.ViewObject.Selectable = False


Gui.activeDocument().activeView().viewAxonometric()
App.activeDocument().recompute()

f=flowNode.createFlow()

f.boundMode='Bound Cylinder'

f.dimU=30
f.dimV=30

f.deltaPosition.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-5)


try:f.boundBox=App.ActiveDocument.Box
except: pass

Gui.SendMsgToActiveView("ViewFit")
f.countSlices=100
f.count2Slides=2
f.count3Slides=6
f.count4Slides=14

f.sleep=0.1
f.Proxy.main()


# run()

