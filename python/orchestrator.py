import os
import subprocess
import requests
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON_DIR = BASE_DIR / 'python'
JS_DIR = BASE_DIR / 'js'
PHP_ENDPOINT = 'http://localhost:8000/publisher.php'

# 1. Generate product content and image
print('Running product generator...')
gen_proc = subprocess.run([
    'python', str(PYTHON_DIR / 'product_generator.py')
], cwd=PYTHON_DIR, capture_output=True, text=True)
print(gen_proc.stdout)

# 2. Generate mockup visual
print('Running mockup visualizer...')
mockup_proc = subprocess.run([
    'node', str(JS_DIR / 'mockup_visualizer.js')
], cwd=JS_DIR, capture_output=True, text=True)
print(mockup_proc.stdout)

# 3. Collect product data
product_json_path = PYTHON_DIR / 'product.json'
if not product_json_path.exists():
    print('⚠️ product.json not found, creating fallback data...')
    product_data = {
        "title": "AI Generated T-Shirt",
        "description": "A unique AI-generated t-shirt design",
        "tags": ["ai-generated", "creative", "modern"],
        "keywords": ["ai-generated", "creative", "modern", "design", "fashion"]
    }
    with open(product_json_path, 'w') as f:
        json.dump(product_data, f, indent=2)
    print('✅ Created fallback product.json')
else:
    with open(product_json_path, 'r') as f:
        product_data = json.load(f)

# Load mockup data
mockup_json_path = JS_DIR / 'mockup.json'
if mockup_json_path.exists():
    with open(mockup_json_path, 'r') as f:
        mockup_data = json.load(f)
else:
    print('⚠️ mockup.json not found, creating fallback data...')
    mockup_data = {
        "mockup_url": str(JS_DIR / "mockup.png"),
        "width": 2500,
        "height": 2500,
        "product_image": str(PYTHON_DIR / "generated_image.png"),
        "template": str(JS_DIR / "template.png")
    }

# Merge data
product_payload = {
    **product_data,
    'mockup': mockup_data
}

# 4. Publish to PHP endpoint
print('Publishing to PHP endpoint...')
try:
    resp = requests.post(PHP_ENDPOINT, json=product_payload)
    print('Response:', resp.text)
except Exception as e:
    print('Failed to POST to PHP endpoint:', e)

# 5. Save the final payload
samples_dir = BASE_DIR / 'samples'
samples_dir.mkdir(exist_ok=True)
with open(samples_dir / 'final_product_payload.json', 'w') as f:
    json.dump(product_payload, f, indent=2)
print('Pipeline complete. All data saved.') 