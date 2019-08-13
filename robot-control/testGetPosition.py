
import time
from CheaperManusController import ArmController




def testGetPosition():
	arm = ArmController()
	while(true):
		position = arm.getPostion()
		x = position[0]
		y = position[1]
		print("x: " + str(x) + ",y: " + str(y))
		print("")
		time.Sleep(1) # delay one second
		

def main():
	testGetPosition()

if __name__ == "__main__":
	main()
