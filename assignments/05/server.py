import socket
import sys
from dftp import DFTP

# Example usage of the server: python server.py localhost 1234

# Creating a socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# Preliminary value checks for values which were provided by the user.
try:
    (ip,port) = DFTP.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

# Binding the socket.
try:
    sock.bind((ip,port))
except (socket.gaierror):
    print "Error, please check the ip and port for any mistakes."

# Listening for requests.
sock.listen(5)

#Main functionality.
while True:
    try:
        # Establishing a connection.
        print "Waiting for new connections."
        (client,addr) = sock.accept()
        print "A new connection from ",addr

        # Getting the request's "header" (METHOD BODYLENGTH PARAMETER).
        requestItems = DFTP.receiveHeader(client)

        # Testing for a correct number of items (METHOD BODYLENGTH PARAMETER).
        # If malformed, then the server responds with ERROR and continues to listen for connections.
        if len(requestItems) != 3:
            print "Invaled request: ",requestItems[0]
            response = DFTP.writeMessage("ERROR",0,4,None)
            DFTP.sendMessage(response,client)
            client.close()
            continue

        # Spreading the request's items.
        method,bodylength,parameter,body = DFTP.parseItems(requestItems)

        # The response's are not allowed to ask for the server's download folder's parent folders.
        # If asking, then the server responds with ERROR and continues to listen for connections.
        if(parameter.find('../') != -1):
            print "Invalid path, client tried to enter parent folders!"
            response = DFTP.writeMessage("ERROR",0,4,None)
            DFTP.sendMessage(response,client)
            client.close()
            continue

        # The spec states that the current client requests' body length is 0.
        # If 0, then the server responds with ERROR and continues to listen for connections.
        if bodylength != 0:
            print "Request's body length is non-zero. Terminating."
            response = DFTP.writeMessage("ERROR",0,4,None)
            DFTP.sendMessage(response,client)
            client.close()
            continue

        # Specifies the default download folder.
        basedir = "files/"
        response = ""
        # LIST response.
        if method == "LIST":
            try:
                # The request param "." gets the default folder's file names.
                if parameter == ".":
                    body,files = DFTP.listFiles(basedir,None)
                # The request param ie. "folder1" gets the default folder's subfolder's file names.
                else:
                    body,files = DFTP.listFiles(basedir,parameter)
                # LISTRESPONSE with the file names.
                response = DFTP.writeMessage("LISTRESPONSE",len(body),files,body)
                print response
            except OSError:
                # Folder not found or the request param is a file name.
                response = DFTP.writeMessage("ERROR",0,1,None)
                print response
        # DOWNLOAD response.
        elif method == "DOWNLOAD":
            try:
                # DOWNLOAD response with a single file. The request param is a relative path to the file ie. "nicepic.png", "folder1/fileInFolder1.txt".
                filename,data = DFTP.downloadFile(basedir,parameter)
                response = DFTP.writeMessage("FILE",len(data),filename,data)
                print "FILE",len(data),filename
            except IOError as ex:
                # ERROR response if the requested "file" is a dir.
                if ex.args[0] == 21:
                    print "IOError 21, 'Is a directory'"
                    response = DFTP.writeMessage("ERROR",0,2,None)
                # ERROR response if the requested file doesn't exists.
                elif ex.args[0] == 2:
                    print "IOError 2, 'No such file or directory'"
                    response = DFTP.writeMessage("ERROR",0,3,None)
        # Sending the response to the client.
        DFTP.sendMessage(response,client)
        client.close()
        print "Closed the connection to",addr,"\n"
    except KeyboardInterrupt:
        print "\nGood bye."
        client.close()
        sock.close()
        break
