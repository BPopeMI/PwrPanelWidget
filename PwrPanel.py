# 0.2a Ver
# BPopeMI @ Github
import tkinter as tk
from tkinter import ttk
import subprocess
import setproctitle  # Process title
import os # Import os module to work with file paths
from PIL import Image, ImageTk

class PowerPanelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Power Panel GUI")

        # Set window size and position
        self.root.geometry("600x400+100+100")

        # Create a notebook widget to hold multiple tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create UPS status tab
        self.create_status_tab()

        # Start updating status in real-time
        self.update_status()

    def create_status_tab(self):
        status_tab = ttk.Frame(self.notebook)
        self.notebook.add(status_tab, text='Status')

        # Create a frame for the text area
        text_frame = tk.Frame(status_tab)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrollable text area to display the UPS status
        self.text_area = tk.Text(text_frame, bg='black', fg='white', font=('Arial', 12))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def get_status(self):
        try:
            result = subprocess.run(['sudo', 'pwrstat', '-status'], capture_output=True, text=True, check=True)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, result.stdout)
        except subprocess.CalledProcessError as e:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"An error occurred: {e}")

    def update_status(self):
        # Update the status and schedule the next update
        self.get_status()
        self.root.after(5000, self.update_status)  # Update every 5 seconds

if __name__ == "__main__":
    # Custom process title
    setproctitle.setproctitle("Power Panel GUI")

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the icon file
    icon_path = os.path.join(script_dir, "Pwr.ico")

    # Create the main window
    root = tk.Tk()

    # Open the icon file using PIL
    icon_image = Image.open(icon_path)

    # Convert the image to Tkinter format
    icon_photo = ImageTk.PhotoImage(icon_image)

    # Set the window icon
    root.tk.call('wm', 'iconphoto', root._w, icon_photo)

    # Create an instance of the PowerPanelGUI class
    app = PowerPanelGUI(root)

    # Run the main loop to keep the window open
    root.mainloop()
