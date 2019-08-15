from CheaperManusController import ArmController
import time
import numpy as np



def printRobotInformation(arm):
	print("joint angles (deg)" + str(list(arm.getJointAngles()*180.0/np.pi)))
	print("position (m): " + str(list(arm.getPosition())))
	print("velocity (m/s): " + str(list(arm.getVelocity())))
	print("force (Nm): " + str(list(arm.getForce())))
	print("")
	

def testForceControl():
	arm = ArmController()
	kx = 50.0
	bx = 500.0
	ky = 50.0
	by = 500.0
	K = np.array([[kx,bx],[ky,by]])
	
	x = 0.0
	y = 0.4
	r = np.array([x,y])
	
	previousTime = time.time()
	#count = 0
	while(True):
		arm.setImpedance(K,r)
		#time.sleep(0.1)
		
		if (time.time() - previousTime > 5):	
			printRobotInformation(arm)
			previousTime = time.time()
		
		#count += 1
		#if (count % 100 == 0):
			#print("Count: " + str(count))
def main():
	testForceControl()
	
	
if __name__ == "__main__":
	main()
