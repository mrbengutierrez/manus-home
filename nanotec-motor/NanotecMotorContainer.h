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
#include <map>     // for function map


#include "NanotecMotor.h"  // for executing functions
using namespace std; 


class NanotecMotorContainer
{
	private: // Variables
		std::map<std::string, NanotecMotor> _motorMap; // "serial port" : motor_pointer
	
	public: // Methods
		
		void insert(std::string serialPort, NanotecMotor motor);
		
		bool contains(std::string serialPort);
		
		NanotecMotor getMotor(std::string serialPort);
		
		void removeMotor(std::string serialPort);			
};


#endif
