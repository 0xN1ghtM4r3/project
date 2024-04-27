import socket
from concurrent.futures import ThreadPoolExecutor
import customtkinter
from CTkMessagebox import CTkMessagebox
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")



def scan_ports(target_host):
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
    target_host = host_entry.get()
    if not target_host:
        customtkinter.showwarning("Warning", "Please enter a target host.")
        return
    scan_ports(target_host)

root = customtkinter.CTk()
root.title("Port Scanner")
root.geometry("850x500")


host_label = customtkinter.CTkLabel(root, text="Target Host:")
host_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

host_entry = customtkinter.CTkEntry(root, width=100)
host_entry.grid(row=0, column=1, padx=5, pady=5)

scan_button = customtkinter.CTkButton(root, text="Scan Ports", command=scan_button_clicked)
scan_button.grid(row=0, column=2, padx=5, pady=5)

result_text = customtkinter.CTkTextbox(root, width=200, height=200)
result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
