# Vigenère decryption function
def g_key(msg, key):
    key = list(key)
    if len(msg) == len(key):
        return key
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def dec(enc_msg, key):
    decrypted_text = []
    key = g_key(enc_msg, key)
    for i in range(len(enc_msg)):
        char = enc_msg[i]
        if char.isupper():
            decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('A'))
        elif char.islower():
            decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('a'))
        else:
            decrypted_char = char
        decrypted_text.append(decrypted_char)
    return "".join(decrypted_text)

# Read the keys from 'Zerologon Phished.txt' file
with open("Zerologon Phished.txt", "r") as file:
    key_list = [line.strip() for line in file.readlines()]  # Strips newline characters

# Encoded message (from your earlier example)
encoded_message = "zhdwqmj{CPro5khGjcezVyag}"

# Brute-force decryption
for key in key_list:
    key = key.replace(" ", "")  # Remove spaces from keys if needed
    decrypted_message = dec(encoded_message, key)
    if decrypted_message.startswith("zeroday{"):
        print(f"Key: {key}")
        print(f"Decrypted message: {decrypted_message}")
        break

