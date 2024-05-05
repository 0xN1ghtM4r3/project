import customtkinter
from CTkMessagebox import CTkMessagebox
import tkinter
import psutil
import hashlib
from concurrent.futures import ThreadPoolExecutor
import subprocess
import ipaddress
import time
import json
import socket
from scapy.all import *
from tkinter import ttk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("850x500")

global frame
global frame1

drone_ip = None
selected_interface = None
selected_manufacturer = None 


def test_1():
    print("testing")


def test_2():
    print("checkpoint")

def des1():
    frame1.destroy()

def des2():
    frame2.destroy()

def des3():
    frame3.destroy()

def des4():
    frame4.destroy()

def des5():
    frame5.destroy()

def des6():
    frame6.destroy()

def des7():
    frame7.destroy()

def des8():
    frame8.destroy()

def des9():
    frame9.destroy()

def des10():
    frame10.destroy()
def des11():
    frame11.destroy()

# def des11():
#     frame11.destroy()
#
def des12():
    frame12.destroy()

def des13():
    frame13.destroy()


# ------------------------------------------------------------
# ------------------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON data in users.json file.")
        return {}


def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)


def Login():
    global frame
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    def user_login():
        users = load_users()
        username = username_entry.get()
        password = password_entry.get()
        hashed_password = hash_password(password)
        print("Username:", username)
        print("Password:",hashed_password)
        if username in users:
            if users[username]["password"] == hashed_password:
                print("Login successful!")
                Homepage()
                return True
            else:
                CTkMessagebox(title="Error", message="Incorrect password", icon="cancel")
        else:
            CTkMessagebox(title="Error", message="Username or Password Invalid", icon="cancel")

    label = customtkinter.CTkLabel(master=frame, text="Login", font=("Roboto", 24))
    label.pack(pady=(40, 10), padx=10)

    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=250)
    username_entry.pack(pady=(10, 10), padx=10)

    password_entry = customtkinter.CTkEntry(master=frame, show="*", placeholder_text="Password", width=250)
    password_entry.pack(pady=(10, 10), padx=10)

    login_button = customtkinter.CTkButton(master=frame, text="Login", command=user_login)
    login_button.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame, text="Sign up", command=Sign_up)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame, text="Forget Password !", command=Reset, fg_color="transparent")
    button3.pack(pady=2, padx=10)

    switch = customtkinter.CTkSwitch(master=frame, text="Remember me?", onvalue="on", offvalue="off")
    switch.pack(pady=12, padx=10)


def Sign_up():
    frame.destroy()
    global frame1
    frame1 = customtkinter.CTkFrame(master=root)
    frame1.pack(pady=20, padx=60, fill="both", expand=True)

    def create_user():
        users = load_users()
        username = create_user_entry.get()
        if username in users:
            print("Username already exists.")
            CTkMessagebox(title="Error", message="User already exists.", icon="cancel")
            return
        password = create_password_entry.get()
        hashed_password = hash_password(password)
        users[username] = {"password": hashed_password}
        save_users(users)
        CTkMessagebox(title="Success", message="User created successfully.", icon="check")
        print("User created successfully.")

    label = customtkinter.CTkLabel(master=frame1, text="Sign up", font=("Roboto", 24))
    label.pack(pady=(10, 10), padx=10)

    create_user_entry = customtkinter.CTkEntry(master=frame1, placeholder_text="Username", width=250)
    create_user_entry.pack(pady=(10, 10), padx=10)

    create_password_entry = customtkinter.CTkEntry(master=frame1, show="*", placeholder_text="Password", width=250)
    create_password_entry.pack(pady=(10, 10), padx=10)

    check_var = customtkinter.StringVar(value="off")
    checkbox = customtkinter.CTkCheckBox(frame1, text=" I Have Read and Agree to Terms and Conditions",
                                         variable=check_var, onvalue="on", offvalue="off")
    checkbox.pack(pady=5, padx=10)

    button1 = customtkinter.CTkButton(master=frame1, text="Create Account", command=create_user)
    button1.pack(pady=5, padx=10)

    button3 = customtkinter.CTkButton(master=frame1, text="Already Have an Account !",
                                      command=lambda: [des1(), Login()], fg_color="transparent")
    button3.pack(pady=2, padx=10)


