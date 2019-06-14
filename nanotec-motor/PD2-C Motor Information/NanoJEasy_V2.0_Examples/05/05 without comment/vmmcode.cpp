map U16 ControlWord as output 0x6040:00
map U32 Inputs as input 0x60FD:00

#include "wrapper.h"


void user()
{
	bool bEnabled = false;  		
	
	od_write(0x6060, 0x00, 0xff);		
	

	Out.ControlWord = 0x6;				
	do 	{
		yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   
	
	
	
	while(true)
	{
		if((In.Inputs & 0x80000) != 0)  
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