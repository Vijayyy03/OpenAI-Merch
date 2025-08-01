import os
import subprocess
import json
from pathlib import Path
from shopify_integration import ShopifyIntegration

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON_DIR = BASE_DIR / 'python'
JS_DIR = BASE_DIR / 'js'

def run_pipeline_with_shopify():
    """Run the complete pipeline with Shopify integration"""
    
    print("🚀 Starting Merch Maker Lite Pipeline with Shopify Integration")
    print("=" * 60)
    
    # 1. Generate product content and image
    print('\n📝 Step 1: Generating product content and image...')
    gen_proc = subprocess.run([
        'python', str(PYTHON_DIR / 'product_generator.py')
    ], cwd=PYTHON_DIR, capture_output=True, text=True)
    print(gen_proc.stdout)
    
    if gen_proc.returncode != 0:
        print(f"❌ Product generation failed: {gen_proc.stderr}")
        return False
    
    # 2. Generate mockup visual
    print('\n🎨 Step 2: Creating professional mockup...')
    mockup_proc = subprocess.run([
        'node', str(JS_DIR / 'mockup_visualizer.js')
    ], cwd=JS_DIR, capture_output=True, text=True)
    print(mockup_proc.stdout)
    
    if mockup_proc.returncode != 0:
        print(f"❌ Mockup generation failed: {mockup_proc.stderr}")
        return False
    
    # 3. Collect product data
    print('\n📊 Step 3: Collecting product data...')
    try:
        with open(PYTHON_DIR / 'product.json', 'r') as f:
            product_data = json.load(f)
        with open(JS_DIR / 'mockup.json', 'r') as f:
            mockup_data = json.load(f)
        
        # Merge data
        product_payload = {
            **product_data,
            'mockup': mockup_data
        }
        
        print(f"✅ Product data collected: {product_data.get('title', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Failed to collect product data: {e}")
        return False
    
    # 4. Upload to Shopify
    print('\n🛍️ Step 4: Uploading to Shopify...')
    try:
        shopify = ShopifyIntegration()
        
        # Get mockup path
        mockup_path = JS_DIR / 'mockup.png'
        
        # Create product in Shopify
        shopify_product = shopify.create_product(product_data, str(mockup_path))
        
        if shopify_product:
            print(f"✅ Product uploaded to Shopify successfully!")
            print(f"   Product ID: {shopify_product.get('id')}")
            print(f"   Title: {shopify_product.get('title')}")
            print(f"   Status: {shopify_product.get('status')}")
            
            # Optionally publish the product
            publish_choice = input("\n🤔 Would you like to publish this product? (y/n): ").lower()
            if publish_choice == 'y':
                if shopify.publish_product(shopify_product['id']):
                    print("✅ Product published and now live on Shopify!")
                else:
                    print("⚠️ Product created but not published (still in draft mode)")
            
            # Save the final payload with Shopify info
            final_payload = {
                **product_payload,
                'shopify': {
                    'product_id': shopify_product.get('id'),
                    'status': shopify_product.get('status'),
                    'admin_url': f"https://{shopify.shop_url}/admin/products/{shopify_product.get('id')}"
                }
            }
            
            # Save to samples directory
            with open(BASE_DIR / 'samples' / 'shopify_product_payload.json', 'w') as f:
                json.dump(final_payload, f, indent=2)
            
            print(f"\n📁 Final payload saved to: samples/shopify_product_payload.json")
            print(f"🔗 View product in Shopify admin: {final_payload['shopify']['admin_url']}")
            
            return True
        else:
            print("❌ Failed to upload product to Shopify")
            return False
            
    except Exception as e:
        print(f"❌ Shopify integration failed: {e}")
        return False

def test_shopify_connection():
    """Test the Shopify connection before running the pipeline"""
    print("🔍 Testing Shopify connection...")
    try:
        shopify = ShopifyIntegration()
        products = shopify.get_products(limit=1)
        print(f"✅ Shopify connection successful!")
        print(f"   Store: {shopify.shop_url}")
        print(f"   Products found: {len(products)}")
        return True
    except Exception as e:
        print(f"❌ Shopify connection failed: {e}")
        print("\n📋 Please ensure you have set up your .env file with:")
        print("   SHOPIFY_SHOP_URL=your-store.myshopify.com")
        print("   SHOPIFY_ACCESS_TOKEN=your-access-token")
        return False

if __name__ == "__main__":
    print("Merch Maker Lite - Shopify Integration")
    print("=" * 40)
    
    # Test connection first
    if test_shopify_connection():
        print("\n🚀 Starting pipeline...")
        success = run_pipeline_with_shopify()
        
        if success:
            print("\n🎉 Pipeline completed successfully!")
            print("Your AI-generated product is now live on Shopify!")
        else:
            print("\n❌ Pipeline failed. Please check the errors above.")
    else:
        print("\n❌ Cannot proceed without Shopify connection.")
        print("Please set up your Shopify credentials and try again.") 