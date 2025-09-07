# Avalanche
**Category:** Pwn
**Difficulty:** 3/10
**Author:** moaiman

## Description

I don't trust stl containers so I wrote my own hash table ... I sure hope it's bug free

## Distribution 

only challenge/bin/Avalanche

## Solution

This is a simple buffer overflow problem with a little hash collision sprinkled in. The objective is to change the formatter in the printf statement to "%s" so that you can print the flag. This is possible because the hash tables insertion function is bugged and doesn't wrap around when probing. There is a stack guard function in place that protects the 248 bytes between the end of the hash table and the formatter by checking that all the bytes are 0, however this function is only called immediately after insertion but before rehashing. Because the rehashing function also uses the bugged insertion function you can use it to overflow into the the formatter's address. 
The rehashing function reallocates the buffer on the stack so the offset between the formatter address and the end of buffer remains constant and allocates its current capacity + 2, so the capacity goes like 8 -> 18 -> 38 -> 78. Using chinese remainder theorem we can know that any element that hashes to $ 15048\,mod\,(17784) $ will hash to $ 0\,mod\,(8) $ , $ 0\,mod\,(18) $ and $ 0\,mod\,(38) $ , but $ 72\,mod\,(78) $. So if you insert 38 elements which hash to a number of that form, when the table rehashes you'll get 38 collisions at the 72nd position. This will overflow all the way into the formatter address and you'll be able to print the flag.  
