import socket
import threading

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("localhost",8888))
s.listen(5)

def clientthread(client,addr):
    while True:
        data = client.recv(1024)
        reply = "OK"
        if not data:
            break
        print data
        client.send(reply)
    client.close()

while True:
    client,addr = s.accept()
    print "connected:",addr[0],":",str(addr[1])

    thread = threading.Thread(target=clientthread,args=(client,addr))
    thread.start()

s.close()
