<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "smartRectifier";

$startDate = $_GET["startDate"];
$endDate = $_GET["endDate"];
$sensorType = $_GET["type"];

if(!isset($startDate) || !isset($endDate) || !isset($sensorType)) {
    echo "[]";
    exit();
}

$sensorTypeString = "";
switch ($sensorType) {
    case 0:
        $sensorTypeString = "sensorVAC";
        break;
    case 1:
        $sensorTypeString = "sensorVBat";
        break;
    case 2:
        $sensorTypeString = "sensorIBat";
        break;
    case 3:
        $sensorTypeString = "sensorILoad";
        break;
    case 4:
        $sensorTypeString = "sensorModem0";
        break;
    case 5:
        $sensorTypeString = "sensorModem1";
        break;
    case 6:
        $sensorTypeString = "sensorModem2";
        break;
    case 7:
        $sensorTypeString = "sensorModem3";
        break;
    case 8:
        $sensorTypeString = "sensorBUC";
        break;
    case 9:
        $sensorTypeString = "sensorSCPC";
        break;
    case 10:
        $sensorTypeString = "sensorSCADA";
        break;
    case 11:
        $sensorTypeString = "sensorTemp";
        break;
    default:
        echo "[]";
        exit();
}

//create DB connection
$conn = new mysqli($servername,$username,$password,$dbname);
//check DB connection
if($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

//Fetch data to DB
$sql = "SELECT TIMESTAMP(tdate, ttime) AS 'time', " .$sensorTypeString. " AS 'value'" 
    . " FROM sensorDataHistory" 
    . " WHERE TIMESTAMP(tdate, ttime) >= '" .$startDate. "'"
    . " AND TIMESTAMP(tdate, ttime) <= '" .$endDate. "'";

$arr = array();
if ($result = mysqli_query($conn, $sql)) {
    /* fetch associative array */
    while ($row = mysqli_fetch_row($result)) {
        array_push($arr,
            array(
                'time' => $row[0],
                'value' => (float)$row[1]
            )
        );
    }

    /* free result set */
    mysqli_free_result($result);
}

echo json_encode($arr);

$conn->close();
?>