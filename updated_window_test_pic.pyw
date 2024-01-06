import os
import sys
import logging
from PIL import Image, ImageTk
import tkinter as tk
import portalocker
from filelock import Timeout, FileLock
import tempfile

# Configure logging
logging.basicConfig(filename='application.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.debug("Starting the application.")

temp_dir = tempfile.gettempdir()  # Returns a directory like 'C:/Users/{Username}/AppData/Local/Temp'
lock_file_path = os.path.join(temp_dir, 'window_test_pic.lock')

# Check if the lock file exists
if os.path.exists(lock_file_path):
    logging.info("Application is already running.")
    print("Application is already running.")
    sys.exit(0)

# Create the lock file
try:
    # Use 'x' mode to create the file, failing if it already exists
    with open(lock_file_path, 'x') as lock_file:
        lock_file.write('Lock')
    logging.debug("Lock file created, continuing execution.")
except FileExistsError:
    logging.info("Application is already running.")
    print("Application is already running.")
    sys.exit(0)
finally:
    # The lock will be released when the 'with' block is exited, either normally or through an exception.
    logging.debug("Application is closing.")

def on_yes_click():
    for widget in window.winfo_children():
        widget.destroy()
    tk.Label(window, text="Yes").pack()

def on_no_click():
    # Delete the lock file and close the window
    logging.debug("on_no_click called.")
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
    window.destroy()

def clean_up():
    # Safeguard the clean-up code
    if window.winfo_exists():  # Checks if the window still exists
        window.destroy()
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
        logging.debug("Lock file deleted.")

# Create the main window
window = tk.Tk()

# Bind the clean_up function to the window close event
window.protocol("WM_DELETE_WINDOW", clean_up)
window.title("Yes or No")

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to a fraction of the screen size
# For example, half of the screen size
window_width = int(screen_width / 3)
window_height = int(screen_height / 2)

# Set the initial size of the window
window.geometry(f'{window_width}x{window_height}')

# Load the image
try:
    image_path = 'C:\\Users\\dylan\\Downloads\\Palk.png'
    original_image = Image.open(image_path)

    # Calculate the scaling factor to fit the image within a portion of the screen width, preserving aspect ratio
    max_image_width = screen_width / 4  # For example, half the screen width
    original_width, original_height = original_image.size
    scaling_factor = min(max_image_width / original_width, 1)  # Ensure the image doesn't scale up if smaller than max size

    # Calculate new size while maintaining aspect ratio
    new_size = (int(original_width * scaling_factor), int(original_height * scaling_factor))

    # Resize the image
    resized_image = original_image.resize(new_size, Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)

    image_label = tk.Label(window, image=image)
    image_label.image = image  # Keep a reference to avoid garbage collection
    image_label.pack()
except Exception as e:
    print(f"Error loading or resizing image: {e}")
    # Optionally, continue with the rest of the GUI if image fails to load
    # exit()

# Create the buttons
button_yes = tk.Button(window, text="Yes?", command=on_yes_click)
button_no = tk.Button(window, text="No?", command=on_no_click)

# Place the buttons in the window
button_yes.pack()
button_no.pack()

# Run the application
try:
    window.mainloop()
finally:
    clean_up()
