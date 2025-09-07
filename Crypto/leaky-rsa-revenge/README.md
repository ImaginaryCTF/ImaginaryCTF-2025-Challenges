# leaky-rsa
**Category:** Crypto
**Difficulty:** Easy
**Author:** wjaaaaaaat

## Description
A few of my bits are leaky... but they're not important. That's why they're called the least significant!

## Distribution
chall.py

## Solution
It is similar to the LSB oracle attack.

https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack

In that attack, we send `pow(2, e*i, n) * c` for decryption and get back `((pow(2, i, n) * m) % n) % 2`. Note that `(pow(2, i+1, n) * m) % n` is `2 * ((pow(2, i, n) * m) % n)` minus `0` or `n`, depending on if `(pow(2, i, n) * m) % n` is greater than or less than `n/2`. So, comparing `((pow(2, i, n) * m) % n) % 2` and `((pow(2, i+1, n) * m) % n) % 2` gives us the MSB of `pow(2, i, n) * m`.

In this slightly modified version, we get a random one of the lower four bits. First, we try instances until we get an `n` that is -1 mod 16. Now, say we get the third LSB (index 2, fours place). We can send over `pow(2, e*(i+3), n) * c` and get back `((8 * pow(2, i, n) * m) % n) & 4`. Note that `((8 * pow(2, i, n) * m) % n) & 4 == int((((8 * pow(2, i, n) * m) % n) % 8) >= 4)` and `((8 * pow(2, i, n) * m) % n) % 8` is `(0 - n * ((8 * pow(2, i, n) * m) // n)) % 8 == ((8 * pow(2, i, n) * m) // n) % 8`. Note that this value tells us which of the intervals `[0, n/8)`, ..., `[7*n/8, n)` that `pow(2, i, n) * m` is in, but we only get the MSB of it (from the `>= 4` or `& 4`) so we basically get one MSG of `pow(2, i, n) * m`. Repeating this will allow us to obtain all of `m`.
