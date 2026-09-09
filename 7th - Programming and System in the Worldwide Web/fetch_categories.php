<?php

include 'db_config.php'; // Make sure this script connects to your database

header('Content-Type: application/json');

// Query to get items from the database
$sql = "
    SELECT CategoryName, CategoryID
    FROM Category
    ORDER BY CategoryName
    ";
    
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $items = [];
    while ($row = $result->fetch_assoc()) {
        $items[] = [
            'CategoryName' => $row['CategoryName'],
            'CategoryID' => $row['CategoryID']
        ];
    }
    echo json_encode($items);
} else {
    echo json_encode([]);
}

$conn->close();
?>
