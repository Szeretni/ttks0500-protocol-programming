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
        request = client.recv(1024)
        print "A message: ",request

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

        if method == "LIST" and bodylenght != 0:
            print "LIST's body lenght != 0"
            client.close()
            continue
        elif method == "LIST":
            baseDir = "files"
            if parameter == ".":
                files = os.listdir("files")
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
                body = os.listdir(str("files/%s" % parameter))
                response = fns.writeMessage("LISTRESPONSE",len(body),len(files),body)
                print response
                client.send(response)


        client.close()
    except KeyboardInterrupt:
        print "\nGood bye."
        client.close()
        sock.close()
        break
