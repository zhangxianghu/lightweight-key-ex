import socket
import sys
import base64
import os
import json
import random
import time

from Crypto.Protocol.SecretSharing import Shamir
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from binascii import hexlify

start_time = time.time()

"""number of test keys and their indices for cut-and-choose"""
index_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# Dictionary for test key shares on client 2
test_key = {}

# number of helpers
helpers = 2

# number of test keys
num_tk = 10

# opening set
open_tk = []

# Store shares of received messages from Bob and it is used for reconstructing each test kyes
share_temp = []

# Store shares for checking
share_from_helper = []

# Reconstructed test keys which are used to decrypt encrypted session key
key_list = []

# session key list, choose the majority for real session key 
temp_sk = []

# Addresses for helpers
address_list = []

#Here we define the UDP IP address as well as the port number that we have
# already defined in the client python script.
	# Ip address example
	# UDP_IP_ADDRESS = "127.0.0.1"
	# UDP_PORT_NO = 6789
bobSockHelper = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the IP address and port: use local host
server_address = ('localhost', 9998)

# Receive data from Helpers
bobSockHelper.bind(server_address)

# print("test key is:", test_key)
temp = helpers

time_init_end = time.time() - start_time

# ------------ print("Bob receiving test key shares from helpers:\n")

while temp != 0:
	# print('\nBob waiting to receive message', file=sys.stderr)
	time_latency_helper_start = time.time()
	data, address = bobSockHelper.recvfrom(128)

	if data == b"Closing socket":
		temp -= 1
		# print(helpers)
	else: 
		# ----------- print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
		print(data, file=sys.stderr)
		if address not in address_list:
			address_list.append(address)

		if address in test_key:
			test_key[address].append(data)
		else: 
			test_key[address] = [data]
	# print("test key ----:", test_key)

time_latency_helper_end = time.time() - time_latency_helper_start

# print("test key ----:", test_key)
# --------------- print("\nTest key shares from helpers are received!\n")

# --------------- print("\nBob reconstructing test keys:\n")
time_combine_start = time.time()

for i in range(num_tk):
	k = 1
	share_temp = []
	for j in test_key:
		# print("test")
		# print("\ntest kyes", share_temp)
		share_temp.append((k, test_key[j][i]))
		# print("\ntest kyes", share_temp)
		k += 1
	share_from_helper.append(share_temp)
	key_list.append(Shamir.combine(share_temp))
	# print("test keys", Shamir.combine(share_temp))
# ------------- print("\nreconstruction completed!\n")

# print("key_list", key_list)

# ---------------- print('closing socket of helpers to Bob\n\n\n', file=sys.stderr)
bobSockHelper.close()

time_combine_end = time.time() - time_combine_start

time_share_alice_start = time.time()

# Confirm and ask for encrypted session key
key_confirm = b"key received"
client_address = ('localhost', 9997)
# Create socket for Bob to receive messages from Alice.
bobSockAlice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bobSockAlice.bind(server_address)

"""opening keys set: index of key_list"""
# ---------- print("\nBob starts to choose evaluation set and send it to Alice:")
eval_list = list(random.sample(range(10), 5))
# ---------- print(eval_list)
sent = bobSockAlice.sendto(bytearray(eval_list), client_address)
# ---------- print(bytearray(eval_list))
# ---------- print("\nSending evaluation set completed!")

"""Bob recives openning shares from Alice"""
# ---------- print("\nBob wating for openning shares from Alice:\n")

"""Bob check share consistent, if not, send cheating helpers to Alice.
   If this part is unnecessary, comment following part
"""
open_list = list(index_set.difference(set(eval_list)))

test_key = []

# ---------- print(open_list)

time_share_alice_end = time.time() - time_share_alice_start

time_latency_share_alice_start = time.time()
while True:
	data, address = bobSockAlice.recvfrom(128)
	# print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
	# print("This is the opening shares from Alice:")
	# print(data, file=sys.stderr)
	if data == b"oss":
		break
	test_key.append(data)
time_latency_share_alice_end = time.time() - time_latency_share_alice_start

