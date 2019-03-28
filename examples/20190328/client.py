import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",8888))

while True:
    try:
        msg = raw_input("Write a message: ")
        s.send(msg)
        print s.recv(1024)
    except KeyboardInterrupt:
        s.close()
