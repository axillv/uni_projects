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


$sql = "
    SELECT
        off.OfferID,
        items.Name,
        cat.CategoryName,
        offitems.Quantity,
        off.DateCreated,
        IFNULL(off.DateAssignedVehicle, '-') DateAssignedVehicle,
        IFNULL(off.DateFinished, '-') DateFinished
    FROM Offers off
    LEFT JOIN OfferItems offitems ON off.OfferID = offitems.OfferID
    INNER JOIN Items items ON offitems.ItemID = items.ItemID
    LEFT JOIN Category cat ON items.CategoryID = cat.CategoryID
    LEFT JOIN Citizen cit ON off.CitizenID = cit.CitizenID
    WHERE cit.CitizenID = $citizen_id";

$result = $conn->query($sql);
$items = [];
if ($result->num_rows > 0){
    while ($row = $result->fetch_assoc()) {
        $items[] = [
            'OfferID' => $row['OfferID'],
            'Name' => $row['Name'],
            'CategoryName' => $row['CategoryName'],
            'Quantity' => $row['Quantity'],
            'DateCreated' => $row['DateCreated'],
            'DateAssignedVehicle' => $row['DateAssignedVehicle'],
            'DateFinished' => $row['DateFinished']
        ];
    }
}
$conn->close();
echo json_encode($items);

?>
