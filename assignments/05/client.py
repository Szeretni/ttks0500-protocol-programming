import socket
import sys
from functions import Functions as fns

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    (ip,port) = fns.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

try:
    requestItems = sys.argv[3].strip().split(" ")
    if len(requestItems) != 3:
        raise ValueError("The request is invalid. Example request: LIST 0 .")
    else:
        try:
            sock.connect((ip,port))
        except (socket.gaierror, socket.error):
            print "Error, please check the ip and port for any mistakes. Otherwise, the server might be down."
            exit()
        method = requestItems[0]
        bodylenght = requestItems[1]
        parameter = requestItems[2]
        body = None

        try:
            request = fns.writeMessage(method,bodylenght,parameter,body)
            sentBytes = 0
            while True:
                sentBytes += sock.send(request[sentBytes:])
                if sentBytes == len(request):
                    print "A request sent succesfully."
                    break
        except NameError as ex:
            print ex
        except ValueError:
            pass
        except TypeError as ex:
            print ex
        except AssertionError as ex:
            print ex
#    response = sock.recv(fns.getBufferSize())
    response = ""
    metadataLen = 0
    print "Waiting for a response"
    while True:
        responseData = sock.recv(1)
        response += responseData
        if response.find("\r\n") != -1:
            print "The response's metadata received succesfully."
            metadataLen = len(response)
            break
    responseItems = response.split(" ")
    method = responseItems[0]
    bodyLen = int(responseItems[1])
    parameter = responseItems[2].strip()
    body = ""
    while bodyLen != len(body):
        body += sock.recv(fns.getBufferSize())
    if method == "FILE":
        print response
        fileName = parameter
        file = open(fileName,"wb")
        file.write(body)
        file.close()
        print fileName,"downloaded."
    else:
        print response,body
    sock.close()
except socket.error:
    print "Connection closed."
    sock.close()
except ValueError as ex:
    print ex
    sock.close()
