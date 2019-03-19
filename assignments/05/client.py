import socket
import sys
from functions import Functions as fns

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    (ip,port) = fns.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

try:
    sock.connect((ip,port))
except (socket.gaierror, socket.error):
    print "Error, please check the ip and port for any mistakes. Otherwise, the server might be down."
#    exit()

try:
    fns.writeMessage("mes","mes","mes","mes")
except NameError as ex:
    print ex
    exit()
