from secret import FLAG, p, g, b

def setup():
    B = pow(g, b, p)
    return p, g, B, b 

def commit(v, s, g, B, p):
    return (pow(g, v, p) * pow(B, s, p)) % p

def challenge():
    p, g, B, _ = setup()
    
    print("Welcome to my Commitment Challenge!")
    print("This is some public parameters for u:")
    print(f"p = {p}")
    print(f"g = {g}")
    print(f"B = {B}")
    
    try:
        print("\nCreate your commitment!")
        v = int(input("Enter v: "))
        s = int(input("Enter s: "))
        commitment = commit(v, s, g, B, p)
        print(f"Your commitment is: {commitment}")
        
        print("\nOpen your commitment with different values!")
        v2 = int(input("Enter v': "))
        s2 = int(input("Enter s': "))
        commitment2 = commit(v2, s2, g, B, p)
        
        if v == v2 and s == s2:
            print("You used same values! Denied!")
            return
        
        if commitment == commitment2:
            print("\nCongratulations! You managed to break my commitment scheme!")
            print(f"Flag: {FLAG}")
        else:
            print("\nSorry, that's not correct :c")
    
    except ValueError:
        print("Invalid input!")
        
if __name__ == "__main__":
    challenge()