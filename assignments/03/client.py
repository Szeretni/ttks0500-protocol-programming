import socket
import sys

#argv1 addr, argv2 port, argv3 message

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect((sys.argv[1],int(sys.argv[2])))
except (TypeError,IndexError):
    print "error, please check the arguments"
    s.close()
    exit()
except socket.error:
    print "connection refused"
    s.close()
    exit()
try:
    sentBytes = s.send(sys.argv[3])
    if sentBytes == len(sys.argv[3]):
        print "sent the message:",sys.argv[3]
    else:
        print "did't send the message"
except TypeError:
    print "invalid send arg"
except NameError:
    print"no such variable"
except IndexError:
    print "check args"
s.close()

''' output
assignments/03$ python client.py "localhost" 8888 "hello world"
sent the message: hello world
'''
