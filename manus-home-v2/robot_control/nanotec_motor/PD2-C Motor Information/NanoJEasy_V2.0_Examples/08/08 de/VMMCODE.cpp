//in diesem Beispiel werden verschiedene Fahrprofile (Positionsmodus) über die digitalen Eingänge ausgewählt und gestartet. Zuerst wird eine Referenzfahrt durchgeführt. 

/* Wenn 4 Fahrprofile:
Eingang 1	0		
Eingang 2	Position 1		
Eingang 3	Position 2		
Eingänge 1+2 	Position 3		

Wenn 6 Fahrprofile:
Eingang 1	0		
Eingang 2	Position 1		
Eingang 3	Position 2		
Eingänge 1+2 	Position 3		
Eingänge 1+3	Position 4		
Eingänge 2+3	Position 5		

Wenn 8 Fahrprofile:
Eingang 1	0		
Eingang 2	Position 1		
Eingang 3	Position 2		
Eingang 6 	Position 3		
Eingänge 1+2	Position 4		
Eingänge 1+3	Position 5		
Eingänge 1+6 	Position 6		
Eingänge 2+3	Position 7		*/

//1. Schritt: mappen von häufig verwenden SDO´s

map U32 Inputs as input 0x60FD:00
map U16 ControlWord as output 0x6040:00
map U16 StatusWord as input 0x6041:00
map S32 TargetPosition as output 0x607A:00
map S08	OperationMode as output 0x6060:00
map S32 Profiles as input 0x2400:01


#include "wrapper.h"

//2. Schritt: Hauptfunktion aufrufen und gewünschte Einstellungen treffen

