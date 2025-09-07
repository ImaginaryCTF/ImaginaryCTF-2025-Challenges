# obfuscated-2
**Category:** Forensics
**Difficulty:** Medium-Hard
**Author:** Eth007

## Description
we can't fix it if we never face it

same handout as `obfuscated-1`

## Distribution

## Writeup
Find the `sm.dat` file in `AppData\Roaming\GlobalSCAPE\` folder to find the IP and username for the FTP server. Decrypting the file gives a password of `REDACTED` that doesn't work. But in the PuTTY saved proxy credentials, we can see another password that is REDACTED, but in registry slack space we can see the end of the password, which is the beginning of the bee movie. Googling it and completing it gives us the full password, and we can then log on to the server and get the flag.
