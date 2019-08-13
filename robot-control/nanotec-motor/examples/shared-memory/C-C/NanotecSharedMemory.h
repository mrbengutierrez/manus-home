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
#include <sstream>     // string stream function for casting

using namespace std; 




class NanotecSharedMemory
{
	private: // Variables
		
		// Pointer to the shared memory location
		char *_strPointer;
		
		// shared memory id number
		int _shmid;
		
		// Size in bytes of the shared memory location
		int _numBytes;
		
		
	private: // Methods
		// counts the number of delimiters in a sequence
		static int countDelimiters(char delimiter, char* sequence, int sequenceLength);
		
		static std::vector<std::string> splitString(std::string stringToSplit, std::string delimiter);
		
		// execute parsed input from memory
		static bool callFunctionUsingVector(std::vector<std::string> splittedStringVector);
		
	public: // Methods
		
		// initialize the shared memory location
		NanotecSharedMemory();
		~NanotecSharedMemory();
		
		// read memory location
		char* readMemory();	
		
		// write to memory location
		void writeMemory(char* sequenceToWrite);
		
		// execute instruction at memory location
		bool executeMemory();
	
};



