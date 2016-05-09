# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- miki - my kivy like creation tools
#--
#-- microelly 2016
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------




def creatorFunction(name):
	print "creator Function ", name
	if name.startswith('Part::'):
		return "App.activeDocument().addObject(name,label)"
	if name.startswith('So'):
		return "coin."+name+'()'
	if name.startswith('QtGui'):
		return name+"()"
# QtGui.QPushButton()

	if name in ['Plugger','Manager']:
		return 'Animation.create'+name+'()'
	return name+'()'
#	print "no creater Function ***************************"
	return None



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
	print (mess + "\n" +"-->  ".join(l2))



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
#		print self.app
		self.ids={}



	def parse2(self,s):
		print "parse2 --------------------------"
		print "p2", self.app
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
			print l
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
	#				print refs[res.group(2)]
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

				print "huhu"
				print app
				res=re.search("(\S+[^:]):\s*([^:]\S.*)",st)
				if res:
					print app
					r=[l,line,parent,"att val",res.group(1),eval(res.group(2))]
					if res.group(1) =='Name':
						print "setze Namen von parent"
						print parent
						print rs[parent]
						rs[parent].append(res.group(2))
						print rs[parent]
				else:
					res=re.search("(\S+):",st)
					if res:    
						r=[l,line,parent,"obj", res.group(1),'no anchor']

		for r in rs:
				print r

		print refs
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
					print "**", f
					
					h=eval(f)
					print h
					if len(l)<7:
						l.append(None)
					l.append(h)
					print l
			if  l[2] <> 0:
				if l[4]=='Name': continue
				if l[3]=='obj' or  l[3]=='anchor':
					parent=self.lines[l[2]][7]
					print parent
					print l
					print l[7]
					self.addChild(parent,l[7])
					print l
				if l[3]=='link':
					print "hu"
					parent=self.lines[l[2]][7]
					print parent
					print l
					print l[6]
					try:
						child=self.lines[l[6]][7]
						print child
						self.addChild(parent,child)
						print l
					except:
						# link eines attribs
				#----------------------------------
						method=l[4]
						v=self.lines[l[6]][6]
						kk=eval("parent."+l[4])
						cnkk=kk.__class__.__name__
						print ["vor function ", cnkk]
						if cnkk.startswith('So'):
							print "So ..."
							print v
							print v.__class__
							ex="parent."+method+".setValue(" +str(v) + ")"
							exec(ex)
							continue
						if cnkk =='builtin_function_or_method':
							# qt 2...
							print "mche was"
							print v
							print "parent."+l[4]
							kk(v)
							print "okay"
							continue
						cn=v.__class__.__name__
						print [v,cn]
						if cn=='int' or  cn=='float':
							ex="parent."+l[4]+"="+str(v)
						elif cn=='str':
							ex="parent."+l[4]+"='"+v+"'"
						else:
							print "nicht implementierter typ"
							ex=''
						print "*** "+ex
						exec(ex)
				#-----------------------------------
			if l[3]=='att val' or  l[3]=='anchor attr':
					print l
					parent=self.lines[l[2]][7]
					method=l[4]

					if l[3]=='att val':
						print "NORMALx bal"
						print method
						v=l[5]
					else:
						print "anchor val"
						v=l[6]
					if method=='id':
						self.ids[v]=parent
						continue

					kk=eval("parent."+l[4])
					cnkk=kk.__class__.__name__
					print "vor function ", cnkk
					if cnkk.startswith('So'):
						print "So ..."
						print v
						print v.__class__
						ex="parent."+method+".setValue(" +str(v) + ")"
						exec(ex)
						continue
					
					if cnkk =='builtin_function_or_method':
							# qt 3...
							print "mche was"
							print v
							print "parent."+l[4]
							kk(v)
							print "okay"
							continue

					cn=v.__class__.__name__
					print [v,cn]
					if cn=='int' or  cn=='float':
						ex="parent."+l[4]+"="+str(v)
					elif cn=='str':
						ex="parent."+l[4]+"='"+v+"'"
					else:
						print "nicht implementierter typ"
						ex=''
					print "*** "+ex
					exec(ex)


	def showSo(self):
		for l in self.lines:
			if  l[2] == 0 and l[0] <>-1:
					print l
					r=l[7]
					print r
					if r.__class__.__name__.startswith('So'):
						sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
						sg.addChild(r)



	def showSo2(self,dokname):
		for l in self.lines:
			if  l[2] == 0 and l[0] <>-1:
					print l
					r=l[7]
					print r
					if r.__class__.__name__.startswith('So'):
						dok = FreeCADGui.getDocument(dokname)
						sg=dok.ActiveView.getSceneGraph()
						sg.addChild(r)



	def addChild(self,p,c):
		cc=c.__class__.__name__
		print p
		print c
		print c.__class__
		print cc
		
		if str(c.__class__).startswith("<type 'PySide.QtGui."):
			print "pyside"
			print p
			dir(p)
			print p.layout
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
		print self.app
		self.parse2(string)
		self.build()
		self.showSo()


	def report(results=[]):
		print "Results ..."
		for r in results:
			print r
			if r.__class__.__name__.startswith('So'):
				sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
				sg.addChild(r)

		print "Data ..."
		for ob in self.objects:
			print ob

		print self.anchors

		for r in self.roots:
			print r




