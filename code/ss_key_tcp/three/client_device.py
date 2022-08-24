import socket
import sys
import base64
import os
import json
import random
import time
from hwcounter import Timer, count, count_end

from Crypto.Protocol.SecretSharing import Shamir
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from binascii import hexlify

time_start = time.time()

server4_address = ('10.0.0.7', 10002)
server3_address = ('10.0.0.6', 10001)
server2_address = ('10.0.0.5', 10000)
server1_address = ('10.0.0.4', 9999)
client2_address = ('10.0.0.2', 9998)
client1_address = ('10.0.0.1', 9997)


""" Security level"""
sec_lev = 128

""" Number of helpers
	Modify this part for more test keys
""" 
helpers = 3

""" Number of test keys
	Modify this part for more test keys
"""
num_tk = 10

"""test key list initialization"""
key_list = []

"""test key shares list initialization"""
key_list_shares = []

""" number of test keys and their indices for cut-and-choose
	Modify this part for more test keys
"""
index_set = {0}
for i in range(1, num_tk):
	index_set.add(i)

"""opening keys set: index of key_list"""
eval_list = []

"""ending message"""
end_message = b"Closing socket"

""" Create device1 socket to servers
	Modify this part for more helpers
"""

time_setting_end = time.time() - time_start

aliceSockserver1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('connecting to server1: %s port %s' % server1_address)
aliceSockserver1.connect(server1_address)

aliceSockserver2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('connecting to server2: %s port %s' % server2_address)
aliceSockserver2.connect(server2_address)

aliceSockserver3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('connecting to %s port %s' % server3_address)
aliceSockserver3.connect(server3_address)

# if more helpers, uncomment following
# aliceSockserver4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('connecting to %s port %s' % server4_address)
# aliceSockserver4.connect(server4_address)

""" test key generation
	Modify this if you need higher security level
	By default, it is 128-bit (16 bytes) security, 
"""
time_key_share_start = time.time()

#-------- print("Alice generating test keys:\n")
for i in range(num_tk):
	key = os.urandom(16)
	key_list.append(key)

# print("\n\nKey list is: ", key_list)

try:
	for i in index_set:
		""" Secret sharing each test key
			Modify this part for t-out-of-n 
		"""
		shares = Shamir.split(3, 3, key_list[i])
		# print("\nKey:", key_list[i])
		# print("Shares are:", shares)
		""" Sending shares to each helper"""
		aliceSockserver1.sendall(shares[0][1])
		aliceSockserver2.sendall(shares[1][1])
		aliceSockserver3.sendall(shares[2][1])
		# if more helpers, uncomment following
		# aliceSockserver4.sendall(shares[3][1])
		key_list_shares.append(shares)
	# aliceSockserver1.sendall(end_message)
	# aliceSockserver2.sendall(end_message)
	# aliceSockserver3.sendall(end_message)
finally:
	# print("\n\nAll key shares", key_list_shares)
	print('\nclosing socket for server1\n')
	aliceSockserver1.close()
	print('\nclosing socket for server2\n')
	aliceSockserver2.close()
	print('\nclosing socket for server3\n')
	aliceSockserver3.close()
	# if more helpers, uncomment following
	# print('\nclosing socket for server4\n')
	# aliceSockserver4.close()

time_key_share_end = time.time() - time_key_share_start

time_latency_eval_start = time.time()
# Create socket with Bob for opening set
bobSockAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('starting up on %s port %s' % client1_address)
bobSockAlice.bind(client1_address)
bobSockAlice.listen(1)
# print('waiting for a connection from Bob')
connection, client_address = bobSockAlice.accept()
# print('connection from', client_address)

# Receive evaluation list and create open list
data = connection.recv(sec_lev)

time_latency_eval_end = time.time() - time_latency_eval_start

time_open_share_start = time.time()

eval_list = list(data)
# print(eval_list)
open_list = list(index_set.difference(set(eval_list)))

# Send opening shares
k = 0

for i in open_list:
	for j in range(helpers):
		# print("sending key shares: ", key_list_shares[i][j][1])
		connection.sendall(key_list_shares[i][j][1])
		# connection.sendall(b"test")
		k = k + 1

# Generate session key and encrypt it
session_key = os.urandom(16)
# print("\nThe session key is: ", session_key)

temp_sk = []
len_flag = True

for i in eval_list:
	key = key_list[i]
	# print("encyrption: ", i, "--", key_list[i])
	# Encryption of the session key
	cipher = AES.new(key, AES.MODE_CBC)
	ct_bytes = cipher.encrypt(pad(session_key, AES.block_size))
	iv = b64encode(cipher.iv).decode('utf-8')
	ct = b64encode(ct_bytes).decode('utf-8')
	result = json.dumps({'iv':iv, 'ciphertext':ct})
	byte_result = result.encode('utf-8')
	# print("\n\nsending encrypted session key to Bob:", byte_result)
	if len_flag:
		connection.sendall(str(len(byte_result)).encode('utf-8'))
		len_flag = False
	connection.sendall(byte_result)
	# print("encryption key is: ", key)
	# print("Ciphertext length: ", len(byte_result), byte_result)

time_open_share_end = time.time() - time_open_share_start
	# result = byte_result.decode('utf-8')
	# b64 = json.loads(result)
	# iv = b64decode(b64['iv'])
	# ct = b64decode(b64['ciphertext'])
	# cipher = AES.new(key, AES.MODE_CBC, iv)
	# pt = unpad(cipher.decrypt(ct), AES.block_size)
	# # print("The message was: ", pt)
	# temp_sk.append(pt)
	# j += 1

# print("session key list:", temp_sk, "\n\n")



time_total_exe_client = time_setting_end + time_key_share_end + time_open_share_end
time_total_latency_client = time_latency_eval_end

# print(time_setting_end, time_key_share_end, time_open_share_end)
print("Client 1 total running time is: ", time_total_exe_client)
print("Client 1 total latency time is: ", time_total_latency_client)
# for j in range(5):
# connection.sendall(b"session key transfer")
# print(k)


