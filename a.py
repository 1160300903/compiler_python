from collections import namedtuple
class Input():
    def __init__(self, source):
        self.i = 0
        self.begin = 0
        self.source = source
    def get_char(self,move_begin = False):
            self.i += 1
            return self.source[self.i-1]
    def move_begin(self):
        self.begin += 1
    def retract(self):
        self.i -= 1
    def copy_token(self):
        result = self.source[self.begin:self.i]
        self.begin = self.i
        return result
    def reset_begin(self):
        self.begin = self.i
#表示符 1
#无符号整数 2
#无符号浮点数 3
#布尔常数 4
Keydict = {"do":5,"if":6,"else":7,"int":8
,"boolean":9,"float":10,"while":11}
booldict = {"true":1,"false":0}#存储属性值不是种别码
Optiondict = {"+":12,"-":13,"*":14,"/":15,"**":16,">":17,"<":18,">=":19,
                "<=":20,"==":21,"!=":22,"&&":23,"||":24,"!":25}
Boundarydict = {"(":26,")":27,"{":28,"}":29,"[":30,"]":31,";":32,",":32,"=":34}
class SymbolItem(namedtuple("SymbolItem","name type value")):
    pass
class SymbolTable():
    def __init__(self):
        self.table = []
    def add(self, token):
        self.table.append(SymbolItem(token,None,None))#名字，属性，值
        return len(self.table)-1
    def search(self, token):
        for i in range(len(self.table)):
            if self.table[i].name == token:
                return i
        return -1
si = SymbolTable()
def error_handle():
    pass#TODO
def token_scan(path):
    file1 = open(path,"r")
    source = file1.read()
    input = Input(source)
    char = input.get_char()
    while char ==" " or char == "\t" or char == "\n":
        char = input.get_char(True)
    if char.isalpha() or char == "_":
        char = input.get_char()
        while char.isalnum() or char =="_":
            char = input.get_char()
        input.retract()
        token = input.copy_token()
        if token in Keydict:
            return Keydict[token],0
        if token in booldict:
            return 4,booldict[token]
        location = si.search(token)
        if location == -1:
            return 1, si.add(token)
        else:
            return 1, location
    elif char.isdigit():
        isInt = True
        char = input.get_char()
        while char.isdigit():
            char = input.get_char()
        if char == ".":
            char = input.get_char()
            isInt = False
            while char.isdigit():
                char = input.get_char()
        input.retract()
        token = input.copy_token()
        if isInt:
            return (2, int(token))
        if not isInt:
            return (3,float(token))
    elif char == "*":
        char = input.get_char()
        if char == "*":
            return (Optiondict["**"], 0)
        else:
            input.retract()
            return (Optiondict["*"], 0)
    elif char == "=":
        char = input.get_char()
        if char =="=":
            return (Optiondict["=="], 0) 
        else:
            input.retract()
            return (Optiondict["="], 0)
    elif char == "<":
        char = input.get_char()
        if char == "=":
            return (Optiondict["<="], 0)
        else:
            input.retract()
            return (Optiondict["<"],0)
    elif char == ">":
        char = input.get_char()
        if char == "=":
            return (Optiondict[">="],0)
        else:
            input.retract()
            return (Optiondict[">"],0)
    elif char == "!":
        char = input.get_char()
        if char == "=":
            return (Optiondict["!="],0)
        else:
            input.retract()
            return (Optiondict["!"],0)
    elif char == "&":
        char = input.get_char()
        if char == "&":
            return (Optiondict["&&"],0)
        else:
            error_handle()
            return None
    elif char == "|":
        char = input.get_char()
        if char == "|":
            return (Optiondict["||"],0)
        else:
            error_handle()
            return None
    elif char == "+":
        return (Optiondict["+"],0)
    elif char == "-":
        return (Optiondict["-"],0)
    elif char == "/":
        char = input.get_char()
        if char == "*":
            while True:
                char = input.get_char()
                while char == "*":
                    char = input.get_char()
                    if char == "/":#测试用例 **/
                        return  None         
        else:
            return (Optiondict["/"],0)
    elif char == "(":
        return (Boundarydict["("],0)
    elif char == ")":
        return (Boundarydict[")"],0)
    elif char == "{":
        return (Boundarydict["{"],0)
    elif char == "}":
        return (Boundarydict["}"],0)
    elif char == "[":
        return (Boundarydict["["],0)
    elif char == "]":
        return (Boundarydict["]"],0)
    elif char == ";":
        return (Boundarydict[";"],0)
    elif char == ",":
        return (Boundarydict[","],0)
    else:
        error_handle()   
            
        