from ftplib import FTP
import socket
import paramiko
import telnetlib

from concurrent.futures import ThreadPoolExecutor

class TelnetConnector:
    def __init__(self, drone_ip, open_ports):
        self.drone_ip = drone_ip
        self.open_ports = open_ports
        self.telnet = telnetlib.Telnet()

    def check_telnet_port(self):
        return any(port == 23 for port, _ in self.open_ports)

    def connect(self):
        if not self.check_telnet_port():
            print("[-] Telnet port (23) is closed.")
            return
        try:
            self.telnet.open(self.host, self.port)
            print("Connected to Telnet server successfully.")
        except Exception as e:
            print(f"Failed to connect to Telnet server: {e}")

    def get_kernel_version(self):
        try:
            # Send command to get kernel version
            self.telnet.write(b'uname -r\n')
            
            # Read response
            kernel_version = self.telnet.read_until(b'\n').decode().strip()
            
            print("Kernel version:", kernel_version)
        except Exception as e:
            print(f"Failed to get kernel version: {e}")

    def disconnect(self):
        try:
            self.telnet.close()
            print("Disconnected from Telnet server.")
        except Exception as e:
            print(f"Error while disconnecting: {e}")


class PortScanner:
    def __init__(self, target_host):
        self.target_host = target_host
        self.open_ports = []

    def scan_ports(self):
        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Adjust timeout as needed
                    result = s.connect_ex((self.target_host, port))
                    if result == 0:
                        service = socket.getservbyport(port)
                        self.open_ports.append((port, service))
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_version:
                                s_version.settimeout(1)  # Adjust timeout as needed
                                s_version.connect((self.target_host, port))
                                s_version.sendall(b"GET / HTTP/1.0\r\n\r\n")
                                banner = s_version.recv(1024).decode("utf-8")
                                print(f"Version: {banner.strip()}")
                        except socket.error:
                            pass
            except socket.error:
                pass

        print(f"Scanning host: {self.target_host}")
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_port, port) for port in range(1, 1001)]  # Scan common ports
            for future in futures:
                future.result()  # Wait for all tasks to complete
        return self.open_ports

# Example usage:

scanner = PortScanner("127.0.0.1")
open_ports = scanner.scan_ports()
print("Open ports:", open_ports)
    
TelnetConnector("127.0.0.1", open_ports).connect()