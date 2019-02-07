import socket

VALID_METHODS = ["GET","POST","PUT"]

request_line = "GET / HTTP/1.1"
status_line = "HTTP/1.1 200 OK"

def parse_request_line(line):
    parts = line.split(" ")
    if len(parts) != 3:
        print "Malformed request line"
    method = parts[0]
    resource = parts[1]
    version = parts[2]

    if method not in VALID_METHODS:
        print "UnknownHTTPMethod"

    return (method,resource,version)

def validate_http_version(version):
    if "/" not in version:
        print "MalformedHTTPVersion"

    (name,number) = version.split("/")

    if name != "HTTP":
        print "MalformedHTTPVersion"

    if "." not in number:
        print "MalformedHTTPVersion"

    #check major minor digits

    return "kaikki ok"

print parse_request_line(request_line)
esim = "HTTP/1.1"
print validate_http_version(esim)
