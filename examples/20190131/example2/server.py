import socket

osoite = "localhost"
portti = 8888
sijainti = "/home/student/"

def main():
	sukka = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sukka.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	sukka.bind(("localhost",8888))
	sukka.listen(5)
	print "servu on paalla"

	while True:
		client,addr = sukka.accept()
		filename = client.recv(1)
		while not "\n" in filename:
			filename += client.recv(1)

		filename = filename.strip()
		print len(filename),filename

		kuva = open(sijainti+filename,"wb")

		data = client.recv(1024)

		while data:
			kuva.write(data)
			data = client.recv(1024)

		print "kuva tuli perille!"

		kuva.close()
		break

	sukka.close()

main()
