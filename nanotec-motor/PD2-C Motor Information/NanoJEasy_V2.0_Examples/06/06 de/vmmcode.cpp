//in diesem Beispiel wird der Drehzahl-Modus gewählt, die state machine eingeschaltet, mit einem Eingang freigegeben und die Drehzahl mit dem Analogeingang geregelt

//1. Schritt: mappen von häufig verwenden SDO´s

map U16 ControlWord as output 0x6040:00
map S08 OperationMode as output 0x6060:00
map S16 TargetVelocity as output 0x6042:00
map U32 Inputs as input 0x60FD:00
map S32 AnalogInput as input 0x3320:01

#include "wrapper.h"
#define MAXSPEED 200					// 10V am Analogeingang entsprechen 200 U/min  // 10V on analog input equals to 200 rpm

S16 VelocityFilter(S16 velocity);    	// erstellen von 2 Variablen, wobei VelocityFilter eine Funktion ist von velocity

//2. Schritt: Hauptfunktion aufrufen und gewünschte Einstellungen treffen

void user()
{
		
	bool bEnabled = false;   			// bool Variable mit Name "bEnabled"
		
	Out.OperationMode = 2;				// setzt den Operationsmodus auf Drehzahlmodus (mit Mapping, Zeile 5-9)
	//od_write(0x6060,0x00, 2);			// setzt ebenfalls den Operationsmodus (ohne Mapping, Zeile 5-9)
		
	Out.TargetVelocity = 0;				// setzt die Zielgeschwindigkeit auf 0 U/min (Standardeinheit)(mit Mapping, Zeile 5-9)
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
				// überprüft das Statusword (0x6041) auf die Bitmaske xxxx xxxx x01x 0011					
				Out.ControlWord = 0xF;	// schaltet in den Zustand "enable operation" und startet den velocity mode
				do 	{
						yield();						// warten auf den nächsten Zyklus (1ms)
					}
					while ( (od_read(0x6041, 0x00) & 0xEF) != 0x27);   // wartet bis der Zustand ist "operation enabled"	
					// überprüft das Statusword (0x6041) auf die Bitmaske: xxxx xxxx x01x 0111	
				
			}
		}
		else    // wenn Eingang 4 low ist
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
		
		S16 velocity = In.AnalogInput;   	// Analogeingang auslesen 0x3320:01 

		velocity = (velocity * MAXSPEED) / 950;	// Skalierung 0-10V -> 0-200 RPM 

		Out.TargetVelocity = VelocityFilter(velocity);  // Filter wegen ADC Störungen  

		yield();						// warten auf den nächsten Zyklus (1ms)
	}	
		
}	


//4. Schritt: Filter für den Analogeingang


S16 VelocityFilter(S16 velocity)
{
	static S16 lastvelocity;			// selbst ernannte Variable
	static S16 velocityfractional;		// selbst ernannte Variable
	
	// Drehzahl Filter:    /
	if (velocity < lastvelocity)
	{
		if ((lastvelocity - velocity) < 5)    // nur kleine Änderung?  
		{
			velocity = lastvelocity;      // Drehzahl bleibt konstant 
			velocityfractional--;

			if (velocityfractional < -20)  // wenn fracitonal zu groß, Drehzahl anpassen   
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

	// Totbereich (keine Bewegung in der Nähe von analog 0)  
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
