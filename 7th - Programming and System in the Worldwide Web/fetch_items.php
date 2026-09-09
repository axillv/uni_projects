<?php

include 'db_config.php'; // Make sure this script connects to your database

header('Content-Type: application/json');

// Query to get items from the database
$sql = "
    SELECT Name, ItemID, CategoryID
    FROM Items
    ORDER BY Name
    ";
    
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $items = [];
    while ($row = $result->fetch_assoc()) {
        $items[] = [
            'Name' => $row['Name'],
            'ItemID' => $row['ItemID'],
            'CategoryID' => $row['CategoryID']
            
        ];
    }
    echo json_encode($items);
} else {
    echo json_encode([]);
}

$conn->close();
?>
