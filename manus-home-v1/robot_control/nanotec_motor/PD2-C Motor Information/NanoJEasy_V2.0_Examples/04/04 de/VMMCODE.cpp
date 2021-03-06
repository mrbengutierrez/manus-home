//in diesem Beispiel wird der Drehzahl-Modus gewählt, die state machine eingeschaltet, mit einem Eingang freigegeben und die Drehzahl mit dem Analogeingang geregelt

//1. Schritt: mappen von häufig verwenden SDO´s

map U16 ControlWord as output 0x6040:00
map S08 OperationMode as output 0x6060:00
map S16 TargetVelocity as inout 0x6042:00
map U32 Inputs as input 0x60FD:00
map S32 AnalogInput as input 0x3320:01
map U32 Outputs as output 0x60FE:01

#include "wrapper.h"

//2. Schritt: Hauptfunktion aufrufen und gewünschte Einstellungen treffen

void user()
{
		
	bool bEnabled = false;   			// bool Variable mit Name "bEnabled"
		
	Out.OperationMode = 2;				// setzt den Operationsmodus auf Drehzahlmodus (mit Mapping, Zeile 5-9)
	//od_write(0x6060,0x00, 2);			// setzt ebenfalls den Operationsmodus (ohne Mapping, Zeile 5-9)
		
	InOut.TargetVelocity = 0;				// setzt die Zielgeschwindigkeit auf 0 U/min (Standardeinheit)(mit Mapping, Zeile 5-9)
	//od_write(0x6042,0x00, 0);			// setzt die Zielgeschwindigkeit auf 0 U/min (Standardeinheit)(ohne Mapping, Zeile 5-9)
		
//3. Schritt: State maschine hochfahren, Eingang als "Freigabe" verwenden, Analogeingang auslesen

	Out.ControlWord = 0x6;				// schaltet in den Zustand "enable voltage"
	do 	{
		yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wartet bis der Zustand ist "enable voltage" 

	// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0001
		
		

	while(true)							// Endlosschleife
	{
		
		InOut.TargetVelocity = In.AnalogInput;// Zielgeschwindigkeit = Analogwert (0-1023)
		
		if((In.Inputs & 0x10000) != 0)  // Abfrage ob Eingang 1 nicht low ist
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
					// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	de
				
			}
		}
		else    // wenn Eingang 1 low ist
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
		
		if(InOut.TargetVelocity>200)  	// wenn die Zeilgeschwindigkeit >200 dann...
		{
			Out.Outputs = 0x10000;      // schalte Ausgang 1 high
		}
		else
		{
			Out.Outputs = 0x00000;      // sonst Ausgang 1 low
			}	

		yield();						// warten auf den nächsten Zyklus (1ms)
	}	
		
}	