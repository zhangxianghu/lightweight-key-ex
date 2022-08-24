import time
import socket
import os
import sys

from hwcounter import Timer, count, count_end
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# RFC 3526 - More Modular Exponential (MODP) Diffie-Hellman groups for 
# Internet Key Exchange (IKE) https://tools.ietf.org/html/rfc3526 

time_start = time.time()
CPU_start = count()

# Accept a TCP connection and bind the address
client_address = ('10.0.0.1', 10000)
server_address = ('10.0.0.2', 9999)
serverSockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSockClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('starting up on %s port %s' % server_address)
serverSockClient.bind(server_address)

CPU_server_socket_end = count_end() - CPU_start
time_server_socket_end = time.time() - time_start

# Listen for incoming connections
serverSockClient.listen(1)
print('waiting for a connection')
connection, client_address = serverSockClient.accept()

try:
	print('connection from', client_address)
	time_latency_server_start = time.time()
	client_serialized_public = connection.recv(1024)
	time_latency_server_end = time.time() - time_latency_server_start
	
	time_server_session_start = time.time()
	CPU_server_session_start = count()
	# Generate server's private key and public key for use in the exchange.
	client_public_key = serialization.load_pem_public_key(client_serialized_public,backend=default_backend())
	server_private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
	server_public_key = server_private_key.public_key()
	# serialize server's public key to send
	server_serialized_public = server_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
	# print("\nserver_serialized_public:", server_serialized_public)
	connection.sendall(server_serialized_public)

	# Session key generation
	shared_key = server_private_key.exchange(ec.ECDH(), client_public_key)
	# Perform key derivation.
	derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(shared_key)
	# print(shared_key)
	CPU_server_session_end = count_end() - CPU_server_session_start
	time_server_session_end = time.time() - time_server_session_start
finally:
	time_total_server = time_server_socket_end + time_server_session_end
	time_total_CPU = CPU_server_socket_end + CPU_server_session_end
	total_messages_send = len(server_serialized_public)
	total_messages_receive = len(client_serialized_public)
	# Clean up the connection
	print("\n\nClient 2 total running time is:", time_total_server)
	print("\n\nClient 2 total waiting time is:", time_latency_server_end)
	print("Client 2 total CPU time is: ", time_total_CPU)
	print("Total message send: ", total_messages_send)
	print("Total message receive: ", total_messages_receive)
	print("Bandwidth: ", total_messages_receive + total_messages_send)
	print("\nconnection closing...\n")
	connection.close()
	print(derived_key)
	print("\nSession end.")

	f = open("eval_ecc_2.txt", "a")
	f.write("\n" + str(time_total_server) + "\t" + str(time_latency_server_end) + "\t" + str(time_total_CPU))
	# f.write("\n" + str(time_latency_server_end))
	# f.write("\n" + str(time_total_CPU))
	# f.write("\n" + str(total_messages_send))
	# f.write("\n" + str(total_messages_receive))
	# f.write("\n" + str(total_messages_receive + total_messages_send))

	f.close()