def Reset():
    frame.destroy()
    global frame2
    frame2 = customtkinter.CTkFrame(master=root)
    frame2.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame2, text="Password Reset", font=("Roboto", 24))
    label.pack(pady=(40, 10), padx=10)

    entry = customtkinter.CTkEntry(master=frame2, placeholder_text="Username", width=250)
    entry.pack(pady=(10, 10), padx=10)

    entry2 = customtkinter.CTkEntry(master=frame2, placeholder_text="Email", width=250)
    entry2.pack(pady=(10, 10), padx=10)

    entry2 = customtkinter.CTkEntry(master=frame2, placeholder_text="Confirmation Code (OTP)", width=250)
    entry2.pack(pady=(10, 10), padx=10)

    button1 = customtkinter.CTkButton(master=frame2, text="Reset", command=test_1)
    button1.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame2, text="Back", command=lambda: [des2(), Login()],
                                      fg_color="transparent")
    button3.pack(pady=2, padx=10)


# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
def Homepage():
    frame.destroy()
    global frame3
    frame3 = customtkinter.CTkFrame(master=root)
    frame3.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame3, text="Drone Pentesting", font=("Roboto", 46))
    label.pack(pady=(60, 35), padx=10)

    button1 = customtkinter.CTkButton(master=frame3, text="Scan", command=interface_page)
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame3, text="History", command=History)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame3, text="Back", command=lambda: [des3(), Login()],
                                      fg_color="transparent")
    button3.pack(pady=2, padx=10)


# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************

def interface_page():
    frame3.destroy()
    global frame4
    frame4 = customtkinter.CTkFrame(master=root)
    frame4.pack(pady=20, padx=60, fill="both", expand=True)
    

    def get_network_interfaces():
        # Get a list of network interfaces
        interfaces = psutil.net_if_addrs()
        return list(interfaces.keys())

    def select_interface():
        global selected_interface
        selected_interface = interface_combobox.get()
        print("Selected Interface:", selected_interface)
        WifiScan()

    # Create the main application window
    '''root.title("Select Network Interface")'''

    # Get available network interfaces
    interfaces = get_network_interfaces()

    # Create a label
    label = customtkinter.CTkLabel(master=frame4, text="Select Network Interface:")
    label.pack(pady=10)

    # Create a combobox to select the network interface
    interface_combobox = customtkinter.CTkComboBox(master=frame4, values=interfaces, state="readonly")
    interface_combobox.pack()

    # Create a button to select the interface
    select_button = customtkinter.CTkButton(master=frame4, text="Select Interface", command=select_interface)
    select_button.pack(pady=10)

    button = customtkinter.CTkButton(master=frame4, text="Back", command=lambda: [des4(), Homepage()],
                                      fg_color="transparent")
    button.pack(pady=10, padx=10)

# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
def networks_list():
    nertworks = scan()
    return nertworks

def scan():
    try:
        output = subprocess.check_output(f"iwlist {selected_interface} scan", shell=True).decode()
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return
    networks = parse_scan_output(output)
    return networks


def parse_scan_output(output):
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


def connect_to_wifi(wifi_name, password):
    command = f'nmcli device wifi connect "{wifi_name}" password "{password}"'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Connected to {wifi_name} successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to connect to {wifi_name}.")

# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************

def WifiScan():
    frame4.destroy()
    global frame5
    frame5 = customtkinter.CTkFrame(master=root)
    frame5.pack(pady=20, padx=60, fill="both", expand=True)

    selected_network = None

    def connect():
        selected_wifi_name = network_combobox.get()  # Get the selected Wi-Fi name
        if selected_wifi_name:  # Check if a Wi-Fi name is selected
            password = password_entry.get()
            connect_to_wifi(selected_wifi_name, password)
            DroneSelectPage()

    scan_button = customtkinter.CTkButton(master=frame5, text="Scan", command=networks_list)
    scan_button.pack(pady=10)
    network_combobox = customtkinter.CTkComboBox(master=frame5, values=networks_list(), state="readonly")
    network_combobox.pack(pady=5)
    password_label = customtkinter.CTkLabel(master=frame5, text="Password:")
    password_label.pack(pady=5)
    password_entry = customtkinter.CTkEntry(master=frame5, show="*")
    password_entry.pack(pady=5)
    connect_button = customtkinter.CTkButton(master=frame5, text="Connect", command=connect)
    connect_button.pack(pady=5)

    button4 = customtkinter.CTkButton(master=frame5, text="Back", command=lambda: [des5(), interface_page()])
    button4.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)


# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
## Drone selector
def ping_host(ip):
    result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        return ip

def DroneSelectPage():
    frame5.destroy()
    global frame6
    frame6 = customtkinter.CTkFrame(master=root)
    frame6.pack(pady=20, padx=60, fill="both", expand=True)

    def scan_network():
        #cidr = "192.168.87.0/24"
        #cidr = "10.0.0.0/22"
        cidr = "192.168.1.0/24"
        live_hosts = []
        network = ipaddress.ip_network(cidr)

        # Display loading screen
        loading_label = customtkinter.CTkLabel(master=frame6, text="Scanning network...")
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
            var = customtkinter.CTkCheckBox(master=frame6, text=host)
            var.pack(padx=10, pady=2)
            checkboxes.append((host, var))

    def select_device():
        selected_devices = [host for host, var in checkboxes if var.get()]
        if not selected_devices or len(selected_devices) > 1:
            CTkMessagebox(title="Error", message="Select One Device", icon="cancel") 
        else:
            global drone_ip
            drone_ip = selected_devices[0]  # Save selected drone IP globally
            selected_device_label.configure(text="Selected device: " + drone_ip)
            time.sleep(1)
            manufacturer_page()
            #selected_manufacturer()
    checkboxes = []

    live_devices_label = customtkinter.CTkLabel(master=frame6, text="Available devices:")
    live_devices_label.pack(padx=10, pady=5)

    selected_device_label = customtkinter.CTkLabel(master=frame6, text="")
    selected_device_label.pack(padx=10, pady=5)

    select_button = customtkinter.CTkButton(master=frame6, text="Select Device", command=select_device)
    select_button.pack(padx=10, pady=5)

    scan_network()  # Start the scan automatically   
# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
## manfucture selector
def manufacturer_page():
    frame6.destroy()
    global frame7
    frame7 = customtkinter.CTkFrame(master=root)
    frame7.pack(pady=20, padx=60, fill="both", expand=True)
    def choose_manufacturer():
        """Gets the selected manufacturer from the combobox and saves it in `selected_manufacturer`."""
        global selected_manufacturer  # Declare variable as global to access outside the function
        selected_manufacturer = combobox.get()
        print("You selected:", selected_manufacturer)
        Scan_Page()


  # Create the label
    label = customtkinter.CTkLabel(master=frame7, text="Select a manufacturer:")
    label.pack(padx=10, pady=10)

  # Create the combobox widget
    manufacturers = ["DJI", "Parrot", "Yuneec"]
    combobox = customtkinter.CTkComboBox(master=frame7, values=manufacturers)
    combobox.pack(padx=10, pady=10)

  # Create the button
    button = customtkinter.CTkButton(master=frame7, text="Choose", command=choose_manufacturer )
    button.pack(padx=10, pady=10)

  # Declare `selected_manufacturer` globally (optional, but recommended for clarity)

# ********************************************************************************************
# ********************************************************************************************
# ********************************************************************************************
def Scan_Page():
    frame7.destroy()
    global frame8
    frame8 = customtkinter.CTkFrame(master=root)
    frame8.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame8, text="Choose Test method...", font=("Roboto", 36))
    label.pack(pady=(60, 35), padx=10)

    button1 = customtkinter.CTkButton(master=frame8, text="Full Test", command=FullTest)
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame8, text="Custom Test", command=CustomTest)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame8, text="Back", command=lambda: [des8(), manufacturer_page()],
                                      fg_color="transparent")
    button3.pack(pady=12, padx=10)


def FullTest():
    frame8.destroy()
    global frame9
    frame9 = customtkinter.CTkFrame(master=root)
    frame9.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame9, text="Testing...", font=("Roboto", 36), text_color="#329983")
    label.pack(pady=20, padx=20)
    
    button = customtkinter.CTkButton(master=frame9, text="Port Scanning", command=ports)
    button.pack(pady=18, padx=40)
   
    button4 = customtkinter.CTkButton(master=frame9, text="Back", command=lambda: [des9(), Scan_Page()])
    button4.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)

