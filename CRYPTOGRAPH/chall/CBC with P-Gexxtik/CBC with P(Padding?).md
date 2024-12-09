given source code:
```python
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
```

This is AES CBC encryption with padding

The popular attack on CBC is padding oracle attack
- When we send a ciphertext to decrypt (option 2), it tells us if decryption failed (through the try/except)
- The encryption is using a modified CBC mode where the IV for the next block is XOR of current ciphertext block and current plaintext block
- We can get the encrypted secret multiple times (option 1)
- We get to know if decryption failed through error messages

creating the automation script below to get the secret, decrypt the secret, and submit it in option 3

```python
from binascii import hexlify, unhexlify
import socket
import sys
import time

def connect_to_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def receive_until(sock, delim=b'>'):
    data = b''
    while not data.endswith(delim):
        data += sock.recv(1)
    return data

def try_decrypt(ct_hex, sock):
    try:
        receive_until(sock, b'> ')
        sock.send(b'2\n')
        receive_until(sock, b'> ')
        sock.send(ct_hex.encode() + b'\n')
        response = receive_until(sock, b'>')
        return b'Something went wrong' not in response
    except:
        return False

def decrypt_block(prev_block, curr_block, sock):
    block_size = 16
    intermediate = bytearray(block_size)
    decrypted = bytearray(block_size)
    
    for byte_pos in range(block_size-1, -1, -1):
        padding_value = block_size - byte_pos
        test_block = bytearray(prev_block)
        
        for pad_pos in range(byte_pos + 1, block_size):
            test_block[pad_pos] ^= intermediate[pad_pos] ^ padding_value
            
        for test_value in range(256):
            test_block[byte_pos] = prev_block[byte_pos] ^ test_value
            test_ct = hexlify(test_block + curr_block).decode()
            
            if try_decrypt(test_ct, sock):
                intermediate[byte_pos] = test_value ^ padding_value
                decrypted[byte_pos] = intermediate[byte_pos] ^ prev_block[byte_pos]
                sys.stdout.write(f'\rDecrypting: {byte_pos:2d}/16')
                sys.stdout.flush()
                break
                
    print()
    return bytes(decrypted)

def get_encrypted_secret(sock):
    receive_until(sock, b'> ')
    sock.send(b'1\n')
    response = receive_until(sock, b'>')
    return response.split(b'\n')[0].decode().strip()

def send_decrypted_secret(sock, secret):
    receive_until(sock, b'> ')
    sock.send(b'3\n')
    receive_until(sock, b'> ')
    sock.send(hexlify(secret) + b'\n')
    return receive_until(sock, b'>').decode()

def decrypt_secret(encrypted_hex, sock):
    ct = unhexlify(encrypted_hex)
    block_size = 16
    blocks = [ct[i:i+block_size] for i in range(0, len(ct), block_size)]
    
    plaintext = b''
    for i in range(1, len(blocks)):
        print(f"\nBlock {i} of {len(blocks)-1}")
        decrypted_block = decrypt_block(blocks[i-1], blocks[i], sock)
        plaintext += decrypted_block
        
        if i < len(blocks) - 1:
            blocks[i] = bytes(x ^ y for x, y in zip(blocks[i], decrypted_block))
    
    return plaintext

def main():
    host = "152.118.201.242"
    port = 9090
    
    print(f"Connecting to {host}:{port}")
    sock = connect_to_server(host, port)
    
    print("Getting encrypted secret...")
    encrypted_hex = get_encrypted_secret(sock)
    print(f"Encrypted secret: {encrypted_hex}")
    
    print("\nStarting decryption...")
    decrypted = decrypt_secret(encrypted_hex, sock)
    
    print("\nDecrypted value:", decrypted)
    print("Sending back to server...")
    
    flag = send_decrypted_secret(sock, decrypted)
    print("\nServer response:", flag)
    
    sock.close()

if __name__ == "__main__":
    main()
```

