from collections import namedtuple
from lexical_analysis import lexical_parse
class Expression(namedtuple("Expression","leftside rightside")):
    pass
class Item(namedtuple("Item","leftside rightside loc_of_point ex_symbol")):
    pass
class Queue():
    def __init__(self):
        self.array = []
    def dequeue(self):
        return self.array.pop(0)
    def enqueue(self,a):
        self.array.append(a)
    def is_empty(self):
        if len(self.array) == 0:
            return True
        return False
    def In(self,a):
        if a in self.array:
            return True
        return False
    def index(self,a):
        return self.array.index(a)
class Stack():
    def __init__(self):
        self.array = []
    def push(self,a):
        self.array.append(a)
    def pop(self,n):
        for i in range(n):
            self.array.pop()
    def get_top(self):
        return self.array[-1]
    def is_empty(self):
        if len(self.array) == 0:
            return True
        return False
    def show_stack(self):
        if self.is_empty():
            return ""
        else:
            string = str(self.array[0])
            for i in range(1,len(self.array)):
                string += str(self.array[i])
            return string
class grammer_parser():
    def __init__(self,path):
        self.terminators = set()
        self.variable = set()
        self.null_symbol = set("ε")
        self.expression = []
        self.first_dict = {}
        self.all_clourse = []
        self.map_of_clourses = {}
        self.action = []
        self.goto = []
        self.follow_dict = {}
        self.symbol_stack = None
        self.state_stack = None
        self.type_code = None
        self.token_list = None
        with open(path,"r") as g:
            g.readline()
            state = 1
            for line in g.readlines():
                line = line.strip()
                if line == "Variable":
                    state = 2
                    continue
                if line == "Expression":
                    state = 3
                    continue
                if state == 1:
                    for t in line.split():
                        assert t not in self.terminators
                        self.terminators.add(t)
                elif state == 2:
                    assert line.split("#")[0] not in self.variable
                    self.variable.add(line.split("#")[0])
                elif state == 3:
                    if line=="":
                        continue
                    temp_variable,right_side = line.split("::=")
                    for a in right_side.split():
                        assert a in self.terminators or a in self.variable or a == "ε"
                    assert temp_variable in self.variable
                    if right_side=="ε":
                        self.expression.append(Expression(temp_variable,tuple()))
                    else:
                        self.expression.append(Expression(temp_variable,tuple(right_side.split())))
        self.first_set_for_char()
        self.get_all_clourse()
        self.get_table()
        self.get_follow()
    def get_follow(self):
        for a in self.variable:
            self.follow_dict[a] = set()
        self.follow_dict["start"] = set(["#"])
        while True:
            stable = True
            for e in self.expression:
                for i in range(len(e.rightside)):
                    char = e.rightside[i]
                    if char in self.variable:
                        if i == len(e.rightside)-1 and char!=e.leftside and (self.follow_dict[e.leftside]-self.follow_dict[char])!=set():
                            self.follow_dict[char] = self.follow_dict[char] | self.follow_dict[e.leftside]
                            stable = False
                        elif i!= len(e.rightside)-1:
                            first_beta = self.first_set_for_string(e.rightside[i+1:])
                            if ((first_beta - set(["ε"]))- self.follow_dict[char]) != set():
                                self.follow_dict[char] = self.follow_dict[char] | (first_beta-set(["ε"]))
                                stable = False
                            if "ε" in first_beta and char!= e.leftside and (self.follow_dict[e.leftside]-self.follow_dict[char])!=set():
                                self.follow_dict[char] = self.follow_dict[char] | self.follow_dict[e.leftside]
                                stable = False
            if stable:
                break
        for v in self.follow_dict:
            assert "ε" not in self.follow_dict[v]
    def first_set_for_char(self):
        for char in self.terminators:
            self.first_dict[char] = set([char])
        for char in self.variable:
            self.first_dict[char] = set()
        while True:
            stable = True
            for e in self.expression:
                if len(e.rightside)==0 and "ε" not in self.first_dict[e.leftside]:
                        self.first_dict[e.leftside].add("ε")
                        stable = False
                else:
                    for i in range(len(e.rightside)):
                        if e.rightside[i] in self.variable:
                            if len((self.first_dict[e.rightside[i]]-set(["ε"]))-self.first_dict[e.leftside])>0:
                                self.first_dict[e.leftside] = self.first_dict[e.leftside] | (self.first_dict[e.rightside[i]]-set(["ε"]))
                                stable = False
                        elif e.rightside[i] in self.terminators and e.rightside[i] not in self.first_dict[e.leftside]:
                            self.first_dict[e.leftside].add(e.rightside[i])
                            stable = False
                        if i == len(e.rightside)-1 and "ε" in self.first_dict[e.rightside[i]] and "ε" not in self.first_dict[e.leftside]:
                            self.first_dict[e.leftside].add("ε")
                            stable = False
                        if "ε" not in self.first_dict[e.rightside[i]]:
                            break
            if stable:
                break
                        
    def first_set_for_string(self,string):
        first = set()
        if string == ["ε"] or string == []:
            first.add("ε")
            return first
        else:
            for i in range(len(string)):
                item = string[i]
                first = first | (self.first_dict[item]-set("ε"))
                if i == len(string)-1 and "ε" in self.first_dict[item]:
                    first.add("ε")
                if "ε" not in self.first_dict[item]:
                    break
            return first
    def is_not_specified(self,item):
        if item.loc_of_point >= len(item.rightside):
            return False
        return True
    def get_clourse(self,I):
        clourse_set = set(I)
        while True:
            temp_set = set()
            for item in clourse_set:
                if self.is_not_specified(item) and item.rightside[item.loc_of_point] in self.variable:
                    all_char = self.first_set_for_string(item.rightside[item.loc_of_point+1:]+(item.ex_symbol,))
                    for e in self.expression:
                        if e.leftside == item.rightside[item.loc_of_point]:
                            for c in all_char:
                                new_item = Item(e.leftside,e.rightside,0,c)
                                if new_item not in clourse_set:
                                    temp_set.add(new_item)
            if temp_set:
                clourse_set = clourse_set | temp_set
            else:
                break
        return clourse_set
    def Go(self,I,X):
        assert X != "ε"
        successive_item_set = set()
        for item in I:
            if self.is_not_specified(item) and item.rightside[item.loc_of_point] == X:
                successive_item_set.add(Item(item.leftside,item.rightside,item.loc_of_point+1,item.ex_symbol))
        return self.get_clourse(successive_item_set)
    def get_all_clourse(self):
        queue = Queue()
        all_clourse = self.all_clourse
        queue.enqueue(self.get_clourse([Item(self.expression[0].leftside,self.expression[0].rightside,0,"#")]))
        i = 0
        while not queue.is_empty():
            current = queue.dequeue()
            all_clourse.append(current)
            current_index = len(all_clourse)-1
            self.map_of_clourses[current_index] = {}
            for x in sorted(list(self.terminators | self.variable)):
                next = self.Go(current,x)
                if next != set() and next not in self.all_clourse and not queue.In(next):#next不为空，并且不在队列中，也不在all_clourse中
                    queue.enqueue(next)
                    i+=1
                if next in self.all_clourse:
                    self.map_of_clourses[current_index][x] = self.all_clourse.index(next) 
                elif queue.In(next):
                    self.map_of_clourses[current_index][x] = len(self.all_clourse)+queue.index(next)
    def find_expression(self,item):
        for i in range(len(self.expression)):
            e = self.expression[i]
            if e.rightside == item.rightside and e.leftside == item.leftside:
                return i
        return -1
    def get_table(self):
        self.action = []
        self.goto = []
        for i in range(len(self.all_clourse)):
            self.action.append({})
            self.goto.append({})
        for i in range(len(self.all_clourse)):
            for char in self.map_of_clourses[i]:
                if char in self.terminators:
                    self.action[i][char] = self.map_of_clourses[i][char]
                elif char in self.variable:
                    self.goto[i][char] = self.map_of_clourses[i][char]
            for item in self.all_clourse[i]:
                if item.loc_of_point == len(item.rightside):
                    index = self.find_expression(item)
                    if index==0 and item.ex_symbol == "#":
                        assert "#" not in self.action[i]
                        self.action[i]["#"] = "acc"
                    else:
                        assert item.ex_symbol not in self.action[i] 
                        self.action[i][item.ex_symbol] = "r"+str(index)
    def grammar_parse(self,verbose=True):
        self.symbol_stack = Stack()
        self.state_stack = Stack()
        self.symbol_stack.push("#")
        self.state_stack.push(0)
        expression_file = open("规约过程.txt","w")
        index = 0
        while True:
            try:
                top_state = self.state_stack.get_top()
                char = self.token_list[index]
                command = self.action[top_state][char]
                if isinstance(command,int):#读入动作
                    self.state_stack.push(command)
                    self.symbol_stack.push(char)
                    index+=1
                elif command=="acc":#接受动作
                    break
                else:#规约动作
                    e = self.expression[int(command[1:])]
                    self.state_stack.pop(len(e.rightside))
                    self.symbol_stack.pop(len(e.rightside))
                    self.symbol_stack.push(e.leftside)
                    if verbose:
                        expression_file.write(e.leftside+"::="+"".join(e.rightside)+"\n")
                    top_state = self.state_stack.get_top()
                    self.state_stack.push(self.goto[top_state][e.leftside])
                #print(self.symbol_stack.array)#打印符号栈
            except KeyError as e:
                while True:
                    top_state = self.state_stack.get_top()
                    if "P" in self.goto[top_state]:
                        break
                    self.state_stack.pop(1)
                    self.symbol_stack.pop(1)
                state = self.goto[top_state]["P"]#压入栈的状态
                self.state_stack.push(state)
                self.symbol_stack.push("P")
                while True:
                    char = self.token_list[index]
                    if char not in self.follow_dict["P"]:
                        index += 1
                        if index>=len(self.token_list):
                            index=len(self.token_list)-1
                            break
                    else:
                        break
                print("Error at Line ["+str(self.type_code[index][2])+"]：[the error is near "+self.init_token_list[index]+"]")
    def show_table(self,verbose=False):
        sorted_terminators = sorted(list(self.terminators))
        sorted_variable = sorted(list(self.variable))
        with open("LR(1)分析表.txt","w") as l:
            if verbose:
                """for i in range(len(self.all_clourse)):
                    sorted_expression = sorted(list(self.all_clourse[i]))
                    for item in sorted_expression:
                        temp_list = list(item.rightside)
                        temp_list.insert(item.loc_of_point,".")
                        print(item.leftside+"::="+"".join(temp_list)+"\t"+item.ex_symbol)"""
                l.write("\t\t"+"\t\t".join(sorted_terminators)+"\t\t"+"\t\t".join(sorted_variable)+"\n")
                for i in range(len(self.all_clourse)):
                    l.write(str(i)+"\t\t")
                    for char in sorted_terminators:
                        if char in self.action[i]:
                            l.write(str(self.action[i][char])+"\t\t")
                        else:
                            l.write("\t\t")
                    for char in sorted_variable:
                        if char in self.goto[i]:
                            l.write(str(self.goto[i][char])+"\t\t")
                        else:
                            l.write("\t\t")
                    l.write("\n")
            l.write("状态数"+str(len(self.all_clourse)))
    def read_tokens(self):
        self.type_code = []
        self.token_list = []
        self.init_token_list = []
        name_map = {"1":"id","2":"CI","3":"CF","5":"CS"}
        with open("token.txt","r") as t:
            lines = t.readlines()
            for line in lines:
                token,type_code = line.strip().split()
                type_code = tuple(type_code[1:len(type_code)-1].split(","))
                if type_code[0] in name_map:
                    self.token_list.append(name_map[type_code[0]])
                else:
                    self.token_list.append(token)
                self.init_token_list.append(token)
                self.type_code.append(type_code)
        self.token_list.append("#")
        self.init_token_list.append("end of the codes")
        self.type_code.append((None,None,self.type_code[-1][2]))
if __name__ == "__main__":
    lexical_parse()
    g = grammer_parser("grammar.txt")
    g.show_table(True)#在文件中打印符号表。现在已经打印过了，所以注释掉了
    g.read_tokens()
    g.grammar_parse()