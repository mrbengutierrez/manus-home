map U16 ControlWord as output 0x6040:00
map S08 OperationMode as output 0x6060:00
map S16 TargetVelocity as output 0x6042:00
map U32 Inputs as input 0x60FD:00
map S32 AnalogInput as input 0x3320:01

#include "wrapper.h"
#define MAXSPEED 200		

S16 VelocityFilter(S16 velocity);    


void user()
{
		
	bool bEnabled = false;   			
		
	Out.OperationMode = 2;				

		
	Out.TargetVelocity = 0;				


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
		
		S16 velocity = In.AnalogInput;     

		velocity = (velocity * MAXSPEED) / 950;     

		Out.TargetVelocity = VelocityFilter(velocity);    


		yield();						
	}	
		
}	



S16 VelocityFilter(S16 velocity)
{
	static S16 lastvelocity;
	static S16 velocityfractional;
	
	
	if (velocity < lastvelocity)
	{
		if ((lastvelocity - velocity) < 5)   
		{
			velocity = lastvelocity;      
			velocityfractional--;

			if (velocityfractional < -20)   
			{
				velocity--;
				velocityfractional = 0;
			}
		}
        else
        {
          velocityfractional = 0;
        }
	}
	else if (velocity > lastvelocity)
	{
		if ((velocity - lastvelocity) < 5)
		{
			velocity = lastvelocity;
			velocityfractional++;

			if (velocityfractional > 20)
			{
				velocity++;
				velocityfractional = 0;
			}
		}
        else
        {
          velocityfractional = 0;
        }
	}

    if (velocity > 0)
    {
		velocity -= 10;
		
		if (velocity < 0)
		{
			velocity = 0;
		}
    }
    else if (velocity < 0)
    {
		velocity += 10;
		
		if (velocity > 0)
		{
			velocity = 0;
		}
    }

	lastvelocity = velocity;

	return velocity;
}
