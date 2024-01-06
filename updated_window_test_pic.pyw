import os
import sys
import logging
from PIL import Image, ImageTk
import tkinter as tk
import portalocker

# Configure logging
logging.basicConfig(filename='application.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.debug("Starting the application.")

# Path to the lock file
lock_file_path = 'C:/Temp/window_test_pic.lock'

# Try to open (and lock) the lock file exclusively
try:
    with open(lock_file_path, 'w') as lock_file:
        portalocker.lock(lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
        logging.debug("Lock acquired, continuing execution.")
        # Rest of your application code
except portalocker.LockException:
    logging.info("Another instance of the application is already running.")
    print("Another instance of the application is already running.")
    sys.exit(0)

# Create the lock file
logging.debug("Creating the lock file.")
try:
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write('')
except Exception as e:
    logging.error(f"Error creating lock file: {e}")
    raise

from PIL import Image, ImageTk

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
    # Delete the lock file if it exists
    logging.debug("clean_up called.")
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)
    # Close the application
    window.destroy()

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
window.mainloop()
