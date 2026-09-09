<?php
header('Content-Type: application/json');

// Get the citizen name from the URL
if (isset($_SERVER['PATH_INFO'])) {
    $citizen_id = trim($_SERVER['PATH_INFO'], '/'); // Trim leading and trailing slashes
} else {
    echo json_encode(['success' => false, 'message' => 'No citizen ID provided']);
    exit;
}

// Include the database configuration file
include '../../db_config.php';


// Get the selected offer IDs from the POST request
if (!isset($_POST['requestIDs'])) {
    echo json_encode(['success' => false, 'message' => 'No request IDs provided']);
    exit;
}

$requestIDs = explode(',', $_POST['requestIDs']);

try {
    foreach ($requestIDs as $requestID) {
        // Prepare a statement to check the request status
        $stmt_check = $conn->prepare("SELECT Status FROM Requests WHERE RequestID = ? AND CitizenID = ?");
        $stmt_check->bind_param("ii", $requestID, $citizen_id);
        $stmt_check->execute();
        $result = $stmt_check->get_result();
        $request = $result->fetch_assoc();

        if ($request['Status'] === 'PENDING') {
            // If the status is "pending", proceed with the deletion
            $stmt_delete = $conn->prepare("DELETE FROM Requests WHERE RequestID = ? AND CitizenID = ?");
            $stmt_delete->bind_param("ii", $requestID, $citizen_id);
            $stmt_delete->execute();
        } else {
            echo json_encode(['success' => false, 'message' => "Request ID $requestID cannot be deleted. It is no longer pending."]);
            exit;
        }
    }

    echo json_encode(['success' => true, 'message' => 'Request(s) deleted successfully']);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $e->getMessage()]);
} finally {
    $stmt_check->close();
    $conn->close();
}
