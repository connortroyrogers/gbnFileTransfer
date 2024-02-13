'''##############################################
 * Netster-py chat.py - Connor Rogers (controge)
 * CREATED: 9/27/23
 *
 * This program provides code for a chat server
 * and chat client that allow connections via
 * TCP and UDP. The server provides a response
 * that echos the user input unless the input
 * fits specific cases
 ##############################################'''
import socket
def chat_server(iface:str, port:int, use_udp:bool) -> None:
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
        sock.listen()

    connections = 0

    try:
        print("Hello, I am a server")
        #operating loop
        while True:
            if not use_udp:
                print(f"Waiting for a connection on {iface}:{port}...")
                # tcp accept new connection
                client_socket, client_address = sock.accept()
                connections += 1
                print(f"Connection {connections} from {client_address}")
            else:
                client_data, client_address = sock.recvfrom(256)
                print(f"Received data from {client_address}")

            #loop for client messages
            while True:
                if not use_udp:
                    data = client_socket.recv(256).decode()
                else:
                    data = client_data.decode()
                if not data:
                    break
                #handle different special messages
                if data == "hello":
                    response = "world"

                elif data == "goodbye":
                    response = "farewell"

                elif data == "exit":
                    response = "ok"
                #if no special messages, return client message
                else:
                    response = data
                if not use_udp:
                    #send response via TCP
                    client_socket.send(response.encode())
                else:
                    #send response via UDP
                    sock.sendto(response.encode(), client_address)

                if not use_udp:
                    #tcp message received
                    print(f"got message from {client_address}")

                if(data == 'exit'):
                    #break connection to client and close server
                    if not use_udp:
                        client_socket.close()
                    return
                if(data == 'goodbye'):
                    #break connection to client
                    if not use_udp:
                        client_socket.close()
                    break

    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        sock.close()

def chat_client(host:str, port:int, use_udp:bool) -> None:
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
        while True:
            # get input
            user_input = input()

            if not user_input:
                #if message is empty break connection
                break

            if not use_udp:
                #send user input with TCP
                sock.send(user_input.encode())
                #print server response
                response = sock.recv(256).decode()
                print(response)
            else:
                #send user input with UDP
                server_address = (host, port)
                sock.sendto(user_input.encode(), server_address)
                #print server response
                response, server_address = sock.recvfrom(256)
                print(response.decode())
            if(user_input == 'goodbye' or user_input == 'exit'):
                #break connection to server with special messages
                break

    #if user uses keyboard interrupt, disconnect from server
    except KeyboardInterrupt:
        print("Client terminated by user.")
    finally:
        sock.close()
            
