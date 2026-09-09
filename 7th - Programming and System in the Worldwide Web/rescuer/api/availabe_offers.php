<?php
header('Content-Type: application/json');

# Include the database configuration file
include '../../db_config.php';

$sql = "
        SELECT 
        off.OfferID, 
        off.CitizenID, 
        off.DateCreated, 
        off.DateAssignedVehicle,
        off.Status,
        cit.Name, 
        cit.Surname, 
        cit.Phone,
        cit.Latitude, 
        cit.Longitude,
        GROUP_CONCAT(offitems.ItemID) AS ItemIDs,
        GROUP_CONCAT(items.Name SEPARATOR ', ') AS ItemNames,
        GROUP_CONCAT(offitems.Quantity SEPARATOR ', ') AS ItemQuantities
    FROM Offers off
    JOIN Citizen cit on cit.CitizenID = off.CitizenID
    LEFT JOIN OfferItems offitems on off.OfferID = offitems.OfferID
    LEFT JOIN Items on offitems.ItemID = Items.ItemID
    WHERE off.RescuerID is null
    GROUP BY off.OfferID, 
        off.CitizenID, 
        off.DateCreated, 
        off.Status,
        cit.Name, 
        cit.Surname, 
        cit.Phone,
        cit.Latitude, 
        cit.Longitude

";

$results = $conn->query($sql);
$offers = [];
$offerOffsets = []; // for unstacking offers from the same citizen

if ($results->num_rows > 0) {
    while ($row = $results->fetch_assoc()) {
        $citizenID = $row['CitizenID'];

        # Increment the offset for this citizen's offers
        if (!isset($offerOffsets[$citizenID])) {
            $offerOffsets[$citizenID] = 0;
        }
        $offerOffsets[$citizenID] += 1;

        # Apply the offset for offers
        $row['Latitude'] += $offerOffsets[$citizenID] * 0.0000678;
        $row['Longitude'] += $offerOffsets[$citizenID] * 0.0000570;

        $offers[] = $row;
    }
}

echo json_encode($offers);
$conn->close();
?>
