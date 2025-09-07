from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secrets import randbelow, token_bytes
import json

with open('flag.txt') as f:
    flag = f.read().strip()

class CLCG:
    
    def __init__(self, length):
        self.p = getPrime(256)
        self.A = [randbelow(self.p) for _ in range(length)]
        self.C = [randbelow(self.p) for _ in range(length)]
        self.X = [randbelow(self.p) for _ in range(length)]
    
    def rand(self):
        self.X = [(a * x + c) % self.p for a, x, c in zip(self.A, self.X, self.C)]
        return int.to_bytes((sum(self.X) % self.p) >> 192, 8)

NUM_HINTS = 36

clcg = CLCG(8)
data = dict()
data['p'] = clcg.p
data['A'] = clcg.A
data['hints'] = [clcg.rand().hex() for _ in range(NUM_HINTS)]

key = clcg.rand() + clcg.rand()
iv = token_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
data['iv'] = iv.hex()
data['ct'] = cipher.encrypt(pad(flag.encode(), 16)).hex()

print(json.dumps(data))
