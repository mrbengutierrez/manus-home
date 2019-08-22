#ifndef CLASS_NANOTECMOTOR
#define CLASS_NANOTECMOTOR
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
#define GEAR_RATIO 10 // gear ratio of the gearbox that is added.

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
    
    // ID number of the motor
    int _ID;   
    char* _serialPort;
    
    // for keeping track of multi-turn rotor configurations
    int _initialEncoderValue;
    int _encoderValueOffset;
    
    
  public:

    /**
     * Methods implemented in the code file (cpp).
     */

    // Basic methods: constructors and set properties.
    //NanotecMotor(); // default constructor, only for initializing containers
    NanotecMotor(const char *serialPort, const int ID = 0);
    ~NanotecMotor();
    NanotecMotor(const NanotecMotor &oldNanotecMotor); // copy constructor
    NanotecMotor& operator=(const NanotecMotor &oldNanotecMotor); // assignment constructor
    //NanotecMotor* operator=(const NanotecMotor &oldNanotecMotor);
    
    // method to get the ID number of the motor
    int getID();
    char* getSerialPort();
    
    // Modes of Operation
    void torqueMode(int torque = 0, int maxTorque = 1000, int maxCurr = 1800, int nomCurr = 1800, int slope = 1000);
    void angularVelocityMode(int angVel = 0);
    void angularPositionMode(double angPos = 0.0, int angVel = 200);
    
    // Methods to control motor
    void setTorque(int torque);
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
    
    // function to convert degrees to encoder ticks
    int degreesToVirtualEncoderTicks(double degrees);
    int degreesToPhysicalEncoderTicks(double degrees);
    
    // calculates sign of a value
    double sign(double value);
};




#endif
