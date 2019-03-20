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
    exit()


try:
    requestRaw = raw_input("Make a request: ")
    requestItems = requestRaw.split(" ")

    if len(requestItems) != 3:
        print "The request is missing parts. Example request: LIST 0 ."
    else:
        method = requestItems[0]
        bodylenght = requestItems[1]
        parameter = requestItems[2]
        body = None

        try:
            sock.send(fns.writeMessage(method,bodylenght,parameter,body))
        except NameError as ex:
            print ex
        except ValueError:
            pass
        except TypeError as ex:
            print ex
        except AssertionError as ex:
            print ex
    sock.close()
except socket.error:
    print "Connection closed."
    sock.close()
    exit()
