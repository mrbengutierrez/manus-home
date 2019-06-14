/**
 * Class CommunicationNT, code file with constructors and all methods.
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
 * Including own libraries.
 */
#include "CommunicationNT.h"



/************** Basic methods: constructors and set properties **************/



/**
 * Default Constructor.
 */
CommunicationNT::CommunicationNT(const char *serialPort)
{
  _header = (unsigned char *)malloc(sizeof(unsigned char)*2);
  memcpy( _header, (unsigned char *)"\x4E\x54", 2 );
  _length = (unsigned char *)malloc(sizeof(unsigned char)*2);
  _modbusEncap = (unsigned char *)malloc(sizeof(unsigned char)*3);
  memcpy( _modbusEncap, (unsigned char *)"\x05\x2B\x0D", 3 );
  _mode = (unsigned char *)malloc(sizeof(unsigned char)*2);
  _can = (unsigned char *)malloc(sizeof(unsigned char)*1);
  memcpy( _can, (unsigned char *)"\x01", 1 );
  _objIdxSub = (unsigned char *)malloc(sizeof(unsigned char)*3);
  _startAddr = (unsigned char *)malloc(sizeof(unsigned char)*2);
  memcpy( _startAddr, (unsigned char *)"\x00\x00", 2 );
  _dataSize = (unsigned char *)malloc(sizeof(unsigned char)*2);
  _data = (unsigned char *)malloc(sizeof(unsigned char)*MAXDAT);
  _crc = (unsigned char *)malloc(sizeof(unsigned char)*2);
  _wMessage = (unsigned char *)malloc(sizeof(unsigned char)*MAXLEN);
  _output = (unsigned char *)malloc(sizeof(unsigned char)*MAXLEN);
  
  
  initializeSerial(serialPort);
}



/********** Methods to manage the communication for Nanotec motors **********/



/**
 * Method to initialize the configuration to read and write using serial
 * communication via the USB port.
 */
void CommunicationNT::initializeSerial(const char *serialPort)
{
  // Opening the port /dev/ttyUSB0 or /dev/ttyACM0 to read and write.
  // Non blocking mode.
  _fd = open( serialPort, O_RDWR | O_NOCTTY );// | O_NDELAY

  // If the port is open.
  if ( _fd != -1 )
  {
    // Configure port reading
    //fcntl( _fd, F_SETFL, FNDELAY );
    // Main structure to configure options.
    struct termios options;
    // Get the current options for the port.
    tcgetattr( _fd, &options );
    // Set the baud rates to 19200 (Nanotec motors) for input and output.
    cfsetispeed( &options, B19200 );
    cfsetospeed( &options, B19200 );
    options.c_cflag &= ~PARENB; // No parity, 1 stop bit (8N1).
    options.c_cflag &= ~CSTOPB;
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8; // 8 data bits.
    // Turn off hardware flow control.
    options.c_cflag &= ~CRTSCTS;
    // Enable the receiver and set local mode.
    options.c_cflag |= CLOCAL | CREAD;
    options.c_iflag &= ~(IXON | IXOFF | IXANY); // To disable i/o control.
    // To sent raw data. It is unprocessed, so they may be used as they are read
    // To disable canonical input, echo, visually erase chars, terminal signals.
    options.c_lflag &= ~( ICANON | ECHO | ECHOE | ISIG);
    //options.c_oflag &= ~OPOST; // Disable output processing.
    options.c_cc[VMIN] = 1; // Wait 10 characters come in before read returns.
    options.c_cc[VTIME] = 0; // No minimum time to read before read returns.
    // Write our changes to the port configuration.
    tcsetattr( _fd, TCSANOW, &options );
 
    // Wait for the nanotec motor to reset.
    usleep(1000*1000);
    tcflush( _fd, TCIFLUSH );
  }
  else
  {
    cout << "Error in serial port" << endl;
    perror("Opening");
    closePort();
    exit(0);
  }
}


/**
 * Function to read the data coming from the serial communication.
 *
 * @param m  Size of the buffer to read those m characters
 *
 * @return  true if the value is 1, false if it is 0.
 */
bool CommunicationNT::readSerial( int size )
{
  // Initializing buffer.
  unsigned char buffer = ' ';

  // Reading from the serial port.
  int result = 0;
  if ( _fd != -1 )
  {
    if ( DEBUG )
      cout << "  Receiving: " << endl;
    for ( int i=0; i<size; i++)
    {
      // Reading one byte with an hex value at a time.
      result = read( _fd, &buffer, sizeof(buffer) );     
      if ( result == -1 )
        cout << "Error Receiving!" << endl;
      if ( DEBUG )
        printf("%02X-", buffer );
      _output[i] = buffer;
    }
    if ( DEBUG )
      printf("\n\n");
    return true;
  }

  return false;
}


