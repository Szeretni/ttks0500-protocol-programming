import socket
import sys
import threading
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

        # Spreading the request's items.
        method,bodylength,parameter,body = DFTP.validateInput(requestItems)

        # The spec states that the current client requests' body length is 0.
        # If 0, then the server responds with ERROR and continues to listen for connections.
        if bodylength != 0:
            print "Request's body length is non-zero. Terminating."
            response = DFTP.writeMessage("ERROR",0,4,None)
            DFTP.sendMessage(response,client)
            client.close()
            continue

        response = ""
        # LIST response.
        if method == "LIST":
            try:
                response = ""
                # The request param "." gets the default folder's file names.
                if parameter == ".":
                    body, files = DFTP.listTodo()
                    response = DFTP.writeMessage("LISTRESPONSE",len(body),files,body)
                # The request param ie. "folder1" gets the default folder's subfolder's file names.
                else:
                    response = DFTP.writeMessage("ERROR",0,1,None)
                # LISTRESPONSE with the file names.
                print response
            except OSError:
                # Folder not found or the request param is a file name.
                response = DFTP.writeMessage("ERROR",0,1,None)
                print response
        # ADD response.
        elif method == "ADD":
            try:
                DFTP.writeTodo(parameter)
#                response = DFTP.writeMessage("FILE",len(data),filename,data)
#                print "FILE",len(data),filename
                response = DFTP.writeMessage("OK",0,0,None)
                print "OK"
            except IOError as ex:
                # ERROR response if the requested "file" is a dir.
                if ex.args[0] == 21:
                    print "IOError 21, 'Is a directory'"
                    response = DFTP.writeMessage("ERROR",0,2,None)
                # ERROR response if the requested file doesn't exists.
                elif ex.args[0] == 2:
                    print "IOError 2, 'No such file or directory'"
                    response = DFTP.writeMessage("ERROR",0,3,None)
        elif method == "DONE":
            print "done"
            try:
                DFTP.doneTodo(parameter)
#                response = DFTP.writeMessage("FILE",len(data),filename,data)
#                print "FILE",len(data),filename
                response = DFTP.writeMessage("OK",0,0,None)
                print "OK"
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
