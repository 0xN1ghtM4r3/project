import os
import webbrowser
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog

class PDFViewerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("PDF Viewer")
        self.geometry("800x600")

        self.label = ctk.CTkLabel(self, text="Select a directory to view PDFs")
        self.label.pack(pady=10)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=10)

        self.pdf_frame = ctk.CTkFrame(self)
        self.pdf_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.pdf_directory = ""

    def browse_directory(self):
        self.pdf_directory = filedialog.askdirectory()
        if not self.pdf_directory:
            return

        self.update_pdf_grid()

    def update_pdf_grid(self):
        for widget in self.pdf_frame.winfo_children():
            widget.destroy()

        row = 0
        col = 0
        for filename in os.listdir(self.pdf_directory):
            if filename.lower().endswith(".pdf"):
                pdf_button = ctk.CTkButton(self.pdf_frame, text=filename, command=lambda f=filename: self.view_pdf(f))
                pdf_button.grid(row=row, column=col, padx=10, pady=10)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

    def view_pdf(self, pdf_filename):
        pdf_path = os.path.join(self.pdf_directory, pdf_filename)
        webbrowser.open_new(pdf_path)


if __name__ == "__main__":
    app = PDFViewerApp()
    app.mainloop()

