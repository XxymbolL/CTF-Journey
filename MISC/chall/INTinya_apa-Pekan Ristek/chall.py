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
