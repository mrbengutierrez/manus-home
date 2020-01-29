"""
This file tests the kinematics for the cheaper MIT MANUS
Author: Benjamin Gutierrez
email: bengutie@mit.edu
"""





import numpy as np
import matplotlib.pylab as plt
import scipy as sp
from CheaperManusController import Kinematics as Kinematics


class Graphics:

    def __init__(self):
        """Constructor for Graphics object"""
        pass

    def plotPosition(x,y):
        """ plots the position of the robot on the screen"""
        pass



        

class TestKinematics:

    def __init__(self):
        """initializes the tester with an ArmSimulator"""
        self.armSimulator = Kinematics()

    def runAllTests(self):
        """Runs all the tests for the ArmSimulator"""
        self.testKinematics()
        self.testTorqueAndForce()
        self.testAngularVelocityAndVelocity()
    
    def testComplimentaryFunctions(self,listOfTuples,functionA,functionB,printStringList,isKinematics = False):
        q = np.array([np.pi/4,  (3/4)*np.pi])
        
        numPoints = len(listOfTuples)
        
        inList = [np.array(listOfTuples[i]) for i in range(numPoints)]
        
        outList = []
        for element in inList:
            if isKinematics:
                outList.append( functionA(element) )
            else:
                outList.append( functionA(element,q) )
        
        inListActual = []
        for element in outList:
            if isKinematics:
                inListActual.append( functionB(element) )
            else:
                inListActual.append( functionB(element,q) )
                
        for i in range(numPoints):
            inList[i] = tuple([round(elem,2) for elem in inList[i]])
            outList[i] = tuple([round(elem,2) for elem in outList[i]])
            inListActual[i] = tuple([round(elem,2) for elem in inListActual[i]])
            
        print("Testing " + printStringList[0] + " and " + printStringList[1])
        print(printStringList[2] + " (input): " + str(list(inList)))
        print(printStringList[3] + ": " + str(list(outList)))
        print(printStringList[2] + " (output): " + str(list(inListActual)))
        
        # check if expect joint angles equal actual joint angles
        epsilon = 0.0001
        isSuccess = True
        for i in range(numPoints):
            if np.abs( inList[i][0] - inListActual[i][0] ) > epsilon:
                isSuccess = False
            if np.abs( inList[i][1] - inListActual[i][1] ) > epsilon:
                isSuccess = False
        print("isSuccess: " + str(isSuccess))
        print("")
        

    def testKinematics(self):
        """tests the kinematics of the arm simulator"""
        degList = [(90.0,0.0), (135.0,45.0), (155.0,25.0), (180.0,90.0)]
        degToRad = np.pi/180.0;
        qList = [(tupleValue[0]*degToRad,tupleValue[1]*degToRad) for tupleValue in degList]
        #qList = [(np.pi/2,np.pi/4), ((3/4)*np.pi,np.pi/4),  ((3/4)*np.pi,np.pi/2)]
        functionA = self.armSimulator.forwardKinematics
        functionB = self.armSimulator.inverseKinematics
        printStringList = ["forwardKinematics","inverseKinematics","joint angles","position"]
        self.testComplimentaryFunctions(qList,functionA,functionB,printStringList,True)

    def testTorqueAndForce(self):
        """tests the torqueToForce and forceToTorque of the arm simulator"""
        
        tList = [(0,0),(0,10),(10,10),(30,-10),(-10,20),(-20,0)]
        functionA = self.armSimulator.torqueToForce
        functionB = self.armSimulator.forceToTorque
        printStringList = ["torqueToForce","ForceToTorque","torque","force"]
        self.testComplimentaryFunctions(tList,functionA,functionB,printStringList)

    def testAngularVelocityAndVelocity(self):
        """tests the angularVelocityToVelocity and velocityToAngularVelocity of the arm simulator"""

        qDotList = [(0,0),(0,10),(10,10),(30,-10),(-10,20),(-20,0)]
        functionA = self.armSimulator.angularVelocityToVelocity
        functionB = self.armSimulator.velocityToAngularVelocity
        printStringList = ["angularVelocityToVelocity","velocityToAngularVelocity","angular velocity", "velocity"]
        self.testComplimentaryFunctions(qDotList,functionA,functionB,printStringList)

    
        
        
    





def main():
    tester = TestKinematics()
    tester.runAllTests()

if __name__ == "__main__":
    main()
