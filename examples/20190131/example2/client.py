import socket

osoite = "localhost"
portti = 8888
tiedosto = "kisu.jpg"

def main():
	sukka = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sukka.connect((osoite,portti))

	sukka.send(tiedosto+"\n")

	kuva = open(tiedosto, 'rb')

	data = kuva.read(1024)

	while data:
		sukka.send(data)
		data = kuva.read(1024)

	print "Kuva lahetetty onnistuneesti"
	kuva.close()
	sukka.close()

main()
