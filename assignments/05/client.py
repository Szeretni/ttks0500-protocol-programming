import socket
import sys

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except (IndexError, ValueError):
    print "Error, please check the arguments. Valid syntax: python client.py <ip> <port>"

try:
    sock.connect((ip,port))
except (socket.gaierror):
    print "Error, please check the ip and port for any mistakes. Otherwise, the server might be down."
