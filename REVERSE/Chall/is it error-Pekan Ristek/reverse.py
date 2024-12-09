import os
import struct
import time

# Path to the given .pyc file
pyc_file = "chall.pyc"

# Open the .pyc file
with open(pyc_file, 'rb') as f:
    # Read the original header (first 16 bytes)
    original_header = f.read(16)
    # Print the first 16 bytes to inspect the header (for debugging)
    print(f"Original header: {original_header.hex()}")

# Magic number for Python 3.10
magic_number = b'\x4c\x0f\x0d\x0a'

# Get current timestamp (Unix time)
timestamp = int(time.time())

# Estimate file size based on the .pyc file
file_size = os.path.getsize(pyc_file)

# Pack the new header
new_header = struct.pack('4s I I', magic_number, timestamp, file_size)

# Open the new .pyc file to write the updated header
with open("fixed_chall.pyc", "wb") as new_f:
    new_f.write(new_header)
    
    # Write the rest of the .pyc bytecode (after the original 16-byte header)
    with open(pyc_file, 'rb') as original_f:
        original_f.seek(16)  # Skip the original header
        new_f.write(original_f.read())

print("Header fixed and new .pyc file created: fixed_chall.pyc")

