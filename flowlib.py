
import numpy as np

def force(x,y,z,p,t=0):
	''' force on place x,y,z under velocity p at time t '''
	# no force if the speed is more than 5
	if np.max(np.abs(p))>5:
		return [0,0,0]

	return [0,0,0.5]



def forceTest(x,y,z,p,t=0):

	# test force 
	if t>70:
		return (0,0,0)

	if z>200 and x<y:
		return (4,2,-14)

	if z>200 and x>=y:
		return (4,2,4)

	return (0,0,0.3)


def force(x,y,z,p,t=0):
	return forceTest(x,y,z,p,t)




def damper(x,y,z,p,t=0):
	alpha=np.arctan2(x,y)

	if alpha>0 and alpha<0.1: return(1,1,0.2)
	if alpha>0.8 and alpha<1.1: return(1,1,0.1)

	return (1,1,1)


def force(x,y,z,p,t=0):
	k=0.002
	m=0.003
	#if x**2+y**2 >3600:
	if x**2+y**2 >100:
		return(k*y-m*x,-k*x-m*y,-1)
	else:
		return(k*y,-k*x,-0)
	return (0,0,-1)

