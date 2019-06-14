////in diesem Beispiel wird der Positions-Modus gewählt, der Motor fährt zwischen 2 Positionen, die über "VMM Input" Objekte eingestellt werden (z.B. in der Konfigurationsdatei)

//1. Schritt: mappen von häufig verwenden SDO´s
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

//2. Schritt: Hauptfunktion aufrufen und gewünschte Einstellungen treffen

void user()
{
	od_write(0x6060,0x00, 1);								 //setzt den Operationsmodus auf Positionsmodus 
	
	Out.TargetPosition = In.Position1;					//setzt die Zielposition auf den Wert von 0x2400:01	
	
	Out.ProfileVelocity = In.Speed1;						//setzt die Zielgeschwindigkeit auf den Wert von 0x2400:03	
	
//3. Schritt: State maschine hochfahren
	sleep(In.Pause);                        //setzt die Pausezeit auf den Wert von 0x2400:05
	Out.ControlWord = 0x6;				// schaltet in den Zustand "enable voltage"
	do 	{
		yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wartet bis der Zustand ist "enable voltage" 

	// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0001

	
	
	Out.ControlWord = 0x7;	// schaltet in den Zustand "switched on"
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wartet bis der Zustand ist "switched on" 
		// überprüft das Statusword (0x6041) auf die Bitmaske xxxx xxxx x01x 0011		

	
	while(true)    	// Endlosschleife
	{	
	
			Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" 
			do 	{
					yield();						// warten auf den nächsten Zyklus (1ms)
				}
				while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
				// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
			Out.TargetPosition = In.Position1;						//setzt die Zielposition auf den Wert von 0x2400:01	
			Out.ProfileVelocity = In.Speed1;					//setzt die Zielgeschwindigkeit auf den Wert von 0x2400:03
	
			Out.ControlWord = 0x5F;					//relative Positionierung starten
			yield();
			
			while((In.StatusWord & 0x400) !=0x400)            //warte bis "Target reached" Bit 10  gesetzt wird 
			{
				Out.Time+=1;			//zähle die ms bis Position erreicht und schreibe ins 0x2500:01, jedes yield ist einer 1ms Zyklus 
				yield();
			}	
			sleep(In.Pause);             //setzt die Pausezeit auf den Wert von 0x2400:05
			Out.Time=0;                  //Variable zurücksetzen
			Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" (setzt das Start-Bit zurück)
			do 	{
					yield();						// warten auf den nächsten Zyklus (1ms)
				}
				while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
				// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
			
			Out.TargetPosition = In.Position2;					//setzt die Zielposition auf den Wert von 0x2400:02	
			Out.ProfileVelocity = In.Speed2;						//setzt die Zielgeschwindigkeit auf den Wert von 0x2400:04	
		
			Out.ControlWord = 0x5F;							//relative Positionierung starte			
			yield();
			while((In.StatusWord & 0x400) !=0x400)          //warte bis "Target reached" Bit 10 gesetzt wird 
			{
				
				yield();
			}	
			
			sleep(In.Pause2);              //setzt die Pausezeit auf den Wert von 0x2400:06	
		
			yield();
		
	}	
}	