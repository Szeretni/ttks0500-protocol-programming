import socket
import sys
from dftp import DFTP

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    (ip,port) = DFTP.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

try:
    userInput = sys.argv[3].strip().split(" ")
    method,bodylenght,parameter,body = DFTP.validateInput(userInput)

    try:
        sock.connect((ip,port))
    except (socket.gaierror, socket.error):
        print "Error, please check the ip and port for any mistakes. Otherwise, the server might be down."
        exit()

    message = DFTP.writeMessage(method,bodylenght,parameter,body)
    DFTP.sendMessage(message,sock)
    DFTP.receiveMessage(sock)

    sock.close()
except socket.error:
    print "Connection closed."
    sock.close()
except ValueError as ex:
    print ex
    sock.close()
except NameError as ex:
    print ex
    sock.close()
except TypeError as ex:
    print ex
    sock.close()
except AssertionError as ex:
    print ex
    sock.close()
