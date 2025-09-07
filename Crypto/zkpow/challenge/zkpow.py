#!/usr/bin/env python3

import hashlib, secrets, json, time

# --- Utility functions ---
def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()
def hexf(b: bytes) -> str:
    return b.hex()
def commit_vertex(v: int, color_label: int, nonce: bytes) -> bytes:
    return sha256(b"vertex:" + str(v).encode() + b":" + str(color_label).encode() + b":" + nonce)

# --- Merkle tree helpers ---
def build_merkle_tree(leaves_hex):
    leaves = [bytes.fromhex(h) for h in leaves_hex]
    if len(leaves) == 0:
        return hexf(sha256(b"")), [[sha256(b"")]]
    levels = [leaves]
    cur = leaves
    while len(cur) > 1:
        nxt = []
        for i in range(0, len(cur), 2):
            left = cur[i]
            right = cur[i+1] if i+1 < len(cur) else left
            nxt.append(sha256(left + right))
        levels.append(nxt)
        cur = nxt
    return hexf(levels[-1][0]), levels

def merkle_proof_for_index(levels, index):
    proof = []
    idx = index
    for level in levels[:-1]:
        if idx % 2 == 0:
            sib_index = idx + 1 if idx + 1 < len(level) else idx
            sibling = level[sib_index]
            proof.append((hexf(sibling), False))
        else:
            sib_index = idx - 1
            sibling = level[sib_index]
            proof.append((hexf(sibling), True))
        idx //= 2
    return proof

def verify_merkle_proof(root_hex, leaf_hex, proof):
    cur = bytes.fromhex(leaf_hex)
    for sibling_hex, sibling_is_left in proof:
        sibling = bytes.fromhex(sibling_hex)
        if sibling_is_left:
            cur = sha256(sibling + cur)
        else:
            cur = sha256(cur + sibling)
    return hexf(cur) == root_hex

# --- Fiat-Shamir edge selection ---
def fiat_shamir_select_index(root_hex, m):
    return int.from_bytes(hashlib.sha256(root_hex.encode()).digest(), "big") % m

# --- Configurable graph generator ---
def make_graph(n_vertices=1000, p_good=0.75, p_bad=0.003):
    coloring = [secrets.randbelow(3) for _ in range(n_vertices)]
    parts = {0: [], 1: [], 2: []}

    for v, c in enumerate(coloring):
        parts[c].append(v)
        edges = []

    for c1 in range(3):
        for c2 in range(c1+1, 3):
            A, B = parts[c1], parts[c2]
            for u in A:
               for v in B:
                   if secrets.randbelow(1_000_000) / 1_000_000 < p_good:
                       edges.append((u, v)) # spice things up :)

    for c in range(3):
        part = parts[c]
        for i in range(len(part)):
            for j in range(i+1, len(part)):
                if secrets.randbelow(1_000_000) / 1_000_000 < p_bad:
                    edges.append((part[i], part[j]))

    return edges, n_vertices

# --- zkPoW prover ---
def zkpow_prove(edges, coloring, n_vertices=1000):
    verts = list(range(n_vertices))

    # permutation + colors
    perm = [0,1,2]
    secrets.SystemRandom().shuffle(perm)
    permuted = {v: perm[coloring[v]] for v in verts}
    nonces = {v: secrets.token_bytes(16) for v in verts}

    leaves_hex = [hexf(commit_vertex(v, permuted[v], nonces[v])) for v in verts]
    merkle_root, levels = build_merkle_tree(leaves_hex)

    # pick single edge
    idx = fiat_shamir_select_index(merkle_root, len(edges))
    u,v = edges[idx]

    # prepare openings
    openings = {}
    for w in (u,v):
        openings[w] = {
            "color": permuted[w],
            "nonce": hexf(nonces[w]),
            "merkle_proof": merkle_proof_for_index(levels, w)
        }

    proof = {
        "merkle_root": merkle_root,
        "openings": openings,
    }
    return json.dumps(proof)

# --- zkPoW verifier ---
def zkpow_verify(proof, edges):
    merkle_root = proof["merkle_root"]
    openings = proof["openings"]

    # verify Merkle proofs
    for v_s, opened in openings.items():
        v = int(v_s)
        leaf_hex = hexf(commit_vertex(v, opened["color"], bytes.fromhex(opened["nonce"])))
        if not verify_merkle_proof(merkle_root, leaf_hex, opened["merkle_proof"]):
            print(f"Merkle proof failed for vertex {v}")
            return False

    # recompute chosen edge
    idx = fiat_shamir_select_index(merkle_root, len(edges))
    u,v = map(str, edges[idx])
    if u not in openings or v not in openings:
        print(f"Missing opening for endpoints of edge {idx}")
        return False
    if openings[u]["color"] == openings[v]["color"]:
        print(f"Edge {idx} endpoints same color -> invalid")
        return False
    return True

def main():
    print("==zk-proof-of-work: enabled==")
    for i in range(50):
        print(f"==round {i}==")
        edges, n_vertices = make_graph(i * 33 + 10, 0.8)
        print(json.dumps({"n": n_vertices, "edges": edges}))
        start = time.time()
        proof = json.loads(input("proof: "))
        end = time.time()
        if end - start > 5:
            print("too slow!")
            exit(-1)
        ok = zkpow_verify(proof, edges)
        if ok:
            print("verified!")
        else:
            print("failed!")
            exit(-1)

    flag = open("flag.txt").read()
    print("flag:", flag)

if __name__ == "__main__":
    main()
