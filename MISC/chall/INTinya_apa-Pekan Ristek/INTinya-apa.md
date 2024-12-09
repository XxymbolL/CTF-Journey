## [100 pts] INTinya-apa

###### Description

siapa suka ngitung? bantu itungin dong

Author: Ultramy

`nc 34.101.36.1 9009`

Flag = `NETSOS{intinya_biar_gabisa_ngitung_manual_tapi_kalo_jago_ttp_bisa_sih_3a00da3a18}`

given source code:
```python
import time
import sys
import random
import time
import sys

flag = "NETSOS{sample}"

print("Sebelum main aku tes dulu ya")
questions2 = input("Apa yang sama dengan 1? Jawab: ")
ans = int(questions2)

if questions2 == "1":
    print("Coba lagi")
    sys.exit()

if "," in questions2:
    print("Coba lagi")
    sys.exit()

if "-" in questions2:
    print("Coba lagi")
    sys.exit()

if "+" in questions2:
    print("Coba lagi")
    sys.exit()

if ans != 1:
    print("Coba lagi")
    sys.exit()

print("Nice, sekarang kita mulai permainannya!")
num_questions = 100

for _ in range(num_questions):
    a = random.randint(10, 30)
    b = random.randint(10, 30)
    answer = a * b
    start_time = time.time()

    try:
        user_input = int(input(f"Berapa {a} * {b}? "))
        end_time = time.time()
        if end_time - start_time > 2:
            print("cepetin dong")
            sys.exit()

        if user_input != answer:
            print("Salah!")
            sys.exit()

    except ValueError:
        print("Invalid!")
        sys.exit()

print("GG! Pasti cape, waktunya tidur zzz...")

questions = int(input("Mau tidur berapa lama? "))
alarm = 130
total_sleep_time = 0

for i in range(questions):
    sleep_time = pow(2, i)
    total_sleep_time += sleep_time

    if total_sleep_time > alarm:
        print(f"Alarm berbunyi dan kamu terbangun")
        sys.exit(1)

    print(f"Tidur selama {sleep_time} detik...")
    time.sleep(sleep_time)

print("Dalam mimpimu kamu mendapat: " + flag[:questions])
```

The first problem that arise is when asked about what number is similar to 1, without using any of this symbol{+,.,-}, hence **01**.

The second problem arise,
since it required to perform massive calculation in short period of time, it required to do automatically with python automation.

the third problem is when asked on how long we sleep, this create a problem because the max sleep time is 130 while the more we input the more exponentially grow the sleep time. Also, the time here is required to get the flag as we need the slicing to be maximized. hence, input -1 is still valid and will slice the string to 1 before last index of string flag.


Solve:
```python
from pwn import *
import time
import re


r = remote('34.101.36.1', 9009)


r.recvuntil('Jawab: ')
r.sendline('01')

num_questions = 100
for _ in range(num_questions):
    question = r.recvuntil('?').decode()
    match = re.search(r'(\d+)\s\*\s(\d+)', question)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        answer = a * b
        r.sendline(str(answer))
        response = r.recvuntil(' ').decode()
        if "Salah!" in response:
            print("Got an incorrect answer")
            break
    else:
        print("Failed to match multiplication question format.")
        break


r.recvuntil('Mau tidur berapa lama? ')
questions = -1
r.sendline(str(questions))

r.recvuntil('kamu mendapat: ')
flag_part = r.recvline().decode().strip()
print(flag_part)
r.close()
```