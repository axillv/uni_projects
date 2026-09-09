<?php
include '../db_config.php';

header('Content-Type: application/json');

$action = isset($_POST['action']) ? $_POST['action'] : null;

switch ($action) {
    case 'fetchCategories':
        fetchCategories($conn);
        break;
    case 'fetchItems':
        fetchItems($conn);
        break;
    case 'fetchItemDetails':
        fetchItemDetails($conn);
        break;
    case 'createCategory':
        createCategory($conn);
        break;
    case 'createItem':
        createItem($conn);
        break;
    case 'updateItemDetails':
        updateItemDetails($conn);
        break;
    case 'deleteCategory':  // Add deleteCategory action
        deleteCategory($conn);
        break;
    case 'deleteItem':  // Add deleteItem action
        deleteItem($conn);
        break;
    default:
        echo json_encode(['success' => false, 'message' => 'Invalid action']);
}

// Fetch all categories
function fetchCategories($conn) {
    $query = "SELECT CategoryID, CategoryName FROM Category";
    $result = $conn->query($query);
    if ($result) {
        $categories = [];
        while ($row = $result->fetch_assoc()) {
            $categories[] = $row;
        }
        echo json_encode($categories);
    } else {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
    }
}

// Fetch items for a selected category
function fetchItems($conn) {
    $categoryId = $_POST['categoryId'];
    $query = "SELECT ItemID, Name FROM Items WHERE CategoryID = ?";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
        return;
    }
    $stmt->bind_param("i", $categoryId);
    $stmt->execute();
    $result = $stmt->get_result();
    if ($result) {
        $items = [];
        while ($row = $result->fetch_assoc()) {
            $items[] = $row;
        }
        echo json_encode($items);
    } else {
        echo json_encode(['success' => false, 'message' => $stmt->error]); // Send DB error message
    }
}

// Fetch item details
function fetchItemDetails($conn) {
    $itemId = $_POST['itemId'];
    $query = "SELECT i.DetailName, i.DetailValue, w.Quantity FROM Items i LEFT JOIN Warehouse w ON i.ItemID = w.ItemID WHERE i.ItemID = ?";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
        return;
    }
    $stmt->bind_param("i", $itemId);
    $stmt->execute();
    $result = $stmt->get_result();
    if ($result) {
        $itemDetails = $result->fetch_assoc();
        echo json_encode($itemDetails);
    } else {
        echo json_encode(['success' => false, 'message' => $stmt->error]); // Send DB error message
    }
}

// Create a new category
function createCategory($conn) {
    $categoryName = $_POST['categoryName'];
    $query = "INSERT INTO Category (CategoryName) VALUES (?)";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
        return;
    }
    $stmt->bind_param("s", $categoryName);
    $success = $stmt->execute();
    if ($success) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => $stmt->error]); // Send DB error message
    }
}

// Create a new item
function createItem($conn) {
    $categoryId = $_POST['categoryId'];
    $itemName = $_POST['itemName'];
    $detailName = $_POST['detailName'];
    $detailValue = $_POST['detailValue'];
    $quantity = $_POST['quantity'];

    if (!is_numeric($quantity) || $quantity <= 0) {
        echo json_encode(['success' => false, 'message' => 'Invalid quantity. Please enter a positive number.']);
        return;
    }

    $query = "INSERT INTO Items (CategoryID, Name, DetailName, DetailValue) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
        return;
    }
    $stmt->bind_param("isss", $categoryId, $itemName, $detailName, $detailValue);
    $success = $stmt->execute();
    if ($success) {
        $itemId = $stmt->insert_id;
        $warehouseQuery = "INSERT INTO Warehouse (ItemID, Quantity) VALUES (?, ?)";
        $warehouseStmt = $conn->prepare($warehouseQuery);
        $warehouseStmt->bind_param("ii", $itemId, $quantity);
        $warehouseStmt->execute();
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => $stmt->error]); // Send DB error message
    }
}

// Update item details
// Update item details
function updateItemDetails($conn) {
    $itemId = $_POST['itemId'];
    $detailName = $_POST['detailName'];
    $detailValue = $_POST['detailValue'];
    $quantity = $_POST['quantity'];

    if (!is_numeric($quantity) || $quantity <= 0) {
        echo json_encode(['success' => false, 'message' => 'Invalid quantity. Please enter a positive number.']);
        return;
    }

    // Update the Items table
    $query = "UPDATE Items SET DetailName = ?, DetailValue = ? WHERE ItemID = ?";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
        return;
    }
    $stmt->bind_param("ssi", $detailName, $detailValue, $itemId);
    $successItems = $stmt->execute();

    // Check if item exists in the Warehouse table
    $checkWarehouseQuery = "SELECT * FROM Warehouse WHERE ItemID = ?";
    $stmtCheck = $conn->prepare($checkWarehouseQuery);
    $stmtCheck->bind_param("i", $itemId);
    $stmtCheck->execute();
    $resultCheck = $stmtCheck->get_result();

    if ($resultCheck->num_rows > 0) {
        // If item exists in Warehouse, update the quantity
        $queryWarehouse = "UPDATE Warehouse SET Quantity = ? WHERE ItemID = ?";
        $stmtWarehouse = $conn->prepare($queryWarehouse);
        $stmtWarehouse->bind_param("ii", $quantity, $itemId);
    } else {
        // If item does not exist, insert a new row
        $queryWarehouse = "INSERT INTO Warehouse (ItemID, Quantity) VALUES (?, ?)";
        $stmtWarehouse = $conn->prepare($queryWarehouse);
        $stmtWarehouse->bind_param("ii", $itemId, $quantity);
    }

    $successWarehouse = $stmtWarehouse->execute();

    if ($successItems && $successWarehouse) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => $conn->error]); // Send DB error message
    }
}

// Delete category
function deleteCategory($conn) {
    $categoryId = $_POST['id'];
    $query = "DELETE FROM Category WHERE CategoryID = ?";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]);
        return;
    }
    $stmt->bind_param("i", $categoryId);
    $success = $stmt->execute();
    if ($success) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => $stmt->error]);
    }
}

// Delete item
function deleteItem($conn) {
    $itemId = $_POST['id'];
    $query = "DELETE FROM Items WHERE ItemID = ?";
    $stmt = $conn->prepare($query);
    if (!$stmt) {
        echo json_encode(['success' => false, 'message' => $conn->error]);
        return;
    }
    $stmt->bind_param("i", $itemId);
    $success = $stmt->execute();
    if ($success) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => $stmt->error]);
    }
}

$conn->close();
?>
