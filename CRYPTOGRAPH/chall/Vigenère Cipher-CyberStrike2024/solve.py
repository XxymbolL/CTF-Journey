from collections import defaultdict

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().strip()

def frequency_analysis(text):
    frequency_count = defaultdict(int)
    for char in text:
        frequency_count[char] += 1
    total_chars = len(text)
    frequencies = {char: count / total_chars for char, count in frequency_count.items()}
    return frequencies

def estimate_key(ciphertext, key_length, letter_frequencies):
    cipher_parts = ['' for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        cipher_parts[i % key_length] += char

    key = ''
    for part in cipher_parts:
        part_frequencies = frequency_analysis(part)
        correlation = {}
        for char in part_frequencies:
            correlation[char] = sum([part_frequencies[c] * letter_frequencies.get(c, 0) for c in 'abcdefghijklmnopqrstuvwxyz'])
        most_correlated_char = max(correlation, key=correlation.get)
        shift = (ord(most_correlated_char) - ord('e')) % 26
        key_char = chr(ord('a') + shift)
        key += key_char
    return key

def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():  # Ensure character is a letter
            shift = (ord(char) - ord(key[i % key_length])) % 26
            if char.isupper():  # Preserve uppercase letters
                decrypted_char = chr(shift + ord('A'))
            else:
                decrypted_char = chr(shift + ord('a'))
            decrypted_text += decrypted_char
        else:
            decrypted_text += char  # Copy non-alphabetic characters
    return decrypted_text

def main():
    ciphertext = read_file('ciphertext.txt')
    key_length = int(read_file('key_length.txt'))
    letter_frequencies = {}
    with open('letter_frequencies.txt', 'r') as file:
        for line in file:
            letter, frequency = line.strip().split(': ')
            letter_frequencies[letter] = float(frequency)

    key = estimate_key(ciphertext, key_length, letter_frequencies)
    decrypted_message = vigenere_decrypt(ciphertext, key)

    print(f"Estimated Key: {key}")
    print(f"Decrypted Message: {decrypted_message}")

if __name__ == '__main__':
    main()
