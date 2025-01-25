import cv2
import numpy as np
import pygetwindow as gw
import pyautogui
import time
import os

def get_pokemon_names(folder_path):
    pokemon_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            pokemon_name = filename.split('_')[1].replace('.png', '')
            pokemon_dict[filename] = pokemon_name
    return pokemon_dict

def preprocess_template(template):
    # Convert to grayscale
    gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # Create binary mask
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    # Convert to solid gray (128,128,128) like in the quiz
    result = np.zeros_like(gray)
    result[binary > 0] = 128
    return result

def match_silhouette(screenshot, template, pokemon_name):
    # Show what we're processing
    processed_template = preprocess_template(template)
    
    # Display current processing
    cv2.imshow('Current Pokemon', template)
    cv2.imshow('Processed Template', processed_template)
    cv2.imshow('Screenshot', screenshot)
    cv2.waitKey(1)
    
    # Try multiple scales
    scales = [0.1]
    max_confidence = 0
    
    for scale in scales:
        width = int(template.shape[1] * scale)
        height = int(template.shape[0] * scale)
        resized = cv2.resize(processed_template, (width, height))
        
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        confidence = np.max(result)
        max_confidence = max(max_confidence, confidence)
        
        print(f"Matching {pokemon_name} at scale {scale}: confidence = {confidence}")
    
    return max_confidence

def setup_window_capture():
    quiz_window = gw.getWindowsWithTitle("Pokémon Quiz - Google Chrome")
    if not quiz_window:
        raise Exception("Could not find Pokemon Quiz window. Make sure the quiz is open in Chrome.")
    
    window = quiz_window[0]
    window.activate()
    time.sleep(2)
    return window

def play_quiz():
    # Setup window capture
    quiz_window = gw.getWindowsWithTitle("Pokémon Quiz - Google Chrome")[0]
    quiz_window.activate()
    time.sleep(2)  # Give time for window to activate
    
    # Load reference silhouettes
    silhouettes_path = "pokemon_sprites"
    pokemon_names = get_pokemon_names(silhouettes_path)
    matched_pokemon = set()  # Track matches
    
    print("Starting Pokemon Quiz automation...")
    print(f"Loaded {len(pokemon_names)} Pokemon references")
    
    while True:
        try:
            # Capture full window
            screenshot = pyautogui.screenshot(region=(
                quiz_window.left,
                quiz_window.top,
                quiz_window.width,
                quiz_window.height
            ))
            
            # Convert to numpy array for OpenCV
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            
            # Save current screenshot for debugging
            cv2.imwrite('current_screen.png', screenshot)
            
            # Convert to grayscale for processing
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Process each Pokemon
            for filename, pokemon_name in pokemon_names.items():
                if pokemon_name in matched_pokemon:
                    continue
                
                template_path = os.path.join(silhouettes_path, filename)
                template = cv2.imread(template_path)
                
                if template is None:
                    print(f"Failed to load template: {filename}")
                    continue
                
                confidence = match_silhouette(gray_screenshot, template, pokemon_name)
                
                if confidence > 0.6:  # Adjust threshold as needed
                    print(f"Match found: {pokemon_name} ({confidence:.2f})")
                    pyautogui.write(pokemon_name)
                    pyautogui.press('enter')
                    matched_pokemon.add(pokemon_name)
                    time.sleep(0.3)  # Brief delay between entries
            
            # Optional: Print progress
            print(f"Current matches: {len(matched_pokemon)}/{len(pokemon_names)}")
            
            # Exit if mouse moved to top-left corner
            if pyautogui.position().x == 0 and pyautogui.position().y == 0:
                print("Exit signal received")
                break
                
            time.sleep(0.005)  # Small delay to prevent excessive CPU usage
            
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            continue

    
if __name__ == "__main__":
    try:
        play_quiz()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        cv2.destroyAllWindows()