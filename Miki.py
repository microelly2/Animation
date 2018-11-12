# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- miki - my kivy like creation tools
#--
#-- microelly 2016
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------




def creatorFunction(name):
	if name.startswith('Part::'):
		return "App.activeDocument().addObject(name,label)"
	if name.startswith('So'):
		return "coin."+name+'()'
	if name.startswith('QtGui'):
		return name+"()"

	if name in ['Plugger','Manager']:
		return 'Animation.create'+name+'()'
	return name+'()'



import FreeCAD,Animation,FreeCADGui
import re
import pivy
from pivy import coin

App=FreeCAD

import PySide
from PySide import QtCore, QtGui, QtSvg

import traceback,sys
def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=[lls[(l-3)],lls[(l-1)]]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))
	print(mess + "\n" +"-->  ".join(l2))



#***************
YourSpecialCreator=Animation.createManager

def  fv(name="vertical"):
	w=QtGui.QWidget()

	w.setStyleSheet("QWidget { font: bold 18px;color:brown;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
	layout = QtGui.QVBoxLayout()
	layout.setAlignment(QtCore.Qt.AlignTop)
	w.setLayout(layout)

	pB= QtGui.QLabel(name)
	layout.addWidget(pB)
	w.setWindowTitle("Testfenster")
	w.show()
	w.layout=layout
	return w

def  fh(name="horizontal"):
	w=QtGui.QWidget()
	w.setStyleSheet("QWidget { font: bold 18px;color:blue;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
	layout = QtGui.QHBoxLayout()
	layout.setAlignment(QtCore.Qt.AlignLeft)
	w.setLayout(layout)
	pB= QtGui.QLabel(name)
	pB.setStyleSheet("QWidget { font: bold 18px;color:red;border-style: outset;border-width: 3px;border-radius: 10px;border-color: blue;}")
	layout.addWidget(pB)
	w.show()
	w.layout=layout
	return w


VerticalLayout=fv
HorzontalLayout=fh

#***************


class Miki():
	def __init__(self):
		self.objects=[]
		self.anchors={}
		self.indents=[]
		self.olistref=[]
		self.indpos=-1
		self.roots=[]
		self.app=None
		self.ids={}



	def parse2(self,s):
		app=self.app
		
		ls=s.splitlines()
		line=0
		depth=0
		d=[0,0,0,0,0,0,0,0,0,0]
		ln=[0,0,0,0,0,0,0,0,0,0]
		refs={}
		rs=[]
		r=None
		r=[-1,0,0,'']
		for l in ls:
			if r: 
				rs.append(r)
				r=[-1,0,0,'']
			line += 1
			if l.startswith('#:'):
				res=re.search("#:\s*(\S.*)",l)
				r=[l,line,-1,'cmd',res.group(1)]
				continue

			if l.startswith('#'):
				continue
				
			res=re.search("(\s*)(\S.*)",l)
			if res:
				l=len(res.group(1))
				if l==0:
					depth=0
				if d[depth]<l:
					depth += 1
				elif d[depth]>l:
					depth -= 1
				d[depth]=l
				ln[depth]=line
				parent=ln[depth-1]

				r=[l,line,parent,res.group(2)]
				st=res.group(2)
				
				res=re.search("(\S+):\s*\*(\S+)",st)
				if res:
					r=[l,line,parent,'link',res.group(1),res.group(2),refs[res.group(2)]]
					continue

				res=re.search("(\S+):\s*&(\S+)\s+(\S.*)",st)
				if res:
					r=[l,line,parent,"anchor attr",res.group(1),res.group(2),res.group(3)]
					refs[res.group(2)]=line
					continue

				res=re.search("(\S+):\s*&(\S+)",st)
				if res:
					r=[l,line,parent,"anchor",res.group(1),res.group(2)]
					refs[res.group(2)]=line
					continue

				res=re.search("(\S+[^:]):\s*([^:]\S.*)",st)
				if res:
					r=[l,line,parent,"att val",res.group(1),eval(res.group(2))]
					if res.group(1) =='Name':
						rs[parent].append(res.group(2))
				else:
					res=re.search("(\S+):",st)
					if res:    
						r=[l,line,parent,"obj", res.group(1),'no anchor']

		self.lines=rs



	def build(self):
		for l in self.lines:
			if l[3]=='cmd':
				try: 
					exec(l[4])
				except:
					sayexc(str(["Error exec:",l[4]]))
				continue
			if l[3]=='obj' or  l[3]=='anchor':
					name=l[4]
					f=creatorFunction(l[4])
					if len(l)<7: # no name for object
						l.append('')
					label=l[6]
					
					h=eval(f)
					if len(l)<7:
						l.append(None)
					l.append(h)
			if  l[2] != 0:
				if l[4]=='Name': continue
				if l[3]=='obj' or  l[3]=='anchor':
					parent=self.lines[l[2]][7]
					self.addChild(parent,l[7])
				if l[3]=='link':
					parent=self.lines[l[2]][7]
					try:
						child=self.lines[l[6]][7]
						self.addChild(parent,child)
					except:
						# link eines attribs
						method=l[4]
						v=self.lines[l[6]][6]
						kk=eval("parent."+l[4])
						cnkk=kk.__class__.__name__
						if cnkk.startswith('So'):
							ex="parent."+method+".setValue(" +str(v) + ")"
							exec(ex)
							continue
						if cnkk =='builtin_function_or_method':
							# qt 2...
							kk(v)
							continue
						cn=v.__class__.__name__
						if cn=='int' or  cn=='float':
							ex="parent."+l[4]+"="+str(v)
						elif cn=='str':
							ex="parent."+l[4]+"='"+v+"'"
						else:
							print( "nicht implementierter typ")
							ex=''
						print( "*** "+ex)
						exec(ex)
				#-----------------------------------
			if l[3]=='att val' or  l[3]=='anchor attr':
					parent=self.lines[l[2]][7]
					method=l[4]

					if l[3]=='att val':
						v=l[5]
					else:
						v=l[6]
					if method=='id':
						self.ids[v]=parent
						continue

					kk=eval("parent."+l[4])
					cnkk=kk.__class__.__name__

					if cnkk.startswith('So'):
						ex="parent."+method+".setValue(" +str(v) + ")"
						exec(ex)
						continue
					
					if cnkk =='builtin_function_or_method':
							# qt 3...
							kk(v)
							continue

					cn=v.__class__.__name__
					if cn=='int' or  cn=='float':
						ex="parent."+l[4]+"="+str(v)
					elif cn=='str':
						ex="parent."+l[4]+"='"+v+"'"
					else:
						print("nicht implementierter typ")
						ex=''
					print("*** "+ex)
					exec(ex)


	def showSo(self):
		for l in self.lines:
			if  l[2] == 0 and l[0] !=-1:
					r=l[7]
					if r.__class__.__name__.startswith('So'):
						sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
						sg.addChild(r)



	def showSo2(self,dokname):
		for l in self.lines:
			if  l[2] == 0 and l[0] !=-1:
					r=l[7]
					if r.__class__.__name__.startswith('So'):
						dok = FreeCADGui.getDocument(dokname)
						sg=dok.ActiveView.getSceneGraph()
						sg.addChild(r)



	def addChild(self,p,c):
		cc=c.__class__.__name__
		
		if str(c.__class__).startswith("<type 'PySide.QtGui."):
			p.layout.addWidget(c)
			return
		
		if cc.startswith('So'):
			p.addChild(c)
			return

		if str(p.TypeId)=='Part::MultiFuse':
			z=p.Shapes
			z.append(c)
			p.Shapes=z
		elif str(p.TypeId)=='Part::Compound':
			z=p.Links
			z.append(c)
			p.Links=z
		else:
			try: 
				p.addObject(c)
			except: 
				FreeCAD.Console.PrintError("\naddObject funktioniert nicht")
				FreeCAD.Console.PrintError([p,c])


	def run(self,string):
		self.parse2(string)
		self.build()
		self.showSo()


	def report(results=[]):
		for r in results:
			if r.__class__.__name__.startswith('So'):
				sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
				sg.addChild(r)




