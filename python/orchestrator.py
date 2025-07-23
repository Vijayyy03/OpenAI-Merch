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
with open(PYTHON_DIR / 'product.json', 'r') as f:
    product_data = json.load(f)
with open(JS_DIR / 'mockup.json', 'r') as f:
    mockup_data = json.load(f)

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
with open(BASE_DIR / 'samples' / 'final_product_payload.json', 'w') as f:
    json.dump(product_payload, f, indent=2)
print('Pipeline complete. All data saved.') 