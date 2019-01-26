'''
Assignment 01 (1 point)
Write a function that takes two (2) parameters
    Socket
    Data
Function should send all of the data to the socket
send() might not send everything!
Function should raise an exception if some error occurs
This can be any error and exception can be your own string
Optional step:
create a server side function that does the opposite (receives until the message is fully received)
Hints:
How you know how many bytes your string is?
send()-method returns something usefull
Compare something until 2 values match with each other
'''

import socket
import sys

def function1(socket,data):
    try:
        socket.connect(("localhost",8888))
        print "bytes sent:",socket.sendall(data) # returns the number of bytes sent
        print socket.recv(1024)
        socket.close()
    except:
        print sys.exc_info()[0]

def initsock():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return s

def initdata():
    data = "terve"
    print "size of data in bytes:",sys.getsizeof(data)-33 # str objects seems to have 33 bytes preallocated + 1 byte per additional char
    return data

function1(initsock(),initdata())
