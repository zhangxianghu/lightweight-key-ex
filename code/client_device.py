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

# Number of helpers
helpers = 2

# Number of test keys
num_tk = 10

"""ending message"""
end_message = b"Closing socket"

"""test key list initialization"""
key_list = []

"""test key shares list initialization"""
key_list_shares = []

"""number of test keys and their indices for cut-and-choose"""
index_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

"""opening keys set: index of key_list"""
eval_list = []

"""evaluation keys set: index of key_list"""
# choose_set = index_set.difference(cut_set)

# declare our serverSocket upon which
# we will be listening for UDP messages
aliceSockHelper = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
server_2_address = ('localhost', 9999)

#Here we define the UDP IP address as well as the port number that we have
# already defined in the client python script.
	# Ip address example
	# UDP_IP_ADDRESS = "127.0.0.1"
	# UDP_PORT_NO = 6789

# test key generation
#-------- print("Alice generating test keys:\n")
for i in range(num_tk):
	key = os.urandom(16)
	key_list.append(key)
	# print(len(key_list))
#--------	print("Test key", i+1, key)
#-------- print("\nKey generation completed!")	

# print("key list:", key_list)

#--------print("\nAlice secret sharing test keys and sending them to helpers: -------")
for i in index_set:
	shares = Shamir.split(2, 2, key_list[i])
	key_list_shares.append(shares)
	# print(shares[0][1])
	# print(shares[1][1])
	# print('sending "%s"' % key, file=sys.stderr)
	# print("Alice sending messages to helper1, share 1:")
	sent = aliceSockHelper.sendto(shares[0][1], server_address)
	# print("Alice sending messages to helper2, share 2:")
	# print(shares,"\n")
	sent = aliceSockHelper.sendto(shares[1][1], server_2_address)

sent = aliceSockHelper.sendto(end_message, server_address)
sent = aliceSockHelper.sendto(end_message, server_2_address)

# print(key_list_shares)
#-------- print("\nSending key shares completed!")

#--------print('\nclosing socket of Alice to Helper', file=sys.stderr)
aliceSockHelper.close()

# Create socket for messages from Alice to Bob
bobSockAlice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Alice receive messages from Bob so Alice can send encrypted session key
client_address = ('localhost', 9997)
client_2_address = ('localhost', 9998)
bobSockAlice.bind(client_address)

time_to_helper_end = time.time() - start_time

"""Alice receives opening set from Bob"""
# --------- print('\nAlice waiting for evaluation set from Bob:', file=sys.stderr)

wait_time_eval_start = time.time()

data, address = bobSockAlice.recvfrom(128)

wait_time_eval_end = time.time() - wait_time_eval_start

# ---------- print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
# get the opening set
time_share_to_bob_start = time.time()

eval_list = list(data)
# ---------- print(list(data), file=sys.stderr)
# ---------- print("\nAlice received the opening set from Bob!")

"""Alice sends openning shares to Bob and 
   wait for confirm message from Bob to see 
   if there is any cheating helpers. 
   If not checking, comment following
"""
# -------- print("\nAlice starts sending openning to Bob:")
open_list = list(index_set.difference(set(eval_list)))
# -------- print(open_list)
# -------- print(key_list_shares, "\n\n\n")

# Finish this part
for i in open_list:
	for j in range(helpers):
		# ---------- print(key_list_shares[i][j][1])
		bobSockAlice.sendto(key_list_shares[i][j][1], client_2_address)

bobSockAlice.sendto(b"oss", client_2_address)
"""Comment above if not checking"""

time_share_to_bob_end = time.time() - time_share_to_bob_start

# bobSockAlice.sendto(b"This is a test", client_2_address)
# bobSockAlice.sendto(np.array(key_list_shares).tobytes(), client_2_address)

# Alice ready to send session key when Bob is ready, receive "key received" message from Bob
while True:
	# ------- print('\nAlice waiting for message from Bob to prepapre encrypted session key:', file=sys.stderr)
	wait_time_confirm_start = time.time()
	data, address = bobSockAlice.recvfrom(128)
	wait_time_confirm_end = time.time() - wait_time_confirm_start
	# ------- print('received %s bytes from %s' % (len(data), address), file=sys.stderr)
	# ------- print(data, file=sys.stderr)
	# sent = bobSockAlice.sendto(b"messages", client_2_address)
	# print("messages sent:", sent)
	break

time_sk_to_bob_start = time.time()
data = os.urandom(16)
# ------- print("\nMessages received from Bob and session key is generated!")
# ------- print("session key:", data, "\n\n\n")

# Alice starts to send session key, choose either 1 of the following 2

"""1. The following is to send evaluation set of ciphertexts"""
#-------- print("\nAlice starts sending encrypted session key to Bob:")
for i in eval_list:
	key = key_list[i]
	# Encryption of the session key
	cipher = AES.new(key, AES.MODE_CBC)
	ct_bytes = cipher.encrypt(pad(data, AES.block_size))
	iv = b64encode(cipher.iv).decode('utf-8')
	ct = b64encode(ct_bytes).decode('utf-8')
	result = json.dumps({'iv':iv, 'ciphertext':ct})
	byte_result = result.encode('utf-8')
	# -------- print("\nsending encrypted session key to Bob:", byte_result)
	bobSockAlice.sendto(byte_result, client_2_address)

time_sk_to_bob_end = time.time() - time_sk_to_bob_start

total_run_time = time_to_helper_end + time_share_to_bob_end + time_sk_to_bob_end
print("\ntotal running time is:", total_run_time)
total_wait_time = wait_time_eval_end + wait_time_confirm_end 
print("total latency time is:", total_wait_time)

print("\nSession key established: ", data)
"""2. The following is to send all ciphertexts."""
# print("\nAlice starts sending encrypted session key to Bob:")
# for j in range(num_tk):
# 	key = key_list[j]
# # Encryption of the session key
# 	cipher = AES.new(key, AES.MODE_CBC)
# 	ct_bytes = cipher.encrypt(pad(data, AES.block_size))
# 	iv = b64encode(cipher.iv).decode('utf-8')
# 	ct = b64encode(ct_bytes).decode('utf-8')
# 	result = json.dumps({'iv':iv, 'ciphertext':ct})
# 	byte_result = result.encode('utf-8')
# 	print("\nsending encrypted session key to Bob:", byte_result)
# 	bobSockAlice.sendto(byte_result, client_2_address)

# Sending encrypted session key over
bobSockAlice.sendto(b"session key sent", client_2_address)
# ---------- print("\nSending encrypted session key completed!\n\n\n")

# ---------- print('closing socket of Alice to Bob', file=sys.stderr)
bobSockAlice.close()

print("\nSession end.")

# Decryption of the session key
# 	b64 = json.loads(result)
# 	iv = b64decode(b64['iv'])
# 	ct = b64decode(b64['ciphertext'])
# 	cipher = AES.new(key, AES.MODE_CBC, iv)
# 	pt = unpad(cipher.decrypt(ct), AES.block_size)
# 	print("The message was: ", pt)
# 	# print(int.from_bytes(pt, sys.byteorder, signed = False))
# 	print("---------------")

# try:
	# Send data
	# print('sending "%s"' % key_message, file=sys.stderr)
	# sent = aliceSockHelper.sendto(key_message, server_address)

	# Receive response
	# print >> sys.stderr, 'waiting to receive'
	# data, server = sock.recvfrom(4096)
	# print >> sys.stderr, 'received "%s"' % data
# finally:
