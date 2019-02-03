import socket
import assignment02functions as f

def main():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind(("localhost",8888))
	sock.listen(5)
	(client,addr) = sock.accept()
	print "Received a connection from",addr
	print client.recv(1024)
	client.send(f.writeMsg())
	sock.close()

if __name__ == "__main__":
	main()
