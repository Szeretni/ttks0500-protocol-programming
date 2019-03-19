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
        if bodylenght <= 0:
            raise ValueError("Invalid body lengt.")

    @staticmethod
    def getValidMethods():
        return ["LIST","LISTRESPONSE","DOWNLOAD","FILE","ERROR"]
