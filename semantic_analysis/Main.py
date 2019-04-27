import sys
sys.path.append(".")
from lexical_analysis import lexical_parse
from grammar_analysis import grammar_parser
if __name__ == "__main__":
    print(1)
    lexical_parse()
    g = grammar_parser("grammar.txt")
    g.show_table(True)#在文件中打印符号表。现在已经打印过了，所以注释掉了
    print(2)
    g.read_tokens()
    g.grammar_parse()
    g.show_symbol_table()