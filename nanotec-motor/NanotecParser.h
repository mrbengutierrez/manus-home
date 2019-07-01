#ifndef CLASS_NANOTECPARSER
#define CLASS_NANOTECPARSER


/**
 * This header file is responsible for string interface for the NanotecMotor.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 28, 2019
 * 
 */

#include <iostream> 
#include <stdio.h> 
#include <string.h> 
#include <stdlib.h> 
#include "unistd.h"  // time
#include <vector>   // vector for string container
#include <sstream>  // for string to memory address conversions
#include <unordered_map>     // for function map


#include "NanotecMotor.h"  // for executing functions
using namespace std; 




class NanotecParser
{
	//private: // Variables
		//std::unordered_map<std::string, void*> _functionMap;
	
	private: // Methods
		
		static int countDelimiters(char delimiter, char* sequence, int sequenceLength);
		
		static std::vector<std::string> splitString(std::string stringToSplit, std::string delimiter);
		
		// execute parsed input from memory
		static std::string callFunctionUsingVector(std::vector<std::string> splittedStringVector);
		
		// string to type conversion functions
		static double stringToDouble(std::string stringToConvert);
		static int stringToInt(std::string stringToConvert);
		static char* stringToCharPointer(std::string stringToConvert);
		static void* stringToVoidPointer(std::string stringToConvert);
		
		// type to string conversion functions
		static std::string  doubleToString(double doubleToConvert);
		static std::string intToString(int intToConvert);
		static std::string charPointerToString(char* charPointerToConvert);
		static std::string voidPointerToString(void* voidPointerToConvert);
		
		//Methods to interface with NanotecMotor.h
		
		static std::string nanotecMotor(std::vector<std::string> argumentVector);
		static std::string getID(std::vector<std::string> argumentVector);
		
		static std::string torqueMode( std::vector<std::string> argumentVector );
		static std::string angularVelocityMode( std::vector<std::string> argumentVector );
		static std::string angularPositionMode( std::vector<std::string> argumentVector );
		
		static std::string setTorque( std::vector<std::string> argumentVector );
		static std::string setAngularVelocity( std::vector<std::string> argumentVector );
		static std::string setRelativeAngularPosition( std::vector<std::string> argumentVector );
		static std::string setAbsoluteAngularPosition( std::vector<std::string> argumentVector );
		static std::string setAbsoluteAngularPositionShortestPath( std::vector<std::string> argumentVector );
		static std::string stop( std::vector<std::string> argumentVector );
		
		static std::string getTorque( std::vector<std::string> argumentVector );
		static std::string getAngularVelocity( std::vector<std::string> argumentVector );
		static std::string getAbsoluteAngularPosition( std::vector<std::string> argumentVector );
		static std::string readPhysicalEncoder( std::vector<std::string> argumentVector );
		
		static std::string closePort( std::vector<std::string> argumentVector );
		
		

	
	public: // Methods
		
		// constructor
		//NanotecParser();
		
		// parses string and executes using NanotecMotor.h
		static std::string execute(std::string stringToExecute);
		
		// join multiple strings using a delimiter
		static std::string stringJoiner( std::vector<std::string> stringVector, std::string deliminator );
};

#endif
