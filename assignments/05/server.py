import os
import socket
import sys
from functions import Functions as fns

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

try:
    (ip,port) = fns.argumentCheck(sys.argv)
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
        request = client.recv(fns.getBufferSize())
        print "A request:\n",request

        request = request
        requestItems = request.split(" ")

        if len(requestItems) != 3:
            print "Invaled request: ",request
            client.close()
            continue

        method = requestItems[0]
        bodylenght = int(requestItems[1])
        parameterAndBody = requestItems[2].split("\r\n")
        parameter = parameterAndBody[0]
        if(parameter.find('../') != -1):
            print "Invalid path, don't try to enter parent folders!"
            client.close()
            continue

        if bodylenght != 0:
            print "Request's body lenght is non-zero. Terminating."
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
                response = fns.writeMessage("LISTRESPONSE",len(body),len(files),body)
                print response
                client.send(response)
            else:
                try:
                    files = os.listdir(str("files/%s" % parameter))
                    body = ""
                    for x in range(0,len(files)):
                        if x != len(files)-1:
                            body += files[x] + "\r\n"
                        else:
                            body += files[x]
                    response = fns.writeMessage("LISTRESPONSE",len(body),len(files),body)
                    print response
                    client.send(response)
                except OSError:
                    response = fns.writeMessage("ERROR",0,1,None)
                    print response
                    client.send(response)
        elif method == "DOWNLOAD":
            parameterItems = parameter.split("/")
            numOfItems = len(parameterItems)
            fileName = parameterItems[numOfItems-1]
            path = parameter[:(len(parameter)-len(fileName))]
            try:
                folder = "files/%s" % path
                folderAndfile = folder + fileName
                file = open(folderAndfile)
                data = file.read(fns.getBufferSize())
                response = fns.writeMessage("FILE",len(data),fileName,data)
                client.send(response)
            except IOError as ex:
                if ex.args[0] == 21:
                    print "IOError 21, 'Is a directory'"
                    response = fns.writeMessage("ERROR",0,2,None)
                    client.send(response)
                elif ex.args[0] == 2:
                    print "IOError 2, 'No such file or directory'"
                    response = fns.writeMessage("ERROR",0,3,None)
                    client.send(response)

        client.close()
    except KeyboardInterrupt:
        print "\nGood bye."
        client.close()
        sock.close()
        break
