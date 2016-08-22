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

def sendto(sock, mac_dst, interface, payload):
     mac_source=mac_to_hex(open('/sys/class/net/'+interface+'/address').readline())
     mac_dest = mac_to_hex(mac_dst)
     ethertype=binascii.unhexlify("88B5")
     _=("ip:192.168.1.1\n netmask:255.255.255.0\n gateway:192.168.1.254\n dns-nameservers:8.8.8.8-8.8.4.4")
     payload=_.encode("ASCII")
     sock.bind((interface,0))
     print (mac_source)
     sock.send(mac_dest+mac_source+ethertype+payload)
     print("inviato")
     
def open_socket_read():
    return socket(AF_PACKET, SOCK_RAW, htons(0x88b6))

def open_socket_write():
    return socket(AF_PACKET, SOCK_RAW, htons(0x88b5))

def receive(sock, interface):
     sock.bind((interface,0))
     data=sock.recv(65536)
     return unpack(data)

def unpack(packet):
     mac_dst=decode_mac(packet[:6])
     mac_src=decode_mac(packet[6:12])
     ethertype=decode_ethertype(packet[12:14]))
     payload= decode_payload(packet[14:]))
     print ("MAC DST: %s \nMAC SRC: %s" % (mac_dst, mac_src))
     print ("PAYLOAD:", payload)
     return mac_src, payload

def decode_mac(mac):
     _=(binascii.hexlify(mac)).decode("ASCII")     
     return ":".join([_[x:x+2] for x in range(0, len(_), 2)])

def decode_ethertype(ethertype):
     return binascii.hexlify(ethertype).decode("ASCII")

def decode_payload(payload):
     return payload.decode("ASCII")


#line_list = read_file()
payload="l'indirizzo che avrai e': "
sock_read=open_socket_read()
print("socket lettura aperto")
open_write=0;
while 1:
    print("Attendo client")
    packet=receive(sock_read, "lo")
    mac=packet[0]
    payload_recv=packet[1]
    if not open_write:
        sock_write=open_socket_write()
        print("socket scrittura aperto")
        open_write=1
    if open_write:
        time.sleep(0.1)
        #ip=find_ip_by_mac(line_list, mac) if payload_recv=="Voglio un ip"
        #if ip==-1: 
            #print("Errore, impossibile trovare l'indirizzo mac: %s nella tabella"%(mac))
        #else:
        sendto(sock_write, mac,"lo", payload)
