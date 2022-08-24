from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

import random
import socket
import os

key = RSA.generate(3072)

# session_key = os.urandom(16)

private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
print(private_key)

public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
print(public_key)

# data = "I met aliens in UFO. Here is the map.".encode("utf-8")
file_out = open("encrypted_data.bin", "wb")

recipient_key = RSA.import_key(open("receiver.pem").read())

print("\n\n", recipient_key.publickey())

session_key = os.urandom(16)
print("before", session_key)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# cipher_aes = AES.new(session_key, AES.MODE_EAX)
# ciphertext, tag = cipher_aes.encrypt_and_digest(data)
# [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

print("\n\n\n\n", enc_session_key)

# file_in = open("encrypted_data.bin", "rb")
private_key = RSA.import_key(open("private.pem").read())

# enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

print("after:", session_key)
print("\nSession end.")

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
