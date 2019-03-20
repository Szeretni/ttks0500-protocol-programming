class Functions:
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
    def writeMessage(method, bodylenght, parameters,body):
        if method not in Functions.getValidMethods():
            raise NameError("Invalid method.")
        try:
            if int(bodylenght) < 0:
                raise TypeError("Invalid body lenght.")
        except ValueError as ex:
            print "Body lenght is not a number."
            raise ex
        if parameters is None:
            raise AssertionError("Error, parameter is null.")

        return "%s %s %s\r\n%s" %(method, bodylenght, parameters, body)

    @staticmethod
    def getValidMethods():
        return ["LIST","LISTRESPONSE","DOWNLOAD","FILE","ERROR"]
