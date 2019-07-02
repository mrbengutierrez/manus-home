#ifndef CLASS_NANOTECMOTORCONTAINER
#define CLASS_NANOTECMOTORCONTAINER


/**
 * This header file is responsible for managing multiple NanotecMotor.h objects
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date July 2, 2019
 * 
 */

#include <iostream> 
#include <stdio.h> 
#include <string.h> 
#include <stdlib.h> 
#include <vector>     // for function map


#include "NanotecMotor.h"  // for executing functions
using namespace std; 

#define maxNumberofMotors 100


class NanotecMotorContainer
{
	private: // Variables
	
		// vectors maintain rep invariant
		// ideally it would be better to use a map for constant time lookups
		// however there were issues in getting the NanotecParser to work when
		// using a map to maintain the rep invariant.
		std::vector<std::string> _serialPortVector; // "serial port" : motor_pointer
		NanotecMotor* _nanotecMotorArray[maxNumberofMotors];
		
		int _numMotors;
	
	public: // Methods
	
		NanotecMotorContainer();
		
		void insert(std::string serialPort, NanotecMotor* motor);
		
		bool contains(std::string serialPort);
		
		NanotecMotor* getMotor(std::string serialPort);
		
		void removeMotor(std::string serialPort);			
};


#endif
