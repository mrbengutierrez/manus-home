"""
This file constructs an arm simulator for the cheaper MIT MANUS

Author: Benjamin Gutierrez
email: bengutie@mit.edu
"""





import numpy as np
import matplotlib.pylab as plt
import scipy as sp


class Graphics:

    def __init__(self):
        """Constructor for Graphics object"""
        pass

    def plotPosition(x,y):
        """ plots the position of the robot on the screen"""
        pass



        

class TestArmSimulator:

    def __init__(self):
        """initializes the tester with an ArmSimulator"""
        self.armSimulator = ArmSimulator()

    def runAllTests(self):
        """Runs all the tests for the ArmSimulator"""
        self.testKinematics()
        self.testTorqueAndForce()
        self.testAngularVelocityAndVelocity()

    def testKinematics(self):
        """tests the kinematics of the arm simulator"""

        # construct lists of joint angles
        numPoints = 5
        q1List = np.linspace(np.pi/2, (3/4)*np.pi,numPoints)
        q2List = np.linspace(np.pi/4, np.pi/2,numPoints)

        # use forwardKinematics to convert joint angles to position
        xList = []
        yList = []
        for i in range(numPoints):
            position = self.armSimulator.forwardKinematics(q1List[i],q2List[i])
            xList.append( position[0] )
            yList.append( position[1] )

        # use inverseKinematics to convert position back into joint angles
        q1ListTest = []
        q2ListTest = []
        for i in range(numPoints):
            angles = self.armSimulator.inverseKinematics(xList[i],yList[i])
            q1ListTest.append( angles[0] )
            q2ListTest.append( angles[1] )

        # print the results
        print("testKinematics")
        print("q1List (input): " + str(q1List))
        print("q2List (input): " +str(q2List))
        print("xList: " + str(xList))
        print("yList: " + str(yList))
        print("q1List (output): " + str(q1ListTest))
        print("q2List (output): " + str(q2ListTest))

        # check if expect joint angles equal actual joint angles
        epsilon = 0.0001
        isSuccess = True
        for i in range(numPoints):
            if np.abs( q1List[i] - q1ListTest[i] ) > epsilon:
                isSuccess = False
            if np.abs( q2List[i] - q2ListTest[i] ) > epsilon:
                isSuccess = False
        print("isSuccess: " + str(isSuccess))
        print("")

    def testTorqueAndForce(self):
        """tests the torqueToForce and forceToTorque of the arm simulator"""

        # construct lists of torques
        numPoints = 6
        t1List = [0,0,10,30,-10,-20]
        t2List = [0,10,10,-10,20,0]

        # use torqueToForce to convert torque to force
        FxList = []
        FyList = []
        for i in range(numPoints):
            forces = self.armSimulator.torqueToForce(t1List[i],t2List[i])
            FxList.append( forces[0] )
            FyList.append( forces[1] )

        # use forceToTorque to convert force back into torque
        t1ListTest = []
        t2ListTest = []
        for i in range(numPoints):
            torques = self.armSimulator.forceToTorque(FxList[i],FyList[i])
            t1ListTest.append( torques[0] )
            t2ListTest.append( torques[1] )

        # print the results
        print("test torqueToForce and forceToTorque")
        print("t1List (input): " + str(t1List))
        print("t2List (input): " +str(t2List))
        print("FxList: " + str(FxList))
        print("FyList: " + str(FyList))
        print("t1List (output): " + str(t1ListTest))
        print("t2List (output): " + str(t2ListTest))

        # check if expect joint angles equal actual joint angles
        epsilon = 0.0001
        isSuccess = True
        for i in range(numPoints):
            if np.abs( t1List[i] - t1ListTest[i] ) > epsilon:
                isSuccess = False
            if np.abs( t2List[i] - t2ListTest[i] ) > epsilon:
                isSuccess = False
        print("isSuccess: " + str(isSuccess))
        print("")

    def testAngularVelocityAndVelocity(self):
        """tests the angularVelocityToVelocity and velocityToAngularVelocity of the arm simulator"""

        # construct lists of torques
        numPoints = 6
        t1List = [0,0,10,30,-10,-20]
        t2List = [0,10,10,-10,20,0]

        # use angularVelocityToVelocity to convert angular velocity to velocity
        FxList = []
        FyList = []
        for i in range(numPoints):
            forces = self.armSimulator.angularVelocityToVelocity(t1List[i],t2List[i])
            FxList.append( forces[0] )
            FyList.append( forces[1] )

        # use velocityToAngularVelocity to convert velocity to angular velocity
        t1ListTest = []
        t2ListTest = []
        for i in range(numPoints):
            torques = self.armSimulator.velocityToAngularVelocity(FxList[i],FyList[i])
            t1ListTest.append( torques[0] )
            t2ListTest.append( torques[1] )

        # print the results
        print("test angularVelocityToVelocity and velocityToAngularVelocity")
        print("t1List (input): " + str(t1List))
        print("t2List (input): " +str(t2List))
        print("FxList: " + str(FxList))
        print("FyList: " + str(FyList))
        print("t1List (output): " + str(t1ListTest))
        print("t2List (output): " + str(t2ListTest))

        # check if expect joint angles equal actual joint angles
        epsilon = 0.0001
        isSuccess = True
        for i in range(numPoints):
            if np.abs( t1List[i] - t1ListTest[i] ) > epsilon:
                isSuccess = False
            if np.abs( t2List[i] - t2ListTest[i] ) > epsilon:
                isSuccess = False
        print("isSuccess: " + str(isSuccess))
        print("")

    
        
        
    
