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
        write_header(self,f,self.headers)
        f.write("\r\n")
        f.flush() #tyhjentää bufferin eli pakoittaa kirjoituksen file-objektiin ilman sen sulkemista
        print "Request sent"

def write_header(self,f,headers):
#    print "write_headers"
    # https://tools.ietf.org/html/rfc7230#section-3.2
    for header,value in headers.iteritems():
        f.write("%s: %s\r\n" % (header,value))

# luodaan uusi luokka demonstroimaan http-responea
# tärkeää huomata, että statusline eroaa requestlinesta
class HttpResponse:
    def __init__(self,status_code,reason,body,headers={}):
        self.status_code = status_code
        self.reason = reason
        self.body = body
        self.headers = headers
        # https://tools.ietf.org/html/rfc7230#section-3

    @staticmethod
    def read_from(f):
        status_code,reason = HttpResponse.read_statusline(f)
        headers = read_headers(f)
        body = "".join(f.readlines())
        return HttpResponse(status_code,reason,body,headers)

    def write_to(self,f):
        f.write("HTTP/1.1 %d %s\r\n" % (self.status_code,self.reason))
        write_header(self,f,self.headers)
        f.write("\r\n")
        f.write("%s" % self.body)
        f.flush()

    # luodaanstaattinen metodi statuslinen lukemiseen
    # annetaan parametrina fileobject
    # staattista metodia kutsutaan luokan nimellä ja metodilla
    @staticmethod
    def read_statusline(f):
        # readline metodi palauttaa string kaikki ennen \n merkkiä ja myös sen
        # siistitään merkkijono strip(), joka poistaa whitespaces
        status_line = f.readline().strip()

        # number of items, matches rfc?
        # reason may have multiple items when split with sp
        parts = status_line.split(" ")
        print len(parts)
        if len(parts) < 3:
            print "MalformedStatusline"

        version = parts[0]
        if version != "HTTP/1.1":
            print "UnsupportedHttpVersion"

        try:
            status_code = int(parts[1])
        except ValueError:
            print "Not a number"

        reason = " ".join(parts[2:]).strip()

        return (status_code,reason)

    def read_headers(self,f):
        headers = {}
        for rawline in f:
            line = rawline.strip()
            if line == "":
                break
            parts = line.split(":")
            if len(parts) < 2:
                print "MalformedHttpHeader"
            key = parts[0].strip()
            value = ".".join.parts[1:].strip()
            headers[key] = value
        return headers

class UnknownHTTPMethodException(Exception):
    pass

class NoHostHeaderException(Exception):
    pass
    # code blockit eivät saa olla tyhjiä, siksi pass keyword
