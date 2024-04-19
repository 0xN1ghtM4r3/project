import customtkinter  # Import customTkinter library


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("850x500")

def manufacturer_page():
  def choose_manufacturer():
    """Gets the selected manufacturer from the combobox and saves it in `selected_manufacturer`."""
    global selected_manufacturer  # Declare variable as global to access outside the function
    selected_manufacturer = combobox.get()
    print("You selected:", selected_manufacturer)


  # Create the label
  label = customtkinter.CTkLabel(master=root, text="Select a manufacturer:")
  label.pack(padx=10, pady=10)

  # Create the combobox widget
  manufacturers = ["DJI", "Parrot", "Yuneec"]
  combobox = customtkinter.CTkComboBox(master=root, values=manufacturers)
  combobox.pack(padx=10, pady=10)

  # Create the button
  button = customtkinter.CTkButton(master=root, text="Choose", command=choose_manufacturer)
  button.pack(padx=10, pady=10)

  # Declare `selected_manufacturer` globally (optional, but recommended for clarity)
  selected_manufacturer = None  # Initially set to None

# Run the main event loop
root.mainloop()
