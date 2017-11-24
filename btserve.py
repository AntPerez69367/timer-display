# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
from text import *
import threading

class BluetoothServer(threading.Thread):
	def __init__(self):
		self.connected = False
		self.server_sock=BluetoothSocket( RFCOMM )
		self.server_sock.bind(("",PORT_ANY))
		self.server_sock.listen(1)
		self.port = self.server_sock.getsockname()[1]
		self.uuid = "00001101-0000-1000-8000-00805f9b34fb"
		myLED = Display()
		myLED.isDaemon = True
		myLED.start()

		advertise_service( self.server_sock, "TimerDisplay",
					   service_id = self.uuid,
					   service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
					   profiles = [ SERIAL_PORT_PROFILE ],
	#                   protocols = [ OBEX_UUID ]
						)

		while True:
			try:
				if not self.connected:
					self.hostbt()

				# Receive Data
				data = self.client_sock.recv(1024).decode()
				if len(data) == 0:
					pass
				else:
					print("received [%s]" % data)
					# Stop Command
					if data == '99':
						output = "Stop Command Acknowledge"
						self.client_sock.send(output.encode())
						myLED.sessionSet("00:00:00", 0)
						myLED.running = False
					else:
					# Start Command
						if myLED.running:
							print("Thread already started")
							pass
						else:
							output = "Start Command Acknowledge"
							self.client_sock.send(output.encode())
							args = data.split('_')
							myLED.sessionSet(args[0], args[2])
							myLED.running = True
							print ("Received Timer Data: %s" % (args[0]))
							print ("Received Survey Name: %s" % (args[1]))
							print ("Received Slide Length: %s" % (args[2]))
			except Exception as e:
				self.connected = False

		self.closeconnections()



	def hostbt(self):
		print("Waiting for connection on RFCOMM channel %d" % self.port)
		self.client_sock, self.client_info = self.server_sock.accept()
		print("Accepted connection from ", self.client_info)
		self.connected = True


	def send(self, output):
		try:
			print("Send command received")
			self.sock.send(output.encode())
		except Exception as e:
			print("Unable to send: %s" % (output))


	def closeconnections(self):
		print("disconnected")
		self.client_sock.close()
		self.server_sock.close()
		print("all done")

if __name__ == "__main__":
	btserver = BluetoothServer()
