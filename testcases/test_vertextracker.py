


import FreeCAD
import Animation, Placer,Toucher, VertexTracker



FreeCAD.newDocument("Unbenannt")

box=FreeCAD.activeDocument().addObject("Part::Box","Static")
box.Height=40
box.Length=100

box2=FreeCAD.activeDocument().addObject("Part::Box","Animated")
box2.Placement.Base=FreeCAD.Vector(.0,.0,0.)

toucher=Toucher.createToucher("Force the Common",box)

#
# Example: track the vertexes of a changing fusion
#

placer=Placer.createPlacer("Box Placer",box2)
placer.x="100*time-10"
placer.y=" -5  if time< 0.5 else 7"
placer.z="5+30*(0.5-time)**2"
placer.arc="0"
placer.time=0

manager=Animation.createManager()
manager.intervall = 100
manager.sleeptime = 0.0

fuse=App.activeDocument().addObject("Part::MultiFuse","Fusion")
fuse.Shapes = [box,box2]
fuse.ViewObject.ShapeColor=(1.0,1.0,.5)
fuse.ViewObject.Transparency=70

vertextracker=VertexTracker.createVertexTracker("Track of the Fusion")
vertextracker.src=fuse

manager.addObject(placer)
manager.addObject(toucher)
manager.addObject(vertextracker)

# run the manager
manager.Proxy.run()

# show track data

vertextracker.Proxy.show()

# generate pathes for the tracks
vertextracker.Proxy.gen()


