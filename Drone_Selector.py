import customtkinter
from concurrent.futures import ThreadPoolExecutor
from CTkMessagebox import CTkMessagebox
import subprocess
import ipaddress
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("850x500")

def ping_host(ip):
    result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        return ip

def DroneSelectPage():
    def scan_network():
        cidr = "192.168.1.0/24"
        live_hosts = []
        network = ipaddress.ip_network(cidr)

        # Display loading screen
        loading_label = customtkinter.CTkLabel(master=frame, text="Scanning network...")
        loading_label.pack(padx=10, pady=10)
        root.update()
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
            var = customtkinter.CTkCheckBox(master=frame, text=host)
            var.pack(padx=10, pady=2)
            checkboxes.append((host, var))

    def select_device():
        selected_devices = [host for host, var in checkboxes if var.get()]
        if not selected_devices or len(selected_devices) > 1:
            CTkMessagebox(title="Error", message="Select One Device", icon="cancel") 
        else:
             selected_device_label.configure(text="Selected device(s): " + ', '.join(selected_devices))
        
    checkboxes = []

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(padx=10, pady=10)

    live_devices_label = customtkinter.CTkLabel(master=frame, text="Available devices:")
    live_devices_label.pack(padx=10, pady=5)

    selected_device_label = customtkinter.CTkLabel(master=frame, text="")
    selected_device_label.pack(padx=10, pady=5)

    select_button = customtkinter.CTkButton(master=frame, text="Select Device", command=select_device)
    select_button.pack(padx=10, pady=5)

    scan_network()  # Start the scan automatically

DroneSelectPage()
root.mainloop()
