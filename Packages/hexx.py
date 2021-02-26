def mac_addr(mac_add_bytes):
    # convert the bytes to string
    mac_add_str = map('{:02x}'.format, mac_add_bytes)
    return ':'.join(mac_add_str).upper()


def encode_hex(byte_block):
    hex_ = []
    for x in byte_block:
        # in 16byte return, we taking one string portion not the full array
        hex_.append(f"{x:02x}")
        # 02x : pads 2 spaces and append the hex value of that bit
    hex_ = list(zip(hex_[::2], hex_[1::2]))
    bytes_to_hex = ""  # returning as hex format

    for x in hex_:
        bytes_to_hex += f"{x[0]}{x[1]} "  # to join em as 4

    return bytes_to_hex