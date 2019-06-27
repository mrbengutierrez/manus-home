/**
 * This header file is responsible for managing the shared memory interface
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


using namespace std; 


class SharedMemory
{
	private: // Variables
		
		// Pointer to the shared memory location
		char *_strPointer;
		
		// shared memory id number
		int _shmid;
		
		// Size in bytes of the shared memory location
		int _numBytes;
		
		
	private: // Methods
		
	public: // Methods
		
		// initialize the shared memory location
		SharedMemory(const int keyValue = 65, const int numBytes = 1024);
		~SharedMemory();
		
		// read memory location
		char* readMemory();	
		
		// write to memory location
		void writeMemory(char* sequenceToWrite);
	
};
