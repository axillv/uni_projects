<?php
header('Content-Type: application/json');

// Include the database configuration file
include '../db_config.php';

// Function to generate random coordinates within a given radius (5 km in this case)
function getRandomCoordinates($base_latitude, $base_longitude, $radius_km) {
    $radius_in_meters = $radius_km * 1000;

    // Random distance and angle within the radius
    $random_distance = mt_rand() / mt_getrandmax() * $radius_in_meters;
    $random_angle = mt_rand() / mt_getrandmax() * 2 * M_PI;

    // Convert distance and angle to latitude and longitude offsets
    $delta_lat = ($random_distance * cos($random_angle)) / 111320; // approx meters per degree latitude
    $delta_lng = ($random_distance * sin($random_angle)) / (111320 * cos(deg2rad($base_latitude))); // meters per degree longitude

    // New latitude and longitude
    $new_latitude = $base_latitude + $delta_lat;
    $new_longitude = $base_longitude + $delta_lng;

    return array('latitude' => $new_latitude, 'longitude' => $new_longitude);
}

// Retrieve base location from the database
$baseLocationQuery = "SELECT Latitude, Longitude FROM BaseLocation LIMIT 1";
$result = $conn->query($baseLocationQuery);

if ($result->num_rows > 0) {
    $baseLocation = $result->fetch_assoc();
    $base_latitude = $baseLocation['Latitude'];
    $base_longitude = $baseLocation['Longitude'];
} else {
    die(json_encode(['success' => false, 'message' => 'Base location not found']));
}

// Retrieve data from POST request
$username = $_POST['username'];
$password = $_POST['password'];

// First, call the stored procedure to create the rescuer and one vehicle
try {
    // Generate random coordinates for the vehicle within a 5 km radius
    $vehiclePosition = getRandomCoordinates($base_latitude, $base_longitude, 5); 

    // Call the stored procedure to create a new rescuer and a vehicle
    $stmt = $conn->prepare("CALL CreateNewRescuer(?, ?, ?, ?)");
    $stmt->bind_param("ssdd", $username, $password, $vehiclePosition['latitude'], $vehiclePosition['longitude']);
    $stmt->execute();

    echo json_encode(['success' => true, 'message' => 'Rescuer and vehicle created successfully']);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $e->getMessage()]);
} finally {
    $stmt->close();
    $conn->close();
}
