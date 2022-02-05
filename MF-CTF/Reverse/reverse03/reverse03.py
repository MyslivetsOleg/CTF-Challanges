def generate(name):
    if 13 != len(name):
        return False
    valid = [
        int.from_bytes(name[:4], 'big'),
        int.from_bytes(name[4:8], 'big'),
        int.from_bytes(name[8:], 'big')
    ]
    valid[0] ^= valid[2]
    valid[2] ^= valid[0]
    valid[0] ^= valid[2]
    return '{:08x}-{:08x}-{:08x}'.format(*valid)


name = "SPCS_CTF_2021".encode('utf-8')
print("[!]Serial Number:" + generate(name))
