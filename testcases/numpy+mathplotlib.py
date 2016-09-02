
import numpyNode
reload(numpyNode)

t=numpyNode.createNP()
#t.sourceObject= App.ActiveDocument.Plot001
#t.expression2="4* np.arctan2(in2,in3)"



import  mathplotlibNode
from mathplotlibNode import createMPL

t=createMPL()
t.sourceObject= App.ActiveDocument.My_Manager
t.countSources=4
t.sourceData="step"

t.source1Object= App.ActiveDocument.Box001
t.source1Data="Placement.Rotation.Angle"


t.source2Object= App.ActiveDocument.Box001
t.source2Data="Placement.Base.x"

t.source3Object= App.ActiveDocument.Box001
t.source3Data="Placement.Base.y"

# t.expression2="2* np.arctan2(in2,in3)"

t.record=True

t.source2Values=[1,2,3,4]
t.source3Values=[1,3,2,5]
App.ActiveDocument.Numpy.sourceObject=t


t2=createMPL()
t2.sourceObject= App.ActiveDocument.My_Manager
t2.sourceData="step"

t2.source1Object= App.ActiveDocument.Box001
t2.source1Data="Placement.Rotation.Angle"


t2.sourceObject= App.ActiveDocument.My_Manager
t2.useNumpy=True
t2.sourceNumpy=App.ActiveDocument.Numpy
t2.useOut0=True
t2.useOut1=True
t2.useOut2=True
t2.record=True

	
