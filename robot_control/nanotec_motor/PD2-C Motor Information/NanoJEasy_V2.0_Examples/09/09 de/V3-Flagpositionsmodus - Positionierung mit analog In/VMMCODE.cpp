//in diesem Beispiel wird der Positionsmodus gewählt und gestartet, nach dem Triggersignal wird eine analog vorgegebene Position angefahren (Flagpositionsmodus)


//1. Schritt: mappen von häufig verwenden SDO´s
map U16 ControlWord as output 0x6040:00
map S16 ProfileVelocity as output 0x6081:00
map S32 TargetPosition as output 0x607A:00
map U32 Inputs as input 0x60FD:00
map S32 ActualPosition as input 0x6064:00
map S32 AnalogInput as input 0x3320:01

#include "wrapper.h"



//2. Schritt: Hauptfunktion aufrufen und gewünschte Einstellungen treffen
void user()
{
	od_write(0x6060,0x00, 1);							 // setzt den Operationsmodus auf Positionsmodus
	Out.ProfileVelocity = 200;						// setzt die Zielgeschwindigkeit auf 200 U/min
	Out.TargetPosition = 1000000000;					// setzt eine Zielposition, nur als Limit
		
//3. Schritt: State maschine hochfahren	
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
		
	Out.ControlWord = 0x4F;	// schaltet in den Zustand "enable operation" , Zielposition relative
	do 	{
			yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
		// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
	
	Out.ControlWord = 0x5F;								// startet die Fahrt	
	yield();
		
		
	while(true)         // Endlosschleife
	{	
		//3. Schritt: neue Zielposition senden sobald EIngang 1 (Trigger) high
		if((In.Inputs & 0x10000) == 0x10000)				// wenn Eingang 1 (Trigger) high...
		{
			Out.TargetPosition = In.ActualPosition + (In.AnalogInput * 10);	  //setzt die neue Zielposition abhängig von der Istposition und Analogeingang 
			Out.ProfileVelocity = 50;						// neue Zielgeschwidnigkeit=50 U/min
			yield();
			Out.ControlWord = 0x2F;							// setzt das Startbit 4 zurück ,neue Zielposition muss sofort übernommen werrden (Bit 5)
			yield();
			Out.ControlWord = 0x3F;							// startet die  absolute Positionierung 	
			yield();
			while((In.Inputs & 0x10000) == 0x10000)			// warte während Eingang 1 noch high
			{
				yield();
			}	
		}
		yield();
	}	
}	