void user() 
{   
	
	//Referenzfahrt		
	od_write(0x6098, 0x00, 35);                // Homing Methode, siehe Handbuch . 35 referenziert auf die aktuelle Position
	
	od_write(0x608F, 0x01, 720);				// Schrittauflösung, z.B. 720 Schritte/Umdrehung  	
	
	od_write(0x608F, 0x02, 1);				
	
	
	Out.ControlWord = 0x6;				// schaltet in den Zustand "enable voltage"
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wartet bis der Zustand ist "enable voltage" 

	// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0001
	
	
	Out.OperationMode = 6;               // setzt den Operationsmodus auf Homing 
	yield();
		
	Out.ControlWord = 0x7;	// schaltet in den Zustand "switched on"
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wartet bis der Zustand ist "switched on" 
		// überprüft das Statusword (0x6041) auf die Bitmaske xxxx xxxx x01x 0011					
	Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
		// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
		
	Out.ControlWord = 0x1F;				//startet die Fahrt	
	yield();
	while((In.StatusWord & 0x1400)!=0x1400)             		//warte bis Referenazfahrt angeschlossen, Bits 12 und 10 beide high
		{
			yield();
		} 
	
	Out.ControlWord = 0x7;	// schaltet in den Zustand "switched on", um den Operationsmodus zu wechseln
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wartet bis der Zustand ist "switched on" 
		// überprüft das Statusword (0x6041) auf die Bitmaske xxxx xxxx x01x 0011	
	
	Out.OperationMode = 1;                       // setzt den Operationsmodus auf Positionsmodus 
	yield();
	
	
	Out.TargetPosition = 0;             //Zielposition ist 0  

		
	Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
		// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
	
	
	
	while(true)        			 // Endlosschleife
	{
		
		switch( In.Profiles )   // wähle Teil des Programms abhängig von der Anzahl der Fahrrofile (Objekt 0x2400:01)  

		{
			
		case 4:			//	///////////////////////////////////////// 4 Fahrprofile/Positionen  ////////////////////////////
	
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) ) 	// Eingang 1 nur = Referenzposition 
			{		

				 
				Out.TargetPosition =0;                         //Zielposition ist 0    
				if((In.Inputs & 0x100000) == 0x100000)        //Eingang  5 , start  
				{
				
					
					Out.ControlWord = 0x1F;	               //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)           //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
						
				}else               
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000)) 	// Eingang  2 nur = Position 1 
			{		
					
				
				Out.TargetPosition =720;                       //hier Position 1 setzen
				if((In.Inputs & 0x100000) == 0x100000)        //Eingang  5 , start 
				{
					
					
					Out.ControlWord = 0x1F;	                  //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x40000) == 0x40000) 	// Eingang 3 = Position 2 
			{		
				
							
				Out.TargetPosition =1440;                     //hier Position 2 setzen
				if((In.Inputs & 0x100000) == 0x100000)         //Eingang  5 , start  
				{
				
					Out.ControlWord = 0x1F;	                   //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	// Eingänge 1+2 = Position 3 
			{		
					
			 
				Out.TargetPosition =2160;                     //hier Position 3 setzen
				if((In.Inputs & 0x100000) == 0x100000)        //Eingang  5 , start 
				{
				
					
					Out.ControlWord = 0x1F;	                      //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			yield();
			break; 
			
			
		case 6:			///////////////////////////////////////// 6 Fahrprofile/Positionen  ////////////////////////////	
			
		
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) && ((In.Inputs & 0x40000) != 0x40000) ) 	// Eingang 1 nur = Referenzposition 
			{		
				
				Out.TargetPosition =0;                        //Zielposition ist 0  
				if((In.Inputs & 0x100000) == 0x100000)        //Eingang  5 , start 
				{
					
					Out.ControlWord = 0x1F;	                  //startet eine absolute Positionierung    
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x40000) != 0x40000)) 	// Eingang 2 nur  = Position 1 
			{				
				Out.TargetPosition =480;                          //hier Position 1setzen
				if((In.Inputs & 0x100000) == 0x100000)           //Eingang  5 , start 
				{
					
					Out.ControlWord = 0x1F;	                     //startet eine absolute Positionierung  
					yield();
					while((In.StatusWord & 0x400) !=0x400)           //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
					
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			if (((In.Inputs & 0x40000) == 0x40000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)   ) 	// Eingang 3 nur = Position 2 	
			{				
				
				Out.TargetPosition =960;                        //hier Position 2 setzen
				if((In.Inputs & 0x100000) == 0x100000)         //Eingang  5 , start
				{
					
					
					Out.ControlWord = 0x1F;	                    //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)               //warte bis "Target reached" Bit 10 gesetzt wird 
					{
		
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	// Eingänge  1+2 = Position 3 
			{				
				Out.TargetPosition =1440;                     //hier Position 3 setzen
				if((In.Inputs & 0x100000) == 0x100000)       //Eingang  5 , start
				{
					
					Out.ControlWord = 0x1F;	                 //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)               //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x50000) == 0x50000) 	// Eingänge 1+3 = Position 4  
			{		
				
				Out.TargetPosition =1920;                  //hier Position 4 setzen
				if((In.Inputs & 0x100000) == 0x100000)       //Eingang  5 , start
				{
					
					Out.ControlWord = 0x1F;	                  //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)              //warte bis "Target reached" Bit 10 gesetzt wird 
					{
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
				}
			}
			
			if ((In.Inputs & 0x60000) == 0x60000) 	// Eingänge 2+3 = Position 5 
			{		
				
				Out.TargetPosition =2400;                 //hier Position 5 setzen
				if((In.Inputs & 0x100000) == 0x100000)          //Eingang  5 , start
				{
				
					Out.ControlWord = 0x1F;	                   //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //warte bis "Target reached" Bit 10 gesetzt wird 
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
					do 	{
							yield();						// warten auf den nächsten Zyklus (1ms)
						}
						while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
						// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
					
					
				}
			}
				yield();
			break;
			
			
		case 8:			///////////////////////////////////////// 8 Fahrprofile/Positionen    ////////////////////////////	
			
		
			if ( ((In.Inputs & 0x10000) == 0x10000) && ((In.Inputs & 0x20000) != 0x20000) && ((In.Inputs & 0x40000) != 0x40000) && ((In.Inputs & 0x200000) != 0x200000) ) 	// Eingang 1 nur = Referenzposition
			{				
				Out.TargetPosition =0;
				if((In.Inputs & 0x100000) == 0x100000)          //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	                    //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			if ( ((In.Inputs & 0x20000) == 0x20000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x40000) != 0x40000) && ((In.Inputs & 0x200000) != 0x200000)) 	// Eingang 2 nur  = Position 1 // Input 2 only = Position 1
			{				
				Out.TargetPosition =360;
				if((In.Inputs & 0x100000) == 0x100000)         //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	                  //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			if (((In.Inputs & 0x40000) == 0x40000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)  && ((In.Inputs & 0x200000) != 0x200000)  ) 	// Eingang 3 nur = Position 2 // Input 3 only = Position 2
			{				
				Out.TargetPosition =720;
				if((In.Inputs & 0x100000) == 0x100000)         //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	                    //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)               //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			if (((In.Inputs & 0x200000) == 0x200000) && ((In.Inputs & 0x10000) != 0x10000) && ((In.Inputs & 0x20000) != 0x20000)  && ((In.Inputs & 0x40000) != 0x40000)  ) 	// Eingang 6 nur = Position 3 // Input 6 only = Position 3
			{				
				Out.TargetPosition =1080;
				if((In.Inputs & 0x100000) == 0x100000)        //Eingang  5 , starte  //input 5 trigger movement
				{;
					
					Out.ControlWord = 0x1F;	                 //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)              //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			
			if ((In.Inputs & 0x30000) == 0x30000) 	// Eingänge 1+2 = Position 4 	// Inputs 1+2 = Position 4
			{				
				Out.TargetPosition =1440;
				if((In.Inputs & 0x100000) == 0x100000)       //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	               //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
									
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			if ((In.Inputs & 0x50000) == 0x50000) 	// Eingänge 1+3 = Position 5 // Inputs 1+3 = Position 5
			{				
				Out.TargetPosition =1800;
				if((In.Inputs & 0x100000) == 0x100000)        //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	                  //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)             //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{

						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			if ((In.Inputs & 0x210000) == 0x210000) 	// Eingänge 1+6 = Position 6 // Inputs 1+6 = Position 6
			{				
				Out.TargetPosition =2160;
				if((In.Inputs & 0x100000) == 0x100000)         //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	                   //startet eine absolute Positionierung 
					while((In.StatusWord & 0x400) !=0x400)            //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
						
						yield();
					}	
					
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			
			
			if ((In.Inputs & 0x60000) == 0x60000) 	// Eingänge 2+3 = Position 7 	// Inputs 2+3 = Position 7
			{				
				Out.TargetPosition =2520;
				if((In.Inputs & 0x100000) == 0x100000)       //Eingang  5 , starte  //input 5 trigger movement
				{
					
					Out.ControlWord = 0x1F;	                 //startet eine absolute Positionierung 
					yield();
					while((In.StatusWord & 0x400) !=0x400)            //warte bis Fahrt abgeschlossen,  Bit 10 (Target reached) ist 1 //wait until move complete, then bit 10 (Target reached) is 1
					{
						
						yield();
					}	
				}else
				{

					Out.ControlWord = 0xF;					
					yield();
					
				}
			}
			yield();
			break;
		
		case 0:    //Default, wenn 2400:01==0, nichts tun
				default:
				yield();
				break;
		
		
		
	}
 }
} 