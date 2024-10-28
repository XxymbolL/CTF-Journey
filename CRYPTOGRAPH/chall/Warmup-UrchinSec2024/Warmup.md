#cryptography #cipher #medium

Is this a real warmup?

## Chall
Given ciphertext:
```
Ciphertext: [251, 210, 197, 79, 48, 120, 179, 12, 197, 143, 107, 230, 230, 230, 89, 89, 107, 217, 217, 217, 80, 242, 158, 179, 25, 55, 210, 80, 88, 230, 107, 80, 43, 199, 43, 80, 30, 230, 251, 80, 125, 55, 25, 80, 48, 25, 204, 204, 204, 204, 215]
```

and enc.py:
```python
from sympy import mod_inverse

def generate_knapsack():
    knapsack = [1, 2]
    for i in range(6):
        knapsack.append(sum(knapsack) + 1)
    return knapsack

def convert_to_bits(message):
    bits = []
    for char in message:
        char_bits = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in char_bits])
    return bits

def encrypt_message(message, knapsack, m, n):
    bits = convert_to_bits(message)
    chunk_size = len(knapsack)
    chunks = [bits[i:i + chunk_size] for i in range(0, len(bits), chunk_size)]
    ciphertext = []
    for chunk in chunks:
        if len(chunk) < chunk_size:
            chunk += [0] * (chunk_size - len(chunk))
        c_value = sum(k * b for k, b in zip(knapsack, chunk))
        encrypted_value = (c_value * n) % m
        ciphertext.append(encrypted_value)
    return ciphertext

if __name__ == "__main__":
    message = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    knapsack = generate_knapsack()
    m = 257
    n = random.randint(-1000, 1000)
    ciphertext = encrypt_message(message, knapsack, m, n)
    print("Ciphertext:", ciphertext)
```

#### Code Explanation
##### Generate Knapsack
Generate knapsack function generate a list with length of 8 with consist of [1,2,4,8,16,32,64,128] (the base$_{10}$ representation of each Bit as it goes to $2^{8-1}$)
##### Convert to bits
Create 1D list of message bits which the list contain of bit representation of each char in message. 
`char_bits = bin(ord(char))[2:].zfill(8)` takes the char to its ASCII decimal value and then translate to binary value with removed `0b` in the beginning. with `.zfill(8)` act as padding to make it consistent in 8 bit representation.
##### Encrypt Message
The encrypt Message takes parameter of Message, Knapsack ([1,2,4,8,16,32,64,128]), m, and n.
First it create an empty list of ciphertext that will be the program output, convert the message to list of bits with second function, and create the chunk_size variable as the length of knapsack. 

`chunks = [bits[i:i + chunk_size] for i in range(0, len(bits), chunk_size)]`
This list comprehension work as follow:
- as chunk_size variable is at constant of 8, it creates a chunk in each 8 bits corresponding to each char ascii value.
- iterate in each bit with step of 8
- put the bits[i : i + chunk_size] in the chunks list

Then it iterate for each chunk in the chunks list with contain below:
- check if the len of chunk is less than chunk_size (probably occur in the last slicing) and append a 0 so the length is the same
- the variable c_value is the base$_{10}$ representation but with the reversed MSB with LSB
- now the encrypted_value can be obtained by multiplying the c_value with n(n is random in range of (-1000, 1000)) and mod it with m which have value of 257.
- append the encrypted_value into cipertext list that will be returned

###### Example
```python
Message = 'AB'
bits = convert_to_bits(message)
-> bits = [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0]
chunk_size = 8 
chunks = [bits[i:i + chunk_size] for i in range(0, len(bits), chunk_size)]
-> chunks = [     
	[0, 1, 0, 0, 0, 0, 0, 1],  # Represents 'A'     
	[0, 1, 0, 0, 0, 0, 1, 0]   # Represents 'B' 
	]
c_value = (1 * 0) + (2 * 1) + (4 * 0) + (8 * 0) + (16 * 0) + (32 * 0) + (64 * 0) + (128 * 1) = 130 #c_value of 'A'
encrypted_value = (130 * n) % 257 #encrypted_value of 'A'
```

## Solution
```python
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
```
### Brute-Force
first, create code to decrypt the message with parameter same as encrypt message function.
At the beginning of the function, immediately check whenever the m and n is coprime or not as we can only get the [[Modular Invers]] if $gcd(m,n)$ is 1 or comprime.

After calculating to modular invers, get back the c_value by calculating `(encrypted_value * n_invers) % m`

if we got the c_value, its easy to get back the original value as it only just the decimal representation of inverse bit.
