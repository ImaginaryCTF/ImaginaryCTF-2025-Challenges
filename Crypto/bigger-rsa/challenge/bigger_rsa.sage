from Crypto.Util.number import getPrime, bytes_to_long
import secrets

n = 32
e = 0x10001
N = 64

flag = b'ictf{REDACTED}'
flag = secrets.token_bytes((n * 63) - len(flag)) + flag

ps = [getPrime(512) for _ in range(n)]

m = 1
for i in ps:
    m *= i

nums = [CRT([1 + secrets.randbits(260) for _ in range(n)],ps) for __ in range(N)]
ct = pow(bytes_to_long(flag),e,m)
print(f"ct={ct}")
print(f"m={m}")
print(f"nums={nums}")
