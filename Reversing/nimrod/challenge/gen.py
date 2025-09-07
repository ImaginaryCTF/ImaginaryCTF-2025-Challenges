def lcg_keystream(seed, length, a=1664525, c=1013904223, m=2**32):
    s = seed
    stream = []
    for _ in range(length):
        s = (a * s + c) % m
        stream.append((s >> 16) & 0xFF)
    return stream

def xor_encrypt(flag, seed):
    stream = lcg_keystream(seed, len(flag))
    return [ord(c) ^ k for c, k in zip(flag, stream)]

def format_as_nim_array(byte_list):
    return "@[" + ", ".join(str(b) for b in byte_list) + "]"

if __name__ == "__main__":
    flag = "ictf{a_mighty_hunter_bfc16cce9dc8}"
    seed = 0x13371337

    encrypted = xor_encrypt(flag, seed)
    print("Encrypted Flag Bytes for Nim:")
    print(format_as_nim_array(encrypted))
