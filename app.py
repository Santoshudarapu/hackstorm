from flask import Flask, render_template, request, jsonify
import random
import colorsys
import math

app = Flask(__name__)

def get_complementary_hue(hue):
    return (hue + 0.5) % 1.0

def get_analogous_hues(hue, count=2, angle=0.02):
    hues = []
    start = hue - (angle * (count - 1) / 2)
    for i in range(count):
        hues.append((start + (i * angle)) % 1.0)
    return hues

def get_triadic_hues(hue):
    return [hue, (hue + 0.333) % 1.0, (hue + 0.666) % 1.0]

def get_split_complementary_hues(hue, angle=0.042):
    comp = get_complementary_hue(hue)
    return [hue, (comp - angle) % 1.0, (comp + angle) % 1.0]

def adjust_saturation(base_sat, index, style):
    if style == 'gradient':
        return max(0.2, base_sat - (index * 0.15))
    elif style == 'vibrant':
        return min(1.0, base_sat + (0.05 * (2 - abs(2 - index))))
    elif style == 'muted':
        return base_sat * (0.8 - (index * 0.1))
    elif style == 'pastel':
        return base_sat * (0.5 - (index * 0.05))
    return base_sat

def adjust_brightness(base_bright, index, style):
    if style == 'gradient':
        return max(0.3, base_bright - (index * 0.12))
    elif style == 'vibrant':
        return min(1.0, base_bright - (0.05 * abs(2 - index)))
    elif style == 'dark':
        return base_bright * (0.7 - (index * 0.1))
    elif style == 'light':
        return min(1.0, base_bright + (0.05 * (2 - abs(2 - index))))
    return base_bright

