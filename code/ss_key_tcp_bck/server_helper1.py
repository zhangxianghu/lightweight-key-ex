import socket
import sys

""" Security level"""
sec_lev = 128

""" Number of test keys
	Modify this part for more test keys
"""
num_tk = 10

end_message = b"Closing socket"

server3_address = ('10.0.0.6', 10001)
server2_address = ('10.0.0.5', 10000)
server1_address = ('10.0.0.4', 9999)
client2_address = ('10.0.0.2', 9998)
client1_address = ('10.0.0.1', 9997)

share_list = []

# server1 socket with Alice, receive shares
server1SockAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('starting up on %s port %s' % server1_address)
server1SockAlice.bind(server1_address)

# Listen for incoming connections
server1SockAlice.listen(1)
print('waiting for a connection from Alice')
connection, client_address = server1SockAlice.accept()
print('connection from', client_address)

# server1 socket with Bob, forward shares
server1SockBob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('connecting to %s port %s' % client2_address)
# server1SockBob.connect(client2_address)

receive = ""

try:
	# while True:
	for i in range(num_tk):
		data = connection.recv(sec_lev)
		# print("\nreceived data:", data)
		# if data == end_message:
		# 	print("-------true")
		# 	break
		# else:
		share_list.append(data)
finally:
	# Clean up the connection
	print("\nconnection closing...\n")
	connection.close()
	print("\nSession end.")

try:
	server1SockBob.connect(client2_address)
	for share in share_list:
		# print(share)
		server1SockBob.sendall(share)
	# server1SockBob.sendall(b"Closing socket")
except:
	print("error")

server1SockBob.close()
# print(share_list)
# print("\n\n", receive)
# server1SockBob.sendall(b"test")
# print(share_list)

