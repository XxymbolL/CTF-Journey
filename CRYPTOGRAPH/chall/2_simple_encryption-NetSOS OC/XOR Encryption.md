given this xor_encryption.py
```python
from secret import secret, flag

def segment(text):
    return [text[i:i+7] for i in range(0, len(text), 7)]

def cipher(char1, char2):
    return chr(ord(char1) ^ ord(char2))

segments = segment(flag)

ct = ""

for segment in segments:
    for x in range(len(segment)):
        res = cipher(segment[x], secret[x])
        ct += res

print(ct.encode().hex())

# ct = 23743f217c3e012605121378323159452a2d7e5c3f327a19415e0820326203465828252c5f2f2d6b5d2832045f43010e4f0b045e4b4e
```

it looks that this is xor the flag with segment
we need to get the segment back first, the segment function is slicing the flag into 7 byte each segment
so the secret must also 7 bytes, `secret = "???????"`

since we know the first 7 flag must be `NETSOS{`, we can xor once again to get back the secret