def generate_palette(description):
    # Enhanced color mapping with precise calibration
    keywords = {
        'sunset': {
            'hue': 0.025,
            'palette': 'gradient',
            'saturation': 0.95,
            'brightness': 0.95,
            'hues': [0.025, 0.042, 0.917, 0.833, 0.75],  # Warm orange to deep purple
            'saturations': [0.95, 0.9, 0.85, 0.9, 0.85],
            'brightnesses': [0.95, 0.9, 0.85, 0.8, 0.75]
        },
        'beach': {
            'hue': 0.5,
            'palette': 'complementary',
            'saturation': 0.8,
            'brightness': 0.9,
            'hues': [0.5, 0.583, 0.167, 0.083, 0.042],  # Ocean blue, sand, and sun
            'saturations': [0.8, 0.7, 0.4, 0.6, 0.85],
            'brightnesses': [0.9, 0.8, 0.95, 0.9, 0.95]
        },
        'forest': {
            'hue': 0.333,
            'palette': 'analogous',
            'saturation': 0.85,
            'brightness': 0.75,
            'hues': [0.333, 0.292, 0.375, 0.258, 0.417],  # Rich forest greens
            'saturations': [0.85, 0.8, 0.9, 0.75, 0.85],
            'brightnesses': [0.75, 0.7, 0.8, 0.65, 0.85]
        },
        'tech': {
            'hue': 0.583,
            'palette': 'monochromatic',
            'saturation': 0.7,
            'brightness': 0.9,
            'hues': [0.583, 0.583, 0.583, 0.583, 0.583],  # Clean tech blues
            'saturations': [0.7, 0.6, 0.5, 0.8, 0.4],
            'brightnesses': [0.9, 0.8, 0.7, 1.0, 0.6]
        },
        'modern': {
            'hue': 0.667,
            'palette': 'minimal',
            'saturation': 0.3,
            'brightness': 0.95,
            'hues': [0.667, 0.0, 0.0, 0.0, 0.667],  # Sleek grays with accent
            'saturations': [0.3, 0.0, 0.0, 0.0, 0.4],
            'brightnesses': [0.95, 0.9, 0.7, 0.3, 0.8]
        },
        'autumn': {
            'hue': 0.083,
            'palette': 'warm',
            'saturation': 0.85,
            'brightness': 0.85,
            'hues': [0.083, 0.042, 0.125, 0.025, 0.167],  # Rich autumn colors
            'saturations': [0.85, 0.9, 0.8, 0.95, 0.75],
            'brightnesses': [0.85, 0.8, 0.9, 0.75, 0.85]
        },
        'warm': {
            'hue': 0.042,
            'palette': 'warm',
            'saturation': 0.8,
            'brightness': 0.9,
            'hues': [0.042, 0.083, 0.025, 0.125, 0.0],  # Warm oranges and reds
            'saturations': [0.8, 0.85, 0.9, 0.75, 0.95],
            'brightnesses': [0.9, 0.85, 0.95, 0.8, 0.9]
        },
        'cool': {
            'hue': 0.583,
            'palette': 'cool',
            'saturation': 0.7,
            'brightness': 0.85,
            'hues': [0.583, 0.542, 0.625, 0.5, 0.667],  # Cool blues and purples
            'saturations': [0.7, 0.65, 0.75, 0.6, 0.8],
            'brightnesses': [0.85, 0.9, 0.8, 0.95, 0.75]
        },
        'night': {
            'hue': 0.667,
            'palette': 'dark',
            'saturation': 0.9,
            'brightness': 0.6,
            'hues': [0.667, 0.708, 0.625, 0.75, 0.583],  # Deep night blues
            'saturations': [0.9, 0.85, 0.95, 0.8, 0.9],
            'brightnesses': [0.6, 0.5, 0.7, 0.4, 0.65]
        },
        'earth': {
            'hue': 0.083,
            'palette': 'natural',
            'saturation': 0.6,
            'brightness': 0.8,
            'hues': [0.083, 0.042, 0.125, 0.025, 0.167],  # Earth tones
            'saturations': [0.6, 0.55, 0.65, 0.5, 0.7],
            'brightnesses': [0.8, 0.75, 0.85, 0.7, 0.9]
        },
        'nature': {
            'hue': 0.333,
            'palette': 'fresh',
            'saturation': 0.75,
            'brightness': 0.85,
            'hues': [0.333, 0.292, 0.375, 0.167, 0.417],  # Natural greens
            'saturations': [0.75, 0.7, 0.8, 0.65, 0.85],
            'brightnesses': [0.85, 0.8, 0.9, 0.75, 0.95]
        },
        'sky': {
            'hue': 0.583,
            'palette': 'bright',
            'saturation': 0.65,
            'brightness': 0.95,
            'hues': [0.583, 0.542, 0.625, 0.5, 0.667],  # Sky blues
            'saturations': [0.65, 0.6, 0.7, 0.55, 0.75],
            'brightnesses': [0.95, 1.0, 0.9, 0.85, 0.8]
        },
        'ocean': {
            'hue': 0.542,
            'palette': 'monochromatic',
            'saturation': 0.85,
            'brightness': 0.85,
            'hues': [0.542, 0.55, 0.558, 0.533, 0.525],  # Deep ocean blues
            'saturations': [0.85, 0.8, 0.75, 0.9, 0.85],
            'brightnesses': [0.85, 0.8, 0.75, 0.9, 0.7]
        },
        'fire': {
            'hue': 0.025,
            'palette': 'warm',
            'saturation': 1.0,
            'brightness': 0.95,
            'hues': [0.025, 0.042, 0.008, 0.058, 0.075],  # Fire tones
            'saturations': [1.0, 0.95, 1.0, 0.9, 0.85],
            'brightnesses': [0.95, 0.9, 1.0, 0.85, 0.8]
        },
        'royal': {
            'hue': 0.75,
            'palette': 'rich',
            'saturation': 0.95,
            'brightness': 0.8,
            'hues': [0.75, 0.792, 0.708, 0.833, 0.667],  # Rich royal colors
            'saturations': [0.95, 0.9, 1.0, 0.85, 0.9],
            'brightnesses': [0.8, 0.75, 0.85, 0.7, 0.9]
        }
    }

    # Process description to find matching keyword
    description = description.lower().strip()
    matched_keyword = None
    
    # Find exact match first
    for keyword in keywords:
        if keyword in description:
            matched_keyword = keyword
            break
    
    # If no exact match, find closest match
    if not matched_keyword:
        for keyword in keywords:
            if any(word in description for word in keyword.split()):
                matched_keyword = keyword
                break
    
    # Use default if no match found
    if not matched_keyword:
        matched_keyword = 'modern'
    
    # Get color settings
    settings = keywords[matched_keyword]
    
    # Generate colors using precise HSV values
    colors = []
    for i in range(5):
        h = settings['hues'][i]
        s = settings['saturations'][i]
        v = settings['brightnesses'][i]
        
        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(h, s, v)
        
        # Convert RGB to hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        colors.append(hex_color)
    
    return colors

@app.route('/', methods=['GET', 'POST'])
def index():
    colors = None
    description = None
    
    if request.method == 'POST':
        description = request.form.get('description')
        if description:
            colors = generate_palette(description)
            if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                return jsonify({'colors': colors})
    
    return render_template('index.html', colors=colors, description=description)

if __name__ == '__main__':
    app.run(debug=True)