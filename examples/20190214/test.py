# -*- coding: utf-8 -*-
from request import HttpRequest
import socket

def main():
    host = "httpbin.org"
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,80))

    # https://tools.ietf.org/html/rfc7230#section-6.1
    req = HttpRequest("GET","/",headers={"Host":host,"Connection":"close"})

    f = sock.makefile()
    req.write_to(f)
    for line in f:
        print line
    f.close()
    sock.close()

main()
