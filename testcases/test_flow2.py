import flowNode
reload (flowNode)


if App.ActiveDocument==None:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")


b=App.ActiveDocument.addObject("Part::Box","Box")
b.Length=130
b.Width=100
b.Height=200
b.Placement.Base=App.Vector(-65,-50,-200)
b.ViewObject.Transparency=70
b.ViewObject.Selectable = False

Gui.activeDocument().activeView().viewAxonometric()
App.activeDocument().recompute()

f=flowNode.createFlow()

f.boundMode='Bound Box'
f.startFace = "Rectangle"

f.boundMode = "Bound Cylinder"
f.startFace = "Circle"


f.dimU=12
f.dimV=100
f.noise=0



try:f.boundBox=App.ActiveDocument.Box
except: pass

Gui.SendMsgToActiveView("ViewFit")
f.countSlices=400
f.count2Slides=2
f.count3Slides=6
f.count4Slides=14

f.lengthStartCloud = 130
f.widthStartCloud = 100

f.sleep=0.1
#f.Proxy.main()
