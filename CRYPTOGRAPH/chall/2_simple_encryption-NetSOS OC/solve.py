flag = "NETSOS{"
ct = "23743f217c3e012605121378323159452a2d7e5c3f327a19415e0820326203465828252c5f2f2d6b5d2832045f43010e4f0b045e4b4e"

ct_char = bytes.fromhex(ct).decode()
print(ct_char)

def segment(text):
    return [text[i:i+7] for i in range(0, len(text), 7)]

def cipher(char1, char2):
    return chr(ord(char1) ^ ord(char2))

segments = segment(ct_char)

secrets = ""

for x in range(len(flag)):
    secret = cipher(segments[x], flag[x])
    secrets += secret

print (secrets)

flags = ""
for segment in segments:
    for x in range(len(segment)):
        res = cipher(segment[x], secrets[x])
        flags += res

print(flags)
