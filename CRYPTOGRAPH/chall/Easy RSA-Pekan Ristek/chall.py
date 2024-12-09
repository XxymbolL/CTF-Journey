from Crypto.Util.number import getPrime, bytes_to_long
from secret import FLAG
from py_ecc.bls12_381 import curve_order

class RSA:
    def __init__(self):
        self.p = getPrime(2048)
        self.q = getPrime(2048)
        self.n = self.p * self.q
        self.e = 0x10001
        self.curve_order = curve_order
    
    def check_proof(self, proof_hex):
        try:
            p_claimed = int(proof_hex[:128], 16) % self.curve_order
            q_claimed = int(proof_hex[128:], 16) % self.curve_order
            
            if p_claimed == 1 or p_claimed == -1 or q_claimed == 1 or q_claimed == -1 or p_claimed == 2 or q_claimed == 2:
                return False
            
            return (p_claimed * q_claimed) % self.curve_order == self.n % self.curve_order

        except:
            return False

def challenge():
    rsa = RSA()
    
    print("Welcome to the Zero Knowledge RSA Proof Challenge!")
    print("Can you factorize this modulus?")
    print(f"RSA Modulus n = {rsa.n}")
    
    while True:
        proof = input("Enter proof (hex): ").strip()
        
        if rsa.check_proof(proof):
            print(f"Congrats!!! You managed to proof it!")
            print(f"This is your reward: {FLAG}")
        else:
            print("Wrong proof :C")

if __name__ == "__main__":
    challenge()