<?php
header('Content-Type: application/json');

// Include the database configuration file
include 'db_config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $inputUsername = $_POST['username'];
    $inputPassword = $_POST['password'];

    // Fetch the User's basic info
    $sql = "SELECT UserID, Password, Role FROM Users WHERE Username = ?";
    $stmt = $conn->prepare($sql);

    if ($stmt === false) {
        die(json_encode(['success' => false, 'message' => 'Database error']));
    }

    $stmt->bind_param('s', $inputUsername);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($userID, $storedPassword, $role);
        $stmt->fetch();

        // Verify password (ideally, this would use password hashing)
        if ($inputPassword === $storedPassword) {
            $idField = '';
            $table = '';
            $specificID = '';

            // Determine the role and retrieve the specific ID (AdminID, RescuerID, CitizenID)
            if ($role === 'Administrator') {
                $sql = "SELECT AdminID FROM Administrator WHERE UserID = ?";
                $table = 'Administrator';
                $idField = 'AdminID';
            } elseif ($role === 'Rescuer') {
                $sql = "SELECT RescuerID FROM Rescuer WHERE UserID = ?";
                $table = 'Rescuer';
                $idField = 'RescuerID';
            } elseif ($role === 'Citizen') {
                $sql = "SELECT CitizenID FROM Citizen WHERE UserID = ?";
                $table = 'Citizen';
                $idField = 'CitizenID';
            }

            // Fetch the specific ID based on the role
            if ($table && $idField) {
                $stmt = $conn->prepare($sql);
                $stmt->bind_param('i', $userID);
                $stmt->execute();
                $stmt->bind_result($specificID);
                $stmt->fetch();

                echo json_encode([
                    'success' => true,
                    'role' => $role,
                    'userID' => $userID,
                    'specificID' => $specificID,  // This could be AdminID, RescuerID, or CitizenID
                ]);
            } else {
                echo json_encode(['success' => false, 'message' => 'Role not recognized.']);
            }
        } else {
            echo json_encode(['success' => false, 'message' => 'Invalid password']);
        }
    } else {
        echo json_encode(['success' => false, 'message' => 'Username not found']);
    }

    $stmt->close();
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method']);
}

$conn->close();
?>
