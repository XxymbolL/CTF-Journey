from binascii import hexlify, unhexlify
import sys

def try_decrypt(ct_hex, oracle_function):
    """Attempt to decrypt and return if padding is valid"""
    try:
        return oracle_function(ct_hex)
    except:
        return False

def decrypt_block(prev_block, curr_block, oracle_function, block_size=16):
    """Decrypt a single block using padding oracle attack"""
    intermediate = bytearray(block_size)
    decrypted = bytearray(block_size)
    
    # For each byte position in the block
    for byte_pos in range(block_size-1, -1, -1):
        padding_value = block_size - byte_pos
        
        # Prepare test block with known padding bytes
        test_block = bytearray(prev_block)
        for pad_pos in range(byte_pos + 1, block_size):
            test_block[pad_pos] ^= intermediate[pad_pos] ^ padding_value
            
        # Try all possible values
        found = False
        for test_value in range(256):
            test_block[byte_pos] = prev_block[byte_pos] ^ test_value
            test_ct = hexlify(test_block + curr_block).decode()
            
            if try_decrypt(test_ct, oracle_function):
                intermediate[byte_pos] = test_value ^ padding_value
                decrypted[byte_pos] = intermediate[byte_pos] ^ prev_block[byte_pos]
                found = True
                # Show progress
                sys.stdout.write(f'\rDecrypting: {byte_pos:2d}/16 bytes for current block')
                sys.stdout.flush()
                break
        
        if not found:
            print(f"\nWarning: Could not find valid value for byte {byte_pos}")
            
    print()  # New line after progress
    return bytes(decrypted)

def decrypt_secret(encrypted_hex, oracle_function):
    """Decrypt the entire ciphertext"""
    try:
        ct = unhexlify(encrypted_hex)
    except:
        print("Error: Invalid hex string")
        return None
        
    block_size = 16
    
    if len(ct) % block_size != 0:
        print("Error: Ciphertext length is not a multiple of block size")
        return None
        
    blocks = [ct[i:i+block_size] for i in range(0, len(ct), block_size)]
    if len(blocks) < 2:
        print("Error: Ciphertext too short")
        return None
        
    print(f"Total blocks to decrypt: {len(blocks)-1}")
    plaintext = b''
    
    for i in range(1, len(blocks)):
        print(f"\nDecrypting block {i} of {len(blocks)-1}")
        decrypted_block = decrypt_block(blocks[i-1], blocks[i], oracle_function)
        plaintext += decrypted_block
        
        # Modified CBC mode: update next IV
        if i < len(blocks) - 1:
            blocks[i] = bytes(x ^ y for x, y in zip(blocks[i], decrypted_block))
    
    return plaintext

def local_oracle(ct_hex):
    """Local oracle function that communicates with the server"""
    # Here we simulate server interaction
    # In real usage, this would send the ciphertext to the server and check response
    try:
        ct = unhexlify(ct_hex)
        # Send to server option 2
        # If we reach here, decryption succeeded
        return True
    except:
        # If we get here, decryption failed
        return False

def main():
    print("=== Padding Oracle Attack for Modified CBC Mode ===")
    print("\nPaste the encrypted secret (hex format) from server option 1:")
    encrypted_hex = input().strip()
    
    print("\nStarting decryption...")
    result = decrypt_secret(encrypted_hex, local_oracle)
    
    if result is not None:
        print("\nDecryption completed!")
        print("\nDecrypted value (hex):", hexlify(result).decode())
        print("Decrypted value (raw):", result)
        print("\nYou can now send this value to server option 3 to get the flag!")

if __name__ == "__main__":
    main()
