from datetime import datetime

def get_key_from_minute(minute: int) -> str:
    # Same as in your JS: minute + 32
    return chr(minute + 32)

def xor_decrypt(hex_str: str, key: str) -> str:
    decrypted = ""
    for i in range(0, len(hex_str), 2):
        byte = int(hex_str[i:i+2], 16)
        decrypted += chr(byte ^ ord(key))
    return decrypted

if __name__ == "__main__":
    ciphertext = input("Enter encrypted hex: ").strip()
    minute = int(input("Enter minute (0–59): ").strip())
    key = get_key_from_minute(minute)

    try:
        plaintext = xor_decrypt(ciphertext, key)
        print("Decrypted text:", plaintext)
    except Exception as e:
        print("Error:", e)
