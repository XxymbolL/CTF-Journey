from pwn import *
import time
import re

# Connect to the server
r = remote('34.101.36.1', 9009)

# Step 1: Respond to the first question (Apa yang sama dengan 1?)
r.recvuntil('Jawab: ')
r.sendline('01')  # Answer with '01' to avoid exit

# Step 2: Handle the multiplication questions
num_questions = 100
for _ in range(num_questions):
    # Read the multiplication question (we expect a format like "Berapa 12 * 15?")
    question = r.recvuntil('?').decode()
    
    # Use regular expression to extract the two numbers
    match = re.search(r'(\d+)\s\*\s(\d+)', question)
    if match:
        a = int(match.group(1))
        b = int(match.group(2))
        # Calculate the answer
        answer = a * b
        
        # Send the answer back
        r.sendline(str(answer))
        
        # Receive the response (Salah! or next question)
        response = r.recvuntil(' ').decode()
        if "Salah!" in response:
            print("Got an incorrect answer, exiting!")
            break
    else:
        print("Failed to match multiplication question format.")
        break

# Step 3: Respond to the sleep question (Mau tidur berapa lama?)
r.recvuntil('Mau tidur berapa lama? ')
questions = -1  # Increase the number of questions to reveal more of the flag
r.sendline(str(questions))
alarm = 130
total_sleep_time = 0

# Calculate the sleep times and send answers
sleep_times = []
for i in range(questions):
    sleep_time = pow(2, i)
    total_sleep_time += sleep_time
    sleep_times.append(sleep_time)

    if total_sleep_time > alarm:
        print(f"Alarm berbunyi dan kamu terbangun")
        break

    print(f"Tidur selama {sleep_time} detik...")
    time.sleep(sleep_time)

# Step 4: Get the flag
r.recvuntil('kamu mendapat: ')
flag_part = r.recvline().decode().strip()
print("Flag received: ", flag_part)

# Close the connection
r.close()

