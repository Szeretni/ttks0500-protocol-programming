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
''' output
size of outgoing data: 5000
clien has sent 5000 bytes
server has received 5000 bytes
closing connection
'''

import socket
import sys

def sendData(socket,data):
    try:
        socket.connect(("localhost",8888))
        sizeOfData = sys.getsizeof(data)-33 # str objects seems to have 33 bytes preallocated + 1 byte per additional char
        print "size of outgoing data:",sizeOfData
        sentData = 0
        while sentData < sizeOfData:
            sentData += socket.send(data[sentData:]) # returns the number of bytes sent
            print "clien has sent %d bytes" % sentData
        msg = ""
        while True:
            msg += socket.recv(1)
            while not "\n" in msg:
                msg += socket.recv(1)
            if int(msg) == sentData:
                print "server has received %s bytes" % msg.strip()
                socket.send("closeConn")
                break
            msg = ""
        socket.close()
        print "closing connection"
    except:
        print sys.exc_info()[0]

def initsock():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return s

def initdata():
    data = "terve" * 1000
    return data

sendData(initsock(),initdata())
