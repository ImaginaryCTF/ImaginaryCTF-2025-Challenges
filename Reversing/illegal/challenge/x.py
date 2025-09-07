from Crypto.Util import number
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64, random, string
from Crypto.Cipher import ARC4
import gmpy2
from gmpy2 import is_prime

N = 701397522185828618510848689144141769697437689896256198450292185705109859171997422035448595344213238310599935761546507227145586997889267802727882254006212128665715259479298495016335295935617918597221108264157646296756173693328821375707478413840371160154021219872312339790070013576581593041274351519716226001932710350562964171877345004685711580962156605279574878006989339472636045161874912709847493504238149686396507832679605003965586890880990952041073510320469324548905541408310599957304827589243721478126274222195932168114283099328563879447938233775465671657881618285158602801168150361781856392930006354774353480956730859004866086394467279495168591604869515408399459090537939179992287578572547341396413257153557017569098084905689000418684173340720880629917824721126107715645386240102164837467817194542767352379856244478607224642294709998068407396061014954404234149821388635913337986155878230458457799263017931292713449032352536278714310149161272628555832368132182244134594811705949995726387737299686506183592979053247739062412749662824863144126368099113635523511146559478889856275411001080837561433881481306661502015218791699004203077809690399292921506723166584199942797815446126232706601490412458700448908951928021686850440569025753

def flip_bit(n, bit_index):
    """Flip the bit at position bit_index (0 = MSB)."""
    num_bits = n.bit_length()
    # Convert MSB index to LSB index
    lsb_index = num_bits - 1 - bit_index
    if lsb_index < 0:
        raise ValueError("Bit index out of range")
    return n ^ (1 << lsb_index)

def factor_small_primes(candidate, small_bound=2**16):
    remaining = candidate
    for f in range(2, small_bound):
        if is_prime(f):
            while remaining % f == 0:
                remaining //= f
        if remaining == 1:
            break
    return remaining

def factor_one_small_prime(candidate, small_bound=2**16):
    """
    Factor out at most one small prime <= small_bound.
    Returns remaining cofactor after removing one small prime (if any).
    """
    for f in range(2, small_bound):
        if is_prime(f) and candidate % f == 0:
            return candidate // f  # remove only the first small prime
    return candidate  # no small prime factor found

def is_large_prime_after_small_factors(candidate, small_bound=2**16):
    if is_prime(candidate):
        return False
#    remaining = factor_small_primes(candidate, small_bound)
    remaining = factor_one_small_prime(candidate, small_bound) # because i didn't wanna deal with the math
    return remaining > 1 and is_prime(remaining)

def check_bit_flips(n, start_byte=256, small_bound=2**16):
    start_bit = start_byte * 8
    for i in range(start_bit, n.bit_length()):
        candidate = flip_bit(n, i)
        if is_large_prime_after_small_factors(candidate, small_bound):
            # Return immediately after first find
            return (i, candidate)
    return None

print("Checking bit flips after byte 256 for prime or large-prime-after-small-factors...")
result = check_bit_flips(N)

if result:
    bit_index, candidate = result
    print(f"First valid flip found: Bit {bit_index} -> {candidate}")
else:
    print("No candidates found.")

p = 0
for i in range(2, 2**16):
  if candidate % i == 0:
    p = i
    break

q = candidate // p
n = candidate

print(p,q,n)

priv = key = RSA.construct((n, 65537, pow(65537, -1, (p-1)*(q-1)))) # you need to patch out the gcd(d,n) == 1 check in your pycryptodome
                                                                    # it's not needed for correctness
pub = key.publickey()

def generate_license_key() -> str:
    while True:
        # Generate 25 random chars (A-Z, 0-9)
        chars = [random.choice(string.ascii_uppercase + string.digits) for _ in range(25)]
        # Compute checksum: sum(ord(c) % 36) % 36 must be 7
        total = sum((ord(c) % 36) for c in chars)
        if total % 36 == 7:
            break  # valid key
    # Insert dashes every 5 chars
    groups = [ ''.join(chars[i:i+5]) for i in range(0, 25, 5) ]
    return '-'.join(groups)

def deterministic_shuffle(data: bytes, seed: int) -> bytes:
    data = bytearray(data)
    n = len(data)
    for i in range(n):
        j = (i + seed * (i + 1)) % n
        data[i], data[j] = data[j], data[i]
    return bytes(data)


# --- Export modulus and RC4 encrypt (license system data) ---
modulus = pub.n
mod_bytes = modulus.to_bytes((modulus.bit_length() + 7) // 8, "big")
print(modulus)
print(priv.d)
print(priv.e)

rc4_key_mod = b')f\x10\t\x10y%\xd1jN\xf9\n\xff\xf5=_'
cipher = ARC4.new(rc4_key_mod)
enc_mod_bytes = cipher.encrypt(mod_bytes)

print("RC4 key (modulus):", rc4_key_mod)
print("Encrypted modulus:", list(enc_mod_bytes))

# --- Generate license key ---
license_key = generate_license_key()
print("Generated License Key:", license_key)

# --- Sign license key ---
h = SHA256.new(license_key.encode())
signature = pkcs1_15.new(priv).sign(h)   # 256 bytes

# --- RC4-encrypt the human-readable key ---
rc4_key_human = b'k\xd9\x9f\x1b\xe1\xd4_z\xdc\x8e\x1f\xa5\xe6G\xe3R'
cipher_human = ARC4.new(rc4_key_human)
enc_license_key = cipher_human.encrypt(license_key.encode())  # 29 bytes

# --- Concatenate into a fixed binary blob ---
blob = enc_license_key + signature   # 29 + 256 = 285 bytes
blob = deterministic_shuffle(blob, 64601)

kcipher1 = ARC4.new(enc_mod_bytes[:256])
kcipher2 = ARC4.new(enc_mod_bytes[:256])
print(kcipher1.encrypt(rc4_key_mod))
print(kcipher2.encrypt(rc4_key_human))

# --- Encode whole thing as base64 ---
license_blob = base64.b64encode(blob).decode()

print("Flip index: ", 0x62130 * 8 + bit_index - (bit_index % 8) + (7-(bit_index % 8)))
print("License blob (base64):", license_blob)

