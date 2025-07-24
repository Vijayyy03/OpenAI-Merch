import os
import openai
from dotenv import load_dotenv
import requests
import shutil

# Load environment variables from .env file in the same directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# --- MOCKING FOR TESTING WITHOUT API KEY ---
if os.getenv("MOCK_OPENAI", "0") == "1":
    from unittest.mock import MagicMock
    # Mock chat completion
    openai.chat = MagicMock()
    openai.chat.completions.create = MagicMock(return_value=type("obj", (object,), {
        "choices": [type("obj", (object,), {"message": type("obj", (object,), {"content": '{"title": "Test Shirt", "description": "A test shirt", "tags": ["test", "shirt"]}'})})]
    })())
    # Mock image generation
    openai.images = MagicMock()
    openai.images.generate = MagicMock(return_value=type("obj", (object,), {
        "data": [type("obj", (object,), {"url": "https://example.com/fake-image.png"})]
    })())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# --- Product Content Generation ---
def generate_product_content():
    prompt = (
        "Generate a creative product idea for a t-shirt. "
        "Return a JSON with: title, description, and 5-10 tags."
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.9,
    )
    content = response.choices[0].message.content
    return content

# --- Product Image Generation ---
def generate_product_image(prompt, output_path="generated_image.png"):
    if os.getenv("MOCK_OPENAI", "0") == "1":
        # In mock mode, copy dummy.png as the generated image
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "dummy.png"), output_path)
        return output_path
    dalle_response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = dalle_response.data[0].url
    img_data = requests.get(image_url).content
    with open(output_path, 'wb') as handler:
        handler.write(img_data)
    return output_path

if __name__ == "__main__":
    print("Generating product content...")
    product_json = generate_product_content()
    print(product_json)
    # Extract title for image prompt (simple approach)
    import json
    try:
        product = json.loads(product_json)
        image_prompt = f"A high-quality product image for: {product['title']}"
    except Exception:
        image_prompt = "A creative t-shirt design"
    print("Generating product image...")
    image_path = generate_product_image(image_prompt)
    print(f"Image saved to {image_path}")
    # Save product JSON
    with open("product.json", "w") as f:
        f.write(product_json)
    print("Product data and image generated.") 