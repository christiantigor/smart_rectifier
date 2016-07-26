<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "srDB";

$startDate = $_GET["startDate"];
$endDate = $_GET["endDate"];

if(!isset($startDate) || !isset($endDate)) {
    echo "";
    exit();
}

//create DB connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check DB connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Fetch data to DB
$sql = "SELECT TIMESTAMP(dt) AS 'time',"
    . " srVAC AS 'srVAC', srVBat AS 'srVBat', srIBat AS 'srIBat', srILoad AS 'srILoad',"
    . " sr6V5 AS 'sr6V5', sr12V AS 'sr12V', sr13V5 AS 'sr13V5', sr19V5 AS 'sr19V5',"
    . " sr24V AS 'sr24V', sr48V_A AS 'sr48V_A', sr48V_B AS 'sr48V_B', srTemp AS 'srTemp'" 
    . " FROM srHistory" 
    . " WHERE TIMESTAMP(dt) >= '" .$startDate. "'"
    . " AND TIMESTAMP(dt) <= '" .$endDate. "'";

$result = mysqli_query($conn, $sql);
$num_fields = mysqli_num_fields($result); 
$headers = array(); 
while ($property = mysqli_fetch_field($result)) {
    array_push($headers, $property->name);
}

$fp = fopen('php://output', 'w'); 
if ($fp && $result) 
{     
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="export.csv"');
    header('Pragma: no-cache');
    header('Expires: 0');
    fputcsv($fp, $headers); 
    while ($row = mysqli_fetch_row($result))
    {
        fputcsv($fp, array_values($row)); 
    }
    $conn->close();
    die; 
} else {
    $conn->close();
    echo "";
    exit();
}

?>
