# -*- coding: utf-8 -*-
import socket

def send_data(socket,data):
    total = 0
    while total < len(data):
        sent = socket.send(data[total:])
        total += sent
    print "Sent %d bytes" % total

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(("localhost",8888))

viesti = u"説" * 1000

data = viesti.encode("utf-8")

send_data(socket,data)
socket.close()