def CustomTest():
    frame8.destroy()
    global frame11
    frame11 = customtkinter.CTkFrame(master=root)
    frame11.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame11, text="Choose Test Method", font=("Roboto", 36), text_color="#329983")
    label.pack(pady=20, padx=20)

    radio = customtkinter.CTkRadioButton(frame11, text="Test 1")
    radio.pack(pady=(6, 3), padx=50, anchor="w")
    radio2 = customtkinter.CTkRadioButton(frame11, text="Test 2")
    radio2.pack(pady=(6, 3), padx=50, anchor="w")
    radio3 = customtkinter.CTkRadioButton(frame11, text="Test 3")
    radio3.pack(pady=(6, 3), padx=50, anchor="w")
    radio4 = customtkinter.CTkRadioButton(frame11, text="Test 4")
    radio4.pack(pady=(6, 3), padx=50, anchor="w")

    button3 = customtkinter.CTkButton(master=frame11, text="Start Test", command=test_1)
    button3.pack(pady=(0, 18), padx=(0, 40), anchor="se", expand=True)

    button4 = customtkinter.CTkButton(master=frame11, text="Back", command=lambda: [des11(), Scan_Page()])
    button4.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)

#****************************************************************************************
#****************************************************************************************
#**************************************ports*******************************************
#****************************************************************************************
def scan_ports(target_host, result_text):
    open_ports = []

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Adjust timeout as needed
                result = s.connect_ex((target_host, port))
                if result == 0:
                    service = socket.getservbyport(port)
                    open_ports.append((port, service))
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_version:
                            s_version.settimeout(1)  # Adjust timeout as needed
                            s_version.connect((target_host, port))
                            s_version.sendall(b"GET / HTTP/1.0\r\n\r\n")
                            banner = s_version.recv(1024).decode("utf-8")
                            print(f"Version: {banner.strip()}")
                    except socket.error:
                        pass
        except socket.error:
            pass
    
    result_text.delete("1.0", customtkinter.END)
    result_text.insert(customtkinter.END, f"Scanning host: {target_host}\n")
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, port) for port in range(1, 1001)]  # Scan common ports
        for future in futures:
            future.result()  # Wait for all tasks to complete
    result_text.insert(customtkinter.END, "Open ports:\n")
    for port, service in open_ports:
        result_text.insert(customtkinter.END, f"Port: {port}, Service: {service}\n")

def scan_button_clicked():
    target_host = drone_ip
    if not target_host:
        customtkinter.showwarning("Warning", "Please enter a target host.")
        return
    scan_ports(target_host, result_text)
    
def ports():
    frame9.destroy()
    global frame12
    frame12 = customtkinter.CTkFrame(master=root)
    frame12.pack(pady=20, padx=60, fill="both", expand=True)
    
    scan_button = customtkinter.CTkButton(master=frame12, text="Scan Ports", command=scan_button_clicked)
    scan_button.pack(padx=10, pady=20)
    next_button = customtkinter.CTkButton(master=frame12, text="next", command=DroneControllerPage)
    next_button.pack(padx=10, pady=20)
    global result_text
    result_text = customtkinter.CTkTextbox(master=frame12, width=200, height=200)
    result_text.pack(padx=10, pady=5)
    
    
#****************************************************************************************
#****************************************************************************************
#****************************************************************************************
#****************************************************************************************

def send_payload(command, seq_num):
        ip_address = drone_ip  # Replace "your_ip_address" with the actual IP address
        port = 5556  # Adjust the port number according to your setup
        try:
            if command == "up":
                payload = "AT*REF={},290717696\r"
            elif command == "down":
                payload = "AT*REF={},290711696\r"
            elif command == "right":
                payload = "AT*REF={},290721696\r"
            elif command == "left":
                payload = "AT*REF={},290731696\r"
            elif command == "takeoff":
                payload = "AT*REF={},290741696\r"
            elif command == "land":
                payload = "AT*REF={},290751696\r"
            elif command == "turnoncamera":
                payload = "AT*REF={},2907510942\r"
            else:
                log("Invalid command. Please enter 'up', 'down', 'right', 'left', 'takeoff', 'land', or 'turnOnCamera'.")
                return
            
            formatted_payload = payload.format(seq_num)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(formatted_payload.encode(), (ip_address, port))
            sock.close()
            log("Payload sent successfully: " + formatted_payload)
        
        except Exception as e:
            log("Error: " + str(e))
        
