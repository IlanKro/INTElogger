from cryptography.fernet import Fernet

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