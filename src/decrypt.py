from encryption import Encryption  # relative imports are weird in python.

chunk = ""
decrypted_log = ""
for byt in Encryption.bytes_from_file("INTEcoin.dat"):  # Reads stolen data file as chunks and save them in a list
	if byt == "@":
		decrypted_log += Encryption.decrypt(chunk.encode())
		chunk = ""
		continue
	chunk += byt
print(decrypted_log)

with open("plaintext.txt", "a") as file:
    file.write(decrypted_log)
    file.close()
