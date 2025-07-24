# OpenAI-Merch

## Overview
OpenAI-Merch is an automated backend pipeline that generates and publishes AI-created product listings using multiple APIs and programming languages. The pipeline simulates a mini eCommerce product automation system, generating product ideas, images, mockups, and publishing them via a fake API endpoint.

**Languages Used:**
- Python (AI, automation)
- JavaScript (Node.js, mockup generation)
- PHP (Fake publishing endpoint)

## Project Structure
```
Ecom/
├── python/
│   ├── product_generator.py
│   ├── orchestrator.py
│   ├── requirements.txt
│   └── generated files (product.json, generated_image.png)
├── js/
│   ├── mockup_visualizer.js
│   ├── package.json
│   ├── template.png
│   └── generated files (mockup.png, mockup.json)
├── php/
│   └── publisher.php
├── samples/
│   └── final_product_payload.json
└── README.md
```

## Setup Instructions

### 1. Python (Product Generator & Orchestrator)
- Navigate to `python/` directory.
- Create a virtual environment and install dependencies:
  ```
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```
- Add your OpenAI API key to a `.env` file:
  ```
  OPENAI_API_KEY=your-openai-api-key-here
  ```

### 2. JavaScript (Mockup Visualizer)
- Navigate to `js/` directory.
- Install dependencies:
  ```
  npm install
  ```
- Add a PNG mockup template as `template.png` in the `js/` directory.

### 3. PHP (Fake Product Publisher)
- Navigate to `php/` directory.
- Start the PHP server:
  ```
  php -S localhost:8000
  ```

## Running the Full Pipeline
1. Ensure the PHP server is running (`php -S localhost:8000` in `php/`).
2. Activate the Python virtual environment (`venv\Scripts\activate` in `python/`).
3. Run the orchestrator script:
   ```
   python orchestrator.py
   ```
4. The pipeline will:
   - Generate product content and image (Python)
   - Create a mockup (Node.js)
   - Publish to the PHP endpoint
   - Save the final payload in `samples/final_product_payload.json`

## Sample Outputs
- `python/generated_image.png`: AI-generated product image
- `python/product.json`: Product data (title, description, tags, keywords)
- `js/mockup.png`: Product mockup image
- `js/mockup.json`: Mockup metadata
- `samples/final_product_payload.json`: Final merged product data

## Notes
- The PHP endpoint is for demonstration only and does not persist data.
- For the mockup, use any transparent PNG as a template (e.g., t-shirt mockup).
- The orchestrator can be scheduled for automation.

---

**Enjoy automating your AI-powered merch pipeline!**
