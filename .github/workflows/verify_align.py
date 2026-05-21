#!/usr/bin/env python3
import struct, sys

if len(sys.argv) < 2:
    print("Usage: verify_align.py <path_to_binary>")
    sys.exit(1)

path = sys.argv[1]
with open(path, 'rb') as f:
    data = f.read()

e_phoff = struct.unpack_from('<Q', data, 32)[0]
e_phentsize = struct.unpack_from('<H', data, 54)[0]
e_phnum = struct.unpack_from('<H', data, 56)[0]

aligns = []
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    if struct.unpack_from('<I', data, off)[0] == 1:  # PT_LOAD
        aligns.append(struct.unpack_from('<Q', data, off + 48)[0])

ok = all(a >= 16384 for a in aligns)
if not ok:
    print(f"FAILED: {path} is not 16KB page aligned!")
    sys.exit(1)

print(f"PASSED: {path} is 16KB page aligned")
