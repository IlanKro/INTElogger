import time
import random
from multiprocessing import Process

"""
Fake miner
"""
class Miner(Process):
    _INTEcoins = 0
    _file_count = 1
    def __init__(self):
        super().__init__(None, self)
        print("Welcome to INTEminer for INTEcoins!")
        print("Mining..", end = "")

    def run(self):
        while True:
            # Miner messages
            print(".", end = "")
            randomNumber = random.randint(1, 100)
            time.sleep(randomNumber/20) # Sleeps for a short random time
            if randomNumber%10 == 0:
                self._INTEcoins += randomNumber
                print("\nMined {} INTEcoins! You currently have {} coins!".format(randomNumber, self._INTEcoins))
                print("Mining", end = "")

            # Writes fake logs
            if randomNumber%50 == 0:
                self._file_count+=1
            else:
                with open("logs/INTEcoin{}.dat".format(self._file_count), "a") as file:
                    file.write("{0:b}".format(random.randint(10000000000,100000000000)))
                    file.close()