def initMsg():
    return "hello world"

def msgLen(msg):
    return len(msg)

def writeMsg():
    msg = initMsg()
    return str(msgLen(msg))+"\n"+msg

def readMsg(msg):
    payloadBytes = calcIncMsgLen(msg)
    return readPayload(msg,payloadBytes)

def calcIncMsgLen(msg):
    incomingBytes = ""
    while 1:
        byte = msg.read(1)
        if byte == "\n":
            break
        else:
            incomingBytes += byte
    return int(incomingBytes)

def readPayload(msg,payloadBytes):
    
