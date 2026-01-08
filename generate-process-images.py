#!/usr/bin/env python3
"""Generate process step images for IWT science section flipbook"""

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
    exit(1)

images_dir = Path(__file__).parent / 'images'
images_dir.mkdir(exist_ok=True)

# Consistent style for all process images
style_guide = """
Style requirements:
- Isometric 3D perspective (30-degree angle)
- Clean, minimal, professional industrial illustration
- Color palette: warm tan/gold (#D4A055) as accent, white/light gray background, dark gray (#1A1A1A) for equipment
- Simple geometric shapes, no complex details
- Soft shadows for depth
- Square format (1:1 aspect ratio)
- No text or labels in the image
- Single focal point in center
- Professional technical diagram aesthetic
- Consistent lighting from top-left
"""

# Process step images - each shows one stage of the Thermoselect process
process_steps = [
    {
        'name': 'process-step-1',
        'prompt': f"""An isometric illustration of waste reception at an industrial facility.
Show a garbage truck dumping mixed waste (colorful bags, boxes, debris) into a large reception hopper/pit.
The hopper should be a large tan/gold colored industrial container with a hydraulic press mechanism visible.
Waste is being compressed into dense rectangular plugs.
Clean industrial setting with concrete floor.
{style_guide}"""
    },
    {
        'name': 'process-step-2',
        'prompt': f"""An isometric illustration of a pyrolysis chamber (degasification).
Show a horizontal cylindrical chamber in dark gray with tan/gold accents.
Inside, show compressed waste plugs moving through the heated chamber.
Wavy heat lines emanating from the chamber walls (orange/red glow).
Steam and gas rising from the chamber into pipes above.
No flames - only radiant heat visualization.
{style_guide}"""
    },
    {
        'name': 'process-step-3',
        'prompt': f"""An isometric illustration of a high-temperature gasification reactor.
Show a large vertical cylindrical reactor vessel in dark gray.
Glowing orange/yellow core visible through a window showing 2000°C temperature.
Oxygen injection pipes in blue feeding into the reactor.
Molten material (orange glow) at the bottom.
Synthesis gas pipes exiting from the top.
{style_guide}"""
    },
    {
        'name': 'process-step-4',
        'prompt': f"""An isometric illustration of a shock quench cooling system.
Show molten material (glowing orange) falling into a water quench tank.
Steam clouds rising from the rapid cooling process.
The quench tank is a large industrial vessel in tan/gold color.
Conveyor belt carrying cooled dark gray granular material (vitrified slag) out of the tank.
Small metal pellets being separated on a secondary conveyor.
{style_guide}"""
    },
    {
        'name': 'process-step-5',
        'prompt': f"""An isometric illustration of a gas cleaning and water treatment system.
Show multiple cylindrical scrubber towers in tan/gold color.
Pipes connecting the towers showing gas flow.
A water treatment basin with clean blue water.
Small containers collecting byproducts: yellow sulfur, gray zinc concentrate, white salts.
Clean synthesis gas pipe exiting to the right.
{style_guide}"""
    },
    {
        'name': 'process-step-6',
        'prompt': f"""An isometric illustration of syngas energy conversion outputs.
Show clean synthesis gas pipe entering from the left.
A gas turbine generator in the center producing electricity (with power lines/lightning bolt symbol).
Additional output pipes branching to: a fuel container labeled area, industrial storage tanks.
Green energy symbols or leaf accents to show clean energy.
Power transmission tower in background.
{style_guide}"""
    }
]


def generate_image(prompt, previous_image=None):
    """Generate an image using Gemini API, optionally using previous image for continuity"""
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}'

    # Build parts list
    parts = []

    if previous_image:
        # Include previous image for visual continuity
        parts.append({
            'text': 'Here is the previous frame in our process sequence. Generate the next frame maintaining the same visual style, perspective, and color palette:'
        })
        parts.append({
            'inlineData': {
                'mimeType': previous_image['mimeType'],
                'data': previous_image['data']
            }
        })
        parts.append({
            'text': f'Now generate the next frame:\n\n{prompt}'
        })
    else:
        parts.append({
            'text': prompt
        })

    request_body = {
        'contents': [{
            'parts': parts
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
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode('utf-8'))

            if 'error' in result:
                raise Exception(result['error'].get('message', 'Unknown error'))

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
    print('Generating process step images for science section flipbook...\n')
    print('Each image will be fed into the next for visual continuity.\n')

    successful = 0
    failed = 0
    previous_image = None

    for i, step in enumerate(process_steps):
        print(f'Generating: {step["name"]} (step {i+1}/6)...')
        try:
            image_data = generate_image(step['prompt'], previous_image)
            save_image(step['name'], image_data)
            previous_image = image_data  # Chain to next image
            successful += 1
            # Rate limiting
            time.sleep(3)
        except Exception as e:
            print(f'  Failed: {e}')
            failed += 1
            # Continue with no previous image if one fails
            previous_image = None

    print(f'\nGeneration complete!')
    print(f'  Successful: {successful}')
    print(f'  Failed: {failed}')


if __name__ == '__main__':
    main()
