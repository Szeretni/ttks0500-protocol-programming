def sendMsg(socket):
    msg = initMsg()
    msg_len = msgLen(msg)
    sentBytes = 0
    sendMsgLen(socket,msg_len)
    while sentBytes < msg_len:
        sentBytes += socket.send(msg[sentBytes:])
        print "sent %d of %d bytes" % (sentBytes,msg_len)

def initMsg():
    return "hello world" * 1000

def msgLen(msg):
    return len(msg)

def sendMsgLen(socket,msg_len):
    socket.send(str(msg_len)+"\n")

def readMsg(client):
    incomingBytes = calcIncMsgLen(client)
    receivedBytes = 0
    payload = ""
    while receivedBytes < incomingBytes:
        payload += client.recv(1024)
        receivedBytes = len(payload)
        print "received %d of %d bytes" % (receivedBytes,incomingBytes)

def calcIncMsgLen(client):
    incomingBytes = ""
    while 1:
        byte = client.recv(1)
        if byte == "\n":
            break
        else:
            incomingBytes += byte
    return int(incomingBytes)
