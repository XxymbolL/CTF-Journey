Given file below:
![[sqwrd.jpg]]

It seems that we can find hidden flag in the image given.

# Solve
Let's start with basic enumeration
By doing exiftool, we got detail info below:
```
❯ exiftool sqwrd.jpg                                 ─╯
ExifTool Version Number         : 12.76
File Name                       : sqwrd.jpg
Directory                       : .
File Size                       : 124 kB
File Modification Date/Time     : 2023:09:23 13:29:25+07:00
File Access Date/Time           : 2024:10:29 10:58:11+07:00
File Inode Change Date/Time     : 2024:10:29 10:58:08+07:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 96
Y Resolution                    : 96
Comment                         : The sender's name is written on the image.
Image Width                     : 750
Image Height                    : 693
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 750x693
Megapixels                      : 0.520
```

there are detail on comment where it says that the sender's name is written on the image.
`RJPTSBNSUtBRUwgVE8gUk9CRVJU`
Lets save it for later...

The next step must be to extract the image using binwalk as it contain compressed data:
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
69916         0x1111C         xz compressed data
```

`binwalk -e sqwrd.jpg` should extract the image

it result in appearance of file 1111C as it the binary offset separated from image.

Analyzing the file, it seems that it was TAR file
```
❯ exiftool 1111C                                     ─╯
ExifTool Version Number         : 12.76
File Name                       : 1111C
Directory                       : .
File Size                       : 61 kB
File Modification Date/Time     : 2024:10:29 11:08:42+07:00
File Access Date/Time           : 2024:10:29 11:09:31+07:00
File Inode Change Date/Time     : 2024:10:29 11:08:42+07:00
File Permissions                : -rw-r--r--
File Type                       : TAR
File Type Extension             : tar
MIME Type                       : application/x-tar
Warning                         : Unsupported file type
```

using `tar -xf 1111C` resulting in pdf file entitled `message.pdf`

![[message.pdf]]

it looks like the `message.pdf` had hidden message inside the pdf that supposed to be the organ that needed to fulfill the flag which require `sender_organ_receiver`



