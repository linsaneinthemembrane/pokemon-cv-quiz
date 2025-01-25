from PIL import Image, ImageOps, ImageFilter, UnidentifiedImageError
import os

def create_silhouettes():
    sprites_folder = "pokemon_sprites"
    
    base_folders = [
        "generation-i", "generation-ii", "generation-iii",
        "generation-iv", "generation-v", "generation-vi",
        "generation-vii", "generation-viii", "generation-ix"
    ]
    
    for gen_folder in base_folders:
        source_path = os.path.join(sprites_folder, gen_folder)
        if not os.path.exists(source_path):
            print(f"Skipping {gen_folder} - folder not found")
            continue
            
        silhouette_folder = f"{gen_folder}-silhouettes"
        os.makedirs(silhouette_folder, exist_ok=True)
        
        for filename in os.listdir(source_path):
            if filename.endswith('.png'):
                input_path = os.path.join(source_path, filename)
                output_path = os.path.join(silhouette_folder, filename)
                
                try:
                    # Convert to binary mask
                    image = Image.open(input_path).convert('RGBA')
                    
                    mask = image.split()[3]
                    
                    # Fill with gray
                    gray_value = 128  # Medium gray
                    silhouette = Image.new('RGB', image.size, (gray_value, gray_value, gray_value))
                    
                    # Apply mask
                    silhouette.putalpha(mask)
                    
                    # Save as PNG
                    silhouette.save(output_path, 'PNG')
                    print(f"Created silhouette for {filename}")
                except UnidentifiedImageError:
                    print(f"Failed to process {filename} - corrupted or invalid image")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    create_silhouettes()
