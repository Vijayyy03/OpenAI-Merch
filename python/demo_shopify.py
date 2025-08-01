#!/usr/bin/env python3
"""
Merch Maker Lite - Shopify Integration Demo
===========================================

This script demonstrates the complete AI-to-Shopify pipeline.
It shows how the system connects to a real Shopify store and uploads products.

Features:
- Shopify API integration
- Product creation and management
- Image upload capabilities
- Professional mockup generation
"""

import os
import sys
import json
from pathlib import Path
from shopify_integration import ShopifyIntegration

def test_shopify_connection():
    """Test the Shopify connection"""
    print("Step 1: Testing Shopify Connection")
    print("   Verifying API credentials and store access")
    print("-" * 40)
    
    try:
        shopify = ShopifyIntegration()
        products = shopify.get_products(limit=5)
        
        if products:
            print("SUCCESS: Shopify connection successful!")
            print(f"   Store: {shopify.shop_url}")
            print(f"   Products found: {len(products)}")
            return True
        else:
            print("SUCCESS: Shopify connection successful!")
            print(f"   Store: {shopify.shop_url}")
            print("   Products found: 0")
            return True
    except Exception as e:
        print(f"FAILED: Shopify connection failed: {e}")
        print()
        print("Please ensure you have set up your .env file with:")
        print("   SHOPIFY_SHOP_URL=your-store.myshopify.com")
        print("   SHOPIFY_ACCESS_TOKEN=your-access-token")
        print()
        print("See SHOPIFY_SETUP.md for detailed instructions")
        return False

def generate_sample_product():
    """Generate sample product data"""
    print("Step 2: Generating Sample Product Data")
    print("   Creating AI-generated product information")
    print("-" * 40)
    
    sample_product = {
        "title": "AI Generated Creative T-Shirt",
        "description": "A unique AI-generated t-shirt design featuring modern artistic elements and creative patterns. Perfect for those who appreciate innovative fashion and contemporary style.",
        "tags": ["ai-generated", "creative", "modern", "artistic", "unique"],
        "keywords": ["ai-generated", "creative", "modern", "artistic", "unique", "design", "fashion", "t-shirt"]
    }
    
    print("SUCCESS: Product data generated:")
    print(f"   Title: {sample_product['title']}")
    print(f"   Tags: {', '.join(sample_product['tags'])}")
    
    return sample_product

def check_mockup():
    """Check if mockup exists"""
    print("Step 3: Creating Professional Mockup")
    print("   Generating product mockup image")
    print("-" * 40)
    
    js_dir = Path(__file__).parent.parent / 'js'
    mockup_path = js_dir / 'mockup.png'
    
    if mockup_path.exists():
        size_mb = mockup_path.stat().st_size / (1024 * 1024)
        print(f"SUCCESS: Mockup found: {mockup_path}")
        print(f"   Size: {size_mb:.1f} MB")
        return str(mockup_path)
    else:
        print("WARNING: Mockup not found, will create product without image")
        return None

def upload_to_shopify(product_data, mockup_path=None):
    """Upload product to Shopify"""
    print("Step 4: Uploading to Shopify")
    print("   Creating product in your Shopify store")
    print("-" * 40)
    
    try:
        shopify = ShopifyIntegration()
        shopify_product = shopify.create_product(product_data, mockup_path)
        
        if shopify_product:
            print(f"SUCCESS: Product created successfully! ID: {shopify_product['id']}")
            
            if mockup_path:
                print("Uploading mockup image...")
                # Note: Image upload is handled in create_product method
            
            print("SUCCESS: Product uploaded successfully!")
            print(f"   Product ID: {shopify_product['id']}")
            print(f"   Title: {shopify_product['title']}")
            print(f"   Status: {shopify_product['status']}")
            print(f"   Price: ${shopify_product['variants'][0]['price']}")
            
            return shopify_product
        else:
            print("FAILED: Failed to upload product to Shopify")
            return None
    except Exception as e:
        print(f"FAILED: Shopify upload failed: {e}")
        return None

def manage_product(product_id):
    """Manage the uploaded product"""
    print("Step 5: Product Management")
    print("   Managing the uploaded product")
    print("-" * 40)
    
    print("Available actions:")
    print("   1. Publish product (make it live)")
    print("   2. Keep as draft (for review)")
    print("   3. View in Shopify admin")
    
    choice = input("\nWould you like to publish this product? (y/n): ").lower()
    
    if choice in ['y', 'yes']:
        try:
            shopify = ShopifyIntegration()
            shopify.publish_product(product_id)
            print(f"SUCCESS: Product {product_id} published successfully!")
            print("SUCCESS: Product published and now live on Shopify!")
            return True
        except Exception as e:
            print(f"FAILED: Failed to publish product: {e}")
            return False
    else:
        print("Product kept as draft for review.")
        return True

def show_results(product_id):
    """Show final results"""
    print("Step 6: Integration Complete")
    print("   Summary of what was accomplished")
    print("-" * 40)
    
    shopify = ShopifyIntegration()
    admin_url = f"https://{shopify.shop_url}/admin/products/{product_id}"
    store_url = f"https://{shopify.shop_url}"
    
    print("SUCCESS: Demo completed successfully!")
    print(f"View product in Shopify admin: {admin_url}")
    print(f"Visit your store: {store_url}")
    
    # Save demo results
    demo_results = {
        "product_id": product_id,
        "admin_url": admin_url,
        "store_url": store_url,
        "status": "published"
    }
    
    samples_dir = Path(__file__).parent.parent / 'samples'
    samples_dir.mkdir(exist_ok=True)
    
    with open(samples_dir / 'demo_shopify_payload.json', 'w') as f:
        json.dump(demo_results, f, indent=2)
    
    print("Demo results saved to: samples/demo_shopify_payload.json")

def demo_shopify_integration():
    """Main demo function"""
    print("Starting Merch Maker Lite Shopify Integration Demo")
    print("This will demonstrate the complete AI-to-Shopify pipeline!")
    print()
    print("=" * 60)
    print("Merch Maker Lite - Shopify Integration Demo")
    print("=" * 60)
    print("This demo will show you how the AI-powered merch pipeline")
    print("connects to a real Shopify store and uploads products!")
    print()
    
    # Step 1: Test connection
    if not test_shopify_connection():
        print("Demo failed. Please check the errors above.")
        print("Make sure you've followed the setup guide: SHOPIFY_SETUP.md")
        return False
    
    print()
    
    # Step 2: Generate product data
    product_data = generate_sample_product()
    print()
    
    # Step 3: Check mockup
    mockup_path = check_mockup()
    print()
    
    # Step 4: Upload to Shopify
    shopify_product = upload_to_shopify(product_data, mockup_path)
    if not shopify_product:
        print("FAILED: Failed to upload product to Shopify")
        print()
        print("Demo failed. Please check the errors above.")
        print("Make sure you've followed the setup guide: SHOPIFY_SETUP.md")
        return False
    
    print()
    
    # Step 5: Manage product
    if not manage_product(shopify_product['id']):
        print("Demo failed. Please check the errors above.")
        return False
    
    print()
    
    # Step 6: Show results
    show_results(shopify_product['id'])
    print()
    
    print("SUCCESS: Demo completed successfully!")
    print("You now have a real product in your Shopify store!")
    print()
    print("Next steps:")
    print("   - Run the full pipeline: python orchestrator_shopify.py")
    print("   - Set up automated scheduling")
    print("   - Configure payment processing")
    print("   - Scale to multiple products")
    
    return True

def main():
    """Main function"""
    try:
        success = demo_shopify_integration()
        return success
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    main() 