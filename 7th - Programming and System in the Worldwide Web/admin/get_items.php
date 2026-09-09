<?php

include '../db_config.php'; // Make sure this script connects to your database

header('Content-Type: application/json');

// Query to get items from the database
$query = "SELECT ItemID, Name FROM Items";
$result = $conn->query($query);

if ($result->num_rows > 0) {
    $items = array();
    while ($row = $result->fetch_assoc()) {
        $items[] = $row;
    }
    echo json_encode($items);
} else {
    echo json_encode([]);
}

$conn->close();
?>
