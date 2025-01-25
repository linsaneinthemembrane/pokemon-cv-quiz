import requests
import os
import json

def download_pokemon_sprites():
    base_url = "https://pokeapi.co/api/v2/"
    sprite_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"
    
    main_folder = "pokemon_sprites"
    os.makedirs(main_folder, exist_ok=True)
    
    generations = requests.get(f"{base_url}generation").json()["results"]
    
    for gen in generations:
        gen_data = requests.get(gen["url"]).json()
        gen_name = gen_data["name"]
        print(f"Downloading sprites for Generation {gen_name}")
        
        gen_folder = os.path.join(main_folder, gen_name)
        os.makedirs(gen_folder, exist_ok=True)
        
        # take all pokemon in this gen
        for species in gen_data["pokemon_species"]:
            species_data = requests.get(species["url"]).json()
            pokemon_id = species_data["id"]
            pokemon_name = species_data["name"]
            
            # naming
            sprite_file = f"{pokemon_id}.png"
            full_sprite_url = f"{sprite_url}{sprite_file}"
            
            sprite_response = requests.get(full_sprite_url)
            if sprite_response.status_code == 200:
                # Save the sprite
                with open(os.path.join(gen_folder, f"{pokemon_id}_{pokemon_name}.png"), "wb") as f:
                    f.write(sprite_response.content)
                print(f"Downloaded sprite for {pokemon_name}")
            else:
                print(f"Failed to download sprite for {pokemon_name}")

if __name__ == "__main__":
    download_pokemon_sprites()
