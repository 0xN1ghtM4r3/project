import customtkinter
from CTkMessagebox import CTkMessagebox
from ftplib import FTP

def connect_and_list_files():
    ip_address = ip_entry.get()
    try:
        global ftp
        ftp = FTP(ip_address)
        ftp.login()  # Try null session login
        files = ftp.nlst()
        ftp.quit()

        # Clear existing entries (assuming previous entries were labels)
        for widget in file_list_frame.winfo_children():
            widget.destroy()

        for file in files:
            # Create a CTkLabel for each file in the frame
            file_label = customtkinter.CTkLabel(master=file_list_frame, text=file)
            file_label.pack()
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Failed to connect or list files: {e}")

def download_all_files():
    if not len(file_list_frame.winfo_children()):
        CTkMessagebox(title="Error", message="No files listed")
        return
    
    save_directory = customtkinter.filedialog.askdirectory()
    if not save_directory:
        return
    
    try:
        ftp = FTP(ip_entry.get())
        ftp.login()
        
        for child in file_list_frame.winfo_children():
            filename = child.cget("text")  # Get filename from label text
            with open(f"{save_directory}/{filename}", "wb") as file:
                ftp.retrbinary(f"RETR {filename}", file.write)
        
        ftp.quit()
        CTkMessagebox(title="Success", message="All files downloaded successfully")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Failed to download files: {e}")

# Create the main window
app = customtkinter.CTk()
app.geometry("400x400")
app.title("FTP Null Session File List")

# IP Address Entry
ip_label = customtkinter.CTkLabel(master=app, text="Enter FTP Server IP:")
ip_label.pack(pady=12)
ip_entry = customtkinter.CTkEntry(master=app, width=200)
ip_entry.pack()

# Connect Button
connect_button = customtkinter.CTkButton(master=app, text="Connect and List Files", command=connect_and_list_files)
connect_button.pack(pady=12)

# File List (CTkFrame)
file_list_frame = customtkinter.CTkFrame(master=app)
file_list_frame.pack(pady=12)

# Download All Files Button
download_all_button = customtkinter.CTkButton(master=app, text="Download All Files", command=download_all_files)
download_all_button.pack(pady=12)

app.mainloop()
