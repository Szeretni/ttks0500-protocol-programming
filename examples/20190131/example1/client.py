import socket
import toiminnallisuus

sukka = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sukka.connect(("localhost",8888))

data = "A"*2000

toiminnallisuus.laheta_viesti(sukka,data)

vastaus = toiminnallisuus.lue_viesti(sukka)
print vastaus
sukka.close()

