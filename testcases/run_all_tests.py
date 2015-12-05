

ll=['test_manager','test_placer']

for fkn  in ll:
	print fkn," ##################################"
	fn='/usr/lib/freecad/Mod/Animation/testcases/' + fkn +'.py'
	d={};
	exec("import FreeCAD,FreeCADGui;App=FreeCAD;\n" + open(fn).read() + "\n\n",d,d)

