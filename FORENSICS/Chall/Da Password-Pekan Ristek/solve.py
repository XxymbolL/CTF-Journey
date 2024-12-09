import zipfile

# Path to the ZIP file and password file
zip_file_path = 'flag.zip'
password = '43=29c.f]7f^Bf+72!'  # Use the password directly

# Function to extract using the password
def extract_zip(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode())  # Password should be encoded to bytes
        print(f"Password found: {password}")
        return True
    except (RuntimeError, zipfile.BadZipFile):
        print("Password is incorrect.")
        return False

# Open the ZIP file and attempt extraction with the password
with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
    if extract_zip(zip_file, password):
        print("Extraction successful!")
    else:
        print("Failed to extract ZIP file with the given password.")

