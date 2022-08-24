import socket
import sys

# declare our serverSocket upon which
# we will be listening for UDP messages

# Socket from Alice to helper 2
helperSockAlice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Socket from helper2 to Bob
helperSockBob = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Here we define the UDP IP address as well as the port number that we have
# already defined in the client python script.
	# Ip address example
	# UDP_IP_ADDRESS = "127.0.0.1"
	# UDP_PORT_NO = 6789

# Bind the socket to the IP address and port: use local host
server_address = ('localhost', 9999)

# Send data to Bob
client_2_address = ('localhost', 9998)

# Receive data from Alice
helperSockAlice.bind(server_address)

while True:
	print('\nHelper2 waiting to receive message from Alice', file=sys.stderr)
	data, address = helperSockAlice.recvfrom(128)

	print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
	print(data, file=sys.stderr)

	# Helper2 sends messages to Bob
	print('\nHelper2 sending messages to Bob', file=sys.stderr)
	sent = helperSockBob.sendto(data, client_2_address)

	"""The server sends data to some address
	if data:
		sent = sock.sendto(data, address)
		print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
	"""