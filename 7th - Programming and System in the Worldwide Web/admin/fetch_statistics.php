<?php
include '../db_config.php'; // Ensure your database connection is included

header('Content-Type: application/json');

// Get the start and end dates from the request
$startDate = isset($_POST['startDate']) ? $_POST['startDate'] : null;
$endDate = isset($_POST['endDate']) ? $_POST['endDate'] : null;

// If no startDate or endDate provided, set them to fetch all data
if (empty($startDate) || empty($endDate)) {
    $startDate = '2000-01-01'; // Set a very early date to fetch all records
    $endDate = date('Y-m-d');  // Use today's date as the end date
}

// Query to get requests grouped by week
$queryRequests = "
    SELECT 
        DATE_FORMAT(DATE_SUB(DateCreated, INTERVAL WEEKDAY(DateCreated) DAY), '%Y-%m-%d') AS weekStart,
        DATE_FORMAT(DATE_ADD(DATE_SUB(DateCreated, INTERVAL WEEKDAY(DateCreated) DAY), INTERVAL 6 DAY), '%Y-%m-%d') AS weekEnd,
        SUM(CASE WHEN Status IN ('PENDING', 'INPROGRESS') THEN 1 ELSE 0 END) AS newRequests,
        SUM(CASE WHEN Status = 'FINISHED' THEN 1 ELSE 0 END) AS completedRequests
    FROM Requests
    WHERE DateCreated BETWEEN ? AND ?
    GROUP BY weekStart, weekEnd
    ORDER BY weekStart ASC";

$stmtRequests = $conn->prepare($queryRequests);
$stmtRequests->bind_param('ss', $startDate, $endDate);
$stmtRequests->execute();
$resultRequests = $stmtRequests->get_result();
$dataRequests = $resultRequests->fetch_all(MYSQLI_ASSOC);
$stmtRequests->close();

// Query to get offers grouped by week
$queryOffers = "
    SELECT 
        DATE_FORMAT(DATE_SUB(DateCreated, INTERVAL WEEKDAY(DateCreated) DAY), '%Y-%m-%d') AS weekStart,
        DATE_FORMAT(DATE_ADD(DATE_SUB(DateCreated, INTERVAL WEEKDAY(DateCreated) DAY), INTERVAL 6 DAY), '%Y-%m-%d') AS weekEnd,
        SUM(CASE WHEN Status IN ('PENDING', 'INPROGRESS') THEN 1 ELSE 0 END) AS newOffers,
        SUM(CASE WHEN Status = 'FINISHED' THEN 1 ELSE 0 END) AS completedOffers
    FROM Offers
    WHERE DateCreated BETWEEN ? AND ?
    GROUP BY weekStart, weekEnd
    ORDER BY weekStart ASC";

$stmtOffers = $conn->prepare($queryOffers);
$stmtOffers->bind_param('ss', $startDate, $endDate);
$stmtOffers->execute();
$resultOffers = $stmtOffers->get_result();
$dataOffers = $resultOffers->fetch_all(MYSQLI_ASSOC); // Corrected line
$stmtOffers->close();

$conn->close();

// Merge both datasets into one response
$response = [
    'requests' => $dataRequests,
    'offers' => $dataOffers
];

echo json_encode($response);

?>