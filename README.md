# IWT Website

A sleek, modern website for Interstate Waste Technologies.

## Quick Start

1. Open `index.html` in your browser to view the website
2. (Optional) Generate custom images using the Gemini API

## Generating Images with Google Gemini (Nano Banana)

The website includes placeholder graphics. To generate custom isometric images matching the PDF style:

### Option 1: Google AI Studio (Easiest)

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Select "Create new prompt" and choose an image model
3. Use prompts from `generate-images.js` to generate each image
4. Download and save to the `images/` folder

### Option 2: Node.js Script

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)

2. Set your API key:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

3. Run the generator:
   ```bash
   node generate-images.js
   ```

4. Images will be saved to the `images/` folder

### Image Style Guide

All images should follow this style:
- **Isometric 3D perspective** (30-degree angle)
- **Flat colors** with minimal gradients
- **Color palette**: warm tan/gold (#D4A055), white, gray
- **Clean geometric shapes**
- **Soft shadows** for depth
- **White or light gray background**
- **No text in images**

## File Structure

```
iwt/
├── index.html          # Main website
├── generate-images.js  # Image generation script
├── README.md           # This file
└── images/             # Generated images folder
    ├── hero-plant.png
    ├── modular-plant-1.png
    ├── modular-plant-2.png
    ├── modular-plant-3.png
    ├── pipeline-milwaukee.png
    ├── pipeline-virginia.png
    ├── pipeline-louisiana.png
    ├── product-jet-fuel.png
    ├── product-ethanol.png
    ├── product-meg.png
    ├── product-pet.png
    ├── data-center.png
    └── japan-map.png
```

## Brand Colors

- **Gold/Tan**: #D4A055 (primary)
- **Gold Light**: #E8C48A
- **Gold Dark**: #B8863D
- **Black**: #1A1A1A
- **White**: #FFFFFF

## Credits

Built for Interstate Waste Technologies - Turning Garbage Into Power
