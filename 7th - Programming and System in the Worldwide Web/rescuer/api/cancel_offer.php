<?php
// Connect to the database
include 'db_connect.php';  // Adjust the path to your DB connection file

// Get the POST data
$data = json_decode(file_get_contents("php://input"), true);
$task_id = $data['task_id'];

// Call the stored procedure to cancel the request
$stmt = $conn->prepare("CALL CancelRequest(?)");
$stmt->bind_param("i", $task_id);

if ($stmt->execute()) {
    echo json_encode(['message' => 'Request canceled successfully.']);
} else {
    echo json_encode(['error' => 'Failed to cancel request.']);
}

$stmt->close();
$conn->close();
?>
