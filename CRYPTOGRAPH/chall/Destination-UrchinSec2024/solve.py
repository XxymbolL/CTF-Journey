# Open the file and read the contents
with open('chall.txt', 'r') as file:
    # Read the line and convert it to a list of integers
    numbers = list(map(int, file.readline().strip().split()))

# Adjust the numbers so that 'a' corresponds to 97 (ASCII)
decoded_string = ''.join(chr(num-1) for num in numbers)

# Print the decoded string
print(decoded_string)

