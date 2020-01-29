

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
#include <sys/socket.h> // for socket programming
#include <netinet/in.h>  // for network commands

#include "NanotecMotor.h"  // for executing functions
#include "NanotecParser.h" // for parsing instructions
using namespace std; 


#define PORT 8080 



// Server side C/C++ program to demonstrate Socket programming 

class NanotecNetworkServer
{
	private: // Variables
		
		// Parses string instructions that are sent in data register.
		NanotecParser* _Parser;
	
	private: // Methods
		
		
		
		
	public: // Methods
		
		// initialize the shared memory location
		NanotecNetworkServer();
		~NanotecNetworkServer();
		
		// read port
		std::string readFromPort();
		
		// write to port
		void writeToPort(std::string stringToWrite);
		
		// execute instruction at memory location
		bool execute();
		
		void start();
	
};
