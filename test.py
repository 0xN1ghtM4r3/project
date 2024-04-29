import socket
import time

# Define the IP address and port to send the payloads to
ip_address = "192.168.1.3"  # Replace "your_ip_address" with the actual IP address
port = 5556  # Adjust the port number according to your setup

# Function to send payload to the given IP address
def send_payload(command, seq_num):
    try:
        # Define the payloads for the specified command with a placeholder for sequence number
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
        else:
            print("Invalid command. Please enter 'up', 'down', 'right', 'left', 'takeoff', or 'land'.")
            return
        
        # Format the payload with the sequence number
        formatted_payload = payload.format(seq_num)
        
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Send the formatted payload
        sock.sendto(formatted_payload.encode(), (ip_address, port))
        
        # Close the socket
        sock.close()
        
        print("Payload sent successfully:", formatted_payload)
        
    except Exception as e:
        print("Error:", e)

# Main function to send payloads
def main():
    while True:
        # Prompt the user to input the command name
        command = input("Enter command name (up/down/right/left/takeoff/land): ").lower()
        
        # Check if the command is valid
        if command in ["up", "down", "right", "left", "takeoff", "land"]:
            seq_num = 0
            packet_count = 0  # Counter for sent packets
            while packet_count < 5:
                send_payload(command, seq_num)
                time.sleep(1)  # Wait for 1 second before sending the next payload
                seq_num += 1
                packet_count += 1
            
            # Reset packet count
            packet_count = 0
        else:
            print("Invalid command. Please enter 'up', 'down', 'right', 'left', 'takeoff', or 'land'.")

if __name__ == "__main__":
    main()