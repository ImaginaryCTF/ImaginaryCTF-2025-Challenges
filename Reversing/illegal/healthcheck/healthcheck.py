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
#print(conn.recvuntil(b'== proof-of-work: '))
#if conn.recvline().startswith(b'enabled'):
#   handle_pow(r)


conn.sendline(b"3217339")
conn.sendline(b"eSwRuQyrmu3NaktW/FScH1yWNsUqFq1SwS9jI333/E8L9r3q8Uz/HBEPgz/olIiOVSXp/N3Z75tyMEHokO1pUzKRAvJt81L/YD2pl+nAlgbZUCjGyGYe5vwWA2+PHwgWZqsknYBrVz5URNiC1nOSyDR7ZEQBSmHHROE+GnG0tiKYBk2YbXx6Ltyhw6LUEnvgROqb2D9sFOpzdtCIlxIAq4Ya5TSLXN7zhyEU4sSbRwUNRgXZg28T2gLUlMMY9kXSrdiwvTOrVywN3K5/EA+SxJr8HpYcKKFaAROVBkqbmdatfgSgCCIq1A1cFi2M1b4jKmQPwFV5V2UD9IdStP0YFhwawIYqlB5vS6/XrYVk1q4rHbmbOD2FgzPTKMZj+wg0fw6rIfr6iuSOgaR666xtUbg95WKGkU/cIHYsogv48El5Fsc5kh0Ft6yOu4medb2qA3KAhVFS8hLWNa2fGWKuEvD1N/HjEp/DpJeXbpRhfZPLPogLrEiYFkHibVn5wXTFAEgTsNHlmufG4Z5AO4K/Yn+B1dp8wibrfAEig97mXq5s/rfe0fGElvjPB5P4ANTV4uxzTrM+7UBDUnPQh45LpD6jthCmtZtYqKQ2f2ErmkzFrroLctB1p2jy/9KpYSQOUB4QschGKTnfWyS9/mT5aOYR4epOvLXrTTJIRagzW363zSnv8mNIyJVkM4N8oDAPGPKdydVZHsQjnErG8g==")
res = conn.recvall()
print(res)
conn.close()

if b"ictf{" in res:
    exit(0)
exit(1)
