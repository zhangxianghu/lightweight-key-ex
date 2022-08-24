import socket
import sys

def start_server(cc_alg):
    if cc_alg in ["reno", "cubic", "westwood"]:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_CONGESTION = getattr(socket, 'TCP_CONGESTION', 13)

        if cc_alg == "reno":
            sock.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b"reno")
        elif cc_alg == "cubic":
            sock.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b"cubic")
        elif cc_alg == "westwood":
            sock.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, b"westwood")

        # Bind the socket to the port
        server_address = ('10.0.0.2', 10000)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        #while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            not_done = True
            while not_done:
                data = connection.recv(15000)
                #print('received "%s"' % data)
                """
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no more data from', client_address)
                    #connetion.close()
                    not_done = False
                    break
                """
                if not data:
                    print('no more data from', client_address)
                    #connetion.close()
                    not_done = False
                    break


        finally:
            # Clean up the connectio
            connection.close()
    else:
        print('not a proper cc_alg')

if __name__ == '__main__':
    cc_alg = sys.argv[1]
    start_server(cc_alg)
