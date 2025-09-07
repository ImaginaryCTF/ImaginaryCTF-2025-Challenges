# bigger-rsa
**Category:** Crypto
**Difficulty:** Easy
**Author:** moaiman

## Description
Is 300 kb enough to make RSA a good candidate for PQC ... well maybe not but it's still got a smaller key size than McEliece 

## Distribution
just bigger-rsa.zip

## Solution
Use Lattice reduction on nums to acquire some factors of m (this is somewhat expensive and takes about 5 minutes to run on my computer). This won't give the full factorization of m but will give enough to recover some prime factors by taking gcds with each other. Divide m by the prime factors you get for an easier lattice and repeat the process until you've acquired all the factors and decrypt the cipher text. See solve.sage