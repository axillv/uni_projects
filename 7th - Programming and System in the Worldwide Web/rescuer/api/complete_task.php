<?php
// Include the database connection
include '../../db_config.php';  // Adjust this to your actual DB connection file

// Get the POST data
$data = json_decode(file_get_contents("php://input"), true);
$task_id = $data['task_id'];
$task_type = $data['task_type'];
$rescuer_id = $data['rescuer_id'];  // Assuming you are passing the rescuer ID from the frontend

// Check if task ID, task type, and rescuer ID are provided
if (empty($task_id) || empty($task_type) || empty($rescuer_id)) {
    echo json_encode(['error' => 'Task ID, Task Type, or Rescuer ID not provided.']);
    exit;
}

try {
    // Begin transaction
    $conn->begin_transaction();

    // Handle Offer Completion
    if ($task_type === 'Offer') {
        // Call the stored procedure for loading the vehicle from the offer
        $stmt = $conn->prepare("CALL LoadVehicleFromOffer(?, ?)");
        $stmt->bind_param("ii", $task_id, $rescuer_id);
        if (!$stmt->execute()) {
            throw new Exception($stmt->error);
        }

        // After loading the vehicle, mark the offer as finished
        $stmt_finish = $conn->prepare("CALL FinishOffer(?)");
        $stmt_finish->bind_param("i", $task_id);
        if (!$stmt_finish->execute()) {
            throw new Exception($stmt_finish->error);
        }

    } 
    // Handle Request Completion
    else if ($task_type === 'Request') {
        // Call the stored procedure for unloading the vehicle on request completion
        $stmt = $conn->prepare("CALL UnloadVehicleOnRequestCompletion(?, ?)");
        $stmt->bind_param("ii", $rescuer_id, $task_id);
        if (!$stmt->execute()) {
            throw new Exception($stmt->error);
        }

        // After unloading the vehicle, mark the request as finished
        $stmt_finish = $conn->prepare("CALL FinishRequest(?)");
        $stmt_finish->bind_param("i", $task_id);
        if (!$stmt_finish->execute()) {
            throw new Exception($stmt_finish->error);
        }
    } 
    else {
        throw new Exception('Invalid task type provided.');
    }

    // Commit transaction
    $conn->commit();

    // Respond with success message
    echo json_encode(['message' => 'Task completed successfully.']);

} catch (Exception $e) {
    // Rollback transaction on error
    $conn->rollback();
    
    // Return the error message to the frontend
    echo json_encode(['error' => $e->getMessage()]);
}

// Close the statement and connection
$stmt->close();
if (isset($stmt_finish)) {
    $stmt_finish->close();
}
$conn->close();
?>
