from .Ethernet import Ethernet
import struct
import socket
import binascii
from helper import encode_hex, mac_addr



class Protocol:
    def __init__(self, ethernet: Ethernet):
        self.data = ethernet.data  
        self.eth = ethernet

        self.ETH_TYPE = {
            8: IPv4(self.data[ethernet.ETH_LEN:20+ethernet.ETH_LEN], ethernet),
            1544: ARP(self.data[ethernet.ETH_LEN:42])
        }


class IPv4:
    def __init__(self, ip_header, eth: Ethernet):
        self.ip_header = ip_header
        self.eth = eth
     
        self.PROTOCOLS = {
            1: "ICMP",
            6: "TCP",
            17: "UDP",
            53: "DNS"
        }


        iph = struct.unpack('!BBHHHBBH4s4s', self.ip_header)


        self.version_ihl = iph[0]
        self.version = self.version_ihl >> 4
        self.ihl = self.version_ihl & 0xF 
        self.ttl = iph[5]
        self.protocol = iph[6]
        self.s_addr = socket.inet_ntoa(iph[8])
        self.d_addr = socket.inet_ntoa(iph[9])


    def _show_cap(self):        

        if self.protocol == 1:
            u = self.iph_length + self.eth.ETH_LEN
            icmph_length = 4
            icmp_header = self.eth.data[u:u+4]

            icmph = struct.unpack('!BBH', icmp_header)
            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]
            type_status = ""
            if icmp_type == 0:
                type_status = "0 (Echo Reply)"
            elif icmp_type == 8:
                type_status = "8 (Echo Request)"

            print(f'Type {type_status}, Code {code}, Checksum {checksum}')


            h_size = self.eth.ETH_LEN + self.iph_length + \
                icmph_length  
            data_size = len(self.eth.data) - h_size

            data = self.eth.data[h_size:]
            print(f'Data {encode_hex(bytes(data))}')

        try:
            print(f'Protocol : {self.PROTOCOLS[self.protocol]}')
        except KeyError:
            print(f"Protocol : {self.protocol}") 

    def __call__(self):
        print(
            f'Internet Protocol Version {self.version}, Dst {self.d_addr}, Src {self.s_addr}')
        self._show_cap()


class ARP:
    def __init__(self, arp_header):
        self.arp_header = arp_header
        arph = struct.unpack("!2s2s1s1s2s6s4s6s4s", self.arp_header)


        self.protocol_size = binascii.hexlify(arph[3]).decode('utf-8')
        self.protocol_type = binascii.hexlify(arph[1]).decode('utf-8')


        self.src_mac = mac_addr(arph[5])
        self.dst_mac = mac_addr(arph[7])


        self.src_ip = socket.inet_ntoa(arph[6])
        self.dst_ip = socket.inet_ntoa(arph[8])


    def __call__(self):
        print(
            f"Protocol Size {self.protocol_size}, Protocol Type {self.protocol_type}")
        print(f"Sender MAC Address: {self.src_mac}, Sender IP: {self.src_ip}")
        print(f"Target MAC Address: {self.dst_mac}, Target IP: {self.dst_ip}")