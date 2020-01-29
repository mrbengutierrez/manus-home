map U16 ControlWord as output 0x6040:00
map S16 ProfileVelocity as output 0x6081:00
map S32 TargetPosition as output 0x607A:00
map U32 Inputs as input 0x60FD:00
map S32 ActualPosition as input 0x6064:00
map S32 AnalogInput as input 0x3320:01

#include "wrapper.h"



void user()
{
	od_write(0x6060,0x00, 1);								
	Out.ProfileVelocity = 200;							
	Out.TargetPosition = 1000000000;					
		

	Out.ControlWord = 0x6;				
	do 	{
		yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);    


	
	Out.ControlWord = 0x7;	
	do 	{
			yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);    
		
		
	Out.ControlWord = 0x4F;	
	do 	{
			yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);  	
			
	
	Out.ControlWord = 0x5F;								
	yield();
		
		
	while(true)          
	{	
		yield();
	}	
}	