/**
 * Method to send the x and y coordinates to the Arduino with the serial
 * communication.
 *
 * @param buffer  Message to send. Unsigned char to send hex values
 */
void CommunicationNT::writeSerial( unsigned char buffer[], int size )
{
  // Sending data to the serial port.
  int result = 0;
  if ( _fd != -1 ) // If the port is open.
  {
    //if ( DEBUG )//|| ( _lastTor < 11 && _lastTor > 0 ) )
    if ( DEBUG )
    {
      cout << "  Sending (" << size << "):" << endl;
      for ( int i=0; i<size; i++ )
        printf("%02X ", buffer[i] );
      printf("\n");
    }
    result = write( _fd, buffer, size );
    if ( result == -1 )
      cout << "Error Receiving!" << endl;
    //cout << " Res: " << result << endl; // -1 error.
  }
  else
    cout << "Closed port" << endl;
}


/**
 * Method to close the port of the serial communication.
 */
void CommunicationNT::closePort()
{
  // If the port is open, it will close.
  if ( _fd != -1 )
    close( _fd );
}

  

  
/**
 * Method to prepare the message of bytes to send the corresponding command in read mode.
 *
 * @param obj  Object Index with Subindex
 * @param size  Size of the data in bytes
 * @param data  Data value
 * 
 * @param useful part of message sent back in decimal
 */
long CommunicationNT::readCommand( unsigned char *obj, int size, int data ) //unsigned char *siz, unsigned char *dat ) 
{
  // Read mode. 
  memcpy( _mode, (unsigned char *)"\x00\x00", 2 );

  // Send and read the output.
  sendCommand( obj, size, data );

  // convert hex output of return message to decimal
  unsigned int dec[4];
  dec[0] = _output[20];
  dec[1] = _output[19];
  dec[2] = _output[18];
  dec[3] = _output[17];
  unsigned long output = 0; // multiply by 16^0, 16^2, 16^4, 16^6.
  output = dec[3]+dec[2]*256+dec[1]*65536+dec[0]*16777216;
  return output;
}	


/**
 * Method to prepare the message of bytes to send the corresponding command in read mode.
 *
 * @param obj  Object Index with Subindex
 * @param size  Size of the data in bytes
 * @param data  Data value
 * 
 * @param full message sent back as full character array
 */
unsigned char* CommunicationNT::readCommandFull( unsigned char *obj, int size, int data ) //unsigned char *siz, unsigned char *dat ) 
{
  // Read mode. 
  memcpy( _mode, (unsigned char *)"\x00\x00", 2 );

  // Send and read the output.
  sendCommand( obj, size, data );
  return _output;
}	
  



/**
 * Method to prepare the message of bytes to send the corresponding command in write mode.
 *
 * @param obj  Object Index with Subindex
 * @param size  Size of the data in bytes
 * @param data  Data value
 */
void CommunicationNT::writeCommand( unsigned char *obj, int size, int data ) //unsigned char *siz, unsigned char *dat ) 
{
	// Write mode. 
    memcpy( _mode, (unsigned char *)"\x01\x00", 2 );
	
	// send the command
	sendCommand( obj, size, data );
}



long CommunicationNT::readCommand16bit( unsigned char *obj, int size, int data ) //unsigned char *siz, unsigned char *dat ) 
{
  // Read mode. 
  memcpy( _mode, (unsigned char *)"\x00\x00", 2 );

  // Send and read the output.
  int numBits = 16;
  sendCommand( obj, size, data, numBits );

  // convert hex output of return message to decimal
  short dec[4];
  dec[0] = _output[17];
  dec[1] = _output[18];
  short output = 0; // multiply by 16^0, 16^2
  output = dec[0]+dec[1]*256;
  return output;
}


/**
 * Method to prepare the message of bytes to send the corresponding command.
 *
 * @param obj  Object Index with Subindex
 * @param size  Size of the data in bytes
 * @param data  Data value
 * @param numBits number of bits of return message (optional)
 */
void CommunicationNT::sendCommand( unsigned char *obj, int size, int data, int numBits) //unsigned char *siz, unsigned char *dat )
{
  memcpy( _length, (unsigned char *)decToHex( MINLEN+size+2, 2, 1 ), 2 );
  memcpy( _objIdxSub, obj, 3 );
  memcpy( _dataSize, (unsigned char *)decToHex( size, 2, 1 ), 2 );
  if ( size > 0 )
    memcpy( _data, (unsigned char *)decToHex( data, size, 0 ), size );

  buildWholeMessage( size );
  writeSerial( _wMessage, MINLEN+size+6 );
  
  if (numBits == 32) {
	  if ( size > 0 ) {
		readSerial( 19 ); // 0 bit return message
	} else {
		readSerial( 23 ); // 32 bit return message
	}
  } else if (numBits == 16) {
	  readSerial(21);  // 16 bit return message
  }
	
		
}


