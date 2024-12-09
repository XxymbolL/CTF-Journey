from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.PublicKey import RSA

# Given values from the original code
n = 75611426846733548074395480486780420981996787746017992648766135297637412285786150518117412694353982730260339956103884006288811320733838224383508053272022147576879837387832237758766368883785181788819830865502742223519174450711328116138334507355907760483294595081173498453913346400135595506222134398989893494557
c = 24212544624137544627332056856124783218030228372400575745228195070749322642454653243200427755138872322964104254459633443311831377773274893652079118515291791542588544740764343640874607587628716007542872080742346529911701255688660521461743298540534157126929059855272833923180385515893193983225857155189935911538
e = 7

# The known part of the message before the colon
known_part = b"ketika bangga menjadi kontingen gemastik UI dan mendapatkan juara umum, tapi anda divisi 2, my honest impression: "

# Step 1: Slice the original ciphertext `c` to focus only on the encrypted part of the flag
# First, find the length of the known part in bytes
known_part_length = len(known_part)

# Convert the known part to a number (long integer)
known_part_long = bytes_to_long(known_part)

# Step 2: Slice the ciphertext based on the length of the known part
# Since the ciphertext is the result of encrypting the message `m` with RSA, we need to assume that the
# part before the colon is the encrypted `known_part` and the rest is the encrypted flag
# The ciphertext `c` is the encrypted version of the message `m = known_part + flag`
# So we need to slice `c` to get the part corresponding to the flag.

# To get the flag's encrypted part, we can subtract the encrypted known part from `c`
c_flag = c - pow(known_part_long, e, n)

# Step 3: Decrypt the remaining part (the flag) using RSA
# Decrypt the flag part of the ciphertext using the private key `d`
d = 1  # In this case, we are simplifying for the example, d=1
flag_encrypted = c_flag
flag_decrypted = pow(flag_encrypted, d, n)

# Convert the long integer back to bytes to reveal the flag
flag = long_to_bytes(flag_decrypted)

# Step 4: Output the decrypted flag
print("Decrypted Flag:", flag.decode(errors='ignore'))

