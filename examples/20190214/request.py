# -*- coding: utf-8 -*-

# request methods
# https://tools.ietf.org/html/rfc7231#section-4

HTTP_VALID_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE"
]

# message format
# https://tools.ietf.org/html/rfc7230#section-3

class HttpRequest:
    def __init__(self,method,resource="/",headers={},body=None):
        self.method = method
        self.resource = resource
        self.headers = headers

        if method not in HTTP_VALID_METHODS:
            raise UnknownHTTPMethodException("Invalid method)")
        else:
            print "Request method was ok"

        # https://tools.ietf.org/html/rfc7230#section-5.4
        if not "Host" in headers.keys():
            raise NoHostHeaderException()
        else:
            print "Request: Host header was ok"

    def write_to(self,f):
        print "Request: request's write method"
        # https://tools.ietf.org/html/rfc7230#section-3.1.1
        f.write("%s %s HTTP/1.1\r\n" % (self.method,self.resource))
        self.write_header(f,self.headers)
        f.write("\r\n")
        f.flush() #tyhjentää bufferin eli pakoittaa kirjoituksen file-objektiin ilman sen sulkemista
        print "Request sent"

    def write_header(self,f,headers):
        print "write_headers"
        # https://tools.ietf.org/html/rfc7230#section-3.2
        for header,value in headers.iteritems():
            f.write("%s: %s\r\n" % (header,value))

class UnknownHTTPMethodException(Exception):
    pass

class NoHostHeaderException(Exception):
    pass
    # code blockit eivät saa olla tyhjiä, siksi pass keyword
