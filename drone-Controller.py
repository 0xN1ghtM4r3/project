import customtkinter as ct

class DroneControllerApp(ct.CTk):
    def __init__(self):
        super().__init__()

        self.title("Drone Controller")
        self.geometry("400x300")

        self.bind("<KeyPress>", self.handle_key_press)
        self.create_widgets()

    def create_widgets(self):
        # Labels
        self.label = ct.CTkLabel(master=self, text="Drone Controller", font=("Arial", 16))
        self.label.pack(pady=10)

        # Up Button (Top Center)
        self.up_btn = ct.CTkButton(master=self, text="Up (↑)", command=self.move_up)
        self.up_btn.pack(pady=20, padx=self.winfo_width() // 2 - self.up_btn.winfo_width() // 2)

        # Left Button (Left Center)
        self.left_btn = ct.CTkButton(master=self, text="Left (←)", command=self.move_left)
        self.left_btn.pack(pady=20, padx=self.winfo_width() // 4 - self.left_btn.winfo_width() // 2)

        # Right Button (Right Center)
        self.right_btn = ct.CTkButton(master=self, text="Right (→)", command=self.move_right)
        self.right_btn.pack(pady=20, padx=self.winfo_width() * 3 // 4 - self.right_btn.winfo_width() // 2)

        # Down Button (Bottom Center)
        self.down_btn = ct.CTkButton(master=self, text="Down (↓)", command=self.move_down)
        self.down_btn.pack(pady=20, padx=self.winfo_width() // 2 - self.down_btn.winfo_width() // 2)

        # Takeoff and Land Buttons (Optional, you can place them elsewhere)
        self.takeoff_btn = ct.CTkButton(master=self, text="Takeoff", command=self.takeoff)
        self.takeoff_btn.pack()

        self.land_btn = ct.CTkButton(master=self, text="Land", command=self.land)
        self.land_btn.pack()

    def handle_key_press(self, event):
        key = event.keysym.lower()

        if key == "up":
            self.move_up()
        elif key == "down":
            self.move_down()
        elif key == "left":
            self.move_left()
        elif key == "right":
            self.move_right()

    def move_up(self):
        # Add your logic to move the drone up
        print("Moving drone up")

    def move_down(self):
        # Add your logic to move the drone down
        print("Moving drone down")

    def move_left(self):
        # Add your logic to move the drone left
        print("Moving drone left")

    def move_right(self):
        # Add your logic to move the drone right
        print("Moving drone right")

    def takeoff(self):
        # Add your logic to initiate drone takeoff
        print("Drone takeoff")

    def land(self):
        # Add your logic to land the drone
        print("Drone landing")

if __name__ == "__main__":
    app = DroneControllerApp()
    app.mainloop()
