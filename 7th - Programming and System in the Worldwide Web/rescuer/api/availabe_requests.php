<?php
header('Content-Type: application/json');

# Include the database configuration file
include '../../db_config.php';

$sql = "
    SELECT 
        req.RequestID, 
        req.CitizenID, 
        req.DateCreated, 
        req.DateAssignedVehicle,
        req.Status,
        cit.Name, 
        cit.Surname, 
        cit.Phone,
        cit.Latitude, 
        cit.Longitude,
        GROUP_CONCAT(reqItems.ItemID) AS ItemIDs,
        GROUP_CONCAT(items.Name SEPARATOR ', ') AS ItemNames,
        GROUP_CONCAT(reqItems.Quantity SEPARATOR ', ') AS ItemQuantities
    FROM Requests req
    JOIN Citizen cit on cit.CitizenID = req.CitizenID
    LEFT JOIN RequestItems reqitems on req.RequestID = reqitems.RequestID
    LEFT JOIN Items on reqitems.ItemID = Items.ItemID
    WHERE req.RescuerID is null
    GROUP BY req.RequestID, 
        req.RequestID, 
        req.CitizenID, 
        req.DateCreated, 
        req.Status,
        cit.Name, 
        cit.Surname, 
        cit.Phone,
        cit.Latitude, 
        cit.Longitude
";

$results = $conn->query($sql);
$requests = [];
$requestOffsets = []; // for unstacking requests from the same citizen

if ($results->num_rows > 0) {
    while ($row = $results->fetch_assoc()) {
        $citizenID = $row['CitizenID'];

        # Increment the offset for this citizen's requests
        if (!isset($requestOffsets[$citizenID])) {
            $requestOffsets[$citizenID] = 0;
        }
        $requestOffsets[$citizenID] += 1;

        // Apply the offset for requests
        $row['Latitude'] += $requestOffsets[$citizenID] * 0.0000608;
        $row['Longitude'] += $requestOffsets[$citizenID] * 0.00006555;

        $requests[] = $row;
    }
}

echo json_encode($requests);
$conn->close();
?>