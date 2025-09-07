import hashlib, secrets, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# --- Fiat-Shamir edge selection (k=1 fixed) ---
def fiat_shamir_select_index(root_hex, m):
    return int.from_bytes(hashlib.sha256(root_hex.encode()).digest(), "big") % m

import secrets

def zkpow_forge_chain_fast(edges, n_vertices=1000, max_attempts=1000):
    """
    Forge zkPoW with a chain, building it in O(n):
    - Preprocess edges into adjacency list for fast neighbor lookup
    - Build a chain along random neighbors
    - Color the chain to avoid conflicts
    - Check Fiat-Shamir edge, retry if needed
    """
    verts = list(range(n_vertices))

    # --- preprocess edges into adjacency list ---
    adj = defaultdict(list)
    for u,v in edges:
        adj[u].append(v)
        adj[v].append(u)

    for attempt in range(max_attempts):
        # pick a random starting vertex
        chain = []
        used = set()
        v = secrets.randbelow(n_vertices)
        chain.append(v)
        used.add(v)

        # build chain greedily (O(n) traversal)
        while len(chain) < n_vertices:  # optional: cap chain length at n_vertices
            neighbors = [w for w in adj[v] if w not in used]
            if not neighbors:
                break
            # pick next vertex randomly
            v = secrets.choice(neighbors)
            chain.append(v)
            used.add(v)

        # assign colors along chain to avoid conflicts
        coloring = {}
        for i, v in enumerate(chain):
            forbidden = set()
            if i > 0:
                forbidden.add(coloring[chain[i-1]])
            coloring[v] = secrets.choice([c for c in range(3) if c not in forbidden])

        # assign remaining vertices random colors
        for v in verts:
            if v not in coloring:
                coloring[v] = secrets.randbelow(3)

        # --- commitments / Merkle tree ---
        nonces = {v: secrets.token_bytes(16) for v in verts}
        leaves_hex = [hexf(commit_vertex(v, coloring[v], nonces[v])) for v in verts]
        merkle_root, levels = build_merkle_tree(leaves_hex)

        # --- Fiat-Shamir picks a single edge ---
        idx = fiat_shamir_select_index(merkle_root, len(edges))
        u,v = edges[idx]

        # check if edge endpoints are in chain and colored differently
        if u in chain and v in chain and coloring[u] != coloring[v]:
            openings = {}
            for w in (u,v):
                openings[w] = {
                    "color": coloring[w],
                    "nonce": hexf(nonces[w]),
                    "merkle_proof": merkle_proof_for_index(levels, w)
                }
            proof = {
                "merkle_root": merkle_root,
                "openings": openings,
            }
            return proof

    raise RuntimeError(f"Failed to forge after {max_attempts} attempts")

def zkpow_forge_chain_fast(edges, n_vertices=1000, max_attempts=1000):
    """
    Forge zkPoW by:
    - Building a chain once and fixing its coloring
    - Randomizing colors for remaining vertices on each attempt
    - Checking Fiat-Shamir edge
    """
    verts = list(range(n_vertices))

    # --- preprocess edges into adjacency list ---
    adj = defaultdict(list)
    for u,v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # --- build chain once ---
    chain = []
    used = set()
    v = secrets.randbelow(n_vertices)
    chain.append(v)
    used.add(v)
    while len(chain) < n_vertices:  # optionally cap chain length
        neighbors = [w for w in adj[v] if w not in used]
        if not neighbors:
            break
        v = secrets.choice(neighbors)
        chain.append(v)
        used.add(v)

    # --- assign colors along chain to avoid conflicts ---
    chain_coloring = {}
    for i, v in enumerate(chain):
        forbidden = set()
        if i > 0:
            forbidden.add(chain_coloring[chain[i-1]])
        chain_coloring[v] = secrets.choice([c for c in range(3) if c not in forbidden])

    # --- attempts: randomize remaining vertices ---
    for attempt in range(max_attempts):
        coloring = dict(chain_coloring)  # start with fixed chain colors
        for v in verts:
            if v not in coloring:
                coloring[v] = secrets.randbelow(3)

        # --- commitments / Merkle tree ---
        nonces = {v: secrets.token_bytes(16) for v in verts}
        leaves_hex = [hexf(commit_vertex(v, coloring[v], nonces[v])) for v in verts]
        merkle_root, levels = build_merkle_tree(leaves_hex)

        # --- Fiat-Shamir picks a single edge ---
        idx = fiat_shamir_select_index(merkle_root, len(edges))
        u,v = edges[idx]

        # check if edge endpoints are in chain and colored differently
        if u in chain and v in chain and coloring[u] != coloring[v]:
            openings = {}
            for w in (u,v):
                openings[w] = {
                    "color": coloring[w],
                    "nonce": hexf(nonces[w]),
                    "merkle_proof": merkle_proof_for_index(levels, w)
                }
            proof = {
                "merkle_root": merkle_root,
                "openings": openings,
            }
            return proof

    raise RuntimeError(f"Failed to forge after {max_attempts} attempts")

from pwn import *

#context.log_level = 'debug'
#conn = process(["python3", "zkpow.py"])
#conn = remote("localhost", 1337)
conn = remote("zkpow.chal.imaginaryctf.org", 1337)
for i in range(50):
  conn.recvuntil(f"==round {i}==\n".encode())
  start = time.time()
  a = json.loads(conn.recvline().strip())
  proof = json.dumps(zkpow_forge_chain_fast(a["edges"], a["n"]))
  conn.sendline(proof.encode())
  end = time.time()
  print(i, end - start)

conn.interactive()
