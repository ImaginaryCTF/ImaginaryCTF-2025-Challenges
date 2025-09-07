# extra-crunchy-bits
**Category:** Crypto
**Difficulty:** Medium
**Author:** puzzler7

## Description
help they crunched my flag

Plaintext and flag are both in English.

## Distribution
- ecb.py
- enc.bin

## Solution
Every two characters of the plaintext becomes 16 bytes of the ciphertext. Because this is AES ECB, it's vulnerable to frequency analysis - identify the most common English bigrams (either by analyzing a large body of text or by downloading a list), match it to the most common 16 bytes in the ciphertext, and voila... at least, in theory.

In practice, I wasn't able to get pure frequency analysis to work here. It should be possible to write a hill climbing algorithm to decrypt this, especially because once it even partially works, a human should be able to identify the plaintext ("Ode to ECB" poem, then the flag, then Project Gutenberg "The Picture of Dorian Grey", then Project Gutenberg "Great Expectations"). 
