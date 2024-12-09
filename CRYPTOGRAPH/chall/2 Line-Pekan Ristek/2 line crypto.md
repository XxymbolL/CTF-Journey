## [100 pts] two line crypto

###### Description

ez nimah, (teksnya bahasa inggris)

Author: kejuwafel (upi)



given source code:
```python
n = open('plaintext', 'r').read()
print(''.join(chr(ord(a) ^ ord(b)) for a, b in zip(n, n[1:])), file=open('ciphertext', 'w'))
```
and the ciphertext

since it was just XOR encryption, using XOR property which is:
a xor b = c
then
a xor c = b or b xor c = a

we can perform a reverse on the ciphertext by performing xor of the first char with an bruteforce ASCII char until found the intended one or containing the flag

```python
ciphertext = open('ciphertext', 'r').read()

def brute_force_decryption(ciphertext, target_substring):
    for guess in range(32, 127):  
        plaintext = [chr(ord(ciphertext[0]) ^ guess)]
        for i in range(1, len(ciphertext)):
            plaintext.append(chr(ord(ciphertext[i - 1]) ^ ord(plaintext[i - 1])))

        # Check if contain specific word
        decrypted_text = ''.join(plaintext)
        if target_substring in decrypted_text:
            print(f"Found target '{target_substring}' with first character guess: {chr(guess)}")
            
            for line in decrypted_text.splitlines():
                if target_substring in line:
                    return line


    print(f"Target '{target_substring}' not found in plaintext.")
    return None


target_substring = "NETSOS"

found_line = brute_force_decryption(ciphertext, target_substring)

if found_line:
    print(found_line)
```

