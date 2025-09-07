#!sage
from time import time
from Crypto.Util.number import long_to_bytes

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
final = poly.gcd(poly2)
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
GCD: 13 seconds
Final degree: 457
ictf{mayb3_d0nt_m4ke_th3_sca1ar_a_f4ctor_0f_the_ord3r}
ictf{mayb3_d0nt_m4ke_th3_sca1ar_a_f4ctor_0f_the_ord3r}
'''