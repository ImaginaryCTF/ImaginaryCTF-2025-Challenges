# Feistier Network
**Category:** Crypto
**Difficulty:** 4/10
**Author:** moaiman

## Description
I fixed my key generator this time, I'm so confident in it I'll even let you seed my rng

## Distribution
just chal.py

## writeup
cpython doesn't hash integer types when seeding (but it does for strings for some reason???) instead it just obfuscates them into random's state vector. This process is invertible so you can find a given number to achieve any*(1 in 4 billion states are possible) state you want. Find a state that will result in random outputting a palindromic sequence of length 623 and you can turn the encryption oracle into a decryption one. 