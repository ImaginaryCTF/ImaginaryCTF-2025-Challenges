#!/usr/bin/env -S python3 -u

import pwn
import secrets
import time
import sys
import os

print("Length: ", end="")
length = sys.stdin.readline().encode()
print("Payload: ", end="")
payload = sys.stdin.readline().encode()

if len(payload) >= 0x300 or not payload.isascii():
    print("NO!")
    exit(1)

def check(payload):
    tmpdir = f"/dev/shm/{secrets.token_hex(5)}"
    os.mkdir(tmpdir)
    f = open(f'{tmpdir}/secret.txt', 'wb')
    token = secrets.token_hex(0x18).encode()
    f.write(token)
    f.close()
    con = pwn.process("/home/user/vuln", cwd=tmpdir)
    con.send(length.ljust(4, b"\0"))
    con.sendline(payload)
    con.recvall()
    con.close()
    try:
        f = open(f'{tmpdir}/win.txt', 'rb')
        ret = f.read() == token
        f.close()
        print(ret)
        os.system(f"rm -rf {tmpdir}")
        return ret
    except FileNotFoundError:
        os.system(f"rm -rf {tmpdir}")
        return False

total = 200
passed = sum([check(payload) for _ in range(total)])
print(f"Total: {total} Passed: {passed}")
if passed > 195:
    print("CONSISTENT ENOUGH FOR ME :D")
    print(open("/home/user/flag.txt").read())
    exit(0)
print("NOT CONSISTENT ENOUGH")
exit(1)
