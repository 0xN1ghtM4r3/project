import customtkinter
from CTkMessagebox import CTkMessagebox
import tkinter
import psutil
import hashlib
import json
from scapy.all import *
from tkinter import ttk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("850x500")

global frame
global frame1
def test_1():
    print("testing")

def test_2():
    print("checkpoint")

def des1():
    frame1.destroy()

def des2():
    frame2.destroy()

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

#--------------------------------------------------------------------------
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
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
def Login():
    global frame
    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True )
    def user_login():
        users = load_users()
        username = username_entry.get()
        password = password_entry.get()
        hashed_password = hash_password(password)
        if username in users and users[username]["password"] == hashed_password:
            print("Login successful!")
            Homepage()
            return True
        else:
             CTkMessagebox(title="Error", message="Username or Password Invalid", icon="cancel")
    label = customtkinter.CTkLabel(master=frame, text="Login", font=("Roboto", 24))
    label.pack(pady=(40,10), padx=10)

    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username", width=250)
    username_entry.pack(pady=(10,10), padx=10)

    password_entry = customtkinter.CTkEntry(master=frame,show="*", placeholder_text="Password", width=250)
    password_entry.pack(pady=(10,10), padx=10)

    login_button = customtkinter.CTkButton(master=frame, text="Login", command=user_login)
    login_button.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame, text="Sign up",  command=Sign_up)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame, text="Forget Password !",  command=Reset, fg_color="transparent")
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
        password = create_user_entry.get()
        hashed_password = hash_password(password)
        users[username] = {"password": hashed_password}
        save_users(users)
        print("User created successfully.")

    label = customtkinter.CTkLabel(master=frame1, text="Sign up", font=("Roboto", 24))
    label.pack(pady=(10,10), padx=10)

    create_user_entry = customtkinter.CTkEntry(master=frame1, placeholder_text="Username", width=250)
    create_user_entry.pack(pady=(10,10), padx=10)

    create_password_entry = customtkinter.CTkEntry(master=frame1,show="*", placeholder_text="Password", width=250)
    create_password_entry.pack(pady=(10, 10), padx=10)


    check_var = customtkinter.StringVar(value="off")
    checkbox = customtkinter.CTkCheckBox(frame1, text=" I Have Read and Agree to Terms and Conditions", variable=check_var, onvalue="on", offvalue="off")
    checkbox.pack(pady=5, padx=10)

    button1 = customtkinter.CTkButton(master=frame1, text="Create Account", command=create_user)
    button1.pack(pady=5, padx=10)


    button3 = customtkinter.CTkButton(master=frame1, text="Already Have an Account !", command=lambda:[des1(), Login()], fg_color="transparent")
    button3.pack(pady=2, padx=10)

def Reset():
    frame.destroy()
    global frame2
    frame2 = customtkinter.CTkFrame(master=root)
    frame2.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame2, text="Password Reset", font=("Roboto", 24))
    label.pack(pady=(40,10), padx=10)

    entry = customtkinter.CTkEntry(master=frame2, placeholder_text="Username", width=250)
    entry.pack(pady=(10,10), padx=10)

    entry2 = customtkinter.CTkEntry(master=frame2, placeholder_text="Email", width=250)
    entry2.pack(pady=(10,10), padx=10)

    entry2 = customtkinter.CTkEntry(master=frame2, placeholder_text="Confirmation Code (OTP)", width=250)
    entry2.pack(pady=(10,10), padx=10)

    button1 = customtkinter.CTkButton(master=frame2, text="Reset", command=test_1)
    button1.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame2, text="Back", command=lambda: [des2(), Login()], fg_color="transparent")
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

    button2 = customtkinter.CTkButton(master=frame3, text="History", command=test_1)
    button2.pack(pady=12, padx=10)
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
    selected_interface = None
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
    root.title("Select Network Interface")

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
            Scan_Page()

    scan_button = customtkinter.CTkButton(master=frame5, text="Scan", command=networks_list)
    scan_button.pack(pady=10)
    network_combobox = customtkinter.CTkComboBox(master=frame5,values=networks_list(), state="readonly")
    network_combobox.pack(pady=5)
    password_label = customtkinter.CTkLabel(master=frame5, text="Password:")
    password_label.pack(pady=5)
    password_entry = customtkinter.CTkEntry(master=frame5, show="*")
    password_entry.pack(pady=5)
    connect_button = customtkinter.CTkButton(master=frame5, text="Connect", command=connect)
    connect_button.pack(pady=5)


    button4 = customtkinter.CTkButton(master=frame5, text="Back", command=lambda: [des5(), interface_page()])
    button4.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)

