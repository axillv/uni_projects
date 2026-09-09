<?php
header('Content-Type: application/json');

// Include the database configuration file
include '../db_config.php';

// Fetch base location
$base_sql = "
    SELECT BaseName, Latitude, Longitude
    FROM BaseLocation
    LIMIT 1;
";

$base_result = $conn->query($base_sql);
$base_location = $base_result->fetch_assoc();

// Simplified vehicle query with corrected syntax
$vehicles_sql = "
    SELECT 
        v.VehicleID,
        u.Username AS RescuerUsername,
        v.Latitude + 0.0001 AS VehicleLat,
        v.Longitude + 0.0001 AS VehicleLng,
        IFNULL(SUM(vi.Quantity), 0) AS `Load`,
        COUNT(DISTINCT req.RequestID) AS RequestCount,
        COUNT(DISTINCT off.OfferID) AS OfferCount,
        GROUP_CONCAT(DISTINCT req.RequestID) AS AssignedRequests,
        GROUP_CONCAT(DISTINCT off.OfferID) AS AssignedOffers
    FROM Vehicles v
    JOIN Rescuer r ON v.RescuerID = r.RescuerID
    JOIN Users u ON r.UserID = u.UserID
    LEFT JOIN VehicleItems vi ON v.VehicleID = vi.VehicleID
    LEFT JOIN Requests req ON req.RescuerID = r.RescuerID AND req.Status IN ('PENDING', 'INPROGRESS')
    LEFT JOIN Offers off ON off.RescuerID = r.RescuerID AND off.Status IN ('PENDING', 'INPROGRESS')
    GROUP BY v.VehicleID, u.Username, v.Latitude, v.Longitude;
";

$vehicles_result = $conn->query($vehicles_sql);
$vehicles = [];
if ($vehicles_result->num_rows > 0) {
    while ($row = $vehicles_result->fetch_assoc()) {
        // Calculate the status based on the RequestCount and OfferCount
        $row['Status'] = ($row['RequestCount'] > 0 || $row['OfferCount'] > 0) ? 'Ενεργό' : 'Ανενεργό';

        // Calculate the total number of active tasks
        $row['ActiveTasks'] = $row['RequestCount'] + $row['OfferCount'];

        // Add the vehicle data to the array
        $vehicles[] = $row;
    }
}

// Initialize counters for requests and offers
$requestOffsets = [];
$offerOffsets = [];

// Fetch requests excluding 'FINISHED'
$requests_sql = "
    SELECT 
        req.RequestID,
        req.RescuerID,
        c.CitizenID,
        c.Name,
        c.Phone,
        req.Status,
        req.DateCreated,
        req.DateAssignedVehicle,
        u.Username AS RescuerUsername,
        v.VehicleID AS AssignedVehicleID,
        c.Latitude AS RequestLat,
        c.Longitude AS RequestLng,
        GROUP_CONCAT(ri.ItemID) AS ItemIDs,
        GROUP_CONCAT(i.Name SEPARATOR ', ') AS ItemNames,
        GROUP_CONCAT(ri.Quantity SEPARATOR ', ') AS ItemQuantities
    FROM Requests req
    JOIN Citizen c ON req.CitizenID = c.CitizenID
    LEFT JOIN Rescuer r ON req.RescuerID = r.RescuerID
    LEFT JOIN Users u ON r.UserID = u.UserID
    LEFT JOIN RequestItems ri ON req.RequestID = ri.RequestID
    LEFT JOIN Items i ON ri.ItemID = i.ItemID
    LEFT JOIN Vehicles v ON r.RescuerID = v.RescuerID
    WHERE req.Status IN ('PENDING', 'INPROGRESS')
    GROUP BY req.RequestID, req.RescuerID, c.CitizenID, c.Name, c.Phone, req.Status, req.DateCreated, req.DateAssignedVehicle, u.Username, v.VehicleID, c.Latitude, c.Longitude;
";

$requests_result = $conn->query($requests_sql);
$requests = [];
if ($requests_result->num_rows > 0) {
    while ($row = $requests_result->fetch_assoc()) {
        $citizenID = $row['CitizenID'];

        // Increment the offset for this citizen's requests
        if (!isset($requestOffsets[$citizenID])) {
            $requestOffsets[$citizenID] = 0;
        }
        $requestOffsets[$citizenID] += 1;

        // Apply the offset for requests
        $row['RequestLat'] += $requestOffsets[$citizenID] * 0.0000608;
        $row['RequestLng'] += $requestOffsets[$citizenID] * 0.00006555;

        $requests[] = $row;
    }
}

// Fetch offers excluding 'FINISHED'
$offers_sql = "
    SELECT 
        off.OfferID,
        off.RescuerID,
        c.CitizenID,
        c.Name,
        c.Phone,
        off.Status,
        off.DateCreated,
        off.DateAssignedVehicle,
        u.Username AS RescuerUsername,
        v.VehicleID AS AssignedVehicleID,
        c.Latitude AS OfferLat,
        c.Longitude AS OfferLng,
        GROUP_CONCAT(oi.ItemID) AS ItemIDs,
        GROUP_CONCAT(i.Name SEPARATOR ', ') AS ItemNames,
        GROUP_CONCAT(oi.Quantity SEPARATOR ', ') AS ItemQuantities
    FROM Offers off
    JOIN Citizen c ON off.CitizenID = c.CitizenID
    LEFT JOIN Rescuer r ON off.RescuerID = r.RescuerID
    LEFT JOIN Users u ON r.UserID = u.UserID
    LEFT JOIN OfferItems oi ON off.OfferID = oi.OfferID
    LEFT JOIN Items i ON oi.ItemID = i.ItemID
    LEFT JOIN Vehicles v ON r.RescuerID = v.RescuerID
    WHERE off.Status IN ('PENDING', 'INPROGRESS')
    GROUP BY off.OfferID, off.RescuerID, c.CitizenID, c.Name, c.Phone, off.Status, off.DateCreated, off.DateAssignedVehicle, u.Username, v.VehicleID, c.Latitude, c.Longitude;
";

$offers_result = $conn->query($offers_sql);
$offers = [];
if ($offers_result->num_rows > 0) {
    while ($row = $offers_result->fetch_assoc()) {
        $citizenID = $row['CitizenID'];

        // Increment the offset for this citizen's offers
        if (!isset($offerOffsets[$citizenID])) {
            $offerOffsets[$citizenID] = 0;
        }
        $offerOffsets[$citizenID] += 1;

        // Apply the offset for offers
        $row['OfferLat'] += $offerOffsets[$citizenID] * 0.0000678;
        $row['OfferLng'] += $offerOffsets[$citizenID] * 0.0000570;

        $offers[] = $row;
    }
}

// Combine all data into one response
$response = [
    'base' => $base_location,
    'vehicles' => $vehicles,
    'requests' => $requests,
    'offers' => $offers,
];

echo json_encode($response);
$conn->close();
?>
