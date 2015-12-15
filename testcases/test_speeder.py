

#
#
# testcase Speeder
#
#

import Animation
from Animation import *
reload(Animation)

import Placer
reload(Placer)

import Speeder
reload(Speeder)



# d=App.newDocument("Unbenannt")
r=Draft.makeRectangle(length=200,height=100.,placement=pl,face=True,support=None)
r.Placement.Base.z=-0.01


b=App.activeDocument().addObject("Part::Box","PingPong Box")
b.ViewObject.ShapeColor=(1.0,.0,.0)
r=Placer.createPlacer("BoxPlacer ping pong",b)
r.arc="0"

s=Speeder.createSpeeder("Speeder Ping Pong")
s.mode='ping pong'
s.target=r


b1=App.activeDocument().addObject("Part::Box","Reverse moving Box")
b1.ViewObject.ShapeColor=(1.0,1.0,.0)
r1=Placer.createPlacer("BoxPlacer reverse",b1)
r1.arc="0"
r1.y="10"
s1=Speeder.createSpeeder("Speeder backward")
s1.mode='backward'
s1.target=r1


b2=App.activeDocument().addObject("Part::Box","Forced forward moving Box")
b2.ViewObject.ShapeColor=(1.0,.0,1.0)
r2=Placer.createPlacer("BoxPlacer quad",b2)
r2.arc="0"
r2.y="20"

s2=Speeder.createSpeeder("Speeder quadratic")
s2.expressiontrafo="100*time**2"
s2.mode='expression'
s2.target=r2


b3=App.activeDocument().addObject("Part::Box","Forward moving Box")
b3.ViewObject.ShapeColor=(.0,1.0,1.0)
r3=Placer.createPlacer("BoxPlacer normal",b3)
r3.arc="0"
r3.y="30"

s3=Speeder.createSpeeder("Speeder forward")
s3.mode='forward'
s3.target=r3



m=createManager()
m.intervall = 101
m.sleeptime = 0.01

m.addObject(s)
m.addObject(s1)
m.addObject(s2)
m.addObject(s3)


#
#
# testcase AnimationControlPanel
#
#

import AnimationControlPanel
reload(AnimationControlPanel)

w=AnimationControlPanel.createAnimationControlPanel()
w.line1=["Speeder_Ping_Pong","Speeder_quadratic"]
w.line2=["Speeder_forward","Speeder_backward"]
w.line3=["BoxPlacer_normal","BoxPlacer_quad","BoxPlacer_reverse"] 


App.activeDocument().recompute()
Gui.SendMsgToActiveView("ViewFit")







m.Proxy.run()
w.ViewObject.Proxy.edit()



