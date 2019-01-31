import socket
import toiminnallisuus

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.bind(("localhost",8888))
s.listen(5)

client,addr = s.accept()

viesti = toiminnallisuus.lue_viesti(client)
print viesti

toiminnallisuus.laheta_viesti(client,"SAIN T:SERVERI")
client.close()
s.close()
