from Crypto.Util.number import getPrime, bytes_to_long, inverse
from py_ecc.bls12_381 import curve_order

# Simulated RSA setup
class RSA:
    def __init__(self):
        self.p = getPrime(2048)
        self.q = getPrime(2048)
        self.n = self.p * self.q
        self.e = 0x10001
        self.curve_order = curve_order

rsa = RSA()

# Step 1: Compute n % curve_order
n_mod_curve = rsa.n % rsa.curve_order

# Step 2: Find valid p_claimed and q_claimed
# Start with any number not violating constraints and adjust
p_claimed = 3  # A valid choice as it’s not 1, -1, or 2
q_claimed = (n_mod_curve * inverse(p_claimed, rsa.curve_order)) % rsa.curve_order

# Ensure q_claimed is valid
if q_claimed in [1, -1, 2]:
    raise ValueError("q_claimed is invalid")

# Step 3: Create proof_hex
proof_hex = f"{p_claimed:0128x}{q_claimed:0128x}"

print("Generated Proof:", proof_hex)

