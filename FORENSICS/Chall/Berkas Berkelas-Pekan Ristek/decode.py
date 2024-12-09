import base64

with open("cGFzc3dvcmQ9aW5pc29hbGZvcmVu.zip", "rb") as file:
    encoded_data = file.read()

decoded_data = base64.b64decode(encoded_data)

with open("decoded_file.zip", "wb") as out_file:
    out_file.write(decoded_data)

