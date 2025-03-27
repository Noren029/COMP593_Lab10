from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import os
import ctypes
from pokeapi import get_pokemon_info

# Set Windows Taskbar Icon
app_id = 'Pokemon.ImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

def fetch_and_display_image(event=None):
    """Fetch Pokémon image from API and display it in the Tkinter window."""
    pokemon_name = combobox_choose.get().lower()
    if pokemon_name not in ['pikachu', 'charizard', 'clefairy']:
        return  # Prevent errors if no Pokémon is chosen

    poke_info = get_pokemon_info(pokemon_name)
    if poke_info and 'sprites' in poke_info:
        image_url = poke_info['sprites']['front_default']
        if image_url:
            response = requests.get(image_url)
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((150, 150), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img_data)

            lbl_image.config(image=img)
            lbl_image.image = img  # Keep reference to prevent garbage collection

            # Enable the "Set as Desktop Image" button when a Pokémon is selected
            btn_set_desktop.config(state=NORMAL)

            # Save the image for later use
            global saved_image_path
            saved_image_path = os.path.join(os.getcwd(), "pokemon_wallpaper.jpg")
            img_data.save(saved_image_path, "JPEG")

def set_desktop_wallpaper():
    """Set the saved Pokémon image as desktop wallpaper (Windows only)."""
    if saved_image_path:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, saved_image_path, 3)

def main():
    global combobox_choose, lbl_image, btn_set_desktop, saved_image_path  

    root = Tk()
    root.title("Pokémon Image Viewer")
    root.geometry("800x600")
    root.resizable(True, True)

    # Change Python Default Icon to Custom Icon
    root.iconbitmap("pokeball.ico")

    # Image frame and label
    frm_image = ttk.Frame(root)
    frm_image.grid(row=0, column=0, pady=(20, 10))
    lbl_image = ttk.Label(frm_image, text="Pokémon Image")
    lbl_image.grid(row=0, column=0, padx=(10, 5), pady=10)

    # Combobox input frame
    frm_combobox = ttk.Frame(root)
    frm_combobox.grid(row=1, column=0, pady=(20, 10))
    poke_list = ['pikachu', 'charizard', 'clefairy']
    combobox_choose = ttk.Combobox(frm_combobox, values=poke_list, state='readonly')
    combobox_choose.set("Choose a Pokémon")
    combobox_choose.grid(padx=10, pady=10)

    # Bind event to enable button when Pokémon is selected
    combobox_choose.bind("<<ComboboxSelected>>", fetch_and_display_image)

    # "Set as Desktop Image" button (Initially Disabled)
    btn_set_desktop = ttk.Button(root, text="Set as Desktop Image", command=set_desktop_wallpaper, state=DISABLED)
    btn_set_desktop.grid(row=2, column=0, pady=(10, 20))

    root.mainloop()

main()
