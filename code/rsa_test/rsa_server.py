from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from hwcounter import Timer, count, count_end

import random
import socket
import os
import time

time_run_start = time.time()
CPU_start = count()

client_address = ('10.0.0.1', 10000)
server_address = ('10.0.0.2', 9999)

# Bind the socket to the port
serverSockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSockClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('starting up on %s port %s' % server_address)
serverSockClient.bind(server_address)

CPU_init_end = count_end() - CPU_start
time_init_end = time.time() - time_run_start

# Listen for incoming connections
serverSockClient.listen(1)

# while True:
# Wait for a connection

print('waiting for a connection')
connection, client_address = serverSockClient.accept()

try:
	print('connection from', client_address)
	time_latency_server_start = time.time()
	client_pkc = connection.recv(1024)
	time_sk_encrypt_start = time.time()
	CPU_sk_encrypt_start = count()
	time_latency_client_end = time.time() - time_latency_server_start

	file_out = open("client_pkc.pem", "wb")
	file_out.write(client_pkc)
	# ----------- print(client_pkc)

	file_out = open("encrypted_data1.bin", "wb")

	# Encrypt the session key with the public RSA key
	recipient_key = RSA.import_key(open("client_pkc.pem").read())
	print("\n\n", recipient_key.publickey())
	# Session key
	session_key = os.urandom(16)
	print("before", session_key)
	cipher_rsa = PKCS1_OAEP.new(recipient_key)
	enc_session_key = cipher_rsa.encrypt(session_key)
	# ------------ print("\n\n\n\n", enc_session_key)

	connection.sendall(enc_session_key)
	CPU_sk_encrypt_end = count_end() - CPU_sk_encrypt_start
	time_sk_encrypt_end = time.time() - time_sk_encrypt_start

	# Generates session key and encrypt it with client's public RSA key
	# recipient_key = RSA.import_key(open("receiver.pem").read())
	# session_key = os.urandom(16)
	# cipher_rsa = PKCS1_OAEP.new(recipient_key)
	# enc_session_key = cipher_rsa.encrypt(session_key)

	# print("\n\n\n\n", enc_session_key)

	# print("\n\n", recipient_key.publickey())

	# session_key = os.urandom(16)

	# # Encrypt the session key with the public RSA key
	# cipher_rsa = PKCS1_OAEP.new(recipient_key)
	# enc_session_key = cipher_rsa.encrypt(session_key)

    # Receive the data in small chunks and retransmit it
    # not_done = Ture
    # while not_done:
        # print >>sys.stderr, 'received "%s"' % data
        # if not data:
        #     print('sending data back to the client')
        #     connection.sendall(data)
        # else:
        #     print >>sys.stderr, 'no more data from', client_address
        #     break

finally:
	time_total_server = time_init_end + time_sk_encrypt_end
	time_total_CPU = CPU_init_end + CPU_sk_encrypt_end
	total_messages_send = len(enc_session_key)
	total_messages_receive = len(client_pkc)
	# Clean up the connection
	print("\n\nClient2 total running time is:", time_total_server)
	print("\n\nClient2 total waiting time is:", time_latency_client_end)
	print("Client 1 total CPU time is: ", time_total_CPU)
	print("Total message send: ", total_messages_send)
	print("Total message receive: ", total_messages_receive)
	print("Bandwidth: ", total_messages_receive + total_messages_send)
	print("connection closing...")
	connection.close()

	f = open("eval_rsa_2.txt", "a")
	f.write("\n" + str(time_total_server) + "\t" + str(time_latency_client_end) + "\t" + str(time_total_CPU))
	# f.write("\n\n\n" + "Client 2 total running time is: " + str(time_total_server))
	# f.write("\nClient 2 total latency time is: " + str(time_latency_client_end))
	# f.write("\nClient 2 total CPU time is: " + str(time_total_CPU))
	# f.write("\nTotal message send: " + str(total_messages_send))
	# f.write("\nTotal message receive: " + str(total_messages_receive))
	# f.write("\nBandwidth: " + str(total_messages_receive + total_messages_send))

	f.close()





