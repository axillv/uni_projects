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
if (!isset($_POST['offerIDs'])) {
    echo json_encode(['success' => false, 'message' => 'No offer IDs provided']);
    exit;
}

$offerIDs = explode(',', $_POST['offerIDs']);

try {
    foreach ($offerIDs as $offerID) {
        // Prepare a statement to check the offer status
        $stmt_check = $conn->prepare("SELECT Status FROM Offers WHERE OfferID = ? AND CitizenID = ?");
        $stmt_check->bind_param("ii", $offerID, $citizen_id);
        $stmt_check->execute();
        $result = $stmt_check->get_result();
        $offer = $result->fetch_assoc();

        if ($offer['Status'] === 'PENDING') {
            // If the status is "pending", proceed with the deletion
            $stmt_delete = $conn->prepare("DELETE FROM Offers WHERE OfferID = ? AND CitizenID = ?");
            $stmt_delete->bind_param("ii", $offerID, $citizen_id);
            $stmt_delete->execute();
        } else {
            echo json_encode(['success' => false, 'message' => "Offer ID $offerID cannot be deleted. It is no longer pending."]);
            exit;
        }
    }

    echo json_encode(['success' => true, 'message' => 'Offer(s) deleted successfully']);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Error: ' . $e->getMessage()]);
} finally {
    $stmt_check->close();
    $conn->close();
}
?>
