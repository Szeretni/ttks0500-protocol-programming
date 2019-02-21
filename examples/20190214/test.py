# -*- coding: utf-8 -*-
from request import HttpRequest,HttpResponse
import socket
import sys

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

def main1():
    host = "httpbin.org"
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,80))

    # https://tools.ietf.org/html/rfc7230#section-6.1
    req = HttpRequest("GET","/",headers={"Host":host,"Connection":"close"})

    f = sock.makefile()
    req.write_to(f)

    '''
    response = HttpResponse.read_from(f)
    print response.status_code
    print "tästä alkaa responsen body"
    print response.body
    '''

    response = HttpResponse(200,"OK","Olen torso\n",headers={"Host":"localhost"})
    response.write_to(sys.stdout)

    f.close()
    sock.close()

main1()
