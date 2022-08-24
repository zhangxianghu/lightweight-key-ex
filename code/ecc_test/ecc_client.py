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

time_start = time.time()
CPU_start = count()

# Create TCP connection with server
client_address = ('10.0.0.1', 10000)
server_address = ('10.0.0.2', 9999)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

# Generate client's private key and public key for use in the exchange.
client_private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
client_public_key = client_private_key.public_key()
# serialize client's public key to send
client_serialized_public = client_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

try:
	# send client's serialized public key
	sock.sendall(client_serialized_public)
	CPU_client_key_end = count_end() - CPU_start
	time_client_key_end = time.time() - time_start
	# print("\nclient_serialized_public:", client_serialized_public)
	# receive server's serialized public key
	time_latency_client_start = time.time()
	server_serialized_public = sock.recv(1024)
	time_latency_client_end = time.time() - time_latency_client_start
	# print("\nserver_serialized_public:", server_serialized_public)
	
	time_client_sk_start = time.time()
	CPU_client_sk_start = count()
	# Session key generation
	server_public_key = serialization.load_pem_public_key(server_serialized_public,backend=default_backend())
	shared_key = client_private_key.exchange(ec.ECDH(), server_public_key)
	# Perform key derivation.
	derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(shared_key)
	# print(shared_key)
	# print(derived_key)
	CPU_client_sk_end = count_end() - CPU_client_sk_start
	time_client_sk_end = time.time() - time_client_sk_start
finally:
	time_total_client = time_client_key_end + time_client_sk_end
	time_total_CPU = CPU_client_key_end + CPU_client_sk_end
	total_messages_send = len(client_serialized_public)
	total_messages_receive = len(server_serialized_public)

	print("\n\nClient1 total running time is:", time_total_client)
	print("\n\nClient1 total waiting time is:", time_latency_client_end)
	print("Client 1 total CPU time is: ", time_total_CPU)
	print("Total message send: ", total_messages_send)
	print("Total message receive: ", total_messages_receive)
	print("Bandwidth: ", total_messages_receive + total_messages_send)
	print('\nclosing socket\n')
	sock.close()
	print(derived_key)
	print("\nSession end.")

	f = open("eval_ecc_1.txt", "a")
	f.write("\n" + str(time_total_client) + "\t" + str(time_latency_client_end) + "\t" + str(time_total_CPU))
	# f.write("\n\n\n" + "Client 1 total running time is: " + str(time_total_client))
	# f.write("\nClient 1 total latency time is: " + str(time_latency_client_end))
	# f.write("\nClient 1 total CPU time is: " + str(time_total_CPU))
	# f.write("\nTotal message send: " + str(total_messages_send))
	# f.write("\nTotal message receive: " + str(total_messages_receive))
	# f.write("\nBandwidth: " + str(total_messages_receive + total_messages_send))

	f.close()



