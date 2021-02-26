#!/usr/bin/python3
import struct
import socket
import binascii
from Packages.hexx import encode_hex, mac_addr

# Ethernet Header
class Ethernet:
    def __init__(self, data):
        self.data = data  #sending to protocols
        self.dest_mac = ""
        self.src_mac = ""
        self.eth_protocol = ""
        self.ETH_LEN = 14

    # get the ethernet packet frames
    def frame(self):
        # #unpacking (retireving bytes 6s for dest and source) data = need only 14 bytes
        self.dest_mac, self.src_mac, self.eth_protocol = struct.unpack('!6s6sH', self.data[:14])
        return mac_addr(self.dest_mac), mac_addr(self.src_mac), socket.htons(self.eth_protocol)
        # return the destination, source address and the ethernet protocol

#Protocol Classes
class Protocol:
    def __init__(self, ethernet: Ethernet):
        self.data = ethernet.data  # got from ethernet.py
        self.eth = ethernet

        # types of ethernet protocol
        self.ETH_TYPE = {
            8: IPv4(self.data[ethernet.ETH_LEN:20+ethernet.ETH_LEN], ethernet), #0x0800
            56710: IPv6(self.data[ethernet.ETH_LEN:], ethernet), #0x86dd
            1544: ARP(self.data[ethernet.ETH_LEN:42]) #0x0806
        }

#Ipv6 Header
class IPv6:
    def __init__(self, data, eth: Ethernet):
        try:
            self.ipv6_first_word, self.payload_legth, self.protocol, self.hoplimit = struct.unpack(">IHBB", data[0:8])
            self.src_ip = socket.inet_ntop(socket.AF_INET6, data[8:24])
            self.dst_ip = socket.inet_ntop(socket.AF_INET6, data[24:40])
            self.version = self.ipv6_first_word >> 28
            traffic_class = int(self.ipv6_first_word >> 16) & 4095
            flow_label = int(self.ipv6_first_word) & 65535
        except ValueError:
            pass
            
    def __call__(self):
        print(f'--> Internet Protocol Version: {self.version}, Dst: {self.dst_ip}, Src: {self.src_ip}')
        print(f"First word: {self.ipv6_first_word}, Payload size: {self.payload_legth}, Protocol: {self.protocol}, Max Hops: {self.hoplimit} <---")

#Ipv4 Header
class IPv4:
    def __init__(self, ip_header, eth: Ethernet):
        self.ip_header = ip_header
        self.eth = eth
        # possible protocols    #dicts
        self.PROTOCOLS = {
            1: "ICMP",
            6: "TCP",
            17:"UDP",
            53: "DNS"
        }
        # unpack the header
        iph = struct.unpack('!BBHHHBBH4s4s', self.ip_header)
        # and get all the header info
        self.version_ihl = iph[0]
        # shift the version 4 bits to the left (>>)
        self.version = self.version_ihl >> 4
        # if the ihl version is hex 15 else 0  #internet header length
        self.ihl = self.version_ihl & 0xF  # hex(15) diff format
        self.iph_length = self.ihl * 4  # standa
        self.tot_len = iph[2]
        self.ttl = iph[5]
        self.protocol = iph[6]
        self.ip_checksum = iph[7]
        # get the ip adddress bytes and convert it to an IP
        self.s_addr = socket.inet_ntoa(iph[8])
        self.d_addr = socket.inet_ntoa(iph[9])

    def _show_pack(self):        # '_' means only inside a class
        # ICMP Packets
        if self.protocol == 1:
            u = self.iph_length + self.eth.ETH_LEN
            icmph_length = 4
            icmp_header = self.eth.data[u:u+4]

            # unpack the header
            icmph = struct.unpack('!BBH', icmp_header)
            icmp_type = icmph[0]
            code = icmph[1]
            checksum = icmph[2]
            # check for the status type
            type_status = ""
            if icmp_type == 0:
                type_status = "0 (Echo Reply)"
            elif icmp_type == 8:
                type_status = "8 (Echo Request)"
            print("---> Internet Control Message Protocol <---")
            print(f'Type: {type_status}, Code: {code}, Checksum: {checksum}')
            # get data from the packet and encode it as hex and print it
            h_size = self.eth.ETH_LEN + self.iph_length + \
                icmph_length  # calulate the header size
            # get the original data size from the data
            data_size = len(self.eth.data) - h_size
            # get the data from the header size calculated
            data = self.eth.data[h_size:]
            print(f'Data ( {encode_hex(bytes(data))})')
        #TCP HEADER
        if self.protocol == 6:
            packet = struct.unpack('!HHLLHHHHHH', self.eth.data[:24])
            print("---> Transmission Control Protocol <---")
            print(f"Src port: {packet[0]}, Dst port: {packet[1]}, Sequence: {packet[2]}, Aknowledgement: {packet[3]}")

        #UDP HEADER
        if self.protocol == 17:
            data = self.eth.data[self.eth.ETH_LEN:]
            src_port, dest_port, size = struct.unpack('!HH2xH', data[:8])
            data = data[8:]
            print("---> User Datagram Protocol <---")
            print(f"Src port: {src_port}, Dst port: {dest_port}, Size: {size}")
            print(f'Data ( {encode_hex(bytes(data))})')

        else:
            try:
                # some other IP packet like IGMP
                # print the protocol from the dict
                print(f'Protocol : {self.PROTOCOLS[self.protocol]}')
            except KeyError:
                print(f"Protocol : {self.protocol}")  # to skip key error

    # python's dunder method: runs when the instance of the class is called
    def __call__(self):
        print(f'---> Internet Protocol Version: {self.version}, Header_length: {self.iph_length}, TTL: {self.ttl}')
        print(f"Protocol: {self.protocol}, Checksum: {self.ip_checksum}, Source IP: {self.s_addr}, Destination IP: {self.d_addr} <---")
        self._show_pack()

#ARP Header
class ARP:
    def __init__(self, arp_header):
        self.arp_header = arp_header
        arph = struct.unpack("!2s2s1s1s2s6s4s6s4s", self.arp_header)

        # convert bytes to hex and then decode it as string
        self.protocol_size = binascii.hexlify(arph[3]).decode('utf-8')
        self.protocol_type = binascii.hexlify(arph[1]).decode('utf-8')

        # get the mac address bytes and convert it to a string
        self.src_mac = mac_addr(arph[5])
        self.dst_mac = mac_addr(arph[7])

        # get the ip bytes and convert it to an IP string
        self.src_ip = socket.inet_ntoa(arph[6])
        self.dst_ip = socket.inet_ntoa(arph[8])

    # python's dunder method: runs when the instance of the class is called
    def __call__(self):
        print("---> Address Resolution Protocol <---")
        print(f"Protocol Size: {self.protocol_size}, Protocol Type: {self.protocol_type}")
        print(f"who has: {self.dst_ip} ?,Target MAC Address: {self.dst_mac}")
        print(f"Tell: {self.src_ip}, Sender MAC: {self.src_mac}")
