from grammer_analysis import *
if __name__ == "__main__":
    g = grammer_parser("test.txt")
    g.show_table()
    g.parse("abab",True)
