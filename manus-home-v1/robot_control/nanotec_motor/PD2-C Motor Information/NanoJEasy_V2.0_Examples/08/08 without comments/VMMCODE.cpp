map U32 Inputs as input 0x60FD:00
map U16 ControlWord as output 0x6040:00
map U16 StatusWord as input 0x6041:00
map S32 TargetPosition as output 0x607A:00
map S08	OperationMode as output 0x6060:00
map S32 Profiles as input 0x2400:01


#include "wrapper.h"


void user() 
{   
	
	od_write(0x6098, 0x00, 35);              
	
	od_write(0x608F, 0x01, 720);			 	
	
	od_write(0x608F, 0x02, 1);				
	
	
	
	Out.ControlWord = 0x6;			
		do 	{
			yield();						
			}
			while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);    
		
	
	
	Out.OperationMode = 6;                
	yield();
		
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
			
	
	Out.ControlWord = 0x1F;				
	yield();
	while((In.StatusWord & 0x1400)!=0x1400)             	 
		{
			yield();
		} 
	
	Out.ControlWord = 0x7;	
	do 	{
			yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);    
				
	
	Out.OperationMode = 1;                    
	yield();
	
	
	Out.TargetPosition = 0;           
	yield();
	
	
	
	Out.ControlWord = 0xF;	
	do 	{
			yield();						
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);  	
	
	
	
	while(true)           
	{
		
		switch( In.Profiles )  

		{
			
		case 4:	
	
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) ) 	
			{		

				
				Out.TargetPosition =0;                        
				if((In.Inputs & 0x100000) == 0x100000)        
				{
				
					
					Out.ControlWord = 0x1F;	               
					yield();
					while((In.StatusWord & 0x400) !=0x400)            
					{
									
						yield();
					}	
						
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
						
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000)) 	
			{		
					
				
				Out.TargetPosition =720;                       
				if((In.Inputs & 0x100000) == 0x100000)        
				{
					
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)             
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   	
						
					
				}
			}
			
			if ((In.Inputs & 0x40000) == 0x40000) 	
			{		
				
							
				Out.TargetPosition =1440;                      
				if((In.Inputs & 0x100000) == 0x100000)         
				{
				
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)             
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();					
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   	
						
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	
			{		
					
			
				Out.TargetPosition =2160;                    
				if((In.Inputs & 0x100000) == 0x100000)      
				{
				
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();					
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
							
					
				}
			}
			yield();
			break; 
			
			
		case 6:				
			
		
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) && ((In.Inputs & 0x40000) != 0x40000) ) 	
			{				
				Out.TargetPosition =0;                        
				if((In.Inputs & 0x100000) == 0x100000)        
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)          
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);  
							
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x40000) != 0x40000)) 	
			{				
				Out.TargetPosition =480;                      
				if((In.Inputs & 0x100000) == 0x100000)      
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)          
					{
									
						yield();
					}	
					yield();
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   	
							
					
				}
			}
			
			if (((In.Inputs & 0x40000) == 0x40000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)   ) 		
			{				
				Out.TargetPosition =960;                       
				if((In.Inputs & 0x100000) == 0x100000)        
				{
					
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)             
					{
		
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
						
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	 
			{				
				Out.TargetPosition =1440;                    
				if((In.Inputs & 0x100000) == 0x100000)     
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)             
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);  
						
					
				}
			}
			
			if ((In.Inputs & 0x50000) == 0x50000) 	
			{				
				Out.TargetPosition =1920;                       
				if((In.Inputs & 0x100000) == 0x100000)         
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   	
	
					
				}
			}
			
			if ((In.Inputs & 0x60000) == 0x60000) 	
			{				
				Out.TargetPosition =2400;                          
				if((In.Inputs & 0x100000) == 0x100000)          
				{
				
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
						
					
				}
			}
				yield();
			break;
			
			
		case 8:				
			
		
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) && ((In.Inputs & 0x40000) != 0x40000) && ((In.Inputs & 0x200000) != 0x200000) ) 	 
			{				
				Out.TargetPosition =0;                           
				if((In.Inputs & 0x100000) == 0x100000)           
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)          
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();					
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
					
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x40000) != 0x40000) && ((In.Inputs & 0x200000) != 0x200000)) 	
			{				
				Out.TargetPosition =360;                          
				if((In.Inputs & 0x100000) == 0x100000)        
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
							
					
				}
			}
			
			if (((In.Inputs & 0x40000) == 0x40000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)  && ((In.Inputs & 0x200000) != 0x200000)  ) 	
			{				
				Out.TargetPosition =720;                       
				if((In.Inputs & 0x100000) == 0x100000)       
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)          
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);  
					
					
				}
			}
			
			if (((In.Inputs & 0x200000) == 0x200000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)  && ((In.Inputs & 0x40000) != 0x40000)  ) 	 
			{				
				Out.TargetPosition =1080;                       
				if((In.Inputs & 0x100000) == 0x100000)        
				{;
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
							
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	
			{				
				Out.TargetPosition =1440;                      
				if((In.Inputs & 0x100000) == 0x100000)        
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)         
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
					
					
				}
			}
			
			if ((In.Inputs & 0x50000) == 0x50000) 	
			{				
				Out.TargetPosition =1800;                        
				if((In.Inputs & 0x100000) == 0x100000)        
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{

						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);  
						
					
				}
			}
			
			if ((In.Inputs & 0x210000) == 0x210000) 	
			{				                                  
				Out.TargetPosition =2160;                     
				if((In.Inputs & 0x100000) == 0x100000)         
				{
					
					Out.ControlWord = 0x1F;	
					while((In.StatusWord & 0x400) !=0x400)         
					{
						
						yield();
					}	
					
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
							
					
				}
			}
			
			
			if ((In.Inputs & 0x60000) == 0x60000) 
			{				
				Out.TargetPosition =2520;                    
				if((In.Inputs & 0x100000) == 0x100000)       
				{
					
					Out.ControlWord = 0x1F;	
					yield();
					while((In.StatusWord & 0x400) !=0x400)           
					{
						
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	
					do 	{
							yield();						
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   
							
					
				}
			}
			yield();
			break;
		
		case 0:                 
				default:
				yield();
				break;
		
		
		
	}
 }
} 