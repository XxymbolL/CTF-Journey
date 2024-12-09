from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
import random
import math

FLAG = b'[redacted]'

def gen_key():

    q = getPrime(1024)
    upperb = int(math.sqrt(q // 2))
    lowerb = int(math.sqrt(q // 4))
    f = random.randint(2, upperb)

    while True:
        g = random.randint(lowerb, upperb)
        if math.gcd(f, g) == 1:
            break
    h = (inverse(f, q) * g) % q
        
    return (q, h), (f, g)


def encrypt(q, h, m):

    assert m < int(math.sqrt(q // 2))
    r = random.randint(2, int(math.sqrt(q // 2)))
    e = (r * h + m) % q

    return e
    

def decrypt(q, h, f, g, e):

    a = (f * e) % q
    m = (a * inverse_mod(f, g)) % g

    return m

pub, priv = gen_key()
q, h = pub
f, g = priv

e = encrypt(q, h, bytes_to_long(FLAG))

print(f'Public key: {(q,h)}')
print(f'Encrypted Flag: {e}')
