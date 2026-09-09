<?php
// Include the database connection
include '../../db_config.php';  // Adjust this to your actual DB connection file


try {
    // Prepare the query to fetch all warehouse items
    $stmt = $conn->prepare("
        SELECT i.ItemID, i.Name, i.DetailName, i.DetailValue, w.Quantity, c.CategoryName
        FROM Warehouse w
        JOIN Items i ON w.ItemID = i.ItemID
        JOIN Category c ON i.CategoryID = c.CategoryID
    ");

    // Execute the query
    $stmt->execute();
    $result = $stmt->get_result();

    // Fetch data
    $warehouse_items = [];
    while ($row = $result->fetch_assoc()) {
        $warehouse_items[] = $row;
    }

    // Return the data as JSON
    echo json_encode(['data' => $warehouse_items]);

} catch (Exception $e) {
    // Handle exceptions and return an error
    echo json_encode(['error' => $e->getMessage()]);
}

// Close the statement and connection
$stmt->close();
$conn->close();
?>
