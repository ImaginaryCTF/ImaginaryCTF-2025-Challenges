#!/usr/bin/env python3

import secrets
from Crypto.Cipher import AES
from base64 import b64encode
import re

pt = open('plaintext.txt').read()
pt = pt.replace("\n", ' ')
while '  ' in pt:
    pt = pt.replace('  ', ' ')
pt = pt.lower()

assert(re.search(r'ictf{[a-z]+}', pt))

charset = "abcdefghijklmnopqrstuwyz "
pt = ''.join(i for i in pt if i in charset)


pt = ''.join(hex(ord(i))[-2:] for i in pt)
pt = ''.join(hex(ord(i))[-2:] for i in pt)
pt = ''.join(hex(ord(i))[-2:] for i in pt)
pt = pt.encode()
key = secrets.token_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(pt)
open("enc.bin", "wb").write(ct)