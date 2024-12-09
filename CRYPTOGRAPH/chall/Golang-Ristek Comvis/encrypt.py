from Crypto.Cipher import AES
import binascii

def pad(data, block_size):
    """
    Apply PKCS#7 padding to the input data.
    """
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encrypt_ecb(plaintext, key):
    """
    Encrypts plaintext using AES in ECB mode.
    """
    # Ensure key and plaintext are bytes
    key = key.encode()  # Convert secretKey string to bytes
    plaintext = plaintext.encode()  # Convert plaintext to bytes
    
    # Initialize AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Pad plaintext to match block size
    padded_plaintext = pad(plaintext, AES.block_size)
    
    # Encrypt the padded plaintext
    encrypted = cipher.encrypt(padded_plaintext)
    return binascii.hexlify(encrypted).decode()  # Return hex-encoded ciphertext

if __name__ == "__main__":
    secret_key = "PEKANRIZZTEK2024"  # Must be exactly 16 bytes for AES-128
    plaintext_message = "NETSOS"  # Replace this with the message to encrypt

    encrypted_message = encrypt_ecb(plaintext_message, secret_key)
    print(f"Encrypted message (hex): {encrypted_message}")

