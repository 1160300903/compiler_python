from grammar_analysis import Stack
from grammar_analysis import Queue
from collections import namedtuple
from grammar_analysis import grammar_parser
#把书上的符号属性修改了的：id.addr改为id.name
class symbol_item(namedtuple("symbol_item","name type offset redundant_point")):
    pass
class array_dope_vector(namedtuple("array_dope_vector","dimension limits address type")):
    pass
class symbol_table():
    def __init__(self,table):
        self.table = []
        self.offset = 0
        self.father_table = table
    def add(self, token):
        self.table.append(symbol_item(token,None,None))#名字，属性，offset
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
class semantic_action():
    def __init__(self,grammar_parser):
        self.offset_stack = Stack()
        self.table_stack = Stack()
        self.offset_stack.push(0)
        init_table = symbol_table(None)
        self.table_stack.push(init_table)
        self.g = grammar_parser
        self.g.init_table = init_table
        self.attribute_stack = grammar_parser.attribute_stack
        self.code_file = open("intermediate_code.txt","w")
        self.temp_count = 0
        self.code_list = []
        self.next_quad = 0
        self.param_queue = Queue()
        self.action_array = [self.semantic_action_0,self.semantic_action_1,self.semantic_action_2,self.semantic_action_3,self.semantic_action_4,self.semantic_action_5
        ,self.semantic_action_6,self.semantic_action_7,self.semantic_action_8,self.semantic_action_9,self.semantic_action_10
        ,self.semantic_action_11,self.semantic_action_12,self.semantic_action_13,self.semantic_action_14,self.semantic_action_15,
        self.semantic_action_16,self.semantic_action_17,self.semantic_action_18,self.semantic_action_19,self.semantic_action_20,
        self.semantic_action_21,self.semantic_action_22,self.semantic_action_23,self.semantic_action_24,self.semantic_action_25,
        self.semantic_action_26,self.semantic_action_27,self.semantic_action_28,self.semantic_action_29,self.semantic_action_30,
        self.semantic_action_31,self.semantic_action_32,self.semantic_action_33,self.semantic_action_34,self.semantic_action_35,
        self.semantic_action_36,self.semantic_action_37,self.semantic_action_38,self.semantic_action_39,self.semantic_action_40,
        self.semantic_action_41,self.semantic_action_42,self.semantic_action_43,self.semantic_action_44,self.semantic_action_45,
        self.semantic_action_46,self.semantic_action_47,self.semantic_action_48,self.semantic_action_49,self.semantic_action_50,
        self.semantic_action_51,self.semantic_action_52,self.semantic_action_53,self.semantic_action_54,self.semantic_action_55,
        self.semantic_action_56,self.semantic_action_57,self.semantic_action_58,self.semantic_action_59,self.semantic_action_60,
        self.semantic_action_61,self.semantic_action_62,self.semantic_action_63,self.semantic_action_64,self.semantic_action_65,
        self.semantic_action_66,self.semantic_action_67,self.semantic_action_68]
    def do_action(self,index):
        self.action_array[index]()
    def new_temp(self):
        result = "$"+str(self.temp_count)
        self.temp_count += 1
        return result
    def gencode(self,op,first,second,result):
        self.code_list.append(code(op,first,second,result))
        self.next_quad += 1
    #{addwidth(top(tblptr),top(offset));
    #在外层过程符号表中加入当前过程
    #pop(tblptr);pop(offset)}
    #D::=def id M1 ( Param ) { W' Z }
    def semantic_action_5(self):
        offset = self.offset_stack.get_top()
        t = self.table_stack.get_top()
        t.set_offset(offset)
        name = self.attribute_stack.get_top(9)["addr"]
        t.father_table.add(symbol_item(name,"fuction",None,t))
        self.table_stack.pop(1)
        self.offset_stack.pop(1)
        return {}
    #Z::=return E ;
    #{if 需要返回结果 then gencode(‘:=’, E.addr, -, F);
    #gencode(‘ret’, -, -, -)}
    def semantic_action_6(self):
        E = self.attribute_stack.get_top(2)
        self.gencode("=",E["addr"],None,"F")
        self.gencode("ret",None,None,None)
        return {}
    #M1::=ε
    def semantic_action_7(self):
        t = symbol_table(self.table_stack.get_top())
        self.table_stack.push(t)
        self.offset_stack.push(0)
        return {}
    #S::=T id ;
    def semantic_action_10(self):
        t = self.table_stack.get_top()
        id_name = self.attribute_stack.get_top(2)["addr"]
        T_type = self.attribute_stack.get_top(3)["type"]
        T_width = self.attribute_stack.get_top(3)["width"]
        offset = self.offset_stack.get_top()
        if "array_dope_vector" in self.attribute_stack.get_top(3):#数组或者正常变量
            redundant_point = self.attribute_stack.get_top(3)["array_dope_vector"]
            if redundant_point != None:
                redundant_point.address = offset
        else:#结构体
            redundant_point = self.attribute_stack.get_top(3)["table"]
        t.add(symbol_item(id_name,T_type,offset,redundant_point))
        self.offset_stack.pop(1)
        self.offset_stack.push(offset+T_width)
        return {}
    #Param::=T id
    def semantic_action_11(self):
        t = self.table_stack.get_top()
        id_name = self.attribute_stack.get_top(1)["addr"]
        T_type = self.attribute_stack.get_top(2)["type"]
        T_width = self.attribute_stack.get_top(2)["width"]
        offset = self.offset_stack.get_top()
        if "array_dope_vector" in self.attribute_stack.get_top(3):#数组或者正常变量
            redundant_point = self.attribute_stack.get_top(3)["array_dope_vector"]
            if redundant_point != None:
                redundant_point.address = offset
        else:#结构体
            redundant_point = self.attribute_stack.get_top(3)["table"]
        t.add(symbol_item(id_name,T_type,offset,redundant_point))
        self.offset_stack.pop(1)
        self.offset_stack.push(offset+T_width)
        return {}
    #Param::=Param , T id
    def semantic_action_12(self):
        t = self.table_stack.get_top()
        id_name = self.attribute_stack.get_top(1)["addr"]
        T_type = self.attribute_stack.get_top(2)["type"]
        T_width = self.attribute_stack.get_top(2)["width"]
        offset = self.offset_stack.get_top()
        if "array_dope_vector" in self.attribute_stack.get_top(3):#数组或者正常变量
            redundant_point = self.attribute_stack.get_top(3)["array_dope_vector"]
            if redundant_point != None:
                redundant_point.address = offset
        else:#结构体
            redundant_point = self.attribute_stack.get_top(3)["table"]
        t.add(symbol_item(id_name,T_type,offset,redundant_point))
        self.offset_stack.pop(1)
        self.offset_stack.push(offset+T_width)
        return {}
    #{T.type := integer; T.width := 4}
    #X::=int
    def semantic_action_16(self):
        X_attribute = {"type":"int","width":4}
        return X_attribute
    #X::=float
    #{T.type :=real; T.width :=8}
    def semantic_action_17(self):
        X_attribute = {"type":"float","width":8}
        return X_attribute
    #X::=boolean
    def semantic_action_18(self):
        X_attribute = {"type":"boolean","width":1}
        return X_attribute
    #X::=char
    def semantic_action_19(self):
        X_attribute = {"type":"char","width":1}
        return X_attribute
    #C::=ε
    def semantic_action_21(self):
        C_attribute = {"array_dope_vector":None}
        return C_attribute
    #C::=[ CI ] C
    def semantic_action_20(self):
        right_C_attribute = self.attribute_stack.get_top(1)
        left_C_attribute = {}
        limit = self.attribute_stack.get_top(3)["value"]
        if right_C_attribute["array_dope_vector"] == None:
            left_C_attribute["array_dope_vector"] = array_dope_vector(1,(limit,),None,None)
        else:
            pre_vector = right_C_attribute["array_dope_vector"]
            left_C_attribute["array_dope_vector"] = array_dope_vector(pre_vector.dimension+1,pre_vector.limits+(limit,),None,None)
        return left_C_attribute
    #T::=X C 生成类型
    #{T.type := array(num.val, T1.type);T.width := num.val×X.width}数组
    #{T.type := X.type ;T.width := X.width}正常变量
    #给符号表准备类型和redunant_point的信息
    def semantic_action_13(self):
        T_attribute = {}
        vector = self.attribute_stack.get_top(1)["array_dope_vector"]
        X_attribute = self.attribute_stack.get_top(2)
        #正常变量
        if vector == None:
            T_attribute["type"] = X_attribute["type"]
            T_attribute["width"] = X_attribute["width"]
            T_attribute["array_dope_vector"] = None
        else:#数组
            T_attribute["type"] = "array"
            total = vector.limits[0]
            for i in range(1,vector.dimension):
                total *= vector.limit[i]
            T_attribute["width"] = total * X_attribute["width"]
            T_attribute["array_dope_vector"] = vector
        return T_attribute
    #T → record M2 D end {T.type := record(top(tblptr));
    #T.width := top(offset);
    #pop(tblptr); pop(offset)}
    #T::=struct { M2 Param } 
    def semantic_action_14(self):
        T_attribute = {}
        T_attribute["type"] = "record"
        T_attribute["width"] = self.offset_stack.get_top(1)
        T_attribute["table"] = self.table_stack.get_top(1)
        self.table_stack.get_top(1).set_offset(self.offset_stack.get_top(1))
        self.offset_stack.pop(1)
        self.table_stack.pop(1)
        return T_attribute

    #M2 →ε{t:= mktable(previous); push(t, tblptr); push(0, offset)}
    def semantic_action_15(self):
        t = symbol_table(self.table_stack.get_top(1))
        self.table_stack.push(t)
        self.offset_stack.push(0)
        return {}
    #{if Left.offset=null then  /*Left是简单变量id*/
    #gencode(Left.addr ':=' E.addr);
    #else
    #gencode(Left.addr '[' Left.offset '] ' ':=' E.addr)} /*Left是数组元素*/
    #S::=Left = E ;
    def semantic_action_24(self):
        left_offset = self.attribute_stack.get_top(4)["offset"]
        left_addr = self.attribute_stack.get_top(4)["addr"]
        E_addr = self.attribute_stack.get_top(2)["addr"]
        if left_offset == None:
            self.gencode("=",str(E_addr),None,str(left_addr))
        else:
            self.gencode("=",str(E_addr),None,str(left_addr)+"["+str(left_offset)+"]")
        return {}
    #S::=Left = B ;
    def semantic_action_25(self):
        left = self.attribute_stack.get_top(4)
        left = self.attribute_stack.get_top(4)
        B = self.attribute_stack.get_top(2)
        if left["offset"] == None:
            result = str(left["addr"])
        else:
            result= str(left["addr"])+"["+str(left["offset"])+"]"
        self.back_patch(B["truelist"],self.next_quad)
        self.back_patch(B["falselist"],self.next_quad+2)
        self.gencode("=","true",None,result)
        self.gencode("goto",None,None,self.next_quad+2)
        self.gencode("=","false",None,result)
        return {}
    #Left::=id
    #{Left.addr:=id.addr; Left.offset:=null}
    def semantic_action_26(self):
        id_addr = self.attribute_stack.get_top(1)["addr"]
        left_attribute = {}
        left_attribute["addr"] = id_addr
        left_attribute["offset"] = None
        return left_attribute
    def width(self,array_type):
        if array_type == "int":
            return "4"
        elif array_type == "float":
            return "8"
        elif array_type == "char" or array_type == "boolean":
            return "1"
    #Left::=L
    #{ Left.addr:=newtemp;        /*Left是数组元素，因此存放基址和位移*/
    #Left.offset:=newtemp;
    #gencode(Left.addr ':=' c(L.array));
    #gencode(Left.offset ':=' L.addr '*' width(L.array))}
    def semantic_action_27(self):
        left_attribute = {}
        left_attribute["addr"] = self.new_temp()
        left_attribute["offset"] = self.new_temp()
        l_array = self.attribute_stack.get_top(1)["array"]
        l_addr = self.attribute_stack.get_top(1)["addr"]
        self.gencode("=",str(l_array.address),None,left_attribute["addr"])
        self.gencode("*",l_addr,self.width(l_array.type),left_attribute["offset"])
        return left_attribute
    #Left::=id . Left 
    #最终推到出的形式为struct.struct.struct.id或者struct.struct.struct.L
    #右部 left 有 addr 和 offset addr存的是结构体的复合名字 offset存的是数组的偏移量
    #Left.addr:=id.name+Left1.addr        /*Left是数组元素，因此存放基址和位移*/
    #Left.offset:=Left1.addr
    def semantic_action_28(self):
        left_attribute = {}
        left_attribute["addr"] = self.attribute_stack.get_top(3)["addr"]+"."+self.attribute_stack.get_top(1)["addr"]
        left_attribute["offset"] = self.attribute_stack.get_top(1)["offset"]
        return left_attribute
    #L::=id [ E ]
    #{L.array:=id.addr; L.addr:= E.addr; L.ndim:=1}
    #array用来存内情向量表
    #数组id的addr为内情向量
    def semantic_action_29(self):
        L_attribute = {}
        id_name = self.attribute_stack.get_top(4)["addr"]
        L_attribute["array"] = self.table_stack.get_top(1).search(id_name).redundant_point
        L_attribute["addr"] = self.attribute_stack.get_top(2)["addr"]
        L_attribute["ndim"] = 1
        return L_attribute
    #{t:=newtemp;
    # m:= L1.ndim+1;
    #gencode(t ':=' L1.addr '*' limit(L1.array, m)); /*计算em-1×nm */
    #gencode(t ':=' t '+' E.addr);                    /* 计算+ im  */
    #L.array:= L1.array;
    #L.addr:=t;
    #L.ndim:=m}
    #L::=L1 [ E ]
    def semantic_action_30(self):
        L_attribute = {}
        t = self.new_temp()
        m = self.attribute_stack.get_top(4)["ndim"]+1
        L1 = self.attribute_stack.get_top(4)
        E = self.attribute_stack.get_top(2)
        self.gencode("*",L1["addr"],L1["array"].limits[m],t)
        self.gencode("+",t,E["addr"],t)
        L_attribute["array"] = L1["array"]
        L_attribute["addr"] = t
        L_attribute["ndim"] = m
        return L_attribute
    #E::=E1 + Y
    #{E.addr:=newtemp;gencode(E.addr ':='E1.addr'+'Y.addr)}
    def semantic_action_31(self):
        E_attribute = {}
        E_attribute["addr"] = self.new_temp()
        E1 = self.attribute_stack.get_top(3)
        Y = self.attribute_stack.get_top(1)
        self.gencode("+",E1["addr"],Y["addr"],E_attribute["addr"])
        return E_attribute
    #E::=E1 - Y
    #{E.addr:=newtemp;gencode(E.addr ':='E1.addr'-'Y.addr)}
    def semantic_action_32(self):
        E_attribute = {}
        E_attribute["addr"] = self.new_temp()
        E1 = self.attribute_stack.get_top(3)
        Y = self.attribute_stack.get_top(1)
        self.gencode("-",E1["addr"],Y["addr"],E_attribute["addr"])
        return E_attribute
    #E::=Y
    #{E.addr:=Y.addr}
    def semantic_action_33(self):
        E_attribute = {}
        E_attribute["addr"] = self.attribute_stack.get_top(1)["addr"]
        return E_attribute
    #Y::=Y1 * F
    #{Y.addr:=newtemp;gencode(Y.addr ':='Y1.addr'*'F.addr)}
    def semantic_action_34(self):
        Y_attribute = {}
        Y_attribute["addr"] = self.new_temp()
        Y1 = self.attribute_stack.get_top(3)
        F = self.attribute_stack.get_top(1)
        self.gencode("*",Y1["addr"],F["addr"],Y_attribute["addr"])
        return Y_attribute
    #Y::=Y1 / F
    #{Y.addr:=newtemp;gencode(Y.addr ':='Y1.addr'/'F.addr)} 
    def semantic_action_35(self):
        Y_attribute = {}
        Y_attribute["addr"] = self.new_temp()
        Y1 = self.attribute_stack.get_top(3)
        F = self.attribute_stack.get_top(1)
        self.gencode("/",Y1["addr"],F["addr"],Y_attribute["addr"])
        return Y_attribute
    #Y::=F
    #{Y.addr:=F.addr}
    def semantic_action_36(self):
        Y_attribute = {}
        Y_attribute["addr"] = self.attribute_stack.get_top(1)["addr"]
        return Y_attribute
    #F::=( M )
    #{F.addr:=M.addr}
    def semantic_action_37(self):
        F_attribute = {}
        F_attribute["addr"] = self.attribute_stack.get_top(2)["addr"]
        return F_attribute
    #F::=M
    #F.addr:=M.addr
    def semantic_action_38(self):
        F_attribute = {}
        F_attribute["addr"] = self.attribute_stack.get_top(1)["addr"]
        return F_attribute
    #{if Left.offset=null then /*Left是简单id*/
    #M.addr:= Left.addr
    #else begin           /*Left是数组元素*/
    #M.addr:=newtemp;
    #gencode(M.addr ':=' Left.addr ' [' Left.offset ']')
    #end}
    #M::=Left
    def semantic_action_39(self):
        M_attribute = {}
        Left = self.attribute_stack.get_top(1)
        if Left["offset"] == None:
            M_attribute["addr"] = Left["addr"]
        else:
            M_attribute["addr"] = self.new_temp()
            self.gencode("=",Left["addr"] + "[" + Left["offset"] + "]",None,M_attribute["addr"])
        return M_attribute
    #M::=CI
    #M.addr:=newtemp;
    #gencode(M.addr ':=' CI)
    def semantic_action_40(self):
        M_attribute = {}
        M_attribute["addr"] = self.new_temp()
        CI = self.attribute_stack.get_top(1)
        self.gencode("=",str(CI["value"]),None,M_attribute["addr"])
        return M_attribute
    #M::=CF
    #M.addr:=newtemp;
    #gencode(M.addr ':=' CF)
    def semantic_action_41(self):
        M_attribute = {}
        M_attribute["addr"] = self.new_temp()
        CF = self.attribute_stack.get_top(1)
        self.gencode("=",str(CF["value"]),None,M_attribute["addr"])
        return M_attribute
    #M::=CC
    #M.addr:=newtemp;
    #gencode(M.addr ':=' CC)
    def semantic_action_42(self):
        M_attribute = {}
        M_attribute["addr"] = self.new_temp()
        CC = self.attribute_stack.get_top(1)
        self.gencode("=",str(CC["value"]),None,M_attribute["addr"])
        return M_attribute
    def back_patch(self,code_index_list,quad):
        for index in code_index_list:
            self.code_list[index].result = quad
    def merge(self,list1,list2):
        return list1+list2
    def makelist(self,quad):
        return [quad]
    #{backpatch(B.truelist, M3.quad);
    #S.nextlist := merge(B.falselist, W'.nextlist)}
    #S::= if B { M3 W' }
    def semantic_action_43(self):
        S_attribute = {}
        B = self.attribute_stack.get_top(5)
        M3 = self.attribute_stack.get_top(3)
        W_ = self.attribute_stack.get_top(2)
        self.back_patch(B["truelist"],M3["quad"])
        S_attribute["nextlist"] = self.merge(B["falselist"],W_["nextlist"])
        return S_attribute
    #{backpatch(B.truelist, M31.quad);
    #backpatch(B.falselist, M32.quad);
    #S.nextlist := merge(W'1.nextlist, merge(M4.nextlist, W'2.nextlist))}
    #S::= if B { M31 W'1 M4 } else { M32 W'2 }
    def semantic_action_44(self):
        S_attribute = {}
        B = self.attribute_stack.get_top(11)
        M31 = self.attribute_stack.get_top(9)
        M32 = self.attribute_stack.get_top(3)
        W_1 = self.attribute_stack.get_top(8)
        W_2 = self.attribute_stack.get_top(2)
        M4 = self.attribute_stack.get_top(7)
        self.back_patch(B["truelist"],M31["quad"])
        self.back_patch(B["falselist"],M32["quad"])
        S_attribute["nextlist"] = self.merge(W_1["nextlist"],self.merge(M4["nextlist"],W_2["nextlist"]))
        return S_attribute
    #{backpatch(W'.nextlist, M31.quad); 
    #backpatch(B.truelist,M32.quad);
    #S.nextlist:=B.falselist; 
    #gencode('goto'M31.quad)}
    #S::= while M31 B do { M32 W' }
    def semantic_action_45(self):
        S_attribute = {}
        W_ = self.attribute_stack.get_top(2)
        M32 = self.attribute_stack.get_top(3)
        B = self.attribute_stack.get_top(6)
        M31 = self.attribute_stack.get_top(7)
        self.back_patch(W_["nextlist"],M31["quad"])
        self.back_patch(B["truelist"],M32["quad"])
        S_attribute["nextlist"] = B["falselist"]
        self.gencode("goto",None,None,M31["quad"])
        return S_attribute
    #{M.quad := nextquad}
    #M3::=ε
    def semantic_action_46(self):
        M3_attirbute = {}
        M3_attirbute["quad"] = self.next_quad
        return M3_attirbute
    #{M4.nextlist := makelist(nextquad); gencode('goto –')}
    #M4::=ε
    def semantic_action_47(self):
        M4_attribute = {}
        M4_attribute["nextlist"] = self.makelist(self.next_quad)
        self.gencode("goto",None,None,None)
    #{ backpatch(B1.falselist, M3.quad);
	#B.truelist := merge(B1.truelist, G.truelist);
	#B.falselist := G.falselist}
    #B::=B1 || M3 G
    def semantic_action_48(self):
        B_attribute = {}
        B1 = self.attribute_stack.get_top(4)
        M3 = self.attribute_stack.get_top(2)
        G = self.attribute_stack.get_top(1)
        self.back_patch(B1["falselist"],M3["quad"])
        B_attribute["truelist"] = self.merge(B1["truelist"],G["truelist"])
        B_attribute["falselist"] = G["falselist"]
        return B_attribute
    #B.truelist = G.truelist
    #B.falselist = G.falselist
    #B::=G
    def semantic_action_49(self):
        B_attribute = {}
        G = self.attribute_stack.get_top(1)
        B_attribute["truelist"] = G["truelist"]
        B_attribute["falselist"] = G["falselist"]
        return B_attribute
    #{backpatch(G1.truelist, M3.quad);
	#G.truelist := H.truelist;
	#G.falselist := merge(G1.falselist, H.falselist)}
    #G::=G1 && M3 H
    def semantic_action_50(self):
        G_attribute = {}
        G1 = self.attribute_stack.get_top(4)
        M3 = self.attribute_stack.get_top(2)
        H = self.attribute_stack.get_top(1)
        self.back_patch(G1["truelist"],M3["quad"])
        G_attribute["truelist"] = H["truelist"]
        G_attribute["falselist"] = self.merge(G1["falselist"],H["falselist"])
        return G_attribute
    #G.truelist = H.truelist
    #G.falselist = H.falselist
    #G::=H
    def semantic_action_51(self):
        G_attribute = {}
        H = self.attribute_stack.get_top(1)
        G_attribute["truelist"] = H["truelist"]
        G_attribute["falselist"] = H["falselist"]
        return G_attribute
    #H.truelist := H1.falselist; H.falselist := H1.truelist
    #H::=! H1
    def semantic_action_52(self):
        H_attribute = {}
        H1 = self.attribute_stack.get_top(1)
        H_attribute["truelist"] = H1["falselist"]
        H_attribute["falselist"] = H1["truelist"]
        return H_attribute
    #H.truelist = I.truelist
    #H.falselist = I.falselist
    #H::=I
    def semantic_action_53(self):
        H_attribute = {}
        I = self.attribute_stack.get_top(1)
        H_attribute["truelist"] = I["truelist"]
        H_attribute["falselist"] = I["truelist"]
    #{I.truelist :=makelist(nextquad);
    #I.falselist := makelist(nextquad+1);
	#gencode('if' E1.addr R.op E2.addr 'goto –');
	#gencode('goto –')}
    #I::=E1 R E2
    def semantic_action_54(self):
        I_attribute = {}
        E2 = self.attribute_stack.get_top(1)
        R = self.attribute_stack.get_top(2)
        E1 = self.attribute_stack.get_top(3)
        I_attribute["truelist"] = self.makelist(self.next_quad)
        I_attribute["falselist"] = self.makelist(self.next_quad+1)
        self.gencode("goto"+R.op,E1["addr"],E2["addr"],None)
        self.gencode("goto",None,None,None)
        return I_attribute
    #I.truelist := B.truelist;
    #I.falselist := B.falselist
    #I::=( B )
    def semantic_action_55(self):
        I_attribute = {}
        B = self.attribute_stack.get_top(2)
        I_attribute["truelist"] = B["truelist"]
        I_attribute["falselist"] = B["falselist"]
        return I_attribute
    #I::=true
    #I.truelist := makelist(nextquad);
    #gencode('goto –')
    def semantic_action_56(self):
        I_attribute = {}
        I_attribute["truelist"] = self.makelist(self.next_quad)
        self.gencode("goto",None,None,None)
        return I_attribute
    #I.falselist := makelist(nextquad);
    # gencode('goto –')
    #I::=false
    def semantic_action_57(self):
        I_attribute = {}
        I_attribute["falselist"] = self.makelist(self.next_quad)
        self.gencode("goto",None,None,None)
        return I_attribute
    #R.op = "<"
    #R::=<
    def semantic_action_58(self):
        R_attribute = {"op":"<"}
        return R_attribute
    #R.op = "<="
    #R::=< =
    def semantic_action_59(self):
        R_attribute = {"op":"<="}
        return R_attribute
    #R.op = "=="
    #R::== =
    def semantic_action_60(self):
        R_attribute = {"op":"=="}
        return R_attribute
    #R.op = "! ="
    #R::=! =
    def semantic_action_61(self):
        R_attribute = {"op":"!="}
        return R_attribute
    #R.op = ">"
    #R::=>
    def semantic_action_62(self):
        R_attribute = {"op":">"}
        return R_attribute
    #R.op = ">="
    #R::=> =
    def semantic_action_63(self):
        R_attribute = {"op":">="}
        return R_attribute
    #{backpatch(W'1.nextlist, M3.quad); 
    #W'.nextlist = S.nextlist if S has nextlist
    #or W'.nextlist = []
    #W'::=W'1 M3 S 
    def semantic_action_9(self):
        W__attribute = {}
        W_1 = self.attribute_stack.get_top(3)
        M3 = self.attribute_stack.get_top(2)
        S = self.attribute_stack.get_top(1)
        self.back_patch(W_1["nextlist"],M3["quad"])
        if "nextlist" in S:
            W__attribute["nextlist"] = S["nextlist"]
        else:
            W__attribute["nextlist"] = []
        return W__attribute
    #W'.nextlist = S.nextlist if S has nextlist
    #or W'.nextlist = []
    #W'::=S
    def semantic_action_8(self):
        W__attribute = {}
        S = self.attribute_stack.get_top(1)
        if "nextlist" in S:
            W__attribute["nextlist"] = S["nextlist"]
        else:
            W__attribute["nextlist"] = []
        return W__attribute
    #P.nextlist = S.nextlist if S has nextlist
    #or P.nextlist = []
    #P::=S
    def semantic_action_4(self):
        P_attribute = {}
        S = self.attribute_stack.get_top(1)
        if "nextlist" in S:
            P_attribute["nextlist"] = S["nextlist"]
        else:
            P_attribute["nextlist"] = []
        return P_attribute
    #P.nextlist = []
    #P::=D
    def semantic_action_3(self):
        P_attribute = {}
        P_attribute["nextlist"] = []
        return P_attribute
    #P'::=P
    #P'.nextlist = P.nextlist
    def semantic_action_2(self):
        P__attribute = {}
        P = self.attribute_stack.get_top(1)
        P__attribute["nextlist"] = P["nextlist"]
        return P__attribute
    #P'::=P'1 M3 P
    #{backpatch(P'1.nextlist, M3.quad); 
    #P'.nextlist = P.nextlist
    def semantic_action_1(self):
        P__attribute = {}
        P = self.attribute_stack.get_top(1)
        M3 = self.attribute_stack.get_top(2)
        P_1 = self.attribute_stack.get_top(3)
        self.back_patch(P_1["nextlist"],M3["quad"])
        P__attribute["nextlist"] = P["nextlist"]
        return P__attribute
    #start::=P'
    def semantic_action_0(self):
        return {}
    # {n :=0; 
    #repeat
    #n:=n+1；
    #从queue的队首取出一个实参地址p;
	#gencode('param', -, -, p);
    #until queue为空;
	#gencode('call', id.addr, n, -)}
    #S::=call id ( Elist ) ;
    def semantic_action_64(self):
        id = self.attribute_stack.get_top(5)
        n=0
        while not self.param_queue.is_empty():
            p = self.param_queue.dequeue()
            self.gencode("param",None,None,p)
            n+=1
        self.gencode("call",id["addr"],n,None)
    #Elist::=Elist , E
    #{将E.addr添加到queue的队尾}
    def semantic_action_65(self):
        E = self.attribute_stack.get_top(1)
        self.param_queue.enqueue(E["addr"])
        return {}
    #Elist::=E
    #初始化queue，然后将E.addr加入到queue的队尾。
    def semantic_action_66(self):
        E = self.attribute_stack.get_top(1)
        self.param_queue.enqueue(E["addr"])
        return {}
    #List::=id
    def semantic_action_68(self):
        id = self.attribute_stack.get_top(1)
        self.param_queue.enqueue(id["addr"])
        return {}
    #List::=List , id
    ##{将id.addr添加到queue的队尾}
    def semantic_action_67(self):
        id = self.attribute_stack.get_top(1)
        self.param_queue.enqueue(id["addr"])
        return {}
    #{n:=0;
    #repeat 
    #move(Queue, in);
    #gencode(‘param’, -, -, in);
    #n:=n+1;
    #until Queue为空;
    #gencode(‘call’, ‘SYSOUT’, n, -)}
    #S::=print ( Elist ) ;
    def semantic_action_22(self):
        n = 0
        while not self.param_queue.is_empty():
            p = self.param_queue.dequeue()
            self.gencode("param",None,None,p)
            n = n+1
        self.gencode("call","SYSOUT",n,None)
        return {}
    #{n:=0;
    #repeat 
    #move(Queue, in);
    #gencode(‘par’, ‘in’, -, -);
    #n:=n+1;
    #until Queue为空;
    #gencode(‘call’, ‘SYSIN’, n, -);}
    #S::=input ( List ) ;
    def semantic_action_23(self):
        List = self.attribute_stack.get_top(3)
        n = 0
        while not self.param_queue.is_empty():
            p = self.param_queue.dequeue()
            self.gencode("param",None,None,p)
            n = n+1
        self.gencode("call","SYSIN",n,None)
        return {}