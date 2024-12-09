import socket

def recvuntil(sock, delimiter, buffer_size=1024):
    """
    Receive data from the socket until the delimiter is encountered.
    """
    data = b""
    while not data.endswith(delimiter):
        chunk = sock.recv(buffer_size)
        if not chunk:
            raise ConnectionError("Server closed the connection.")
        data += chunk
    return data

def send_data(sock, data):
    """
    Send data to the socket.
    """
    sock.sendall(data.encode())

def main():
    # Server details
    host = "34.101.36.1"  # Replace with actual server IP
    port = 9100           # Replace with actual port

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("[*] Connected to the server.")

        try:
            # Receive the welcome message and menu
            welcome_msg = recvuntil(s, b">> ")
            print(welcome_msg.decode(), end="")

            # Select option '2' (Get Flag)
            send_data(s, "2\n")
            
            # Wait for prompt to enter the encrypted message
            prompt_msg = recvuntil(s, b": ")
            print(prompt_msg.decode(), end="")

            # Analyze this phase
            test_ciphertext = "41414141414141414141414141414141\n"  # Example placeholder
            send_data(s, test_ciphertext)

            # Capture server response
            response = recvuntil(s, b"\n")
            print(response.decode(), end="")

            # Check for further prompts or errors
            more_response = recvuntil(s, b">> ")
            print(more_response.decode(), end="")

        except ConnectionError as e:
            print(f"[!] Connection Error: {e}")
        except Exception as e:
            print(f"[!] An error occurred: {e}")

if __name__ == "__main__":
    main()

