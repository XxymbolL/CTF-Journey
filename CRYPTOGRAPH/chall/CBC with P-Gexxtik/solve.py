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
