# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
from text import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "00001101-0000-1000-8000-00805f9b34fb"

advertise_service( server_sock, "TimerDisplay",
				   service_id = uuid,
				   service_classes = [ uuid, SERIAL_PORT_CLASS ],
				   profiles = [ SERIAL_PORT_PROFILE ],
#                   protocols = [ OBEX_UUID ]
					)
myLED = Display()

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
	myLED.sessionSet('00:00:00', 0)
	myLED.start()
	while True:
		data = client_sock.recv(1024).decode()
		if len(data) == 0:
			pass
		else:
			print("received [%s]" % data)
			if data == '99':
				if myLED.isAlive():

			else:
				args = data.split('_')
				myLED.sessionSet(args[0], args[2])
				print ("Received Timer Data: %s" % (args[0]))
				print ("Received Survey Name: %s" % (args[1]))
				print ("Received Slide Length: %s" % (args[2]))

except IOError:
		pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

