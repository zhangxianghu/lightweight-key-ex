from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from hwcounter import Timer, count, count_end

import random
import socket
import os
import time

time_client_start = time.time()
CPU_start = count()

client_address = ('10.0.0.1', 10000)
server_address = ('10.0.0.2', 9999)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('connecting to %s port %s' % server_address)

key = RSA.generate(3072)

CPU_client_key_end = count_end() - CPU_start
time_client_key_end = time.time() - time_client_start

# session_key = os.urandom(16)
time_private_start = time.time()
CPU_private_start = count()
private_key = key.export_key()
CPU_private_end = count_end() - CPU_private_start
time_private_end = time.time() - time_private_start

file_out = open("private.pem", "wb")
file_out.write(private_key)
# print(private_key)

time_public_start = time.time()
CPU_public_start = count()
public_key = key.publickey().export_key()
CPU_public_end = count_end() - CPU_public_start
time_public_end = time.time() - time_public_start
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
# print(public_key)
sock.connect(server_address)
try:
	# Send public key
	# ----------- print('sending "%s"' % public_key)
	sock.sendall(public_key)
	# Receive the encrypted session key
	time_latency_client_start = time.time()
	enc_session_key = sock.recv(1024)

	# ----------- print("--------", enc_session_key)
	time_latency_client_end = time.time() - time_latency_client_start

	# Decrypt and obtain the session key
	private_key = RSA.import_key(open("private.pem").read())
	time_session_key_start = time.time()
	CPU_session_key_start = count()
	cipher_rsa = PKCS1_OAEP.new(private_key)
	session_key = cipher_rsa.decrypt(enc_session_key)

	print("after:", session_key)
finally:
	CPU_session_key_end = count_end() - CPU_session_key_start
	time_session_key_end = time.time() - time_session_key_start
	time_total_client = time_client_key_end + time_session_key_end + time_public_end + time_private_end
	time_total_CPU = CPU_client_key_end + CPU_session_key_end + CPU_public_end + CPU_private_end
	total_messages_send = len(public_key)
	total_messages_receive = len(enc_session_key)

	print("\n\nClient total running time is:", time_total_client)
	print("\n\nClient total waiting time is:", time_latency_client_end)
	print("Client 1 total CPU time is: ", time_total_CPU)
	print("Total message send: ", total_messages_send)
	print("Total message receive: ", total_messages_receive)
	print("Bandwidth: ", total_messages_receive + total_messages_send)
	print('closing socket')
	print("\nSession end.")
	sock.close()

	f = open("eval_rsa_1.txt", "a")
	f.write("\n" + str(time_total_client) + "\t" + str(time_latency_client_end) + "\t" + str(time_total_CPU))
	# f.write("\n\n\n" + "Client 1 total running time is: " + str(time_total_client))
	# f.write("\nClient 1 total latency time is: " + str(time_latency_client_end))
	# f.write("\nClient 1 total CPU time is: " + str(time_total_CPU))
	# f.write("\nTotal message send: " + str(total_messages_send))
	# f.write("\nTotal message receive: " + str(total_messages_receive))
	# f.write("\nBandwidth: " + str(total_messages_receive + total_messages_send))

	f.close()


# data = "I met aliens in UFO. Here is the map.".encode("utf-8")
# file_out = open("encrypted_data.bin", "wb")

# recipient_key = RSA.import_key(open("receiver.pem").read())

# print("\n\n", recipient_key.publickey())

# session_key = os.urandom(16)
# print("before", session_key)

# # Encrypt the session key with the public RSA key
# cipher_rsa = PKCS1_OAEP.new(recipient_key)
# enc_session_key = cipher_rsa.encrypt(session_key)

# cipher_aes = AES.new(session_key, AES.MODE_EAX)
# ciphertext, tag = cipher_aes.encrypt_and_digest(data)
# [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

# print("\n\n\n\n", enc_session_key)

# file_in = open("encrypted_data.bin", "rb")
# private_key = RSA.import_key(open("private.pem").read())

# # enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

# # Decrypt the session key with the private RSA key
# cipher_rsa = PKCS1_OAEP.new(private_key)
# session_key = cipher_rsa.decrypt(enc_session_key)

# print("after:", session_key)

# f = open('mykey.pem','wb')
# f.write(key.export_key('PEM'))
# f.close()

# f = open('mykey.pem','r')
# key = RSA.import_key(f.read())

# aliceSockHelper = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address = ('localhost', 10000)
# server_2_address = ('localhost', 9999)

#Here we define the UDP IP address as well as the port number that we have
# already defined in the client python script.
	# Ip address example
	# UDP_IP_ADDRESS = "127.0.0.1"
	# UDP_PORT_NO = 6789


# for i in index_set:
# 	shares = Shamir.split(2, 2, key_list[i])
# 	key_list_shares.append(shares)
# 	sent = aliceSockHelper.sendto(shares[0][1], server_address)
# 	# print("Alice sending messages to helper2, share 2:")
# 	# print(shares,"\n")
# 	sent = aliceSockHelper.sendto(shares[1][1], server_2_address)

# sent = aliceSockHelper.sendto(end_message, server_address)
# sent = aliceSockHelper.sendto(end_message, server_2_address)
