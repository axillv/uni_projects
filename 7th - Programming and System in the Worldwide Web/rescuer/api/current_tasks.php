<?php
header('Content-Type: application/json');

// Get the citizen name from the URL
if (isset($_SERVER['PATH_INFO'])) {
    $rescuer_id = trim($_SERVER['PATH_INFO'], '/'); // Trim leading and trailing slashes
} else {
    echo json_encode(['error' => 'No rescuer ID provided']);
    return;
}

// Include the database configuration file
include '../../db_config.php';

$offers_sql = "
        SELECT 
        'Offer' AS Type,
        off.OfferID ID, 
        off.CitizenID CitizenID, 
        off.DateCreated DateCreated, 
        off.DateAssignedVehicle DateAssignedVehicle,
        off.Status `Status`,
        cit.Name as Name, 
        cit.Surname Surname,  
        cit.Phone Phone,
        cit.Latitude Latitude, 
        cit.Longitude Longitude,
        GROUP_CONCAT(offitems.ItemID) AS ItemIDs,
        GROUP_CONCAT(items.Name SEPARATOR ', ') AS ItemNames,
        GROUP_CONCAT(offitems.Quantity SEPARATOR ', ') AS ItemQuantities
    FROM Offers off
    JOIN Citizen cit on cit.CitizenID = off.CitizenID
    LEFT JOIN OfferItems offitems on off.OfferID = offitems.OfferID
    LEFT JOIN Items on offitems.ItemID = Items.ItemID
    WHERE off.RescuerID = $rescuer_id and off.Status != 'Finished'
    GROUP BY 
        off.OfferID, 
        off.CitizenID, 
        off.DateCreated, 
        off.Status,
        cit.Name, 
        cit.Surname, 
        cit.Phone,
        cit.Latitude, 
        cit.Longitude

";

$offers_result = $conn->query($offers_sql);
$offers = [];
$offerOffsets = []; // for unstacking offers from the same citizen

if ($offers_result->num_rows > 0) {
    while ($row = $offers_result->fetch_assoc()) {
        $citizenID = $row['CitizenID'];

        // Increment the offset for this citizen's offers
        if (!isset($offerOffsets[$citizenID])) {
            $offerOffsets[$citizenID] = 0;
        }
        $offerOffsets[$citizenID] += 1;

        // Apply the offset for offers
        $row['Latitude'] += $offerOffsets[$citizenID] * 0.0000678;
        $row['Longitude'] += $offerOffsets[$citizenID] * 0.0000570;

        $offers[] = $row;
    }
}


$requests_sql = "
    SELECT 
        'Request' AS Type,
        req.RequestID ID,
        req.CitizenID CitizenID,
        req.DateCreated DateCreated,
        req.DateAssignedVehicle DateAssignedVehicle,
        req.Status `Status`,
        cit.Name AS Name,
        cit.Surname Surname,
        cit.Phone Phone,
        cit.Latitude Latitude,
        cit.Longitude Longitude,
        GROUP_CONCAT(reqItems.ItemID) AS ItemIDs,
        GROUP_CONCAT(items.Name SEPARATOR ', ') AS ItemNames,
        GROUP_CONCAT(reqItems.Quantity SEPARATOR ', ') AS ItemQuantities
    FROM Requests req
    JOIN Citizen cit on cit.CitizenID = req.CitizenID
    LEFT JOIN RequestItems reqitems on req.RequestID = reqitems.RequestID
    LEFT JOIN Items on reqitems.ItemID = Items.ItemID
    WHERE req.RescuerID = $rescuer_id and req.Status != 'Finished'
    GROUP BY req.RequestID, 
        req.RequestID, 
        req.CitizenID, 
        req.DateCreated, 
        req.DateAssignedVehicle,
        req.Status,
        cit.Name, 
        cit.Surname, 
        cit.Phone,
        cit.Latitude, 
        cit.Longitude
";

$requests_result = $conn->query($requests_sql);
$requests = [];
$requestOffsets = []; // for unstacking requests from the same citizen

if ($requests_result->num_rows > 0) {
    while ($row = $requests_result->fetch_assoc()) {
        $citizenID = $row['CitizenID'];

        // Increment the offset for this citizen's requests
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

$tasks = [
    'Offers' => $offers,
    'Requests' => $requests
];

echo json_encode($tasks);
$conn->close();
?>