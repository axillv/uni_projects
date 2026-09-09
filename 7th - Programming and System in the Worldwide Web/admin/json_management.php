<?php
include '../db_config.php';

header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);
$action = isset($data['action']) ? $data['action'] : null;

if ($action === 'processJson') {
    processJsonData($data['data'], $conn);
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid action']);
}

// Function to process JSON data, map category IDs, and insert new items
function processJsonData($jsonData, $conn) {
    $categories = $jsonData['categories'];
    $items = $jsonData['items'];

    // Arrays to store processed names and map old category IDs to new ones
    $processedCategories = [];
    $categoryIdMap = [];

    // Step 1: Insert categories (checking for duplicates in JSON and DB)
    foreach ($categories as $category) {
        $categoryName = strtolower(trim($category['category_name']));
        $oldCategoryId = $category['id'];

        // Skip categories with empty or null names
        if (empty($categoryName)) {
            continue;
        }

        // Check for duplicates in the database
        if (!categoryExists($categoryName, $conn)) {
            $newCategoryId = insertCategory($categoryName, $conn);
            $categoryIdMap[$oldCategoryId] = $newCategoryId;  // Map old ID to new ID
        } else {
            // Get the existing category ID and map it
            $existingCategoryId = getCategoryID($categoryName, $conn);
            $categoryIdMap[$oldCategoryId] = $existingCategoryId;
        }

        // Add the category name to the processed list
        $processedCategories[] = $categoryName;
    }

    // Step 2: Insert items using the mapped category IDs
    foreach ($items as $item) {
        $itemName = strtolower(trim($item['name']));
        $oldCategoryId = $item['category'];

        // Skip items with empty names or unmapped categories
        if (empty($itemName) || !isset($categoryIdMap[$oldCategoryId])) {
            continue; // Skip this item if name or category mapping is missing
        }

        $newCategoryId = $categoryIdMap[$oldCategoryId];

        // Only take the first detail if there are multiple details
        $detailName = isset($item['details'][0]['detail_name']) ? $item['details'][0]['detail_name'] : ''; 
        $detailValue = isset($item['details'][0]['detail_value']) ? $item['details'][0]['detail_value'] : '';

        // Check for duplicates in the database
        if (!itemExists($itemName, $conn)) {
            $itemId =insertItem($itemName, $newCategoryId, $detailName, $detailValue, $conn);

            // Add 5 of the new item to the Warehouse
            addItemToWarehouse($itemId, 5, $conn);
        }
    }

    echo json_encode(['success' => true, 'message' => 'Data processed successfully']);
}

// Check if the category exists (case-insensitive)
function categoryExists($categoryName, $conn) {
    $query = "SELECT COUNT(*) AS count FROM Category WHERE LOWER(CategoryName) = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('s', $categoryName);
    $stmt->execute();
    $result = $stmt->get_result()->fetch_assoc();
    return $result['count'] > 0;
}

// Get the ID of an existing category
function getCategoryID($categoryName, $conn) {
    $query = "SELECT CategoryID FROM Category WHERE LOWER(CategoryName) = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('s', $categoryName);
    $stmt->execute();
    $result = $stmt->get_result()->fetch_assoc();
    return $result['CategoryID'];
}

// Insert a new category and return the new Category ID
function insertCategory($categoryName, $conn) {
    $query = "INSERT INTO Category (CategoryName) VALUES (?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('s', $categoryName);
    $stmt->execute();
    return $stmt->insert_id;  // Return the new category ID
}

// Check if the item exists (case-insensitive)
function itemExists($itemName, $conn) {
    $query = "SELECT COUNT(*) AS count FROM Items WHERE LOWER(Name) = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('s', $itemName);
    $stmt->execute();
    $result = $stmt->get_result()->fetch_assoc();
    return $result['count'] > 0;
}

// Insert a new item (ignores the id in JSON)
function insertItem($itemName, $categoryId, $detailName, $detailValue, $conn) {
    $query = "INSERT INTO Items (CategoryID, Name, DetailName, DetailValue) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('isss', $categoryId, $itemName, $detailName, $detailValue);
    $stmt->execute();
    return $stmt->insert_id;  // Return the new item ID
}

function addItemToWarehouse($itemId, $quantity, $conn) {
    $query = "INSERT INTO Warehouse (ItemID, Quantity) VALUES (?, ?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('ii', $itemId, $quantity);
    $stmt->execute();
}

$conn->close();
?>