def send_command(command):
        seq_num = 0
        packet_count = 0
        if command in ["up", "down", "right", "left", "takeoff", "land"]:
            while packet_count < 5:
                send_payload(command, seq_num)
                time.sleep(1)
                seq_num += 1
                packet_count += 1
            packet_count = 0
        elif command == "turnoncamera":
            send_payload(command, 0)
            subprocess.Popen('pkill nc; pkill vlc', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) 
            time.sleep(1)
            subprocess.Popen('nc -nvlp 1111 -u | vlc -', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)  
            time.sleep(1)
        else:
            log("Invalid command. Please enter 'up', 'down', 'right', 'left', 'takeoff', 'land', or 'turnOnCamera'.")
        
def log(message):
        log_text.insert(customtkinter.END, message + "\n")
        log_text.see(customtkinter.END)

def DroneControllerPage():
    frame12.destroy()
    global frame13
    frame13 = customtkinter.CTkFrame(master=root)
    frame13.pack(pady=20, padx=60, fill="both", expand=True)
  
        
        # Create buttons for each command
    button_up = customtkinter.CTkButton( master=frame13, text="Up ⬆️", command=lambda: send_command("up"))
    button_up.grid(row=1, column=250, padx=5, pady=5)
        
    button_down = customtkinter.CTkButton(  master=frame13, text="Down ⬇️", command=lambda: send_command("down"))
    button_down.grid(row=2, column=250, padx=5, pady=5)
        
    button_right = customtkinter.CTkButton(master=frame13, text="Right ➡️", command=lambda: send_command("right"))
    button_right.grid(row=2, column=270, padx=5, pady=5)
        
    button_left = customtkinter.CTkButton(master=frame13, text="Left ⬅️", command=lambda: send_command("left"))
    button_left.grid(row=2, column=230, padx=5, pady=5)
        
    button_takeoff = customtkinter.CTkButton(master=frame13, text="Takeoff 🚀", command=lambda: send_command("takeoff"))
    button_takeoff.grid(row=3, column=230, padx=5, pady=5)
        
    button_land = customtkinter.CTkButton(master=frame13, text="Land 🛬", command=lambda: send_command("land"))
    button_land.grid(row=3, column=270, padx=5, pady=5)
        
    button_camera = customtkinter.CTkButton(master=frame13, text="Turn On Camera 📷", command=lambda:send_command("turnoncamera"))
    button_camera.grid(row=3, column=250, padx=5, pady=5)
        
        #Log text area
    global log_text
    log_text = customtkinter.CTkTextbox(master=frame13, height=200, width=400)
    log_text.grid(row=4, column=1900, columnspan=4, padx=0, pady=0)
        



#****************************************************************************************
#****************************************************************************************
#**************************************History*******************************************
#****************************************************************************************

def History():
    frame3.destroy()
    global frame10
    frame10 = customtkinter.CTkFrame(master=root)
    frame10.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame10, text="History", font=("Roboto", 36), text_color="#329983")
    label.pack(pady=50, padx=20)

    Reports = []        #"Report 1", "Report 2"
    if not Reports:
        label.configure(text="No Reports Found")
        label.pack(pady=150, padx=20)
    else:
        radio_value = tkinter.StringVar()  # variable to store the selected IP address

        for ip in Reports:
            radio = customtkinter.CTkRadioButton(frame10, text=ip, variable=radio_value, value=ip)
            radio.pack(pady=(6, 3), padx=50, anchor="w")

        button = customtkinter.CTkButton(master=frame10, text="Select Drone", command=test_1())
        button.pack(pady=(0, 18), padx=(0, 40), anchor="se", expand=True)

    button1 = customtkinter.CTkButton(master=frame10, text="Back", command=lambda: [des10(), Homepage()])
    button1.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)

Login()
root.mainloop()
print("Final selected drone IP:", drone_ip)
print(selected_interface)

'''
TODO:   
    - [ ] Port Hacking 22,21
    - [ ] Arp Spoofing - 
    - [ ] History -
'''