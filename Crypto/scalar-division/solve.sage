#!sage
from time import time
from Crypto.Util.number import long_to_bytes

def GCD(a, b):
    def HGCD(a, b):
        if 2 * b.degree() <= a.degree() or a.degree() == 1:
            return 1, 0, 0, 1
        m = a.degree() // 2
        a_top, a_bot = a.quo_rem(x**m)
        b_top, b_bot = b.quo_rem(x**m)
        R00, R01, R10, R11 = HGCD(a_top, b_top)
        c = R00 * a + R01 * b
        d = R10 * a + R11 * b
        q, e = c.quo_rem(d)
        d_top, d_bot = d.quo_rem(x**(m // 2))
        e_top, e_bot = e.quo_rem(x**(m // 2))
        S00, S01, S10, S11 = HGCD(d_top, e_top)
        RET00 = S01 * R00 + (S00 - q * S01) * R10
        RET01 = S01 * R01 + (S00 - q * S01) * R11
        RET10 = S11 * R00 + (S10 - q * S11) * R10
        RET11 = S11 * R01 + (S10 - q * S11) * R11
        return RET00, RET01, RET10, RET11

    q, r = a.quo_rem(b)
    if r == 0:
        return b
    R00, R01, R10, R11 = HGCD(a, b)
    c = R00 * a + R01 * b
    d = R10 * a + R11 * b
    if d == 0:
        return c.monic()
    q, r = c.quo_rem(d)
    if r == 0:
        return d
    return GCD(d, r)

p = 0xbde3c425157a83cbe69cee172d27e2ef9c1bd754ff052d4e7e6a26074efcea673eab9438dc45e0786c4ea54a89f9079ddb21
Qx = 0x686be42f9c3f431296a928c288145a847364bb259c9f5738270d48a7fba035377cc23b27f69d6ae0fad76d745fab25d504d5
E = EllipticCurve(GF(p),[5,7])
start = time()
k = E.order().factor(limit=2**10)[3][0]
print('k:',k)
print('Finding k:',int(time()-start),'seconds')

start = time()
poly = E.multiplication_by_m(k,1)
print('Division Polynomial:',int(time()-start),'seconds')
poly = poly.numerator()-Qx*poly.denominator()

R.<x> = PolynomialRing(GF(p))
poly = R(poly)
print('Degree:',poly.degree())

start = time()
poly2 = pow(x,p,poly)-x
print('Powering:',int(time()-start),'seconds')


start = time()
final = GCD(poly,poly2)
print('GCD:',int(time()-start),'seconds')
print('Final degree:',final.degree())

start = time()
roots = final.roots()

for root in roots:
    for i in range(-1,2,2):
        flag = root[0]
        flag = long_to_bytes(int(flag))
        if flag.isascii():
            print('ictf{'+flag.decode()+'}')

'''
k: 457
Finding k: 15 seconds
Division Polynomial: 15 seconds
Degree: 208849
Powering: 180 seconds
GCD: 67 seconds
ictf{mayb3_d0nt_m4ke_th3_sca1ar_a_f4ctor_0f_the_ord3r}
'''