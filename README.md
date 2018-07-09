These are two simple script write in python that allow sysadmin to configure the interface file on their linux distribution. In this way
we can emulate a dhcp server, without the need of have an actual dhcp-server in the network, and have all the computer static configurated 
based on their mac-address.

ip_setter_server:
This is the server. In a nut this script read from a file the ip-mac association and based on that it assign a configuration to the client that have sent a request. The configuration is a string that consist of: ip address, gateway address, dns address and the name of the network card that need to be configured using those parameters.

ip_setter_client:
This is the client. In a nut this script send a request to broadcast mac and wait for an answer from one server. After the answer is received it's parsed using split function and one by one the parameters of the configuration is estrapolated and is written  to interface
file. This script also modify the hostname of computer with it associated file based on the ip address. After all an "ok" packet is sent to server and the host is rebooted.

Future implementation:
-Creation of an automatic failure list, that based on "ok" packet receive create a list of host that has not been configured.
-Porting from a former C software the function that enable automatic WOL. In this way after an ok packet is received the server automatically boot the next pc in the list. The computer in the lab cannot be boot up at the same time, because initially they have all the same ip address, cause to linux socket implementation that have the need to have an ip address to sent and receive packet, despite the software use a raw socket that access directly the layer 2 of ISO-OSI
