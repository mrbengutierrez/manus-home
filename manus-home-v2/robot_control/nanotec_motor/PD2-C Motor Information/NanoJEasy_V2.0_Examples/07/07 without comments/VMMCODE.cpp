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


void user()
{
	od_write(0x6060,0x00, 1);						
	
	Out.TargetPosition = In.Position1;					
	
	Out.ProfileVelocity = In.Speed1;				
	

	sleep(In.Pause);                      
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

	
	while(true)    
	{	
	
			Out.ControlWord = 0xF;	
			do 	{
					yield();						
				}
				while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
				
			Out.TargetPosition = In.Position1;							
			Out.ProfileVelocity = In.Speed1;					
	
			Out.ControlWord = 0x5F;					
			yield();
			
			while((In.StatusWord & 0x400) !=0x400)          
			{
				Out.Time+=1;		
				yield();
			}	
			sleep(In.Pause);           
			Out.Time=0;               
			
			Out.ControlWord = 0xF;	
			do 	{
					yield();						
				}
				while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
			
			
			Out.TargetPosition = In.Position2;					
			Out.ProfileVelocity = In.Speed2;				
		
			Out.ControlWord = 0x5F;								
			yield();
			while((In.StatusWord & 0x400) !=0x400)         
			{
				
				yield();
			}	
			
			sleep(In.Pause2);            
		
			yield();
		
	}	
}	