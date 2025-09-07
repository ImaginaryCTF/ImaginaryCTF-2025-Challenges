from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, isPrime


with open('out.txt', 'r') as f:
    contents = f.read()
exec(contents)


n = 32
e = 0x10001
N = 64

def GCD_reduce(A):
    for prev in A:
        start = prev
        for i in A:
            c = gcd(i,start)
            if c == 1 or c == start:
                continue
            start = start // c
        if prev != start:
            A.remove(prev)
            A.add(start)
            #recursion makes everything better
            GCD_reduce(A)
            return
        

def reduce(m,nums):
    
    
    A = IntegerMatrix.from_matrix([nums + [1]] + [[0] * i + [m] + [0] * (N - i) for i in range(N)])

    C = LLL.reduction(A)

    gcds = set(int(gcd(i[-1],m)) for i in C)
    
    gcds = gcds.union(set(m // i for i in gcds))
    
    gcds.discard(1)
    gcds.discard(m)
    GCD_reduce(gcds)
    
    return gcds


original_m = m
m_factors = []
while(True):
    if (m == 1):
        print('success found factors')
        break
    
    if isPrime(int(m)):
        m_factors.append(m)
        print('success found factors')
        break
    
    factors = reduce(m,[i % m for i in nums])
    if (len(factors) == 0):
        print('failure :(')
        break
    for i in factors:
        if isPrime(int(i)):
            m_factors.append(i)
            m //= i
T = 1

for i in m_factors:
    T *= i - 1

D = pow(e,-1,T)
f = pow(int(ct),int(D),int(original_m))

print(long_to_bytes(int(f)))