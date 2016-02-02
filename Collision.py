import FreeCAD
print "Module Collision started.!"

#-----------------------------------------

#--------------------------------------------

def col(actor,obstacles):
	
	av=actor.Shape.BoundBox
	for obl in obstacles:
		ov=obl.Shape.BoundBox
		if ov.XMin < av.XMax  and  ov.XMax > av.XMin and ov.YMin <= av.YMax and  ov.YMax >= av.YMin and  ov.ZMin <= av.ZMax and  ov.ZMax >= av.ZMin:
			print obl.Label
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
		return  '/home/thomas/.FreeCAD/Mod/Animation/icons/collider.png'
   
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
		self.s1=FreeCAD.ActiveDocument.addObject("Part::Sphere","s1")
		self.s2=FreeCAD.ActiveDocument.addObject("Part::Sphere","s2")
		self.s3=FreeCAD.ActiveDocument.addObject("Part::Sphere","s3")
		self.comm=FreeCAD.activeDocument().addObject("Part::MultiCommon","Common")
		self.comm.Shapes = [obj.traveller,obj.stator]
		for t in self.comm.Shapes:
			t.ViewObject.Visibility=True
		self.offs=FreeCAD.ActiveDocument.addObject("Part::Offset","Offset")
		self.offs.Source = self.comm
		for s in [self.comm,self.offs]:
			s.ViewObject.ShapeColor = (1.00,0.00,0.00)
			s.ViewObject.Transparency = 30
			obj.addObject(s)
		for s in [self.s1, self.s2]:
			s.Radius=1
			s.ViewObject.ShapeColor = (1.00,0.00,0.00)
			s.ViewObject.Transparency = 80
			obj.addObject(s)
		s=self.s3
		s.Radius=10
		s.ViewObject.ShapeColor = (0.00,1.00,0.00)
		s.ViewObject.Transparency = 80
		obj.addObject(s)


	def die(self):
		try:
			print "DIE"
			for k in [self.offs,self.comm,self.s1,self.s2,self.s3,self.obj2]:
				print k
				print str(k.Name)
				FreeCAD.ActiveDocument.removeObject(str(k.Name))
				print "done"
		except:
			sayexc()

	def execute(self,obj):
		#say(obj.Label)
		#say(obj.ViewObject.Visibility)
		if not obj.ViewObject.Visibility: return
		if not self.Lock:
			self.Lock=True
			try:
				self.findCollision()
				say("findCollision done\n")
			except:
					say("except Fehler beim execute")
			self.Lock=False

	def findCollision(self):

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
		self.s3.Placement.Base=m
		self.s1.Placement.Base=p1
		self.s2.Placement.Base=p2

		pl=[]
		for poipair in points:
			pl.append(poipair[0])
		#print pl
		#wire=Draft.makeWire(pl,closed=False,face=False,support=None)
		#wire.Points=pl

		if dist<0.001:
			#print "Collisoon"
			self.comm.ViewObject.Visibility=True
			self.offs.ViewObject.Visibility=True
			self.s3.ViewObject.Visibility=False
			self.s1.ViewObject.Visibility=False
			self.s2.ViewObject.Visibility=False
	#		wire.ViewObject.Visibility=True
		else:
			#print "Abstand"
			#print d
			self.comm.ViewObject.Visibility=False
			self.offs.ViewObject.Visibility=False
			if dist<5:
				self.s3.ViewObject.Visibility=True
			else:
				self.s3.ViewObject.Visibility=False
			if dist<40:
				self.s1.ViewObject.Visibility=True
				self.s2.ViewObject.Visibility=True
			else:
				self.s1.ViewObject.Visibility=False
				self.s2.ViewObject.Visibility=False

	#		wire.ViewObject.Visibility=False
		return

def createCollision(name='MyCollisionDetector',stator=None,traveller=None):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	obj.addProperty("App::PropertyLink","stator","Base","stator").stator=stator
	obj.addProperty("App::PropertyLink","traveller","Base","traveller").traveller=traveller
	obj.addProperty("App::PropertyFloat","near1","Base","nearDistance ").near1=10
	obj.addProperty("App::PropertyFloat","near2","Base","nearDistance green").near2=5
	obj.addProperty("App::PropertyFloat","offset","Base","Tickness of the Colliosion offset").offset=1
	
	_ViewProvider(obj.ViewObject)
	t=Detector(obj)
	
	return t



if __name__ == '__main__' and True:
	C=App.ActiveDocument.Cone
	B=App.ActiveDocument.Box
	t=createCollision("My Col",B,C)
	t.Proxy.Lock=False
	App.activeDocument().recompute()



