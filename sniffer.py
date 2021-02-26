#!/usr/bin/python3
import struct
import socket
from Packages.Protocols import Protocol, Ethernet


def main():
    # create a socket connection to listen for packets
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    #socket.ntohs(0x0003) tells capture everything including ethernet frames. To capture TCP, UDP, or ICMP only
    try:
        while True:
            # continuously receive/listen for data
            raw_data, _ = conn.recvfrom(65536)

            # create a new Ethernet instance with the raw_data captured
            eth = Ethernet(raw_data)
            dest_mac, src_mac, eth_protocol = eth.frame()  # gather the frame details

            # print the ethernet header info
            print(f'\n---> Ethernet Frame Destination Mac: {dest_mac}, Source Mac: {src_mac}, Type: {eth_protocol} <---')

            # create a protocol instance with the captured ethernet data
            proto = Protocol(eth)
            # call the ethernet type object based on the protocol type
            obj = proto.ETH_TYPE[eth_protocol]
            obj()
            print("")
    except ValueError as E:
        pass
    except KeyboardInterrupt:
        print("\n[END] STOPPED SNIFFING!")
        return


if __name__ == "__main__":
    main()
