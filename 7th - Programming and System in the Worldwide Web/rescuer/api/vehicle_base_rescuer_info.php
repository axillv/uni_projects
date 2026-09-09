<?php
// Get the rescuer ID from the URL
if (isset($_SERVER['PATH_INFO'])) {
    $rescuer_id = trim($_SERVER['PATH_INFO'], '/'); // Trim leading and trailing slashes
} else {
    echo json_encode(['error' => 'No rescuer ID provided']);
    return;
}

include '../../db_config.php';

// Fetch base location
$base_sql = "
    SELECT BaseName, Latitude, Longitude
    FROM BaseLocation
    LIMIT 1;
";

$base_result = $conn->query($base_sql);
$base_location = $base_result->fetch_assoc();

$vehicle_sql = "
    SELECT 
        Latitude + 0.0001 AS Latitude,
        Longitude + 0.0001 AS Longitude
    FROM Vehicles
    WHERE RescuerID = $rescuer_id
";

// Fetch rescuer username
$rescuer_sql = "
    SELECT Users.Username Username
    FROM Rescuer
    LEFT JOIN Users ON Rescuer.UserID = Users.UserID
    WHERE RescuerID = $rescuer_id
";

$rescuer_result = $conn->query($rescuer_sql);
$rescuer_name = $rescuer_result->fetch_assoc();

// assume single vehicle!

$vehicle_result = $conn->query($vehicle_sql);
$vehicle_location = $vehicle_result->fetch_assoc();

$vehicle_base_info = [
    'Base' => $base_location,
    'Vehicle' => $vehicle_location,
    'Rescuer' => $rescuer_name
];

echo json_encode($vehicle_base_info);
$conn->close();
?>