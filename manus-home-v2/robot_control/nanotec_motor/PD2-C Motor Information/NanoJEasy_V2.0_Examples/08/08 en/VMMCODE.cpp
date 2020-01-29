// in this example the digital inputs are used to select betweeen various movement records (position mode) and start them. At first there is a homing done.  

/* If 4 records:
Input 1	     0		
Input  2	Position 1		
Input  3	Position 2		
Inputs 1+2 	Position 3		

IF 6 records:
Input  1	0		
Input  2	Position 1		
Input  3	Position 2		
Inputs 1+2 	Position 3		
Inputs 1+3	Position 4		
Inputs 2+3	Position 5		

If 8 records:
Input  1	0		
Input  2	Position 1		
Input  3	Position 2		
Input  6 	Position 3		
Inputs 1+2	Position 4		
Inputs 1+3	Position 5		
Inputs 1+6 	Position 6		
Inputs 2+3	Position 7		*/

//mapping the frequently used SDO´s

map U32 Inputs as input 0x60FD:00
map U16 ControlWord as output 0x6040:00
map U16 StatusWord as input 0x6041:00
map S32 TargetPosition as output 0x607A:00
map S08	OperationMode as output 0x6060:00
map S32 Profiles as input 0x2400:01


#include "wrapper.h"


