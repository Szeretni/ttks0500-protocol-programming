''' output
new connection: ('127.0.0.1', 50122)
bytes received from client: 1024
bytes received from client: 2048
bytes received from client: 3072
bytes received from client: 4096
bytes received from client: 5000
closing connection
all 5000 bytes received - exiting
'''

import socket

def server():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("localhost",8888))
    s.listen(5)
    client,addr = s.accept()
    data = ""
    print "new connection:",addr
    while True:
        msg = client.recv(1024)
        if msg == "closeConn":
            print "closing connection"
            break
        data += msg
        bytesReceived = len(data)
        print "bytes received from client:",bytesReceived
        client.send(str(bytesReceived)+"\n")
    client.close()
    s.close()
    #print data
    print "all %s bytes received - exiting" % str(bytesReceived)

server()
