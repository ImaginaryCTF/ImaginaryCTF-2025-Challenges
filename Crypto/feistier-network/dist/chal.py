#!/usr/local/bin/python3
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random
from secrets import randbits
import base64
import os


secret_half = randbits(256)

def xor(bytes1,bytes2):
    return bytes(a ^ b for a, b in zip(bytes1, bytes2))

def readflag():
    try:
        flag = os.getenv("FLAG").encode('utf-8')
    except:
        print('the flag is missing please contact ictf admins')
        flag = b'ictf{fake_flag}'
    return flag



def keygen(seed):
    random.seed(seed)
    out = []
    for i in range(623):
        h = SHA256.new()
        h.update(long_to_bytes(secret_half ^ random.getrandbits(32)))
        out.append(h.digest())
    return out



def encryption_round(A,key):
    left,right = A[:32], A[32:]
    h = SHA256.new()
    h.update(xor(right,key))
    new_right = xor(left,h.digest())
    return right + new_right

def encrypt(message,keys):
    encrypted = message[:]
    assert(len(encrypted) == 64)
    for key in keys:
        encrypted = encryption_round(encrypted,key)
    return encrypted
    
    
    
def main():
    try:
        public_half = bytes_to_long(base64.b64decode(str(input("give me your best shot >:)\t"))))
        keys = keygen(public_half)
        flag = readflag().ljust(64, b'\x00')

        while(True):
            choice = int(input("1) print flag\n2) print custom message\n"))
            if (choice == 1):
                print(base64.b64encode(encrypt(flag,keys)).decode('utf-8'))
            elif (choice == 2):
                your_message = base64.b64decode(input("sure what's the message: ")).ljust(64,b'\x00')
                print(base64.b64encode(encrypt(your_message,keys)).decode('utf-8'))
            else:
                exit(1)
                
    except:
        print("don't try and break me (ノಠ益ಠ)ノ彡┻━┻")
        exit(1)
        

if __name__ == "__main__":
    main()