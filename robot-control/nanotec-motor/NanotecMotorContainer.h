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
	
		// array maintain rep invariant, chosen to manage memory of motors
		NanotecMotor* _nanotecMotorArray[maxNumberofMotors];
		
		int _numMotors;
	
	private: // Methods
		int getMotorIndex(std::string serialPort);
	
	public: // Methods
	
		NanotecMotorContainer();
		
		void insert(NanotecMotor* motor);
		
		bool contains(std::string serialPort);
		
		NanotecMotor* getMotor(std::string serialPort);
		
		void removeMotor(std::string serialPort);			
};


#endif
