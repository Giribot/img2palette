# 🎨 img2palette

<img width="731" height="405" alt="example" src="https://github.com/user-attachments/assets/37101d6d-8d1a-47af-8603-7b50e474abf6" />


A Python application that extracts dominant colors from images and generates visual color palettes.
Built with Gradio for an intuitive web interface.

## 🌟 Features

- **Color Extraction**: Automatically extracts dominant colors from any image
- **Smart Grouping**: Uses K-means clustering to group similar colors
- **Hue Sorting**: Optional sorting by color spectrum (red → orange → yellow → green → blue → purple)
- **Customizable**: Adjustable number of colors (5-200) for optimal results
- **Visual Palette**: Generates a square grid palette with color swatches
- **Easy Download**: One-click download of generated palettes
- **Web Interface**: User-friendly Gradio interface with drag & drop support

## 📦 Installation

### Method 1: Automatic Installation (Windows)
```bash
# Download all files in the same folder and double-click:
install_and_run.bat
```
### Method 2: Manual Installation (Windows/Mac/Linux)
```
# Clone the repository
git clone https://github.com/yourusername/color-palette-extractor.git
cd color-palette-extractor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🚀 Usage
Launch the application - The web interface will open automatically in your browser
Upload an image - Drag & drop or click to select an image file
Adjust settings:
Set maximum number of colors (default: 50)
Enable/disable hue sorting (default: enabled)
Click "Extract Colors" - Generate the color palette
Download - Save your palette with the download button

## 🛠️ Technical Details
Dependencies
Pillow: Image processing and manipulation,
NumPy: Numerical computing and array operations,
Gradio: Web interface framework,
Scikit-learn: K-means clustering for color grouping,

## How It Works
Color Extraction: Converts image to RGB and extracts all pixel values,
Color Reduction: Uses K-means clustering to group similar colors when exceeding the limit,
Color Sorting: Optionally sorts colors by hue for better visual organization,
Palette Generation: Creates a square grid with color swatches,
Output: Generates a PNG image of the color palette,
Output Dimensions
Swatch Size: 50×50 pixels (customizable in code),
Grid Layout: Square grid (e.g., 7×7 for 50 colors = 350×350 pixels),
Background: White background for better color visibility,

## 📁 Project Structure
color-palette-extractor/
│
├── app.py                 # Main application script
├── requirements.txt       # Python dependencies
├── install_and_run.bat    # Windows installation script
└── README.md             # This file







