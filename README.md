These are two simple scripts written in python that allow sysadmin to configure the interface file on their Linux distribution. In this way, we can simulate a DHCP server, without having a physical one in the network, and, therefore, to have all the computers statically configured based on their mac-address.

ip_setter_server: this is the server. Basically, this script reads from a file the IP-MAC association and based on that it assigns a configuration to the client that had has sent a request. The configuration is a string that is consisted by the following substrings: IP address, gateway address, DNS address and the name of the network card that needs to be configured using those parameters.

ip_setter_client: this is the client. Briefly, this script sends a request to MAC broadcast and waits for an answer from ip_setter_server. Once it receives the answer, it will parse it by using the split function and one by one the parameters of the configuration will be extrapolated and written into the interface file. This script also modifies the hostname of computer based on its IP address. After completing all these tasks, it will send an "OK" packet to the server and the host will be rebooted.

Future implementations: 

-Creation of an automatic failure list: this consists on creating a list of all the computers where the configuration have been sent but did not replayed with “OK” packet.

-Porting from a former C software the function that enables automatic WOL. This will allow to boot automatically the next computer in the list once the “OK” packet has been received. However, it is not possible to boot up all the computers together because, at the initial stage, they all have the same IP address. This is due to Linux socket implementation that has the need of having an IP address to send and receive despite the software using a raw socket that access directly the layer 2 of ISO-OSI
