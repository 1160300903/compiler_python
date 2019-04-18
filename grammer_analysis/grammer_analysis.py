from collections import namedtuple
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
class grammer_parse():
    def __init__(self):
        self.terminators = set()
        self.variable = set()
        self.null_symbol = set("ε")
        self.expression = []
        self.first_dict = {}
        self.all_clourse = []
        self.map_of_clourses = {}
        self.action = []
        self.goto = []
        self.symbol_stack = None
        self.state_stack = None
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
                        
        
    def first_set_for_string(self,string):
        first = set()
        for i in range(len(string)):
            item = string[i]
            first = first | (self.first_dict[item]-set("ε"))
            if i == len(string)-1 and "ε" in self.first_dict[item]:
                first.add("ε")
            if "ε" not in self.first_dict[item]:
                break
        return first
    def get_clourse(self,I):
        clourse_set = set(I)
        while True:
            stable = True
            for item in clourse_set:
                if item.experssion[item.loc_of_point] in self.variable:
                    for e in self.expression:
                        if e.leftside == item.experssion[item.loc_of_point]:
                            for c in self.first_set_for_string(item.experssion[item.loc_of_point+1:].append(item.ex_symbol)):
                                new_item = Item(e.leftside,e.rightside,0,c)
                                if new_item not in clourse_set:
                                    clourse_set.add(new_item)
                                    stable = False
                            item.experssion.pop()
            if stable:
                break
        return clourse_set
    def Go(self,I,X):
        successive_item_set = set()
        for item in I:
            if item.experssion[item.loc_of_point] == X:
                successive_item_set.add(Item(item.rightside,item.leftside,item.loc_of_point+1,item.ex_symbol))
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
            self.map_of_clourses[i] = {}
            for x in (self.terminators | self.variable - set("ε")):
                next = self.Go(current,x)
                if next != set() and next not in self.all_clourse:
                    queue.enqueue(next)
                    i+=1
                    self.map_of_clourses[current_index][x] = i   
    def find_expression(self,item):
        for i in range(len(self.expression)):
            e = self.expression[i]
            if e.rightside == item.rightside and e.leftside == item.leftside:
                return i
        return -1
    def get_table(self):
        self.action = [{}]*len(self.all_clourse)
        self.goto = [{}]*len(self.all_clourse)
        for i in range(len(self.all_clourse)):
            for char in self.map_of_clourses[i]:
                if char in self.terminators:
                    self.action[char] = self.map_of_clourses[i][char]
                elif char in self.variable:
                    self.goto[char] = self.map_of_clourses[i][char]
            for item in self.all_clourse[i]:
                if item.loc_of_point == len(item.rightside):
                    index = self.find_expression(item)
                    if index==0 and item.ex_symbol == "#":
                        self.action[i]["#"] = "acc"
                    else:
                        self.action[i][item.ex_symbol] = "r"+index
    def parser(self,string):
        self.symbol_stack = Stack()
        self.state_stack = Stack()
        self.symbol_stack.push("#")
        self.state_stack.push(0)
        temp_string = string+"#"
        index = 0
        try:
            while True:
                top_state = self.state_stack.get_top()
                char = temp_string[index]
                command = self.action[top_state][char]
                if command.isdigit():
                    self.state_stack.push(command)
                    self.symbol_stack.push(char)
                    index+=1
                elif command.isalpha():
                    print("接受")
                    break
                else:
                    e = self.expression[int(command[1:])]
                    self.state_stack.pop(len(e.rightside))
                    self.symbol_stack.pop(len(e.rightside))
                    self.symbol_stack.push(e.leftside)
                    top_state = self.state_stack.get_top()
                    self.state_stack.push(self.goto[top_state][e.leftside])
        except KeyError as e:
            print("错误")
            
                    
                        




