import customtkinter
import socket
import time
import subprocess
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class DroneController:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Controller")
        
        self.ip_address = "192.168.1.3"  # Replace "your_ip_address" with the actual IP address
        self.port = 5556  # Adjust the port number according to your setup
        
        self.seq_num = 0
        self.packet_count = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create buttons for each command
        self.button_up = customtkinter.CTkButton(self.root, text="Up", command=lambda: self.send_command("up"))
        self.button_up.grid(row=1, column=250, padx=5, pady=5)
        
        self.button_down = customtkinter.CTkButton(self.root, text="Down", command=lambda: self.send_command("down"))
        self.button_down.grid(row=2, column=250, padx=5, pady=5)
        
        self.button_right = customtkinter.CTkButton(self.root, text="Right", command=lambda: self.send_command("right"))
        self.button_right.grid(row=2, column=270, padx=5, pady=5)
        
        self.button_left = customtkinter.CTkButton(self.root, text="Left", command=lambda: self.send_command("left"))
        self.button_left.grid(row=2, column=230, padx=5, pady=5)
        
        self.button_takeoff = customtkinter.CTkButton(self.root, text="Takeoff", command=lambda: self.send_command("takeoff"))
        self.button_takeoff.grid(row=3, column=230, padx=5, pady=5)
        
        self.button_land = customtkinter.CTkButton(self.root, text="Land", command=lambda: self.send_command("land"))
        self.button_land.grid(row=3, column=270, padx=5, pady=5)
        
        self.button_camera = customtkinter.CTkButton(self.root, text="Turn On Camera", command=lambda: self.send_command("turnoncamera"))
        self.button_camera.grid(row=3, column=250, padx=5, pady=5)
        
        #Log text area
        self.log_text = customtkinter.CTkTextbox(self.root, height=200, width=400)
        self.log_text.grid(row=4, column=1900, columnspan=4, padx=0, pady=0)
        
    def send_payload(self, command, seq_num):
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
                self.log("Invalid command. Please enter 'up', 'down', 'right', 'left', 'takeoff', 'land', or 'turnOnCamera'.")
                return
            
            formatted_payload = payload.format(seq_num)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(formatted_payload.encode(), (self.ip_address, self.port))
            sock.close()
            self.log("Payload sent successfully: " + formatted_payload)
        
        except Exception as e:
            self.log("Error: " + str(e))
        
    def send_command(self, command):
        if command in ["up", "down", "right", "left", "takeoff", "land"]:
            while self.packet_count < 5:
                self.send_payload(command, self.seq_num)
                time.sleep(1)
                self.seq_num += 1
                self.packet_count += 1
            self.packet_count = 0
        elif command == "turnoncamera":
            self.send_payload(command, 0)
            subprocess.Popen('pkill nc; pkill vlc', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) 
            time.sleep(1)
            subprocess.Popen('nc -nvlp 1111 -u | vlc -', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)  
            time.sleep(1)
        else:
            self.log("Invalid command. Please enter 'up', 'down', 'right', 'left', 'takeoff', 'land', or 'turnOnCamera'.")
        
    def log(self, message):
        self.log_text.insert(customtkinter.END, message + "\n")
        self.log_text.see(customtkinter.END)

if __name__ == "__main__":
    root = customtkinter.CTk()
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")
    root.geometry("850x500")
    app = DroneController(root)
    root.mainloop()
