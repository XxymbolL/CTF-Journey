from sympy import mod_inverse

def generate_knapsack():
    knapsack = [1, 2]
    for i in range(6):
        knapsack.append(sum(knapsack) + 1)
    return knapsack

def decrypt_message(ciphertext, knapsack, m, n):
    try:
        # Calculate the modular inverse of n mod m
        n_inverse = mod_inverse(n, m)
    except ValueError:
        return None  # Skip if n does not have an inverse modulo m

    # Decrypt each value in the ciphertext
    decrypted_bits = []
    for encrypted_value in ciphertext:
        # Calculate the original sum before multiplication by n
        c_value = (encrypted_value * n_inverse) % m

        # Solve the superincreasing knapsack to find the bit pattern
        bits = []
        for k in reversed(knapsack):
            if c_value >= k:
                bits.insert(0, 1)
                c_value -= k
            else:
                bits.insert(0, 0)
        decrypted_bits.extend(bits)

    # Convert bits back to characters
    decrypted_message = ""
    for i in range(0, len(decrypted_bits), 8):
        byte = decrypted_bits[i:i + 8]
        char = chr(int("".join(map(str, byte)), 2))
        decrypted_message += char

    return decrypted_message

if __name__ == "__main__":
    ciphertext = [251, 210, 197, 79, 48, 120, 179, 12, 197, 143, 107, 230, 230, 230, 89, 89, 107, 217, 217, 217, 80, 242, 158, 179, 25, 55, 210, 80, 88, 230, 107, 80, 43, 199, 43, 80, 30, 230, 251, 80, 125, 55, 25, 80, 48, 25, 204, 204, 204, 204, 215]
    knapsack = generate_knapsack()
    m = 257

    # Brute-force for n
    for n in range(-1000, 1001):
        decrypted_message = decrypt_message(ciphertext, knapsack, m, n)
        if decrypted_message and all(32 <= ord(c) < 127 for c in decrypted_message):
            print(f"Possible decryption with n={n}: {decrypted_message}")

