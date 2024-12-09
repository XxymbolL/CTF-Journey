from sage.all import *

# Define the elliptic curve
E = EllipticCurve(GF(p), [a, b])

# Compute the order of the elliptic curve
n = E.order()

# Factor the order into small prime powers
factors = n.factor()
primes = [p for p, _ in factors]

# Compute the discrete logarithm for each prime power
xi_values = []
for prime in primes:
    e = factors[prime]
    Qi = Q1 if prime == 2 else Q2  # use Q1 for prime 2, Q2 for other primes
    xi = baby_step_giant_step(Qi, P, prime^e)
    xi_values.append((xi, prime^e))

# Use the CRT to combine the xi values
secret_1 = crt(xi_values, [prime^e for prime, e in factors])
secret_2 = crt(xi_values, [prime^e for prime, e in factors])

# Recover the original FLAG
FLAG = bytes_to_long(secret_1).to_bytes(16, 'big') + bytes_to_long(secret_2).to_bytes(16, 'big')

print(FLAG)
