
import numpy as np

def force1(x,y,z,p,t=0):
	''' force on place x,y,z under velocity p at time t '''
	# no force if the speed is more than 5
	if np.max(np.abs(p))>5:
		return [0,0,0]

	return [0,0,0.5]



def force2(x,y,z,p,t=0):

	# test force 
	if t>70:
		return (0,0,0)

	if z>200 and x<y:
		return (4,2,-14)

	if z>200 and x>=y:
		return (4,2,4)

	return (0,0,0.3)


def damperX(x,y,z,p,t=0):
	alpha=np.arctan2(x,y)

	if alpha>0 and alpha<np.pi*1/3: return(1,1,0.2)
	if alpha>1 and alpha<1.4: return(1,1,0.1)
	if z>20:
		return(0.4,0.4,0)

	return (0.99,1.0,0.99)


def damper2(x,y,z,p,t=0):
	alpha=np.arctan2(x,y)

	if alpha>np.pi*1/3: return(1,1,0.5)
	if alpha<-np.pi*1/2: return(1,1,0.01)

	return (1,1,1)


# drehen
def force3(x,y,z,p,t=0):
	k=0.002
	m=0.0005
	#if x**2+y**2 >3600:
	if x**2+y**2 >100:
		return(k*y-m*x,-k*x-m*y,-0.5)
	else:
		return(k*y,-k*x,-0.2)
	return (0,0,-1)


# ausbreiten und schnell fallen
def force4(x,y,z,p,t=0):
	#return(0.,0,-1)
	return(0.01*y,0.01*x,-1)


def nodamper(x,y,z,p,t=0):
	return (0.9,0.9,1)

def simpleforce(x,y,z,p,t=0):
	if z<-20 and z>-50:
		return (-0.01*x, -0.01*y,-0.5)
	if z<=-70:
		return (0.01*np.sin(z*np.pi/20)*x, 0.01*np.sin(z*np.pi/20)*y,-0.1)
	return (0,0,-1)


force=force4
myforce=force4
mydamper=damper2
