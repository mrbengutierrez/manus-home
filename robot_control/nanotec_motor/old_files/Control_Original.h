#ifndef CLASS_CONTROL
#define CLASS_CONTROL
/**
 * Class Control, header file.
 *
 * Class to control a Nanotec PD2-C motor through USB in Linux.
 *
 * @author Moises Alencastre-Miranda
 * @date 05/17/2018
 * @version 1.5
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

/**
 * Defines.
 * Size of the image width and height.
 * Center of the circle X, Y.
 * Circle radio.
 * Initial coordinates X, Y for a degree zero (0).
 */
#define WI 900
#define HI 900
#define CX 450
#define CY 450
#define RA 400
#define IX 450
#define IY 50



/**
 * Class that includes the definition of the global variables and the methods.
 */
class Control
{
  private:

    /**
     * Object with the reference to the nanotec motor.
     */
    CommunicationNT *_nanotec;

    /**
     * Last angle, difference and torque.
     */
    double _lastAng, _lastDif, _lastTor;


  public:

    /**
     * Methods implemented in the code file (cpp).
     */

    // Basic methods: constructors and set properties.
    Control();
    ~Control();

    // Methods to manage the control.
    void menu();
    void torqueControlByAngleRange( double minA, double maxA );


  private:

    // Functions to do calculations and methods to display.
    int calculateSpringForce( double disAng );
    void message();
};

#endif