def Scan_Page():
    frame5.destroy()
    global frame6
    frame6 = customtkinter.CTkFrame(master=root)
    frame6.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame6, text="Choose Scan method...", font=("Roboto", 36))
    label.pack(pady=(60, 35), padx=10)

    button1 = customtkinter.CTkButton(master=frame6, text="Full Scan", command=FullScan)
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame6, text="Custom Scan", command=test_1)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame6, text="Back", command=lambda: [des5(), WifiScan()], fg_color="transparent")
    button3.pack(pady=12, padx=10)

def FullScan():
    frame6.destroy()
    global frame7
    frame7 = customtkinter.CTkFrame(master=root)
    frame7.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame7, text="Scanning...", font=("Roboto", 36), text_color="#329983")
    label.pack(pady=20, padx=20)

    radio = customtkinter.CTkRadioButton(frame7, text="Drone ... 141.68.44.205")
    radio.pack(pady=(6, 3), padx=50, anchor="w")
    radio2 = customtkinter.CTkRadioButton(frame7, text="Drone ... 141.68.44.205")
    radio2.pack(pady=(6, 3), padx=50, anchor="w")
    radio3 = customtkinter.CTkRadioButton(frame7, text="Drone ... 141.68.44.205")
    radio3.pack(pady=(6, 3), padx=50, anchor="w")
    radio4 = customtkinter.CTkRadioButton(frame7, text="Drone ... 141.68.44.205")
    radio4.pack(pady=(6, 3), padx=50, anchor="w")


    button3 = customtkinter.CTkButton(master=frame7, text="Select Drone", command=Test)
    button3.pack(pady=(0, 18), padx=(0, 40), anchor="se", expand=True)

    button4 = customtkinter.CTkButton(master=frame7, text="Back", command=lambda: [des7(), Scan_Page()])
    button4.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)

def Test():
    frame7.destroy()
    global frame8
    frame8 = customtkinter.CTkFrame(master=root)
    frame8.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame8, text="Choose Test method...", font=("Roboto", 36))
    label.pack(pady=(60, 35), padx=10)

    button1 = customtkinter.CTkButton(master=frame8, text="Full Test", command=test_1)
    button1.pack(pady=12, padx=10)

    button2 = customtkinter.CTkButton(master=frame8, text="Custom Test", command=CustomTest)
    button2.pack(pady=12, padx=10)

    button3 = customtkinter.CTkButton(master=frame8, text="Back", command=lambda: [des7(), FullScan()],fg_color="transparent")
    button3.pack(pady=12, padx=10)

def CustomTest():
    frame8.destroy()
    global frame9
    frame9 = customtkinter.CTkFrame(master=root)
    frame9.pack(pady=20, padx=60, fill="both", expand=True)

    label = customtkinter.CTkLabel(master=frame9, text="Choose Test Method", font=("Roboto", 36), text_color="#329983")
    label.pack(pady=20, padx=20)

    radio = customtkinter.CTkRadioButton(frame9, text="Test 1")
    radio.pack(pady=(6, 3), padx=50, anchor="w")
    radio2 = customtkinter.CTkRadioButton(frame9, text="Test 2")
    radio2.pack(pady=(6, 3), padx=50, anchor="w")
    radio3 = customtkinter.CTkRadioButton(frame9, text="Test 3")
    radio3.pack(pady=(6, 3), padx=50, anchor="w")
    radio4 = customtkinter.CTkRadioButton(frame9, text="Test 4")
    radio4.pack(pady=(6, 3), padx=50, anchor="w")

    button3 = customtkinter.CTkButton(master=frame9, text="Select Drone", command=test_1)
    button3.pack(pady=(0, 18), padx=(0, 40), anchor="se", expand=True)

    button4 = customtkinter.CTkButton(master=frame9, text="Back", command=lambda: [des8(), Test()])
    button4.place(relx=0.15, rely=0.93, anchor=tkinter.CENTER)

Login()
root.mainloop()