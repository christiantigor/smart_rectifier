<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "smartRectifier";

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
$sql = "SELECT TIMESTAMP(tdate, ttime) AS 'time',"
    . " sensorVAC AS 'srVAC', sensorVBat AS 'srVBat', sensorIBat AS 'srIBat', sensorILoad AS 'srILoad',"
    . " sensorModem0 AS 'srMdm0', sensorModem1 AS 'srMdm1', sensorModem2 AS 'srMdm2', sensorModem3 AS 'srMdm3',"
    . " sensorSCADA AS 'srSCADA', sensorSCPC AS 'srSCPC', sensorBUC AS 'srBUC', sensorTemp AS 'srTemp'" 
    . " FROM sensorDataHistory" 
    . " WHERE TIMESTAMP(tdate, ttime) >= '" .$startDate. "'"
    . " AND TIMESTAMP(tdate, ttime) <= '" .$endDate. "'";

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