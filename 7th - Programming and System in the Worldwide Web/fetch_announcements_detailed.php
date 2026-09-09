<?php
header('Content-Type: application/json');

// Include the database configuration file
include 'db_config.php';

$sql = "
    SELECT
        announce.AnnouncementID,
        announce.DateCreated,
        annitems.ItemID,
        annitems.Quantity,
        items.Name,
        items.DetailName,
        items.DetailValue,
        cat.CategoryName

    FROM Announcements announce
    LEFT JOIN AnnouncementItems annitems ON announce.AnnouncementID = annitems.AnnouncementID
    LEFT JOIN Items items ON annitems.ItemID = items.ItemID
    LEFT JOIN Category cat ON items.CategoryID = cat.CategoryID
    ";

$result = $conn->query($sql);
$items = [];
if ($result->num_rows > 0){
    while ($row = $result->fetch_assoc()) {
        $items[] = [
            'AnnouncementID' => $row['AnnouncementID'],
            'DateCreated' => $row['DateCreated'],
            'ItemID' => $row['ItemID'],
            'Quantity' => $row['Quantity'],
            'Name' => $row['Name'],
            'DetailName' => $row['DetailName'],
            'DetailValue' => $row['DetailValue'],
            'CategoryName' => $row['CategoryName']
        ];
    }
}
$conn->close();
echo json_encode($items);

?>
