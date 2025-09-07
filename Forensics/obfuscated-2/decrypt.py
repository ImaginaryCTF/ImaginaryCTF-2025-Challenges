from Crypto.Cipher import DES

enc_bytes = bytes.fromhex('7E9B311248B7C8A8')
vnc_key = bytes.fromhex('e84ad660c4721ae0')

cipher = DES.new(vnc_key, DES.MODE_ECB)
password = cipher.decrypt(enc_bytes)

password = password.rstrip(b'\x00').decode('ascii', errors='ignore')

print("VNC password:", password)
