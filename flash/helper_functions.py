from os import listdir, ilistdir, remove
from time import sleep_ms

def ls():
    for element in ilistdir():
        print(element)

def cat(file):
    with open(file, 'r') as file:
        for line in file.readlines():
            print(line)

def rm(file):
    remove(file)

def lscat():
    files = listdir()
    print("Select File For Cat")
    for f in files:
        print(files.index(f),' : ',f)
    try:
        cat(files[int(input())])
    except Exception as e:
        print(e)

def lsrm():
    files = listdir()
    print("Select File For RM")
    for f in files:
        print(files.index(f),' : ',f)
    try:
        rm(files[int(input())])
    except Exception as e:
        print(e)

def url_decode(encoded_string):
    encoded_string = ":".join(encoded_string.split("%3A"))
    return "/".join(encoded_string.split("%2F"))

def toggle_pin(pin):
    pin.value(not pin.value())

def toggle_pin_loop(pin, ms):
    while True:
        sleep_ms(ms)
        toggle_pin(pin)