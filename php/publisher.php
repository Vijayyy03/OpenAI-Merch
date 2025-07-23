<?php
header('Content-Type: application/json');

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Only POST requests allowed']);
    exit;
}

// Get the raw POST data
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit;
}

// Log/display the received data
file_put_contents('received_product.json', json_encode($data, JSON_PRETTY_PRINT));
echo "Received product data:\n";
print_r($data);

// Return a fake product ID
$response = [
    'status' => 'success',
    'product_id' => uniqid('prod_'),
];
echo json_encode($response); 