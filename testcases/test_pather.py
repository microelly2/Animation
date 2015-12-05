
# pather testcase

import Animation,Draft, Pather, Placer

box=App.ActiveDocument.addObject("Part::Box","Box")
points=[FreeCAD.Vector(22.0,6.0,0.0),
	FreeCAD.Vector(8.,60.5,0.0),
	FreeCAD.Vector(-20,-27.3,0.0),
	FreeCAD.Vector(16.32,-41.3,0.0)]
bspline=Draft.makeBSpline(points)

pa=Pather.createPather('BSpline as Path')
pa.src=bspline

pl=Placer.createPlacer('Placer for Box',box)
pl.x='sx-5'
pl.y='sy-5'
pl.arc='0'
pl.src=pa

m=Animation.createManager()
m.addObject(pa)
m.addObject(pl)

m.Proxy.run()
