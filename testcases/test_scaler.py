import Part, Draft
App=FreeCAD

App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
b=App.ActiveDocument.addObject("Part::Box","Box")

c=Draft.clone(b)
import Animation


m=Animation.createManager("Skaler Manager")

import Scaler
reload(Scaler)

s=Scaler.createScaler("Mein Skalierer")
s.obj2=c
s.duration=80

m.addObject(s)
m.Proxy.run()

