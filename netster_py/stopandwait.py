'''##############################################
 * Netster-py stopandwait.py - Connor Rogers (controge)
 * CREATED: 11/01/23
 *
 * This program provides code for a file transfer server
 * and file transfer client that uses a stop and wait 
 * implementation to ensure a reliable connection
 * between the server and client that minimizes
 * dropped packets and lost data.
 ##############################################'''

from typing import BinaryIO
import socket
import time

TIMEOUT = 0.06
MESSAGELIMIT = 256
ACKMSG = 1
DATAMSG = 0
ENDMSG = 2
MAXRETRIES = 5

#create header generator, which takes in seq, checksum, data
def generatePacket(seq:int, ack:int, messagetype:int, data:bytes) -> bytes:
    return bytes(f'{seq}-|-{ack}-|-{messagetype}-|-', encoding = "utf-8") + data

#get info from header(seq = [0], checksum = [1], messagetype = [2], data = [3])
def breakdownPacket(header:bytes) -> ():
    return header.split(b'-|-')

def rdt_send(sock, data, sequence_number, server_address):
    packet = generatePacket(sequence_number, 0, DATAMSG, data)
    #if length of data is not 0, send packet
    sock.sendto(packet, server_address)
    #print("sent data packet")
    #start_time = time.time()
    #ack_received = False
    retries = 0
    #while not ack_received:
    while retries < MAXRETRIES:
        try:
            sock.settimeout(TIMEOUT)
            ack_packet, _ = sock.recvfrom(256)
            ack = breakdownPacket(ack_packet)
            #if the proper ack is received, return to send next segment of data
            if int(ack[1].decode()) == int(sequence_number) and int(ack[2].decode()) == int(ACKMSG):
                #ack_received = True
                return
        except socket.timeout:
            #print(f"timeout sequence number: {sequence_number}. retransmit...")
            sock.sendto(packet, server_address)
            retries+=1

# Function to receive data using RUDP
def rdt_recv(sock:socket, fp:BinaryIO):
    expected = 0
    datastr = b''
    try:
        while True:
            packet, client_address = sock.recvfrom(1024)
            sequence_number, ack_number, messagetype, data = breakdownPacket(packet)
            #print(sequence_number)
            #print(expected)
            sequence_number = sequence_number.decode()
            if len(data) == 0:
                fp.write(datastr)
                ack_packet = generatePacket(0, sequence_number, ACKMSG, b'')
                sock.sendto(ack_packet, client_address)
                break
            elif int(sequence_number) == expected:
                ack_packet = generatePacket(0, sequence_number, ACKMSG, b'')
                sock.sendto(ack_packet, client_address)
                datastr += data
                expected = 1 - expected
            #else:
                #print(f"Received out-of-sequence packet with sequence number: {sequence_number}")
    except KeyboardInterrupt:
        return
        #print("Timeout while waiting for a packet.")
        
def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    # make socket for udp
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind socket to interface and port
    server_address = (iface, port)
    sock.bind(server_address)
    try:
        print("Hello, I am server")
        rdt_recv(sock, fp)
        sock.close()
        return
    except KeyboardInterrupt:
        print("Server terminated by user.")
    finally:
        sock.close()

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        data = fp.read()
        print("Hello, I am a client")
        seqn = 0
        while data:
            server_address = (host, port)
            rdt_send(sock, data[:MESSAGELIMIT], seqn, server_address)
            data = data[MESSAGELIMIT:]
            if len(data) == 0:
                rdt_send(sock, data, seqn, server_address)
                break
            seqn = 1 - seqn
    except KeyboardInterrupt:
        print("Client terminated by user.")
    finally:
        sock.close()