import requests

BASE_URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/"
flag = ""
n = 31
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_!{}[]?/"

while len(flag) == 0 or flag[-1] != "}":
    plaintext1 = "ab" * n
    cipher1_response = requests.get(BASE_URL + plaintext1.encode().hex() + "/")
    cipher1 = cipher1_response.json()["ciphertext"]

    for ch in alphabet:
        plaintext2 = ("ab" * n + ch).encode().hex()
        cipher2_response = requests.get(BASE_URL + plaintext2 + "/")
        cipher2 = cipher2_response.json()["ciphertext"]

        if cipher1[32:48] == cipher2[32:48]:  # Compare the correct block
            flag += ch
            print(f"Current flag: {flag}")
            break

    n += 1

print(f"Recovered flag: {flag}")

