import settings
from multiprocessing import Process
#import time
#import random
#from os import path

if __name__ == '__main__':
    settings.init()
    p = Process(target = miner)
    p.start()
    p.join()



with Listener(on_press=press) as listener: # Keypress listener
    listener.join()
