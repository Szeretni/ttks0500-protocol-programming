import socket
import sys

#argv1 addr, argv2 port

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
try:
    s.bind((sys.argv[1],int(sys.argv[2])))
except (TypeError,IndexError):
    print "error, please check the arguments"
    exit()
s.listen(5)
while True:
    try:
        print "waiting for a new connection"
        (client,addr) = s.accept()
        print "new connection from",addr
        #not making sure everything is received, not required in this assignment
        print "message from client:",client.recv(1024)
        client.close()
    except KeyboardInterrupt:
        print "\ninterrupted - exiting"
        s.close()
        break

''' output
assignments/03$ python server.py "localhost" 8888
waiting for a new connection
conn from ('127.0.0.1', 39310)
message from client: hello world
waiting for a new connection
'''
