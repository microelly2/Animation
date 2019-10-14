#***************************************************************************
#*																		 *
#*   Copyright (c) 2014, 2018												*  
#*   <microelly2@freecadbuch.de>										   * 
#*   this file is based on the code and the ideas						  *   
#*   of the freecad arch module developed by Yorik van Havre			   *
#*																		 *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	 *
#*   the License, or (at your option) any later version.				   *
#*   for detail see the LICENCE text file.								 *
#*																		 *
#*   This program is distributed in the hope that it will be useful,	   *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		 *
#*   GNU Library General Public License for more details.				  *
#*																		 *
#*   You should have received a copy of the GNU Library General Public	 *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA																   *
#*																		 *
#***************************************************************************

#
#  animation toolkit
#

#import numpy, os
import FreeCAD
import FreeCADGui
import PySide
from PySide import QtGui
import os

import Animation
global __dir__
__dir__ = os.path.dirname(Animation.__file__)



class _CommandActor():

	def __init__(self,name='Actor',icon='/icons/icon3.svg',command='',modul=''):
#		say("create Actor Command")
#		say(name)
		self.name=name
		self.icon=  __dir__+ icon
		self.command=command
		self.modul=modul
#		say(self.icon)

	def GetResources(self): 
		return {'Pixmap' : self.icon, 'MenuText': self.name, 'ToolTip': self.name +' Dialog'} 


	def IsActive(self):
		if FreeCADGui.ActiveDocument:
			return True
		else:
			return False

	def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction("create " + self.name)
			if self.command != '':
				if self.modul !='':
					modul=self.modul
				else:
					modul=self.name
				FreeCADGui.doCommand("import " + modul)
				#FreeCADGui.doCommand("reload(" + modul +")")
				FreeCADGui.doCommand(self.command)
			else:
				FreeCADGui.doCommand("import Animation")
				FreeCADGui.doCommand("Animation.create"+self.name+"()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			Msg("Erst Arbeitsbereich oeffnen")
		return


if FreeCAD.GuiUp:

	FreeCADGui.addCommand('Anim_TA',_CommandActor("Interpolator",'/icons/icon1.svg',"Trackreader.runTA()","Trackreader"))
	FreeCADGui.addCommand('Anim_TB',_CommandActor("Fourier",'/icons/icon2.svg',"Trackreader.runTB()","Trackreader"))
	FreeCADGui.addCommand('Anim_TC',_CommandActor("Noise",'/icons/icon3.svg',"Trackreader.runTC()","Trackreader"))


	FreeCADGui.addCommand('Anim_Abroller',_CommandActor("Abroller",'/icons/abroller.png','Abroller.createAbroller()'))
	FreeCADGui.addCommand('Anim_Adjuster',_CommandActor('Adjuster','/icons/adjuster.png'))
	FreeCADGui.addCommand('Anim_Assembly2Controller',_CommandActor("Assembly2Controller",'/icons/assembly2SolveConstraints.svg',"Assembly2Controller.createAssembly2Controller()"))
	FreeCADGui.addCommand('Anim_Billboard',_CommandActor('Billboard', '/icons/billboard.png'))
	FreeCADGui.addCommand('Anim_Bounder',_CommandActor("Bounder",'/icons/bounder.png'))
	FreeCADGui.addCommand('Anim_Collider',_CommandActor("Collision",'/icons/collider.png',"Collision.createCollision()"))
	FreeCADGui.addCommand('Anim_Combiner',_CommandActor("Combiner",'/icons/combiner.png',"Combiner.createCombiner()"))
	FreeCADGui.addCommand('Anim_Connector',_CommandActor('Connector','/icons/scaler.png'))
	FreeCADGui.addCommand('Anim_ControlPanel',_CommandActor("AnimationControlPanel",'/icons/controlpanel.png',"AnimationControlPanel.createAnimationControlPanel()"))
	FreeCADGui.addCommand('Anim_Delta',_CommandActor("Delta",'/icons/delta.png'))
	FreeCADGui.addCommand('Anim_Diagram',_CommandActor("Diagram",'/icons/diagram.png',"Diagram.createDiagram()"))
	FreeCADGui.addCommand('Anim_Extruder',_CommandActor('Extruder','/icons/extruder.png'))
	FreeCADGui.addCommand('Anim_Filler',_CommandActor('Filler','/icons/filler.png'))
	FreeCADGui.addCommand('Anim_Gearing',_CommandActor('Gearing','/icons/gearing.png','Gearing.createGearing()'))
	FreeCADGui.addCommand('Anim_Kartan',_CommandActor('Kartan','/icons/kardan.png','Kartan.createKartan()'))
	FreeCADGui.addCommand('Anim_Manager',_CommandActor('Manager','/icons/manager.png'))
	FreeCADGui.addCommand('Anim_Mover',_CommandActor('Mover','/icons/mover.png'))
	FreeCADGui.addCommand('Anim_Moviescreen',_CommandActor('Moviescreen', '/icons/moviescreen.png'))
	FreeCADGui.addCommand('Anim_Pather',_CommandActor("Pather",'/icons/pather.png','Pather.createPather()'))
	FreeCADGui.addCommand('Anim_Photographer',_CommandActor('Photographer','/icons/photographer.png'))
	FreeCADGui.addCommand('Anim_Placer',_CommandActor("Placer",'/icons/placer.png',"Placer.createPlacer()"))
	FreeCADGui.addCommand('Anim_Plugger',_CommandActor('Plugger','/icons/plugger.png'))
	FreeCADGui.addCommand('Anim_Rotator',_CommandActor('Rotator','/icons/rotator.png'))
	FreeCADGui.addCommand('Anim_Scaler',_CommandActor('Scaler','/icons/scaler.png','Scaler.createScaler()'))
	FreeCADGui.addCommand('Anim_Snapshot',_CommandActor("Snapshot",'/icons/snapshot.png',"Snapshot.createSnapshot()","Snapshot"))
	FreeCADGui.addCommand('Anim_Speeder',_CommandActor("Speeder",'/icons/speeder.png',"Speeder.createSpeeder()"))
	FreeCADGui.addCommand('Anim_Styler',_CommandActor('Styler', '/icons/styler.png'))
	FreeCADGui.addCommand('Anim_Sum',_CommandActor("Sum",'/icons/sum.png'))
	FreeCADGui.addCommand('Anim_Toucher',_CommandActor("Toucher",'/icons/toucher.png',"Toucher.createToucher()"))
	FreeCADGui.addCommand('Anim_Tracker',_CommandActor("Tracker",'/icons/tracker.png',"Tracker.createTracker()"))
	FreeCADGui.addCommand('Anim_Trackreader',_CommandActor("Trackreader",'/icons/trackreader.png',"Trackreader.createTrackreader()"))
	FreeCADGui.addCommand('Anim_Tranquillizer',_CommandActor('Tranquillizer','/icons/tranq.png'))
	FreeCADGui.addCommand('Anim_Viewpoint',_CommandActor('Viewpoint','/icons/viewpoint.png'))
	FreeCADGui.addCommand('Anim_ViewSequence',_CommandActor("ViewSequence",'/icons/snapshotviewer.png',"Snapshot.createViewSequence()","Snapshot"))
#------------------
#------------------

global _Command
class _Command():

	def __init__(self,lib=None,name=None,icon='/../icons/nurbs.svg',command=None,modul='nurbswb'):

		if lib==None: lmod=modul
		else: lmod=modul+'.'+lib
		if command==None: command=lmod+".run()"
		else: command =lmod + "."+command

		self.lmod=lmod
		self.command=command
		self.modul=modul
		self.icon=  __dir__+ icon

		if name==None: name=command
		self.name=name


	def GetResources(self): 
		return {'Pixmap' : self.icon, 
			'MenuText': self.name, 
			'ToolTip': self.name, 
			'CmdType': "ForEdit" # bleibt aktiv, wenn sketch editor oder andere tasktab an ist
		} 

	def IsActive(self):
		if FreeCADGui.ActiveDocument: return True
		else: return False

	def Activated(self):
		#FreeCAD.ActiveDocument.openTransaction("create " + self.name)
		if self.command != '':
			if self.modul !='': modul=self.modul
			else: modul=self.name
			FreeCADGui.doCommand("import " + modul)
			FreeCADGui.doCommand("import "+self.lmod)
			#FreeCADGui.doCommand("reload("+self.lmod+")")
			FreeCADGui.doCommand(self.command)
		#FreeCAD.ActiveDocument.commitTransaction()
		if FreeCAD.ActiveDocument != None:
			FreeCAD.ActiveDocument.recompute()


class _alwaysActive(_Command):

	def IsActive(self):
		return True

# conditions when a command should be active ..

def always():
	''' always'''
	return True

def ondocument():
	'''if a document is active'''
	return FreeCADGui.ActiveDocument != None

def onselection():
	'''if at least one object is selected'''
	return len(FreeCADGui.Selection.getSelection())>0

def onselection1():
	'''if exactly one object is selected'''
	return len(FreeCADGui.Selection.getSelection())==1

def onselection2():
	'''if exactly two objects are selected'''
	return len(FreeCADGui.Selection.getSelection())==2

def onselection3():
	'''if exactly three objects are selected'''
	return len(FreeCADGui.Selection.getSelection())==3

def onselex():
	'''if at least one subobject is selected'''
	return len(FreeCADGui.Selection.getSelectionEx())!=0

def onselex1():
	'''if exactly one subobject is selected'''
	return len(FreeCADGui.Selection.getSelectionEx())==1


# the menu entry list
FreeCAD.tcmds6=[]

# create menu entries 
'''
def c1(menu,name,*info):
	global _Command
	name1="Nurbs_"+name
	t=_Command(name,*info)
	FreeCADGui.addCommand(name1,t)
	FreeCAD.tcmds5.append([menu,name1,name,'always',info])
'''

def c1a(menu,isactive,name,*info):
	global _Command
	name1="Animation_"+name
	t=_Command(name,*info)
	t.IsActive=isactive
	FreeCADGui.addCommand(name1,t)
	FreeCAD.tcmds6.append([menu,name1,name,isactive,info])


def c2a(menu,isactive,title,name,*info):
	global _Command
	t=_Command(name,*info)
	title1="Animation_"+title
	t.IsActive=isactive
	FreeCADGui.addCommand(title1,t)
	FreeCAD.tcmds6.append([menu,title1,name,isactive,info])


# special conditions for actions



if FreeCAD.GuiUp:

	c2a(["Compounds"],ondocument,'createCompound',"compounds","create Compound of a Selection ",'/icons/comp_create.svg',"create()","animationwb")
	c2a(["Compounds"],ondocument,'addCompound',"compounds","add Selection to Compound",'/icons/comp_add.svg',"add()","animationwb")
	c2a(["Compounds"],ondocument,'deleteCompound',"compounds","delete Selection from Compound",'/icons/comp_delete.svg',"delete()","animationwb")



#-------------------
#-------------------






class AnimationWorkbench(Workbench):
	'''Animation workbench object'''
	
	Icon = """
/* XPM */
static char * animation_xpm[] = {
"16 16 116 2",
"  	c #FFFFFF",
". 	c #F6F1F3",
"+ 	c #F8F4F6",
"@ 	c #FFFEFF",
"# 	c #FBFAFB",
"$ 	c #FEFDFD",
"% 	c #FAF7F8",
"& 	c #CCB1BD",
"* 	c #B792A2",
"= 	c #E5D7DD",
"- 	c #D2BBC5",
"; 	c #FCF9FA",
"> 	c #EBE1E6",
", 	c #C3A4B2",
"' 	c #B1889B",
") 	c #EADFE4",
"! 	c #F0E7EA",
"~ 	c #EFE7EB",
"{ 	c #BE9DAC",
"] 	c #B2899B",
"^ 	c #DAC7CF",
"/ 	c #8A4E69",
"( 	c #A37388",
"_ 	c #DFCFD6",
": 	c #FAF8F9",
"< 	c #EDE4E8",
"[ 	c #C1A1AF",
"} 	c #CDB3BF",
"| 	c #783251",
"1 	c #702647",
"2 	c #762F4F",
"3 	c #F7F2F4",
"4 	c #EEE5E9",
"5 	c #C4A5B2",
"6 	c #F4EEF1",
"7 	c #C2A3B1",
"8 	c #6C1F41",
"9 	c #6F2546",
"0 	c #C3A3B1",
"a 	c #F9F7F8",
"b 	c #ECE3E7",
"c 	c #F3EDEF",
"d 	c #C6A9B6",
"e 	c #691B3D",
"f 	c #82415E",
"g 	c #BF9EAC",
"h 	c #E0D1D8",
"i 	c #FFFEFE",
"j 	c #B48C9E",
"k 	c #C4A5B3",
"l 	c #FEFCFD",
"m 	c #AC8295",
"n 	c #6D2243",
"o 	c #7D3A58",
"p 	c #B994A4",
"q 	c #C09FAD",
"r 	c #D7C2CB",
"s 	c #A87A8E",
"t 	c #6F2445",
"u 	c #884C67",
"v 	c #8C516C",
"w 	c #945D75",
"x 	c #945C75",
"y 	c #6D2244",
"z 	c #81405D",
"A 	c #AA7C91",
"B 	c #945C74",
"C 	c #B894A4",
"D 	c #844562",
"E 	c #FEFEFE",
"F 	c #FBF9FA",
"G 	c #DFCED5",
"H 	c #7E3B59",
"I 	c #7A3553",
"J 	c #702546",
"K 	c #691B3E",
"L 	c #651639",
"M 	c #6B1E40",
"N 	c #651539",
"O 	c #66163A",
"P 	c #7F3C5A",
"Q 	c #E6DADF",
"R 	c #BF9EAD",
"S 	c #B996A6",
"T 	c #6E2345",
"U 	c #E9DEE2",
"V 	c #B28B9C",
"W 	c #F5F0F1",
"X 	c #B58FA0",
"Y 	c #FCFAFB",
"Z 	c #AA7E91",
"` 	c #894B67",
" .	c #722849",
"..	c #8E546E",
"+.	c #C6A8B4",
"@.	c #CCB2BE",
"#.	c #A87B8F",
"$.	c #AF8698",
"%.	c #6B1F41",
"&.	c #E3D4DB",
"*.	c #DDCAD3",
"=.	c #905670",
"-.	c #B690A1",
";.	c #7B3655",
">.	c #77304F",
",.	c #DBC9D1",
"'.	c #8B4E69",
").	c #67193C",
"!.	c #B28B9D",
"~.	c #681A3C",
"{.	c #E6D9DF",
"].	c #783151",
"^.	c #D3BCC7",
"/.	c #773151",
"(.	c #D7C2CC",
"_.	c #FDFCFD",
"      .   .   + @   # $ %       ",
"      &   *   = $   - ; >       ",
"      ,   '   )     - ! ~       ",
"      { $ ] ^ / ( _ & : <       ",
"      [ + } | 1 1 2 & 3 4       ",
"      5 6 7 8 1 1 9 0 a b       ",
"      5 c d e 1 1 f g a h       ",
"  i j k < l m n o 3 p   q r     ",
"  s t u v w x y z A B C D ] E   ",
"F G 5 H I J K 1 9 L M N O P Q   ",
"        R   S T 1 U V W i X Y   ",
"        Z   ` 2  ...+.          ",
"    @.#.$.  %.&.*.M =.  4       ",
"    -.;.>.,.'.    @.).!.~.{.    ",
"        = ].Z       ^./.(.      ",
"          F _.        :         "};"""






	MenuText = "Animation"
	ToolTip = "Animation workbench"

	def Initialize(self):
#		import Animation
#		import Scaler
		
		Gui.activateWorkbench("DraftWorkbench")
		Gui.activateWorkbench("SketcherWorkbench")

		self.functiontools=[
				"Anim_TA",
				"Anim_TB",
				"Anim_TC",
				'Draft_ToggleGrid',
		]

		self.animtools=[
				"Anim_TA",
				"Anim_Mover", 
				"Anim_Rotator",
				
				"Anim_Tranquillizer",

				"Anim_Photographer",
				"Anim_Plugger",
				"Anim_Adjuster",
				
				"Anim_Styler",
				"Anim_Billboard",
				"Anim_Moviescreen",
				"Anim_Extruder",
				"Anim_Viewpoint",


				"Anim_Manager",
				"Anim_Bounder",
				"Anim_Filler",

				"Anim_Gearing",
				"Anim_Kartan",
				"Anim_Scaler",
				
#				"A_Starter",
#				"A_Runner",
#				"B1","B2",
#				"EditObject",

				"Anim_Placer",
				"Anim_Diagram",


'Anim_Collider',
'Anim_Combiner',
'Anim_ControlPanel',
'Anim_Pather',
'Anim_Snapshot',
'Anim_ViewSequence',
'Anim_Speeder',
'Anim_Toucher',
'Anim_Tracker',
'Anim_Trackreader',


'Anim_Abroller',
'Anim_Delta',
'Anim_Sum',


'Anim_Assembly2Controller',
'Anim_Connector',




				
						]
						
		self.actions = [	
			"ScriptAction",
			"LoopAction",
			"WhileAction","RepeatAction","FalseAction","TrueAction","CaseAction","QueryAction"
		]

		self.contextTools=["A_Runner","B1","B2","EditObject"]
		
		
		
		FreeCAD.t=self.appendToolbar("Functions",self.functiontools)
		FreeCAD.t=self.appendToolbar("Animation",self.animtools)
##		FreeCAD.t=self.appendToolbar("ActionScript",self.actions)
		
		self.appendMenu('Functions',self.functiontools)
		self.appendMenu('Animation',self.animtools)
##		self.appendMenu('Script Actions',self.actions)


		# add the commands version 2018 
		menues={}
		ml=[]
		for _t in FreeCAD.tcmds6:
			c=_t[0]
			a=_t[1]
			try:menues[tuple(c)].append(a)

			except: 
				menues[tuple(c)]=[a]
				ml.append(tuple(c))

		for m in ml:
			self.appendMenu(list(m),menues[m])


		
		Log ('Loading Animation Workbench ... done\n')

	def Activated(self):
		Msg("Animation workbench activated\n")
				
	def Deactivated(self):
		Msg("Animation workbench deactivated\n")

	def ContextMenu(self, recipient):
#	  self.appendContextMenu("Animation tools",self.animtools)
# 		self.appendContextMenu("My Animation tools",self.contextTools)
#		self.appendContextMenu("",self.contextTools)
#		FreeCAD.yy=self
		pass

	def GetClassName(self): 
		return "Gui::PythonWorkbench"








FreeCADGui.addWorkbench(AnimationWorkbench)





 
