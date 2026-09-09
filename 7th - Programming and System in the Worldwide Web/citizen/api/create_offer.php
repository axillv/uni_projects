<?php
header('Content-Type: application/json');

// Get the citizen name from the URL
if (isset($_SERVER['PATH_INFO'])) {
    $citizen_id = trim($_SERVER['PATH_INFO'], '/'); // Trim leading and trailing slashes
} else {
    echo json_encode(['error' => 'No citizen ID provided']);
}

// Include the database configuration file
include '../../db_config.php';

$items = rtrim($_POST['items']);
$quantities = rtrim($_POST['quantities']);

// Call the stored procedure
try {
    // Call the stored procedure to create a new rescuer and a vehicle
    $stmt = $conn->prepare("CALL CreateNewOffer(?, ?, ?)");
    $stmt->bind_param("iss", $citizen_id, $items, $quantities);
    $stmt->execute();

    echo json_encode(['success' => true, 'message' => 'Request created succesfuly']);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $e->getMessage()]);
} finally {
    $stmt->close();
    $conn->close();
}

?>