
'''
This program initiates communication with the On Board Diagnositics Engine Management Computer
The communication bus between the Raspberry Pi and the ELM327 interface chip is RS-232 with a baudrate of 115200
The OBD2 protocol of the test vehicle is ISO_9141-2
'''


import csv
import time
import serial
import obd
from datetime import datetime
from bluetooth import*

# Globol variables
ser = None
frame = None


# Establish an RFCOMM bluetooth socket
Blue_Sock = BluetoothSocket( RFCOMM )
Blue_Sock.setblocking( False )

port = 1
# bd_addr = '00:26:08:C4:9E:58'
bd_addr = '28:18:78:D9:C2:FC'

#**************************************************Functions**************************************************

# Establish communication via RS-232 and block until serial connection is acquired
def Open_ser_Communication():
	while True:
		try:
			ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=.3)	# ISO_9141-2 MAX stable response time is 300ms @115200
			return ser
		except:
			print 'pause'
			time.sleep(1)


# Establish/Restablish connection with remote bluetooth device
def Open_Bluetooth_Socket():
	try:
		New_Sock = BluetoothSocket( RFCOMM )
		New_Sock.connect((bd_addr, port))
		print 'Address: ', bd_addr, 'Port number: ', port, ' has been established'
		return New_Sock
	except IOError:
		print 'Socket failed to connect to ', bd_addr, 'Port number: ', port
		return


# Transmit packaged engine sensor payload
def Send_Bluetooth_Data(Transmit_Sock, data):
	try:
		Transmit_Sock.send(data)
	except IOError:
		print 'Packet lost containing: ', data


# Create CSV file for sensor data logging
# File resides on removable media
def Open_File_USB_Drive():
	try:
		ofile = open('/media/FILES/CSV/' + datetime.today().strftime('%Y-%m-%d-%H-%M') +'.csv', 'wb')
		Set_Frame = csv.writer(ofile)
		Set_Frame.writerow(['Time', 'RPM', 'Calculated Engine Load', 'Coolant Temp'])
		print 'CSV file created, engine data is being logged'
		return Set_Frame
	except IOError:
 		print 'USB is not present'
		print 'CSV Datalogging disabled'
		return None

#*********************************************Program_Execution*******************************************

ser = Open_ser_Communication()		# Establish communication with engine | Blocking
start_time = datetime.now()			# Timestamp of first communication with engine
frame = Open_File_USB_Drive() 		# Open sensor logging file
Blue_Sock = Open_Bluetooth_Socket() # Create RFCOMM socket
time.sleep(1)						# Pause for communcation syncing
#Blue_Sock.setblocking( False )
#ser.write('STSBR 115200\r')

if ser.isOpen():					# Print the condition of serial comm to terminal window
	print 'Serial port is open and communicating'

try:
	while(1):
		RPM = obd.getrpm(ser)
		Cooland_temp = obd.getcoolanttemp(ser)
		Engine_Load = obd.getengineload(ser)
		data = unicode(datetime.now()-start_time)+ ',' + unicode(RPM)+','+ unicode(Engine_Load)+ ',' + unicode(Cooland_temp)
		print Blue_Sock
		if frame:
			frame.writerow([datetime.now() - start_time,RPM,Engine_Load,Cooland_temp])
		if Blue_Sock:
			Send_Bluetooth_Data(Blue_Sock,data)
		else:
                        #print 'Socket messed up   ',Blue_Sock
			Blue_Sock = Open_Bluetooth_Socket()
		print data
		
except KeyboardInterrupt:
	ser.close()
	Blue_Sock.close()
	print ser.isOpen()
	exit(0)
except serial.SerialException:
	ser.close()
	Blue_Sock.close()
	print ser.isOpen()
	exit(0)
