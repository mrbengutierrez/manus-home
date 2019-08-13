deutsch:


Im Beispiel 1 wird der Drehzahl-Modus gewählt und die state machine eingeschaltet, der Motor fängt automatisch zu drehen an

Im Beispiel 2 kommt ein Freigabeeingang dazu, damit der Motor nicht automatisch startet sondern mit dem Eingang gestartet wird

Im Beispiel 3 kommt der analoge Eingang dazu, hier kann dann die Drehzahl variiert werden

Im Beispiel 4 wird zusätzlich noch der Ausgang geschaltet je nachdem ob der Motor > oder < 200 U/min dreht.

Im Beispiel 5 wird der Takt-Richtungs-Modus gewählt, die State machine eingeschaltet und über Eingang 4 die Freigabe geschaltet

Beispiel 6 ist wie Beispiel 3 mit Vorgabe der max. Geschwindigkeit, Skalierung, Filter und Totbereich

Im Beispiel 7 wird der Positions-Modus gewählt, der Motor fährt zwischen 2 Positionen, die über "VMM Input" Objekte eingestellt werden (z.B. in der Konfigurationsdatei)

Im Beispiel 8 werden verschiedene Fahrprofile (Positionsmodus) über die digitalen Eingänge ausgewählt und gestartet. Zuerst wird eine automatische Referenzfahrt durchgeführt. 

Im Beispiel 9 V1 wird der Positionsmodus gewählt und gestartet

Im Beispiel 9 V2 wird der Positionsmodus gewählt und gestartet, nach dem Triggersignal wird eine vorgegebene Position angefahren (Flagpositionsmodus)

Im Beispiel 9 V3 wird der Positionsmodus gewählt und gestartet, nach dem Triggersignal wird eine analog vorgegebene Position angefahren (Flagpositionsmodus)


english:


in example 1 the velocity mode will be selected and the state machine will be started, the motor runs automatically.

in example 2 a enable input is added, to start the motor manually.

in example 3 the function analog input is added, there the speed can be set

in example 4 the output will be switched, depending on whether the speed is > or < than 200 rpm

in example 5 the clock-direction mode will be selected, the state machine will be started and the enable input at input 4 is added

example 6 is the same like example 3 + define of max speed, scaling, filter and play near 0

in example 7 the position mode will be selected and the motor will move between 2 positions that can be set via "VMM Input" Objects (for exmaple in the configuration file)

in example 8 the digital inputs are used to select betweeen various movement records (position mode) and start them. At power up there is an automatical homing done.  

in example 9 V1 the position mode will be selected and started

in example 9 V2 the position mode will be selected and started, after the input 1 is triggered, the motor moves to a set position (flagposition mode)

in example 9 V3 the position mode will be selected and started, after the input 1 is triggered, the motor moves to a analog set position (flagposition mode)




