#!/usr/bin/env python3
"""
Merch Maker Lite - One Command Runner
=====================================

This script provides a simple way to run the entire project with one command.
It automatically detects your setup and runs the appropriate mode.

Usage:
    python run_project.py                    # Auto-detect best mode
    python run_project.py --shopify         # Force Shopify mode
    python run_project.py --simulation      # Force simulation mode
    python run_project.py --demo            # Force demo mode
    python run_project.py --help            # Show help
"""

import os
import sys
import subprocess
from pathlib import Path

def check_shopify_credentials():
    """Check if Shopify credentials are properly configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        shop_url = os.getenv('SHOPIFY_SHOP_URL')
        access_token = os.getenv('SHOPIFY_ACCESS_TOKEN')
        
        if shop_url and access_token and not shop_url.startswith('your-'):
            return True
        return False
    except:
        return False

def check_openai_credentials():
    """Check if OpenAI credentials are properly configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and not api_key.startswith('your-'):
            return True
        return False
    except:
        return False

def run_shopify_demo():
    """Run the Shopify integration demo"""
    print("🚀 Running Shopify Integration Demo...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, 'demo_shopify.py'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Shopify demo completed successfully!")
            return True
        else:
            print("❌ Shopify demo failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running Shopify demo: {e}")
        return False

def run_simulation():
    """Run the simulation mode"""
    print("🎭 Running Simulation Mode...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, 'orchestrator.py'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Simulation completed successfully!")
            return True
        else:
            print("❌ Simulation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running simulation: {e}")
        return False

def run_full_pipeline():
    """Run the full Shopify pipeline"""
    print("🔄 Running Full Shopify Pipeline...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, 'orchestrator_shopify.py'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Full pipeline completed successfully!")
            return True
        else:
            print("❌ Full pipeline failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running full pipeline: {e}")
        return False

def show_help():
    """Show help information"""
    print("""
🎯 Merch Maker Lite - One Command Runner
========================================

This script automatically detects your setup and runs the best available mode.

Available Modes:
1. Shopify Demo (Recommended) - Interactive demo with real Shopify integration
2. Full Pipeline - Complete AI-to-Shopify workflow
3. Simulation - Offline demo with fallback data

Usage:
    python run_project.py                    # Auto-detect best mode
    python run_project.py --shopify         # Force Shopify mode
    python run_project.py --simulation      # Force simulation mode
    python run_project.py --demo            # Force demo mode
    python run_project.py --help            # Show this help

Requirements:
- Shopify Demo: Requires Shopify credentials in .env file
- Full Pipeline: Requires both OpenAI and Shopify credentials
- Simulation: No credentials required (works offline)

For setup instructions, see:
- SHOPIFY_SETUP.md - Detailed Shopify setup guide
- README.md - Project overview
""")

def main():
    """Main function to run the project"""
    print("🎯 Merch Maker Lite - One Command Runner")
    print("=" * 50)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode in ['--help', '-h', 'help']:
            show_help()
            return
        
        elif mode in ['--shopify', '-s']:
            if check_shopify_credentials():
                run_shopify_demo()
            else:
                print("❌ Shopify credentials not found. Please set up your .env file.")
                print("📖 See SHOPIFY_SETUP.md for instructions.")
            return
        
        elif mode in ['--simulation', '--sim', '-sim']:
            run_simulation()
            return
        
        elif mode in ['--demo', '-d']:
            run_shopify_demo()
            return
        
        else:
            print(f"❌ Unknown mode: {mode}")
            show_help()
            return
    
    # Auto-detect best mode
    print("🔍 Auto-detecting best mode...")
    
    has_shopify = check_shopify_credentials()
    has_openai = check_openai_credentials()
    
    print(f"📊 Setup Status:")
    print(f"   Shopify Integration: {'✅ Ready' if has_shopify else '❌ Not configured'}")
    print(f"   OpenAI Integration: {'✅ Ready' if has_openai else '❌ Not configured'}")
    print()
    
    # Determine best mode
    if has_shopify:
        print("🎯 Recommended: Shopify Demo Mode")
        print("   This will create a real product in your Shopify store!")
        print()
        
        choice = input("🤔 Run Shopify demo? (y/n): ").lower()
        if choice in ['y', 'yes', '']:
            run_shopify_demo()
        else:
            print("👋 Demo cancelled.")
    
    elif has_openai:
        print("🎯 Available: Full Pipeline Mode")
        print("   This will use AI to generate products and upload to Shopify.")
        print()
        
        choice = input("🤔 Run full pipeline? (y/n): ").lower()
        if choice in ['y', 'yes', '']:
            run_full_pipeline()
        else:
            print("👋 Pipeline cancelled.")
    
    else:
        print("🎯 Available: Simulation Mode")
        print("   This will run offline with fallback data.")
        print()
        
        choice = input("🤔 Run simulation? (y/n): ").lower()
        if choice in ['y', 'yes', '']:
            run_simulation()
        else:
            print("👋 Simulation cancelled.")
    
    print()
    print("📖 For setup help:")
    print("   - SHOPIFY_SETUP.md - Detailed setup guide")
    print("   - README.md - Project overview")

if __name__ == "__main__":
    main() 