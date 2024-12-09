import hashlib;import time;from Crypto.Cipher import AES;from Crypto.Util.Padding import pad;import os
FLAG = b"NETSOS{INI_FAKE_FLAG}"
#Complying with Executive Order 13026, atleast entropy-wise
key = hashlib.md5(str(int(time.time())).encode()).digest()[:5] + str(int(time.time())).encode() + b"\x00"
cipher = AES.new(key, AES.MODE_CBC, iv=hashlib.md5(str(int(time.time())).encode()).digest())
plain = pad(FLAG, 16)
ciphertext = cipher.encrypt(plain)
print(ciphertext)
# Print result :
# b'/3R9\x0b\xfd\xa9\xf3\x08\x89\xb2\xf27E\xe2E\x10\r6\xb1\xad\x96uJeC\\v\x88\xc6\x1c\x97'