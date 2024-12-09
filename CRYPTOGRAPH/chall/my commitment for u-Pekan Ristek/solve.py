from pwn import *
import sympy

# Function to solve the discrete logarithm (returns None if it doesn't exist)
def solve_discrete_log(C, base, mod):
    try:
        return sympy.discrete_log(C, base, mod)
    except ValueError:
        return None  # Log doesn't exist

def main():
    conn = remote("34.101.36.1", 9017)
    
    # Receive p, g, and B from the server
    conn.recvuntil("p = ")
    p = int(conn.recvline().strip())
    
    conn.recvuntil("g = ")
    g = int(conn.recvline().strip())
    
    conn.recvuntil("B = ")
    B = int(conn.recvline().strip())
    
    print(f"p: {p}, g: {g}, B: {B}")
    
    # Step 1: Create your commitment
    # Assume we need to choose a random value v
    v = 123456  # Replace with your chosen value for v (or use a random value)
    
    # Step 2: Compute C1 = g^v * B^s % p
    # Let's assume s = 0 for now (or choose s based on the problem)
    s = 0
    
    C1 = (pow(g, v, p) * pow(B, s, p)) % p
    print(f"Commitment C1: {C1}")
    
    # Step 3: Compute the discrete logarithms
    log_g = solve_discrete_log(C1, g, p)  # log_g is the discrete log of C1 to base g
    log_B = solve_discrete_log(C1, B, p)  # log_B is the discrete log of C1 to base B
    
    if log_g is not None and log_B is not None:
        print(f"Found log_g: {log_g}, log_B: {log_B}")
        
        # Now, compute v and s based on the log values.
        v = log_g
        s = log_B
        
        # Send v and s to the server
        conn.sendlineafter("Enter v: ", str(v))
        conn.sendlineafter("Enter s: ", str(s))
        
        # Get the result of the commitment
        conn.recvuntil("Your commitment is: ")
        commitment = conn.recvline().strip()
        print(f"Server's commitment: {commitment}")
    
    else:
        print("Discrete logarithm calculation failed.")
        # Handle failure cases, maybe with an alternate approach or brute force
    
    conn.close()

if __name__ == "__main__":
    main()

