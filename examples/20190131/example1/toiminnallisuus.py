def send_data(socket,data):
	total = 0
	while total < len(data):
		lahetetty = socket.send(data[total:])
		total += lahetetty
	print "Lahetettiin %d tavua" % total

def laheta_viesti(socket,data):
	data_len = len(data)
	send_data(socket,str(data_len)+"\n")
	send_data(socket,data)

def lue_pituus(socket):
	bufferi = ""
	while True:
		apu = socket.recv(1)
		if apu == "\n":
			break
		bufferi += apu
	return int(bufferi)

def lue_viesti(socket):
	bufferi = ""
	pituus = lue_pituus(socket)
	print "Tavuja tulossa: ", pituus

	vastaanotettu = 0

	while vastaanotettu < pituus:
		data = socket.recv(1024)
		bufferi += data
		vastaanotettu += len(data)

	return bufferi


