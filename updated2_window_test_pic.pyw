import os
import sys
import logging
import tkinter as tk
from PIL import Image, ImageTk
import winerror
import win32event
import win32api
import win32con

logging.basicConfig(filename='application.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Unique name for the mutex (specific to your application)
mutex_name = "window_test_pic_python_practice"

# Try to create a mutex
logging.debug("Attempting to create mutex.")
mutex_handle = win32event.CreateMutex(None, False, mutex_name)
last_error = win32api.GetLastError()
logging.debug(f"Mutex created, last error: {last_error}")

if last_error == winerror.ERROR_ALREADY_EXISTS:
    logging.debug("Detected that the application is already running.")
    win32api.CloseHandle(mutex_handle)
    logging.debug("Mutex handle closed.")
    sys.exit(0)

# Check if the mutex already exists
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    win32api.CloseHandle(mutex_handle)
    print("Application is already running.")
    sys.exit(0)

def on_yes_click():
    for widget in window.winfo_children():
        widget.destroy()
    tk.Label(window, text="Yes").pack()
    pass

def on_no_click():
    window.destroy()
    pass

# Create the main window
window = tk.Tk()

def clean_up():
    logging.info("Cleaning up and exiting.")
    win32api.CloseHandle(mutex_handle)
    window.destroy()
    pass

# Bind the clean_up function to the window close event
window.protocol("WM_DELETE_WINDOW", clean_up)

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

# Release the mutex when the application is closing
win32api.CloseHandle(mutex_handle)
