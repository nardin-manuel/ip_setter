#!/usr/bin/python3
import binascii
import time
from socket import *
def read_file():
    delimeter = " "
    confirmed = "n"
    line_list = {'mac':[], 'ip':[]}
    
    while (confirmed != "s"):
        
        file_src = input("Inserisci la path del file: ")
        print("il file selezionato e' il seguente:", file_src, "accettare?[s/N]")
        confirmed = input()
    file = open(file_src, "r")
        
    for line in file:
        line = (line[:-1] if '\n' in line else line).split(delimeter, 1)  # tutta la linea tranne l'ultimo carattere(\n). Splitto sul delimeter. 1 solo delimimeter nella stringa
        print (line)
        line_list['mac'].append(line[0])
        line_list['ip'].append(line[1])
    file.close()
    return line_list
    
def find_ip_by_mac(line_list, mac):
    return line_list['ip'][line_list['mac'].index(mac)]
      
def mac_to_hex(mac):
    mac=mac[:-1] if mac[-1]=='\n' else mac
    return binascii.unhexlify(mac.replace(":",""))

def sendto(mac_dst, interface, payload):
     mac_source=mac_to_hex(open('/sys/class/net/'+interface+'/address').readline())
     mac_dest = mac_to_hex(mac_dst)
     ethertype=binascii.unhexlify("88B5")
     _=("ip:192.168.1.1\n netmask:255.255.255.0\n gateway:192.168.1.254\n dns-nameservers:8.8.8.8-8.8.4.4")
     payload=_.encode("ASCII")
     sock=socket(AF_PACKET, SOCK_RAW, htons(0x0003))
     sock.bind((interface,0))
     print (mac_source)
     sock.send(mac_dest+mac_source+ethertype+payload)
     print("invio") 
#     sock.close()

def receive(interface):
     sock=socket(AF_PACKET, SOCK_RAW, htons(0x88b6))
     sock.bind((interface,0))
     data=sock.recv(65536)
     return unpack(data)
#     sock.close()


def unpack(packet):
     mac_dst=decode_mac(packet[:6])
     return decode_mac(packet[6:12])
     print ("MAC DST: %s \nMAC SRC: %s"% ( mac_dst, mac_src))
     print ("ETHERTYPE:", decode_ethertype(packet[12:14]))
     print ("PAYLOAD:" , decode_payload(packet[14:]))

def decode_mac(mac):
     _=(binascii.hexlify(mac)).decode("ASCII")     
     return ":".join([_[x:x+2] for x in range(0, len(_), 2)])

def decode_ethertype(ethertype):
     return binascii.hexlify(ethertype).decode("ASCII")

def decode_payload(payload):
     return payload.decode("ASCII")


#line_list = read_file()
#ip=find_ip_by_mac(line_list, "7c:5c:f8:52:73:08")
payload="l'indirizzo che avrai e': "
for i in range(0, 10):
    mac=receive("lo")
    sendto(mac,"lo", payload)
