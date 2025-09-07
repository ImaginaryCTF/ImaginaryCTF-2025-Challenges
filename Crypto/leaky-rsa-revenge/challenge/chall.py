#!/usr/local/bin/python3
import json
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secrets import randbelow, token_bytes
from hashlib import sha256

with open('flag.txt') as f:
    flag = f.read()

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
d = pow(e, -1, (p-1)*(q-1))

key_m = randbelow(n)
key_c = pow(key_m, e, n)

key = sha256(str(key_m).encode()).digest()[:16]
iv = token_bytes(16)
ct = AES.new(key, AES.MODE_CBC, IV=iv).encrypt(pad(flag.encode(), 16))

print(json.dumps({'n': n, 'c': key_c, 'iv': iv.hex(), 'ct': ct.hex()}))

def get_bit(n, k):
    return (n >> k) % 2

for _ in range(1024):
    idx = randbelow(4)
    print(json.dumps({'idx': idx}))
    try:
        response = json.loads(input())
        c = response['c'] % n
        assert c != key_c
        m = pow(c, d, n)
        b = get_bit(m, idx)
    except (json.JSONDecodeError, TypeError, KeyError, ValueError, AssertionError):
        b = 2
    print(json.dumps({'b': b}))
