from Crypto.Cipher import AES
import json

with open('out.txt') as f:
    out = json.load(f)

p = out["p"]
A = out["A"]
hints = [int(hint, 16) for hint in out['hints']]
last = hints[-1] << 192
hints = [hints[i+1] - hints[i] for i in range(len(hints) - 1)]
ct = bytes.fromhex(out['ct'])
iv = bytes.fromhex(out['iv'])

def decrypt(rand1, rand2):
    cipher = AES.new(int.to_bytes(rand1, 8) + int.to_bytes(rand2, 8), AES.MODE_CBC, iv=iv)
    return cipher.decrypt(ct)

P.<x> = PolynomialRing(GF(p))
rec = list(map(int, prod(x - a for a in A)))
L = [[0 for _ in range(i)] + rec + [0 for _ in range(len(hints) - len(rec) - i)] for i in range(len(hints) - len(rec) + 1)] + [[p * int(i==j) for j in range(len(hints))] for i in range(len(rec) - 1)]
L = Matrix(ZZ, L)

B = L.LLL()
yprime = (2**192) * vector(ZZ, hints)
Byprime = B * yprime
v = vector(ZZ, [round(i/p) for i in Byprime])
Bzprime = v * p - Byprime
zprime = (B**(-1)) * Bzprime
#print([len(bin(i)) for i in zprime]) - debug - should be around 192

xprime = list(yprime + zprime)
for _ in range(2):
    xprime.append((-vector(rec[:-1]) * vector(xprime[-len(rec)+1:])) % p)
rand1 = ((last + xprime[-2]) % p) >> 192
rand2 = ((last + xprime[-2] + xprime[-1]) % p) >> 192
for r1 in range(rand1 - 4, rand1 + 4):
    for r2 in range(rand2 - 4, rand2 + 4):
        flag = decrypt(r1, r2)
        if b'ictf' in flag: print(flag)
