// in this example the position mode will be selected and started, after the input 1 is triggered, the motor moves to a set position (flagposition mode)

//1. Step: mapping the frequently used SDO´s
map U16 ControlWord as output 0x6040:00
map S16 ProfileVelocity as output 0x6081:00
map S32 TargetPosition as output 0x607A:00
map U32 Inputs as input 0x60FD:00
map S32 ActualPosition as input 0x6064:00
map S32 AnalogInput as input 0x3320:01

#include "wrapper.h"



//2. Step: call Main function and set the speed and mode of operation
void user()
{
	od_write(0x6060,0x00, 1);								// set the mode of operation to profile position
	Out.ProfileVelocity = 200;							//sets the profile velocity to 200 rpm
	Out.TargetPosition = 1000000000;					// setting the target position (just as a limit)
		
//3. Step: switch on the state machine
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
		
	Out.ControlWord = 0x4F;	// switch to the "enable operation" state , target position relative
	do 	{
			yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
	
	Out.ControlWord = 0x5F;								// start	
	yield();
		
		
	while(true)          	// endless loop
	{	
		//3. Step: set new target position when input 1 (trigger) high 
		if((In.Inputs & 0x10000) == 0x10000)				// if input 1 (trigger)wenn Eingang 1 (trigger) high
			{
			Out.TargetPosition = In.ActualPosition + 2000;	  //sets the new target position depending on the actual position and analog input
			Out.ProfileVelocity = 50;						// new profile velocity is 50 rpm
			yield();
			Out.ControlWord = 0x2F;							// reset start bit 4, new target position must be acknowledged as new set point immediately(Bit 5)
			yield();
			Out.ControlWord = 0x3F;							// starts the absolute positioning 	
			yield();
			while((In.Inputs & 0x10000) == 0x10000)			// wait while Input 1 still high
			{
				yield();
			}	
		}
		yield();
	}	
}	