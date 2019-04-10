import os

class DFTP:
    def __init__(self):
        pass

    # Returns ip and port, if provided correctly.
    @staticmethod
    def argumentCheck(argv):
        try:
            ip = argv[1]
            port = int(argv[2])
            return (ip,port)
        except (IndexError, ValueError) as ex:
            print "Error, please check the arguments. Valid syntax: python client/server.py <ip> <port>"
            raise ex

    # Returns request params if they can be parsed from the CLI command the user provided.
    @staticmethod
    def validateInput(requestItems):
        print requestItems

        numItems = len(requestItems)
        thirdItem = ""
        for x in range(2,numItems):
            thirdItem += requestItems[x] + " "
        for x in range(2,numItems):
            requestItems.pop()
        print thirdItem
        requestItems.append(thirdItem)
        print requestItems
#        requestItems.insert(2,thirdItem)
        if len(requestItems) != 3:
            raise ValueError("The request is invalid. Example request: LIST 0 .")

        method,bodylength,parameter,body = DFTP.parseItems(requestItems)
        DFTP.validateValues(method,bodylength,parameter,body)

        return method,bodylength,parameter,body

    # Runs checks to the values provided by the user.
    @staticmethod
    def validateValues(method,bodylength,parameter,body):
        if method not in DFTP.getValidMethods():
            raise NameError("Invalid method.")
        try:
            if bodylength < 0:
                raise TypeError("Invalid body length.")
        except ValueError as ex:
            raise ValueError("Body length is not a number.")
        if parameter is None:
            raise AssertionError("Error, parameter is null.")

    # Returns parameters from an array.
    @staticmethod
    def parseItems(messageItems):
        method = messageItems[0]
        bodylength = int(messageItems[1])
        # Strips ""\r\n"
        parameter = messageItems[2].strip()
        if len(messageItems) == 3:
            body = None
        else:
            body = messageItems[3]

        return method,bodylength,parameter,body

    # Writes the response/request. The body can be None, for example, in LIST request and ERROR response.
    @staticmethod
    def writeMessage(method,bodylength,parameter,body):
        DFTP.validateValues(method,bodylength,parameter,body)
        print "writeMessage",parameter

        if body is None:
            return "%s %s %s\r\n" % (method, bodylength, parameter)
        else:
            return "%s %s %s\r\n%s" % (method, bodylength, parameter, body)

    # Sends the response/request.
    @staticmethod
    def sendMessage(message,sock):
        sentBytes = 0
        while True:
            sentBytes += sock.send(message[sentBytes:])
            if sentBytes == len(message):
                print "A message sent succesfully."
                break

    # Receives and returns "header" (METHOD BODYLENGTH PARAMETER) from the request/response.
    @staticmethod
    def receiveHeader(sock):
        header = ""
        headerlength = 0
        print "Waiting for a message."
        while True:
            headerdata = sock.recv(1)
            header += headerdata
            if header.find("\r\n") != -1:
                print "Received the message succesfully."
                headerlength = len(header)
                break
        header = header.strip()
        headeritems = header.split(" ")
        print header
        return headeritems

    # Receives and returns body (METHOD BODYLENGTH PARAMETER) from the request/response.
    @staticmethod
    def receiveBody(sock,headeritems):
        method,bodylength,parameter,body = DFTP.parseItems(headeritems)
        body = ""
        buffersize = DFTP.getBufferSize()
        while bodylength != len(body):
            # Adjusting the buffer in order to not get a possible follow up message.
            if buffersize > (bodylength-len(body)):
                buffersize = bodylength-len(body)
            body += sock.recv(buffersize)
        # Downloaded file has to be written to tbe client's storage. Content of the file are not printed, not sensible in the case of large binaries.
        if method == "FILE":
            filename = parameter
            file = open(filename,"wb")
            file.write(body)
            file.close()
            print filename,"downloaded."
        # No point to print a empty body.
        elif body != "":
            print body

    @staticmethod
    def writeTodo(parameter):
        with open("todo.txt","a") as todoFile:
            todoFile.write(parameter)
            todoFile.write("\r\n")

    @staticmethod
    def doneTodo(parameter):
        lines = ""
        with open("todo.txt","r") as todoFile:
            lines = todoFile.readlines()
        with open("todo.txt","w") as todoFile:
            for index,line in enumerate(lines):
                if index != (int(parameter) -1):
                    todoFile.write(line)


    # OS folder navigation and listing of the files. parameter = None means the default folder.
    @staticmethod
    def listFiles(basedir,parameter):
        if parameter == None:
            files = os.listdir(basedir)
        else:
            files = os.listdir(basedir + parameter)
        # Populates the body with names of the files. Doesn't add "\r\n" suffix to the last file name.
        body = ""
        for x in range(0,len(files)):
            if x != len(files)-1:
                body += files[x] + "\r\n"
            else:
                body += files[x]
        return body,len(files)

    @staticmethod
    def listTodo():
        body = ""
        i = 1
        with open("todo.txt") as todoFile:
            for line in todoFile:
                prefix = "%d) " % i
                i += 1
                body += prefix + line

        return body,len(body)

    # OS folder navigation and reading a specific file's data for the FILE response.
    @staticmethod
    def downloadFile(basedir,parameter):
        # Splitting in order to get the file name and path.
        parameterItems = parameter.split("/")
        numOfItems = len(parameterItems)
        filename = parameterItems[numOfItems-1]
        path = parameter[:(len(parameter)-len(filename))]
        # Opening, reading and closing the file.
        folder = basedir + path
        folderAndfile = folder + filename
        file = open(folderAndfile)
        data = file.read()
        file.close()
        return filename,data

    # Valid methods.
    @staticmethod
    def getValidMethods():
        return ["LIST","LISTRESPONSE","DOWNLOAD","FILE","ERROR","ADD","OK","DONE"]

    # Socket's default buffersize for sending and receiving. Feel free to adjust.
    @staticmethod
    def getBufferSize():
        return 1024
