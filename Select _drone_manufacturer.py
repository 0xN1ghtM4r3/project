import customtkinter  # Import customTkinter library

def choose_manufacturer():
  """Gets the selected manufacturer from the combobox and saves it in `selected_manufacturer`."""
  global selected_manufacturer  # Declare variable as global to access outside the function
  selected_manufacturer = combobox.get()
  print("You selected:", selected_manufacturer)

# Create the main window
window = customtkinter.CTk()
window.geometry("300x100")  # Set window size (optional)
window.title("Manufacturer Selection")

# Create the label
label = customtkinter.CTkLabel(window, text="Select a manufacturer:")
label.pack(padx=10, pady=10)

# Create the combobox widget
manufacturers = ["DJI", "Parrot", "Yuneec"]
combobox = customtkinter.CTkComboBox(window, values=manufacturers)
combobox.pack(padx=10, pady=10)

# Create the button
button = customtkinter.CTkButton(window, text="Choose", command=choose_manufacturer)
button.pack(padx=10, pady=10)

# Declare `selected_manufacturer` globally (optional, but recommended for clarity)
selected_manufacturer = None  # Initially set to None

# Run the main event loop
window.mainloop()
