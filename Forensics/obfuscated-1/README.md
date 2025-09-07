# obfuscated-1
**Category:** Forensics
**Difficulty:** Easy
**Author:** Eth007

## Description
I installed every old software known to man... The flag is the VNC password, wrapped in `ictf{}`.

## Distribution
- Users.zip

## writeup
Open the registry hive in NTUSER.DAT, and get the encrypted password in `Software\TightVNC\Server`. Use decrypt.py to decrypt and get the plaintext password.
