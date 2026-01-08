#!/usr/bin/env python3
"""
IWT Image Generator using Google Gemini API (Nano Banana)

Usage:
    export GEMINI_API_KEY="your-key-here"
    python3 generate-images.py
"""

import os
import base64
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = os.environ.get('GEMINI_API_KEY')
MODEL = 'gemini-2.0-flash-exp'

if not API_KEY:
    print('Error: GEMINI_API_KEY environment variable not set')
    print('Get your API key from: https://aistudio.google.com/apikey')
    print('Then run: export GEMINI_API_KEY="your-key-here"')
    exit(1)

# Create images directory
images_dir = Path(__file__).parent / 'images'
images_dir.mkdir(exist_ok=True)

# Style guide for consistent isometric flat-color images
style_guide = """
Style requirements:
- Isometric 3D perspective (30-degree angle)
- Flat colors with minimal gradients
- Clean, modern, professional aesthetic
- Color palette: warm tan/gold (#D4A055), white, gray, with subtle accent colors
- No text or labels in the image
- Simple geometric shapes
- Soft shadows for depth
- White or light gray background
- Professional industrial/tech aesthetic
"""

# Image prompts matching the PDF style
image_prompts = [
    {
        'name': 'modular-plant-1',
        'prompt': f'An isometric view of a modular industrial waste processing facility with multiple smokestacks, conveyor systems, and a main processing building. The design is modern with flat tan/brown roofing and industrial gray equipment. Clean lines and professional aesthetic. {style_guide}'
    },
    {
        'name': 'modular-plant-2',
        'prompt': f'An isometric view of a modular gasification unit with large cylindrical pressure vessels in pink/salmon color, metal piping, and supporting steel structure. Industrial equipment module for a waste-to-energy plant. {style_guide}'
    },
    {
        'name': 'modular-plant-3',
        'prompt': f'An isometric view of an industrial gas processing module with multiple spherical tanks, a tall cylindrical column, and metal framework. The tanks are in muted pink/beige colors with industrial gray piping. {style_guide}'
    },
    {
        'name': 'pipeline-milwaukee',
        'prompt': f'An aerial isometric view of a modern waste-to-energy facility campus with multiple buildings, large cylindrical storage tanks, green landscaping, and a parking area. Set in a green countryside. Professional industrial facility. {style_guide}'
    },
    {
        'name': 'pipeline-virginia',
        'prompt': f'An aerial isometric view of a medium-scale waste processing plant with large dome-shaped biogas digesters, modern industrial buildings, and solar panels on the roof. Clean facility design. {style_guide}'
    },
    {
        'name': 'pipeline-louisiana',
        'prompt': f'An aerial isometric view of a large industrial petrochemical integration facility with tall processing towers, multiple storage tanks, and steel framework structures. Modern waste-to-energy plant. {style_guide}'
    },
    {
        'name': 'product-jet-fuel',
        'prompt': f'An isometric view of a metal fuel barrel/drum for jet fuel with a diamond hazard warning label. Industrial steel container with silver metallic finish. Simple clean design. {style_guide}'
    },
    {
        'name': 'product-ethanol',
        'prompt': f'An isometric view of a glass laboratory bottle containing clear liquid ethanol with a black cap. The bottle has a simple label. Clean laboratory/scientific aesthetic. {style_guide}'
    },
    {
        'name': 'product-meg',
        'prompt': f'An isometric view of a blue industrial chemical barrel/drum for storing monoethylene glycol. Large 55-gallon drum with blue finish. Industrial container design. {style_guide}'
    },
    {
        'name': 'product-pet',
        'prompt': f'An isometric view of colorful PET plastic bottles - one red, one green, one orange, and a white container. Representing polyethylene terephthalate products. Consumer plastic bottles. {style_guide}'
    },
]


def generate_image(prompt):
    """Generate an image using Gemini API"""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}'

    request_body = {
        'contents': [{
            'parts': [{
                'text': prompt
            }]
        }],
        'generationConfig': {
            'responseModalities': ['TEXT', 'IMAGE']
        }
    }

    data = json.dumps(request_body).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))

            if 'error' in result:
                raise Exception(result['error'].get('message', 'Unknown error'))

            # Extract image from response
            candidates = result.get('candidates', [])
            for candidate in candidates:
                parts = candidate.get('content', {}).get('parts', [])
                for part in parts:
                    if 'inlineData' in part:
                        return {
                            'mimeType': part['inlineData']['mimeType'],
                            'data': part['inlineData']['data']
                        }

            raise Exception('No image in response')

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f'HTTP {e.code}: {error_body}')


def save_image(name, image_data):
    """Save base64 image to file"""
    ext = 'png' if 'png' in image_data['mimeType'] else 'jpg'
    filename = images_dir / f'{name}.{ext}'

    image_bytes = base64.b64decode(image_data['data'])
    filename.write_bytes(image_bytes)

    print(f'  Saved: {filename}')
    return filename


def main():
    print('Starting IWT image generation...\n')
    print(f'Generating {len(image_prompts)} images in isometric flat-color style\n')

    successful = 0
    failed = 0

    for img in image_prompts:
        print(f'Generating: {img["name"]}...')
        try:
            image_data = generate_image(img['prompt'])
            save_image(img['name'], image_data)
            successful += 1
            # Rate limiting - wait 3 seconds between requests
            time.sleep(3)
        except Exception as e:
            print(f'  Failed: {e}')
            failed += 1

    print(f'\nImage generation complete!')
    print(f'  Successful: {successful}')
    print(f'  Failed: {failed}')
    print(f'  Images saved to: {images_dir}')


if __name__ == '__main__':
    main()
