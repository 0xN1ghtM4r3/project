import tkinter as tk
from tkinter import ttk
import psutil

def get_network_interfaces():
    # Get a list of network interfaces
    interfaces = psutil.net_if_addrs()
    return list(interfaces.keys())

def on_select(event):
    selected_idx = interface_combobox.current()
    selected_interface = interfaces[selected_idx]
    print("Selected Interface:", selected_interface)

# Create the main application window
root = tk.Tk()
root.title("Select Network Interface")

# Get available network interfaces
interfaces = get_network_interfaces()

# Create a label
label = tk.Label(root, text="Select Network Interface:")
label.pack(pady=10)

# Create a combobox to select the network interface
interface_combobox = ttk.Combobox(root, values=interfaces, state="readonly")
interface_combobox.pack()

# Bind the selection event
interface_combobox.bind("<<ComboboxSelected>>", on_select)

# Run the application
root.mainloop()
