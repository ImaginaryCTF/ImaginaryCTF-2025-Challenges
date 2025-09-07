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
import base64
import argparse



def handle_pow(r):
    r.recvuntil(b'python3 ')
    r.recvuntil(b' solve ')
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    r.recvuntil(b'Correct\n')


def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8 or 1, 'big')

def conv_array_to_number(L):
    out = 0
    for i in reversed(L):
        out = (out << 32) + i
    return out

def init_genrand(n, seed):
    state = [0] * n
    state[0] = seed & 0xFFFFFFFF
    for i in range(1, n):
        state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xFFFFFFFF
    return state

def invert_init_array(target_state):
    n = 624
    init_key = [0] * n
    initial_state = init_genrand(n, 19650218)
    state = target_state[:]
    state[0] = state[-1]

    i = 2
    for _ in range(n - 1):
        i -= 1
        if i == 0:
            i = n - 1
        prev = state[i - 1]
        mix = (prev ^ (prev >> 30)) & 0xFFFFFFFF
        state[i] = (state[i] + i) & 0xFFFFFFFF
        state[i] = (state[i] ^ (mix * 1566083941)) & 0xFFFFFFFF

    i, j = 2, 0
    final_state = state[:]

    for _ in range(n):
        if j == 0:
            j = n
        if i == 1:
            state[0] = state[-1]
            i = n
        i -= 1
        j -= 1
        prev = state[i - 1]
        mix = (prev ^ (prev >> 30)) & 0xFFFFFFFF
        temp = (initial_state[i] ^ (mix * 1664525)) & 0xFFFFFFFF
        init_key[j] = (state[i] - j - temp) & 0xFFFFFFFF
        state[i] = (temp + init_key[j] + j) & 0xFFFFFFFF

    intermediate = 1564561
    mix = intermediate ^ (intermediate >> 30)
    temp = (initial_state[2] ^ (mix * 1664525)) & 0xFFFFFFFF
    init_key[1] = (final_state[2] - temp - 1) & 0xFFFFFFFF

    mix = initial_state[0] ^ (initial_state[0] >> 32)
    temp = (initial_state[1] ^ (mix * 1664525)) & 0xFFFFFFFF
    init_key[0] = (intermediate - temp) & 0xFFFFFFFF

    mix = final_state[-1] ^ (final_state[-1] >> 30)
    temp = (intermediate ^ (mix * 1664525)) & 0xFFFFFFFF
    init_key[-1] = (final_state[1] - temp - (n - 1)) & 0xFFFFFFFF

    return conv_array_to_number(init_key)
        
def find_seed():
    state = [0x80000000 for _ in range(227)] + [0 for _ in range(227,624)]
    seed = invert_init_array(state)
    return seed

def check_solve(r):
    pwn_seed = base64.b64encode(long_to_bytes(find_seed()))
    r.sendline(pwn_seed)
    A = r.recvuntil(b"print custom message\n")
    #print('received initial contact',A)
    r.sendline(b'1')
    response = base64.b64decode(r.recvline())
    #print('received response', response)
    answer = base64.b64encode(response[32:] + response[:32])
    r.recvuntil(b'print custom message\n')
    
    r.sendline(b'2')
    r.recvuntil(b"sure what's the message: ")
    
    r.sendline(answer)
    
    response = base64.b64decode(r.recvuntil(b'\n'))
    print(response)
    flag = response[32:] + response[:32]
    if b'ictf{' in flag and b'ictf{fake_flag}' not in flag:
        return
    else:
        exit(1)






def main(address,port):
    
    conn = pwnlib.tubes.remote.remote(address,port)
    pow_statement = conn.recvuntil([b'proof-of-work: ',b'give me your best shot >:)\t',])
    #print(pow_statement)
    if b'proof-of-work' in pow_statement:
        pow_statement = conn.recvline()
        #print(pow_statement)
        if pow_statement.startswith(b'enabled'):
            handle_pow(conn)
        if not b'give me your best shot >:)\t' in pow_statement:
            A = conn.recvuntil(b'give me your best shot >:)\t')
    check_solve(conn)
    




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="address and port to use, default is localhost and 1337.")
    parser.add_argument("--address", "-a", type=str, default="localhost", help="address to use")
    parser.add_argument("--port", "-p", type=int, default=1337, help="port to use")
    args = parser.parse_args()
    main(args.address,args.port)
