# Pokemon CV Quiz Automation

[![Demo Video](https://img.youtube.com/vi/dXSMtpPaXHQ/0.jpg)](https://www.youtube.com/watch?v=dXSMtpPaXHQ)

*Using the bot it took 10:32 to name every single Pokemon (minus 3)*


## Overview
This project automates the Pokemon Quiz game using computer vision and image processing. It includes three main components:
1. Pokemon sprite downloading using PokeAPI
2. Sprite preprocessing to create silhouettes
3. Quiz automation using template matching

## Setup and Installation

### Prerequisites
```
pip install opencv-python numpy pygetwindow pyautogui Pillow requests
```

### Getting Started

1. **Download Pokemon Sprites** (script.py)
```
python script.py
```
This will:
- Connect to PokeAPI
- Download sprites for all Pokemon generations
- Save them in organized folders by generation
2. **Create Silhouettes** (outline.py)
```
python outline.py
```
This will:
- Process downloaded sprites
- Create gray silhouettes
- Save them in generation-specific folders
3. **Run Quiz Automation** (automate_quiz.py)
```
python automate_quiz.py
```
This will:
- Open the Pokemon Quiz in Chrome
- Match silhouettes with templates
- Automatically input Pokemon names

## Features

### API Integration
- Uses PokeAPI for sprite collection
- Handles all Pokemon generations
- Organized file structure

### Image Processing
- Converts sprites to silhouettes
- Maintains aspect ratios
- Handles transparency

### Quiz Automation
- Real-time template matching
- Multiple scale detection
- Confidence-based matching
- Automatic name entry

## Example Files
The repository includes example files for:
- Original Pokemon sprites (first 5)
- Processed silhouettes (first 5)
These demonstrate the expected input/output formats.

## Troubleshooting

- **Window Detection**: Ensure Pokemon Quiz is open in Chrome
- **Image Processing**: Check sprite folder structure
- **Quiz Automation**: Adjust confidence threshold if needed

## Exit Instructions
Move your mouse cursor to the top-left corner (coordinates 0,0) to stop the automation script.

## Notes
- Processing all Pokemon sprites may take time
- Large sprite collections should be handled via Git LFS
- Example folders show expected file formats
