n = open('plaintext', 'r').read()
print(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(n, n[1:])), file=open('ciphertext', 'w'))