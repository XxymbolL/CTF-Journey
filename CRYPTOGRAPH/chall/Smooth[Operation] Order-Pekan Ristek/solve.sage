from Crypto.Util.number import long_to_bytes
from sage.all import *

# Define the elliptic curve parameters
p = 0xa5dad2cb65b65ab89ed2248be2971c0d
a, b = 0x30f053bb9020808b81da81c50a1a7c21, 0x189f0bef55f3c0ef3cf1e04d6efd41e2

# Create the elliptic curve E over the finite field GF(p)
E = EllipticCurve(GF(p), [a, b])

# Define the base point P
P = E(0x4db87652e8891721e7460f359b008588, 0x912992fe31e3b97d49bf423678341915)

# Function to recover the FLAG from secrets
def recover_flag(secret_1, secret_2):
    # Convert secrets back to bytes
    flag_part1 = long_to_bytes(secret_1)
    flag_part2 = long_to_bytes(secret_2)
    
    # Concatenate the two parts to form the original FLAG
    return flag_part1 + flag_part2

# Example secrets (replace these with the actual recovered secrets)
secret_1 = 141871326394037957187833263626514911585  # Example value for secret_1
secret_2 = 125844234866178483352217905750283979760  # Example value for secret_2

# Recover the FLAG
recovered_flag = recover_flag(secret_1, secret_2)

# Print the recovered FLAG
print("Recovered FLAG:", recovered_flag)