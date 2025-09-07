import json
from pwn import *
from sage.all import RealField
from tqdm import trange
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

def init():
#    return process(['python3', 'chall.py'])
    return remote('leaky-rsa-revenge.chal.imaginaryctf.org', 1337)

def recv(chall):
    return json.loads(chall.recvline().decode())

def send(data, chall):
    chall.sendline(json.dumps(data))

def get_chall():
    chall = init()
    data = recv(chall)
    n = data['n']
    while n % 16 != 15: # can probably do with other but this makes it easier
        chall.close()
        chall = init()
        data = recv(chall)
        n = data['n']
    return chall, n

def solve(chall, n):
    c = data['c']
    ct = bytes.fromhex(data['ct'])
    iv = bytes.fromhex(data['iv'])

    R = RealField(2048)

    m = R(0)
    two = pow(2, 65537, n)
    for i in trange(1024):
        idx = recv(chall)['idx']
        send({'c': (c * pow(two, i + idx + 1)) % n}, chall)
        b = recv(chall)['b']
        assert b != 2
        m += b * n / R(2**(i+1))

    m = int(m)
    for guess in range(m - 4, m + 4):
        key = sha256(str(guess).encode()).digest()[:16]
        flag = unpad(AES.new(key, AES.MODE_CBC, IV=iv).decrypt(ct), 16).strip()
        if flag[:5] + flag[-1:] == 'ictf{}':
            print(flag)
            break
    else:
        print('flag not found... :(')
        exit(1)

chall, n = get_chall()
solve(chall, n)
