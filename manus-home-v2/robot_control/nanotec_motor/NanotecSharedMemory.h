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
#include "NanotecParser.h" // for parsing instructions
using namespace std; 

#define DATA_KEY 65;
#define STATUS_KEY 88;



class NanotecSharedMemory
{
	private: // Variables
		
		// Pointers to the shared memory location
		
		/**
		 * _dataSharedMemory manages the data that is transferred between functions.
		 * clients can send commands to be executed, and servers can send return values back
		 * 
		 */
		SharedMemory * _dataSharedMemory;
		
		/**
		 * _statusSharedMemory manages the status of memory transfer
		 * clients write "start" when they have written to the data memory
		 * servers write "end" when they have executed the instruction and written to data memory
		 */
		SharedMemory * _statusSharedMemory;
		
		// Parses string instructions that are sent in data register.
		NanotecParser* _Parser;
	
	private: // Methods
		
		
		
		
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
		
		void start();
	
};

#endif


