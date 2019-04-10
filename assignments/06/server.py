import logging
import socket
import sys
import threading
import time
from todo import TODO

# Example usage of the server: python server.py localhost 1234

# Creating a socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# Preliminary value checks for values which were provided by the user.
try:
    (ip,port) = TODO.argumentCheck(sys.argv)
except (IndexError, ValueError):
    exit()

# Binding the socket.
try:
    sock.bind((ip,port))
except (socket.gaierror):
    print "Error, please check the ip and port for any mistakes."

# Listening for requests.
sock.listen(5)

# Lock is used to mutual exclusion when todo.txt is accessed for read/write ops
lock = threading.Lock()

# Client thread (main loop is last in this file)
# Logging to a file to prove that mutex works
logging.basicConfig(filename="debug.log",level=logging.DEBUG,format="(%(asctime)s  %(threadName)s %(message)s)")
def clientThread(client,addr):
    try:
        # Getting the request's "header" (METHOD BODYLENGTH PARAMETER).
        requestItems = TODO.receiveHeader(client)

        # Spreading the request's items.
        method,bodylength,parameter,body = TODO.validateInput(requestItems)

        # The spec states that the current client requests' body length is 0.
        # If 0, then the server responds with ERROR and continues to listen for connections.
        if bodylength != 0:
            print "Request's body length is non-zero. Terminating."
            response = TODO.writeMessage("ERROR",0,1,None)
            TODO.sendMessage(response,client)
            client.close()

        response = ""
        # LIST response.
        if method == "LIST":
            logging.debug("trying to acquire the lock")
            lock.acquire()
            logging.debug("acquired the lock for listing todo item")
            try:
                if parameter == ".":
                    body, files = TODO.listTodo()
                    # LISTRESPONSE with todo items.
                    response = TODO.writeMessage("LISTRESPONSE",len(body),files,body)
                else:
                    response = TODO.writeMessage("ERROR",0,2,None)
            except:
                response = TODO.writeMessage("ERROR",0,2,None)
            finally:
                lock.release()
                logging.debug("released the lock")
        # ADD response.
        elif method == "ADD":
            logging.debug("trying to acquire the lock")
            lock.acquire()
            logging.debug("acquired the lock for adding todo item")
            time.sleep(5)
            try:
                TODO.writeTodo(parameter)
                response = TODO.writeMessage("OK",0,1,None)
            except:
                response = TODO.writeMessage("ERROR",0,3,None)
            finally:
                lock.release()
                logging.debug("released the lock")
        elif method == "DONE":
            logging.debug("trying to acquire the lock")
            lock.acquire()
            logging.debug("acquired the lock for removing todo item")
            time.sleep(5)
            try:
                TODO.doneTodo(parameter)
                response = TODO.writeMessage("OK",0,2,None)
            except:
                response = TODO.writeMessage("ERROR",0,4,None)
            finally:
                lock.release()
                logging.debug("released the lock")
        # Sending the response to the client.
        TODO.sendMessage(response,client)
        client.close()
        print "Closed the connection to",addr,"\n"
    except KeyboardInterrupt:
        print "\nGood bye."
        client.close()

#Main functionality.
while True:
    try:
        # Establishing a connection.
        print "Waiting for new connections."
        (client,addr) = sock.accept()
        print "A new connection from ",addr

        # Starting a new thread for connection. Allows multiple simultaneous client connections.
        thread = threading.Thread(target=clientThread,args=(client,addr))
        thread.start()
    except KeyboardInterrupt:
        print "\nGood bye."
        client.close()
        break

sock.close()
