'''
Modify the client and the server example (from the material) to work correctly for arbitrarily sized messages.
This means two things: Make sure everything gets sent and received. Figure out a way to specify the length of the message to the receiver (on other words; how client knows how many bytes is incoming?)
'''

import socket
import assignment02functions as f

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",8888))
s.send(f.writeMsg())
print s.recv(1024)
s.close()
