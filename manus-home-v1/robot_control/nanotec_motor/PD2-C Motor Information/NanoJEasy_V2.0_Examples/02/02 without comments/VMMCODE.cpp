map U16 ControlWord as output 0x6040:00
map S08 OperationMode as output 0x6060:00
map S16 TargetVelocity as output 0x6042:00
map U32 Inputs as input 0x60FD:00

#include "wrapper.h"


void user()
{
		
	bool bEnabled = false;   			
		
	Out.OperationMode = 2;				
		
	Out.TargetVelocity = 200;				
	
	
	Out.ControlWord = 0x6;				
	do 	{
		yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   
	
		

	while(true)							
	{
		
	
		if((In.Inputs & 0x10000) != 0)  
		{	
			if (bEnabled == false)		
			{
				bEnabled = true;		
				Out.ControlWord = 0x7;	
				do 	{
						yield();						
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   	
					
				Out.ControlWord = 0xF;	
				do 	{
						yield();						
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
					
			}
		}
		else   
		{	
			if (bEnabled == true)		
			{
				bEnabled = false;		
				Out.ControlWord = 0x6;	
				do 	{
						yield();						
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);  
	
					
				
			}
		}

		yield();						
	}	
		
}	