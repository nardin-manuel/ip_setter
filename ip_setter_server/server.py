#!/usr/bin/python3
import binascii
import time
from socket import *
def read_file():
	delimeter = " "
	confirmed = "n"
	line_list = {'mac':[], 'ip':[]}

	while (confirmed != "s"):
		file_src = input("Inserisci il path del file: ")
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
	mac = mac[:-1] if mac[-1] == '\n' else mac
	return binascii.unhexlify(mac.replace(":", ""))

def sendto(sock, mac_dst, interface, payload):
	mac_source = mac_to_hex(open('/sys/class/net/' + interface + '/address').readline())
	mac_dest = mac_to_hex(mac_dst)
	ethertype = binascii.unhexlify("88B5")
	#_ = ("ip:192.168.1.1\n netmask:255.255.255.0\n gateway:192.168.1.254\n dns-nameservers:8.8.8.8-8.8.4.4")
	payload = payload.encode("ASCII")
	sock.bind((interface, 0))
#	print (mac_source)
	sock.send(mac_dest + mac_source + ethertype + payload)
	print("inviato")

def open_socket_read():
	return socket(AF_PACKET, SOCK_RAW, htons(0x88b6))

def open_socket_write():
	return socket(AF_PACKET, SOCK_RAW, htons(0x88b5))

def receive(sock, interface):
	sock.bind((interface, 0))
	data = sock.recv(65536)
	return unpack(data)

def unpack(packet):
	mac_dst = decode_mac(packet[:6])
	mac_src = decode_mac(packet[6:12]).upper()
	ethertype = decode_ethertype(packet[12:14])
	payload = decode_payload(packet[14:])
	print ("MAC DST: %s \nMAC SRC: %s" % (mac_dst, mac_src))
	print ("PAYLOAD:", payload)
	return mac_src, payload

def decode_mac(mac):
	_ = (binascii.hexlify(mac)).decode("ASCII")	
	return ":".join([_[x:x + 2] for x in range(0, len(_), 2)])

def decode_ethertype(ethertype):
	return binascii.hexlify(ethertype).decode("ASCII")

def decode_payload(payload):
	return payload.decode("ASCII")

def ack_recv(line_list, out_list, mac):
	ip = find_ip_by_mac(line_list, mac)
	out_list['mac'].append(mac)
	out_list['ip'].append(ip)
	print("OK ricevuto dall' ip:", ip)

def create_recovery_file(out_list):
	confirmed = "n"
	while (confirmed != "s"):
		file_src = input("Inserisci la path del file: ")
		print("il file selezionato e' il seguente:", file_src, "accettare?[s/N]")
		confirmed = input()
	file = open(file_src, "w")
	for i in range(len(out_list['mac'])):
		
		file.write(out_list['mac'][i] + " " + out_list['ip'][i] + "\n")
	file.close()
	
	
#****************************************************MAIN****************************************************#
line_list = read_file()
gateway = input("Inserisci il gateway: ")
interface = input("Inserisci interfaccia: ")
netmask="255.255.255.0"
dns = "8.8.8.8 172.16.240.253"
out_list = {'mac':[], 'ip':[]}
sock_read = open_socket_read()
print("socket lettura aperto")
open_write = 0;
i = 0
while i < (len(line_list['ip'])):
	print("Attendo client")
	mac, payload_recv = receive(sock_read, "enp4s0")	
	if not open_write:
		sock_write = open_socket_write()
		print("socket scrittura aperto")
		open_write = 1
	if open_write:
		time.sleep(0.1)
		#print(id(stringa),id(payload_recv))
		print(repr(payload_recv))
		if "1" in payload_recv:
			try:
				ip = find_ip_by_mac(line_list, mac)
				print ("Richiesta ricevuta dall'ip:", ip)
				print("Richiesta #:", i+1)
				payload = (interface + ":" + ip + ":" +netmask+ ":" + gateway + ":" + dns)
				sendto(sock_write, mac, "enp4s0", payload)
				i += 1
			except ValueError:	
				print("Errore, impossibile trovare l'indirizzo mac: %s nella tabella" % (mac))
		elif "OK" in payload_recv:
			ack_recv(line_list, out_list, mac)
		else:
			print("Ricevuto una cosa strana:", payload_recv)		
sock_read.close()
sock_write.close()
print("A tutti i computer nella lista e' stato dato un ip")
if(len(line_list['ip']) > len(out_list['ip'])):
	print ("Non tutti i computer hanno risposto")
	s = set(out_list['mac'])
	out_list['mac'] = [line for line in line_list['mac'] if line not in s]
	out_list['ip'] = [find_ip_by_mac(line_list, mac) for mac in out_list['mac']]
	print("i computer che non hanno risposto sono i seguenti:", out_list)
	create_recovery_file(out_list) if (input("vuoi creare un file contenente solo i computer che non hanno risposto per riprovare?[Y/n]") == "Y") else exit	
else:
	print("Tutti i computer hanno risposto")
	exit

