#ifndef CLASS_COMMUNICATIONNT
#define CLASS_COMMUNICATIONNT
/**
 * Class CommunicationNT, header file.
 *
 * Class to manage the communication with the Nanotec motors through USB.
 * All the communication is based on sending an array of hexadecimal values
 * (around 19 to 23 bytes of length) through serial communication.
 * After sending an array (must be unsigned char) there is always an answer
 * that needs to be read.
 * Tested with motors: PD2-C USB.
 *
 * Information from Lincoln about the USB communication to the Nanotec motor:
 *
 * 4E 54: NT , always the same, Nanotec specific header for USB
 * 00 0F: Message Length     (15 bytes form here on to be sent)    
 * 05: Modbus Address , default is 5
 * 2B 0D: Encapsulated transfer identifier, always 2B 0D.          
 * 00 00:    00 00 for read and hex 01 00for write
 * 01 :CANopen Cob-ID, always 01                        
 * 60 64: Object-Index   of  Can-Object (0x6064for actual position, big endian)
 * 00: Sub-Index  of  Can-Object  0x6064:00               
 * 00 00: Start-Address , always 0
 * 00 00: Data-size in byte, only for write      
 * F9 C8: CRC
 * Standard Modbus CRC  CRC16. Initial value 0xFFFF , polynomial 0xA001. Always
 * the same for the same command.
 * CRC calculator https://www.lammertbies.nl/comm/info/crc-calculation.html 
 * 
 * Lincoln Noggle
 * Application Engineer
 * Nanotec Electronic US Inc.
 * 38 Montvale Ave., Suite 400 C15
 * Stoneham, MA 02180
 * Office: +1.781.219.3343 Ext 3
 * Email: lincoln.noggle@us.nanotec.com | www.us.nanotec.com
 *
 * @author Moises Alencastre-Miranda
 * @author Benjamin Gutierrez
 * @date 06/10/2019
 * @version 1.6
 */


/**
 * Including C++ libraries for display on screen, respectively.
 */
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>  // String function definitions.
#include <unistd.h>  // UNIX standard function definitions.
#include <fcntl.h>   // File control definitions.
#include <errno.h>   // Error number definitions.
#include <termios.h> // POSIX terminal control definitions.
#include <math.h>

/**
 * Defined values.
 * Maximum length of the message in bytes.
 * Minimum length of the message in bytes.
 * Maximum length of the data in bytes.
 * Stiffness constant.
 * Value to map the torque force to percentage.
 */
#define MAXLEN 24
#define MINLEN 13
#define MAXDAT 4
#define STIFF 100.0
#define VALMAP 22
#define DEBUG 0


/**
 * For use the libraries std (for cout, endl, etc).
 */
using namespace std;


/**
 * Class that includes the definition of the global variables and the methods.
 */
class CommunicationNT
{
  private:

    /**
     * Reference to the file descriptor.
     */
    int _fd;

    /**
     * Header of Nanotec. First 2 bytes.
     */
    unsigned char *_header;

    /**
     * Length of the message in bytes. 2 bytes after the header.
     */
    unsigned char *_length;

    /**
     * Modbus address (1 byte with always with 05) and encapsulated transfer
     * identifier (2 bytes always with 2B 0D). 3 bytes after the length.
     */
    unsigned char *_modbusEncap;

    /**
     * Mode, 2 bytes after the modbusEncap: 00 00 for read, 01 00 for write.
     */
    unsigned char *_mode;

    /**
     * CANopen, 1 byte after the mode, always with 01.
     */
    unsigned char *_can;

    /**
     * Nanotec object index with subindex or hexadecimal address of the function
     * to read/write from the motor. 3 bytes after the CAN.
     * Commonly the subindex is 00.
     */
    unsigned char *_objIdxSub;

    /**
     * Start address. 2 bytes after Object Index-Subindex, always with 00 00.
     */
    unsigned char *_startAddr;

    /**
     * Data size in bytes, only for write. 2 bytes after start address.
     */
    unsigned char *_dataSize;

    /**
     * Data (after data size), commonly between 0 and 4 bytes. The data is
     * reversed, the bytes need to be read from right to left.
     */
    unsigned char *_data;

    /**
     * Cyclic Redundancy Check (CRC). 2 final bytes. Code calculated for error
     * detection.
     */
    unsigned char *_crc;

    /**
     * The whole message to send.
     */
    unsigned char *_wMessage;

    /**
     * Output to read.
     */
    unsigned char *_output;


  public:

    /**
     * Methods implemented in the code file (cpp).
     */

    // Basic methods: constructors and set properties.
    CommunicationNT(const char *serialPort);

    // Methods to manage the communication for Nanotec motors.
    void writeCommand( unsigned char *obj, int size, int data );
    long readCommand( unsigned char *obj, int size, int data ); // works for most commands
    unsigned char* readCommandFull( unsigned char *obj, int size, int data );
    long readCommand16bit( unsigned char *obj, int size, int data );
    void closePort();


  private:

    void initializeSerial(const char *serialPort);
    bool readSerial( int size );
    void writeSerial( unsigned char buffer[], int size );
    void sendCommand( unsigned char *obj, int size, int data, int numBits = 32 );
    unsigned char *decToHex( int value, int num, int mode );
    void buildWholeMessage( int datSize );
    unsigned int crc16modbus( unsigned char *buffer, int length );
};

#endif
