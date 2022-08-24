import base64
import os, random
import sys
from Crypto.Protocol.SecretSharing import Shamir
# from binascii import hexlify

index_set = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

key_list = []

for i in range(10):
	key = os.urandom(16)
	key_dec = int.from_bytes(key, sys.byteorder, signed = False)
	print(key_dec)
	key_list.append(key_dec)

print("--------------")

print(key_list)

cut_set = set(random.sample(range(10), 5))
choose_set = index_set.difference(cut_set)

for i in cut_set:
	print(key_list[i])

for j in cut_set:
	print(key_list[j])

print(cut_set)
print(choose_set)

