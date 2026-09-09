<?php
// Include your database connection script here
include '../db_config.php'; // Make sure this script connects to your database

header('Content-Type: application/json');

// Get the incoming JSON data
$data = json_decode(file_get_contents('php://input'), true);

// Extract admin ID and items array
$adminID = $data['adminID'];
$items = $data['items']; // This is an array of items with 'name' and 'quantity'

// Prepare comma-separated strings for item names and quantities
$itemNames = [];
$quantities = [];

foreach ($items as $item) {
    $itemNames[] = $item['name']; // Assuming 'name' holds the item name
    $quantities[] = $item['quantity']; // Assuming 'quantity' holds the quantity
}

// Convert arrays to comma-separated strings
$itemNamesString = implode(',', $itemNames);
$quantitiesString = implode(',', $quantities);

try {
    // Prepare the SQL statement to call the stored procedure
    $stmt = $conn->prepare("CALL CreateNewAnnouncement(?, ?, ?)");
    $stmt->bind_param("iss", $adminID, $itemNamesString, $quantitiesString);

    // Execute the statement
    if ($stmt->execute()) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Database error']);
    }

    // Close the statement and connection
    $stmt->close();
    $conn->close();
} catch (Exception $e) {
    // Handle exceptions and return an error message
    echo json_encode(['success' => false, 'message' => $e->getMessage()]);
}
?>
