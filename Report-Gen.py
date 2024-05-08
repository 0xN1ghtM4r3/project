import customtkinter
from tkinter import messagebox
from fpdf import FPDF
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
class ReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Security Check Report Generator")

        # Center the window
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        # Generate Report Button
        generate_button = customtkinter.CTkButton(root, text="Generate Report", command=self.generate_report)
        generate_button.place(relx=0.5, rely=0.5, anchor="center")

    def generate_report(self):
        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", style='B', size=20)
        pdf.cell(200, 10, txt="Security Check Report", ln=True, align="C")
        pdf.ln(15)

        # System Information
        system_info = {
            "Username": "n1ght",
            "Drone Manufacture": "DJI",
            "Drone IP": "192.168.1.6",
            "Network Interface": "wlan0",
            "Open Ports": "SSH (22), FTP (21), AAFTP (3000)",
            "Kernel Version": "6.8.9-arch1-1 #1 SMP PREEMPT_DYNAMIC Thu, 02 May 2024 17:49:46 +0000 x86_64 GNU/Linux"
        }

        # Subtitle for System Information
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, txt="System Information", ln=True)
        pdf.ln(10)

        # Add system information to PDF
        for param, value in system_info.items():
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt=f"{param}: {value}", ln=True)

        # Security Issues
        security_issues = {
            "SSH Brute Force": "SSH brute force is a method of attempting to gain unauthorized access to a system by trying many passwords until the correct one is found.\nMitigation: Use strong, unique passwords, implement SSH key-based authentication, and use tools like fail2ban to block repeated failed login attempts.",
            "FTP NullSession": "FTP null session is a type of security vulnerability where an attacker can access an FTP server without authentication.\nMitigation: Disable anonymous FTP access, restrict access to authorized users only, and use secure FTP protocols such as SFTP or FTPS.",
            "Command Injection": "Command injection is an attack in which the goal is execution of arbitrary commands on the host operating system via a vulnerable application.\nMitigation: Validate and sanitize user input, use parameterized queries in databases, and employ web application firewalls (WAFs) to detect and block command injection attacks.",
            "Drone Instruction Injection": "Drone instruction injection is a type of attack where an attacker injects malicious instructions into the commands sent to a drone, potentially gaining unauthorized control.\nMitigation: Encrypt communications between the controller and the drone, implement secure authentication mechanisms, and regularly update drone firmware to patch known vulnerabilities.",
            "ARP Spoof": "ARP spoofing is a technique whereby an attacker sends fake Address Resolution Protocol (ARP) messages onto a local area network in order to link the attacker’s MAC address with the IP address of a legitimate member of the network.\nMitigation: Use ARP spoofing detection tools, implement static ARP entries, and use secure protocols like ARPSEC to prevent ARP spoofing attacks.",
            "DoS on Drone Operator": "Denial-of-Service (DoS) attacks on drone operators involve flooding the operator's communication channels with traffic, rendering them unable to control the drone effectively.\nMitigation: Use encrypted communication channels, implement DoS protection mechanisms such as rate limiting and traffic filtering, and employ intrusion detection systems to detect and respond to DoS attacks."
        }

        # Header for Security Issues
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, txt="Security Issues", ln=True)
        pdf.ln(10)

        # Add security issues to PDF
        for param, value in security_issues.items():
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, txt=f"{param}:", ln=True)
            pdf.set_text_color(255, 0, 0)  # Red color for security issues
            pdf.multi_cell(0, 10, txt=value.encode('latin-1', 'replace').decode('latin-1'), align='L')
            pdf.set_text_color(0, 0, 0)  # Reset text color
            pdf.ln(10)

        # Save PDF
        pdf_filename = "security_check_report.pdf"
        pdf.output(pdf_filename)

        # Show success message
        CTkMessagebox(title="Success", message=f"PDF report generated successfully: {pdf_filename}",
                  icon="check")

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = ReportGenerator(root)
    root.mainloop()
