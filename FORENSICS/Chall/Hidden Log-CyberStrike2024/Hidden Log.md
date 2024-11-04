Seorang pengguna melakukan aktivitas yang mencurigakan di dalam sistemnya. Namun, semua bukti yang dapat digunakan untuk menangkap pengguna ini tersembunyi di dalam sebuah file. Investigasilah file ini dan temukan flag yang tersembunyi. Petunjuk: Perhatikan file yang terkandung di dalam file lain dan juga log yang mencurigakan

 [forensic_challenge.zip](https://ssctf.id/files/e6e3d1a9d93e63e43e5b3ab22cc1c78c/forensic_challenge.zip?token=eyJ1c2VyX2lkIjoyNDEsInRlYW1faWQiOjI2LCJmaWxlX2lkIjoxNX0.ZwnoSw.E__oFnuoR9s7DHGKT6j5FkoRhJo)

# Solve
First and Foremost, we do some binwalk in the file
`binwalk forensic_challenge.zip`
which output the following:
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
189           0xBD            Zip archive data, at least v1.0 to extract, compressed size: 25, uncompressed size: 25, name: important.txt
368           0x170           End of Zip archive, footer length: 22
```

it seems nothing strange within the file, so maybe we can find some hint while unzipping the file.
```
❯ unzip forensic_challenge.zip                    ─╯
Archive:  forensic_challenge.zip
warning [forensic_challenge.zip]:  189 extra bytes at beginning or within zipfile
  (attempting to process anyway)
 extracting: important.txt
```
Wait! there are some warning going on while extracting.
but lets check the important.txt first:
```
❯ cat important.txt                                                ─╯
Ini adalah file penting.
❯ binwalk important.txt                                            ─╯

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
```
seems like nothing else going on the file important.txt

let's extract the extra bytes to see the what's hidden behind it!
```
# Extract the first 189 bytes (assuming extra data is at the start)
❯ dd if=forensic_challenge.zip of=extra_data.bin bs=1 count=189

189+0 records in
189+0 records out
189 bytes transferred in 0.001168 secs (161815 bytes/sec)
```

```
❯ hexdump -C extra_data.bin                                        ─╯

00000000  55 73 65 72 20 6c 6f 67  69 6e 20 61 74 74 65 6d  |User login attem|
00000010  70 74 20 66 61 69 6c 65  64 3a 20 32 30 32 34 2d  |pt failed: 2024-|
00000020  31 30 2d 30 33 20 31 32  3a 34 35 3a 32 33 0a 55  |10-03 12:45:23.U|
00000030  73 65 72 20 6c 6f 67 69  6e 20 73 75 63 63 65 73  |ser login succes|
00000040  73 66 75 6c 3a 20 32 30  32 34 2d 31 30 2d 30 33  |sful: 2024-10-03|
00000050  20 31 32 3a 34 36 3a 31  30 0a 46 69 6c 65 20 64  | 12:46:10.File d|
00000060  6f 77 6e 6c 6f 61 64 65  64 3a 20 73 75 73 70 69  |ownloaded: suspi|
00000070  63 69 6f 75 73 5f 66 69  6c 65 2e 7a 69 70 0a 55  |cious_file.zip.U|
00000080  73 65 72 20 6c 6f 67 67  65 64 20 6f 75 74 3a 20  |ser logged out: |
00000090  32 30 32 34 2d 31 30 2d  30 33 20 31 32 3a 35 30  |2024-10-03 12:50|
000000a0  3a 34 35 0a 43 54 46 7b  61 73 6b 64 6a 61 73 6b  |:45.CTF{askdjask|
000000b0  6a 64 31 32 33 32 38 30  39 31 32 7d 0a           |jd123280912}.|
000000bd
```

OH! it can be seen that the flag is `CTF{askdjaskjd123280912}`
