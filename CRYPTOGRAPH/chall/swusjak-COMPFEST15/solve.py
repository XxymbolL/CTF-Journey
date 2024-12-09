from Crypto.Util.number import long_to_bytes, bytes_to_long

p = 1179478847235411356076287763101027881
e = 0x10001

class MultiplicativeGroup:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(self, other):
        a = (self.a * other.a - 6969 * self.b * other.b) % p
        b = (self.a * other.b + self.b * other.a - 69 * self.b * other.b) % p
        return MultiplicativeGroup(a, b)

    def __pow__(self, n):
        res = MultiplicativeGroup(1, 0)
        base = self
        while n:
            if n & 1:
                res *= base
            base *= base
            n >>= 1
        return res

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def decrypt_block(enc_block):
    a = enc_block % p
    b = enc_block // p
    enc_m = MultiplicativeGroup(a, b)
    d = modinv(e, (p - 1))
    dec_m = enc_m ** d
    return dec_m.a + dec_m.b * p

def block_to_bytes(blocks):
    res = 0
    for i in range(len(blocks) - 1, -1, -1):
        res *= p**2
        res += blocks[i]
    return long_to_bytes(res)

# Read encrypted data
with open("flag.enc", "rb") as f:
    enc_data = f.read()

# Process into blocks
enc_blocks = []
msg_int = bytes_to_long(enc_data)
while msg_int:
    enc_blocks.append(msg_int % (p**2))
    msg_int //= p**2

# Decrypt blocks
dec_blocks = [decrypt_block(block) for block in enc_blocks]

# Validate decryption and correct padding if necessary
try:
    flag = block_to_bytes(dec_blocks)
    print("Decryption successful.")
except ValueError as e:
    print("Error in decryption:", e)

# Save result
with open("flag_dec_final.png", "wb") as f:
    f.write(flag)

