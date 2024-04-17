import customtkinter
from concurrent.futures import ThreadPoolExecutor
import subprocess
import ipaddress
import time

def ping_host(ip):
    result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        return ip

def scan_network():
    cidr = "192.168.1.0/24"
    live_hosts = []
    network = ipaddress.ip_network(cidr)

    # Display loading screen
    loading_label = customtkinter.CTkLabel(master=app, text="Scanning network...")
    loading_label.pack(padx=10, pady=10)
    app.update()
    time.sleep(2)  # Simulate scan time (adjust as needed)
    loading_label.destroy()

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(ping_host, str(ip)) for ip in network.hosts()]
    for future in futures:
        result = future.result()
        if result:
            live_hosts.append(result)
    populate_checkbox(live_hosts)

def populate_checkbox(live_hosts):
    for host in live_hosts:
        var = customtkinter.CTkCheckBox(master=app, text=host)
        var.pack(padx=10, pady=2)
        checkboxes.append((host, var))

def start_scan():
    # Removed functionality as scan starts automatically
    pass

def select_device():
    selected_devices = [host for host, var in checkboxes if var.get()]
    selected_device_label.set_textc("Selected device(s): " + ', '.join(selected_devices))

app = customtkinter.CTk()
app.geometry("400x300")
app.title("Network Scanner")

# Removed CIDR entry as it's pre-defined

scan_button = customtkinter.CTkButton(master=app,text="Re-scan", command=start_scan)
scan_button.pack(padx=10, pady=5)

checkboxes = []

live_devices_label = customtkinter.CTkLabel(master=app,text="")
live_devices_label.pack(padx=10, pady=5)

selected_device_label = customtkinter.CTkLabel(master=app,text="")
selected_device_label.pack(padx=10, pady=5)

# Start the scan automatically
scan_network()

app.mainloop()
