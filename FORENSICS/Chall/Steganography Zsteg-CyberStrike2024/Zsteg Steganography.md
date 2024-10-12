You are given an image file named `hidden_flag.png` that contains embedded data (steganography). Your task is to analyze the image, find the hidden flag, and explain the method used to conceal the flag.

# Solve
```bash
❯ zsteg ctf.png                            
b1,r,lsb,xy         .. text: "CTF{hidden_flag}"
b4,bgr,msb,xy       .. file: MPEG ADTS, layer I, v2, Monaural
```

found flag
`CTF{hidden_flag}`