# weird-app
**Category:** Reversing
**Difficulty:** 4/10
**Author:** cleverbear57

## Description
I made this weird android app, but all it gave me was this .apk file. Can you get the flag from it?

## Distribution
weird.zip

## writeup
 Running the .apk file with an emulator will give you a scrambled flag, and when you decompile the .apk file you can see the encryption algorithm. You can write a solve script to reverse the encryption which gives the flag.
