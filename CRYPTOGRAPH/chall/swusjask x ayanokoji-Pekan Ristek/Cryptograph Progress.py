from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long

p,q = getPrime(512), getPrime(512)

n = p * q

message = b"REDACTED"
m = bytes_to_long(message)

e = 7

c = pow(m, e, n)

print(f"truncated message = {message[:-15]}")
print(f"n = {n}")
print(f"c = {c}")

# Output
# truncated message = b'ketika bangga menjadi kontingen gemastik UI dan mendapatkan juara umum, tapi anda divisi 2, my honest impression: '
# n = 75611426846733548074395480486780420981996787746017992648766135297637412285786150518117412694353982730260339956103884006288811320733838224383508053272022147576879837387832237758766368883785181788819830865502742223519174450711328116138334507355907760483294595081173498453913346400135595506222134398989893494557
# c = 24212544624137544627332056856124783218030228372400575745228195070749322642454653243200427755138872322964104254459633443311831377773274893652079118515291791542588544740764343640874607587628716007542872080742346529911701255688660521461743298540534157126929059855272833923180385515893193983225857155189935911538