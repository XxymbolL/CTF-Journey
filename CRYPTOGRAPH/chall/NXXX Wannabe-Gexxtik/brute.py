from Crypto.Util.number import long_to_bytes
import math

def inverse_mod(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

# Challenge parameters from enc_text.txt
q = 100030868936662823974280475437726758792108049671585106587368083120441191552561661791371214308294761989583805012156039761474002459351077511500925372820399761061091840156879390124291998820813893329355372121872594634337653186988495289479782496551127655317223259483509331193578574322152311718209760723145599099081
h = 15339958133673884223011396622251891594086618196858881296538274407954414819691806449185256800344482499951325693672290396016641925678227339657298660891756245492601867480561644261829881192242150335691747262205734925765139964637276361805884538307565788917954906645522196786690734068852380611685467498982614705992
e = 31999352162817863414077755367432123914513636949900959298008573011077958012781585033034156921504631925374669097646629268416960797271591570302923820577730633679308082190843803869879569134586782970288418209510174514078496160511525371898784666247422187349130552468747763895877602156728200606673024994343791869671

# Calculate bounds based on original encryption code
upperb = int(math.sqrt(q // 2))
lowerb = int(math.sqrt(q // 4))

def try_decrypt(f, g):
    try:
        # Calculate a = f * e mod q
        a = (f * e) % q
        # Recover m using the decryption function
        m = (a * inverse_mod(f, g)) % g
        
        # Convert to bytes and check if it looks like a flag
        flag = long_to_bytes(m)
        # Most CTF flags are ASCII printable and contain 'flag'
        if all(32 <= b <= 126 for b in flag):
            return flag
    except:
        return None
    return None

def find_flag():
    print("Starting decryption...")
    
    # Based on the original code's bounds
    f_start = 2
    f_end = min(1000, upperb)  # Start with smaller range
    
    for f in range(f_start, f_end):
        if f % 100 == 0:
            print(f"Trying f = {f}")
            
        # Calculate potential g based on relationship between f and h
        g = (f * h) % q
        
        if lowerb <= g <= upperb and math.gcd(f, g) == 1:
            result = try_decrypt(f, g)
            if result:
                print(f"\nFound potential flag with f={f}, g={g}")
                print(f"Flag: {result}")
                return

    print("No flag found in current range")

if __name__ == "__main__":
    find_flag()
