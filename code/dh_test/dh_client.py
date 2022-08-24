import dh
import time
import socket
import os
import sys

from hwcounter import Timer, count, count_end

time_start = time.time()
CPU_start = count()

client_address = ('10.0.0.1', 10000)
server_address = ('10.0.0.2', 9999)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
	# Send public key
	# ----------- print('sending "%s"' % public_key)
	d1 = dh.DiffieHellman(16)
	d1_pubkey = d1.gen_public_key()
	# print(d1_pubkey)
	# print(type(d1_pubkey))
	# print((d1_pubkey).to_bytes(384, sys.byteorder, signed = False))
	# security parameter / 8 = 384
	sock.sendall((d1_pubkey).to_bytes(512, sys.byteorder, signed = False))
	CPU_d1_key_end = count_end() - CPU_start
	time_d1_key_end = time.time() - time_start

	time_latency_client_start = time.time()
	d2_pubkey_byte = sock.recv(512)
	time_latency_client_end = time.time() - time_latency_client_start

	# print(d2_pubkey_byte)
	time_share_key_start = time.time() 
	CPU_share_key_start = count()
	d2_pubkey = int.from_bytes(d2_pubkey_byte, sys.byteorder, signed = False)
	d1_sharedkey = d1.gen_shared_key(d2_pubkey)
	# print("####")
	print(d1_sharedkey)
	CPU_share_key_end = count_end() - CPU_share_key_start 
	time_share_key_end = time.time() - time_share_key_start
	# ----------- print("--------", enc_session_key)
	# time_latency_client_end = time.time() - time_latency_client_start

	# Decrypt and obtain the session key
	# time_session_key_start = time.time()
	# private_key = RSA.import_key(open("private.pem").read())
	# cipher_rsa = PKCS1_OAEP.new(private_key)
	# session_key = cipher_rsa.decrypt(enc_session_key)
	# print("after:", session_key)
finally:
	time_total_client = time_d1_key_end + time_share_key_end
	time_total_CPU = CPU_d1_key_end + CPU_share_key_end
	total_messages_send = len((d1_pubkey).to_bytes(512, sys.byteorder, signed = False))
	total_messages_receive = len(d2_pubkey_byte)
	
	print("\n\nClient total running time is:", time_total_client)
	print("\n\nClient total waiting time is:", time_latency_client_end)
	print("Client 1 total CPU time is: ", time_total_CPU)
	print("Total message send: ", total_messages_send)
	print("Total message receive: ", total_messages_receive)
	print("Bandwidth: ", total_messages_receive + total_messages_send)
	print('closing socket')
	print("\nSession end.")
	sock.close()

	f = open("eval_dh_1.txt", "a")
	f.write("\n" + str(time_total_client) + "\t" + str(time_latency_client_end) + "\t" + str(time_total_CPU))
	# f.write("\n\n\n" + "Client 1 total running time is: " + str(time_total_client))
	# f.write("\nClient 1 total latency time is: " + str(time_latency_client_end))
	# f.write("\nClient 1 total CPU time is: " + str(time_total_CPU))
	# f.write("\nTotal message send: " + str(total_messages_send))
	# f.write("\nTotal message receive: " + str(total_messages_receive))
	# f.write("\nBandwidth: " + str(total_messages_receive + total_messages_send - 128 * 2))

	f.close()
# RFC 3526 - More Modular Exponential (MODP) Diffie-Hellman groups for 
# Internet Key Exchange (IKE) https://tools.ietf.org/html/rfc3526 


########### From cryptography library #############
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import dh
# from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# import time

# # Generate some parameters. These can be reused.
# parameters = dh.generate_parameters(generator=2, key_size=3072, backend=default_backend())
# print("start")
# # Generate a private key for use in the exchange.
# time_start = time.time()
# print("start1", parameters)
# server_private_key = parameters.generate_private_key()
# print("start2")
# # In a real handshake the peer is a remote client. For this
# # example we'll generate another local private key though. Note that in
# # a DH handshake both peers must agree on a common set of parameters.
# peer_private_key = parameters.generate_private_key()
# print("start3")
# shared_key = server_private_key.exchange(peer_private_key.public_key())
# print("start4")
# # Perform key derivation.
# derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(shared_key)
# print("star5")
# # And now we can demonstrate that the handshake performed in the
# # opposite direction gives the same final value
# same_shared_key = peer_private_key.exchange(server_private_key.public_key())
# # print("start6")
# # print(same_shared_key)
# same_derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(same_shared_key)

# derived_key == same_derived_key
# print(derived_key)
# time_end = time.time() - time_start
# print(time_end)

