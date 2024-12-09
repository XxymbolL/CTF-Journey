import socket
from Crypto.Util.number import bytes_to_long, long_to_bytes
from py_ecc.bls12_381 import curve_order


def compute_proof(n):
    """
    Compute a valid proof based on the modulus `n`.
    """
    p_claimed = 3  # Example: Choose small valid values
    q_claimed = pow(n, -1, curve_order) * 3 % curve_order  # Modular inverse of `n` mod curve_order, scaled by 3

    # Ensure the proof satisfies the conditions
    assert (p_claimed * q_claimed) % curve_order == n % curve_order
    proof = f"{p_claimed:0128x}{q_claimed:0128x}"
    return proof


def main():
    host = "34.101.36.1"
    port = 9016

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Receive welcome message
        response = s.recv(4096).decode()
        print(response)

        # Parse modulus `n` from the server's response
        lines = response.splitlines()
        for line in lines:
            if "RSA Modulus n =" in line:
                n = int(line.split("=")[1].strip())
                break

        # Generate the proof
        proof = compute_proof(n)

        # Send the proof
        s.sendall(proof.encode() + b"\n")

        # Receive the server's response
        response = s.recv(4096).decode()
        print(response)


if __name__ == "__main__":
    main()

