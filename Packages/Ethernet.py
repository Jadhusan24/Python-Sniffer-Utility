import socket
import struct
from helper import mac_addr


class Ethernet:
    def __init__(self, data):
        self.data = data 
        self.dest_mac = ""
        self.src_mac = ""
        self.eth_protocol = ""
        self.ETH_LEN = 14


    def frame(self):
        self.dest_mac, self.src_mac, self.eth_protocol = struct.unpack(
            '!6s6sH', self.data[:14])
        return mac_addr(self.dest_mac), mac_addr(self.src_mac), socket.htons(self.eth_protocol)
