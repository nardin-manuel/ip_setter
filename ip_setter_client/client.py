#!/usr/bin/python3
import binascii
from socket import *

def receive(interface):
	sock = socket(AF_PACKET, SOCK_RAW, htons(0x88b5))
	sock.bind((interface, 0))
	print("Attendo pacchetto")
	data = sock.recv(65536)
	sock.close()
	return unpack(data)

def unpack(packet):
	mac_dst = decode_mac(packet[:6])
	mac_src = decode_mac(packet[6:12])
        payload=decode_payload(packet[14:])
	print ("MAC DST: %s \nMAC SRC: %s" % (mac_dst, mac_src))
	print ("ETHERTYPE:", decode_ethertype(packet[12:14]))
	print ("PAYLOAD:" , payload)
        return mac_src, payload

def decode_mac(mac):
	_ = (binascii.hexlify(mac)).decode("ASCII")	
	return ":".join([_[x:x + 2] for x in range(0, len(_), 2)])

def decode_ethertype(ethertype):
	return binascii.hexlify(ethertype).decode("ASCII")

def decode_payload(payload):
	return payload.decode("ASCII")

def mac_to_hex(mac):
    mac = mac[:-1] if mac[-1] == '\n' else mac
    return binascii.unhexlify(mac.replace(":", ""))

def request(mac_dst, interface, payload):
    # print(mac_src)
	mac_source = mac_to_hex(open('/sys/class/net/' + interface + '/address').readline())
# 	mac_source=mac_to_hex(mac_source)
	mac_dest = mac_to_hex(mac_dst)
	ethertype = binascii.unhexlify("88B6")
	payload = payload.encode("ASCII")
	sock = socket(AF_PACKET, SOCK_RAW, htons(0x0003))
	sock.bind((interface, 0))
# 	print (mac_source)
	sock.send(mac_dest + mac_source + ethertype + payload)
	print("invio")
	sock.close()

def set_interfaces(payload):
	interfaces, ip, netmask, gateway, dns=payload.split(":",4))
	string=("auto lo \n
	iface lo inet loopback\n
	\n
	auto "+interface+"\n
	iface "+interface+" inet static\n
	address "+ip+"\n
	gateway "+gateway+"\n
	netmask "+netmask+"\n
	dns-nameservers "+dns+"\n")
	file=open("/etc/network/interfaces", "w")
        file.write(string)
        file.close()

request("ff:ff:ff:ff:ff:ff", "enp0s25", "1")
mac, payload=receive("enp0s25")
set_interfaces(payload)
request(mac, "enp0s25", "OK")
