// in diesem Beispiel wird der Takt/Richtungsmodus gewählt und mit einem Eingang freigegeben

//1. Schritt: mappen von häufig verwenden SDO´s
map U16 ControlWord as output 0x6040:00
map U32 Inputs as input 0x60FD:00

#include "wrapper.h"

//2. Schritt: Main aufrufen und gewünschte Einstellungen treffen

void user()
{
	bool bEnabled = false;  			// bool Variable mit Name "bEnabled"
	
	od_write(0x6060, 0x00, 0xff);		// setzt den Operationsmodus auf Takt-Richtung (0xff = -1)
	
//3. Schritt: State maschine hochfahren, Eingang als "Freigabe" verwenden, Analogeingang auslesen

	
		Out.ControlWord = 0x6;				// schaltet in den Zustand "enable voltage"
	do 	{
		yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wartet bis der Zustand ist "enable voltage" 

	// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0001
	
	
	while(true)
	{
		if((In.Inputs & 0x80000) != 0)  // Abfrage ob Eingang 4 nicht low ist
		{	
			if (bEnabled == false)		// und Motor läuft nicht
			{
				bEnabled = true;		// dann starte Motor mit...
				Out.ControlWord = 0x7;	// schaltet in den Zustand "switched on"
				do 	{
						yield();						// warten auf den nächsten Zyklus (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wartet bis der Zustand ist "switched on" 
				// überprüft das Statusword (0x6041) auf die Bitmaske xxxx xxxx x01x 0011					// warten auf den nächsten Zyklus (1ms)
				Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" und startet den velocity mode
				do 	{
						yield();						// warten auf den nächsten Zyklus (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
					// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
			}
		}
		else                			// wenn Eingang 1 low ist
		{	
			if (bEnabled == true)		// und Motor ist gestartet
			{
				bEnabled = false;		// dann stoppe den Motor mit...
				Out.ControlWord = 0x6;	// schaltet in den Zustand "enable voltage"
				do 	{
						yield();						// warten auf den nächsten Zyklus (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wartet bis der Zustand ist "enable voltage" 

					// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0001
			}
		}

		yield();						// warten auf den nächsten Zyklus (1ms)
	} 
}	