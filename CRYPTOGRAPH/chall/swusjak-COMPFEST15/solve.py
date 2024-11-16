from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy import mod_inverse

# Constants
p = 1179478847235411356076287763101027881
e = 0x10001

# Function to convert bytes to blocks
def bytes_to_block(msg: bytes):
    res = []
    msg_int = bytes_to_long(msg)
    while msg_int:
        res.append(msg_int % (p**2))
        msg_int //= p**2
    return res

# Function to convert blocks back to bytes
def block_to_bytes(blocks: list[int]):
    res = 0
    for i in range(len(blocks) - 1, -1, -1):
        res *= p**2
        res += blocks[i]
    return long_to_bytes(res)

# MultiplicativeGroup class for encryption and decryption
class MultiplicativeGroup:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __mul__(self, other) -> "MultiplicativeGroup":
        a = (self.a * other.a - 6969 * self.b * other.b) % p
        b = (self.a * other.b + self.b * other.a - 69 * self.b * other.b) % p
        return MultiplicativeGroup(a, b)

    def __pow__(self, n) -> "MultiplicativeGroup":
        res = MultiplicativeGroup(1, 0)
        base = self
        while n:
            if n & 1:
                res *= base
            base *= base
            n >>= 1
        return res
    
    def __repr__(self):
        return f"({self.a}, {self.b})"

# Function to decrypt a block
def decrypt_block(c):
    a = c % p
    b = c // p
    m = MultiplicativeGroup(a, b)
    d = mod_inverse(e, p - 1)  # Modular inverse of e mod (p-1)
    m_dec = m ** d
    return m_dec.a + m_dec.b * p

if __name__ == "__main__":
    # Read encrypted flag from file
    with open("flag.enc", "rb") as f:
        enc = f.read()

    # Split the encrypted data into blocks
    encrypted_blocks = bytes_to_block(enc)

    # Decrypt each block
    decrypted_blocks = []
    for c in encrypted_blocks:
        decrypted_blocks.append(decrypt_block(c))

    # Convert decrypted blocks back to bytes
    decrypted_flag = block_to_bytes(decrypted_blocks)

    # Save the decrypted flag (which should be a PNG file)
    with open("recovered_flag.png", "wb") as f:
        f.write(decrypted_flag)

    print("Decryption complete. Recovered flag saved as 'recovered_flag.png'.")

