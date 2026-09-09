<?php
header('Content-Type: application/json');

// Include the database configuration file
include '../db_config.php'; // Use the existing $conn variable from db_config.php

// Ensure the correct charset
mysqli_set_charset($conn, "utf8mb4");

// Check if the connection is valid
if (!$conn) {
    die(json_encode(['error' => 'Database connection failed: ' . mysqli_connect_error()]));
}

// Your SQL query remains unchanged
$query = "
    SELECT 
        c.CategoryName AS Category, 
        i.Name, 
        i.DetailName, 
        i.DetailValue, 
        COALESCE(SUM(w.Quantity), 0) AS Quantity, 
        'In Warehouse' AS Location, 
        w.ItemID 
    FROM Warehouse w 
    LEFT JOIN Items i ON w.ItemID = i.ItemID 
    LEFT JOIN Category c ON i.CategoryID = c.CategoryID 
    GROUP BY w.ItemID, c.CategoryName, i.Name, i.DetailName, i.DetailValue

    UNION

    SELECT 
        c.CategoryName AS Category, 
        i.Name, 
        i.DetailName, 
        i.DetailValue, 
        COALESCE(SUM(vi.Quantity), 0) AS Quantity, 
        CONCAT('On Vehicle (', u.Username, ')') AS Location, 
        vi.ItemID 
    FROM VehicleItems vi 
    LEFT JOIN Items i ON vi.ItemID = i.ItemID 
    LEFT JOIN Category c ON i.CategoryID = c.CategoryID 
    LEFT JOIN Vehicles v ON vi.VehicleID = v.VehicleID 
    LEFT JOIN Rescuer r ON v.RescuerID = r.RescuerID 
    LEFT JOIN Users u ON r.UserID = u.UserID
    GROUP BY vi.ItemID, c.CategoryName, i.Name, i.DetailName, i.DetailValue, u.Username;
";

$result = mysqli_query($conn, $query); // Use $conn from db_config.php

if (!$result) {
    die(json_encode(['error' => 'Query failed: ' . mysqli_error($conn)]));
}

$items = [];

// Fetch data from query and format it as an associative array
while ($row = mysqli_fetch_assoc($result)) {
    $items[] = [
        'Category' => $row['Category'],
        'Name' => $row['Name'],
        'DetailName' => $row['DetailName'],
        'DetailValue' => $row['DetailValue'],
        'Quantity' => $row['Quantity'],
        'Location' => $row['Location'],
        'ItemID' => $row['ItemID']
    ];
}

// Output the JSON-encoded result
echo json_encode($items);
?>
