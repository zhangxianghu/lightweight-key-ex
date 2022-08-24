import dh
import time
import socket
import os
import sys

from hwcounter import Timer, count, count_end
# RFC 3526 - More Modular Exponential (MODP) Diffie-Hellman groups for 
# Internet Key Exchange (IKE) https://tools.ietf.org/html/rfc3526 
time_start = time.time()
CPU_start = count()

client_address = ('10.0.0.1', 10000)
server_address = ('10.0.0.2', 9999)

# Bind the socket to the port
serverSockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSockClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('starting up on %s port %s' % server_address)
serverSockClient.bind(server_address)

# time_init_end = time.time() - time_run_start

# Listen for incoming connections
serverSockClient.listen(1)

# while True:
# Wait for a connection
CPU_d2_key_end = count_end() - CPU_start
time_d2_key_end = time.time() - time_start

print('waiting for a connection')
connection, client_address = serverSockClient.accept()

try:
	print('connection from', client_address)

	time_latency_server_start = time.time()
	d1_pubkey_byte = connection.recv(512)
	time_latency_server_end = time.time() - time_latency_server_start

	time_share_key_start = time.time()
	CPU_share_key_start = count()
	d2 = dh.DiffieHellman(16)
	
	d2_pubkey = d2.gen_public_key()
	# print(d1_pubkey_byte)
	d1_pubkey = int.from_bytes(d1_pubkey_byte, sys.byteorder, signed = False)
	d2_sharedkey = d2.gen_shared_key(d1_pubkey)
	# print("####")
	print(d2_sharedkey)

	connection.sendall((d2_pubkey).to_bytes(512, sys.byteorder, signed = False))
	CPU_share_key_end = count_end() - CPU_share_key_start
	time_share_key_end = time.time() - time_share_key_start
	# time_latency_client_end = time.time() - time_latency_server_start

	# time_sk_encrypt_start = time.time()
	# file_out = open("client_pkc.pem", "wb")
	# file_out.write(client_pkc)
	# ----------- print(client_pkc)

	# file_out = open("encrypted_data1.bin", "wb")

	# Encrypt the session key with the public RSA key
	# recipient_key = RSA.import_key(open("client_pkc.pem").read())
	# ------------ print("\n\n", recipient_key.publickey())
	# Session key
	# session_key = os.urandom(16)
	# print("before", session_key)
	# cipher_rsa = PKCS1_OAEP.new(recipient_key)
	# enc_session_key = cipher_rsa.encrypt(session_key)
	# ------------ print("\n\n\n\n", enc_session_key)

	# connection.sendall(enc_session_key)

	# time_sk_encrypt_end = time.time() - time_sk_encrypt_start

finally:
	time_total_server = time_d2_key_end + time_share_key_end + 0
	time_total_CPU = CPU_d2_key_end + CPU_share_key_end
	total_messages_send = len((d2_pubkey).to_bytes(512, sys.byteorder, signed = False))
	total_messages_receive = len(d1_pubkey_byte)
	# Clean up the connection
	print("\n\nServer total running time is:", time_total_server)
	print("\n\nServer total waiting time is:", time_latency_server_end)
	print("Client 1 total CPU time is: ", time_total_CPU)
	print("Total message send: ", total_messages_send)
	print("Total message receive: ", total_messages_receive)
	print("Bandwidth: ", total_messages_receive + total_messages_send)
	print("connection closing...")
	connection.close()

	f = open("eval_dh_2.txt", "a")
	f.write("\n" + str(time_total_server) + "\t" + str(time_latency_server_end) + "\t" + str(time_total_CPU))
	# f.write("\n\n\n" + "Client 2 total running time is: " + str(time_total_server))
	# f.write("\nClient 2 total latency time is: " + str(time_latency_server_end))
	# f.write("\nClient 2 total CPU time is: " + str(time_total_CPU))
	# f.write("\nTotal message send: " + str(total_messages_send))
	# f.write("\nTotal message receive: " + str(total_messages_receive))
	# f.write("\nBandwidth is: " + str(total_messages_receive + total_messages_send - 128*2))

	f.close()

# d1_sharedkey = d1.gen_shared_key(d2_pubkey)
# d2_sharedkey = d2.gen_shared_key(d1_pubkey)
# d1_sharedkey == d2_sharedkey

# end_time = time.time() - start_time

# print(d1_sharedkey)
# print(d2_sharedkey)
# print(end_time)