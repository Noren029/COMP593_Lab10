import requests
import os
from PIL import Image

def get_pokemon_list():
    """Fetch a list of 50 Pokémon names."""
    url = "https://pokeapi.co/api/v2/pokemon?limit=50"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [pokemon['name'].capitalize() for pokemon in data['results']]
    return []

def get_pokemon_info(pokemon_name):
    """Fetch detailed information about a specific Pokémon."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def download_pokemon_image(pokemon_name, save_dir="images"):
    """Download the official artwork for a Pokémon and save it locally."""
    os.makedirs(save_dir, exist_ok=True)
    image_path = os.path.join(save_dir, f"{pokemon_name}.png")
    
    if os.path.exists(image_path):
        print(f"Image for {pokemon_name} already exists.")
        return image_path  # Skip downloading if the file exists
    
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info:
        # Safely access nested fields
        image_url = pokemon_info.get("sprites", {}).get("other", {}).get("official-artwork", {}).get("front_default")
        if image_url:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Image for {pokemon_name} downloaded successfully.")
                return image_path
            else:
                print(f"Failed to download image for {pokemon_name}.")
        else:
            print(f"No image found for {pokemon_name}.")
    else:
        print(f"Failed to fetch data for {pokemon_name}.")
    
    return None
