<?php
$servername = "localhost";
$username = "monitor";
$password = "1234";
$dbname = "srDB";

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
        $sensorTypeString = "srVAC";
        break;
    case 1:
        $sensorTypeString = "srVBat";
        break;
    case 2:
        $sensorTypeString = "srIBat";
        break;
    case 3:
        $sensorTypeString = "srILoad";
        break;
    case 4:
        $sensorTypeString = "sr6V5";
        break;
    case 5:
        $sensorTypeString = "sr12V";
        break;
    case 6:
        $sensorTypeString = "sr13V5";
        break;
    case 7:
        $sensorTypeString = "sr19V5";
        break;
    case 8:
        $sensorTypeString = "sr24V";
        break;
    case 9:
        $sensorTypeString = "sr48V_A";
        break;
    case 10:
        $sensorTypeString = "sr48V_B";
        break;
    case 11:
        $sensorTypeString = "srTemp";
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
$sql = "SELECT TIMESTAMP(dt) AS 'time', " .$sensorTypeString. " AS 'value'" 
    . " FROM srHistory" 
    . " WHERE TIMESTAMP(dt) >= '" .$startDate. "'"
    . " AND TIMESTAMP(dt) <= '" .$endDate. "'";

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
