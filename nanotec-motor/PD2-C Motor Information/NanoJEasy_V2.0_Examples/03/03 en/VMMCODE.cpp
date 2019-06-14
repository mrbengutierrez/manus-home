//in this example the operationmode will be set to velocity mode, the state machine will be switched on, enabled with an input and the speed controled by analog input

//1. Step: mapping the frequently used SDO´s

map U16 ControlWord as output 0x6040:00
map S08 OperationMode as output 0x6060:00
map S16 TargetVelocity as output 0x6042:00
map U32 Inputs as input 0x60FD:00
map S32 AnalogInput as input 0x3320:01

#include "wrapper.h"

//2. Step: call main function and set the speed and mode of operation

void user()
{
		
	bool bEnabled = false;   			// bool variable with name "bEnabled"
		
	Out.OperationMode = 2;				// set the mode of operation to velocity mode (with mapping, line 5-9)
	//od_write(0x6060,0x00, 2);			// would also set the mode of operation to velocity mode (without mapping, line 5-9)
		
	Out.TargetVelocity = 0;				// set the target velocity to 0 rpm (basicvalue)(with mapping, line 5-9)
	//od_write(0x6042,0x00, 0);			// set the target velocity to 0 rpm (basicvalue)(without mapping, line 5-9)
		
//3. Step: switch on the state machine, use enable input, reading analog input

	Out.ControlWord = 0x6;				// switch to the "enable voltage" state
	do 	{
		yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wait until drive is in state "enable voltage"
	

	// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0001
		

	while(true)							// endless loop
	{
		Out.TargetVelocity = In.AnalogInput;// target velocity=analogue value (0-1023) 
	
		if((In.Inputs & 0x10000) != 0)  // checking input 1 for not low
		{	
			if (bEnabled == false)		// motor is not running
			{
				bEnabled = true;		// then start the motor with...
				Out.ControlWord = 0x7;	// switch to the "switched on" state
				do 	{
						yield();						// waiting for the next cycle (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wait until drive is in state "switched on"	
					// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0011				// waiting for the next cycle (1ms)
				Out.ControlWord = 0xF;	// switch to the "enable operation" state and starts the velocity mode
				do 	{
						yield();						// waiting for the next cycle (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
					// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
			}
		}
		else    // if input 1 is low
		{	
			if (bEnabled == true)		// motor is started
			{
				bEnabled = false;		// then stop the motor with...
				Out.ControlWord = 0x6;	// switch to the "enable voltage" state 
				do 	{
						yield();						// waiting for the next cycle (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wait until drive is in state "enable voltage"
	
					// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0001
				
			}
		}
		
	

		yield();						// waiting for the next cycle (1ms)
	}	
		
}	