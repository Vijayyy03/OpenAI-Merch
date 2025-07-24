const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');
const path = require('path');

// Paths
const productImagePath = path.join(__dirname, '../python/generated_image.png');
const templatePath = path.join(__dirname, 'template.png');
const outputMockupPath = path.join(__dirname, 'mockup.png');

async function createMockup() {
  // Load template and product image
  const [template, productImg] = await Promise.all([
    loadImage(templatePath),
    loadImage(productImagePath)
  ]);

  // Create canvas with template size
  const canvas = createCanvas(template.width, template.height);
  const ctx = canvas.getContext('2d');

  // Draw template
  ctx.drawImage(template, 0, 0);

  // Overlay product image (centered, scaled)
  const imgW = template.width * 0.6;
  const imgH = template.height * 0.6;
  const imgX = (template.width - imgW) / 2;
  const imgY = (template.height - imgH) / 2;
  ctx.drawImage(productImg, imgX, imgY, imgW, imgH);

  // Save mockup
  const out = fs.createWriteStream(outputMockupPath);
  const stream = canvas.createPNGStream();
  stream.pipe(out);
  out.on('finish', () => {
    // Output Printful-like JSON
    const mockupJson = {
      mockup_url: outputMockupPath,
      width: template.width,
      height: template.height,
      product_image: productImagePath,
      template: templatePath
    };
    fs.writeFileSync(path.join(__dirname, 'mockup.json'), JSON.stringify(mockupJson, null, 2));
    console.log('Mockup created:', mockupJson);
  });
}

createMockup().catch(err => {
  console.error('Error creating mockup:', err);
}); 