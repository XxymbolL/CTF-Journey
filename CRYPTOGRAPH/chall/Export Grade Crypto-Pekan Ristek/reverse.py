import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time

# Given ciphertext (from the print result)
ciphertext = b'/3R9\x0b\xfd\xa9\xf3\x08\x89\xb2\xf27E\xe2E\x10\r6\xb1\xad\x96uJeC\\v\x88\xc6\x1c\x97'

# The flag should be the same length and structure as given in the encryption code
key = hashlib.md5(str(int(time.time())).encode()).digest()[:5] + str(int(time.time())).encode() + b"\x00"
iv = hashlib.md5(str(int(time.time())).encode()).digest()

# Initialize the AES cipher for decryption in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt the ciphertext and unpad it
decrypted_data = unpad(cipher.decrypt(ciphertext), 16)

# Convert the decrypted data to a string (the flag)
print(decrypted_data.decode())

