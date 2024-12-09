# Read the ciphertext
ciphertext = open('ciphertext', 'r').read()

# Function to attempt decryption with different guesses for the first character
def brute_force_decryption(ciphertext, target_substring):
    for guess in range(32, 127):  # Test characters from ASCII 32 to 126 (printable characters)
        # Start by guessing the first character (assumed to be space or some other character)
        plaintext = [chr(ord(ciphertext[0]) ^ guess)]  # XOR the first char with the guess
        
        # Recover the rest of the plaintext
        for i in range(1, len(ciphertext)):
            plaintext.append(chr(ord(ciphertext[i - 1]) ^ ord(plaintext[i - 1])))
        
        # Check if the target substring "NETSOS" is in the recovered plaintext
        decrypted_text = ''.join(plaintext)
        if target_substring in decrypted_text:
            print(f"Found target '{target_substring}' with first character guess: {chr(guess)}")
            # Extract the line containing the target substring
            for line in decrypted_text.splitlines():
                if target_substring in line:
                    # Return the line containing the target substring
                    return line

    # If no match found, return None
    print(f"Target '{target_substring}' not found in plaintext.")
    return None

# Define the target substring to look for
target_substring = "NETSOS"

# Try to decrypt and find the target substring
found_line = brute_force_decryption(ciphertext, target_substring)

# Optionally, print the result if found
if found_line:
    print(found_line)

