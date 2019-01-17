class Calc:
    def __init__(self):
      while(True):
        op = raw_input("enter operation (sum,sub,mul,div): ")
        arg1 = self.args()
        arg2 = self.args()
        res = self.calculate(op,arg1,arg2)
        self.printRes(op,res)

    def args(self):
        try:
            arg = float(raw_input("enter a number: "))
        except ValueError:
            print "not a number"
            arg = self.args()
        return arg

    def calculate(self,op,arg1,arg2):
      if op == "sum":
        return self.sum(arg1,arg2)
      elif op == "sub":
        return self.sub(arg1,arg2)
      elif op == "mul":
        return self.mul(arg1,arg2)
      elif op == "div":
        return self.div(arg1,arg2)

    def sum(self,arg1,arg2):
        return arg1 + arg2
    def sub(self,arg1,arg2):
        return arg1 - arg2
    def mul(self,arg1,arg2):
        return arg1 * arg2
    def div(self,arg1,arg2):
        return arg1 / arg2

    def printRes(self,op,res):
        print op , " result: " , res

#init
try:
    calc = Calc()
except KeyboardInterrupt:
    print "exiting"

''' example output
enter operation (sum,sub,mul,div): sum
enter a number: 3
enter a number: 5
sum  result:  8.0
enter operation (sum,sub,mul,div): 
exiting
>>> 
'''
