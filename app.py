from PIL import Image
import numpy as np
import math
import gradio as gr
import io
from collections import Counter
from sklearn.cluster import KMeans
import colorsys

def rgb_to_hsv(rgb):
    """Convertit RGB vers HSV"""
    r, g, b = rgb / 255.0
    return np.array(colorsys.rgb_to_hsv(r, g, b))

def extract_dominant_colors(image, max_colors=100):
    """Extrait les couleurs dominantes en regroupant par teintes"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convertit en tableau numpy
    np_image = np.array(image)
    pixels = np_image.reshape(-1, 3)
    
    if len(pixels) == 0:
        return np.array([])
    
    # Si on a moins de couleurs que la limite, on retourne toutes les couleurs uniques
    unique_pixels = np.unique(pixels, axis=0)
    if len(unique_pixels) <= max_colors:
        return unique_pixels
    
    # Sinon, on utilise K-means pour regrouper les couleurs similaires
    kmeans = KMeans(n_clusters=max_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Retourne les centres des clusters (couleurs dominantes)
    return kmeans.cluster_centers_.astype(int)

def sort_colors_by_hue(colors):
    """Trie les couleurs par teinte (HSL)"""
    def get_hue(rgb):
        r, g, b = rgb / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return h
    
    def get_brightness(rgb):
        return np.mean(rgb)
    
    # Trie d'abord par teinte, puis par luminosité
    sorted_colors = sorted(colors, key=lambda rgb: (get_hue(rgb), get_brightness(rgb)))
    return np.array(sorted_colors)

def create_color_palette(colors, square_size=50):
    if len(colors) == 0:
        return None
        
    num_colors = len(colors)
    # Calcul du nombre de colonnes et lignes pour faire un carré
    grid_size = math.ceil(math.sqrt(num_colors))
    palette_size = grid_size * square_size

    # Crée une image vide
    palette = Image.new("RGB", (palette_size, palette_size), (255, 255, 255))

    for i, color in enumerate(colors):
        r, g, b = color
        # Crée un carré de la couleur
        color_square = Image.new("RGB", (square_size, square_size), (int(r), int(g), int(b)))
        x = (i % grid_size) * square_size
        y = (i // grid_size) * square_size
        palette.paste(color_square, (x, y))

    return palette

def process_image(input_image, max_colors, sort_by_hue):
    if input_image is None:
        return None, "Veuillez uploader une image"
    
    try:
        # Extraction des couleurs dominantes
        colors = extract_dominant_colors(input_image, max_colors)
        
        # Tri par teinte si demandé
        if sort_by_hue and len(colors) > 0:
            colors = sort_colors_by_hue(colors)
        
        # Création de la palette
        palette = create_color_palette(colors)
        
        if palette is not None:
            message = f"Palette créée avec {len(colors)} couleurs dominantes"
            return palette, message
        else:
            return None, "Aucune couleur trouvée dans l'image"
            
    except Exception as e:
        return None, f"Erreur lors du traitement : {str(e)}"

def download_palette(input_image, max_colors, sort_by_hue):
    if input_image is None:
        return None
    
    try:
        colors = extract_dominant_colors(input_image, max_colors)
        if sort_by_hue and len(colors) > 0:
            colors = sort_colors_by_hue(colors)
        palette = create_color_palette(colors)
        if palette:
            # Sauvegarde dans un buffer
            buffer = io.BytesIO()
            palette.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer
    except:
        return None

# Création de l'interface Gradio
with gr.Blocks(title="Extracteur de Palette de Couleurs") as demo:
    gr.Markdown("# 🎨 Extracteur de Palette de Couleurs")
    gr.Markdown("Upload une image pour extraire les couleurs dominantes et créer une palette visuelle")
    
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="pil", label="Image d'entrée")
            max_colors = gr.Slider(minimum=5, maximum=200, value=50, step=5, label="Nombre maximum de couleurs")
            sort_by_hue = gr.Checkbox(value=True, label="Trier par teintes")
            with gr.Row():
                submit_btn = gr.Button("🎨 Extraire les couleurs", variant="primary")
                download_btn = gr.DownloadButton("💾 Télécharger la palette", variant="secondary")
        
        with gr.Column():
            output_image = gr.Image(label="Palette de couleurs", interactive=False)
            status_text = gr.Textbox(label="Statut", interactive=False)
    
    # Traitement principal
    submit_btn.click(
        fn=process_image,
        inputs=[input_image, max_colors, sort_by_hue],
        outputs=[output_image, status_text]
    )
    
    # Téléchargement
    download_btn.click(
        fn=download_palette,
        inputs=[input_image, max_colors, sort_by_hue],
        outputs=[download_btn]
    )
    
    # Exemples
    gr.Examples(
        examples=[
            ["https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1200px-React-icon.svg.png", 50, True],
            ["https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/HTML5_logo_and_wordmark.svg/1200px-HTML5_logo_and_wordmark.svg.png", 30, True]
        ],
        inputs=[input_image, max_colors, sort_by_hue],
        outputs=[output_image, status_text],
        fn=process_image
    )

if __name__ == "__main__":
    demo.launch()