"""
Pokémon Image Viewer

A Tkinter-based GUI application that allows users to:
- Select a Pokémon from a dropdown list (fetched from PokéAPI)
- Display the Pokémon's image
- Set the image as the desktop wallpaper (Windows only)

Dependencies:
- `pokeapi.py` (a module with functions to fetch Pokémon list and download images)
- `Pillow` (for image manipulation)
- `ctypes` (for setting wallpaper on Windows)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
import ctypes
import os
from pokeapi import get_pokemon_list, download_pokemon_image
from PIL import Image  # Importing PIL for image manipulation

# Set Windows Taskbar Icon (optional)
app_id = 'Pokemon.ImageViewer'

def fetch_and_display_image(event=None):
    """
    Fetch Pokémon image from API and display it in the Tkinter window.

    Retrieves the selected Pokémon's image using `download_pokemon_image`,
    then displays it in the GUI. Enables the "Set as Desktop Image" button
    once an image is successfully loaded.

    Args:
        event (optional): The event that triggers this function (e.g., combobox selection).
    """
    pokemon_name = combo.get().lower()
    
    if pokemon_name:
        # Get the Pokémon image using the download_pokemon_image function
        image_path = download_pokemon_image(pokemon_name)

        if image_path:
            # Open the downloaded image using PhotoImage and display it
            photo = PhotoImage(file=image_path)
            img_label.config(image=photo)
            img_label.photo = photo  # Keep reference to prevent garbage collection

            # Enable the "Set as Desktop Image" button when a Pokémon is selected
            btn_set_desktop.config(state=tk.NORMAL)

            # Save the image path for later use (in case it's needed for setting as wallpaper)
            global saved_image_path
            saved_image_path = image_path  # Save the path of the image

        else:
            messagebox.showerror("Error", "Image not found!")

def set_desktop_wallpaper():
    """
    Set the saved Pokémon image as desktop wallpaper (Windows only).

    Converts the image to a `.jpg` format if necessary,
    then uses Windows API (`ctypes`) to set it as the wallpaper.

    Displays an error message if the operation fails.
    """
    if saved_image_path:
        # Ensure the saved image has the .jpg extension, as Windows prefers jpg for wallpapers
        wallpaper_path = saved_image_path if saved_image_path.lower().endswith('.jpg') else saved_image_path.replace('.png', '.jpg')

        # Convert the image to JPG if it's in PNG format
        if not saved_image_path.lower().endswith('.jpg'):
            try:
                img = Image.open(saved_image_path)
                img = img.convert("RGB")  # Convert to RGB to support JPG format
                img.save(wallpaper_path, "JPEG")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert image to JPG: {e}")
                return

        # Use ctypes to set the wallpaper
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
        
        if result == 0:  # If the function fails
            messagebox.showerror("Error", "Failed to set wallpaper.")
        else:
            messagebox.showinfo("Success", "Wallpaper set successfully!")

def exit_app():
    """
    Exit the application by closing the Tkinter GUI.
    """
    root.quit()

def main():
    """
    Main function to initialize and run the Tkinter GUI.

    The function sets up the window, frames, widgets (combobox, image display, buttons),
    and handles user interaction.
    """
    # Initialize Tkinter window
    global root
    root = tk.Tk()
    root.title("Pokémon Image Viewer")
    root.geometry("600x650")
    root.resizable(True, True)
    root.iconbitmap("pokeball.ico")

    # Image frame and label
    frm_image = ttk.Frame(root)
    frm_image.pack(pady=20)
    global img_label
    img_label = tk.Label(frm_image, text="Pokémon Image")
    img_label.pack()

    # Combobox input frame
    frame = ttk.Frame(root)
    frame.pack(pady=20)

    # Combobox to select Pokémon
    global combo
    combo = ttk.Combobox(frame, state="readonly", width=30)
    combo['values'] = get_pokemon_list()  # Populate with Pokémon list
    combo.pack()
    combo.bind("<<ComboboxSelected>>", fetch_and_display_image)

    # "Set as Desktop Image" button (Initially Disabled)
    global btn_set_desktop
    btn_set_desktop = ttk.Button(root, text="Set as Desktop Image", command=set_desktop_wallpaper, state=tk.DISABLED)
    btn_set_desktop.pack(pady=10)


    root.mainloop()

# Call the main function directly
main()
