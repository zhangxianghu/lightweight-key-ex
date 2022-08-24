import socket
import sys

""" Security level"""
sec_lev = 128

""" Number of test keys
	Modify this part for more test keys
"""
num_tk = 10

helper_index = b"3"
share_list = [helper_index]

end_message = b"Closing socket"

server4_address = ('10.0.0.7', 10002)
server3_address = ('10.0.0.6', 10001)
server2_address = ('10.0.0.5', 10000)
server1_address = ('10.0.0.4', 9999)
client2_address = ('10.0.0.2', 9998)
client1_address = ('10.0.0.1', 9997)

# server3 socket with Alice, receive shares
server3SockAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('starting up on %s port %s' % server3_address)
server3SockAlice.bind(server3_address)

# Listen for incoming connections
server3SockAlice.listen(1)
# print('waiting for a connection from Alice')
connection, client_address = server3SockAlice.accept()
# print('connection from', client_address)

# server3 socket with Bob, forward shares
server3SockBob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('connecting to %s port %s' % client2_address)
# server3SockBob.connect(client2_address)

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
	# print("\nconnection closing...\n")
	connection.close()
	print("\nSession end.")

try:
	server3SockBob.connect(client2_address)
	for share in share_list:
		print(share)
		server3SockBob.sendall(share)
	# server3SockBob.sendall(b"Closing socket")
except:
	print("error")

server3SockBob.close()
print(share_list)
# print("\n\nreceive", receive)
# server3SockBob.sendall(b"test")
# print(share_list)

