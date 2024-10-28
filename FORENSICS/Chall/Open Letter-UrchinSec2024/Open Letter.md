#Forensics #medium

UrchinSec has issued an important letter to all participants in this year’s Aware CTF. But something unexpected lies within the document, concealed from plain sight. Your task is to analyze the letter carefully and uncover the hidden message and help the admin.

_Can you reveal what’s hidden in the open letter?_

# Solve
first use **binwalk** extract to get the metadata of the file, in this case is _word_ file.
```bash
binwalk -e Open\ Letter.docx
-> _Open\ Letter.docx.extracted
```
after got the folder, directly change the directory to the extracted docx.

then use grep with recursive command in case that the flag contains in one of the .xml
```bash
❯ grep -r "urchinsec{" .                            ─╯

./word/settings.xml:		<w:message w:val="Here is the Admin password: urchinsec{w0rd2z1p_zip2w0rd_c9f2d3a0}"/></w:reminder>
```

Ergo, we directly get the flag as `urchinsec{w0rd2z1p_zip2w0rd_c9f2d3a0}`