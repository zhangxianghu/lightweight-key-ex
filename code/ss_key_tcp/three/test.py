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

time_start = time.time()

server4_address = ('localhost', 10002)
server3_address = ('localhost', 10001)
server2_address = ('localhost', 10000)
server1_address = ('localhost', 9999)
client2_address = ('localhost', 9998)
client1_address = ('localhost', 9997)


""" Security level"""
sec_lev = 128

""" Number of helpers
	Modify this part for more test keys
""" 
helpers = 5

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


""" test key generation
	Modify this if you need higher security level
	By default, it is 128-bit (16 bytes) security, 
"""

#-------- print("Alice generating test keys:\n")
for i in range(num_tk):
	key = os.urandom(16)
	key_list.append(key)


for i in index_set:
	shares = Shamir.split(2, 2, key_list[i])
	key_list_shares.append(shares)

# print("\n All shares", key_list_shares)

key_test = os.urandom(16)
print("Key generation:", key)
shares = Shamir.split(3, 5, key)

print("\nkey shares:", shares)

print("\nrecover key:", Shamir.combine(shares))

key_list_test = []

test_shares = [(1, b'\x81\xd0(/cwn\xacx\x9b\x90\xdc\xc7Z\xf8\xae'), (2, b'\x94\x7f\xbd\xbd\xaf\xe7D\xf77\xbc\xe9T*j\x84\x83')]

print("\ntest recover key:", Shamir.combine(test_shares))

# for i in range(num_tk):
# 	print("recover key:", Shamir.combine(key_list_shares[i]))

for i in range(num_tk):
	k = 1
	share_temp = []
	for j in range(helpers):
		# print("test")
		# print("\ntest kyes", share_temp)
		share_temp.append(key_list_shares[i][j])
		# print("\ntest kyes", share_temp)
		k += 1
	# share_from_helper.append(share_temp)
	# print("\n",share_temp)
	# print("recover key:", Shamir.combine(share_temp))
	# key_list_test.append(Shamir.combine(share_temp))
# print(share_temp)
# print("\n\nKey list is: ", key_list)

# print("\n\nmore test:")
# # original = [(1, b'\xec6\xbc\xf2\xa2W7&E1"\xa2\xab\x07\xa7\x91'), (2, b'\xf8\x1b;%U9J`)rI\xee\xf4\xdf\xc1\x8d'), (3, b'\x0b\xff\xb9\x97\xf8\x1c\x9e\xa2\rL\x90\xd5>h\x1c\x04'), (4, b'\xd0@4\x8a\xbb\xe5\xb0\xec\xf1\xf4\x9fvKo\r\xb5')]
# original = [(1, b'\xec6\xbc\xf2\xa2W7&E1"\xa2\xab\x07\xa7\x91'), (2, b'\x0b\xff\xb9\x97\xf8\x1c\x9e\xa2\rL\x90\xd5>h\x1c\x04'), (3, b'\xd0@4\x8a\xbb\xe5\xb0\xec\xf1\xf4\x9fvKo\r\xb5'), (4, b'\xf8\x1b;%U9J`)rI\xee\xf4\xdf\xc1\x8d')]
# # print(original)

# print("recover original key:", Shamir.combine(original))

# # new = [(1, b'\xd0@4\x8a\xbb\xe5\xb0\xec\xf1\xf4\x9fvKo\r\xb5'), (2, b'\xf8\x1b;%U9J`)rI\xee\xf4\xdf\xc1\x8d'), (3, b'\x0b\xff\xb9\x97\xf8\x1c\x9e\xa2\rL\x90\xd5>h\x1c\x04'), (4, b'\xec6\xbc\xf2\xa2W7&E1"\xa2\xab\x07\xa7\x91')]
# new = [(1, b'\xd0@4\x8a\xbb\xe5\xb0\xec\xf1\xf4\x9fvKo\r\xb5'), (2, b'\xec6\xbc\xf2\xa2W7&E1"\xa2\xab\x07\xa7\x91'), (3, b'\x0b\xff\xb9\x97\xf8\x1c\x9e\xa2\rL\x90\xd5>h\x1c\x04'), (4, b'\xf8\x1b;%U9J`)rI\xee\xf4\xdf\xc1\x8d')]
# print("recover new key:", Shamir.combine(new))






