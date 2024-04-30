import socket
import subprocess
import turtle
# Define the IP address and port to listen on
ip_address = "0.0.0.0"  # Listen on all available network interfaces
port = 5556  # Port to listen on

# ASCII art for a drone
drone_art = """
⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀
⠀⢀⣀⣀⣀⣈⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣁⣀⣀⣀⡀⠀
⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀
⠀⠀⠀⣾⣿⣿⣿⣿⠀⠀⠀⠀⠀⠞⠛⠛⠳⠀⠀⠀⠀⠀⣿⣿⣿⣿⣷⠀⠀⠀
⠀⠀⠀⠛⠛⠻⠿⠿⣿⣿⣿⡟⢁⡴⠛⠛⢦⡈⢻⣿⣿⣿⠿⠿⠟⠛⠛⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡈⠁⠘⢧⣀⣀⡼⠃⠈⢁⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠋⠀⢶⣄⣉⣉⣠⡶⠀⠙⢿⣷⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣠⣾⠟⠋⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠙⠻⣷⣄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠛⢁⣀⡀⠀⠀⠀⠀⠀⠀⢀⣀⡈⠛⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# Payload-message mapping
payload_messages = {
    "290717696": "Drone goes up",
    "290711696": "Drone goes down",
    "290721696": "Drone moves right",
    "290731696": "Drone moves left",
    "290741696": "Drone takes off",
    "290751696": "Drone lands"
}

# Function to start FTP and SSH services
def start_services():
    try:
        # Start FTP service
        subprocess.run(['sudo', 'service', 'vsftpd', 'start'], check=True)
        print("FTP service started successfully.")
        
        # Start SSH service
        subprocess.run(['sudo', 'service', 'ssh', 'start'], check=True)
        print("SSH service started successfully.")
       
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

camera_started = False
def turn_camera_on(op_ip):
    global camera_started
    if camera_started:
        print("Camera is already started")
        return
    try:
        if camera_started == False:
            # Start Streaming
            ffmpeg_command = [
                "ffmpeg",
                "-re",
                "-i",
                "./Camera.mp4",
                "-c:v",
                "copy",
                "-f",
                "mpegts",
                f"udp://{op_ip}:1111"
            ]

            # Execute the command
            subprocess.Popen(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
            print("Camera is started successfully")
            camera_started = True
        else:
            print("Camera is already started")
    except Exception as e:
        print(f"Error occurred while starting the camera: {e}")
# Start FTP and SSH services
start_services()

# Print ASCII art for drone
print(drone_art)

# Print SSH and FTP are ready
print("SSH is ready")
print("FTP is ready")
print("Camera is ready")
print("Ready For Receiving Instructions  on {}:{}".format(ip_address, port))

# Create a turtle screen
screen = turtle.Screen()
screen.setup(1200,700)
# Create a turtle object
arrow = turtle.Turtle()
turtle.register_shape('drone.gif')
screen.bgpic('map.gif')
turtle.bgcolor("black")
turtle.pencolor("red")
arrow.shape('drone.gif')
arrow.shapesize(stretch_wid=2, stretch_len=2, outline=8)  
# Define the function to move the arrow
def move_drone(command):
    if command == "up":
        arrow.setheading(90)  # Set the arrow's heading to up (north)
        arrow.forward(10)  # Move the arrow forward
    elif command == "down":
        arrow.setheading(270)  # Set the arrow's heading to down (south)
        arrow.forward(10)  # Move the arrow forward
    elif command == "right":
        arrow.setheading(0)  # Set the arrow's heading to right (east)
        arrow.forward(10)  # Move the arrow forward
    elif command == "left":
        arrow.setheading(180)  # Set the arrow's heading to left (west)
        arrow.forward(10)  # Move the arrow forward
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the IP address and port
sock.bind((ip_address, port))

# Continuously receive and print payloads
while True:
    # Receive data from the socket
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    operator_ip = addr[0]
    # Decode the received data and strip any leading/trailing whitespace
    payload = data.decode().strip()
    if "290717696" in payload:
        print(f"Received payload [{payload}]: Drone goes up")
        move_drone("up")
    elif "290711696" in payload:
        print(f"Received payload [{payload}]: Drone goes down")
        move_drone("down")
    elif "290721696" in payload:
        print(f"Received payload [{payload}]: Drone goes right")
        move_drone("right")
    elif "290731696" in payload:
        print(f"Received payload [{payload}]: Drone goes left")
        move_drone("left")
    elif "290741696" in payload:
        print(f"Received payload [{payload}]: Drone is taking off")
    elif "290751696" in payload:
        print(f"Received payload [{payload}]: Drone lands")
    elif "2907510942" in payload:
        turn_camera_on(operator_ip)
    else:
        print("Received unknown payload:", payload)
