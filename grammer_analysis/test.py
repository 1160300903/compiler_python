from grammer_analysis import *
if __name__ == "__main__":
    g = grammer_parser("sample.txt")
    print(g.follow_dict)
    print()
    print(g.first_dict)