class ArmSimulator:
    def __init__(self):
        inchesToMeters = 0.0254;
        self.l1 = 13.25 * inchesToMeters
        self.l2 = 13.25 * inchesToMeters
        self.l3 = 15.5 * inchesToMeters
        self.l4 = 15.5 * inchesToMeters
        self.d = 3 * inchesToMeters

    def forwardKinematics(self,q1,q2):
        """converts joint angles to end effector position

        Parameters:
        q1 (float): left joint angle
        q2 (float): right joint angle

        Returns:
        (tuple of floats): (x,y) The end effector position
        """
        x_d = self.l2*np.cos(q2) + self.d
        y_d = self.l2*np.sin(q2)
        x_c = self.l1*np.cos(q1) - self.d
        y_c = self.l1*np.sin(q1)

        psi = np.arctan2(y_d - y_c, x_d - x_c)
        
        h = np.sqrt( (y_d - y_c)**2 + (x_d - x_c)**2 )
        delta = np.arccos( (self.l3**2 + h**2 - self.l4**2) / (2*self.l3*h) )

        theta3 = delta + psi
        
        x = x_c + self.l3*np.cos(theta3)
        y = y_c + self.l3*np.sin(theta3)

        return (x,y)

    def inverseKinematics(self,x,y):
        """converts end effector position to joint angles

        Parameters:
        x (float): x end effector position in meters
        y (float): y end effector position in meters

        Returns:
        (tuple of floats): (x,y) The joint parameters
        """

        # x,y --> q1
        alpha1 = np.arctan2(y,x+self.d)
        r1 = np.sqrt((x+self.d)**2 + y**2)
        gamma1 = np.arccos( (self.l1**2 + r1**2 - self.l3**2) / (2*self.l1*r1) )
        q1 = alpha1 + gamma1

        # x,y --> q2
        alpha2 = np.arctan2(y,x-self.d)
        r2 = np.sqrt((x-self.d)**2 + y**2)
        gamma2 = np.arccos( (r2**2 + self.l2**2 - self.l4**2) / (2 * self.l2 * r2) )
        q2 =  alpha2 - gamma2

        return (q1,q2)

    def Jacobian(self,q1,q2):
        """Returns the Jacobian matrix for a given set of joint angles

        Parameters:
        q1 (float): left joint angle in radians
        q2 (float): right joint angle in radians

        Returns:
        (numpy.matrix): the Jacobian matrix
        """
        pass

    def computeActualJacobian(self,q):
        """Returns the Jacobian matrix for a given set of joint angles
            using the actual Jacobian

        Parameters:
        q (tuple of floats): joint angles in radians, q[0] is left, q[1] is right

        Returns:
        (2x2 numpy.array): the Jacobian matrix
        """
        cos = np.cos
        sin = np.sin
        acos = np.arccos
        atan2 = np.arctan2
        real = lambda x: x.real
        imag = lambda x: x.imag

        dXdQ1 = - l1*sin(q1) + l3*sin(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l1*cos(q1)) - imag(l1*sin(q1)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l1*sin(q1)) + imag(l1*cos(q1)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
        dXdQ2 = -l3*sin(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l2*cos(q2)) - imag(l2*sin(q2)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l2*sin(q2)) + imag(l2*cos(q2)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
        dYdQ1 = l1*cos(q1) - l3*cos(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l1*sin(q1)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l1*cos(q1)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l1*cos(q1)) - imag(l1*sin(q1)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l1*sin(q1)) + imag(l1*cos(q1)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
        dYdQ2 = l3*cos(atan2(l2*sin(q2) - l1*sin(q1), 2*d - l1*cos(q1) + l2*cos(q2)) + acos(((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2))))*(((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))/(2*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(1/2)) - ((2*l2*sin(q2)*(2*d - l1*cos(q1) + l2*cos(q2)) + 2*l2*cos(q2)*(l1*sin(q1) - l2*sin(q2)))*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2))/(4*l3*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)**(3/2)))/(1 - ((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2 + l3**2 - l4**2)**2/(4*l3**2*((l1*sin(q1) - l2*sin(q2))**2 + (2*d - l1*cos(q1) + l2*cos(q2))**2)))**(1/2) + (((real(l2*cos(q2)) - imag(l2*sin(q2)))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2))) + ((real(l2*sin(q2)) + imag(l2*cos(q2)))*(real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2))))/(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)*(2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2)/((real(l2*sin(q2)) - real(l1*sin(q1)) + 2*imag(d) - imag(l1*cos(q1)) + imag(l2*cos(q2)))**2 + (2*real(d) - real(l1*cos(q1)) + real(l2*cos(q2)) + imag(l1*sin(q1)) - imag(l2*sin(q2)))**2))
        return np.array([[dXQ1,dXQ2],[dYdQ1,dYdQ2]])


    def torqueToForce(self,t1,t2):
        """Converts joint torques to enpoint forces

        Parameters:
        t1 (float): left joint torque in newton-meters
        t2 (float): right joint angle in newton-meters

        Returns:
        (tuple of floats): (fx,fy) the end effector forces
        """
        # TODO
        return (0,0)

    def forceToTorque(self,fx,fy):
        """Converts endpoint forces to joint torques

        Parameters:
        fx (float): x endpoint force in newtons
        fy (float): y endpoint force in newtons

        Returns:
        (tuple of floats): (t1,t2) the joint torques
        """
        # TODO
        return (0,0)

    def angularVelocityToVelocity(self,qDot1,qDot2):
        """Converts joint angular velocities to end effector velocity

        Parameters:
        qDot1 (float): left joint angular velocity in radians per second
        qDot2 (float): right joint angular velocity in radians per second

        Returns:
        (tuple of floats): (vx,vy) the end effector velocity
        """
        # TODO
        return (0,0)

    def velocityToAngularVelocity(self,vx,vy):
        """Converts the end effector velocity to joint angular velocities

        Parameters:
        vx (float): x endpoint velocity
        vy (float): y endpoint velocity

        Returns:
        (tuple of floats): (qDot1,qDot2) the joint angular velocities
        """
        # TODO
        return (0,0)      

    def movePosition(x,y):
        """moves robot arm simulator to position"""
        pass

    def moveAngle(q1,q2):
        """moves robot arm simulator to angle"""
        return



def main():
    tester = TestArmSimulator()
    tester.runAllTests()

if __name__ == "__main__":
    main()

