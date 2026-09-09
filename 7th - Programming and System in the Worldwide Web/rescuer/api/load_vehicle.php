<?php
if (isset($_SERVER['PATH_INFO'])) {
    $rescuer_id = trim($_SERVER['PATH_INFO'], '/');
} else {
    echo json_encode(['error' => 'No rescuer ID provided']);
    exit;
}

// Include the database configuration file
include '../../db_config.php';

// Get the JSON input
$data = json_decode(file_get_contents('php://input'), true);

$item_ids = $data['item_ids'];
$item_quantities = $data['item_quantities'];
//convert arrays to strings
$item_ids = implode(',', $item_ids);
$item_quantities = implode(',', $item_quantities);

// Prepare and execute procedure
$sql = "CALL LoadFromWarehouseToVehicle(?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param('iss', $rescuer_id, $item_ids, $item_quantities);

$response = [];

try {
    if ($stmt->execute()) {
        $response['success'] = true;
        $response['message'] = 'Vehicle unloaded successfully';
    } else {
        $response['success'] = false;
        $response['error'] = $stmt->error;
    }
} catch (Exception $e) {
    $response['success'] = false;
    $response['error'] = $e->getMessage();
}

echo json_encode($response);

$stmt->close();
$conn->close();
