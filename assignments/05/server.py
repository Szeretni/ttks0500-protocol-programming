import socket
import sys

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

try:
    ip = sys.argv[1]
    port = int(sys.argv[2])
except (IndexError, ValueError):
    print "Error, please check the arguments. Valid syntax: python server.py <ip> <port>"

try:
    sock.bind((ip,port))
except (socket.gaierror):
    print "Error, please check the ip and port for any mistakes."
