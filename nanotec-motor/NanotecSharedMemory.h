#ifndef CLASS_NANOTECSHAREDMEMORY
#define CLASS_NANOTECSHAREDMEMORY

/**
 * This header file is responsible for managing the shared memory interface for the NanotecMotor.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 26, 2019
 * 
 */

#include <iostream> 
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <stdio.h> 
#include <string.h> 
#include <stdlib.h> 
#include "unistd.h"  // time
#include <vector>   // vector for string container

#include "NanotecMotor.h"  // for executing functions
#include "SharedMemory.h"  // include shared memory objects
using namespace std; 



class NanotecSharedMemory
{
	private: // Variables
		
		// Pointer to the shared memory location
		SharedMemory * _dataSharedMemory;
		SharedMemory * _statusSharedMemory;
		
	
	private: // Methods
		
		static int countDelimiters(char delimiter, char* sequence, int sequenceLength);
		
		static std::vector<std::string> splitString(std::string stringToSplit, std::string delimiter);
		
		// execute parsed input from memory
		static bool callFunctionUsingVector(std::vector<std::string> splittedStringVector);
		
		
		
	public: // Methods
		
		// initialize the shared memory location
		NanotecSharedMemory();
		~NanotecSharedMemory();
		
		// read memory location
		std::string readData();
		std::string readStatus();
		
		// write to memory location
		void writeData(std::string stringToWrite);
		void writeStatus(std::string stringToWrite);
		
		// execute instruction at memory location
		bool executeMemory();
	
};

#endif


