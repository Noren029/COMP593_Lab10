import requests
import os

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_info():
    """Fetch a list of Pokémon names from the PokéAPI."""
    response = requests.get(POKEAPI_URL + "?limit=1000")  # Get all Pokémon
    if response.status_code == 200:
        data = response.json()
        return [pokemon['name'] for pokemon in data['results']]
    return []

def download_pokemon_artwork(pokemon_name, save_dir="pokemon_images"):
    """Download the official artwork for a Pokémon and save it locally."""
    url = f"{POKEAPI_URL}{pokemon_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['sprites']['other']['official-artwork']['front_default']
        
        if image_url:
            # Ensure the save directory exists
            os.makedirs(save_dir, exist_ok=True)
            
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                file_path = os.path.join(save_dir, f"{pokemon_name}.png")
                with open(file_path, "wb") as f:
                    f.write(image_response.content)
                return file_path
    return None
