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

aliceSockHelper = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
server_2_address = ('localhost', 9999)

#Here we define the UDP IP address as well as the port number that we have
# already defined in the client python script.
	# Ip address example
	# UDP_IP_ADDRESS = "127.0.0.1"
	# UDP_PORT_NO = 6789


for i in index_set:
	shares = Shamir.split(2, 2, key_list[i])
	key_list_shares.append(shares)
	sent = aliceSockHelper.sendto(shares[0][1], server_address)
	# print("Alice sending messages to helper2, share 2:")
	# print(shares,"\n")
	sent = aliceSockHelper.sendto(shares[1][1], server_2_address)

sent = aliceSockHelper.sendto(end_message, server_address)
sent = aliceSockHelper.sendto(end_message, server_2_address)

print("\nSession end.")
