import socket
import functions as f

def main():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sock.bind(("localhost",8888))
	sock.listen(5)
	(client,addr) = sock.accept()
	print "Received a connection from",addr
	f.readMsg(client)
	sock.close()

if __name__ == "__main__":
	main()

''' output
Received a connection from ('127.0.0.1', 59178)
received 1024 of 11000 bytes
received 2048 of 11000 bytes
received 3072 of 11000 bytes
received 4096 of 11000 bytes
received 5120 of 11000 bytes
received 6144 of 11000 bytes
received 7168 of 11000 bytes
received 8192 of 11000 bytes
received 9216 of 11000 bytes
received 10240 of 11000 bytes
received 11000 of 11000 bytes
'''
