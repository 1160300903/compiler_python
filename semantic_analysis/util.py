from collections import namedtuple
class symbol_item():
    def __init__(self,name,my_type,offset,redundant_point):
        self.name = name
        self.type = my_type
        self.offset = offset
        self.redundant_point = redundant_point
    def show_item(self,end="\n"):
        print("(",self.name,",",self.type,",",self.offset,",",self.redundant_point,")",end=end)
class array_dope_vector():
    def __init__(self,dimension,limits,address,my_type):
        self.dimension = dimension
        self.limits = limits
        self.address = address
        self.type = my_type
    def show_vector(self):
        print("(",self.dimension,",",self.limits,",",self.address,",",self.type,")")
class symbol_table():
    def __init__(self,table):
        self.table = []
        self.offset = 0
        self.father_table = table
    def add(self, symbol_item_instance):
        self.table.append(symbol_item_instance)#名字，属性，offset
        return len(self.table)-1
    def search(self, token):
        current = self
        while current != None:
            for i in range(len(current.table)):
                if current.table[i].name == token:
                    return current.table[i]
            current = current.father_table
        return None
    def set_offset(self,offset):
        self.offset = offset
class code():
    def __init__(self,op,first,second,result):
        self.op = op
        self.first = first
        self.second = second
        self.result = result 
    def toString(self):
        return "("+str(self.op)+","+str(self.first)+","+str(self.second)+","+str(self.result)+")"
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
    def pop(self,n=1):
        result = self.array[-n:]
        for _ in range(n):
            self.array.pop()
        return result
    def get_top(self,n=1):
        return self.array[-n]
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
if __name__ == "__main__":
    print("util")