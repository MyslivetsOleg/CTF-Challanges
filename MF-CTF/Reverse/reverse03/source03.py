# Generate serial for name 'SPCS_CTF_2021'

def check(name, serial):
    name = bytes(name, 'utf-8')

    if len(name) != 13:
        return False

    valid = [
        int.from_bytes(name[:4], 'big'),
        int.from_bytes(name[4:8], 'big'),
        int.from_bytes(name[8:], 'big')
    ]

    valid[0] ^= valid[2]
    valid[2] ^= valid[0]
    valid[0] ^= valid[2]

    return serial == '{:08x}-{:08x}-{:08x}'.format(*valid)


name = input('What is your name?\n> ')
serial = input('... and your serial?\n> ')
print('Your serial is {}'.format('valid!' if check(name, serial) else 'invalid...'))
