# -*- coding: utf-8 -*-
import socket

def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("localhost",8888))
    s.listen(5)
    (client,addr) = s.accept()
    while True:
        data = client.recv(1024)
        if data == "":
            break
        print data.decode("utf-8", "replace")

main()
