import socket
import traceback
import sys
import base64
import os
import json
import random
import time

from hwcounter import Timer, count, count_end
from threading import Thread
from Crypto.Protocol.SecretSharing import Shamir
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from binascii import hexlify

time_latency_shares_end = 0

def client_thread(server_address, connection, ip, port, max_buffer_size = 128):
	byte_total = b''
	time_latency_shares_start = time.time()
	for i in range(num_tk):
		client_input = connection.recv(max_buffer_size)
		# if ip not in address_list:
		byte_total += client_input
		# print(client_input, ",---- ")
	# print("Client is requesting to quit")
	connection.close()
	# print("Connection " + ip + ":" + port + " closed")
	# print("receiveing test:", byte_total)
	global time_latency_shares_end 
	# print(time_latency_shares_end)
	time_latency_shares_end = time.time() - time_latency_shares_start + time_latency_shares_end
	if server_address not in address_list:
		address_list.append(server_address)
	# print("-------------")
	helper_index = byte_total[:1]
	# print("helper index:", helper_index)
	for i in range(num_tk):
		share_split = byte_total[16*i+1:16*i+17]
		# print("\n\n", share_split)
		if server_address in test_key:
			test_key[server_address].append([helper_index, share_split])
		else:
			test_key[server_address] = [[helper_index, share_split]]

	# print("server_address: ", address_list)
	# while is_active:
	# 	client_input = connection.recv(max_buffer_size)
	# 	if b"Closing socket" in client_input:
	# 		print("Client is requesting to quit")
	# 		connection.close()
	# 		print("Connection " + ip + ":" + port + " closed")
	# 		is_active = False
	# 	else:
	# 		# if ip not in address_list:
	# 		print(client_input, ",---- ")

time_start = time.time()
CPU_start = count()

""" Security level"""
sec_lev = 128

""" Number of helpers
	Modify this part for more test keys
""" 
helpers = 4

""" Number of test keys
	Modify this part for more test keys
"""
num_tk = 10

""" length of cipher text
	Modify this part if it has longer cipher
"""
len_cipher = 76

# Addresses for helpers
address_list = []

# Dictionary for test key shares on client 2
test_key = {}

# Reconstructed test keys which are used to decrypt encrypted session key
key_list = []

# Store shares for checking
share_from_helper = []

# session key list, choose the majority for real session key 
temp_sk = []

""" number of test keys and their indices for cut-and-choose
	Modify this part for more test keys
"""
index_set = {0}
for i in range(1, num_tk):
	index_set.add(i)

end_message = b"Closing socket"

server4_address = ('10.0.0.7', 10002)
server3_address = ('10.0.0.6', 10001)
server2_address = ('10.0.0.5', 10000)
server1_address = ('10.0.0.4', 9999)
client2_address = ('10.0.0.2', 9998)
client1_address = ('10.0.0.1', 9997)

bobSockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('starting up on %s port %s' % client2_address)
bobSockServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
bobSockServer.bind(client2_address)

CPU_setting_end = count_end() - CPU_start
time_setting_end = time.time() - time_start

# Listen for incoming connections
bobSockServer.listen(4)
# print('waiting for a connection from servers')

thread_test = []

time_latency_shares_start = time.time()

for i in range(helpers):
	connection, server_address = bobSockServer.accept()
	# print('connection from', server_address)
	# connection, address = soc.accept()
	ip, port = str(server_address[0]), str(server_address[1])
	try:
		t = Thread(target=client_thread, args=(server_address, connection, ip, port))
		thread_test.append(t)
		t.start()
	except:
		print("Thread did not start.")
		traceback.print_exc()

# Wait for all threads finish
for x in thread_test:
	x.join()

# print("Test key is: ", test_key)

time_key_recover_start = time.time()
CPU_key_recover_start = count()

index = 0

for i in range(num_tk):
	k = 1
	share_temp = []
	for j in test_key:
		# print("test")
		# print("\ntest kyes", share_temp)
		# share_temp.append((k, test_key[j][i]))
		index = int(test_key[j][i][0])
		share_temp.append((index, test_key[j][i][1]))
		# print("index is:", index)
		# share_temp.insert(index-1, (index, test_key[j][i][1]))
		# print("\ntest kyes", share_temp)
		k += 1
	share_temp.sort()
	# print("\nCurrent shares", share_temp)
	# print("\nrecover key:", Shamir.combine(share_temp))
	key_list.append(Shamir.combine(share_temp))
	share_from_helper.append(share_temp)

# print("-----\nshare temp is: ", share_temp)
# Clean up the connection
# print("\nconnection closing...\n")
# print("\nSession end.")
# print("\nKey list is: ", key_list)
CPU_key_recover_end = count_end() - CPU_key_recover_start
time_key_recover_end = time.time() - time_key_recover_start

