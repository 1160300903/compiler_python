from collections import namedtuple
class Input():
    def __init__(self, source):
        self.i = 0
        self.begin = 0
        self.source = source
    def get_char(self,move_begin = False):
        if self.i>=len(self.source):
            exit(0)
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
    def isEnd(self):
        if self.begin >= len(source):
            return True
        return False
#标识符 1
#无符号整数 2
#无符号浮点数 3
#布尔常数 4
Keydict = {a[1]:a[0] for a in enumerate(["do","if","else","int","boolean","float","while"],start = 5)}
booldict = {"true":1,"false":0}#存储属性值不是种别码
Optiondict = {a[1]:a[0] for a in enumerate(["+","-","*","/","**","++",">","<",">=","<=","==","!=","&&","||","!"],start = 5+len(Keydict))}
Boundarydict = {a[1]:a[0] for a in enumerate(["(",")","{","}","[","]",";",",","="],start = 5+len(Keydict)+len(Optiondict))}
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
def token_scan(input):
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
            return token, Keydict[token],0
        if token in booldict:
            return token, 4,booldict[token]
        location = si.search(token)
        if location == -1:
            return token, 1, si.add(token)
        else:
            return token, 1, location
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
            return (token, 2, int(token))
        if not isInt:
            return (token, 3,float(token))
    elif char == "*":
        char = input.get_char()
        if char == "*":
            return ("**", Optiondict["**"], 0)
        else:
            input.retract()
            return ("*", Optiondict["*"], 0)
    elif char == "=":
        char = input.get_char()
        if char =="=":
            return ("==", Optiondict["=="], 0) 
        else:
            input.retract()
            return ("=", Boundarydict["="], 0)
    elif char == "<":
        char = input.get_char()
        if char == "=":
            return ("<=", Optiondict["<="], 0)
        else:
            input.retract()
            return ("<", Optiondict["<"],0)
    elif char == ">":
        char = input.get_char()
        if char == "=":
            return (">=", Optiondict[">="],0)
        else:
            input.retract()
            return (">", Optiondict[">"],0)
    elif char == "!":
        char = input.get_char()
        if char == "=":
            return ("!=", Optiondict["!="],0)
        else:
            input.retract()
            return ("!", Optiondict["!"],0)
    elif char == "&":
        char = input.get_char()
        if char == "&":
            return ("&&", Optiondict["&&"],0)
        else:
            error_handle()
            return None
    elif char == "|":
        char = input.get_char()
        if char == "|":
            return ("||", Optiondict["||"],0)
        else:
            error_handle()
            return None
    elif char == "+":
        char = input.get_char()
        if char == "+":
            return ("++",Optiondict["++"],0)
        else:
            input.retract()
            return ("+", Optiondict["+"],0)
    elif char == "-":
        return ("-", Optiondict["-"],0)
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
            return ("/", Optiondict["/"],0)
    elif char == "(":
        return ("(", Boundarydict["("],0)
    elif char == ")":
        return (")", Boundarydict[")"],0)
    elif char == "{":
        return ("{", Boundarydict["{"],0)
    elif char == "}":
        return ("}", Boundarydict["}"],0)
    elif char == "[":
        return ("[", Boundarydict["["],0)
    elif char == "]":
        return ("]", Boundarydict["]"],0)
    elif char == ";":
        return (";", Boundarydict[";"],0)
    elif char == ",":
        return (",", Boundarydict[","],0)
    else:
        error_handle()   
if __name__ == "__main__":
    with open("属性表.txt","w") as typeFile:
        typeFile.write("字符串\t种别码\t属性值\n")
        typeFile.write("标识符\t1\t不定\n")  
        typeFile.write("整数\t2\t不定\n") 
        typeFile.write("浮点数\t3\t不定\n") 
        typeFile.write("true\t4\t1\n") 
        typeFile.write("false\t4\t0\n") 
        for key in Keydict:
            typeFile.write(key+"\t"+str(Keydict[key])+"\t0\n")
        for key in Optiondict:
            typeFile.write(key+"\t"+str(Optiondict[key])+"\t0\n")
        for key in Boundarydict:
            typeFile.write(key+"\t"+str(Boundarydict[key])+"\t0\n")

    file1 = open("test.txt","r")
    source = file1.read()
    input = Input(source)
    while(True):
        token, type_code,attribute = token_scan(input)
        input.reset_begin()
        print(token + "\t\t" +"<"+str(type_code)+"\t, "+str(attribute)+" >")


            
        