#cryptography #easy

Take me to my destination 😫

given chall.txt as below:
```
118 115 100 105 106 111 116 102 100 124 66 84 68 74 74 96 117 115 53 111 116 103 49 115 110 96 50 99 105 57 102 54 126
```

this problem seems to be an decimal representation of something.
# Solve
![[Screenshot 2024-10-28 at 09.31.25.png]]
Using [Cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Decimal('Space',false)&input=MTE4IDExNSAxMDAgMTA1IDEwNiAxMTEgMTE2IDEwMiAxMDAgMTI0IDY2IDg0IDY4IDc0IDc0IDk2IDExNyAxMTUgNTMgMTExIDExNiAxMDMgNDkgMTE1IDExMCA5NiA1MCA5OSAxMDUgNTcgMTAyIDU0IDEyNgo&oeol=NEL) it seems that it was not an ordinary decimal representation of char.

because the known flag format is `urchinsec{flag}` it known that the first 10 chunk must be `urchinsec{` 

as the first one is 118 and the 'u' ASCII representation is 117, it need to be subtracted first by 1 before decoded into ASCII char.

## Code
```python
# Open the file and read the contents
with open('chall.txt', 'r') as file:
    # Read the line and convert it to a list of integers
    numbers = list(map(int, file.readline().strip().split()))

# Adjust the numbers so that 'a' corresponds to 97 (ASCII)
decoded_string = ''.join(chr(num-1) for num in numbers)

# Print the decoded string
print(decoded_string)
```

by running the script, we can get the flag as follows:
`urchinsec{ASCII_tr4nsf0rm_1bh8e5}`