eval_list = list(random.sample(range(10), 5))
open_list = list(index_set.difference(set(eval_list)))

time_latency_alice_start = time.time()
bobSockAlice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bobSockAlice.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
# print('connecting to Alice: %s port %s' % client1_address)
bobSockAlice.connect(client1_address)
time_latency_alice_end = time.time() - time_latency_alice_start

time_eval_start = time.time()
CPU_eval_start = count()
bobSockAlice.sendall(bytearray(eval_list))

test_key = b''
CPU_eval_end = count_end() - CPU_eval_start
time_eval_end = time.time() - time_eval_start

time_latency_open_start = time.time()

while True:
	# print("\n receiving: \n")
	data = bobSockAlice.recv(sec_lev)
	if data:
		test_key += data
	else:
		break

time_latency_open_end = time.time() - time_latency_open_start
# print("\ntest key is ---: ", test_key)

time_session_key_start = time.time()
CPU_session_key_start = count()

cipher_start = helpers*len(open_list)*16

len_cipher = int(test_key[cipher_start:cipher_start+2])
# print("\n---length is: ", len_cipher)

# Two bytes for storing length
cipher_start += 2


j = 0
for i in range(len(eval_list)): 
	enc_session_key = test_key[cipher_start+len_cipher*i:cipher_start+len_cipher*i+len_cipher]
	# print("decryption key is: ", key_list[eval_list[j]])
	# print("Ciphertext length: ", len(enc_session_key), enc_session_key)
	key = key_list[eval_list[j]]
	result = enc_session_key.decode('utf-8')
	b64 = json.loads(result)
	iv = b64decode(b64['iv'])
	ct = b64decode(b64['ciphertext'])
	cipher = AES.new(key, AES.MODE_CBC, iv)
	pt = unpad(cipher.decrypt(ct), AES.block_size)
	temp_sk.append(pt)
	j += 1

# print("session key list:", temp_sk, "\n\n")
# print(open_list)

k = 0
j = 0
cheat_flag = False

for i in range(helpers * len(open_list)):
	if k == helpers: 
		j += 1
		k = 0
	test_split = test_key[16*i:16*i+16]
	# print("\ntest_split is: ", test_split)
	# print("shares from helper: \n", share_from_helper[open_list[j]])
	temp_list = []
	"""	Test wrong keys, it can output which test key is wrong
		If you want to output helper ID, modify this part
	"""	
	# if j == 2: 
	# 	for l in range(3):
	# 		share_from_helper[open_list[j]][l] = share_from_helper[open_list[j-1]][l]
	for l in range(helpers):
		temp_list.append(share_from_helper[open_list[j]][l][1]) 
	if test_split not in temp_list:
		cheat_flag = True
		print(open_list[j], "test key is wrong: ", share_from_helper[open_list[j]])
	k += 1

CPU_session_key_end = count_end() - CPU_session_key_start
time_session_key_end = time.time() - time_session_key_start

# print(eval_list)
# for i in eval_list:
# 	print(key_list[i])

# for i in range(5):
time_total_exe_client = time_setting_end + time_key_recover_end + time_eval_end + time_session_key_end
time_total_latency_client = time_latency_shares_end + time_latency_alice_end + time_latency_open_end
time_total_CPU = CPU_setting_end + CPU_key_recover_end + CPU_eval_end + CPU_session_key_end
total_messages_receive = 16 * helpers * num_tk * 2
total_messages_send = 4 * 5
# print(time_setting_end, time_key_share_end, time_open_share_end)
# print(time_setting_end, time_key_recover_end, time_eval_end, time_session_key_end)
# print(time_latency_shares_end, time_latency_alice_end, time_latency_open_end)
f = open("eval_sss_2.txt", "a")
print("The session key is: ", temp_sk[0])
print("Client 2 total running time is: ", time_total_exe_client)
print("Client 2 total latency time is: ", time_total_latency_client)
print("Client 2 total CPU time is: ", time_total_CPU)
print("Total message send: ", total_messages_send)
print("Total message receive: ", total_messages_receive)
print("Bandwidth: ", total_messages_receive + total_messages_send)

f.write("\n" + str(time_total_exe_client) + "\t" + str(time_total_latency_client) + "\t" + str(time_total_CPU))
# f.write("\n\n\n" + "Client 1 total running time is: " + str(time_total_exe_client))
# f.write("\nClient 1 total latency time is: " + str(time_total_latency_client))
# f.write("\nClient 1 total CPU time is: " + str(time_total_CPU))
# f.write("\nTotal message send: " + str(total_messages_send))
# f.write("\nTotal message receive: " + str(total_messages_receive))
# f.write("\nBandwidth: " + str(total_messages_receive + total_messages_send))

f.close()
# print("share from helper: ", share_from_helper)
# open_list = list(data)

