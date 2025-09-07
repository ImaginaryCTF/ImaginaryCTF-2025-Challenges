#!/usr/bin/env python3

import subprocess
import shutil
import tempfile
import os
import random
import base64

CHECKER_BIN = "./checker"  # original binary
FLAG_FILE = "./flag.txt"   # path to flag

def flip_bit_in_file(input_path, bit_index):
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="checker_", dir="./tmp")
    os.close(tmp_fd)
    with open(input_path, "rb") as f:
        data = bytearray(f.read())
    byte_index = bit_index // 8
    bit_in_byte = bit_index % 8
    if byte_index >= len(data):
        raise ValueError(f"Bit index {bit_index} out of range for file of size {len(data)} bytes")
    data[byte_index] ^= (1 << bit_in_byte)
    with open(tmp_path, "wb") as f:
        f.write(data)
    os.chmod(tmp_path, 0o755)
    return tmp_path

def main():
    try:
        bit_index = int(input("Enter the bit index to flip: "))
        tmp_bin = flip_bit_in_file(CHECKER_BIN, bit_index)
        license_key = input("Enter the license key (base64, one line): ").strip()

        try:
            decoded = base64.b64decode(license_key, validate=True)
        except Exception:
            print("Invalid base64 input!")
            os.remove(tmp_bin)
            return

        proc = subprocess.run([tmp_bin], input=license_key, capture_output=True, text=True)

        print(proc.stdout)
        print(proc.stderr)

        if "SUCCESS" in proc.stdout:
            if os.path.exists(FLAG_FILE):
                with open(FLAG_FILE, "r") as f:
                    print("\nFLAG:", f.read())
            else:
                print("Flag file not found!")
        else:
            print("License key invalid or binary did not print SUCCESS.")

    finally:
        if 'tmp_bin' in locals() and os.path.exists(tmp_bin):
            os.remove(tmp_bin)

if __name__ == "__main__":
    main()
