"""

 with open("us439.csv", "r") as filetypeobject:
    header = ["switchname"]
    dictreadertypeobject = csv.DictReader(filetypeobject, fieldnames = header)
    inputswitchlist = []
    for i in dictreadertypeobject:
        inputswitchlist.append(i["switchname"])
    inputswitchlist.pop(0)
    reachability(inputswitchlist)
    
    """


#f = open("one.txt", "r")

# f.write("hello\nhuigkhj\nytfcfgh\nsdf")

for i in open("one.csv", "r"):
    print(i, end='')