time_checking_start = time.time()
k = 0
cheat_flag = 0
for i in open_list:
	j = 0
	# ------- print(share_from_helper[i][j])
	# ------- print(test_key[k])
	if share_from_helper[i][j][1] != test_key[k]:
		# Add cheating message and send it to Alice
		cheat_flag = 1
		break
		# print("True---")
	# else:
		# print("false++++++")
		# break
	# print(share_from_helper[i][j+1])
	k += 1
	# --------- print(test_key[k])
	if share_from_helper[i][j+1][1] != test_key[k]:
		# Add cheating message and send it to Alice
		cheat_flag = 1
		break
		# print("True again------")
	# else:
		# print("false++++++")
		# break
	k += 1
# ----------- if(cheat_flag == 0):
# -----------	print("\npass the checking phase!!!\n")
# ----------- print("\n\n\nreceived all opening shares from Alice and checking completed!!")
"""If this part is unnecessary, comment following part"""

# ---------- print("\nBob sending confirm message to Alice\n")

# Bob sending confirm messages to Alice to notify Alice that all test keys are received
sent = bobSockAlice.sendto(key_confirm, client_address)
# ---------- print("Confirm message sent!")

time_checking_end = time.time() - time_checking_start

# Bob receives encrypted session key from Alice, choose either 1 of the following 2

time_decrypt = 0
time_latency_decrypt = 0

"""1. The following is to receive evaluation set of ciphertexts"""
# ----------- print("Bob receiving encrypted session key from Alice:\n")
for j in eval_list:
	# print('\nBob waiting to receive encrypted session key from Alice', file=sys.stderr)
	time_latency_decrypt_start = time.time()
	data, address = bobSockAlice.recvfrom(128)
	time_latency_decrypt = time_latency_decrypt + (time.time() - time_latency_decrypt_start)
	# ------------- print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
	# print(data, file=sys.stderr)
# Decryption of the session key
	time_decryption_start = time.time()
	key = key_list[j]
	result = data.decode('utf-8')
	b64 = json.loads(result)
	iv = b64decode(b64['iv'])
	ct = b64decode(b64['ciphertext'])
	cipher = AES.new(key, AES.MODE_CBC, iv)
	pt = unpad(cipher.decrypt(ct), AES.block_size)
	# print("The message was: ", pt)
	temp_sk.append(pt)
	time_decrypt = time_decrypt + (time.time() - time_decryption_start)
	# print(int.from_bytes(pt, sys.byteorder, signed = False))
	# ------------- print("Obtained session key ", j+1)

"""2. The following is to receive all ciphertexts"""
# print("Bob receiving encrypted session key from Alice:\n")
# for j in range(num_tk):
# 	# print('\nBob waiting to receive encrypted session key from Alice', file=sys.stderr)
# 	data, address = bobSockAlice.recvfrom(128)

# 	print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
# 	# print(data, file=sys.stderr)
# # Decryption of the session key
# 	key = key_list[j]
# 	result = data.decode('utf-8')
# 	b64 = json.loads(result)
# 	iv = b64decode(b64['iv'])
# 	ct = b64decode(b64['ciphertext'])
# 	cipher = AES.new(key, AES.MODE_CBC, iv)
# 	pt = unpad(cipher.decrypt(ct), AES.block_size)
# 	# print("The message was: ", pt)
# 	temp_sk.append(pt)
# 	# print(int.from_bytes(pt, sys.byteorder, signed = False))
# 	print("Obtained session key ", j+1)


# print("\nsession keys are recovered and stored!\n")

# print(len(temp_sk))
# print(temp_sk)
# print("\n\n\n\n\n", share_from_helper)

# print("\n\n\n\n\n", test_key, "\n\n\n\n\n")
total_run_time = time_init_end + time_checking_end + time_combine_end + time_decrypt
print("\ntotal running time is:", total_run_time)
total_latency_time = time_latency_helper_end + time_latency_share_alice_end + time_latency_decrypt
print("total latency time is:", total_latency_time)

print("\nSession key established:", temp_sk[0])

print("\nSession end.")

# try:
	# Send data
	# print('sending "%s"' % key_message, file=sys.stderr)
	# sent = aliceSockHelper.sendto(key_message, server_address)

	# Receive response
	# print >> sys.stderr, 'waiting to receive'
	# data, server = sock.recvfrom(4096)
	# print >> sys.stderr, 'received "%s"' % data
# finally:
