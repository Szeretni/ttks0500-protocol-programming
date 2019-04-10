import socket
import sys
from todo import TODO

# Example usage of the client: python client.py localhost 1234 "LIST 0 ."

# Creating a socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Preliminary value checks for values which were provided by the user.
try:
    # Get ip and port from the values.
    (ip,port) = TODO.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

# Main functionality.
try:
    # Get method, bodylength, parameter and body (Client requests in this spec does not have a body).
    userInput = sys.argv[3].strip().split(" ")
    method,bodylength,parameter,body = TODO.validateInput(userInput)

    # Connecting to the server.
    try:
        sock.connect((ip,port))
    except (socket.gaierror, socket.error):
        print "Error, please check the ip and port for any mistakes. Otherwise, the server might be down."
        exit()

    # Write and send a request to the server. Get the response's "header" (METHOD BODYLENGTH PARAMETER) and a possible body.
    message = TODO.writeMessage(method,bodylength,parameter,body)
    TODO.sendMessage(message,sock)
    headeritems = TODO.receiveHeader(sock)
    TODO.receiveBody(sock,headeritems)
except socket.error:
    print "Connection closed."
except ValueError as ex:
    print ex
except NameError as ex:
    print ex
except TypeError as ex:
    print ex
except AssertionError as ex:
    print ex
finally:
    # Close the socket.
    sock.close()
