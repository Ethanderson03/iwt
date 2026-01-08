/**
 * IWT Image Generator using Google Gemini API (Nano Banana)
 *
 * Setup:
 * 1. Get an API key from https://aistudio.google.com/apikey
 * 2. Run: npm install @google/generative-ai
 * 3. Set your API key: export GEMINI_API_KEY="your-key-here"
 * 4. Run: node generate-images.js
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const API_KEY = process.env.GEMINI_API_KEY;
const MODEL = 'gemini-2.0-flash-exp'; // Nano Banana model

if (!API_KEY) {
    console.error('Error: GEMINI_API_KEY environment variable not set');
    console.log('Get your API key from: https://aistudio.google.com/apikey');
    console.log('Then run: export GEMINI_API_KEY="your-key-here"');
    process.exit(1);
}

// Create images directory
const imagesDir = path.join(__dirname, 'images');
if (!fs.existsSync(imagesDir)) {
    fs.mkdirSync(imagesDir);
}

// Style guide for consistent isometric flat-color images
const styleGuide = `
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
`;

// Image prompts matching the PDF style
const imagePrompts = [
    {
        name: 'hero-plant',
        prompt: `An isometric view of a modern waste-to-energy gasification plant facility. The building has industrial smokestacks, large cylindrical tanks, and processing equipment. Clean and professional appearance with warm tan/gold accents on the building. ${styleGuide}`,
        aspectRatio: '16:9'
    },
    {
        name: 'modular-plant-1',
        prompt: `An isometric view of a modular industrial waste processing facility with multiple smokestacks, conveyor systems, and a main processing building. The design is modern with flat tan/brown roofing and industrial gray equipment. Clean lines and professional aesthetic. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'modular-plant-2',
        prompt: `An isometric view of a modular gasification unit with large cylindrical pressure vessels in pink/salmon color, metal piping, and supporting steel structure. Industrial equipment module for a waste-to-energy plant. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'modular-plant-3',
        prompt: `An isometric view of an industrial gas processing module with multiple spherical tanks, a tall cylindrical column, and metal framework. The tanks are in muted pink/beige colors with industrial gray piping. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'pipeline-milwaukee',
        prompt: `An aerial isometric view of a modern waste-to-energy facility campus with multiple buildings, large cylindrical storage tanks, green landscaping, and a parking area. Set in a green countryside. Professional industrial facility. ${styleGuide}`,
        aspectRatio: '4:3'
    },
    {
        name: 'pipeline-virginia',
        prompt: `An aerial isometric view of a medium-scale waste processing plant with large dome-shaped biogas digesters, modern industrial buildings, and solar panels on the roof. Clean facility design. ${styleGuide}`,
        aspectRatio: '4:3'
    },
    {
        name: 'pipeline-louisiana',
        prompt: `An aerial isometric view of a large industrial petrochemical integration facility with tall processing towers, multiple storage tanks, and steel framework structures. Modern waste-to-energy plant. ${styleGuide}`,
        aspectRatio: '4:3'
    },
    {
        name: 'product-jet-fuel',
        prompt: `An isometric view of a metal fuel barrel/drum for jet fuel with a diamond hazard warning label. Industrial steel container with silver metallic finish. Simple clean design. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'product-ethanol',
        prompt: `An isometric view of a glass laboratory bottle containing clear liquid ethanol with a black cap. The bottle has a simple label. Clean laboratory/scientific aesthetic. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'product-meg',
        prompt: `An isometric view of a blue industrial chemical barrel/drum for storing monoethylene glycol. Large 55-gallon drum with blue finish. Industrial container design. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'product-pet',
        prompt: `An isometric view of colorful PET plastic bottles - one red, one green, one orange, and a white container. Representing polyethylene terephthalate products. Consumer plastic bottles. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'data-center',
        prompt: `An isometric view of a modern AI data center building with rows of server racks visible through glass walls, cooling units on the roof, and clean geometric architecture. Blue accent lighting. ${styleGuide}`,
        aspectRatio: '16:9'
    },
    {
        name: 'garbage-truck',
        prompt: `An isometric view of a modern garbage collection truck in green or tan color, with a compactor body. Clean municipal waste collection vehicle design. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'syngas-flame',
        prompt: `An isometric view of a clean-burning natural gas flame emerging from an industrial burner or furnace opening. Blue and orange flame with industrial metal housing. ${styleGuide}`,
        aspectRatio: '1:1'
    },
    {
        name: 'japan-map',
        prompt: `An isometric stylized map of Japan with 7 location markers/pins distributed across the country. The map is in a warm tan/beige color with the markers in gold. Minimal design. ${styleGuide}`,
        aspectRatio: '4:3'
    }
];

async function generateImage(prompt, aspectRatio = '1:1') {
    const requestBody = {
        contents: [{
            parts: [{
                text: prompt
            }]
        }],
        generationConfig: {
            responseModalities: ['TEXT', 'IMAGE'],
            candidateCount: 1
        }
    };

    const options = {
        hostname: 'generativelanguage.googleapis.com',
        path: `/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const response = JSON.parse(data);
                    if (response.error) {
                        reject(new Error(response.error.message));
                        return;
                    }

                    // Extract image data from response
                    const candidates = response.candidates || [];
                    for (const candidate of candidates) {
                        const parts = candidate.content?.parts || [];
                        for (const part of parts) {
                            if (part.inlineData) {
                                resolve({
                                    mimeType: part.inlineData.mimeType,
                                    data: part.inlineData.data
                                });
                                return;
                            }
                        }
                    }
                    reject(new Error('No image in response'));
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', reject);
        req.write(JSON.stringify(requestBody));
        req.end();
    });
}

async function saveImage(name, imageData) {
    const extension = imageData.mimeType.includes('png') ? 'png' : 'jpg';
    const filename = path.join(imagesDir, `${name}.${extension}`);
    const buffer = Buffer.from(imageData.data, 'base64');
    fs.writeFileSync(filename, buffer);
    console.log(`Saved: ${filename}`);
    return filename;
}

async function generateAllImages() {
    console.log('Starting IWT image generation...\n');
    console.log(`Generating ${imagePrompts.length} images in isometric flat-color style\n`);

    for (const img of imagePrompts) {
        console.log(`Generating: ${img.name}...`);
        try {
            const imageData = await generateImage(img.prompt, img.aspectRatio);
            await saveImage(img.name, imageData);
            // Rate limiting - wait 2 seconds between requests
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (error) {
            console.error(`Failed to generate ${img.name}: ${error.message}`);
        }
    }

    console.log('\nImage generation complete!');
    console.log(`Images saved to: ${imagesDir}`);
}

// Run if called directly
if (require.main === module) {
    generateAllImages().catch(console.error);
}

module.exports = { generateImage, imagePrompts };
