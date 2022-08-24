import socket
import sys

def start_client(cc_alg):
    if cc_alg in ["reno", "cubic", "westwood"]:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_CONGESTION = getattr(socket, 'TCP_CONGESTION', 13)

        if cc_alg == "reno":
            sock.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b"reno")
        elif cc_alg == "cubic":
            sock.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b"cubic")
        elif cc_alg == "westwood":
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b"westwood")

        # Connect the socket to the port where the server is listening
        server_address = ('10.0.0.2', 10000)
        print(sys.stderr, 'connecting to %s port %s' % server_address)
        sock.connect(server_address)

        try:

            # Send data
            #message = 'This is the message.  It will be repeated.'
            with open('/vagrant/data3.txt', 'r') as file:
                message = file.read().replace('\n', '')

            #print('sending "%s"' % message)
            sock.sendto(message.encode(),server_address)
            #sock.sendall(message)

            """
            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print('received "%s"' % data)
            """

        finally:
            print('closing socket')
            sock.close()
    else:
        print('not a proper cc_alg')


if __name__ == '__main__':
    cc_alg = sys.argv[1]
    start_client(cc_alg)
