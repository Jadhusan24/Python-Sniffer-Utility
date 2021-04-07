# Sniffer Utility
    This illustrates the use of TCP DUMB command

### [REFERENCE?](https://en.wikipedia.org/wiki/Packet_analyzer)
    Packet sniffer that can intercept and log traffic that passes over a computer network or part of a network.
  
  
[![Twitter](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jadhusan24/) 

### _USAGE_
- [x] Ethernet
- [x] ARP
- [x] IPv6
- [x] IPv4
- [x] TCP
- [x] UDP
- [x] ICMP
- [ ] DNS
  
#### I have tested this program on Windows 10 Enterprise using WSL ver 2.

![WinVer](./Screenshots/win.jpg) ![WinVer](./Screenshots/wsl.jpg)

-----------------------------------
###       W I N D O W S
-----------------------------------
Excute this program using WSL
- open WSL Terminal
- navigate to  file path
- type the following command
>python sniffer.py www.github.com [DomainName] <br/>
>python sniffer.py 8.8.8.8 [IpAddr] <br/>
-----------------------------------
###         L I N U X
-----------------------------------
- open terminal
- navigate to file path
- type the following command
>sudo python3 sniffer.py www.github.com [DomainName] <br/>
>sudo python3 sniffer.py 8.8.8.8 [IpAddr] <br/>

### _REQUIRMENT_
- Run using SUDO privilege
- Run using Administration privilege

### _RESULT_

- Ethernet
    ![WinVer](./Screenshots/1.jpg)

- ARP
    ![WinVer](./Screenshots/2.jpg)

- ICMP
    ![WinVer](./Screenshots/3.jpg)
    
- UDP
    ![WinVer](./Screenshots/4.jpg)

- TCP
    ![WinVer](./Screenshots/5.jpg)

- IPv4
    ![WinVer](./Screenshots/6.jpg)

- IPv6
    ![WinVer](./Screenshots/7.jpg)

### Demonstration 

![](/Screenshots/output.gif)
