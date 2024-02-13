import argparse

import socket, time

from gobackn import gbn_server, gbn_client

def runServer(iface, port, fp):
    gbn_server(iface, port,fp)
def runClient(host,port,fp):
    gbn_client(host,port,fp)


mode = input("Would you like to send or receive? (Input: 'SEND' or 'RECEIVE'): ")
if(mode == "SEND"):
    host = input("Input the host (localhost for local transfer): ")
    port = input("Input the port: ")
    file = input("What is the name of the file you want to send?: ")
    runClient(host,port,file)
if(mode == "RECEIVE"):
    iface = input("Input the interface (ip / localhost for local transfer): ")
    port = input("Input the port: ")
    file = input("What file would you like to save the transfer to?: ")
    runServer(iface,port,file)
