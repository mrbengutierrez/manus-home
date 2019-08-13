
import numpy as np
import scipy as sp
import matplotlib.pylab as plt
import random









class Kinematics:

    def __init__(self):
        # initialize lengths in inches
        self.L_6 = 0
        
        self.L_1 = 16
        self.L_2 = 12
        self.L_3 = self.L_2 + self.L_6 * np.sqrt(2)/2
        self.L_4 = self.L_1 + self.L_6 * np.sqrt(2)/2
        self.L_5 = 8

        # manus lengths
        #self.L_1 = 16
        #self.L_2 = 6
        #self.L_3 = 6
        #self.L_4 = 16
        #self.L_5 = 14
        #self.L_6 = 0

    def forwardKinematics(self,q_1,q_2):
        
        x_A = self.L_2*np.cos(q_1) - self.L_6/2;
        y_A = self.L_2*np.sin(q_1);
        x_B = self.L_1*np.cos(q_2) + self.L_6/2;
        y_B = self.L_1*np.sin(q_2);

        h = np.sqrt((y_B - y_A)**2 + (x_B - x_A)**2);
        delta_1 = np.arccos(h/(2*self.L_4));

        psi = np.arctan2(y_B - y_A, x_B - x_A);
        phi_1 = delta_1 + psi;
        phi_2 = np.pi - (phi_1 - 2*psi)

        x_D = x_A + self.L_4*np.cos(phi_1) + self.L_5*np.cos(phi_2);
        y_D = y_A + self.L_4*np.sin(phi_1) + self.L_5*np.sin(phi_2);

        return [x_D,y_D]

    def inverseKinematics(self,x,y):

        x_C = x - self.L_5 * cos(phi_2)
        y_C = y - self.L_5 * sin(phi_2)

        k_1 = np.sqrt( (x_C + self.L_6/2)**2 + y_C**2 )
        k_2 = np.sqrt( (x_c - self.L_6/2)**2 + y_C**2 )

        gamma_1 = np.arccos( (self.L_2**2 + k_1**2 - self.L_4**2) / (2 * self.L_2 * k_1) )
        gamma_2 = np.arccos( (self.L_1**2 + k_2**2 - self.L_3**2) / (2 * self.L_1 * k_2) )
        
        epsilon_1 = np.arctan2(y_C, x_C + L_6/2)
        epsilon_2 = np.arctan2(y_C, x_C - L_6/2)
        
        q_1 = epsilon_1 + gamma_1
        q_2 = epsilon_2 - gamma_2

        return [q_1,q_2]

    def plotWorkspaceUniform(self):
        """Plots the workspace base on valid joint angles"""

        # lower and upper limits on joint angles
        q_2_lower = 0
        q_2_upper = 1/2 * np.pi

        q_1_lower = 1/2 * np.pi
        q_1_upper = 1 * np.pi

        numPoints = 100
        q_1_points = sp.linspace(q_1_lower,q_1_upper,numPoints)
        q_2_points = sp.linspace(q_2_lower,q_2_upper,numPoints)
        x_points = []
        y_points = []
        #for _ in range(numPoints):
            #q_1 = random.uniform(q_lower, q_upper)
            #q_2 = random.uniform(q_lower,q_upper)
        for q_1 in q_1_points:
            for q_2 in q_2_points:
                coordinates = self.forwardKinematics(q_1,q_2)
                x_points.append( coordinates[0] )
                y_points.append( coordinates[1] )

        # use min and max points to make sure 0,0 is used as origin.
        xMin = min( x_points )
        yMin = min( y_points)
        x_points = [x - xMin for x in x_points]
        y_points = [y - yMin for y in y_points]
        
        plt.plot(x_points,y_points,".")
        plt.title("Workspace area")
        plt.xlabel("X axis (in)")
        plt.ylabel("Y axis (in)")
        plt.show()

    @staticmethod
    def isValidAngle(q_1,q_2):
        if (1/2 * np.pi < q_1) and (q_1 < np.pi) and (0 < q_2) and (q_2 < 1/2 * np.pi):
            return True

        if q_2 < q_1:
            return True
        
        return False
        
        
    def plotWorkspaceRandom(self):
        """Plots the workspace base on valid joint angles"""

        # lower and upper limits on joint angles
        q_lower = 0
        q_upper = np.pi

        numPoints = 10000

        x_points = []
        y_points = []
        for _ in range(numPoints):
            q_1 = random.uniform(q_lower, q_upper)
            q_2 = random.uniform(q_lower,q_upper)
            if Kinematics.isValidAngle(q_1,q_2):
                coordinates = self.forwardKinematics(q_1,q_2)
                x_points.append( coordinates[0] )
                y_points.append( coordinates[1] )

        # use min and max points to make sure 0,0 is used as origin.
        xMin = min( x_points )
        yMin = min( y_points)
        x_points = [x - xMin for x in x_points]
        y_points = [y - yMin for y in y_points]
        
        plt.plot(x_points,y_points,".")
        plt.title("Workspace area")
        plt.xlabel("X axis (in)")
        plt.ylabel("Y axis (in)")
        plt.show()















def main():
    Kin = Kinematics()
    Kin.plotWorkspaceUniform()
    #Kin.plotWorkspaceRandom()






if __name__ == "__main__":
    main()
