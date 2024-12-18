from Crypto.Util.number import bytes_to_long

p = 0xa5dad2cb65b65ab89ed2248be2971c0d
a, b = 0x30f053bb9020808b81da81c50a1a7c21, 0x189f0bef55f3c0ef3cf1e04d6efd41e2

E = EllipticCurve(GF(p), [a, b])

P = E(0x4db87652e8891721e7460f359b008588, 0x912992fe31e3b97d49bf423678341915)

FLAG = b"REDACTED"

assert len(FLAG) == 34

secret_1, secret_2 = bytes_to_long(FLAG[:16]), bytes_to_long(FLAG[16:])
Q1, Q2 = secret_1 * P, secret_2 * P

print(Q1)
print(Q2)

# (141871326394037957187833263626514911585 : 174098354046021519394739744751443534570 : 1)
# (125844234866178483352217905750283979760 : 64010582201626611563220522021101030460 : 1)