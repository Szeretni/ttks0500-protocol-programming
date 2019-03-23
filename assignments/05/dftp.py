class DFTP:
    def __init__(self):
        pass

    @staticmethod
    def argumentCheck(argv):
        try:
            ip = argv[1]
            port = int(argv[2])
            return (ip,port)
        except (IndexError, ValueError) as ex:
            print "Error, please check the arguments. Valid syntax: python client/server.py <ip> <port>"
            raise ex

    @staticmethod
    def validateInput(requestItems):
        if len(requestItems) != 3:
            raise ValueError("The request is invalid. Example request: LIST 0 .")

        (method,bodylenght,parameter,body) = DFTP.parseInput(requestItems)

        if method not in DFTP.getValidMethods():
            raise NameError("Invalid method.")

        try:
            if int(bodylenght) < 0:
                raise TypeError("Invalid body lenght.")
        except ValueError:
            raise ValueError("Body lenght is not a number.")

        if parameter is None:
            raise AssertionError("Error, parameter is null.")

        return method,bodylenght,parameter,body

    @staticmethod
    def parseInput(requestItems):
        method = requestItems[0]
        bodylenght = requestItems[1]
        parameter = requestItems[2]
        body = None

        return method,bodylenght,parameter,body

    @staticmethod
    def writeMessage(method,bodylenght,parameter,body):
        if method not in DFTP.getValidMethods():
            raise NameError("Invalid method.")
        try:
            if int(bodylenght) < 0:
                raise TypeError("Invalid body lenght.")
        except ValueError as ex:
            print "Body lenght is not a number."
            raise ex
        if parameter is None:
            raise AssertionError("Error, parameter is null.")
        if body is None:
            return "%s %s %s\r\n" %(method, bodylenght, parameter)
        else:
            return "%s %s %s\r\n%s" %(method, bodylenght, parameter, body)

    @staticmethod
    def sendMessage(message,sock):
        sentBytes = 0
        while True:
            sentBytes += sock.send(message[sentBytes:])
            if sentBytes == len(message):
                print "A message sent succesfully."
                break

    @staticmethod
    def receiveMessage(sock):
        response = ""
        metadataLen = 0
        print "Waiting for a message."
        while True:
            responseData = sock.recv(1)
            response += responseData
            if response.find("\r\n") != -1:
                print "Received the message succesfully."
                metadataLen = len(response)
                break
        responseItems = response.split(" ")
        method = responseItems[0]
        bodyLen = int(responseItems[1])
        parameter = responseItems[2].strip()
        body = ""
        while bodyLen != len(body):
            body += sock.recv(DFTP.getBufferSize())
        if method == "FILE":
            print response
            fileName = parameter
            file = open(fileName,"wb")
            file.write(body)
            file.close()
            print fileName,"downloaded."
        else:
            print response,body

    @staticmethod
    def getValidMethods():
        return ["LIST","LISTRESPONSE","DOWNLOAD","FILE","ERROR"]

    @staticmethod
    def getBufferSize():
        return 1024
