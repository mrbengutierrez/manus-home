// in this example the operationmode will be set to position mode and the motor will move between 2 positions that can be set via "VMM Input" Objects (for exmaple in the configuration file)

//1. Step: mapping the frequently used SDO´s
map U16 ControlWord as output 0x6040:00
map U16 StatusWord as input 0x6041:00
map S32 TargetPosition as output 0x607A:00
map U32 Inputs as input 0x60FD:00
map U32 ProfileVelocity as output 0x6081:00
map S32 Position1 as input 0x2400:01
map S32 Position2 as input 0x2400:02
map S32 Speed1 as input 0x2400:03
map S32 Speed2 as input 0x2400:04
map S32 Pause as input 0x2400:05
map S32 Pause2 as input 0x2400:06
map S32 Time as output 0x2500:01

#include "wrapper.h"

//2. Step: call Main function and set the speed and mode of operation

void user()
{
	od_write(0x6060,0x00, 1);							// set the mode of operation to profile position
	
	Out.TargetPosition = In.Position1;					// setting the target position to the value written in 0x2400:01 
	
	Out.ProfileVelocity = In.Speed1;					// setting the profile velocity to the value written in 0x2400:03 
	
//3. Step: switch on the state machine
	sleep(In.Pause);                       // setting the sleep time to the value written in 0x2400:05 
	Out.ControlWord = 0x6;				// switch to the "enable voltage" state
	do 	{
		yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);    // wait until drive is in state "enable voltage"	
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0001

	
	
	Out.ControlWord = 0x7;	// switch to the "switched on" state
	do 	{
			yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wait until drive is in state "switched on" 
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0011		

	
	while(true)    	// endless loop
	{	
	
			Out.ControlWord = 0xF;	// switch to the "enable operation" state
			do 	{
					yield();						// waiting for the next cycle (1ms)
				}
				while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
				// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
			Out.TargetPosition = In.Position1;						// setting the target position to the value written in 0x2400:01 	
			Out.ProfileVelocity = In.Speed1;					// setting the profile velocity to the value written in 0x2400:03 
	
			Out.ControlWord = 0x5F;					// start positioning,  relative	
			yield();
			
			while((In.StatusWord & 0x400) !=0x400)           //wait till "Target reached" 10 bit is high 
			{
				Out.Time+=1;			//count time till target reached and write to 0x2500:01 (every yield is an one 1ms cycle)
				yield();
			}	
			sleep(In.Pause);             // setting the sleep time to the value written in 0x2400:05 
			Out.Time=0;                  //reset variable
			
			Out.ControlWord = 0xF;	// switch to the "enable operation" state, reset start bit
			do 	{
					yield();						// waiting for the next cycle (1ms)
				}
				while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
				// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
			
			Out.TargetPosition = In.Position2;						// setting the target position to the value written in 0x2400:02 
			Out.ProfileVelocity = In.Speed2;					// setting the profile velocity to the value written in 0x2400:04 
		
			Out.ControlWord = 0x5F;							// start positioning,  relative			
			yield();
			while((In.StatusWord & 0x400) !=0x400)          //wait till "Target reached" 10 bit is high 
			{
				
				yield();
			}	
			
			sleep(In.Pause2);             // setting the sleep time to the value written in 0x2400:06 
		
			yield();
		
	}	
}	