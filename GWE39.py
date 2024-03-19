import subprocess
import re
import socket
import os
import hashlib
import math
import sys
from scapy.all import *
import ipaddress
from datetime import datetime
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
    
    def extract_subnet(self,interface):
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

    def get_devices(self,cidr):
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
            device_info = {"mac": res[1].hwsrc, "ip": res[1].psrc, "name": self.get_device_name(res[1].psrc)}
            devices.append(device_info)
        return devices
    
    def get_device_name(self,ip_address):
        try:
            # Attempt to resolve the device name using NetBIOS queries
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname.split(".")[0]  # Use only the hostname part
        except (socket.herror, socket.gaierror):
            return ""  # Return an empty string if unable to resolve the device name
        
    def select_target_device(self, cidr):
        devices = self.get_devices(cidr)
        
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

    def scan_ports(host):
        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Adjust timeout as needed
                    s.connect((host, port))
                    service = socket.getservbyport(port)
                    print(f"Port {port} open: {service}")
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_version:
                            s_version.settimeout(1)  # Adjust timeout as needed
                            s_version.connect((host, port))
                            s_version.sendall(b"GET / HTTP/1.0\r\n\r\n")
                            banner = s_version.recv(1024).decode("utf-8")
                            print(f"Version: {banner.strip()}")
                    except socket.error:
                        pass
            except socket.error:
                pass
            
        print(f"Scanning host: {host}")
        with ThreadPoolExecutor(max_workers=50) as executor:
            for port in range(1, 1001):  # Scan common ports
                executor.submit(scan_port, port)

# ARP Spoofing & Vidieo Intercepting

# SSH Connection and Building aa backdoor

# Get Drone Manufacturer

# Turnon Camera

# Instruction Inejection

# main
interface_manager = InterfaceManager()
selected_interface = interface_manager.get_user_input()
wifi_scanner = WiFi_toolkit(selected_interface)
x= wifi_scanner.extract_subnet(selected_interface)
print(x)
drone_ip=wifi_scanner.select_target_device(x)
print(drone_ip)