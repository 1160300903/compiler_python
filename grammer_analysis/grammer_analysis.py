from collections import namedtuple
class Expression(namedtuple("Expression","leftside rightside")):
    pass
class grammer_parse():
    def __init__(self):
        self.terminators = set()
        self.variable = set()
        self.expression = []
        self.first_dict = {}
        with open("grammar.txt","r") as g:
            g.readline()
            state = 1
            for line in g.readlines():
                if line == "Variable":
                    state = 2
                    break
                if line == "Expression":
                    state = 3
                    break
                if state == 1:
                    for t in line.split():
                        self.terminators.add(t)
                elif state == 2:
                    self.variable.add(line.split("#")[0])
                elif state == 3:
                    temp_variable,right_side = line.split("::=")
                    self.expression.append(Expression(temp_variable,right_side.split()))
    def first_set_for_char(self):
        for char in self.terminators:
            self.first_dict[char] = set([char])
        for char in self.variable:
            self.first_dict[char] = set()
        while True:
            stable = True
            for e in self.expression:
                for i in range(len(e.rightside)):
                    if e.rightside[i] in self.variable:
                        if len((self.first_dict[e.rightside[i]]-set(["ε"]))-self.first_dict[e.leftside])>0:
                            self.first_dict[e.leftside] = self.first_dict[e.leftside] | (self.first_dict[e.rightside[i]]-set(["ε"]))
                            stable = False
                    elif e.rightside[i] in self.terminators and e.rightside[i] not in self.first_dict[e.leftside]:
                        self.first_dict[e.leftside].add(e.rightside[i])
                        stable =False
                    if i == len(e.rightside)-1 and "ε" in self.first_dict[e.rightside[i]] and "ε" not in self.first_dict[e.leftside]:
                        self.first_dict[e.leftside].add("ε")
                        stable = False
                    if "ε" not in self.first_dict[e.rightside[i]]:
                        break
            if stable:
                break
                        
        
    def first_set_for_string(self,char):
        pass
    

