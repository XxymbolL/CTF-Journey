from Crypto.Util.number import long_to_bytes
from math import gcd, sqrt

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inverse_mod(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m

# Given values
q = 100030868936662823974280475437726758792108049671585106587368083120441191552561661791371214308294761989583805012156039761474002459351077511500925372820399761061091840156879390124291998820813893329355372121872594634337653186988495289479782496551127655317223259483509331193578574322152311718209760723145599099081
h = 15339958133673884223011396622251891594086618196858881296538274407954414819691806449185256800344482499951325693672290396016641925678227339657298660891756245492601867480561644261829881192242150335691747262205734925765139964637276361805884538307565788917954906645522196786690734068852380611685467498982614705992
e = 31999352162817863414077755367432123914513636949900959298008573011077958012781585033034156921504631925374669097646629268416960797271591570302923820577730633679308082190843803869879569134586782970288418209510174514078496160511525371898784666247422187349130552468747763895877602156728200606673024994343791869671

# Calculate bounds
upperb = int(sqrt(q // 2))
lowerb = int(sqrt(q // 4))

print(f"Search bounds: {lowerb} to {upperb}")

# Key observation: f * h ≡ g mod q
# Since g is in [lowerb, upperb], we can try small values of f

def try_decrypt(f, q, h, e):
    try:
        # Calculate potential g
        g = (f * h) % q
        if not (lowerb <= g <= upperb):
            return None
        
        if gcd(f, g) != 1:
            return None
            
        # Try decryption
        a = (f * e) % q
        m = (a * inverse_mod(f, g)) % g
        
        # Try to decode and check if it looks like a flag
        flag = long_to_bytes(m)
        if b'flag' in flag.lower() or b'ctf' in flag.lower():
            return flag
    except:
        return None
    return None

# Try small f values since we know f is small
for f in range(2, 1000):
    if f % 100 == 0:
        print(f"Trying f = {f}")
    result = try_decrypt(f, q, h, e)
    if result:
        print(f"Found flag with f = {f}:")
        print(result.decode())
        break

# If the above fails, try backwards from upperbound
if not result:
    for f in range(upperb, upperb - 1000, -1):
        if f % 100 == 0:
            print(f"Trying f = {f}")
        result = try_decrypt(f, q, h, e)
        if result:
            print(f"Found flag with f = {f}:")
            print(result.decode())
            break
