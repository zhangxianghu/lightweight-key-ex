# from cryptography.fernet import Fernet
import base64
import os
import sys
import json
import random

from Crypto.Protocol.SecretSharing import Shamir
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from binascii import hexlify

"""session key generation"""
session_key = os.urandom(16)
print(session_key)
session_key_dec = int.from_bytes(session_key, sys.byteorder, signed = False)
print(session_key_dec)

"""test key list initialization"""
key_list = []

"""number of test keys and their indices for cut-and-choose"""
index_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

"""list of test keys"""
for i in range(10):
	key = os.urandom(16)
	key_list.append(key)

	"""keys: byte array to integers"""
	# key_dec = int.from_bytes(key, sys.byteorder, signed = False)
	# print(key_dec)
	# key_list.append(key_dec)

"""opening keys set: index of key_list"""
cut_set = set(random.sample(range(10), 5))

"""evaluation keys set: index of key_list"""
choose_set = index_set.difference(cut_set)

"""--- secret sharing example"""
for i in range(10):
	# shares = Shamir.split(2, 4, int.from_bytes(key_list[i], sys.byteorder, signed = False))
	shares = Shamir.split(2, 4, key_list[i])
	# print(key_list[i])
	print("key shares are:", shares)
	key_rec = Shamir.combine(shares)
	# print(key_rec)
	# print(int.from_bytes(key_rec, "big", signed = False))
	# print("+++++++++++")

# for idx, share in shares:
# 	print(idx, hex(int.from_bytes(share, "big", signed = False)))


"""array of bytes to integer"""
# key_dec = int.from_bytes(key, sys.byteorder, signed = False)
"""integer to array of bytes"""
# (key_dec).to_bytes(16, sys.byteorder, signed = False)

"""--- example of encryption and decryption """
for i in choose_set:
	key = key_list[i]
	
	data = session_key
	cipher = AES.new(key, AES.MODE_CBC)
	ct_bytes = cipher.encrypt(pad(data, AES.block_size))
	iv = b64encode(cipher.iv).decode('utf-8')
	ct = b64encode(ct_bytes).decode('utf-8')
	result = json.dumps({'iv':iv, 'ciphertext':ct})
	# print(result)

	b64 = json.loads(result)
	iv = b64decode(b64['iv'])
	ct = b64decode(b64['ciphertext'])
	cipher = AES.new(key, AES.MODE_CBC, iv)
	pt = unpad(cipher.decrypt(ct), AES.block_size)
	# print("The message was: ", pt)
	# print(int.from_bytes(pt, sys.byteorder, signed = False))
	print("---------------")

"""
print(key)
print(key_dec)

"""

"""--- secret sharing example
shares = Shamir.split(2, 5, key_dec)
print(shares)

for idx, share in shares:
	print(idx, hex(int.from_bytes(share, "big", signed = False)))

key_rec = Shamir.combine(shares)
# print(key_rec)
print(int.from_bytes(key_rec, "big", signed = False))
"""

# shares_rec = []

# for x in range(2):
# 	in_str = raw_input("Enter index and share separated by comma: ")
# 	idx, share = [ strip(s) for s in in_str.split(",") ]
# 	shares.append((idx, unhexlify(share)))
# 	key = Shamir.combine(shares)



