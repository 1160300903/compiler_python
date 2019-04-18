from collections import namedtuple
class Input():
    def __init__(self, source):
        self.i = 0
        self.begin = 0
        self.source = source
        self.legal_char = set()
        self.row = 1
        self.column = 0
        with open("alphabet.txt","r") as letter:
            for a in letter.readline().split():
                self.legal_char.add(a)

    def get_char(self,move_begin = False):
        if self.i>=len(self.source):
            return ""
        self.i += 1
        if self.source[self.i-1]=="\n":
            self.row += 1
            self.column = 0
        else:
            self.column += 1
        if(move_begin):
            self.begin += 1#此时读入一个废字符，i和begin都加一
        return self.source[self.i-1]
    def move_begin(self):
        self.begin += 1
    def retract(self):
        self.i -= 1
        if self.source[self.i]=="\n":
            self.row -= 1
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
Keydict = {a[1]:a[0] for a in enumerate(["do","if","else","int","boolean","float","while","struct"],start = 5)}
booldict = {"true":1,"false":0}#存储属性值不是种别码
Optiondict = {a[1]:a[0] for a in enumerate(["+","-","*","/",">","<",">=","<=","==","!=","&&","||","!"],start = 5+len(Keydict))}
Boundarydict = {a[1]:a[0] for a in enumerate(["(",")","{","}","[","]",";","=",","],start = 5+len(Keydict)+len(Optiondict))}
class SymbolItem(namedtuple("SymbolItem","name type offset")):
    pass
class SymbolTable():
    def __init__(self):
        self.table = []
    def add(self, token):
        self.table.append(SymbolItem(token,None,None))#名字，属性，offset
        return len(self.table)-1
    def search(self, token):
        for i in range(len(self.table)):
            if self.table[i].name == token:
                return i
        return -1
    def showTable(self):
        print("符号表")
        for i in range(len(self.table)):
            print("标识符:%s\t类型:%s\t偏移值:%s"%self.table[i])
        with open("符号表.txt","w") as st:
            for i in range(len(self.table)):
                st.write("标识符:%s\t类型:%s\t偏移值:%s\n"%self.table[i])
si = SymbolTable()

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
            if not char.isdigit():
                print("error: %drow,%dcolumn,%s"%(input.row,input.column,"小数点后有错误"))
                input.retract()
                return (None,None,None)
            while char.isdigit():
                char = input.get_char()
        if char =="e":
            char = input.get_char()
            isInt = False
            if char =="+" or char =="-":
                char = input.get_char()
                if not char.isdigit():
                    print("error: %drow,%dcolumn,%s"%(input.row,input.column,"科学计数法有错误"))
                    input.retract()
                    return (None,None,None)
            elif not char.isdigit():
                print("error: %drow,%dcolumn,%s"%(input.row,input.column,"科学计数法有错误"))
                input.retract()
                return (None,None,None)
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
            print("error: %drow,%dcolumn,%s"%(input.row,input.column,"缺少一个&"))
            input.retract()
            return (None,None,None)
    elif char == "|":
        char = input.get_char()
        if char == "|":
            return ("||", Optiondict["||"],0)
        else:
            print("error: %drow,%dcolumn,%s"%(input.row,input.column,"缺少一个|"))
            input.retract()
            return (None,None,None)
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
                if char == "":
                    print("error: %drow,%dcolumn,%s"%(input.row,input.column,"注释不封闭")) 
                    return "",None,None
                while char == "*":
                    char = input.get_char()
                    if char == "":
                        print("error: %drow,%dcolumn,%s"%(input.row,input.column,"注释不封闭")) 
                        return "",None,None
                    if char == "/":#测试用例 **/
                        return  (None,None,None)        
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
    elif char == "":
        return "",None,None
    else:
        print("error: %drow,%dcolumn,%s"%(input.row,input.column,"非法字符")) 
        return None,None,None
if __name__ == "__main__":
    with open("种别码表.txt","w") as typeFile:
        typeFile.write("字符串\t种别码\t属性值\n")
        typeFile.write("标识符\t1\t符号表地址\n")  
        typeFile.write("整数\t2\t整数数值\n") 
        typeFile.write("浮点数\t3\t浮点数值\n") 
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
    file2 = open("token.txt","w")
    while(True):
        token, type_code,attribute = token_scan(input)
        input.reset_begin()
        if token == None:
            continue
        elif token == "":
            break
        file2.write(token + "\t\t" +"<"+str(type_code)+"\t, "+str(attribute)+" >\n")
    si.showTable()
    file1.close()
    file2.close()