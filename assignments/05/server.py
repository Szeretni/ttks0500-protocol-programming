import os
import socket
import sys
from dftp import DFTP

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

try:
    (ip,port) = DFTP.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

try:
    sock.bind((ip,port))
except (socket.gaierror):
    print "Error, please check the ip and port for any mistakes."

sock.listen(5)

while True:
    try:
        print "Waiting for new connections."
        (client,addr) = sock.accept()
        print "A new connection from ",addr
        requestData = client.recv(DFTP.getBufferSize())
        request = ""
        while True:
            request += requestData
            if request.find("\r\n") != -1:
                print "A request received succesfully."
                break
            requestData = client.recv(DFTP.getBufferSize())
        print "The request:\n",request

        requestItems = request.split(" ")

        if len(requestItems) != 3:
            print "Invaled request: ",request
            response = DFTP.writeMessage("ERROR",0,4,None)
            print "Sending a message."
            print response
            sentBytes = 0
            while True:
                sentBytes += client.send(response[sentBytes:])
                if sentBytes == len(response):
                    print "The message sent succesfully."
                    break
            client.close()
            continue

        method = requestItems[0]
        bodylenght = int(requestItems[1])
        parameterAndBody = requestItems[2].split("\r\n")
        parameter = parameterAndBody[0]
        if(parameter.find('../') != -1):
            print "Invalid path, don't try to enter parent folders!"
            response = DFTP.writeMessage("ERROR",0,4,None)
            print "Sending a message."
            print response
            sentBytes = 0
            while True:
                sentBytes += client.send(response[sentBytes:])
                if sentBytes == len(response):
                    print "The message sent succesfully."
                    break
            client.close()
            continue

        if bodylenght != 0:
            print "Request's body lenght is non-zero. Terminating."
            response = DFTP.writeMessage("ERROR",0,4,None)
            print "Sending a message."
            print response
            sentBytes = 0
            while True:
                sentBytes += client.send(response[sentBytes:])
                if sentBytes == len(response):
                    print "The message sent succesfully."
                    break
            client.close()
            continue

        baseDir = "files"
        if method == "LIST":
            if parameter == ".":
                files = os.listdir("files/")
                body = ""
                for x in range(0,len(files)):
                    if x != len(files)-1:
                        body += files[x] + "\r\n"
                    else:
                        body += files[x]
                response = DFTP.writeMessage("LISTRESPONSE",len(body),len(files),body)
                print "Sending a message."
                print response
                sentBytes = 0
                while True:
                    sentBytes += client.send(response[sentBytes:])
                    if sentBytes == len(response):
                        print "The message sent succesfully."
                        break
            else:
                try:
                    files = os.listdir(str("files/%s" % parameter))
                    body = ""
                    for x in range(0,len(files)):
                        if x != len(files)-1:
                            body += files[x] + "\r\n"
                        else:
                            body += files[x]
                    response = DFTP.writeMessage("LISTRESPONSE",len(body),len(files),body)
                    print "Sending a message."
                    print response
                    sentBytes = 0
                    while True:
                        sentBytes += client.send(response[sentBytes:])
                        if sentBytes == len(response):
                            print "The message sent succesfully."
                            break
                except OSError:
                    response = DFTP.writeMessage("ERROR",0,1,None)
                    print "Sending a message."
                    print response
                    sentBytes = 0
                    while True:
                        sentBytes += client.send(response[sentBytes:])
                        if sentBytes == len(response):
                            print "The message sent succesfully."
                            break
        elif method == "DOWNLOAD":
            parameterItems = parameter.split("/")
            numOfItems = len(parameterItems)
            fileName = parameterItems[numOfItems-1]
            path = parameter[:(len(parameter)-len(fileName))]
            try:
                folder = "files/%s" % path
                folderAndfile = folder + fileName
                file = open(folderAndfile)
                data = file.read()
                response = DFTP.writeMessage("FILE",len(data),fileName,data)
                print "Sending a message."
                sentBytes = 0
                while True:
                    sentBytes += client.send(response[sentBytes:])
                    if sentBytes == len(response):
                        print "The message sent succesfully."
                        break
            except IOError as ex:
                if ex.args[0] == 21:
                    print "IOError 21, 'Is a directory'"
                    response = DFTP.writeMessage("ERROR",0,2,None)
                    print "Sending a message."
                    print response
                    sentBytes = 0
                    while True:
                        sentBytes += client.send(response[sentBytes:])
                        if sentBytes == len(response):
                            print "The message sent succesfully."
                            break
                elif ex.args[0] == 2:
                    print "IOError 2, 'No such file or directory'"
                    response = DFTP.writeMessage("ERROR",0,3,None)
                    print "Sending a message."
                    print response
                    sentBytes = 0
                    while True:
                        sentBytes += client.send(response[sentBytes:])
                        if sentBytes == len(response):
                            print "The message sent succesfully."
                            break
        client.close()
        print "Connection closed to",addr,"\n"
    except KeyboardInterrupt:
        print "\nGood bye."
        client.close()
        sock.close()
        break
