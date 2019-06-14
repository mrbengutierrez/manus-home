#ifndef CLASS_CONTROL
#define CLASS_CONTROL
/**
 * Class NanotecMotor, header file.
 *
 * Class to control a Nanotec PD2-C motor through USB in Linux.
 *
 * @author Moises Alencastre-Miranda
 * @author Benjamin Gutierrez
 * @date 06/10/2019
 * @version 1.6
 */


/**
 * Including C++ libraries for display on screen, respectively.
 */
//#include <unistd.h>
#include <iostream>

/**
 * Own libraries.
 */
#include "CommunicationNT.h"

// Global Constant Definitions
#define VIRTUAL_TICKS_PER_REV 2000 // Number of virtual encoder ticks for 1 revolution.
#define PHYSICAL_TICKS_PER_REV 4096 // Number of physical encoder ticks for 1 revolution.

/**
 * Class that includes the definition of the global variables and the methods.
 */
class NanotecMotor
{
  private:

    /**
     * Object with the reference to the nanotec motor.
     */
    CommunicationNT *_nanotec;
    
    // keep track of motor mode
    enum _motorModeType {NONE, TORQUE, ANGULAR_VELOCITY, ANGULAR_POSITION};
    _motorModeType _motorMode;

    //Last angle, difference and torque.
    double _lastAng, _lastDif, _lastTor;
    
    // ID number of the motor
    int _ID;
    
    
  public:

    /**
     * Methods implemented in the code file (cpp).
     */

    // Basic methods: constructors and set properties.
    NanotecMotor(const char *serialPort, const int ID = 0);
    ~NanotecMotor();
    
    // method to get the ID number of the motor
    int getID();

    // Methods to test torque command of motor
    void menu();
    
    // Modes of Operation
    void torqueMode(int torque = 0, int maxTorque = 1000, int maxCurr = 1800, int nomCurr = 1800, int slope = 1000);
    void angularVelocityMode(int angVel = 0);
    void angularPositionMode(double angPos = 0.0, int angVel = 200);
    
    // Methods to control motor
    void setTorque(int torque);
    void torqueControlByAngleRange( double minA, double maxA );
    void setAngularVelocity( int angVel );   
    void setRelativeAngularPosition( double angPos, int angVel = 200 );
    void setAbsoluteAngularPosition( double angPos, int angVel = 200 );
    void setAbsoluteAngularPositionShortestPath( double angPos, int angVel = 200 );
    void stop();
    
    // Methods to get information from motor
    int getTorque();
    int getAngularVelocity();
    double getAbsoluteAngularPosition();
    int readPhysicalEncoder();
    
    // Method to close the serial port connection
    void closePort();


  private:

    // Functions to do calculations and methods to display.
    int calculateSpringForce( double disAng );
    void message();
    
    // function to convert degrees to encoder ticks
    int degreesToVirtualEncoderTicks(double degrees);
    int degreesToPhysicalEncoderTicks(double degrees);
    
    // calculates sign of a value
    double sign(double value);
};




#endif
