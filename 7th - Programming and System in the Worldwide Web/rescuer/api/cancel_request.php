<?php
// Include the database connection
include '../../db_config.php';

// Get the POST data
$data = json_decode(file_get_contents("php://input"), true);
$task_id = $data['task_id'];
//send id as front error


// Check if task ID is provided
if (empty($task_id)) {
    echo json_encode(['error' => 'No task ID provided.']);
    exit;
}

// Prepare the SQL statement to call the CancelRequest procedure
$stmt = $conn->prepare("CALL CancelRequest(?)");
$stmt->bind_param("i", $task_id);

// Execute the query and return the result
if ($stmt->execute()) {
    echo json_encode(['message' => 'Request canceled successfully.']);
} else {
    echo json_encode(['error' => 'Failed to cancel request.']);
}

// Close the statement and connection
$stmt->close();
$conn->close();
?>
