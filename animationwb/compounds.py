import FreeCAD
import FreeCADGui



def run():
	print "animationwb.compounds.run"




def delete():
	s=FreeCADGui.Selection.getSelection()
	comp=s[-1]
	unlinks=s[:-1]
	links=comp.Links
	linksnew=[]
	for l in links:
		if l not in unlinks:
			linksnew += [l]
	comp.Links=linksnew


def add():
	s=FreeCADGui.Selection.getSelection()
	comp=s[-1]
	addlinks=s[:-1]
	links=comp.Links
	for l in addlinks:
		if l not in links:
			links += [l]
	comp.Links=links



def create():
	s=FreeCADGui.Selection.getSelection()
	comp=FreeCAD.ActiveDocument.addObject("Part::Compound","Compound")
	comp.Links=s




