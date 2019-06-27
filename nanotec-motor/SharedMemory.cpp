/**
 * This header file is definitions of the shared memory interface for the NanotecSharedMemory.h
 * 
 * @author Benjamin Gutierrez (bengutie@mit.edu)
 * @date June 26, 2019
 * 
 */

#include "SharedMemory.h"



SharedMemory::SharedMemory(const int keyValue, const int numBytes)
{
	// ftok to generate unique key 
    key_t key = ftok("shmfile",keyValue); 
  
    // shmget returns an identifier in shmid 
    _numBytes = numBytes; // number of bytes of the shared memory location
    _shmid = shmget(key,_numBytes,0666|IPC_CREAT); 
  
    // shmat to attach to shared memory 
    _strPointer = (char*) shmat(_shmid,(void*)0,0);
    
    // Write empty character '\0' as the empty sequence
    char emptyChar = '\0';
    char * emptyCharPointer = &emptyChar;
    this->writeMemory(emptyCharPointer); 
    
}

SharedMemory::~SharedMemory()
{
	//detach from shared memory  
    shmdt(_strPointer); 
    
    // destroy the shared memory 
    shmctl(_shmid,IPC_RMID,NULL); 
}

 /**
  * Returns a copy of the string in the shared memory location
  */
char* SharedMemory::readMemory()
{
	char* dataPointer = (char *)malloc(sizeof(char)*_numBytes);
	strcpy( dataPointer, _strPointer );
	return dataPointer; 
}

/** Writes a sequence of characters to the shared memory location
 * 
 * @param sequenceToWrite sequence to write to shared memory location
 */
void SharedMemory::writeMemory(char* sequenceToWrite)
{
	strcpy(_strPointer,sequenceToWrite);
}





/*  TESTING
int main() 
{ 
    int uniqueKey = 0x65;
    SharedMemory *memObjPointer = new SharedMemory(uniqueKey);
    
    while(true) {
		cout << endl;
		
		
		
		char* dataRead = memObjPointer->readMemory();
		cout << "dataRead (before): " << dataRead << endl;
		
		memObjPointer->writeMemory("bob");
		
		dataRead = memObjPointer->readMemory();
		cout << "dataRead (after): " << dataRead << endl;
		
		memObjPointer->writeMemory("sally mae");
		sleep(2);
	}
	
	delete memObjPointer;
  
    return 0; 
} 
*/
