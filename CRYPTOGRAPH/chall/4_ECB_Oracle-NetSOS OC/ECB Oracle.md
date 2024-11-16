https://aes.cryptohack.org/ecb_oracle/

given source:
```python
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad 
KEY = ? 
FLAG = ? 


@chal.route('/ecb_oracle/encrypt/<plaintext>/') 
def encrypt(plaintext): 
	plaintext = bytes.fromhex(plaintext) 
	padded = pad(plaintext + FLAG.encode(), 16) 
	cipher = AES.new(KEY, AES.MODE_ECB) 
	try: 
		encrypted = cipher.encrypt(padded) 
	except ValueError as e: 
		return {"error": str(e)} 
	return {"ciphertext": encrypted.hex()}
```

padded = pad(plaintext + FLAG.encode(), 16) 
the padding is plaintext + FLAG
when test the plaintext as 'a', the output is
`{"ciphertext":"fc77218fdd7ec0824480746c9fc55ca47a55b6b6959613d98c9b0976d44818a6"}`

```
fc77218fdd7ec0824480746c9fc55ca4
7a55b6b6959613d98c9b0976d44818a6
```

there are 2 blocks, lets test with other plaintext
test with this long plaintext `ababababababababababababababababababababababababababababababababababababababababababababababababababababababab`

```
6e28e4534fb3ad0782a3f8e57ab849a1
6e28e4534fb3ad0782a3f8e57ab849a1
6e28e4534fb3ad0782a3f8e57ab849a1
f657bc1fa2d64ea7ce67b1a46597a465
434922b13621857cef31d035e6ffb0c5
9863b1089f6206d6e75e071a1d6574e4
```

the pattern 
6e28e4534fb3ad0782a3f8e57ab849a1
6e28e4534fb3ad0782a3f8e57ab849a1
6e28e4534fb3ad0782a3f8e57ab849a1

is repeating
