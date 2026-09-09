<?php

// get id from url
if (isset($_SERVER['PATH_INFO'])) {
    $rescuer_id = trim($_SERVER['PATH_INFO'], '/');
} else {
    echo json_encode(['error' => 'No rescuer ID provided']);
}

// Include the database configuration file
include '../../db_config.php';

// Get the JSON input
$data = json_decode(file_get_contents('php://input'), true);

$latitude = $data['latitude'];
$longitude = $data['longitude'];

// Prepare and execute the update statement
$sql = "UPDATE Vehicles SET Latitude = ?, Longitude = ? WHERE RescuerID = $rescuer_id"; 
// Assuming there's only one vehicle

$stmt = $conn->prepare($sql);
$stmt->bind_param('dd', $latitude, $longitude);

$response = [];

if ($stmt->execute()) {
    $response['success'] = true;
    $response['message'] = 'Base location updated successfully';
} else {
    $response['success'] = false;
    $response['error'] = $stmt->error;
}

echo json_encode($response);

$conn->close();
?>
