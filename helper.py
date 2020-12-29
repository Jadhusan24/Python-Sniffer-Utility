def mac_addr(mac_add_bytes):
    mac_add_str = map('{:02x}'.format, mac_add_bytes)
    return ':'.join(mac_add_str).upper()


def encode_hex(byte_block):
    hex_ = []
    for x in byte_block:
        hex_.append(f"{x:02x}")
    hex_ = list(zip(hex_[::2], hex_[1::2]))
    bytes_to_hex = "" 

    for x in hex_:
        bytes_to_hex += f"{x[0]}{x[1]} " 

    return bytes_to_hex