void user() 
{   
	
	// Homing Mode	
	od_write(0x6098, 0x00, 35);               // homing method, see manual, method 35 sets current position to home
	
	od_write(0x608F, 0x01, 720);			 	// position resolution, example 720 steps/revolution
	
	od_write(0x608F, 0x02, 1);				
	
	
	
	Out.ControlWord = 0x6;				// switch to the "enable voltage" state
		do 	{
			yield();						// waiting for the next cycle (1ms)
			}
			while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);    // wait until drive is in state "enable voltage"	// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0001
			// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0001
	
	
	Out.OperationMode = 6;                //Mode of operation=Homing
	yield();
		
	Out.ControlWord = 0x7;	// switch to the "switched on" state
	do 	{
			yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wait until drive is in state "switched on" 
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0011		
	
	Out.ControlWord = 0xF;	// switch to the "enable operation" state
	do 	{
			yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
	
	Out.ControlWord = 0x1F;				//start	homing
	yield();
	while((In.StatusWord & 0x1400)!=0x1400)             	 // wait till homing is fnished, Bits 12 und 10 are both high 
		{
			yield();
		} 
	
	Out.ControlWord = 0x7;	// switch to the "switched on" state, in order to switch to operation mode position
	do 	{
			yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wait until drive is in state "switched on" 
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0011		
	
	Out.OperationMode = 1;                      // Mode of operation= Position Mode
	yield();
	
		
	
	Out.TargetPosition = 0;             // target position is 0
	yield();
	
	
	
	Out.ControlWord = 0xF;	// switch to the "enable operation" state
	do 	{
			yield();						// waiting for the next cycle (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
		// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
	
	
	
	while(true)           // endless loop
	{
		
		switch( In.Profiles )   //switch between parts of the program according to number of profiles used (o0bject 0x2400:01)

		{
			
		case 4:			//	///////////////////////////////////////// 4 profiles/positions  ////////////////////////////
	
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) ) 	// Input 1 only = Home position
			{		

				
				Out.TargetPosition =0;                         //target position is 0
				if((In.Inputs & 0x100000) == 0x100000)        //input 5 trigger movement
				{
				
					
					Out.ControlWord = 0x1F;	               //start, absolute
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
						
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000)) 	 //Input 2 only = Position 1
			{		
					
				
				Out.TargetPosition =720;                       //enter  position 1 here
				if((In.Inputs & 0x100000) == 0x100000)        //input 5 trigger movement 
				{
					
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)              //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x40000) == 0x40000) 	//Input 3 = Position 2
			{		
				
							
				Out.TargetPosition =1440;                        //enter  position 2 here
				if((In.Inputs & 0x100000) == 0x100000)          //input 5 trigger movement 
				{
				
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	 // Inputs 1+2 = Position 3
			{		
					
			
				Out.TargetPosition =2160;                     //enter  position 3 here
				if((In.Inputs & 0x100000) == 0x100000)       //input 5 trigger movement 
				{
				
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			yield();
			break; 
			
			
		case 6:			///////////////////////////////////////// 6 profiles/positions  ////////////////////////////	
			
		
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) && ((In.Inputs & 0x40000) != 0x40000) ) 	// Input 1 only = Home
			{				
				Out.TargetPosition =0;                         //target position is 0
				if((In.Inputs & 0x100000) == 0x100000)        //input 5 trigger movement 
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x40000) != 0x40000)) 	 // Input 2 only = Position 1
			{				
				Out.TargetPosition =480;                       //enter  position 1 here
				if((In.Inputs & 0x100000) == 0x100000)        //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
					yield();
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if (((In.Inputs & 0x40000) == 0x40000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)   ) 		// Input 3 only= Position 2
			{				
				Out.TargetPosition =960;                        //enter  position 2 here
				if((In.Inputs & 0x100000) == 0x100000)         //input 5 trigger movement
				{
					
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)              //wait till "Target reached" 10 bit is high 
					{
		
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	 // Inputs 1+2 = Position 3
			{				
				Out.TargetPosition =1440;                     //enter  position 3 here
				if((In.Inputs & 0x100000) == 0x100000)       //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)              //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x50000) == 0x50000) 	 // Inputs 1+3 = Position 4
			{				
				Out.TargetPosition =1920;                        //enter  position 4 here
				if((In.Inputs & 0x100000) == 0x100000)          //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x60000) == 0x60000) 	 // Inputs 2+3 = Position 5
			{				
				Out.TargetPosition =2400;                          //enter  position 5 here
				if((In.Inputs & 0x100000) == 0x100000)            //input 5 trigger movement
				{
				
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
				yield();
			break;
			
			
		case 8:			///////////////////////////////////////// 8 profiles/positions   ////////////////////////////	
			
		
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) && ((In.Inputs & 0x40000) != 0x40000) && ((In.Inputs & 0x200000) != 0x200000) ) 	 // Input 1 only = Home
			{				
				Out.TargetPosition =0;                            //target position is 0
				if((In.Inputs & 0x100000) == 0x100000)           //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x40000) != 0x40000) && ((In.Inputs & 0x200000) != 0x200000)) 	// Input 2 only = Position 1
			{				
				Out.TargetPosition =360;                          //enter  position 1 here
				if((In.Inputs & 0x100000) == 0x100000)          //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if (((In.Inputs & 0x40000) == 0x40000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)  && ((In.Inputs & 0x200000) != 0x200000)  ) 	 // Input 3 only = Position 2
			{				
				Out.TargetPosition =720;                        //enter  position 2 here
				if((In.Inputs & 0x100000) == 0x100000)        //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if (((In.Inputs & 0x200000) == 0x200000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)  && ((In.Inputs & 0x40000) != 0x40000)  ) 	 // Input 6 only = Position 3
			{				
				Out.TargetPosition =1080;                       //enter  position 3 here
				if((In.Inputs & 0x100000) == 0x100000)         //input 5 trigger movement
				{;
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	// Inputs 1+2 = Position 4
			{				
				Out.TargetPosition =1440;                       //enter  position 4 here
				if((In.Inputs & 0x100000) == 0x100000)         //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)          //wait till "Target reached" 10 bit is high 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x50000) == 0x50000) 	 // Inputs 1+3 = Position 5
			{				
				Out.TargetPosition =1800;                        //enter  position 1 here
				if((In.Inputs & 0x100000) == 0x100000)          //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{

						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x210000) == 0x210000) 	 // Inputs 1+6 = Position 6
			{				                                  
				Out.TargetPosition =2160;                       //enter  position 6 here
				if((In.Inputs & 0x100000) == 0x100000)         //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					while((In.StatusWord & 0x400) !=0x400)          //wait till "Target reached" 10 bit is high 
					{
						
						yield();
					}	
					
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			
			
			if ((In.Inputs & 0x60000) == 0x60000) 	// Inputs 2+3 = Position 7
			{				
				Out.TargetPosition =2520;                     //enter  position 7 here
				if((In.Inputs & 0x100000) == 0x100000)       //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //wait till "Target reached" 10 bit is high 
					{
						
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// switch to the "enable operation" state
					do 	{
							yield();						// waiting for the next cycle (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wait until drive is in state "operation enabled"	
						// checking the statusword (0x6041) for the bitmask: xxxx xxxx x01x 0111	
					
				}
			}
			yield();
			break;
		
		case 0:                  // default, 2400:01==0 then do nothing
				default:
				yield();
				break;
		
		
		
	}
 }
} 