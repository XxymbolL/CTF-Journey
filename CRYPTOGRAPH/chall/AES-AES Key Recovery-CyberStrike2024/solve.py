from Crypto.Cipher import AES
import binascii

# Read the ciphertext from a file in binary mode
with open("ciphertext.txt", "rb") as f:
    ciphertext = f.read()  # Read the binary data directly

# Known plaintext for the start of the ciphertext
known_plaintext = b'CTF{jafupaudp9fu'
# Recovered XOR result (XOR of IV and the known plaintext)
recovered_xor = bytes.fromhex("4e1d8c421f92bd2b018026e6d97d700c")

# AES block size is 16 bytes
BLOCK_SIZE = 16

# Split ciphertext into blocks of 16 bytes
cipher_blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]

# First block (IV) and the rest are ciphertext
iv = cipher_blocks[0]
ciphertext_blocks = cipher_blocks[1:]

# XOR function to combine bytes
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# To recover the full plaintext
plaintext = bytearray()

# Add the known plaintext to the output
plaintext.extend(known_plaintext)

# Initialize the previous ciphertext as the IV for the first block
previous_ciphertext = iv

# Decrypt the rest of the blocks
for i in range(len(ciphertext_blocks)):
    # Create a new AES cipher instance with the recovered key (which we deduced)
    # In this scenario, the actual key needs to be deduced from previous XOR operations.
    cipher = AES.new(recovered_xor, AES.MODE_CBC, previous_ciphertext)

    # Decrypt the current ciphertext block
    decrypted_block = cipher.decrypt(ciphertext_blocks[i])

    # XOR the decrypted block with the previous ciphertext to obtain the plaintext
    plaintext_block = xor_bytes(decrypted_block, previous_ciphertext)
    plaintext.extend(plaintext_block)

    # Update the previous ciphertext for the next block
    previous_ciphertext = ciphertext_blocks[i]

# Convert plaintext to string and print
try:
    print("Recovered Full Plaintext:", plaintext.decode('utf-8'))
except UnicodeDecodeError:
    print("Recovered Full Plaintext (raw bytes):", plaintext)

