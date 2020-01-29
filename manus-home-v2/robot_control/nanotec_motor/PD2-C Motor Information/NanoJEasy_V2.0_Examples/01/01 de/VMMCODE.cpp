//in diesem Beispiel wird der Drehzahl-Modus gewählt und die state machine eingeschaltet

//1. Schritt: mappen von häufig verwenden SDO´s

map U16 ControlWord as output 0x6040:00
map S08 OperationMode as output 0x6060:00
map S16 TargetVelocity as output 0x6042:00

#include "wrapper.h"


//2. Schritt: Hauptfunktion aufrufen und gewünschte Einstellungen treffen

void user()
{
	
	//sleep(5000);                      // warte 5000 Millisekunden (optional wenn gewünscht)
	Out.OperationMode = 2;				// setzt den Operationsmodus auf Drehzahlmodus (mit Mapping, Zeile 5-7)
	//od_write(0x6060,0x00, 2);			// setzt ebenfalls den Operationsmodus (ohne Mapping, Zeile 5-7)
		
	Out.TargetVelocity = 200;			// setzt die Zielgeschwindigkeit auf 200 U/min (Standardeinheit)(mit Mapping, Zeile 5-7)
	//od_write(0x6042,0x00, 200);		// setzt die Zielgeschwindigkeit auf 200 U/min (Standardeinheit)(ohne Mapping, Zeile 5-7)
		
//3. Schritt: State machine hochfahren

	Out.ControlWord = 0x6;				// schaltet in den Zustand "enable voltage"
	do 	{
		yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x21);   // wartet bis der Zustand ist "enable voltage" 
	
	// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0001
	
	Out.ControlWord = 0x7;				// schaltet in den Zustand "switched on"
	do 	{
		yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x23);   // wartet bis der Zustand ist "switched on" 
	// überprüft das Statusword (0x6041) auf die Bitmaske xxxx xxxx x01x 0011	
		
	Out.ControlWord = 0xF;				// schaltet in den Zustand "enable operation" und startet den velocity mode							
	do 	{
		yield();						// warten auf den nächsten Zyklus (1ms)
		}
		while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
	// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
		
	while(true)							// Endlosschleife
	{yield();}	                      	// warten auf den nächsten Zyklus (1ms)
		
}	