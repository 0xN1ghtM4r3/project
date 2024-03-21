import subprocess

def connect_to_wifi(wifi_name, password):
    command = f'nmcli device wifi connect "{wifi_name}" password "{password}"'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Connected to {wifi_name} successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to connect to {wifi_name}.")

# Example usage:
wifi_name = input("Enter WiFi name: ")
password = input("Enter password: ")
connect_to_wifi(wifi_name, password)