/**
 * Function to convert a decimal to a hexadecimal value.
 *
 * @param value  Value in decimal to convert to hexadecimal
 * @param num  Number of bytes in the output
 * @param mode  0 for reverse, 1 for normal
 */
unsigned char *CommunicationNT::decToHex( int value, int num, int mode )
{
  //printf( "val: %d\n", value );
  char arrayNums[num*2]; // Array with hex calculated in hex.
  int i = 0, residue = 0;
  for ( i=0; i<num*2; i++ ) // Initialize array with zeros.
    arrayNums[i] = '0';

  i = 0;
  while ( value > 0 && i<num*2 )
  {
    residue = value % 16;
    //printf( "res: %d\n", residue );

    // Asign values in hex using ascii table (numbers and upper case letters).
    arrayNums[i++] = ( residue < 10 ) ? (char)residue+48 : (char)residue+55;

    value /= 16;
  }

 // Array with hex values to fill.
  unsigned char *arrayHex = (unsigned char *)malloc(sizeof(unsigned char)*num);
  char chars[3]; // Temporal array of chars.
  unsigned int hexInt; // Temporal integer to store the hex value.
  int k = ( mode == 0 ) ? 0 : num-1; 
  // Loop to convert the array of chars with the hex digits to a unsigned char.
  for ( i=0; i<num*2; i+=2 )
  {
    sprintf( chars, "%c%c", arrayNums[i+1], arrayNums[i] );
    //printf("tempChars: %s\n", chars );
    sscanf( chars, "%02x", &hexInt );
    if ( mode == 0 )
      arrayHex[k++] = (unsigned char)hexInt;
    else
      arrayHex[k--] = (unsigned char)hexInt;
  }
  return arrayHex;
}


/**
 * Method to build the whole message with the bytes in the corresponding order.
 *
 * @param datSize  Size of the data in bytes
 */
void CommunicationNT::buildWholeMessage( int datSize )
{
  //printf("len: %d\n", MINLEN+datSize );
  // First, we need to build the internal message.
  // Concatenate all the corresponding bytes in order.
  unsigned char *message =(unsigned char *)malloc(sizeof(unsigned char)*MINLEN+datSize);
  memcpy( message, _modbusEncap, 3 );
  memcpy( message+3, _mode, 2 );
  memcpy( message+5, _can, 1 );
  memcpy( message+6, _objIdxSub, 3 );
  memcpy( message+9, _startAddr, 2 );
  memcpy( message+11, _dataSize, 2 );
  if ( datSize > 0 )
    memcpy( message+13, _data, datSize );

  // Calculate the CRC for the message and convert it to unsigned char *.
  unsigned char *arrayHex = (unsigned char *)malloc(sizeof(unsigned char)*2);
  char charArr[5]; // Temporal array of chars.
  unsigned int hexInt; // Temporal integer to store the hex value.
  sprintf( charArr, "%04X", crc16modbus( message, MINLEN+datSize ) );
  sscanf( &charArr[0], "%02x", &hexInt );
  arrayHex[1] = (unsigned char)hexInt;
  sscanf( &charArr[2], "%02x", &hexInt );
  arrayHex[0] = (unsigned char)hexInt;
  memcpy( _crc, (unsigned char *)arrayHex, 2 );

  // Now build the whole message to be send.
  // Concatenate all the corresponding bytes in order.
  memcpy( _wMessage, _header, 2 );
  memcpy( _wMessage+2, _length, 2 );
  memcpy( _wMessage+4, message, MINLEN+datSize );
  memcpy( _wMessage+4+MINLEN+datSize, _crc, 2 );
  /*
  for ( int i=0; i<MINLEN+datSize+6; i++ )
    printf("%02X ", _wMessage[i] );
  printf("\n");
  */
}


/**
 * Function to calculate the CRC of the message.
 *
 * @param buffer  Message
 * @param length  Length of the message
 *
 * @return  CRC value in 2 bytes as int
 */
unsigned int CommunicationNT::crc16modbus( unsigned char *buffer, int length )
{
  /*
  printf("mes (%d):", length );
  for ( int i=0; i<length; i++ )
    printf("%02X ", buffer[i] );
  printf("\n");
  */
  unsigned int crc = 0xFFFF;
  for ( int i=0; i<length; i++ )
  {
    crc ^= (unsigned int)buffer[i];    // XOR byte to LSB.
  
    for ( int j=8; j!=0; j-- ) // For each bit.
      if ( (crc & 0x0001) != 0 ) // LSB in 1.
      {
        crc >>= 1; // Shift right.
        crc ^= 0xA001; // XOR.
      }
      else 
        crc >>= 1;
  }
  //printf("crc: %d\n", crc ); 
  return crc;
}

