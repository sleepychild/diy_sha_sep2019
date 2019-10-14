import os

def ls():
    for element in  os.ilistdir():
        print(element)

def cat(file):
    with open(file, 'r') as file:
        for line in file.readlines():
            print(line)

def lscat():
    files = os.listdir()
    print("Select File For Cat")
    for f in files:
        print(files.index(f),' : ',f)
    try:
        cat(files[int(input())])
    except Exception as e:
        print(e)