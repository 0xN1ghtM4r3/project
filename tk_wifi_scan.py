import customtkinter
import subprocess
import re

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("850x500")

def connect_to_wifi(wifi_name, password):
    command = f'nmcli device wifi connect "{wifi_name}" password "{password}"'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Connected to {wifi_name} successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to connect to {wifi_name}.")

class WifiScannerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Wi-Fi Network Scanner")

        self.selected_network = None
        
        self.scan_button = customtkinter.CTkButton(self.master, text="Scan", command=self.networks_list)
        self.scan_button.pack(pady=10)
        
        self.network_combobox = customtkinter.CTkComboBox(self.master,values=self.networks_list(), state="readonly")
        self.network_combobox.pack(pady=5)
        
        self.password_label = customtkinter.CTkLabel(self.master, text="Password:")
        self.password_label.pack(pady=5)
        
        self.password_entry = customtkinter.CTkEntry(self.master, show="*")
        self.password_entry.pack(pady=5)
        
        self.connect_button = customtkinter.CTkButton(self.master, text="Connect", command=self.connect)
        self.connect_button.pack(pady=5)
    def networks_list(self):
        nertworks = self.scan()
        return nertworks
    def scan(self):
        try:
            output = subprocess.check_output("iwlist wlan0 scan", shell=True).decode()
        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return
        
        networks = self.parse_scan_output(output)
        return networks
    
    def parse_scan_output(self, output):
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
        
        return [network["ESSID"] for network in networks if network["ESSID"]]
    
    def connect(self):
        selected_wifi_name = self.network_combobox.get()  # Get the selected Wi-Fi name
        if selected_wifi_name:  # Check if a Wi-Fi name is selected
            password = self.password_entry.get()
            connect_to_wifi(selected_wifi_name, password)

def main():
    app = WifiScannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
