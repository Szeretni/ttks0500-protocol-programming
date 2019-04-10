import os

class TODO:
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
        # Parameter may have multiple parts such as: "ADD 0 eat veggies7"
        # Where "eat veggies7" is the parameter.
        # At this point requestItems is a list ['ADD', '0', 'eat', 'veggies7']
        # Here the list is manipulated in order to force it to a list with three elems.
        # Because this way no refactoring is required elsewhere.
        numItems = len(requestItems)
        thirdItem = ""
        for x in range(2,numItems):
            thirdItem += requestItems[x] + " "
        for x in range(2,numItems):
            requestItems.pop()
        requestItems.append(thirdItem)

        if len(requestItems) != 3:
            raise ValueError("The request is invalid. Example request: LIST 0 .")

        method,bodylength,parameter,body = TODO.parseItems(requestItems)
        TODO.validateValues(method,bodylength,parameter,body)

        return method,bodylength,parameter,body

    # Runs checks to the values provided by the user.
    @staticmethod
    def validateValues(method,bodylength,parameter,body):
        if method not in TODO.getValidMethods():
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
        TODO.validateValues(method,bodylength,parameter,body)

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
        method,bodylength,parameter,body = TODO.parseItems(headeritems)
        body = ""
        buffersize = TODO.getBufferSize()
        while bodylength != len(body):
            # Adjusting the buffer in order to not get a possible follow up message.
            if buffersize > (bodylength-len(body)):
                buffersize = bodylength-len(body)
            body += sock.recv(buffersize)
        print body

    # Adds a new todo item to the todo file. Parameter is the todo item such as "eat veggies".
    @staticmethod
    def writeTodo(parameter):
        with open("todo.txt","a") as todoFile:
            todoFile.write(parameter)
            todoFile.write("\r\n")

    # Removes a done task from the todo file. Parameter is an index number of a line.
    @staticmethod
    def doneTodo(parameter):
        lines = ""
        with open("todo.txt","r") as todoFile:
            lines = todoFile.readlines()
        with open("todo.txt","w") as todoFile:
            for index,line in enumerate(lines):
                if index != (int(parameter) -1):
                    todoFile.write(line)

    # Reads contents of the todo file and returns it to the client.
    # The items are numbered and the number is used in DONE requests.
    @staticmethod
    def listTodo():
        body = ""
        i = 1
        with open("todo.txt") as todoFile:
            for line in todoFile:
                prefix = "%d) " % i
                i += 1
                body += prefix + line

        # Returns the todo items in a response body and number of items in the todo file.
        return body,(i-1)

    # Valid methods.
    @staticmethod
    def getValidMethods():
        return ["LIST","LISTRESPONSE","ERROR","ADD","OK","DONE"]

    # Socket's default buffersize for sending and receiving. Feel free to adjust.
    @staticmethod
    def getBufferSize():
        return 1024
