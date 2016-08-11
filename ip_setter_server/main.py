import socket


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
        line_list['mac'].append(line[0])
        line_list['ip'].append(line[1])
    file.close()
    return line_list
    
def find_ip_by_mac(line_list, mac):
    return line_list['ip'][line_list['mac'].index(mac)]
      
def connection():
    sock=socket.socket(AF_PACKET,SOCK_DGRAM)
    sock.bind(interface)
    sock.sendto("prova",mac_dest)
    
    
    
    

#line_list = read_file()
#print(line_list)
#print(find_ip_by_mac(line_list, "cc:bb:aa:dd:ee:ff"))
connection()