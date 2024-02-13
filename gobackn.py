'''##############################################
 * gobackn.py - Connor Rogers
 * CREATED: 11/17/23
 *
 * This program provides code for a file transfer server
 * and file transfer client that uses a go back n
 * implementation to ensure a reliable connection
 * between the server and client that minimizes
 * dropped packets and lost data, and maximizes
 * file transfer speed.
 ##############################################'''

from typing import BinaryIO
import socket

TIMEOUT = 0.06
MESSAGELIMIT = 256
ACKMSG = 1
DATAMSG = 0
ENDMSG = 2
MAXRETRIES = 5
WINDOW_SIZE = 4

#generate header with sequence number, akc number, message type, and data
def generatePacket(seq: int, ack: int, messagetype: int, data: bytes) -> bytes:
    return bytes(f'{seq}-|-{ack}-|-{messagetype}-|-', encoding="utf-8") + data

#get info from header (seq = [0], checksum = [1], messagetype = [2], data = [3])
def breakdownPacket(header: bytes) -> ():
    return header.split(b'-|-')

def rdt_send(sock, data, sequence_number, server_address):
    #intialize variables
    base = 1
    window = []
    seqbuffer = 0
    #set timeout
    sock.settimeout(TIMEOUT)
    #sending data loop
    while data:
        #aslong as sequence_number is lower than window size
        if(sequence_number < base+WINDOW_SIZE):
            packet = generatePacket(sequence_number, 0, DATAMSG, data[:MESSAGELIMIT])
            sock.sendto(packet, server_address)
            seqbuffer = sequence_number
            sequence_number += 1
            window.append(packet)
            data = data[MESSAGELIMIT:]
        #if window is filled, receive acks, and clear acked packets from window
        try:
            ack_packet, _ = sock.recvfrom(256)
            ack = breakdownPacket(ack_packet)
            ack_number = int(ack[1].decode())
            if ack_number == seqbuffer:
                del window[0]
                base += 1
        except socket.timeout:
            #on timeout, resend unacked packets
            for i in window:
                sock.sendto(i, server_address)
    #send end message when "while data" is false
    end_packet = generatePacket(0, 0, ENDMSG, b'')
    sock.sendto(end_packet, server_address)

def rdt_recv(sock: socket, fp: BinaryIO):
    #initialize required variables
    expected_seq = 1
    datastr = b''
    messagetype = 0
    try:
        #receiving data loop
        while True:
            #receivee packet
            packet, client_address = sock.recvfrom(1024)
            #split packet into different parts
            sequence_number, ack_number, messagetype, data = breakdownPacket(packet)
            #convert sequence number and messagetype to integers
            sequence_number = int(sequence_number.decode())
            messagetype = int(messagetype.decode())
            #if the message received is an end message, break loop
            if messagetype == ENDMSG:
                break
            #if sequence number is expected, update datastring and send ack
            if sequence_number == expected_seq:
                datastr += data
                expected_seq += 1
                ack_packet = generatePacket(0, sequence_number, ACKMSG, b'')
                sock.sendto(ack_packet, client_address)
            else:
                #if received out of order, send ack for last correct packet received
                ack_packet = generatePacket(0, expected_seq, ACKMSG, b'')
                sock.sendto(ack_packet, client_address)
    except KeyboardInterrupt:
        return
    finally:
        fp.write(datastr)
        sock.close()

#server function to intialize gbn udp server
def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind socket to interface and port
    server_address = (iface, port)
    sock.bind(server_address)
    try:
        print("Hello, I am server")
        #receive data from client
        rdt_recv(sock, fp)
    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        sock.close()

#client function to initialize gbn udp client
def gbn_client(host: str, port: int, fp: BinaryIO) -> None:
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        #initialize server address
        server_address = (host,port)
        #read data from file
        data = fp.read()
        print("Hello, I am a client")
        #initialize sequence number
        seqn = 1
        #send data to server
        rdt_send(sock, data, seqn, server_address)
    except KeyboardInterrupt:
        print("Client terminated by user.")
    finally:
        sock.close()
