from flag import flag
import numpy as np
import random
import string


def conj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])


def mul(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])


def rotate(v, q):
    return mul(mul(q, v), conj(q))


ar = []
for c in [flag[i:i+3].ljust(3, "0") for i in range(0, len(flag), 3)]:
    ar.append(np.concatenate(
        (np.array([random.uniform(0, 255)]), np.array([ord(a) for a in c]))))
r = np.random.randn(4)
r /= np.linalg.norm(r)
a = np.linalg.qr(np.random.randn(3, 3))[0]
if np.linalg.det(a) < 0:
    a[:, 0] = -a[:, 0]
s = 1.25
t = np.random.uniform(-90, 90, size=3)
sigma = 0.22
for i, v in enumerate(ar):
    tmp = rotate(v, r)
    vec = tmp[1:]
    vec = s * (a @ vec) + t + np.random.normal(0, sigma, size=3)
    ar[i] = np.concatenate((np.array([tmp[0]]), vec))

print(ar)
