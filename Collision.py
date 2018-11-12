import FreeCAD

from say import *

__dir__ = os.path.dirname(__file__)	

#-----------------------------------------

#--------------------------------------------

def col(actor,obstacles):
	
	av=actor.Shape.BoundBox
	for obl in obstacles:
		ov=obl.Shape.BoundBox
		if ov.XMin < av.XMax  and  ov.XMax > av.XMin and ov.YMin <= av.YMax and  ov.YMax >= av.YMin and  ov.ZMin <= av.ZMax and  ov.ZMax >= av.ZMin:
			print(obl.Label)
			obl.ViewObject.DiffuseColor=(1.0,0.0,0.0)
		else:
			obl.ViewObject.DiffuseColor=(1.0,1.0,0.0)  

#--------------------------------------------


import Part


def say(a):
	FreeCAD.Console.PrintMessage(a)

import FreeCAD,os,FreeCADGui,time,sys,traceback
def sayexc(mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))

class _ViewProvider(object):
 
	def getIcon(self):
		
		return  __dir__ + '/icons/collider.png'
   
	def __init__(self,vobj):
		vobj.Proxy = self


	def attach(self,vobj):
		self.Object = vobj.Object
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


class Detector():

	def __init__(self,obj):
		obj.Proxy = self
		self.obj2=obj
		self.Type = "_Manager"
		self.Lock=False
		if obj.s1==None:
			obj.s1=FreeCAD.ActiveDocument.addObject("Part::Sphere","s1")
		if obj.s2==None:
			obj.s2=FreeCAD.ActiveDocument.addObject("Part::Sphere","s2")
		if obj.s3==None:
			obj.s3=FreeCAD.ActiveDocument.addObject("Part::Sphere","s3")
#		self.comm=FreeCAD.activeDocument().addObject("Part::MultiCommon","Common")
#		self.comm.Shapes = [obj.traveller,obj.stator]
		if obj.comm==None:
			obj.comm = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",'Collision')
			obj.comm.ViewObject.Proxy=object()
		try:
			s=obj.traveller.Shape
			s2=obj.stator.Shape
			# obj.Shape=s.fuse(s2)
			obj.comm.Shape=s.common(s2)
			for t in self.comm.Shapes:
				t.ViewObject.Visibility=True
		except: pass
		if obj.offs==None:
			obj.offs=FreeCAD.ActiveDocument.addObject("Part::Offset","Offset")
		try: obj.offs.Source = obj.comm
		except: pass
		for s in [obj.comm,obj.offs]:
			s.ViewObject.ShapeColor = (1.00,0.00,0.00)
			s.ViewObject.Transparency = 30
			obj.addObject(s)
		for s in [obj.s1, obj.s2]:
			s.Radius=1
			s.ViewObject.ShapeColor = (1.00,0.00,0.00)
			s.ViewObject.Transparency = 80
			obj.addObject(s)
		s=obj.s3
		s.Radius=10
		s.ViewObject.ShapeColor = (0.00,1.00,0.00)
		s.ViewObject.Transparency = 80
		obj.addObject(s)


	def die(self):
		try:
			print("DIE")
			for k in [self.offs,self.comm,self.s1,self.s2,self.s3,self.obj2]:
				print(k,str(k.Name))
				FreeCAD.ActiveDocument.removeObject(str(k.Name))
		except:
			sayexc()

	def execute(self,obj):
		#say(obj.Label)
		#say(obj.ViewObject.Visibility)
		try: self.Lock
		except: 
			self.Lock= False
			self.obj2=obj
		
		if not obj.ViewObject.Visibility: return
		if not self.Lock:
			self.Lock=True
			try:
				self.findCollision()
				say("findCollision done\n")
			except:
					sayexc("except Fehler beim execute")
			self.Lock=False

	def findCollision(self):
		obj=self.obj2

		C=self.obj2.stator
		B=self.obj2.traveller
		d=C.Shape.distToShape(B.Shape)

		dist=d[0]
		points=d[1]
		for poipair in points:
			#print poipair
			pass

		# process only one near point 
		p1=poipair[0]
		p2=poipair[1]

		m=FreeCAD.Vector((p1[0]+p2[0])/2,(p1[1]+p2[1])/2,(p1[2]+p2[2])/2)
		obj.s3.Placement.Base=m
		obj.s1.Placement.Base=p1
		obj.s2.Placement.Base=p2

		pl=[]
		for poipair in points:
			pl.append(poipair[0])

		if dist<0.001:
			s=B.Shape
			s2=C.Shape

			if obj.mode==1:
				obj.comm.Shape=s.common(s2)
			if obj.mode==2:
				try:
					s3=obj.comm.Shape
					t=s3.fuse(s.common(s2))
					obj.comm.Shape=t.removeSplitter()
				except:
					obj.comm.Shape=s.common(s2)
			if obj.hidemode == 1:
				obj.comm.ViewObject.Visibility=True
				obj.offs.ViewObject.Visibility=True
				
				obj.s3.ViewObject.Visibility=False
				obj.s1.ViewObject.Visibility=False
				obj.s2.ViewObject.Visibility=False
	#		wire.ViewObject.Visibility=True
		else:
			#print "Abstand"
			#print d
			if obj.hidemode == 1:
				obj.comm.ViewObject.Visibility=False
				obj.offs.ViewObject.Visibility=False
				if dist<5:
					obj.s3.ViewObject.Visibility=True
				else:
					obj.s3.ViewObject.Visibility=False
				if dist<40:
					obj.s1.ViewObject.Visibility=True
					obj.s2.ViewObject.Visibility=True
				else:
					obj.s1.ViewObject.Visibility=False
					obj.s2.ViewObject.Visibility=False

	#		wire.ViewObject.Visibility=False
		return

def createCollision(name='MyCollisionDetector',stator=None,traveller=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","stator","Base","stator").stator=stator
	obj.addProperty("App::PropertyLink","traveller","Base","traveller").traveller=traveller
	obj.addProperty("App::PropertyFloat","near1","Base","nearDistance ").near1=10
	obj.addProperty("App::PropertyFloat","near2","Base","nearDistance green").near2=5
	obj.addProperty("App::PropertyFloat","offset","Base","Tickness of the Colliosion offset").offset=1
	
	obj.addProperty("App::PropertyLink","s1","helper","s1")
	obj.addProperty("App::PropertyLink","s2","helper","s2")
	obj.addProperty("App::PropertyLink","s3","helper","s3")
	obj.addProperty("App::PropertyLink","comm","helper","common")
	obj.addProperty("App::PropertyLink","offs","helper","offset")
	obj.addProperty("App::PropertyInteger","mode","helper","1 only common, 2 additive commons ").mode=1
	obj.addProperty("App::PropertyInteger","hidemode","helper","1 auto, 2 off").hidemode=1
	
	_ViewProvider(obj.ViewObject)
	t=Detector(obj)
	
	return t



if __name__ == '__main__' and True:
	C=App.ActiveDocument.Cone
	B=App.ActiveDocument.Box
	t=createCollision("My Col",B,C)
	t.Proxy.Lock=False
	App.activeDocument().recompute()



