from settings import *

"""
Fake miner
"""
def miner():
    print("Welcome to INTEminer for INTEcoins!")
    print("Mining", end = "")
    INTEcoins=0
    file_count = 1
    while True:
        # Miner messages
        print(".", end = "")
        randomNumber = random.randint(1, 100)
        time.sleep(randomNumber/20) # Sleep for a short random time
        if randomNumber%10 == 0:
            INTEcoins += randomNumber
            print("\nMined {} INTEcoins! You currently have {} coins!".format(randomNumber, INTEcoins))
            print("Mining", end = "")

        # Write fake logs
        if randomNumber%50 == 0:
            file_count+=1
        else:
            with open(LOGS_PATH + "INTEcoin{}.dat".format(file_count), "a") as file:
                file.write("{0:b}".format(random.randint(10000000000,100000000000)))
                file.close()