# Encrypted numbers (first few from the output you got)
encrypted_numbers = [
    78.0, 70.0, 86.0, 86.0, 83.0, 88.0, 129.0, 123.0, 112.0, 114.0, 
    125.0, 106.0, 117.0, 128.0, 109.0, 112.0, 111.0, 135.0, 119.0, 
    133.0, 141.0, 116.0, 130.0, 134.0, 134.0, 128.0, 121.0, 129.0, 
    136.0, 126.0, 133.0, 126.0, 130.0, 134.0, 133.0, 132.0, 153.0, 
    152.0, 139.0, 134.0, 156.0
]

# The known flag prefix "NETSOS{"
flag_prefix = "NETSOS{"
ascii_values = [ord(c) for c in flag_prefix]

# Step 1: Calculate the offsets by subtracting ASCII values of "NETSOS{" from the encrypted numbers
offsets = [int(encrypted_numbers[i]) - ascii_values[i] for i in range(len(flag_prefix))]
print("Offsets:", offsets)

# Step 2: Apply the offsets to the rest of the encrypted numbers to decrypt
decrypted_flag = ''.join(
    chr(int(encrypted_numbers[i]) - offsets[i % len(offsets)]) for i in range(len(encrypted_numbers))
)

# Step 3: Print the decrypted flag
print("Decrypted Flag:", decrypted_flag)

