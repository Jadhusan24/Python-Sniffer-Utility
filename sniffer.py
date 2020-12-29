#raw socket is an internet socket that allows direct sending and 
#receiving of Internet Protocol packets without any protocol-specific transport layer formatting.
import struct
import socket
from Packages.Ethernet import Ethernet
from Packages.Protocols import Protocol


def main():
    # create a socket connection to listen for packets
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    try:
        while True:
            # continuously receive/listen for data
            raw_data, _ = conn.recvfrom(65536)

            # create a new Ethernet instance with the raw_data captured
            eth = Ethernet(raw_data)
            dest_mac, src_mac, eth_protocol = eth.frame()  # gather the frame details

            # print the ethernet header info
            print(
                f'\nEthernet Frame Dst {dest_mac}, Src: {src_mac}, Type {eth_protocol}')

            proto = Protocol(eth)
            obj = proto.ETH_TYPE[eth_protocol]
            obj()
            print("")
    except KeyboardInterrupt:
        print("\n[END] STOPPED SNIFFING!")
        return


if __name__ == "__main__":
    main()
