import socket

def server():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(("localhost",8888))
	s.listen(5)
	(client,addr) = s.accept()
	print "uusi yhteys osoitteesta",addr
	print client.recv(1024)
	client.send("Moi vaan t.server")

server()

