'''##############################################
 * Netster-py filetransfer.py - Connor Rogers (controge)
 * CREATED: 10/11/23
 *
 * This program provides code for a file transfer server
 * and file transfer client that allow connections via
 * TCP and UDP. The server provides an interface for the
 * Client to send a file that is copied by the server to
 * a specified file at the server's location
 ##############################################'''

from typing import BinaryIO
import socket
def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    if use_udp:
        # make socket for udp
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind socket to interface and port
        server_address = (iface, port)
        sock.bind(server_address)
    else:
        # make socket for tcp
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind socket to interface and port
        server_address = (iface, port)
        sock.bind(server_address)
        # listen for connections
        sock.listen(1)
    connections = 0
    try:
        print("Hello, I am a server")
        #operating loop
        while True:
            if not use_udp and connections <= 1:
                # tcp accept new connection
                client_socket, client_address = sock.accept()
                connections+=1
            elif use_udp and connections <= 1:
                client_data, client_address = sock.recvfrom(256)
                connections+=1
            else:
                break
            if not use_udp:
                while True:
            #loop for client messages
                    data = client_socket.recv(256)
                    if data != b'':
                        fp.write(data)
                    else:
                        break                
                fp.close()    
                sock.close()
                return
            if use_udp:
                data = client_data
                if data == b'':
                    fp.close()
                    break
                else:
                    fp.write(data)

    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        sock.close()

def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    if use_udp:
        # make socket for UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        # make socket for TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if not use_udp:
            # connect to server with TCP
            server_address = (host, port)
            sock.connect(server_address)
        print("Hello, I am a client")
        #operating loop
        emptydata = b''
        while True:
            # get input
            data = fp.read(256)
            if not data:
                break
            if not use_udp:
                #send user input with TCP
                sock.send(data)
                sock.send(emptydata)
            else:
                #send user input with UDP
                server_address = (host, port)
                sock.sendto(data, server_address)
                sock.sendto(emptydata, server_address)
        sock.close()

    #if user uses keyboard interrupt, disconnect from server
    except KeyboardInterrupt:
        print("Client terminated by user.")
    finally:
        sock.close()
