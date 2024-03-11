import subprocess
import re
import socket
import os
import hashlib
import math
import sys
from scapy.all import *
from datetime import datetime
import json

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
class WiFiScanner:
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

# WiFi pasword Crack

# Scan connected Devices

# Select Drone

# Scan Ports

# Drone Password Brute Force

# ARP Spoofing & Vidieo Intercepting

# SSH Connection and Building aa backdoor

# Get Drone Manufacturer

# Turnon Camera

# Instruction Inejection

# main
interface_manager = InterfaceManager()
selected_interface = interface_manager.get_user_input()
print(f"Selected interface: {selected_interface}")