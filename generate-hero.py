#!/usr/bin/env python3
"""Generate hero background image for IWT website"""

import os
import base64
import json
import urllib.request
from pathlib import Path

API_KEY = os.environ.get('GEMINI_API_KEY')
MODEL = 'gemini-2.0-flash-exp'

images_dir = Path(__file__).parent / 'images'
images_dir.mkdir(exist_ok=True)

prompt = """
Create a wide, abstract illustration representing waste-to-energy transformation for a company website hero section.

The image should show:
- On the left side: Abstract/stylized representation of waste/garbage (geometric shapes, simplified forms)
- In the center: A transformation process - energy flow, light rays, or conversion symbolism
- On the right side: Clean energy powering technology - subtle data center or power symbols

Style requirements:
- Warm color palette dominated by tan/gold (#D4A055) and amber tones
- Clean, modern, corporate aesthetic
- Abstract and artistic - NOT realistic garbage or facilities
- Subtle, not overpowering - this will be a background image
- Flowing, dynamic composition from left to right
- Light/white background that fades to transparent or light gray
- Professional and sophisticated
- Minimal detail, more suggestive shapes and gradients
- Isometric or flat design style

This is for a professional B2B company website. The image should convey transformation, sustainability, and technology without being literal or cartoonish. Think abstract data visualization meets energy flow diagram.
"""

def generate_image():
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
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    print('Generating hero background...')
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode('utf-8'))

        for candidate in result.get('candidates', []):
            for part in candidate.get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    ext = 'png' if 'png' in part['inlineData']['mimeType'] else 'jpg'
                    filename = images_dir / f'hero-bg.{ext}'
                    image_bytes = base64.b64decode(part['inlineData']['data'])
                    filename.write_bytes(image_bytes)
                    print(f'Saved: {filename}')
                    return

    print('No image generated')

if __name__ == '__main__':
    generate_image()
