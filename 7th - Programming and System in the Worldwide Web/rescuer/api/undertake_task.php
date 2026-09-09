<?php
if (isset($_SERVER['PATH_INFO'])) {
    $rescuer_id = trim($_SERVER['PATH_INFO'], '/'); // Trim leading and trailing slashes
} else {
    echo json_encode(['error' => 'No rescuer ID provided']);
    return;
}

// Include the database configuration file
include '../../db_config.php';

$data = json_decode(file_get_contents('php://input'), true);

$task_id = $data['task_id'];
$task_type = $data['task_type'];

// check if offer or request
if ($task_type == 'Request') {
    $stmt = $conn->prepare("CALL AssignRequest(?, ?)");
} else {
    $stmt = $conn->prepare("CALL AssignOffer(?, ?)");
}

$stmt->bind_param("ii", $task_id, $rescuer_id);


try {
    $stmt->execute();
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $e->getMessage()]);
    return;
}

// check if error
if ($stmt->error) {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $stmt->error]);
} else {
    echo json_encode(['success' => true, 'message' => 'Task accepted successfully']);
}

$conn->close();
?>