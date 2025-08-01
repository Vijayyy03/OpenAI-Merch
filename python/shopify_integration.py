import os
import requests
import json
import base64
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables with error handling
try:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Using default placeholder values")

class ShopifyIntegration:
    def __init__(self):
        # Use environment variables for credentials
        self.shop_url = os.getenv('SHOPIFY_SHOP_URL', 'your-store.myshopify.com')
        self.access_token = os.getenv('SHOPIFY_ACCESS_TOKEN', 'your-access-token')
        self.api_version = '2024-01'  # Latest stable version
        
        if not self.shop_url or not self.access_token or self.shop_url == 'your-store.myshopify.com':
            raise ValueError("SHOPIFY_SHOP_URL and SHOPIFY_ACCESS_TOKEN must be set in .env file")
        
        # Remove https:// and trailing slash if present
        self.shop_url = self.shop_url.replace('https://', '').replace('http://', '').rstrip('/')
        self.base_url = f"https://{self.shop_url}/admin/api/{self.api_version}"
        
        self.headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.access_token
        }
    
    def upload_image_to_shopify(self, image_path, alt_text="Product Image"):
        """Upload an image to Shopify and return the image ID"""
        try:
            # Read and encode the image
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare the image data
            image_payload = {
                "image": {
                    "attachment": image_data,
                    "filename": Path(image_path).name,
                    "alt": alt_text
                }
            }
            
            # Upload image to Shopify
            response = requests.post(
                f"{self.base_url}/images.json",
                headers=self.headers,
                json=image_payload
            )
            
            if response.status_code == 201:
                image_data = response.json()
                return image_data['image']['id']
            else:
                print(f"Failed to upload image: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None
    
    def create_product(self, product_data, mockup_path=None):
        """Create a product in Shopify"""
        try:
            # Prepare product payload
            product_payload = {
                "product": {
                    "title": product_data.get('title', 'AI Generated T-Shirt'),
                    "body_html": product_data.get('description', 'AI-generated t-shirt design'),
                    "vendor": "AI Merch Maker",
                    "product_type": "T-Shirt",
                    "tags": ", ".join(product_data.get('tags', [])),
                    "status": "draft",  # Start as draft for safety
                    "variants": [
                        {
                            "option1": "Default Title",
                            "price": "19.99",
                            "compare_at_price": "24.99",
                            "inventory_quantity": 100,
                            "inventory_management": "shopify"
                        }
                    ],
                    "options": [
                        {
                            "name": "Title",
                            "values": ["Default Title"]
                        }
                    ]
                }
            }
            
            # Create the product
            response = requests.post(
                f"{self.base_url}/products.json",
                headers=self.headers,
                json=product_payload
            )
            
            if response.status_code == 201:
                product_info = response.json()
                product_id = product_info['product']['id']
                print(f"✅ Product created successfully! ID: {product_id}")
                
                # Upload mockup image if provided
                if mockup_path and os.path.exists(mockup_path):
                    print("📸 Uploading mockup image...")
                    image_id = self.upload_image_to_shopify(mockup_path, f"Mockup for {product_data.get('title')}")
                    if image_id:
                        print(f"✅ Image uploaded successfully! Image ID: {image_id}")
                
                return product_info['product']
            else:
                print(f"❌ Failed to create product: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating product: {e}")
            return None
    
    def get_products(self, limit=10):
        """Get list of products from Shopify"""
        try:
            response = requests.get(
                f"{self.base_url}/products.json?limit={limit}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()['products']
            else:
                print(f"Failed to get products: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def publish_product(self, product_id):
        """Publish a product (change status from draft to active)"""
        try:
            product_payload = {
                "product": {
                    "id": product_id,
                    "status": "active"
                }
            }
            
            response = requests.put(
                f"{self.base_url}/products/{product_id}.json",
                headers=self.headers,
                json=product_payload
            )
            
            if response.status_code == 200:
                print(f"✅ Product {product_id} published successfully!")
                return True
            else:
                print(f"❌ Failed to publish product: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error publishing product: {e}")
            return False

def test_shopify_connection():
    """Test the Shopify connection"""
    try:
        shopify = ShopifyIntegration()
        products = shopify.get_products(limit=1)
        print(f"✅ Shopify connection successful! Found {len(products)} products.")
        return True
    except Exception as e:
        print(f"❌ Shopify connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the integration
    if test_shopify_connection():
        print("Shopify integration is working correctly!")
    else:
        print("Please check your Shopify credentials in the .env file") 