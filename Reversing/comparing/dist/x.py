import heapq

def decode_even(s: str):
    for len1 in range(2, 4):
        for len2 in range(2, 4):
            if len1 + len2 >= len(s):
                continue
            val1 = int(s[:len1])
            val3 = int(s[len1:len1+len2])
            if not (32 <= val1 <= 126 and 32 <= val3 <= 126):
                continue
            idx_str = s[len1+len2:-len1-len2]
            idx = int(idx_str) if idx_str else 0
            suffix = s[-(len1+len2):]
            expected = str(val3)[::-1] + str(val1)[::-1]
            if suffix == expected:
                return val1, val3, idx
    return None


def decode_odd(s: str):
    for len1 in range(2, 4):
        for len2 in range(2, 4):
            if len1 + len2 >= len(s):
                continue
            val1 = int(s[:len1])
            val3 = int(s[len1:len1+len2])
            if not (32 <= val1 <= 126 and 32 <= val3 <= 126):
                continue
            idx_str = s[len1+len2:]
            try:
                idx = int(idx_str)
            except ValueError:
                continue
            return val1, val3, idx
    return None


def decode_line(s):
    return decode_odd(s) or decode_even(s)


def main():
    with open("output.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Step 1: decode pairs of lines -> recover tuples (ch1, ch2, idx)
    tuples = []
    for i in range(0, len(lines), 2):
        val1, val3, idx1 = decode_line(lines[i])
        val2, val4, idx2 = decode_line(lines[i+1])
        # Rebuild original tuples pushed into the PQ
        tuples.append((chr(val1), chr(val2), idx1))
        tuples.append((chr(val3), chr(val4), idx2))

    # Step 2: simulate the priority_queue ordering
    # C++ Compare: smaller (ch1+ch2) comes first
    heap = []
    for t in tuples:
        ch1, ch2, idx = t
        weight = ord(ch1) + ord(ch2)
        heapq.heappush(heap, (weight, idx, ch1, ch2))

    # Step 3: pop in PQ order and rebuild flag
    flag_parts = {}
    while heap:
        w1, i1, a1, b1 = heapq.heappop(heap)
        w2, i2, a2, b2 = heapq.heappop(heap)

        # The actual flag chars are (a1,b1) and (a2,b2)
        flag_parts[i1] = a1 + b1
        flag_parts[i2] = a2 + b2

    # Step 4: order by index
    flag = "".join(flag_parts[i] for i in sorted(flag_parts.keys()))
    print("Recovered flag:", flag)


if __name__ == "__main__":
    main()
