<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

header('Content-Type: application/json');

// Include the database configuration file
include 'db_config.php';


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputUsername = $_POST['username'];
    $inputPassword = $_POST['password'];
    $firstName = $_POST['firstName'];
    $lastName = $_POST['lastName'];
    $phoneNumber = $_POST['phoneNumber'];
    $latitude = isset($_POST['latitude']) ? $_POST['latitude'] : null;
    $longitude = isset($_POST['longitude']) ? $_POST['longitude'] : null;


    $stmt = $conn->prepare("CALL CreateNewCitizen(?, ?, ?, ?, ?, ?, ?)");
    if ($stmt === false) {
        die(json_encode(['success' => false, 'message' => 'Prepare failed: ' . $conn->error]));
    }

    $stmt->bind_param('sssssss', $inputUsername, $inputPassword, $firstName, $lastName, $phoneNumber, $latitude, $longitude);

    if ($stmt->execute()) {
        echo json_encode(['success' => true, 'message' => 'User registered successfully']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Execute failed: ' . $stmt->error]);
    }

    $stmt->close();
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}

$conn->close();
?>
