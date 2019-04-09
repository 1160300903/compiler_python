from collections import namedtuple
class Input(namedtuple("Input","i source")):
        pass
def get_char(input):
        input.i += 1
        return input.source[i-1]
def token_scan(path):
    file1 = open(path,"r")
    source = file1.read()
    input = Input(i = 0, source = source)
    ch = 
    while(char ==" " or char == "\t" or char = "\n"):
        ch = 