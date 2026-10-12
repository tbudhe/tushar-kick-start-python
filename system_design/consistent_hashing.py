import hashlib
import bisect
from dataclasses import dataclass, field
from collections import Counter

CLOCK_SIZE = 12
VIRTUAL_NODES = 2


# CLOCK_SIZE =  2**32  PROD 
# VIRTUAL_NODES =  150 PROD

def _hash(name: str) -> int:
    text_bytes = name.encode()                      # "user:42" -> b'user:42'
    all_16_bytes = hashlib.md5(text_bytes).digest()  # 16-byte fingerprint
    first_4_bytes = all_16_bytes[:4]                # take 4 bytes
    number = int.from_bytes(first_4_bytes, "big")   # -> a big number
    return number % CLOCK_SIZE


@dataclass
class ConsistentHashRing:
    spots: list[int] = field(default_factory=list)
    owner: dict[int, str] = field(default_factory=dict)

    def add_server(self, server_name: str) -> None:
        for i in range(VIRTUAL_NODES):
            label = f"{server_name}#{i}"
            spot = _hash(label)
            bisect.insort(self.spots, spot)
            self.owner[spot] = server_name

    def get_server(self, key: str) -> str:
        return self.get_server_at(_hash(key))          # real use: name -> spot

    def get_server_at(self, key_spot: int) -> str:
        raw_idx = bisect.bisect_left(self.spots, key_spot)
        idx = raw_idx % len(self.spots)
        return self.owner[self.spots[idx]]

    def get_servers(self, key: str, n: int) -> list[str]:
        return self.get_servers_at(_hash(key), n)

    def get_servers_at(self, key_spot: int, n: int) -> list[str]:
        start = bisect.bisect_left(self.spots, key_spot)
        result = []
        for step in range(len(self.spots)):
            idx = (step+start) % len(self.spots)
            server = self.owner[self.spots[idx]]
            if server not in result:
                result.append(server)
            if (len(result) == n):
                break
        return result

    def remove_server(self, server_name: str) -> None:
        for i in range(VIRTUAL_NODES):
            label = f"{server_name}#{i}"
            spot = _hash(label)
            self.spots.remove(spot)
            del self.owner[spot]


ring = ConsistentHashRing()
for s in ["server 0", "server 1", "server 2"]:
    ring.add_server(s)
keys = [f"user:{i}" for i in range(10)]

# 1. Owner and replicas agree, with no duplicate servers
before = {k: ring.get_server(k) for k in keys}
for k in keys:
    replicas = ring.get_servers(k, 2)
    assert replicas[0] == before[k]
    assert len(set(replicas)) == len(replicas)

# 2. Asking for more copies than servers doesn't loop forever
assert len(ring.get_servers("user:1", 5)) == 3

# 3. Removing a server moves ONLY that server's keys
ring.remove_server("server 0")
after = {k: ring.get_server(k) for k in keys}
moved = [k for k in keys if before[k] != after[k]]
assert all(before[k] == "server 0" for k in moved)

# 4. Adding it back restores the exact same mapping
ring.add_server("server 0")
assert {k: ring.get_server(k) for k in keys} == before

print(Counter(before.values()))
print(f"moved {len(moved)} of {len(keys)} keys")
print("all tests passed")
