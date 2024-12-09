from binascii import hexlify, unhexlify
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint

key = urandom(AES.key_size[0])
secret = urandom(randint(AES.block_size, 4 * AES.block_size))

def xor(a, b):
    return bytes([a[i] ^ b[i] for i in range(len(a))])

def encrypt(msg):
    pt = pad(msg, AES.block_size)
    iv = urandom(AES.block_size)
    ct = iv[:]
    for i in range(0, len(pt), AES.block_size):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct += cipher.encrypt(pt[i:i+AES.block_size])
        iv = xor(ct[-AES.block_size:], pt[i:i + AES.block_size])
    return ct

def decrypt(ct):
    iv = ct[:AES.block_size]
    pt = b''
    for i in range(AES.block_size, len(ct), AES.block_size):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt += cipher.decrypt(ct[i:i+AES.block_size])
        iv = xor(ct[i:i + AES.block_size], pt[-AES.block_size:])
    return unpad(pt, AES.block_size)


rnd = urandom(AES.block_size)
assert decrypt(encrypt(rnd)) == rnd

def menu():
    print('1. Get encrypted secret')
    print('2. Decrypt a message')
    print('3. Get flag')
    print('4. Exit')

while True:
    try:
        menu()
        choice = input('> ')
        if choice == '1':
            res = hexlify(encrypt(secret)).decode()
            print(res)
        elif (choice == '2'):
            ct = unhexlify(input('> '))
            decrypt(ct)
        elif (choice == '3'):
            answer = unhexlify(input('> ').strip())
            if answer == secret:
                print(open('flag.txt', 'rb').read())
            break
        elif (choice == '4'):
            print('Bye.')
            break
        else:
            print('Invalid input!')
    except:
        print('Something went wrong.')