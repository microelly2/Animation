#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2014                                                    *  
#*   <microelly2@freecadbuch.de>                                           * 
#*   this file is based on the code and the ideas                          *   
#*   of the freecad arch module developed by Yorik van Havre               *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

#
#  animation toolkit
#

class AnimationWorkbench(Workbench):
    "Animation workbench object"
    Icon=   '/home/tog/freecad_buch/b034_animation_wb/icons/animation.png'

    MenuText = "Animation"
    ToolTip = "Animation workbench"

    def Initialize(self):
        import Animation
        self.animtools=[
				"Anim_Mover", 
				"Anim_Rotator",
				"Anim_Tranquillizer",

				"Anim_Photographer",
				"Anim_Plugger",
				"Anim_Adjuster",

				"Anim_Manager",
				"A_Starter",
				"A_Runner",
				"B1","B2","EditObject",
						]

        self.contextTools=["A_Runner","B1","B2","EditObject"]

        FreeCAD.t=self.appendToolbar("Animation",self.animtools)
        self.appendMenu('Animation',self.animtools)
#        self.appendCommandbar("&Generic Tools",["ColorCodeShape"])

        
        Log ('Loading School module... done\n')

    def Activated(self):
        Msg("Animation workbench activated\n")
                
    def Deactivated(self):
        Msg("Animation workbench deactivated\n")

    def ContextMenu(self, recipient):
  #      self.appendContextMenu("Animation tools",self.animtools)
        self.appendContextMenu("My Animation tools",self.contextTools)
        self.appendContextMenu("",self.contextTools)
        FreeCAD.yy=self

    def GetClassName(self): 
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(AnimationWorkbench)







 
