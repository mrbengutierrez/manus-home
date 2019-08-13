/**
 * This cpp file is definitions of the shared memory interface for the SharedMemory.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 26, 2019
 * 
 */


#include "NanotecSharedMemory.h"



SharedMemory::SharedMemory(const int keyValue, const int numBytes)
{
	/*
	//destroy shared memory
	key_t key_test = keyValue;
	int shmid_test = shmget(key_test,_numBytes,0666|IPC_CREAT); 
	shmctl(shmid_test,IPC_RMID,NULL); 
	
	// ftok to generate unique key 
    key_t key = ftok("shmfile",keyValue); 
    cout << "keyValue: " << keyValue << ", key: " << key << endl;
    */
  
    // shmget returns an identifier in shmid 
    _numBytes = numBytes; // number of bytes of the shared memory location
    _shmid = shmget(keyValue,_numBytes,0666|IPC_CREAT); 
  
    // shmat to attach to shared memory 
    _strPointer = (char*) shmat(_shmid,(void*)0,0);
    
    // Write empty string as the empty sequence
    this->writeMemory(""); 
    
    // Allocate memory for lastReadPointer
    _lastReadPointer = (char *)malloc(sizeof(char)*_numBytes);
    
}

SharedMemory::~SharedMemory()
{
	//detach from shared memory  
    shmdt(_strPointer); 
    
    // destroy the shared memory 
    shmctl(_shmid,IPC_RMID,NULL); 
    
    // allocated memory
    free( _lastReadPointer);
    
}

 /**
  * Returns a copy of the string in the shared memory location
  */
std::string SharedMemory::readMemory()
{

	strcpy( _lastReadPointer, _strPointer );
	std::string stringRead( _lastReadPointer );
	return stringRead; 
}

/** Writes a string of characters to the shared memory location
 * 
 * @param stringToWrite string to write to shared memory location
 */
void SharedMemory::writeMemory(std::string stringToWrite)
{
	const char* sequenceToWrite = stringToWrite.c_str();
	strcpy(_strPointer,sequenceToWrite);
}





/*  TESTING
int main() 
{ 
    int uniqueKey = 65;
    int numBytes = 1024;
    SharedMemory *memObjPointer = new SharedMemory(uniqueKey,numBytes);
    
    long count = 0;
    while(count < 10) {
		//cout << endl;
		
		
		
		std::string dataRead = memObjPointer->readMemory();
		//cout << "dataRead (before): " << dataRead << endl;
		
		memObjPointer->writeMemory("bob");
		
		dataRead = memObjPointer->readMemory();
		//cout << "dataRead (after): " << dataRead << endl;
		
		memObjPointer->writeMemory("sally mae");
		//sleep(2);
		//count++;
	}
	
	delete memObjPointer;
  
    return 0; 
} 
*/
